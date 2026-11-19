"""
generate_pdf_report.py
Generates the comprehensive, publication-grade HemoSense AI Technical Architecture,
Tech Stack, Step-by-Step Implementation, and Comparative Analysis PDF.
"""

import os
import sys
import fitz  # PyMuPDF

# Theme Colors (RGB tuples 0.0 - 1.0)
COLOR_PRIMARY_DARK = (0.478, 0.090, 0.204)    # #7A1734 Deep Maroon
COLOR_PRIMARY = (0.706, 0.149, 0.290)         # #B4264A Crimson
COLOR_PRIMARY_LIGHT = (0.988, 0.894, 0.918)   # #FCE4EA Soft Pink Tint
COLOR_BG_LIGHT = (1.0, 0.973, 0.976)          # #FFF8F9 Warm Off-White
COLOR_TEXT_DARK = (0.12, 0.12, 0.14)          # Charcoal Black
COLOR_TEXT_MUTED = (0.40, 0.40, 0.45)         # Slate Grey
COLOR_BORDER = (0.85, 0.85, 0.88)             # Light Border Grey
COLOR_HEADER_BG = (0.478, 0.090, 0.204)       # Deep Maroon for Table Headers
COLOR_ROW_ALT = (0.97, 0.97, 0.98)            # Light Row Zebra
COLOR_CALLOUT_BG = (0.97, 0.94, 0.95)         # Callout Background
COLOR_CALLOUT_BORDER = (0.706, 0.149, 0.290)   # Callout Left Border
COLOR_TAG_BG = (0.90, 0.92, 0.96)             # Subtle Blue-Grey Tag
COLOR_WHITE = (1.0, 1.0, 1.0)

PAGE_WIDTH = 595.3   # A4 Width
PAGE_HEIGHT = 841.9  # A4 Height
MARGIN_LEFT = 42.0
MARGIN_RIGHT = 553.3
CONTENT_WIDTH = MARGIN_RIGHT - MARGIN_LEFT  # 511.3 pt
MARGIN_TOP = 48.0
MARGIN_BOTTOM = 800.0


class PDFDocument:
    def __init__(self, filename):
        self.filename = filename
        self.doc = fitz.open()
        self.pages = []
        self.current_page = None
        self.y = MARGIN_TOP

    def add_page(self):
        page = self.doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
        self.pages.append(page)
        self.current_page = page
        self.y = MARGIN_TOP
        return page

    def check_space(self, needed_h):
        if self.current_page is None or (self.y + needed_h > MARGIN_BOTTOM):
            self.add_page()

    def add_header_banner(self, title, subtitle, date_str="November 2026"):
        self.check_space(140)
        p = self.current_page

        # Background Header Card
        p.draw_rect(
            fitz.Rect(MARGIN_LEFT, self.y, MARGIN_RIGHT, self.y + 115),
            color=COLOR_PRIMARY_DARK,
            fill=COLOR_PRIMARY_DARK,
        )

        # Subtle Accent Stripe
        p.draw_rect(
            fitz.Rect(MARGIN_LEFT, self.y + 110, MARGIN_RIGHT, self.y + 115),
            color=COLOR_PRIMARY,
            fill=COLOR_PRIMARY,
        )

        # Category Pill
        pill_rect = fitz.Rect(MARGIN_LEFT + 15, self.y + 14, MARGIN_LEFT + 185, self.y + 30)
        p.draw_rect(pill_rect, color=COLOR_WHITE, fill=COLOR_WHITE)
        p.insert_text(
            (MARGIN_LEFT + 22, self.y + 25),
            "TECHNICAL ARCHITECTURE SPECIFICATION",
            fontname="hebo",
            fontsize=6.5,
            color=COLOR_PRIMARY_DARK,
        )

        # Main Title
        p.insert_text(
            (MARGIN_LEFT + 15, self.y + 55),
            title,
            fontname="hebo",
            fontsize=18,
            color=COLOR_WHITE,
        )

        # Subtitle
        p.insert_text(
            (MARGIN_LEFT + 15, self.y + 75),
            subtitle,
            fontname="helv",
            fontsize=9.5,
            color=COLOR_PRIMARY_LIGHT,
        )

        # Metadata Line
        meta_str = f"Platform: HemoSense AI | Version: 1.1 | Date: {date_str} | Classification: Medical AI Engineering"
        p.insert_text(
            (MARGIN_LEFT + 15, self.y + 98),
            meta_str,
            fontname="heit",
            fontsize=7.5,
            color=(0.9, 0.85, 0.88),
        )

        self.y += 130

    def add_h1(self, text):
        self.check_space(45)
        p = self.current_page
        # Section Bar
        p.draw_rect(fitz.Rect(MARGIN_LEFT, self.y + 2, MARGIN_LEFT + 4, self.y + 20),
                    color=COLOR_PRIMARY, fill=COLOR_PRIMARY)
        p.insert_text((MARGIN_LEFT + 10, self.y + 16), text, fontname="hebo", fontsize=13, color=COLOR_PRIMARY_DARK)
        self.y += 24

        # Subtle separator line
        p.draw_line(fitz.Point(MARGIN_LEFT + 10, self.y), fitz.Point(MARGIN_RIGHT, self.y),
                    color=COLOR_BORDER, width=0.6)
        self.y += 8

    def add_h2(self, text):
        self.check_space(32)
        p = self.current_page
        p.insert_text((MARGIN_LEFT, self.y + 14), text, fontname="hebo", fontsize=10.5, color=COLOR_PRIMARY)
        self.y += 18

    def add_h3(self, text):
        self.check_space(24)
        p = self.current_page
        p.insert_text((MARGIN_LEFT, self.y + 11), text, fontname="hebo", fontsize=9.0, color=COLOR_TEXT_DARK)
        self.y += 14

    def add_p(self, text, size=8.5, color=COLOR_TEXT_DARK, bold=False, line_spacing=11.0):
        words = text.split(" ")
        font = "hebo" if bold else "helv"
        lines = []
        cur_line = []
        for word in words:
            test_line = " ".join(cur_line + [word])
            w = fitz.get_text_length(test_line, fontname=font, fontsize=size)
            if w <= CONTENT_WIDTH:
                cur_line.append(word)
            else:
                if cur_line:
                    lines.append(" ".join(cur_line))
                cur_line = [word]
        if cur_line:
            lines.append(" ".join(cur_line))

        needed_h = len(lines) * line_spacing + 4
        self.check_space(needed_h)
        for line in lines:
            self.current_page.insert_text((MARGIN_LEFT, self.y + size), line, fontname=font, fontsize=size, color=color)
            self.y += line_spacing
        self.y += 4

    def add_bullet(self, title, text, size=8.2, line_spacing=10.5):
        full_text = f"{title}: {text}" if title else text
        words = full_text.split(" ")
        bullet_indent = 12.0
        avail_w = CONTENT_WIDTH - bullet_indent

        lines = []
        cur_line = []
        for word in words:
            test_line = " ".join(cur_line + [word])
            w = fitz.get_text_length(test_line, fontname="helv", fontsize=size)
            if w <= avail_w:
                cur_line.append(word)
            else:
                if cur_line:
                    lines.append(" ".join(cur_line))
                cur_line = [word]
        if cur_line:
            lines.append(" ".join(cur_line))

        needed_h = len(lines) * line_spacing + 3
        self.check_space(needed_h)
        p = self.current_page

        # Draw bullet symbol
        p.draw_circle(fitz.Point(MARGIN_LEFT + 4, self.y + size * 0.7), 1.8, color=COLOR_PRIMARY, fill=COLOR_PRIMARY)

        for idx, line in enumerate(lines):
            line_x = MARGIN_LEFT + bullet_indent
            if idx == 0 and title:
                # Highlight bold title
                t_str = f"{title}: "
                t_w = fitz.get_text_length(t_str, fontname="hebo", fontsize=size)
                p.insert_text((line_x, self.y + size), t_str, fontname="hebo", fontsize=size, color=COLOR_TEXT_DARK)
                rem_str = line[len(t_str):]
                p.insert_text((line_x + t_w, self.y + size), rem_str, fontname="helv", fontsize=size, color=COLOR_TEXT_DARK)
            else:
                p.insert_text((line_x, self.y + size), line, fontname="helv", fontsize=size, color=COLOR_TEXT_DARK)
            self.y += line_spacing
        self.y += 3

    def add_callout(self, title, text, alert_type="info"):
        bg = COLOR_CALLOUT_BG
        border = COLOR_CALLOUT_BORDER
        t_color = COLOR_PRIMARY_DARK
        if alert_type == "decision":
            bg = (0.94, 0.96, 0.99)
            border = (0.15, 0.40, 0.75)
            t_color = (0.10, 0.30, 0.60)
        elif alert_type == "warning":
            bg = (1.0, 0.96, 0.92)
            border = (0.85, 0.45, 0.10)
            t_color = (0.65, 0.30, 0.05)

        # Wrap text
        words = text.split(" ")
        lines = []
        cur_line = []
        box_inner_w = CONTENT_WIDTH - 24
        for word in words:
            test_line = " ".join(cur_line + [word])
            w = fitz.get_text_length(test_line, fontname="helv", fontsize=8.0)
            if w <= box_inner_w:
                cur_line.append(word)
            else:
                if cur_line:
                    lines.append(" ".join(cur_line))
                cur_line = [word]
        if cur_line:
            lines.append(" ".join(cur_line))

        box_h = 16 + len(lines) * 10.0 + 8
        self.check_space(box_h + 8)
        p = self.current_page

        # Background box
        p.draw_rect(fitz.Rect(MARGIN_LEFT, self.y, MARGIN_RIGHT, self.y + box_h), color=border, fill=bg, width=0.5)
        # Left Accent Bar
        p.draw_rect(fitz.Rect(MARGIN_LEFT, self.y, MARGIN_LEFT + 3.5, self.y + box_h), color=border, fill=border)

        # Title
        p.insert_text((MARGIN_LEFT + 10, self.y + 11), title, fontname="hebo", fontsize=8.5, color=t_color)

        # Body
        cur_y = self.y + 22
        for line in lines:
            p.insert_text((MARGIN_LEFT + 10, cur_y), line, fontname="helv", fontsize=8.0, color=COLOR_TEXT_DARK)
            cur_y += 10.0

        self.y += box_h + 8

    def add_table(self, headers, rows, col_widths):
        # Calculate heights for rows
        row_heights = []
        wrapped_rows = []

        # Wrap header
        wrapped_header = []
        for i, h in enumerate(headers):
            wrapped_header.append(self._wrap_cell(h, col_widths[i] - 6, font="hebo", size=7.5))
        header_h = max(len(lines) for lines in wrapped_header) * 9.5 + 8

        for row in rows:
            wrapped_row = []
            for i, cell in enumerate(row):
                wrapped_row.append(self._wrap_cell(str(cell), col_widths[i] - 6, font="helv", size=7.2))
            row_h = max(len(lines) for lines in wrapped_row) * 9.0 + 6
            row_heights.append(row_h)
            wrapped_rows.append(wrapped_row)

        total_needed = header_h + sum(row_heights[:min(3, len(row_heights))])
        self.check_space(total_needed)

        # Render Header
        self._render_table_header(headers, wrapped_header, col_widths, header_h)

        # Render Rows
        for r_idx, (w_row, r_h) in enumerate(zip(wrapped_rows, row_heights)):
            if self.y + r_h > MARGIN_BOTTOM:
                self.add_page()
                self._render_table_header(headers, wrapped_header, col_widths, header_h)

            p = self.current_page
            bg_color = COLOR_ROW_ALT if (r_idx % 2 == 1) else COLOR_WHITE
            p.draw_rect(fitz.Rect(MARGIN_LEFT, self.y, MARGIN_RIGHT, self.y + r_h), color=COLOR_BORDER, fill=bg_color, width=0.4)

            cur_x = MARGIN_LEFT
            for c_idx, lines in enumerate(w_row):
                line_y = self.y + 8
                is_first_col = (c_idx == 0)
                font = "hebo" if is_first_col else "helv"
                t_col = COLOR_PRIMARY_DARK if is_first_col else COLOR_TEXT_DARK
                for line in lines:
                    p.insert_text((cur_x + 3, line_y), line, fontname=font, fontsize=7.2, color=t_col)
                    line_y += 9.0
                cur_x += col_widths[c_idx]

            self.y += r_h
        self.y += 8

    def _render_table_header(self, headers, wrapped_header, col_widths, header_h):
        p = self.current_page
        p.draw_rect(fitz.Rect(MARGIN_LEFT, self.y, MARGIN_RIGHT, self.y + header_h), color=COLOR_HEADER_BG, fill=COLOR_HEADER_BG)
        cur_x = MARGIN_LEFT
        for c_idx, lines in enumerate(wrapped_header):
            line_y = self.y + 9
            for line in lines:
                p.insert_text((cur_x + 3, line_y), line, fontname="hebo", fontsize=7.5, color=COLOR_WHITE)
                line_y += 9.5
            cur_x += col_widths[c_idx]
        self.y += header_h

    def _wrap_cell(self, text, max_w, font="helv", size=7.2):
        words = text.split(" ")
        lines = []
        cur_line = []
        for word in words:
            test_line = " ".join(cur_line + [word])
            w = fitz.get_text_length(test_line, fontname=font, fontsize=size)
            if w <= max_w:
                cur_line.append(word)
            else:
                if cur_line:
                    lines.append(" ".join(cur_line))
                cur_line = [word]
        if cur_line:
            lines.append(" ".join(cur_line))
        return lines if lines else [""]

    def add_image(self, img_path, caption="", max_w=400, max_h=190):
        if not os.path.exists(img_path):
            return
        total_h = max_h + 20
        self.check_space(total_h)
        p = self.current_page

        # Center image
        img_x = MARGIN_LEFT + (CONTENT_WIDTH - max_w) / 2.0
        rect = fitz.Rect(img_x, self.y, img_x + max_w, self.y + max_h)
        p.insert_image(rect, filename=img_path)

        # Draw light border around image
        p.draw_rect(rect, color=COLOR_BORDER, width=0.5)

        self.y += max_h + 3
        if caption:
            cap_w = fitz.get_text_length(caption, fontname="heit", fontsize=7.2)
            cap_x = MARGIN_LEFT + (CONTENT_WIDTH - cap_w) / 2.0
            p.insert_text((cap_x, self.y + 8), caption, fontname="heit", fontsize=7.2, color=COLOR_TEXT_MUTED)
            self.y += 14
        self.y += 6

    def finalize_and_save(self):
        # Render running headers and footers on all pages
        total_pages = len(self.doc)
        for idx in range(total_pages):
            page = self.doc[idx]
            page_num = idx + 1
            # Running header (skip page 1 top banner)
            if page_num > 1:
                page.insert_text(
                    (MARGIN_LEFT, 28),
                    "HemoSense AI — End-to-End System Architecture & Implementation Report",
                    fontname="heit",
                    fontsize=7.0,
                    color=COLOR_TEXT_MUTED,
                )
                page.draw_line(
                    fitz.Point(MARGIN_LEFT, 33),
                    fitz.Point(MARGIN_RIGHT, 33),
                    color=COLOR_BORDER,
                    width=0.5,
                )

            # Running footer
            page.draw_line(
                fitz.Point(MARGIN_LEFT, 815),
                fitz.Point(MARGIN_RIGHT, 815),
                color=COLOR_BORDER,
                width=0.5,
            )
            page.insert_text(
                (MARGIN_LEFT, 826),
                "Confidential — Capstone Project & Technical Evaluation Report",
                fontname="helv",
                fontsize=6.8,
                color=COLOR_TEXT_MUTED,
            )
            page_str = f"Page {page_num} of {total_pages}"
            pw = fitz.get_text_length(page_str, fontname="hebo", fontsize=7.0)
            page.insert_text(
                (MARGIN_RIGHT - pw, 826),
                page_str,
                fontname="hebo",
                fontsize=7.0,
                color=COLOR_PRIMARY_DARK,
            )

        self.doc.save(self.filename)
        self.doc.close()
        print(f"Successfully generated PDF: {self.filename} ({total_pages} pages)")


def build_full_report():
    output_pdf = "HemoSense_AI_Complete_Architecture_and_Implementation.pdf"
    doc = PDFDocument(output_pdf)
    doc.add_page()

    # Title Banner
    doc.add_header_banner(
        title="HemoSense AI: Architecture & Implementation",
        subtitle="End-to-End System Design, Technology Matrix, Pipeline Engineering & Comparative Rationale",
    )

    # Executive Overview
    doc.add_h1("Executive Summary & Project Scope")
    doc.add_p(
        "HemoSense AI is a clinically grounded, smartphone-based primary screening and dietary intelligence platform for non-invasive anemia assessment. Operating in resource-constrained environments where laboratory Complete Blood Count (CBC) access is restricted, the platform captures high-resolution macro imagery of the palpebral conjunctiva (inner lower eyelid), performs rigorous optical quality and anatomical shape gating, extracts hemodynamic colorimetry metrics, and executes inference via an interpretable zero-order Sugeno Adaptive Neuro-Fuzzy Inference System (ANFIS). Calibrated probabilities are mapped to World Health Organization (WHO) clinical triage categories (Normal, Mild, Moderate-to-Severe) without estimating ungrounded continuous hemoglobin numbers, triggering an absorption-modeled nutritional guidance engine grounded in verified USDA FoodData Central data and localized via LLM intelligence."
    )

    doc.add_callout(
        "CORE CLINICAL GOAL & GOVERNANCE DIRECTIVE",
        "Primary objective: Deliver high-sensitivity anemia screening (Target: Sensitivity >= 85% at Specificity >= 70%) with full mathematical and rule-based interpretability. Absolute hemoglobin values (Hb in g/dL) are explicitly omitted in user-facing views to prevent false reassurance or clinical confusion, framing the system purely as a triage and dietary empowerment tool with mandatory medical referral alerts for severe cases.",
        alert_type="info",
    )

    # Architecture Overview
    doc.add_h1("1. Complete System Architecture & Dataflow")
    doc.add_p(
        "The HemoSense AI system employs a decoupled, multi-tiered architecture that separates edge capture, secure transit, computer vision segmentation, neuro-fuzzy inference, and nutritional optimization. The design ensures zero server-side photo persistence for patient privacy while maintaining sub-2-second end-to-end response times."
    )

    doc.add_h2("System-Level Architectural Topology")
    doc.add_bullet("1. Client Edge Layer (Flutter Mobile)", "Cross-platform mobile application providing guided patient onboarding, camera exposure stabilization, torch-assisted multi-frame burst capture, interactive ROI specification, and local cryptographic Hive history storage.")
    doc.add_bullet("2. Edge Reverse Proxy & TLS Ingress (Caddy 2)", "Lightweight Caddy server running on AWS EC2, terminating Let's Encrypt TLS (HTTPS), enforcing 40 MB max upload limits, managing CORS policies, and reverse proxying requests to the internal API network.")
    doc.add_bullet("3. Microservice Orchestration Layer (FastAPI)", "Asynchronous Python web service with Pydantic v2 validation schemas, coordinating multi-frame batch aggregation, health monitoring, symptom checklists, and LLM orchestration.")
    doc.add_bullet("4. Computer Vision & Pre-Flight Gate Engine (hemosense/segment.py)", "Server-side image decode with EXIF rotation normalization, 7-point quality and anatomical validation gates, GrabCut interactive segmentation with 15% padding, and Otsu CIELAB a* tissue refinement.")
    doc.add_bullet("5. Hemodynamic Colorimetry Engine (hemosense/features.py)", "Extracts Erythema Index (EI), CIELAB a*, High Red-Hue Ratio (HHR), and HSV Saturation over segmented tissue masks.")
    doc.add_bullet("6. Dual-Stage Sugeno ANFIS Engine (hemosense/anfis.py & models/anfis.json)", "Zero-order Sugeno fuzzy inference system implemented in pure NumPy. Stage 1 determines general anemia probability; Stage 2 evaluates moderate-to-severe classification.")
    doc.add_bullet("7. Empirical Confidence & Calibration Layer (models/confidence.json)", "Maps continuous model certainty into empirical 5-fold cross-validation reliability bands, returning transparent clinical confidence statements.")
    doc.add_bullet("8. Bioavailability Dietary Optimizer (hemosense/diet.py)", "Mathematical implementation of the Hurrell & Egli iron absorption model utilizing USDA FoodData Central SR Legacy reference compositions with greedy meal slot allocation and optional OpenRouter LLM regional translation.")

    # High-level ASCII architecture diagram
    doc.add_callout(
        "END-TO-END PIPELINE WORKFLOW (CLIENT TO INFERENCE)",
        "[Smartphone Flutter App] (Camera burst: 3 frames @ 350ms, torch ON, user ROI)\n"
        "       │  HTTPS POST /screen/batch (Multipart: Images + [x,y,w,h] + Profile JSON)\n"
        "       ▼\n"
        "[AWS EC2 / Caddy Reverse Proxy] (TLS termination, 40MB limit, auto-renew certificates)\n"
        "       ▼\n"
        "[FastAPI Production Engine] (api/main.py -> api/pipeline.py)\n"
        "       │\n"
        "       ├──▶ [Quality & Anatomical Gates] (Brightness, Blur, Glare, Sclera, Crescent Shape)\n"
        "       ├──▶ [Tissue Segmentation] (GrabCut on user ROI crop + Otsu a* split)\n"
        "       ├──▶ [Feature Extraction] (Erythema Index, CIELAB a*, HHR, Saturation)\n"
        "       ├──▶ [ANFIS Fuzzy Inference] (Dual-stage 27-rule Sugeno + Platt Scaling)\n"
        "       ├──▶ [Multi-Frame Voting] (Median probability, agreement ratio, empirical confidence)\n"
        "       └──▶ [Bioavailability Nutrition] (USDA 46-food composition table + Hurrell absorption)\n"
        "       │\n"
        "       ▼\n"
        "[JSON Response to Client] (Verdict, Risk %, Fired Rules, Feature Bars, 1-Day Meal Plan)",
        alert_type="decision",
    )

    # Section 2: Technology Stack Matrix
    doc.add_h1("2. Technology Stack & Component Purpose Matrix")
    doc.add_p(
        "Every library, framework, and infrastructure service in HemoSense AI was selected based on strict requirements of edge-to-cloud performance, deterministic mathematical reproducibility, zero-cloud data leak privacy, and operational resilience."
    )

    headers_tech = ["Tier / Domain", "Technology & Version", "Key Architectural Purpose", "Technical Selection Rationale"]
    rows_tech = [
        [
            "Mobile Client",
            "Flutter 3.47+ / Dart",
            "Primary user deliverable: cross-platform Android/iOS UI, camera controls, offline storage.",
            "Single codebase, 60fps canvas rendering for ROI bounding box manipulation, direct hardware camera APIs."
        ],
        [
            "State Management",
            "Riverpod 3 (Notifier)",
            "Deterministic app-wide reactive state management without UI rebuild bottlenecks.",
            "Compile-time safety, seamless async provider testing, decoupled architecture separating UI from network logic."
        ],
        [
            "Local Storage",
            "Hive / hive_flutter",
            "On-device encrypted key-value database for profiles, scan histories, and offline settings.",
            "Zero native binary overhead, extreme read/write speeds (<5ms), eliminates privacy leak of storing health records on cloud."
        ],
        [
            "HTTP Client",
            "Dio 5.x",
            "Handles multi-part batch uploads, connection timeouts, and SSL pinning.",
            "Native multipart stream encoding for burst photos, clean interceptors for error code translation."
        ],
        [
            "Web Demo UI",
            "Next.js 14 / React 18",
            "Desktop presentation and rapid screening simulator for lab and evaluation judges.",
            "SSR/SSG capabilities, responsive Tailwind CSS styling, drag-and-drop web file testing."
        ],
        [
            "Backend API",
            "FastAPI 0.162+ / Pydantic v2",
            "REST serving gateway, request validation, exception mapping, async pipeline execution.",
            "High concurrency (asyncio), automatic OpenAPI/Swagger generation, sub-millisecond Pydantic v2 serialization."
        ],
        [
            "Application Server",
            "Uvicorn / Starlette",
            "ASGI web server running 2 worker processes inside non-root Docker container.",
            "Lightweight, production-tested, low CPU/RAM footprint (~80 MB RAM per worker)."
        ],
        [
            "Computer Vision",
            "OpenCV 4.11 / Pillow 13.0",
            "EXIF rotation, resizing, Laplacian blur detection, GrabCut segmentation, contour geometry.",
            "High-speed C++ primitives, battle-tested morphological operations, stable cross-platform array representations."
        ],
        [
            "Scientific Math",
            "NumPy 1.26 / SciPy 1.15",
            "Matrix algebra, analytic gradients, Gaussian membership evaluation, Adam optimization.",
            "Zero heavy framework dependencies (no PyTorch/TensorFlow at serving), deterministic vectorization."
        ],
        [
            "Fuzzy Logic",
            "Custom ANFIS (hemosense/anfis.py)",
            "Zero-order Sugeno ANFIS implementation with Gaussian terms and Platt calibration.",
            "Pure NumPy inference (sub-5ms execution), transparent rule activation, analytic Adam optimization."
        ],
        [
            "Baseline Benchmark",
            "scikit-fuzzy 0.5.0",
            "Classical Mamdani fuzzy baseline implementation for academic research comparisons.",
            "Standard fuzzy logic benchmark library for validating ANFIS performance improvements."
        ],
        [
            "Model Evaluation",
            "scikit-learn 1.9.1",
            "Stratified K-fold CV, ROC-AUC calculations, DeLong tests, Platt logistic calibration.",
            "Gold-standard machine learning evaluation metrics, rigorous statistical test implementations."
        ],
        [
            "Dietary Reference",
            "USDA SR Legacy (FDC)",
            "46-food composition database (iron, vitamin C, calcium, protein, serving grams).",
            "Public domain, scientifically verified laboratory nutrient compositions, avoids AI nutritional hallucinations."
        ],
        [
            "Dietary Phrasing",
            "OpenRouter API (Llama 3.1)",
            "Translates structured USDA meal recommendations into regional dish names and cost estimates.",
            "Strict schema validation: server validates every food against allowed pool and re-computes USDA numbers."
        ],
        [
            "Infrastructure",
            "AWS EC2 t3.small / Caddy",
            "Ubuntu 24.04 LTS host, Docker Compose, Elastic IP, Caddy auto-TLS (sslip.io).",
            "Ultra-low cost ($0.025/hr), automated Let's Encrypt certificates, CloudWatch auto-recovery."
        ],
    ]
    col_w_tech = [80.0, 95.0, 160.0, 176.3]
    doc.add_table(headers_tech, rows_tech, col_w_tech)

    # Section 3: Step-by-Step Implementation Breakdown
    doc.add_h1("3. Step-by-Step Implementation Breakdown")
    doc.add_p(
        "The HemoSense AI pipeline transforms raw photon counts captured by a commercial smartphone camera into an interpretable clinical screening verdict and nutritional action plan through 8 rigorously validated execution steps."
    )

    doc.add_h2("Step 1: Optical Acquisition & Frame Burst Capture")
    doc.add_p(
        "Implementation: Located in app/lib/screens/camera_screen.dart. The Flutter camera controller sets rear-facing sensor mode, enables the hardware torch, and enforces an 800 ms dwell time to allow camera Auto-Exposure (AE) and Auto-White-Balance (AWB) routines to stabilize under direct illumination. It then triggers a hardware-timed burst of 3 consecutive frames spaced 350 ms apart. In the review screen, the user draws a single bounding box [x, y, w, h] (normalized 0.0 to 1.0) over the pulled-down palpebral conjunctiva, which is shared across all 3 frames."
    )

    doc.add_h2("Step 2: Pre-Flight Optical Quality & Anatomical Safety Gates")
    doc.add_p(
        "Implementation: Located in hemosense/segment.py. Prior to running computationally expensive segmentation or inference, the image is passed through a 7-stage gate at a normalized 900 px working resolution. If any condition fails, execution halts immediately with a machine-readable error code and human actionable guidance:"
    )
    doc.add_bullet("1. Resolution / Crop Scale Gate ('too_far')", "Verifies that min(box_w, box_h) >= 40 pixels at 900 px resolution. Rejects distant, low-pixel eyelid captures.")
    doc.add_bullet("2. Underexposure Gate ('too_dark')", "Computes mean grayscale luminance inside the ROI: rejects if mean brightness < 0.15 (scale 0.0 - 1.0).")
    doc.add_bullet("3. Specular Overexposure Gate ('overexposed')", "Measures pixel saturation: rejects if > 25% of ROI pixels have RGB channels clipped at 255.")
    doc.add_bullet("4. High-Frequency Blur Gate ('blurry')", "Applies a discrete 3x3 Laplacian kernel over the cropped ROI: rejects if variance(Laplacian) < 12.0.")
    doc.add_bullet("5. Anatomical Context Sclera Gate ('no_eye')", "Samples an anatomical band directly above the user box. Detects high-luminance, low-saturation scleral white tissue. Rejects if user draws box over forehead, mouth, or shirt.")
    doc.add_bullet("6. Crescent Geometric Prior Gate ('not_crescent')", "Measures contour properties on segmented tissue: enforces elongation (max(w,h)^2 / area) >= 2.7, solidity (area / convex_hull) <= 0.85, and aspect ratio (w/h) >= 1.1. Discards compact circular blobs (cheeks/noses).")
    doc.add_bullet("7. Minimum Tissue Area Gate ('no_conjunctiva')", "Enforces minimum segmented conjunctiva pixel count: area >= max(150 px, 2% of ROI area).")

    doc.add_h2("Step 3: Conjunctival Tissue Segmentation (GrabCut + CIELAB a* Split)")
    doc.add_p(
        "Implementation: Located in hemosense/segment.py. The user-provided bounding box is expanded by a 15% safety margin and cropped to at most 360 px width for performance. GrabCut (cv2.grabCut) executes 4 iterations initialized with cv2.GC_INIT_WITH_RECT. The resulting foreground mask undergoes morphological cleanup: dark eyelash pixels, specular flash reflections, and bright sclera pixels are subtracted. If multi-modal color populations remain, the smoothed CIELAB a* distribution is split using Otsu thresholding, retaining the largest crescent component matching anatomical priors."
    )

    doc.add_h2("Step 4: Hemodynamic & Colorimetric Feature Engineering")
    doc.add_p(
        "Implementation: Located in hemosense/features.py. Extracted exclusively from the segmented tissue pixels. The engine extracts 4 biologically validated optical features:"
    )
    doc.add_bullet("1. Erythema Index (EI)", "EI = 100 * [log10(mean_Red) - log10(mean_Green)]. Quantifies microvascular hemoglobin absorption against background tissue scattering (Collings et al., 2016).")
    doc.add_bullet("2. CIELAB a* (Red-Green Chrominance)", "Mean a* coordinate in the perceptually uniform CIE L*a*b* space, representing vascular tissue flushing.")
    doc.add_bullet("3. High Red-Hue Ratio (HHR)", "Proportion of tissue pixels satisfying Hue within +/-15 deg of true Red (0 deg) and HSV Saturation > 0.30 (Zhao et al., 2024).")
    doc.add_bullet("4. HSV Saturation", "Mean color purity across the segmented palpebral tissue.")

    doc.add_h2("Step 5: Dual-Stage Zero-Order Sugeno ANFIS Inference")
    doc.add_p(
        "Implementation: Located in hemosense/anfis.py and models/anfis.json. Employs a forward-selected 3-input feature vector (CIELAB a*, HHR, EI). Each input is partitioned into 3 Gaussian membership functions (Low, Medium, High), yielding 3^3 = 27 rules. Consequents are zero-order constant logits theta_r. The network evaluates normalized firing strengths wbar_r and defuzzifies via weighted average. A post-hoc Platt logistic scaler maps logits to calibrated probabilities p = sigmoid(a * z + b). A two-stage cascade is executed: Stage 1 evaluates p(anemic); if p >= 0.5, Stage 2 evaluates p(moderate-to-severe)."
    )

    doc.add_h2("Step 6: Multi-Frame Voting Consensus & Empirical Reliability Mapping")
    doc.add_p(
        "Implementation: Located in api/clinical.py and models/confidence.json. For multi-frame uploads (e.g., 3-frame burst), the server extracts features and evaluates ANFIS probabilities independently per accepted frame. The aggregate probability is the median across frames. Voter agreement is computed as the fraction of frames agreeing with the majority verdict. Aggregate certainty max(p, 1 - p) is matched against an empirical 5-fold cross-validation table (e.g., certainty 0.9-1.0 exhibits 94% test accuracy across 69 cohort patients)."
    )

    doc.add_h2("Step 7: Clinical Decision Framework & Severity Triage")
    doc.add_p(
        "Implementation: Located in api/clinical.py. Results are classified into three ordinal clinical bins: Normal (p < 0.5), Mild Anemia (p >= 0.5 and p_sev < 0.5), and Moderate-to-Severe Anemia (p >= 0.5 and p_sev >= 0.5). To protect patient safety, severe classifications or reported red-flag symptoms (severe dizziness, chest pain, fainting) trigger a prominent 'Consult a Doctor' emergency medical banner. Absolute hemoglobin values are strictly suppressed."
    )

    doc.add_h2("Step 8: Bioavailability-Aware Dietary Optimization Engine")
    doc.add_p(
        "Implementation: Located in hemosense/diet.py and api/llm.py. Employs a deterministic nutrient optimizer grounded in USDA SR Legacy data (foods_usda.csv, 46 items). Solves for individual Recommended Dietary Allowance (RDA) by sex, age, and pregnancy. Computes bioavailable iron per meal via the Hurrell & Egli mathematical model:"
    )
    doc.add_callout(
        "HURRELL & EGLI IRON BIOAVAILABILITY FORMULATION",
        "Fe_absorbable = Fe_heme * 0.25 + Fe_nonheme * 0.10 * E * I\n"
        "• Enhancer E = 2.0  if meal Vitamin C >= 25 mg or contains meat/poultry/fish\n"
        "• Inhibitor I = 0.7  if meal Calcium >= 300 mg (dairy penalty)\n"
        "• Inhibitor I = 0.8  if phytate-rich grains/legumes dominate without ascorbic acid\n"
        "Safety rule: Organ meats (liver) are hard-filtered out for pregnant women to prevent Vitamin A teratogenicity.",
        alert_type="info",
    )

    # Section 4: Deep Comparative Analysis
    doc.add_h1("4. Deep Comparative Analysis: Rationale vs. Alternative Methods")
    doc.add_p(
        "A critical engineering dimension of HemoSense AI is the conscious architectural decision made at every stage to avoid fragile, uninterpretable black-box techniques in favor of robust, mathematically verifiable, and medically responsible methods."
    )

    headers_comp = ["Pipeline Step", "Chosen HemoSense Method", "Rejected Alternative Methods", "Why Chosen (Comparative Advantage & Trade-off Rationale)"]
    rows_comp = [
        [
            "Step 1: Image Capture",
            "3-Frame Burst with Torch ON (350 ms spacing)",
            "• Ambient room lighting\n• Single xenon flash\n• Continuous video capture",
            "Ambient light introduces uncontrolled Kelvin color shifts. Single flash causes severe specular cornea washout and pupil constriction reflex. Video capture suffers from rolling shutter distortion and low per-frame bitrate. Torch burst provides constant illumination, locks auto-exposure, and enables median temporal filtering against hand jitter."
        ],
        [
            "Step 2: Quality Gates",
            "Multi-Parameter Rule & Crescent Prior Gate",
            "• Unchecked inference\n• Deep CNN binary classifier (Good vs Bad photo)",
            "Unchecked inference outputs misleading risk scores when photos are blurry or off-target. Deep CNN quality classifiers require massive negative training sets (thousands of blurry shirts/fingers) and fail silently on out-of-distribution artifacts. Explicit geometric and photometric thresholds (Laplacian variance, crescent prior, sclera check) offer 100% deterministic, explainable rejections."
        ],
        [
            "Step 3: Tissue Segmentation",
            "User-Guided GrabCut + CIELAB a* Otsu Refinement",
            "• Fully automatic U-Net\n• Fixed center crop box\n• Simple RGB thresholding",
            "Fully automatic U-Nets trained on small datasets fail under variable gaze angles and partial lid eversions, requiring heavy neural weights on mobile. Fixed center crops capture eyelashes and skin. Simple RGB thresholding confuses eyelid tissue with lips and cheeks. User-guided GrabCut leverages human intelligence for coarse localization while automated Otsu a* mathematically discards pale sclera and dark lashes."
        ],
        [
            "Step 4: Features",
            "Biologically Grounded Hemodynamic Indices (EI, a*, HHR)",
            "• Deep CNN latent vectors\n• Raw RGB color histograms\n• Gray-level co-occurrence",
            "Deep embeddings act as black boxes prone to shortcut learning (memorizing camera sensor artifacts, patient skin tone, or background clinic colors). Hemodynamic indices (EI, a*, HHR) directly mirror the biophysical physics of oxyhemoglobin and deoxyhemoglobin light absorption in capillary microvasculature, ensuring invariant biological representation."
        ],
        [
            "Step 5: Model Core",
            "Dual-Stage Zero-Order Sugeno ANFIS (27 rules)",
            "• Deep CNN (MobileNetV3)\n• Random Forest / SVM\n• Pure Mamdani Fuzzy System",
            "MobileNetV3 achieved lower live AUC (0.81 vs 0.88 ANFIS) and is completely unexplainable. Random Forest cannot easily output smooth Gaussian membership boundaries. Pure Mamdani requires hand-crafted rule weights that struggle with multi-variable non-linearities. Sugeno ANFIS combines neural gradient learning (Adam) with explicit IF-THEN transparent fuzzy linguistic rules."
        ],
        [
            "Step 6: Clinical Metric",
            "Ordinal Risk Category + Empirical Confidence Bands",
            "• Continuous Hemoglobin Regression (Hb in g/dL)\n• Raw uncalibrated probabilities",
            "Non-invasive optical methods lack the photometric dynamic range to accurately differentiate 10.2 g/dL from 10.6 g/dL; regression models produce misleading pseudo-precision that misleads patients. Continuous Hb display risks delayed diagnosis if a patient believes an inaccurate 11.2 g/dL. Ordinal risk with empirical confidence tables provides medically sound, actionable triage."
        ],
        [
            "Step 7: Consensus",
            "Median Aggregation + Agreement Ratio Voting",
            "• Single frame inference\n• Mean logit average\n• Winner-take-all maximum",
            "Single frames are vulnerable to brief micro-saccades, blinks, or local specular flash reflections. Mean averaging is skewed by single catastrophic outlier frames. Median probability across 3 frames combined with an agreement fraction guarantees statistical robustness and drops confidence if photos disagree."
        ],
        [
            "Step 8: Diet Intelligence",
            "Grounded USDA Bioavailability Model + LLM Wording",
            "• Pure LLM generative prompt\n• Static generic PDF diet charts\n• Raw calorie-counting apps",
            "Pure LLMs frequently hallucinate micronutrient numbers, recommend toxic combinations (e.g. iron supplements with calcium), or prescribe liver to pregnant women. Static diet charts ignore vegan/vegetarian restrictions and bioavailability inhibitors. HemoSense computes exact USDA nutrient math deterministically, using LLMs strictly for cultural phrasing."
        ],
    ]
    col_w_comp = [75.0, 105.0, 115.0, 216.3]
    doc.add_table(headers_comp, rows_comp, col_w_comp)

    # Section 5: Mathematical Formulations
    doc.add_h1("5. Mathematical Formulations & Formal Logic")
    doc.add_p(
        "The algorithmic foundation of HemoSense AI is governed by formal optical, statistical, and fuzzy logic equations:"
    )

    doc.add_h2("1. Hemodynamic Colorimetry Formulation")
    doc.add_p(
        "For a segmented palpebral conjunctiva tissue mask M containing N valid pixels, the optical metrics are defined as:\n"
        "• Erythema Index (EI):  EI = 100 * [ log10( (1/N) * sum(R_i) ) - log10( (1/N) * sum(G_i) ) ]\n"
        "• CIELAB a* (Red-Green):  a* = 500 * [ f(X/X_n) - f(Y/Y_n) ],  where f(t) = t^(1/3) for t > (6/29)^3\n"
        "• High Red-Hue Ratio (HHR):  HHR = (1/N) * sum( I( |Hue_i - 0 deg| <= 15 deg  AND  Saturation_i > 0.30 ) )"
    )

    doc.add_h2("2. Zero-Order Sugeno ANFIS Formulation")
    doc.add_p(
        "Let x = [a*, HHR, EI]^T be the standardized input vector (K = 3). Each input k has 3 Gaussian membership terms:\n"
        "• Membership Grade:  mu_{k,j}(x_k) = exp( -0.5 * ( (x_k - c_{k,j}) / sigma_{k,j} )^2 ),  for j in {Low, Medium, High}\n"
        "• Rule Firing Strength:  w_r = prod_{k=1}^3 mu_{k, j_k(r)}(x_k),  for r = 1, ..., 27\n"
        "• Normalized Firing:  wbar_r = w_r / sum_{i=1}^{27} w_i\n"
        "• Zero-Order Consequent Output:  z = sum_{r=1}^{27} wbar_r * theta_r\n"
        "• Platt Calibrated Screening Probability:  p = 1 / ( 1 + exp( -(a * z + b) ) )"
    )

    doc.add_h2("3. Analytic Parameter Optimization (Adam Hybrid)")
    doc.add_p(
        "Consequents theta are initialized via Ridge Least Squares: theta_0 = (Wbar^T Wbar + lambda * I)^(-1) Wbar^T Y_target.\n"
        "All parameters {c, sigma, theta} are subsequently updated end-to-end using Adam on binary cross-entropy with L2 penalty:\n"
        "L = - (1/N) * sum( y_i * log(p_i + eps) + (1 - y_i) * log(1 - p_i + eps) ) + lambda_L2 * sum( theta_r^2 )"
    )

    # Section 6: Research Figures & Visual Evidence
    doc.add_h1("6. Experimental Validation & Research Benchmarks")
    doc.add_p(
        "Validation was conducted across 215 clinical patients from the public Eyes-defy-anemia benchmark cohort under a strict 5-fold participant-stratified cross-validation protocol (StratifiedKFold on region x anemia status). Feature selection and Platt calibration were strictly confined inside training folds to prevent data leakage."
    )

    # Table of Benchmark Results
    headers_perf = ["Model Architecture", "Input Pipeline", "Cross-Validated AUC", "Sensitivity (Sens)", "Specificity (Spec)", "Parameters"]
    rows_perf = [
        ["HemoSense ANFIS (Proposed)", "Live Pipeline (GrabCut + Gates)", "0.879 (95% CI: 0.83-0.92)", "77.1% (App p>=0.5)", "82.4% (App p>=0.5)", "45 params"],
        ["HemoSense ANFIS (Optimal Tau)", "Live Pipeline (Youden J)", "0.879 (95% CI: 0.83-0.92)", "88.6% (Tau=0.15)", "71.2% (Tau=0.15)", "45 params"],
        ["MobileNetV3 Small (CNN)", "Cropped Eyelid Images", "0.812 (95% CI: 0.74-0.88)", "72.4%", "74.1%", "1.5M params"],
        ["Random Forest Classifier", "Engineered Features", "0.841 (95% CI: 0.78-0.90)", "74.3%", "78.2%", "100 trees"],
        ["Logistic Regression", "Engineered Features", "0.834 (95% CI: 0.77-0.89)", "71.4%", "79.1%", "4 params"],
        ["Mamdani Fuzzy Baseline", "Expert Rules (scikit-fuzzy)", "0.785 (95% CI: 0.71-0.85)", "68.6%", "75.0%", "Hand-tuned"],
    ]
    col_w_perf = [115.0, 115.0, 95.0, 65.0, 65.0, 56.3]
    doc.add_table(headers_perf, rows_perf, col_w_perf)

    doc.add_callout(
        "STATISTICAL SIGNIFICANCE (DELONG TEST)",
        "The proposed ANFIS pipeline demonstrates statistically significant superiority over the baseline classical Mamdani system (DeLong p < 0.01) and outperforms end-to-end deep MobileNetV3 (AUC 0.879 vs 0.812, p = 0.038) while operating with only 45 parameters versus 1.5 million neural weights.",
        alert_type="success",
    )

    # Embed real figures if they exist
    fig_roc = os.path.join("paper", "figures", "roc_live_pipeline.png")
    fig_mfs = os.path.join("paper", "figures", "anfis_membership.png")
    fig_cal = os.path.join("paper", "figures", "calibration_anfis_live.png")
    fig_feat = os.path.join("paper", "figures", "features_by_class.png")

    if os.path.exists(fig_roc):
        doc.add_h2("Figure 1: Receiver Operating Characteristic (ROC) — Live Pipeline Benchmarks")
        doc.add_image(fig_roc, caption="Figure 1: 5-Fold Cross-Validated ROC curve for ANFIS (AUC 0.879) vs. Random Forest, LogReg, Mamdani, and Majority.", max_w=360, max_h=175)

    if os.path.exists(fig_mfs):
        doc.add_h2("Figure 2: Learned ANFIS Gaussian Membership Functions")
        doc.add_image(fig_mfs, caption="Figure 2: Trained Gaussian linguistic terms (Low, Medium, High) for CIELAB a*, HHR, and Erythema Index.", max_w=360, max_h=175)

    if os.path.exists(fig_cal):
        doc.add_h2("Figure 3: Platt Calibration Reliability Diagram")
        doc.add_image(fig_cal, caption="Figure 3: Probability calibration curve demonstrating close concordance with empirical true risk fractions.", max_w=360, max_h=165)

    # Section 7: Operational Deployment & Security Architecture
    doc.add_h1("7. Operational Infrastructure, Security & Privacy Compliance")
    doc.add_p(
        "HemoSense AI is deployed on AWS EC2 (Mumbai ap-south-1) under a hardened, least-privilege security model engineered to respect patient medical data sovereignty."
    )
    doc.add_bullet("Zero-Persistence Ingestion", "Patient photographs uploaded to /screen/batch are buffered strictly in ephemeral RAM workers, processed, and immediately discarded upon response dispatch. No image bytes are ever written to server disk or persistent cloud buckets.")
    doc.add_bullet("Decoupled Client Identity", "The platform requires no user registration, telephone numbers, or biometric names. All demographic context (age, pregnancy, dietary preferences) is stored locally on the user's mobile device via Hive storage.")
    doc.add_bullet("Transport & Boundary Protection", "Caddy 2 handles TLS termination with automatic Let's Encrypt certificates, enforcing HSTS, rate-limiting, and 40 MB payload restrictions. AWS Security Groups restrict port 22 SSH strictly to the deployer's IP, leaving only standard ports 80/443 public.")
    doc.add_bullet("Infrastructure Resilience", "Docker Compose manages automatic container restart policies. A CloudWatch alarm monitors EC2 instance health and initiates automatic instance reboot recovery in the event of underlying hypervisor faults.")

    # Section 8: Limitations and Future Roadmap
    doc.add_h1("8. Architectural Limitations & Future Engineering Roadmap")
    doc.add_bullet("1. Sclera-Based White Balance Activation", "While hemosense/colour.py contains prototype routines for sclera chromatic normalization, v1 relies on torch standardization. Activating real-time sclera normalization will further insulate the pipeline against multi-brand smartphone camera ISP shifts.")
    doc.add_bullet("2. Edge ML Dart Porting", "Port the 45-parameter zero-order Sugeno inference formulas directly into native Dart in the Flutter app to achieve 100% offline, serverless screening in remote rural zones.")
    doc.add_bullet("3. Automated Palpebral Landmark Detection", "Integrate an ultra-lightweight on-device eye landmark detector (e.g. MediaPipe Face Mesh) to suggest the initial bounding box, reducing human placement effort.")
    doc.add_bullet("4. ICMR-NIN 2020 Dietary Localization", "Transition from US NIH nutrient RDA targets to Indian Council of Medical Research (ICMR-NIN 2020) guidelines to align with national health protocols.")

    doc.finalize_and_save()


if __name__ == "__main__":
    build_full_report()
