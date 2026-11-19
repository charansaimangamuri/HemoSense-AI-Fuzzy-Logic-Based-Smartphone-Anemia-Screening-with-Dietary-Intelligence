"""
generate_aws_deployment_diagram.py
Generates Image 4:
Diagram: AWS deployment & GitHub Actions CI/CD pipeline
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

def create_aws_deployment_diagram(output_path):
    fig, ax = plt.subplots(figsize=(15, 9.5), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9.5)
    ax.axis("off")
    fig.patch.set_facecolor("#FFFFFF")

    # Header Title
    ax.text(7.5, 9.15, "HemoSense AI: AWS Cloud Deployment & CI/CD Pipeline Architecture",
            fontsize=15, fontweight="bold", ha="center", va="center", color="#7A1734")
    ax.text(7.5, 8.85, "Continuous Integration via GitHub Actions to Production Docker Compose on AWS EC2 (ap-south-1 Mumbai)",
            fontsize=9.2, fontstyle="italic", ha="center", va="center", color="#64748B")

    # ==================== LEFT PANEL: CI/CD PIPELINE (GITHUB ACTIONS) ====================
    c_cicd = FancyBboxPatch((0.5, 0.6), 4.4, 7.9, boxstyle="round,pad=0.12,rounding_size=0.15",
                            facecolor="#F8FAFC", edgecolor="#2563EB", linewidth=1.8)
    ax.add_patch(c_cicd)

    h_cicd = FancyBboxPatch((0.7, 8.05), 4.0, 0.35, boxstyle="round,pad=0.04,rounding_size=0.08",
                            facecolor="#1D4ED8", edgecolor="none")
    ax.add_patch(h_cicd)
    ax.text(2.7, 8.22, "CI / CD PIPELINE & DEPLOYMENT AUTOMATION", fontsize=8.2, fontweight="bold",
            ha="center", va="center", color="#FFFFFF")

    y_ci = 7.7
    ci_cards = [
        ("1. Source Control & Trigger", "#FFFFFF", "#0F172A", [
            "• Developer Workstation: git push origin main",
            "• GitHub Repository: HemoSense-AI-...",
            "• Webhook triggers GitHub Actions workflow",
            "• File: .github/workflows/ci.yml"
        ]),
        ("2. Automated CI Matrix (GitHub Runner)", "#EFF6FF", "#1E40AF", [
            "• Job A: Python Backend Quality Suite",
            "  - 45 pytest tests (ANFIS gradients, CV, diet)",
            "  - Pydantic v2 schema validation checks",
            "• Job B: Flutter Mobile App Verification",
            "  - flutter analyze (zero lint issues)",
            "  - flutter test (widget & unit test pass)"
        ]),
        ("3. Deployment Automation (deploy/aws_deploy.sh)", "#FEF3C7", "#92400E", [
            "• Idempotent bash script using AWS CLI & SSH",
            "• Verifies/creates IAM Policy: HemoSenseDeploy",
            "• Packages code bundle: deploy/bundle.tgz",
            "• SCP bundle to EC2 host via key: ~/.ssh/hemosense-key",
            "• Remote Docker Compose build & container restart",
            "• Smoke test execution: curl https://.../health"
        ]),
        ("4. Automated Teardown (deploy/aws_teardown.sh)", "#F1F5F9", "#475569", [
            "• Single-command complete resource decommission",
            "• Releases Elastic IP, terminates EC2 instance",
            "• Deletes Security Group and CloudWatch alarm"
        ]),
    ]
    for ct, cbg, ccol, clines in ci_cards:
        ch = 0.26 + len(clines) * 0.18
        cb = FancyBboxPatch((0.7, y_ci - ch), 4.0, ch, boxstyle="round,pad=0.04,rounding_size=0.06",
                            facecolor=cbg, edgecolor="#CBD5E1", linewidth=0.8)
        ax.add_patch(cb)
        ax.text(0.85, y_ci - 0.12, ct, fontsize=7.5, fontweight="bold", color=ccol)
        ly = y_ci - 0.28
        for l in clines:
            ax.text(0.95, ly, l, fontsize=6.3, color="#334155")
            ly -= 0.18
        y_ci -= (ch + 0.13)

    # Connecting Arrow: CI/CD -> AWS Cloud
    ax.annotate("", xy=(5.5, 4.8), xytext=(4.9, 4.8),
                arrowprops=dict(facecolor="#2563EB", edgecolor="#2563EB", width=2.5, headwidth=7.0))
    ax.text(5.2, 5.05, "SSH / SCP\nDeploy Script", fontsize=6.8, fontweight="bold", ha="center", va="center", color="#1D4ED8")

    # ==================== RIGHT PANEL: AWS PRODUCTION ENVIRONMENT ====================
    c_aws = FancyBboxPatch((5.5, 0.6), 9.0, 7.9, boxstyle="round,pad=0.12,rounding_size=0.15",
                           facecolor="#FFFBEB", edgecolor="#D97706", linewidth=1.8)
    ax.add_patch(c_aws)

    h_aws = FancyBboxPatch((5.7, 8.05), 8.6, 0.35, boxstyle="round,pad=0.04,rounding_size=0.08",
                           facecolor="#D97706", edgecolor="none")
    ax.add_patch(h_aws)
    ax.text(10.0, 8.22, "AWS PRODUCTION ENVIRONMENT (ap-south-1 Mumbai) — HARDENED INFRASTRUCTURE",
            fontsize=8.5, fontweight="bold", ha="center", va="center", color="#FFFFFF")

    # Top AWS Specs Banner
    spec_box = FancyBboxPatch((5.7, 7.25), 8.6, 0.68, boxstyle="round,pad=0.04,rounding_size=0.06",
                              facecolor="#FFFFFF", edgecolor="#F59E0B", linewidth=1.0)
    ax.add_patch(spec_box)
    ax.text(5.9, 7.72, "VPC & Security Group: hemosense-sg", fontsize=7.8, fontweight="bold", color="#B45309")
    ax.text(10.0, 7.72, "Elastic IP: 3.111.237.63 (DNS: 3-111-237-63.sslip.io)", fontsize=7.8, fontweight="bold", ha="center", color="#78350F")
    ax.text(14.1, 7.72, "Cost: ~$0.025 / hr", fontsize=7.8, fontweight="bold", ha="right", color="#16A34A")

    ax.text(5.9, 7.42, "• Inbound Ports: 80 (HTTP redirect), 443 (HTTPS public) from 0.0.0.0/0", fontsize=6.8, color="#475569")
    ax.text(10.8, 7.42, "• Port 22 (SSH): Restricted strictly to deployer's static IP", fontsize=6.8, color="#475569")

    # EC2 Virtual Server Container
    c_ec2 = FancyBboxPatch((5.7, 1.8), 8.6, 5.3, boxstyle="round,pad=0.08,rounding_size=0.10",
                           facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.2)
    ax.add_patch(c_ec2)

    ax.text(5.9, 6.85, "EC2 Virtual Machine: t3.small Instance", fontsize=8.2, fontweight="bold", color="#0F172A")
    ax.text(14.1, 6.85, "Ubuntu 24.04 LTS | 2 vCPU | 2 GB RAM | 2 GB Swap | IMDSv2 Required", fontsize=6.8, ha="right", color="#64748B")

    # CloudWatch Resilience Box
    cw_box = FancyBboxPatch((5.9, 6.05), 8.2, 0.52, boxstyle="round,pad=0.04,rounding_size=0.06",
                            facecolor="#FEF2F2", edgecolor="#EF4444", linewidth=0.8)
    ax.add_patch(cw_box)
    ax.text(6.1, 6.38, "CloudWatch Auto-Recover Alarm: hemosense-auto-recover", fontsize=7.2, fontweight="bold", color="#991B1B")
    ax.text(6.1, 6.18, "Triggers on StatusCheckFailed_System >= 2 periods -> Automated hardware instance reboot & recovery",
            fontsize=6.5, color="#7F1D1D")

    # Docker Compose Stack
    c_dock = FancyBboxPatch((5.9, 2.0), 8.2, 3.9, boxstyle="round,pad=0.06,rounding_size=0.08",
                            facecolor="#F8FAFC", edgecolor="#94A3B8", linewidth=1.0)
    ax.add_patch(c_dock)
    ax.text(6.1, 5.65, "Docker Compose Multi-Container Stack (deploy/docker-compose.yml)", fontsize=7.8, fontweight="bold", color="#1E293B")

    # Container 1: Caddy Reverse Proxy
    c1_box = FancyBboxPatch((6.1, 2.3), 3.8, 3.1, boxstyle="round,pad=0.04,rounding_size=0.06",
                            facecolor="#EFF6FF", edgecolor="#3B82F6", linewidth=1.0)
    ax.add_patch(c1_box)
    ax.text(8.0, 5.15, "Container 1: Caddy Proxy", fontsize=7.8, fontweight="bold", ha="center", color="#1E40AF")
    ax.text(8.0, 4.95, "caddy:2.8-alpine (Public Ingress)", fontsize=6.8, fontstyle="italic", ha="center", color="#2563EB")
    
    c1_lines = [
        "• Binds host ports 80 & 443",
        "• Automatic ACME TLS (Let's Encrypt)",
        "• Enforces 40 MB max upload limit",
        "• HSTS, CORS & security headers",
        "• Reverse proxy -> api:8000",
        "• Volume: caddy_data (certs)",
        "• Restart policy: unless-stopped"
    ]
    c1_y = 4.65
    for l in c1_lines:
        ax.text(6.3, c1_y, l, fontsize=6.3, color="#1E293B")
        c1_y -= 0.18

    # Arrow inside Docker: Caddy -> API
    ax.annotate("", xy=(10.3, 3.85), xytext=(9.9, 3.85),
                arrowprops=dict(facecolor="#2563EB", edgecolor="#2563EB", width=2.0, headwidth=6.0))
    ax.text(10.1, 4.10, "Proxy\n:8000", fontsize=6.5, fontweight="bold", ha="center", va="center", color="#1D4ED8")

    # Container 2: FastAPI Service
    c2_box = FancyBboxPatch((10.3, 2.3), 3.6, 3.1, boxstyle="round,pad=0.04,rounding_size=0.06",
                            facecolor="#FDF2F4", edgecolor="#BE123C", linewidth=1.0)
    ax.add_patch(c2_box)
    ax.text(12.1, 5.15, "Container 2: HemoSense API", fontsize=7.8, fontweight="bold", ha="center", color="#9F1239")
    ax.text(12.1, 4.95, "python:3.11-slim (hemosense-api)", fontsize=6.8, fontstyle="italic", ha="center", color="#E11D48")

    c2_lines = [
        "• Uvicorn ASGI with 2 workers",
        "• Non-root secure execution user",
        "• Ephemeral RAM processing (No disk)",
        "• hemosense/ shared ML & CV core",
        "• models/anfis.json (45 params)",
        "• Health check endpoint: /health",
        "• Memory limit: 1.2 GB"
    ]
    c2_y = 4.65
    for l in c2_lines:
        ax.text(10.5, c2_y, l, fontsize=6.3, color="#1E293B")
        c2_y -= 0.18

    # Bottom External Services Bar
    b_ext = FancyBboxPatch((5.7, 0.8), 8.6, 0.85, boxstyle="round,pad=0.04,rounding_size=0.06",
                           facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=0.8)
    ax.add_patch(b_ext)
    ax.text(5.9, 1.45, "External Outbound HTTPS Dependencies (Outbound Port 443 Only):", fontsize=7.2, fontweight="bold", color="#334155")
    ax.text(5.9, 1.25, "1. Let's Encrypt ACME: Automated domain validation & 90-day TLS certificate renewal.", fontsize=6.5, color="#475569")
    ax.text(5.9, 1.05, "2. Amazon Bedrock / OpenRouter API: Optional Llama 3.1 dietary dish naming (fails over to local rule planner).", fontsize=6.5, color="#475569")
    ax.text(5.9, 0.88, "3. Ubuntu Security Repositories: Unattended daily security patches & package upgrades.", fontsize=6.5, color="#475569")

    # Save figure
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated Image 4: {output_path}")

if __name__ == "__main__":
    out_dir = os.path.join("paper", "figures")
    os.makedirs(out_dir, exist_ok=True)
    create_aws_deployment_diagram(os.path.join(out_dir, "aws_deployment_diagram.png"))
