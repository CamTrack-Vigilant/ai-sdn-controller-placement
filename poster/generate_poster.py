#!/usr/bin/env python3
"""
Generate an ultra-high-definition, print-ready, self-contained academic poster for the UNIZULU Postgraduate Symposium.
"""
import os
import base64
import subprocess

WORKSPACE = "/home/pro/Desktop/ai-sdn-controller-placement"
POSTER_DIR = os.path.join(WORKSPACE, "poster")

def img_to_b64(path):
    full_path = os.path.join(WORKSPACE, path)
    if os.path.exists(full_path):
        with open(full_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            ext = os.path.splitext(path)[1].lower().replace(".", "")
            if ext == "jpg": ext = "jpeg"
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
  <title>UNIZULU Postgraduate Symposium Poster - Thabang Mhlokoma</title>
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
      --bg-light: #f4f6f9;
      --card-bg: #ffffff;
      --card-border: #cbd5e1;
      --text-main: #0f172a;
      --text-muted: #334155;
      --text-light: #64748b;
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
      padding: 10mm 15mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 7mm;
    }}

    /* ================= HEADER ================= */
    .header {{
      background: linear-gradient(135deg, #05162e 0%, #0b2545 45%, #13315c 100%);
      border-radius: 18px;
      padding: 8mm 16mm;
      color: #ffffff;
      display: grid;
      grid-template-columns: 215mm 1fr 210mm;
      align-items: center;
      gap: 12mm;
      border-bottom: 5mm solid var(--unizulu-accent);
      box-shadow: 0 12px 30px rgba(11, 37, 69, 0.2);
    }}

    .logo-container {{
      background: #ffffff;
      padding: 3.5mm 6mm;
      border-radius: 12px;
      display: flex;
      align-items: center;
      gap: 5mm;
      box-shadow: 0 6px 15px rgba(0,0,0,0.15);
    }}

    .logo-container img {{
      height: 23mm;
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
      font-size: 15.5pt;
      font-weight: 800;
      color: #0b2545;
      letter-spacing: 0.5px;
      line-height: 1.15;
    }}

    .logo-text-sub {{
      font-size: 9.8pt;
      font-weight: 700;
      color: #92400e;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-top: 1mm;
    }}

    .title-container {{
      text-align: center;
    }}

    .symposium-pill {{
      display: inline-block;
      background: rgba(224, 169, 38, 0.25);
      border: 1.5px solid var(--unizulu-accent);
      color: #ffd166;
      font-size: 14.5pt;
      font-weight: 800;
      padding: 2mm 12mm;
      border-radius: 50px;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      margin-bottom: 3mm;
    }}

    .poster-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 31pt;
      font-weight: 800;
      line-height: 1.18;
      color: #ffffff;
      margin-bottom: 3mm;
      letter-spacing: -0.3px;
    }}

    .poster-meta {{
      font-size: 17.5pt;
      color: #e2e8f0;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 6mm;
    }}

    .author-highlight {{
      color: #ffffff;
      font-weight: 700;
    }}

    .supervisor-highlight {{
      color: #ffd166;
      font-weight: 700;
    }}

    .header-right {{
      text-align: right;
      border-left: 2px solid rgba(255,255,255,0.25);
      padding-left: 8mm;
    }}

    .dept-title {{
      font-size: 16.5pt;
      font-weight: 800;
      color: #ffffff;
    }}

    .faculty-title {{
      font-size: 14pt;
      color: #cbd5e1;
      margin-top: 1.5mm;
    }}

    .theme-tag {{
      font-size: 11.5pt;
      color: var(--unizulu-accent);
      font-style: italic;
      margin-top: 2mm;
      line-height: 1.25;
    }}

    /* ================= 3-COLUMN MAIN GRID ================= */
    .grid-content {{
      display: grid;
      grid-template-columns: 1fr 1.2fr 1fr;
      gap: 8mm;
      flex: 1;
      min-height: 0;
    }}

    .col {{
      display: flex;
      flex-direction: column;
      gap: 6mm;
      height: 100%;
    }}

    /* ================= CARDS ================= */
    .card {{
      background: var(--card-bg);
      border-radius: 14px;
      padding: 5.5mm 7.5mm;
      border: 1.5px solid var(--card-border);
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
      display: flex;
      flex-direction: column;
    }}

    .card.grow {{
      flex: 1;
    }}

    .card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 3px solid var(--unizulu-blue);
      padding-bottom: 2.5mm;
      margin-bottom: 3.5mm;
    }}

    .card-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 18pt;
      font-weight: 800;
      color: var(--unizulu-blue);
      display: flex;
      align-items: center;
      gap: 3mm;
    }}

    .sec-num {{
      background: var(--unizulu-blue);
      color: #ffffff;
      width: 7.5mm;
      height: 7.5mm;
      border-radius: 50%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 12.5pt;
      font-weight: 800;
    }}

    .badge {{
      font-size: 10.5pt;
      font-weight: 700;
      padding: 1.2mm 4.5mm;
      border-radius: 20px;
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }}

    .badge-blue {{ background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }}
    .badge-gold {{ background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }}
    .badge-green {{ background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }}

    .card-body {{
      font-size: 12.8pt;
      line-height: 1.42;
      color: var(--text-muted);
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 2.8mm;
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
      border-left: 3.5mm solid var(--unizulu-navy);
      padding: 2.5mm 4.5mm;
      border-radius: 0 8px 8px 0;
      font-size: 12.2pt;
    }}

    .callout.gold {{
      background: #fffdf5;
      border-left-color: var(--unizulu-accent);
    }}

    .callout.green {{
      background: #f0fdf4;
      border-left-color: var(--tech-green);
    }}

    /* Research Questions */
    .rq-box {{
      background: #f1f5f9;
      border-left: 3.5mm solid var(--tech-cyan);
      border-radius: 6px;
      padding: 2.2mm 3.8mm;
      font-size: 12.2pt;
      line-height: 1.35;
    }}

    .rq-box strong {{
      color: var(--unizulu-navy);
      font-size: 12.6pt;
    }}

    /* Paradigms 2x2 Grid */
    .paradigm-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2.5mm;
    }}

    .paradigm-card {{
      background: #f8fafc;
      border: 1.2px solid #e2e8f0;
      border-radius: 8px;
      padding: 2.2mm 3.2mm;
    }}

    .paradigm-title {{
      font-size: 12.2pt;
      font-weight: 700;
      color: var(--unizulu-blue);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .complexity-tag {{
      font-family: 'Fira Code', monospace;
      font-size: 10.5pt;
      font-weight: 600;
      color: var(--text-light);
    }}

    .paradigm-desc {{
      font-size: 10.5pt;
      color: var(--text-muted);
      margin-top: 1mm;
      line-height: 1.25;
    }}

    /* Visual Figures */
    .fig-box {{
      background: #ffffff;
      border: 1.5px solid #e2e8f0;
      border-radius: 10px;
      padding: 2mm;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      flex: 1;
    }}

    .fig-box img {{
      max-width: 100%;
      height: auto;
      max-height: 100%;
      border-radius: 6px;
      object-fit: contain;
    }}

    .fig-caption {{
      font-size: 10.5pt;
      color: var(--text-light);
      font-style: italic;
      margin-top: 1.5mm;
      line-height: 1.2;
    }}

    /* Stat Cards Row */
    .stat-banner {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 2.5mm;
    }}

    .metric-pill {{
      background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
      border: 2px solid #e2e8f0;
      border-radius: 10px;
      padding: 2.5mm 1.5mm;
      text-align: center;
      box-shadow: 0 3px 8px rgba(0,0,0,0.03);
    }}

    .metric-pill.gold {{
      background: linear-gradient(135deg, #fffdf5 0%, #fef9e7 100%);
      border-color: #fde68a;
    }}

    .metric-val {{
      font-family: 'Outfit', sans-serif;
      font-size: 21pt;
      font-weight: 900;
      color: var(--unizulu-navy);
      line-height: 1.1;
    }}

    .metric-val.gold {{ color: #b45309; }}
    .metric-val.blue {{ color: #0284c7; }}
    .metric-val.green {{ color: #15803d; }}

    .metric-lbl {{
      font-size: 9.2pt;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--text-light);
      margin-top: 1mm;
      letter-spacing: 0.4px;
    }}

    /* Custom Data Table */
    .table-box {{
      border: 1.2px solid #cbd5e1;
      border-radius: 8px;
      overflow: hidden;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 11pt;
    }}

    th {{
      background: var(--unizulu-navy);
      color: #ffffff;
      padding: 2mm 3mm;
      font-weight: 700;
      text-align: left;
      font-size: 10.8pt;
      text-transform: uppercase;
      letter-spacing: 0.4px;
    }}

    td {{
      padding: 1.8mm 3mm;
      border-bottom: 1px solid #e2e8f0;
      color: var(--text-muted);
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

    .badge-win {{
      background: #16a34a;
      color: #ffffff;
      font-size: 8.5pt;
      font-weight: 800;
      padding: 0.4mm 2.2mm;
      border-radius: 4px;
      margin-left: 1.5mm;
    }}

    /* Decision Split */
    .decision-split {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2.5mm;
    }}

    .dec-card {{
      padding: 2.5mm 3.5mm;
      border-radius: 8px;
      font-size: 11pt;
      line-height: 1.32;
    }}

    .dec-card.classical {{
      background: #f0fdf4;
      border: 1.5px solid #86efac;
    }}

    .dec-card.drl {{
      background: #eff6ff;
      border: 1.5px solid #93c5fd;
    }}

    .dec-header {{
      font-size: 12pt;
      font-weight: 800;
      margin-bottom: 1mm;
      display: flex;
      align-items: center;
      gap: 1.5mm;
    }}

    .dec-card.classical .dec-header {{ color: #15803d; }}
    .dec-card.drl .dec-header {{ color: #1d4ed8; }}

    /* ================= FOOTER ================= */
    .footer {{
      background: #ffffff;
      border-radius: 12px;
      padding: 2.5mm 10mm;
      border: 1.5px solid var(--card-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 10.5pt;
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
        <div class="symposium-pill">2026 Postgraduate Symposium • Digital Innovation Track</div>
        <h1 class="poster-title">Decision-Grade Multi-Objective Benchmarking and Emulation of Controller Placement in Software-Defined Networks</h1>
        <div class="poster-meta">
          <span>Principal Investigator: <strong class="author-highlight">Thabang Mhlokoma</strong> (Honours B.Sc. Computer Science)</span>
          <span>•</span>
          <span>Supervisor: <strong class="supervisor-highlight">Prof. Mudali</strong></span>
        </div>
      </div>

      <div class="header-right">
        <div class="dept-title">Department of Computer Science</div>
        <div class="faculty-title">Faculty of Science, Agriculture & Engineering</div>
        <div class="theme-tag">"Driving Sustainable Futures Through Interdisciplinary Research & Digital Innovation"</div>
      </div>
    </header>

    <!-- ================= 3-COLUMN MAIN GRID ================= -->
    <main class="grid-content">

      <!-- ================= COLUMN 1 ================= -->
      <section class="col">

        <!-- 1. Background & Problem -->
        <div class="card" style="flex: 0.85;">
          <div class="card-header">
            <h2 class="card-title"><span class="sec-num">1</span> Background & Motivation</h2>
            <span class="badge badge-blue">SDN Architecture</span>
          </div>
          <div class="card-body">
            <p>
              Software-Defined Networking (SDN) decouples control logic from physical forwarding hardware. In multi-site WANs, optimizing the <strong>Controller Placement Problem (CPP)</strong> is an <em>NP-hard</em> facility location challenge balancing propagation latency, fault tolerance, and computational cost.
            </p>
            <div class="callout gold">
              <strong>The Methodological Gap:</strong> Deep Reinforcement Learning (DRL) is frequently advocated for CPP. However, existing studies evaluate models on single-metric latency under isolated conditions, ignoring computational energy costs, training runtimes, and real-world OpenFlow validation.
            </div>
          </div>
        </div>

        <!-- 2. Research Questions -->
        <div class="card" style="flex: 0.95;">
          <div class="card-header">
            <h2 class="card-title"><span class="sec-num">2</span> Research Questions</h2>
            <span class="badge badge-gold">Objectives</span>
          </div>
          <div class="card-body">
            <div class="rq-box">
              <strong>RQ1 (Performance & Latency):</strong> How do DRL algorithms (PyTorch DQN) compare against classical heuristics (<em>K</em>-Means, Greedy <em>K</em>-Center) in minimizing propagation latency <em>L</em>(<em>P</em>) and maximizing <em>N</em>−1 reliability?
            </div>
            <div class="rq-box">
              <strong>RQ2 (Complexity Tax <em>ω</em>):</strong> What computational overhead (s/episode) is incurred by AI models across varying topology scales (<em>N</em> = 20, 50)?
            </div>
            <div class="rq-box">
              <strong>RQ3 (Hardware-in-the-Loop Emulation):</strong> Do algorithmic rankings translate to real OpenFlow control Round Trip Times (RTT) in Mininet?
            </div>
          </div>
        </div>

        <!-- 3. Placement Paradigms & Pipeline -->
        <div class="card grow" style="flex: 1.35;">
          <div class="card-header">
            <h2 class="card-title"><span class="sec-num">3</span> 5 Placement Paradigms & Pipeline</h2>
            <span class="badge badge-green">Methodology</span>
          </div>
          <div class="card-body">
            <div class="paradigm-grid">
              <div class="paradigm-card">
                <div class="paradigm-title"><span>1. Random Baseline</span> <span class="complexity-tag">O(1)</span></div>
                <div class="paradigm-desc">Stochastic uniform node selection baseline.</div>
              </div>
              <div class="paradigm-card">
                <div class="paradigm-title"><span>2. Greedy K-Center</span> <span class="complexity-tag" style="color:var(--tech-cyan)">O(k·N)</span></div>
                <div class="paradigm-desc">Gonzalez 2-approx minimax radius heuristic.</div>
              </div>
              <div class="paradigm-card">
                <div class="paradigm-title"><span>3. K-Means Medoids</span> <span class="complexity-tag" style="color:var(--tech-green)">O(I·k·N)</span></div>
                <div class="paradigm-desc">Graph geodesic shortest-path partitioning.</div>
              </div>
              <div class="paradigm-card">
                <div class="paradigm-title"><span>4. Genetic Algorithm</span> <span class="complexity-tag" style="color:var(--tech-purple)">O(G·P)</span></div>
                <div class="paradigm-desc">Combinatorial evolutionary crossover search.</div>
              </div>
            </div>

            <div class="paradigm-card" style="border-left: 3.5mm solid #f59e0b;">
              <div class="paradigm-title"><span>5. PyTorch Deep Q-Network (DQN)</span> <span class="complexity-tag" style="color:#d97706">DRL Model</span></div>
              <div class="paradigm-desc">Adaptive neural placement (64×64 MLP), <em>γ</em> = 0.99, <em>α</em> = 0.001, replay buffer 10⁴, <em>ε</em>-greedy decay.</div>
            </div>

            <div class="fig-box">
              <img src="{workflow_b64}" alt="Research Methodology Workflow">
              <div class="fig-caption">Fig. 1. End-to-end multi-objective benchmark and Mininet OpenFlow emulation pipeline.</div>
            </div>
          </div>
        </div>

      </section>

      <!-- ================= COLUMN 2 ================= -->
      <section class="col">

        <!-- Stat Banner -->
        <div class="stat-banner">
          <div class="metric-pill gold">
            <div class="metric-val gold">2.852 ms</div>
            <div class="metric-lbl">Mininet RTT (K-Means)</div>
          </div>
          <div class="metric-pill">
            <div class="metric-val blue">&lt; 5 ms</div>
            <div class="metric-lbl">Heuristic Compute</div>
          </div>
          <div class="metric-pill">
            <div class="metric-val green">100 %</div>
            <div class="metric-lbl">N−1 Link Reliability</div>
          </div>
          <div class="metric-pill">
            <div class="metric-val">20 Ep.</div>
            <div class="metric-lbl">DQN Convergence</div>
          </div>
        </div>

        <!-- 4. 3D Pareto Frontier -->
        <div class="card grow" style="flex: 1.55;">
          <div class="card-header">
            <h2 class="card-title"><span class="sec-num">4</span> 3-Axis Multi-Objective Pareto Space</h2>
            <span class="badge badge-blue">Trade-Off Analysis</span>
          </div>
          <div class="card-body">
            <div class="fig-box">
              <img src="{pareto_b64}" alt="3D Pareto Optimization Frontier">
              <div class="fig-caption">Fig. 2. Joint 3-Axis Pareto space: Latency <em>L</em>(<em>P</em>) (ms) vs <em>N</em>−1 Reliability <em>Reach</em><sub>avg</sub> (%) vs Compute Time <em>ω</em> (s).</div>
            </div>
            <p>
              The non-dominated Pareto frontier proves that <strong>K-Means Clustering</strong> and <strong>Greedy K-Center</strong> achieve the optimal trade-off boundary—delivering minimal latency with near-zero compute overhead (<em>ω</em> &lt; 0.005 s).
            </p>
          </div>
        </div>

        <!-- 5. DQN Convergence Dynamics -->
        <div class="card grow" style="flex: 1.45;">
          <div class="card-header">
            <h2 class="card-title"><span class="sec-num">5</span> DQN Training & Policy Dynamics</h2>
            <span class="badge badge-gold">1,000 Episodes</span>
          </div>
          <div class="card-body">
            <div class="fig-box">
              <img src="{dqn_b64}" alt="DQN Convergence Curve">
              <div class="fig-caption">Fig. 3. 1,000-episode DQN reward trajectory on Internet2 (<em>N</em> = 34, <em>k</em> = 3), converging within 20 episodes.</div>
            </div>
            <p>
              DQN converged rapidly to a mean reward of <strong>13.199</strong> (total runtime: 21.26 s, <em>ω</em> = 0.0213 s/episode). However, it incurs a <strong>4,000× computational tax</strong> over heuristic clustering without achieving lower propagation latency.
            </p>
          </div>
        </div>

      </section>

      <!-- ================= COLUMN 3 ================= -->
      <section class="col">

        <!-- 6. Mininet OpenFlow Emulation Table -->
        <div class="card" style="flex: 1.25;">
          <div class="card-header">
            <h2 class="card-title"><span class="sec-num">6</span> Mininet OpenFlow Emulation</h2>
            <span class="badge badge-green">Emulated Validation</span>
          </div>
          <div class="card-body">
            <p>
              Hardware-in-the-loop control RTT was measured in real-time across virtual Open vSwitch networks on Internet2 WAN (<em>N</em> = 34, <em>k</em> = 3):
            </p>
            <div class="table-box">
              <table>
                <thead>
                  <tr>
                    <th>Algorithm Paradigm</th>
                    <th>Control RTT</th>
                    <th>Compute <em>ω</em></th>
                    <th><em>N</em>−1 Rel.</th>
                    <th>Pareto Rank</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="win-row">
                    <td><strong>K-Means Clustering</strong> <span class="badge-win">TOP</span></td>
                    <td><strong>2.852 ms</strong></td>
                    <td><strong>0.003 s</strong></td>
                    <td><strong>100%</strong></td>
                    <td><strong>Rank 1</strong></td>
                  </tr>
                  <tr>
                    <td><strong>Greedy K-Center</strong></td>
                    <td>3.104 ms</td>
                    <td>0.002 s</td>
                    <td>100%</td>
                    <td>Rank 2</td>
                  </tr>
                  <tr>
                    <td><strong>PyTorch DQN</strong></td>
                    <td>2.914 ms</td>
                    <td>21.26 s</td>
                    <td>100%</td>
                    <td>Rank 3</td>
                  </tr>
                  <tr>
                    <td><strong>Genetic Algorithm (GA)</strong></td>
                    <td>3.180 ms</td>
                    <td>0.450 s</td>
                    <td>100%</td>
                    <td>Rank 4</td>
                  </tr>
                  <tr>
                    <td><strong>Random Baseline</strong></td>
                    <td>4.820 ms</td>
                    <td>0.0001 s</td>
                    <td>85.2%</td>
                    <td>Rank 5</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="callout green">
              <strong>Statistical Significance:</strong> Factorial ANOVA confirms significant algorithmic effect (<em>F</em>(4, 55) = 89.4, <em>p</em> &lt; 0.001). Post-hoc Tukey HSD proves K-Means significantly outperforms GA and Random baselines.
            </div>
          </div>
        </div>

        <!-- 7. Decision Framework -->
        <div class="card" style="flex: 0.95;">
          <div class="card-header">
            <h2 class="card-title"><span class="sec-num">7</span> Sustainable Decision Framework</h2>
            <span class="badge badge-blue">Operator Guide</span>
          </div>
          <div class="card-body">
            <div class="decision-split">
              <div class="dec-card classical">
                <div class="dec-header">✓ Static WANs (N ≤ 50)</div>
                <p><strong>Deploy K-Means / Greedy K-Center:</strong> Sub-5ms compute overhead, zero GPU requirement, minimal energy consumption, and provable latency bounds.</p>
              </div>
              <div class="dec-card drl">
                <div class="dec-header">⚡ Dynamic / Volatile WANs</div>
                <p><strong>Deploy PyTorch DRL / DQN:</strong> Strictly justified when facing real-time topology churn, high-frequency link degradation, or multi-tenant traffic shifts.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 8. Conclusions & Recommendations -->
        <div class="card grow" style="flex: 1.05;">
          <div class="card-header">
            <h2 class="card-title"><span class="sec-num">8</span> Conclusions & Recommendations</h2>
            <span class="badge badge-gold">Key Takeaways</span>
          </div>
          <div class="card-body">
            <p>
              • <strong>Decision Efficiency:</strong> For static WANs, classical clustering delivers optimal decision quality without neural training overhead.
            </p>
            <p>
              • <strong>Sustainable Digital Innovation:</strong> Eliminating unnecessary AI compute aligns directly with green networking paradigms by avoiding computational complexity taxes.
            </p>
            <p>
              • <strong>Practical Recommendation:</strong> Adopt a tiered placement architecture—use deterministic heuristics as the primary operational backbone, triggering DRL adaptation only during severe network churn.
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
        <strong>Key References:</strong> [1] Heller et al. (2012) <em>CCR</em> • [2] Gonzalez (1985) <em>TCS</em> • [7] Farahi et al. (2026) <em>IEEE TNSM</em>
      </div>
      <div>
        <strong>Symposium 2026</strong>
      </div>
    </footer>

  </div>

</body>
</html>
"""

with open(os.path.join(POSTER_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✓ Successfully updated poster HTML: {os.path.join(POSTER_DIR, 'index.html')}")

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
    "file://" + os.path.join(POSTER_DIR, "index.html")
]

print("Rendering PDF...")
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

print("Poster generation complete!")
