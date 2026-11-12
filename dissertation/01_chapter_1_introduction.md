# CHAPTER ONE

# 1.0 INTRODUCTION

## 1.1 OVERVIEW

Wide Area Networks (WANs) support cloud computing, enterprise interconnects, and national research backbones that require low forwarding latency and predictable fault recovery. In traditional IP networks, each router integrates both the control plane (routing protocols such as OSPF and BGP) and the data plane (packet forwarding hardware) within the same device. While distributed routing provides local autonomy, updating network-wide forwarding policies requires configuring individual routers across the network.

Software Defined Networking (SDN) decouples the control plane from the forwarding hardware, centralizing routing and policy decisions in software controllers that program switches via standardized southbound interfaces such as OpenFlow (Ali et al., 2025; AlQaruty et al., 2025; Boudi, 2026). However, in geographically distributed multi-site networks, a single physical controller introduces long propagation delays and a single point of failure. Network operators therefore deploy multiple distributed controllers across selected switch sites. Determining how many controllers to deploy and which switch nodes should host them is known as the Controller Placement Problem (CPP) (Mohanty et al., 2021; Yusuf et al., 2023; Vardhan & SriBhargav, 2025).

## 1.2 BACKGROUND OF STUDY

Contemporary SDN literature formulates the Controller Placement Problem as an $NP$-hard facility location problem over a network graph $G = (V, E)$, demonstrating on wide-area research backbones such as Internet2 that choosing controller locations carefully reduces both average and worst-case switch-to-controller propagation latency (Mohanty et al., 2021; Xu et al., 2023; Priya et al., 2025). In multi-site WAN deployments, controller placement affects three primary operational metrics:

1. Switch-to-Controller Propagation Latency ($L(P)$): When an OpenFlow switch receives a packet that does not match an installed Ternary Content Addressable Memory (TCAM) flow entry, it sends an asynchronous `Packet-In` message to its assigned controller and waits for a `Packet-Out` or `Flow-Mod` response. The shortest-path propagation distance between switches and controllers determines the baseline delay of this control loop (Mohanty et al., 2021; Yue et al., 2022).
2. Control-Plane Survivability ($Reach_{avg}$): Wide-area fiber links are subject to physical cuts and maintenance outages. Under single-link ($N-1$) failures, a link cut along a topological bridge can isolate switches from their assigned controllers, preventing new flow rules from being installed (Wang & Chen, 2021; Kazemi & Montazerolghaem, 2023).
3. Computational Overhead ($\omega_{\text{train}}$ and $\tau_{\text{inf}}$): Algorithms used to select controller locations vary widely in compute time. Single-shot heuristics compute placements directly from the distance matrix in milliseconds, whereas reinforcement learning methods require an iterative offline training phase before fast forward-pass inference can be executed (Kurra et al., 2025; Farahi et al., 2026).

Contemporary work on the CPP spans three primary optimization families: deterministic facility-location approximations and spatial graph partitioning such as Greedy $K$-Center and $K$-Means clustering (Mohanty et al., 2021; Xiao & Chen, 2021; Priya et al., 2025), evolutionary and swarm metaheuristics such as Genetic Algorithms and hybrid HSA-PSO (Radam et al., 2022; Xu et al., 2023; Yusuf et al., 2023), and Deep Reinforcement Learning (DRL) architectures, including MuZero-based agents (Benoudifa et al., 2023), coherent dynamic DRL (CAPFUL) (Kurra et al., 2025), and Adaptive Policy Deep $Q$-Networks (AP-DQN) (Farahi et al., 2026), which formulate controller placement as a Markov Decision Process (MDP).

## 1.3 PROBLEM STATEMENT

Although recent literature frequently proposes Deep Reinforcement Learning for SDN controller placement, published comparisons typically evaluate algorithms on propagation latency alone while omitting computational cost and experimental design details. Specifically, four limitations recur in existing comparative studies:

1. Conflation or Omission of Computational Cost: Studies rarely report the offline training time ($\omega_{\text{train}}$) required for neural policy convergence alongside the online forward-pass inference time ($\tau_{\text{inf}}$) and the execution time of classical heuristics.
2. Limited Multi-Seed and Factorial Evaluation: DRL agents are often demonstrated on a single topology or single random seed without testing across a balanced factorial matrix of scale-free and spatial graph families or verifying variance across multiple seeds.
3. Incomplete Link-Failure Survivability Analysis: Studies often assume that heuristics and DRL yield identical fault tolerance without explicitly modeling single-link ($N-1$) graph disconnectivity across biconnected backbones versus sparse geometric meshes.
4. Lack of Multi-Objective Pareto Synthesis: Without joint evaluation across latency $L(P)$, single-link reachability $Reach_{avg}(P)$, and computational cost $\omega$, infrastructure planners cannot determine when simple heuristics are sufficient and when reinforcement learning is warranted.

## 1.4 RESEARCH GOAL AND OBJECTIVES

### 1.4.1 Research Goal

The goal of this research is to design and execute a reproducible, multi-objective benchmark of classical heuristic, metaheuristic, and Deep Reinforcement Learning controller placement algorithms across canonical and synthetic multi-site SDN topologies ($N \le 50$), quantifying the trade-offs among propagation latency, single-link failure survivability, and computational cost.

### 1.4.2 Specific Research Objectives

1. Construct an automated Python benchmarking pipeline (`ai-sdn-controller-placement`) supporting canonical WAN topologies (`Internet2` and `ATT-MPLS`) and synthetic graph generators (`Barabási-Albert` and `Waxman` at $N \in \{20, 50\}$).
2. Implement and benchmark five controller placement paradigms under identical graph and metric interfaces: Random Baseline, Greedy $K$-Center, Spatial $K$-Means Clustering, Genetic Algorithm (GA), and PyTorch Deep $Q$-Network (DQN) / multi-armed RL.
3. Evaluate DQN convergence over a 1,000-episode pilot on Internet2 and conduct a 10-run multi-seed stability audit ($5\text{ seeds} \times 2\text{ canonical topologies}$) measuring reward stability, action entropy, and per-episode training time.
4. Execute a balanced $5 \times 2 \times 2 \times 3$ multi-seed synthetic factorial experiment ($60\text{ cells} \times 5\text{ seeds} = 300\text{ observations}$) and evaluate main effects via multi-factor ANOVA ($F(4, 240)$) and Tukey HSD post-hoc contrasts.
5. Synthesize two-dimensional and three-dimensional Pareto frontiers across latency $L(P)$, single-link reliability $Reach_{avg}(P)$, and compute overhead, distinguishing offline training cost ($\omega_{\text{train}}$) from online inference latency ($\tau_{\text{inf}}$).
6. Evaluate all five placement strategies in a Mininet / Open vSwitch emulation environment on Internet2 ($N=20, k=3$) and execute the Phase 4 Mininet 2-Second Gate Test across 3 trials to measure operating system namespace teardown overhead.
7. Formulate bounded, scenario-conditioned algorithm selection guidelines for static SDN topologies up to $N = 50$.

## 1.5 SIGNIFICANCE OF STUDY

This study contributes to empirical networking research and practical SDN engineering in three ways:

1. Multi-Objective Evaluation Methodology: By jointly measuring propagation latency $L(P)$, single-link survivability $Reach_{avg}(P)$, offline training time $\omega_{\text{train}}$, and online inference time $\tau_{\text{inf}}$, the benchmark avoids single-metric bias and clarifies the distinction between training overhead and inference speed.
2. Topology-Specific Heuristic Insights: Contrasting scale-free Barabási-Albert graphs against planar Waxman graphs demonstrates how degree distribution and spatial embedding govern the relative accuracy of Greedy $K$-Center and $K$-Means clustering.
3. Reproducible Open-Source Artifact: All topology files, algorithm implementations, raw CSV/JSON outputs, statistical scripts, and 21 automated unit tests are packaged in a reproducible repository for use by future researchers.

## 1.6 ORGANIZATION OF THE DISSERTATION

The remainder of this mini-dissertation is organized as follows:

- Chapter Two (Literature Review) reviews SDN control-plane architecture, mathematical formulations of the $k$-median and $k$-center controller placement problems, heuristics, metaheuristics, Deep $Q$-Networks, and $N-1$ link-failure survivability.
- Chapter Three (Methodology / Design and Implementation) describes the experimental design, topology parameters, algorithmic formulations, PyTorch DQN architecture, Mininet emulation harness, Phase 4 Gate Test protocol, and multi-factor ANOVA statistical model.
- Chapter Four (Results and Discussion) presents the empirical results from the 1,000-episode pilot, the 10-run stability audit, the 300-observation factorial matrix, the 3D Pareto frontier analysis, the 5-way Mininet RTT evaluation, and the Phase 4 Gate Test, followed by bounded deployment guidelines ($N \le 50$) and study limitations.
- Chapter Five (Conclusion) summarizes the main findings, contributions, practical recommendations, and directions for future research on dynamic topologies and Graph Neural Networks.
