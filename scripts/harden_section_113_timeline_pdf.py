#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import shutil
import fitz


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PDF_PATH = DOCS / "Research Proposal Template with Contant- PG Studies - Hons_linked.pdf"
REPORT_PATH = DOCS / "Section_11_3_timeline_hardening_report.txt"


TABLE_TEXT = """11.3 Research Process - Gantt Chart (UNIZULU 2026 Aligned)

Table 1. 9-Phase DRL-SDN Workflow and Milestone Map
Legend: X = active window

+----+------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| ID | Phase                              | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov |
+----+------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| P1 | Proposal & Ethics                  |  X  |  X  |     |     |     |     |     |     |     |
| P2 | Environment Setup                  |     |  X  |     |     |     |     |     |     |     |
| P3 | Pilot & Calibration                |     |  X  |  X  |     |     |     |     |     |     |
| P4 | Factorial Simulation Sprint        |     |     |  X  |  X  |     |     |     |     |     |
| P5 | DRL Training & Pareto Optimization |     |     |     |     |  X  |  X  |     |     |     |
| P6 | Analysis (ANOVA/Tukey HSD)         |     |     |     |     |     |     |  X  |     |     |
| P7 | Draft + Research Paper             |     |     |     |     |     |     |     |  X  |     |
| P8 | Prototype Demo Preparation         |     |     |     |     |     |     |     |  X  |  X  |
| P9 | Final Correction & Archiving       |     |     |     |     |     |     |     |     |  X  |
+----+------------------------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+

Milestones: Ethics Apr 17/27 | Proposal May 18/25 | Progress Jul 06/13 | Mock Sep 28 |
Draft Oct 26-30 | Defense Nov 04-06 | Final Nov 09-13 | Research Paper in P7/P9.

Outputs: P2 stack integration | P3 baseline 0.0226 s/episode | P4-P6 data+Pareto+stats |
P7-P9 draft paper + final submission + archive.
"""


def main() -> int:
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"Missing PDF: {PDF_PATH}")

    doc = fitz.open(PDF_PATH)

    target_page_index = None
    sec113_rect = None
    sec12_rect = None

    candidates: list[tuple[int, fitz.Rect, fitz.Rect | None]] = []
    heading_probes = [
        "11.3 Research process - Gantt chart",
        "11.3 Research Process - Gantt-Style Technical Workflow",
        "11.3 Research Process - Gantt Chart",
    ]

    for i, page in enumerate(doc):
        page_text = page.get_text("text")
        if "11 RESOURCES REQUIRED AND PROJECT PLAN" not in page_text:
            continue
        r113 = []
        for probe in heading_probes:
            r113 = page.search_for(probe)
            if r113:
                break
        if not r113:
            continue
        r12 = page.search_for("12 FEASIBILITY OF THE STUDY")
        sec113 = min(r113, key=lambda r: (r.y0, r.x0))
        sec12 = min(r12, key=lambda r: (r.y0, r.x0)) if r12 else None
        candidates.append((i, sec113, sec12))

    if candidates:
        # Use the last occurrence to avoid TOC and capture the actual body section.
        target_page_index, sec113_rect, sec12_rect = candidates[-1]

    if target_page_index is None or sec113_rect is None:
        raise RuntimeError("Could not find Section 11.3 heading in target PDF")

    page = doc[target_page_index]

    # Full reset for the 11.3 body area to avoid residual/overlapping legacy table text.
    y0 = sec113_rect.y0 - 4
    y1 = 785
    redact = fitz.Rect(45, y0, 553, y1)

    page.add_redact_annot(redact, fill=(1, 1, 1))
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

    textbox = fitz.Rect(48, y0 + 2, 550, y1 - 2)

    inserted = False
    used_size = None
    for size in (7.4, 7.2, 7.0, 6.8, 6.6, 6.4, 6.2):
        rc = page.insert_textbox(
            textbox,
            TABLE_TEXT,
            fontname="cour",
            fontsize=size,
            color=(0, 0, 0),
            align=fitz.TEXT_ALIGN_LEFT,
        )
        if rc >= 0:
            inserted = True
            used_size = size
            break

    if not inserted:
        raise RuntimeError("Section 11.3 replacement text did not fit the target area")

    # Ensure Section 12 heading is not lost when page-level cleanup removed it.
    next_index = target_page_index + 1
    if next_index < len(doc):
        next_page = doc[next_index]
        next_text = next_page.get_text("text")
        if "12 FEASIBILITY OF THE STUDY" not in next_text:
            next_page.insert_text((72, 74), "12 FEASIBILITY OF THE STUDY", fontname="helv", fontsize=10.5, color=(0, 0, 0))
        if "12.1 Researcher Competency and Technical Capacity" not in next_text:
            next_page.insert_text((72, 90), "12.1 Researcher Competency and Technical Capacity", fontname="helv", fontsize=9.2, color=(0, 0, 0))

    tmp_path = PDF_PATH.with_name(PDF_PATH.stem + "_tmp.pdf")
    doc.save(tmp_path, garbage=4, deflate=True)
    doc.close()

    shutil.move(str(tmp_path), str(PDF_PATH))

    report = []
    report.append(f"Updated: {PDF_PATH}")
    report.append(f"Page: {target_page_index + 1}")
    report.append(f"Redaction rect: {redact}")
    report.append(f"Font size used: {used_size}")
    report.append("Section 11.3 replaced with 9-phase UNIZULU-aligned workflow table.")
    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")

    print(f"Updated: {PDF_PATH}")
    print(f"Report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
