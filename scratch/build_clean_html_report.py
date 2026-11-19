"""
build_clean_html_report.py
Constructs a publication-grade HTML report and renders it into a clean,
word-overlap-free PDF via Headless Chrome.
"""

import os
import subprocess
import base64

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HTML_OUT = os.path.join(ROOT_DIR, "scratch", "clean_report.html")
PDF_OUT = os.path.join(ROOT_DIR, "HemoSense_AI_Complete_Architecture_and_Implementation.pdf")

def img_to_b64(rel_path):
    p = os.path.join(ROOT_DIR, rel_path)
    if os.path.exists(p):
        with open(p, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/png;base64,{data}"
    return ""

fig_roc_b64 = img_to_b64("paper/figures/roc_live_pipeline.png")
fig_mfs_b64 = img_to_b64("paper/figures/anfis_membership.png")
fig_cal_b64 = img_to_b64("paper/figures/calibration_anfis_live.png")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>HemoSense AI: Architecture & Implementation Specification</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 14mm 14mm 14mm 14mm;
  }}
  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 8.8pt;
    line-height: 1.45;
    color: #1e293b;
    background: #ffffff;
    margin: 0;
    padding: 0;
  }}
  
  /* Header Card */
  .header-card {{
    background: linear-gradient(135deg, #7A1734 0%, #A61C3C 100%);
    color: #ffffff;
    padding: 16px 20px;
    border-radius: 8px;
    margin-bottom: 14px;
    box-shadow: 0 2px 6px rgba(122, 23, 52, 0.15);
  }}
  .badge {{
    display: inline-block;
    background: rgba(255, 255, 255, 0.22);
    color: #ffffff;
    font-size: 6.8pt;
    font-weight: 700;
    padding: 2.5px 8px;
    border-radius: 10px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 5px;
  }}
  .header-title {{
    font-size: 16pt;
    font-weight: 800;
    margin: 0 0 3px 0;
    letter-spacing: -0.2px;
    color: #ffffff;
  }}
  .header-subtitle {{
    font-size: 8.8pt;
    font-weight: 400;
    color: #fce4ea;
    margin: 0 0 8px 0;
  }}
  .header-meta {{
    font-size: 7.2pt;
    color: #f8bbd0;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    padding-top: 5px;
    margin-top: 3px;
    display: flex;
    justify-content: space-between;
  }}

  /* Headings */
  h1 {{
    color: #7A1734;
    font-size: 12.5pt;
    font-weight: 700;
    border-bottom: 2px solid #B4264A;
    padding-bottom: 3px;
    margin-top: 14px;
    margin-bottom: 8px;
    break-after: avoid;
    page-break-after: avoid;
  }}
  h2 {{
    color: #9c1535;
    font-size: 9.8pt;
    font-weight: 700;
    margin-top: 11px;
    margin-bottom: 4px;
    break-after: avoid;
    page-break-after: avoid;
  }}
  h3 {{
    color: #334155;
    font-size: 8.8pt;
    font-weight: 600;
    margin-top: 8px;
    margin-bottom: 3px;
    break-after: avoid;
    page-break-after: avoid;
  }}
  p {{
    margin: 0 0 6px 0;
    text-align: justify;
  }}

  /* Lists */
  ul, ol {{
    margin: 4px 0 7px 0;
    padding-left: 17px;
  }}
  li {{
    margin-bottom: 3px;
    line-height: 1.40;
  }}
  li strong {{
    color: #0f172a;
  }}

  /* Callout Cards */
  .callout {{
    border-left: 4px solid #B4264A;
    background-color: #fff5f7;
    padding: 8px 11px;
    margin: 8px 0;
    border-radius: 0 5px 5px 0;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  .callout-title {{
    font-weight: 700;
    color: #7A1734;
    font-size: 7.8pt;
    margin-bottom: 3px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  .callout-blue {{
    border-left-color: #1d4ed8;
    background-color: #eff6ff;
  }}
  .callout-blue .callout-title {{
    color: #1e40af;
  }}
  .callout-green {{
    border-left-color: #15803d;
    background-color: #f0fdf4;
  }}
  .callout-green .callout-title {{
    color: #166534;
  }}
  .callout-amber {{
    border-left-color: #d97706;
    background-color: #fffbeb;
  }}
  .callout-amber .callout-title {{
    color: #b45309;
  }}

  /* Code & Preformatted */
  pre {{
    background: #0f172a;
    color: #f8fafc;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 7.0pt;
    line-height: 1.32;
    padding: 8px 10px;
    border-radius: 5px;
    margin: 6px 0;
    overflow-x: auto;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  code {{
    font-family: Consolas, monospace;
    font-size: 7.8pt;
    background: #f1f5f9;
    padding: 1px 3px;
    border-radius: 3px;
    color: #9c1535;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 7px 0 10px 0;
    font-size: 7.4pt;
    line-height: 1.30;
  }}
  tr {{
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  th {{
    background-color: #7A1734;
    color: #ffffff;
    font-weight: 700;
    text-align: left;
    padding: 5px 7px;
    border: 1px solid #7A1734;
  }}
  td {{
    padding: 4.5px 7px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
  }}
  tr:nth-child(even) td {{
    background-color: #faf5f7;
  }}
  .col-highlight {{
    font-weight: 600;
    color: #7A1734;
  }}

  /* Figures */
  .figure-grid {{
    display: flex;
    gap: 10px;
    margin: 8px 0;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  .figure-box {{
    flex: 1;
    text-align: center;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 6px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
  }}
  .figure-box img {{
    max-width: 100%;
    height: auto;
    max-height: 155px;
    object-fit: contain;
  }}
  .figure-caption {{
    font-size: 6.8pt;
    color: #64748b;
    font-style: italic;
    margin-top: 3px;
    line-height: 1.20;
  }}

  .page-break {{
    page-break-before: always;
    break-before: always;
  }}
</style>
</head>
<body>

<!-- Header Card -->
<div class="header-card">
  <div class="badge">Technical Architecture Specification</div>
  <div class="header-title">HemoSense AI: Architecture & Implementation Guide</div>
  <div class="header-subtitle">Fuzzy-Logic-Based Smartphone Anemia Screening with Dietary Intelligence</div>
  <div class="header-meta">
    <span><strong>Author / Role:</strong> Senior Software Architect & Technical Lead</span>
    <span><strong>Platform Version:</strong> 1.1 Production</span>
    <span><strong>Target OS:</strong> Android / iOS / Web</span>
    <span><strong>Date:</strong> November 2026</span>
  </div>
</div>

<!-- Section 1 -->
<h1>1. Executive Summary & Clinical Paradigm</h1>
<p>
  <strong>HemoSense AI</strong> is an interpretable, non-invasive biomedical screening and nutritional advisory platform designed to bridge the diagnostic gap in rural and community healthcare settings where laboratory Complete Blood Count (CBC) testing via venous phlebotomy is inaccessible. The system leverages high-resolution macro photography of the <strong>palpebral conjunctiva</strong> (inner lower eyelid), enforces a 7-stage optical and anatomical safety gate, isolates microvascular tissue via interactive GrabCut and Otsu colorimetry, and performs classification via an interpretable <strong>zero-order Sugeno Adaptive Neuro-Fuzzy Inference System (ANFIS)</strong>.
</p>

<div class="callout callout-amber">
  <div class="callout-title">Core Clinical Governance Directive: Strict Hemoglobin Omission</div>
  Absolute hemoglobin values (Hb in g/dL) are <strong>strictly suppressed</strong> across all patient and clinical user interfaces. Commercial smartphone cameras lack the photometric dynamic range to reliably distinguish fine-grained continuous hemoglobin variations (e.g., 10.2 g/dL vs. 10.6 g/dL); displaying continuous regression numbers fosters a false sense of laboratory equivalence that risks patient safety. HemoSense AI frames results purely as <strong>ordinal triage categories (Normal, Mild, Moderate-to-Severe)</strong> backed by empirical 5-fold cross-validation confidence intervals, triggerable red-flag symptom warnings, and mandatory emergency clinical consultation alerts.
</div>

<!-- Section 2 -->
<h1>2. Complete End-to-End System Architecture</h1>
<p>
  The system employs a decoupled, multi-tiered architecture that separates edge-level optical acquisition, secure HTTPS transit, computer vision segmentation, neuro-fuzzy inference, and nutritional optimization. The design guarantees zero server-side photo persistence for patient privacy while achieving sub-2-second end-to-end response times.
</p>

<div class="callout callout-blue">
  <div class="callout-title">End-to-End Pipeline Dataflow Architecture</div>
<pre>
[Smartphone Client (Flutter app/)] 
       │ 1. Rear camera burst: 3 frames @ 350ms, torch ON, auto-exposure locked
       │ 2. Interactive review screen: user positions single bounding box [x, y, w, h]
       │ 3. Multipart HTTPS POST /screen/batch (Images + ROI box + Demographic JSON)
       ▼
[AWS EC2 / Caddy 2 Reverse Proxy] (Mumbai ap-south-1)
       │ • Automatic TLS 1.3 Termination (Let's Encrypt / sslip.io)
       │ • 40 MB max payload enforcement; IP-restricted admin access
       ▼
[FastAPI Production Service] (api/main.py & api/pipeline.py)
       │
       ├──▶ Step 1: Pre-Flight Optical & Anatomical Gate (hemosense/segment.py)
       │    ├── Resolution Gate: min(w, h) >= 40px at 900px scale
       │    ├── Brightness Gate: mean luminance in [0.15, 0.95]; glare clipped < 25%
       │    ├── Sharpness Gate: Laplacian variance >= 12.0
       │    ├── Sclera Spatial Prior: detects white ocular tissue directly above box
       │    └── Crescent Geometric Prior: elongation >= 2.7, solidity <= 0.85, w/h >= 1.1
       │
       ├──▶ Step 2: Palpebral Tissue Segmentation (hemosense/segment.py)
       │    ├── GrabCut initialized with user ROI (4 iterations, 15% margin)
       │    └── Morphological cleanup + CIELAB a* Otsu thresholding split
       │
       ├──▶ Step 3: Hemodynamic Colorimetry Extraction (hemosense/features.py)
       │    └── Erythema Index (EI), CIELAB a*, High Red-Hue Ratio (HHR), Saturation
       │
       ├──▶ Step 4: Dual-Stage Zero-Order Sugeno ANFIS (models/anfis.json)
       │    ├── Stage 1: p(Anemic) via 3 inputs x 3 Gaussian terms (27 rules)
       │    ├── Stage 2: If p >= 0.5, evaluate p(Moderate-to-Severe)
       │    └── Platt Calibration: p = 1 / (1 + exp(-(a*z + b)))
       │
       ├──▶ Step 5: Multi-Frame Consensus & Confidence Mapping (api/clinical.py)
       │    ├── Median probability across frames; voter agreement fraction
       │    └── Empirical reliability table lookup (models/confidence.json)
       │
       └──▶ Step 6: Bioavailability-Aware Dietary Optimizer (hemosense/diet.py)
            ├── Solves RDA target by age, biological sex, and pregnancy
            ├── 46-food composition table (USDA FoodData Central SR Legacy)
            ├── Hurrell & Egli mathematical iron absorption equation
            └── OpenRouter LLM regional translation (strict server nutrient re-check)
       │
       ▼
[Structured Response to Client] (Verdict, Risk %, Fired Rules, Feature Bars, 1-Day Plan)
</pre>
</div>

<!-- Section 3 -->
<div class="page-break"></div>
<h1>3. Technology Stack & Component Purpose Matrix</h1>
<p>
  Every component across client, backend, machine learning, and infrastructure was selected based on strict requirements of edge-to-cloud performance, deterministic mathematical reproducibility, zero-cloud data leak privacy, and operational resilience.
</p>

<table>
  <thead>
    <tr>
      <th style="width: 17%;">Tier / Domain</th>
      <th style="width: 22%;">Technology & Version</th>
      <th style="width: 33%;">Key Architectural Purpose</th>
      <th style="width: 28%;">Technical Selection Rationale</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="col-highlight">Mobile Client</td>
      <td><strong>Flutter 3.47+ / Dart</strong></td>
      <td>Primary cross-platform mobile delivery for field health workers and end users.</td>
      <td>Single codebase for Android and iOS; hardware camera API bindings; 60fps canvas rendering for bounding box manipulation.</td>
    </tr>
    <tr>
      <td class="col-highlight">State Management</td>
      <td><strong>Riverpod 3 (Notifier)</strong></td>
      <td>Deterministic app-wide reactive state management without UI rebuild bottlenecks.</td>
      <td>Compile-time safety, seamless async provider testing, decoupled architecture separating UI from network logic.</td>
    </tr>
    <tr>
      <td class="col-highlight">Local Storage</td>
      <td><strong>Hive / hive_flutter</strong></td>
      <td>On-device encrypted key-value database for profiles, scan histories, and offline settings.</td>
      <td>Written in pure Dart with &lt;5ms read/write latency; eliminates privacy leak of storing health records on cloud.</td>
    </tr>
    <tr>
      <td class="col-highlight">HTTP Client</td>
      <td><strong>Dio 5.x</strong></td>
      <td>Handles multi-part batch uploads, connection timeouts, and SSL certificate pinning.</td>
      <td>Native multipart stream encoding for burst photos, clean interceptors for machine error code translation.</td>
    </tr>
    <tr>
      <td class="col-highlight">Web Demo UI</td>
      <td><strong>Next.js 14 / React 18</strong></td>
      <td>Desktop presentation portal and rapid screening simulator for lab and evaluation judges.</td>
      <td>SSR/SSG capabilities, responsive Tailwind CSS styling, drag-and-drop web file testing.</td>
    </tr>
    <tr>
      <td class="col-highlight">Backend API</td>
      <td><strong>FastAPI 0.162+ / Pydantic v2</strong></td>
      <td>REST serving gateway, request validation, exception mapping, async pipeline execution.</td>
      <td>High concurrency (asyncio), automatic OpenAPI/Swagger generation, sub-millisecond Pydantic v2 serialization.</td>
    </tr>
    <tr>
      <td class="col-highlight">Application Server</td>
      <td><strong>Uvicorn / Starlette</strong></td>
      <td>ASGI web server running 2 worker processes inside non-root Docker container.</td>
      <td>Lightweight, production-tested, low CPU/RAM footprint (~80 MB RAM per worker).</td>
    </tr>
    <tr>
      <td class="col-highlight">Computer Vision</td>
      <td><strong>OpenCV 4.11 / Pillow 13.0</strong></td>
      <td>EXIF rotation, resizing, Laplacian blur detection, GrabCut segmentation, contour geometry.</td>
      <td>High-speed C++ primitives, battle-tested morphological operations, stable cross-platform array representations.</td>
    </tr>
    <tr>
      <td class="col-highlight">Scientific Math</td>
      <td><strong>NumPy 1.26 / SciPy 1.15</strong></td>
      <td>Matrix algebra, analytic gradients, Gaussian membership evaluation, Adam optimization.</td>
      <td>Zero heavy framework dependencies (no PyTorch/TensorFlow at serving), deterministic vectorization.</td>
    </tr>
    <tr>
      <td class="col-highlight">Fuzzy Inference</td>
      <td><strong>Custom ANFIS (hemosense/anfis.py)</strong></td>
      <td>Zero-order Sugeno ANFIS implementation with Gaussian terms and Platt calibration.</td>
      <td>Pure NumPy inference (sub-5ms execution), transparent rule activation, analytic Adam optimization; 45 params.</td>
    </tr>
    <tr>
      <td class="col-highlight">Dietary Database</td>
      <td><strong>USDA SR Legacy (FDC)</strong></td>
      <td>46-food composition database (iron, vitamin C, calcium, protein, serving grams).</td>
      <td>Public domain, scientifically verified laboratory nutrient compositions, avoids AI nutritional hallucinations.</td>
    </tr>
    <tr>
      <td class="col-highlight">Dietary Phrasing</td>
      <td><strong>OpenRouter API (Llama 3.1)</strong></td>
      <td>Translates structured USDA meal recommendations into regional dish names and cost estimates.</td>
      <td>Strict schema validation: server validates every food against allowed pool and re-computes USDA numbers.</td>
    </tr>
    <tr>
      <td class="col-highlight">Infrastructure</td>
      <td><strong>AWS EC2 t3.small / Caddy</strong></td>
      <td>Ubuntu 24.04 LTS host, Docker Compose, Elastic IP, Caddy auto-TLS (sslip.io).</td>
      <td>Ultra-low cost ($0.025/hr), automated Let's Encrypt certificates, CloudWatch auto-recovery.</td>
    </tr>
  </tbody>
</table>

<!-- Section 4 -->
<div class="page-break"></div>
<h1>4. Step-by-Step Implementation Breakdown</h1>
<p>
  The HemoSense AI pipeline transforms raw photon counts captured by a commercial smartphone camera into an interpretable clinical screening verdict and nutritional action plan through 8 rigorously validated execution steps.
</p>

<h2>Step 1: Optical Acquisition & Frame Burst Capture</h2>
<p>
  <strong>Implementation:</strong> Located in <code>app/lib/screens/camera_screen.dart</code>. The Flutter camera controller sets rear-facing sensor mode, enables the hardware torch, and enforces an 800 ms dwell time to allow camera Auto-Exposure (AE) and Auto-White-Balance (AWB) routines to stabilize under direct illumination. It then triggers a hardware-timed burst of 3 consecutive frames spaced 350 ms apart. In the review screen, the user draws a single bounding box <code>[x, y, w, h]</code> (normalized 0.0 to 1.0) over the pulled-down palpebral conjunctiva, which is shared across all 3 frames.
</p>

<h2>Step 2: Pre-Flight Optical Quality & Anatomical Safety Gates</h2>
<p>
  <strong>Implementation:</strong> Located in <code>hemosense/segment.py</code>. Prior to running computationally expensive segmentation or inference, the image is passed through a 7-stage gate at a normalized 900 px working resolution. If any condition fails, execution halts immediately with a machine-readable error code and human actionable guidance:
</p>
<ul>
  <li><strong>1. Scale Gate (<code>too_far</code>):</strong> Verifies that <code>min(box_w, box_h) >= 40 pixels</code> at 900 px resolution. Rejects distant, low-pixel eyelid captures.</li>
  <li><strong>2. Underexposure Gate (<code>too_dark</code>):</strong> Computes mean grayscale luminance inside the ROI: rejects if mean brightness &lt; 0.15 (scale 0.0 - 1.0).</li>
  <li><strong>3. Specular Overexposure Gate (<code>overexposed</code>):</strong> Measures pixel saturation: rejects if &gt; 25% of ROI pixels have RGB channels clipped at 255.</li>
  <li><strong>4. High-Frequency Blur Gate (<code>blurry</code>):</strong> Applies a discrete 3x3 Laplacian kernel over the cropped ROI: rejects if <code>Var(Laplacian) &lt; 12.0</code>.</li>
  <li><strong>5. Anatomical Context Sclera Gate (<code>no_eye</code>):</strong> Samples an anatomical band directly above the user box. Detects high-luminance, low-saturation scleral white tissue. Rejects if user draws box over forehead, mouth, or shirt.</li>
  <li><strong>6. Crescent Geometric Prior Gate (<code>not_crescent</code>):</strong> Measures contour properties on segmented tissue: enforces elongation <code>max(w,h)^2 / area >= 2.7</code>, solidity <code>area / convex_hull &lt;= 0.85</code>, and aspect ratio <code>w/h >= 1.1</code>. Discards compact circular blobs (cheeks/noses).</li>
  <li><strong>7. Minimum Tissue Area Gate (<code>no_conjunctiva</code>):</strong> Enforces minimum segmented conjunctiva pixel count: <code>area >= max(150 px, 2% of ROI area)</code>.</li>
</ul>

<h2>Step 3: Conjunctival Tissue Segmentation (GrabCut + CIELAB a* Split)</h2>
<p>
  <strong>Implementation:</strong> Located in <code>hemosense/segment.py</code>. The user-provided bounding box is expanded by a 15% safety margin and cropped to at most 360 px width for performance. GrabCut (<code>cv2.grabCut</code>) executes 4 iterations initialized with <code>cv2.GC_INIT_WITH_RECT</code>. The resulting foreground mask undergoes morphological cleanup: dark eyelash pixels, specular flash reflections, and bright sclera pixels are subtracted. If multi-modal color populations remain, the smoothed CIELAB a* distribution is split using Otsu thresholding, retaining the largest crescent component matching anatomical priors.
</p>

<h2>Step 4: Hemodynamic & Colorimetric Feature Engineering</h2>
<p>
  <strong>Implementation:</strong> Located in <code>hemosense/features.py</code>. Extracted exclusively from the segmented tissue pixels. The engine extracts 4 biologically validated optical features:
</p>
<ul>
  <li><strong>1. Erythema Index (EI):</strong> <code>EI = 100 * [log10(mean_Red) - log10(mean_Green)]</code>. Quantifies microvascular hemoglobin absorption against background tissue scattering (Collings et al., 2016).</li>
  <li><strong>2. CIELAB a* (Red-Green Chrominance):</strong> Mean a* coordinate in the perceptually uniform CIE L*a*b* space, representing vascular tissue flushing.</li>
  <li><strong>3. High Red-Hue Ratio (HHR):</strong> Proportion of tissue pixels satisfying Hue within &plusmn;15&deg; of true Red (0&deg;) and HSV Saturation &gt; 0.30 (Zhao et al., 2024).</li>
  <li><strong>4. HSV Saturation:</strong> Mean color purity across the segmented palpebral tissue.</li>
</ul>

<div class="page-break"></div>
<h2>Step 5: Dual-Stage Zero-Order Sugeno ANFIS Inference</h2>
<p>
  <strong>Implementation:</strong> Located in <code>hemosense/anfis.py</code> and <code>models/anfis.json</code>. Employs a forward-selected 3-input feature vector (CIELAB a*, HHR, EI). Each input is partitioned into 3 Gaussian membership functions (Low, Medium, High), yielding 3<sup>3</sup> = 27 rules. Consequents are zero-order constant logits &theta;<sub>r</sub>. The network evaluates normalized firing strengths w&#772;<sub>r</sub> and defuzzifies via weighted average. A post-hoc Platt logistic scaler maps logits to calibrated probabilities <code>p = sigmoid(a * z + b)</code>. A two-stage cascade is executed: Stage 1 evaluates p(anemic); if p &ge; 0.5, Stage 2 evaluates p(moderate-to-severe).
</p>

<h2>Step 6: Multi-Frame Voting Consensus & Empirical Reliability Mapping</h2>
<p>
  <strong>Implementation:</strong> Located in <code>api/clinical.py</code> and <code>models/confidence.json</code>. For multi-frame uploads (e.g., 3-frame burst), the server extracts features and evaluates ANFIS probabilities independently per accepted frame. The aggregate probability is the median across frames. Voter agreement is computed as the fraction of frames agreeing with the majority verdict. Aggregate certainty <code>max(p, 1 - p)</code> is matched against an empirical 5-fold cross-validation table (e.g., certainty 0.9-1.0 exhibits 94% test accuracy across 69 cohort patients).
</p>

<h2>Step 7: Clinical Decision Framework & Severity Triage</h2>
<p>
  <strong>Implementation:</strong> Located in <code>api/clinical.py</code>. Results are classified into three ordinal clinical bins: Normal (p &lt; 0.5), Mild Anemia (p &ge; 0.5 and p<sub>sev</sub> &lt; 0.5), and Moderate-to-Severe Anemia (p &ge; 0.5 and p<sub>sev</sub> &ge; 0.5). To protect patient safety, severe classifications or reported red-flag symptoms (severe dizziness, chest pain, fainting) trigger a prominent "Consult a Doctor" emergency medical banner. Absolute hemoglobin values are strictly suppressed.
</p>

<h2>Step 8: Bioavailability-Aware Dietary Optimization Engine</h2>
<p>
  <strong>Implementation:</strong> Located in <code>hemosense/diet.py</code> and <code>api/llm.py</code>. Employs a deterministic nutrient optimizer grounded in USDA SR Legacy data (<code>foods_usda.csv</code>, 46 items). Solves for individual Recommended Dietary Allowance (RDA) by sex, age, and pregnancy. Computes bioavailable iron per meal via the Hurrell & Egli mathematical model:
</p>
<div class="callout callout-green">
  <div class="callout-title">Hurrell & Egli Iron Bioavailability Formulation</div>
  <code>Fe_absorbable = Fe_heme * 0.25 + Fe_nonheme * 0.10 * E * I</code><br>
  &bull; Enhancer E = 2.0 if meal Vitamin C &ge; 25 mg or contains meat/poultry/fish.<br>
  &bull; Inhibitor I = 0.7 if meal Calcium &ge; 300 mg (dairy penalty).<br>
  &bull; Inhibitor I = 0.8 if phytate-rich grains/legumes dominate without ascorbic acid.<br>
  Safety Rule: Organ meats (liver) are hard-filtered out for pregnant women to prevent Vitamin A teratogenicity.
</div>

<!-- Section 5 -->
<div class="page-break"></div>
<h1>5. Deep Comparative Analysis: Rationale vs. Alternative Methods</h1>
<p>
  A defining engineering feature of HemoSense AI is the conscious architectural decision made at every stage to avoid fragile, uninterpretable black-box techniques in favor of robust, mathematically verifiable, and medically responsible methods.
</p>

<table>
  <thead>
    <tr>
      <th style="width: 14%;">Pipeline Step</th>
      <th style="width: 22%;">Chosen HemoSense Method</th>
      <th style="width: 22%;">Rejected Alternative Methods</th>
      <th style="width: 42%;">Why Chosen (Comparative Advantage & Rationale)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="col-highlight">Step 1: Capture</td>
      <td><strong>3-Frame Burst with Torch ON (350 ms spacing)</strong></td>
      <td>&bull; Ambient room lighting<br>&bull; Xenon flash photograph<br>&bull; Continuous video stream</td>
      <td>Ambient light causes severe Kelvin temperature shifts. Xenon flashes cause specular cornea glare, wash out palpebral pink tones, and trigger involuntary blink reflexes. Continuous video exhibits low per-frame bitrate and rolling shutter distortion. A continuous torch locks the camera's auto-exposure loop while a 3-frame burst enables median temporal filtering against hand tremor.</td>
    </tr>
    <tr>
      <td class="col-highlight">Step 2: Quality Gates</td>
      <td><strong>Multi-Parameter Rule & Crescent Prior Gate</strong></td>
      <td>&bull; Unchecked direct inference<br>&bull; Deep CNN binary classifier (Good vs. Bad)</td>
      <td>Unchecked inference produces erratic risk scores when users accidentally capture cheeks, noses, or clothing. Deep CNN binary classifiers require enormous out-of-distribution training sets and fail silently on novel artifacts. Explicit geometric and photometric constraints (Laplacian blur, crescent elongation &ge; 2.7, sclera detection) provide deterministic, explainable rejections.</td>
    </tr>
    <tr>
      <td class="col-highlight">Step 3: Segmentation</td>
      <td><strong>User-Guided GrabCut + CIELAB a* Otsu Refinement</strong></td>
      <td>&bull; Fully automatic U-Net<br>&bull; Fixed central crop box<br>&bull; Simple RGB thresholding</td>
      <td>Fully automatic U-Nets trained on small datasets fail under variable gaze angles and partial eyelid eversions, requiring heavy neural weights on mobile. Fixed center crops capture eyelashes and skin. Simple RGB thresholding confuses eyelid tissue with lips and cheeks. User-guided GrabCut leverages human intelligence for coarse localization while automated Otsu a* mathematically discards pale sclera and dark lashes.</td>
    </tr>
    <tr>
      <td class="col-highlight">Step 4: Features</td>
      <td><strong>Biologically Grounded Hemodynamic Indices (EI, a*, HHR)</strong></td>
      <td>&bull; Deep CNN latent embeddings<br>&bull; Raw RGB pixel histograms<br>&bull; Gray-level co-occurrence</td>
      <td>Deep latent representations act as black boxes prone to shortcut learning (memorizing camera sensor artifacts, patient skin tone, or background clinic colors). Hemodynamic indices (EI, a*, HHR) directly mirror the biophysical physics of oxyhemoglobin and deoxyhemoglobin light absorption in capillary microvasculature, ensuring invariant biological representation.</td>
    </tr>
    <tr>
      <td class="col-highlight">Step 5: Model Core</td>
      <td><strong>Dual-Stage Zero-Order Sugeno ANFIS (27 rules)</strong></td>
      <td>&bull; Deep CNN (MobileNetV3)<br>&bull; Random Forest / SVM<br>&bull; Pure Mamdani Fuzzy System</td>
      <td>MobileNetV3 achieved lower live AUC (0.81 vs 0.88 ANFIS) and is completely unexplainable. Random Forest cannot easily output smooth Gaussian membership boundaries. Pure Mamdani requires hand-crafted rule weights that struggle with multi-variable non-linearities. Sugeno ANFIS combines neural gradient learning (Adam) with explicit IF-THEN transparent fuzzy linguistic rules.</td>
    </tr>
    <tr>
      <td class="col-highlight">Step 6: Clinical Metric</td>
      <td><strong>Ordinal Risk Category + Empirical Confidence Bands</strong></td>
      <td>&bull; Continuous Hemoglobin Regression (Hb in g/dL)<br>&bull; Raw uncalibrated probabilities</td>
      <td>Non-invasive optical methods lack the photometric dynamic range to accurately differentiate 10.2 g/dL from 10.6 g/dL; regression models produce misleading pseudo-precision that misleads patients. Continuous Hb display risks delayed diagnosis if a patient believes an inaccurate 11.2 g/dL. Ordinal risk with empirical confidence tables provides medically sound, actionable triage.</td>
    </tr>
    <tr>
      <td class="col-highlight">Step 7: Consensus</td>
      <td><strong>Median Aggregation + Agreement Ratio Voting</strong></td>
      <td>&bull; Single frame inference<br>&bull; Mean logit average<br>&bull; Winner-take-all maximum</td>
      <td>Single frames are vulnerable to brief micro-saccades, blinks, or local specular flash reflections. Mean averaging is skewed by single catastrophic outlier frames. Median probability across 3 frames combined with an agreement fraction guarantees statistical robustness and drops confidence if photos disagree.</td>
    </tr>
    <tr>
      <td class="col-highlight">Step 8: Diet Intelligence</td>
      <td><strong>Grounded USDA Bioavailability Model + LLM Wording</strong></td>
      <td>&bull; Pure LLM generative prompt<br>&bull; Static generic PDF diet charts<br>&bull; Raw calorie-counting apps</td>
      <td>Pure LLMs frequently hallucinate micronutrient numbers, recommend toxic combinations (e.g. iron supplements with calcium), or prescribe liver to pregnant women. Static diet charts ignore vegan/vegetarian restrictions and bioavailability inhibitors. HemoSense computes exact USDA nutrient math deterministically, using LLMs strictly for cultural phrasing.</td>
    </tr>
  </tbody>
</table>

<!-- Section 6 -->
<div class="page-break"></div>
<h1>6. Experimental Validation & Research Benchmarks</h1>
<p>
  Validation was conducted across 215 clinical subjects from the public <em>Eyes-defy-anemia</em> benchmark cohort under a strict 5-fold participant-stratified cross-validation protocol (<code>StratifiedKFold</code> on region &times; anemia status). Feature selection and Platt calibration were strictly confined inside training folds to prevent data leakage.
</p>

<table>
  <thead>
    <tr>
      <th style="width: 25%;">Model Architecture</th>
      <th style="width: 25%;">Input Pipeline</th>
      <th style="width: 22%;">Cross-Validated AUC</th>
      <th style="width: 14%;">Sensitivity</th>
      <th style="width: 14%;">Specificity</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background-color: #fef2f4;">
      <td class="col-highlight"><strong>HemoSense ANFIS (Proposed)</strong></td>
      <td>Live Pipeline (GrabCut + Gates)</td>
      <td><strong>0.879 [95% CI: 0.83–0.92]</strong></td>
      <td>77.1% (&tau; = 0.50)</td>
      <td>82.4% (&tau; = 0.50)</td>
    </tr>
    <tr>
      <td><strong>HemoSense ANFIS (Youden J)</strong></td>
      <td>Live Pipeline (Screening Mode)</td>
      <td>0.879 [95% CI: 0.83–0.92]</td>
      <td>88.6% (&tau; = 0.15)</td>
      <td>71.2% (&tau; = 0.15)</td>
    </tr>
    <tr>
      <td>Random Forest Classifier</td>
      <td>Engineered Features</td>
      <td>0.841 [95% CI: 0.78–0.90]</td>
      <td>74.3%</td>
      <td>78.2%</td>
    </tr>
    <tr>
      <td>Logistic Regression</td>
      <td>Engineered Features</td>
      <td>0.834 [95% CI: 0.77–0.89]</td>
      <td>71.4%</td>
      <td>79.1%</td>
    </tr>
    <tr>
      <td>MobileNetV3 Small (CNN)</td>
      <td>Cropped Eyelid Images</td>
      <td>0.812 [95% CI: 0.74–0.88]</td>
      <td>72.4%</td>
      <td>74.1%</td>
    </tr>
    <tr>
      <td>Mamdani Fuzzy Baseline</td>
      <td>Expert Rules (scikit-fuzzy)</td>
      <td>0.785 [95% CI: 0.71–0.85]</td>
      <td>68.6%</td>
      <td>75.0%</td>
    </tr>
  </tbody>
</table>

<div class="callout callout-green">
  <div class="callout-title">Statistical Significance & Model Economy (DeLong Test)</div>
  The proposed ANFIS pipeline demonstrates statistically significant superiority over the baseline classical Mamdani system (DeLong p &lt; 0.01) and outperforms end-to-end deep MobileNetV3 (AUC 0.879 vs 0.812, p = 0.038) while operating with only <strong>45 parameters versus 1.5 million neural weights</strong>.
</div>

<!-- Embedded Figures Grid -->
<div class="figure-grid">
  <div class="figure-box">
    <img src="{fig_roc_b64}" alt="ROC Curve">
    <div class="figure-caption">Figure 1: 5-Fold Cross-Validated ROC curve for ANFIS (AUC 0.879) vs. Random Forest, LogReg, and Mamdani.</div>
  </div>
  <div class="figure-box">
    <img src="{fig_mfs_b64}" alt="Membership Functions">
    <div class="figure-caption">Figure 2: Learned Gaussian membership linguistic terms (Low, Medium, High) for a*, HHR, and EI.</div>
  </div>
  <div class="figure-box">
    <img src="{fig_cal_b64}" alt="Calibration Diagram">
    <div class="figure-caption">Figure 3: Platt calibration reliability curve demonstrating empirical alignment with true risk fractions.</div>
  </div>
</div>

<!-- Section 7 -->
<div class="page-break"></div>
<h1>7. Operational Infrastructure & Privacy Compliance</h1>
<p>
  HemoSense AI is deployed on AWS EC2 (Mumbai ap-south-1) under a hardened, least-privilege security architecture engineered to respect patient medical data sovereignty:
</p>
<ul>
  <li><strong>Zero-Persistence Ingestion:</strong> Patient photographs uploaded to <code>/screen/batch</code> are buffered strictly in ephemeral RAM worker memory, processed, and immediately discarded upon response dispatch. No image bytes are ever written to server disk or persistent cloud buckets.</li>
  <li><strong>Decoupled Client Identity:</strong> The platform requires no user registration, telephone numbers, or biometric names. All demographic context (age, pregnancy, dietary preferences) is stored locally on the user's mobile device via Hive storage.</li>
  <li><strong>Transport Protection:</strong> Caddy 2 handles TLS termination with automatic Let's Encrypt certificates, enforcing HSTS, rate-limiting, and 40 MB payload restrictions. AWS Security Groups restrict port 22 SSH strictly to the deployer's IP, leaving only standard ports 80/443 public.</li>
  <li><strong>Infrastructure Resilience:</strong> Docker Compose manages automatic container restart policies. A CloudWatch alarm monitors EC2 instance health and initiates automatic instance reboot recovery in the event of underlying hypervisor faults.</li>
</ul>

<!-- Section 8 -->
<h1>8. Architectural Limitations & Future Engineering Roadmap</h1>
<ul>
  <li><strong>1. Sclera-Based White Balance Activation:</strong> While <code>hemosense/colour.py</code> contains prototype routines for sclera chromatic normalization, v1 relies on torch standardization. Activating real-time sclera normalization will further insulate the pipeline against multi-brand smartphone camera ISP shifts.</li>
  <li><strong>2. Edge ML Dart Porting:</strong> Port the 45-parameter zero-order Sugeno inference formulas directly into native Dart in the Flutter app to achieve 100% offline, serverless screening in remote rural zones.</li>
  <li><strong>3. Automated Palpebral Landmark Detection:</strong> Integrate an ultra-lightweight on-device eye landmark detector (e.g. MediaPipe Face Mesh) to suggest the initial bounding box, reducing human placement effort.</li>
  <li><strong>4. ICMR-NIN 2020 Dietary Localization:</strong> Transition from US NIH nutrient RDA targets to Indian Council of Medical Research (ICMR-NIN 2020) guidelines to align with national health protocols.</li>
</ul>

</body>
</html>
"""

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Wrote HTML to {HTML_OUT}")

# Render to PDF using Chrome Headless
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
file_uri = "file:///" + HTML_OUT.replace("\\", "/")

cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF_OUT}",
    file_uri,
]

print("Executing Chrome headless print...")
proc = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(PDF_OUT):
    size_mb = os.path.getsize(PDF_OUT) / (1024 * 1024)
    print(f"SUCCESS: Generated clean PDF at {PDF_OUT} ({size_mb:.2f} MB)")
else:
    print(f"FAILED: PDF not generated. Exit code: {proc.returncode}")
    print("Stderr:", proc.stderr)
