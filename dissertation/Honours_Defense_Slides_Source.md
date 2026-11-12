---
title: "Decision-Grade Multi-Objective Benchmarking of AI and Heuristic Controller Placement in Multi-Site Software Defined Networks"
subtitle: "BSc Honours in Computer Science Mini-Dissertation Defense | University of Zululand (2026) | Aligned with UNIZULU 2026 Scoring Rubric (100 Marks)"
author: "Thabang Nhlokoma Buthelezi (230011908) | Supervisors: Prof. P. Mudali & Mr. S. Zwane | Dissemination: SATNAC 2026 Paper & Poster"
date: "November 2026"
---

# Slide 2: The Controller Placement Problem & Literature Gap (2021–2026)

- **Multi-Site WAN Challenge**: Decoupling the control plane from OpenFlow switches introduces propagation delay L(P) and single-link (N−1) cut vulnerability (Mohanty et al., 2021; Wang & Chen, 2021; Boudi, 2026).
- **Three Blind Spots (2021–2026)**: (1) *Single-Metric Myopia* strands switches behind bridges (Yusuf et al., 2023); (2) *Conflating Training (ω_train) & Inference (τ_inf)* in DRL (Benoudifa et al., 2023; Kurra et al., 2025; Farahi et al., 2026); (3) *Unvalidated Graph Models* omit OVS queuing (Priya et al., 2025).

| Study (2021–2026) | Primary Method | Latency L(P) | N−1 Link Reliability | ω_train vs. τ_inf | Mininet RTT | 3D Pareto |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| Mohanty et al. (2021) | k-Center Heuristic | Yes | No | Omitted | No | No |
| Wang & Chen (2021) | Link-Failure Foresight | Yes | Yes | Omitted | No | No |
| Radam et al. (2022) | Hybrid HSA-PSO | Yes | Partial | Omitted | No | Partial |
| Benoudifa et al. (2023) | MuZero DRL | Yes | No | Omitted | No | No |
| Yusuf et al. (2023) | CPCSA Critical Switch | Yes | Yes | Omitted | Yes | No |
| Kurra et al. (2025) | CAPFUL Dynamic DRL | Yes | Partial | Omitted | Partial | No |
| Farahi et al. (2026) | AP-DQN (PyTorch DRL) | Yes | Partial | Omitted | No | No |
| **This Study (2026)** | **5-Way Benchmark** | **Yes** | **Yes (Reach_avg)** | **Yes (Separated)** | **Yes (5-Way)** | **Yes (2D/3D)** |

::: notes
[Slide 2 - Problem Statement & Literature Gap (~1 min 20 sec) | Rubric Sec. 1: Problem & Literature (10 Marks)]:
Moving to Slide 2—which addresses Section 1 of the Honours Scoring Rubric on Problem Formulation and Literature—when SDN decouples the control plane from forwarding switches across a multi-site WAN, every Packet-In and Flow-Mod message must traverse physical optical fiber links (Mohanty et al., 2021; Boudi, 2026). Where we place k controllers directly governs both control-plane latency and fault tolerance (Wang & Chen, 2021; Xu et al., 2023). [Gesture to Table 2.1] When we systematically audited the 2021-to-2026 literature in Table 2.1, we uncovered three methodological blind spots. First, optimizing propagation latency alone frequently strands peripheral switches behind fragile bridge links (Yusuf et al., 2023). Second—and most importantly—recent Deep Reinforcement Learning frameworks like MuZero by Benoudifa et al. (2023), CAPFUL by Kurra et al. (2025), and AP-DQN by Farahi et al. (2026) celebrate sub-millisecond inference speed while ignoring the multi-second offline training tax required to learn that policy. Third, pure shortest-path models rarely check whether graph rankings survive inside an emulated OpenFlow kernel. That brings us to our research questions on Slide 3.
:::

# Slide 3: Research Questions, 7 Objectives & Formal Hypotheses

- **RQ1 (→ Obj. 1, 2, 3, 4, 5)**: How do the 5 paradigms trade off L(P), N−1 reachability, and ω_train vs. τ_inf?
- **RQ2 (→ Obj. 1, 4, 5, 7)**: How does graph topology (scale-free BA, planar Waxman, WANs) govern dominance?
- **RQ3 (→ Obj. 3, 6, 7)**: Do graph rankings hold in Mininet/OVS RTT, and at what T_break does DQN amortize ω_train?
- **Hypotheses (α = 0.05, N ≤ 50)**: **H_01 (Null)**: No DRL latency gain; **H_11 (Alt.)**: Static ω_train leaves DRL dominated.

| Obj. | Specific Research Objective (Dissertation Sec. 1.4.2) | RQs | Primary Deliverable & Empirical Verification | Slide / Ch. |
| :--- | :--- | :---: | :--- | :---: |
| **Obj. 1** | Build Python benchmark pipeline (`Internet2`, `ATT-MPLS`, `BA`, `Waxman`) | **RQ1, RQ2** | Modular graph & SHA-256 cached N−1 engine (10⁻⁹ parity, 46.4% faster) | Slide 4 (Ch. 3) |
| **Obj. 2** | Implement 5 paradigms: Random, K-Center, K-Means, GA & PyTorch DQN | **RQ1** | Unified API across all 5 placement algorithms (22/22 unit tests pass) | Slide 5 (Ch. 3) |
| **Obj. 3** | Run 1,000-ep DQN pilot (`Internet2`) & 10-run stability audit (10k ep) | **RQ1, RQ3** | Converges in ~20 ep (13.199 mean); `divergence_flag = False` (10/10) | Slides 6–7 (Ch. 4) |
| **Obj. 4** | Execute 5 × 2 × 2 × 3 synthetic factorial matrix (N_obs = 300) & ANOVA | **RQ1, RQ2** | GA wins 12/12 cells; ANOVA F=118.90 (p<0.0001); DQN vs KM p=0.68 | Slides 8–9 (Ch. 4) |
| **Obj. 5** | Synthesize 2D & 3D Pareto frontiers across L(P), Reach_avg, and ω_train | **RQ1, RQ2** | Greedy K-Center (`BA`) & K-Means (`Waxman`) dominate static frontier | Slides 8–9 (Ch. 4) |
| **Obj. 6** | Validate 5 strategies in Mininet/OVS (`TCLink`) & 3-trial 2s Gate Test | **RQ3** | Exact rank parity (ρ=+1.00; GA 2.718 ms, KM 2.852 ms); Gate 2,876 ms | Slides 11–12 (Ch. 4) |
| **Obj. 7** | Formulate bounded deployment guide (N ≤ 50) & 1k-state churn T_break | **RQ2, RQ3** | Decision flowchart (N ≤ 50); DQN breaks even at T_break = 59–65 ep | Slides 10, 13 (Ch. 4–5) |

::: notes
[Slide 3 - Research Questions, 7 Specific Objectives & Hypotheses (~1 min 35 sec) | Rubric Sec. 1 (10 Marks)]:
On Slide 3, we present the explicit traceability matrix showing how our overarching research goal and three research questions map directly to our seven specific research objectives from Section 1.4.2 and our formal statistical hypotheses. [Pause] First, Research Question 1 asks how our five paradigms trade off propagation latency, N-1 link survivability, and offline training versus online inference compute time. As shown in the table, RQ1 is answered through Objective 1—constructing our automated Python pipeline and SHA-256 N-1 survivability engine; Objective 2—implementing all five placement paradigms under a unified interface; Objective 3—evaluating PyTorch DQN convergence over a 1,000-episode pilot and a 10-run multi-seed stability audit; Objective 4—executing our 300-run multi-factor ANOVA benchmark; and Objective 5—synthesizing the 2D and 3D Pareto frontiers. [Emphasize] Second, Research Question 2 investigates how graph structure—scale-free Barabási-Albert hubs versus planar Waxman meshes and real carrier backbones—governs algorithmic dominance, which is operationalized by Objectives 1, 4, 5, and 7. [Gesture to bottom of table] Third, Research Question 3 tests whether our graph rankings hold inside live Mininet OpenFlow emulation and under dynamic link churn. This is fulfilled by Objective 6—our five-way Mininet RTT validation and 3-trial 2-Second Gate Test—and Objective 7, which formulates our bounded deployment guidelines for N <= 50 and establishes the exact link-churn break-even horizon T_break. Together, these seven objectives test our null hypothesis H_01 against our alternative hypothesis H_11 at alpha = 0.05.
:::

# Slide 4: Comparative Methodology Workflow & Three-Axis Formulation

::::: columns
::: {.column width="52%"}
- **Three-Axis Metrics (Fig. 3.1 Legend)**:
  - **Latency ℓ = L(P) ↓**: Mean shortest-path delay (ms) (Mohanty et al., 2021).
  - **Reliability R = Reach_avg(P) ↑**: N−1 single-link cut survivability (0–1) (Wang & Chen, 2021).
  - **Complexity ω vs. τ_inf ↓**: Training (s/ep) vs. inference (ms) + SHA-256 cache (46.4% faster).
- **Fig. 3.1 Comparative Workflow Phases**:
  - **Phase 1 (Multi-Topology Iteration)**: `Internet2`, `ATT-MPLS`, `BA`, `Waxman` across k ∈ {2, 3, 5} & CPU thermal cooldown control.
  - **Heuristic Track (Blue) vs. DRL Loop (Green)**: 3-step offline heuristic deployment vs. closed-loop PyTorch DQN Action–Reward–State training (**no cross-seeding** of DRL priors).
  - **Phase 3 & 4 (Validation & Planner Matrix)**: Data fusion → ANOVA/Tukey HSD, Pareto-front synthesis (ℓ vs. R vs. τ), ranking stability, & Scenario-Conditioned Selection Matrix (UNIZULU ethics compliant).
:::
::: {.column width="48%"}
![Figure 3.1: Heuristic vs. DRL Comparative Research Workflow.](docs/figures/proposal_methodology_workflow.png)
:::
:::::

::: notes
[Slide 4 - Comparative Workflow Diagram, Three-Axis Formulation & Ethics (~1 min 40 sec) | Rubric Sec. 2: Analysis & Research Design (10 Marks)]:
On Slide 4, we address Section 2 of the scoring rubric—Analysis, Research Design, Reproducibility, and Ethics—by walking directly through our end-to-end comparative methodology workflow in Figure 3.1. [Gesture to Top-Right of Figure 3.1] Look first at Phase 1 in the top-right corner of the diagram: our experimental harness iterates across canonical carrier backbones—Internet2 and ATT-MPLS—as well as synthetic Barabási-Albert and Waxman topologies under controller budgets k = 2, 3, and 5, incorporating automatic CPU thermal cooldown controls so hardware throttling never distorts our timing measurements. [Gesture to Left Blue Column and Center Green Column] From Phase 1, the workflow splits into two strictly isolated tracks—and notice the white callout badge at the top: 'No cross-seeding: heuristic solutions are NOT used as DRL priors,' ensuring a completely fair, unassisted benchmark. In the left blue track, heuristic methods—Greedy K-Center, K-Means, and GA—take the topology input in Step 1, compute a placement offline in Step 2, and deploy into Mininet in Step 3 to measure static network performance. In the center green track, our PyTorch Deep Q-Network operates as a closed-loop agent: selecting placement actions, observing network state transitions, updating neural weights via reward backpropagation, and aggregating episodic metrics. [Gesture to Bottom-Left Legend] As shown in the bottom-left legend of Figure 3.1, both tracks collect three exact metrics: propagation latency l = L(P) in milliseconds, N-1 single-link reachability R = Reach_avg(P) in [0, 1] accelerated by 46.4% via our SHA-256 component cache, and computational complexity omega separated into training time per episode versus online inference tau. [Gesture to Bottom Orange and Red Blocks] Finally, Phase 3 fuses all outputs for Multi-Factor ANOVA and Tukey HSD testing, 3D Pareto-front synthesis, and Mininet ranking stability, which feed directly into Phase 4 in the bottom-right corner: our Scenario-Conditioned Selection Matrix for network planners. All experiments use fixed random seeds on non-human topologies in full compliance with UNIZULU ethics guidelines.
:::

# Slide 5: System Architecture & Five Competing Placement Paradigms

::::: columns
::: {.column width="52%"}
- **1. Random Baseline**: Seeded uniform sampling without replacement (`22/22` unit tests passing).
- **2. Greedy K-Center**: Farthest-first 2-approximation in O(kN) lookups (Mohanty et al., 2021; Vardhan & SriBhargav, 2025).
- **3. Spatial K-Means**: Coordinate partitioning with graph medoid snapping (Xiao & Chen, 2021; Priya et al., 2025).
- **4. Genetic Algorithm (GA)**: Tournament selection, uniform crossover, swap mutation p_m = 0.15 (Radam et al., 2022; Xu et al., 2023).
- **5. PyTorch DQN & Bandit RL**: Replicates AP-DQN (Farahi et al., 2026) — MLP `N → 64 → 64 → N`, α = 0.001, γ = 0.99, batch 32, replay 10,000:
  - Composite Reward: R(P) = 10 · (L_max − L(P)) / L_max + 5 · Reach_avg(P) ∈ [0, 15].
:::
::: {.column width="48%"}
![Figure 3.2: System Architecture of the Benchmark and Mininet Harness.](docs/figures/system_architecture_diagram.png)
:::
:::::

::: notes
[Slide 5 - System Architecture & Five Paradigms (~1 min 20 sec) | Rubric Sec. 2 (10 Marks) & Sec. 3: Implementation (30 Marks)]:
On Slide 5, we transition into Section 3 of the scoring rubric—Implementation and Experimentation, which carries the highest weight of 30 marks. [Gesture to Figure 3.2] We engineered all five placement paradigms inside a single modular Python and PyTorch architecture verified by 22 automated unit tests in test_metrics_and_algorithms.py. Alongside our seeded Random baseline and deterministic Greedy K-Center heuristic, we implemented Spatial K-Means clustering with discrete graph medoid snapping (Xiao & Chen, 2021; Priya et al., 2025) and an elitist Genetic Algorithm with swap mutation (Radam et al., 2022; Yusuf et al., 2023). [Emphasize] For our Deep Reinforcement Learning benchmark, we faithfully replicated the 2026 AP-DQN specification of Farahi et al. (2026) in PyTorch: a three-layer Multi-Layer Perceptron mapping an N-dimensional node-degree state vector through two 64-unit ReLU hidden layers to N action Q-values, trained with experience replay of 10,000 transitions and a target network optimizing the composite reward R(P) in [0, 15].
:::

# Slide 6: Phase 1 Results — PyTorch DQN 1,000-Episode Convergence

::::: columns
::: {.column width="48%"}
- **Canonical Internet2 (N = 20, M = 26, k = 3)**:
  - Rapid convergence within **~20 episodes** as ε decays (1.0 → 0.05).
  - **Grand Training Mean Reward**: **13.055 ± 0.589**
  - **Post-Convergence Final-10 Mean**: **13.199**
  - **Peak Episode Reward**: **14.607 / 15.0** (L(P) = 1.420 ms, Reach_avg = 100.0%).
- **Training vs. Inference Split**:
  - **Uncached ω_train**: **21.26 s** (21.26 ms/ep)
  - **Cached ω_train**: **11.40 s** (11.40 ms/ep, **46.4% faster**)
  - **Online Forward Pass τ_inf**: **0.029 ms**
:::
::: {.column width="52%"}
![Figure 4.1: PyTorch DQN 1,000-Episode Convergence on Internet2 (N=20, k=3).](results/dqn_1000_episodes_convergence.png)
:::
:::::

::: notes
[Slide 6 - PyTorch DQN 1,000-Episode Convergence (~1 min 15 sec) | Rubric Sec. 3: Implementation & Experimentation (30 Marks)]:
Continuing our Section 3 implementation verification on Slide 6: before any researcher can credibly argue that Deep Reinforcement Learning is outperformed by classical heuristics on static networks, they must first prove that their neural network genuinely converged and wasn't simply poorly tuned. [Gesture to Figure 4.1] Figure 4.1 provides that proof on the canonical 20-node Internet2 backbone. Across 1,000 training episodes, our PyTorch DQN climbs steeply during initial exploration and stabilizes within 20 episodes, achieving a grand training mean reward of 13.055 +/- 0.589, a final 10-episode rolling average of 13.199, and a peak reward of 14.607 out of 15.0—corresponding to 1.420 ms latency and 100% single-link reachability. [Emphasize] However, look at the compute breakdown: training those 1,000 episodes takes 21.26 seconds uncached—or 11.40 seconds with our SHA-256 component cache, a 46.4% speedup—before a single forward pass can execute in 0.029 milliseconds.
:::

# Slide 7: 10-Run Multi-Seed DQN Stability Audit (10,000 Episodes)

::::: columns
::: {.column width="48%"}
- **Multi-Seed Audit (`stability_summary.csv`)**:
  - **5 Seeds** {42, 123, 256, 512, 1024} × **2 Canonical WANs** (`Internet2`, `ATT-MPLS`) × 1,000 Ep.
- **Internet2 (N = 20, M = 26)**:
  - Mean Best Reward: **14.194 ± 0.063**
  - Rolling Mean (Last 100): **12.654 ± 0.348**
  - Training Rate: **11.40 ± 0.11 ms/ep**
- **ATT-MPLS (N = 21, M = 54)**:
  - Mean Best Reward: **14.854 ± 0.395**
  - Rolling Mean (Last 100): **12.557 ± 0.328**
  - Training Rate: **19.22 ± 6.31 ms/ep**
- **Result**: **`divergence_flag = False` in 10 / 10 runs** (Action Entropy 0.953–0.982).
:::
::: {.column width="52%"}
![Figure 4.2: Multi-Seed DQN Convergence and Rolling Reward Distribution.](results/rl_analysis/convergence_analysis.png)
:::
:::::

::: notes
[Slide 7 - Multi-Seed DQN Stability Audit (~1 min 10 sec) | Rubric Sec. 3: Implementation Verification (30 Marks)]:
A frequent flaw in reinforcement learning studies is cherry-picking a single favourable random seed. [Gesture to Figure 4.2] To rigorously verify our implementation under Section 3 of the rubric, Slide 7 and Figure 4.2 present our 10-run Multi-Seed Stability Audit across five independent random seeds on both Internet2 and the dense 21-node, 54-link ATT-MPLS backbone, totaling 10,000 training episodes. [Emphasize] Across all 10 audit runs in Table 4.1, zero gradient explosions or policy collapses occurred—divergence_flag remained False in 10 out of 10 runs. On Internet2, the agent achieved a tight mean best reward of 14.194 +/- 0.063, and on ATT-MPLS it reached 14.854 +/- 0.395, with normalized action entropy between 0.953 and 0.982. Having proved that our DRL implementation is stable and reproducible, let us examine our Section 4 Results and Discussion on Slide 8.
:::

# Slide 8: Phase 2 — 300-Run Synthetic Factorial Matrix (BA vs. Waxman)

::::: columns
::: {.column width="50%"}
- **Balanced 5 × 2 × 2 × 3 Matrix (N_obs = 300)**:
  - **GA Wins Raw Latency in 12 / 12 Cells (100%)**: Up to **55.29%** gain over Random on Waxman (N = 20, k = 5: **1.879 ms**) and **39.26%** on BA (N = 20, k = 3: **4.321 ms**).
  - **Scale-Free BA (m = 2)**: Greedy K-Center captures core hubs in **0.026–0.207 ms** (100% Pareto-optimal), whereas K-Means suffers 2D projection distortion at k = 2.
  - **Planar Waxman (α = 0.4)**: K-Means closely tracks GA (**1.998 ms** vs. **1.879 ms** at N = 20, k = 5) in **4.57 ms**.
  - **Static RL Dominated**: Upfront training (ω_train = 58.3–1086.2 ms) leaves RL Pareto-dominated across all 12 static cells.
:::
::: {.column width="50%"}
![Figure 4.3: Pareto Latency-Cost Trade-Off on Barabási-Albert (N=50, k=3).](results/graphs/latency_cost_pareto_20261017_052319/latency_cost_pareto_barabasi_albert_n50_k3_20261017_052319.png)
:::
:::::

::: notes
[Slide 8 - 300-Run Synthetic Factorial Matrix (~1 min 20 sec) | Rubric Sec. 4: Results & Discussion (10 Marks)]:
Slide 8 addresses Section 4 of the scoring rubric—Results and Discussion—through our 300-observation synthetic factorial benchmark comparing Barabási-Albert scale-free networks against Waxman spatial networks across N=20 and N=50, illustrated by the Pareto frontier in Figure 4.3. [Gesture to Figure 4.3] Three key findings emerge. First, our Genetic Algorithm achieved the lowest mean propagation latency in all 12 out of 12 synthetic factorial cells, reducing latency by up to 55.29% over Random and beating Reinforcement Learning in every single cell. [Emphasize] Second, graph topology dictates which fast heuristic excels: on scale-free Barabási-Albert graphs where degree-skewed hubs dominate, Greedy K-Center locks onto the central hubs in under 0.21 milliseconds and stays on the Pareto frontier in 100% of cells. Conversely, on planar Waxman meshes where link probability decays with Euclidean distance, Spatial K-Means closely matches GA in under 5 milliseconds. Third, when total training time is included on static graphs, RL is Pareto-dominated across all 12 synthetic cells.
:::

# Slide 9: Multi-Factor ANOVA (N_obs = 300) & 3D Pareto Surface

::::: columns
::: {.column width="54%"}
| Source of Variation (Table 4.4b) | SS | df | MS | F-Stat | p-Value / Result |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Algorithm Family** | 389.92 | 4 | 97.48 | **118.90** | **< 0.0001** |
| **Topology (BA vs WX)** | 204.31 | 1 | 204.31 | **249.21** | **< 0.0001** |
| **Node Scale (N)** | 412.08 | 1 | 412.08 | **502.64** | **< 0.0001** |
| **Budget (k)** | 188.45 | 2 | 94.23 | **114.93** | **< 0.0001** |
| **Within-Cell Error** | 196.77 | 240 | 0.82 | — | *(51 int. df)* |
| **Tukey HSD (GA/KM vs Rnd)** | — | 240 | — | **d = 1.42** | **p < 0.001 (Large)** |
| **Static DQN vs K-Means** | — | 8 | — | **t = 0.42** | **p = 0.68 (NS)** |
| **Menger N−1 Survivability** | Biconn: | **100%** | Waxman: | **94.5–98.8%** | Bridge Cuts |
:::
::: {.column width="46%"}
![Figure 4.5: 3D Multi-Objective Pareto Surface.](SDN_Pareto_3D_Print.png)
:::
:::::

::: notes
[Slide 9 - Multi-Factor ANOVA & 3D Pareto Surface (~1 min 15 sec) | Rubric Sec. 4: Statistical Analysis & Discussion (10 Marks)]:
On Slide 9, we formally test our hypotheses using Multi-Factor Analysis of Variance across all 300 observations in Table 4.4b, alongside our 3D Pareto surface in Figure 4.5. [Gesture to ANOVA table and Figure 4.5] Partitioning the 299 total degrees of freedom into 8 main-effect degrees of freedom, 51 interaction degrees of freedom, and 240 pure within-cell error degrees of freedom confirms highly significant effects across all four factors: Algorithm Family yields F(4, 240) = 118.90, p < 0.0001. Post-hoc Tukey HSD tests confirm a large effect size of Cohen's d = 1.42 over Random. [Emphasize] Yet a two-sample contrast between PyTorch DQN/RL and K-Means on static canonical runs yields t(8) = 0.42, p = 0.68—confirming our alternative hypothesis H_11 that multi-second DRL training buys no statistically significant latency gain on static networks! Furthermore, our N-1 engine proves 100% survivability on 2-edge-connected backbones versus 94.47% to 98.79% on bridge-prone Waxman graphs.
:::

# Slide 10: Phase 3 — Dynamic Link Churn & Amortization Horizon (T_break)

- **1,000-State Dynamic Churn Benchmark (`dynamic_churn_summary.csv`)**: 5 Seeds × 100 Sequential Non-Bridge Link-Churn Epochs on Internet2 & ATT-MPLS (k = 3).
- **Break-Even Horizon**: T_break = ⌈ω_train / (τ_algo − τ_DQN,inf)⌉ (200-ep cached pre-training, zero-retraining online forward passes in 0.021–0.026 ms/epoch).

| Topology (k=3) | Algorithm | Upfront ω_train (ms) | Online τ_inf (ms/ep) | Cumulative Ω(100) (ms) | Mean Churn L(P_t) (ms) | Reach_avg (%) | Break-Even T_break vs. DQN |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Internet2** | **PyTorch DQN (Inference)** | 772.79 | **0.0257** | 775.36 | 2.287 | 99.57% | Baseline Reference |
| **Internet2** | **Genetic Algorithm (GA)** | 0.00 | 13.2030 | 1320.30 | **1.450** | 99.63% | **59.0 epochs** (42–101) |
| **Internet2** | **K-Means Clustering** | 0.00 | 5.2689 | 526.90 | 1.528 | 99.63% | **145.8 epochs** (104–235) |
| **Internet2** | **Greedy K-Center** | 0.00 | 0.0497 | **4.97** | 1.654 | **99.93%** | **31,901.4 epochs** |
| **ATT-MPLS** | **PyTorch DQN (Inference)** | 921.69 | **0.0213** | 923.81 | 2.931 | 99.98% | Baseline Reference |
| **ATT-MPLS** | **Genetic Algorithm (GA)** | 0.00 | 14.1233 | 1412.34 | **2.317** | 99.98% | **65.2 epochs** (44–84) |
| **ATT-MPLS** | **K-Means Clustering** | 0.00 | 4.4728 | 447.28 | 2.904 | 99.98% | **207.6 epochs** (147–276) |
| **ATT-MPLS** | **Greedy K-Center** | 0.00 | 0.0725 | **7.25** | 2.854 | **100.00%** | **17,955.2 epochs** |

::: notes
[Slide 10 - Dynamic Link Churn & Break-Even Amortization (~1 min 25 sec) | Rubric Sec. 3 (30 Marks) & Sec. 4 (10 Marks)]:
Now, what happens when the network topology is NOT static? Slide 10 presents our 1,000-state Dynamic Topology Churn experiment in Section 4.1.6 and Table 4.6B, motivated by dynamic SDN reconfiguration studies (Hechmi et al., 2025; Kurra et al., 2025). [Gesture to Table 4.6B] Here, we pre-trained our PyTorch DQN once on the base topology and then subjected Internet2 and ATT-MPLS to 100 sequential link-cut and restoration epochs across 5 seeds. At each epoch t, the pre-trained DQN updated its placement via a single greedy forward pass in just 0.0213 to 0.0257 milliseconds without retraining, whereas GA, K-Means, and Greedy had to re-compute from scratch. [Emphasize] Look at the right-most column: DQN amortizes its upfront training cost after an average of 59.0 epochs on Internet2 and 65.2 epochs on ATT-MPLS against GA, and after 145.8 to 207.6 epochs against K-Means! Critically, however, because the replicated MLP state vector only observes node degrees rather than perturbed shortest paths, classical heuristics still maintain lower post-churn latency (1.450 ms vs. 2.287 ms).
:::

# Slide 11: Phase 4 — Five-Way Mininet OpenFlow RTT Validation

- **Emulation Calibration (`simulation/mininet_simulation.py`)**: Open vSwitch (`OVSSwitch`) + `TCLink` scaled via d_tc(u, v) = max(0.10 ms, 2.0 × w(u, v)) with ±0.5 ms uniform queuing jitter (AlQaruty et al., 2025; Jaadouni & Saadi, 2025).
- **Ordinal Ranking Invariance**: Exact Spearman rank correlation ρ = +1.00 (GA ≺ K-Means ≺ Greedy ≺ RL/DQN ≺ Random).

| Placement Strategy | Selected Controller Nodes (Internet2, N=20, k=3) | Mean Emulated RTT (ms) | Worst-Case RTT (ms) | Graph Latency L(P) (ms) | RTT Overhead vs. L(P) (ms) | N−1 Reliability |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Genetic Algorithm** | `['n1', 'n15', 'n16']` | **2.718 (Rank 1)** | 6.903 | 1.403 | +1.315 | 100.0% |
| **K-Means Clustering** | `['n1', 'n16', 'n9']` | **2.852 (Rank 2)** | **5.764 (Best Tail)** | 1.469 | +1.383 | 100.0% |
| **Greedy K-Center** | `['n1', 'n10', 'n6']` | 2.934 (Rank 3) | 6.664 | 1.511 | +1.423 | 100.0% |
| **Bandit RL / DQN** | `['n1', 'n10', 'n5']` | 3.056 (Rank 4) | 6.718 | 1.564 | +1.492 | 100.0% |
| **Random Baseline** | `['n13', 'n0', 'n18']` | 3.374 (Rank 5) | 6.944 | 1.734 | +1.640 | 100.0% |

::: notes
[Slide 11 - Five-Way Mininet Emulation (~1 min 15 sec) | Rubric Sec. 3 (30 Marks) & Sec. 4 (10 Marks)]:
On Slide 11, we answer Research Question 3 and strengthen our Section 3 systems experimentation by evaluating all five placements inside a live Linux Mininet and Open vSwitch emulation on Internet2 (N=20, k=3), reported in Table 4.5. [Gesture to Table 4.5] Each virtual Ethernet link configures TCLink delay as 2.0x the geodesic edge weight with a 0.10 ms access floor and +/- 0.5 ms uniform queuing jitter to capture round-trip control-channel traversal (AlQaruty et al., 2025; Jaadouni & Saadi, 2025). [Emphasize] Look at the emulated Round-Trip Times: the Genetic Algorithm achieves the lowest mean RTT at 2.718 milliseconds—a 19.4% reduction over Random—while Spatial K-Means achieves the second-lowest mean RTT at 2.852 ms and the best worst-case tail RTT at 5.764 ms. Both outperform Bandit RL / DQN at 3.056 ms. Most importantly, the ordinal ranking across all five paradigms matches our one-way Dijkstra metrics with a Spearman rank correlation of +1.00.
:::

# Slide 12: Phase 4 Mininet "2-Second Gate Test" (`mininet_overhead_validation.json`)

- **Pre-Experiment Gate Criterion (Section 3.4.3)**: Full Mininet lifecycle (Phases A+B+C+D) must execute in < 2,000 ms/episode to permit online Mininet-in-the-loop RL training.
- **Architectural Justification**: Running 1,000 episodes inside Mininet would spend **~48 minutes per seed** (69.06% in Linux OVS bridge teardown), validating two-stage cached graph training + post-hoc Mininet validation.

| Execution Phase (Internet2 11-PoP Core, k=3) | Trial 1 (ms) | Trial 2 (ms) | Trial 3 (ms) | Mean Overhead (ms) | Share of Lifecycle (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Phase A (Topology Instantiation)** | 695.86 | 638.98 | 651.99 | 662.28 | 23.03% |
| **Phase B (Controller Binding & OVS Start)** | 133.59 | 138.16 | 141.31 | 137.69 | 4.79% |
| **Phase C (`iperf3` 0.2 s Traffic Burst)** | 83.75 | 92.55 | 93.27 | 89.86 | 3.13% |
| **Phase D (OVS Cleanup & Teardown `mn -c`)** | 2,061.49 | 1,927.44 | 1,968.09 | **1,985.68** | **69.06%** |
| **Active Online Control Loop (A + B + C)** | 913.20 | 869.69 | 886.56 | **889.82** | 30.94% |
| **Full Lifecycle Overhead (A + B + C + D)** | **2,974.69** | **2,797.13** | **2,854.66** | **2,875.49** | **100.00% (`WARN`)** |

::: notes
[Slide 12 - Phase 4 Mininet 2-Second Gate Test (~1 min 15 sec) | Rubric Sec. 3: Systems Instrumentation (30 Marks)]:
An examiner evaluating Section 3 of the rubric might ask: why did we train our PyTorch DQN on cached NetworkX graphs and validate in Mininet post-hoc, rather than running Mininet inside every single RL training episode? [Pause] Slide 12 and Table 4.6 give the exact empirical answer from our Phase 4 Two-Second Gate Test. When we instrumented a single Mininet episode across four lifecycle phases on the 11-node Internet2 core, the active OpenFlow loop—Phases A, B, and C—averaged 889.82 milliseconds. [Emphasize] However, Phase D—stopping Open vSwitch bridges and cleaning Linux kernel namespaces via mn -c—consumed 1,985.68 milliseconds, or 69.06% of the 2,875.49 ms total per-episode lifecycle! Because all three trials exceeded our 2,000 ms gate threshold, embedding Mininet inside 10,000 training episodes would spend nearly 8 hours measuring Linux bridge teardown rather than neural learning.
:::

# Slide 13: Bounded Infrastructure Deployment Decision Framework (N ≤ 50)

::::: columns
::: {.column width="50%"}
- **1. Static Planar Regional Mesh (N ≤ 50)**:
  - **Deploy Spatial K-Means**: τ = 3.19–8.14 ms, zero training, best worst-case Mininet tail RTT (5.764 ms).
- **2. Scale-Free Hub-and-Spoke Core (N ≤ 50)**:
  - **Deploy Greedy K-Center**: τ = 0.026–0.207 ms, zero training, 100% Pareto frontier membership.
- **3. Offline Strategic Capacity Planning**:
  - **Deploy Genetic Algorithm (GA)**: τ = 12.9–75.9 ms, lowest mean latency (12/12 cells) & best mean RTT (2.718 ms).
- **4. High-Churn Topologies (T_churn > 60–208 Epochs)**:
  - **Deploy Pre-Trained PyTorch DQN**: τ_inf = 0.021–0.026 ms/ep, amortizing ω_train after T_break = 59.0–65.2 epochs vs. GA.
:::
::: {.column width="50%"}
![Figure 4.6: Bounded Infrastructure Deployment Decision Flowchart (N <= 50).](docs/figures/decision_framework_flowchart.png)
:::
:::::

::: notes
[Slide 13 - Bounded Decision Framework (~1 min 15 sec) | Rubric Sec. 6: Conclusions & Contributions (10 Marks)]:
Moving to Section 6 of the rubric—Conclusions and Contributions—Slide 13 translates our empirical findings into the bounded deployment decision flowchart in Figure 4.6 and Table 4.7 for networks up to 50 nodes (Ali et al., 2025; Boudi, 2026). [Gesture to Figure 4.6] First, for static regional planar meshes where average and tail latency matter, engineers should deploy Spatial K-Means: it executes in 3.2 to 8.1 milliseconds with zero training and achieves the lowest worst-case RTT of 5.764 ms. Second, for scale-free hub-and-spoke backbones requiring sub-millisecond computation, deploy Greedy K-Center in 0.026 to 0.207 milliseconds. Third, for offline strategic capacity planning where global minimum latency (2.718 ms RTT) and bridge protection are paramount, deploy our Genetic Algorithm in 13 to 76 milliseconds. [Emphasize] Reserve pre-trained Deep Q-Networks for high-churn environments exceeding 60 to 208 reconfigurations where sub-millisecond forward passes amortize upfront training.
:::

# Slide 14: Scope Boundaries, Limitations & Future Research Horizons

- **Scope Boundaries & Threats to Validity (N ≤ 50)**:
  1. **Fixed-Dimension MLP State Vector (`N → 64 → 64 → N`)**: Bound to node count N and normalized node degrees (Farahi et al., 2026); explains why zero-retraining DQN inference trails GA in post-churn latency (2.287 ms vs. 1.450 ms on Internet2).
  2. **Single-Link (N−1) Failure Model**: Evaluates single-edge removals rather than correlated multi-link (N−k) fiber cuts or controller node crashes.
  3. **Single-Host Virtualized Emulation**: Models edge-weighted `TCLink` propagation and queuing jitter on a single Linux host rather than distributed hardware testbeds.
- **Future Research Directions**:
  1. **Inductive Graph Neural Networks (GNNs)**: Replace fixed MLP layers with permutation-equivariant Message-Passing GNNs for zero-shot scale generalization across N ∈ [100, 500] (Jadhav & Pujar, 2025; Kurra et al., 2025).
  2. **Time-Varying Traffic & East-West Raft Consensus**: Integrate live ONOS/Ryu NetFlow loads and distributed controller state-synchronization delays (Ali et al., 2025; Hechmi et al., 2025; Yue et al., 2022).

::: notes
[Slide 14 - Limitations & Future Work (~1 min 10 sec) | Rubric Sec. 6: Specific Limitations & Recommendations (10 Marks)]:
On Slide 14, in direct fulfillment of Section 6 of the scoring rubric, we transparently bound our conclusions and outline justified recommendations for future work. First, because we replicated the fixed-dimension MLP architecture of Farahi et al. (2026), the input and output layers are locked to node count N and observe node degrees rather than message-passing over edge weights. That explains both why an MLP trained on N=20 cannot be applied zero-shot to N=50, and why its post-churn latency trails full Dijkstra heuristics. [Pause] Second, our survivability engine models N-1 single-link fiber cuts rather than correlated multi-link disasters or dynamic switch-migration queuing (Yue et al., 2022; Mystakidis et al., 2025). Consequently, the natural next step for Master's research is replacing the fixed MLP with an inductive Graph Neural Network across 100 to 500 nodes, coupled with live ONOS or Ryu east-west traffic telemetry (Ali et al., 2025; Jadhav & Pujar, 2025).
:::

# Slide 15: Conclusion, 7-Objective Achievement & Dissemination Outputs

- **1. All 7 Research Objectives Achieved (100% Verified, `22/22` Unit Tests Passing)**:
  - **Obj. 1–3 (Models, 5 Paradigms & SHA-256 Cache)**: 300 factorial runs (F(4, 240) = 118.90, p < 0.0001), 10,000 stability audit episodes (`0` divergences), & 46.4% cache speedup.
  - **Obj. 4–5 (Static Pareto & Topology Sensitivity)**: Heuristics (K-Means 3.19–8.14 ms, Greedy 0.026–0.207 ms) & GA (12.9–75.9 ms) match or beat DRL (t(8) = 0.42, p = 0.68) with **zero training tax**.
  - **Obj. 6–7 (Mininet RTT, Dynamic Churn T_break & Framework)**: Spearman ρ = +1.00 in 5-way Mininet RTT (2.718 ms GA); T_break = 59.0–65.2 epochs vs. GA; Phase 4 Gate Test (2,875.49 ms).
- **2. Rubric Section 7 Dissemination Deliverables Submitted**:
  - **SATNAC 2026 IEEE Conference Paper**: `docs/SATNAC_RESEARCH_PAPER.pdf` (6-page IEEE double-column article targeting DHET-accredited SATNAC proceedings).
  - **UNIZULU Faculty Research Symposium Poster**: `poster/POSTER_Thabang_Mhlokoma_UNIZULU_2026.pdf`.
- **Thank You! I warmly welcome questions from Prof. Mudali, Mr. Zwane, and the Examination Panel.**

::: notes
[Slide 15 - Conclusion, Objective Achievement & Dissemination (~1 min 20 sec) | Rubric Sec. 6 (10 Marks) & Sec. 7 (10 Marks)]:
To conclude on Slide 15: this study has systematically achieved all seven research objectives across 300 factorial observations, 10,000 multi-seed stability episodes, 1,000 dynamic link-churn states, and five-way Mininet emulation. [Emphasize] First, on static WANs up to 50 nodes, we proved that Genetic Algorithms and Spatial K-Means match or outperform Deep Reinforcement Learning in latency (2.718 ms and 2.852 ms vs. 3.056 ms RTT) and bridge survivability without incurring an 11.4 to 21.3 second training tax. Second, under dynamic link churn, we pinpointed the exact break-even horizon—59 to 65 epochs against GA and 146 to 208 epochs against K-Means—where sub-millisecond DQN inference (0.021 to 0.026 ms) amortizes offline training. Third, in fulfillment of Section 7 of the UNIZULU Scoring Rubric on Dissemination of Results, we have prepared and submitted both a complete 6-page IEEE conference paper targeting SATNAC 2026 and an official UNIZULU Faculty Research Symposium poster alongside this dissertation. [Pause] Thank you, Prof. Mudali, Mr. Zwane, and members of the panel. I warmly welcome your questions.
:::
