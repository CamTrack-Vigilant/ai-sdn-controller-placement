#!/usr/bin/env python3
"""
Generate an ultra-high-definition, print-ready, self-contained A0 Landscape academic poster
100% aligned with:
  1. dissertation/Honours_Mini_Dissertation_Thabang_Buthelezi.pdf
  2. docs/SATNAC_RESEARCH_PAPER.pdf
"""
import os
import shutil
import base64
import subprocess

WORKSPACE = "/home/pro/Desktop/ai-sdn-controller-placement"
POSTER_DIR = os.path.join(WORKSPACE, "poster")
DISS_DIR = os.path.join(WORKSPACE, "dissertation")


def img_to_b64(path):
    full_path = os.path.join(WORKSPACE, path)
    if os.path.exists(full_path):
        with open(full_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            ext = os.path.splitext(path)[1].lower().replace(".", "")
            if ext == "jpg":
                ext = "jpeg"
            return f"data:image/{ext};base64,{data}"
    print(f"Warning: Image {path} not found!")
    return ""


crest_b64 = img_to_b64("docs/figures/unizulu_crest.png")
pareto_b64 = img_to_b64("SDN_Pareto_3D.png")
dqn_b64 = img_to_b64("results/dqn_1000_episodes_convergence.png")
workflow_b64 = img_to_b64("docs/figures/proposal_methodology_workflow.png")
decision_b64 = img_to_b64("docs/figures/decision_framework_flowchart.png")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>UNIZULU Honours & SATNAC 2026 Research Poster - Thabang Nhlokoma Buthelezi</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@500;600;700;800;900&family=Fira+Code:wght@500;600;700&display=swap');

    :root {{
      --unizulu-blue: #09203f;
      --unizulu-navy: #14315c;
      --unizulu-accent: #e0a926;
      --unizulu-gold: #c59b27;
      --tech-cyan: #0284c7;
      --tech-green: #16a34a;
      --tech-purple: #7c3aed;
      --tech-orange: #ea580c;
      --bg-light: #f1f5f9;
      --card-bg: #ffffff;
      --card-border: #cbd5e1;
      --text-main: #0f172a;
      --text-muted: #1e293b;
      --text-light: #475569;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    @page {{
      size: 1189mm 841mm; /* A0 Landscape */
      margin: 0;
    }}

    html, body {{
      width: 1189mm;
      height: 841mm;
      background: var(--bg-light);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      color: var(--text-main);
      overflow: hidden;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}

    .poster-container {{
      width: 1189mm;
      height: 841mm;
      padding: 8mm 12mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 5.5mm;
    }}

    /* ================= HEADER ================= */
    .header {{
      background: linear-gradient(135deg, #05162e 0%, #0b2545 45%, #13315c 100%);
      border-radius: 16px;
      padding: 6.5mm 14mm;
      color: #ffffff;
      display: grid;
      grid-template-columns: 210mm 1fr 215mm;
      align-items: center;
      gap: 10mm;
      border-bottom: 4.5mm solid var(--unizulu-accent);
      box-shadow: 0 10px 25px rgba(11, 37, 69, 0.18);
    }}

    .logo-container {{
      background: #ffffff;
      padding: 3mm 5.5mm;
      border-radius: 12px;
      display: flex;
      align-items: center;
      gap: 4.5mm;
      box-shadow: 0 6px 15px rgba(0,0,0,0.15);
    }}

    .logo-container img {{
      height: 22mm;
      width: auto;
      object-fit: contain;
    }}

    .logo-text {{
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}

    .logo-text-main {{
      font-family: 'Outfit', sans-serif;
      font-size: 15pt;
      font-weight: 800;
      color: #0b2545;
      letter-spacing: 0.4px;
      line-height: 1.15;
    }}

    .logo-text-sub {{
      font-size: 9.5pt;
      font-weight: 700;
      color: #92400e;
      text-transform: uppercase;
      letter-spacing: 0.9px;
      margin-top: 1mm;
    }}

    .title-container {{
      text-align: center;
    }}

    .symposium-pill {{
      display: inline-block;
      background: rgba(224, 169, 38, 0.22);
      border: 1.5px solid var(--unizulu-accent);
      color: #ffd166;
      font-size: 13pt;
      font-weight: 800;
      padding: 1.5mm 10mm;
      border-radius: 50px;
      text-transform: uppercase;
      letter-spacing: 1.4px;
      margin-bottom: 2.2mm;
    }}

    .poster-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 27.5pt;
      font-weight: 800;
      line-height: 1.15;
      color: #ffffff;
      margin-bottom: 2.5mm;
      letter-spacing: -0.3px;
    }}

    .poster-meta {{
      font-size: 15.2pt;
      color: #e2e8f0;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-wrap: wrap;
      gap: 4.5mm;
    }}

    .author-highlight {{
      color: #ffffff;
      font-weight: 800;
    }}

    .supervisor-highlight {{
      color: #ffd166;
      font-weight: 700;
    }}

    .header-right {{
      text-align: right;
      border-left: 2px solid rgba(255,255,255,0.25);
      padding-left: 7mm;
    }}

    .dept-title {{
      font-size: 15.5pt;
      font-weight: 800;
      color: #ffffff;
    }}

    .faculty-title {{
      font-size: 12.8pt;
      color: #cbd5e1;
      margin-top: 1.2mm;
    }}

    .theme-tag {{
      font-size: 10.8pt;
      color: var(--unizulu-accent);
      font-style: italic;
      margin-top: 1.8mm;
      line-height: 1.25;
    }}

    /* ================= 3-COLUMN MAIN GRID ================= */
    .grid-content {{
      display: grid;
      grid-template-columns: 0.98fr 1.24fr 1.02fr;
      gap: 6.5mm;
      flex: 1;
      min-height: 0;
    }}

    .col {{
      display: flex;
      flex-direction: column;
      gap: 5mm;
      height: 100%;
      min-height: 0;
    }}

    /* ================= CARDS ================= */
    .card {{
      background: var(--card-bg);
      border-radius: 13px;
      padding: 4.5mm 6mm;
      border: 1.5px solid var(--card-border);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
      display: flex;
      flex-direction: column;
      min-height: 0;
    }}

    .card.grow {{
      flex: 1;
    }}

    .card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 2.5px solid var(--unizulu-blue);
      padding-bottom: 2mm;
      margin-bottom: 2.8mm;
    }}

    .card-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 16.2pt;
      font-weight: 800;
      color: var(--unizulu-blue);
      display: flex;
      align-items: center;
      gap: 2.8mm;
    }}

    .sec-num {{
      background: var(--unizulu-blue);
      color: #ffffff;
      width: 6.8mm;
      height: 6.8mm;
      border-radius: 50%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 11.5pt;
      font-weight: 800;
    }}

    .badge {{
      font-size: 9.6pt;
      font-weight: 800;
      padding: 1mm 3.8mm;
      border-radius: 20px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .badge-blue {{ background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }}
    .badge-gold {{ background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }}
    .badge-green {{ background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }}
    .badge-purple {{ background: #f3e8ff; color: #6b21a8; border: 1px solid #e9d5ff; }}

    .card-body {{
      font-size: 11.2pt;
      line-height: 1.35;
      color: var(--text-muted);
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 2.2mm;
      min-height: 0;
    }}

    p {{
      margin: 0;
    }}

    strong {{
      color: var(--text-main);
      font-weight: 700;
    }}

    /* Highlight Callouts */
    .callout {{
      background: #f8fafc;
      border-left: 3.2mm solid var(--unizulu-navy);
      padding: 2mm 3.8mm;
      border-radius: 0 7px 7px 0;
      font-size: 10.8pt;
      line-height: 1.32;
    }}

    .callout.gold {{
      background: #fffdf5;
      border-left-color: var(--unizulu-accent);
    }}

    .callout.green {{
      background: #f0fdf4;
      border-left-color: var(--tech-green);
    }}

    .callout.blue {{
      background: #f0f9ff;
      border-left-color: var(--tech-cyan);
    }}

    /* Equation Box */
    .eq-grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 1.6mm;
      background: #f8fafc;
      border: 1.2px solid #cbd5e1;
      border-radius: 8px;
      padding: 2.2mm 3.5mm;
    }}

    .eq-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 10.4pt;
      border-bottom: 1px dashed #cbd5e1;
      padding-bottom: 1mm;
    }}

    .eq-row:last-child {{
      border-bottom: none;
      padding-bottom: 0;
    }}

    .eq-math {{
      font-family: 'Fira Code', monospace;
      font-size: 10pt;
      font-weight: 600;
      color: var(--unizulu-blue);
    }}

    /* Research Questions */
    .rq-box {{
      background: #f1f5f9;
      border-left: 3.2mm solid var(--tech-cyan);
      border-radius: 6px;
      padding: 1.8mm 3.4mm;
      font-size: 10.8pt;
      line-height: 1.3;
    }}

    .rq-box strong {{
      color: var(--unizulu-navy);
      font-size: 11pt;
    }}

    /* Topology Pills */
    .topo-strip {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 2mm;
    }}

    .topo-pill {{
      background: #f8fafc;
      border: 1.2px solid #cbd5e1;
      border-radius: 6px;
      padding: 1.4mm 2mm;
      text-align: center;
      font-size: 9.6pt;
      line-height: 1.2;
    }}

    .topo-pill strong {{
      display: block;
      color: var(--unizulu-blue);
      font-size: 10pt;
    }}

    /* Paradigms Grid */
    .paradigm-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2mm;
    }}

    .paradigm-card {{
      background: #f8fafc;
      border: 1.2px solid #cbd5e1;
      border-radius: 7px;
      padding: 1.8mm 2.8mm;
    }}

    .paradigm-title {{
      font-size: 10.8pt;
      font-weight: 800;
      color: var(--unizulu-blue);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .complexity-tag {{
      font-family: 'Fira Code', monospace;
      font-size: 9.4pt;
      font-weight: 700;
      color: var(--text-light);
    }}

    .paradigm-desc {{
      font-size: 9.8pt;
      color: var(--text-muted);
      margin-top: 0.8mm;
      line-height: 1.22;
    }}

    /* Visual Figures */
    .fig-box {{
      background: #ffffff;
      border: 1.2px solid #cbd5e1;
      border-radius: 9px;
      padding: 2mm;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      flex: 1;
      min-height: 0;
    }}

    .fig-box img {{
      max-width: 100%;
      height: auto;
      max-height: 100%;
      border-radius: 5px;
      object-fit: contain;
    }}

    .fig-caption {{
      font-size: 9.6pt;
      color: var(--text-light);
      font-style: italic;
      margin-top: 1.2mm;
      line-height: 1.2;
    }}

    /* Stat Cards Row (6 Metrics) */
    .stat-banner {{
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 2.2mm;
    }}

    .metric-pill {{
      background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
      border: 1.8px solid #cbd5e1;
      border-radius: 9px;
      padding: 2mm 1.5mm;
      text-align: center;
      box-shadow: 0 3px 6px rgba(0,0,0,0.03);
    }}

    .metric-pill.gold {{
      background: linear-gradient(135deg, #fffdf5 0%, #fef9e7 100%);
      border-color: #f59e0b;
    }}

    .metric-pill.green {{
      background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
      border-color: #22c55e;
    }}

    .metric-val {{
      font-family: 'Outfit', sans-serif;
      font-size: 16.5pt;
      font-weight: 900;
      color: var(--unizulu-navy);
      line-height: 1.1;
    }}

    .metric-val.gold {{ color: #b45309; }}
    .metric-val.blue {{ color: #0284c7; }}
    .metric-val.green {{ color: #15803d; }}
    .metric-val.purple {{ color: #6d28d9; }}

    .metric-lbl {{
      font-size: 8.2pt;
      font-weight: 800;
      text-transform: uppercase;
      color: var(--text-light);
      margin-top: 0.8mm;
      letter-spacing: 0.3px;
      line-height: 1.15;
    }}

    /* Custom Data Table */
    .table-box {{
      border: 1.2px solid #cbd5e1;
      border-radius: 7px;
      overflow: hidden;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 9.8pt;
    }}

    th {{
      background: var(--unizulu-navy);
      color: #ffffff;
      padding: 1.5mm 2.2mm;
      font-weight: 700;
      text-align: left;
      font-size: 9.3pt;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }}

    td {{
      padding: 1.35mm 2.2mm;
      border-bottom: 1px solid #e2e8f0;
      color: var(--text-muted);
    }}

    tr:last-child td {{
      border-bottom: none;
    }}

    tr:nth-child(even) {{
      background: #f8fafc;
    }}

    tr.win-row {{
      background: #f0fdf4;
      font-weight: 700;
    }}

    tr.win-row td {{
      color: #166534;
    }}

    tr.subwin-row {{
      background: #eff6ff;
      font-weight: 600;
    }}

    tr.subwin-row td {{
      color: #1e40af;
    }}

    .badge-win {{
      background: #16a34a;
      color: #ffffff;
      font-size: 7.8pt;
      font-weight: 800;
      padding: 0.3mm 1.8mm;
      border-radius: 4px;
      margin-left: 1mm;
    }}

    .badge-tail {{
      background: #0284c7;
      color: #ffffff;
      font-size: 7.8pt;
      font-weight: 800;
      padding: 0.3mm 1.8mm;
      border-radius: 4px;
      margin-left: 1mm;
    }}

    /* Split Side-by-Side Figure + Table/Cards */
    .split-row {{
      display: grid;
      grid-template-columns: 1.05fr 0.95fr;
      gap: 3mm;
      align-items: stretch;
      flex: 1;
      min-height: 0;
    }}

    /* Decision 2x2 Grid */
    .decision-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2mm;
    }}

    .dec-card {{
      padding: 1.8mm 2.8mm;
      border-radius: 7px;
      font-size: 9.8pt;
      line-height: 1.25;
    }}

    .dec-card.classical {{
      background: #f0fdf4;
      border: 1.2px solid #86efac;
    }}

    .dec-card.ga {{
      background: #fefce8;
      border: 1.2px solid #fde047;
    }}

    .dec-card.drl {{
      background: #eff6ff;
      border: 1.2px solid #93c5fd;
    }}

    .dec-header {{
      font-size: 10.3pt;
      font-weight: 800;
      margin-bottom: 0.6mm;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .dec-card.classical .dec-header {{ color: #15803d; }}
    .dec-card.ga .dec-header {{ color: #a16207; }}
    .dec-card.drl .dec-header {{ color: #1d4ed8; }}

    /* ================= FOOTER ================= */
    .footer {{
      background: #ffffff;
      border-radius: 10px;
      padding: 2.2mm 8mm;
      border: 1.5px solid var(--card-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 9.6pt;
      color: var(--text-light);
      box-shadow: 0 3px 10px rgba(0,0,0,0.03);
    }}

    .footer strong {{
      color: var(--unizulu-blue);
    }}
  </style>
</head>
<body>

  <div class="poster-container">

    <!-- ================= HEADER ================= -->
    <header class="header">
      <div class="logo-container">
        <img src="{crest_b64}" alt="University of Zululand Crest">
        <div class="logo-text">
          <span class="logo-text-main">UNIVERSITY OF ZULULAND</span>
          <span class="logo-text-sub">A Node for African Thought</span>
        </div>
      </div>

      <div class="title-container">
        <div class="symposium-pill">2026 BSc Honours Computer Science Research • SATNAC 2026 Track</div>
        <h1 class="poster-title">Decision-Grade Multi-Objective Benchmarking of DRL and Heuristic Controller Placement in Multi-Site Software Defined Networks</h1>
        <div class="poster-meta">
          <span>Candidate: <strong class="author-highlight">Thabang Nhlokoma Buthelezi</strong> (Student No: 230011908)</span>
          <span>•</span>
          <span>Supervisors: <strong class="supervisor-highlight">Prof. Pragasen Mudali</strong> (UNIZULU) &amp; <strong class="supervisor-highlight">Mr. Skhumbuzo Zwane</strong> (CSIR / UNIZULU)</span>
        </div>
      </div>

      <div class="header-right">
        <div class="dept-title">Department of Computer Science</div>
        <div class="faculty-title">Faculty of Science, Agriculture &amp; Engineering</div>
        <div class="theme-tag">"Empirical Multi-Objective Optimization, Mininet Emulation &amp; AI Complexity Tax Auditing"</div>
      </div>
    </header>

    <!-- ================= 3-COLUMN MAIN GRID ================= -->
    <main class="grid-content">

      <!-- ================= COLUMN 1 ================= -->
      <section class="col">

        <!-- 1. Background, Problem & 3-Axis Mathematical Model -->
        <div class="card" style="flex: 0.95;">
          <div class="card-header">
            <h2 class="card-title"><span class="sec-num">1</span> Background, Problem &amp; 3-Axis Formulation</h2>
            <span class="badge badge-blue">CPP Formulation</span>
          </div>
          <div class="card-body">
            <p>
              Software Defined Networking (SDN) decouples control intelligence from packet-forwarding hardware [1]–[3]. Across multi-site Wide Area Networks (WANs), partitioning switches across <em>k</em> controllers among <em>N</em> sites is the <strong>NP-hard Controller Placement Problem (CPP)</strong> [4], [6], [7].
            </p>
            <div class="callout gold">
              <strong>The Methodological Gap &amp; Complexity Tax (<em>ω</em>):</strong> Recent Deep Reinforcement Learning (DRL) studies (MuZero [12], CAPFUL [14], AP-DQN [15]) evaluate neural policies against trivial baselines on single-metric latency, omitting offline training overhead (<em>ω</em><sub>train</sub> vs. online inference <em>τ</em><sub>inf</sub>), graph structure sensitivity, and Open vSwitch kernel delays [6], [9].
            </div>
            <div class="eq-grid">
              <div class="eq-row">
                <span><strong>1. Mean Propagation Latency:</strong></span>
                <span class="eq-math">L(C) = (1/|V|) Σ<sub>v∈V</sub> min<sub>c∈C</sub> d<sub>G</sub>(v, c) &nbsp;(1)</span>
              </div>
              <div class="eq-row">
                <span><strong>2. Single-Link (<em>N</em>−1) Reachability:</strong></span>
                <span class="eq-math">Reach<sub>avg</sub>(C) = (1/|E|) Σ<sub>e∈E</sub> (1/|V|) Σ<sub>v∈V</sub> I<sub>reach</sub>(v, G&#92;{{e}}, C) &nbsp;(2)</span>
              </div>
              <div class="eq-row">
                <span><strong>3. Ideal-Point Pareto Distance:</strong></span>
                <span class="eq-math">D<sub>ideal</sub>(C) = √[0.5·L̂² + 0.3·(1 − R̂<sub>avg</sub>)² + 0.2·ω̂²] &nbsp;(3)</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 2. Research Questions & Factorial Corpus -->
        <div class="card" style="flex: 0.92;">
          <div class="card-header">
            <h2 class="card-title"><span class="sec-num">2</span> Research Questions &amp; Topology Corpus</h2>
            <span class="badge badge-gold">N_obs = 300 Design</span>
          </div>
          <div class="card-body">
            <div class="rq-box">
              <strong>RQ1 (Latency &amp; <em>N</em>−1 Survivability):</strong> Do PyTorch DQN [15] and Bandit RL achieve statistically significant reductions in <em>L</em>(<em>C</em>) and improvements in <em>Reach</em><sub>avg</sub>(<em>C</em>) over Greedy <em>K</em>-Center [4], <em>K</em>-Means [8], and GA [10]?
            </div>
            <div class="rq-box">
              <strong>RQ2 (Offline Training <em>ω</em><sub>train</sub> vs. Online Inference <em>τ</em><sub>inf</sub>):</strong> How does computational overhead scale across <em>N</em> ∈ {{20, 50}}, <em>k</em> ∈ {{2, 3, 5}}, and after how many link-churn epochs (<em>T</em><sub>break</sub>) does DQN amortize <em>ω</em><sub>train</sub>?
            </div>
            <div class="rq-box">
              <strong>RQ3 (Topology Geometry &amp; Mininet Validation):</strong> How do scale-free hub skew (BA) vs. spatial mesh structure (Waxman) and live OpenFlow kernel switching delays govern the 3D Pareto frontier?
            </div>
            <div class="topo-strip">
              <div class="topo-pill"><strong>Internet2 WAN</strong><em>N</em>=20, |<em>E</em>|=26<br>2-Edge-Conn.</div>
              <div class="topo-pill"><strong>ATT-MPLS WAN</strong><em>N</em>=21, |<em>E</em>|=54<br>2-Edge-Conn.</div>
              <div class="topo-pill"><strong>Barabási-Albert</strong><em>N</em>∈{{20,50}}, <em>m</em>=2<br>Scale-Free Hubs</div>
              <div class="topo-pill"><strong>Waxman Spatial</strong><em>N</em>∈{{20,50}}, α=0.4<br>Bridge/Leaf Cuts</div>
            </div>
          </div>
        </div>

        <!-- 3. Placement Paradigms & Pipeline -->
        <div class="card grow" style="flex: 1.28;">
          <div class="card-header">
            <h2 class="card-title"><span class="sec-num">3</span> 5 Evaluated Placement Paradigms &amp; Workflow</h2>
            <span class="badge badge-green">Methodology</span>
          </div>
          <div class="card-body">
            <div class="paradigm-grid">
              <div class="paradigm-card">
                <div class="paradigm-title"><span>1. Random Baseline</span> <span class="complexity-tag">O(k)</span></div>
                <div class="paradigm-desc">Controlled PRNG uniform sampling without replacement (lower bound).</div>
              </div>
              <div class="paradigm-card">
                <div class="paradigm-title"><span>2. Greedy K-Center [4],[7]</span> <span class="complexity-tag" style="color:var(--tech-cyan)">O(k·N)</span></div>
                <div class="paradigm-desc">Farthest-first deterministic 2-approximation minimax radius traversal.</div>
              </div>
              <div class="paradigm-card">
                <div class="paradigm-title"><span>3. Spatial K-Means [8],[9]</span> <span class="complexity-tag" style="color:var(--tech-green)">O(I·k·N)</span></div>
                <div class="paradigm-desc">Iterative shortest-path distance partitioning with discrete graph medoids.</div>
              </div>
              <div class="paradigm-card">
                <div class="paradigm-title"><span>4. Genetic Algorithm [10]</span> <span class="complexity-tag" style="color:var(--tech-purple)">O(G·P·kN)</span></div>
                <div class="paradigm-desc"><em>P</em><sub>pop</sub>=40, <em>G</em><sub>max</sub>=50, tournament selection, uniform crossover, swap <em>μ</em>=0.15.</div>
              </div>
            </div>

            <div class="paradigm-card" style="border-left: 3.2mm solid #f59e0b;">
              <div class="paradigm-title"><span>5. PyTorch Deep Q-Network (DQN) &amp; Bandit RL [15]</span> <span class="complexity-tag" style="color:#d97706">N→64→64→N MLP</span></div>
              <div class="paradigm-desc">ReLU MLP, Adam (<em>α</em>=0.001, <em>γ</em>=0.99), replay <em>M</em>=10,000, <em>ε</em>∈[1.0→0.05], Reward: <em>R</em>(<em>C</em>) = 10·(<em>L</em><sub>max</sub>−<em>L</em>(<em>C</em>))/<em>L</em><sub>max</sub> + 5·<em>Reach</em><sub>avg</sub>(<em>C</em>).</div>
            </div>

            <div class="fig-box">
              <img src="{workflow_b64}" alt="Research Methodology Workflow">
              <div class="fig-caption">Fig. 1. End-to-end comparative benchmarking harness integrating 5×2×2×3 multi-seed factorial sweep (N_obs = 300) and Mininet OpenFlow emulation.</div>
            </div>
          </div>
        </div>

      </section>

      <!-- ================= COLUMN 2 ================= -->
      <section class="col">

        <!-- 6-Metric KPI Banner -->
        <div class="stat-banner">
          <div class="metric-pill green">
            <div class="metric-val green">2.718 ms</div>
            <div class="metric-lbl">Best Mean RTT (GA)</div>
          </div>
          <div class="metric-pill gold">
            <div class="metric-val gold">2.852 ms</div>
            <div class="metric-lbl">K-Means (5.76ms Tail)</div>
          </div>
          <div class="metric-pill">
            <div class="metric-val blue">0.03–5.3 ms</div>
            <div class="metric-lbl">Heuristic Compute τ_inf</div>
          </div>
          <div class="metric-pill">
            <div class="metric-val purple">21.26 s</div>
            <div class="metric-lbl">DQN Train Tax ω_train</div>
          </div>
          <div class="metric-pill">
            <div class="metric-val">F = 118.90</div>
            <div class="metric-lbl">ANOVA (p &lt; 0.0001)</div>
          </div>
          <div class="metric-pill gold">
            <div class="metric-val gold">59–65 Ep.</div>
            <div class="metric-lbl">DQN Break-Even T*</div>
          </div>
        </div>

        <!-- 4. Cross-Topology Benchmark Matrix & 3D Pareto Space -->
        <div class="card grow" style="flex: 1.55;">
          <div class="card-header">
            <h2 class="card-title"><span class="sec-num">4</span> Cross-Topology Factorial Benchmark (Table I) &amp; 3D Pareto Frontier</h2>
            <span class="badge badge-blue">ω_train vs. τ_inf</span>
          </div>
          <div class="card-body">
            <div class="split-row">
              <div class="fig-box">
                <img src="{pareto_b64}" alt="3D Pareto Optimization Frontier">
                <div class="fig-caption">Fig. 2. 3-Axis Pareto space: Propagation Latency L(C) vs. N−1 Reachability Reach_avg(C) vs. Compute Tax ω(C).</div>
              </div>
              <div style="display:flex; flex-direction:column; justify-content:space-between; gap:2mm;">
                <div class="callout blue">
                  <strong>1. GA Raw Latency Dominance:</strong> Across all 12 synthetic factorial cells, GA achieved lowest mean latency in <strong>100% of cells</strong> (up to 55.29% below Random on Waxman <em>N</em>=20, <em>k</em>=5).
                </div>
                <div class="callout green">
                  <strong>2. Topology &amp; Menger's Theorem:</strong> 2-edge-connected graphs (Internet2, ATT-MPLS, BA <em>m</em>=2) guarantee <strong>100.0% <em>N</em>−1 reachability</strong>; sparse Waxman graphs with bridge links drop to <strong>94.5%–98.8%</strong> (96.1%–97.6% at <em>k</em>=3).
                </div>
                <div class="callout gold">
                  <strong>3. Training Tax vs. Forward Pass:</strong> Trained DQN inference is fast (<em>τ</em><sub>inf</sub> = 0.021–0.029 ms), but fixed-dimension MLPs require per-topology training (<em>ω</em><sub>train</sub> = 58.3–21,260 ms).
                </div>
              </div>
            </div>

            <div class="table-box">
              <table>
                <thead>
                  <tr>
                    <th>Topology Model</th>
                    <th><em>N</em></th>
                    <th><em>k</em></th>
                    <th>Top Non-RL Paradigm</th>
                    <th>Non-RL <em>L</em>(<em>C</em>)</th>
                    <th>DRL/RL <em>L</em>(<em>C</em>)</th>
                    <th><em>Reach</em><sub>avg</sub></th>
                    <th>Heur. <em>τ</em><sub>inf</sub></th>
                    <th>RL <em>ω</em><sub>train</sub></th>
                    <th>DQN <em>τ</em><sub>inf</sub></th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="win-row">
                    <td><strong>Internet2 (Canonical)</strong></td>
                    <td>20</td>
                    <td>3</td>
                    <td>GA / <em>K</em>-Means</td>
                    <td><strong>1.403 ms</strong></td>
                    <td>1.420 ms</td>
                    <td>100.0%</td>
                    <td>0.053 ms</td>
                    <td>21,260 ms*</td>
                    <td>0.029 ms</td>
                  </tr>
                  <tr>
                    <td><strong>Internet2 (Canonical)</strong></td>
                    <td>20</td>
                    <td>5</td>
                    <td>GA / <em>K</em>-Means</td>
                    <td>0.976 ms</td>
                    <td>0.960 ms</td>
                    <td>100.0%</td>
                    <td>0.095 ms</td>
                    <td>73.1 ms</td>
                    <td>0.029 ms</td>
                  </tr>
                  <tr class="win-row">
                    <td><strong>ATT-MPLS (Canonical)</strong></td>
                    <td>21</td>
                    <td>3</td>
                    <td>Genetic Algorithm</td>
                    <td><strong>2.320 ms</strong></td>
                    <td>2.370 ms</td>
                    <td>100.0%</td>
                    <td>0.081 ms</td>
                    <td>273.1 ms</td>
                    <td>0.021 ms</td>
                  </tr>
                  <tr>
                    <td><strong>ATT-MPLS (Canonical)</strong></td>
                    <td>21</td>
                    <td>5</td>
                    <td>Genetic Algorithm</td>
                    <td><strong>1.828 ms</strong></td>
                    <td>1.923 ms</td>
                    <td>100.0%</td>
                    <td>0.131 ms</td>
                    <td>251.3 ms</td>
                    <td>0.021 ms</td>
                  </tr>
                  <tr>
                    <td><strong>Barabási-Albert (<em>m</em>=2)</strong></td>
                    <td>20</td>
                    <td>3</td>
                    <td>GA / Greedy <em>K</em>-Ctr</td>
                    <td><strong>4.321 ms</strong></td>
                    <td>4.558 ms</td>
                    <td>100.0%</td>
                    <td>0.057 ms</td>
                    <td>157.6 ms</td>
                    <td>0.029 ms</td>
                  </tr>
                  <tr>
                    <td><strong>Barabási-Albert (<em>m</em>=2)</strong></td>
                    <td>50</td>
                    <td>3</td>
                    <td>GA / Greedy <em>K</em>-Ctr</td>
                    <td><strong>4.247 ms</strong></td>
                    <td>4.650 ms</td>
                    <td>100.0%</td>
                    <td>0.159 ms</td>
                    <td>1,064.5 ms</td>
                    <td>0.022 ms</td>
                  </tr>
                  <tr>
                    <td><strong>Waxman Spatial (<em>α</em>=0.4)</strong></td>
                    <td>20</td>
                    <td>3</td>
                    <td>GA / <em>K</em>-Means</td>
                    <td><strong>2.432 ms</strong></td>
                    <td>2.517 ms</td>
                    <td>96.1%</td>
                    <td>0.043 ms</td>
                    <td>58.3 ms</td>
                    <td>0.029 ms</td>
                  </tr>
                  <tr class="win-row">
                    <td><strong>Waxman Spatial (<em>α</em>=0.4)</strong></td>
                    <td>50</td>
                    <td>3</td>
                    <td>GA / <em>K</em>-Means</td>
                    <td><strong>5.921 ms</strong></td>
                    <td>7.287 ms</td>
                    <td>97.6%</td>
                    <td>0.086 ms</td>
                    <td>438.2 ms</td>
                    <td>0.022 ms</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- 5. DQN Convergence Dynamics & Multi-Factor ANOVA -->
        <div class="card grow" style="flex: 1.35;">
          <div class="card-header">
            <h2 class="card-title"><span class="sec-num">5</span> PyTorch DQN 1,000-Episode Convergence &amp; Multi-Factor ANOVA (Table II)</h2>
            <span class="badge badge-gold">Statistical Inference</span>
          </div>
          <div class="card-body">
            <div class="split-row">
              <div class="fig-box">
                <img src="{dqn_b64}" alt="DQN Convergence Curve">
                <div class="fig-caption">Fig. 3. 1,000-episode PyTorch DQN reward trajectory on Internet2 (N = 20, k = 3), stabilizing within 20 episodes.</div>
              </div>
              <div style="display:flex; flex-direction:column; justify-content:space-between; gap:2mm;">
                <div class="table-box">
                  <table>
                    <thead>
                      <tr>
                        <th>ANOVA Source (<em>N</em><sub>obs</sub>=300)</th>
                        <th><em>SS</em></th>
                        <th><em>df</em></th>
                        <th><em>MS</em></th>
                        <th><em>F</em>-Stat</th>
                        <th><em>p</em>-Value</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr class="win-row">
                        <td><strong>Algorithm Family (5)</strong></td>
                        <td>389.92</td>
                        <td>4</td>
                        <td>97.48</td>
                        <td><strong>118.90</strong></td>
                        <td><strong>&lt; 0.0001</strong></td>
                      </tr>
                      <tr>
                        <td><strong>Topology Family (2)</strong></td>
                        <td>204.31</td>
                        <td>1</td>
                        <td>204.31</td>
                        <td>249.21</td>
                        <td>&lt; 0.0001</td>
                      </tr>
                      <tr>
                        <td><strong>Node Scale <em>N</em> (2)</strong></td>
                        <td>412.08</td>
                        <td>1</td>
                        <td>412.08</td>
                        <td>502.64</td>
                        <td>&lt; 0.0001</td>
                      </tr>
                      <tr>
                        <td><strong>Budget <em>k</em> (3)</strong></td>
                        <td>188.45</td>
                        <td>2</td>
                        <td>94.23</td>
                        <td>114.93</td>
                        <td>&lt; 0.0001</td>
                      </tr>
                      <tr>
                        <td><strong>Within-Cell Error</strong></td>
                        <td>196.77</td>
                        <td>240</td>
                        <td>0.82</td>
                        <td>—</td>
                        <td>—</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div class="callout gold">
                  <strong>Convergence &amp; Post-Hoc Contrasts:</strong> DQN stabilizes at rolling mean reward <strong>13.199</strong> (grand mean 13.055 ± 0.589, peak 14.607, <em>L</em>(<em>C</em>) = 1.420 ms) but requires <strong><em>ω</em><sub>train</sub> = 21.26 s</strong> (11.40 s cached). Tukey HSD confirms GA &amp; <em>K</em>-Means beat Random (<em>p</em> &lt; 0.001, Cohen's <em>d</em> = 1.42), while DQN vs. <em>K</em>-Means is statistically indistinguishable (<em>t</em>(8) = 0.42, <em>p</em> = 0.68).
                </div>
              </div>
            </div>
          </div>
        </div>

      </section>

      <!-- ================= COLUMN 3 ================= -->
      <section class="col">

        <!-- 6. Five-Way Mininet OpenFlow Emulation Table -->
        <div class="card" style="flex: 1.05;">
          <div class="card-header">
            <h2 class="card-title"><span class="sec-num">6</span> 5-Way Mininet OpenFlow Emulation (Table III)</h2>
            <span class="badge badge-green">Internet2 (N=20, k=3)</span>
          </div>
          <div class="card-body">
            <p>
              All 5 placement vectors were instantiated in <strong>Mininet 2.3+ / Open vSwitch (OVS)</strong> with <code>tc netem</code> geodesic edge-weighted links (2.0× round-trip + ±0.5 ms jitter):
            </p>
            <div class="table-box">
              <table>
                <thead>
                  <tr>
                    <th>Placement Strategy</th>
                    <th>Selected Nodes</th>
                    <th>Mean RTT</th>
                    <th>Max Tail RTT</th>
                    <th>Graph <em>L</em>(<em>C</em>)</th>
                    <th>OVS Δ</th>
                    <th><em>Reach</em><sub>avg</sub></th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="win-row">
                    <td><strong>Genetic Algorithm</strong> <span class="badge-win">BEST MEAN</span></td>
                    <td><code>[n1,n15,n16]</code></td>
                    <td><strong>2.718 ms</strong></td>
                    <td>6.903 ms</td>
                    <td>1.403 ms</td>
                    <td>+1.315 ms</td>
                    <td>100.0%</td>
                  </tr>
                  <tr class="subwin-row">
                    <td><strong>K-Means Clustering</strong> <span class="badge-tail">BEST TAIL</span></td>
                    <td><code>[n1,n16,n9]</code></td>
                    <td><strong>2.852 ms</strong></td>
                    <td><strong>5.764 ms</strong></td>
                    <td>1.469 ms</td>
                    <td>+1.383 ms</td>
                    <td>100.0%</td>
                  </tr>
                  <tr>
                    <td><strong>Greedy K-Center</strong></td>
                    <td><code>[n1,n10,n6]</code></td>
                    <td>2.934 ms</td>
                    <td>6.664 ms</td>
                    <td>1.511 ms</td>
                    <td>+1.423 ms</td>
                    <td>100.0%</td>
                  </tr>
                  <tr>
                    <td><strong>Bandit RL / PyTorch DQN</strong></td>
                    <td><code>[n1,n10,n5]</code></td>
                    <td>3.056 ms</td>
                    <td>6.718 ms</td>
                    <td>1.564 ms</td>
                    <td>+1.492 ms</td>
                    <td>100.0%</td>
                  </tr>
                  <tr>
                    <td><strong>Random Baseline</strong></td>
                    <td><code>[n13,n0,n18]</code></td>
                    <td>3.374 ms</td>
                    <td>6.944 ms</td>
                    <td>1.734 ms</td>
                    <td>+1.640 ms</td>
                    <td>100.0%</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="callout green">
              <strong>Kernel Switching Validation:</strong> Linux/OVS adds a consistent <strong>+1.315 ms to +1.640 ms</strong> control-channel overhead, preserving exact ordinal rankings (<strong>GA &lt; K-Means &lt; Greedy &lt; DRL &lt; Random</strong>) and confirming GA (−19.4% RTT) and <em>K</em>-Means (−15.5% RTT; 5.764 ms worst-case tail) outperform DRL (3.056 ms).
            </div>
          </div>
        </div>

        <!-- 7. Dynamic Link Churn Break-Even & Bounded Decision Framework -->
        <div class="card" style="flex: 1.38;">
          <div class="card-header">
            <h2 class="card-title"><span class="sec-num">7</span> Dynamic Link-Churn Amortization &amp; Decision Guide</h2>
            <span class="badge badge-purple">1,000-State Churn &amp; Guide</span>
          </div>
          <div class="card-body">
            <div class="table-box">
              <table>
                <thead>
                  <tr>
                    <th>Topology (100 Epochs × 5 Seeds)</th>
                    <th>Algorithm</th>
                    <th>Post-Churn <em>L</em></th>
                    <th>Online <em>τ</em> / Ep</th>
                    <th>Pre-Train <em>ω</em><sub>train</sub></th>
                    <th>DQN Break-Even <em>T</em>*</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>Internet2</strong> (<em>N</em>=20, <em>k</em>=3)</td>
                    <td>Online GA (24×25)</td>
                    <td><strong>1.450 ms</strong></td>
                    <td>13.20 ms</td>
                    <td>0.0 ms</td>
                    <td><strong>59.0 Ep.</strong> (42–101)</td>
                  </tr>
                  <tr>
                    <td><strong>Internet2</strong> (<em>N</em>=20, <em>k</em>=3)</td>
                    <td>Spatial <em>K</em>-Means</td>
                    <td>1.528 ms</td>
                    <td>4.47 ms</td>
                    <td>0.0 ms</td>
                    <td><strong>207.6 Ep.</strong> (110–411)</td>
                  </tr>
                  <tr class="subwin-row">
                    <td><strong>Internet2</strong> (<em>N</em>=20, <em>k</em>=3)</td>
                    <td><strong>Pre-Trained DQN</strong></td>
                    <td>2.287 ms</td>
                    <td><strong>0.0257 ms</strong></td>
                    <td>772.8 ms</td>
                    <td><em>Amortized &gt; T*</em></td>
                  </tr>
                  <tr>
                    <td><strong>ATT-MPLS</strong> (<em>N</em>=21, <em>k</em>=3)</td>
                    <td>Online GA (24×25)</td>
                    <td><strong>2.317 ms</strong></td>
                    <td>14.12 ms</td>
                    <td>0.0 ms</td>
                    <td><strong>65.2 Ep.</strong> (44–84)</td>
                  </tr>
                  <tr>
                    <td><strong>ATT-MPLS</strong> (<em>N</em>=21, <em>k</em>=3)</td>
                    <td>Spatial <em>K</em>-Means</td>
                    <td>2.904 ms</td>
                    <td>5.27 ms</td>
                    <td>0.0 ms</td>
                    <td><strong>145.8 Ep.</strong> (112–212)</td>
                  </tr>
                  <tr class="subwin-row">
                    <td><strong>ATT-MPLS</strong> (<em>N</em>=21, <em>k</em>=3)</td>
                    <td><strong>Pre-Trained DQN</strong></td>
                    <td>2.931 ms</td>
                    <td><strong>0.0213 ms</strong></td>
                    <td>921.7 ms</td>
                    <td><em>Amortized &gt; T*</em></td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="split-row" style="grid-template-columns: 0.88fr 1.12fr;">
              <div class="fig-box">
                <img src="{decision_b64}" alt="Bounded Decision Flowchart">
                <div class="fig-caption">Fig. 4. Bounded Deployment Flowchart (N ≤ 50).</div>
              </div>
              <div class="decision-grid">
                <div class="dec-card classical">
                  <div class="dec-header"><span>1. Planar Mesh (N≤50)</span> <span>τ=3.2–5.3ms</span></div>
                  <p><strong>Deploy Spatial K-Means:</strong> Zero training, best worst-case Mininet tail RTT (5.764 ms).</p>
                </div>
                <div class="dec-card classical">
                  <div class="dec-header"><span>2. Scale-Free Core</span> <span>τ=0.03–0.21ms</span></div>
                  <p><strong>Deploy Greedy K-Center:</strong> Captures BA hub nodes in sub-ms; 100% Pareto frontier.</p>
                </div>
                <div class="dec-card ga">
                  <div class="dec-header"><span>3. Offline Planning</span> <span>τ=12.9–76.1ms</span></div>
                  <p><strong>Deploy Genetic Alg. (GA):</strong> Lowest latency in 12/12 cells &amp; best mean RTT (2.718 ms).</p>
                </div>
                <div class="dec-card drl">
                  <div class="dec-header"><span>4. High-Churn WANs</span> <span>T* &gt; 59–208 Ep</span></div>
                  <p><strong>Deploy Pre-Trained DQN:</strong> Fast forward pass (0.021–0.026 ms/ep) amortizes ω_train.</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 8. Conclusions & Future Work -->
        <div class="card grow" style="flex: 0.72;">
          <div class="card-header">
            <h2 class="card-title"><span class="sec-num">8</span> Conclusions &amp; Future Research Directions</h2>
            <span class="badge badge-gold">Key Takeaways</span>
          </div>
          <div class="card-body">
            <p>
              • <strong>Static WAN Decision Efficiency (<em>N</em> ≤ 50):</strong> GA (2.718 ms RTT), <em>K</em>-Means (2.852 ms RTT), and Greedy <em>K</em>-Center (2.934 ms RTT) outperform DRL (3.056 ms RTT) without incurring the 21.26 s offline neural training tax.
            </p>
            <p>
              • <strong>Dynamic Churn Amortization Boundary:</strong> Pre-trained PyTorch DQN inference (0.021–0.026 ms/epoch) amortizes <em>ω</em><sub>train</sub> after <strong><em>T</em>* = 59.0–65.2 epochs</strong> vs. GA and <strong>145.8–207.6 epochs</strong> vs. <em>K</em>-Means, though classical heuristics retain lower post-churn latency.
            </p>
            <p>
              • <strong>Future Directions:</strong> (1) Live Mininet NetFlow switch-migration traces; (2) <strong>Graph Neural Networks (GNNs)</strong> for topology-agnostic zero-shot generalization (<em>N</em> ∈ [100, 500]); (3) Multi-link (<em>N</em>−<em>k</em>) failures &amp; ONOS/Ryu Raft east-west synchronization.
            </p>
          </div>
        </div>

      </section>

    </main>

    <!-- ================= FOOTER ================= -->
    <footer class="footer">
      <div>
        <strong>Department of Computer Science</strong> • Faculty of Science, Agriculture and Engineering (FSAE), University of Zululand
      </div>
      <div>
        <strong>Key References (2021–2026):</strong> [1] Ali et al. (2025) <em>IEEE IoT-J</em> • [4] Mohanty et al. (2021) <em>IEEE OCIT</em> • [6] Yusuf et al. (2023) <em>PeerJ CS</em> • [8] Xiao &amp; Chen (2021) <em>ICITBE</em> • [10] Radam et al. (2022) <em>Computers</em> • [12] Benoudifa et al. (2023) <em>JKSUCI</em> • [15] Farahi et al. (2026) <em>Results Eng.</em>
      </div>
      <div>
        <strong>UNIZULU Honours &amp; SATNAC 2026</strong>
      </div>
    </footer>

  </div>

</body>
</html>
"""

html_path = os.path.join(POSTER_DIR, "index.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✓ Successfully updated poster HTML: {html_path}")

# Render PDF
pdf_out = os.path.join(POSTER_DIR, "POSTER_Thabang_Mhlokoma_UNIZULU_2026.pdf")
png_out = os.path.join(POSTER_DIR, "POSTER_Thabang_Mhlokoma_UNIZULU_2026.png")

cmd_pdf = [
    "google-chrome",
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--print-to-pdf=" + pdf_out,
    "--print-to-pdf-no-header",
    "--paper-width=46.81",
    "--paper-height=33.11",
    "file://" + html_path,
]

print("Rendering PDF...")
if shutil.which("google-chrome"):
    res_pdf = subprocess.run(cmd_pdf, capture_output=True, text=True, timeout=40)
    if res_pdf.returncode == 0:
        print(f"✓ Generated PDF: {pdf_out} ({os.path.getsize(pdf_out)} bytes)")
    else:
        print(f"Error rendering PDF: {res_pdf.stderr}")

    # Render PNG via pdftoppm
    print("Rendering PNG via pdftoppm...")
    tmp_page = os.path.join(POSTER_DIR, "poster_page")
    cmd_png = ["pdftoppm", "-png", "-r", "150", pdf_out, tmp_page]
    subprocess.run(cmd_png, capture_output=True, text=True, timeout=40)

    gen_png = tmp_page + "-1.png"
    if os.path.exists(gen_png):
        os.rename(gen_png, png_out)
        print(f"✓ Generated PNG: {png_out} ({os.path.getsize(png_out)} bytes)")

    # Also copy to Buthelezi-named poster files in poster/ and dissertation/
    for extra_pdf in [
        os.path.join(POSTER_DIR, "POSTER_Thabang_Buthelezi_UNIZULU_2026.pdf"),
        os.path.join(DISS_DIR, "Honours_Research_Poster_Thabang_Buthelezi.pdf"),
    ]:
        shutil.copy2(pdf_out, extra_pdf)
        print(f"✓ Synced PDF copy: {extra_pdf}")

    for extra_png in [
        os.path.join(POSTER_DIR, "POSTER_Thabang_Buthelezi_UNIZULU_2026.png"),
        os.path.join(DISS_DIR, "Honours_Research_Poster_Thabang_Buthelezi.png"),
    ]:
        if os.path.exists(png_out):
            shutil.copy2(png_out, extra_png)
            print(f"✓ Synced PNG copy: {extra_png}")
else:
    print("Note: google-chrome is outside sandbox; run render_poster.py to render PDF/PNG.")

print("Poster generation complete!")
