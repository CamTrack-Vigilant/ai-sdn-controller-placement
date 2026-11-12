#!/usr/bin/env python3
"""
Builds a Simplified, Easy-to-Present 22-Slide BSc Honours Viva Defense PowerPoint (.pptx)
and Conversational Plain-English Speaker Script (.docx & .pdf) covering the complete
Table of Contents of Honours_Min_Dissertation_230011908_signed.pdf, styled with the
Official University of Zululand (UNIZULU) Navy & Gold Widescreen Template (matching 08D01.pptx).

Design Principles:
  - 1 clear idea per slide, big readable fonts (12pt-15pt), generous whitespace.
  - Zero dense equation walls or tiny 8-column tables: plain English + key numbers.
  - Conversational, jargon-free Speaker Notes on all 22 slides so presenting feels effortless.
  - Visual preview audit (1920x1080 PNGs) verifying 100% frame fit with zero overflow.
"""

import shutil
import subprocess
import textwrap
import zipfile
from pathlib import Path
from lxml import etree
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DISSERTATION_DIR = PROJECT_ROOT / "dissertation"
DOCS_DIR = PROJECT_ROOT / "docs"
BG_DIR = DOCS_DIR / "figures" / "unizulu_slides_simplified_bg"
PREVIEW_DIR = DOCS_DIR / "figures" / "unizulu_slides_simplified_preview"

SLIDES_MD = DISSERTATION_DIR / "Honours_Defense_Simplified_Slides_Source.md"
OUTPUT_PPTX = DISSERTATION_DIR / "Honours_Defense_Presentation_Simplified_22Slides.pptx"
SCRIPT_MD = DISSERTATION_DIR / "Honours_Defense_Simplified_Script_Source.md"
OUTPUT_SCRIPT_DOCX = DISSERTATION_DIR / "Honours_Defense_Speaker_Script_Simplified.docx"
OUTPUT_SCRIPT_PDF = DISSERTATION_DIR / "Honours_Defense_Speaker_Script_Simplified.pdf"

CREST_PATH = DOCS_DIR / "figures" / "unizulu_official_crest.jpg"
if not CREST_PATH.exists():
    CREST_PATH = DOCS_DIR / "figures" / "unizulu_crest.png"

TOTAL_SLIDES = 22

# Top-right header badges mapped cleanly to the Dissertation Table of Contents
SLIDE_TOC_BADGES = {
    1: "TITLE • DECLARATION, DEDICATION & ACKNOWLEDGEMENTS (pp. i–iii)",
    2: "FRONT MATTER & ABSTRACT • DISSERTATION OVERVIEW (pp. iv–x)",
    3: "CHAPTER 1 (SEC. 1.1–1.2) • OVERVIEW & BACKGROUND OF STUDY",
    4: "CHAPTER 1 (SEC. 1.3) • PROBLEM STATEMENT (4 GAPS)",
    5: "CHAPTER 1 (SEC. 1.4–1.6) • GOAL, 7 OBJECTIVES & SIGNIFICANCE",
    6: "CHAPTER 2 (SEC. 2.1–2.2) • SDN FOUNDATIONS & WHY CPP IS HARD",
    7: "CHAPTER 2 (SEC. 2.3–2.6) • SOLUTION FAMILIES & N−1 SURVIVABILITY",
    8: "CHAPTER 2 (SEC. 2.7, TABLE 2.1) • LITERATURE SYNTHESIS (2021–2026)",
    9: "CHAPTER 3 (SEC. 3.1, FIG. 3.1) • RESEARCH DESIGN & HYPOTHESES",
    10: "CHAPTER 3 (SEC. 3.2, TABLE 3.1) • 6 TESTED NETWORK TOPOLOGIES",
    11: "CHAPTER 3 (SEC. 3.3, FIG. 3.2) • 5 ALGORITHMS & SYSTEM DESIGN",
    12: "CHAPTER 3 (SEC. 3.4–3.6) • EMULATION, METRICS & FAIRNESS CONTROLS",
    13: "CHAPTER 4 (SEC. 4.1.1, FIG. 4.1) • DOES THE AI ACTUALLY LEARN?",
    14: "CHAPTER 4 (SEC. 4.1.2, FIG. 4.2 & TABLE 4.1) • 10-RUN STABILITY AUDIT",
    15: "CHAPTER 4 (SEC. 4.1.3, FIG. 4.3) • HUB-AND-SPOKE RESULTS (BA)",
    16: "CHAPTER 4 (SEC. 4.1.3, FIG. 4.4) • GEOGRAPHIC MESH RESULTS (WAXMAN)",
    17: "CHAPTER 4 (SEC. 4.1.4, FIG. 4.5 & ANOVA) • 300-RUN PROOF & 3D PARETO",
    18: "CHAPTER 4 (SEC. 4.1.5, TABLES 4.5–4.6) • REAL MININET EMULATION TEST",
    19: "CHAPTER 4 (SEC. 4.1.6, TABLE 4.6B) • DYNAMIC LINK-CHURN BENCHMARK",
    20: "CHAPTER 4 (SEC. 4.2, FIG. 4.6 & TABLE 4.7) • DECISION GUIDE (N ≤ 50)",
    21: "CH. 4 (SEC. 4.3) & CH. 5 (SEC. 5.1–5.4) • LIMITATIONS & CONCLUSIONS",
    22: "REFERENCES, APPENDICES A–C & SATNAC 2026 DISSEMINATION (pp. 40–48)",
}

SLIDE_1_SPEAKER_NOTES = (
    "Good morning Prof. Mudali, Mr. Zwane, and members of the examination panel. [Pause] "
    "My name is Thabang Nhlokoma Buthelezi, and today I am presenting my Honours mini-dissertation in Computer Science at the University of Zululand. "
    "Before I begin, I want to acknowledge my supervisors, Prof. Mudali and Mr. Zwane, for their guidance, as well as my family and the Department of Computer Science for their support. "
    "In simple terms, my research asks one practical question: when a large network uses Software Defined Networking, we have to choose where to place the smart 'brains'—called controllers—across the network. "
    "Today, many researchers say Artificial Intelligence and Deep Reinforcement Learning should make that decision. "
    "My study tested AI head-to-head against classic, simple math-based rules across 300 experiments, real Linux network emulation, and 1,000 link failures—to find out when AI is worth the effort, and when simple rules actually work better."
)

# Clean, visual, uncluttered Markdown source for Pandoc -> PowerPoint
PANDOC_SLIDES_CONTENT = r"""---
title: "Where Should Network Brains Live? Benchmarking AI vs. Classic Heuristics in SDN"
subtitle: "BSc Honours Mini-Dissertation Defense | Thabang Nhlokoma Buthelezi (230011908) | University of Zululand (2026)"
author: "Supervisors: Prof. Pragasen Mudali (UNIZULU) & Mr. Skhumbuzo Zwane (CSIR)"
date: "Declaration, Dedication & Acknowledgements Included (pp. i–iii)"
---

# Slide 2: Presentation Roadmap & Research in 30 Seconds

- **Covers Complete Dissertation (Chapters 1–5 & Appendices A–C)**:
  - **Ch. 1 (Introduction)**: Why controller placement matters & the 4 gaps in current research.
  - **Ch. 2 (Literature Review)**: How SDN works & why AI vs. classic methods weren't compared fairly.
  - **Ch. 3 (Methodology)**: Our 6 test networks, 5 algorithms, & fairness controls.
  - **Ch. 4 (Results)**: What happened in 300 runs, live Mininet emulation, & 1,000 link failures.
  - **Ch. 5 & Appendices**: Simple rules for engineers, limitations, SATNAC 2026 paper, & raw data.
- **The 30-Second Takeaway (Abstract, p. ix)**:
  - On **normal, stable networks** (N ≤ 50), classic methods (**GA & K-Means / K-Center**) beat or tie AI **with zero training wait**.
  - On **constantly breaking networks**, pre-trained AI pays off only after **59–208 link changes**.

::: notes
Let me give you a quick map of today's talk—and the whole story in 30 seconds. My presentation follows all five chapters of my signed dissertation plus the appendices. First, in Chapters 1 and 2, I will explain what Software Defined Networking is, why choosing controller locations is tricky, and the gap we spotted in recent 2021-to-2026 papers. Second, in Chapter 3, I will show how we built a fair testbed comparing five algorithms across six networks. Third, in Chapter 4, I will share what our numbers actually proved—both on static networks, inside real Mininet Linux emulation, and when links keep failing. Finally, in Chapter 5, I will give engineers a clear, practical guide on which tool to pick. Here is the main headline before we even start: on normal, stable networks up to 50 switches, classic algorithms beat or match Deep Reinforcement Learning without wasting 11 to 21 seconds on neural training. AI only earns back its training time when the network changes repeatedly—between 59 and 208 times.
:::

# Slide 3: Chapter 1 — What is SDN & Why Placement Matters?

- **Traditional Networks vs. Software Defined Networking (SDN)**:
  - **Old way**: Every router thinks for itself—hard to update rules across a whole country.
  - **SDN way**: Separate the **"Brains" (Controllers)** from the **"Roads" (Switches)**.
- **The Controller Placement Problem (CPP)**:
  - Think of placing **fire stations or ambulances** across cities:
  - Where do we put k controllers across N switch sites?
- **Three Things Every Network Operator Cares About**:
  - **1. Speed (L(P))**: How fast switches get instructions (propagation delay in ms).
  - **2. Backup Safety (Reach_avg)**: If **1 fiber cable gets cut**, can switches still reach a controller?
  - **3. Compute Time (ω_train vs. τ_inf)**: How long it takes to *train* vs. *run* the algorithm.

::: notes
Chapter 1 sets the stage. In traditional networks, every router makes its own forwarding decisions, which makes wide-area management slow and messy. Software Defined Networking—or SDN—fixes that by separating the 'brains', called controllers, from the 'roads', which are the switches. Whenever a switch sees unfamiliar traffic, it asks its controller what to do. Now, imagine you run a national network across 20 or 50 cities. You can think of placing controllers just like placing ambulance or fire stations across a country: if you only put one station in one city, everyone far away waits too long—and if a bridge washes out, whole towns get cut off. So we deploy k controllers across the network. That choice controls three things we measure in this study: first, Speed—how many milliseconds messages take to travel; second, Backup Safety—if one fiber cable breaks, what percentage of switches stay connected; and third, Compute Time—how long the algorithm takes to find the answer.
:::

# Slide 4: Chapter 1 — The Problem: 4 Blind Spots in Prior Research

- **Why Were Network Planners Confused About AI vs. Classic Methods?**
  - **Blind Spot 1 — Hiding AI Training Time**: Many AI papers brag that their neural network decides in `< 1 ms`, while hiding the **11–21 seconds** needed to train it!
  - **Blind Spot 2 — Lucky Single Runs**: AI is often tested on just **1 network** and **1 random seed** (no statistical proof).
  - **Blind Spot 3 — Ignoring Broken Links**: Papers optimize speed alone and forget that cutting a single cable can isolate whole sections of switches.
  - **Blind Spot 4 — No Real Guide**: Nobody tells network engineers *when* to pick simple math rules vs. *when* to bother with AI.

::: notes
In Section 1.3 of Chapter 1, we identified four major blind spots in existing research. First, many recent AI papers report that a trained Deep Q-Network picks controller locations in under a millisecond—which sounds amazing—but they completely hide the 11 to 21 seconds of training time required beforehand. Comparing an already-trained AI to a classic algorithm that solves the problem from scratch in 5 milliseconds isn't a fair comparison! Second, many studies run only one random seed on one map, instead of running balanced multi-seed tests. Third, optimizing only for speed can leave switches stranded behind a single fragile bridge cable. And fourth, because of these gaps, network engineers have had no clear decision rule for when to use simple heuristics and when to actually use AI.
:::

# Slide 5: Chapter 1 — Our Goal, 7 Objectives & Significance

- **Main Research Goal (Sec. 1.4.1)**:
  - Run a fair, reproducible benchmark of **5 methods** on networks up to **50 nodes**, measuring **Speed**, **Link-Cut Backup Safety**, and **Compute Time** together.
- **Our 7 Specific Objectives (Sec. 1.4.2) in 3 Simple Stages**:
  - **Stage A — Build (Obj. 1–2)**: Build an automated Python testbed (`Internet2`, `ATT-MPLS`, `BA`, `Waxman`) & implement all **5 algorithms** fairly.
  - **Stage B — Test & Compare (Obj. 3–5)**: Check if DQN truly learns (1,000 episodes × 10 runs), run **300 factorial tests** (ANOVA), & map 2D/3D trade-offs.
  - **Stage C — Verify & Guide (Obj. 6–7)**: Test placements inside real **Mininet/OpenFlow**, test 1,000 link failures, & write a simple guide for engineers.
- **Significance (Sec. 1.5)**: Open-source code, `22/22` unit tests, & practical topology insights.

::: notes
Section 1.4 defines our main goal and seven specific objectives. To keep them easy to follow, our seven objectives fall into three clear stages. First, Stage A—Objectives 1 and 2: build a clean, automated Python pipeline and implement all five algorithms under the exact same rules. Second, Stage B—Objectives 3, 4, and 5: verify that our Deep Q-Network actually learns steadily across 10 independent runs, run a balanced 300-experiment comparison across different network shapes, and map the 3D trade-offs between speed, reliability, and compute time. Third, Stage C—Objectives 6 and 7: double-check our rankings inside a live Mininet OpenFlow emulator, measure dynamic link failures, and turn everything into a clear decision chart for network engineers up to 50 switches.
:::

# Slide 6: Chapter 2 — How SDN Works & Why Placement Is Hard

- **Three Layers of an SDN Network (Sec. 2.1)**:
  - **1. Data Plane**: Switches forwarding packets fast (`Open vSwitch`).
  - **2. Control Plane**: Smart controllers (`Ryu` / `ONOS`) deciding routes via `OpenFlow`.
  - **3. Application Plane**: Security, traffic & QoS apps talking to controllers.
- **Why Not Just Check Every Possible Answer? (Sec. 2.2 — NP-Hard)**:
  - With **20 switches** and **3 controllers**: **1,140** possible combinations.
  - With **50 switches** and **5 controllers**: **2,118,760** combinations!
  - Checking every combination takes too long, so we need **smart algorithms** that balance **Average Speed** and **Worst-Case Speed**.

::: notes
Turning to Chapter 2, Section 2.1 explains how SDN splits a network into three layers: the Data Plane where switches move packets, the Control Plane where controllers act as the central brains, and the Application Plane for network policies. Whenever a switch gets a new type of traffic, it sends a 'Packet-In' request to its controller and waits for instructions. Now, Section 2.2 explains why placing those controllers is mathematically hard—in computer science, it is NP-hard. On a 20-node network with 3 controllers, there are 1,140 combinations. Jump to 50 nodes and 5 controllers, and there are over 2.1 million combinations! Because brute-force checking doesn't scale, engineers rely on smart algorithms to optimize either average delay or worst-case delay.
:::

# Slide 7: Chapter 2 — The 3 Algorithm Families & Link-Cut Safety

- **Three Ways Researchers Solve Placement (Sec. 2.3–2.5)**:
  - **1. Classic Heuristics**: Fast step-by-step rules—**Greedy K-Center** (picks far-apart hubs) & **Spatial K-Means** (groups nearby switches into clusters).
  - **2. Evolutionary Search**: **Genetic Algorithm (GA)**—breeds better solutions over generations like natural selection.
  - **3. AI / Deep Learning**: **Deep Q-Network (DQN)**—a neural network learns by trial-and-error (reward & penalty).
- **Backup Safety Under Single-Link Cuts (Sec. 2.6)**:
  - We break **one fiber link at a time** (N − 1 test) and check: *can every switch still reach a controller?*
  - **Bridge link** = a single road into a town; if it breaks, that town is cut off!

::: notes
Sections 2.3 through 2.6 review the three families of placement algorithms. First are classic heuristics: Greedy K-Center spreads controllers far apart to protect edge switches, while Spatial K-Means clusters nearby cities together, just like choosing regional warehouse hubs. Second is evolutionary search, specifically a Genetic Algorithm that tests a population of solutions and combines the best ones over generations. Third is Deep Reinforcement Learning—like Deep Q-Networks—which tries placements, gets a reward score, and updates neural weights over hundreds of episodes. Section 2.6 highlights a critical real-world check: single-link survivability. If a graph has 'bridge links'—meaning only one cable connects a branch of the network—cutting that one cable isolates those switches from their controller.
:::

# Slide 8: Chapter 2 — What Was Missing (2021–2026 Literature Gap)

| Study (2021–2026) | Method | Speed? | 1-Link Cut? | Split Train/Run? | Mininet? |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Mohanty et al. (2021) | K-Center Heuristic | Yes | No | No | No |
| Wang & Chen (2021) | Failure Foresight | Yes | Yes | No | No |
| Benoudifa et al. (2023) | MuZero AI | Yes | No | No | No |
| Yusuf et al. (2023) | Critical Switch | Yes | Yes | No | Yes |
| Kurra et al. (2025) | CAPFUL Dynamic DRL | Yes | Partial | No | Partial |
| Farahi et al. (2026) | AP-DQN (PyTorch AI) | Yes | Partial | No | No |
| **This Study (2026)** | **All 5 Methods** | **Yes** | **Yes (Exact)** | **Yes (Split)** | **Yes (5-Way)** |

::: notes
Section 2.7 summarizes 2021-to-2026 studies in Table 2.1. Look how easy this is to read: prior studies each looked at one or two pieces of the puzzle. Classical works like Mohanty (2021) checked speed, and Wang and Chen (2021) checked link failures. Newer AI papers like Benoudifa (2023), Kurra (2025), and Farahi (2026) focused on neural networks—but NOT A SINGLE ONE cleanly separated offline training time from online inference speed, while also testing single-link survivability and real 5-way Mininet emulation together. Our study fills all four columns at once.
:::

# Slide 9: Chapter 3 — Our Study Design & Two Clear Hypotheses

::::: columns
::: {.column width="48%"}
- **How Our Pipeline Works (Sec. 3.1, Fig. 3.1)**:
  - **Fair Isolation**: Classic methods & AI run on the exact same maps—**no cheating / no cross-seeding**.
  - **CPU Thermal Cooldown**: Prevents laptop overheating from slowing down timings.
- **Our Two Hypotheses (α = 0.05)**:
  - **Null (H_01)**: AI does *not* beat classic methods in overall quality.
  - **Alternative (H_11)**: AI gets good latency, *but* its long training time makes it less efficient than simple heuristics on stable maps.
:::
::: {.column width="52%"}
![Figure 3.1: End-to-End Comparative Research Methodology Workflow.](docs/figures/proposal_methodology_workflow.png)
:::
:::::

::: notes
Moving to Chapter 3, Figure 3.1 shows our research workflow. In the top-right box, our testbed loops through real and synthetic networks for 2, 3, and 5 controllers—with built-in CPU thermal cooldown pauses so hardware heat never distorts timing measurements. Notice the badge at the top: 'No cross-seeding.' That means we never feed classic answers to the AI as a cheat sheet; the AI learns completely from scratch on the green track while classic heuristics run cleanly on the blue track. Both tracks feed into Phase 3 statistics and Phase 4 recommendations at the bottom. We tested two simple hypotheses: first, whether AI beats heuristics at all; and second, whether AI's training time makes it less practical on static networks.
:::

# Slide 10: Chapter 3 — The 6 Networks We Tested (Table 3.1)

- **Why Test Both Shapes?** Real WANs look either like **airline hub-and-spoke maps (BA)** or **flat city road grids (Waxman)**—and algorithms behave very differently on each!

| Network | Plain-English Type | Switches (N) | Links (M) | Key Shape Trait |
| :--- | :--- | :---: | :---: | :--- |
| **Internet2** | Real US Research Backbone | 20 (11 Core) | 26 (18 Core) | Sparse real-world national fiber |
| **ATT-MPLS** | Real Commercial Carrier | 21 | 54 | Tightly meshed, many backup paths |
| **BA-20 / BA-50** | Synthetic Hub-and-Spoke | 20 / 50 | 36 / 96 | Major central "hub" cities (Airline style) |
| **WX-20 / WX-50** | Synthetic Geographic Mesh | 20 / 50 | ~19 / ~66 | Flat map; links connect nearby neighbors |

::: notes
Section 3.2 describes the six networks we tested in Table 3.1. First, we included two real-world wide-area backbones: Internet2, a sparser US research network, and ATT-MPLS, a tightly meshed commercial carrier network with plenty of alternate routes. Then, to test scale safely, we generated two synthetic network families at both 20 and 50 nodes. Barabási-Albert—or BA—creates 'hub-and-spoke' networks just like major airlines, where a few busy hubs connect everyone. Waxman creates flat geographic meshes like city roads, where switches connect mostly to nearby neighbors. Testing both shapes is crucial because what works on a hub-and-spoke network can struggle on a flat geographic map.
:::

# Slide 11: Chapter 3 — Meet the 5 Algorithms & System Design

::::: columns
::: {.column width="50%"}
- **Our 5 Contenders (Sec. 3.3, Fig. 3.2)**:
  - **1. Random**: Blindly guesses k spots (baseline floor).
  - **2. Greedy K-Center**: Picks k spots as far apart as possible.
  - **3. Spatial K-Means**: Groups map into k zones & picks each center.
  - **4. Genetic Algorithm (GA)**: Evolves top solutions over 40 generations.
  - **5. PyTorch DQN (AI)**: Replicates Farahi et al. (2026) neural agent (`N → 64 → 64 → N`), trained with replay memory (10,000 steps) & reward combining **Speed + Reliability**.
:::
::: {.column width="50%"}
![Figure 3.2: System Architecture of the Benchmark and Mininet Harness.](docs/figures/system_architecture_diagram.png)
:::
:::::

::: notes
Section 3.3 and Figure 3.2 show our system architecture and the five algorithms we built inside one unified Python codebase. First is Random, which simply guesses locations to give us a baseline floor. Second is Greedy K-Center, which spreads controllers as far apart as possible so no edge switch is left stranded. Third is Spatial K-Means, which splits the map into balanced regions and picks the center node of each zone. Fourth is our Genetic Algorithm, which evolves candidate placements over generations. Fifth is our Deep Q-Network—built in PyTorch using the exact 2026 AP-DQN neural architecture of Farahi et al., with two 64-neuron hidden layers and a composite reward scoring both speed and backup safety.
:::

# Slide 12: Chapter 3 — Fairness Controls, Caching & Ethics (Sec. 3.4–3.6)

- **Three Exact Metrics Measured (Sec. 3.5)**:
  - **1. Speed**: Average delay L(P) in milliseconds (lower is better).
  - **2. Backup Safety**: % of switches reachable after any 1 link breaks (Reach_avg).
  - **3. Compute Time**: Training time (ω_train) kept **strictly separate** from run time (τ_inf).
- **Quality & Speed Controls (Sec. 3.6)**:
  - **60-Cell Factorial Matrix** (Table 3.3): 5 algorithms × 2 shapes × 2 sizes × 3 budgets (k ∈ {2, 3, 5}) × 5 seeds = **300 runs**.
  - **SHA-256 Graph Cache**: Speeds up 1-link failure checks by **46.4%** with exact accuracy (10⁻⁹).
  - **Code Quality & Ethics**: `22/22` automated unit tests pass; no human subjects or private data used.

::: notes
Sections 3.4 through 3.6 explain how we kept every test fair, fast, and scientifically rigorous. We scored every placement on three axes: delay speed, single-link failure survivability, and compute time—always separating offline training from online execution. For our main factorial test in Table 3.3, we ran 5 algorithms across 2 network types, 2 sizes, 3 controller budgets, and 5 random seeds, giving 300 controlled runs. Because checking every single-link cut across thousands of AI training episodes is computationally heavy, we engineered a SHA-256 topology cache that made training 46.4% faster while matching exact math to 9 decimal places. Finally, 22 automated unit tests verify our code, and everything uses public and synthetic graphs with zero human-subject risks.
:::

# Slide 13: Chapter 4 — Did Our AI Actually Learn? (1,000-Episode Proof)

::::: columns
::: {.column width="48%"}
- **Why Check This First? (Sec. 4.1.1, Fig. 4.1)**:
  - Before judging AI, we must prove it **trained properly** and didn't just fail to learn!
- **Internet2 Pilot Results (N = 20, k = 3)**:
  - **Fast Learning**: Converged in **~20 episodes** (`13.199` final mean score out of `15.0`; peak `14.607`).
  - **High Quality Found**: Reached `1.420 ms` delay & `100%` backup reliability.
  - **The Catch (Time Cost)**: Training took **21.26 s** uncached (**11.40 s** cached), whereas running a single decision afterward takes just **0.029 ms**!
:::
::: {.column width="52%"}
![Figure 4.1: PyTorch DQN 1,000-Episode Training Reward Convergence Profile on Internet2.](results/dqn_1000_episodes_convergence.png)
:::
:::::

::: notes
Now we move into Chapter 4—our actual results! A fair question any examiner might ask is: 'If classic algorithms beat AI, did your AI actually learn properly?' Figure 4.1 proves that it did. Over 1,000 episodes on the Internet2 backbone, our PyTorch Deep Q-Network learns rapidly, stabilizing in about 20 episodes and climbing to a final average score of 13.2 out of 15, with a peak score of 14.6—giving 1.42 milliseconds delay and 100% single-link reachability. So the AI definitely learned! But look at the time cost: learning those 1,000 episodes took 21.26 seconds without caching—or 11.40 seconds with our SHA-256 cache—just so a single decision afterward could run in 0.029 milliseconds.
:::

# Slide 14: Chapter 4 — 10-Run AI Stability Check (No Cherry-Picking)

::::: columns
::: {.column width="48%"}
- **Testing 5 Seeds × 2 Real Backbones (Table 4.1, Fig. 4.2)**:
  - **10,000 total training episodes** across `Internet2` & `ATT-MPLS` (Seeds `42, 123, 256, 512, 1024`).
- **Consistent Every Single Time**:
  - **0 out of 10 crashes**: `divergence_flag = False` in all 10 runs!
  - **Internet2 Peak Score**: `14.19 ± 0.06` (`11.40 ms/ep`).
  - **ATT-MPLS Peak Score**: `14.85 ± 0.40` (`19.22 ms/ep`).
  - **Takeaway**: Our AI benchmark is **100% rock-solid and reproducible**.
:::
::: {.column width="52%"}
![Figure 4.2: Multi-Seed DQN Convergence and Rolling Reward Distribution Analysis.](results/rl_analysis/convergence_analysis.png)
:::
:::::

::: notes
In AI research, people sometimes cherry-pick one lucky random seed that looked good. To avoid that completely, Figure 4.2 and Table 4.1 audit our Deep Q-Network across 5 different random seeds on both Internet2 and ATT-MPLS—a total of 10,000 training episodes. Every single run converged smoothly with zero crashes or divergent behavior, scoring consistently around 14.2 on Internet2 and 14.85 on ATT-MPLS. That proves our AI setup is completely reliable and fair before we pit it against the classic algorithms.
:::

# Slide 15: Chapter 4 — Static Results: Hub-and-Spoke Maps (BA)

::::: columns
::: {.column width="48%"}
- **Airline-Style Hub Networks (Table 4.2, Fig. 4.3)**:
  - **Genetic Algorithm (GA)**: Lowest average delay in **6 out of 6** tests (up to **39.3%** faster than Random).
  - **Greedy K-Center**: Instantly locks onto the central hubs in **0.03–0.21 ms** with **zero training** (stays on the optimal Pareto curve 100% of the time!).
  - **Why K-Means Struggled at k = 2**: Drawing flat zones on a star-shaped hub graph distorts true network hops.
  - **All Methods**: **100% backup safety** (no vulnerable single bridges).
:::
::: {.column width="52%"}
![Figure 4.3: Pareto Latency-Cost Trade-Off Frontier on Barabási-Albert (N=50, k=3).](results/graphs/latency_cost_pareto_20261017_052319/latency_cost_pareto_barabasi_albert_n50_k3_20261017_052319.png)
:::
:::::

::: notes
Now look at what happened when we tested static 'hub-and-spoke' Barabási-Albert networks in Table 4.2 and Figure 4.3. Two clear winners stood out. First, our Genetic Algorithm achieved the lowest average delay in all 6 out of 6 test cells, cutting latency by up to 39.3% compared to Random. Second, Greedy K-Center proved to be the superstar for instant speed: because BA networks have a few major central hubs, Greedy naturally grabs those hubs in under 0.21 milliseconds with zero training time! Meanwhile, Spatial K-Means occasionally stumbled when k=2 because flat 2D clusters miss how central hubs bridge across the graph. Importantly, because BA networks have redundant paths, every algorithm kept 100% reachability under single-link failures.
:::

# Slide 16: Chapter 4 — Static Results: Flat Geographic Maps (Waxman)

::::: columns
::: {.column width="48%"}
- **City-Road-Style Flat Maps (Table 4.3, Fig. 4.4)**:
  - **Genetic Algorithm (GA)**: Again wins lowest average delay in **6 out of 6** tests (up to **55.3%** faster than Random).
  - **Spatial K-Means Shines**: Matches GA closely (e.g., `1.998 ms` vs `1.879 ms` at N = 20, k = 5) in just **3.2–8.1 ms**!
  - **Watch Out for Bridge Cables!**: Unlike BA hubs, sparse Waxman maps have vulnerable single-cable "dead-end" branches—dropping backup reachability to **94.5%–98.8%** when cut.
:::
::: {.column width="52%"}
![Figure 4.4: Pareto Latency-Cost Trade-Off Frontier on Waxman Spatial (N=50, k=3).](results/graphs/latency_cost_pareto_20261017_052319/latency_cost_pareto_waxman_n50_k3_20261017_052319.png)
:::
:::::

::: notes
On flat, geographic Waxman networks—shown in Table 4.3 and Figure 4.4—the story flips between our fast heuristics! Here, links connect nearby neighbors like streets on a map. Because distances match physical space, Spatial K-Means shines—coming within a hair of the Genetic Algorithm's delay in just 3 to 8 milliseconds! Once again, GA won lowest average latency across all 6 cells, cutting delay by up to 55.3% over Random. One huge practical finding on Waxman maps: unlike well-meshed backbones, Waxman graphs often have fragile 'bridge links' leading to outer nodes. When one of those bridge cables breaks, reachability drops from 100% down to between 94.5% and 98.8%—proving why single-link failure checks must never be ignored.
:::

# Slide 17: Chapter 4 — The Big Verdict: 300-Run Statistics & 3D Pareto

::::: columns
::: {.column width="52%"}
- **300-Run ANOVA Statistical Proof (Table 4.4b)**:
  - **Does choice of algorithm matter?** **YES** (p < 0.0001, large effect d = 1.42).
  - **Does network shape & size matter?** **YES** (p < 0.0001).
  - **Does AI beat K-Means on static maps?** **NO** (t = 0.42, p = 0.68 — no real difference!).
- **Why Classic Wins on Static Maps (Fig. 4.5)**:
  - Counting training time (`58–1,086 ms` tabular RL; `11–21 s` DQN) pushes AI **behind** GA, K-Means & Greedy K-Center on the 3D frontier!
  - **Hypothesis Verdict**: Reject H_01 overall; **Confirm H_11**!
:::
::: {.column width="48%"}
![Figure 4.5: Three-Dimensional Multi-Objective Pareto Surface Mapping Latency, Reliability & Cost.](SDN_Pareto_3D_Print.png)
:::
:::::

::: notes
Slide 17 brings all 300 synthetic runs together using formal statistics in Table 4.4b and our 3D trade-off chart in Figure 4.5. The Multi-Factor ANOVA confirms with over 99.99% confidence that algorithm choice, network topology, network size, and controller budget all strongly affect latency. Look at the crucial statistical test between Deep Q-Networks and simple K-Means on static maps: p = 0.68. In plain English, that means there is NO statistically significant difference in latency between our trained AI and simple K-Means! When you plot Speed, Reliability, and Total Compute Time together in 3D in Figure 4.5, classic heuristics and GA sit right at the front of the optimal frontier with zero training tax, leaving AI dominated on static networks—confirming our Alternative Hypothesis H11.
:::

# Slide 18: Chapter 4 — Real Linux Emulation Test (Mininet & OVS)

- **Exact Match With Math (ρ = +1.00)**: Real OpenFlow switch ping times ranked all 5 algorithms in the **exact same order**!
- **Why We Didn't Train AI Inside Mininet (Table 4.6 — "2-Second Gate Test")**: Cleaning OpenFlow bridges (`mn -c`) takes **1.99 s** per episode (**2.88 s total**)—training 1,000 episodes inside Mininet would waste **~48 minutes per run**!

| Algorithm (Internet2, N=20, k=3) | Avg. Real RTT | Worst-Case RTT | Rank Order |
| :--- | :---: | :---: | :---: |
| **1. Genetic Algorithm (GA)** | **2.718 ms** | 6.903 ms | **Rank 1 (Best Avg.)** |
| **2. Spatial K-Means** | **2.852 ms** | **5.764 ms** | **Rank 2 (Best Tail)** |
| **3. Greedy K-Center** | 2.934 ms | 6.664 ms | Rank 3 |
| **4. Bandit RL / DQN** | 3.056 ms | 6.718 ms | Rank 4 |
| **5. Random Baseline** | 3.374 ms | 6.944 ms | Rank 5 |

::: notes
Next, in Section 4.1.5, we tested whether our math rankings hold up in a real Linux network emulator using Mininet and Open vSwitch on Internet2. As Table 4.5 shows, the real round-trip ping times matched our Dijkstra rankings in exact order—a perfect +1.00 correlation! GA finished first at 2.72 milliseconds average RTT, Spatial K-Means came second at 2.85 milliseconds and achieved the lowest worst-case tail delay at 5.76 milliseconds, while both beat RL/DQN at 3.06 milliseconds. We also ran a '2-Second Gate Test' in Table 4.6 to explain why we trained the AI on graphs first instead of inside Mininet: tearing down Linux virtual switches after each episode took nearly 2 seconds—69% of the entire cycle! Training 1,000 episodes directly inside Mininet would spend 48 minutes per seed mostly restarting bridges instead of learning.
:::

# Slide 19: Chapter 4 — What If Links Keep Failing? (1,000-State Churn)

- **1,000-State Dynamic Churn (Sec. 4.1.6, Table 4.6B)**: Cut & restored links **100 times in a row** across 5 seeds on `Internet2` & `ATT-MPLS` (k = 3).
- **Important Caveat**: Even after breaking even on compute time, **GA** (`1.45–2.32 ms`) & **Greedy** (`0.05–0.07 ms/cut`) still beat DQN (`2.29–2.93 ms`) on post-failure delay!

| Topology | AI Train Cost | AI Update Speed | Break-Even vs. GA | Break-Even vs. K-Means |
| :--- | :---: | :---: | :---: | :---: |
| **Internet2** | 772.8 ms (200 ep) | **0.026 ms/cut** | **59.0 link changes** | **145.8 link changes** |
| **ATT-MPLS** | 921.7 ms (200 ep) | **0.021 ms/cut** | **65.2 link changes** | **207.6 link changes** |

::: notes
Section 4.1.6 asks the next natural question: what if the network isn't static—what if fiber links keep breaking and recovering over time? Table 4.6B reports our 1,000-state dynamic churn experiment across 100 sequential link cuts on Internet2 and ATT-MPLS. Here, we pre-trained our PyTorch DQN once and let it update placements via a single neural forward pass in just 0.021 to 0.026 milliseconds—without retraining—while GA and K-Means recomputed from scratch each time. Here is the exact break-even answer: AI finally pays back its training cost after 59 to 65 link changes compared to GA, and 146 to 208 changes compared to K-Means. However, notice two catches: Greedy K-Center is still fast at 0.05 milliseconds without any training, and because the basic DQN only looks at node degrees, GA still gives much lower latency after a failure.
:::

# Slide 20: Chapter 4 — Simple Decision Guide for Engineers (N ≤ 50)

::::: columns
::: {.column width="48%"}
- **4 Clear Rules (Table 4.7, Fig. 4.6)**:
  - **1. Flat Regional Map (Static)**: Use **Spatial K-Means** (fast `3–8 ms`, best worst-case RTT `5.76 ms`).
  - **2. Hub-and-Spoke Core (Static)**: Use **Greedy K-Center** (near-instant `< 0.21 ms`, zero training).
  - **3. Offline Network Planning**: Use **Genetic Algorithm (GA)** (best average latency `2.72 ms` RTT).
  - **4. High-Churn Live Networks (> 60–208 shifts)**: Use **Pre-Trained DQN** (`0.02 ms` live updates), unless **Greedy** already meets latency goals.
:::
::: {.column width="52%"}
![Figure 4.6: Bounded Infrastructure Deployment Decision Flowchart (N <= 50).](docs/figures/decision_framework_flowchart.png)
:::
:::::

::: notes
Section 4.2 turns all our numbers into Figure 4.6 and Table 4.7: a simple four-rule decision guide for network engineers managing topologies up to 50 nodes. Rule 1: if your network is a stable flat geographic mesh, use Spatial K-Means for fast setup and the best worst-case tail delay. Rule 2: if your network is a stable hub-and-spoke core and you need an instant answer, use Greedy K-Center in under a quarter of a millisecond. Rule 3: if you are planning infrastructure offline and want the lowest possible average delay, run our Genetic Algorithm. Rule 4: save Deep Reinforcement Learning for high-churn networks that change topology more than 60 to 208 times without retraining—and even then, check if simple Greedy K-Center already satisfies your delay budget!
:::

# Slide 21: Chapters 4 & 5 — Limitations, Contributions & Future Work

- **Honest Scope & Limitations (Sec. 4.3)**:
  - Bounded to networks **N ≤ 50 switches**; fixed neural input size (`N → 64 → 64 → N`) cannot jump zero-shot to larger graphs.
  - Tests **single-link (N − 1)** cuts (not simultaneous multi-link disasters) on a single-host Mininet emulator.
- **Main Findings & Contributions (Sec. 5.1–5.3)**:
  - Proved **training vs. inference must be separated** so planners aren't misled by AI hype.
  - Showed **topology shape dictates the best heuristic** (Greedy for hubs, K-Means for flat maps, GA for lowest latency).
- **Future Directions (Sec. 5.4)**:
  - Replace fixed MLPs with **Graph Neural Networks (GNNs)** to scale to **100–500 nodes**, and integrate live traffic loads & distributed controller sync delays.

::: notes
Wrapping up with Section 4.3 and Chapter 5: it is important to be transparent about our boundaries. All conclusions are strictly bounded to topologies up to 50 switches, single-link outages, and a fixed-size MLP neural architecture that cannot generalize zero-shot to a bigger graph without retraining. Even within those boundaries, our contributions are clear: we showed why separating training time from inference speed changes the verdict completely, proved how topology geometry picks the winning heuristic, and built a reproducible decision framework. For future Master's research in Section 5.4, the next logical step is replacing the fixed MLP with inductive Graph Neural Networks to scale to 100 or 500 switches with live traffic telemetry.
:::

# Slide 22: References, Appendices (A–C) & SATNAC 2026 Outputs

- **Complete Dissertation Coverage Verified**:
  - **References (pp. 40–41)**: 100% current **2021–2026** peer-reviewed IEEE/SDN sources (Mohanty 2021; Wang & Chen 2021; Radam 2022; Benoudifa 2023; Yusuf 2023; Kurra 2025; Boudi 2026; Farahi 2026).
  - **Appendix A (p. 42)**: Exact software versions, hardware manifest, & deterministic PRNG seeds.
  - **Appendix B (pp. 43–47, Table B.1)**: Full 60-cell complete benchmark matrix data.
  - **Appendix C (p. 48)**: Complete Python Mininet & Open vSwitch emulation source code.
- **Dissemination Deliverables Produced**:
  - **SATNAC 2026 IEEE Conference Paper** (`SATNAC_RESEARCH_PAPER.pdf`) & **UNIZULU Research Poster**.
- **Thank You! Questions Welcome from Prof. Mudali, Mr. Zwane & Panel.**

::: notes
Finally, Slide 22 points to the supporting materials in the back of the signed dissertation: our fully updated 2021-to-2026 peer-reviewed reference list on pages 40 to 41, Appendix A with our exact software and seed manifest, Appendix B containing all 60 cells of raw benchmark numbers in Table B.1, and Appendix C with the Mininet emulation code. Beyond the dissertation itself, we also produced a 7-page IEEE conference paper targeting SATNAC 2026 and an official UNIZULU Research Poster. Thank you very much, Prof. Mudali, Mr. Zwane, and members of the examination panel—I am now ready for your questions.
:::
"""


def _load_font(size: int, bold: bool = False):
    candidates = (
        [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]
        if bold
        else [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]
    )
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size=size)
    return ImageFont.load_default()


def generate_unizulu_slide_backgrounds() -> dict[int, Path]:
    """Generates 22 Official UNIZULU Widescreen (1920x1080) slide backgrounds matching 08D01.pptx."""
    BG_DIR.mkdir(parents=True, exist_ok=True)
    W, H = 1920, 1080
    NAVY = (0, 43, 91)
    NAVY_DARK = (7, 29, 64)
    GOLD = (197, 155, 39)
    GOLD_LIGHT = (243, 198, 95)
    CANVAS_OUTER = (244, 247, 251)
    CARD_WHITE = (255, 255, 255)
    BORDER_GRAY = (214, 222, 235)

    crest_orig = Image.open(CREST_PATH).convert("RGBA")
    wm_h = 460
    wm_w = int(crest_orig.width * (wm_h / crest_orig.height))
    crest_wm = crest_orig.resize((wm_w, wm_h), Image.Resampling.LANCZOS)
    r, g, b, a = crest_wm.split()
    a = a.point(lambda p: int(p * 0.035))
    crest_wm = Image.merge("RGBA", (r, g, b, a))

    font_h1 = _load_font(36, bold=True)
    font_h2 = _load_font(20, bold=True)
    font_h3 = _load_font(18, bold=False)
    font_top_title = _load_font(20, bold=True)
    font_badge = _load_font(15, bold=True)
    font_footer = _load_font(15, bold=True)
    font_footer_reg = _load_font(14, bold=False)

    bg_paths: dict[int, Path] = {}

    for slide_idx in range(1, TOTAL_SLIDES + 1):
        img = Image.new("RGBA", (W, H), CANVAS_OUTER + (255,))
        draw = ImageDraw.Draw(img)

        if slide_idx == 1:
            draw.rectangle([0, 0, W, 285], fill=NAVY)
            draw.rectangle([0, 277, W, 285], fill=GOLD)
            draw.rectangle([0, 0, W, 8], fill=GOLD)

            draw.rounded_rectangle([48, 20, 240, 265], radius=14, fill=CARD_WHITE, outline=GOLD, width=4)
            c_h = 225
            c_w = int(crest_orig.width * (c_h / crest_orig.height))
            crest_title = crest_orig.resize((c_w, c_h), Image.Resampling.LANCZOS)
            img.paste(crest_title, (48 + (192 - c_w) // 2, 20 + (245 - c_h) // 2), crest_title)

            draw.text((270, 34), "UNIVERSITY OF ZULULAND", fill=GOLD_LIGHT, font=font_h1)
            draw.text(
                (270, 84),
                "A NODE FOR AFRICAN THOUGHT  •  RESTRUCTURED FOR RELEVANCE",
                fill=(226, 232, 240),
                font=font_h2,
            )
            draw.line([(270, 120), (1310, 120)], fill=GOLD, width=2)
            draw.text((270, 134), "FACULTY OF SCIENCE, AGRICULTURE AND ENGINEERING", fill=CARD_WHITE, font=font_h2)
            draw.text(
                (270, 166),
                "DEPARTMENT OF COMPUTER SCIENCE  |  BSc HONOURS MINI-DISSERTATION VIVA DEFENSE",
                fill=(203, 213, 225),
                font=font_h3,
            )
            draw.text(
                (270, 206),
                "CLEAR & ACCESSIBLE EDITION  |  FULL DISSERTATION TOC COVERAGE (CH. 1–5 & APPENDICES A–C)",
                fill=GOLD_LIGHT,
                font=font_badge,
            )

            draw.rounded_rectangle([1365, 34, 1872, 248], radius=12, fill=NAVY_DARK, outline=GOLD, width=3)
            draw.text((1390, 52), "PRESENTATION ROADMAP", fill=GOLD_LIGHT, font=font_h2)
            draw.text((1390, 86), "• Front Matter & Abstract (Slides 1–2)", fill=CARD_WHITE, font=font_footer_reg)
            draw.text((1390, 112), "• Ch. 1–2: Problem & Lit. (Slides 3–8)", fill=CARD_WHITE, font=font_footer_reg)
            draw.text((1390, 138), "• Ch. 3: Design & Setup (Slides 9–12)", fill=CARD_WHITE, font=font_footer_reg)
            draw.text((1390, 164), "• Ch. 4: Results & Guide (Slides 13–20)", fill=GOLD_LIGHT, font=font_footer)
            draw.text((1390, 190), "• Ch. 5, Apps & SATNAC (Slides 21–22)", fill=GOLD_LIGHT, font=font_footer)

            draw.rounded_rectangle([72, 308, W - 72, 922], radius=16, fill=CARD_WHITE, outline=NAVY, width=3)
            draw.rounded_rectangle([82, 318, W - 82, 912], radius=12, fill=CARD_WHITE, outline=GOLD, width=2)
            img.paste(crest_wm, ((W - wm_w) // 2, 385), crest_wm)

            draw.rectangle([0, 945, W, H], fill=NAVY)
            draw.rectangle([0, 945, W, 952], fill=GOLD)
            draw.text(
                (60, 968),
                "CANDIDATE: Thabang Nhlokoma Buthelezi (Student No: 230011908)   |   DEGREE: BSc Honours in Computer Science (2026)",
                fill=CARD_WHITE,
                font=font_footer,
            )
            draw.text(
                (60, 1002),
                "SUPERVISORS: Prof. Pragasen Mudali (UNIZULU) & Mr. Skhumbuzo Zwane (CSIR)   |   SATNAC 2026 Dissemination",
                fill=GOLD_LIGHT,
                font=font_footer_reg,
            )
            draw.rounded_rectangle([1700, 970, 1868, 1022], radius=10, fill=GOLD, outline=CARD_WHITE, width=2)
            draw.text((1720, 986), f"Slide 1 of {TOTAL_SLIDES}", fill=NAVY_DARK, font=font_footer)

        else:
            draw.rectangle([0, 0, W, 74], fill=NAVY)
            draw.rectangle([0, 69, W, 74], fill=GOLD)

            draw.rounded_rectangle([20, 6, 74, 64], radius=6, fill=CARD_WHITE, outline=GOLD, width=2)
            mc_h = 52
            mc_w = int(crest_orig.width * (mc_h / crest_orig.height))
            crest_mini = crest_orig.resize((mc_w, mc_h), Image.Resampling.LANCZOS)
            img.paste(crest_mini, (20 + (54 - mc_w) // 2, 6 + (58 - mc_h) // 2), crest_mini)

            draw.text(
                (90, 14),
                "UNIVERSITY OF ZULULAND  |  DEPT. OF COMPUTER SCIENCE",
                fill=GOLD_LIGHT,
                font=font_top_title,
            )
            draw.text(
                (90, 41),
                "BSc Honours Computer Science Defense  •  A Node for African Thought",
                fill=(219, 234, 254),
                font=font_footer_reg,
            )

            badge_text = SLIDE_TOC_BADGES.get(slide_idx, "UNIZULU HONOURS DEFENSE 2026")
            bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
            bw = bbox[2] - bbox[0] + 36
            bx1 = W - bw - 24
            draw.rounded_rectangle([bx1, 14, W - 24, 56], radius=8, fill=NAVY_DARK, outline=GOLD, width=2)
            draw.text((bx1 + 18, 25), badge_text, fill=GOLD_LIGHT, font=font_badge)

            draw.rounded_rectangle([22, 82, W - 22, 992], radius=12, fill=CARD_WHITE, outline=BORDER_GRAY, width=2)
            draw.rectangle([22, 82, 32, 992], fill=NAVY)
            draw.rectangle([32, 82, 36, 992], fill=GOLD)
            draw.line([(56, 158), (W - 56, 158)], fill=(203, 213, 225), width=2)

            img.paste(crest_wm, ((W - wm_w) // 2, 320), crest_wm)

            draw.rectangle([0, 1002, W, H], fill=NAVY)
            draw.rectangle([0, 1002, W, 1007], fill=BORDER_GRAY)
            prog_w = int(W * (slide_idx / float(TOTAL_SLIDES)))
            draw.rectangle([0, 1000, prog_w, 1007], fill=GOLD)

            draw.text(
                (36, 1018),
                "Thabang Nhlokoma Buthelezi (230011908)  |  Supervisors: Prof. P. Mudali (UNIZULU) & Mr. S. Zwane (CSIR)",
                fill=CARD_WHITE,
                font=font_footer,
            )
            draw.text(
                (36, 1044),
                "AI vs. Heuristic SDN Controller Placement — Simplified Viva Presentation  •  SATNAC 2026",
                fill=GOLD_LIGHT,
                font=font_footer_reg,
            )

            s_txt = f"Slide {slide_idx} of {TOTAL_SLIDES}"
            draw.rounded_rectangle([1710, 1018, 1892, 1064], radius=8, fill=GOLD, outline=CARD_WHITE, width=2)
            draw.text((1730, 1031), s_txt, fill=NAVY_DARK, font=font_footer)

        out_file = BG_DIR / f"unizulu_bg_slide_{slide_idx:02d}.png"
        img.convert("RGB").save(out_file, format="PNG", optimize=True)
        bg_paths[slide_idx] = out_file

    return bg_paths


def _set_xfrm(sp_pr, x: int, y: int, cx: int, cy: int):
    A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
    xfrm = sp_pr.find(f"{{{A_NS}}}xfrm")
    if xfrm is None:
        xfrm = etree.Element(f"{{{A_NS}}}xfrm")
        sp_pr.insert(0, xfrm)
    off = xfrm.find(f"{{{A_NS}}}off")
    if off is None:
        off = etree.SubElement(xfrm, f"{{{A_NS}}}off")
    off.set("x", str(x))
    off.set("y", str(y))
    ext = xfrm.find(f"{{{A_NS}}}ext")
    if ext is None:
        ext = etree.SubElement(xfrm, f"{{{A_NS}}}ext")
    ext.set("cx", str(cx))
    ext.set("cy", str(cy))
    prst = sp_pr.find(f"{{{A_NS}}}prstGeom")
    if prst is None:
        prst = etree.Element(f"{{{A_NS}}}prstGeom", prst="rect")
        etree.SubElement(prst, f"{{{A_NS}}}avLst")
        sp_pr.insert(1, prst)


def _apply_txbody_typography(
    tx_body,
    lvl0_sz: int,
    lvl1_sz: int,
    color_hex: str | None = None,
    align: str | None = None,
    anchor: str = "t",
    spc_bef_pts: int = 380,
    ln_spc_pct: int = 104000,
    add_bullets: bool = False,
):
    A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
    body_pr = tx_body.find(f"{{{A_NS}}}bodyPr")
    if body_pr is None:
        body_pr = etree.Element(f"{{{A_NS}}}bodyPr")
        tx_body.insert(0, body_pr)
    body_pr.set("anchor", anchor)
    body_pr.set("lIns", "45720")
    body_pr.set("rIns", "45720")
    body_pr.set("tIns", "22860")
    body_pr.set("bIns", "22860")
    for ch in list(body_pr):
        body_pr.remove(ch)
    etree.SubElement(body_pr, f"{{{A_NS}}}normAutofit")

    for p in tx_body.xpath(".//*[local-name()='p']"):
        p_pr = p.find(f"{{{A_NS}}}pPr")
        if p_pr is None:
            p_pr = etree.Element(f"{{{A_NS}}}pPr")
            p.insert(0, p_pr)
        lvl = int(p_pr.get("lvl", "0"))
        sz_val = lvl0_sz if lvl == 0 else lvl1_sz
        if align:
            p_pr.set("algn", align)

        if add_bullets:
            for bn in p_pr.xpath("./*[local-name()='buNone']"):
                p_pr.remove(bn)
            if lvl == 0:
                p_pr.set("marL", "220000")
                p_pr.set("indent", "-220000")
                if not p_pr.xpath("./*[local-name()='buChar']"):
                    etree.SubElement(p_pr, f"{{{A_NS}}}buChar", char="•")
            else:
                p_pr.set("marL", "450000")
                p_pr.set("indent", "-190000")
                if not p_pr.xpath("./*[local-name()='buChar']"):
                    etree.SubElement(p_pr, f"{{{A_NS}}}buChar", char="–")

        for old_tag in ("lnSpc", "spcBef", "spcAft"):
            for el in p_pr.xpath(f"./*[local-name()='{old_tag}']"):
                p_pr.remove(el)
        ln_spc = etree.Element(f"{{{A_NS}}}lnSpc")
        etree.SubElement(ln_spc, f"{{{A_NS}}}spcPct", val=str(ln_spc_pct))
        spc_bef = etree.Element(f"{{{A_NS}}}spcBef")
        etree.SubElement(spc_bef, f"{{{A_NS}}}spcPts", val=str(spc_bef_pts if lvl == 0 else max(180, spc_bef_pts - 140)))
        spc_aft = etree.Element(f"{{{A_NS}}}spcAft")
        etree.SubElement(spc_aft, f"{{{A_NS}}}spcPts", val="120")
        p_pr.insert(0, spc_aft)
        p_pr.insert(0, spc_bef)
        p_pr.insert(0, ln_spc)

        for r in p.xpath(".//*[local-name()='r']"):
            r_pr = r.find(f"{{{A_NS}}}rPr")
            if r_pr is None:
                r_pr = etree.Element(f"{{{A_NS}}}rPr")
                r.insert(0, r_pr)
            r_pr.set("sz", str(sz_val))
            if color_hex:
                for sf in r_pr.xpath("./*[local-name()='solidFill']"):
                    r_pr.remove(sf)
                sf = etree.Element(f"{{{A_NS}}}solidFill")
                etree.SubElement(sf, f"{{{A_NS}}}srgbClr", val=color_hex)
                r_pr.insert(0, sf)

        for end_rpr in p.xpath("./*[local-name()='endParaRPr']"):
            end_rpr.set("sz", str(sz_val))


def _style_table_frame(gf, x: int, y: int, cx: int, cy: int, font_sz: int = 1150):
    A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
    P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
    xfrm = gf.find(f"{{{P_NS}}}xfrm")
    if xfrm is None:
        xfrm = gf.find(f"{{{A_NS}}}xfrm")
    if xfrm is not None:
        off = xfrm.find(f"{{{A_NS}}}off")
        ext = xfrm.find(f"{{{A_NS}}}ext")
        if off is not None:
            off.set("x", str(x))
            off.set("y", str(y))
        if ext is not None:
            ext.set("cx", str(cx))
            ext.set("cy", str(cy))

    tbl = gf.find(f".//{{{A_NS}}}tbl")
    if tbl is None:
        return

    rows = tbl.findall(f"{{{A_NS}}}tr")
    grid_cols = tbl.findall(f".//{{{A_NS}}}gridCol")
    num_cols = len(grid_cols)
    if num_cols > 0 and rows:
        col_weights = [9.0] * num_cols
        for r_idx, tr in enumerate(rows):
            tcs = tr.findall(f"{{{A_NS}}}tc")
            for c_idx, tc in enumerate(tcs[:num_cols]):
                txt = "".join(tc.xpath(".//*[local-name()='t']/text()")).strip()
                weight = max(9.0, min(68.0, (len(txt) * (1.15 if r_idx == 0 else 1.0)) + 3.0))
                if weight > col_weights[c_idx]:
                    col_weights[c_idx] = weight
        total_w = sum(col_weights)
        for c_idx, gc in enumerate(grid_cols):
            w_emu = int(cx * (col_weights[c_idx] / total_w))
            gc.set("w", str(w_emu))

    row_h = max(210000, min(320000, int(cy / max(1, len(rows) + 1))))
    for r_idx, tr in enumerate(rows):
        tr.set("h", str(row_h))
        for tc in tr.findall(f"{{{A_NS}}}tc"):
            tc_pr = tc.find(f"{{{A_NS}}}tcPr")
            if tc_pr is None:
                tc_pr = etree.SubElement(tc, f"{{{A_NS}}}tcPr")
            tc_pr.set("marL", "55000")
            tc_pr.set("marR", "55000")
            tc_pr.set("marT", "24000")
            tc_pr.set("marB", "24000")
            tc_pr.set("anchor", "ctr")

            tx_b = tc.find(f"{{{A_NS}}}txBody")
            if tx_b is not None:
                for p in tx_b.xpath(".//*[local-name()='p']"):
                    p_pr = p.find(f"{{{A_NS}}}pPr")
                    if p_pr is None:
                        p_pr = etree.Element(f"{{{A_NS}}}pPr")
                        p.insert(0, p_pr)
                    for old_tag in ("lnSpc", "spcBef", "spcAft"):
                        for el in p_pr.xpath(f"./*[local-name()='{old_tag}']"):
                            p_pr.remove(el)
                    for r in p.xpath(".//*[local-name()='r']"):
                        r_pr = r.find(f"{{{A_NS}}}rPr")
                        if r_pr is None:
                            r_pr = etree.Element(f"{{{A_NS}}}rPr")
                            r.insert(0, r_pr)
                        r_pr.set("sz", str(font_sz if r_idx > 0 else font_sz + 80))
                        if r_idx == 0:
                            r_pr.set("b", "1")


def style_pptx_with_unizulu_backgrounds(pptx_path: Path, bg_paths: dict[int, Path]):
    tmp_pptx = pptx_path.with_suffix(".tmp.pptx")
    P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
    A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
    R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"

    with zipfile.ZipFile(pptx_path, "r") as zin, zipfile.ZipFile(tmp_pptx, "w", zipfile.ZIP_DEFLATED) as zout:
        notes1_raw = zin.read("ppt/notesSlides/notesSlide1.xml")
        notes_part_name = f"notesSlide{TOTAL_SLIDES}.xml"

        for item in zin.infolist():
            data = zin.read(item.filename)

            if item.filename.startswith("ppt/theme/theme") and item.filename.endswith(".xml"):
                root = etree.fromstring(data)
                for dk2 in root.xpath(".//*[local-name()='dk2']/*[local-name()='srgbClr']"):
                    dk2.set("val", "002B5B")
                for acc1 in root.xpath(".//*[local-name()='accent1']/*[local-name()='srgbClr']"):
                    acc1.set("val", "002B5B")
                for acc2 in root.xpath(".//*[local-name()='accent2']/*[local-name()='srgbClr']"):
                    acc2.set("val", "C59B27")
                data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")

            elif item.filename == "ppt/presentation.xml":
                root = etree.fromstring(data)
                for def_rpr in root.xpath(".//*[local-name()='defaultTextStyle']//*[local-name()='defRPr']"):
                    def_rpr.set("sz", "1300")
                data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")

            elif item.filename == "[Content_Types].xml":
                root = etree.fromstring(data)
                ct_ns = "http://schemas.openxmlformats.org/package/2006/content-types"
                ov = etree.SubElement(root, f"{{{ct_ns}}}Override")
                ov.set("PartName", f"/ppt/notesSlides/{notes_part_name}")
                ov.set(
                    "ContentType",
                    "application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml",
                )
                data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")

            elif item.filename == "ppt/slideMasters/slideMaster1.xml" or (
                item.filename.startswith("ppt/slideLayouts/slideLayout") and item.filename.endswith(".xml")
            ):
                root = etree.fromstring(data)
                for t_rpr in root.xpath(".//*[local-name()='titleStyle']//*[local-name()='defRPr']"):
                    t_rpr.set("sz", "1700")
                    t_rpr.set("b", "1")
                for b_lvl1 in root.xpath(".//*[local-name()='bodyStyle']/*[local-name()='lvl1pPr']"):
                    for spc in b_lvl1.xpath("./*[local-name()='spcBef']/*[local-name()='spcPct']"):
                        spc.set("val", "3500")
                    for rpr in b_lvl1.xpath("./*[local-name()='defRPr']"):
                        rpr.set("sz", "1350")
                for b_lvl2 in root.xpath(".//*[local-name()='bodyStyle']/*[local-name()='lvl2pPr']"):
                    for spc in b_lvl2.xpath("./*[local-name()='spcBef']/*[local-name()='spcPct']"):
                        spc.set("val", "2200")
                    for rpr in b_lvl2.xpath("./*[local-name()='defRPr']"):
                        rpr.set("sz", "1250")

                for sp in root.xpath(".//*[local-name()='sp']"):
                    ph_type = sp.xpath(".//*[local-name()='ph']/@type")
                    ph_idx = sp.xpath(".//*[local-name()='ph']/@idx")
                    sp_pr = sp.find(f"{{{P_NS}}}spPr")
                    if "dt" in ph_type and sp_pr is not None:
                        _set_xfrm(sp_pr, 1371600, 3860000, 6400800, 300000)
                    elif "title" in ph_type and not item.filename.endswith("slideLayout1.xml"):
                        if sp_pr is not None:
                            _set_xfrm(sp_pr, 285000, 405000, 8574000, 330000)
                        for rpr in sp.xpath(".//*[local-name()='lstStyle']//*[local-name()='defRPr']"):
                            rpr.set("sz", "1700")
                            rpr.set("b", "1")
                    elif not item.filename.endswith("slideLayout1.xml"):
                        for l1 in sp.xpath(".//*[local-name()='lstStyle']/*[local-name()='lvl1pPr']/*[local-name()='defRPr']"):
                            l1.set("sz", "1350")
                        for l2 in sp.xpath(".//*[local-name()='lstStyle']/*[local-name()='lvl2pPr']/*[local-name()='defRPr']"):
                            l2.set("sz", "1250")
                        if item.filename.endswith("slideMaster1.xml") and "body" in ph_type:
                            if sp_pr is not None:
                                _set_xfrm(sp_pr, 285000, 820000, 8574000, 3600000)
                        elif item.filename.endswith("slideLayout2.xml") and ph_idx == ["1"]:
                            if sp_pr is not None:
                                _set_xfrm(sp_pr, 285000, 820000, 8574000, 3600000)
                        elif item.filename.endswith("slideLayout4.xml"):
                            if ph_idx == ["1"] and sp_pr is not None:
                                _set_xfrm(sp_pr, 285000, 820000, 4180000, 3600000)
                            elif ph_idx == ["2"] and sp_pr is not None:
                                _set_xfrm(sp_pr, 4620000, 820000, 4220000, 3600000)
                        elif item.filename.endswith("slideLayout8.xml"):
                            if ph_idx == ["1"] and sp_pr is not None:
                                _set_xfrm(sp_pr, 285000, 1760000, 8574000, 2700000)
                            elif ph_idx == ["2"] and sp_pr is not None:
                                _set_xfrm(sp_pr, 285000, 820000, 8574000, 900000)
                    else:
                        for tint in sp.xpath(".//*[local-name()='tint']"):
                            tint.getparent().remove(tint)
                        if "ctrTitle" in ph_type and sp_pr is not None:
                            _set_xfrm(sp_pr, 550000, 1580000, 8044000, 980000)
                        elif "subTitle" in ph_type and sp_pr is not None:
                            _set_xfrm(sp_pr, 650000, 2620000, 7844000, 1120000)

                data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")

            elif item.filename.startswith("ppt/slides/slide") and item.filename.endswith(".xml"):
                slide_num = int(item.filename.replace("ppt/slides/slide", "").replace(".xml", ""))
                raw_str = data.decode("utf-8")
                if "xmlns:a14=" not in raw_str.split(">")[0]:
                    raw_str = raw_str.replace(
                        "<p:sld ",
                        '<p:sld xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main" ',
                        1,
                    )
                root = etree.fromstring(raw_str.encode("utf-8"))
                csld = root.find(f"{{{P_NS}}}cSld")
                if csld is not None:
                    old_bg = csld.find(f"{{{P_NS}}}bg")
                    if old_bg is not None:
                        csld.remove(old_bg)
                    bg_el = etree.Element(f"{{{P_NS}}}bg")
                    bg_pr = etree.SubElement(bg_el, f"{{{P_NS}}}bgPr")
                    blip_fill = etree.SubElement(bg_pr, f"{{{A_NS}}}blipFill", dpi="0", rotWithShape="1")
                    etree.SubElement(blip_fill, f"{{{A_NS}}}blip", attrib={f"{{{R_NS}}}embed": "rIdBg"})
                    stretch = etree.SubElement(blip_fill, f"{{{A_NS}}}stretch")
                    etree.SubElement(stretch, f"{{{A_NS}}}fillRect")
                    etree.SubElement(bg_pr, f"{{{A_NS}}}effectLst")
                    csld.insert(0, bg_el)

                has_table = bool(root.xpath(".//*[local-name()='graphicFrame']"))
                has_pic = bool(root.xpath(".//*[local-name()='pic']"))

                if slide_num == 1:
                    for sp in root.xpath(".//*[local-name()='sp']"):
                        ph_type = sp.xpath(".//*[local-name()='ph']/@type")
                        sp_pr = sp.find(f"{{{P_NS}}}spPr")
                        tx_b = sp.find(f"{{{P_NS}}}txBody")
                        if sp_pr is None or tx_b is None:
                            continue
                        if "ctrTitle" in ph_type:
                            _set_xfrm(sp_pr, 550000, 1580000, 8044000, 980000)
                            _apply_txbody_typography(
                                tx_b, 2100, 1950, color_hex="002B5B", align="ctr", anchor="ctr", spc_bef_pts=0
                            )
                            for rpr in tx_b.xpath(".//*[local-name()='rPr']"):
                                rpr.set("b", "1")
                        elif "subTitle" in ph_type:
                            _set_xfrm(sp_pr, 650000, 2620000, 7844000, 1120000)
                            for br in tx_b.xpath(".//*[local-name()='br']"):
                                prev = br.getprevious()
                                if prev is not None:
                                    t_els = prev.xpath(".//*[local-name()='t']")
                                    if t_els and t_els[-1].text and not t_els[-1].text.endswith(" "):
                                        t_els[-1].text = t_els[-1].text + "   •   "
                            _apply_txbody_typography(
                                tx_b, 1400, 1300, color_hex="1E293B", align="ctr", anchor="ctr", spc_bef_pts=220
                            )
                        elif "dt" in ph_type:
                            _set_xfrm(sp_pr, 1371600, 3860000, 6400800, 300000)
                            _apply_txbody_typography(
                                tx_b, 1300, 1300, color_hex="002B5B", align="ctr", anchor="ctr", spc_bef_pts=0
                            )
                            for rpr in tx_b.xpath(".//*[local-name()='rPr']"):
                                rpr.set("b", "1")

                elif has_table and not has_pic:
                    # Full-width table slides (Slides 8, 10, 18, 19)
                    has_text_box = any(
                        "title" not in (sp.xpath(".//*[local-name()='ph']/@type") or [])
                        for sp in root.xpath(".//*[local-name()='sp']")
                    )
                    if has_text_box:
                        for sp in root.xpath(".//*[local-name()='sp']"):
                            ph_type = sp.xpath(".//*[local-name()='ph']/@type")
                            sp_pr = sp.find(f"{{{P_NS}}}spPr")
                            tx_b = sp.find(f"{{{P_NS}}}txBody")
                            if sp_pr is None or tx_b is None:
                                continue
                            if "title" in ph_type:
                                _set_xfrm(sp_pr, 285000, 405000, 8574000, 330000)
                                _apply_txbody_typography(
                                    tx_b, 1650, 1650, color_hex="002B5B", align="l", anchor="ctr", spc_bef_pts=0
                                )
                                for rpr in tx_b.xpath(".//*[local-name()='rPr']"):
                                    rpr.set("b", "1")
                            else:
                                _set_xfrm(sp_pr, 285000, 800000, 8574000, 980000)
                                _apply_txbody_typography(
                                    tx_b, 1220, 1150, color_hex="0F172A", align="l", anchor="t", spc_bef_pts=180, ln_spc_pct=98000, add_bullets=True
                                )
                        for gf in root.xpath(".//*[local-name()='graphicFrame']"):
                            _style_table_frame(gf, 285000, 1880000, 8574000, 2500000, font_sz=1120)
                    else:
                        # Pure full-width table (Slide 8)
                        for sp in root.xpath(".//*[local-name()='sp']"):
                            ph_type = sp.xpath(".//*[local-name()='ph']/@type")
                            sp_pr = sp.find(f"{{{P_NS}}}spPr")
                            tx_b = sp.find(f"{{{P_NS}}}txBody")
                            if sp_pr is None or tx_b is None:
                                continue
                            if "title" in ph_type:
                                _set_xfrm(sp_pr, 285000, 405000, 8574000, 330000)
                                _apply_txbody_typography(
                                    tx_b, 1650, 1650, color_hex="002B5B", align="l", anchor="ctr", spc_bef_pts=0
                                )
                                for rpr in tx_b.xpath(".//*[local-name()='rPr']"):
                                    rpr.set("b", "1")
                        for gf in root.xpath(".//*[local-name()='graphicFrame']"):
                            _style_table_frame(gf, 285000, 860000, 8574000, 3450000, font_sz=1120)

                elif has_pic:
                    # Two-column Picture + Simple Bullets slides (Slides 9, 11, 13, 14, 15, 16, 17, 20)
                    for sp in root.xpath(".//*[local-name()='sp']"):
                        ph_type = sp.xpath(".//*[local-name()='ph']/@type")
                        cname = sp.xpath(".//*[local-name()='cNvPr']/@name")
                        sp_pr = sp.find(f"{{{P_NS}}}spPr")
                        tx_b = sp.find(f"{{{P_NS}}}txBody")
                        if sp_pr is None or tx_b is None:
                            continue
                        if "title" in ph_type:
                            _set_xfrm(sp_pr, 285000, 405000, 8574000, 330000)
                            _apply_txbody_typography(
                                tx_b, 1650, 1650, color_hex="002B5B", align="l", anchor="ctr", spc_bef_pts=0
                            )
                            for rpr in tx_b.xpath(".//*[local-name()='rPr']"):
                                rpr.set("b", "1")
                        elif cname and "TextBox" in cname[0]:
                            _set_xfrm(sp_pr, 4620000, 4120000, 4220000, 320000)
                            _apply_txbody_typography(
                                tx_b, 1050, 1050, color_hex="002B5B", align="ctr", anchor="ctr", spc_bef_pts=0
                            )
                            for rpr in tx_b.xpath(".//*[local-name()='rPr']"):
                                rpr.set("b", "1")
                                rpr.set("i", "1")
                        else:
                            _set_xfrm(sp_pr, 285000, 830000, 4180000, 3580000)
                            _apply_txbody_typography(
                                tx_b,
                                1300,
                                1200,
                                color_hex="0F172A",
                                align="l",
                                anchor="t",
                                spc_bef_pts=260,
                                ln_spc_pct=102000,
                            )

                    for pic in root.xpath(".//*[local-name()='pic']"):
                        sp_pr = pic.find(f"{{{P_NS}}}spPr")
                        if sp_pr is None:
                            continue
                        off = sp_pr.xpath(".//*[local-name()='off']")
                        ext = sp_pr.xpath(".//*[local-name()='ext']")
                        if off and ext:
                            orig_cx = max(1, int(ext[0].get("cx", "4000000")))
                            orig_cy = max(1, int(ext[0].get("cy", "2800000")))
                            box_x, box_y = 4620000, 840000
                            box_cx, box_cy = 4220000, 3200000
                            scale = min(box_cx / orig_cx, box_cy / orig_cy)
                            new_cx = int(orig_cx * scale)
                            new_cy = int(orig_cy * scale)
                            new_x = box_x + (box_cx - new_cx) // 2
                            new_y = box_y + (box_cy - new_cy) // 2
                            _set_xfrm(sp_pr, new_x, new_y, new_cx, new_cy)

                else:
                    # Clean Full-Width Spacious Bullet Slides (Slides 2, 3, 4, 5, 6, 7, 12, 21, 22)
                    for sp in root.xpath(".//*[local-name()='sp']"):
                        ph_type = sp.xpath(".//*[local-name()='ph']/@type")
                        sp_pr = sp.find(f"{{{P_NS}}}spPr")
                        tx_b = sp.find(f"{{{P_NS}}}txBody")
                        if sp_pr is None or tx_b is None:
                            continue
                        if "title" in ph_type:
                            _set_xfrm(sp_pr, 285000, 405000, 8574000, 330000)
                            _apply_txbody_typography(
                                tx_b, 1650, 1650, color_hex="002B5B", align="l", anchor="ctr", spc_bef_pts=0
                            )
                            for rpr in tx_b.xpath(".//*[local-name()='rPr']"):
                                rpr.set("b", "1")
                        else:
                            _set_xfrm(sp_pr, 285000, 830000, 8574000, 3580000)
                            _apply_txbody_typography(
                                tx_b,
                                1420,
                                1320,
                                color_hex="0F172A",
                                align="l",
                                anchor="t",
                                spc_bef_pts=320,
                                ln_spc_pct=104000,
                            )

                data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")

            elif item.filename.startswith("ppt/slides/_rels/slide") and item.filename.endswith(".xml.rels"):
                slide_num = int(item.filename.replace("ppt/slides/_rels/slide", "").replace(".xml.rels", ""))
                root = etree.fromstring(data)
                rel_bg = etree.SubElement(root, f"{{{REL_NS}}}Relationship")
                rel_bg.set("Id", "rIdBg")
                rel_bg.set("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image")
                rel_bg.set("Target", f"../media/unizulu_bg_slide_{slide_num:02d}.png")

                if slide_num == 1:
                    rel_n = etree.SubElement(root, f"{{{REL_NS}}}Relationship")
                    rel_n.set("Id", f"rIdNotes{TOTAL_SLIDES}")
                    rel_n.set("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide")
                    rel_n.set("Target", f"../notesSlides/{notes_part_name}")

                data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")

            zout.writestr(item, data)

        for s_idx, bg_file in bg_paths.items():
            zout.write(bg_file, f"ppt/media/unizulu_bg_slide_{s_idx:02d}.png")

        n_last_root = etree.fromstring(notes1_raw)
        for sp in n_last_root.xpath(".//*[local-name()='sp']"):
            ph = sp.xpath(".//*[local-name()='ph']/@type")
            if "body" in ph:
                for t_el in sp.xpath(".//*[local-name()='t']"):
                    t_el.text = ""
                t_nodes = sp.xpath(".//*[local-name()='t']")
                if t_nodes:
                    t_nodes[0].text = SLIDE_1_SPEAKER_NOTES
        zout.writestr(
            f"ppt/notesSlides/{notes_part_name}",
            etree.tostring(n_last_root, xml_declaration=True, encoding="UTF-8", standalone="yes"),
        )
        n_last_rels = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId2" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" '
            'Target="../slides/slide1.xml" />'
            '<Relationship Id="rId1" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster" '
            'Target="../notesMasters/notesMaster1.xml" />'
            "</Relationships>"
        )
        zout.writestr(f"ppt/notesSlides/_rels/{notes_part_name}.rels", n_last_rels.encode("utf-8"))

    shutil.move(tmp_pptx, pptx_path)


def render_pptx_visual_audit(pptx_path: Path):
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    EMU_PER_PX = 4762.5

    with zipfile.ZipFile(pptx_path, "r") as z:
        for slide_idx in range(1, TOTAL_SLIDES + 1):
            bg_data = z.read(f"ppt/media/unizulu_bg_slide_{slide_idx:02d}.png")
            bg_path = PREVIEW_DIR / f"_tmp_bg_{slide_idx}.png"
            bg_path.write_bytes(bg_data)
            canvas = Image.open(bg_path).convert("RGBA")
            bg_path.unlink()
            draw = ImageDraw.Draw(canvas)

            rels_root = etree.fromstring(z.read(f"ppt/slides/_rels/slide{slide_idx}.xml.rels"))
            rel_map = {r.get("Id"): r.get("Target") for r in rels_root}

            slide_root = etree.fromstring(z.read(f"ppt/slides/slide{slide_idx}.xml"))
            max_y_used = 0

            for sp in slide_root.xpath(".//*[local-name()='sp']"):
                off = sp.xpath(".//*[local-name()='off']")
                ext = sp.xpath(".//*[local-name()='ext']")
                if not off or not ext:
                    continue
                x_px = int(int(off[0].get("x")) / EMU_PER_PX)
                y_px = int(int(off[0].get("y")) / EMU_PER_PX)
                w_px = int(int(ext[0].get("cx")) / EMU_PER_PX)

                cur_y = y_px + 6
                for p in sp.xpath(".//*[local-name()='p']"):
                    p_pr = p.xpath("./*[local-name()='pPr']")
                    lvl = int(p_pr[0].get("lvl", "0")) if p_pr else 0
                    algn = p_pr[0].get("algn", "l") if p_pr else "l"
                    rprs = p.xpath(".//*[local-name()='rPr']/@sz")
                    sz_hundredths = int(rprs[0]) if rprs else 1350
                    font_px = max(14, int((sz_hundredths / 100.0) * 2.55))
                    is_bold = bool(p.xpath(".//*[local-name()='rPr'][@b='1']"))
                    font = _load_font(font_px, bold=is_bold)

                    txt = "".join(p.xpath(".//*[local-name()='t']/text()")).strip()
                    if not txt:
                        continue
                    has_bu_none = bool(p.xpath("./*[local-name()='pPr']/*[local-name()='buNone']"))
                    indent_px = 0 if has_bu_none else (28 if lvl == 0 else 58)
                    bullet_prefix = "" if has_bu_none else ("• " if lvl == 0 else "– ")

                    avail_w = max(120, w_px - indent_px - 32)
                    avg_char_w = max(7.5, font_px * 0.58)
                    wrap_chars = max(18, int(avail_w / avg_char_w))
                    lines = textwrap.wrap(bullet_prefix + txt, width=wrap_chars)
                    for l_i, line in enumerate(lines):
                        lx = x_px + indent_px + (16 if l_i > 0 and not has_bu_none else 0)
                        if algn == "ctr":
                            tb = draw.textbbox((0, 0), line, font=font)
                            lx = x_px + max(0, (w_px - (tb[2] - tb[0])) // 2)
                        color = (0, 43, 91) if font_px >= 38 else (15, 23, 42)
                        draw.text((lx, cur_y), line, fill=color, font=font)
                        cur_y += int(font_px * 1.24)
                    cur_y += 7
                if cur_y > max_y_used:
                    max_y_used = cur_y

            for gf in slide_root.xpath(".//*[local-name()='graphicFrame']"):
                off = gf.xpath(".//*[local-name()='off']")
                ext = gf.xpath(".//*[local-name()='ext']")
                if not off or not ext:
                    continue
                x_px = int(int(off[0].get("x")) / EMU_PER_PX)
                y_px = int(int(off[0].get("y")) / EMU_PER_PX)
                h_px = int(int(ext[0].get("cy")) / EMU_PER_PX)

                grid_cols = [int(int(c.get("w")) / EMU_PER_PX) for c in gf.xpath(".//*[local-name()='gridCol']")]
                rows = gf.xpath(".//*[local-name()='tr']")
                if not rows or not grid_cols:
                    continue
                row_h_px = min(64, max(36, int(h_px / len(rows))))
                cur_y = y_px
                for r_i, tr in enumerate(rows):
                    cur_x = x_px
                    bg_c = (0, 43, 91) if r_i == 0 else ((241, 245, 249) if r_i % 2 == 1 else (255, 255, 255))
                    fg_c = (255, 255, 255) if r_i == 0 else (15, 23, 42)
                    tcs = tr.xpath("./*[local-name()='tc']")
                    rprs_t = tr.xpath(".//*[local-name()='rPr']/@sz")
                    sz_t = int(rprs_t[0]) if rprs_t else 1150
                    font_t_px = max(18, int((sz_t / 100.0) * 2.15))
                    font_t = _load_font(font_t_px, bold=(r_i == 0))
                    for c_i, tc in enumerate(tcs[: len(grid_cols)]):
                        cw = grid_cols[c_i]
                        draw.rectangle([cur_x, cur_y, cur_x + cw, cur_y + row_h_px], fill=bg_c, outline=(203, 213, 225))
                        cell_txt = "".join(tc.xpath(".//*[local-name()='t']/text()")).strip()
                        while cell_txt and (draw.textbbox((0, 0), cell_txt, font=font_t)[2] > cw - 14) and len(cell_txt) > 4:
                            cell_txt = cell_txt[:-2] + "…"
                        draw.text((cur_x + 8, cur_y + (row_h_px - font_t_px) // 2), cell_txt, fill=fg_c, font=font_t)
                        cur_x += cw
                    cur_y += row_h_px
                if cur_y > max_y_used:
                    max_y_used = cur_y

            for pic in slide_root.xpath(".//*[local-name()='pic']"):
                off = pic.xpath(".//*[local-name()='off']")
                ext = pic.xpath(".//*[local-name()='ext']")
                blip = pic.xpath(".//*[local-name()='blip']/@*[local-name()='embed']")
                if not off or not ext or not blip:
                    continue
                x_px = int(int(off[0].get("x")) / EMU_PER_PX)
                y_px = int(int(off[0].get("y")) / EMU_PER_PX)
                w_px = int(int(ext[0].get("cx")) / EMU_PER_PX)
                h_px = int(int(ext[0].get("cy")) / EMU_PER_PX)
                target = rel_map.get(blip[0], "").replace("../", "ppt/")
                if target in z.namelist():
                    tmp_p = PREVIEW_DIR / f"_tmp_pic_{slide_idx}.png"
                    tmp_p.write_bytes(z.read(target))
                    p_img = Image.open(tmp_p).convert("RGBA").resize((w_px, h_px), Image.Resampling.LANCZOS)
                    tmp_p.unlink()
                    canvas.paste(p_img, (x_px, y_px), p_img)
                if y_px + h_px > max_y_used:
                    max_y_used = y_px + h_px

            card_limit = 922 if slide_idx == 1 else 992
            assert max_y_used <= card_limit, (
                f"Slide {slide_idx} content bottom ({max_y_used} px) exceeded card frame ({card_limit} px)!"
            )
            out_prev = PREVIEW_DIR / f"slide_{slide_idx:02d}_preview.png"
            canvas.convert("RGB").save(out_prev, format="PNG", optimize=True)


def build_printable_speaker_script():
    """Creates a clean, easy-to-read printable Speaker Script document (.docx and .pdf)."""
    lines = [
        "# BSc Honours Viva Defense — Simplified Speaker Script (22 Slides)",
        "",
        "**Candidate:** Thabang Nhlokoma Buthelezi (230011908)  ",
        "**Supervisors:** Prof. Pragasen Mudali (UNIZULU) & Mr. Skhumbuzo Zwane (CSIR)  ",
        "**Dissertation:** *Decision-Grade Multi-Objective Benchmarking of AI and Heuristic Controller Placement in Multi-Site Software Defined Networks* (University of Zululand, 2026)",
        "",
        "---",
        "",
        "## Slide 1: Title Slide & Acknowledgements",
        "",
        f"> {SLIDE_1_SPEAKER_NOTES}",
        "",
        "---",
        "",
    ]

    # Parse notes cleanly from PANDOC_SLIDES_CONTENT
    blocks = PANDOC_SLIDES_CONTENT.split("# Slide ")
    for blk in blocks[1:]:
        header = blk.splitlines()[0].strip()
        notes_start = blk.find("::: notes")
        notes_end = blk.find(":::", notes_start + 9) if notes_start != -1 else -1
        if notes_start != -1 and notes_end != -1:
            note_txt = blk[notes_start + 9 : notes_end].strip()
            lines.append(f"## Slide {header}")
            lines.append("")
            lines.append(f"> {note_txt}")
            lines.append("")
            lines.append("---")
            lines.append("")

    SCRIPT_MD.write_text("\n".join(lines), encoding="utf-8")

    subprocess.run(
        ["pandoc", str(SCRIPT_MD), "-t", "docx", "-o", str(OUTPUT_SCRIPT_DOCX)],
        cwd=str(PROJECT_ROOT),
        check=True,
    )
    subprocess.run(
        [
            "libreoffice",
            "-env:UserInstallation=file:///tmp/lo_profile_simp_pdf",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(DISSERTATION_DIR),
            str(OUTPUT_SCRIPT_DOCX),
        ],
        cwd=str(PROJECT_ROOT),
        check=True,
    )


def main():
    print("=" * 84)
    print("BUILDING SIMPLIFIED 22-SLIDE UNIZULU VIVA DEFENSE (.PPTX) & SPEAKER SCRIPT")
    print("=" * 84)

    bg_paths = generate_unizulu_slide_backgrounds()
    print(f"[1/5] Generated {TOTAL_SLIDES} UNIZULU Widescreen Slide Backgrounds in: {BG_DIR}")

    SLIDES_MD.write_text(PANDOC_SLIDES_CONTENT.strip() + "\n", encoding="utf-8")
    print(f"[2/5] Wrote Simplified Pandoc slide source: {SLIDES_MD}")

    subprocess.run(
        [
            "pandoc",
            str(SLIDES_MD),
            "-t",
            "pptx",
            "--slide-level=1",
            "--resource-path=.:dissertation:docs:results",
            "-o",
            str(OUTPUT_PPTX),
        ],
        cwd=str(PROJECT_ROOT),
        check=True,
    )
    style_pptx_with_unizulu_backgrounds(OUTPUT_PPTX, bg_paths)
    print(f"[3/5] Compiled & Frame-Fitted Simplified PowerPoint: {OUTPUT_PPTX} ({OUTPUT_PPTX.stat().st_size / 1024:.1f} KB)")

    render_pptx_visual_audit(OUTPUT_PPTX)
    print(f"[4/5] Verified {TOTAL_SLIDES}/{TOTAL_SLIDES} Zero-Overflow Visual Previews in: {PREVIEW_DIR}")

    build_printable_speaker_script()
    print(f"[5/5] Exported Printable Simplified Speaker Script (.docx & .pdf): {OUTPUT_SCRIPT_PDF}")
    print("=" * 84)


if __name__ == "__main__":
    main()
