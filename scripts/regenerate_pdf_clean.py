#!/usr/bin/env python3
"""
Regenerate Research_Proposal_Hardened_Final.pdf with clean methodology section.
This script rebuilds the PDF from pages 1-10 and 15+ (preserving them),
then inserts newly rendered methodology pages 11-14 without redaction artifacts.
"""

import fitz  # PyMuPDF
import io
from pathlib import Path

PDF_PATH = Path(__file__).parent.parent / "docs" / "Research_Proposal_Hardened_Final.pdf"
BACKUP_PDF = Path(__file__).parent.parent / "docs" / "Research_Proposal_Methodology_Backup.pdf"
OUTPUT_PDF = PDF_PATH  # Overwrite in-place
TMP_PDF = Path(__file__).parent.parent / "docs" / "Research_Proposal_Clean_Temp.pdf"

METHODOLOGY_TEXT = """## 8 RESEARCH METHODOLOGY

This study adopts a methodology designed to produce objective, reproducible, and decision-relevant evidence on the comparative performance of AI-driven and heuristic controller placement methods in multi-site SDN environments.

### 8.1 Research Philosophy

This study is grounded in a positivist research philosophy. Positivism is appropriate because the phenomenon under investigation is measurable and testable: controller placement methods produce observable outcomes such as latency, reliability, runtime, and resource cost. The aim is not to interpret subjective experiences, but to evaluate whether one algorithmic class performs better than another under controlled conditions.

### 8.2 Research Approach

The study follows a deductive research approach. Deduction is suitable because the investigation begins with existing ideas from optimization theory and controller placement literature, then tests whether predefined methods satisfy explicit performance criteria. This aligns with the research trajectory: problem statement identifies a decision gap, research questions ask whether AI methods offer meaningful advantages, and the methodology tests that claim through controlled experimentation.

### 8.3 Research Design

The study uses an experimental research design with a factorial structure. Experimental design is appropriate because the core purpose is to compare method performance under controlled and repeatable conditions. The factorial framework examines multiple independent variables simultaneously: method type, topology family, and network scale. This enables observation of main effects and interaction effects, supporting scenario-conditioned method selection guidance.

### 8.4 Data Collection

Data collection is conducted in a controlled simulation and emulation workflow rather than through human participants. This is appropriate because the research problem concerns measurable algorithmic performance under standardized conditions. The collection process is designed to preserve repeatability, minimize uncontrolled variance, and support transparent cross-method comparison.

#### 8.4.1 Parameter Justification and Technical Stack Defense

This study adopts Mininet, a PyTorch-based DQN/DRL implementation, and Internet2/ATT-MPLS-class topologies as a tightly coupled methodological stack because this is the only configuration that simultaneously satisfies baseline comparability, metric transparency, and operational realism across the three method families in the literature. This choice is necessitated by the empirical structure of prior work.

Group A foundational studies show that controller-placement claims are highly topology-dependent, with Internet2-scale evaluation establishing the canonical latency baseline (Heller et al., 2012). Group B meta-heuristic studies report strong gains under simulation-specific settings, but with transferability and parameter-sensitivity limitations (Radam et al., 2022). Group C DQN/DRL studies report substantial improvements but often under-specify reproducibility-critical implementation details and reliability operationalization (Farahi et al., 2026; Benoudifa et al., 2023).

First, baseline parity is non-negotiable. The use of Internet2 and ATT-MPLS-class topologies is deliberate to replicate the structural conditions under which foundational CPP latency claims were established (Heller et al., 2012). Ensuring cross-study parity at the topology layer prevents inflated AI claims caused by easier synthetic graph regimes.

Second, this study introduces a formal reliability specification to eliminate black-box scoring. Reliability is explicitly defined as the mean fraction of nodes that remain controller-reachable under single-link failure across all edge removals. Directly addressing reporting limitations where reliability is presented as an aggregate score without fully auditable operationalization (Benoudifa et al., 2023), this definition makes each reliability claim independently recalculable from graph state and controller set.

Third, the reproducibility pivot to a full PyTorch DQN/DRL stack is required by convergence-control expectations in AP-DQN and MuZero literature (Farahi et al., 2026; Benoudifa et al., 2023). The prior lightweight reward baseline is useful for exploratory benchmarking but cannot provide replay-based stabilization, target-network synchronization, and gradient-level diagnostics expected in contemporary DRL evidence. Farahi et al. (2026) report concrete DQN settings: learning rate 0.001, batch size 32, discount factor gamma 0.99, and 1000 episodes. These values provide a quantitative reference band for implementation and hyperparameter calibration.

Finally, operational validity requires Mininet with Iperf3-driven traffic generation. Analytical or offline optimization remains essential for theory but insufficient for deployment-facing inference. Mininet introduces packet-level behavior, contention effects, and emulation-time variability that abstract graph optimization cannot represent.

#### 8.4.2 Design and Description of Instruments

The study instruments include Mininet and Python-based simulation/emulation environment, DQN/DRL and baseline controller-placement implementations, experiment orchestration scripts, structured logging pipelines, and metric extraction utilities. This design is justified because it combines parameter control, repeatability, and operational safety, and avoids disruption of production network infrastructure.

#### 8.4.3 Data Collection Procedures

Data collection proceeds in a controlled sequence: First, experimental topologies are generated or selected by predefined topology families and scale levels. Second, each controller-placement method is executed under identical topology and scale conditions to preserve attribution fairness. Third, each run captures structured logs, packet-level traces, and metric artifacts for auditability. Latency is derived from control-related communication propagation. Reliability is computed as the mean fraction of nodes reachable from at least one controller under each single-link failure. Computational cost is derived from runtime, convergence duration, and execution overhead.

### 8.5 Data Analysis Methods and Procedures

The analysis combines descriptive, inferential, and multi-objective methods. Descriptive statistics summarize means, dispersion, and performance ranges per method and scenario. Inferential analysis uses t-tests for pairwise comparisons and analysis of variance for factorial effects and interactions across method type, topology family, and network scale. Pareto-front analysis evaluates trade-offs across latency, reliability, and computational cost. This integrated strategy supports positivist validity requirements by making claims measurable, replicable, and statistically testable, while producing scenario-conditioned decision guidance for practical controller-placement selection.

### 8.6 Research Quality: Ethical and Safety Issues

### 8.7 Data Management and Storage"""

def main():
    print("Regenerating PDF with clean methodology pages...")
    
    # Open original PDF
    doc = fitz.open(PDF_PATH)
    
    # Create new document starting from page 1–10 (index 0–9)
    new_doc = fitz.open()
    
    # Copy pages 1–10 (indices 0–9) from original
    for i in range(10):
        if i < len(doc):
            new_doc.insert_pdf(doc, from_page=i, to_page=i)
    
    # Create new methodology pages (11–14) with text layout
    methodology_pages = _create_methodology_pages()
    for page in methodology_pages:
        new_doc.insert_pdf(page)
    
    # Append pages 15+ (indices 14+) from original if they exist
    for i in range(14, len(doc)):
        new_doc.insert_pdf(doc, from_page=i, to_page=i)
    
    # Save as temporary file first, then replace original
    new_doc.save(str(TMP_PDF), garbage=4, deflate=True)
    new_doc.close()
    doc.close()
    
    # Replace original
    import shutil
    shutil.copy(OUTPUT_PDF, BACKUP_PDF)  # Create backup
    shutil.move(str(TMP_PDF), str(OUTPUT_PDF))
    
    print(f"✅ Clean PDF regenerated: {OUTPUT_PDF}")
    print(f"✅ Backup saved: {BACKUP_PDF}")


def _create_methodology_pages():
    """Create new methodology pages 11–14 as fresh fitz documents."""
    pages = []
    
    # Page 11: Sections 8.1–8.4 intro
    doc11 = fitz.open()
    page11 = doc11.new_page(width=595, height=842)  # A4
    _insert_text_block(page11, METHODOLOGY_TEXT[:2000], y_start=50)
    pages.append(doc11)
    
    # Page 12: Section 8.4.1 part 1
    doc12 = fitz.open()
    page12 = doc12.new_page(width=595, height=842)
    _insert_text_block(page12, METHODOLOGY_TEXT[2000:5000], y_start=50)
    pages.append(doc12)
    
    # Page 13: Section 8.4.1–8.4.3
    doc13 = fitz.open()
    page13 = doc13.new_page(width=595, height=842)
    _insert_text_block(page13, METHODOLOGY_TEXT[5000:8000], y_start=50)
    pages.append(doc13)
    
    # Page 14: Section 8.5–8.7
    doc14 = fitz.open()
    page14 = doc14.new_page(width=595, height=842)
    _insert_text_block(page14, METHODOLOGY_TEXT[8000:], y_start=50)
    pages.append(doc14)
    
    return pages


def _insert_text_block(page, text, y_start=50, fontsize=10.5):
    """Insert text block into page with word wrap."""
    rect = fitz.Rect(50, y_start, 545, 800)  # A4 standard margins
    page.insert_textbox(rect, text, fontsize=fontsize, fontname="helv", color=(0, 0, 0))


if __name__ == "__main__":
    main()
