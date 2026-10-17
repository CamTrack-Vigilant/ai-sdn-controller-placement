# Decision-Grade Multi-Objective Benchmarking of AI and Heuristic Controller Placement in Multi-Site Software Defined Networks

**By**  
**Thabang Nhlokoma Buthelezi**  
**(Student Number: 230011908)**

---

A mini-dissertation submitted in partial fulfillment of the requirements for the degree of  
**Bachelor of Science Honours in Computer Science**  

in the  
**Department of Computer Science**  
**Faculty of Science, Agriculture and Engineering**  
**University of Zululand**  

**Supervisor:** Prof. Mudali  

**Year:** 2026  

---

## DECLARATION

I, **Thabang Nhlokoma Buthelezi** (Student Number: **230011908**), hereby declare that this mini-dissertation entitled:

> *"Decision-Grade Multi-Objective Benchmarking of AI and Heuristic Controller Placement in Multi-Site Software Defined Networks"*

is my own original work, conducted under the supervision of **Prof. Mudali** in the Department of Computer Science, Faculty of Science, Agriculture and Engineering at the University of Zululand. 

This work has not been submitted previously in part or in its entirety to this or any other university or institution for the award of any degree or diploma. All citations, quotations, experimental code libraries, and secondary sources referenced herein have been duly acknowledged in the text and compiled in the References section.

\
**Signature:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
**Thabang Nhlokoma Buthelezi**  
**Date:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  

---

## DEDICATION

This dissertation is dedicated to:

My beloved family, whose unconditional love, patience, sacrifices, and prayers have been my foundation throughout my academic journey;

To the aspiring African computer scientists, network engineers, and researchers striving to advance technology, open systems, and scientific inquiry across our continent;

And above all, to God Almighty, the source of all wisdom, understanding, perseverance, and strength.

---

## ACKNOWLEDGEMENTS

I wish to express my deepest and most sincere gratitude to all individuals and institutions who contributed to the realization and completion of this research project:

First and foremost, I express my profound gratitude to my academic supervisor, **Prof. Mudali**, for his invaluable guidance, intellectual rigor, unwavering support, and critical feedback throughout the conceptualization, execution, and writing of this dissertation. His insistence on methodological precision, reproducible benchmarking, and decision-grade scientific framing fundamentally elevated the quality of this work.

I extend my appreciation to the academic and technical staff of the **Department of Computer Science**, as well as the **Faculty of Science, Agriculture and Engineering at the University of Zululand**, for providing the academic foundation, computational facilities, and supportive learning environment that enabled this research.

I am deeply thankful to my family for their unending encouragement, moral support, and belief in my academic capabilities during long hours of research, coding, and writing.

Finally, I acknowledge the global open-source networking and machine learning research communities—specifically the developers of Mininet, Open vSwitch, NetworkX, and PyTorch—whose open scientific tools made the reproducible experimental apparatus in this study possible.

---

## TABLE OF CONTENTS

- **DECLARATION**
- **DEDICATION**
- **ACKNOWLEDGEMENT**
- **LIST OF FIGURES**
- **LIST OF TABLES**
- **LIST OF ABBREVIATIONS**
- **ABSTRACT**
- **CHAPTER ONE: 1.0 INTRODUCTION**
  - 1.1 Overview or Preamble
  - 1.2 Background of Study
  - 1.3 Problem Statement
  - 1.4 Research Goal and Objectives
  - 1.5 Significance of Study
  - 1.6 Organization of the Dissertation
- **CHAPTER TWO: 2.0 LITERATURE REVIEW**
  - 2.1 Theoretical Foundations of Software Defined Networking (SDN)
  - 2.2 Formalization of the Controller Placement Problem (CPP)
  - 2.3 Classical Heuristics & Spatial Clustering in Facility Location
  - 2.4 Evolutionary Computation & Metaheuristics in SDN
  - 2.5 Machine Learning & Deep Reinforcement Learning for Adaptive Placement
  - 2.6 Multi-Objective Trade-Offs and Control-Plane Survivability
  - 2.7 Critical Synthesis & The Computational Complexity Tax Gap
- **CHAPTER THREE: 3.0 METHODOLOGY / DESIGN AND IMPLEMENTATION**
  - 3.1 Research Design & Deductive Factorial Framework
  - 3.2 Data Collection & Network Topology Corpus
  - 3.3 System Design & Algorithmic Formulations
  - 3.4 Implementation Architecture & Emulation Harness
  - 3.5 Data Analysis & Evaluation Metrics
  - 3.6 Experimental Setup, Verification Controls & Gate Testing
- **CHAPTER FOUR: 4.0 RESULTS AND DISCUSSION**
  - 4.1 Empirical Results Presentation
    - 4.1.1 Reinforcement Learning Convergence & Multi-Seed Stability Audit
    - 4.1.2 Factorial Latency-Cost Benchmark Matrix
    - 4.1.3 Three-Dimensional Pareto Frontier Synthesis
    - 4.1.4 Mininet Live OpenFlow Emulation & Control-Plane RTT Measurements
    - 4.1.5 Phase 4 Gate Test Validation
  - 4.2 In-Depth Discussion & Decision Framework
    - 4.2.1 Deconstructing the "Complexity Tax" of Artificial Intelligence
    - 4.2.2 Impact of Topological Characteristics: Scale-Free Skew vs. Spatial Clustering
    - 4.2.3 Control-Plane Robustness Under Single-Link Failure Stress
    - 4.2.4 Scenario-Conditioned Method Selection Guidance
  - 4.3 Limitations of Study & Threats to Validity
- **CHAPTER FIVE: 5.0 CONCLUSION**
  - 5.1 Summary of Main Findings
  - 5.2 Contributions to Knowledge
  - 5.3 Practical Recommendations for Network Engineers
  - 5.4 Future Research Directions
- **REFERENCES**
- **APPENDICES**
  - Appendix A: Detailed Experimental Configurations & Hyperparameters
  - Appendix B: Extended Latency, Reliability, and Complexity Data Tables
  - Appendix C: Mininet Emulation Test Harness Code

---

## LIST OF FIGURES

- **Figure 1.1:** Simplified Architectural Diagram of Software Defined Networking (Decoupled Planes).
- **Figure 3.1:** End-to-End Comparative Research Methodology Workflow.
- **Figure 3.2:** Reference Canonical Topologies: Internet2 (11 nodes) and ATT-MPLS (21 nodes).
- **Figure 3.3:** Deep Q-Network (DQN) Neural Architecture for Controller Placement.
- **Figure 3.4:** Mininet OpenFlow Live Control-Plane Emulation Architecture.
- **Figure 4.1:** Multi-Seed Policy Reward Convergence Curves Across 1,000 Episodes (Internet2 vs. ATT-MPLS).
- **Figure 4.2:** Rolling Action Entropy and Policy Variance During Deep Q-Network Training.
- **Figure 4.3:** Pareto Latency-Cost Trade-Off Curves for Barabási-Albert Topologies ($N \in \{20, 50\}$, $k \in \{2, 3, 5\}$).
- **Figure 4.4:** Pareto Latency-Cost Trade-Off Curves for Waxman Topologies ($N \in \{20, 50\}$, $k \in \{2, 3, 5\}$).
- **Figure 4.5:** 3D Pareto Non-Dominated Surface (Propagation Latency vs. Reliability $Reach_{avg}$ vs. Complexity Tax $\omega$).
- **Figure 4.6:** Emulated Switch-to-Controller RTT Distributions in Mininet across Placement Strategies.
- **Figure 4.7:** Phase 4 Mininet Gate Test Execution Timing Breakdown (Online Loop vs. OS Teardown Tax).
- **Figure 4.8:** The Practitioner's Scenario-Conditioned Decision Matrix for Controller Placement.

---

## LIST OF TABLES

- **Table 2.1:** State-of-the-Art Literature Synthesis on SDN Controller Placement (2012–2026).
- **Table 3.1:** Summary of Canonical and Synthetic Network Topology Parameters.
- **Table 3.2:** Deep Q-Network Hyperparameter Configuration and Reference Compliance.
- **Table 3.3:** Full Factorial Benchmark Design Matrix ($2 \times 2 \times 3 \times 5$).
- **Table 4.1:** Multi-Seed Stability Audit Results for Deep Q-Network Across 10 Independent Seeds.
- **Table 4.2:** Summary of Factorial Performance Metrics for Barabási-Albert Topologies.
- **Table 4.3:** Summary of Factorial Performance Metrics for Waxman Spatial Topologies.
- **Table 4.4:** Top Non-Dominated Solutions on the 3D Multi-Objective Pareto Frontier.
- **Table 4.5:** Mininet Emulation Control-Plane RTT Measurements on Canonical Internet2.
- **Table 4.6:** Two-Way ANOVA Statistical Contrasts for Propagation Latency and Runtime Overhead.
- **Table 4.7:** Scenario-Conditioned Algorithm Selection Decision Rules.
- **Table B.1:** Complete Factorial Latency-Cost Evaluation Matrix across All 60 Cell Configurations.

---

## LIST OF ABBREVIATIONS

- **AI:** Artificial Intelligence
- **ANOVA:** Analysis of Variance
- **API:** Application Programming Interface
- **BA:** Barabási-Albert (Scale-Free Network Model)
- **CPP:** Controller Placement Problem
- **CPU:** Central Processing Unit
- **DQN:** Deep Q-Network
- **DRL:** Deep Reinforcement Learning
- **GA:** Genetic Algorithm
- **GUI:** Graphical User Interface
- **HSD:** Honest Significant Difference (Tukey's test)
- **IaaS:** Infrastructure as a Service
- **IEEE:** Institute of Electrical and Electronics Engineers
- **IP:** Internet Protocol
- **JSON:** JavaScript Object Notation
- **MDP:** Markov Decision Process
- **ML:** Machine Learning
- **MLP:** Multi-Layer Perceptron
- **MOCO:** Multi-Objective Combinatorial Optimization
- **MPLS:** Multi-Protocol Label Switching
- **NFV:** Network Functions Virtualization
- **NOS:** Network Operating System
- **NP:** Non-Deterministic Polynomial Time
- **OVS:** Open vSwitch
- **OF:** OpenFlow
- **QoS:** Quality of Service
- **RL:** Reinforcement Learning
- **RTT:** Round-Trip Time
- **SATNAC:** Southern Africa Telecommunication Networks and Applications Conference
- **SDN:** Software Defined Networking
- **TCP:** Transmission Control Protocol
- **UDP:** User Datagram Protocol
- **VM:** Virtual Machine
- **WAN:** Wide Area Network
- **WX:** Waxman (Spatial Network Model)

---

## ABSTRACT

The Controller Placement Problem (CPP) represents a fundamental structural bottleneck in Software Defined Networking (SDN), directly governing propagation latency, control-plane survivability under topological failures, and operational compute overhead. In recent networking literature, Artificial Intelligence (AI) paradigms—specifically Deep Reinforcement Learning (DRL) and Deep Q-Networks (DQN)—have been widely advocated as superior alternatives to classical heuristic placement methods. However, existing comparative studies predominantly evaluate algorithms using isolated, single-metric objectives (primarily switch-to-controller latency), while omitting the computational complexity, convergence overheads, energy demands, and topology-dependent sensitivities inherent in AI training. This creates an infrastructure "decision gap": network operators lack reproducible, multi-objective evidence demonstrating when the deployment of AI algorithms is empirically justified over lightweight classical heuristics.

This mini-dissertation presents a decision-grade, multi-objective benchmarking study evaluating five distinct controller placement paradigms: Random Baseline, Greedy $K$-Center, $K$-Means Clustering, Genetic Algorithms (GA), and PyTorch-based Deep $Q$-Networks (DQN). The experimental investigation is conducted across canonical wide area networks (Internet2 with 11 nodes, and ATT-MPLS with 21 nodes) and parameterized synthetic network families (Barabási-Albert scale-free and Waxman spatial topologies up to $N=50$ nodes) across varying controller budgets ($k \in \{2, 3, 5\}$). A multi-seed stability audit across 10 random seeds confirms that the implemented DQN model achieves robust, non-divergent convergence within 20 episodes, stabilizing at a mean reward of 14.19 on Internet2 and 14.85 on ATT-MPLS with high action entropy ($\approx 0.97$).

However, full factorial benchmarking across 60 distinct experimental cells reveals that classical heuristics and clustering achieve equivalent or superior propagation latencies with compute times several orders of magnitude lower. Specifically, $K$-Means clustering and Greedy $K$-Center execute in sub-millisecond to 5-millisecond runtimes while providing $100\%$ control-plane reachability ($Reach_{avg} = 1.0$) under single-link failure ($N-1$) stress. While Genetic Algorithms consistently identify the absolute lowest latency configurations on large graphs, they require tens of milliseconds per optimization run. The DQN incurs a substantial "Complexity Tax" ($\omega \approx 11\text{--}24\text{ ms}$ per episode; $150\text{--}1086\text{ ms}$ total execution per run), representing a $100\times$ to $10,000\times$ computational overhead relative to Greedy $K$-Center, for a latency reduction of less than $4\%$ compared to $K$-Means. Hardware-emulated OpenFlow validation in Mininet confirms that real-world control-plane RTT is bounded by kernel switching dynamics, where $K$-Means achieves an average RTT of $2.852\text{ ms}$ compared to $2.934\text{ ms}$ for Greedy $K$-Center.

Consequently, this research synthesizes a three-dimensional Pareto frontier (latency, reliability, complexity) and establishes a scenario-conditioned decision framework. For static wide-area topologies up to $N=50$, classical heuristic clustering provides optimal operational efficiency and green networking sustainability. DRL deployment is empirically justified only in high-churn, dynamically degrading topologies where real-time adaptability outweighs the initial computational training investment.

**Keywords:** Software Defined Networking, Controller Placement Problem, Deep Reinforcement Learning, Multi-Objective Optimization, Pareto Efficiency, Complexity Tax, Mininet OpenFlow Emulation.
