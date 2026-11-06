#!/usr/bin/env python3
"""
Compilation script for University of Zululand BSc Honours Mini-Dissertation.
Builds Honours_Mini_Dissertation_Thabang_Buthelezi.docx and .pdf using the exact
Cover Pages (with University of Zululand crest/logo), 3-Section Roman/Arabic page
numbering layout, and populated Table of Contents from:
  docs/Honours Mini-Dissertation Template (1).docx
"""

import io
import re
import sys
import shutil
import zipfile
import subprocess
from copy import deepcopy
from pathlib import Path

import docx
from docx.shared import Pt, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from lxml import etree

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DISSERTATION_DIR = PROJECT_ROOT / "dissertation"
DOCS_DIR = PROJECT_ROOT / "docs"
TEMPLATE_DOCX = DOCS_DIR / "Honours Mini-Dissertation Template (1).docx"

CHAPTERS = [
    "00_front_matter.md",
    "01_chapter_1_introduction.md",
    "02_chapter_2_literature_review.md",
    "03_chapter_3_methodology.md",
    "04_chapter_4_results_and_discussion.md",
    "05_chapter_5_conclusion.md",
    "06_references.md",
    "07_appendices.md",
]

BODY_CHAPTERS = CHAPTERS[1:]

MASTER_MD = DISSERTATION_DIR / "Honours_Mini_Dissertation_Thabang_Buthelezi.md"
OUTPUT_DOCX = DISSERTATION_DIR / "Honours_Mini_Dissertation_Thabang_Buthelezi.docx"
OUTPUT_PDF = DISSERTATION_DIR / "Honours_Mini_Dissertation_Thabang_Buthelezi.pdf"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"

TITLE_TEXT = (
    "Decision-Grade Multi-Objective Benchmarking of AI and Heuristic "
    "Controller Placement in Multi-Site Software Defined Networks"
)

FIGURES_LIST = [
    ("Figure 3.1", "Figure 3.1: End-to-End Comparative Research Methodology Workflow."),
    ("Figure 3.2", "Figure 3.2: System Architecture of the Multi-Objective Controller Placement Benchmark and Mininet Emulation Harness."),
    ("Figure 4.1", "Figure 4.1: PyTorch DQN 1,000-Episode Training Reward Convergence Profile on Canonical Internet2 Topology (N = 20, k = 3)."),
    ("Figure 4.2", "Figure 4.2: Multi-Seed DQN Convergence and Rolling Reward Distribution Analysis."),
    ("Figure 4.3", "Figure 4.3: Pareto Latency-Cost Trade-Off Frontier on Barabási-Albert Topology (N = 50, k = 3)."),
    ("Figure 4.4", "Figure 4.4: Pareto Latency-Cost Trade-Off Frontier on Waxman Spatial Topology (N = 50, k = 3)."),
    ("Figure 4.5", "Figure 4.5: Three-Dimensional Multi-Objective Pareto Surface Mapping Propagation Latency, Single-Link Reliability, and Computational Complexity Tax."),
    ("Figure 4.6", "Figure 4.6: Bounded Infrastructure Deployment Decision Flowchart (N <= 50)."),
]

TABLES_LIST = [
    ("Table 2.1:", "Table 2.1: Literature Synthesis on SDN Controller Placement (2012–2026)."),
    ("Table 3.1:", "Table 3.1: Summary of Canonical and Synthetic Network Topology Parameters."),
    ("Table 3.2:", "Table 3.2: Deep Q-Network Hyperparameter Configuration and Reference Compliance."),
    ("Table 3.3:", "Table 3.3: Full Factorial Benchmark Design Matrix (2 x 2 x 3 x 5 = 60 Cells)."),
    ("Table 4.1:", "Table 4.1: Multi-Seed Stability Audit Results for Deep Q-Network Across 10 Independent Runs."),
    ("Table 4.2:", "Table 4.2: Summary of Factorial Performance Metrics for Barabási-Albert Topologies."),
    ("Table 4.3:", "Table 4.3: Summary of Factorial Performance Metrics for Waxman Spatial Topologies."),
    ("Table 4.4:", "Table 4.4: Multi-Objective Benchmark Comparison on Canonical Topologies at k = 5."),
    ("Table 4.4b:", "Table 4.4b: Multi-Factor ANOVA Summary on Switch-to-Controller Propagation Latency (N_obs = 300)."),
    ("Table 4.5:", "Table 4.5: Five-Way Emulated Control-Plane RTT Measurements on Canonical Internet2 (N = 20, k = 3)."),
    ("Table 4.6:", "Table 4.6: Phase 4 Mininet Overhead Gate Test Timing Breakdown Across 3 Trials."),
    ("Table 4.7:", "Table 4.7: Scenario-Conditioned Algorithm Selection Decision Rules (Bounded to N <= 50)."),
    ("Table B.1:", "Table B.1: Complete Proposal-Aligned Multi-Objective Benchmark Matrix Across Canonical and Synthetic Topologies."),
]

ABBREVIATIONS_LIST = [
    ("AI", "Artificial Intelligence"),
    ("ANOVA", "Analysis of Variance"),
    ("API", "Application Programming Interface"),
    ("BA", "Barabási-Albert (Scale-Free Network Model)"),
    ("CPP", "Controller Placement Problem"),
    ("CPU", "Central Processing Unit"),
    ("DQN", "Deep Q-Network"),
    ("DRL", "Deep Reinforcement Learning"),
    ("GA", "Genetic Algorithm"),
    ("HSD", "Honest Significant Difference (Tukey's test)"),
    ("MDP", "Markov Decision Process"),
    ("MLP", "Multi-Layer Perceptron"),
    ("MPLS", "Multi-Protocol Label Switching"),
    ("NOS", "Network Operating System"),
    ("OVS", "Open vSwitch"),
    ("RL", "Reinforcement Learning"),
    ("RTT", "Round-Trip Time"),
    ("SDN", "Software Defined Networking"),
    ("TCAM", "Ternary Content Addressable Memory"),
    ("WAN", "Wide Area Network"),
    ("WX", "Waxman (Spatial Network Model)"),
]


def int_to_roman(n: int) -> str:
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ["m", "cm", "d", "cd", "c", "xc", "l", "xl", "x", "ix", "v", "iv", "i"]
    roman_num = ""
    i = 0
    while n > 0:
        for _ in range(n // val[i]):
            roman_num += syb[i]
            n -= val[i]
        i += 1
    return roman_num


def make_w_el(tag: str, **attrs):
    el = etree.Element(f"{{{W_NS}}}{tag}")
    for k, v in attrs.items():
        el.set(f"{{{W_NS}}}{k}", str(v))
    return el


def make_page_break_p():
    p = make_w_el("p")
    r = make_w_el("r")
    br = make_w_el("br", type="page")
    r.append(br)
    p.append(r)
    return p


def make_centered_heading1(text: str):
    p = make_w_el("p")
    pPr = make_w_el("pPr")
    pPr.append(make_w_el("pStyle", val="Heading1"))
    pPr.append(make_w_el("keepNext"))
    pPr.append(make_w_el("spacing", before="240", after="180", line="240", lineRule="auto"))
    pPr.append(make_w_el("ind", left="0", right="0", firstLine="0", hanging="0"))
    pPr.append(make_w_el("jc", val="center"))
    p.append(pPr)
    r = make_w_el("r")
    rPr = make_w_el("rPr")
    rPr.append(make_w_el("rFonts", ascii="Arial", hAnsi="Arial", cs="Arial"))
    rPr.append(make_w_el("b"))
    rPr.append(make_w_el("bCs"))
    rPr.append(make_w_el("color", val="000000"))
    rPr.append(make_w_el("sz", val="28"))
    rPr.append(make_w_el("szCs", val="28"))
    r.append(rPr)
    t = make_w_el("t")
    t.text = text
    r.append(t)
    p.append(r)
    return p


def make_body_p(text: str, bold: bool = False, italic: bool = False, align: str = "both", space_after: int = 160):
    p = make_w_el("p")
    pPr = make_w_el("pPr")
    pPr.append(make_w_el("pStyle", val="BodyText"))
    pPr.append(make_w_el("spacing", after=str(space_after), line="360", lineRule="auto"))
    pPr.append(make_w_el("ind", left="0", right="0", firstLine="0", hanging="0"))
    pPr.append(make_w_el("jc", val=align))
    p.append(pPr)
    if text:
        r = make_w_el("r")
        rPr = make_w_el("rPr")
        rFonts = make_w_el("rFonts", ascii="Arial", hAnsi="Arial", cs="Arial")
        rPr.append(rFonts)
        rPr.append(make_w_el("color", val="000000"))
        rPr.append(make_w_el("sz", val="24"))
        rPr.append(make_w_el("szCs", val="24"))
        if bold:
            rPr.append(make_w_el("b"))
        if italic:
            rPr.append(make_w_el("i"))
        r.append(rPr)
        t = make_w_el("t")
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        t.text = text
        r.append(t)
        p.append(r)
    return p


def make_tabbed_entry_p(label: str, page_str: str, style_id: str = "TOC1", bold: bool = False):
    p = make_w_el("p")
    pPr = make_w_el("pPr")
    pPr.append(make_w_el("pStyle", val=style_id))
    tabs = make_w_el("tabs")
    tab = make_w_el("tab", val="right", leader="dot", pos="9000")
    tabs.append(tab)
    pPr.append(tabs)
    pPr.append(make_w_el("spacing", after="80", line="240", lineRule="auto"))
    p.append(pPr)

    # Label run
    r1 = make_w_el("r")
    rPr1 = make_w_el("rPr")
    rPr1.append(make_w_el("rFonts", ascii="Arial", hAnsi="Arial", cs="Arial"))
    rPr1.append(make_w_el("color", val="000000"))
    rPr1.append(make_w_el("sz", val="22"))
    rPr1.append(make_w_el("szCs", val="22"))
    if bold:
        rPr1.append(make_w_el("b"))
    r1.append(rPr1)
    t1 = make_w_el("t")
    t1.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    t1.text = label
    r1.append(t1)
    p.append(r1)

    # Tab run
    r_tab = make_w_el("r")
    r_tab.append(make_w_el("tab"))
    p.append(r_tab)

    # Page number run
    r2 = make_w_el("r")
    rPr2 = make_w_el("rPr")
    rPr2.append(make_w_el("rFonts", ascii="Arial", hAnsi="Arial", cs="Arial"))
    rPr2.append(make_w_el("color", val="000000"))
    rPr2.append(make_w_el("sz", val="22"))
    rPr2.append(make_w_el("szCs", val="22"))
    if bold:
        rPr2.append(make_w_el("b"))
    r2.append(rPr2)
    t2 = make_w_el("t")
    t2.text = str(page_str)
    r2.append(t2)
    p.append(r2)
    return p


def build_toc_sdt(toc_entries):
    """Build the <w:sdt> Table of Contents block matching the University of Zululand template."""
    sdt = make_w_el("sdt")
    sdtPr = make_w_el("sdtPr")
    docPartObj = make_w_el("docPartObj")
    docPartObj.append(make_w_el("docPartGallery", val="Table of Contents"))
    docPartObj.append(make_w_el("docPartUnique"))
    sdtPr.append(docPartObj)
    sdt.append(sdtPr)

    sdtContent = make_w_el("sdtContent")
    for idx, (level, label, page_str) in enumerate(toc_entries):
        style_id = "TOC1" if level == 1 else "TOC2"
        is_bold = (
            level == 1
            and (
                label.startswith("CHAPTER ")
                or re.match(r"^[1-5]\.0\s", label)
                or label in ("DECLARATION", "DEDICATION", "ACKNOWLEDGEMENT", "LIST OF FIGURES", "LIST OF TABLES", "LIST OF ABBREVIATIONS", "ABSTRACT", "REFERENCES", "APPENDIX")
            )
        )
        p = make_tabbed_entry_p(label, page_str, style_id=style_id, bold=is_bold)
        sdtContent.append(p)
    sdt.append(sdtContent)
    return sdt


def build_cover_and_front_matter(doc, logo_bytes: bytes, sect0_pr, sect1_pr, page_map: dict):
    """
    Construct the complete XML element list for:
      - Section 0: Outer Cover Page (with University of Zululand logo) + Inner Title Page
      - Section 1: Declaration, Dedication, Acknowledgement, Table of Contents,
                   List of Figures, List of Tables, List of Abbreviations, Abstract
    """
    elements = []

    def make_cover_text_p(text: str, font_name: str = "Times New Roman", size_pt: int = 18, bold: bool = False, space_before: int = 0, space_after: int = 120):
        p = make_w_el("p")
        pPr = make_w_el("pPr")
        pPr.append(make_w_el("jc", val="center"))
        pPr.append(make_w_el("spacing", before=str(space_before), after=str(space_after), line="276", lineRule="auto"))
        p.append(pPr)
        if text:
            r = make_w_el("r")
            rPr = make_w_el("rPr")
            rPr.append(make_w_el("rFonts", ascii=font_name, hAnsi=font_name, cs=font_name))
            hp = str(int(size_pt * 2))
            rPr.append(make_w_el("sz", val=hp))
            rPr.append(make_w_el("szCs", val=hp))
            if bold:
                rPr.append(make_w_el("b"))
                rPr.append(make_w_el("bCs"))
            r.append(rPr)
            t = make_w_el("t")
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            t.text = text
            r.append(t)
            p.append(r)
        return p

    # --- PAGE 1: OUTER COVER PAGE (with University of Zululand Logo) ---
    elements.append(make_cover_text_p(TITLE_TEXT, font_name="Times New Roman", size_pt=22, bold=True, space_before=240, space_after=600))

    # Create a temporary paragraph in doc to generate the inline picture XML with proper rId
    logo_p = doc.add_paragraph()
    logo_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    logo_run = logo_p.add_run()
    logo_run.add_picture(io.BytesIO(logo_bytes), width=Emu(3673685), height=Emu(3873731))
    logo_el = deepcopy(logo_p._element)
    doc._body._body.remove(logo_p._element)
    elements.append(logo_el)

    elements.append(make_cover_text_p("THABANG NHLOKOMA BUTHELEZI", font_name="Calibri", size_pt=18, bold=True, space_before=960, space_after=720))
    elements.append(make_cover_text_p("2026", font_name="Calibri", size_pt=16, bold=True, space_before=480, space_after=120))
    elements.append(make_page_break_p())

    # --- PAGE 2: INNER TITLE PAGE ---
    elements.append(make_cover_text_p(TITLE_TEXT, font_name="Times New Roman", size_pt=22, bold=True, space_before=240, space_after=600))
    elements.append(make_cover_text_p("THABANG NHLOKOMA BUTHELEZI", font_name="Calibri", size_pt=18, bold=True, space_before=360, space_after=60))
    elements.append(make_cover_text_p("(230011908)", font_name="Calibri", size_pt=16, bold=False, space_before=0, space_after=480))
    elements.append(make_cover_text_p("A Mini dissertation submitted in partial fulfillment of the requirements", font_name="Calibri", size_pt=15, bold=False, space_before=120, space_after=120))
    elements.append(make_cover_text_p("For", font_name="Calibri", size_pt=15, bold=False, space_before=60, space_after=120))
    elements.append(make_cover_text_p("BSc Honours Degree in Computer Science", font_name="Calibri", size_pt=16, bold=True, space_before=60, space_after=360))
    elements.append(make_cover_text_p("Supervisor: Prof. Pragasen Mudali", font_name="Calibri", size_pt=15, bold=False, space_before=120, space_after=60))
    elements.append(make_cover_text_p("Co-Supervisor: Mr. Skhumbuzo Zwane", font_name="Calibri", size_pt=15, bold=False, space_before=0, space_after=480))
    elements.append(make_cover_text_p("Department of Computer Science,", font_name="Calibri", size_pt=15, bold=False, space_before=120, space_after=60))
    elements.append(make_cover_text_p("Faculty of Science, Agriculture and Engineering", font_name="Calibri", size_pt=15, bold=False, space_before=60, space_after=60))
    elements.append(make_cover_text_p("University of Zululand", font_name="Calibri", size_pt=15, bold=False, space_before=60, space_after=120))

    # End Section 0 with sect0_pr inside a paragraph
    p_sect0 = make_w_el("p")
    pPr_s0 = make_w_el("pPr")
    pPr_s0.append(deepcopy(sect0_pr))
    p_sect0.append(pPr_s0)
    elements.append(p_sect0)

    # --- SECTION 1: FRONT MATTER (Roman numerals i, ii, iii...) ---
    # 1. DECLARATION
    elements.append(make_centered_heading1("DECLARATION"))
    elements.append(make_body_p("", space_after=120))
    elements.append(make_body_p(
        "I, Thabang Nhlokoma Buthelezi (Student Number: 230011908), hereby declare that this mini-dissertation entitled:"
    ))
    elements.append(make_body_p(
        f'"{TITLE_TEXT}"', bold=True, italic=True, align="center", space_after=200
    ))
    elements.append(make_body_p(
        "is my own original work, conducted under the supervision of Prof. Pragasen Mudali and Mr. Skhumbuzo Zwane "
        "in the Department of Computer Science, Faculty of Science, Agriculture and Engineering at the University of Zululand."
    ))
    elements.append(make_body_p(
        "This work has not been submitted previously in part or in its entirety to this or any other university or "
        "institution for the award of any degree or diploma. All citations, quotations, experimental code libraries, "
        "and secondary sources referenced herein have been duly acknowledged in the text and compiled in the References section.",
        space_after=480
    ))
    elements.append(make_body_p("Signature: ____________________________________", space_after=120))
    elements.append(make_body_p("Thabang Nhlokoma Buthelezi", bold=True, space_after=240))
    elements.append(make_body_p("Date: _________________________________________", space_after=120))
    elements.append(make_page_break_p())

    # 2. DEDICATION
    elements.append(make_centered_heading1("DEDICATION"))
    elements.append(make_body_p("", space_after=120))
    elements.append(make_body_p(
        "This mini-dissertation is dedicated to my family, whose patience, sacrifices, and prayers "
        "have supported me throughout my studies at the University of Zululand."
    ))
    elements.append(make_page_break_p())

    # 3. ACKNOWLEDGEMENT
    elements.append(make_centered_heading1("ACKNOWLEDGEMENT"))
    elements.append(make_body_p("", space_after=120))
    elements.append(make_body_p(
        "I wish to express my sincere gratitude to my supervisor, Prof. Pragasen Mudali, and co-supervisor, "
        "Mr. Skhumbuzo Zwane, for their guidance, technical feedback, and encouragement throughout the design, "
        "implementation, and writing of this research project."
    ))
    elements.append(make_body_p(
        "I also thank the academic and technical staff of the Department of Computer Science in the Faculty of "
        "Science, Agriculture and Engineering at the University of Zululand for providing the laboratory facilities "
        "and learning environment that made this work possible. Finally, I thank my family and fellow Honours "
        "students for their support throughout the academic year."
    ))
    elements.append(make_page_break_p())

    # 4. TABLE OF CONTENTS (Matches P156 + SDT of Template)
    p_toc_title = make_w_el("p")
    pPr_toc = make_w_el("pPr")
    pPr_toc.append(make_w_el("jc", val="center"))
    pPr_toc.append(make_w_el("spacing", before="120", after="240"))
    p_toc_title.append(pPr_toc)
    r_toc = make_w_el("r")
    rPr_toc = make_w_el("rPr")
    rPr_toc.append(make_w_el("b"))
    rPr_toc.append(make_w_el("u", val="single"))
    rPr_toc.append(make_w_el("sz", val="28"))
    rPr_toc.append(make_w_el("szCs", val="28"))
    r_toc.append(rPr_toc)
    t_toc = make_w_el("t")
    t_toc.text = "TABLE OF CONTENTS"
    r_toc.append(t_toc)
    p_toc_title.append(r_toc)
    elements.append(p_toc_title)

    toc_entries = page_map.get("toc_entries", [])
    elements.append(build_toc_sdt(toc_entries))
    elements.append(make_page_break_p())

    # 5. LIST OF FIGURES
    elements.append(make_centered_heading1("LIST OF FIGURES"))
    elements.append(make_body_p("", space_after=120))
    fig_pages = page_map.get("figures", {})
    for key, desc in FIGURES_LIST:
        pg = fig_pages.get(key, "15")
        elements.append(make_tabbed_entry_p(desc, pg, style_id="TOC1", bold=False))
    elements.append(make_page_break_p())

    # 6. LIST OF TABLES
    elements.append(make_centered_heading1("LIST OF TABLES"))
    elements.append(make_body_p("", space_after=120))
    tbl_pages = page_map.get("tables", {})
    for key, desc in TABLES_LIST:
        pg = tbl_pages.get(key, "10")
        elements.append(make_tabbed_entry_p(desc, pg, style_id="TOC1", bold=False))
    elements.append(make_page_break_p())

    # 7. LIST OF ABBREVIATIONS
    elements.append(make_centered_heading1("LIST OF ABBREVIATIONS"))
    elements.append(make_body_p("", space_after=120))
    for abbr, full_name in ABBREVIATIONS_LIST:
        p_ab = make_w_el("p")
        pPr_ab = make_w_el("pPr")
        pPr_ab.append(make_w_el("pStyle", val="BodyText"))
        tabs_ab = make_w_el("tabs")
        tabs_ab.append(make_w_el("tab", val="left", pos="1800"))
        pPr_ab.append(tabs_ab)
        pPr_ab.append(make_w_el("spacing", after="80", line="276", lineRule="auto"))
        p_ab.append(pPr_ab)

        r_k = make_w_el("r")
        rPr_k = make_w_el("rPr")
        rPr_k.append(make_w_el("rFonts", ascii="Arial", hAnsi="Arial", cs="Arial"))
        rPr_k.append(make_w_el("b"))
        rPr_k.append(make_w_el("sz", val="24"))
        r_k.append(rPr_k)
        t_k = make_w_el("t")
        t_k.text = abbr
        r_k.append(t_k)
        p_ab.append(r_k)

        r_tb = make_w_el("r")
        r_tb.append(make_w_el("tab"))
        p_ab.append(r_tb)

        r_v = make_w_el("r")
        rPr_v = make_w_el("rPr")
        rPr_v.append(make_w_el("rFonts", ascii="Arial", hAnsi="Arial", cs="Arial"))
        rPr_v.append(make_w_el("sz", val="24"))
        r_v.append(rPr_v)
        t_v = make_w_el("t")
        t_v.text = full_name
        r_v.append(t_v)
        p_ab.append(r_v)
        elements.append(p_ab)
    elements.append(make_page_break_p())

    # 8. ABSTRACT
    elements.append(make_centered_heading1("ABSTRACT"))
    elements.append(make_body_p("", space_after=60))
    abstract_paragraphs = [
        "The Controller Placement Problem (CPP) in Software Defined Networking (SDN) requires selecting k switch locations to host control-plane instances so that switch-to-controller propagation latency is minimized while maintaining control-plane reachability under link failures. Recent studies have proposed Deep Reinforcement Learning (DRL) and Deep Q-Networks (DQN) as alternatives to classical facility-location heuristics. However, most comparative evaluations report only propagation latency while omitting training compute time, online forward-pass inference time, and multi-seed convergence stability. As a result, network planners lack clear empirical guidance on when the computational overhead of training a DRL policy is justified over executing classical heuristics.",
        "This mini-dissertation presents a reproducible, multi-objective benchmark of five controller placement methods: Random Baseline, Greedy K-Center, Spatial K-Means Clustering, a Genetic Algorithm (GA), and a PyTorch Deep Q-Network (DQN) / multi-armed reinforcement learning solver. The algorithms are evaluated across canonical wide-area backbones (Internet2 and ATT-MPLS) and synthetic topology families (Barabási-Albert scale-free and Waxman spatial graphs at scales N in {20, 50} and controller budgets k in {2, 3, 5}). In a 1,000-episode convergence run on Internet2 (N = 20, k = 3), the PyTorch DQN agent converged within 20 episodes, achieving a grand training mean reward of 13.055 +/- 0.589 and a final 10-episode average reward of 13.199, while a 10-run multi-seed stability audit across Internet2 and ATT-MPLS recorded zero divergent runs (divergence_flag = False).",
        "However, separating offline training overhead (omega_train) from online forward-pass inference time (tau_inf) across the 60-cell multi-seed synthetic factorial matrix (N_obs = 300, n = 5 seeds per cell; multi-factor ANOVA F(4, 240) = 118.90, p < 0.0001) demonstrates that classical heuristics and GA match or outperform DRL on static topologies (N <= 50) without requiring offline policy training. While a trained DQN executes a single greedy forward pass in tau_inf = 0.021-0.029 ms, training the network requires omega_train = 21.26 s (0.0213 s/episode), whereas Greedy K-Center (0.026-0.207 ms), K-Means (3.19-8.14 ms), and GA (12.88-75.87 ms) compute placements directly in a single run. Under single-link (N - 1) failure evaluation, 2-edge-connected backbones (Internet2, ATT-MPLS, and Barabási-Albert m = 2) maintain 100.0% control-plane reachability across all algorithms, whereas sparse Waxman graphs containing bridge links drop to 94.47%-98.79%. Five-way emulation on Internet2 (N = 20, k = 3) confirms that GA (2.718 ms mean RTT) and K-Means (2.852 ms mean RTT; 5.764 ms worst-case RTT) outperform Greedy K-Center (2.934 ms), Bandit RL / DQN (3.056 ms), and Random (3.374 ms). Within the tested static WAN scope (N <= 50), classical heuristics and GA provide the best multi-objective trade-off, while DRL is framed as a candidate hypothesis for future evaluation under online topological churn.",
    ]
    for ap in abstract_paragraphs:
        p_ap = make_body_p(ap, space_after=100)
        p_ap.find(f"{{{W_NS}}}pPr").find(f"{{{W_NS}}}spacing").set(f"{{{W_NS}}}line", "300")
        elements.append(p_ap)
    p_kw = make_body_p(
        "Keywords: Software Defined Networking, Controller Placement Problem, Deep Reinforcement Learning, Multi-Objective Optimization, Pareto Efficiency, Mininet Emulation.",
        bold=True, space_after=60
    )
    p_kw.find(f"{{{W_NS}}}pPr").find(f"{{{W_NS}}}spacing").set(f"{{{W_NS}}}line", "300")
    elements.append(p_kw)

    # End Section 1 with sect1_pr inside a paragraph (so CHAPTER ONE starts on Arabic Page 1!)
    p_sect1 = make_w_el("p")
    pPr_s1 = make_w_el("pPr")
    pPr_s1.append(deepcopy(sect1_pr))
    p_sect1.append(pPr_s1)
    elements.append(p_sect1)

    return elements


def format_body_chapters(doc, sect2_pr):
    """
    Format all body headings, subheadings, tables, and chapter page breaks in Section 2.
    Also returns the list of (level, heading_text) discovered in Section 2 for the TOC.
    """
    body = doc.element.body
    discovered_headings = []

    chapter_markers = {
        "CHAPTER ONE",
        "CHAPTER TWO",
        "CHAPTER THREE",
        "CHAPTER FOUR",
        "CHAPTER FIVE",
        "REFERENCES",
        "APPENDIX",
    }

    in_references = False
    in_appendix = False

    def set_pPr_layout(p, align="both", line="360", before="0", after="160", left="0", hanging="0", keep_next=False, page_break_before=False):
        pPr = p.find(f"{{{W_NS}}}pPr")
        if pPr is None:
            pPr = make_w_el("pPr")
            p.insert(0, pPr)
        for tag_to_clear in ("jc", "ind", "spacing", "keepNext", "pageBreakBefore"):
            old_el = pPr.find(f"{{{W_NS}}}{tag_to_clear}")
            if old_el is not None:
                pPr.remove(old_el)
        if page_break_before:
            pPr.append(make_w_el("pageBreakBefore"))
        if keep_next:
            pPr.append(make_w_el("keepNext"))
        pPr.append(make_w_el("spacing", before=str(before), after=str(after), line=str(line), lineRule="auto"))
        if hanging != "0":
            pPr.append(make_w_el("ind", left=str(left), right="0", hanging=str(hanging)))
        else:
            pPr.append(make_w_el("ind", left=str(left), right="0", firstLine="0"))
        pPr.append(make_w_el("jc", val=align))

    for p in list(body.xpath("./w:p")):
        txt = "".join(p.xpath(".//w:t/text()")).strip()
        pStyle_vals = p.xpath("./w:pPr/w:pStyle/@w:val")
        pStyle = pStyle_vals[0] if pStyle_vals else ""
        has_drawing = len(p.xpath(".//*[local-name()='drawing']")) > 0

        if txt == "REFERENCES":
            in_references = True
            in_appendix = False
        elif txt == "APPENDIX":
            in_references = False
            in_appendix = True

        if pStyle == "Heading1":
            pb = (txt in chapter_markers and txt != "CHAPTER ONE")
            set_pPr_layout(p, align="center", line="240", before="240", after="180", keep_next=True, page_break_before=pb)
            for r in p.xpath("./w:r"):
                rPr = r.find(f"{{{W_NS}}}rPr")
                if rPr is None:
                    rPr = make_w_el("rPr")
                    r.insert(0, rPr)
                rPr.append(make_w_el("rFonts", ascii="Arial", hAnsi="Arial", cs="Arial"))
                rPr.append(make_w_el("b"))
                rPr.append(make_w_el("bCs"))
                rPr.append(make_w_el("color", val="000000"))
                rPr.append(make_w_el("sz", val="28"))
                rPr.append(make_w_el("szCs", val="28"))
            if txt:
                discovered_headings.append((1, txt))

        elif pStyle == "Heading2":
            set_pPr_layout(p, align="left", line="240", before="240", after="120", keep_next=True)
            for r in p.xpath("./w:r"):
                rPr = r.find(f"{{{W_NS}}}rPr")
                if rPr is None:
                    rPr = make_w_el("rPr")
                    r.insert(0, rPr)
                rPr.append(make_w_el("rFonts", ascii="Arial", hAnsi="Arial", cs="Arial"))
                rPr.append(make_w_el("b"))
                rPr.append(make_w_el("bCs"))
                rPr.append(make_w_el("color", val="000000"))
                rPr.append(make_w_el("sz", val="24"))
                rPr.append(make_w_el("szCs", val="24"))
            if txt:
                discovered_headings.append((2, txt))

        elif pStyle == "Heading3":
            set_pPr_layout(p, align="left", line="240", before="180", after="100", keep_next=True)
            for r in p.xpath("./w:r"):
                rPr = r.find(f"{{{W_NS}}}rPr")
                if rPr is None:
                    rPr = make_w_el("rPr")
                    r.insert(0, rPr)
                rPr.append(make_w_el("rFonts", ascii="Arial", hAnsi="Arial", cs="Arial"))
                rPr.append(make_w_el("b"))
                rPr.append(make_w_el("bCs"))
                rPr.append(make_w_el("color", val="000000"))
                rPr.append(make_w_el("sz", val="24"))
                rPr.append(make_w_el("szCs", val="24"))

        elif has_drawing:
            set_pPr_layout(p, align="center", line="240", before="180", after="60", keep_next=True)

        elif txt.startswith("Figure ") and ":" in txt[:15]:
            set_pPr_layout(p, align="center", line="240", before="60", after="200", keep_next=False)
            for r in p.xpath("./w:r"):
                rPr = r.find(f"{{{W_NS}}}rPr")
                if rPr is None:
                    rPr = make_w_el("rPr")
                    r.insert(0, rPr)
                rPr.append(make_w_el("sz", val="20"))
                rPr.append(make_w_el("szCs", val="20"))

        elif txt.startswith("Table ") and ":" in txt[:15]:
            set_pPr_layout(p, align="left", line="240", before="200", after="80", keep_next=True)
            for r in p.xpath("./w:r"):
                rPr = r.find(f"{{{W_NS}}}rPr")
                if rPr is None:
                    rPr = make_w_el("rPr")
                    r.insert(0, rPr)
                rPr.append(make_w_el("sz", val="21"))
                rPr.append(make_w_el("szCs", val="21"))

        elif pStyle == "SourceCode" or (in_appendix and pStyle not in ("BodyText", "FirstParagraph", "Normal")):
            set_pPr_layout(p, align="left", line="240", before="0", after="20")

        elif in_references and txt:
            # APA 7th / Harvard hanging indent (0.5 inch = 720 twips), single-spaced within entry, 8pt after
            set_pPr_layout(p, align="both", line="240", before="0", after="160", left="720", hanging="720")

        elif pStyle in ("BodyText", "FirstParagraph", "Normal", "Compact"):
            # UNIZULU standard: 1.5 line spacing (360), justified
            set_pPr_layout(p, align="both", line="360", before="0", after="160")

    # Set compact 8.5pt font, cantSplit rows, and repeat header row inside data tables
    for tbl in body.xpath("./w:tbl"):
        tstyle = tbl.xpath("./w:tblPr/w:tblStyle/@w:val")
        if tstyle and tstyle[0] == "FigureTable":
            continue
        for r_idx, tr in enumerate(tbl.xpath("./w:tr")):
            trPr = tr.find(f"{{{W_NS}}}trPr")
            if trPr is None:
                trPr = make_w_el("trPr")
                tr.insert(0, trPr)
            if trPr.find(f"{{{W_NS}}}cantSplit") is None:
                trPr.append(make_w_el("cantSplit"))
            if r_idx == 0 and trPr.find(f"{{{W_NS}}}tblHeader") is None:
                trPr.append(make_w_el("tblHeader", val="true"))
        for r in tbl.xpath(".//w:r"):
            rPr = r.find(f"{{{W_NS}}}rPr")
            if rPr is None:
                rPr = make_w_el("rPr")
                r.insert(0, rPr)
            rPr.append(make_w_el("sz", val="17"))
            rPr.append(make_w_el("szCs", val="17"))

    # Replace final body <w:sectPr> with sect2_pr (Arabic page numbering starting at 1)
    old_sectPr = body.find(f"{{{W_NS}}}sectPr")
    if old_sectPr is not None:
        body.remove(old_sectPr)
    body.append(deepcopy(sect2_pr))

    return discovered_headings


def copy_template_headers_footers(docx_path: Path, tpl_path: Path):
    """
    Ensure footer1.xml (blank cover footer), footer2.xml (PAGE number footer),
    and Pandoc's Table/Compact styles are packaged inside docx_path.
    """
    with zipfile.ZipFile(tpl_path, "r") as z_tpl:
        ftr1_bytes = z_tpl.read("word/footer1.xml")
        ftr2_bytes = z_tpl.read("word/footer2.xml")
        hdr1_bytes = z_tpl.read("word/header1.xml")
        hdr2_bytes = z_tpl.read("word/header2.xml")

    pandoc_ref_bytes = subprocess.check_output(["pandoc", "--print-default-data-file", "reference.docx"])
    with zipfile.ZipFile(io.BytesIO(pandoc_ref_bytes), "r") as z_pdoc:
        pdoc_styles_root = etree.fromstring(z_pdoc.read("word/styles.xml"))

    tmp_zip = docx_path.with_suffix(".tmp.docx")
    with zipfile.ZipFile(docx_path, "r") as zin, zipfile.ZipFile(tmp_zip, "w", zipfile.ZIP_DEFLATED) as zout:
        existing_names = set(zin.namelist())
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/styles.xml":
                styles_root = etree.fromstring(data)
                existing_sids = {
                    el.get(f"{{{W_NS}}}styleId")
                    for el in styles_root.xpath(".//*[local-name()='style']")
                }
                for el in pdoc_styles_root.xpath(".//*[local-name()='style']"):
                    sid = el.get(f"{{{W_NS}}}styleId")
                    if sid in ("Table", "Compact", "ImageCaption", "CaptionedFigure", "Figure"):
                        if sid not in existing_sids:
                            styles_root.append(deepcopy(el))
                data = etree.tostring(styles_root, xml_declaration=True, encoding="UTF-8", standalone="yes")
            elif item.filename == "word/_rels/document.xml.rels":
                rels_root = etree.fromstring(data)
                existing_ids = {el.get("Id") for el in rels_root}
                new_rels = [
                    ("rId_hdr1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/header", "header1.xml"),
                    ("rId_hdr2", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/header", "header2.xml"),
                    ("rId_ftr1", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer", "footer1.xml"),
                    ("rId_ftr2", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer", "footer2.xml"),
                ]
                for rid, rtype, target in new_rels:
                    if rid not in existing_ids:
                        rel_el = etree.Element(f"{{{REL_NS}}}Relationship")
                        rel_el.set("Id", rid)
                        rel_el.set("Type", rtype)
                        rel_el.set("Target", target)
                        rels_root.append(rel_el)
                data = etree.tostring(rels_root, xml_declaration=True, encoding="UTF-8", standalone="yes")
            elif item.filename == "[Content_Types].xml":
                ct_root = etree.fromstring(data)
                existing_parts = {el.get("PartName") for el in ct_root}
                part_specs = [
                    ("/word/header1.xml", "application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"),
                    ("/word/header2.xml", "application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"),
                    ("/word/footer1.xml", "application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"),
                    ("/word/footer2.xml", "application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"),
                ]
                for pname, ctype in part_specs:
                    if pname not in existing_parts:
                        ov = etree.Element("{http://schemas.openxmlformats.org/package/2006/content-types}Override")
                        ov.set("PartName", pname)
                        ov.set("ContentType", ctype)
                        ct_root.append(ov)
                data = etree.tostring(ct_root, xml_declaration=True, encoding="UTF-8", standalone="yes")
            zout.writestr(item, data)

        if "word/header1.xml" not in existing_names:
            zout.writestr("word/header1.xml", hdr1_bytes)
        if "word/header2.xml" not in existing_names:
            zout.writestr("word/header2.xml", hdr2_bytes)
        if "word/footer1.xml" not in existing_names:
            zout.writestr("word/footer1.xml", ftr1_bytes)
        if "word/footer2.xml" not in existing_names:
            zout.writestr("word/footer2.xml", ftr2_bytes)

    shutil.move(tmp_zip, docx_path)


def extract_exact_page_numbers(pdf_path: Path, body_headings):
    """
    Parse the rendered PDF page-by-page using pdftotext to determine the exact
    Roman numeral pages for Front Matter and Arabic page numbers for all Chapters,
    Sections, Figures, and Tables.
    """
    txt_out = subprocess.check_output(["pdftotext", str(pdf_path), "-"], text=True)
    raw_pages = txt_out.split("\x0c")
    if raw_pages and not raw_pages[-1].strip():
        raw_pages.pop()

    # Find which physical 0-based page index corresponds to CHAPTER ONE (Arabic Page 1)
    ch1_idx = None
    for idx, ptxt in enumerate(raw_pages):
        lines = [ln.strip() for ln in ptxt.splitlines() if ln.strip()]
        if lines and lines[0] == "CHAPTER ONE":
            ch1_idx = idx
            break
    if ch1_idx is None:
        ch1_idx = 11

    # Front matter starts on physical page index 2 (after Cover Page 1 and Cover Page 2)
    fm_targets = [
        "DECLARATION",
        "DEDICATION",
        "ACKNOWLEDGEMENT",
        "LIST OF FIGURES",
        "LIST OF TABLES",
        "LIST OF ABBREVIATIONS",
        "ABSTRACT",
    ]
    fm_pages = {}
    for fm in fm_targets:
        for idx in range(2, ch1_idx):
            lines = [ln.strip() for ln in raw_pages[idx].splitlines() if ln.strip()]
            if lines and lines[0] == fm:
                roman_num = int_to_roman(idx - 1)  # idx=2 -> i (1)
                fm_pages[fm] = roman_num
                break

    toc_entries = []
    for fm in fm_targets:
        toc_entries.append((1, fm, fm_pages.get(fm, "i")))

    # Find Arabic page numbers for every body heading
    search_start = ch1_idx
    for level, h_text in body_headings:
        found_arabic = None
        norm_h = re.sub(r"\s+", " ", h_text).strip()
        prefix_key = norm_h[:28]
        for idx in range(search_start, len(raw_pages)):
            norm_page = re.sub(r"\s+", " ", raw_pages[idx])
            if norm_h in norm_page or prefix_key in norm_page:
                found_arabic = str(idx - ch1_idx + 1)
                search_start = idx
                break
        if found_arabic is None:
            # Fallback scan across all body pages
            for idx in range(ch1_idx, len(raw_pages)):
                norm_page = re.sub(r"\s+", " ", raw_pages[idx])
                if prefix_key in norm_page:
                    found_arabic = str(idx - ch1_idx + 1)
                    break
        toc_entries.append((level, h_text, found_arabic or "1"))

    # Find Arabic page numbers for every Figure
    fig_pages = {}
    for key, _ in FIGURES_LIST:
        for idx in range(ch1_idx, len(raw_pages)):
            norm_page = re.sub(r"\s+", " ", raw_pages[idx])
            if key in norm_page:
                fig_pages[key] = str(idx - ch1_idx + 1)
                break

    # Find Arabic page numbers for every Table
    tbl_pages = {}
    for key, _ in TABLES_LIST:
        for idx in range(ch1_idx, len(raw_pages)):
            norm_page = re.sub(r"\s+", " ", raw_pages[idx])
            if key in norm_page:
                tbl_pages[key] = str(idx - ch1_idx + 1)
                break

    return {
        "toc_entries": toc_entries,
        "figures": fig_pages,
        "tables": tbl_pages,
    }


def make_section_prs():
    """Create the 3 section property (<w:sectPr>) elements matching the template."""
    def base_sect_pr():
        sp = make_w_el("sectPr")
        sp.append(make_w_el("pgSz", w="11906", h="16838"))
        sp.append(make_w_el("pgMar", top="1440", right="1440", bottom="1440", left="1440", header="720", footer="720", gutter="0"))
        return sp

    # Section 0: Cover Pages (unnumbered, blank footer1)
    s0 = base_sect_pr()
    ftr_ref0 = make_w_el("footerReference", type="default")
    ftr_ref0.set(f"{{{R_NS}}}id", "rId_ftr1")
    s0.insert(0, ftr_ref0)

    # Section 1: Front Matter (Roman numerals i, ii, iii..., footer2)
    s1 = base_sect_pr()
    hdr_ref1 = make_w_el("headerReference", type="default")
    hdr_ref1.set(f"{{{R_NS}}}id", "rId_hdr1")
    ftr_ref1 = make_w_el("footerReference", type="default")
    ftr_ref1.set(f"{{{R_NS}}}id", "rId_ftr2")
    s1.insert(0, ftr_ref1)
    s1.insert(0, hdr_ref1)
    s1.append(make_w_el("pgNumType", fmt="lowerRoman", start="1"))

    # Section 2: Main Body Chapters (Arabic numerals 1, 2, 3..., footer2)
    s2 = base_sect_pr()
    hdr_ref2 = make_w_el("headerReference", type="default")
    hdr_ref2.set(f"{{{R_NS}}}id", "rId_hdr2")
    ftr_ref2 = make_w_el("footerReference", type="default")
    ftr_ref2.set(f"{{{R_NS}}}id", "rId_ftr2")
    s2.insert(0, ftr_ref2)
    s2.insert(0, hdr_ref2)
    s2.append(make_w_el("pgNumType", start="1"))

    return s0, s1, s2


def compile_dissertation():
    print("=" * 80)
    print("COMPILING BSC HONOURS MINI-DISSERTATION: THABANG NHLOKOMA BUTHELEZI")
    print("=" * 80)

    # 1. Concatenate all modular markdown files into Master Markdown
    print(f"\n[1/5] Concatenating {len(CHAPTERS)} modular chapter files...")
    full_content = []
    body_content = []
    total_words = 0
    total_lines = 0

    for ch_name in CHAPTERS:
        ch_path = DISSERTATION_DIR / ch_name
        if not ch_path.exists():
            print(f"  [ERROR] Missing chapter file: {ch_path}")
            sys.exit(1)
        content = ch_path.read_text(encoding="utf-8")
        lines = content.count("\n")
        words = len(content.split())
        total_lines += lines
        total_words += words
        print(f"  + Added {ch_name:<38} ({lines:>4} lines, {words:>5} words)")
        full_content.append(content)
        full_content.append("\n\n")
        if ch_name in BODY_CHAPTERS:
            body_content.append(content)
            body_content.append("\n\n")

    MASTER_MD.write_text("".join(full_content), encoding="utf-8")
    body_md_path = DISSERTATION_DIR / ".body_staging.md"
    body_md_path.write_text("".join(body_content), encoding="utf-8")
    print(f"\n[OK] Wrote Master Markdown: {MASTER_MD}")
    print(f"     Total Lines: {total_lines:,} | Total Words: {total_words:,}")

    # 2. Compile body chapters via Pandoc using the official template for styles
    print("\n[2/5] Compiling body chapters with Pandoc...")
    base_body_docx = DISSERTATION_DIR / ".body_staging.docx"
    pandoc_cmd = [
        "pandoc",
        str(body_md_path),
        f"--reference-doc={TEMPLATE_DOCX}",
        f"--resource-path={DISSERTATION_DIR}:{PROJECT_ROOT}",
        "-o",
        str(base_body_docx),
    ]
    subprocess.run(pandoc_cmd, check=True, capture_output=True, text=True)

    # Extract University of Zululand logo from Template
    with zipfile.ZipFile(TEMPLATE_DOCX, "r") as z_tpl:
        logo_bytes = z_tpl.read("word/media/image1.jpeg")

    s0_pr, s1_pr, s2_pr = make_section_prs()

    # 3. Pass 1: Build DOCX with Cover Pages, University Logo, Front Matter, and Body to compute exact page numbers
    print("\n[3/5] Pass 1: Injecting Template Cover Pages (University of Zululand Logo) & Front Matter...")
    doc_p1 = docx.Document(str(base_body_docx))
    body_headings = format_body_chapters(doc_p1, s2_pr)

    initial_toc = [
        (1, "DECLARATION", "i"),
        (1, "DEDICATION", "ii"),
        (1, "ACKNOWLEDGEMENT", "iii"),
        (1, "LIST OF FIGURES", "vi"),
        (1, "LIST OF TABLES", "vii"),
        (1, "LIST OF ABBREVIATIONS", "viii"),
        (1, "ABSTRACT", "ix"),
    ] + [(lvl, h, "1") for lvl, h in body_headings]

    fm_elements_p1 = build_cover_and_front_matter(
        doc_p1, logo_bytes, s0_pr, s1_pr, {"toc_entries": initial_toc, "figures": {}, "tables": {}}
    )
    for idx, el in enumerate(fm_elements_p1):
        doc_p1.element.body.insert(idx, el)

    doc_p1.save(str(OUTPUT_DOCX))
    copy_template_headers_footers(OUTPUT_DOCX, TEMPLATE_DOCX)

    # Export Pass 1 PDF to measure exact page numbers
    lo_cmd = [
        "libreoffice",
        "--headless",
        "-env:UserInstallation=file:///tmp/lo_profile_dissertation",
        "--convert-to",
        "pdf",
        "--outdir",
        str(DISSERTATION_DIR),
        str(OUTPUT_DOCX),
    ]
    subprocess.run(lo_cmd, check=True, capture_output=True, text=True)
    exact_page_map = extract_exact_page_numbers(OUTPUT_PDF, body_headings)

    # 4. Pass 2: Rebuild DOCX with exact verified page numbers in TOC, List of Figures, and List of Tables
    print("\n[4/5] Pass 2: Populating exact verified page numbers into Table of Contents, List of Figures & Tables...")
    doc_p2 = docx.Document(str(base_body_docx))
    format_body_chapters(doc_p2, s2_pr)
    fm_elements_p2 = build_cover_and_front_matter(
        doc_p2, logo_bytes, s0_pr, s1_pr, exact_page_map
    )
    for idx, el in enumerate(fm_elements_p2):
        doc_p2.element.body.insert(idx, el)

    doc_p2.save(str(OUTPUT_DOCX))
    copy_template_headers_footers(OUTPUT_DOCX, TEMPLATE_DOCX)

    # Cleanup staging files
    body_md_path.unlink(missing_ok=True)
    base_body_docx.unlink(missing_ok=True)

    # 5. Export Final PDF
    print("\n[5/5] Exporting final Adobe PDF (.pdf)...")
    subprocess.run(lo_cmd, check=True, capture_output=True, text=True)

    docx_size_kb = OUTPUT_DOCX.stat().st_size / 1024
    pdf_size_kb = OUTPUT_PDF.stat().st_size / 1024
    print(f"\n[SUCCESS] Successfully compiled Mini-Dissertation (.docx and .pdf)!")
    print(f"  Output DOCX: {OUTPUT_DOCX} ({docx_size_kb:.1f} KB)")
    print(f"  Output PDF:  {OUTPUT_PDF} ({pdf_size_kb:.1f} KB)")
    print("=" * 80)


if __name__ == "__main__":
    compile_dissertation()
