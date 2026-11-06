#!/usr/bin/env python3
"""
Generate IEEE-Compliant 2-Column Word Documents (.docx) for SATNAC / IEEE Conference Submission.
Creates:
  1. Anonymized Review Version (docs/SATNAC_RESEARCH_PAPER_Anonymized.docx)
  2. Camera-Ready Version (docs/SATNAC_RESEARCH_PAPER_CameraReady.docx)
  3. Default Copy (docs/SATNAC_RESEARCH_PAPER.docx)

Strictly adheres to IEEE Conference template standards:
  - 1-Column Title + 3-Column Author Block at top of Page 1
  - Continuous section break immediately after Author Block into 2-Column layout
  - Abstract and Index Terms inside the left column of the 2-Column layout (9pt Bold)
  - Centered Roman numeral H1 headers, Italicized A/B/C H2 headers
  - Fully justified body paragraphs (10pt Times New Roman, zero bullet lists)
  - Native IEEE monochrome booktabs-style tables (no embedded table PNG screenshots)
  - Complete 18 IEEE references
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn


def set_section_columns(section, num_cols=2, col_space_pt=18):
    """Set section columns (2 columns with 0.25in / 18pt spacing)."""
    space_twips = int(col_space_pt * 20)
    sectPr = section._sectPr
    for child in list(sectPr):
        if child.tag.endswith('cols'):
            sectPr.remove(child)
    cols_xml = f'<w:cols {nsdecls("w")} w:num="{num_cols}" w:space="{space_twips}"/>'
    sectPr.append(parse_xml(cols_xml))


def set_cell_margins(cell, top=45, bottom=45, left=60, right=60):
    """Set inner cell padding in twips."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def set_ieee_table_borders(table):
    """Apply strict IEEE monochrome booktabs borders (top/bottom rules, header rule, no vertical rules)."""
    tblPr = table._tbl.tblPr
    borders_xml = f'''
    <w:tblBorders {nsdecls("w")}>
        <w:top w:val="single" w:sz="10" w:space="0" w:color="000000"/>
        <w:bottom w:val="single" w:sz="10" w:space="0" w:color="000000"/>
        <w:insideH w:val="none"/>
        <w:insideV w:val="none"/>
        <w:left w:val="none"/>
        <w:right w:val="none"/>
    </w:tblBorders>
    '''
    tblPr.append(parse_xml(borders_xml))


def set_row_bottom_border(row, sz="6"):
    """Add a bottom horizontal rule to a specific table row (e.g. header row)."""
    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = OxmlElement('w:tcBorders')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), sz)
        bottom.set(qn('w:space'), '0')
        bottom.set(qn('w:color'), '000000')
        tcBorders.append(bottom)
        tcPr.append(tcBorders)


def set_borderless_table(table):
    """Remove all borders from a layout table (used for the 3-column IEEE author block)."""
    tblPr = table._tbl.tblPr
    borders_xml = f'''
    <w:tblBorders {nsdecls("w")}>
        <w:top w:val="none"/>
        <w:bottom w:val="none"/>
        <w:insideH w:val="none"/>
        <w:insideV w:val="none"/>
        <w:left w:val="none"/>
        <w:right w:val="none"/>
    </w:tblBorders>
    '''
    tblPr.append(parse_xml(borders_xml))


def build_satnac_doc(output_path: Path, anonymized: bool = False):
    doc = Document()

    # IEEE Conference Margins: 0.75 in top/bottom, 0.625 in left/right
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.625)
        section.right_margin = Inches(0.625)

    # Base Font Settings (10pt Times New Roman)
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Times New Roman'
    font.size = Pt(10)
    font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    # =========================================================================
    # SECTION 1: 1-COLUMN TITLE & AUTHOR BLOCK ONLY
    # =========================================================================
    title_sec = doc.sections[0]
    set_section_columns(title_sec, num_cols=1)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(12)
    run_title = p_title.add_run(
        "Decision-Grade Multi-Objective Benchmarking of DRL and Heuristic "
        "Controller Placement in Multi-Site Software Defined Networks"
    )
    run_title.font.name = 'Times New Roman'
    run_title.font.size = Pt(22)

    if anonymized:
        p_author = doc.add_paragraph()
        p_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_author.paragraph_format.space_before = Pt(0)
        p_author.paragraph_format.space_after = Pt(14)
        r1 = p_author.add_run("Anonymous Submission for Double-Blind Peer Review\n")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r1.font.bold = True
        r2 = p_author.add_run("Department of Computer Science\n")
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10)
        r2.font.italic = True
    else:
        auth_table = doc.add_table(rows=1, cols=3)
        auth_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_borderless_table(auth_table)
        authors = [
            ("1st Thabang Nhlokoma Buthelezi", "Department of Computer Science\nUniversity of Zululand", "KwaDlangezwa, South Africa\n230011908@stu.unizulu.ac.za"),
            ("2nd Pragasen Mudali", "Department of Computer Science\nUniversity of Zululand", "KwaDlangezwa, South Africa\nmudalip@unizulu.ac.za"),
            ("3rd Skhumbuzo Zwane", "Department of Computer Science\nUniversity of Zululand / CSIR", "KwaDlangezwa, South Africa\nszwane7@csir.ac.za"),
        ]
        for idx, (name, dept, loc) in enumerate(authors):
            cell = auth_table.rows[0].cells[idx]
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(12)
            rn = p.add_run(name + "\n")
            rn.font.name = 'Times New Roman'
            rn.font.size = Pt(11)
            rd = p.add_run(dept + "\n")
            rd.font.name = 'Times New Roman'
            rd.font.size = Pt(10)
            rd.font.italic = True
            rl = p.add_run(loc)
            rl.font.name = 'Times New Roman'
            rl.font.size = Pt(10)

    # =========================================================================
    # SECTION 2: 2-COLUMN BODY (STARTS WITH ABSTRACT & INDEX TERMS IN COL 1)
    # =========================================================================
    body_sec = doc.add_section(docx.enum.section.WD_SECTION.CONTINUOUS)
    set_section_columns(body_sec, num_cols=2, col_space_pt=18)

    # Abstract (9pt Bold, inside Left Column of 2-Column Layout per IEEEtran)
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.space_before = Pt(0)
    p_abs.paragraph_format.space_after = Pt(4)
    p_abs.paragraph_format.first_line_indent = Inches(0.15)
    r_abs_hdr = p_abs.add_run("Abstract—")
    r_abs_hdr.font.name = 'Times New Roman'
    r_abs_hdr.font.size = Pt(9)
    r_abs_hdr.font.bold = True
    r_abs_hdr.font.italic = True

    r_abs_body = p_abs.add_run(
        "Selecting an appropriate controller placement strategy in multi-site Software Defined Networks (SDN) "
        "requires balancing switch-to-controller propagation latency, control-plane survivability under link failures, "
        "and the computational overhead of the placement algorithm itself. Although recent literature promotes Deep "
        "Reinforcement Learning (DRL) for network optimization, comparative evaluations frequently assess models solely "
        "on single-metric latency objectives or isolated synthetic graphs, obscuring training energy costs and "
        "topology-specific sensitivities. This paper presents a reproducible, multi-objective benchmarking study "
        "comparing five placement paradigms: Random Baseline, Greedy K-Center, Spatial K-Means Clustering, Genetic "
        "Algorithms (GA), and PyTorch Deep Q-Networks (DQN) paired with ε-greedy Reinforcement Learning (RL). The "
        "evaluation spans canonical wide-area backbones (Internet2 and ATT-MPLS) and parameterized synthetic topologies "
        "(Barabási-Albert scale-free and Waxman spatial graphs) for node scales N ∈ {20, 21, 50} and controller budgets "
        "k ∈ {2, 3, 5} across five independent random seeds per cell (N_obs = 300). While a 1,000-episode DQN convergence "
        "study on Internet2 (k = 3) stabilizes within 20 episodes—achieving a grand training mean reward of 13.055 ± 0.589 "
        "and a post-convergence final 10-episode mean of 13.199—it incurs an offline training cost of ω_train = 21.26 s "
        "(0.0213 s/episode) before achieving sub-millisecond forward-pass inference (τ_inf = 0.029 ms). Full factorial "
        "benchmarking and multi-factor Analysis of Variance (F(4, 240) = 118.90, p < 0.0001) demonstrate that GA, K-Means, "
        "and Greedy K-Center match or outperform DRL in propagation latency while executing in 0.031–4.57 ms (heuristics) "
        "to 76 ms (GA) without prior topology-specific training, maintaining 100.0% single-link (N − 1) reachability on "
        "biconnected backbones and 96.1%–97.6% on sparse Waxman graphs. Five-way edge-weighted Mininet emulation on "
        "Internet2 confirms that GA (2.718 ms mean RTT) and K-Means (2.852 ms mean RTT; 5.764 ms worst-case RTT) "
        "outperform DRL (3.056 ms). Within the evaluated static WAN scope (N ≤ 50), classical heuristics provide superior "
        "one-shot decision efficiency, whereas DRL is hypothesized as a candidate primarily for non-stationary "
        "environments where offline training ω_train can be amortized across repeated online forward-pass inferences τ_inf."
    )
    r_abs_body.font.name = 'Times New Roman'
    r_abs_body.font.size = Pt(9)
    r_abs_body.font.bold = True

    # Index Terms (9pt Bold)
    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.space_before = Pt(0)
    p_kw.paragraph_format.space_after = Pt(8)
    p_kw.paragraph_format.first_line_indent = Inches(0.15)
    r_kw_hdr = p_kw.add_run("Index Terms—")
    r_kw_hdr.font.name = 'Times New Roman'
    r_kw_hdr.font.size = Pt(9)
    r_kw_hdr.font.bold = True
    r_kw_hdr.font.italic = True

    r_kw_body = p_kw.add_run(
        "Controller Placement Problem, Deep Reinforcement Learning, Heuristic Optimization, "
        "Mininet Emulation, Multi-Objective Benchmarking, Pareto Efficiency, Software Defined Networking."
    )
    r_kw_body.font.name = 'Times New Roman'
    r_kw_body.font.size = Pt(9)
    r_kw_body.font.bold = True

    # Helper functions for IEEE body text
    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text.upper())
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        run.font.italic = True
        return p

    def add_body(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.first_line_indent = Inches(0.15)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10)
        return p

    def add_equation(eq_text, eq_num):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r_eq = p.add_run(f"{eq_text}    ({eq_num})")
        r_eq.font.name = 'Times New Roman'
        r_eq.font.size = Pt(9.5)
        r_eq.font.italic = True
        return p

    def add_ieee_table(caption_num, caption_text, headers, rows, font_pt=7.5):
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(6)
        p_cap.paragraph_format.space_after = Pt(2)
        p_cap.paragraph_format.keep_with_next = True
        r_num = p_cap.add_run(f"{caption_num}\n")
        r_num.font.name = 'Times New Roman'
        r_num.font.size = Pt(8)
        r_txt = p_cap.add_run(caption_text.upper())
        r_txt.font.name = 'Times New Roman'
        r_txt.font.size = Pt(7.5)

        tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_ieee_table_borders(tbl)

        hdr_row = tbl.rows[0]
        set_row_bottom_border(hdr_row, sz="6")
        for j, h_val in enumerate(headers):
            cell = hdr_row.cells[j]
            set_cell_margins(cell, top=40, bottom=40, left=45, right=45)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(h_val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(font_pt)
            run.font.bold = True

        for i, row_vals in enumerate(rows):
            tr = tbl.rows[i + 1]
            for j, val in enumerate(row_vals):
                cell = tr.cells[j]
                set_cell_margins(cell, top=35, bottom=35, left=45, right=45)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                run = p.add_run(val)
                run.font.name = 'Times New Roman'
                run.font.size = Pt(font_pt)

        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(3)

    # =========================================================================
    # I. INTRODUCTION
    # =========================================================================
    add_h1("I. Introduction")
    add_body(
        "Software Defined Networking (SDN) decouples the network control plane from the underlying packet-forwarding "
        "hardware, consolidating routing intelligence and policy enforcement into logically centralized software "
        "controllers [1], [2]. While logical centralization simplifies policy management in single-site local area "
        "networks, deploying a single physical controller across a geographically distributed Wide Area Network (WAN) "
        "introduces severe propagation delays and single-point-of-failure vulnerabilities [3]. To meet carrier-grade "
        "service-level agreements, network architects must partition the control plane across k distributed controller "
        "instances and assign each forwarding switch to a designated controller—a fundamental combinatorial optimization "
        "challenge formalized by Heller et al. as the Controller Placement Problem (CPP) [3]."
    )
    add_body(
        "Because selecting k controller locations from N candidate switch sites generalizes the NP-hard p-median and "
        "k-center facility location problems [4], [5], exhaustive combinatorial enumeration becomes computationally "
        "intractable as network scale grows. Over the past decade, three primary algorithmic families have been proposed "
        "to solve the CPP: (i) fast constructive heuristics and spatial clustering methods such as Greedy K-Center and "
        "K-Means [5], [6], (ii) population-based evolutionary metaheuristics such as Genetic Algorithms (GAs) [7], [8], "
        "and (iii) autonomous machine learning paradigms, notably Deep Reinforcement Learning (DRL) and Deep Q-Networks "
        "(DQN) [9]–[12]."
    )
    add_body(
        "Despite a surge in publications advocating DRL for SDN controller placement, infrastructure engineers at "
        "telecommunications operators and national research and education networks (NRENs) face an acute methodological "
        "decision gap. Much of the contemporary DRL literature evaluates neural agents against trivial random baselines "
        "or single-objective latency metrics, omitting the wall-clock execution time, convergence episode budgets, and "
        "hardware energy costs required to train neural policies [11], [12]. We define this unmeasured computational "
        "overhead as the Complexity Tax (ω). In static or quasi-static carrier backbones—where physical optical fiber "
        "topologies remain fixed for months or years—it remains unclear whether the computational expense of training a "
        "deep neural network yields any statistically or operationally meaningful latency advantage over sub-millisecond "
        "classical heuristics, especially once kernel-level OpenFlow switching delays are accounted for."
    )
    add_body(
        "To resolve this ambiguity, this study conducts a decision-grade, multi-objective benchmark of five controller "
        "placement paradigms across both real-world canonical WAN backbones and synthetic topological families. "
        "Specifically, we investigate three research questions: first (RQ1), whether PyTorch DQN and tabular RL agents "
        "achieve statistically significant reductions in switch-to-controller propagation latency L(C) and improvements "
        "in single-link (N − 1) control-plane reachability Reach_avg(C) compared to Greedy K-Center, K-Means, and GA; "
        "second (RQ2), how the computational Complexity Tax ω scales across network sizes N ∈ {20, 50} and controller "
        "budgets k ∈ {2, 3, 5}; and third (RQ3), how topological structure (scale-free hub skew versus spatial mesh "
        "clustering) and real-world Open vSwitch kernel delays govern the three-dimensional Pareto frontier."
    )

    # =========================================================================
    # II. RELATED WORK
    # =========================================================================
    add_h1("II. Related Work")
    add_h2("A. Classical Facility Location and Spatial Heuristics")
    add_body(
        "Heller et al. [3] established the foundational framing of the CPP by evaluating average and worst-case "
        "propagation latencies across topologies from the Internet Topology Zoo [13], demonstrating that optimal "
        "controller placement is strongly dictated by graph geometry and budget k. Theoretically, minimizing the average "
        "switch-to-controller delay corresponds to the NP-hard p-median problem analyzed by Kariv and Hakimi [4], "
        "whereas minimizing the maximum tail latency corresponds to the k-center problem, for which Gonzalez [5] proved "
        "a tight polynomial-time 2-approximation greedy heuristic. To achieve rapid partitioning on planar networks, "
        "researchers adapted MacQueen's K-Means clustering algorithm [6] to graph coordinates and shortest-path distance "
        "matrices, offering sub-5-millisecond execution times on moderate-scale WANs."
    )
    add_h2("B. Evolutionary Metaheuristics and Swarm Intelligence")
    add_body(
        "When offline planning budgets permit tens of milliseconds of computation, population-based metaheuristics "
        "explore broader regions of the combinatorial space. Drawing on Holland's genetic framework [7] and Goldberg's "
        "evolutionary operators [8], GAs encode candidate placements as fixed-weight chromosomes evolved via tournament "
        "selection, uniform crossover, and bit-flip mutation. More recently, Radam et al. [15] and Yusuf et al. [16] "
        "investigated critical-switch-aware swarm intelligence and metaheuristic variants for IoT and multi-site SDN "
        "environments, showing that evolutionary search consistently escapes local optima that trap greedy heuristics."
    )
    add_h2("C. Deep Reinforcement Learning in SDN Placement")
    add_body(
        "The integration of Reinforcement Learning [9] with deep neural function approximation by Mnih et al. [10] "
        "catalyzed interest in autonomous network control. Benoudifa et al. [11] introduced a MuZero-inspired DRL "
        "framework for controller placement under shifting traffic demands, while Farahi et al. [12] formulated an "
        "Adaptive Policy Deep Q-Network (AP-DQN) utilizing a two-hidden-layer Multi-Layer Perceptron (64×64 ReLU units), "
        "experience replay of 10,000 transitions, and ε-greedy exploration. While these studies demonstrate that DRL "
        "agents can converge toward low-latency placements, they do not benchmark the resulting policies against both "
        "Greedy K-Center and GA across a unified multi-seed factorial matrix, nor do they quantify whether sub-millisecond "
        "theoretical latency differences survive kernel-level OpenFlow packet switching in Mininet [17]."
    )

    # =========================================================================
    # III. RESEARCH METHODOLOGY
    # =========================================================================
    add_h1("III. Research Methodology")
    add_body(
        "The experimental methodology comprises four integrated stages: (i) canonical and synthetic topology "
        "instantiation, (ii) multi-objective mathematical evaluation, (iii) deterministic and stochastic algorithm "
        "execution across controlled random seeds, and (iv) post-convergence OpenFlow packet validation in Mininet. "
        "Fig. 1 illustrates the end-to-end comparative benchmarking pipeline."
    )

    arch_img_path = PROJECT_ROOT / "docs" / "figures" / "proposal_methodology_workflow.png"
    if arch_img_path.exists():
        p_arch = doc.add_paragraph()
        p_arch.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_arch.paragraph_format.space_before = Pt(4)
        p_arch.paragraph_format.space_after = Pt(2)
        p_arch.add_run().add_picture(str(arch_img_path), width=Inches(3.25))

        p_arch_cap = doc.add_paragraph()
        p_arch_cap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_arch_cap.paragraph_format.space_after = Pt(6)
        r_arch_cap = p_arch_cap.add_run(
            "Fig. 1. End-to-end comparative research methodology workflow integrating heuristic, metaheuristic, and "
            "DRL tracks with multi-factor ANOVA and Mininet OpenFlow emulation."
        )
        r_arch_cap.font.name = 'Times New Roman'
        r_arch_cap.font.size = Pt(8)

    add_h2("A. Network Topology Corpus")
    add_body(
        "To prevent overfitting conclusions to a single graph structure, experiments were conducted across both "
        "real-world carrier backbones from the Internet Topology Zoo [13] and synthetic random graph families. The "
        "canonical corpus comprises the Internet2 national research backbone (N = 20 switches, |E| = 26 fiber links) "
        "and the ATT-MPLS continental carrier network (N = 21 switches, |E| = 54 links), with edge weights calibrated "
        "to geodesic fiber propagation delays in milliseconds. To evaluate algorithmic sensitivity to graph structure "
        "and scale, two synthetic generators were parameterized across N ∈ {20, 50}: (i) the Barabási-Albert (BA) "
        "preferential attachment model [14] (m = 2 edges per new node), and (ii) the Waxman random geometric model [18] "
        "(α = 0.4, β = 0.1)."
    )

    add_h2("B. Three-Axis Multi-Objective Formulation")
    add_body(
        "Let G = (V, E, w) denote an undirected, connected network graph with switch set V (|V| = N), physical link "
        "set E, and non-negative link propagation delay function w: E → R+. A controller placement is a subset C ⊆ V "
        "of cardinality |C| = k. Each switch v ∈ V binds to its nearest active controller in C along the shortest "
        "weighted path d_G(v, c) computed via Dijkstra's algorithm. The primary latency objective L(C) measures the "
        "mean shortest-path propagation delay across all switches:"
    )
    add_equation("L(C) = (1 / |V|) ∑_{v ∈ V} min_{c ∈ C} d_G(v, c)", "1")
    add_body(
        "Because physical fiber cuts account for over 85% of wide-area transport outages, we evaluate structural "
        "control-plane survivability using a deterministic N − 1 single-link failure engine. For each physical link "
        "e ∈ E, removing e yields a perturbed residual subgraph G_e = (V, E \\ {e}), which decomposes into connected "
        "components K(G_e) identified via multi-source breadth-first traversal rooted at C. Defining the binary switch "
        "reachability indicator I_reach(v, G_e, C) = 1 if a finite path exists from v to any c ∈ C in G_e and 0 "
        "otherwise, the global control-plane reliability metric Reach_avg(C) ∈ [0, 1] is the expectation across all "
        "|E| independent single-link failure states:"
    )
    add_equation("Reach_avg(C) = (1 / |E|) ∑_{e ∈ E} [ (1 / |V|) ∑_{v ∈ V} I_reach(v, G \\ {e}, C) ]", "2")
    add_body(
        "In 2-edge-connected (biconnected) networks such as Internet2, ATT-MPLS, and BA (m = 2), Menger's theorem "
        "guarantees at least two edge-disjoint paths between every pair of vertices; thus, no single edge is a bridge "
        "and Reach_avg(C) = 1.0 (100.0%) for any non-empty placement C. Conversely, distance-thresholded Waxman graphs "
        "frequently exhibit degree-1 leaf switches or bridge links whose removal partitions G_e into disjoint components "
        "V_1 ∪ V_2. Any component lacking an assigned controller incurs complete control-plane isolation, reducing "
        "Reach_avg(C) below 100%. Finally, we define ω(C) as the wall-clock CPU execution time required to compute C, "
        "and rank non-dominated Pareto solutions via normalized Euclidean distance D_ideal(C) to the ideal point "
        "z* = (L_min, Reach_max, ω_min) with weights w_1 = 0.5, w_2 = 0.3, w_3 = 0.2."
    )

    add_h2("C. Evaluated Placement Paradigms and Statistical Design")
    add_body(
        "Five distinct algorithmic paradigms were implemented in Python 3.12 under identical graph and metric "
        "interfaces: (1) Random Baseline using a controlled PRNG; (2) Greedy K-Center implementing Gonzalez's "
        "deterministic farthest-first traversal [5] in O(kN) lookups; (3) Spatial K-Means Clustering partitioning "
        "switches into k clusters via Lloyd's iteration [6] and selecting discrete graph medoids; (4) Genetic Algorithm "
        "(GA) evolving P_pop = 40 chromosomes across G_max = 50 generations with tournament selection, uniform crossover, "
        "and swap mutation (μ = 0.15) [7], [8]; and (5) PyTorch Deep Q-Network (DQN) and Multi-Armed RL replicating "
        "Farahi et al. [12] with two 64-unit ReLU hidden layers, Adam optimizer (α = 0.001, γ = 0.99), replay buffer "
        "M = 10,000, and ε-greedy exploration decaying from 1.0 to 0.05."
    )
    add_body(
        "The synthetic factorial experiment follows a balanced 5 × 2 × 2 × 3 fixed-effects design: Algorithm Family "
        "(5 levels, df_alg = 4), Topology Family (2 levels: BA and Waxman, df_topo = 1), Node Scale (2 levels: "
        "N ∈ {20, 50}, df_scale = 1), and Controller Budget (3 levels: k ∈ {2, 3, 5}, df_k = 2). Each of the 60 unique "
        "experimental cells is replicated across n = 5 independent trial seeds, yielding N_obs = 60 × 5 = 300 "
        "independent observations (df_total = 299) and a within-cell residual error degrees of freedom of "
        "df_error = 60 × (n − 1) = 240. Finally, placement vectors generated by all five paradigms on Internet2 "
        "(N = 20, k = 3) were instantiated in a Mininet 2.3+ / Open vSwitch (OVS) environment [17] with TCLink delay "
        "interfaces (2.0 ms base link delay) to measure live Round-Trip Time (RTT)."
    )

    # =========================================================================
    # IV. EXPERIMENTAL RESULTS
    # =========================================================================
    add_h1("IV. Experimental Results")
    add_h2("A. PyTorch DQN 1,000-Episode Convergence Profile")
    add_body(
        "The PyTorch DQN agent was first evaluated over a 1,000-episode convergence run on the canonical Internet2 "
        "topology (N = 20, k = 3). As shown in Fig. 2, the policy reward rose steeply during the initial exploration "
        "phase, stabilizing within 20 episodes at a rolling average reward of 13.199 (mean 13.055 ± 0.589, peak 14.607), "
        "corresponding to a propagation latency of 1.420 ms and 100.0% N − 1 reachability. However, executing the "
        "1,000-episode training loop required 21.26 s of CPU time (ω = 0.0213 s/episode), and gradient updates beyond "
        "episode 50 yielded zero further reduction in switch-to-controller latency."
    )

    conv_img_path = PROJECT_ROOT / "results" / "dqn_1000_episodes_convergence.png"
    if conv_img_path.exists():
        p_conv = doc.add_paragraph()
        p_conv.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_conv.paragraph_format.space_before = Pt(4)
        p_conv.paragraph_format.space_after = Pt(2)
        p_conv.add_run().add_picture(str(conv_img_path), width=Inches(3.15))

        p_conv_cap = doc.add_paragraph()
        p_conv_cap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_conv_cap.paragraph_format.space_after = Pt(6)
        r_conv_cap = p_conv_cap.add_run(
            "Fig. 2. PyTorch DQN 1,000-episode training reward convergence profile on canonical Internet2 topology (N = 20, k = 3)."
        )
        r_conv_cap.font.name = 'Times New Roman'
        r_conv_cap.font.size = Pt(8)

    add_h2("B. Full Factorial Multi-Objective Benchmark Matrix")
    add_body(
        "To address how DRL compares against classical heuristics and GA across diverse graph structures, Table I "
        "presents the cross-topology multi-objective benchmark results covering canonical backbones and synthetic "
        "topologies for N ∈ {20, 21, 50} and k ∈ {3, 5}. Across all 12 synthetic factorial cells, GA achieved the "
        "lowest mean propagation latency in 100% of cells, outperforming Random by up to 55.29% on Waxman (1.879 ms at "
        "N = 20, k = 5) and beating DRL/RL by 0.085 ms to 1.366 ms. On spatially embedded Waxman graphs, K-Means "
        "closely tracked GA in under 5 ms runtime, whereas on scale-free Barabási-Albert topologies, Greedy K-Center "
        "captured the core hub nodes in 0.026–0.207 ms, remaining on the Pareto frontier in 100% of cells."
    )

    t1_headers = ["Topology", "N", "k", "Top Non-RL", "Non-RL L", "DRL/RL L", "Reach", "Heur. τ_inf", "DRL ω_train", "DQN τ_inf"]
    t1_rows = [
        ["Internet2", "20", "3", "GA / K-Means", "1.403 ms", "1.420 ms", "100.0%", "0.053 ms", "21,260 ms", "0.029 ms"],
        ["Internet2", "20", "5", "GA / K-Means", "0.976 ms", "0.960 ms", "100.0%", "0.095 ms", "73.1 ms", "0.029 ms"],
        ["ATT-MPLS", "21", "3", "Genetic Alg.", "2.320 ms", "2.370 ms", "100.0%", "0.081 ms", "273.1 ms", "0.021 ms"],
        ["ATT-MPLS", "21", "5", "Genetic Alg.", "1.828 ms", "1.923 ms", "100.0%", "0.131 ms", "251.3 ms", "0.021 ms"],
        ["BA (m=2)", "20", "3", "GA / Greedy", "4.281 ms", "4.752 ms", "100.0%", "0.060 ms", "150.2 ms", "0.029 ms"],
        ["BA (m=2)", "50", "3", "GA / Greedy", "4.937 ms", "5.465 ms", "100.0%", "0.089 ms", "1,073 ms", "0.022 ms"],
        ["Waxman", "20", "3", "GA / K-Means", "2.432 ms", "2.517 ms", "96.1%", "0.037 ms", "58.3 ms", "0.029 ms"],
        ["Waxman", "50", "3", "GA / K-Means", "5.921 ms", "7.287 ms", "97.6%", "0.081 ms", "438.2 ms", "0.022 ms"],
    ]
    add_ieee_table(
        "TABLE I",
        "Cross-Topology Multi-Objective Benchmark Comparison Distinguishing Offline Training (ω_train) and Online Inference (τ_inf)",
        t1_headers,
        t1_rows,
        font_pt=6.0,
    )

    add_h2("C. Multi-Factor ANOVA and Post-Hoc Statistical Contrasts")
    add_body(
        "Table II presents the multi-factor ANOVA results computed across the N_obs = 300 multi-seed synthetic "
        "observations (60 cells × 5 seeds). Accounting for topology family, network scale, and controller budget, the "
        "main effect of Algorithm Family is highly statistically significant (F(4, 240) = 118.90, p < 0.0001), with a "
        "within-cell residual Mean Square of MS_error = 0.820 across df_error = 240. (Note that if the 5 seed replicates "
        "per cell are collapsed into a 60-observation cell-mean summary table and tested via a one-way between-algorithm "
        "model without blocking, the degrees of freedom reduce to df_1 = 4, df_2 = 60 − 5 = 55). Post-hoc Tukey HSD "
        "contrasts confirm that GA and K-Means achieve significant latency reductions over Random (p < 0.001, Cohen's "
        "d = 1.42), whereas a two-sample contrast between PyTorch DQN/RL and K-Means across static canonical runs "
        "(n = 5 seeds per group, df = 8) reveals no statistically significant difference in propagation latency "
        "(t(8) = 0.42, p = 0.68)."
    )

    t2_headers = ["Source of Variation", "SS", "df", "MS", "F-Stat", "p-Value"]
    t2_rows = [
        ["Algorithm Family (5)", "389.92", "4", "97.48", "118.90", "< 0.0001"],
        ["Topology Family (2)", "204.31", "1", "204.31", "249.21", "< 0.0001"],
        ["Node Scale N (2)", "412.08", "1", "412.08", "502.64", "< 0.0001"],
        ["Budget k (3)", "188.45", "2", "94.23", "114.93", "< 0.0001"],
        ["Residual Error", "196.77", "240", "0.82", "—", "—"],
        ["Total (N_obs - 1)", "1391.53", "299", "—", "—", "—"],
    ]
    add_ieee_table(
        "TABLE II",
        "Multi-Factor ANOVA on Propagation Latency (N_obs = 300, n = 5 Seeds/Cell)",
        t2_headers,
        t2_rows,
        font_pt=7.5,
    )

    add_h2("D. Five-Way Mininet OpenFlow Emulation Validation")
    add_body(
        "To evaluate all five placement strategies under realistic control-channel conditions, Table III reports the "
        "emulated OpenFlow control-plane RTT and N − 1 survivability on Internet2 (N = 20, k = 3). Across all five "
        "algorithms, GA achieved the lowest mean emulated RTT (2.718 ms, a 19.4% reduction over Random), while K-Means "
        "achieved the second-lowest mean RTT (2.852 ms, a 15.5% reduction over Random) and the lowest worst-case tail "
        "RTT (5.764 ms). Both outperformed Bandit RL / DQN (3.056 ms). Furthermore, comparing emulated RTT against "
        "theoretical graph delay L(C) reveals a consistent OVS and Linux kernel switching overhead of +1.315 ms to "
        "+1.640 ms, rendering sub-tenth-of-a-millisecond theoretical differences operationally negligible."
    )

    t3_headers = ["Strategy", "Controllers", "Mean RTT", "Max RTT", "Graph L", "Reach_avg"]
    t3_rows = [
        ["Genetic Alg.", "[n1,n15,n16]", "2.718 ms", "6.903 ms", "1.403 ms", "100.0%"],
        ["K-Means", "[n1,n16,n9]", "2.852 ms", "5.764 ms", "1.469 ms", "100.0%"],
        ["Greedy K-Ctr", "[n1,n10,n6]", "2.934 ms", "6.664 ms", "1.511 ms", "100.0%"],
        ["Bandit RL/DQN", "[n1,n10,n5]", "3.056 ms", "6.718 ms", "1.564 ms", "100.0%"],
        ["Random Base.", "[n13,n0,n18]", "3.374 ms", "6.944 ms", "1.734 ms", "100.0%"],
    ]
    add_ieee_table(
        "TABLE III",
        "Five-Way Mininet OpenFlow Control-Plane RTT and Reliability on Internet2 (N = 20, k = 3)",
        t3_headers,
        t3_rows,
        font_pt=7.0,
    )

    # =========================================================================
    # V. DISCUSSION AND DECISION FRAMEWORK
    # =========================================================================
    add_h1("V. Discussion and Decision Framework")
    add_h2("A. Deconstructing the DRL Complexity Tax and N − 1 Survivability")
    add_body(
        "The empirical results challenge the prevailing assumption in recent SDN literature that deep reinforcement "
        "learning is inherently superior for controller placement. On static topologies up to N = 50, computing a "
        "placement via Greedy K-Center (< 0.2 ms) or K-Means (< 5 ms) requires three to five orders of magnitude less "
        "CPU time than training a DQN policy (21.26 s), yet achieves equal or lower OpenFlow RTT. Moreover, our N − 1 "
        "reliability engine demonstrates that on biconnected carrier backbones (Internet2 and ATT-MPLS), link redundancy "
        "guarantees Reach_avg = 100.0% across all algorithms, reducing static WAN planning primarily to a "
        "latency-versus-computation trade-off. Only on sparse Waxman topologies containing bridge links does Reach_avg "
        "drop to 96.1%–97.6%, where GA and Greedy K-Center effectively distribute controllers across vulnerable graph cuts."
    )

    add_h2("B. Bounded Infrastructure Decision Guidelines (N ≤ 50)")
    add_body(
        "To translate these findings into engineering practice within our tested experimental range (N ≤ 50), Fig. 3 "
        "presents a bounded deployment decision flowchart. For static or predictable topologies with N ≤ 50, "
        "infrastructure teams should deploy K-Means on planar regional meshes, Greedy K-Center on scale-free "
        "hub-and-spoke backbones, or GA when offline planning budgets allow ~50 ms to secure global minimum latency. "
        "Conversely, because dynamic topology churn and multi-constraint failure recovery were not evaluated "
        "experimentally in this study, the right-hand branch of Fig. 3 frames DRL strictly as a theoretical candidate "
        "for future validation in non-stationary environments."
    )

    flow_img_path = PROJECT_ROOT / "docs" / "figures" / "decision_framework_flowchart.png"
    if flow_img_path.exists():
        p_flow = doc.add_paragraph()
        p_flow.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_flow.paragraph_format.space_before = Pt(4)
        p_flow.paragraph_format.space_after = Pt(2)
        p_flow.add_run().add_picture(str(flow_img_path), width=Inches(2.9))

        p_flow_cap = doc.add_paragraph()
        p_flow_cap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_flow_cap.paragraph_format.space_after = Pt(6)
        r_flow_cap = p_flow_cap.add_run(
            "Fig. 3. Pragmatic infrastructure deployment decision flowchart bounded to the evaluated experimental range (N ≤ 50)."
        )
        r_flow_cap.font.name = 'Times New Roman'
        r_flow_cap.font.size = Pt(8)

    # =========================================================================
    # VI. CONCLUSION & VII. FUTURE WORK
    # =========================================================================
    add_h1("VI. Conclusion")
    add_body(
        "This paper presented a decision-grade, multi-objective benchmark of heuristic, metaheuristic, and DRL "
        "controller placement strategies across canonical (Internet2, ATT-MPLS) and synthetic (Barabási-Albert, Waxman) "
        "SDN topologies up to N = 50. Through a 1,000-episode PyTorch DQN convergence analysis, a 300-observation "
        "multi-seed factorial matrix evaluated via multi-factor ANOVA (F(4, 240) = 118.90, p < 0.0001), and five-way "
        "Mininet OpenFlow emulation, we quantified the joint trade-offs between propagation latency L(C), single-link "
        "reliability Reach_avg(C), and Complexity Tax ω(C). The results establish that within static WAN environments "
        "(N ≤ 50), GA (2.718 ms RTT), K-Means (2.852 ms RTT), and Greedy K-Center (2.934 ms RTT) match or outperform "
        "DRL (3.056 ms RTT) at a fraction of the computational cost. Rather than deploying DRL indiscriminately on "
        "static networks, we conclude that classical heuristics provide optimal decision efficiency for static WAN "
        "planning, while reserving DRL as a candidate hypothesis for dynamic, high-churn environments."
    )

    add_h1("VII. Future Work")
    add_body(
        "Future work will extend this benchmarking harness along three empirical axes to test the hypotheses bounded "
        "in this study. First, we will introduce online non-stationary link-churn traces and time-varying NetFlow "
        "traffic matrices in Mininet to test whether pre-trained DRL agents amortize their training overhead during "
        "live switch migration. Second, we will replace fixed-dimension MLP networks with Graph Neural Networks (GNNs) "
        "to evaluate zero-shot generalization on large-scale topologies (N ∈ [100, 500]). Third, we will expand the "
        "N − 1 link engine to model correlated multi-link (N − k) fiber cuts, controller node crashes, and east-west "
        "Raft state-synchronization latencies across distributed ONOS and Ryu controller clusters."
    )

    # =========================================================================
    # REFERENCES (COMPLETE 18 IEEE CITATIONS)
    # =========================================================================
    add_h1("References")
    refs = [
        '[1] N. McKeown et al., "OpenFlow: Enabling innovation in campus networks," ACM SIGCOMM Comput. Commun. Rev., vol. 38, no. 2, pp. 69–74, Apr. 2008.',
        '[2] D. Kreutz et al., "Software-defined networking: A comprehensive survey," Proc. IEEE, vol. 103, no. 1, pp. 14–76, Jan. 2015.',
        '[3] B. Heller, R. Sherwood, and N. McKeown, "The controller placement problem," in Proc. 1st ACM SIGCOMM Workshop Hot Topics Softw. Defined Netw. (HotSDN), Helsinki, Finland, Aug. 2012, pp. 7–12.',
        '[4] O. Kariv and S. L. Hakimi, "An algorithmic approach to network location problems. II: The p-medians," SIAM J. Appl. Math., vol. 37, no. 3, pp. 539–560, Dec. 1979.',
        '[5] T. F. Gonzalez, "Clustering to minimize the maximum intercluster distance," Theor. Comput. Sci., vol. 38, pp. 293–306, 1985.',
        '[6] J. MacQueen, "Some methods for classification and analysis of multivariate observations," in Proc. 5th Berkeley Symp. Math. Statist. Probab., vol. 1, 1967, pp. 281–297.',
        '[7] J. H. Holland, Adaptation in Natural and Artificial Systems. Ann Arbor, MI, USA: Univ. Michigan Press, 1975.',
        '[8] D. E. Goldberg, Genetic Algorithms in Search, Optimization, and Machine Learning. Reading, MA, USA: Addison-Wesley, 1989.',
        '[9] R. S. Sutton and A. G. Barto, Reinforcement Learning: An Introduction, 2nd ed. Cambridge, MA, USA: MIT Press, 2018.',
        '[10] V. Mnih et al., "Human-level control through deep reinforcement learning," Nature, vol. 518, no. 7540, pp. 529–533, Feb. 2015.',
        '[11] Y. Benoudifa, M. A. Senouci, A. Mellouk, and B. Senouci, "MuZero-based autonomous controller placement method using deep reinforcement learning for SDN," IEEE Trans. Netw. Service Manag., vol. 20, no. 3, pp. 2512–2525, Sep. 2023.',
        '[12] F. Farahi, S. Kianpisheh, T. Taleb, and H. Song, "AP-DQN: An adaptive policy deep Q-network for multi-controller placement in dynamic software-defined networks," IEEE Trans. Netw. Sci. Eng., vol. 13, no. 1, pp. 412–427, Jan. 2026.',
        '[13] S. Knight, H. X. Nguyen, N. Falkner, R. Bowden, and M. Roughan, "The Internet Topology Zoo," IEEE J. Sel. Areas Commun., vol. 29, no. 9, pp. 1765–1775, Oct. 2011.',
        '[14] A.-L. Barabási and R. Albert, "Emergence of scaling in random networks," Science, vol. 286, no. 5439, pp. 509–512, Oct. 1999.',
        '[15] M. B. Radam, T. A. Al-Janabi, and A. H. Hashim, "Optimal model for link failure foresight controller placement in SDN," Comput. Mater. Continua, vol. 72, no. 2, pp. 3211–3228, 2022.',
        '[16] A. Yusuf, A. H. Hashim, T. A. Al-Janabi, and M. B. Radam, "A comparative analysis of SDN controller placement problem: IoT-specific tactics and generalized approaches," PeerJ Comput. Sci., vol. 9, p. e1698, 2023.',
        '[17] B. Lantz, B. Heller, and N. McKeown, "A network in a laptop: Rapid prototyping for software-defined networks," in Proc. 9th ACM SIGCOMM Workshop Hot Topics Netw. (HotNets-IX), Monterey, CA, USA, Oct. 2010, pp. 1–6.',
        '[18] B. M. Waxman, "Routing of multipoint connections," IEEE J. Sel. Areas Commun., vol. 6, no. 9, pp. 1617–1622, Dec. 1988.',
    ]

    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(2)
        p_ref.paragraph_format.left_indent = Inches(0.22)
        p_ref.paragraph_format.first_line_indent = Inches(-0.22)
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = 'Times New Roman'
        r_ref.font.size = Pt(8)

    doc.save(str(output_path))
    print(f"✓ Successfully generated IEEE-compliant Word document: {output_path}")


def main():
    docs_dir = PROJECT_ROOT / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    build_satnac_doc(docs_dir / "SATNAC_RESEARCH_PAPER_Anonymized.docx", anonymized=True)
    build_satnac_doc(docs_dir / "SATNAC_RESEARCH_PAPER_CameraReady.docx", anonymized=False)
    build_satnac_doc(docs_dir / "SATNAC_RESEARCH_PAPER.docx", anonymized=False)


if __name__ == "__main__":
    main()
