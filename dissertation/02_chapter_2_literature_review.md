# CHAPTER TWO

# 2.0 LITERATURE REVIEW

## 2.1 THEORETICAL FOUNDATIONS OF SOFTWARE DEFINED NETWORKING (SDN)

Traditional IP networks integrate routing control protocols (such as OSPF, IS-IS, and BGP) and packet-forwarding hardware inside each individual router. While distributed control allows routers to recompute paths locally during link outages, expressing network-wide traffic engineering, congestion prediction, or security policies requires configuring each device individually across vendor-specific command-line interfaces (Mystakidis et al., 2025; AlQaruty et al., 2025).

Software Defined Networking (SDN) separates network functionality into three planes (Ali et al., 2025; Jaadouni & Saadi, 2025; Boudi, 2026):

1. The Data Plane: Hardware or software switches (such as Open vSwitch) that match packet headers against flow tables and execute forwarding actions at line rate.
2. The Control Plane: One or more software controllers (such as Ryu, ONOS, or OpenDaylight) that maintain a global network topology view and install forwarding rules into switches via southbound protocols such as OpenFlow (Yue et al., 2022; Jadhav & Pujar, 2025).
3. The Application Plane: Intent-based networking, QoS-aware routing, mobility management, and security automation applications that communicate policy requirements to the control plane via northbound APIs (Ali et al., 2025; AlQaruty et al., 2025; Hechmi et al., 2025).

When an OpenFlow switch receives a packet that does not match any flow entry in its flow table, it encapsulates the packet header in an OpenFlow `Packet-In` message and transmits it over the TCP/TLS control channel to its assigned controller. The controller computes a forwarding path and replies with a `Packet-Out` and `Flow-Mod` message (Yue et al., 2022; Priya et al., 2025). Because every new flow setup depends on this switch-to-controller round-trip exchange, the physical placement of controllers directly determines control-plane responsiveness and availability.

## 2.2 FORMALIZATION OF THE CONTROLLER PLACEMENT PROBLEM (CPP)

In a campus or single-site data center network, a single controller instance can manage switches with sub-millisecond propagation delay (Priya et al., 2025). In a wide-area network (WAN) spanning hundreds or thousands of kilometers, optical fiber propagation adds roughly $5\text{ ms}$ per $1,000\text{ km}$, and a single controller becomes both a latency bottleneck and a single point of failure. Multi-site WANs therefore require placing a set of $k$ controllers across the topology (Mohanty et al., 2021; Vardhan & SriBhargav, 2025).

In modern SDN optimization literature, an SDN topology is modeled as an undirected connected graph $G = (V, E)$, where $V$ is the set of $N$ switches, $E$ is the set of $M$ physical links, and $d(v, u)$ is the shortest-path propagation distance between nodes $v$ and $u$ (Mohanty et al., 2021; Yusuf et al., 2023). Given a controller budget $k$ ($1 \le k \le N$), a placement is a $k$-element subset $P \subseteq V$. Two primary facility-location latency objectives govern the CPP (Mohanty et al., 2021; Xiao & Chen, 2021; Xu et al., 2023):

1. Average Switch-to-Controller Propagation Latency ($k$-Median Objective):
   $$L_{avg}(P) = \frac{1}{N} \sum_{v \in V} \min_{c \in P} d(v, c)$$

2. Worst-Case Switch-to-Controller Propagation Latency ($k$-Center Objective):
   $$L_{max}(P) = \max_{v \in V} \min_{c \in P} d(v, c)$$

Both the $k$-median and $k$-center controller placement formulations are $NP$-hard on general graphs (Mohanty et al., 2021; Kazemi & Montazerolghaem, 2023; Vardhan & SriBhargav, 2025). The number of candidate $k$-controller subsets is $\binom{N}{k} = \frac{N!}{k!(N-k)!}$, which grows from $\binom{20}{3} = 1,140$ at $N=20, k=3$ to $\binom{50}{5} = 2,118,760$ at $N=50, k=5$, motivating approximation heuristics, metaheuristics, and learning-based methods (Boudi, 2026; Farahi et al., 2026).

## 2.3 CLASSICAL HEURISTICS & SPATIAL CLUSTERING IN FACILITY LOCATION

### 2.3.1 Greedy $K$-Center Approximation
Farthest-first Greedy $K$-Center traversal provides a deterministic polynomial-time 2-approximation for the $k$-center objective in $\mathcal{O}(k \cdot N)$ distance lookups (Mohanty et al., 2021; Vardhan & SriBhargav, 2025). Starting from an initial center node $c_1$, each subsequent controller $c_i$ ($i = 2, \dots, k$) is placed at the switch that is farthest from the currently selected controller set:
$$c_i = \arg\max_{v \in V} \left( \min_{c \in \{c_1, \dots, c_{i-1}\}} d(v, c) \right)$$
While Greedy $K$-Center executes in sub-millisecond time and bounds worst-case tail latency, placing controllers at extreme peripheral nodes can yield higher average latency $L_{avg}(P)$ than $k$-median partitioning methods (Mohanty et al., 2021; Yusuf et al., 2023).

### 2.3.2 Spatial $K$-Means Clustering and Network Partitioning
Partitioning-based controller placement methods such as $K$-Means and GOKA cluster fusion divide $N$ switches into $k$ sub-domains to minimize within-cluster propagation variance (Xiao & Chen, 2021; Priya et al., 2025). Adapted to network graphs, switches are embedded in a metric coordinate space and partitioned iteratively:

1. Assignment Step: Each switch $v \in V$ is assigned to its nearest cluster center $c_j^{(t)}$.
2. Update Step: Each cluster center is updated to the centroid or discrete graph medoid minimizing intra-cluster distance:
   $$c_j^{(t+1)} = \arg\min_{u \in S_j} \sum_{v \in S_j} d(u, v)$$
$K$-Means directly targets the average latency ($k$-median) objective and performs well on planar geometric networks (Xiao & Chen, 2021; Priya et al., 2025), but its accuracy degrades on non-planar, degree-skewed scale-free topologies where 2D coordinate projections distort shortest-path distances (Vardhan & SriBhargav, 2025).

## 2.4 EVOLUTIONARY COMPUTATION & METAHEURISTICS IN SDN

To optimize non-linear or multi-objective placement criteria without relying on Euclidean coordinate projections, researchers have applied population-based evolutionary and swarm metaheuristics, including Genetic Algorithms (GA), hybrid Harmony Search-Particle Swarm Optimization (HSA-PSO), and critical-switch-aware placement (CPCSA) (Radam et al., 2022; Xu et al., 2023; Yusuf et al., 2023). A GA maintains a population of candidate $k$-node subsets and evolves them over multiple generations using tournament selection, cardinality-preserving crossover, and random node-swap mutation (Radam et al., 2022; Boudi, 2026). Although evolutionary metaheuristics reliably find near-global optima on medium-scale graphs ($N \le 50$), evaluating the shortest-path fitness of every chromosome across dozens of generations requires tens of milliseconds per run—roughly two orders of magnitude more compute time than Greedy $K$-Center.

## 2.5 MACHINE LEARNING & DEEP REINFORCEMENT LEARNING FOR ADAPTIVE PLACEMENT

### 2.5.1 Markov Decision Process (MDP) Formulation
In recent AI-driven SDN optimization (Benoudifa et al., 2023; Hechmi et al., 2025; Kurra et al., 2025; Farahi et al., 2026), controller selection is formulated as a Markov Decision Process $(S, A, P_r, R, \gamma)$:

- State Space ($S$): A vector representation $s_t \in \mathbb{R}^N$ encoding node degrees or current controller locations.
- Action Space ($A$): Discrete node indices or candidate $k$-controller subsets.
- Reward Function ($R$): A scalar signal combining normalized propagation latency reduction and control-plane reachability $Reach_{avg}(P)$.
- Discount Factor ($0 \le \gamma < 1$): Weighting factor for future rewards along an episode trajectory.

### 2.5.2 Deep $Q$-Networks (DQN) and Recent SDN Literature
Deep $Q$-Networks (DQN) approximate the action-value function $Q(s, a; \theta)$ with a neural network trained via experience replay and a periodically synchronized target network $Q(s, a; \theta^-)$ (Kurra et al., 2025; Farahi et al., 2026):
$$\mathcal{L}(\theta) = \mathbb{E}_{(s, a, r, s') \sim \mathcal{D}} \left[ \left( r + \gamma \max_{a'} Q(s', a'; \theta^-) - Q(s, a; \theta) \right)^2 \right]$$
In recent SDN controller placement literature (2021–2026):

- Farahi et al. (2026) proposed AP-DQN for multi-controller placement using a two-hidden-layer MLP ($64 \times 64$ ReLU units), learning rate $\alpha = 0.001$, batch size $32$, discount factor $\gamma = 0.99$, replay buffer capacity $10,000$, and $\epsilon$-greedy decay from $1.0$ to $0.05$.
- Kurra et al. (2025) introduced CAPFUL, a coherent dynamic controller placement method using deep reinforcement learning for adaptive SDN control planes.
- Benoudifa et al. (2023) proposed an autonomous MuZero-based controller placement agent combining tree search with learned latent dynamics.
- Wang & Chen (2021) and Kazemi & Montazerolghaem (2023) modeled link-failure foresight and robust optimization under parameter uncertainty to preserve switch-to-controller connectivity during link outages.

## 2.6 MULTI-OBJECTIVE TRADE-OFFS AND CONTROL-PLANE SURVIVABILITY

### 2.6.1 Single-Link ($N-1$) Failure Survivability
Wide-area fiber links are subject to single-link cuts ($N-1$ failures). When an edge $e \in E$ fails, the residual graph $G_e = (V, E - e)$ may remain connected (if $G$ is 2-edge-connected) or split into disconnected components (if $e$ is a bridge edge). Following Wang & Chen (2021) and Yusuf et al. (2023), single-link control-plane reliability $Reach_{avg}(P)$ is defined as the mean fraction of switches $N_{reach}(G_e, P)$ that retain a valid path to at least one controller in $P$ across all $M$ single-edge removals:
$$Reach_{avg}(P) = \frac{1}{M} \sum_{e \in E} \frac{N_{reach}(G_e, P)}{N}$$

### 2.6.2 Pareto Dominance
When comparing algorithms across propagation latency $L(P)$, reliability $Reach_{avg}(P)$, and compute cost $\omega$ (Radam et al., 2022; Xu et al., 2023; Boudi, 2026), a solution $P_1$ Pareto-dominates $P_2$ ($P_1 \succ P_2$) if $P_1$ is no worse than $P_2$ in all three metrics and strictly better in at least one metric:
$$L(P_1) \le L(P_2), \quad Reach_{avg}(P_1) \ge Reach_{avg}(P_2), \quad \omega(P_1) \le \omega(P_2)$$

## 2.7 LITERATURE SYNTHESIS & RESEARCH GAP

Table 2.1 compares representative studies from the recent SDN controller placement literature (2021–2026) across evaluation metrics, statistical design, and emulation validation.

**Table 2.1: Literature Synthesis on SDN Controller Placement (2021–2026)**

| Study | Primary Method | Topologies Evaluated | Latency $L(P)$ | $N-1$ Link Reliability | Offline vs. Online Time ($\omega_{\text{train}}, \tau_{\text{inf}}$) | Mininet Emulation | Multi-Objective Pareto Analysis |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| Mohanty et al. (2021) | $k$-Center / Latency Minimization | Topology Zoo WANs | Yes ($L_{avg}, L_{max}$) | No | Omitted | No | No |
| Wang & Chen (2021) | Link-Failure Foresight Model | WAN Topologies | Yes | Yes ($N-1$ Links) | Omitted | No | No |
| Xiao & Chen (2021) | GOKA Partition & Cluster Fusion | Topology Zoo WANs | Yes ($L_{avg}$) | No | Partial | No | No |
| Radam et al. (2022) | Hybrid HSA-PSO Metaheuristic | Multi-Controller WAN | Yes ($L_{avg}, L_{max}$) | Partial | Omitted | No | Partial |
| Benoudifa et al. (2023) | MuZero DRL Agent | Topology Zoo WANs | Yes | No | Omitted | No | No |
| Yusuf et al. (2023) | Critical-Switch-Aware (CPCSA) | Topology Zoo / OS3E | Yes | Yes (Critical Links) | Omitted | Yes | No |
| Kurra et al. (2025) | CAPFUL Dynamic DRL | Dynamic SDN WANs | Yes | Partial | Omitted | Partial | No |
| Vardhan & SriBhargav (2025) | Comparative IoT & WAN CPP | IoT / WAN Topologies | Yes | Partial | Analytical | No | No |
| Farahi et al. (2026) | AP-DQN (Deep Q-Network) | Topology Zoo WANs | Yes | Partial | Omitted | No | No |
| This Study (2026) | 5-Way Benchmark (Heuristics, GA, DQN/RL) | Internet2, ATT-MPLS, BA, Waxman ($N \le 50$) | Yes ($L_{avg}, L_{max}$) | Yes ($Reach_{avg}$) | Yes ($\omega_{\text{train}}$ and $\tau_{\text{inf}}$) | Yes (5-Way RTT & Gate Test) | Yes (2D & 3D Frontiers) |

As Table 2.1 shows, recent controller placement studies (2021–2026) have not jointly benchmarked offline training overhead ($\omega_{\text{train}}$), online inference latency ($\tau_{\text{inf}}$), and $N-1$ link-failure survivability against Greedy $K$-Center, $K$-Means, and GA across a multi-seed factorial matrix. Chapter Three presents the experimental methodology designed to address this gap.
