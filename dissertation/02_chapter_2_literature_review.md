# CHAPTER TWO

# 2.0 LITERATURE REVIEW

## 2.1 THEORETICAL FOUNDATIONS OF SOFTWARE DEFINED NETWORKING (SDN)

Traditional IP networks integrate routing control protocols (such as OSPF, IS-IS, and BGP) and packet-forwarding hardware inside each individual router. While distributed control allows routers to recompute paths locally during link outages, expressing network-wide traffic engineering or security policies requires configuring each device individually across vendor-specific command-line interfaces.

Software Defined Networking (SDN) separates network functionality into three planes (McKeown et al., 2008; Kreutz et al., 2015):

1. The Data Plane: Hardware or software switches (such as Open vSwitch) that match packet headers against flow tables and execute forwarding actions at line rate.
2. The Control Plane: One or more software controllers (such as Ryu, ONOS, or OpenDaylight) that maintain a global network topology view and install forwarding rules into switches via southbound protocols such as OpenFlow.
3. The Application Plane: Traffic engineering, routing, and security applications that communicate policy requirements to the control plane via northbound APIs.

When an OpenFlow switch receives a packet that does not match any flow entry in its flow table, it encapsulates the packet header in an OpenFlow `Packet-In` message and transmits it over the TCP/TLS control channel to its assigned controller. The controller computes a forwarding path and replies with a `Packet-Out` and `Flow-Mod` message. Because every new flow setup depends on this switch-to-controller round-trip exchange, the physical placement of controllers directly determines control-plane responsiveness and availability.

## 2.2 FORMALIZATION OF THE CONTROLLER PLACEMENT PROBLEM (CPP)

In a campus or single-site data center network, a single controller instance can manage switches with sub-millisecond propagation delay. In a wide-area network (WAN) spanning hundreds or thousands of kilometers, optical fiber propagation adds roughly $5\text{ ms}$ per $1,000\text{ km}$, and a single controller becomes both a latency bottleneck and a single point of failure. Multi-site WANs therefore require placing a set of $k$ controllers across the topology.

Heller et al. (2012) modeled an SDN topology as an undirected connected graph $G = (V, E)$, where $V$ is the set of $N$ switches, $E$ is the set of $M$ physical links, and $d(v, u)$ is the shortest-path propagation distance between nodes $v$ and $u$. Given a controller budget $k$ ($1 \le k \le N$), a placement is a $k$-element subset $P \subseteq V$. Heller et al. (2012) analyzed two primary facility-location objectives:

1. Average Switch-to-Controller Propagation Latency ($k$-Median Objective):
   $$L_{avg}(P) = \frac{1}{N} \sum_{v \in V} \min_{c \in P} d(v, c)$$

2. Worst-Case Switch-to-Controller Propagation Latency ($k$-Center Objective):
   $$L_{max}(P) = \max_{v \in V} \min_{c \in P} d(v, c)$$

Both the $k$-median and $k$-center problems are $NP$-hard on general graphs (Kariv & Hakimi, 1979; Gonzalez, 1985). The number of candidate $k$-controller subsets is $\binom{N}{k} = \frac{N!}{k!(N-k)!}$, which grows from $\binom{20}{3} = 1,140$ at $N=20, k=3$ to $\binom{50}{5} = 2,118,760$ at $N=50, k=5$, motivating approximation heuristics, metaheuristics, and learning-based methods.

## 2.3 CLASSICAL HEURISTICS & SPATIAL CLUSTERING IN FACILITY LOCATION

### 2.3.1 Greedy $K$-Center Approximation (Gonzalez's Algorithm)
Gonzalez (1985) presented a deterministic farthest-first traversal algorithm for the $k$-center problem that guarantees a worst-case approximation factor of 2 in $\mathcal{O}(k \cdot N)$ distance lookups. Starting from an initial center node $c_1$, each subsequent controller $c_i$ ($i = 2, \dots, k$) is placed at the switch that is farthest from the currently selected controller set:
$$c_i = \arg\max_{v \in V} \left( \min_{c \in \{c_1, \dots, c_{i-1}\}} d(v, c) \right)$$
While Greedy $K$-Center executes in sub-millisecond time and bounds worst-case tail latency, placing controllers at extreme peripheral nodes can yield higher average latency $L_{avg}(P)$ than $k$-median methods.

### 2.3.2 Spatial $K$-Means Clustering
MacQueen (1967) formulated $K$-Means clustering to partition $N$ points into $k$ clusters minimizing within-cluster variance. Adapted to network graphs, switches are embedded in a metric coordinate space and partitioned iteratively:

1. Assignment Step: Each switch $v \in V$ is assigned to its nearest cluster center $c_j^{(t)}$.
2. Update Step: Each cluster center is updated to the centroid or discrete graph medoid minimizing intra-cluster distance:
   $$c_j^{(t+1)} = \arg\min_{u \in S_j} \sum_{v \in S_j} d(u, v)$$
$K$-Means directly targets the average latency ($k$-median) objective and performs well on planar geometric networks, but its accuracy degrades on non-planar, degree-skewed scale-free topologies where 2D coordinate projections distort shortest-path distances.

## 2.4 EVOLUTIONARY COMPUTATION & METAHEURISTICS IN SDN

To optimize non-linear or multi-objective placement criteria without relying on Euclidean coordinate projections, researchers have applied evolutionary metaheuristics such as Genetic Algorithms (GA) (Holland, 1975; Goldberg, 1989; Yusuf et al., 2023). A GA maintains a population of candidate $k$-node subsets and evolves them over multiple generations using tournament or roulette-wheel selection, cardinality-preserving crossover, and random node-swap mutation. Although GAs reliably find near-global optima on medium-scale graphs ($N \le 50$), evaluating the shortest-path fitness of every chromosome across dozens of generations requires tens of milliseconds per run—roughly two orders of magnitude more compute time than Greedy $K$-Center.

## 2.5 MACHINE LEARNING & DEEP REINFORCEMENT LEARNING FOR ADAPTIVE PLACEMENT

### 2.5.1 Markov Decision Process (MDP) Formulation
In reinforcement learning approaches to the CPP (Sutton & Barto, 2018), controller selection is formulated as a Markov Decision Process $(S, A, P_r, R, \gamma)$:

- State Space ($S$): A vector representation $s_t \in \mathbb{R}^N$ encoding node degrees or current controller locations.
- Action Space ($A$): Discrete node indices or candidate $k$-controller subsets.
- Reward Function ($R$): A scalar signal combining normalized propagation latency reduction and control-plane reachability $Reach_{avg}(P)$.
- Discount Factor ($0 \le \gamma < 1$): Weighting factor for future rewards along an episode trajectory.

### 2.5.2 Deep $Q$-Networks (DQN) and Recent SDN Literature
Mnih et al. (2015) introduced Deep $Q$-Networks (DQN), approximating the action-value function $Q(s, a; \theta)$ with a neural network trained via experience replay and a periodically synchronized target network $Q(s, a; \theta^-)$:
$$\mathcal{L}(\theta) = \mathbb{E}_{(s, a, r, s') \sim \mathcal{D}} \left[ \left( r + \gamma \max_{a'} Q(s', a'; \theta^-) - Q(s, a; \theta) \right)^2 \right]$$
In recent SDN controller placement literature:

- Farahi et al. (2026) proposed AP-DQN for multi-controller placement using a two-hidden-layer MLP ($64 \times 64$ ReLU units), learning rate $\alpha = 0.001$, batch size $32$, discount factor $\gamma = 0.99$, replay buffer capacity $10,000$, and $\epsilon$-greedy decay from $1.0$ to $0.05$.
- Benoudifa et al. (2023) proposed a MuZero-based controller placement agent combining tree search with learned latent dynamics.
- Radam et al. (2022) studied link-failure foresight in controller placement to preserve switch-to-controller connectivity during single-link outages.

## 2.6 MULTI-OBJECTIVE TRADE-OFFS AND CONTROL-PLANE SURVIVABILITY

### 2.6.1 Single-Link ($N-1$) Failure Survivability
Wide-area fiber links are subject to single-link cuts ($N-1$ failures). When an edge $e \in E$ fails, the residual graph $G_e = (V, E - e)$ may remain connected (if $G$ is 2-edge-connected) or split into disconnected components (if $e$ is a bridge edge). Following Radam et al. (2022), single-link control-plane reliability $Reach_{avg}(P)$ is defined as the mean fraction of switches $N_{reach}(G_e, P)$ that retain a valid path to at least one controller in $P$ across all $M$ single-edge removals:
$$Reach_{avg}(P) = \frac{1}{M} \sum_{e \in E} \frac{N_{reach}(G_e, P)}{N}$$

### 2.6.2 Pareto Dominance
When comparing algorithms across propagation latency $L(P)$, reliability $Reach_{avg}(P)$, and compute cost $\omega$, a solution $P_1$ Pareto-dominates $P_2$ ($P_1 \succ P_2$) if $P_1$ is no worse than $P_2$ in all three metrics and strictly better in at least one metric:
$$L(P_1) \le L(P_2), \quad Reach_{avg}(P_1) \ge Reach_{avg}(P_2), \quad \omega(P_1) \le \omega(P_2)$$

## 2.7 LITERATURE SYNTHESIS & RESEARCH GAP

Table 2.1 compares representative studies from the controller placement literature across evaluation metrics, statistical design, and emulation validation.

**Table 2.1: Literature Synthesis on SDN Controller Placement (2012–2026)**

| Study | Primary Method | Topologies Evaluated | Latency $L(P)$ | $N-1$ Link Reliability | Offline vs. Online Time ($\omega_{\text{train}}, \tau_{\text{inf}}$) | Mininet Emulation | Multi-Objective Pareto Analysis |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| Heller et al. (2012) | Exhaustive / $k$-Median | Internet2, Topology Zoo | Yes ($L_{avg}, L_{max}$) | No | Omitted | No | No |
| Gonzalez (1985) | Greedy $K$-Center | General Metric Graphs | Yes ($L_{max}$) | No | Analytical $\mathcal{O}(kN)$ | No | No |
| MacQueen (1967) | $K$-Means Clustering | Metric Spaces | Yes ($L_{avg}$) | No | Analytical $\mathcal{O}(kNt)$ | No | No |
| Radam et al. (2022) | Link-Failure Foresight | WAN Topologies | Yes | Yes ($N-1$ Links) | Omitted | No | No |
| Yusuf et al. (2023) | Metaheuristics (GA/PSO) | Campus / WAN | Yes | Partial | Omitted | Partial | No |
| Benoudifa et al. (2023) | MuZero DRL | Synthetic WAN | Yes | No | Omitted | No | No |
| Farahi et al. (2026) | AP-DQN (DRL) | Topology Zoo WANs | Yes | Partial | Omitted | No | No |
| This Study (2026) | 5-Way Benchmark (Heuristics, GA, DQN/RL) | Internet2, ATT-MPLS, BA, Waxman ($N \le 50$) | Yes ($L_{avg}, L_{max}$) | Yes ($Reach_{avg}$) | Yes ($\omega_{\text{train}}$ and $\tau_{\text{inf}}$) | Yes (5-Way RTT & Gate Test) | Yes (2D & 3D Frontiers) |

As Table 2.1 shows, prior DRL controller placement studies have not jointly benchmarked offline training overhead ($\omega_{\text{train}}$), online inference latency ($\tau_{\text{inf}}$), and $N-1$ link-failure survivability against Greedy $K$-Center, $K$-Means, and GA across a multi-seed factorial matrix. Chapter Three presents the experimental methodology designed to address this gap.
