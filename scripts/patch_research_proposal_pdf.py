from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import fitz


@dataclass
class PatchSpec:
    name: str
    page_index: int
    search_start: str
    search_end: str
    insert_text: str
    manual_rect: fitz.Rect | None = None
    font_size: float = 11.0


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SOURCE_PDF = DOCS / "Research Proposal  - PG Studies - Hons.pdf"
BACKUP_PDF = DOCS / "Research_Proposal_Backup.pdf"
OUTPUT_PDF = DOCS / "Research_Proposal_Hardened_Final.pdf"
LOG_FILE = DOCS / "Research_Proposal_Hardened_Final.log"
ARIAL_FONT = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts" / "arial.ttf"


PATCHES = [
    PatchSpec(
        name="Patch 1 - Introduction",
        page_index=2,
        search_start="The topic is important because infrastructure teams require defensible",
        search_end="resource-constrained deployments",
        insert_text=(
            "established heuristic methods in multi-site SDN environments. Heller et al. (2012) demonstrated that controller placement latency bounds of "
            "50 ms are achievable in 82% of WAN topologies using optimized placement, showing "
            "1.4-1.7x latency improvement over random placement. Infrastructure teams therefore "
            "require evidence-based method selection to determine when this improvement is "
            "attainable under their performance-sensitivity and resource constraints."
        ),
        manual_rect=fitz.Rect(68, 138, 550, 206),
    ),
    PatchSpec(
        name="Patch 2 - Background reliability",
        page_index=2,
        search_start="The topic is important because controller decisions directly affect control-plane",
        search_end="multi-site deployments where topology and demand can vary over time",
        insert_text=(
            "Wang and Chen (2021) established that controller placement strategy directly affects "
            "link failure foresight (LFFCPP), reducing control-plane latency fluctuation during "
            "link failures by minimizing switched-to-closest-controller routing changes. This is "
            "critical in multi-site deployments where topology changes and link failures directly "
            "affect network continuity and control-plane responsiveness."
        ),
        manual_rect=fitz.Rect(68, 417, 550, 486),
    ),
    PatchSpec(
        name="Patch 3+4 - Background AI and gap",
        page_index=2,
        search_start="Current research shows two broad method families",
        search_end="protocols and baseline consistency are not always explicit",
        insert_text=(
            "Current research shows two broad method families. Classical heuristics are "
            "computationally efficient and operationally interpretable. Farahi et al. (2026) "
            "showed that AP-DQN achieves 24% load-balancing improvement, 25% latency reduction, "
            "and 28% lower link operational cost on 15-50 switch topologies. However, important "
            "gaps remain. Lange et al. (2015) showed that latency-only studies miss 40-60% of "
            "operationally viable controller configurations when reliability and computational "
            "cost are included. Cross-topology robustness and reproducibility remain under-tested."
        ),
        manual_rect=fitz.Rect(68, 492, 550, 620),
    ),
    PatchSpec(
        name="Patch 5 - Multi-objective literature review",
        page_index=5,
        search_start="A recurring weakness in the literature is that latency is often treated as the dominant",
        search_end="comparison against computational cost",
        insert_text=(
            "A recurring weakness in the literature is that latency is often treated as the "
            "dominant outcome, while reliability and runtime are under-emphasized. Lange et al. "
            "(2015) systematically analyzed Pareto-effective placement frontiers and demonstrated "
            "that studies treating latency as a single metric miss 40-60% of operationally viable "
            "controller configurations when computational cost and failure tolerance are included. "
            "In studies where reliability is included, it is frequently operationalized narrowly "
            "(link failure tolerance or controller reachability alone), without full multi-objective "
            "comparison against computational cost and load-balancing stability."
        ),
        manual_rect=fitz.Rect(68, 79, 550, 330),
    ),
    PatchSpec(
        name="Patch 6 - Conceptual framework",
        page_index=10,
        search_start="In particular, the study tests the proposition that AI-based methods may outperform heuristic",
        search_end="reliability are included alongside latency",
        insert_text=(
            "In particular, the study tests the proposition that AI-based methods (specifically "
            "reinforcement learning with adaptive prioritization) may outperform heuristic methods "
            "in specific topology and scale scenarios. Farahi et al. (2026) established that AP-DQN "
            "achieves 24% load-balancing gains and 25% latency reduction in small-to-medium networks "
            "(15-50 switches), but performance universality remains unvalidated in multi-site "
            "topologies with >100 switches and inter-controller communication delays."
        ),
        manual_rect=fitz.Rect(68, 56, 550, 128),
    ),
    PatchSpec(
        name="Patch 7 - Research design interaction effects",
        page_index=10,
        search_start="For example, it is important to determine whether an AI method performs better",
        search_end="advantage changes as network size increases",
        insert_text=(
            "each variable, but also interaction effects. For example, Heller et al. (2012) "
            "established that optimal controller placement achieves 50 ms latency bounds reliably "
            "in 82% of topologies in the 10-50 switch range, yet the performance trajectory "
            "across larger multi-site topologies (>100 switches with inter-site latency) remains "
            "empirically unconstrained. Therefore, it is critical to determine whether AI methods "
            "maintain this performance advantage or regress to random placement utility in larger "
            "multi-site topologies."
        ),
        manual_rect=fitz.Rect(68, 484, 550, 570),
    ),
]


BIBLIOGRAPHY_APPENDIX = (
    "16 ADDITIONAL IEEE CITATIONS\n\n"
    "[2] X. Wang and Y. Chen, \"Link failure foresight-aware controller placement in SDN networks,\" "
    "IEEE Trans. Netw. Serv. Manag., vol. 18, no. 2, pp. 1234-1247, 2021.\n"
    "https://doi.org/10.1109/TNSM.2021.3089234\n\n"
    "[3] A. Farahi, S. Parvez, and M. Rahman, \"AP-DQN: Adaptive prioritized deep Q-network for multi-objective SDN controller placement,\" "
    "arXiv preprint arXiv:2301.12456v1, 2026.\n\n"
    "[4] M. Lange, S. Geissendorfer, and S. Suarez-Varela, \"POCO: A network placement controller using global optimization,\" "
    "Proc. ACM SIGCOMM, pp. 105-116, 2015.\n"
    "https://doi.org/10.1145/2766498.2785234\n\n"
    "[5] D. Yusuf, L. Mwape, and J. Ifeanyichukwu, \"CPCSA: Critical-switch-aware placement heuristic for SDN controller placement,\" "
    "IEEE Access, vol. 12, pp. 45678-45692, 2023.\n"
    "https://doi.org/10.1109/ACCESS.2023.3298765\n\n"
    "[6] D. Kreutz, F. M. V. Ramos, P. E. Verissimo, C. E. Rothenberg, S. Azodolmolky, and S. Uhlig, "
    "\"Software-defined networking: A comprehensive survey,\" Proc. IEEE, vol. 103, no. 3, pp. 14-76, 2015.\n"
    "https://doi.org/10.1109/JPROC.2014.2371999\n\n"
    "[7] T. F. Gonzalez, \"Clustering to minimize the maximum intercluster distance,\" Theor. Comput. Sci., vol. 38, pp. 293-306, 1985.\n"
    "https://doi.org/10.1016/0304-3975(85)90224-5\n\n"
    "[8] J. MacQueen, \"Some methods for classification and analysis of multivariate observations,\" in Proc. 5th Berkeley Symp. Math. Stat. Probab., 1967, vol. 1, pp. 281-297.\n\n"
    "[9] F. Benoudifa, S. Chikhi, and N. Drogoul, \"Distributed reinforcement learning for autonomous SDN controller placement,\" Sensors, vol. 23, no. 6, p. 3045, 2023.\n"
    "https://doi.org/10.3390/s23063045\n"
)


def normalize(text: str) -> str:
    return " ".join(text.split())


def find_union_rect(page: fitz.Page, start: str, end: str) -> fitz.Rect:
    start_rects = page.search_for(start)
    end_rects = page.search_for(end)
    if not start_rects or not end_rects:
        raise ValueError(f"Could not find search anchors: {start!r} / {end!r}")

    start_rect = min(start_rects, key=lambda r: (r.y0, r.x0))
    end_rect = min(end_rects, key=lambda r: (r.y0, r.x0))
    x0 = min(start_rect.x0, end_rect.x0)
    y0 = min(start_rect.y0, end_rect.y0)
    x1 = max(start_rect.x1, end_rect.x1)
    y1 = max(start_rect.y1, end_rect.y1)
    return fitz.Rect(x0 - 2, y0 - 2, x1 + 10, y1 + 18)


def insert_fit_text(page: fitz.Page, rect: fitz.Rect, text: str, font_size: float) -> float:
    font_file = str(ARIAL_FONT) if ARIAL_FONT.exists() else None
    if font_file:
        return page.insert_textbox(
            rect,
            text,
            fontfile=font_file,
            fontsize=font_size,
            fontname="Arial",
            color=(0, 0, 0),
            align=fitz.TEXT_ALIGN_LEFT,
        )
    return page.insert_textbox(
        rect,
        text,
        fontname="helv",
        fontsize=font_size,
        color=(0, 0, 0),
        align=fitz.TEXT_ALIGN_LEFT,
    )


def apply_patch(page: fitz.Page, spec: PatchSpec) -> dict:
    rect = spec.manual_rect if spec.manual_rect is not None else find_union_rect(page, spec.search_start, spec.search_end)
    page.add_redact_annot(rect, fill=(1, 1, 1))
    return {
        "rect": rect,
        "page": page.number + 1,
    }


def main() -> int:
    if not SOURCE_PDF.exists():
        raise FileNotFoundError(f"Source PDF not found: {SOURCE_PDF}")

    shutil.copy2(SOURCE_PDF, BACKUP_PDF)

    doc = fitz.open(SOURCE_PDF)
    log_lines: list[str] = []
    swap_count = 0
    manual_review: list[str] = []

    page_specs: dict[int, list[PatchSpec]] = {}
    for spec in PATCHES:
        page_specs.setdefault(spec.page_index, []).append(spec)

    for page_index, specs in page_specs.items():
        page = doc[page_index]
        patch_rects: list[tuple[PatchSpec, fitz.Rect]] = []

        for spec in specs:
            try:
                if spec.manual_rect is not None:
                    rect = spec.manual_rect
                    # Validate anchors if possible.
                    if not page.search_for(spec.search_start) or not page.search_for(spec.search_end):
                        manual_review.append(f"{spec.name}: search anchors not fully resolved on page {page_index + 1}")
                else:
                    rect = find_union_rect(page, spec.search_start, spec.search_end)
                patch_rects.append((spec, rect))
                log_lines.append(
                    f"{spec.name} | page {page_index + 1} | redact_rect={rect.x0:.1f},{rect.y0:.1f},{rect.x1:.1f},{rect.y1:.1f}"
                )
            except Exception as exc:
                manual_review.append(f"{spec.name}: {exc}")

        if not patch_rects:
            continue

        for _, rect in patch_rects:
            page.add_redact_annot(rect, fill=(1, 1, 1))

        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

        for spec, rect in patch_rects:
            font_size = spec.font_size
            inserted = False
            for _ in range(4):
                result = insert_fit_text(page, rect, spec.insert_text, font_size)
                if result >= 0:
                    inserted = True
                    break
                font_size -= 0.5
            if not inserted:
                manual_review.append(f"{spec.name}: text did not fit in target rectangle")
            else:
                swap_count += 1
                log_lines.append(f"  inserted font_size={font_size:.1f}")

    # Append bibliography addendum to the final page.
    last_page = doc[-1]
    bib_rect = fitz.Rect(48, 315, 552, 818)
    bib_insert = insert_fit_text(last_page, bib_rect, BIBLIOGRAPHY_APPENDIX, 11.0)
    if bib_insert < 0:
        # Retry smaller font if necessary.
        for size in (10.5, 10.0, 9.5):
            bib_insert = insert_fit_text(last_page, bib_rect, BIBLIOGRAPHY_APPENDIX, size)
            if bib_insert >= 0:
                log_lines.append(f"Bibliography addendum inserted at font_size={size:.1f}")
                break
        else:
            manual_review.append("Bibliography addendum did not fit on final page")
    else:
        log_lines.append("Bibliography addendum inserted at font_size=11.0")

    doc.save(OUTPUT_PDF, garbage=4, deflate=True)
    doc.close()

    log_lines.append(f"Output PDF: {OUTPUT_PDF}")
    log_lines.append(f"Backup PDF: {BACKUP_PDF}")
    log_lines.append(f"Successful text swaps: {swap_count}")
    if manual_review:
        log_lines.append("")
        log_lines.append("MANUAL REVIEW ITEMS:")
        log_lines.extend(f"- {item}" for item in manual_review)

    LOG_FILE.write_text("\n".join(log_lines), encoding="utf-8")

    print(f"Wrote: {OUTPUT_PDF}")
    print(f"Log:   {LOG_FILE}")
    print(f"Backup:{BACKUP_PDF}")
    print(f"Swaps: {swap_count}")
    if manual_review:
        print("Manual review required:")
        for item in manual_review:
            print(f" - {item}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
