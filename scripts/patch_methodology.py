"""Patch Section 8.4-8.5 in the proposal PDF with merged methodology text.

This script:
1) Locates Section 8.4 start and Section 9 start
2) Redacts the 8.4-8.5 area across pages
3) Inserts updated 8.4, 8.4.1, 8.4.2, 8.4.3, and 8.5 text blocks
4) Saves updated PDF and creates a backup
"""

from __future__ import annotations

from pathlib import Path
import shutil
import fitz

ROOT = Path(r"c:\Users\fanele\AI-Driven Controller Placement Optimization in Multi-Site Software Defined Networks\ai-sdn-controller-placement")
DOCS = ROOT / "docs"
PDF_PATH = DOCS / "Research_Proposal_Hardened_Final.pdf"
BACKUP_PATH = DOCS / "Research_Proposal_Methodology_Backup.pdf"
TMP_PATH = DOCS / "Research_Proposal_Hardened_Final.tmp.pdf"

# Updated methodology text split across patched pages to avoid overflow/clipping.
BLOCK_1 = (
    "8.4 Data collection\n"
    "Data collection is conducted in a controlled simulation and emulation workflow rather than through human participants. "
    "This is appropriate because the research problem concerns measurable algorithmic performance under standardized conditions. "
    "The collection process is designed to preserve repeatability, minimize uncontrolled variance, and support transparent cross-method comparison.\n\n"
    "8.4.1 Parameter Justification and Technical Stack Defense\n"
    "This study adopts Mininet, a PyTorch-based DQN/DRL implementation, and Internet2/ATT-MPLS-class topologies as a tightly coupled methodological stack because this is the only configuration that simultaneously satisfies baseline comparability, metric transparency, and operational realism across the three method families in the literature. "
    "This choice is necessitated by the empirical structure of prior work. Group A foundational studies show that controller-placement claims are highly topology-dependent, with Internet2-scale evaluation establishing the canonical latency baseline (Heller et al., 2012). "
    "Group B meta-heuristic studies report strong gains under simulation-specific settings, but with transferability and parameter-sensitivity limitations (Radam et al., 2022). "
    "Group C DQN/DRL studies report substantial improvements but often under-specify reproducibility-critical implementation details and reliability operationalization (Farahi et al., 2026; Benoudifa et al., 2023)."
)

BLOCK_2 = (
    "First, baseline parity is non-negotiable. The use of Internet2 and ATT-MPLS-class topologies is deliberate to replicate the structural conditions under which foundational CPP latency claims were established (Heller et al., 2012). "
    "Ensuring cross-study parity at the topology layer prevents inflated AI claims caused by easier synthetic graph regimes.\n\n"
    "Second, this study introduces a formal reliability specification to eliminate black-box scoring. Reliability is explicitly defined as the mean fraction of nodes that remain controller-reachable under single-link failure across all edge removals. "
    "Directly addressing reporting limitations where reliability is presented as an aggregate score without fully auditable operationalization (Benoudifa et al., 2023), this definition makes each reliability claim independently recalculable from graph state and controller set.\n\n"
    "Third, the reproducibility pivot to a full PyTorch DQN/DRL stack is required by convergence-control expectations in AP-DQN and MuZero literature (Farahi et al., 2026; Benoudifa et al., 2023). "
    "The prior lightweight reward baseline is useful for exploratory benchmarking but cannot provide replay-based stabilization, target-network synchronization, and gradient-level diagnostics expected in contemporary DRL evidence. "
    "Farahi et al. (2026) report concrete DQN settings, including learning rate 0.001, batch size 32, discount factor gamma 0.99, and 1000 episodes. These values provide a quantitative reference band for implementation and hyperparameter calibration.\n\n"
    "Finally, operational validity requires Mininet with Iperf3-driven traffic generation. Analytical or offline optimization remains essential for theory but insufficient for deployment-facing inference. "
    "Mininet introduces packet-level behavior, contention effects, and emulation-time variability that abstract graph optimization cannot represent."
)

BLOCK_3 = (
    "8.4.2 Design and description of instruments\n"
    "The study instruments include the simulation and emulation environment, DQN/DRL and baseline controller-placement implementations, experiment orchestration scripts, structured logging pipelines, and metric extraction utilities. "
    "Mininet and Python-based instrumentation serve as the primary operational environment for repeatable network experimentation, while topology datasets and generators support controlled scenario construction. "
    "This design is justified because it combines parameter control, repeatability, and operational safety, and avoids disruption of production network infrastructure.\n\n"
    "8.4.3 Data collection procedure(s)\n"
    "Data collection proceeds in a controlled sequence. First, experimental topologies are generated or selected by predefined topology families and scale levels. "
    "Second, each controller-placement method is executed under identical topology and scale conditions to preserve attribution fairness. "
    "Third, each run captures structured logs, packet-level traces, and metric artifacts for auditability. "
    "Latency is derived from control-related communication propagation. Reliability is computed as the mean fraction of nodes reachable from at least one controller under each single-link failure. "
    "Computational cost is derived from runtime, convergence duration, and execution overhead."
)

BLOCK_4 = (
    "8.5 Data analysis method(s) and procedure\n"
    "The analysis combines descriptive, inferential, and multi-objective methods. Descriptive statistics summarize means, dispersion, and performance ranges per method and scenario. "
    "Inferential analysis uses t-tests for pairwise comparisons and analysis of variance for factorial effects and interactions across method type, topology family, and network scale. "
    "Pareto-front analysis is then used to evaluate trade-offs across latency, reliability, and computational cost. This is appropriate because success is not defined by a single metric; methods are evaluated by dominance patterns and compromise quality in combined objective space.\n\n"
    "This integrated strategy supports positivist validity requirements by making claims measurable, replicable, and statistically testable, while producing scenario-conditioned decision guidance for practical controller-placement selection."
)


def locate_anchor_page(doc: fitz.Document, anchor: str) -> tuple[int, fitz.Rect]:
    for i in range(len(doc)):
        rects = doc[i].search_for(anchor)
        if rects:
            return i, rects[0]
    raise RuntimeError(f"Anchor not found: {anchor}")


def redact_section(doc: fitz.Document, start_page: int, start_y: float, end_page: int, end_y: float) -> None:
    left = 60
    right = 552
    top_margin = 55
    bottom_margin = 790

    for page_idx in range(start_page, end_page + 1):
        page = doc[page_idx]
        if page_idx == start_page and page_idx == end_page:
            rect = fitz.Rect(left, max(top_margin, start_y - 4), right, min(bottom_margin, end_y - 8))
        elif page_idx == start_page:
            rect = fitz.Rect(left, max(top_margin, start_y - 4), right, bottom_margin)
        elif page_idx == end_page:
            rect = fitz.Rect(left, top_margin, right, min(bottom_margin, end_y - 8))
        else:
            rect = fitz.Rect(left, top_margin, right, bottom_margin)

        page.add_redact_annot(rect, fill=(1, 1, 1))
        page.apply_redactions()


def insert_blocks(doc: fitz.Document, start_page: int) -> None:
    # Tuned rectangles for Pages 11-14 (1-based), where Section 8.4-8.5 resides.
    rects = [
        fitz.Rect(68, 540, 548, 786),  # page 11 area starting at 8.4 heading
        fitz.Rect(68, 62, 548, 786),   # page 12
        fitz.Rect(68, 62, 548, 786),   # page 13
        fitz.Rect(68, 62, 548, 640),   # page 14; stop before Section 9 heading
    ]
    blocks = [BLOCK_1, BLOCK_2, BLOCK_3, BLOCK_4]
    font_sizes = [10.2, 10.2, 10.4, 10.4]

    for offset, (text, rect, fs) in enumerate(zip(blocks, rects, font_sizes)):
        page = doc[start_page + offset]
        result = page.insert_textbox(
            rect,
            text,
            fontsize=fs,
            fontname="helv",
            color=(0, 0, 0),
            align=fitz.TEXT_ALIGN_LEFT,
        )
        if result < 0:
            raise RuntimeError(f"Text overflow on page {start_page + offset + 1}: deficit={result}")


def main() -> None:
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"Target PDF not found: {PDF_PATH}")

    shutil.copy(PDF_PATH, BACKUP_PATH)

    doc = fitz.open(PDF_PATH)

    start_page, start_rect = locate_anchor_page(doc, "8.4 Data collection")
    end_page, end_rect = locate_anchor_page(doc, "RESEARCH QUALITY: ETHICAL AND SAFETY ISSUES")

    # Redact section 8.4-8.5 region and insert updated blocks.
    redact_section(doc, start_page, start_rect.y0, end_page, end_rect.y0)
    insert_blocks(doc, start_page)

    doc.save(TMP_PATH, garbage=4, deflate=True)
    doc.close()

    shutil.move(TMP_PATH, PDF_PATH)
    print(f"Updated PDF: {PDF_PATH}")
    print(f"Backup PDF: {BACKUP_PATH}")


if __name__ == "__main__":
    main()
