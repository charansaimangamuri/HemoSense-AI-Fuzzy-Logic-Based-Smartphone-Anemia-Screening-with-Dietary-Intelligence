"""
generate_concept_figure.py
Generates Image 1:
Concept figure: phone photographing the lower eyelid -> result -> diet plan
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, ArrowStyle

def create_concept_figure(output_path):
    fig, ax = plt.subplots(figsize=(14, 6.2), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    # Header Title Banner
    ax.text(7.0, 5.85, "HemoSense AI: End-to-End Clinical Screening & Nutritional Concept",
            fontsize=15, fontweight="bold", ha="center", va="center", color="#7A1734")
    ax.text(7.0, 5.55, "From Non-Invasive Smartphone Eyelid Photography to Interpretable Triage and Absorption-Aware Nutrition",
            fontsize=9.5, fontstyle="italic", ha="center", va="center", color="#64748B")

    # Draw 3 Major Stage Cards
    card_y = 0.5
    card_h = 4.6
    card_w = 3.8

    # Stage 1: Optical Acquisition
    c1 = FancyBboxPatch((0.5, card_y), card_w, card_h, boxstyle="round,pad=0.15,rounding_size=0.2",
                        facecolor="#FDF8F9", edgecolor="#B4264A", linewidth=2.0)
    ax.add_patch(c1)

    # Stage 2: AI Screening & Triage
    c2 = FancyBboxPatch((5.1, card_y), card_w, card_h, boxstyle="round,pad=0.15,rounding_size=0.2",
                        facecolor="#F8FAFC", edgecolor="#1E293B", linewidth=2.0)
    ax.add_patch(c2)

    # Stage 3: Dietary Intelligence
    c3 = FancyBboxPatch((9.7, card_y), card_w, card_h, boxstyle="round,pad=0.15,rounding_size=0.2",
                        facecolor="#F0FDF4", edgecolor="#16A34A", linewidth=2.0)
    ax.add_patch(c3)

    # --- STAGE 1 CONTENT ---
    # Step Badge
    b1 = FancyBboxPatch((0.7, 4.6), 3.4, 0.38, boxstyle="round,pad=0.05,rounding_size=0.1",
                        facecolor="#7A1734", edgecolor="none")
    ax.add_patch(b1)
    ax.text(2.4, 4.79, "STAGE 1: OPTICAL ACQUISITION", fontsize=9.0, fontweight="bold",
            ha="center", va="center", color="#FFFFFF")

    # Phone Graphic Representation
    phone = FancyBboxPatch((1.6, 2.3), 1.6, 2.05, boxstyle="round,pad=0.08,rounding_size=0.15",
                           facecolor="#1E293B", edgecolor="#0F172A", linewidth=2.0)
    ax.add_patch(phone)
    screen = FancyBboxPatch((1.7, 2.45), 1.4, 1.75, boxstyle="round,pad=0.05,rounding_size=0.08",
                            facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.0)
    ax.add_patch(screen)

    # Camera Torch Beam
    torch_beam = patches.Polygon([[2.4, 4.3], [1.3, 1.6], [3.5, 1.6]], closed=True,
                                 facecolor="#FEF08A", edgecolor="none", alpha=0.35)
    ax.add_patch(torch_beam)
    ax.text(2.4, 4.15, "TORCH ON", fontsize=6.5, fontweight="bold", ha="center", va="center", color="#854D0E")

    # Stylized Eye Illustration inside screen
    eye_white = patches.Ellipse((2.4, 3.4), 1.1, 0.65, facecolor="#F8FAFC", edgecolor="#94A3B8", linewidth=1.2)
    ax.add_patch(eye_white)
    iris = patches.Circle((2.4, 3.45), 0.28, facecolor="#0284C7", edgecolor="#0369A1", linewidth=1.0)
    pupil = patches.Circle((2.4, 3.45), 0.12, facecolor="#0F172A")
    ax.add_patch(iris)
    ax.add_patch(pupil)

    # Pulled-down lower eyelid (palpebral conjunctiva)
    eyelid = patches.Arc((2.4, 3.3), 1.15, 0.75, theta1=200, theta2=340, edgecolor="#BE123C", linewidth=3.5)
    ax.add_patch(eyelid)

    # User ROI Box
    roi_box = patches.Rectangle((1.9, 2.85), 1.0, 0.35, linewidth=1.5, edgecolor="#E11D48",
                                facecolor="#FFE4E6", alpha=0.6, linestyle="--")
    ax.add_patch(roi_box)
    ax.text(2.4, 3.02, "ROI Bounding Box", fontsize=6.5, fontweight="bold", ha="center", va="center", color="#9F1239")

    # Stage 1 bullets
    ax.text(2.4, 1.85, "1. Patient looks upward gently", fontsize=8.0, ha="center", va="center", color="#334155")
    ax.text(2.4, 1.55, "2. Pulled-down lower eyelid exposed", fontsize=8.0, ha="center", va="center", color="#334155")
    ax.text(2.4, 1.25, "3. Hardware torch locks exposure", fontsize=8.0, ha="center", va="center", color="#334155")
    ax.text(2.4, 0.95, "4. 3-frame burst (350 ms interval)", fontsize=8.0, fontweight="bold", ha="center", va="center", color="#7A1734")

    # --- ARROW 1 -> 2 ---
    ax.annotate("", xy=(4.9, 2.8), xytext=(4.4, 2.8),
                arrowprops=dict(facecolor="#B4264A", edgecolor="#B4264A", width=2.5, headwidth=8.0))
    ax.text(4.65, 3.1, "3 Frames\n+ ROI Box", fontsize=7.2, fontweight="bold", ha="center", va="center", color="#7A1734")

    # --- STAGE 2 CONTENT ---
    b2 = FancyBboxPatch((5.3, 4.6), 3.4, 0.38, boxstyle="round,pad=0.05,rounding_size=0.1",
                        facecolor="#1E293B", edgecolor="none")
    ax.add_patch(b2)
    ax.text(7.0, 4.79, "STAGE 2: AI SCREENING & TRIAGE", fontsize=9.0, fontweight="bold",
            ha="center", va="center", color="#FFFFFF")

    # Pipeline Blocks inside Stage 2
    y_p = 4.15
    boxes_s2 = [
        ("1. Pre-Flight 7-Point Quality Gate", "#F1F5F9", "#475569", "Luminance, blur, crescent shape & sclera check"),
        ("2. Tissue GrabCut + Otsu a* Split", "#F1F5F9", "#475569", "Separates palpebral tissue from lashes/sclera"),
        ("3. Colorimetry (EI, CIELAB a*, HHR)", "#F1F5F9", "#475569", "Hemodynamic microvascular color indices"),
        ("4. Dual-Stage Sugeno ANFIS (27 Rules)", "#FCE4EA", "#9F1239", "Gaussian terms -> Logits -> Platt calibration"),
    ]
    for title, bg_col, text_col, sub in boxes_s2:
        pb = FancyBboxPatch((5.35, y_p - 0.42), 3.3, 0.44, boxstyle="round,pad=0.04,rounding_size=0.08",
                            facecolor=bg_col, edgecolor="#CBD5E1", linewidth=0.8)
        ax.add_patch(pb)
        ax.text(5.45, y_p - 0.12, title, fontsize=7.5, fontweight="bold", color=text_col)
        ax.text(5.45, y_p - 0.30, sub, fontsize=6.5, color="#64748B")
        y_p -= 0.52

    # Result Card Visualization
    res_card = FancyBboxPatch((5.35, 0.72), 3.3, 1.25, boxstyle="round,pad=0.05,rounding_size=0.1",
                              facecolor="#FFFFFF", edgecolor="#B4264A", linewidth=1.5)
    ax.add_patch(res_card)
    ax.text(7.0, 1.75, "SCREENING VERDICT & TRIAGE", fontsize=8.0, fontweight="bold", ha="center", va="center", color="#7A1734")
    
    # Verdict Badge
    v_badge = FancyBboxPatch((5.55, 1.25), 2.9, 0.32, boxstyle="round,pad=0.04,rounding_size=0.08",
                             facecolor="#FEF2F2", edgecolor="#EF4444", linewidth=1.0)
    ax.add_patch(v_badge)
    ax.text(7.0, 1.41, "GRADE: MILD ANEMIA (p = 0.76)", fontsize=7.8, fontweight="bold", ha="center", va="center", color="#B91C1C")
    
    ax.text(7.0, 1.05, "Agreement: 100% (3/3 frames) | Confidence: HIGH", fontsize=7.0, ha="center", va="center", color="#334155")
    ax.text(7.0, 0.85, "* Strictly no continuous Hb (g/dL) estimation", fontsize=6.5, fontstyle="italic", ha="center", va="center", color="#64748B")

    # --- ARROW 2 -> 3 ---
    ax.annotate("", xy=(9.5, 2.8), xytext=(9.0, 2.8),
                arrowprops=dict(facecolor="#16A34A", edgecolor="#16A34A", width=2.5, headwidth=8.0))
    ax.text(9.25, 3.1, "Grade +\nProfile", fontsize=7.2, fontweight="bold", ha="center", va="center", color="#166534")

    # --- STAGE 3 CONTENT ---
    b3 = FancyBboxPatch((9.9, 4.6), 3.4, 0.38, boxstyle="round,pad=0.05,rounding_size=0.1",
                        facecolor="#166534", edgecolor="none")
    ax.add_patch(b3)
    ax.text(11.6, 4.79, "STAGE 3: DIETARY INTELLIGENCE", fontsize=9.0, fontweight="bold",
            ha="center", va="center", color="#FFFFFF")

    # Scientific Foundation Badge
    sci_badge = FancyBboxPatch((10.0, 4.05), 3.2, 0.42, boxstyle="round,pad=0.04,rounding_size=0.08",
                               facecolor="#DCFCE7", edgecolor="#86EFAC", linewidth=0.8)
    ax.add_patch(sci_badge)
    ax.text(11.6, 4.32, "Hurrell & Egli Bioavailability Model", fontsize=7.5, fontweight="bold", ha="center", va="center", color="#166534")
    ax.text(11.6, 4.15, "Fe_abs = Fe_heme*0.25 + Fe_nonheme*0.10 * E * I", fontsize=6.5, ha="center", va="center", color="#14532D")

    # Nutrition Table Items
    y_diet = 3.65
    diet_items = [
        ("Breakfast (8:00 AM)", "Cooked Poha + Lemon juice (Vit C boost E=2.0)", "+3.8 mg Fe"),
        ("Lunch (1:00 PM)", "Spinach Dal + Brown Rice (No tea/coffee)", "+5.2 mg Fe"),
        ("Snack (4:30 PM)", "Roasted chickpeas + Guava slices", "+2.9 mg Fe"),
        ("Dinner (8:00 PM)", "Sprouted Moong Khichdi + Tomato salad", "+4.4 mg Fe"),
    ]
    for meal, food, fe_val in diet_items:
        mb = FancyBboxPatch((10.0, y_diet - 0.40), 3.2, 0.40, boxstyle="round,pad=0.04,rounding_size=0.08",
                            facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=0.7)
        ax.add_patch(mb)
        ax.text(10.1, y_diet - 0.14, meal, fontsize=7.2, fontweight="bold", color="#0F172A")
        ax.text(10.1, y_diet - 0.30, food, fontsize=6.2, color="#475569")
        ax.text(13.1, y_diet - 0.20, fe_val, fontsize=7.0, fontweight="bold", ha="right", color="#16A34A")
        y_diet -= 0.48

    # Daily Summary Pill
    sum_pill = FancyBboxPatch((10.0, 0.72), 3.2, 0.85, boxstyle="round,pad=0.05,rounding_size=0.1",
                              facecolor="#ECFDF5", edgecolor="#10B981", linewidth=1.2)
    ax.add_patch(sum_pill)
    ax.text(11.6, 1.35, "DAILY TOTAL: 16.3 mg Fe (Target: 18.0 mg)", fontsize=7.5, fontweight="bold", ha="center", va="center", color="#065F46")
    ax.text(11.6, 1.15, "Grounded in USDA SR Legacy (46 verified foods)", fontsize=6.5, ha="center", va="center", color="#047857")
    ax.text(11.6, 0.95, "Safe: Organ meats filtered for pregnant patients", fontsize=6.5, fontstyle="italic", ha="center", va="center", color="#059669")

    # Save figure
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated Image 1: {output_path}")

if __name__ == "__main__":
    out_dir = os.path.join("paper", "figures")
    os.makedirs(out_dir, exist_ok=True)
    create_concept_figure(os.path.join(out_dir, "concept_figure.png"))
