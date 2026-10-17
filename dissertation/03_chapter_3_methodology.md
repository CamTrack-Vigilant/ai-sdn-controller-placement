# CHAPTER THREE: 3.0 METHODOLOGY / DESIGN AND IMPLEMENTATION

## 3.1 RESEARCH DESIGN

This research employs a rigorous, **deductive, quantitative, and experimental benchmarking design** rooted in empirical computer science and multi-objective combinatorial optimization. Rather than evaluating algorithms in isolation under disparate assumptions, this study establishes a standardized, controlled experimental framework where all competing controller placement paradigms operate under identical topological representations, identical link latency models, and identical operational constraints.

The experimental workflow is designed to execute a **full factorial matrix evaluation** complemented by a **multi-seed reinforcement learning stability audit** and **virtualized hardware-emulated validation**. Figure 3.1 illustrates the end-to-end research methodology workflow, depicting the interaction between topology generation, algorithm execution, metric extraction, Pareto frontier synthesis, and Mininet OpenFlow emulation.

```
+---------------------------------------------------------------------------------------------------+
|                                   TOPOLOGY GENERATION & INTAKE                                    |
|   +------------------------------------+          +-------------------------------------------+   |
|   | Canonical WANs (Internet2, ATT)    |          | Synthetic Models (Barabasi-Albert, Waxman)|   |
|   +-----------------+------------------+          +---------------------+---------------------+   |
+---------------------|---------------------------------------------------|-------------------------+
                      |                                                   |
                      v                                                   v
+---------------------------------------------------------------------------------------------------+
|                                    FACTORIAL BENCHMARK HARNESS                                    |
|  Controlled Factors: Topology Type x Scale (N in {20, 50}) x Controller Budget (k in {2, 3, 5})   |
|                                                                                                   |
|  [Track A: Classical Heuristics]    [Track B: Metaheuristics]     [Track C: Deep RL (PyTorch DQN)]|
|   - Random Baseline                  - Genetic Algorithm           - Farahi Hyperparameters       |
|   - Greedy K-Center (Gonzalez)         (Crossover, Mutation,       - Replay Buffer (10k)          |
|   - K-Means Spatial Clustering          Elitism, Fitness Eval)     - 10-Seed Stability Audit      |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                  3-AXIS MULTI-OBJECTIVE EVALUATION                                |
|   1. Propagation Latency L(P) [ms]                                                                |
|   2. Control-Plane Reliability Reach_avg [N-1 Single-Link Failure Reachability Engine]            |
|   3. Computational Complexity Tax omega [CPU Execution Runtime in ms / seconds per episode]       |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                               STATISTICAL INFERENCE & DECISION SYNTHESIS                          |
|   - Non-Dominated 3D Pareto Frontier Synthesis & Ideal Point Compromise Distance Ranking          |
|   - Two-Way Factorial ANOVA & Tukey HSD Statistical Significance Contrasts                        |
|   - Scenario-Conditioned Method Selection Guidance Framework                                      |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                              PHASE 4 MININET OPENFLOW HARDWARE EMULATION                          |
|   - Virtualized Open vSwitch (OVS) Kernel Topology                                                |
|   - Live Remote OpenFlow Controllers (127.0.0.1:6633+)                                            |
|   - 2-Second Gate Test: Online Control-Loop Overhead vs. Operating System Teardown Tax           |
|   - Real-World Ping RTT Verification across Synthesized Placements                                |
+---------------------------------------------------------------------------------------------------+
```
*Figure 3.1: End-to-End Comparative Research Methodology Workflow.*

The investigation is governed by two formal scientific hypotheses:
- **Null Hypothesis ($H_{01}$):** In multi-site SDN topologies, Artificial Intelligence and Deep Reinforcement Learning algorithms do not provide a statistically significant improvement in multi-objective decision quality (joint latency, reliability, and computational efficiency) compared to classical heuristics.
- **Alternative Hypothesis ($H_{11}$):** Deep Reinforcement Learning models achieve statistically significant improvements in propagation latency and fault tolerance, but incur a quantifiable "Complexity Tax" ($\omega$) that renders them Pareto-dominated by classical clustering heuristics in static network environments.

---

## 3.2 DATA COLLECTION & NETWORK TOPOLOGY CORPUS

To evaluate algorithmic behavior across realistic wide-area backbones and controlled topological properties, the experimental corpus comprises both **canonical empirical topologies** and **parameterized synthetic network models**. Table 3.1 summarizes the topological characteristics of the benchmark corpus.

### Table 3.1: Summary of Canonical and Synthetic Network Topology Parameters

| Topology Name | Topology Family | Node Count ($N$) | Edge Count ($|E|$) | Mean Node Degree | Clustering Coefficient | Characteristic Graph Property |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Internet2** | Canonical WAN | 11 | 18 | 3.27 | 0.333 | Sparse national research backbone |
| **ATT-MPLS** | Canonical WAN | 21 | 54 | 5.14 | 0.412 | Dense, highly meshed commercial tier-1 backbone |
| **BA-20** | Barabási-Albert | 20 | 36 | 3.60 | 0.285 | Scale-free, power-law degree distribution ($m=2$) |
| **BA-50** | Barabási-Albert | 50 | 96 | 3.84 | 0.174 | Large scale-free network with core hub nodes ($m=2$) |
| **WX-20** | Waxman Spatial | 20 | 19 | 1.90 | 0.050 | Geographically constrained sparse mesh ($\alpha=0.5, \beta=0.2$) |
| **WX-50** | Waxman Spatial | 50 | 53 | 2.12 | 0.042 | Large planar geographic network with sparse long links |

### 3.2.1 Canonical Empirical Topologies
1. **Internet2 Backbone ($N=11, |E|=18$):** The de facto standard reference topology in SDN controller placement literature, originally established by Heller et al. (2012). It models the nationwide United States research network connecting 11 major metropolitan points of presence (PoPs). Nodes exhibit moderate degrees ranging from 2 to 5.
2. **ATT-MPLS Backbone ($N=21, |E|=54$):** Sourced from the Internet Topology Zoo (Knight et al., 2011). It models AT&T's North American commercial Multi-Protocol Label Switching (MPLS) core network. Featuring 21 nodes and 54 bidirectional links, it represents a highly meshed, resilient tier-1 carrier topology with substantial alternative path diversity.

### 3.2.2 Parameterized Synthetic Network Models
To isolate the specific topological drivers governing algorithm performance, synthetic graphs were generated using two mathematically distinct graph-theoretic models implemented via NetworkX:
1. **Barabási-Albert (BA) Scale-Free Model:** Generates networks using a preferential attachment mechanism where new nodes connect to existing nodes with a probability proportional to their degree ($P(k) \sim k^{-\gamma}$). This produces a power-law degree distribution characteristic of the global Internet AS-level topology, featuring a small number of ultra-connected "hub" nodes and a large number of peripheral leaves. Parameterized with attachment parameter $m = 2$ at scales $N = 20$ and $N = 50$.
2. **Waxman Spatial Random Graph Model:** Generates geographically embedded networks (Waxman, 1988) where nodes are distributed uniformly at random on a unit square $[0, 1]^2$. The probability $P(u, v)$ of creating an edge between node $u$ and node $v$ decays exponentially with their Euclidean distance $d(u, v)$:
   $$P(u, v) = \alpha \cdot \exp\left( - \frac{d(u, v)}{\beta \cdot L} \right)$$
   where $L$ is the maximum distance between any two nodes, $\alpha = 0.5$ controls link density, and $\beta = 0.2$ governs the ratio of short to long edges. This produces realistic planar geographic networks with localized clustering.

### 3.2.3 Data Provenance and Ethical Considerations
All topological data utilized in this study are fully synthetic or derived from openly available, anonymized public scientific datasets (Internet Topology Zoo). No proprietary telecommunications records, personally identifiable information (PII), or private enterprise packet traces were ingested, ensuring complete compliance with institutional research ethics standards.

---

## 3.3 SYSTEM DESIGN & ALGORITHMIC FORMULATIONS

Given an undirected graph $G = (V, E)$ with $|V| = N$ switches, let $d(u, v)$ represent the shortest-path distance between nodes $u$ and $v$ computed via Dijkstra's algorithm. Let $P \subseteq V$ denote the set of $k$ selected controller locations ($|P| = k$).

### 3.3.1 Algorithm 1: Random Baseline Placement
The Random baseline uniformly samples $k$ distinct nodes from $V$ without replacement:
$$P_{rand} \sim \text{Uniform}(\{ S \subseteq V : |S| = k \})$$
This serves as the foundational null benchmark. Any intelligent heuristic or AI algorithm must demonstrate statistically significant superiority over this baseline to justify its implementation.

### 3.3.2 Algorithm 2: Greedy $K$-Center Placement (Gonzalez Heuristic)
Implements Gonzalez's 2-approximation algorithm for the $k$-center problem:
1. Initialize $P = \{ v_0 \}$, where $v_0$ is the node with the highest degree centrality.
2. For $i = 2$ to $k$:
   $$c_i = \arg\max_{v \in V \setminus P} \left( \min_{c \in P} d(v, c) \right)$$
   $$P \leftarrow P \cup \{ c_i \}$$
3. Return $P$.

### 3.3.3 Algorithm 3: Spatial $K$-Means Clustering
Treats network nodes as points in coordinate space:
1. For canonical and Waxman graphs, nodes utilize 2D spatial coordinates $(x_i, y_i)$. For Barabási-Albert graphs, nodes are embedded into a 2D Euclidean metric space via classical Multidimensional Scaling (MDS) over the all-pairs shortest-path matrix.
2. Initialize $k$ cluster centroids using $K$-Means++ initialization to ensure dispersed starting seeds.
3. Iteratively execute Voronoi partitioning and centroid updates until centroid displacement drops below $10^{-4}$ or maximum iterations ($T = 300$) are reached.
4. For each final centroid $\mu_j$, select the physically closest graph node as the controller location:
   $$c_j = \arg\min_{v \in V} \| \mathbf{x}_v - \mu_j \|_2$$

### 3.3.4 Algorithm 4: Genetic Algorithm (GA Metaheuristic)
Operates on a discrete combinatorial chromosome representation:
- **Encoding:** A chromosome is represented as an integer vector $\mathbf{g} = [g_1, g_2, \dots, g_k]$ of length $k$, where $g_i \in V$ and all elements are unique.
- **Population & Generations:** Maintains a population of $M_{pop} = 50$ chromosomes evolved over $G_{max} = 50$ generations.
- **Fitness Function:** Designed to minimize average propagation delay:
  $$\text{Fitness}(\mathbf{g}) = \frac{1}{1.0 + L(P_{\mathbf{g}})} = \frac{1}{1.0 + \frac{1}{|V|} \sum_{v \in V} \min_{c \in \mathbf{g}} d(v, c)}$$
- **Selection:** Roulette-wheel selection based on relative fitness probabilities.
- **Crossover:** Two-point crossover applied with probability $p_c = 0.8$. Duplicate alleles resulting from crossover are repaired via greedy replacement with unassigned nodes.
- **Mutation:** Random swap mutation applied with probability $p_m = 0.15$ per individual.
- **Elitism:** The top 2 fittest individuals in each generation are directly copied to the subsequent generation without modification.

### 3.3.5 Algorithm 5: PyTorch Deep $Q$-Network (DQN Architecture)
The reinforcement learning agent is framed within a sequential Markov Decision Process (MDP) designed in strict alignment with state-of-the-art parameters defined by Farahi et al. (2026). Figure 3.2 illustrates the Multi-Layer Perceptron (MLP) architecture.

```
State Vector s_t [1 x N] (Normalized Node Degree & Centrality)
       |
       v
+-----------------------------------+
|  Fully Connected Layer 1 (FC1)    | --> Linear(N -> 64), ReLU Activation
+-----------------------------------+
       |
       v
+-----------------------------------+
|  Fully Connected Layer 2 (FC2)    | --> Linear(64 -> 64), ReLU Activation
+-----------------------------------+
       |
       v
+-----------------------------------+
|  Output Layer (Q-Values)          | --> Linear(64 -> N)
+-----------------------------------+
       |
       v
Action a_t = argmax Q(s_t, a) (Select Next Controller Location)
```
*Figure 3.2: Deep Q-Network (DQN) Neural Architecture for Controller Placement.*

The DQN agent selects controller locations sequentially across $k$ sub-steps to form a complete placement $P = \{a_1, \dots, a_k\}$. 
- **Reward Function:** Incorporates latency minimization, single-link reachability, and uniqueness constraints:
  $$R(P) = 10.0 \cdot \left( \frac{L_{max}^{rand} - L(P)}{L_{max}^{rand}} \right) + 5.0 \cdot Reach_{avg}(P) - \text{Penalty}$$
  where $\text{Penalty} = 20.0$ if the agent selects duplicate nodes within a single placement.

Table 3.2 outlines the exact hyperparameter specifications implemented in the PyTorch DQN pipeline.

### Table 3.2: Deep Q-Network Hyperparameter Configuration and Reference Compliance

| Hyperparameter | Value | Reference / Justification |
| :--- | :--- | :--- |
| **Neural Network Architecture** | MLP: Input($N$) $\to$ 64 $\to$ 64 $\to$ Output($N$) | Farahi et al. (2026) exact match |
| **Activation Functions** | Rectified Linear Unit (ReLU) | Hidden layer standard non-linearity |
| **Optimizer** | Adam ($\beta_1 = 0.9, \beta_2 = 0.999$) | Stable adaptive learning rate gradient descent |
| **Learning Rate ($\alpha$)** | 0.001 ($10^{-3}$) | Farahi et al. (2026) baseline |
| **Discount Factor ($\gamma$)** | 0.99 | Balances immediate and downstream episode rewards |
| **Batch Size** | 32 | Mini-batch stochastic gradient descent |
| **Replay Memory Capacity ($M$)**| 10,000 transitions | Prevents catastrophic forgetting |
| **Exploration Strategy** | $\epsilon$-Greedy: $\epsilon_{start} = 1.0 \to \epsilon_{end} = 0.05$ | Exponential decay: $\epsilon_{t+1} = \max(\epsilon_{end}, \epsilon_t \cdot 0.995)$ |
| **Target Network Update ($\tau$)**| Soft Polyak tracking ($\tau = 0.005$) | Prevents Q-target value oscillation |
| **Episode Budget** | 1,000 training episodes | Sufficient for empirical convergence |

---

## 3.4 IMPLEMENTATION ARCHITECTURE & EMULATION HARNESS

### 3.4.1 Software Engineering Stack
The experimental benchmark is implemented in Python (compatible across versions 3.8 to 3.12). Core computational dependencies include:
- **Graph Processing Engine:** NetworkX 3.2+ for graph generation, shortest-path matrix computation, and edge-removal reachability evaluations;
- **Deep Learning Framework:** PyTorch 2.4+ (CPU-optimized build) for neural tensor operations, autograd backpropagation, and replay buffer sampling;
- **Clustering & Numerics:** Scikit-Learn 1.4+ and NumPy 1.24+ for $K$-Means clustering and metric statistics;
- **Visualization:** Matplotlib, Seaborn, and Plotly for high-resolution Pareto plotting and interactive 3D HTML surface generation.

### 3.4.2 Mininet OpenFlow Emulation Architecture
To validate whether mathematical shortest-path latencies translate into real-world control-plane performance, placements are evaluated within a virtualized Linux network emulation environment using **Mininet 2.3+** and **Open vSwitch (OVS)**. Figure 3.3 illustrates the emulation topology.

```
       +-------------------------------------------------------------+
       |             REMOTE OPENFLOW CONTROLLERS                     |
       |     Controller 1            Controller 2        ...         |
       |  (127.0.0.1:6633)        (127.0.0.1:6634)                   |
       +-------^-------------------------^---------------------------+
               | TCP Control Channel     | TCP Control Channel
       +-------v-------------------------v---------------------------+
       |             OPENFLOW DATA PLANE (OPEN vSWITCH)              |
       |     Switch s1 <---------------> Switch s2 <-----> Switch s3 |
       |        |                           |                 |      |
       +--------|---------------------------|-----------------|------+
                v                           v                 v
             Host h1                     Host h2           Host h3
```
*Figure 3.3: Mininet OpenFlow Live Control-Plane Emulation Architecture.*

In the Mininet environment:
1. Switches are instantiated as kernel-level Open vSwitch (OVS) instances running OpenFlow 1.3.
2. For each node $v \in V$, a virtualized host $h_v$ is attached via a virtual Ethernet (`veth`) interface pair.
3. Links are configured with bidirectional propagation latencies matching the shortest-path graph edge weights.
4. Remote controllers are spawned on distinct localhost TCP ports (`127.0.0.1:6633`, `6634`, etc.). Switches are bound to their assigned controller via the Southbound control channel.
5. Control-plane Round-Trip Time (RTT) is empirically measured by transmitting ICMP ping probes from each host to its designated controller address, capturing kernel packet traversal, flow installation delay, and queuing latency.

### 3.4.3 The Phase 4 Mininet "2-Second Gate Test" Protocol
Running live Mininet network emulations inside iterative reinforcement learning training loops introduces severe operating system overheads (kernel namespace creation, OVS bridge tearing, virtual interface creation). To rigorously evaluate the feasibility of online Mininet-in-the-loop training, a formal **Phase 4 Mininet Overhead Gate Test** was established.

The protocol decomposes Mininet execution into four distinct phases across 3 controlled trials on Internet2:
- **Phase A (Topology Construction):** Instantiation of Mininet network, virtual switches, and host interface bindings.
- **Phase B (Controller Binding & Network Start):** Starting OVS daemons, binding OpenFlow controllers, and initializing static ARP caches.
- **Phase C (Traffic Generation Burst):** Sub-second ICMP ping traffic generation capturing active control-loop delay.
- **Phase D (Cleanup & Teardown):** Halting OVS bridges, releasing Linux network namespaces, and executing `mn -c`.

The protocol defines a strict **Decision Threshold of 2,000 milliseconds per episode**. If the full lifecycle overhead exceeds $2,000\text{ ms}$, online Mininet-in-the-loop training is rejected as out-of-spec, and Mininet evaluation is formally deferred to offline post-convergence validation.

---

## 3.5 DATA ANALYSIS & EVALUATION METRICS

### 3.5.1 Average Switch-to-Controller Propagation Latency ($L(P)$)
The primary performance metric measuring communication delay across all switches $v \in V$ to their closest assigned controller $c \in P$:
$$L(P) = \frac{1}{|V|} \sum_{v \in V} \min_{c \in P} d(v, c)$$
where $d(v, c)$ is the shortest-path distance in milliseconds.

### 3.5.2 Control-Plane Reliability ($Reach_{avg}$) Under Single-Link Failure ($N-1$ Engine)
Quantifies structural control-plane survivability under catastrophic link outages. For each edge $e \in E$, $e$ is removed from $G$ to create degraded graph $G' = (V, E \setminus \{e\})$. Let $V_{reach}(G', P)$ be the subset of switches that maintain an active path to at least one controller in $G'$:
$$Reach_{avg}(P) = \frac{1}{|E|} \sum_{e \in E} \frac{|V_{reach}(G \setminus \{e\}, P)|}{|V|}$$
$Reach_{avg} \in [0.0, 1.0]$, where $1.0$ indicates perfect $100\%$ control-plane reachability across all possible single-link failures.

### 3.5.3 Computational Complexity Tax ($\omega$)
Measures the computational resource cost required to derive the placement solution:
- For reinforcement learning (DQN): $\omega$ is reported as **CPU execution seconds per episode** ($s/episode$) and total elapsed training time ($s$);
- For heuristics and metaheuristics: $\omega$ is reported as **wall-clock CPU execution time in milliseconds** ($ms$).

### 3.5.4 Three-Dimensional Pareto Dominance & Compromise Distance
A solution $P_1$ dominates $P_2$ ($P_1 \succ P_2$) if and only if $L(P_1) \le L(P_2)$, $Reach_{avg}(P_1) \ge Reach_{avg}(P_2)$, and $\omega(P_1) \le \omega(P_2)$, with at least one strict inequality.

To rank non-dominated solutions on the Pareto frontier, the **Ideal Point Compromise Distance ($D_{ideal}$)** is calculated using normalized Euclidean distance to the theoretical ideal objective vector $\mathbf{z}^* = (L_{min}, Reach_{max}, \omega_{min})$:
$$D_{ideal}(P) = \sqrt{ w_1 \left( \frac{L(P) - L_{min}}{L_{max} - L_{min}} \right)^2 + w_2 \left( \frac{Reach_{max} - Reach_{avg}(P)}{Reach_{max} - Reach_{min}} \right)^2 + w_3 \left( \frac{\omega(P) - \omega_{min}}{\omega_{max} - \omega_{min}} \right)^2 }$$
where $w_1 = 0.5$, $w_2 = 0.3$, and $w_3 = 0.2$ reflect operator priority weights.

### 3.5.5 Statistical Hypothesis Testing
To verify whether observed differences between algorithm families are statistically significant, **Two-Way Factorial Analysis of Variance (ANOVA)** is performed, testing main effects and interaction terms across topology scales and controller budgets. Post-hoc pair-wise contrasts are evaluated using **Tukey’s Honest Significant Difference (HSD)** test at a significance threshold of $p < 0.05$.

---

## 3.6 EXPERIMENTAL SETUP, VERIFICATION CONTROLS & GATE TESTING

### 3.6.1 Hardware and Operating System Specifications
All benchmark experiments were conducted on an isolated, dedicated compute workstation with the following hardware specifications:
- **Processor:** x86_64 architecture, multi-core CPU operating at a locked clock frequency of 2.60 GHz;
- **Memory:** 16.0 GB physical DDR4 RAM;
- **Storage:** NVMe Solid-State Storage (read/write bandwidth $> 2,000\text{ MB/s}$);
- **Host OS:** Linux (Ubuntu 22.04 LTS kernel 5.15+);
- **Virtual Machine OS (Mininet):** Ubuntu 20.04 LTS (Python 3.8 environment).

### 3.6.2 Environmental and Verification Controls
To eliminate confounding variables and ensure strict experimental reproducibility:
1. **CPU Frequency Pinning & Thermal Mitigation:** CPU frequency governors were locked to `performance` mode to prevent dynamic frequency scaling. Idle cooldown periods of 10 seconds were enforced between major matrix sweeps to eliminate thermal throttling artifacts.
2. **Deterministic Random Seed Control:** All pseudorandom number generators—including Python's `random`, NumPy's `np.random`, and PyTorch's `torch.manual_seed`—were explicitly seeded. The 10-seed stability audit evaluated the exact seed sequence $S = \{42, 123, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768\}$.
3. **Automated Unit Testing & Linting:** The software harness incorporates 21 automated unit tests verifying topology loading, shortest-path calculation determinism, metric formulation accuracy, and JSON manifest schemas, executing in $0.126\text{ s}$ with a $100\%$ pass rate.

Table 3.3 summarizes the complete factorial design matrix spanning 60 distinct experimental configurations.

### Table 3.3: Full Factorial Benchmark Design Matrix ($2 \times 2 \times 3 \times 5 = 60$ Cells)

| Factor | Factor Levels | Number of Levels | Description |
| :--- | :--- | :---: | :--- |
| **Topology Model** | Barabási-Albert (BA), Waxman (WX) | 2 | Scale-free degree skew vs. spatial planar clustering |
| **Node Scale ($N$)** | $N = 20, N = 50$ | 2 | Small-to-medium enterprise vs. large regional WAN |
| **Controller Budget ($k$)** | $k = 2, k = 3, k = 5$ | 3 | Minimal redundancy, standard budget, high redundancy |
| **Algorithm Family** | Random, Greedy $K$-Center, $K$-Means, GA, DQN | 5 | Baseline, heuristics, metaheuristic, deep RL |
| **Total Factorial Cells** | **$2 \times 2 \times 3 \times 5$** | **60 Cells** | **5 trials per cell (300 total experimental runs)** |
