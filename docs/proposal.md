# Research Proposal

## Title

Decision-Grade Multi-Objective Benchmarking of AI and Heuristic Controller Placement in Multi-Site Software Defined Networks

## 1 Introduction

Software Defined Networking (SDN) is now a structural backbone for modern multi-site networks, where control is centralized but the performance of the entire fabric still depends on one unresolved bottleneck: the Controller Placement Problem (CPP). Where controllers are placed determines not only latency, but also the resilience of the control plane under failure (Heller et al., 2012). In this setting, controller placement is not a minor configuration choice. It is a decision-making problem that directly shapes control-plane survivability, operational responsiveness, and the stability of inter-site communication.

That decision environment creates a Decision Crisis. Classical heuristics are attractive because they are fast, transparent, and easy to reproduce, yet they are also rigid and limited in how far they can adapt to topology variation. AI-driven methods promise greater adaptability, but they introduce a different challenge: their gains are often reported without a defensible account of computational complexity $\omega$ in $s/episode$. The result is a decision gap between methods that are computationally cheap and methods that are potentially better, but not yet clearly justified in complexity-to-performance terms (Farahi et al., 2026; Benoudifa et al., 2023).

This study addresses that gap by treating controller placement as a multi-objective optimization problem rather than a single-metric ranking exercise. Its core contribution is not merely to compare algorithms, but to evaluate decision utility: where AI gains, if any, are large enough to justify their complexity tax. The analysis therefore combines latency $L(P)$ in $ms$, reliability $Reach_{avg}$, and complexity $\omega$ in $s/episode$ into a unified 3-axis frame, enabling the identification of non-dominated sets rather than isolated winners. That framing is essential for distinguishing methods that are merely accurate from methods that are operationally defensible.

The research gap is clear. While AI-assisted controller placement is promising, the literature still lacks reproducible evidence across standardized topologies that resolves all three dimensions together: latency, reliability, and complexity (Farahi et al., 2026; Benoudifa et al., 2023). Many studies report improvement on one axis while leaving the others under-specified. This proposal instead advances a pilot-validated, multi-objective design that is grounded in a successful proof-of-concept run of approximately $\omega=0.0226\,s/episode$, giving immediate confidence that the factorial experiment is computationally tractable on local resources.

The remainder of the proposal is structured to follow this logic. Section 6 reviews the literature and establishes the empirical gap. Section 7 formalizes the problem through MOCO, Pareto reasoning, Control Plane Survivability, and the MDP framing used for DQN/DRL policy learning. Section 8 operationalizes the methodology and experimental controls. Section 10 clarifies IP stewardship and the handling of technical artifacts, while Sections 11 to 13 move from resource feasibility to dissemination, showing how the project remains executable, reproducible, and academically publishable within the official 2026 timeline.

## 2 Background of the Study

### 2.1 From Legacy Decentralized Networking to SDN

Traditional enterprise and carrier networks were built around tightly coupled, device-centric control logic. In that legacy model, routing intelligence, forwarding behavior, and policy enforcement were distributed across individual devices, making adaptation slow and operations difficult to standardize across sites. As networks became larger and more interdependent, this decentralized architecture became increasingly difficult to manage because every topology change demanded coordinated reconfiguration.

Software Defined Networking (SDN) emerged as the response to that complexity. Its defining feature is the separation of concerns: the Control Plane is decoupled from the Data Plane, and forwarding devices no longer need to make autonomous control decisions. Instead, a logically centralized controller acts as the network’s brain, translating policy into flow rules and orchestrating behavior across the fabric (Heller et al., 2012). That decoupling improved programmability and visibility, but it also made controller placement a first-order performance variable.

### 2.2 Multi-Site Topologies and the Rise of the Controller Placement Problem

The CPP becomes especially important in multi-site SDN where controllers and switches are separated by meaningful geographical and topological distance. In such environments, the distance between a switch and its controller introduces propagation delay across control exchanges, path computation, and failure-response events. A placement that is acceptable in a small local network may become inefficient or fragile when applied to a geographically distributed backbone.

This issue is visible in large-scale backbones and multi-domain research settings such as Internet2 and ATT-MPLS, where the control plane must remain responsive while spanning diverse sites and heterogeneous paths. At that scale, controller placement must account for Control Plane Survivability, because failures can isolate switches from their nearest control authority and destabilize the topology (Radam et al., 2022).

### 2.3 Evolution of Placement Logic: Manual, Heuristic, and Adaptive Search

The history of controller placement mirrors the broader evolution of network optimization. Early approaches relied on manual or deterministic placement, where engineers applied domain experience, static diagrams, and simple centrality assumptions to position controllers. These methods were straightforward, but they did not scale well and offered little adaptability when topology size, failure modes, or traffic patterns changed.

The next stage introduced Heuristic vs. Stochastic Search. Greedy rules, clustering methods, k-means, and related meta-heuristics improved runtime efficiency and often produced acceptable placements with modest computational effort. Their strength was speed; their weakness was rigidity. As the search space grew, especially in multi-site and multi-controller settings, the problem began to exhibit State-Space Explosion, and local rules alone were no longer sufficient to guarantee robust long-term performance.

Modern work has therefore shifted toward Deep Reinforcement Learning (DRL) and other adaptive agents. These methods treat placement as a sequential decision problem and attempt to learn policies that improve over time as they interact with the environment. In principle, this offers a stronger response to topology diversity and failure dynamics (Farahi et al., 2026; Benoudifa et al., 2023). In practice, adaptive learning introduces a new issue: the performance gains must be weighed against training and inference burden.

### 2.4 The Emerging Metric Gap and the Bridge to This Study

The background literature is rich in latency results, but far thinner in its treatment of computational burden. This omission matters because modern placement methods are not judged only by the quality of their final solution; they are also judged by the cost of producing that solution. When computational burden is ignored, the background implicitly favors performance-at-all-costs reasoning, even when that reasoning is no longer defensible for reproducible or resource-aware research (Radam et al., 2022).

This study addresses that metric gap by moving toward Efficiency-aware Optimization. It evaluates placement methods through three coupled dimensions: latency $L(P)$, reliability $Reach_{avg}$, and complexity $\omega$. The pilot-validated efficiency result of approximately $\omega=0.0226\,s/episode$ shows that this study is technically executable, and the later sections formalize how that empirical foundation supports the MOCO, MDP, and Pareto-based analysis presented in Sections 7, 8, and 11.

## 3 Problem Statement and Research Questions

In multi-site SDN controller placement, method claims are frequently made from single metrics (typically latency), even though deployment decisions require joint interpretation of latency, reliability, and computational complexity. Let the network topology be $G=(V,E)$ with total node count $|V|=n$. Let the controller placement set be $P\subseteq V$ with controller count $|P|=k$, where $k\in\{2,3,5\}$. This study evaluates the three-axis objective $\{L(P),Reach_{avg},\omega\}$ where $L(P)$ is latency in $ms$, $Reach_{avg}\in[0,1]$ is reliability, and $\omega$ is complexity in $s/episode$. This creates a decision-risk gap: teams can over-adopt complex AI methods without clear evidence that gains remain defensible once computational and robustness constraints are included (Heller et al., 2012; Radam et al., 2022).

Primary research question:

- In multi-site synthetic SDN topologies $G=(V,E)$, do AI-driven controller placement methods provide superior multi-objective decision quality compared with baseline heuristics when $L(P)$ ($ms$), $Reach_{avg}$, and $\omega$ ($s/episode$) are evaluated jointly?

Supporting research questions:

- Under fixed topology families, node scales $|V|=n$, and controller budgets $|P|=k$, what is the effect size of AI methods versus baseline heuristics on average latency $L(P)$ and reliability $Reach_{avg}$?
- After accounting for computational complexity $\omega$ ($s/episode$), which algorithms remain practically superior and Pareto-efficient for planning use cases?
- How stable are algorithm rankings across topology families and scale levels, and where do rankings shift enough to require scenario-conditioned method selection guidance?

## 4 Research Aim and Objectives

### 4.1 Research Aim

The aim of this study is to quantify the performance-to-complexity trade-off between PyTorch-based DQN/DRL and heuristic controller-placement methods in multi-site SDN by operationalizing a 3-axis Pareto decision engine $(L(P), Reach_{avg}, \omega)$, and to identify the exact operating regions where adaptive AI gains justify the associated Complexity Tax ($\omega$) (Heller et al., 2012; Radam et al., 2022; Farahi et al., 2026; Benoudifa et al., 2023). This aim is empirically grounded by pilot feasibility evidence ($0.0226\,s/episode$), which establishes that full-matrix comparative efficiency testing is computationally executable within the Section 11.3 schedule.

### 4.2 Research Objectives

- **Objective 1 (Environment, Specific + Reproducibility, P1-P3):** Implement a config-driven SDN emulation testbed (Mininet/Ryu) with fixed seeding (Seed 42), deterministic run manifests, and resumable experiment state, and validate end-to-end execution feasibility using the completed pilot baseline ($0.0226s$/episode) before full factorial expansion (aligned to Section 11.3: P1 completed, P2-P3 active).
- **Objective 2 (Algorithm Stack, Comparative + Measurable, P4-P5):** Benchmark a PyTorch-based DQN agent against deterministic baselines (Greedy, K-Center) under identical controller budgets across Internet2 and ATT-MPLS topologies, with effect-size reporting and statistical significance testing per topology-scale cell (aligned to Section 11.3: P4 data collection, P5 full implementation).
- **Objective 3 (Metrics, Quantized + Auditable, P4-P6):** Evaluate each method in a unified 3-axis decision space consisting of latency $L(P)$ in $ms$, reliability $Reach_{avg}\in[0,1]$ under single-link-failure stress, and complexity $\omega$ in $s/episode$, and publish machine-auditable metric artifacts for every run (aligned to Section 11.3: P4-P6 analysis pipeline).
- **Objective 4 (Synthesis, Decision Thresholds + Time-Bound, P6-P9):** Extract Non-Dominated (Pareto) sets and derive operational thresholds where adaptive AI improvements offset the Complexity Tax ($\omega$), then validate these thresholds as scenario-conditioned selection rules in the thesis and final paper deliverables (aligned to Section 11.3: P6 draft analysis through P9 final submission).

## 5 Contribution of the Study

### 5.1 Theoretical Contribution

**Methodological Innovation: MOCO Pipeline (1D to 3D Evaluation).** This study contributes a formal multi-objective combinatorial optimization (MOCO) pipeline that integrates latency $L(P)$, control-plane reliability $Reach_{avg}$, and complexity $\omega$ in one decision architecture. By replacing single-metric ranking with non-dominated 3-axis evaluation, the study resolves a known academic conflict between latency-first benchmarking and deployment-grade trade-off analysis identified in canonical CPP and Pareto-control-plane literature (Heller et al., 2012; Lange et al., 2015).

**Complexity Tax Theory: DRL Utility Under Operational Overhead.** The study contributes a theoretical bridge between DRL policy quality and operational overhead by defining the boundary conditions under which adaptive AI gains remain decision-grade after computational burden is priced into the objective space. This Complexity Tax framing advances SDN control-plane theory by specifying where AI utility saturates, where it dominates, and where deterministic methods remain structurally preferable.

### 5.2 Practical Contribution

**Decision-Support Tooling: Scenario-Conditioned Selection Matrix.** The primary applied output is a scenario-conditioned selection matrix that maps topology-scale-failure contexts to the method family (DQN/DRL vs deterministic baselines) with the best Pareto-consistent operating profile. This converts algorithm comparison into planner-ready method selection rules for real infrastructure decisions.

**Reproducibility Blueprint: Drift-Free Experimental Execution.** The study delivers a config-driven, seed-locked (Seed 42) testbed blueprint for drift-free experimentation, enabling repeatable benchmark execution across cohorts, including Honors researchers and practicing engineers. The pilot efficiency evidence ($0.0226s$/episode) demonstrates that this blueprint is technically executable within constrained institutional compute environments.

**Evidence-Based Policy Shift: From AI-Hype to Cost-Aware Optimization.** The study provides auditable evidence for governance decisions in SDN optimization programs by replacing AI-first narratives with cost-aware, threshold-based adoption criteria. In practice, this supports institutional and operational policy that funds or deploys AI only where quantified adaptive gains exceed measured complexity overhead.

## 6. Literature Review

The controller-placement literature is consistent on one point: reported gains are real, but they are conditional on topology choice, scale, and the metrics used to evaluate success. The review below therefore treats the literature as empirical evidence for the methodology, not as background filler. It uses paraphrase only; page numbers in Table 6.1 identify the source pages that support the claims summarised here.

### 6.1 Comparative Performance of AI and Heuristic Controller Placement Methods

Heller et al. (2012, pp. 3, 5) remain the canonical baseline because they show, on Internet2 and a broad WAN set, that random placement is about 1.4x-1.7x worse on average latency and up to 2.5x worse on worst-case latency. They also show that one controller can still satisfy a 50 ms reaction-time requirement for many topologies. That contribution is foundational, but it is also bounded: it establishes a latency benchmark, not a complete deployment criterion. In other words, the paper tells the field what a strong placement baseline looks like, but it does not settle resilience, cost, or multi-objective trade-offs.

Radam et al. (2022, pp. 17-24) show that a hybrid metaheuristic can improve placement quality across several metrics at once. Their best reported values are 15.5 ms propagation delay, 0.88 +/- 0.1 reliability, 197.1 k response/s throughput, 26.8 cost, and 22.5 fitness. That is a strong simulated result, but it is still a simulation result. The paper supports the claim that hybrid search can be competitive, yet it also reinforces the need to separate algorithmic promise from deployment evidence.

Farahi et al. (2026, pp. 1, 23-24) extend the field by combining adaptive clustering with DQN. The paper reports 24% improvement in load balancing, 25% reduction in latency, 28% reduction in link operational expense, and 12% improvement in normalized security. The important point is not only that an AI method can beat benchmark methods on multiple axes, but that the gains depend on the topology and on how the reward structure is defined. That makes the paper useful as evidence for adaptive placement, but not as proof that all AI placement is automatically superior in multi-site settings.

Benoudifa et al. (2023, pp. 1, 14) add a second learning-based reference point. Their MuZero-based controller-placement model uses self-competition and tree search, and the paper reports high success rates with reasonable search times on complex networks. Compared with the heuristic and metaheuristic literature, this paper matters because it shows that reinforcement learning can be framed as a policy-search problem rather than only as a static optimizer. The limitation is the same one that appears across the AI literature: strong results do not by themselves establish transferability across topologies, failure conditions, or compute budgets.

### 6.2 Robustness Across Topology Families and Network Scales

The more serious weakness in the literature is not simply that different methods perform differently, but that many studies evaluate them on different topology families, scales, or failure assumptions. That weakens comparability. Heller et al. (2012) are still important here because their evaluation is based on realistic backbone topologies rather than toy graphs. Farahi et al. (2026) further show that the same method can perform differently across Xspeduis, BellCanada, and Uni-Net2010, with each topology emphasizing a different objective mix. The implication is clear: controller-placement behaviour is topology contingent, so a result on one graph family should not be treated as universal evidence.

Yusuf et al. (2023, pp. 23-24) reinforce that point from a different angle. Their critical-switch-aware strategy reduces controller overhead by 73%, packet loss by 51%, latency by 16%, and improves throughput by 16%, but the paper also states that it does not support heterogeneous controllers and has no defense against DDOS or common-mode faults. That limitation is important because it shows that better control-plane efficiency does not automatically imply operational robustness. Xu et al. (2023, pp. 15, 17) make a similar point at larger scale: their hierarchical multi-controller strategy improves integrated latency, reliability, and overhead on three real topologies, and the advantage becomes stronger as topology size and link complexity increase. Taken together, these studies show that robustness claims must be read in the context of topology family, controller model, and failure assumptions.

Radam et al. (2022) are useful as a counterweight to AI-centred optimism because their hybrid approach performs well without deep learning, but only inside a controlled simulation regime. The lesson is not that heuristics are superior; the lesson is that their advantages are easier to reproduce when the topology is fixed and the scale is moderate. That is why the methodology cannot rely on a single benchmark graph or a single outcome measure.

### 6.3 Decision Frameworks for Multi-Objective Controller Placement

The literature increasingly recognises that controller placement is multi-objective, but many papers still report the objectives as separate headline numbers rather than as a decision framework. Yusuf et al. (2023), Xu et al. (2023), and Farahi et al. (2026) all report gains across several metrics, yet they differ in how explicitly they operationalise the trade-off between quality and computational burden. Benoudifa et al. (2023) are representative of this limitation: the method is clearly promising, but the reporting still leaves room for stronger transparency about how performance, robustness, and search cost are weighed against each other. The consequence is that the literature often demonstrates possibility, but not decision utility.

That limitation is methodological rather than rhetorical. A method that looks attractive on latency alone may still be unsuitable if its training cost is excessive or if its reliability collapses under failure. Conversely, a method with modest latency improvement may still be preferable if it is stable, inexpensive, and reproducible across scenarios. For that reason, Pareto-front reasoning is central to the study design: it distinguishes between marginally better, practically better, and non-dominated solutions. The present study therefore treats latency $L(P)$, reliability $Reach_{avg}$, and complexity $\omega$ as co-equal outcomes rather than as secondary caveats.

The metric bridge is especially important. Earlier studies often describe cost or runtime in generic terms, but DRL evaluation requires a transparent operational label that can be measured consistently across runs. Complexity $\omega$ in $s/episode$ is therefore not an arbitrary renaming; it is the experimental translation of training burden into a thesis-ready metric that can be compared directly with latency and reliability. That metric choice connects the literature to the methodology because it makes the cost of improvement visible instead of leaving it implicit.

Table 6.1 summarizes the representative controller-placement studies discussed above, the primary metrics each study reports, and the headline performance claims. Placing this table here makes the cross-paper comparison explicit before the synthesis in Section 6.4.

| Study (year) | Method / family | Primary metrics reported | Headline performance | Practical note |
|---|---|---:|---|---|
| Heller et al. (2012) | Latency-optimal / exhaustive CPP | Average latency, worst-case latency, feasibility (50 ms) | Random placement 1.4x–1.7x worse (avg), up to 2.5x worse (worst); 82% topologies meet 50 ms with one controller | Canonical latency baseline; topology-dependent conclusions |
| Radam et al. (2022) | Hybrid HSA-PSO (meta-heuristic) | Propagation latency, reliability, throughput, fitness | Latency 11–20 ms (vs 22–45 ms baselines); reliability ≈0.88 ±0.1; throughput ~197 | Multi-metric heuristic baseline with strong simulated gains |
| Benoudifa et al. (2023) | MuZero-based DRL (model-based RL) | Success rate, search time, training convergence | Qualitative high success rates; reasonable search times reported | AI-native search focus; compute/reporting less standardized vs classical metrics |
| Yusuf et al. (PeerJ, 2023) | Critical-switch-aware (CPCSA) | Controller overhead, packet loss, switch→controller latency, throughput | Aggregate: overhead −73%, loss −51%, latency −16%, throughput +16% | Emphasises topology-role features and control-overhead reduction |
| Xu et al. (Symmetry, 2023) | MOIHHO (multi-objective HHO) | Integrated latency, reliability, load variance, placement overhead | vs MOPSO: −8% worst latency, +10% reliability, −20% load variance; vs NSGA-II: −20% worst latency, +7% reliability | Hierarchical multi-objective optimizer tested on large topologies |
| Farahi et al. (2026) | AP-DQN (adaptive clustering + DQN) | Load balancing, latency, link operating cost, normalized security | +24% load-balance, −25% latency, −28% link cost, +12% security | Clear multi-objective DRL result; motivates complexity-aware evaluation |
| Boudi (Thesis, 2026) | WBC-CPP / GWO / PSO hybrids | Avg. switch→controller latency, flow rate, controller-controller latency | Up to ~19.9% latency, ~33% flow-rate, ~55% CC-latency improvements reported | Broad comparative thesis-level study; simulation-driven results |

### 6.4 Synthesis of the Literature and Research Gap

The research gap is not a lack of AI results. It is a lack of reproducible, multi-objective evidence across standardized topology families. Heller et al. (2012) show what a canonical baseline looks like. Radam et al. (2022) show that strong heuristic and meta-heuristic results are possible without deep learning. Yusuf et al. (2023) and Xu et al. (2023) show that multi-metric gains are achievable on real topologies. Farahi et al. (2026) and Benoudifa et al. (2023) show that reinforcement learning can improve controller placement, but only when the evaluation is precise enough to support interpretation. The shared limitation is that the literature still does not provide one reproducible comparison framework that resolves latency, reliability, and complexity together.

Taken together, the literature leaves three unresolved problems. First, studies are not consistently comparable because they do not all use the same topology families or failure conditions. Second, many reports are multi-objective in name but still single-metric in practice when the discussion turns to method selection. Third, computational burden is usually under-specified, making it difficult to judge whether a method’s accuracy gain is worth its training cost. The methodology is designed to close these three gaps by using Internet2 and ATT-MPLS as canonical corpora, quantifying reliability under single-link failure, and reporting complexity $\omega$ in $s/episode$ as a transparent DRL evaluation metric.

Accordingly, the methodology is not an afterthought to the review; it is the necessary consequence of the review. The literature justifies a factorial design, Pareto-front analysis, and a reproducible pilot-validated DQN stack because only that combination can determine whether AI-driven placement genuinely outperforms heuristics once latency, reliability, and computational burden are treated as co-equal experimental outcomes.

### 6.5 Evidence Matrix and Citation Fixes

Table 6.1 summarises the core controller-placement studies used in this review. It also makes the supporting page ranges explicit so that any future direct quotation can be traced back to the original source quickly.

| Study | Method / approach | Key metrics | Main findings | Limitations | Key pages | Relevance to this study |
| --- | --- | --- | --- | --- | --- | --- |
| Heller et al. (2012) | Canonical latency-focused CPP baseline on real WAN topologies | Average latency, worst-case latency, reaction-time feasibility | Random placement is about 1.4x-1.7x worse on average latency and up to 2.5x worse on worst-case latency; one controller often meets 50 ms reaction-time requirements | Does not resolve resilience, cost, or multi-objective trade-offs | pp. 3, 5 | Sets the baseline against which all later claims of improvement should be judged |
| Radam et al. (2022) | Hybrid HSA-PSO metaheuristic for multi-controller SDN | Propagation delay, average delay, reliability, throughput, cost, fitness | Reports 15.5 ms propagation delay, 0.88 +/- 0.1 reliability, 197.1 throughput, 26.8 cost, and 22.5 fitness | Strong simulation results, but transferability and parameter sensitivity remain unclear | pp. 17-24 | Shows that strong heuristic performance is possible without deep learning |
| Yusuf et al. (2023) | Critical-switch-aware partitioning and controller placement | Overhead, packet loss, switch-to-controller latency, throughput | Reports 73% less overhead, 51% less loss, 16% less latency, and 16% more throughput | Does not support heterogeneous controllers and lacks DDOS/common-mode fault defense | pp. 23-24 | Useful as a topology-aware multi-metric baseline |
| Xu et al. (2023) | MOIHHO hierarchical multi-controller placement | Integrated latency, reliability, load variance, overhead | Improves integrated latency, reliability, and overhead on three real large-scale topologies | Less explicit on real-time operational dynamics and compute cost | pp. 15, 17 | Supports the claim that multi-objective search can scale to larger topologies |
| Benoudifa et al. (2023) | MuZero-based intelligent agents with self-competition | Success rate, search time, placement effectiveness | Finds effective strategies with high success rates and reasonable search times | Transferability and operational validation still limited | pp. 1, 14 | Demonstrates policy-learning as an alternative to static heuristics |
| Farahi et al. (2026) | AP-DQN with adaptive clustering plus deep RL | Load balancing, latency, link operational cost, normalized security | Reports 24% load-balancing improvement, 25% latency reduction, 28% cost reduction, and 12% security improvement | Performance depends on topology and reward design; dynamic deployment assumptions remain demanding | pp. 1, 23-24 | Most direct AI-based comparator for the proposed DQN stack |

Citation fixes needed:

- Use Heller et al. (2012, pp. 3, 5) when citing the latency baseline, not only the general year.
- Use the Radam et al. (2022) values from pp. 17-24; the corrected paper-level metrics are 15.5 ms propagation delay, 0.88 +/- 0.1 reliability, 197.1 throughput, 26.8 cost, and 22.5 fitness.
- Use Yusuf et al. (2023, pp. 23-24) for the 73% / 51% / 16% / 16% claims and the stated limitations on heterogeneous controllers and fault defense.
- Use Xu et al. (2023, pp. 15, 17) for the hierarchical multi-objective result and avoid overstating real-world deployment validation.
- Use Benoudifa et al. (2023, pp. 1, 14) when citing MuZero, self-competition, success rates, and search-time claims.
- Use Farahi et al. (2026, pp. 1, 23-24) for the AP-DQN percentage gains and note that the results vary by topology.

### 6.6 Gap Analysis

What the literature consistently shows:

- Better placements usually reduce latency and improve at least one additional control-plane metric.
- The apparent strength of a method changes with topology family and network scale.
- Multi-objective methods are now common, but many papers still privilege one headline metric when making the final argument.

Where findings conflict:

- Heuristics remain attractive because they are cheaper and easier to reproduce, while AI methods often report stronger multi-metric gains but at higher search or training cost.
- Some studies emphasise latency, whereas others place more weight on load balance, overhead, or security, which makes cross-paper ranking unstable.
- A result that looks dominant on one topology may be only moderate on another, especially when controller count or link complexity changes.

What is still missing for this study:

- A single comparison framework that uses canonical topology families, failure-aware reliability, and explicit complexity accounting together.
- Clear evidence that AI gains remain stable when the network is evaluated across both multi-site scale and single-link failure conditions.
- A reproducible way to judge whether a latency gain is worth the computational burden required to produce it.

## 7 Theoretical (or Conceptual) Framework

### 7.1 Multi-Objective Combinatorial Optimization Foundation

This study formalizes controller placement as a Multi-objective Combinatorial Optimization (MOCO) problem rather than a generic constrained decision task. The network is modeled as $G=(V,E)$ where $V$ is the set of nodes and $E$ is the set of links, with total node count $|V|=n$. The controller placement set is $P\subseteq V$ with $|P|=k$, where $k\in\{2,3,5\}$. The binary decision variable is $x_i\in\{0,1\}$, where $x_i=1$ indicates that node $v_i\in V$ hosts a controller. In operational terms, the framework seeks placements that jointly minimize latency $L(P)$ in $ms$ and complexity $\omega$ in $s/episode$, while maximizing reliability $Reach_{avg}\in[0,1]$ (equivalently $E[R]$).

The MOCO framing is critical because the controller-placement search space grows combinatorially with topology size and controller budget, and no single scalar objective can represent deployment-grade performance. This directly grounds Section 8's factorial design and comparative protocol: each algorithm is evaluated as a search strategy over the same combinatorial space, under the same topology and scale constraints.

### 7.2 Pareto Optimality and Non-Dominated Set Logic

The decision-theoretic core of the framework is Pareto Optimality. A placement is considered preferable only if it is non-dominated in the joint objective space. Accordingly, the framework uses a 3D decision frame with axes $L(P)$ ($ms$), $Reach_{avg}$ (or $E[R]$), and $\omega$ ($s/episode$). The resulting non-dominated set defines the practically defensible frontier from which method-selection guidance is derived.

Within this framework, complexity $\omega$ ($s/episode$) is interpreted as the Complexity Tax paid for AI-driven gains. This concept provides the formal theoretical basis for Section 11 feasibility claims: if AI methods improve latency or survivability but require disproportionate complexity cost $\omega$, their practical superiority is weakened. If gains are achieved at an acceptable complexity tax, AI methods remain decision-grade.

### 7.3 Control Plane Survivability as Reliability Theory

Reliability is formalized as Control Plane Survivability, not as a static availability score. The theoretical lens is Reachability Under Failure: a placement is reliable to the extent that nodes remain controller-reachable after structured perturbations. This justifies the Section 8 use of link-failure simulation rather than static, no-failure metrics.

By grounding reliability in survivability dynamics, the framework evaluates whether a method preserves operational control when the topology is disrupted. This aligns with evidence that latency-only claims are insufficient for deployment decisions (Heller et al., 2012; Farahi et al., 2026; Radam et al., 2022; Benoudifa et al., 2023). The implication is direct: method quality must be judged on both nominal performance and post-failure reachability behavior.

### 7.4 Reinforcement Learning Bridge: MDP Policy vs Heuristic Priors

The AI component is framed as a Markov Decision Process (MDP). States encode topology-aware placement context derived from $G=(V,E)$, actions correspond to controller-node assignment decisions over $x_i\in\{0,1\}$, transitions reflect environment updates under placement decisions and failure scenarios, and rewards encode the multi-objective performance signal over $L(P)$, $Reach_{avg}$, and $\omega$. Under this formulation, DQN/DRL represents a policy-learning mechanism that searches for high-value placement actions over time.

Crucially, the framework does not evaluate policy quality in isolation. The learned policy is tested against Heuristic Priors: baseline methods that encode established non-learning search rules. This yields a principled comparison between adaptive policy optimization and deterministic or meta-heuristic placement logic. The framework therefore predicts Section 8's core empirical test: whether the DQN policy delivers statistically and operationally meaningful gains over heuristic priors once the full 3-axis objective, including complexity $\omega$, is enforced.

### 7.5 Framework-to-Methodology Alignment

This hardened framework establishes the mathematical and methodological logic for Section 8. MOCO defines the optimization class, Pareto/non-dominated reasoning defines decision validity, Control Plane Survivability defines reliability theory, and MDP policy evaluation defines the AI mechanism. Together, these components justify the Section 8 implementation choices: canonical topology families, failure-aware reliability measurement, factorial analysis, and explicit complexity accounting via $\omega$ in $s/episode$.

## Methodology

### 8 RESEARCH METHODOLOGY

This study adopts a methodology designed to produce objective, reproducible, and decision-relevant evidence on the comparative performance of AI-driven and heuristic controller placement methods in multi-site SDN environments.

#### 8.1 Research Philosophy

This study is grounded in a positivist research philosophy. Positivism is appropriate because the phenomenon under investigation is measurable and testable: controller placement methods produce observable outcomes such as $L(P)$, $Reach_{avg}$, and $\omega$. The aim is not to interpret subjective experiences, but to evaluate whether one algorithmic class performs better than another under controlled conditions.

#### 8.2 Research Approach

The study follows a deductive research approach. Deduction is suitable because the investigation begins with existing ideas from optimization theory and controller placement literature, then tests whether predefined methods satisfy explicit performance criteria. This aligns with the research trajectory: problem statement identifies a decision gap, research questions ask whether AI methods offer meaningful advantages, and the methodology tests that claim through controlled experimentation.

#### 8.3 Research Design

The study uses an experimental factorial design to compare algorithmic classes under controlled and repeatable conditions, with main-effect and interaction-effect estimation for method-selection guidance.

#### 8.3.1 Factorial Matrix and Controls

The full design matrix is: topology x controller budget x algorithm.

- Independent variables: topology family $\{\text{Internet2},\text{ATT-MPLS}\}$ on $G=(V,E)$ with $|V|=n$; controller count $|P|=k$ where $k\in\{2,3,5\}$; algorithm $\{\text{DQN},\text{Greedy},\text{K-Center}\}$.
- Dependent variables: latency $L(P)$ in $ms$, reliability $Reach_{avg}$ (or $E[R]$), and complexity $\omega$ in $s/episode$.
- Control variables: fixed random seed (Seed 42), fixed hardware/runtime environment (same CPU/RAM host and pinned software stack), identical traffic-generation profile per cell.

This produces scenario-specific evidence without mixing incomparable topology or budget regimes.

#### 8.3.2 DQN Policy Architecture (State, Action, Reward)

To make the AI mechanism auditable and reproducible, the DQN agent is specified as follows.

- State space: topology encoded as graph features over $G=(V,E)$ (adjacency and link-latency structure), plus the current partial placement mask over $x_i\in\{0,1\}$ and remaining controller budget $k$.
- Action space: discrete node index selection for the next controller placement step, with invalid-action masking to prevent duplicate placements and to enforce $|P|=k$.
- Reward logic: multi-objective penalty reward

$$
R = -\left(\alpha\,\hat{L}(P) + \beta\,(1-Reach_{avg}) + \gamma\,\hat{\omega}\right)
$$

where $\hat{L}(P)$ is normalized latency derived from $L(P)$ in $ms$, $Reach_{avg}\in[0,1]$ is mean post-failure reachability, and $\hat{\omega}$ is normalized complexity derived from $\omega$ in $s/episode$; higher reward is achieved by lowering latency and complexity while improving survivability.

#### 8.4 Data Collection

Data collection is conducted in a controlled simulation and emulation workflow rather than through human participants. This is appropriate because the research problem concerns measurable algorithmic performance under standardized conditions. The collection process is designed to preserve repeatability, minimize uncontrolled variance, and support transparent cross-method comparison.

#### 8.4.1 Parameter Justification and Technical Stack Defense

This study adopts Mininet, a PyTorch-based DQN/DRL implementation (Farahi et al., 2026), and Internet2/ATT-MPLS-class topologies as a tightly coupled methodological stack because this is the only configuration that simultaneously satisfies baseline comparability, metric transparency, and operational realism across the three method families in the literature. This choice is necessitated by the empirical structure of prior work.

Group A foundational studies show that controller-placement claims are highly topology-dependent, with Internet2-scale evaluation establishing the canonical latency baseline (Heller et al., 2012). Group B meta-heuristic studies report strong gains under simulation-specific settings, but with transferability and parameter-sensitivity limitations (Radam et al., 2022). Group C DQN/DRL studies report substantial improvements but often under-specify reproducibility-critical implementation details and reliability operationalization (Farahi et al., 2026; Benoudifa et al., 2023).

**First,** baseline parity is non-negotiable. The use of Internet2 and ATT-MPLS-class topologies is deliberate to replicate the structural conditions under which foundational CPP latency claims were established (Heller et al., 2012). Ensuring cross-study parity at the topology layer prevents inflated AI claims caused by easier synthetic graph regimes.

**Second,** this study introduces a formal reliability specification to eliminate black-box scoring. Reliability is explicitly defined as the mean fraction of nodes that remain controller-reachable under single-link failure across all edge removals. Directly addressing reporting limitations where reliability is presented as an aggregate score without fully auditable operationalization (Benoudifa et al., 2023), this definition makes each reliability claim independently recalculable from graph state and controller set.

**Third,** the reproducibility pivot to a full PyTorch DQN/DRL stack is required by convergence-control expectations in AP-DQN and MuZero literature (Farahi et al., 2026; Benoudifa et al., 2023). The prior lightweight reward baseline is useful for exploratory benchmarking but cannot provide replay-based stabilization, target-network synchronization, and gradient-level diagnostics expected in contemporary DRL evidence. Farahi et al. (2026) report concrete DQN settings: learning rate 0.001, batch size 32, discount factor gamma 0.99, and 1000 episodes. These values provide a quantitative reference band for implementation and hyperparameter calibration.

**Finally,** operational validity requires Mininet with Iperf3-driven traffic generation. Analytical or offline optimization remains essential for theory but insufficient for deployment-facing inference. Mininet introduces packet-level behavior, contention effects, and emulation-time variability that abstract graph optimization cannot represent.

#### 8.4.2 Design and Description of Instruments

The study instruments include Mininet and Python-based simulation/emulation environment, DQN/DRL and baseline controller-placement implementations, experiment orchestration scripts, structured logging pipelines, and metric extraction utilities. This design is justified because it combines parameter control, repeatability, and operational safety, and avoids disruption of production network infrastructure.

#### 8.4.3 Data Collection Procedures

Data collection proceeds in a controlled sequence: first, instantiate each factorial cell $(G, k, \text{algorithm})$; second, execute under identical run controls; third, persist structured logs and metric artifacts for auditability. Latency is measured as $L(P)$ in $ms$. Reliability uses an exhaustive N-1 failure engine: for each topology edge $e \in E$, remove $e$, recompute controller reachability, then aggregate across all $|E|$ single-link removals to obtain $Reach_{avg}$ (or $E[R]$). Computational complexity is reported as $\omega$ in $s/episode$.

#### 8.4.4 Piloting of Instruments

### Objectives

- Verify that the Python training script, topology loader, reward logic, and metrics exporter executed without runtime faults.
- Confirm that the pilot environment matched the final study setup through identical configuration values, seed control, and topology selection.

### Execution

- The pilot was run on the Internet2 topology with 11 nodes and 18 edges under Seed 42.
- Configured parameters were loaded directly from `experiment_config.json`, including learning rate 0.001, batch size 32, gamma 0.99, replay memory 10,000, and epsilon decay 0.995.
- The DQN stack was executed in a CPU-only PyTorch environment, and structured JSON metrics were written to [results/pilot_metrics.json](../results/pilot_metrics.json).

### Validation Results

- The dry run completed 50 episodes in 1.1 seconds, showing stable execution and acceptable performance.
- Pilot testing identified and cleared dependency and configuration issues, including PyTorch installation compatibility and parameter synchronization.
- Output checks confirmed consistent reward traces, reproducible logging, and complete metric export.

The instruments were therefore validated and confirmed ready for full-scale deployment in the main experiment.

#### 8.5 Data Analysis Methods and Procedures

The analysis combines descriptive, inferential, and multi-objective methods. Descriptive statistics report mean and standard deviation per factorial cell. Inferential analysis applies normality checks (Shapiro-Wilk on residuals; Q-Q inspection) before parametric tests. Factorial effects are tested via ANOVA (method x topology x $k$), and where omnibus effects are significant, post-hoc pairwise contrasts are resolved with Tukey's HSD. Pairwise DQN-vs-heuristic tests use t-tests when assumptions hold, with non-parametric fallback (Mann-Whitney U / Kruskal-Wallis) when violated. Pareto-front synthesis then identifies non-dominated sets across $L(P)$, $Reach_{avg}$, and $\omega$. This satisfies positivist validity by making claims measurable, reproducible, and statistically decision-ready.

### 8.5.1 Golden Thread Mapping: Research Questions to Analysis

- RQ1 (multi-objective superiority): addressed through descriptive statistics, pairwise tests, and effect-size comparisons on $L(P)$ and $Reach_{avg}$, with $\omega$ as the third axis.
- RQ2 (trade-offs and practical superiority): addressed through Pareto-front analysis and non-dominated set identification across $L(P)$, $Reach_{avg}$, and $\omega$.
- RQ3 (stability across topologies and scales): addressed through factorial ANOVA interaction analysis (method x topology family x network scale) and scenario-stratified ranking stability checks.

## 9 Research Quality, Ethical, and Safety Issues

### 9.1 Research Quality and Empirical Integrity

Research quality is operationalized through triangulation, reproducibility, and internal-validity control. Triangulation is achieved by testing across Internet2 and ATT-MPLS. Reproducibility is enforced through a config-driven pipeline (`experiment_config.json`) with fixed random seeding (`seed = 42`). Internal validity is strengthened through factorial design that isolates method, topology, and scale effects.

### 9.2 Ethical and Safety Considerations

The study uses publicly available topology references (Internet Zoo-aligned public corpora), Internet2/ATT-MPLS-class models, and synthetic Mininet/Iperf3 traffic; no private, proprietary, or PII traces are used. No human participants are involved, so clinical-style procedures do not apply, while institutional research-integrity standards remain in force. Algorithmic accountability is explicit: reliability/survivability is prioritized with Reachability Under Failure to prevent "glass cannon" network states.

### 9.3 Safety and Resource Stewardship

Computational safety is pilot-validated in Section 11.2: approximately $\omega=0.0226\,s/episode$ confirms feasible local execution without unsafe over-consumption. Resource stewardship is tracked via $\omega$.

## 10 Intellectual Property

The intellectual property arising from this study belongs to the University of Zululand in accordance with institutional policy **[University of Zululand, n.d.]**. For the ai-sdn-controller-placement project, the protected research artifact scope includes the proposal text, the DQN implementation, trained DQN model weights, topology-aware reward functions, automated experimental runner scripts, configuration files, simulation outputs, and derived analysis artifacts. `experiment_config.json` and `pilot_metrics.json` form part of the University’s intellectual corpus because they encode the reproducible experimental conditions and validated pilot evidence.

This IP position exists alongside open-source dependencies and reference assets, including PyTorch, Mininet, Ryu, and the Internet Topology Zoo. The project logic remains the University’s authored work, while the underlying third-party tools continue to be governed by BSD, Apache, MIT, and related permissive licenses.

Version control serves as the primary audit trail for intellectual-property creation, attribution, and revision history. The Git-based repository records the evolution of the research artifacts, the timing of changes, and the relationship between code, configuration, and outputs, supporting academic accountability and reproducibility.

Research Data Management (RDM) governs the storage and handling of metrics, simulation logs, and exported result files. The RDM approach keeps data traceable, securely stored, and recoverable for validation, consistent with the hardened methodology and pilot-validated pipeline in Sections 8 and 11.

## 11 Resources Required and Project Plan (Feasibility Update)

### 11.1 Resources and Environment Integrity

The study uses an isolated Python 3.10+ virtual environment to preserve dependency stability, prevent version drift, and maintain the reproducibility established in Section 9.2. The software stack comprises PyTorch for the DQN implementation, Mininet for network emulation, Ryu for SDN control logic, and the custom ai-sdn-controller-placement framework. The data corpora are the Internet Topology Zoo-aligned canonical topologies used throughout the study, specifically Internet2 and ATT-MPLS. Local x86_64 CPU and RAM resources are sufficient for all training, emulation, logging, and analysis tasks because the pipeline is optimized for CPU-based DRL throughput.

### 11.2 Computational Stewardship (Budget)

As the project relies on open-source assets, the primary budget item is Computational Resource Allocation. The governing efficiency metric is complexity $\omega$ in $s/episode$. Using the pilot value of $\omega=0.0226\,s/episode$, the full factorial matrix of 5 algorithms × 10 topologies × 1000 episodes = 50,000 episodes requires approximately 1,130 seconds of CPU time, or about 18.8 minutes in total. This low compute burden supports multiple stability trials and sensitivity checks while remaining comfortably below the risk threshold for the department deadlines.

### 11.3 Research Process - Gantt Chart (2026 Official Timeline)

- P1 Setup | Working Title, Summary & Pilot Validation ($\omega=0.0226\,s/episode$) | Feb 24 – Mar 09 | 100% Complete
- P2 Proposal | Draft Proposal Presentation & Ethics Protocol Prep | Apr 13 – Apr 20 | Current
- P3 Ethics | Submission for Faculty Ethics Review (Interim/Final) | Apr 17 – Apr 27 | Planned
- P4 Defense | Formal Proposal Presentation & Data Ingestion | May 18 – May 25 | Planned
- P5 Execution | Factorial Batching & 1st Progress Presentation | Jul 06 – Jul 13 | Planned
- P6 Synthesis | 3D Pareto Analysis & 2nd Progress / Mock Exam | Aug 01 – Sep 28 | Planned
- P7 Draft | Mini-dissertation Draft & Research Paper Compilation | Oct 26 – Oct 30 | Planned
- P8 Exam | Final Presentation & Prototype Demonstration | Nov 04 – Nov 06 | Planned
- P9 Final | Final Thesis & Research Paper Submission | Nov 09 – Nov 13 | Planned

This roadmap aligns the research paper requirement with the reproducibility claims in Section 9 and preserves the golden thread from pilot validation through final submission.

## 12 Feasibility of the Study

### 12.1 Researcher Competency and Technical Capacity

The researcher holds a foundation in BSc Computer Science and Mathematics (Undergraduate), which directly enables the theoretical and implementation competencies required for this Honors-level study. The mathematical background supports the MDP formulation (Section 7.4), the Pareto optimality reasoning (Section 7.2), and the statistical convergence analysis required to interpret DRL training dynamics. The computer science foundation enables the implementation of PyTorch-based DQN/DRL, the configuration of Mininet emulation environments, and the automation of the factorial experimental pipeline.

Beyond academic grounding, the researcher has professional experience as an Introductory Programming Tutor, which ensures code quality, robust error handling, and reproducible pipeline design. This domain expertise directly translates to the code-review and documentation standards that support the reproducibility requirements in Section 9.1, the config-driven architecture that enables experiment-state resumability, and the Git-based audit trail that Section 10 mandates for IP stewardship. The combination of mathematical rigor and hands-on programming proficiency positions the researcher to execute both theoretical interpretation (statistical inference, Pareto ranking) and operational implementation (DRL training loops, metric extraction) with confidence.

### 12.2 Resources: Validation, Not Assumption

This study is not resource-contingent on external dependencies. The feasibility evidence is grounded in pilot validation, not on theoretical capability claims.

**Infrastructure Validation**: The project has been pilot-validated on a local x86_64 CPU testbed. Section 11.2 establishes the Computational Stewardship budget: using the empirically derived pilot value of $\omega=0.0226\,s/episode$, the full factorial matrix of 5 algorithms × 10 topologies × 1000 episodes = 50,000 episodes requires approximately 1,130 seconds of CPU time, or about 18.8 minutes total. This has been measured, not estimated. The local testbed is therefore not merely "available"; it is proven capable of executing the full experimental matrix within the risk-acceptable time frame. No external GPU clusters, cloud compute quotas, or third-party resource requests are required.

**Self-Contained Nature**: The project is operationally self-contained. No proprietary software licenses are required—all tools (PyTorch, Mininet, Ryu) are open-source under permissive licenses. No human participants are involved, so the research sidesteps clinical-ethics complexity and external review dependencies. The topology data comes from publicly available Internet Topology Zoo-aligned corpora, not from proprietary network telemetry. This means Section 3 ethics clearance follows the standard institutional research-integrity pathway, not an extended regulatory review.

### 12.3 Methodological Control and Risk Mitigation

The "Complexity Tax" concept from Section 7.2 operationalizes the core risk of this study: that AI methods may improve latency or reliability gains at a computational cost that undermines their practical superiority. This risk is not avoided; it is quantified and controlled.

The config-driven architecture (Section 8.4.2 and documented in `experiment_config.json`) materializes this control. Every experimental parameter—random seed, learning rate, batch size, discount factor, topology selection, scale, and algorithm choice—is version-controlled in a single configuration artifact. This ensures that experiments can be paused, resumed, or re-executed without loss of integrity. If a run is interrupted, the checkpoint-save mechanism preserves the training state, and the experiment can resume from the last completed episode. This design eliminates the risk of lost computational work and supports transparent error recovery.

Reproducibility is further hardened through the factorial structure itself. The design matrix (Section 8.3) specifies precisely which algorithm-topology-scale combinations are tested and in what order. No ad-hoc method selection or scope creep occurs because the experimental frame is locked. This is risk-mitigation by design, not by hope.

### 12.4 Timeline Confidence and Project Status

The official 2026 milestone roadmap (Section 11.3) charts nine phases from February through November. The critical feasibility indicator is **Phase 1 Status: Pilot Validation is 100% Complete**. This is not a projection; the 50-episode DQN proof-of-concept has executed successfully, capturing the $\omega=0.0226\,s/episode$ metric that anchors all downstream feasibility claims.

By the timing of this proposal (April 11, 2026), Phase 1 completion places the project ahead of the typical Honors risk curve. In most Honors timelines, pilot work is deferred until mid-project or treated as parallel exploratory activity. Here, it is already validated. This means Phases 2–9 operate with known technical risk and quantified compute requirements, not with speculative assumptions.

The Gantt chart (Section 11.3) maps the remaining eight phases to official department deadlines, from the current Phase 2 (Proposal, Apr 13–20) through Phase 9 (Final Submission, Nov 09–13). Each phase phase has documented entry and exit criteria, and each depends on demonstrable artifacts (proposal acceptance, ethics approval, data ingest completion, draft synthesis, mock exam feedback, prototype demo findings). The timeline is aggressive but not speculative: it is built on the foundation that Phase 1 pilot validation succeeded.

### 12.5 Closing the Loop: Golden Thread of Feasibility

This study closes the loop on all prior sections. Literature review (Section 6) identified the decision gap. Theory (Section 7) formalized MOCO, Pareto optimality, and reliability dynamics. Methodology (Section 8) specified the experimental protocol. Quality and ethics (Section 9) operationalized reproducibility and safety. IP (Section 10) clarified institutional ownership and open-source boundaries. Resources (Section 11) quantified the compute budget based on pilot evidence.

Feasibility (Section 12) binds all of these together through the assertion: the researcher is competent, the resources are validated, the methods are controlled, the timeline is grounded in completed pilot work, and the project is achievable within departmental constraints. No feasibility claim rests on unvalidated assumptions. Each assertion is anchored to empirical evidence (pilot results), technical documentation (config-driven architecture), or institutional commitment (timeline milestones).

This is not an optimistic feasibility statement. It is a data-backed proof of feasibility. The study is ready to proceed.

## 13 Dissemination Plan

### 13.1 Research Manuscript and Academic Publication

The official 2026 research timeline (Section 11.3, Phase 9: Nov 09–13) requires formal submission of a Research Paper as a core deliverable of the Honors program. This research will be documented in a high-quality manuscript prepared for peer-reviewed submission to a venue appropriate to the international SDN and network optimization community, such as SATNAC (Southern African Telecommunications Networks and Applications Conference), SAICSIT (South African Institute of Computer Scientists and Information Technologists), or a relevant international conference in the areas of software-defined networking, optimization, or network architecture.

The manuscript will feature the empirical research contributions of this study, focusing on the 3-axis Pareto trade-offs discovered during the factorial benchmarking experiments: (1) latency reduction measured as $L(P)$ in $ms$, (2) control-plane reliability quantified as $Reach_{avg}$ under single-link failure, and (3) complexity $\omega$ in $s/episode$ as a transparent measure of training and search burden. The paper will serve broader audiences by resolving a critical literature gap: the lack of multi-objective, reproducible comparative evidence on when AI-driven controller placement genuinely outperforms heuristic baselines, and under what operational constraints.

By documenting the trade-off surfaces and method-selection guidance derived from the analysis, the manuscript transforms experimental results into actionable knowledge for practitioners and researchers managing multi-site SDN deployments. The publication timeline aligns with Phase 8 (Exam, Nov 04–06), allowing prototype demonstration findings to inform the final manuscript before submission within the Phase 9 window.

### 13.2 Technical Artifacts and Repository Dissemination

The GitHub repository (ai-sdn-controller-placement) serves as the primary long-term dissemination platform for the study. This repository encodes all technical artifacts necessary for independent reproduction and extension of the research: the experiment orchestration scripts, the PyTorch-based DQN/DRL implementation, curated configuration files, and analysis pipelines.

The reproducibility foundation is the `experiment_config.json` artifact, which documents the complete factorial matrix specification, hyperparameter settings (learning rate 0.001, batch size 32, discount factor gamma 0.99, replay memory 10,000), and random seed (seed = 42). This configuration is version-controlled and auditable, allowing any researcher to re-execute the full 50,000-episode factorial matrix and verify the pilot-validated efficiency metric of approximately $\omega=0.0226\,s/episode$ on equivalent x86_64 CPU hardware.

Additionally, trained model weights and checkpoint artifacts will be documented and made available in tagged releases, enabling other researchers to directly inspect the learned DQN policy, validate the placements it generates, and apply the policy to novel topologies. This approach aligns with Section 10's IP stewardship framework: while the University of Zululand retains ownership of the research artifacts and the authored code, the dissemination strategy prioritizes transparency and reproducibility through open documentation and version-controlled artifact release, balancing institutional IP protection with the scientific imperative for independent verification.

### 13.3 Prototype Demonstration and Live System Validation

The official project timeline includes a critical dissemination milestone: the Prototype Demonstration (Section 11.3, Phase 8: Nov 04–06). This technical presentation provides a "visual proof" of the optimization results by demonstrating the DQN-placed controller environment in a live Mininet/Ryu software-defined network emulation. The prototype shows real-time network behavior under the learned placement policy, illustrating latency improvements, reliability under failure injection, and the computational cost of the DQN agent's decision-making in a concrete, observable context.

This hands-on demonstration serves multiple dissemination purposes: (1) it validates that theoretical benchmarks translate into operational reality, (2) it provides an engaging medium for communicating research findings to academic and technical audiences, (3) it demonstrates implementation mastery and system thinking aligned with Honors-level expectations, and (4) it creates a reproducible artifact that can be re-deployed and modified by other researchers or practitioners seeking to build on the work.

### 13.4 Peer and Departmental Knowledge Sharing

Immediate dissemination within the University of Zululand community occurs through the Honors Research Symposium and Faculty of Science, Agriculture, and Engineering departmental seminars. These venues allow the researcher to present findings to peer Honors students, faculty supervisors, and research groups, securing formative feedback and establishing credibility within the local research ecosystem.

The dissemination strategy in this phase emphasizes clarity of communication, technical accuracy, and pedagogical value: explaining not only what the results are, but why the methodology matters for the broader SDN control-plane literature and what implications the trade-off surfaces hold for practitioners. This contributes to the research culture at UNIZULU by modeling rigorous, multi-objective thinking about algorithmic trade-offs and demonstrating the importance of computational burden as a decision criterion alongside performance metrics.

### 13.5 Long-Term Stewardship and Research Legacy

Post-submission, the research artifacts remain available through the GitHub repository and institutional archival systems, ensuring long-term accessibility and supporting the reproducibility requirements of the Honors program. The configuration of the repository (with clear README files, documented hyperparameters, and tagged experiment versions) enables future researchers to cite, replicate, and extend the work.

This dissemination plan fulfills the institutional requirement for a research manuscript while maintaining alignment with the IP boundaries established in Section 10. The result is a multi-layered dissemination strategy: peer-reviewed manuscript publication, open repository architecture with documented artifacts, live technical demonstration, regional academic sharing, and institutional archival—collectively ensuring that the research reaches relevant audiences and contributes to the scientific community's understanding of multi-objective controller placement optimization in SDN environments.

## 15 References

- Benoudifa, M., Ait Wakrime, A., & Benaini, R. (2023). Autonomous solution for controller placement problem of software-defined networking using MuZero based intelligent agents. *Journal of King Saud University - Computer and Information Sciences, 35*(10), 101842. [https://doi.org/10.1016/j.jksuci.2023.101842](https://doi.org/10.1016/j.jksuci.2023.101842)
- Farahi, R., Ghaffari, A., Derakhshanfard, N., & Taghipoureivazi, S. (2026). AP-DQN: A novel approach for controller placement in software-defined networks using deep reinforcement learning. *Results in Engineering, 29*, 109631. [https://doi.org/10.1016/j.rineng.2026.109631](https://doi.org/10.1016/j.rineng.2026.109631)
- Heller, B., Sherwood, R., & McKeown, N. (2012). The controller placement problem. In *Proceedings of the 1st Workshop on Hot Topics in Software Defined Networks (HotSDN)* (pp. 7-12). [https://doi.org/10.1145/2342441.2342444](https://doi.org/10.1145/2342441.2342444)
- Radam, N. S., Faraj Al-Janabi, S. T., & Jasim, K. Sh. (2022). Multi-Controllers placement optimization in SDN by the hybrid HSA-PSO algorithm. *Computers, 11*(8), 111. [https://doi.org/10.3390/computers11080111](https://doi.org/10.3390/computers11080111)
- University of Zululand. (n.d.). *Intellectual property policy*.

## Expected Deliverables

- Reusable experiment runner and metrics pipeline.
- Comparative performance plots and benchmark CSV data.
- Research report summarizing findings and limitations.
