"""
generate_flowchart.py
Generates Image 3:
Flowchart: capture -> box -> quality gate -> segmentation -> features -> ANFIS -> grade + explanation -> diet
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

def create_flowchart(output_path):
    fig, ax = plt.subplots(figsize=(15, 11), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 11)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    # Header Title
    ax.text(7.5, 10.6, "HemoSense AI: Screening & Dietary Intelligence Flowchart",
            fontsize=16, fontweight="bold", ha="center", va="center", color="#7A1734")
    ax.text(7.5, 10.3, "Step-by-Step Technical Execution Logic: From Image Ingestion to Clinical Triage & Micronutrient Bioavailability",
            fontsize=9.0, fontstyle="italic", ha="center", va="center", color="#64748B")

    # Flowchart layout: Vertical flow with branches
    # X coordinates: Main trunk at x = 4.5, Rejected branch at x = 11.5

    def draw_box(x, y, w, h, title, subtitle, bg_color="#FFFFFF", border_color="#B4264A", text_color="#7A1734", sub_color="#334155", lw=1.5):
        box = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.06,rounding_size=0.12",
                             facecolor=bg_color, edgecolor=border_color, linewidth=lw)
        ax.add_patch(box)
        ax.text(x, y + h*0.20, title, fontsize=8.0, fontweight="bold", ha="center", va="center", color=text_color)
        ax.text(x, y - h*0.20, subtitle, fontsize=6.8, ha="center", va="center", color=sub_color)

    def draw_diamond(x, y, w, h, title, subtitle, bg_color="#FEF3C7", border_color="#D97706"):
        # Diamond shape
        pts = [[x, y + h/2], [x + w/2, y], [x, y - h/2], [x - w/2, y]]
        diamond = patches.Polygon(pts, closed=True, facecolor=bg_color, edgecolor=border_color, linewidth=1.8)
        ax.add_patch(diamond)
        ax.text(x, y + 0.12, title, fontsize=8.0, fontweight="bold", ha="center", va="center", color="#92400E")
        ax.text(x, y - 0.18, subtitle, fontsize=6.5, ha="center", va="center", color="#B45309")

    def draw_arrow(x1, y1, x2, y2, color="#B4264A", label="", label_pos=(0, 0), lw=2.0):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor=color, edgecolor=color, width=lw, headwidth=6.0))
        if label:
            lx = (x1 + x2)/2 + label_pos[0]
            ly = (y1 + y2)/2 + label_pos[1]
            ax.text(lx, ly, label, fontsize=7.2, fontweight="bold", color=color, ha="center", va="center")

    # Main Steps Definition
    main_x = 5.2
    
    # Step 1: Optical Acquisition
    draw_box(main_x, 9.6, 6.6, 0.75, "STEP 1: SMARTPHONE OPTICAL CAPTURE",
             "Hardware torch ON (locks auto-exposure) | 3-frame burst spaced 350 ms apart",
             bg_color="#FDF8F9", border_color="#B4264A", text_color="#7A1734")

    # Arrow 1 -> 2
    draw_arrow(main_x, 9.22, main_x, 8.78)

    # Step 2: Interactive ROI Specification
    draw_box(main_x, 8.4, 6.6, 0.75, "STEP 2: USER EYELID ROI SPECIFICATION",
             "Patient/worker draws bounding box [x, y, w, h] tightly over lower palpebral conjunctiva",
             bg_color="#FDF8F9", border_color="#B4264A", text_color="#7A1734")

    # Arrow 2 -> 3
    draw_arrow(main_x, 8.02, main_x, 7.48)

    # Step 3: Decision Diamond - 7-Stage Pre-Flight Quality Gate
    draw_diamond(main_x, 6.9, 7.2, 1.15, "STEP 3: 7-STAGE QUALITY & ANATOMICAL GATES",
                 "Scale >= 40px | Luminance [0.15, 0.95] | Blur Var(Laplacian) >= 12 | Sclera & Crescent Prior")

    # Branch: FAILED Quality Gate (Right Arrow)
    draw_arrow(main_x + 3.6, 6.9, 10.8, 6.9, color="#DC2626", label="FAILED (Reject)", label_pos=(0, 0.22))

    # Error Box (Right Side)
    err_box = FancyBboxPatch((10.8, 5.8), 3.6, 2.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                             facecolor="#FEF2F2", edgecolor="#DC2626", linewidth=1.8)
    ax.add_patch(err_box)
    ax.text(12.6, 7.7, "HTTP 422 REJECTION", fontsize=8.5, fontweight="bold", ha="center", va="center", color="#991B1B")
    err_lines = [
        "• too_far: Box < 40px at 900px scale",
        "• too_dark: Grayscale luminance < 0.15",
        "• overexposed: > 25% pixels clipped at 255",
        "• blurry: Laplacian variance < 12.0",
        "• no_eye: No white sclera detected above",
        "• not_crescent: Solidity > 0.85 (skin blob)",
        "• no_conjunctiva: Tissue area < 150px",
        "Action: User guided to reposition or retake"
    ]
    ey = 7.35
    for el in err_lines:
        ax.text(11.0, ey, el, fontsize=6.2, color="#7F1D1D")
        ey -= 0.19

    # Branch: PASSED Quality Gate (Down Arrow)
    draw_arrow(main_x, 6.32, main_x, 5.78, color="#16A34A", label="PASSED", label_pos=(0.45, 0))

    # Step 4: Tissue Segmentation
    draw_box(main_x, 5.4, 6.6, 0.75, "STEP 4: PALPEBRAL TISSUE SEGMENTATION",
             "GrabCut initialized on 15% padded ROI (4 iter) + Morphological filter + Otsu a* split",
             bg_color="#F8FAFC", border_color="#0F172A", text_color="#0F172A")

    # Arrow 4 -> 5
    draw_arrow(main_x, 5.02, main_x, 4.58)

    # Step 5: Hemodynamic Feature Engineering
    draw_box(main_x, 4.2, 6.6, 0.75, "STEP 5: COLORIMETRIC FEATURE EXTRACTION",
             "Erythema Index: EI=100*(logR - logG) | CIELAB a* | High Red-Hue Ratio (HHR) | Saturation",
             bg_color="#F8FAFC", border_color="#0F172A", text_color="#0F172A")

    # Arrow 5 -> 6
    draw_arrow(main_x, 3.82, main_x, 3.38)

    # Step 6: Dual-Stage Sugeno ANFIS Inference
    draw_box(main_x, 3.0, 6.6, 0.75, "STEP 6: DUAL-STAGE ZERO-ORDER SUGENO ANFIS",
             "3 inputs x 3 Gaussian terms (27 rules) -> Stage 1: p(Anemic) -> Stage 2: p(Mod-to-Severe)",
             bg_color="#FCE4EA", border_color="#B4264A", text_color="#7A1734")

    # Arrow 6 -> 7
    draw_arrow(main_x, 2.62, main_x, 2.18)

    # Step 7: Multi-Frame Consensus & Triage Grading
    draw_box(main_x, 1.8, 6.6, 0.75, "STEP 7: CONSENSUS AGGREGATION & CLINICAL TRIAGE",
             "Median p across burst | Agreement % | Normal / Mild / Moderate-to-Severe (No continuous Hb)",
             bg_color="#EFF6FF", border_color="#2563EB", text_color="#1E40AF")

    # Arrow 7 -> 8
    draw_arrow(main_x, 1.42, main_x, 0.98)

    # Step 8: Bioavailability-Aware Dietary Optimizer
    draw_box(main_x, 0.6, 6.6, 0.75, "STEP 8: BIOAVAILABILITY DIETARY OPTIMIZER",
             "USDA SR Legacy (46 foods) | Hurrell absorption: Fe_abs = Fe_heme*0.25 + Fe_nonheme*0.10*E*I",
             bg_color="#F0FDF4", border_color="#16A34A", text_color="#166534")

    # Right Side Explanatory Annotations
    # Clinical Safety Callout
    c_safe = FancyBboxPatch((10.8, 3.3), 3.6, 2.2, boxstyle="round,pad=0.08,rounding_size=0.12",
                            facecolor="#FFFBEB", edgecolor="#D97706", linewidth=1.5)
    ax.add_patch(c_safe)
    ax.text(12.6, 5.25, "CLINICAL SAFETY DIRECTIVE", fontsize=8.2, fontweight="bold", ha="center", va="center", color="#B45309")
    safe_lines = [
        "• Strict continuous Hb suppression:",
        "  Prevents false laboratory equivalence.",
        "• Platt Calibrated Probabilities:",
        "  Mapped to 5-fold CV empirical accuracy.",
        "• Emergency Clinical Referral:",
        "  Triggered for Moderate/Severe results or",
        "  red-flag symptoms (chest pain, syncope).",
        "• Teratogenic Safety Filter:",
        "  Organ meats filtered out for pregnancy."
    ]
    sy = 4.90
    for sl in safe_lines:
        ax.text(11.0, sy, sl, fontsize=6.3, color="#92400E")
        sy -= 0.19

    # Dietary Bioavailability Callout
    c_diet = FancyBboxPatch((10.8, 0.6), 3.6, 2.4, boxstyle="round,pad=0.08,rounding_size=0.12",
                            facecolor="#F0FDF4", edgecolor="#16A34A", linewidth=1.5)
    ax.add_patch(c_diet)
    ax.text(12.6, 2.75, "MICRONUTRIENT MODELING", fontsize=8.2, fontweight="bold", ha="center", va="center", color="#166534")
    diet_lines = [
        "• Hurrell & Egli Bioavailability:",
        "  Fe_abs = Fe_heme*0.25 + Fe_non*0.10*E*I",
        "• Enhancer (E = 2.0):",
        "  Vitamin C >= 25 mg or animal tissue.",
        "• Inhibitor (I = 0.7):",
        "  Calcium >= 300 mg (dairy penalty).",
        "• Inhibitor (I = 0.8):",
        "  Phytate-rich grains without Vitamin C.",
        "• Deterministic USDA Nutrient Totals:",
        "  AI strictly limited to cultural phrasing."
    ]
    dy = 2.42
    for dl in diet_lines:
        ax.text(11.0, dy, dl, fontsize=6.3, color="#14532D")
        dy -= 0.18

    # Save figure
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated Image 3: {output_path}")

if __name__ == "__main__":
    out_dir = os.path.join("paper", "figures")
    os.makedirs(out_dir, exist_ok=True)
    create_flowchart(os.path.join(out_dir, "flowchart_pipeline.png"))
