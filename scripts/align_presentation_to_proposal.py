#!/usr/bin/env python3
"""Patch PPTX slides text and notes to align with proposal and rubric.

Produces a new PPTX with '.aligned.pptx' suffix.

Usage: python scripts/align_presentation_to_proposal.py <input.pptx>
"""
import sys
from zipfile import ZipFile
from xml.etree import ElementTree as ET
from pathlib import Path
import shutil
import tempfile

NSMAP = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
}


def find_text_nodes(tree):
    return tree.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}t')


def set_slide_text(slide_xml_path, new_lines):
    ET.register_namespace('a', NSMAP['a'])
    tree = ET.parse(slide_xml_path)
    nodes = find_text_nodes(tree)
    if not nodes:
        return
    # set first N nodes
    for i, nl in enumerate(new_lines):
        if i < len(nodes):
            nodes[i].text = nl
    # clear remaining nodes that would contain old text beyond our replacements
    for j in range(len(new_lines), len(nodes)):
        nodes[j].text = ''
    tree.write(slide_xml_path, encoding='utf-8', xml_declaration=True)


def set_notes_text(notes_xml_path, notes_text):
    try:
        ET.register_namespace('a', NSMAP['a'])
        tree = ET.parse(notes_xml_path)
    except FileNotFoundError:
        return
    nodes = find_text_nodes(tree)
    if nodes:
        nodes[0].text = notes_text
    tree.write(notes_xml_path, encoding='utf-8', xml_declaration=True)


def main():
    if len(sys.argv) < 2:
        print('Usage: align_presentation_to_proposal.py <input.pptx>')
        raise SystemExit(2)
    inp = Path(sys.argv[1])
    if not inp.exists():
        print('Input not found:', inp)
        raise SystemExit(2)
    out = inp.with_name(inp.stem + '.aligned' + inp.suffix)

    # mapping slide index -> new lines and notes
    slides_content = {
        1: {
            'lines': [
                'HONOURS PRESENTATION PROPOSAL • TITLE AND RESEARCH FOCUS',
                'Multi-Objective Decision Analysis for SDN Controller Placement',
                'Decision-Grade Multi-Objective Benchmarking of SDN Controller Placement — Multi-axis evidence for operational decisions',
            ],
            'notes': 'Maps to Proposal §3–§5. One-sentence thesis: Treat controller placement as multi-objective (L, Reach_avg, ω). (0:45)'
        },
        2: {
            'lines': [
                'BACKGROUND AND CONTEXT • THE DISTRIBUTED TRANSITION',
                'The Shift from Centralized Authority to Distributed State Consensus',
                'So What: Controller placement is a decision problem across L, Reach_avg, and Complexity ω — see Proposal §6 & Rubric: Background (15%)'
            ],
            'notes': 'Background: situate the CPP, why multi-site topologies matter. (0:45)'
        },
        3: {
            'lines': [
                'PROBLEM STATEMENT & RESEARCH GAP • SPECIFIC JUSTIFICATIONS',
                'Primary RQ: Do AI-driven placement methods produce Pareto-superior operating points on (L, Reach_avg, ω) vs. heuristics in multi-site topologies?',
                'Supporting RQ1: What is the effect on L and Reach_avg per controller budget k in {2,3,5}?',
                'Supporting RQ2: After pricing complexity ω (s/episode), which methods remain practically superior?'
            ],
            'notes': 'Maps to Proposal §3 — Rubric: Problem Statement (20%). Make RQs clear and researchable. (0:45)'
        },
        4: {
            'lines': [
                'AIM & OBJECTIVES • CRITICAL TARGETS',
                'Objective 1: Build reproducible, config-driven Mininet/Ryu pipeline (Seed=42).',
                'Objective 2: Benchmark DQN vs. Greedy/K-Center across Internet2 and ATT-MPLS at k ∈ {2,3,5}.',
                'Objective 3: Publish auditable metrics L(ms), Reach_avg (N-1), ω(s/episode).',
                'Objective 4: Synthesize Pareto front and derive selection rules.'
            ],
            'notes': 'Maps to Proposal §4 — Rubric: Aim & Objectives (15%). Read objectives crisply. (1:00)'
        },
        5: {
            'lines': [
                'METHODOLOGY PIPELINE • TWO-TIER VALIDATION RIGOR',
                'TIER 1: Synthetic search sweep → produce non-dominated shortlist',
                'TIER 2: Kernel emulation (Mininet) under iperf3 stress; measure RTT',
                'Controls: Seed=42; Topologies={Internet2 (N=11), ATT-MPLS (N=21)}; Budgets k={2,3,5}; N-1 single-link failures; Metrics: L, Reach_avg, ω; Stats: ANOVA + Tukey'
            ],
            'notes': 'Maps to Proposal §8 — Rubric: Methodology (20%). Emphasize reproducibility and statistical plan. (1:00)'
        },
        6: {
            'lines': [
                'EVIDENCE OF FEASIBILITY • MEASURED EMPIRICAL DATA',
                'Pilot KPIs: ω = 0.0226 s/episode; DQN 50 ep elapsed = 1.13s; mean reward = 11.385',
                'Multi-seed verification: seeds [42,123,456,789,999] => Reach_avg = 1.0',
                'Physical Avg RTT = 4.415 ms; Worst = 10.219 ms; rtt - graph ≈ 2.192 ms'
            ],
            'notes': 'Maps to Proposal §11/12 — Rubric: Feasibility (15%). Call out artifact paths: results/pilot_metrics.json, results/rl_analysis/pareto/pareto_shortlist.json. (1:15)'
        },
        7: {
            'lines': [
                'PHASE-6 EXPERIMENTAL VALIDATION • MININET EMULATION CHECKS',
                'Internet2 greedy k-center controllers placed at [0,8,6] → Reach_avg = 1.0',
                'Best Mininet RTT = 4.415 ms; graph-to-emulator delta ≈ 2.19 ms',
                'Interpretation: small, quantifiable translation overhead; supports operational claims'
            ],
            'notes': 'Maps to Proposal §8 — Rubric: Methodology & Contribution. Emphasize translation validity. (0:55)'
        },
        8: {
            'lines': [
                'EXPECTED CONTRIBUTION & STUDY SIGNIFICANCE • RUBRIC ALIGNMENT',
                '1) Theoretical: MOCO pipeline + Complexity Tax (ω).',
                '2) Practical: Reproducible solver→emulator suite and datasets.',
                '3) Policy: Operator selection matrix for topology-conditioned method selection.'
            ],
            'notes': 'Maps to Proposal §5 — Rubric: Contribution (15%). Keep contributions crisp and auditable. (1:00)'
        },
        9: {
            'lines': [
                'TECHNICAL CONSTRAINTS & ENGAGEMENT RISKS • SYSTEM BOUNDARIES',
                'Risks: Linux namespace jitter; scale explosion in ATT-MPLS; training stability.',
                'Mitigations: CPU core pinning; hierarchical clustering for scale; progressive replay buffers.'
            ],
            'notes': 'Maps to Proposal §9 — Rubric: Feasibility & Quality. State mitigations plainly. (0:40)'
        },
        10: {
            'lines': [
                'STRATEGIC TIMELINE & CLOSE • EXAMINERS BLUEPRINT',
                'Request: approval to run full factorial (50,000 episodes). Deliverables: thesis, dataset, code repository.',
                'Ethics: No PII; software metrics only. Timeline: emulator tests by M6; draft by M7; final defense M8.'
            ],
            'notes': 'Maps to Proposal §11/12 — Rubric: Clarity & Presentation (5%). Closing ask and deliverables. (0:20)'
        }
    }

    tmpd = Path(tempfile.mkdtemp())
    try:
        with ZipFile(inp, 'r') as zin:
            zin.extractall(tmpd)

        # patch slides
        for idx, content in slides_content.items():
            slide_name = f'ppt/slides/slide{idx}.xml'
            slide_path = tmpd / slide_name
            if slide_path.exists():
                set_slide_text(slide_path, content['lines'])
            # notes
            notes_name = f'ppt/notesSlides/notesSlide{idx}.xml'
            notes_path = tmpd / notes_name
            if notes_path.exists():
                set_notes_text(notes_path, content['notes'])
            else:
                # try notesMasters or skip if not present
                pass

        # write new pptx
        with ZipFile(out, 'w') as zout:
            for f in tmpd.rglob('*'):
                arcname = str(f.relative_to(tmpd)).replace('\\', '/')
                if f.is_file():
                    zout.write(f, arcname)

        print('Wrote aligned presentation to', out)
    finally:
        shutil.rmtree(tmpd)


if __name__ == '__main__':
    main()
