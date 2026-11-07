# Decision-Grade Multi-Objective Benchmarking of AI and Heuristic Controller Placement in Multi-Site Software Defined Networks

By  
Thabang Nhlokoma Buthelezi  
(Student Number: 230011908)

---

A mini-dissertation submitted in partial fulfillment of the requirements for the degree of  
Bachelor of Science Honours in Computer Science  

in the  
Department of Computer Science  
Faculty of Science, Agriculture and Engineering  
University of Zululand  

Supervisor: Prof. Pragasen Mudali  
Co-Supervisor: Mr. Skhumbuzo Zwane  

Year: 2026  

---

## DECLARATION

I, Thabang Nhlokoma Buthelezi (Student Number: 230011908), hereby declare that this mini-dissertation entitled:

> "Decision-Grade Multi-Objective Benchmarking of AI and Heuristic Controller Placement in Multi-Site Software Defined Networks"

is my own original work, conducted under the supervision of Prof. Pragasen Mudali and Mr. Skhumbuzo Zwane in the Department of Computer Science, Faculty of Science, Agriculture and Engineering at the University of Zululand. 

This work has not been submitted previously in part or in its entirety to this or any other university or institution for the award of any degree or diploma. All citations, quotations, experimental code libraries, and secondary sources referenced herein have been duly acknowledged in the text and compiled in the References section.

\
Signature: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
Thabang Nhlokoma Buthelezi  
Date: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  

---

## DEDICATION

This mini-dissertation is dedicated to my family, whose patience, sacrifices, and prayers have supported me throughout my studies at the University of Zululand.

---

## ACKNOWLEDGEMENTS

I wish to express my sincere gratitude to my supervisor, Prof. Pragasen Mudali, and co-supervisor, Mr. Skhumbuzo Zwane, for their guidance, technical feedback, and encouragement throughout the design, implementation, and writing of this research project.

I also thank the academic and technical staff of the Department of Computer Science in the Faculty of Science, Agriculture and Engineering at the University of Zululand for providing the laboratory facilities and learning environment that made this work possible. Finally, I thank my family and fellow Honours students for their support throughout the academic year.

---

## LIST OF FIGURES

- Figure 3.1: End-to-End Comparative Research Methodology Workflow.
- Figure 3.2: System Architecture of the Multi-Objective Controller Placement Benchmark and Mininet Emulation Harness.
- Figure 4.1: PyTorch DQN 1,000-Episode Training Reward Convergence Profile on Canonical Internet2 Topology ($N=20, k=3$).
- Figure 4.2: Multi-Seed DQN Convergence and Rolling Reward Distribution Analysis.
- Figure 4.3: Pareto Latency-Cost Trade-Off Frontier on Barabási-Albert Topology ($N=50, k=3$).
- Figure 4.4: Pareto Latency-Cost Trade-Off Frontier on Waxman Spatial Topology ($N=50, k=3$).
- Figure 4.5: Three-Dimensional Multi-Objective Pareto Surface Mapping Propagation Latency, Single-Link Reliability, and Computational Complexity Tax.
- Figure 4.6: Bounded Infrastructure Deployment Decision Flowchart ($N \le 50$).

---

## LIST OF TABLES

- Table 2.1: Literature Synthesis on SDN Controller Placement (2012–2026).
- Table 3.1: Summary of Canonical and Synthetic Network Topology Parameters.
- Table 3.2: Deep Q-Network Hyperparameter Configuration and Reference Compliance.
- Table 3.3: Full Factorial Benchmark Design Matrix ($2 \times 2 \times 3 \times 5 = 60$ Cells).
- Table 4.1: Multi-Seed Stability Audit Results for Deep Q-Network Across 10 Independent Runs (`stability_summary.csv`).
- Table 4.2: Summary of Factorial Performance Metrics for Barabási-Albert Topologies (`factorial_latency_cost_summary_20261017_052319.csv`).
- Table 4.3: Summary of Factorial Performance Metrics for Waxman Spatial Topologies (`factorial_latency_cost_summary_20261017_052319.csv`).
- Table 4.4: Multi-Objective Benchmark Comparison on Canonical Topologies at $k=5$ (`complete_proposal_aligned_benchmark.csv`).
- Table 4.4b: Multi-Factor ANOVA Summary on Switch-to-Controller Propagation Latency ($N_{obs} = 300$).
- Table 4.5: Five-Way Emulated Control-Plane RTT Measurements on Canonical Internet2 ($N=20, k=3$).
- Table 4.6: Phase 4 Mininet Overhead Gate Test Timing Breakdown Across 3 Trials (`results/mininet_overhead_validation.json`).
- Table 4.6B: Dynamic Topology Churn and Break-Even Amortization Results ($T_{\text{churn}} = 100$ Epochs $\times$ 5 Seeds, `dynamic_churn_summary.csv`).
- Table 4.7: Scenario-Conditioned Algorithm Selection Decision Rules (Bounded to $N \le 50$).
- Table B.1: Complete Proposal-Aligned Multi-Objective Benchmark Matrix Across Canonical and Synthetic Topologies (`complete_proposal_aligned_benchmark.csv`).

---

## LIST OF ABBREVIATIONS

- AI: Artificial Intelligence
- ANOVA: Analysis of Variance
- API: Application Programming Interface
- BA: Barabási-Albert (Scale-Free Network Model)
- CPP: Controller Placement Problem
- CPU: Central Processing Unit
- DQN: Deep Q-Network
- DRL: Deep Reinforcement Learning
- GA: Genetic Algorithm
- HSD: Honest Significant Difference (Tukey's test)
- MDP: Markov Decision Process
- MLP: Multi-Layer Perceptron
- MPLS: Multi-Protocol Label Switching
- NOS: Network Operating System
- OVS: Open vSwitch
- RL: Reinforcement Learning
- RTT: Round-Trip Time
- SDN: Software Defined Networking
- TCAM: Ternary Content Addressable Memory
- WAN: Wide Area Network
- WX: Waxman (Spatial Network Model)

---

## ABSTRACT

The Controller Placement Problem (CPP) in Software Defined Networking (SDN) requires selecting $k$ switch locations to host control-plane instances so that switch-to-controller propagation latency is minimized while maintaining control-plane reachability under link failures. Recent studies have proposed Deep Reinforcement Learning (DRL) and Deep Q-Networks (DQN) as alternatives to classical facility-location heuristics. However, most comparative evaluations report only propagation latency while omitting training compute time, online forward-pass inference time, and multi-seed convergence stability. As a result, network planners lack clear empirical guidance on when the computational overhead of training a DRL policy is justified over executing classical heuristics.

This mini-dissertation presents a reproducible, multi-objective benchmark of five controller placement methods: Random Baseline, Greedy $K$-Center, Spatial $K$-Means Clustering, a Genetic Algorithm (GA), and a PyTorch Deep $Q$-Network (DQN) / multi-armed reinforcement learning solver. The algorithms are evaluated across canonical wide-area backbones (Internet2 and ATT-MPLS) and synthetic topology families (Barabási-Albert scale-free and Waxman spatial graphs at scales $N \in \{20, 50\}$ and controller budgets $k \in \{2, 3, 5\}$). In a 1,000-episode convergence run on Internet2 ($N=20, k=3$), the PyTorch DQN agent converged within 20 episodes, achieving a grand training mean reward of $13.055 \pm 0.589$ and a final 10-episode average reward of $13.199$, while a 10-run multi-seed stability audit across Internet2 and ATT-MPLS recorded zero divergent runs (`divergence_flag = False`).

However, separating offline training overhead ($\omega_{\text{train}}$) from online forward-pass inference time ($\tau_{\text{inf}}$) across the 60-cell multi-seed synthetic factorial matrix ($N_{obs} = 300$, $n = 5$ seeds per cell; multi-factor ANOVA $F(4, 240) = 118.90, p < 0.0001$) demonstrates that classical heuristics and GA match or outperform DRL on static topologies ($N \le 50$) without requiring offline policy training. While a trained DQN executes a single greedy forward pass in $\tau_{\text{inf}} = 0.021\text{--}0.029\text{ ms}$, training the network requires $\omega_{\text{train}} = 21.26\text{ s}$ ($0.0213\text{ s/episode}$), whereas Greedy $K$-Center ($0.026\text{--}0.207\text{ ms}$), $K$-Means ($3.19\text{--}8.14\text{ ms}$), and GA ($12.88\text{--}75.87\text{ ms}$) compute placements directly in a single run. Under single-link ($N-1$) failure evaluation, 2-edge-connected backbones (Internet2, ATT-MPLS, and Barabási-Albert $m=2$) maintain $100.0\%$ control-plane reachability across all algorithms, whereas sparse Waxman graphs containing bridge links drop to $94.47\%\text{--}98.79\%$. Five-way emulation on Internet2 ($N=20, k=3$) confirms that GA ($2.718\text{ ms}$ mean RTT) and $K$-Means ($2.852\text{ ms}$ mean RTT; $5.764\text{ ms}$ worst-case RTT) outperform Greedy $K$-Center ($2.934\text{ ms}$), Bandit RL / DQN ($3.056\text{ ms}$), and Random ($3.374\text{ ms}$). Furthermore, a 1,000-state dynamic link-churn benchmark shows that pre-trained PyTorch DQN inference ($\tau_{\text{inf}} = 0.021\text{--}0.026\text{ ms/epoch}$) amortizes its upfront training overhead after $59.0\text{--}65.2\text{ epochs}$ against GA and $145.8\text{--}207.6\text{ epochs}$ against $K$-Means, although classical heuristics maintain lower post-churn propagation latency.

Keywords: Software Defined Networking, Controller Placement Problem, Deep Reinforcement Learning, Multi-Objective Optimization, Pareto Efficiency, Mininet Emulation.
