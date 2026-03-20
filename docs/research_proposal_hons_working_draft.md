# RESEARCH PROPOSAL (WORKING DRAFT)

## Provisional Title

Multi-Objective Evaluation of AI-Driven Controller Placement in Multi-Site Software Defined Networks: Balancing Performance, Reliability, and Computational Cost

## Degree and Administrative Details

- Degree: BSc Honours (Computer Science)
- Field of Study: Computer Science / Software Defined Networking
- Faculty: Faculty of Science, Agriculture and Engineering
- Student Name: THABANG NHLOKOMA BUTHELEZI
- Student Number: [Insert Student Number]
- Current Highest Qualification: BSc
- Supervisor: Dr Skhumbuzo Zwane
- Co-Supervisor: Prof Pragasen Mudali
- Year: 2026
- Estimated Date of Submission: November 2026

---

## 1. INTRODUCTION

Software Defined Networking (SDN) separates the control plane from the data plane, making controller placement a central design decision that directly affects network responsiveness, fault tolerance, and operational cost. This study focuses on multi-site SDN environments where topology structure and scale can change algorithm behavior and practical decision quality. The importance of this investigation is that method selection based on a single metric can produce misleading recommendations in real deployments.

This proposal is structured as follows. Section 2 provides the study background and identifies under-investigated areas in existing SDN controller placement research. Section 3 defines the research problem and research questions, followed by the study aim, objectives, and hypotheses in Section 4. Sections 5 to 7 present expected contribution, literature synthesis position, and the conceptual framework. Sections 8 and 9 detail methodology, quality controls, and ethical safeguards. Sections 10 to 14 present intellectual property, resources and project plan, feasibility, dissemination, and proposed chapter division.

---

## 2. BACKGROUND OF THE STUDY

Controller placement in SDN is commonly modeled as an optimization problem where switches are assigned to one or more controllers under latency and resilience constraints. Classical methods such as greedy k-center and clustering-based approaches remain attractive because they are simple and computationally efficient. More recent studies have introduced metaheuristic and learning-based methods, including genetic algorithms and reinforcement learning, to improve placement quality.

Current literature shows clear progress in optimization techniques, but three gaps remain important for this study:

1. Many evaluations prioritize one outcome (usually latency) without sufficient transparency on runtime and convergence burden.
2. Cross-topology and cross-scale behavior is often under-reported, which limits confidence in generalization.
3. AI methods are frequently presented as superior without a consistent baseline and reproducibility protocol.

This study advances knowledge by evaluating AI and non-AI methods in one reproducible benchmark pipeline with explicit multi-objective decision logic. It advances practice by producing scenario-conditioned recommendations on when AI methods are worth their additional computational cost and when baseline heuristics are sufficient.

---

## 3. PROBLEM STATEMENT AND RESEARCH QUESTIONS

### 3.1 Problem Statement

In multi-site SDN environments, controller placement decisions are often made using method claims that emphasize performance in isolation, especially latency, while giving limited attention to computational efficiency, reliability, and topology-dependent behavior. This creates a methodological risk: a placement method may appear optimal in one metric yet be impractical or unstable under realistic constraints. A reproducible, multi-objective comparison framework is therefore required to determine whether AI-driven placement methods are genuinely superior to baseline heuristics under controlled but varied SDN scenarios.

### 3.2 Research Question(s)

Primary research question:

In multi-site synthetic SDN topologies, does an AI-driven controller placement approach outperform baseline heuristic approaches on latency, under reliability and computational efficiency constraints?

Supporting research questions:

1. Performance question:
Do AI-driven placement methods achieve lower average controller-switch latency than baseline heuristics across controlled multi-site topology scenarios?

2. Efficiency question:
Do observed latency improvements remain defensible when runtime and convergence burden are jointly considered?

3. Scalability and reliability question:
Do method rankings remain stable across topology families and scale levels while maintaining acceptable reliability behavior under failure-oriented metrics?

---

## 4. RESEARCH AIM AND OBJECTIVES (AND HYPOTHESES)

### 4.1 Research Aim

To evaluate whether AI-driven controller placement methods provide defensible multi-objective advantages over baseline heuristics in multi-site SDN, using a reproducible factorial benchmarking framework.

### 4.2 Research Objectives and Hypotheses

Research objectives:

1. Build and validate a reproducible experimental pipeline for multi-site SDN controller placement benchmarking.
2. Compare baseline methods (random, greedy k-center, k-means) with AI methods (genetic search and bandit reinforcement learning).
3. Quantify trade-offs between latency, runtime cost, convergence behavior, and reliability-oriented metrics.
4. Determine scenario-conditioned method suitability by topology family and scale.

Hypotheses:

- H1 (Performance): AI-driven methods produce lower average latency than baseline heuristics in selected scenarios.
- H2 (Efficiency): Any AI latency gain must be interpreted alongside runtime and convergence overhead; superiority is not guaranteed under multi-objective evaluation.
- H3 (Scalability/Topology Sensitivity): Relative method ranking changes across topology families and node scales.

---

## 5. CONTRIBUTION OF THE STUDY

### 5.1 Contribution to Knowledge

1. Provides a unified evaluation approach that links performance, reliability, and computational cost in SDN controller placement.
2. Produces evidence on topology-conditioned algorithm behavior rather than one-scenario claims.
3. Strengthens methodological rigor through explicit reproducibility controls (seed traceability, repeated trials, warm-up handling, and run logs).

### 5.2 Contribution to Practice and Policy

1. Offers decision-grade guidance for selecting placement methods under specific operational constraints.
2. Reduces risk of over-claiming AI superiority in infrastructure planning.
3. Supports transparent reporting standards for SDN optimization studies.

### 5.3 Artefact Contribution

1. Reusable benchmark codebase and scripts.
2. Structured experimental outputs (raw, summary, and Pareto-ranked datasets).
3. Visual decision artifacts (Pareto plots and scenario comparison summaries).

---

## 6. LITERATURE REVIEW

The literature is organized around four themes relevant to the research questions.

### 6.1 Controller Placement Foundations

Early SDN controller placement studies formalized delay-oriented placement and highlighted distance-sensitive control performance. Classical optimization formulations and greedy approximations remain foundational for benchmark baselines.

### 6.2 Baseline Heuristic Families

Random placement is commonly used as a floor baseline. Greedy farthest-first strategies and clustering-based approaches provide strong practical baselines because they are fast and often competitive in quality.

### 6.3 AI and Metaheuristic Families

Genetic and reinforcement learning approaches seek adaptive or global improvements, especially in heterogeneous and high-dimensional scenario spaces. Reported gains are promising, but runtime and convergence transparency varies across studies.

### 6.4 Synthesis Gap and Positioning of This Study

Current evidence suggests improvements are possible but not uniformly transferable across topology classes and scales. This study addresses that gap by:

1. Using one controlled benchmark scaffold for all methods.
2. Reporting multi-metric outcomes instead of latency only.
3. Preserving reproducibility and traceability to support defensible conclusions.

---

## 7. THEORETICAL / CONCEPTUAL FRAMEWORK

This study uses a conceptual decision framework that links scenario characteristics, method class, and multi-objective outcomes.

### 7.1 Framework Components

Independent variables:

- Topology family (for example, Barabasi-Albert and Waxman)
- Node scale and controller budget
- Algorithm class (baseline vs AI)

Process variables:

- Optimization runtime
- Convergence behavior (where applicable)

Outcome variables:

- Average latency distance
- Worst-case distance
- Reliability-oriented metric(s)
- Efficiency and Pareto status

Decision layer:

- Scenario-conditioned recommendation based on quality-cost-reliability trade-off

### 7.2 Propositions

- P1: Method superiority is conditional, not universal.
- P2: Multi-objective ranking provides stronger practical guidance than single-metric ranking.
- P3: Reproducibility controls improve confidence in comparative conclusions.

---

## 8. RESEARCH METHODOLOGY

This study is quantitative and experiment-driven. Method decisions are justified to maximize fairness, reproducibility, and explanatory power.

### 8.1 Research Philosophy

Post-positivist with pragmatic orientation.

Rationale: The study tests explicit hypotheses using measurable outcomes, while also emphasizing practical decision relevance for network planning.

### 8.2 Research Approach

Deductive hypothesis-testing approach.

Rationale: Hypotheses H1-H3 are derived from documented gaps and tested using controlled experiments.

### 8.3 Research Design

Computational factorial experiment design.

Rationale: A factorial matrix allows systematic variation of topology family, scale, and controller budget while preserving comparability across algorithms.

### 8.4 Data Collection Context and Source

Primary data source:

- Synthetic topologies generated programmatically.
- Algorithm outputs generated through scripted runs in this repository.

Secondary evidence source:

- Peer-reviewed controller placement literature used for gap justification and interpretation.

### 8.5 Design and Description of Instruments

Core instruments include:

- Topology generators in the project topology module.
- Placement algorithms in baseline and AI modules.
- Experiment runners and analysis scripts.
- CSV and plot outputs as auditable evidence artefacts.

### 8.6 Data Collection Procedure(s)

1. Define scenario matrix using fixed configuration settings.
2. Generate synthetic graph instances per scenario.
3. Execute all placement algorithms under consistent conditions.
4. Run repeated trials with deterministic seed logic.
5. Record outputs to raw and summary files.
6. Preserve seed and trial provenance for reruns.

### 8.7 Piloting of Instruments

Pilot runs are performed to validate metric generation, script behavior, and output integrity before full matrix execution. Pilot outputs are interpreted as preliminary indicators and not treated as final evidence.

### 8.8 Data Analysis Method(s) and Procedure

1. Compute per-scenario descriptive summaries (means, variance-aware interpretation).
2. Compare method rankings on latency and runtime jointly.
3. Evaluate Pareto-optimal points for trade-off quality.
4. Map results to H1-H3 and identify where hypotheses are supported, partially supported, or rejected.
5. Use stability checks across seeds to assess reliability of ranking conclusions.

Core metric definitions include:

- Average latency proxy:
  D_avg(C) = (1 / |V|) * sum_{v in V} min_{c in C} d(v, c)

- Reliability under single-link failure:
  R_link(C) = (1 / |E|) * sum_{e in E} ( |Reach(V, C, G - e)| / |V| )

---

## 9. RESEARCH QUALITY: ETHICAL AND SAFETY ISSUES

### 9.1 Research Quality

Validity controls:

1. Construct validity: metrics map directly to the research questions.
2. Internal validity: common scenario definitions, deterministic seeds, repeated trials, and warm-up controls reduce bias.
3. External validity: multiple topology families and scales support broader interpretation boundaries.

Reliability controls:

1. Version-controlled code and scripts.
2. Repeatable configuration and logged seed provenance.
3. Raw and summary artefacts retained for audit and replication.

Trustworthiness and interpretation controls:

1. Report both strong and weak method outcomes.
2. Avoid one-metric superiority claims.
3. Explicitly state limitations and uncertainty.

### 9.2 Ethical and Safety Considerations

Current ethical scope:

- Core experiments are synthetic and involve no direct human participants.

Informed consent, debriefing, and withdrawal:

- Not applicable for current synthetic-only experiment stage.
- If human participants or sensitive operational datasets are introduced later, formal ethics approval and participant consent procedures will be applied before any data handling.

Protection of participants and data subjects:

- No personal participant data is collected in the present phase.
- Future expansion to real traffic data will require de-identification, access control, and formal approval.

Confidentiality and anonymity:

- Repository outputs are aggregated and non-identifying.

Data storage and security:

1. Project data stored in controlled local and repository structures.
2. Sensitive extensions (if any) to be encrypted and access-restricted.
3. No identifiable raw network traces to be publicly committed.

Safety:

- No physical laboratory hazard is anticipated in the current computational study design.

---

## 10. INTELLECTUAL PROPERTY

1. Existing algorithms and concepts used in this study are acknowledged through formal citations.
2. Novel contribution lies in study design integration, controlled benchmarking, and multi-objective interpretation.
3. Code artefacts in the repository are governed by the project license and institutional policy.
4. Any publication output will include full attribution and co-authorship alignment with supervision policy.

---

## 11. RESOURCES REQUIRED AND PROJECT PLAN

### 11.1 Resources Required

Human resources:

- Candidate researcher
- Supervisor and co-supervisor guidance

Technical resources:

- Personal workstation/laptop
- Python environment and required scientific libraries
- Version control platform and storage

Data resources:

- Synthetic graph generation and derived experiment outputs

### 11.2 Budget

| Item | Estimated Cost (ZAR) | Notes |
| --- | ---: | --- |
| Existing workstation/laptop | 0 | Already available |
| Internet and communication | 800 | Research-related usage estimate |
| Electricity and local compute overhead | 1200 | Approximate period estimate |
| Printing/binding (if required) | 1000 | Draft and final stages |
| Conference or publication support (optional) | 2000 | Contingency |
| Total (estimated) | 5000 | Subject to final faculty guidance |

### 11.3 Research Process - Gantt Chart (2026)

| No. | Milestone | Mar | Apr | May | Jul | Sep | Oct | Nov |
| ---: | --- | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
| 1 | Proposal refinement and draft writing | X | X |  |  |  |  |  |
| 2 | Draft proposal presentation |  | X |  |  |  |  |  |
| 3 | Ethics package to supervisors |  | X |  |  |  |  |  |
| 4 | Signed faculty ethics submission |  | X |  |  |  |  |  |
| 5 | Formal proposal presentation |  |  | X |  |  |  |  |
| 6 | Extended experiments and analysis | X | X | X | X |  |  |  |
| 7 | Progress presentation |  |  |  | X |  |  |  |
| 8 | Mock exam / second progress checkpoint |  |  |  |  | X |  |  |
| 9 | Draft dissertation submission |  |  |  |  |  | X |  |
| 10 | Final presentation and corrected submission |  |  |  |  |  |  | X |

---

## 12. FEASIBILITY OF THE STUDY

The study is feasible within Honours constraints for four reasons:

1. Methodological feasibility: core experimental pipeline and baseline modules already exist and are operational.
2. Technical feasibility: required software stack and computational environment are available.
3. Time feasibility: project milestones are aligned with the 2026 programme schedule.
4. Risk feasibility: major risks (over-claiming, runtime pressure, ethics delays) are identified with mitigations.

Key risks and mitigations:

- Risk: AI runs become computationally expensive.
  Mitigation: staged pilot-first execution, reproducible batching, and explicit efficiency reporting.

- Risk: conclusions become single-metric biased.
  Mitigation: enforced Pareto and multi-metric interpretation protocol.

- Risk: ethics delays for real-data extension.
  Mitigation: synthetic-only boundary until formal approval.

---

## 13. DISSEMINATION PLAN

Planned dissemination channels:

1. Departmental proposal and progress presentations.
2. Final Honours dissertation and oral defense/demo.
3. A conference-style or journal-style manuscript derived from final results.
4. Repository-based release of reproducible non-sensitive artefacts (code, scripts, aggregate outputs, and figures).

Benefit and reciprocity:

- University benefit: reusable benchmark scaffold and methodological template.
- Community/partner benefit: evidence-based guidance on method choice under resource constraints.

---

## 14. PROPOSED CHAPTER DIVISION

1. Chapter 1: Introduction and Problem Context
2. Chapter 2: Literature Review and Conceptual Framework
3. Chapter 3: Research Methodology
4. Chapter 4: Experimental Results and Analysis
5. Chapter 5: Discussion, Implications, and Limitations
6. Chapter 6: Conclusion and Future Work

---

## 15. REFERENCES (INITIAL APA-STYLE LIST)

Barabasi, A.-L., & Albert, R. (1999). Emergence of scaling in random networks. Science, 286(5439), 509-512.

Gonzalez, T. F. (1985). Clustering to minimize the maximum intercluster distance. Theoretical Computer Science, 38, 293-306.

Heller, B., Sherwood, R., & McKeown, N. (2012). The controller placement problem. Proceedings of the First Workshop on Hot Topics in Software Defined Networks, 7-12.

Holland, J. H. (1975). Adaptation in Natural and Artificial Systems. University of Michigan Press.

Kreutz, D., Ramos, F. M. V., Verissimo, P. E., Rothenberg, C. E., Azodolmolky, S., & Uhlig, S. (2015). Software-defined networking: A comprehensive survey. Proceedings of the IEEE, 103(1), 14-76.

MacQueen, J. (1967). Some methods for classification and analysis of multivariate observations. Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability, 1, 281-297.

Sutton, R. S., & Barto, A. G. (2018). Reinforcement Learning: An Introduction (2nd ed.). MIT Press.

Waxman, B. M. (1988). Routing of multipoint connections. IEEE Journal on Selected Areas in Communications, 6(9), 1617-1622.

---

## 16. CANDIDATE'S DECLARATION

I, THABANG NHLOKOMA BUTHELEZI, declare that this proposal is my own work and that all sources used have been acknowledged through appropriate citation.

Signature: ____________________

Date: Monday, 13 April 2026

---

## 17. SUPERVISOR(S) DECLARATION

Supervisor Name: Dr Skhumbuzo Zwane

Signature: ____________________

Date: Monday, 20 April 2026

Co-Supervisor Name: Prof Pragasen Mudali

Signature: ____________________

Date: Monday, 20 April 2026

---

## 18. ANNEXURE A: PARTICIPANT INFORMED CONSENT DECLARATION

Current status:

- Not applicable for the synthetic-only phase of this study.

Contingency statement:

- If the study is extended to include human participants or identifiable operational data, a full informed consent process and ethics-approved consent documentation will be attached before data collection begins.
