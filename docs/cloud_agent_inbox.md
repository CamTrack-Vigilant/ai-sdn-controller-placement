# Google AI Studio Cloud Agent Inbox (Turn 11)

- **Timestamp**: `2026-11-07T01:35:52.608977+00:00`
- **Model**: `gemini-4-argon` (`google-ai-studio-rest`)
- **Synchronized Commit**: `155c42ef21b47e978bf6e4c9ac271dfa71f771ab` (`add/metodology-annotated`, `610` tracked files)
- **Attached Files**: `['dissertation/06_references.md']`

## Local Agent Prompt

Design a complete 15-Slide BSc Honours Computer Science Viva Defense Presentation for Thabang Nhlokoma Buthelezi (230011908) presenting to Prof. Mudali, Mr. Zwane, and the UNIZULU examination panel. For every slide (Slides 1 to 15), provide: (1) Slide Title & Subtitle, (2) Concise on-slide bullet points / table / figure reference (Figures 3.1, 3.2, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6), and (3) A 100% natural, humanized, conversational spoken defense script (~120-160 words per slide, 18-20 minutes total) with delivery cues ([Pause], [Gesture to chart], [Emphasize]) and smooth spoken transitions between slides, grounded in all exact metrics and citing ONLY the attached 2021-2026 references.

## Cloud Agent Response

### `[CODEBASE_SYNC_STATUS]`
- **Active Branch**: `add/metodology-annotated`
- **HEAD Commit**: `155c42ef21b47e978bf6e4c9ac271dfa71f771ab`
- **Tracked File Manifest Count**: `610` files plus `dissertation/06_references.md` (verified 100% strict adherence to the 2021–2026 citation list).
- `REQUEST_FILES: []`

---

### `[CLOUD_AGENT_ANALYSIS]`

# 15-Slide BSc Honours Computer Science Viva Defense Presentation & Spoken Script
**Candidate:** Thabang Nhlokoma Buthelezi (`230011908`)  
**Institution:** Department of Computer Science, University of Zululand  
**Supervisors:** Prof. Pragasen Mudali and Mr. Skhumbuzo Zwane  
**Target Duration:** ~18–20 Minutes (~2,200 words at 115–120 wpm conversational academic pacing)  
**Citation Compliance:** Exclusively cites the 20 approved 2021–2026 references in `dissertation/06_references.md`.

---

## SLIDE 1: Title & Research Identity
- **Slide Title:** Decision-Grade Multi-Objective Benchmarking of DRL and Heuristic Controller Placement in Multi-Site Software Defined Networks
- **Subtitle:** BSc Honours Computer Science Mini-Dissertation Defense | University of Zululand
- **On-Slide Content:**
  - **Candidate:** Thabang Nhlokoma Buthelezi (Student No.: `230011908`)
  - **Supervisors:** Prof. P. Mudali & Mr. S. Zwane
  - **Core Focus:** Evaluating Deep Reinforcement Learning (PyTorch DQN & Bandit RL) against Evolutionary (GA), Clustering ($K$-Means), and Constructive ($K$-Center) Heuristics across Static & Dynamic SDN Topologies ($N \le 50$).
  - **Companion Output:** IEEE / SATNAC 2026 Full Conference Paper & 610-File Reproducible Benchmark Repository (`22/22` Unit Tests Passing).
- **Spoken Defense Script (~135 words):**
  > "Good morning Prof. Mudali, Mr. Zwane, and esteemed members of the examination panel. `[Pause]` My name is Thabang Buthelezi, and today I am proud to defend my BSc Honours mini-dissertation titled *Decision-Grade Multi-Objective Benchmarking of DRL and Heuristic Controller Placement in Multi-Site Software Defined Networks*. `[Emphasize]` Over the past five years, a wave of Software-Defined Networking studies has proposed Deep Reinforcement Learning to solve the Controller Placement Problem. Yet a critical question for real-world network engineers has remained largely unanswered: when we account for multi-second training overhead, single-link failure survivability, and kernel-level OpenFlow switching delays, does Deep Reinforcement Learning actually outperform classical heuristics on small-to-medium Wide Area Networks? `[Pause]` Today, I will walk you through a rigorous, 300-run factorial and 1,000-state dynamic churn investigation that answers this question definitively. Let us begin on Slide 2 with the operational problem."

---

## SLIDE 2: Problem Statement & The 2021–2026 Literature Gap
- **Slide Title:** The Controller Placement Problem (CPP) & Three Methodological Blind Spots
- **Subtitle:** Why Current AI-SDN Benchmarks Mislead Network Operators (2021–2026)
- **On-Slide Content:**
  - **The Multi-Site SDN Challenge:** Decoupling the control plane from data-plane switches (`OVSSwitch`) introduces propagation latency, load imbalance, and single-link failure vulnerability (Mohanty et al., 2021; Wang & Chen, 2021; Boudi, 2026).
  - **Blind Spot 1 — Single-Metric Myopia:** Optimizing propagation latency $L(P)$ alone places controllers on topological bridges, risking control-plane isolation under single-link cuts (Yusuf et al., 2023; Kazemi & Montazerolghaem, 2023).
  - **Blind Spot 2 — Conflating $\omega_{\text{train}}$ and $\tau_{\text{inf}}$:** Recent DRL studies—including MuZero (Benoudifa et al., 2023), CAPFUL (Kurra et al., 2025), and AP-DQN (Farahi et al., 2026)—highlight sub-millisecond forward inference ($\tau_{\text{inf}}$) while omitting or downplaying multi-second offline training cost ($\omega_{\text{train}}$).
  - **Blind Spot 3 — Unvalidated Graph Abstractions:** Pure graph distances ignore Open vSwitch kernel queuing and `TCLink` round-trip variation (Priya et al., 2025; Vardhan & SriBhargav, 2025).
  - **Visual Reference:** *Table 2.1 (Taxonomic Comparison of CPP Literature, 2021–2026)*.
- **Spoken Defense Script (~155 words):**
  > "Moving to Slide 2, when SDN decouples the control plane from forwarding switches across a multi-site WAN, every `Packet-In` and `Flow-Mod` message must traverse physical fiber links (Mohanty et al., 2021; Boudi, 2026). Where we place $k$ controllers determines both control-plane latency and fault tolerance (Wang & Chen, 2021; Xu et al., 2023). `[Gesture to slide]` When we audited the 2021-to-2026 literature summarized in Table 2.1, we uncovered three methodological blind spots. First, single-metric latency optimization frequently strands degree-one switches behind fragile bridge links (Yusuf et al., 2023). Second—and most critically—recent Deep Reinforcement Learning frameworks like MuZero by Benoudifa et al. (2023), CAPFUL by Kurra et al. (2025), and AP-DQN by Farahi et al. (2026) celebrate sub-millisecond inference speed while ignoring the massive upfront training tax required to learn the policy. Third, pure shortest-path models rarely validate whether graph rankings survive inside an emulated OpenFlow kernel. That brings us to our research questions on Slide 3."

---

## SLIDE 3: Research Questions, Objectives & Formal Hypotheses
- **Slide Title:** Research Questions, Specific Objectives & Falsifiable Hypotheses
- **Subtitle:** Bounding the Investigation to Static and Dynamic WANs ($N \le 50, k \in \{2, 3, 5\}$)
- **On-Slide Content:**
  - **RQ1 (Multi-Objective Trade-off):** How do Constructive ($K$-Center), Clustering ($K$-Means), Metaheuristic (GA), and RL/DRL paradigms trade off mean latency $L(P)$, $N-1$ reachability $Reach_{\text{avg}}(P)$, and compute cost ($\omega_{\text{train}}$ vs. $\tau_{\text{inf}}$)?
  - **RQ2 (Topological Sensitivity):** How does graph structure—scale-free Barabási-Albert hubs vs. planar Waxman meshes vs. real Internet2/ATT-MPLS backbones—govern algorithmic dominance?
  - **RQ3 (Emulation & Dynamic Churn):** Do graph-level rankings remain invariant under Mininet/OVS `TCLink` emulation, and after how many link-churn epochs ($T_{\text{break}}$) does pre-trained DQN inference amortize its upfront training cost?
  - **Formal Hypotheses Tested at $\alpha = 0.05$:**
    - $H_{01}$: No significant difference in mean control-plane latency across the five algorithm families ($\mu_{\text{Random}} = \mu_{\text{Greedy}} = \mu_{\text{K-Means}} = \mu_{\text{GA}} = \mu_{\text{DRL}}$).
    - $H_{11}$: At least one paradigm differs significantly, and multi-objective Pareto structure depends on topology and churn horizon.
- **Spoken Defense Script (~140 words):**
  > "On Slide 3, we translated these three blind spots into three falsifiable research questions and seven concrete objectives bounded to networks of up to 50 nodes. `[Pause]` Research Question 1 asks how our five algorithmic paradigms trade off propagation latency, $N-1$ single-link failure reachability, and explicitly separated training versus inference compute times. Research Question 2 investigates how graph structure—specifically scale-free hub-and-spoke networks versus planar spatial meshes and real carrier backbones—shifts algorithmic performance. `[Emphasize]` Research Question 3 asks two practical systems questions: first, do our graph-level rankings hold up inside a live Linux Mininet and Open vSwitch emulation? And second, under continuous link churn, how many topology changes does it take for a pre-trained PyTorch DQN to break even against re-running heuristics from scratch? Let us look at the mathematical framework we built to test these questions on Slide 4."

---

## SLIDE 4: Mathematical Formulation & Four-Phase Architecture
- **Slide Title:** Three-Axis Mathematical Formulation & Four-Phase Evaluation Pipeline
- **Subtitle:** Formalizing Latency, Menger $N-1$ Survivability, and Compute Decomposition
- **On-Slide Content:**
  - **Objective 1 — Mean Geodesic Latency ($L(P)\downarrow$):**
    $$L(P) = \frac{1}{|V|} \sum_{v \in V} \min_{c \in P} d_G(v, c)$$
  - **Objective 2 — Single-Link Failure Survivability ($Reach_{\text{avg}}(P)\uparrow$):**
    $$Reach_{\text{avg}}(P) = \frac{1}{|E| \cdot |V|} \sum_{e \in E} \sum_{v \in V} \mathbb{I}\!\left(\min_{c \in P} d_{G \setminus \{e\}}(v, c) < \infty\right)$$
  - **Objective 3 — Explicit Compute Decomposition ($\omega_{\text{train}}$ vs. $\tau_{\text{inf}}$):** Separating offline episode exploration from single-pass forward execution (Farahi et al., 2026).
  - **3D Pareto Dominance & Compromise Distance ($D_{\text{ideal}}$):** Weights $w_1 = 0.50, w_2 = 0.30, w_3 = 0.20$ with SHA-256 cached component bitmasks ($10^{-9}$ parity).
  - **Visual Reference:** *Figure 3.1 (`methodology_pipeline.png` — Four-Phase Experimental Architecture)*.
- **Spoken Defense Script (~150 words):**
  > "Slide 4 presents our mathematical formulation and the four-phase architecture shown in Figure 3.1. `[Gesture to Figure 3.1]` Every candidate placement $P$ of $k$ controllers is evaluated across three simultaneous axes. First, $L(P)$ measures the average shortest-path propagation delay from every switch to its nearest controller (Mohanty et al., 2021). Second, $Reach_{\text{avg}}(P)$ measures $N-1$ single-link failure survivability by systematically severing each edge $e \in E$ and computing the exact fraction of switches that retain a valid control path (Wang & Chen, 2021; Kazemi & Montazerolghaem, 2023). By Menger's Theorem, any 2-edge-connected graph guarantees 100 percent reachability, whereas graphs with bridge links suffer partitioning. `[Emphasize]` To make 10,000-episode reinforcement learning tractable, we engineered a SHA-256 topology-keyed connected-component cache verified to within $10^{-9}$ floating-point parity of exact Dijkstra recomputation. Let us now compare our five competing algorithms on Slide 5."

---

## SLIDE 5: The Five Competing Algorithmic Paradigms
- **Slide Title:** Five Algorithmic Paradigms & The Replicated AP-DQN Architecture
- **Subtitle:** Contrasting Zero-Training Heuristics Against Deep & Tabular Reinforcement Learning
- **On-Slide Content:**
  - **1. Seeded Random Baseline:** Uniform sampling without replacement ($O(k)$, lower-bound control).
  - **2. Greedy $K$-Center:** Deterministic farthest-first traversal minimizing worst-case radius ($O(k \cdot |E|\log|V|)$).
  - **3. Spatial $K$-Means Clustering:** Coordinate-space centroid partitioning ($n_{\text{init}}=10$) with nearest-node graph snapping (Xiao & Chen, 2021; Priya et al., 2025).
  - **4. Multi-Objective Genetic Algorithm (GA):** Tournament selection ($s=3$), elitism ($E=1$), uniform mutation ($p_m=0.15$) optimizing latency, tail delay, and $N-1$ reachability (Radam et al., 2022; Yusuf et al., 2023).
  - **5. Deep & Tabular Reinforcement Learning (DQN & Bandit RL):**
    - Replicated **AP-DQN** architecture (Farahi et al., 2026): PyTorch MLP ($N \to 64 \to 64 \to N$), Huber loss, target network sync $C=20$, replay buffer $|\mathcal{B}|=2,000$, and normalized reward:
      $$R(P) = 10 \cdot \left(\frac{L_{\max} - L(P)}{L_{\max}}\right) + 5 \cdot Reach_{\text{avg}}(P) \in [0, 15]$$
  - **Visual Reference:** *Figure 3.2 (`dqn_architecture_diagram.png` — Sequential Action-Masked PyTorch DQN)*.
- **Spoken Defense Script (~155 words):**
  > "On Slide 5, we place five distinct algorithmic families head-to-head on identical seeded topologies. Alongside our Random lower bound and deterministic Greedy $K$-Center, we evaluate Spatial $K$-Means clustering (Xiao & Chen, 2021; Priya et al., 2025) and an elitist Multi-Objective Genetic Algorithm inspired by hybrid evolutionary schemes (Radam et al., 2022; Yusuf et al., 2023). `[Gesture to Figure 3.2]` For our AI benchmark shown in Figure 3.2, we faithfully replicated the 2026 AP-DQN architecture of Farahi et al. (2026) in PyTorch. It uses a three-layer Multilayer Perceptron mapping an $N$-dimensional state vector—blending normalized node degree centrality with the active controller mask—through two 64-unit ReLU hidden layers to $N$ action $Q$-values.Invalid repeat selections are masked to $-10^9$. Notice the composite reward function at the bottom of the slide: it scales normalized latency improvement up to 10 points and $N-1$ reachability up to 5 points, giving a theoretical maximum reward of 15.0. Let us see how this DQN converges on Slide 6."

---

## SLIDE 6: Phase 1 Results — PyTorch DQN Convergence & Multi-Seed Stability Audit
- **Slide Title:** PyTorch DQN Convergence & 10-Run Multi-Seed Stability Audit
- **Subtitle:** Proving Authentic Neural Learning Before Claiming Negative Static Results
- **On-Slide Content:**
  - **1,000-Episode Pilot on Internet2 ($N=20, M=26, k=3$):**
    - Grand Mean Reward: **$13.055 \pm 0.589$** | Final-10 Episode Mean: **$13.199$** | Peak Reward: **$14.607 / 15.0$** ($L(P) = 1.420\text{ ms}, Reach_{\text{avg}} = 100.0\%$).
  - **Compute Cost Decomposition:**
    - Uncached Training Time ($\omega_{\text{train}}$): **$21.26\text{ s}$** ($21.26\text{ ms/ep}$).
    - Cached Training Time ($\omega_{\text{train}}$ with SHA-256 $N-1$ cache): **$11.40 \pm 0.11\text{ s}$** ($11.40\text{ ms/ep}$, a **$46.4\%$** speedup).
    - Post-Training Online Inference ($\tau_{\text{inf}}$): **$0.029\text{ ms}$** ($N=20$) and **$0.021\text{ ms}$** ($N=21$).
  - **10-Run Stability Audit (5 Seeds $\times$ 2 Canonical WANs = 10,000 Episodes, Table 4.1):**
    - Action Entropy: **$0.953\text{--}0.982$** | Moving-Average Variance: **$0.168\text{--}0.246$** | **`divergence_flag = False` across 10/10 runs**.
  - **Visual Reference:** *Figure 4.1 (`dqn_training_curve.png` — 1,000-Episode Convergence Profile)*.
- **Spoken Defense Script (~150 words):**
  > "Before a researcher can credibly argue that Deep Reinforcement Learning is outperformed by classical heuristics on static networks, they must first prove that their neural network actually converged and wasn't simply poorly tuned. `[Gesture to Figure 4.1]` Slide 6 and Figure 4.1 provide that proof. Across 1,000 training episodes on Internet2, our PyTorch DQN climbs rapidly during the initial epsilon-decay phase and stabilizes at a grand mean reward of $13.055$, a final-10-episode mean of $13.199$, and a peak reward of $14.607$ out of $15.0$, corresponding to a $1.420\text{ ms}$ latency and $100\%$ reachability. `[Emphasize]` Furthermore, across our 10-run multi-seed stability audit spanning 10,000 episodes on Internet2 and ATT-MPLS in Table 4.1, every single run achieved `divergence_flag = False`. Our SHA-256 component cache cut 1,000-episode training from $21.26\text{ seconds}$ down to $11.40\text{ seconds}$, while forward inference took just $0.021\text{ to }0.029\text{ milliseconds}$. Now, let us see what happens in the 300-run synthetic benchmark on Slide 7."

---

## SLIDE 7: Phase 2 Results — 300-Run Synthetic Factorial Benchmark ($N \in \{20, 50\}$)
- **Slide Title:** 300-Run Synthetic Factorial Sweep: Barabási-Albert vs. Waxman
- **Subtitle:** How Graph Topology Governs Algorithmic Performance (Tables 4.2 & 4.3)
- **On-Slide Content:**
  - **Experimental Design:** $5\text{ Algorithms} \times 2\text{ Topologies} \times 2\text{ Scales } (N \in \{20, 50\}) \times 3\text{ Budgets } (k \in \{2, 3, 5\}) \times 5\text{ Seeds} = \mathbf{300\text{ Runs}}$.
  - **Finding 1 — GA Dominates Latency in $12/12$ Cells ($100\%$):**
    - BA ($N=50, k=3$): GA **$4.247 \pm 0.089\text{ ms}$** ($\omega = 62.4\text{ ms}$) vs. RL **$4.650 \pm 0.019\text{ ms}$** ($\omega = 1,064.5\text{ ms}$).
    - Waxman ($N=50, k=3$): GA **$5.921 \pm 0.013\text{ ms}$** ($\omega = 56.2\text{ ms}$) vs. RL **$7.287 \pm 0.461\text{ ms}$** ($\omega = 438.2\text{ ms}$).
  - **Finding 2 — Structural Sensitivity of $K$-Means vs. Greedy $K$-Center:**
    - On planar **Waxman ($N=20, k=5$)**, $K$-Means achieves **$1.998\text{ ms}$** (`+52.46%` gain over Random), nearly matching GA (**$1.879\text{ ms}$**) in just $4.57\text{ ms}$.
    - On non-planar scale-free **Barabási-Albert ($N=20, k=2$)**, Euclidean centroid averaging misses the topological hub (`-10.73%`, **$7.885\text{ ms}$**), whereas Greedy $K$-Center locks onto hubs in $0.029\text{ ms}$ (**$6.083\text{ ms}$**).
  - **Visual Reference:** *Figure 4.2 (`latency_comparison.png` — Multi-Topology Latency Distribution)*.
- **Spoken Defense Script (~155 words):**
  > "Slide 7 presents the results of our 300-run synthetic factorial sweep across scale-free Barabási-Albert and planar Waxman topologies, illustrated in Figure 4.2 and Tables 4.2 and 4.3. `[Gesture to Figure 4.2]` Two striking patterns emerge. First, the Multi-Objective Genetic Algorithm achieves the lowest mean propagation latency in all 12 out of 12 factorial cells—for instance, $4.247\text{ ms}$ on 50-node Barabási-Albert and $5.921\text{ ms}$ on 50-node Waxman at $k=3$, executing in under $63\text{ milliseconds}$ while beating Reinforcement Learning in every cell. `[Emphasize]` Second, look at the structural contrast between $K$-Means and Greedy $K$-Center. On planar Waxman meshes at $N=20, k=5$, Euclidean proximity aligns with fiber path distance, allowing $K$-Means to reach $1.998\text{ ms}$—a $52.46\%$ improvement over Random. Yet on scale-free Barabási-Albert graphs at $N=20, k=2$, shortest paths jump across non-planar hub shortcuts; Euclidean averaging misses the hub and degrades to $7.885\text{ ms}$, whereas Greedy $K$-Center hits $6.083\text{ ms}$ in $29\text{ microseconds}$. Let us examine the statistical proof on Slide 8."

---

## SLIDE 8: Multi-Factor ANOVA, Post-Hoc Contrasts & Canonical WAN Parity
- **Slide Title:** Multi-Factor ANOVA ($N_{\text{obs}} = 300$) & Canonical WAN Evaluation
- **Subtitle:** Statistical Significance, Effect Sizes, and Menger Bridge Vulnerability
- **On-Slide Content:**
  - **Multi-Factor ANOVA Partitioning ($df_{\text{total}} = 299 = 8\text{ main} + 51\text{ interactions} + 240\text{ pure error}$):**
    - **Algorithm Family ($df=4$):** $F(4, 240) = \mathbf{118.90}, p < 0.0001$ (Rejects $H_{01}$).
    - **Network Scale $N$ ($df=1$):** $F(1, 240) = \mathbf{502.63}, p < 0.0001$ (Largest variance driver, $SS = 412.084$).
    - **Topology Family ($df=1$):** $F(1, 240) = \mathbf{249.21}, p < 0.0001$.
    - **Controller Budget $k$ ($df=2$):** $F(2, 240) = \mathbf{114.93}, p < 0.0001$.
  - **Post-Hoc Contrasts & Effect Sizes:**
    - Optimized vs. Random: Tukey HSD $p < 0.001$, Cohen's $d = \mathbf{1.42}$ (very large effect).
    - DRL/RL vs. $K$-Means on Canonical WANs: $t(8) = \mathbf{0.42}, p = \mathbf{0.68}$ (statistically indistinguishable in latency, despite RL's $10^2\text{--}10^3\times$ compute tax).
  - **Menger Theorem in Action ($Reach_{\text{avg}}$):**
    - Biconnected Internet2, ATT-MPLS, and BA ($m=2$): **$100.0\%$** reachability across all placements.
    - Sparse Waxman ($\bar{d} = 1.90\text{--}2.12$, bridge links): Drops to **$94.47\%\text{--}98.79\%$** (**$96.05\%\text{--}97.58\%$** for GA at $k=3$).
- **Spoken Defense Script (~150 words):**
  > "On Slide 8, we subject our 300 synthetic observations to a four-factor Analysis of Variance in Table 4.4b. `[Gesture to ANOVA bullets]` Partitioning the 299 total degrees of freedom into 8 main-effect degrees of freedom, 51 interaction degrees of freedom, and 240 pure within-cell error degrees of freedom reveals highly significant effects across all four factors: Algorithm Family yields $F(4, 240) = 118.90, p < 0.0001$, decisively rejecting our null hypothesis $H_{01}$. While optimized solvers beat Random with a massive Cohen's $d$ of $1.42$, a two-sample $t$-test between DRL and $K$-Means on our canonical WANs yields $t(8) = 0.42, p = 0.68$—statistically indistinguishable latency despite DRL's orders-of-magnitude higher training time. `[Emphasize]` Equally important is our $N-1$ survivability finding: on 2-edge-connected topologies like Internet2, ATT-MPLS, and Barabási-Albert, Menger's Theorem guarantees $100\%$ single-link failure reachability. On sparse Waxman graphs containing bridge links, however, reachability drops to $94.47\%\text{--}98.79\%$. Let us visualize this in 3D Pareto space on Slide 9."

---

## SLIDE 9: Three-Objective Pareto Frontier & Compute Scaling Analysis
- **Slide Title:** Three-Objective Pareto Dominance & Algorithmic Compute Scaling
- **Subtitle:** Why DRL Is Strictly Pareto-Dominated on Static Topologies ($N \le 50$)
- **On-Slide Content:**
  - **Weight-Free Pareto Dominance ($\succ$):**
    $$P_1 \succ P_2 \iff L(P_1) \le L(P_2) \land Reach_{\text{avg}}(P_1) \ge Reach_{\text{avg}}(P_2) \land \omega(P_1) \le \omega(P_2)$$
  - **Static Pareto Frontier Membership (`complete_proposal_aligned_benchmark.csv`):**
    - **Greedy $K$-Center:** Pareto-optimal in **$100\%$** of scenarios ($\tau = 0.026\text{--}0.207\text{ ms}$, zero training).
    - **Genetic Algorithm:** Pareto-optimal in **$100\%$** of scenarios ($\omega = 12.9\text{--}75.9\text{ ms}$, best latency & bridge resilience).
    - **Spatial $K$-Means:** Pareto-optimal on planar meshes ($\omega = 3.19\text{--}8.14\text{ ms}$, best tail latency).
    - **Bandit RL / PyTorch DQN:** Strictly Pareto-dominated by GA across **all 12 synthetic factorial cells** and ATT-MPLS ($\omega_{\text{train}} = 58.3\text{--}1,086.2\text{ ms}$ for Bandit RL; $11,400\text{--}21,260\text{ ms}$ for 1,000-ep DQN).
  - **Visual References:** *Figure 4.3 (`pareto_latency_reliability.png`) & Figure 4.5 (`execution_time.png` — Log-Scale Compute Costs)*.
- **Spoken Defense Script (~145 words):**
  > "Slide 9 combines Figure 4.3 and Figure 4.5 to show what happens when we evaluate Latency, $N-1$ Reachability, and Total Compute Cost simultaneously in 3D Pareto space. `[Gesture to Figures 4.3 and 4.5]` Remember that pure Pareto dominance is completely independent of user weights: one algorithm dominates another if it is at least as good on all three objectives and strictly better on at least one. Across all 12 synthetic factorial cells and ATT-MPLS, our Genetic Algorithm achieves strictly lower latency, equal or higher reachability, and orders-of-magnitude lower total execution time than Reinforcement Learning. `[Emphasize]` Look at the log-scale execution bars in Figure 4.5: Greedy $K$-Center finishes in under $0.21\text{ milliseconds}$, $K$-Means in $3.2\text{ to }8.1\text{ milliseconds}$, and GA in $12.9\text{ to }75.9\text{ milliseconds}$, whereas RL requires $58\text{ milliseconds}$ to $21.26\text{ seconds}$ of training. That raises Reviewer 3's crucial question on Slide 10: what about dynamic topology churn?"

---

## SLIDE 10: Phase 3 Results — Dynamic Topology Churn & Break-Even Amortization ($T_{\text{break}}$)
- **Slide Title:** 1,000-State Dynamic Link-Churn Experiment & Break-Even Horizon ($T_{\text{break}}$)
- **Subtitle:** Pinpointing When Pre-Trained DQN Inference Amortizes Offline Training (Table 4.6B)
- **On-Slide Content:**
  - **Experimental Design (`run_dynamic_churn_experiment.py`):**
    - Topologies: **Internet2 ($N=20, k=3$)** & **ATT-MPLS ($N=21, k=3$)** | **5 Seeds** $\times$ **$T_{\text{churn}} = 100$ Non-Bridge Link-Cut/Restore Epochs** = **$1,000$ Dynamic Graph States**.
    - Pre-trained PyTorch DQN (200-ep offline $\omega_{\text{train}} = 772.79\text{ ms}$ on Internet2; $921.69\text{ ms}$ on ATT-MPLS) executes **zero-retraining forward inference** ($\tau_{\text{DQN, inf}} = \mathbf{0.0257\text{ ms}}$ and $\mathbf{0.0213\text{ ms}}$) on updated state $s(G_t)$ vs. re-running heuristics from scratch at every epoch $t$:
      $$T_{\text{break}} = \left\lceil \frac{\omega_{\text{train}}}{\tau_{\text{algo}} - \tau_{\text{DQN, inf}}} \right\rceil$$
  - **5-Seed Empirical Break-Even Results (`dynamic_churn_summary.csv`):**

| Topology ($k=3$) | Paradigm | $\omega_{\text{train}}$ (ms) | Online $\tau$ (ms/ep) | $\Omega(100)$ (ms) | Mean $L(P_t)$ (ms) | $Reach_{\text{avg}}$ (%) | Break-Even $T_{\text{break}}$ (Epochs) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Internet2 ($N=20$)** | **PyTorch DQN** | $772.79$ | **$0.0257$** | $775.36$ | $2.287$ | $99.57\%$ | Baseline (Amortized) |
| **Internet2 ($N=20$)** | **Genetic Algorithm** | $0.00$ | $13.2030$ | $1320.30$ | **$1.450$** | $99.63\%$ | **$59.0$** ($42\text{--}101$) |
| **Internet2 ($N=20$)** | **Spatial $K$-Means** | $0.00$ | $5.2689$ | $526.90$ | $1.528$ | $99.63\%$ | **$145.8$** ($104\text{--}235$) |
| **Internet2 ($N=20$)** | **Greedy $K$-Center** | $0.00$ | $0.0497$ | **$4.97$** | $1.654$ | **$99.93\%$** | **$31,901.4$** ($23\text{k--}52.8\text{k}$) |
| **ATT-MPLS ($N=21$)** | **PyTorch DQN** | $921.69$ | **$0.0213$** | $923.81$ | $2.931$ | $99.98\%$ | Baseline (Amortized) |
| **ATT-MPLS ($N=21$)** | **Genetic Algorithm** | $0.00$ | $14.1233$ | $1412.34$ | **$2.317$** | $99.98\%$ | **$65.2$** ($44\text{--}84$) |
| **ATT-MPLS ($N=21$)** | **Spatial $K$-Means** | $0.00$ | $4.4728$ | $447.28$ | $2.904$ | $99.98\%$ | **$207.6$** ($147\text{--}276$) |
| **ATT-MPLS ($N=21$)** | **Greedy $K$-Center** | $0.00$ | $0.0725$ | **$7.25$** | $2.854$ | **$100.00\%$** | **$17,955.2$** ($11.3\text{k--}22.6\text{k}$) |

- **Spoken Defense Script (~160 words):**
  > "Slide 10 presents one of the most important contributions of our study: our 1,000-state Dynamic Topology Churn experiment in Section 4.1.6 and Table 4.6B, motivated by dynamic SDN mobility and reconfiguration challenges (Hechmi et al., 2025; Kurra et al., 2025). `[Gesture to Table 4.6B]` Here, we pre-trained our PyTorch DQN once on the base topology and then subjected Internet2 and ATT-MPLS to 100 sequential link-cut and link-restoration epochs across 5 seeds. At each epoch $t$, the pre-trained DQN updated its placement via a single forward pass in just $0.0213\text{ to }0.0257\text{ milliseconds}$ without retraining, whereas GA, $K$-Means, and Greedy had to re-solve from scratch. `[Emphasize]` Look at the right-most column: DQN amortizes its upfront training cost after an average of **$59.0\text{ epochs}$** on Internet2 and **$65.2\text{ epochs}$** on ATT-MPLS against GA, and after **$145.8\text{ to }207.6\text{ epochs}$** against $K$-Means! However, because our MLP state vector only observes normalized node degrees rather than full perturbed shortest paths, its post-churn latency ($2.287\text{ ms}$) still trails GA ($1.450\text{ ms}$). Let us move to Slide 11 for our Mininet validation."

---

## SLIDE 11: Phase 4 Results — Five-Way Mininet / Open vSwitch Emulation
- **Slide Title:** Phase 4 Five-Way Mininet & Open vSwitch (`OVSSwitch`) Emulation
- **Subtitle:** Validating Graph-Level Rankings Under Edge-Weighted `TCLink` Kernel Queuing (Table 4.5)
- **On-Slide Content:**
  - **Edge-Weighted `TCLink` Parameterization (`simulation/mininet_simulation.py`):**
    $$d_{\text{tc}}(u, v) = \max(0.10\text{ ms}, 2.0 \times w(u, v)), \quad \text{jitter} = \pm 0.5\text{ ms}, \quad d_{\text{access}} = 0.10\text{ ms}$$
  - **Five-Way Emulated Control-Plane RTT on Internet2 ($N=20, M=26, k=3$):**
    1. **Genetic Algorithm (`[3, 12, 17]`):** Graph $L(P) = \mathbf{1.403\text{ ms}} \to$ Mininet Mean RTT $= \mathbf{2.718\text{ ms}}$ | Worst RTT $= 6.903\text{ ms}$.
    2. **Spatial $K$-Means (`[3, 9, 17]`):** Graph $L(P) = \mathbf{1.469\text{ ms}} \to$ Mininet Mean RTT $= \mathbf{2.852\text{ ms}}$ | Worst RTT $= \mathbf{5.764\text{ ms}}$ *(Best Tail RTT)*.
    3. **Greedy $K$-Center (`[3, 11, 16]`):** Graph $L(P) = \mathbf{1.511\text{ ms}} \to$ Mininet Mean RTT $= \mathbf{2.934\text{ ms}}$ | Worst RTT $= 6.664\text{ ms}$.
    4. **Bandit RL / DQN (`[4, 9, 17]`):** Graph $L(P) = \mathbf{1.564\text{ ms}} \to$ Mininet Mean RTT $= \mathbf{3.056\text{ ms}}$ | Worst RTT $= 6.718\text{ ms}$.
    5. **Random Baseline (`[4, 5, 19]`):** Graph $L(P) = \mathbf{1.734\text{ ms}} \to$ Mininet Mean RTT $= \mathbf{3.374\text{ ms}}$ | Worst RTT $= 6.944\text{ ms}$.
  - **Strict Ordinal Ranking Invariance:** Spearman Rank Correlation $\rho = \mathbf{+1.00}$ ($GA \prec \text{K-Means} \prec \text{Greedy} \prec \text{DRL} \prec \text{Random}$).
  - **Visual Reference:** *Figure 4.4 (`mininet_vs_graph_latency.png` — Analytical vs. Emulated RTT)*.
- **Spoken Defense Script (~150 words):**
  > "On Slide 11, we address Research Question 3 by deploying all five converged placements into a live Linux Mininet emulation using Open vSwitch kernel bridges and `TCLink` traffic control on Internet2, shown in Figure 4.4 and Table 4.5. `[Gesture to Figure 4.4]` Each virtual link scales the analytical geodesic edge weight by $2.0\times$ with a $0.10\text{ ms}$ floor and $\pm 0.5\text{ ms}$ uniform jitter to model round-trip `Packet-In` and `Flow-Mod` exchanges under kernel queuing (AlQaruty et al., 2025; Jaadouni & Saadi, 2025). `[Emphasize]` Look at the resulting ordering: Genetic Algorithm achieves the lowest mean emulated RTT at **$2.718\text{ ms}$**, followed by $K$-Means at **$2.852\text{ ms}$**—which also secures the lowest worst-case tail RTT of **$5.764\text{ ms}$**—then Greedy $K$-Center at **$2.934\text{ ms}$**, DRL at **$3.056\text{ ms}$**, and Random at **$3.374\text{ ms}$**. The Spearman rank correlation between one-way NetworkX latency and emulated OpenFlow RTT is $+1.00$, proving strict ordinal invariance. Slide 12 explains why we ran Mininet post-hoc."

---

## SLIDE 12: The Phase 4 Mininet "2-Second Gate Test" & Systems Overhead Breakdown
- **Slide Title:** The Phase 4 Mininet "2-Second Gate Test" (`mininet_overhead_validation.json`)
- **Subtitle:** Why Embedding Live OVS Teardown Inside 10,000 RL Training Episodes Is Methodologically Flawed
- **On-Slide Content:**
  - **Gate Criterion (Section 3.4.3):** Per-episode Mininet lifecycle must remain $< 2,000\text{ ms}$ to justify in-the-loop RL episode resets.
  - **Empirical 3-Trial Breakdown on Internet2 ($N=11, M=18, k=3$, Table 4.6):**
    - **Phase A (Topology Instantiation):** $662.28 \pm 6.45\text{ ms}$ (**$23.03\%$**)
    - **Phase B (Controller Binding & OVS Bridge Startup):** $137.69 \pm 1.15\text{ ms}$ (**$4.79\%$**)
    - **Phase C (`iperf3` $0.2\text{ s}$ Active Control/Data Burst):** $89.86 \pm 2.42\text{ ms}$ (**$3.13\%$**)
    - **Online Control Loop Subtotal (A + B + C):** **$889.82 \pm 8.33\text{ ms}$** (**$30.94\%$**)
    - **Phase D (OVS Bridge Cleanup & Namespace Teardown `mn -c`):** **$1,985.68 \pm 89.20\text{ ms}$** (**$69.06\%$**)
    - **Full Lifecycle Total (A + B + C + D):** **$2,875.49 \pm 91.50\text{ ms}$** (`exceeds_threshold: 3/3`, `decision: WARN`).
- **Spoken Defense Script (~140 words):**
  > "An external examiner might reasonably ask: why did we train our PyTorch DQN on cached NetworkX graphs and validate in Mininet post-hoc, rather than running Mininet inside all 10,000 training episodes? `[Pause]` Slide 12 and Table 4.6 give the exact quantitative answer from our Phase 4 Two-Second Gate Test. When we instrumented a single Mininet episode across four lifecycle phases, the active OpenFlow control loop—Phases A, B, and C—took $889.82\text{ milliseconds}$. `[Emphasize]` However, Phase D—tearing down Linux network namespaces and deleting Open vSwitch bridges via `mn -c`—consumed **$1,985.68\text{ milliseconds}$**, or **$69.06\%$** of the **$2,875.49\text{ ms}$** total per-episode runtime! Because all three trials breached our $2,000\text{ ms}$ gate threshold, running 10,000 episodes inside Mininet would spend nearly 8 hours measuring Linux kernel bridge teardown rather than neural policy optimization. Let us synthesize these findings into our operator decision framework on Slide 13."

---

## SLIDE 13: Decision-Grade Algorithm Selection Framework for SDN Operators
- **Slide Title:** Decision-Grade Paradigm Selection Matrix for SDN Engineers
- **Subtitle:** Matching Algorithmic Complexity to Topology Structure, Latency SLA, and Churn Rate (Table 4.7)
- **On-Slide Content:**
  - **Regime 1 — Offline Capacity Planning & Sparse Bridge-Prone Meshes ($N \le 50$):**
    - **Deploy:** **Multi-Objective Genetic Algorithm (GA)** ($\omega = 12.9\text{--}75.9\text{ ms}$, lowest mean RTT $2.718\text{ ms}$, protects Waxman bridges $96.1\%\text{--}97.6\%$).
  - **Regime 2 — Fast Regional Planar Re-Clustering & Tail-Latency SLA ($N \le 50$):**
    - **Deploy:** **Spatial $K$-Means Clustering** ($\omega = 3.19\text{--}8.14\text{ ms}$, zero training, best Mininet worst-case tail RTT $5.764\text{ ms}$).
  - **Regime 3 — Scale-Free Hub-and-Spoke Core or Sub-Millisecond Emergency Failover:**
    - **Deploy:** **Greedy $K$-Center** ($\tau = 0.026\text{--}0.207\text{ ms}$, zero training, $100\%$ Pareto frontier membership).
  - **Regime 4 — High-Frequency Topology Churn ($T_{\text{churn}} > 60\text{--}208$ Reconfigurations):**
    - **Deploy:** **Pre-Trained PyTorch DQN** ($\tau_{\text{inf}} = 0.021\text{--}0.026\text{ ms}$, amortizing $\omega_{\text{train}}$ after $T_{\text{break}} = 59.0\text{--}65.2$ epochs vs. GA and $145.8\text{--}207.6$ epochs vs. $K$-Means).
  - **Visual Reference:** *Figure 4.6 (`decision_framework_flowchart.png` — Operator Decision Flowchart)*.
- **Spoken Defense Script (~145 words):**
  > "Slide 13 distills our entire empirical study into the actionable decision flowchart in Figure 4.6 and Table 4.7 for national research backbones like SANReN and regional telecom operators (Ali et al., 2025; Boudi, 2026). `[Gesture to Figure 4.6]` First, if an engineer is performing offline capacity planning on a static WAN up to 50 nodes—especially a sparse mesh with bridge links—they should deploy our Multi-Objective Genetic Algorithm: it finishes in under $76\text{ milliseconds}$ and delivers the lowest mean RTT of $2.718\text{ ms}$. Second, if minimizing worst-case tail RTT ($5.764\text{ ms}$) on a planar regional mesh is the priority, deploy Spatial $K$-Means in $3\text{ to }8\text{ milliseconds}$. Third, for sub-millisecond failover on a hub-and-spoke core, deploy Greedy $K$-Center ($0.026\text{--}0.207\text{ ms}$). `[Emphasize]` Finally, pre-trained DRL is justified only when a fixed-node network undergoes more than $60\text{ to }208$ sequential link-churn events between training cycles. Slide 14 outlines our scope boundaries."

---

## SLIDE 14: Methodological Limitations & Future Research Horizons
- **Slide Title:** Scope Boundaries, Limitations & Future Research Directions
- **Subtitle:** Extending from Fixed-Dimension MLPs ($N \le 50$) to Inductive Graph Neural Networks ($N > 100$)
- **On-Slide Content:**
  - **Limitation 1 — Fixed-Dimension MLP State Vector ($N \to 64 \to 64 \to N$):**
    - Weight matrices $W_1 \in \mathbb{R}^{64 \times N}$ and $W_3 \in \mathbb{R}^{N \times 64}$ are locked to node count $N$ and blend placement masks with *unweighted node degree*, explaining why zero-retraining DQN trails GA in post-churn latency ($2.287\text{ ms}$ vs. $1.450\text{ ms}$ on Internet2).
  - **Limitation 2 — Homogeneous Controller Capacity & Unweighted Switch Load:**
    - Dynamic flow migration and heterogeneous CPU queuing (Yue et al., 2022; Hechmi et al., 2025; Mystakidis et al., 2025) are bounded outside the topological placement layer.
  - **Future Direction 1 — Permutation-Equivariant Graph Neural Networks (GNNs):**
    - Replace the fixed MLP with edge-conditioned Message-Passing GNNs over $N \in [100, 500]$ for zero-shot cross-topology generalization (Kurra et al., 2025; Jadhav & Pujar, 2025).
  - **Future Direction 2 — Live Ryu / ONOS Distributed East-West Telemetry:**
    - Couple GNN-DRL with time-varying traffic matrices and energy-aware sleep scheduling (Ali et al., 2025; Jadhav & Pujar, 2025).
- **Spoken Defense Script (~140 words):**
  > "On Slide 14, we candidly examine the boundaries of our study and chart the path for future work. First, because we replicated the fixed-dimension MLP architecture of Farahi et al. (2026), the input and output layers are dimensionally bound to node count $N$ and rely on normalized node degrees rather than message passing over edge weights. That explains both why a model trained on $N=20$ cannot be transferred zero-shot to $N=50$, and why its post-churn latency trails full shortest-path heuristics. `[Pause]` Second, our benchmark models topological propagation and $N-1$ link survivability rather than dynamic switch-migration queuing (Yue et al., 2022; Mystakidis et al., 2025). Consequently, the natural next step for Master's-level research is replacing the MLP with an inductive, edge-aware Graph Neural Network over $100\text{ to }500$ nodes, coupled with live ONOS or Ryu east-west traffic telemetry (Ali et al., 2025; Jadhav & Pujar, 2025). Let us conclude on Slide 15."

---

## SLIDE 15: Conclusion & Key Contributions Summary
- **Slide Title:** Conclusion & Summary of Original Contributions
- **Subtitle:** Rigorous Empirical Clarity for AI-Driven Software Defined Networking
- **On-Slide Content:**
  - **1. Complete Three-Axis Benchmark ($N \le 50$):** Evaluated 5 paradigms across 300 synthetic factorial runs, 10,000 stability audit episodes, 1,000 dynamic link-churn states, and live Mininet/OVS emulation (`22/22` unit tests passing).
  - **2. Decisive Static Finding ($p < 0.0001$):** On static WANs ($N \le 50$), GA ($12.9\text{--}75.9\text{ ms}$) and $K$-Means ($3.19\text{--}8.14\text{ ms}$) strictly dominate or match DRL in latency ($t(8)=0.42, p=0.68$) and Mininet RTT ($2.718\text{ ms}$ and $2.852\text{ ms}$ vs. $3.056\text{ ms}$) without the $11.40\text{--}21.26\text{ s}$ DQN training tax.
  - **3. Exact Dynamic Churn Break-Even Horizon ($T_{\text{break}}$):** Proved that pre-trained DQN online inference ($\tau_{\text{inf}} = 0.021\text{--}0.026\text{ ms}$) amortizes its upfront training cost after **$T_{\text{break}} = 59.0\text{--}65.2\text{ epochs}$** vs. GA and **$145.8\text{--}207.6\text{ epochs}$** vs. $K$-Means.
  - **4. Systems & Reproducibility Legacy:** Established the Phase 4 Mininet 2-Second Gate Test ($2,875.49\text{ ms}$; $69.06\%$ teardown) and SHA-256 $N-1$ component caching ($46.4\%$ training speedup).
  - *Thank you. I now welcome questions from Prof. Mudali, Mr. Zwane, and the Examination Panel.*
- **Spoken Defense Script (~145 words):**
  > "To conclude on Slide 15: this mini-dissertation set out to bring rigorous, decision-grade clarity to AI-based controller placement in Software-Defined Networks. `[Emphasize]` First, across 300 factorial runs and five-way Mininet emulation, we proved that on static WANs up to 50 nodes, classical Genetic Algorithms and Spatial $K$-Means outperform or match Deep Reinforcement Learning in latency ($2.718\text{ ms}$ and $2.852\text{ ms}$ vs. $3.056\text{ ms}$ RTT) and bridge survivability without incurring an $11.4\text{ to }21.3\text{ second}$ training tax. Second, across 1,000 dynamic link-churn states, we established the exact break-even horizon—**$59\text{ to }65\text{ epochs}$** against GA and **$146\text{ to }208\text{ epochs}$** against $K$-Means—where sub-millisecond DQN inference ($0.021\text{--}0.026\text{ ms}$) amortizes offline training. `[Pause]` Thank you, Prof. Mudali, Mr. Zwane, and members of the panel, for your guidance and attention. I now warmly welcome your questions."

---

### `[ACTION_ITEMS_FOR_LOCAL_AGENT]`

1. **Save the Presentation Deck & Script Artifact**:
   - Save this complete 15-slide presentation outline and humanized spoken script to `docs/VIVA_PRESENTATION_15_SLIDES_AND_SCRIPT.md` so the candidate can rehearse directly from it alongside the figures in `results/figures/` (`Figure 3.1` to `Figure 4.6`).
2. **Optional Slide Deck Compilation**:
   - If desired, you can compile `docs/VIVA_PRESENTATION_15_SLIDES_AND_SCRIPT.md` into a PowerPoint (`.pptx`) or Beamer PDF slide deck embedding the 8 figures (`methodology_pipeline.png`, `dqn_architecture_diagram.png`, `dqn_training_curve.png`, `latency_comparison.png`, `pareto_latency_reliability.png`, `mininet_vs_graph_latency.png`, `execution_time.png`, and `decision_framework_flowchart.png`).
