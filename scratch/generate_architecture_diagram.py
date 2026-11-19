"""
generate_architecture_diagram.py
Generates Image 2:
Architecture diagram: Flutter app -> HTTPS (Caddy) -> FastAPI + hemosense core on EC2 -> Amazon Bedrock / OpenRouter
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

def create_architecture_diagram(output_path):
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8.5)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    # Title
    ax.text(7.5, 8.15, "HemoSense AI: End-to-End System Architecture",
            fontsize=16, fontweight="bold", ha="center", va="center", color="#7A1734")
    ax.text(7.5, 7.85, "Edge Flutter Client to Dockerized FastAPI & hemosense Core on AWS EC2 with LLM Dietary Augmentation",
            fontsize=9.5, fontstyle="italic", ha="center", va="center", color="#64748B")

    # ==================== TIER 1: CLIENT EDGE (FLUTTER) ====================
    # Outer Container
    c_edge = FancyBboxPatch((0.5, 0.6), 3.8, 6.9, boxstyle="round,pad=0.12,rounding_size=0.15",
                            facecolor="#FDF8F9", edgecolor="#B4264A", linewidth=1.8)
    ax.add_patch(c_edge)
    
    # Tier Header
    h1 = FancyBboxPatch((0.7, 7.05), 3.4, 0.35, boxstyle="round,pad=0.04,rounding_size=0.08",
                        facecolor="#7A1734", edgecolor="none")
    ax.add_patch(h1)
    ax.text(2.4, 7.22, "EDGE CLIENT (FLUTTER 3.47+ / DART)", fontsize=8.5, fontweight="bold",
            ha="center", va="center", color="#FFFFFF")

    # Edge Sub-components
    y = 6.85
    edge_blocks = [
        ("UI & Presentation Layer", "#FFFFFF", "#9F1239", [
            "• Camera Burst (3 frames @ 350ms, torch ON)",
            "• Interactive Eyelid ROI Box Selector",
            "• 4-Zone Risk Gauge & Rule Explanation View",
            "• Dietary Questionnaire & Meal Plan Screen",
            "• On-device Scan History & Trend Charts"
        ]),
        ("State Management & Core Logic", "#FFFFFF", "#0F172A", [
            "• Riverpod 3 (Notifier-style providers)",
            "• Zero legacy context / compile-time safe",
            "• Async pipeline execution state machine"
        ]),
        ("On-Device Local Storage (Hive)", "#FCE4EA", "#7A1734", [
            "• Encrypted key-value boxes: hs_profile, hs_history",
            "• Pure Dart (< 5ms read/write latency)",
            "• 100% Client Privacy: Zero cloud patient DB"
        ]),
        ("Networking Client (Dio 5.x)", "#FFFFFF", "#0F172A", [
            "• Multipart form stream (photos + ROI JSON)",
            "• Centralized error code interceptors",
            "• Base URL switch (Dev / Prod AWS)"
        ]),
    ]
    for b_title, b_bg, b_col, b_lines in edge_blocks:
        bh = 0.28 + len(b_lines) * 0.19
        pb = FancyBboxPatch((0.7, y - bh), 3.4, bh, boxstyle="round,pad=0.04,rounding_size=0.08",
                            facecolor=b_bg, edgecolor="#CBD5E1", linewidth=0.8)
        ax.add_patch(pb)
        ax.text(0.85, y - 0.14, b_title, fontsize=7.8, fontweight="bold", color=b_col)
        ly = y - 0.32
        for l in b_lines:
            ax.text(0.95, ly, l, fontsize=6.5, color="#334155")
            ly -= 0.19
        y -= (bh + 0.14)

    # ==================== TIER 2: TRANSPORT & INGRESS (CADDY) ====================
    # Connecting Arrow 1 -> 2
    ax.annotate("", xy=(4.9, 4.3), xytext=(4.3, 4.3),
                arrowprops=dict(facecolor="#B4264A", edgecolor="#B4264A", width=2.5, headwidth=7.0))
    ax.text(4.6, 4.55, "HTTPS\nTLS 1.3", fontsize=7.0, fontweight="bold", ha="center", va="center", color="#7A1734")

    c_ingress = FancyBboxPatch((4.9, 2.5), 1.9, 3.6, boxstyle="round,pad=0.10,rounding_size=0.15",
                               facecolor="#EFF6FF", edgecolor="#2563EB", linewidth=1.5)
    ax.add_patch(c_ingress)
    
    h2 = FancyBboxPatch((5.0, 5.75), 1.7, 0.30, boxstyle="round,pad=0.04,rounding_size=0.06",
                        facecolor="#1E40AF", edgecolor="none")
    ax.add_patch(h2)
    ax.text(5.85, 5.90, "INGRESS GATEWAY", fontsize=7.5, fontweight="bold", ha="center", va="center", color="#FFFFFF")
    
    ax.text(5.85, 5.45, "Caddy 2 Proxy", fontsize=8.2, fontweight="bold", ha="center", color="#1E3A8A")
    ax.text(5.85, 5.25, "(caddy:2.8-alpine)", fontsize=6.8, fontstyle="italic", ha="center", color="#3B82F6")
    
    ingress_points = [
        "• Ports 80 & 443",
        "• Auto Let's Encrypt TLS",
        "• Domain: sslip.io",
        "• 40 MB Body Limit",
        "• HSTS & Security Headers",
        "• Reverse proxy -> :8000"
    ]
    iy = 4.85
    for ip in ingress_points:
        ax.text(5.1, iy, ip, fontsize=6.5, color="#1E293B")
        iy -= 0.22

    # Connecting Arrow 2 -> 3
    ax.annotate("", xy=(7.4, 4.3), xytext=(6.8, 4.3),
                arrowprops=dict(facecolor="#2563EB", edgecolor="#2563EB", width=2.0, headwidth=6.0))
    ax.text(7.1, 4.55, "Proxy\n:8000", fontsize=7.0, fontweight="bold", ha="center", va="center", color="#1E40AF")

    # ==================== TIER 3: AWS EC2 HOSTING ENVIRONMENT ====================
    c_aws = FancyBboxPatch((7.4, 0.6), 4.6, 6.9, boxstyle="round,pad=0.12,rounding_size=0.15",
                           facecolor="#F8FAFC", edgecolor="#D97706", linewidth=1.8)
    ax.add_patch(c_aws)
    
    h3 = FancyBboxPatch((7.6, 7.05), 4.2, 0.35, boxstyle="round,pad=0.04,rounding_size=0.08",
                        facecolor="#D97706", edgecolor="none")
    ax.add_patch(h3)
    ax.text(9.7, 7.22, "AWS CLOUD (ap-south-1 Mumbai) — EC2 t3.small", fontsize=8.5, fontweight="bold",
            ha="center", va="center", color="#FFFFFF")

    # AWS Host metadata banner
    aws_meta = FancyBboxPatch((7.6, 6.45), 4.2, 0.50, boxstyle="round,pad=0.04,rounding_size=0.06",
                              facecolor="#FEF3C7", edgecolor="#F59E0B", linewidth=0.8)
    ax.add_patch(aws_meta)
    ax.text(9.7, 6.75, "EC2 t3.small (Ubuntu 24.04 LTS, 2 vCPU, 2GB RAM, 20GB gp3 Encrypted EBS)",
            fontsize=6.8, fontweight="bold", ha="center", color="#92400E")
    ax.text(9.7, 6.55, "Elastic IP: 3.111.237.63 | IMDSv2 Required | CloudWatch StatusCheck Auto-Recover",
            fontsize=6.4, ha="center", color="#B45309")

    # Inside Docker Compose Box
    c_docker = FancyBboxPatch((7.6, 0.8), 4.2, 5.5, boxstyle="round,pad=0.08,rounding_size=0.10",
                              facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.2)
    ax.add_patch(c_docker)
    ax.text(7.8, 6.08, "Docker Compose: API Container (hemosense-api)", fontsize=7.8, fontweight="bold", color="#0F172A")
    ax.text(11.6, 6.08, "Python 3.11-slim (Non-root)", fontsize=6.8, fontstyle="italic", ha="right", color="#64748B")

    # Sub-modules inside API Container
    y_api = 5.9
    api_modules = [
        ("FastAPI Serving Layer (api/main.py, pipeline.py)", "#F1F5F9", "#0F172A", [
            "• Endpoints: /screen/batch, /health, /symptoms, /diet/plan",
            "• Ephemeral in-memory image processing (Zero disk writes)",
            "• Pydantic v2 schemas: DietRecommendationRequest, BatchResult"
        ]),
        ("Clinical Triage & Voting (api/clinical.py)", "#F1F5F9", "#0F172A", [
            "• Multi-frame median probability aggregation",
            "• Voter agreement ratio & empirical confidence lookup",
            "• Triage grading: Normal / Mild / Moderate-to-Severe"
        ]),
        ("Core Scientific Package (hemosense/)", "#FCE4EA", "#7A1734", [
            "• segment.py: 7-point quality gates, GrabCut, Otsu a* split",
            "• features.py: Erythema Index, CIELAB a*, HHR, Saturation",
            "• anfis.py: 2-stage zero-order Sugeno ANFIS (pure NumPy)",
            "• diet.py: Hurrell & Egli iron bioavailability calculation"
        ]),
        ("Serialized Models & Reference Data (models/)", "#F0FDF4", "#166534", [
            "• models/anfis.json (45 parameters, Gaussian MFs + consequents)",
            "• models/confidence.json (5-fold CV empirical accuracy mapping)",
            "• data/foods_usda.csv (46 verified foods from USDA SR Legacy)"
        ]),
    ]
    for m_title, m_bg, m_col, m_lines in api_modules:
        mh = 0.24 + len(m_lines) * 0.17
        mb = FancyBboxPatch((7.75, y_api - mh), 3.9, mh, boxstyle="round,pad=0.04,rounding_size=0.06",
                            facecolor=m_bg, edgecolor="#CBD5E1", linewidth=0.7)
        ax.add_patch(mb)
        ax.text(7.9, y_api - 0.12, m_title, fontsize=7.2, fontweight="bold", color=m_col)
        ly = y_api - 0.27
        for l in m_lines:
            ax.text(8.0, ly, l, fontsize=6.2, color="#334155")
            ly -= 0.17
        y_api -= (mh + 0.11)

    # ==================== TIER 4: LLM INTELLIGENCE ====================
    # Connecting Arrow 3 -> 4 (Dashed / Optional)
    ax.annotate("", xy=(12.6, 4.3), xytext=(12.0, 4.3),
                arrowprops=dict(facecolor="#7C3AED", edgecolor="#7C3AED", width=1.8, headwidth=6.0, linestyle="--"))
    ax.text(12.3, 4.55, "Outbound\nHTTPS", fontsize=6.8, fontweight="bold", ha="center", va="center", color="#6D28D9")

    c_llm = FancyBboxPatch((12.6, 2.3), 1.9, 4.0, boxstyle="round,pad=0.10,rounding_size=0.15",
                           facecolor="#F5F3FF", edgecolor="#7C3AED", linewidth=1.5, linestyle="--")
    ax.add_patch(c_llm)
    
    h4 = FancyBboxPatch((12.7, 5.95), 1.7, 0.30, boxstyle="round,pad=0.04,rounding_size=0.06",
                        facecolor="#6D28D9", edgecolor="none")
    ax.add_patch(h4)
    ax.text(13.55, 6.10, "OPTIONAL LLM", fontsize=7.5, fontweight="bold", ha="center", va="center", color="#FFFFFF")

    ax.text(13.55, 5.65, "Amazon Bedrock /", fontsize=7.8, fontweight="bold", ha="center", color="#4C1D95")
    ax.text(13.55, 5.45, "OpenRouter API", fontsize=7.8, fontweight="bold", ha="center", color="#4C1D95")
    ax.text(13.55, 5.25, "(Llama 3.1 8B)", fontsize=6.8, fontstyle="italic", ha="center", color="#7C3AED")

    llm_points = [
        "• Translates raw foods",
        "  into local dishes",
        "• Estimates meal costs",
        "• Strict Safety Check:",
        "  Server validates foods",
        "  and recomputes USDA",
        "  numbers deterministically",
        "• Fallback to rules if",
        "  API is unavailable"
    ]
    ly = 4.85
    for lp in llm_points:
        ax.text(12.8, ly, lp, fontsize=6.3, color="#1E293B")
        ly -= 0.18

    # Save figure
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated Image 2: {output_path}")

if __name__ == "__main__":
    out_dir = os.path.join("paper", "figures")
    os.makedirs(out_dir, exist_ok=True)
    create_architecture_diagram(os.path.join(out_dir, "architecture_diagram.png"))
