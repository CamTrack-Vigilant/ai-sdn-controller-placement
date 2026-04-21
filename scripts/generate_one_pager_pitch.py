from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

BASE = Path(r"c:\Users\fanele\AI-Driven Controller Placement Optimization in Multi-Site Software Defined Networks\ai-sdn-controller-placement\docs\submit")
OUTPUT = BASE / "ThabangNhlokomaButhelezi_OnePager_DRAFT.pdf"

TITLE = "Decision-Grade Multi-Objective Benchmarking of AI vs Heuristic Controller Placement in Multi-Site SDN"
NAME = "Thabang Nhlokoma Buthelezi"
STUDENT_NUMBER = "230011908"
SUPERVISOR = "Prof Pragasen Mudalu and Dr Skhumbuzo Zwane"

sections = [
    ("Background", "Software-Defined Networking (SDN) separates the control plane from the data plane, enabling centralized orchestration of network decisions. In multi-site environments, heterogeneous link delays and distributed traffic demands make controller placement a decision-critical design problem because it directly affects control-plane latency, stability, and operational efficiency."),
    ("Problem Statement", "Current SDN controller placement research often optimizes isolated metrics, especially latency, while treating controller overhead, adaptation cost, and hardware constraints as secondary concerns. This creates a real gap because AI-based placement may improve performance in simulation but still impose CPU and memory costs that make it less practical than simpler heuristics."),
    ("Aim", "To design and evaluate a decision-grade multi-objective benchmarking framework that compares AI-based and heuristic controller placement methods for multi-site SDN."),
    ("Objectives", [
        "1. To establish heuristic baseline controller placement strategies for multi-site SDN under controlled simulation conditions.",
        "2. To implement AI-based controller placement using Genetic Algorithms and Reinforcement Learning.",
        "3. To measure and compare the methods using latency and controller overhead as the core multi-objective performance metrics.",
        "4. To benchmark the competing approaches and synthesize results into decision-grade guidance on when AI-based placement offers practical value over heuristics.",
    ]),
    ("Proposed Approach", "This study will adopt an experimental design in a simulated SDN environment using Mininet and the Ryu controller. A multi-site topology based on Internet2/GÉANT-style backbone structures will be configured with heterogeneous link delays, bandwidth variation, and site-to-site asymmetry. Traffic will be generated using Iperf and D-ITG under normal, burst, and stress scenarios; a Genetic Algorithm will search for global placements while a Reinforcement Learning agent adapts to changing network state. The framework will be evaluated using propagation delay, Packet-In processing time, and controller CPU and memory utilization, with 30+ runs per scenario and Pareto Front analysis to compare trade-offs."),
    ("Expected Contribution", "The study will produce a Multi-Objective Performance Ledger for multi-site SDN controller placement and a Reproducible Simulation Workflow for evaluating AI and heuristic methods under identical conditions. It will also identify the break-even point at which AI overhead outweighs performance gains, providing a concrete basis for comparative decision-making."),
    ("Significance", "For researchers, this study offers a benchmark for future SDN-AI optimization work and a structured basis for comparing competing placement strategies. For practitioners and network administrators, it provides a decision-grade framework for selecting tools according to specific CPU and RAM constraints in resource-constrained environments."),
]

def build_pdf() -> None:
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "OnePagerTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=12.2,
        leading=14,
        alignment=1,
        spaceAfter=4,
    )
    meta_style = ParagraphStyle(
        "Meta",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=9.4,
        spaceAfter=1.5,
    )
    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=9.2,
        leading=10.4,
        spaceBefore=2.0,
        spaceAfter=1.0,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.25,
        leading=9.25,
        spaceAfter=1.2,
    )
    body_style.spaceBefore = 0

    story = []
    story.append(Paragraph(TITLE, title_style))

    details = Table(
        [[Paragraph("<b>Name:</b> " + NAME, meta_style), Paragraph("<b>Student Number:</b> " + STUDENT_NUMBER, meta_style)],
         [Paragraph("<b>Supervisor:</b> " + SUPERVISOR, meta_style), Paragraph("", meta_style)]],
        colWidths=[88 * mm, 88 * mm],
    )
    details.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.45, colors.black),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(details)
    story.append(Spacer(1, 3.5))

    for heading, content in sections:
        block = [Paragraph(heading, heading_style)]
        if isinstance(content, list):
            for item in content:
                block.append(Paragraph(item, body_style))
        else:
            block.append(Paragraph(content, body_style))
        story.append(KeepTogether(block))

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=12 * mm,
        bottomMargin=11 * mm,
    )
    doc.build(story)


if __name__ == "__main__":
    build_pdf()
    print(f"Wrote {OUTPUT}")
