"""
pipeline.py
Serving glue between the FastAPI layer and the trained HemoSense Phase 2/3 code.

Reuses (does not re-implement) modules from ../scratch:
  - anemia_pipeline: extract_conjunctiva_roi / apply_fuzzy_correction / calculate_erythema_index
  - evaluate:        hb_to_severity  (bins identical to the training labels)

The heavy dependencies (tensorflow, opencv, scikit-fuzzy) are imported lazily so
the app can still boot on machines that only have the web deps installed; any
screen endpoint then fails fast with a clean 503 and a human-readable reason.
"""

import json
import os
import time
from typing import Optional

from api import config

# ---------------------------------------------------------------------------
# Availability state (populated once at startup by main lifespan)
# ---------------------------------------------------------------------------
_state = {
    "model": None,
    "loaded": False,
    "reason": None,
    "name": None,
    "loaded_at": None,
}


class PipelineUnavailableError(Exception):
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


def _why_missing(stage: str, exc: Exception) -> str:
    return f"CNN unavailable: {stage} failed ({type(exc).__name__}: {exc}). " \
           "Run the API in the project environment (Python 3.11/3.12, " \
           "tensorflow<2.17, opencv-python, scikit-fuzzy)."


def load_pipeline():
    """Called once from the FastAPI lifespan. Loads the trained .keras model."""
    _state["loaded"] = False
    _state["reason"] = None
    _state["name"] = None

    if not os.path.exists(config.MODEL_PATH):
        _state["reason"] = (
            f"Model file not found: {config.MODEL_PATH}. "
            "Set HEMOSENSE_MODEL_PATH to a trained .keras file."
        )
        return _state

    try:
        import tensorflow as tf  # noqa: F401
    except Exception as exc:  # noqa: BLE001
        _state["reason"] = _why_missing("importing tensorflow", exc)
        return _state

    from evaluate import hb_to_severity  # noqa: F401  (validate scratch import chain)
    import anemia_pipeline  # noqa: F401  (validates cv2 + skfuzzy)

    try:
        model = tf.keras.models.load_model(config.MODEL_PATH)
        _ = model(tf.zeros((1, 224, 224, 3)))  # warm-up (builds the graph)
    except Exception as exc:  # noqa: BLE001
        _state["reason"] = _why_missing("loading the model", exc)
        return _state

    _state["model"] = model
    _state["loaded"] = True
    _state["name"] = os.path.splitext(os.path.basename(config.MODEL_PATH))[0]
    _state["loaded_at"] = time.time()
    return _state


def get_state() -> dict:
    return dict(_state)


# ---------------------------------------------------------------------------
# Metrics for /health (read from the saved run JSONs, no recomputation)
# ---------------------------------------------------------------------------
def load_metrics() -> dict:
    if not os.path.exists(config.META_PATH):
        return {"note": f"meta file not found: {config.META_PATH}"}
    with open(config.META_PATH, encoding="utf-8") as f:
        meta = json.load(f)
    keep = {
        "run_name": meta.get("run_name"),
        "variant": meta.get("variant"),
        "head": meta.get("head"),
        "lr": meta.get("lr"),
        "epochs_ran": meta.get("epochs_ran"),
        "config": {
            "dropout": meta.get("dropout"),
            "dense_units": meta.get("dense_units"),
            "aug_strength": meta.get("aug_strength"),
        },
        "test_metrics": meta.get("test_metrics"),
    }
    return keep


# ---------------------------------------------------------------------------
# Image decode
# ---------------------------------------------------------------------------
def _decode_rgb_and_bgr(img_bytes: bytes):
    """Returns (rgb_np, bgr_np) from raw upload bytes. Raises on undecodable input."""
    import cv2
    import numpy as np

    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if bgr is None or bgr.size == 0:
        raise ValueError("Could not decode the uploaded image as a color image.")
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return rgb, bgr


def _preprocess_like_training(rgb_np):
    """Matches data_loader._decode_and_resize: resize 224x224, cast float32, /255.
       The keras model's first layer then applies Rescaling(255.0) + EfficientNet
       preprocess_input, exactly as during training."""
    import tensorflow as tf

    t = tf.convert_to_tensor(rgb_np, dtype=tf.uint8)
    t = tf.image.resize(t, (224, 224))
    t = tf.cast(t, tf.float32) / 255.0
    return tf.expand_dims(t, axis=0)


# ---------------------------------------------------------------------------
# Screening
# ---------------------------------------------------------------------------
def _roi_thumbnail_b64(bgr_img, max_side: int = 192) -> Optional[str]:
    """Small PNG data-URL of a BGR image, for UI crop verification."""
    import base64
    import cv2

    h, w = bgr_img.shape[:2]
    scale = min(1.0, max_side / max(h, w))
    if scale < 1.0:
        bgr_img = cv2.resize(bgr_img, (max(1, int(w * scale)), max(1, int(h * scale))),
                             interpolation=cv2.INTER_AREA)
    ok, buf = cv2.imencode(".png", bgr_img)
    if not ok:
        return None
    return "data:image/png;base64," + base64.b64encode(buf.tobytes()).decode("ascii")


def screen_image_bytes(img_bytes: bytes, include_roi: bool = False):
    """Full inference path for POST /screen. Returns a response dict.
    include_roi adds a small fuzzy-corrected ROI thumbnail (`roi_thumbnail`)."""
    if not _state["loaded"]:
        raise PipelineUnavailableError(_state["reason"] or "CNN not loaded.")

    import numpy as np
    from anemia_pipeline import (apply_fuzzy_correction, calculate_erythema_index,
                                 extract_conjunctiva_roi)
    from evaluate import hb_to_severity

    t0 = time.time()

    rgb, bgr = _decode_rgb_and_bgr(img_bytes)

    roi = extract_conjunctiva_roi(bgr)
    roi_note = None

    corrected = apply_fuzzy_correction(roi)

    try:
        ei_raw = float(calculate_erythema_index(roi))
    except Exception:  # noqa: BLE001
        ei_raw = None
    try:
        ei_corrected = float(calculate_erythema_index(corrected))
    except Exception:  # noqa: BLE001
        ei_corrected = None

    # Convert the (possibly BGR) ROI to RGB for the CNN — training fed RGB.
    try:
        import cv2
        roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    except Exception:  # noqa: BLE001
        roi_rgb = roi

    x = _preprocess_like_training(roi_rgb)
    pred = np.asarray(_state["model"].predict(x, verbose=0), dtype=np.float64).reshape(-1)[0]
    hb = float(round(pred, 2))

    severity = str(hb_to_severity(np.asarray([pred]))[0])
    anemic = bool(pred <= 12.0)  # consistent with evaluate.ANEMIA_THRESHOLD

    result = {
        "predicted_hb_gdl": hb,
        "severity_class": severity,
        "anemic": anemic,
        "erythema_index": {"raw": ei_raw, "corrected": ei_corrected},
        "roi": {"detected": roi is not None and roi.size > 0, "note": roi_note},
        "processing_ms": round((time.time() - t0) * 1000, 1),
        "model": _state["name"],
    }
    if include_roi:
        try:
            result["roi_thumbnail"] = _roi_thumbnail_b64(corrected)
        except Exception:  # noqa: BLE001
            result["roi_thumbnail"] = None
    return result


# ---------------------------------------------------------------------------
# ROI debug images (POST /screen/roi)
# ---------------------------------------------------------------------------
def roi_images_b64(img_bytes: bytes):
    """Returns {roi_raw, roi_corrected} as base64 PNG data-URLs."""
    import base64

    try:
        import cv2
        from anemia_pipeline import apply_fuzzy_correction, extract_conjunctiva_roi
    except Exception as exc:  # noqa: BLE001
        raise PipelineUnavailableError(
            _why_missing("OpenCV / fuzzy pipeline (ROI path)", exc)
        )

    _, bgr = _decode_rgb_and_bgr(img_bytes)
    roi = extract_conjunctiva_roi(bgr)
    corrected = apply_fuzzy_correction(roi)

    def _b64(bgr_img):
        ok, buf = cv2.imencode(".png", bgr_img)
        if not ok:
            raise ValueError("Failed to encode ROI as PNG.")
        return "data:image/png;base64," + base64.b64encode(buf.tobytes()).decode("ascii")

    return {"roi_raw": _b64(roi), "roi_corrected": _b64(corrected)}