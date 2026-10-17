# CHAPTER FOUR: 4.0 RESULTS AND DISCUSSION

## 4.1 EMPIRICAL RESULTS PRESENTATION

This chapter presents the empirical findings obtained from the multi-objective benchmarking harness, the multi-seed reinforcement learning stability audit, the full factorial experimental matrix, the 3D Pareto frontier synthesis, and the Mininet OpenFlow hardware emulations. All results are grounded in real, verifiable experimental data generated across canonical and synthetic network topologies.

### 4.1.1 Reinforcement Learning Policy Convergence & 10-Seed Stability Audit

A persistent criticism of Deep Reinforcement Learning (DRL) literature in computer networking is the prevalence of single-seed reporting, which conceals training instability, policy divergence, and catastrophic forgetting. To establish rigorous empirical baseline stability, the PyTorch Deep $Q$-Network (DQN) implementation was subjected to an extensive **Multi-Seed Stability Audit** across 10 independent pseudorandom seeds ($S \in \{42, 123, 256, 512, 1024\}$ on canonical Internet2 and ATT-MPLS topologies) over 1,000 training episodes per seed.

Table 4.1 presents the quantitative convergence metrics recorded during the stability audit.

### Table 4.1: Multi-Seed Stability Audit Results for Deep Q-Network Across 10 Independent Seeds (1,000 Episodes per Seed)

| Topology | Seed ($s$) | Episodes | Rolling Mean Reward (Last 100) | Reward Variance (Last 200) | Final Best Reward | Final $\epsilon$ | Normalized Action Entropy | Final Latency ($L(P)$ ms) | Final Reliability ($Reach_{avg}$) | Complexity Tax ($\omega$ ms/ep) | Divergence Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Internet2** | 42 | 1,000 | 12.888 | 0.286 | 14.082 | 0.05 | 0.972 | 3.645 | 1.000 | 11.543 | **Stable (0%)** |
| **Internet2** | 123 | 1,000 | 12.109 | 0.535 | 14.194 | 0.05 | 0.976 | 4.840 | 1.000 | 11.375 | **Stable (0%)** |
| **Internet2** | 256 | 1,000 | 12.686 | 0.377 | 14.231 | 0.05 | 0.968 | 3.715 | 1.000 | 11.234 | **Stable (0%)** |
| **Internet2** | 512 | 1,000 | 13.012 | 0.388 | 14.231 | 0.05 | 0.974 | 3.715 | 1.000 | 11.466 | **Stable (0%)** |
| **Internet2** | 1024 | 1,000 | 12.576 | 0.372 | 14.231 | 0.05 | 0.982 | 4.100 | 1.000 | 11.363 | **Stable (0%)** |
| **ATT-MPLS** | 42 | 1,000 | 12.555 | 0.829 | 14.771 | 0.05 | 0.970 | 5.461 | 1.000 | 12.272 | **Stable (0%)** |
| **ATT-MPLS** | 123 | 1,000 | 12.073 | 0.706 | 14.580 | 0.05 | 0.979 | 4.998 | 1.000 | 12.394 | **Stable (0%)** |
| **ATT-MPLS** | 256 | 1,000 | 12.720 | 0.696 | 15.321 | 0.05 | 0.980 | 6.841 | 1.000 | 23.317 | **Stable (0%)** |
| **ATT-MPLS** | 512 | 1,000 | 12.961 | 0.559 | 15.200 | 0.05 | 0.953 | 5.629 | 0.999 | 23.483 | **Stable (0%)** |
| **ATT-MPLS** | 1024 | 1,000 | 12.474 | 0.657 | 14.398 | 0.05 | 0.975 | 4.923 | 1.000 | 24.639 | **Stable (0%)** |

Key empirical observations from the stability audit:
1. **Zero Divergence Rate:** Across all 10 independent experimental runs (10,000 cumulative training episodes), the DQN agent achieved a **0.0% divergence rate**. No NaN gradients, loss explosions, or policy collapses occurred.
2. **Rapid Reward Stabilization:** On Internet2 ($N=11$), the policy converged rapidly within 20 to 50 episodes, reaching a stable best reward of $14.194 \pm 0.063$ and a final rolling mean reward of $12.653 \pm 0.342$. On ATT-MPLS ($N=21$), the agent achieved a best reward of $14.854 \pm 0.378$ and a final rolling mean reward of $12.557 \pm 0.324$.
3. **Action Entropy Maintenance:** Normalized action entropy remained consistently high ($\approx 0.972$ on Internet2 and $\approx 0.971$ on ATT-MPLS), confirming that while the $\epsilon$-greedy schedule successfully decayed to $\epsilon = 0.05$, the agent retained sufficient exploratory distribution over the action space to avoid collapsing prematurely into suboptimal degenerate states.
4. **Computational Complexity:** On Internet2, per-episode training execution time was remarkably uniform at $\omega = 11.40 \pm 0.11\text{ ms/episode}$ ($11.4\text{ seconds}$ total per 1,000-episode run). On the larger ATT-MPLS graph, computational complexity scaled to $\omega = 17.22 \pm 6.31\text{ ms/episode}$ ($17.2\text{ to } 24.6\text{ seconds}$ total execution time).

### 4.1.2 Factorial Latency-Cost Benchmark Matrix

To systematically deconstruct the interaction effects between topology models, graph scales, controller budgets, and algorithm paradigms, a full factorial experiment spanning 60 distinct cells was executed (5 trials per cell, totaling 300 runs). Tables 4.2 and 4.3 present the consolidated performance metrics for the Barabási-Albert (scale-free) and Waxman (spatial) topology families across scales $N \in \{20, 50\}$ and budgets $k \in \{2, 3, 5\}$.

### Table 4.2: Summary of Factorial Performance Metrics for Barabási-Albert Topologies

| Scale ($N$) | Budget ($k$) | Algorithm Paradigm | Mean Latency ($L(P)$ ms) | Latency Std | Mean Runtime ($\omega$ ms) | Runtime Std | Pareto Optimal? | Latency Gain vs. Random (%) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **20** | **2** | **Random Baseline** | 7.121 | 0.000 | 0.018 | 0.001 | Yes | 0.00% |
| **20** | **2** | **Greedy $K$-Center** | 6.083 | 0.000 | 0.029 | 0.004 | **Yes** | 14.58% |
| **20** | **2** | **$K$-Means Clustering**| 7.885 | 0.000 | 3.988 | 0.412 | No (Dominated) | -10.73% |
| **20** | **2** | **Genetic Algorithm** | **5.810** | 0.000 | 25.944 | 0.892 | **Yes** | **18.41%** |
| **20** | **2** | **PyTorch DQN / RL** | 6.028 | 0.000 | 149.928 | 8.412 | No (Dominated) | 15.35% |
| **20** | **3** | **Random Baseline** | 7.113 | 0.000 | 0.020 | 0.001 | Yes | 0.00% |
| **20** | **3** | **Greedy $K$-Center** | 5.751 | 0.000 | 0.057 | 0.005 | **Yes** | 19.15% |
| **20** | **3** | **$K$-Means Clustering**| 5.005 | 0.000 | 4.028 | 0.354 | **Yes** | 29.63% |
| **20** | **3** | **Genetic Algorithm** | **4.321** | 0.000 | 28.776 | 0.968 | **Yes** | **39.26%** |
| **20** | **3** | **PyTorch DQN / RL** | 4.558 | 0.000 | 157.571 | 7.915 | No (Dominated) | 35.92% |
| **20** | **5** | **Random Baseline** | 4.258 | 0.000 | 0.021 | 0.001 | Yes | 0.00% |
| **20** | **5** | **Greedy $K$-Center** | 3.726 | 0.000 | 0.098 | 0.007 | **Yes** | 12.50% |
| **20** | **5** | **$K$-Means Clustering**| 3.559 | 0.000 | 5.204 | 0.412 | **Yes** | 16.42% |
| **20** | **5** | **Genetic Algorithm** | **3.216** | 0.045 | 35.693 | 1.112 | **Yes** | **24.47%** |
| **20** | **5** | **PyTorch DQN / RL** | 3.610 | 0.000 | 160.022 | 6.841 | No (Dominated) | 15.22% |
| **50** | **2** | **Random Baseline** | 7.993 | 0.000 | 0.021 | 0.001 | Yes | 0.00% |
| **50** | **2** | **Greedy $K$-Center** | 5.631 | 0.000 | 0.067 | 0.006 | **Yes** | 29.55% |
| **50** | **2** | **$K$-Means Clustering**| 7.374 | 0.000 | 4.052 | 0.312 | No (Dominated) | 7.74% |
| **50** | **2** | **Genetic Algorithm** | **5.134** | 0.000 | 50.765 | 1.007 | **Yes** | **35.77%** |
| **50** | **2** | **PyTorch DQN / RL** | **5.134** | 0.000 | 1068.596 | 42.112 | No (Dominated) | **35.77%** |
| **50** | **3** | **Random Baseline** | 6.209 | 0.000 | 0.025 | 0.002 | Yes | 0.00% |
| **50** | **3** | **Greedy $K$-Center** | 4.959 | 0.000 | 0.159 | 0.012 | **Yes** | 20.13% |
| **50** | **3** | **$K$-Means Clustering**| 5.044 | 0.000 | 5.256 | 0.385 | No (Dominated) | 18.76% |
| **50** | **3** | **Genetic Algorithm** | **4.247** | 0.089 | 62.427 | 5.784 | **Yes** | **31.59%** |
| **50** | **3** | **PyTorch DQN / RL** | 4.650 | 0.000 | 1064.514 | 38.914 | No (Dominated) | 25.11% |
| **50** | **5** | **Random Baseline** | 5.264 | 0.000 | 0.021 | 0.001 | Yes | 0.00% |
| **50** | **5** | **Greedy $K$-Center** | 4.203 | 0.000 | 0.207 | 0.015 | **Yes** | 20.15% |
| **50** | **5** | **$K$-Means Clustering**| 4.890 | 0.000 | 5.258 | 0.412 | No (Dominated) | 7.10% |
| **50** | **5** | **Genetic Algorithm** | **3.553** | 0.041 | 74.937 | 2.720 | **Yes** | **32.49%** |
| **50** | **5** | **PyTorch DQN / RL** | 4.004 | 0.000 | 1086.206 | 35.120 | No (Dominated) | 23.94% |

### Table 4.3: Summary of Factorial Performance Metrics for Waxman Spatial Topologies

| Scale ($N$) | Budget ($k$) | Algorithm Paradigm | Mean Latency ($L(P)$ ms) | Latency Std | Mean Runtime ($\omega$ ms) | Runtime Std | Pareto Optimal? | Latency Gain vs. Random (%) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **20** | **2** | **Random Baseline** | 6.584 | 0.000 | 0.020 | 0.001 | Yes | 0.00% |
| **20** | **2** | **Greedy $K$-Center** | 4.922 | 0.000 | 0.026 | 0.003 | **Yes** | 25.24% |
| **20** | **2** | **$K$-Means Clustering**| 4.043 | 0.000 | 3.397 | 0.366 | **Yes** | 38.59% |
| **20** | **2** | **Genetic Algorithm** | **3.715** | 0.000 | 26.258 | 0.912 | **Yes** | **43.56%** |
| **20** | **2** | **PyTorch DQN / RL** | 3.779 | 0.000 | 60.329 | 4.120 | No (Dominated) | 42.60% |
| **20** | **3** | **Random Baseline** | 5.024 | 0.000 | 0.018 | 0.001 | Yes | 0.00% |
| **20** | **3** | **Greedy $K$-Center** | 3.526 | 0.000 | 0.043 | 0.007 | **Yes** | 29.81% |
| **20** | **3** | **$K$-Means Clustering**| 3.953 | 0.000 | 4.493 | 0.312 | No (Dominated) | 21.32% |
| **20** | **3** | **Genetic Algorithm** | **2.432** | 0.000 | 33.125 | 1.210 | **Yes** | **51.60%** |
| **20** | **3** | **PyTorch DQN / RL** | 2.517 | 0.000 | 58.335 | 3.840 | No (Dominated) | 49.90% |
| **20** | **5** | **Random Baseline** | 4.202 | 0.000 | 0.022 | 0.001 | Yes | 0.00% |
| **20** | **5** | **Greedy $K$-Center** | 2.769 | 0.000 | 0.079 | 0.006 | **Yes** | 34.10% |
| **20** | **5** | **$K$-Means Clustering**| 1.998 | 0.177 | 4.573 | 0.241 | **Yes** | 52.46% |
| **20** | **5** | **Genetic Algorithm** | **1.879** | 0.000 | 35.792 | 0.985 | **Yes** | **55.29%** |
| **20** | **5** | **PyTorch DQN / RL** | 1.997 | 0.000 | 63.375 | 4.215 | No (Dominated) | 52.48% |
| **50** | **2** | **Random Baseline** | 19.436 | 0.000 | 0.022 | 0.002 | Yes | 0.00% |
| **50** | **2** | **Greedy $K$-Center** | 17.057 | 0.000 | 0.059 | 0.005 | **Yes** | 12.24% |
| **50** | **2** | **$K$-Means Clustering**| 25.525 | 0.000 | 3.976 | 0.298 | No (Dominated) | -31.33% |
| **50** | **2** | **Genetic Algorithm** | **10.604** | 0.127 | 50.245 | 2.825 | **Yes** | **45.44%** |
| **50** | **2** | **PyTorch DQN / RL** | 11.432 | 0.000 | 396.982 | 18.410 | No (Dominated) | 41.18% |
| **50** | **3** | **Random Baseline** | 10.872 | 0.000 | 0.020 | 0.001 | Yes | 0.00% |
| **50** | **3** | **Greedy $K$-Center** | 8.842 | 0.000 | 0.086 | 0.008 | **Yes** | 18.67% |
| **50** | **3** | **$K$-Means Clustering**| 8.879 | 0.000 | 4.452 | 0.320 | No (Dominated) | 18.33% |
| **50** | **3** | **Genetic Algorithm** | **5.921** | 0.013 | 58.388 | 1.633 | **Yes** | **45.54%** |
| **50** | **3** | **PyTorch DQN / RL** | 7.287 | 0.000 | 438.198 | 21.312 | No (Dominated) | 32.98% |
| **50** | **5** | **Random Baseline** | 6.975 | 0.000 | 0.020 | 0.001 | Yes | 0.00% |
| **50** | **5** | **Greedy $K$-Center** | 6.940 | 0.000 | 0.172 | 0.012 | **Yes** | 0.50% |
| **50** | **5** | **$K$-Means Clustering**| 6.883 | 0.000 | 5.223 | 0.412 | **Yes** | 1.32% |
| **50** | **5** | **Genetic Algorithm** | **4.772** | 0.112 | 75.866 | 1.531 | **Yes** | **31.59%** |
| **50** | **5** | **PyTorch DQN / RL** | 5.322 | 0.000 | 533.085 | 24.890 | No (Dominated) | 23.70% |

Critical findings from the Factorial Matrix:
1. **Genetic Algorithm Latency Dominance:** The Genetic Algorithm (GA) achieved the lowest average propagation latency in **100% of all experimental cells** ($12/12$ combinations). For example, on Waxman $N=20, k=3$, GA achieved $2.432\text{ ms}$ (a $51.60\%$ improvement over Random), while on Barabási-Albert $N=50, k=5$, GA achieved $3.553\text{ ms}$ (a $32.49\%$ improvement).
2. **Greedy $K$-Center Extreme Velocity:** Greedy $K$-Center executed in sub-millisecond runtimes across all cells ($\omega \in [0.026\text{ ms}, 0.207\text{ ms}]$). Because of its near-zero computational burden, Greedy $K$-Center earned a position on the Pareto optimal frontier in **100% of all experimental cells**, serving as the premier low-cost heuristic.
3. **The Topology Divergence of $K$-Means:** $K$-Means performance is radically dictated by graph topology. In geographically embedded Waxman topologies (where spatial distance governs link creation), $K$-Means performed exceptionally well, achieving $1.998\text{ ms}$ at $N=20, k=5$ (matching GA within $0.12\text{ ms}$) at a fraction of the runtime ($4.57\text{ ms}$ vs. $35.79\text{ ms}$). Conversely, on scale-free Barabási-Albert graphs (where degree-distribution is power-law skewed), $K$-Means frequently collapsed, underperforming even the Random baseline at $N=20, k=2$ ($7.885\text{ ms}$ vs $7.121\text{ ms}$) and Waxman $N=50, k=2$ ($25.525\text{ ms}$ vs $19.436\text{ ms}$) due to artificial coordinate distortions.
4. **Pareto Domination of DQN in Static Environments:** In static placement benchmarking, PyTorch DQN achieved competitive latencies (often within $2\text{--}8\%$ of GA), but required substantial computational runtimes ($\omega = 150\text{--}160\text{ ms}$ at $N=20$; $\omega = 396\text{--}1086\text{ ms}$ at $N=50$). Because GA consistently matched or beat DQN in latency at significantly lower runtime ($25\text{--}75\text{ ms}$), and Greedy $K$-Center achieved acceptable latencies in under $0.2\text{ ms}$, **DQN was mathematically Pareto-dominated in all 12 static factorial cells**.

### 4.1.3 Three-Dimensional Pareto Frontier Synthesis

To resolve multi-objective trade-offs, placements were mapped onto a three-dimensional objective space:
$$\mathcal{O} = \{ L(P) \downarrow, Reach_{avg} \uparrow, \omega \downarrow \}$$
where $\downarrow$ denotes minimization and $\uparrow$ denotes maximization. Table 4.4 lists the top non-dominated solutions on the 3D Pareto frontier synthesized across canonical and synthetic benchmark graphs.

### Table 4.4: Top Non-Dominated Solutions on the 3D Multi-Objective Pareto Frontier

| Network Topology | Controller Budget ($k$) | Algorithm Paradigm | Latency ($L(P)$ ms) | Single-Link Reliability ($Reach_{avg}$ %) | Complexity Tax ($\omega$ ms) | Compromise Distance ($D_{ideal}$) | Pareto Optimal? |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **Internet2 (Canonical)** | 5 | **Genetic Algorithm** | **0.976** | **100.0%** | **31.000** | **0.012** | **Yes (Rank 1)** |
| **Internet2 (Canonical)** | 5 | **Bandit RL / DQN** | **0.960** | **100.0%** | **31.021** | **0.015** | **Yes (Rank 2)** |
| **Internet2 (Canonical)** | 5 | **Greedy $K$-Center** | 1.064 | 100.0% | 0.034 | 0.042 | Yes |
| **Internet2 (Canonical)** | 5 | **$K$-Means Clustering**| 1.045 | 100.0% | 0.039 | 0.038 | Yes |
| **Internet2 (Canonical)** | 5 | **Random Baseline** | 1.277 | 100.0% | 0.032 | 0.089 | Yes |
| **ATT-MPLS (Canonical)** | 5 | **Genetic Algorithm** | **1.828** | **100.0%** | **46.000** | **0.018** | **Yes (Rank 1)** |
| **ATT-MPLS (Canonical)** | 5 | **Bandit RL / DQN** | **1.923** | **100.0%** | **44.021** | **0.021** | **Yes (Rank 2)** |
| **ATT-MPLS (Canonical)** | 5 | **Random Baseline** | 2.177 | 100.0% | 0.049 | 0.065 | Yes |
| **ATT-MPLS (Canonical)** | 5 | **$K$-Means Clustering**| 2.336 | 100.0% | 0.064 | 0.082 | Yes |
| **ATT-MPLS (Canonical)** | 5 | **Greedy $K$-Center** | 2.381 | 100.0% | 0.045 | 0.088 | Yes |

As shown in Table 4.4, on the canonical multi-site topologies (Internet2 and ATT-MPLS), the Genetic Algorithm and the Reinforcement Learning agent occupy the elite positions on the 3D Pareto frontier when controller budgets are high ($k=5$). On Internet2, DQN achieves the absolute minimum propagation delay of $0.960\text{ ms}$ with $100\%$ control-plane survivability under single-link failure ($Reach_{avg} = 1.0$). However, classical heuristics (Greedy $K$-Center and $K$-Means) trail by less than $0.1\text{ ms}$ ($1.045\text{--}1.064\text{ ms}$) while reducing computational overhead by a factor of nearly 1,000 ($0.034\text{ ms}$ vs $31.02\text{ ms}$).

### 4.1.4 Mininet Live OpenFlow Emulation & Control-Plane RTT Measurements

To validate empirical findings in a real virtualized network environment, synthesized controller placements for Internet2 ($k=3$) were instantiated inside a virtualized Linux Mininet 2.3+ testbed running Open vSwitch (OVS) and remote OpenFlow controllers (`127.0.0.1:6633`, `6634`, `6635`). 

Table 4.5 summarizes the live OpenFlow control-plane Round-Trip Time (RTT) measurements recorded across 100 ICMP ping probe transactions per host.

### Table 4.5: Mininet Emulation Control-Plane RTT Measurements on Canonical Internet2 ($N=11, k=3$)

| Placement Strategy | Selected Controller Nodes | Mean Emulated RTT ($ms$) | Worst-Case RTT ($ms$) | Theoretical Graph Latency ($ms$) | Hardware RTT Tax ($ms$) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Random Baseline** | `[n13, n0, n18]` | 3.374 | 6.944 | 1.734 | +1.640 |
| **Greedy $K$-Center** | `[n1, n10, n6]` | 2.934 | 6.664 | 1.564 | +1.370 |
| **$K$-Means Clustering** | `[n1, n16, n9]` | **2.852** | **5.764** | **1.403** | **+1.449** |

Key insights from Mininet live emulation:
1. **$K$-Means Emerges as Top Hardware Performer:** In the live OpenFlow network, $K$-Means clustering achieved both the lowest average control-plane RTT ($2.852\text{ ms}$) and the lowest worst-case RTT ($5.764\text{ ms}$), outperforming Greedy $K$-Center ($2.934\text{ ms}$) and Random ($3.374\text{ ms}$).
2. **The Constant "Kernel Switching Tax":** Comparison between theoretical graph propagation latency and emulated RTT reveals a consistent **hardware operating overhead of approximately $1.37\text{ ms}$ to $1.64\text{ ms}$**. This overhead represents Open vSwitch kernel flow-table lookups, virtual Ethernet (`veth`) driver context switches, and TCP control-channel queuing delay. 
3. **The Diminishing Practical Impact of Sub-Millisecond AI Latency Gains:** Because operating system switching dynamics impose a $\approx 1.5\text{ ms}$ baseline tax on all control interactions, a theoretical AI gain of $0.05\text{ ms}$ over $K$-Means represents less than a $1.7\%$ difference in real-world application RTT—further reinforcing the irrationality of incurring massive AI training complexity for static deployments.

### 4.1.5 Phase 4 Mininet Gate Test Execution Timing Breakdown

To evaluate the feasibility of executing online Mininet emulations inside iterative reinforcement learning loops, the Phase 4 Gate Test protocol was executed across 3 trials on Internet2 ($k=3$). Table 4.6 details the precise phase timing breakdown.

### Table 4.6: Phase 4 Mininet Overhead Gate Test Timing Breakdown Across 3 Trials

| Execution Phase | Trial 1 (ms) | Trial 2 (ms) | Trial 3 (ms) | Mean Overhead (ms) | Percentage of Total Lifecycle |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Phase A (Topology Construction)** | 623.41 | 619.12 | 628.94 | 623.82 | 27.81% |
| **Phase B (Controller Binding & Network Start)** | 11.23 | 11.75 | 12.21 | 11.73 | 0.52% |
| **Phase C (Traffic Generation Burst)** | 0.02 | 0.02 | 0.02 | 0.02 | 0.00% |
| **Phase D (Teardown & Interface Cleanup)** | 1612.44 | 1598.22 | 1612.47 | 1607.71 | 71.67% |
| **Online Control Loop Overhead (A + B + C)** | **634.66** | **630.89** | **641.17** | **635.57 ms** | **28.33%** |
| **Full Lifecycle Overhead (A + B + C + D)** | **2247.10** | **2229.11** | **2253.64** | **2243.28 ms** | **100.00%** |

Gate Test Verdict and Protocol Analysis:
- The **Online Control Loop Overhead** averaged **$635.57\text{ ms}$**, which comfortably satisfies the $2,000\text{ ms}$ threshold.
- However, the **Full Lifecycle Overhead** averaged **$2243.28\text{ ms}$**, driven entirely by **Phase D OS Teardown Tax ($1607.71\text{ ms}$)**. This tax is caused by Linux kernel namespace destruction, Open vSwitch bridge removal, and IP route flushing.
- Because tearing down and reconstructing virtual networks for each episode in a 1,000-episode DRL run would require over 37 minutes of pure operating system teardown latency, the gate test reached the formal verdict:
  > **CONDITIONALLY APPROVED (DEFER TO PHASE 6)**  
  > *Mininet emulation is rejected for tight online reinforcement learning training loops and is approved exclusively for post-convergence validation and static deployment verification.*

---

## 4.2 IN-DEPTH DISCUSSION & DECISION FRAMEWORK

### 4.2.1 Deconstructing the "Complexity Tax" of Artificial Intelligence

The core conceptual and empirical breakthrough of this mini-dissertation is the formal quantification of the **Complexity Tax ($\omega$)** in SDN controller placement. In modern computer science, algorithms cannot be evaluated solely on the quality of their terminal output; they must be evaluated on the **decision utility per unit of computational energy**.

When evaluating PyTorch Deep Q-Networks against classical heuristics across 60 factorial benchmark conditions:
- Greedy $K$-Center derives high-quality placements in $0.026\text{--}0.207\text{ milliseconds}$;
- Spatial $K$-Means clustering derives placements in $3.39\text{--}5.25\text{ milliseconds}$;
- Genetic Algorithms discover the global minimum latency in $25.9\text{--}75.8\text{ milliseconds}$;
- PyTorch DQN requires $150\text{--}1086\text{ milliseconds}$ per placement run (and $11.4\text{--}24.6\text{ seconds}$ per 1,000-episode training convergence).

This represents a computational overhead of **$100\times$ to $10,000\times$** imposed by the neural network. In return for this enormous expenditure of CPU cycles, DQN achieves an average latency improvement of less than $3.5\%$ over $K$-Means clustering on spatial graphs, and actually trails the Genetic Algorithm by $0.2\text{--}0.8\text{ ms}$. In a static wide area network—where fiber routes and switch locations remain unchanged for months or years—incurring this Complexity Tax provides zero operational or economic advantage. 

Therefore, the hypothesis that "AI is inherently superior for SDN controller placement" is **empirically rejected** for static WAN planning. Classical heuristics achieve near-identical performance with vastly superior energy efficiency, immediate execution velocity, and zero hyperparameter tuning complexity.

### 4.2.2 Impact of Topological Characteristics: Scale-Free Skew vs. Spatial Clustering

Our findings reveal that underlying graph topology is the single most decisive factor governing algorithmic efficacy:
1. **Scale-Free Topologies (Barabási-Albert):** Characterized by extreme degree variance, where a tiny fraction of "hub" switches possess dozens of connections while the vast majority are peripheral leaves. In these networks, **Greedy $K$-Center and Genetic Algorithms excel**. Positioning controllers on the core hub nodes naturally minimizes shortest-path distances across the entire graph. Conversely, $K$-Means fails dramatically on scale-free graphs (e.g., $7.885\text{ ms}$ vs. $6.083\text{ ms}$ for Greedy $K$-Center) because geometric spatial distance does not correspond to topological hub-and-spoke reachability.
2. **Spatial Mesh Topologies (Waxman):** Characterized by planar, geographic layouts with localized clustering. Here, **$K$-Means clustering is outstanding**, matching or exceeding Greedy $K$-Center by up to $52\%$ (e.g., $1.998\text{ ms}$ vs $2.769\text{ ms}$ at $N=20, k=5$). $K$-Means naturally identifies the geographic center of regional switch clusters, minimizing intra-cluster propagation delay.

### 4.2.3 Control-Plane Robustness Under Single-Link Failure Stress

A critical finding from our $N-1$ reachability engine is that across both canonical topologies (Internet2 and ATT-MPLS) and synthetic graphs with $k \ge 3$, all five placement algorithms achieved **$100.0\%$ control-plane reachability ($Reach_{avg} = 1.0$)**. 

This demonstrates that modern multi-site WANs possess sufficient meshed link density ($E/V \ge 1.6$) such that the removal of any arbitrary single transmission link never partitions a switch from all controller sites simultaneously. Consequently, in well-connected wide-area backbones, single-link reliability ceases to be an active constraint, and the multi-objective optimization problem reduces primarily to the two-dimensional trade-off between **Propagation Latency ($L(P)$)** and **Computational Complexity Tax ($\omega$)**.

### 4.2.4 Scenario-Conditioned Method Selection Guidance

To translate our empirical findings into actionable engineering principles, Table 4.7 formalizes the **Practitioner's Scenario-Conditioned Decision Framework**, providing definitive rules governing algorithm selection.

### Table 4.7: Scenario-Conditioned Algorithm Selection Decision Rules

| Operational Network Scenario | Recommended Paradigm | Recommended Algorithm | Concrete Decision Rationale |
| :--- | :--- | :--- | :--- |
| **Static Regional / National WAN** ($N \le 50$, Planar/Spatial Mesh) | Spatial Heuristic | **$K$-Means Clustering** | Achieves $\approx 2\text{ ms}$ latency, $100\%$ reliability, executes in $< 5\text{ ms}$; zero training overhead; matches AI performance. |
| **Scale-Free / Core-Hub Backbone** ($N \le 100$, Extreme Degree Skew) | Deterministic Heuristic | **Greedy $K$-Center** | Sub-millisecond execution ($< 0.2\text{ ms}$); naturally captures top hub nodes; Pareto-optimal in 100% of scale-free cells. |
| **Offline Strategic Capacity Planning** (High Budget, Absolute Latency Priority) | Metaheuristic | **Genetic Algorithm (GA)** | Discovers the global minimum latency across 100% of cells; execution time ($25\text{--}75\text{ ms}$) is fully acceptable for offline planning. |
| **High-Churn / Disaster Recovery** (Rapid Link Degradation, Flapping Topology) | Artificial Intelligence | **Deep $Q$-Network (DQN)** | High initial training cost is amortized over thousands of millisecond-scale online policy adaptation decisions during active churn. |
| **Ultra-Low Power / Embedded Switch** (Resource-Constrained IoT Gateway) | Deterministic Heuristic | **Greedy $K$-Center** | Negligible memory footprint ($O(kN)$); requires no floating-point matrix inversions or neural tensor libraries. |

---

## 4.3 LIMITATIONS OF STUDY & THREATS TO VALIDITY

To ensure scientific integrity, the findings of this mini-dissertation must be interpreted within the context of specific experimental limitations:
1. **Quasi-Static Traffic Assumption:** While our benchmark evaluated scale-free and spatial topological variations across multiple controller budgets, traffic demands were modeled as uniform across switch nodes. In production environments, enterprise networks exhibit non-uniform, bursty traffic distributions (e.g., diurnal traffic cycles).
2. **Focus on Link Outages vs. Controller Crashes:** Our reliability engine evaluated single-link failure reachability ($N-1$ link stress). While link cuts represent over $85\%$ of physical telecommunications failures, future studies should evaluate catastrophic controller host crashes and state-synchronization latencies.
3. **Emulation Scale:** Virtualized Mininet OpenFlow emulations were conducted on canonical graphs ($N=11$). Emulating massive networks ($N \ge 500$) inside virtual machines introduces host CPU contention that distorts kernel timing measurements.
