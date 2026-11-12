# 15-Slide BSc Honours Computer Science Viva Defense Presentation & Humanized Spoken Script

- **Candidate**: Thabang Nhlokoma Buthelezi (Student Number: `230011908`)
- **Degree**: BSc Honours in Computer Science
- **Institution**: Department of Computer Science, Faculty of Science, Agriculture and Engineering, University of Zululand (UNIZULU)
- **Supervisors**: Prof. Pragasen Mudali (`mudalip@unizulu.ac.za`) and Mr. Skhumbuzo Zwane (`szwane7@csir.ac.za`)
- **Target Duration**: ~18–20 Minutes (~2,350 words at 115–120 wpm natural conversational pacing)
- **Visual Design**: Official University of Zululand Widescreen (`16:9`, `1920x1080`) Institutional Theme (UNIZULU Crest, Deep Navy `#002B5B`, Gold `#C59B27`, *"A Node for African Thought"*)
- **Rubric Alignment**: 100% Aligned with the Official **UNIZULU Honours Research Scoring Rubric 2026 (`100 Marks`)**
- **Citation Standard**: 100% Current (`2021–2026`) Verified References (`dissertation/06_references.md`)

---

## Official UNIZULU Honours Research Scoring Rubric 2026 Alignment Matrix (100 Marks)

| Rubric Section (`Honours Research Scoring Rubric 2026.docx`) | Weight | Max Marks | Target Distinction Criteria (`8.5–10` per Section) | Primary Defense Slides & Evidence Presented |
| :--- | :---: | :---: | :--- | :--- |
| **1. Problem and Background Work** *(research formulation, justification, objectives & literature)* | $\times 1$ | **10** | Problem clearly defined, appropriately scoped ($N \le 50$) & well justified; Aim, 7 Objectives & 3 RQs align; 2021–2026 literature systematically reviewed & critically discussed. | **Slides 1, 2 & 3** (Multi-site WAN motivation, 3 blind spots in 2021–2026 literature in Table 2.1, alignment of Aim $\leftrightarrow$ 7 Objectives $\leftrightarrow$ RQ1–RQ3 $\leftrightarrow$ Hypotheses $H_{01}/H_{11}$). |
| **2. Analysis and Research Design** *(appropriateness & justification of methods, data, procedures & evaluation)* | $\times 1$ | **10** | Design directly addresses objectives; 3-axis metrics ($L(P), Reach_{\text{avg}}(P), \omega_{\text{train}}$ vs. $\tau_{\text{inf}}$), data sources, reproducibility & ethics clearly justified. | **Slides 4 & 5** (Menger $N-1$ survivability, compute decomposition, canonical `Internet2`/`ATT-MPLS` + synthetic `BA`/`Waxman` provenance, SHA-256 $10^{-9}$ parity cache, fixed seeds, & UNIZULU non-human computational ethics compliance). |
| **3. Implementation or Experimentation** *(execution of the design & application of disciplinary knowledge)* | **$\times 3$** | **30** | Practical & analytical work systematically and competently executed; sound technical understanding; implementation & experiments verified (`22/22` unit tests) and documented. | **Slides 5, 6, 7, 10, 11 & 12** (5 implemented algorithms, PyTorch AP-DQN replication `N->64->64->N`, SHA-256 cache `46.4%` speedup, `22/22` unit tests, 1,000-ep convergence pilot, 10,000-ep multi-seed stability audit with `0/10` divergences, 5-way Mininet `OVSSwitch`/`TCLink` emulation, & Phase 4 2-Second Gate Test). |
| **4. Results and Discussion** *(presentation, analysis & interpretation of findings)* | $\times 1$ | **10** | Results clearly presented & analysed; discussion interprets findings relative to RQs & 2021–2026 literature; implications, unexpected findings & uncertainty considered. | **Slides 8, 9, 10 & 11** (300-run factorial matrix, Multi-Factor ANOVA $F(4,240)=118.90, p<0.0001$, Tukey HSD $d=1.42$, static equivalence $t(8)=0.42, p=0.68$, 3D Pareto surface, & 1,000-state Dynamic Link Churn $T_{\text{break}}=59.0\text{--}65.2$ epochs vs. GA). |
| **5. Quality of Report Writing and Presentation** *(overall linguistic & technical presentation)* | **$\times 2$** | **20** | Coherent, well organised & clearly written; precise technical explanations; properly labelled/referenced tables & figures; accurate 2021–2026 Harvard referencing. | **All 15 Slides (`Slides 1–15`)** (Official UNIZULU Navy & Gold visual hierarchy, numbered `Figure 3.1`–`Figure 4.6` & `Table 2.1`–`Table 4.7`, exact LaTeX math, & 100% current `2021–2026` citations). |
| **6. Conclusions and Contributions** *(extent to which results are analysed & implications explored)* | $\times 1$ | **10** | Conclusions follow logically & explain achievement of aim and all 7 objectives; contribution stated within scope ($N \le 50$); specific limitations & future work justified. | **Slides 13, 14 & 15** (Scenario-conditioned deployment decision framework for $N \le 50$, fixed-MLP & $N-1$ scope boundaries, inductive GNN future work for $N \in [100, 500]$, & 7-for-7 Objective Achievement synthesis). |
| **7. Dissemination of Results** *(conference, faculty research symposium or draft journal article)* | $\times 1$ | **10** | Complete IEEE conference article targeting DHET-accredited venue (SATNAC 2026) + Faculty Research Symposium Poster submitted with dissertation. | **Slides 1 & 15** (Complete 6-page IEEE **SATNAC 2026 Conference Paper** `docs/SATNAC_RESEARCH_PAPER.pdf` & **UNIZULU Faculty Research Symposium Poster** `poster/POSTER_Thabang_Mhlokoma_UNIZULU_2026.pdf`). |
| **TOTAL** | — | **100** | **Target Distinction Grade: $\ge 85\%$ (`95 / 100`)** | **Complete 15-Slide Deck + 43-Page Dissertation + SATNAC Paper + Symposium Poster** |

---

## SLIDE 1: Title, Institutional Identity & Dissemination Deliverables
- **Rubric Mapping**: `All 7 Rubric Sections (100 Marks) | Section 7: Dissemination of Results (10 Marks)`
- **Slide Title**: Decision-Grade Multi-Objective Benchmarking of AI and Heuristic Controller Placement in Multi-Site Software Defined Networks
- **Subtitle**: BSc Honours Computer Science Mini-Dissertation Defense | University of Zululand (2026)
- **On-Slide Content**:
  - **Candidate**: Thabang Nhlokoma Buthelezi (Student No.: `230011908`)
  - **Supervisors**: Prof. Pragasen Mudali (UNIZULU) & Mr. Skhumbuzo Zwane (CSIR)
  - **Core Focus**: Multi-objective benchmarking of Deep Reinforcement Learning (PyTorch DQN & Bandit RL) against Evolutionary (GA), Clustering ($K$-Means), and Constructive ($K$-Center) Heuristics across Static & Dynamic SDN Topologies ($N \le 50$).
  - **Rubric Sec. 7 Dissemination Deliverables Included**:
    1. Complete IEEE-Formatted **SATNAC 2026 Conference Paper** (`docs/SATNAC_RESEARCH_PAPER.pdf`)
    2. Official **UNIZULU Faculty Research Symposium Poster** (`poster/POSTER_Thabang_Mhlokoma_UNIZULU_2026.pdf`)
- **Ready-to-Speak Humanized Script (~145 words | ~1 min 15 sec)**:
  > "Good morning Prof. Mudali, Mr. Zwane, and esteemed members of the examination panel. `[Pause]` My name is Thabang Buthelezi, and today I am proud to present and defend my BSc Honours mini-dissertation in Computer Science at the University of Zululand, titled *Decision-Grade Multi-Objective Benchmarking of AI and Heuristic Controller Placement in Multi-Site Software Defined Networks*. `[Emphasize]` Over the past five years, a wave of Software-Defined Networking studies has proposed Deep Reinforcement Learning to solve the Controller Placement Problem. Yet a practical engineering question has remained largely unanswered: when we account for multi-second offline training overhead, single-link failure survivability, and kernel-level OpenFlow switching delays, does Deep Reinforcement Learning actually outperform classical heuristics on small-to-medium Wide Area Networks? `[Pause]` Today, I will walk you through our 300-run factorial benchmark, our 10,000-episode stability audit, our 1,000-state dynamic churn investigation, and our SATNAC 2026 dissemination paper that answer this question definitively."

---

## SLIDE 2: Problem Statement & The 2021–2026 Literature Gap
- **Rubric Mapping**: `Rubric Section 1: Problem & Background Work (Weight ×1 = 10 Marks) | Section 5: Presentation (20 Marks)`
- **Slide Title**: The Controller Placement Problem (CPP) & Three Methodological Blind Spots
- **Subtitle**: Critical Synthesis of 2021–2026 AI and Heuristic SDN Literature (Table 2.1)
- **On-Slide Content**:
  - **Multi-Site WAN Challenge**: Decoupling the control plane from OpenFlow switches (`OVSSwitch`) introduces propagation delay $L(P)$ and single-link ($N-1$) cut vulnerability (Mohanty et al., 2021; Wang & Chen, 2021; Boudi, 2026).
  - **Three Blind Spots in 2021–2026 Literature**:
    1. *Single-Metric Myopia*: Optimizing latency alone strands switches behind fragile bridge links (Yusuf et al., 2023; Kazemi & Montazerolghaem, 2023).
    2. *Conflating Training ($\omega_{\text{train}}$) & Inference ($\tau_{\text{inf}}$)*: MuZero (Benoudifa et al., 2023), CAPFUL (Kurra et al., 2025), and AP-DQN (Farahi et al., 2026) omit multi-second offline training costs.
    3. *Unvalidated Graph Abstractions*: Pure Dijkstra distances ignore Open vSwitch kernel queuing (Priya et al., 2025; Vardhan & SriBhargav, 2025).

| Study (2021–2026) | Primary Method | Latency $L(P)$ | $N-1$ Link Reliability | $\omega_{\text{train}}$ vs. $\tau_{\text{inf}}$ | Mininet RTT | 3D Pareto |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| Mohanty et al. (2021) | $k$-Center Heuristic | Yes | No | Omitted | No | No |
| Wang & Chen (2021) | Link-Failure Foresight | Yes | Yes | Omitted | No | No |
| Radam et al. (2022) | Hybrid HSA-PSO | Yes | Partial | Omitted | No | Partial |
| Benoudifa et al. (2023) | MuZero DRL | Yes | No | Omitted | No | No |
| Yusuf et al. (2023) | CPCSA Critical Switch | Yes | Yes | Omitted | Yes | No |
| Kurra et al. (2025) | CAPFUL Dynamic DRL | Yes | Partial | Omitted | Partial | No |
| Farahi et al. (2026) | AP-DQN (PyTorch DRL) | Yes | Partial | Omitted | No | No |
| **This Study (2026)** | **5-Way Benchmark** | **Yes** | **Yes ($Reach_{\text{avg}}$)** | **Yes (Separated)** | **Yes (5-Way)** | **Yes (2D/3D)** |

- **Ready-to-Speak Humanized Script (~155 words | ~1 min 20 sec)**:
  > "Moving to Slide 2—which addresses Section 1 of the Honours Scoring Rubric on Problem Formulation and Literature—when SDN decouples the control plane from forwarding switches across a multi-site WAN, every `Packet-In` and `Flow-Mod` message must traverse physical optical fiber links (Mohanty et al., 2021; Boudi, 2026). Where we place $k$ controllers directly governs both control-plane latency and fault tolerance (Wang & Chen, 2021; Xu et al., 2023). `[Gesture to Table 2.1]` When we systematically audited the 2021-to-2026 literature in Table 2.1, we uncovered three methodological blind spots. First, optimizing propagation latency alone frequently strands peripheral switches behind fragile bridge links (Yusuf et al., 2023). Second—and most importantly—recent Deep Reinforcement Learning frameworks like MuZero by Benoudifa et al. (2023), CAPFUL by Kurra et al. (2025), and AP-DQN by Farahi et al. (2026) celebrate sub-millisecond inference speed while ignoring the multi-second offline training tax required to learn that policy. Third, pure shortest-path models rarely check whether graph rankings survive inside an emulated OpenFlow kernel."

---

## SLIDE 3: Research Questions, 7 Specific Objectives & Formal Hypotheses
- **Rubric Mapping**: `Rubric Section 1: Alignment of Aim, 7 Objectives, 3 RQs & Hypotheses (Weight ×1 = 10 Marks)`
- **Slide Title**: Slide 3: Research Questions, 7 Objectives & Formal Hypotheses
- **Subtitle**: Explicit Traceability Matrix Mapping Research Goal, 3 RQs, 7 Specific Objectives & Hypotheses ($N \le 50, k \in \{2, 3, 5\}$)
- **On-Slide Content**:
  - **RQ1 (Multi-Objective Trade-off — Mapped to Obj. 1, 2, 3, 4, 5)**: How do Constructive ($K$-Center), Clustering ($K$-Means), Metaheuristic (GA), and RL/DRL paradigms trade off mean latency $L(P)$, $N-1$ reachability $Reach_{\text{avg}}(P)$, and compute cost ($\omega_{\text{train}}$ vs. $\tau_{\text{inf}}$)?
  - **RQ2 (Topological Sensitivity — Mapped to Obj. 1, 4, 5, 7)**: How does graph structure—scale-free Barabási-Albert hubs vs. planar Waxman meshes vs. canonical Internet2/ATT-MPLS backbones—govern algorithmic dominance?
  - **RQ3 (Emulation & Dynamic Churn — Mapped to Obj. 3, 6, 7)**: Do graph-level rankings remain invariant under Mininet/OVS `TCLink` emulation, and after how many link-churn epochs ($T_{\text{break}}$) does pre-trained DQN inference amortize $\omega_{\text{train}}$?
  - **Hypotheses ($\alpha = 0.05$)**: **$H_{01}$ (Null)**: DRL yields no significant multi-objective gain over heuristics ($N \le 50$). **$H_{11}$ (Alt.)**: DRL matches static latency/reliability, but $\omega_{\text{train}}$ leaves it Pareto-dominated by GA & heuristics.

| Obj. # | Specific Research Objective (Dissertation Sec. 1.4.2) | Mapped RQs | Primary Deliverable & Empirical Verification | Slide / Ch. |
| :--- | :--- | :---: | :--- | :---: |
| **Obj. 1** | Build automated Python benchmark pipeline (`Internet2`, `ATT-MPLS`, `BA`, `Waxman` at $N \in \{20, 50\}$) | **RQ1, RQ2** | Modular graph & SHA-256 cached $N-1$ engine (`10⁻⁹` parity, `46.4%` speedup) | Slide 4 (Ch. 3) |
| **Obj. 2** | Implement & benchmark 5 paradigms: Random, Greedy $K$-Center, $K$-Means, GA, and PyTorch AP-DQN / RL | **RQ1** | Unified API across all 5 algorithms (`22/22` unit tests passing) | Slide 5 (Ch. 3) |
| **Obj. 3** | Evaluate 1,000-ep DQN pilot on `Internet2` & 10-run multi-seed stability audit (`10,000` episodes, 5 seeds) | **RQ1, RQ3** | Stabilizes in `~20 ep` (`13.199` mean); `divergence_flag = False` in `10/10` runs | Slides 6–7 (Ch. 4) |
| **Obj. 4** | Execute balanced $5 \times 2 \times 2 \times 3$ multi-seed synthetic factorial matrix ($N_{\text{obs}} = 300$) with ANOVA & Tukey HSD | **RQ1, RQ2** | GA wins `12/12` cells; ANOVA $F(4,240)=118.90, p<0.0001$; DQN vs KM $p=0.68$ | Slides 8–9 (Ch. 4) |
| **Obj. 5** | Synthesize 2D & 3D Pareto frontiers across $L(P)$, $Reach_{\text{avg}}(P)$, and separated compute ($\omega_{\text{train}}$ vs. $\tau_{\text{inf}}$) | **RQ1, RQ2** | Greedy $K$-Center (`BA`) & $K$-Means (`Waxman`) dominate static Pareto frontier | Slides 8–9 (Ch. 4) |
| **Obj. 6** | Validate 5 strategies in Mininet / Open vSwitch (`TCLink`) on `Internet2` & run 3-trial 2-Second Gate Test | **RQ3** | Exact rank parity ($\rho=+1.00$; GA `2.718 ms`, KM `2.852 ms`); Gate `2,876 ms/ep` | Slides 11–12 (Ch. 4) |
| **Obj. 7** | Formulate bounded deployment guidelines ($N \le 50$) & quantify 1,000-state link-churn break-even ($T_{\text{break}}$) | **RQ2, RQ3** | Decision flowchart ($N \le 50$); DQN breaks even at $T_{\text{break}} = 59.0\text{–}65.2\text{ ep}$ vs GA | Slides 10, 13 (Ch. 4–5) |

- **Ready-to-Speak Humanized Script (~225 words | ~1 min 35 sec)**:
  > "On Slide 3, we present the explicit traceability matrix showing how our overarching research goal and three research questions map directly to our seven specific research objectives from Section 1.4.2 and our formal statistical hypotheses. `[Pause]` First, Research Question 1 asks how our five paradigms trade off propagation latency, $N-1$ link survivability, and offline training versus online inference compute time. As shown in the table, RQ1 is answered through **Objective 1**—constructing our automated Python pipeline and SHA-256 $N-1$ survivability engine; **Objective 2**—implementing all five placement paradigms under a unified interface; **Objective 3**—evaluating PyTorch DQN convergence over a 1,000-episode pilot and a 10-run multi-seed stability audit; **Objective 4**—executing our 300-run multi-factor ANOVA benchmark; and **Objective 5**—synthesizing the 2D and 3D Pareto frontiers. `[Emphasize]` Second, Research Question 2 investigates how graph structure—scale-free Barabási-Albert hubs versus planar Waxman meshes and real carrier backbones—governs algorithmic dominance, which is operationalized by **Objectives 1, 4, 5, and 7**. `[Gesture to bottom of table]` Third, Research Question 3 tests whether our graph rankings hold inside live Mininet OpenFlow emulation and under dynamic link churn. This is fulfilled by **Objective 6**—our five-way Mininet RTT validation and 3-trial 2-Second Gate Test—and **Objective 7**, which formulates our bounded deployment guidelines for $N \le 50$ and establishes the exact link-churn break-even horizon $T_{\text{break}}$. Together, these seven objectives test our null hypothesis $H_{01}$ against our alternative hypothesis $H_{11}$ at $\alpha = 0.05$."

---

## SLIDE 4: Comparative Methodology Workflow & Three-Axis Formulation
- **Rubric Mapping**: `Rubric Section 2: Analysis, Research Design, Reproducibility & Ethics (Weight ×1 = 10 Marks)`
- **Slide Title**: Comparative Methodology Workflow & Three-Axis Formulation
- **Subtitle**: Heuristic vs. DRL Comparative Workflow (Figure 3.1), Evaluation Metrics, and UNIZULU Ethics
- **On-Slide Content**:
  - **Three-Axis Metrics (Fig. 3.1 Bottom-Left Legend)**:
    - **Latency $\ell = L(P)\downarrow$**: Mean shortest-path delay (ms): $L(P) = \frac{1}{N} \sum_{v \in V} \min_{c \in P} d(v, c)$ (Mohanty et al., 2021).
    - **Reliability $R = Reach_{\text{avg}}(P)\uparrow$**: $N-1$ single-link cut survivability ($0\text{–}1$) (Wang & Chen, 2021).
    - **Complexity $\omega$ vs. $\tau_{\text{inf}}\downarrow$**: Training (s/ep) vs. inference (ms) + SHA-256 cache (`10^-9` parity, `46.4%` faster).
  - **Fig. 3.1 Comparative Workflow Phases**:
    - **Phase 1 (Multi-Topology Iteration)**: `Internet2`, `ATT-MPLS`, `BA`, `Waxman` across $k \in \{2, 3, 5\}$ & CPU thermal cooldown control.
    - **Heuristic Track (Blue) vs. DRL Loop (Green)**: 3-step offline heuristic deployment vs. closed-loop PyTorch DQN Action–Reward–State training (**no cross-seeding** of DRL priors).
    - **Phase 3 & 4 (Validation & Planner Matrix)**: Data fusion $\to$ ANOVA/Tukey HSD, Pareto-front synthesis ($\ell$ vs. $R$ vs. $\tau$), ranking stability, & Scenario-Conditioned Selection Matrix (UNIZULU ethics compliant).
  - **Embedded Visual**: `Figure 3.1 (docs/figures/proposal_methodology_workflow.png / docs/diagrams/Gemini_Generated_Image_offmw8offmw8offm (1).png)`
- **Ready-to-Speak Humanized Script (~225 words | ~1 min 40 sec)**:
  > "On Slide 4, we address Section 2 of the scoring rubric—Analysis, Research Design, Reproducibility, and Ethics—by walking directly through our end-to-end comparative methodology workflow in Figure 3.1. `[Gesture to Top-Right of Figure 3.1]` Look first at Phase 1 in the top-right corner of the diagram: our experimental harness iterates across canonical carrier backbones—Internet2 and ATT-MPLS—as well as synthetic Barabási-Albert and Waxman topologies under controller budgets $k = 2, 3$, and $5$, incorporating automatic CPU thermal cooldown controls so hardware throttling never distorts our timing measurements. `[Gesture to Left Blue Column and Center Green Column]` From Phase 1, the workflow splits into two strictly isolated tracks—and notice the white callout badge at the top: *'No cross-seeding: heuristic solutions are NOT used as DRL priors,'* ensuring a completely fair, unassisted benchmark. In the left blue track, heuristic methods—Greedy $K$-Center, $K$-Means, and GA—take the topology input in Step 1, compute a placement offline in Step 2, and deploy into Mininet in Step 3 to measure static network performance. In the center green track, our PyTorch Deep $Q$-Network operates as a closed-loop agent: selecting placement actions, observing network state transitions, updating neural weights via reward backpropagation, and aggregating episodic metrics. `[Gesture to Bottom-Left Legend]` As shown in the bottom-left legend of Figure 3.1, both tracks collect three exact metrics: propagation latency $\ell = L(P)$ in milliseconds, $N-1$ single-link reachability $R = Reach_{\text{avg}}(P) \in [0, 1]$ accelerated by 46.4% via our SHA-256 component cache, and computational complexity $\omega$ separated into training time per episode versus online inference $\tau$. `[Gesture to Bottom Orange and Red Blocks]` Finally, Phase 3 fuses all outputs for Multi-Factor ANOVA and Tukey HSD testing, 3D Pareto-front synthesis, and Mininet ranking stability, which feed directly into Phase 4 in the bottom-right corner: our Scenario-Conditioned Selection Matrix for network planners. All experiments use fixed random seeds on non-human topologies in full compliance with UNIZULU ethics guidelines."

---

## SLIDE 5: System Architecture & Five Competing Placement Paradigms
- **Rubric Mapping**: `Rubric Section 2 (Design — 10 Marks) & Section 3 (Implementation — Weight ×3 = 30 Marks)`
- **Slide Title**: System Architecture & Five Competing Placement Paradigms
- **Subtitle**: Unified Implementation of Heuristics, Metaheuristics, and PyTorch AP-DQN (`22/22` Unit Tests)
- **On-Slide Content**:
  - **1. Random Baseline**: Seeded uniform sampling without replacement (`algorithms/baseline/random_placement.py`).
  - **2. Greedy $K$-Center**: Farthest-first 2-approximation in $\mathcal{O}(kN)$ lookups (Mohanty et al., 2021; Vardhan & SriBhargav, 2025).
  - **3. Spatial $K$-Means**: Coordinate partitioning with graph medoid snapping (Xiao & Chen, 2021; Priya et al., 2025).
  - **4. Genetic Algorithm (GA)**: Tournament selection, uniform crossover, swap mutation $p_m = 0.15$ (Radam et al., 2022; Xu et al., 2023).
  - **5. PyTorch DQN & Bandit RL**: Replicates AP-DQN (Farahi et al., 2026) — MLP `N -> 64 -> 64 -> N`, $\alpha=0.001, \gamma=0.99$, batch $32$, replay $10,000$:
    $$R(P) = 10 \cdot \frac{L_{\max} - L(P)}{L_{\max}} + 5 \cdot Reach_{\text{avg}}(P)$$
  - **Embedded Visual**: `Figure 3.2 (docs/figures/system_architecture_diagram.png)`
- **Ready-to-Speak Humanized Script (~160 words | ~1 min 20 sec)**:
  > "On Slide 5, we transition into Section 3 of the scoring rubric—Implementation and Experimentation, which carries the highest weight of 30 marks. `[Gesture to Figure 3.2]` We engineered all five placement paradigms inside a single modular Python and PyTorch architecture verified by 22 automated unit tests in `test_metrics_and_algorithms.py`. Alongside our seeded Random baseline and deterministic Greedy $K$-Center heuristic, we implemented Spatial $K$-Means clustering with discrete graph medoid snapping (Xiao & Chen, 2021; Priya et al., 2025) and an elitist Genetic Algorithm with swap mutation (Radam et al., 2022; Yusuf et al., 2023). `[Emphasize]` For our Deep Reinforcement Learning benchmark, we faithfully replicated the 2026 AP-DQN specification of Farahi et al. (2026) in PyTorch: a three-layer Multi-Layer Perceptron mapping an $N$-dimensional node-degree state vector through two 64-unit ReLU hidden layers to $N$ action $Q$-values, trained with experience replay of 10,000 transitions and a target network optimizing the composite reward $R(P) \in [0, 15]$."

---

## SLIDE 6: Phase 1 Implementation — PyTorch DQN 1,000-Episode Convergence
- **Rubric Mapping**: `Rubric Section 3: Implementation & Experimentation (Weight ×3 = 30 Marks)`
- **Slide Title**: Phase 1 Results — PyTorch DQN 1,000-Episode Convergence
- **Subtitle**: Verifying Neural Policy Convergence & SHA-256 Cache Acceleration on Internet2 ($N=20, k=3$)
- **On-Slide Content**:
  - **Canonical Internet2 ($N=20, M=26, k=3$)**:
    - Rapid convergence within **~20 episodes** as $\epsilon$ decays ($1.0 \to 0.05$).
    - **Grand Training Mean Reward**: **$13.055 \pm 0.589$**
    - **Post-Convergence Final-10 Mean**: **$13.199$**
    - **Peak Episode Reward**: **$14.607 / 15.0$** ($L(P) = 1.420\text{ ms}, Reach_{\text{avg}} = 100.0\%$).
  - **Training vs. Inference Split**:
    - **Uncached $\omega_{\text{train}}$**: **$21.26\text{ s}$** ($21.26\text{ ms/ep}$)
    - **Cached $\omega_{\text{train}}$**: **$11.40\text{ s}$** ($11.40\text{ ms/ep}$, **$46.4\%$ faster**)
    - **Online Forward Pass $\tau_{\text{inf}}$**: **$0.029\text{ ms}$**
  - **Embedded Visual**: `Figure 4.1 (results/dqn_1000_episodes_convergence.png)`
- **Ready-to-Speak Humanized Script (~150 words | ~1 min 15 sec)**:
  > "Continuing our Section 3 implementation verification on Slide 6: before any researcher can credibly argue that Deep Reinforcement Learning is outperformed by classical heuristics on static networks, they must first prove that their neural network genuinely converged and wasn't simply poorly tuned. `[Gesture to Figure 4.1]` Figure 4.1 provides that proof on the canonical 20-node Internet2 backbone. Across 1,000 training episodes, our PyTorch DQN climbs steeply during initial exploration and stabilizes within 20 episodes, achieving a grand training mean reward of $13.055 \pm 0.589$, a final 10-episode rolling average of $13.199$, and a peak reward of $14.607$ out of $15.0$—corresponding to $1.420\text{ ms}$ latency and $100\%$ single-link reachability. `[Emphasize]` However, look at the compute breakdown: training those 1,000 episodes takes $21.26\text{ seconds}$ uncached—or $11.40\text{ seconds}$ with our SHA-256 component cache, a $46.4\%$ speedup—before a single forward pass can execute in $0.029\text{ milliseconds}$."

---

## SLIDE 7: 10-Run Multi-Seed DQN Stability Audit (10,000 Episodes)
- **Rubric Mapping**: `Rubric Section 3: Implementation Verification & Multi-Seed Reproducibility (Weight ×3 = 30 Marks)`
- **Slide Title**: 10-Run Multi-Seed DQN Stability Audit (10,000 Episodes)
- **Subtitle**: Ruling Out Seed Sensitivity Across Internet2 and ATT-MPLS (`stability_summary.csv`)
- **On-Slide Content**:
  - **Multi-Seed Audit (`stability_summary.csv`)**:
    - **5 Seeds** $\{42, 123, 256, 512, 1024\} \times$ **2 Canonical WANs** (`Internet2`, `ATT-MPLS`) $\times 1,000\text{ Ep}$.
  - **Internet2 ($N=20, M=26$)**:
    - Mean Best Reward: **$14.194 \pm 0.063$**
    - Rolling Mean (Last 100): **$12.654 \pm 0.348$**
    - Training Rate: **$11.40 \pm 0.11\text{ ms/ep}$**
  - **ATT-MPLS ($N=21, M=54$)**:
    - Mean Best Reward: **$14.854 \pm 0.395$**
    - Rolling Mean (Last 100): **$12.557 \pm 0.328$**
    - Training Rate: **$19.22 \pm 6.31\text{ ms/ep}$**
  - **Result**: **`divergence_flag = False` in 10 / 10 runs** (Action Entropy $0.953\text{--}0.982$).
  - **Embedded Visual**: `Figure 4.2 (results/rl_analysis/convergence_analysis.png)`
- **Ready-to-Speak Humanized Script (~140 words | ~1 min 10 sec)**:
  > "A frequent flaw in reinforcement learning studies is cherry-picking a single favourable random seed. `[Gesture to Figure 4.2]` To rigorously verify our implementation under Section 3 of the rubric, Slide 7 and Figure 4.2 present our 10-run Multi-Seed Stability Audit across five independent random seeds on both Internet2 and the dense 21-node, 54-link ATT-MPLS backbone, totaling 10,000 training episodes. `[Emphasize]` Across all 10 audit runs in Table 4.1, zero gradient explosions or policy collapses occurred—`divergence_flag` remained `False` in 10 out of 10 runs. On Internet2, the agent achieved a tight mean best reward of $14.194 \pm 0.063$, and on ATT-MPLS it reached $14.854 \pm 0.395$, with normalized action entropy between $0.953$ and $0.982$. Having proved that our DRL implementation is stable and reproducible, let us examine our Section 4 Results and Discussion on Slide 8."

---

## SLIDE 8: Phase 2 Results — 300-Run Synthetic Factorial Matrix (BA vs. Waxman)
- **Rubric Mapping**: `Rubric Section 4: Results & Discussion — Presentation & Interpretation (Weight ×1 = 10 Marks)`
- **Slide Title**: Phase 2 — 300-Run Synthetic Factorial Matrix (BA vs. Waxman)
- **Subtitle**: How Scale-Free Hubs vs. Planar Spatial Meshes Govern Algorithmic Dominance (Tables 4.2 & 4.3)
- **On-Slide Content**:
  - **Balanced $5 \times 2 \times 2 \times 3$ Matrix ($N_{\text{obs}} = 300$)**:
    - **GA Wins Raw Latency in 12 / 12 Cells (100%)**: Up to **$55.29\%$** gain over Random on Waxman ($N=20, k=5$: **$1.879\text{ ms}$**) and **$39.26\%$** on BA ($N=20, k=3$: **$4.321\text{ ms}$**).
    - **Scale-Free BA ($m=2$)**: Greedy $K$-Center captures core hubs in **$0.026\text{--}0.207\text{ ms}$** ($100\%$ Pareto-optimal), whereas $K$-Means suffers 2D projection distortion at $k=2$.
    - **Planar Waxman ($\alpha=0.4$)**: $K$-Means closely tracks GA (**$1.998\text{ ms}$** vs. **$1.879\text{ ms}$** at $N=20, k=5$) in **$4.57\text{ ms}$**.
    - **Static RL Dominated**: Upfront training ($\omega_{\text{train}} = 58.3\text{--}1086.2\text{ ms}$) leaves RL Pareto-dominated across all 12 static cells.
  - **Embedded Visual**: `Figure 4.3 (results/graphs/latency_cost_pareto_20261017_052319/latency_cost_pareto_barabasi_albert_n50_k3_20261017_052319.png)`
- **Ready-to-Speak Humanized Script (~160 words | ~1 min 20 sec)**:
  > "Slide 8 addresses Section 4 of the scoring rubric—Results and Discussion—through our 300-observation synthetic factorial benchmark comparing Barabási-Albert scale-free networks against Waxman spatial networks across $N=20$ and $N=50$, illustrated by the Pareto frontier in Figure 4.3. `[Gesture to Figure 4.3]` Three key findings emerge. First, our Genetic Algorithm achieved the lowest mean propagation latency in all 12 out of 12 synthetic factorial cells, reducing latency by up to $55.29\%$ over Random and beating Reinforcement Learning in every single cell. `[Emphasize]` Second, graph topology dictates which fast heuristic excels: on scale-free Barabási-Albert graphs where degree-skewed hubs dominate, Greedy $K$-Center locks onto the central hubs in under $0.21\text{ milliseconds}$ and stays on the Pareto frontier in 100% of cells. Conversely, on planar Waxman meshes where link probability decays with Euclidean distance, Spatial $K$-Means closely matches GA in under $5\text{ milliseconds}$. Third, when total training time is included on static graphs, RL is Pareto-dominated across all 12 synthetic cells."

---

## SLIDE 9: Multi-Factor ANOVA ($N_{\text{obs}} = 300$) & 3D Pareto Surface
- **Rubric Mapping**: `Rubric Section 4: Results & Statistical Interpretation (Weight ×1 = 10 Marks)`
- **Slide Title**: Multi-Factor ANOVA ($N_{\text{obs}} = 300$) & 3D Pareto Surface
- **Subtitle**: Hypothesis Testing ($\alpha = 0.05$), Effect Sizes, and Menger $N-1$ Survivability (Table 4.4b)
- **On-Slide Content**:

| Source of Variation (Table 4.4b) | $SS$ | $df$ | $MS$ | $F$-Stat | $p$-Value |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Algorithm Family** | $389.92$ | $4$ | $97.48$ | **$118.90$** | **$< 0.0001$** |
| **Topology (BA vs WX)** | $204.31$ | $1$ | $204.31$ | **$249.21$** | **$< 0.0001$** |
| **Node Scale ($N$)** | $412.08$ | $1$ | $412.08$ | **$502.64$** | **$< 0.0001$** |
| **Budget ($k$)** | $188.45$ | $2$ | $94.23$ | **$114.93$** | **$< 0.0001$** |
| **Within-Cell Error** | $196.77$ | $240$ | $0.82$ | — | *(51 int. df)* |

  - **Post-Hoc Contrasts**:
    - GA / $K$-Means vs. Random: **$p < 0.001$, Cohen's $d = 1.42$**.
    - DQN/RL vs. $K$-Means (static): **$t(8) = 0.42, p = 0.68$ (NS)**.
  - **$N-1$ Survivability**: **$100.0\%$** on biconnected (Internet2, ATT-MPLS, BA) vs. **$94.47\%\text{--}98.79\%$** on bridge-prone Waxman.
  - **Embedded Visual**: `Figure 4.5 (SDN_Pareto_3D_Print.png)`
- **Ready-to-Speak Humanized Script (~155 words | ~1 min 15 sec)**:
  > "On Slide 9, we formally test our hypotheses using Multi-Factor Analysis of Variance across all 300 observations in Table 4.4b, alongside our 3D Pareto surface in Figure 4.5. `[Gesture to ANOVA table and Figure 4.5]` Partitioning the 299 total degrees of freedom into 8 main-effect degrees of freedom, 51 interaction degrees of freedom, and 240 pure within-cell error degrees of freedom confirms highly significant effects across all four factors: Algorithm Family yields $F(4, 240) = 118.90, p < 0.0001$. Post-hoc Tukey HSD tests confirm a large effect size of Cohen's $d = 1.42$ over Random. `[Emphasize]` Yet a two-sample contrast between PyTorch DQN/RL and $K$-Means on static canonical runs yields $t(8) = 0.42, p = 0.68$—confirming our alternative hypothesis $H_{11}$ that multi-second DRL training buys no statistically significant latency gain on static networks! Furthermore, our $N-1$ engine proves 100% survivability on 2-edge-connected backbones versus $94.47\%\text{ to }98.79\%$ on bridge-prone Waxman graphs."

---

## SLIDE 10: Phase 3 — Dynamic Link Churn & Amortization Horizon ($T_{\text{break}}$)
- **Rubric Mapping**: `Rubric Section 3 (Experimentation — 30 Marks) & Section 4 (Results & Discussion — 10 Marks)`
- **Slide Title**: Phase 3 — Dynamic Link Churn & Amortization Horizon ($T_{\text{break}}$)
- **Subtitle**: 1,000-State Non-Stationary Link-Failure Benchmark on Internet2 & ATT-MPLS (Table 4.6B)
- **On-Slide Content**:
  - **1,000-State Dynamic Churn Benchmark (`dynamic_churn_summary.csv`)**: $5\text{ Seeds} \times 100\text{ Non-Bridge Link-Churn Epochs}$ on Internet2 & ATT-MPLS ($k=3$).
  - **Break-Even Horizon**: $T_{\text{break}} = \lceil \omega_{\text{train}} / (\tau_{\text{algo}} - \tau_{\text{DQN, inf}}) \rceil$ (200-episode cached pre-training, zero-retraining online forward passes).

| Topology ($k=3$) | Algorithm | Upfront $\omega_{\text{train}}$ (ms) | Online $\tau_{\text{inf}}$ (ms/ep) | Cumulative $\Omega(100)$ (ms) | Mean Churn $L(P_t)$ (ms) | $Reach_{\text{avg}}$ (%) | Break-Even $T_{\text{break}}$ vs. DQN |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Internet2** | **PyTorch DQN (Inference)** | $772.79$ | **$0.0257$** | $775.36$ | $2.287$ | $99.57\%$ | Baseline Reference |
| **Internet2** | **Genetic Algorithm (GA)** | $0.00$ | $13.2030$ | $1320.30$ | **$1.450$** | $99.63\%$ | **$59.0\text{ epochs}$** ($42\text{--}101$) |
| **Internet2** | **$K$-Means Clustering** | $0.00$ | $5.2689$ | $526.90$ | $1.528$ | $99.63\%$ | **$145.8\text{ epochs}$** ($104\text{--}235$) |
| **Internet2** | **Greedy $K$-Center** | $0.00$ | $0.0497$ | **$4.97$** | $1.654$ | **$99.93\%$** | **$31,901.4\text{ epochs}$** |
| **ATT-MPLS** | **PyTorch DQN (Inference)** | $921.69$ | **$0.0213$** | $923.81$ | $2.931$ | $99.98\%$ | Baseline Reference |
| **ATT-MPLS** | **Genetic Algorithm (GA)** | $0.00$ | $14.1233$ | $1412.34$ | **$2.317$** | $99.98\%$ | **$65.2\text{ epochs}$** ($44\text{--}84$) |
| **ATT-MPLS** | **$K$-Means Clustering** | $0.00$ | $4.4728$ | $447.28$ | $2.904$ | $99.98\%$ | **$207.6\text{ epochs}$** ($147\text{--}276$) |
| **ATT-MPLS** | **Greedy $K$-Center** | $0.00$ | $0.0725$ | **$7.25$** | $2.854$ | **$100.00\%$** | **$17,955.2\text{ epochs}$** |

- **Ready-to-Speak Humanized Script (~165 words | ~1 min 25 sec)**:
  > "Now, what happens when the network topology is NOT static? Slide 10 presents our 1,000-state Dynamic Topology Churn experiment in Section 4.1.6 and Table 4.6B, motivated by dynamic SDN reconfiguration studies (Hechmi et al., 2025; Kurra et al., 2025). `[Gesture to Table 4.6B]` Here, we pre-trained our PyTorch DQN once on the base topology and then subjected Internet2 and ATT-MPLS to 100 sequential link-cut and restoration epochs across 5 seeds. At each epoch $t$, the pre-trained DQN updated its placement via a single greedy forward pass in just $0.0213\text{ to }0.0257\text{ milliseconds}$ without retraining, whereas GA, $K$-Means, and Greedy had to re-compute from scratch. `[Emphasize]` Look at the right-most column: DQN amortizes its upfront training cost after an average of **$59.0\text{ epochs}$** on Internet2 and **$65.2\text{ epochs}$** on ATT-MPLS against GA, and after **$145.8\text{ to }207.6\text{ epochs}$** against $K$-Means! Critically, however, because the replicated MLP state vector only observes node degrees rather than perturbed shortest paths, classical heuristics still maintain lower post-churn latency ($1.450\text{ ms}$ vs. $2.287\text{ ms}$)."

---

## SLIDE 11: Phase 4 — Five-Way Mininet OpenFlow RTT Validation
- **Rubric Mapping**: `Rubric Section 3 (Experimentation — 30 Marks) & Section 4 (Results — 10 Marks)`
- **Slide Title**: Phase 4 — Five-Way Mininet OpenFlow RTT Validation
- **Subtitle**: Kernel-Level Open vSwitch (`OVSSwitch`) & `TCLink` Verification (Table 4.5)
- **On-Slide Content**:
  - **Emulation Calibration (`simulation/mininet_simulation.py`)**: Open vSwitch (`OVSSwitch`) + `TCLink` scaled via $d_{\text{tc}}(u, v) = \max(0.10\text{ ms}, 2.0 \times w(u, v))$ with $\pm 0.5\text{ ms}$ uniform queuing jitter.
  - **Ordinal Ranking Invariance**: Exact Spearman rank correlation $\rho = +1.00$ ($\text{GA} \prec \text{K-Means} \prec \text{Greedy} \prec \text{RL/DQN} \prec \text{Random}$).

| Placement Strategy | Selected Controller Nodes (`Internet2`, $N=20, k=3$) | Mean Emulated RTT (ms) | Worst-Case RTT (ms) | Graph Latency $L(P)$ (ms) | RTT Overhead vs. $L(P)$ (ms) | $N-1$ Reliability |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Genetic Algorithm** | `['n1', 'n15', 'n16']` | **$2.718$ (Rank 1)** | $6.903$ | $1.403$ | $+1.315$ | $100.0\%$ |
| **$K$-Means Clustering** | `['n1', 'n16', 'n9']` | **$2.852$ (Rank 2)** | **$5.764$ (Best Tail)** | $1.469$ | $+1.383$ | $100.0\%$ |
| **Greedy $K$-Center** | `['n1', 'n10', 'n6']` | $2.934$ (Rank 3) | $6.664$ | $1.511$ | $+1.423$ | $100.0\%$ |
| **Bandit RL / DQN** | `['n1', 'n10', 'n5']` | $3.056$ (Rank 4) | $6.718$ | $1.564$ | $+1.492$ | $100.0\%$ |
| **Random Baseline** | `['n13', 'n0', 'n18']` | $3.374$ (Rank 5) | $6.944$ | $1.734$ | $+1.640$ | $100.0\%$ |

- **Ready-to-Speak Humanized Script (~150 words | ~1 min 15 sec)**:
  > "On Slide 11, we answer Research Question 3 and strengthen our Section 3 systems experimentation by evaluating all five placements inside a live Linux Mininet and Open vSwitch emulation on Internet2 ($N=20, k=3$), reported in Table 4.5. `[Gesture to Table 4.5]` Each virtual Ethernet link configures `TCLink` delay as $2.0\times$ the geodesic edge weight with a $0.10\text{ ms}$ access floor and $\pm 0.5\text{ ms}$ uniform queuing jitter to capture round-trip control-channel traversal (AlQaruty et al., 2025; Jaadouni & Saadi, 2025). `[Emphasize]` Look at the emulated Round-Trip Times: the Genetic Algorithm achieves the lowest mean RTT at **$2.718\text{ milliseconds}$**—a $19.4\%$ reduction over Random—while Spatial $K$-Means achieves the second-lowest mean RTT at **$2.852\text{ ms}$** and the best worst-case tail RTT at **$5.764\text{ ms}$**. Both outperform Bandit RL / DQN at **$3.056\text{ ms}$**. Most importantly, the ordinal ranking across all five paradigms matches our one-way Dijkstra metrics with a Spearman rank correlation of $+1.00$."

---

## SLIDE 12: Phase 4 Mininet "2-Second Gate Test" (`mininet_overhead_validation.json`)
- **Rubric Mapping**: `Rubric Section 3: Systems Instrumentation & Architectural Verification (Weight ×3 = 30 Marks)`
- **Slide Title**: Phase 4 Mininet "2-Second Gate Test" (`mininet_overhead_validation.json`)
- **Subtitle**: Empirical Proof Why OVS Bridge Teardown Cannot Be Embedded Inside 1,000 RL Episodes (Table 4.6)
- **On-Slide Content**:
  - **Pre-Experiment Gate Criterion (Section 3.4.3)**: Full Mininet lifecycle (Phases A+B+C+D) must execute in $< 2,000\text{ ms/episode}$ to permit online Mininet-in-the-loop RL training.
  - **Architectural Justification**: Running 1,000 episodes inside Mininet would spend **~48 minutes per seed** ($69.06\%$ in Linux OVS bridge teardown), validating two-stage cached graph training + post-hoc Mininet validation.

| Execution Phase (`Internet2` 11-PoP Core, $k=3$) | Trial 1 (ms) | Trial 2 (ms) | Trial 3 (ms) | Mean Overhead (ms) | Share of Lifecycle (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Phase A (Topology Instantiation)** | $695.86$ | $638.98$ | $651.99$ | $662.28$ | $23.03\%$ |
| **Phase B (Controller Binding & OVS Start)** | $133.59$ | $138.16$ | $141.31$ | $137.69$ | $4.79\%$ |
| **Phase C (`iperf3` 0.2 s Traffic Burst)** | $83.75$ | $92.55$ | $93.27$ | $89.86$ | $3.13\%$ |
| **Phase D (OVS Cleanup & Teardown `mn -c`)** | $2,061.49$ | $1,927.44$ | $1,968.09$ | **$1,985.68$** | **$69.06\%$** |
| **Active Online Control Loop (A + B + C)** | $913.20$ | $869.69$ | $886.56$ | **$889.82$** | $30.94\%$ |
| **Full Lifecycle Overhead (A + B + C + D)** | **$2,974.69$** | **$2,797.13$** | **$2,854.66$** | **$2,875.49$** | **$100.00\%$ (`WARN`)** |

- **Ready-to-Speak Humanized Script (~145 words | ~1 min 15 sec)**:
  > "An examiner evaluating Section 3 of the rubric might ask: why did we train our PyTorch DQN on cached NetworkX graphs and validate in Mininet post-hoc, rather than running Mininet inside every single RL training episode? `[Pause]` Slide 12 and Table 4.6 give the exact empirical answer from our Phase 4 Two-Second Gate Test. When we instrumented a single Mininet episode across four lifecycle phases on the 11-node Internet2 core, the active OpenFlow loop—Phases A, B, and C—averaged $889.82\text{ milliseconds}$. `[Emphasize]` However, Phase D—stopping Open vSwitch bridges and cleaning Linux kernel namespaces via `mn -c`—consumed **$1,985.68\text{ milliseconds}$**, or **$69.06\%$** of the **$2,875.49\text{ ms}$** total per-episode lifecycle! Because all three trials exceeded our $2,000\text{ ms}$ gate threshold, embedding Mininet inside 10,000 training episodes would spend nearly 8 hours measuring Linux bridge teardown rather than neural learning."

---

## SLIDE 13: Bounded Infrastructure Deployment Decision Framework ($N \le 50$)
- **Rubric Mapping**: `Rubric Section 6: Conclusions & Contributions — Practical Implications (Weight ×1 = 10 Marks)`
- **Slide Title**: Bounded Infrastructure Deployment Decision Framework ($N \le 50$)
- **Subtitle**: Actionable Scenario-Conditioned Guidelines for SDN Architects (Figure 4.6 & Table 4.7)
- **On-Slide Content**:
  - **1. Static Planar Regional Mesh ($N \le 50$)**:
    - **Deploy Spatial $K$-Means**: $\tau = 3.19\text{--}8.14\text{ ms}$, zero training, best worst-case Mininet tail RTT ($5.764\text{ ms}$).
  - **2. Scale-Free Hub-and-Spoke Core ($N \le 50$)**:
    - **Deploy Greedy $K$-Center**: $\tau = 0.026\text{--}0.207\text{ ms}$, zero training, $100\%$ Pareto frontier membership.
  - **3. Offline Strategic Capacity Planning**:
    - **Deploy Genetic Algorithm (GA)**: $\tau = 12.9\text{--}75.9\text{ ms}$, lowest mean latency ($12/12$ cells) & best mean RTT ($2.718\text{ ms}$).
  - **4. High-Churn Topologies ($T_{\text{churn}} > 60\text{--}208$ Epochs)**:
    - **Deploy Pre-Trained PyTorch DQN**: $\tau_{\text{inf}} = 0.021\text{--}0.026\text{ ms/ep}$, amortizing $\omega_{\text{train}}$ after $T_{\text{break}} = 59.0\text{--}65.2$ epochs vs. GA.
  - **Embedded Visual**: `Figure 4.6 (docs/figures/decision_framework_flowchart.png)`
- **Ready-to-Speak Humanized Script (~145 words | ~1 min 15 sec)**:
  > "Moving to Section 6 of the rubric—Conclusions and Contributions—Slide 13 translates our empirical findings into the bounded deployment decision flowchart in Figure 4.6 and Table 4.7 for networks up to 50 nodes (Ali et al., 2025; Boudi, 2026). `[Gesture to Figure 4.6]` First, for static regional planar meshes where average and tail latency matter, engineers should deploy Spatial $K$-Means: it executes in $3.2\text{ to }8.1\text{ milliseconds}$ with zero training and achieves the lowest worst-case RTT of $5.764\text{ ms}$. Second, for scale-free hub-and-spoke backbones requiring sub-millisecond computation, deploy Greedy $K$-Center in $0.026\text{ to }0.207\text{ milliseconds}$. Third, for offline strategic capacity planning where global minimum latency ($2.718\text{ ms}$ RTT) and bridge protection are paramount, deploy our Genetic Algorithm in $13\text{ to }76\text{ milliseconds}$. `[Emphasize]` Reserve pre-trained Deep $Q$-Networks for high-churn environments exceeding $60\text{ to }208$ reconfigurations where sub-millisecond forward passes amortize upfront training."

---

## SLIDE 14: Scope Boundaries, Limitations & Future Research Horizons
- **Rubric Mapping**: `Rubric Section 6: Specific Limitations & Justified Recommendations (Weight ×1 = 10 Marks)`
- **Slide Title**: Scope Boundaries, Limitations & Future Research Horizons
- **Subtitle**: Transparent Threats to Validity ($N \le 50$) and Master's-Level Extensions
- **On-Slide Content**:
  - **Scope Boundaries & Threats to Validity ($N \le 50$)**:
    1. **Fixed-Dimension MLP State Vector (`N -> 64 -> 64 -> N`)**: Bound to node count $N$ and normalized node degrees (Farahi et al., 2026); explains why zero-retraining DQN inference trails GA in post-churn latency ($2.287\text{ ms}$ vs. $1.450\text{ ms}$ on Internet2).
    2. **Single-Link ($N-1$) Failure Model**: Evaluates single-edge removals rather than correlated multi-link ($N-k$) fiber cuts or controller node crashes.
    3. **Single-Host Virtualized Emulation**: Models edge-weighted `TCLink` propagation and queuing jitter on a single Linux host rather than distributed hardware testbeds.
  - **Future Research Directions**:
    1. **Inductive Graph Neural Networks (GNNs)**: Replace fixed MLP layers with permutation-equivariant Message-Passing GNNs for zero-shot scale generalization across $N \in [100, 500]$ (Jadhav & Pujar, 2025; Kurra et al., 2025).
    2. **Time-Varying Traffic & East-West Raft Consensus**: Integrate live ONOS/Ryu NetFlow loads and distributed controller state-synchronization delays (Ali et al., 2025; Hechmi et al., 2025; Yue et al., 2022).
- **Ready-to-Speak Humanized Script (~145 words | ~1 min 10 sec)**:
  > "On Slide 14, in direct fulfillment of Section 6 of the scoring rubric, we transparently bound our conclusions and outline justified recommendations for future work. First, because we replicated the fixed-dimension MLP architecture of Farahi et al. (2026), the input and output layers are locked to node count $N$ and observe node degrees rather than message-passing over edge weights. That explains both why an MLP trained on $N=20$ cannot be applied zero-shot to $N=50$, and why its post-churn latency trails full Dijkstra heuristics. `[Pause]` Second, our survivability engine models $N-1$ single-link fiber cuts rather than correlated multi-link disasters or dynamic switch-migration queuing (Yue et al., 2022; Mystakidis et al., 2025). Consequently, the natural next step for Master's research is replacing the fixed MLP with an inductive Graph Neural Network across 100 to 500 nodes, coupled with live ONOS or Ryu east-west traffic telemetry (Ali et al., 2025; Jadhav & Pujar, 2025)."

---

## SLIDE 15: Conclusion, Objective Achievement & Dissemination Outputs
- **Rubric Mapping**: `Rubric Section 6 (Conclusions — 10 Marks) & Section 7 (Dissemination of Results — 10 Marks)`
- **Slide Title**: Conclusion, 7-Objective Achievement & Dissemination Outputs
- **Subtitle**: Full Alignment with UNIZULU 2026 Honours Research Scoring Rubric (100 Marks)
- **On-Slide Content**:
  - **1. All 7 Research Objectives Achieved ($100\%$ Verified, `22/22` Unit Tests Passing)**:
    - **Obj. 1–3 (Models, 5 Paradigms & SHA-256 Cache)**: 300 factorial runs ($F(4, 240) = 118.90, p < 0.0001$), 10,000 stability audit episodes (`0` divergences), & $46.4\%$ cache speedup.
    - **Obj. 4–5 (Static Pareto & Topology Sensitivity)**: Heuristics ($K$-Means $3.19\text{--}8.14\text{ ms}$, Greedy $0.026\text{--}0.207\text{ ms}$) & GA ($12.9\text{--}75.9\text{ ms}$) match or beat DRL ($t(8)=0.42, p=0.68$) with **zero training tax**.
    - **Obj. 6–7 (Mininet RTT, Dynamic Churn $T_{\text{break}}$ & Framework)**: Spearman $\rho = +1.00$ in 5-way Mininet RTT ($2.718\text{ ms}$ GA); $T_{\text{break}} = 59.0\text{--}65.2\text{ epochs}$ vs. GA; Phase 4 Gate Test ($2,875.49\text{ ms}$).
  - **2. Rubric Section 7 Dissemination Deliverables Submitted**:
    - **SATNAC 2026 IEEE Conference Paper**: `docs/SATNAC_RESEARCH_PAPER.pdf` (6-page IEEE double-column article targeting DHET-accredited SATNAC proceedings).
    - **UNIZULU Faculty Research Symposium Poster**: `poster/POSTER_Thabang_Mhlokoma_UNIZULU_2026.pdf`.
  - **Thank You! I warmly welcome questions from Prof. Mudali, Mr. Zwane, and the Examination Panel.**
- **Ready-to-Speak Humanized Script (~160 words | ~1 min 20 sec)**:
  > "To conclude on Slide 15: this study has systematically achieved all seven research objectives across 300 factorial observations, 10,000 multi-seed stability episodes, 1,000 dynamic link-churn states, and five-way Mininet emulation. `[Emphasize]` First, on static WANs up to 50 nodes, we proved that Genetic Algorithms and Spatial $K$-Means match or outperform Deep Reinforcement Learning in latency ($2.718\text{ ms}$ and $2.852\text{ ms}$ vs. $3.056\text{ ms}$ RTT) and bridge survivability without incurring an $11.4\text{ to }21.3\text{ second}$ training tax. Second, under dynamic link churn, we pinpointed the exact break-even horizon—**$59\text{ to }65\text{ epochs}$** against GA and **$146\text{ to }208\text{ epochs}$** against $K$-Means—where sub-millisecond DQN inference ($0.021\text{--}0.026\text{ ms}$) amortizes offline training. Third, in fulfillment of Section 7 of the UNIZULU Scoring Rubric on Dissemination of Results, we have prepared and submitted both a complete 6-page IEEE conference paper targeting SATNAC 2026 and an official UNIZULU Faculty Research Symposium poster alongside this dissertation. `[Pause]` Thank you, Prof. Mudali, Mr. Zwane, and members of the panel. I warmly welcome your questions."
