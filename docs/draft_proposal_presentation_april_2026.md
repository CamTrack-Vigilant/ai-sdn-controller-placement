# Draft Proposal Presentation Outline (April 2026)

## Presentation Meta

- Candidate: Honours Research Student
- Project: AI-Driven Controller Placement Optimization in Multi-Site Software Defined Networks
- Draft proposal slots: 13 April 2026 or 20 April 2026
- Ethics package to supervisors: 17 April 2026
- Target duration: 12 to 15 minutes
- Suggested slide count: 12 slides

## Slide 1: Title and Positioning (1 min)

- Working title:
  Multi-Objective Evaluation of AI-Driven Controller Placement in Multi-Site Software Defined Networks: Balancing Performance, Resilience, and Computational Cost
- One-line purpose:
  Determine when AI placement methods are genuinely better than baseline heuristics under controlled, reproducible SDN scenarios.
- Supervisor or unit context.

Speaker cue:
Move from introducing the topic to stating that this is a scientific comparison study, not only a software build.

## Slide 2: Problem Context and Motivation (1 min)

- SDN controller placement affects latency, resilience, and operating cost.
- Many studies optimize one metric at a time.
- Real infrastructure decisions require trade-off thinking across multiple objectives.

Speaker cue:
State that optimizing only latency can produce fragile or expensive designs.

## Slide 3: Research Gap (1 min)

- Gap 1: Isolated-metric optimization is common.
- Gap 2: Limited evidence on topology-conditioned behavior (different graph structures).
- Gap 3: AI methods are often presented as superior without compute-cost transparency.

Speaker cue:
Emphasize that this project tests the hype versus evidence under a common benchmark setup.

## Slide 4: Research Question and Hypotheses (1 min)

- Primary question:
  In multi-site synthetic SDN topologies, do AI-driven controller placement methods outperform baseline heuristics on latency while remaining computationally efficient and reliable?
- H1: AI methods improve latency relative to baselines in selected scenarios.
- H2: Performance gains must be interpreted jointly with runtime cost and convergence burden.
- H3: Method ranking changes by topology family and scale.

Speaker cue:
Keep this slide concise and transition directly into measurable methodology.

## Slide 5: Objectives and Contributions (1 min)

- Build a reproducible benchmark pipeline.
- Compare 5 methods: random, greedy k-center, k-means, genetic, bandit RL.
- Produce an efficiency frontier combining quality and compute cost.
- Identify where AI is helpful versus where heuristics are sufficient.

Speaker cue:
Frame contributions as practical decision support for infrastructure planning.

## Slide 6: Methodology Design (1.5 min)

- Topologies: Barabasi-Albert and Waxman.
- Node scales and controller budgets are factorially varied.
- Reproducibility controls: fixed seeds, repeated trials, scripted execution.
- Output artifacts: raw CSV, summary CSV, best-per-scenario CSV, Pareto plots.

Suggested visual:
Method flow diagram: topology generation -> algorithm execution -> metric computation -> Pareto analysis.

## Slide 7: Metrics and Evaluation Logic (1.5 min)

- Core metrics:
  - average latency (controller distance proxy)
  - runtime cost (ms)
  - convergence metadata for AI methods
  - reliability-oriented metrics in broader project pipeline
- Decision logic:
  - not best latency only
  - use efficiency ranking and Pareto-optimality

Speaker cue:
Explain that ethical design requires fair, multi-dimensional comparison.

## Slide 8: Pilot Evidence from Current Runs (2 min)

Data source:
results/experiment_data/factorial_latency_cost_summary_20260314_050837.csv

Key pilot observations:

- Barabasi-Albert (n=20, k=3):
  - genetic has best latency (4.923) with high runtime (~41.116 ms)
  - greedy k-center is close on latency (5.299) with very low runtime (~0.141 ms)
  - bandit RL has higher runtime (~588.377 ms) with weaker efficiency rank
- Waxman (n=20, k=3):
  - genetic again has best latency (3.393)
  - k-means is second on latency (4.066) with lower runtime than genetic in this scenario
  - bandit RL remains runtime-heavy (~235.993 ms)

Speaker cue:
Present these as pilot indicators, not final conclusions.

## Slide 9: Interpretation and Risk of Over-Claiming (1 min)

- AI can lead on latency in pilot runs.
- Heuristics may still dominate on latency-cost efficiency in some conditions.
- Therefore, method choice should be scenario-conditioned, not ideology-driven.

Speaker cue:
Use language such as "evidence suggests" and "subject to full matrix confirmation".

## Slide 10: Ethics, Integrity, and Compliance (1 min)

- Ethical mandate: poor design is unethical.
- Internal controls:
  - reproducibility protocol
  - citation integrity and plagiarism prevention
  - data protection boundaries for non-synthetic data
- Date gates:
  - interim ethics package: 17 April 2026
  - signed faculty submission: 27 April 2026

Speaker cue:
State clearly that no real or semi-real traffic data will be used before formal ethics approval.

## Slide 11: Timeline to Proposal and Progress Milestones (1 min)

- 13/20 April: draft proposal presentation.
- 17 April: ethics package to supervisors.
- 27 April: signed ethics submission.
- 18/25 May: proposal presentation.
- 06/13 July: progress presentation.
- 28 September: second progress or mock exam.
- 26 to 30 October: draft submission.
- 04 to 06 November: final presentation/prototype demo.
- 09 to 13 November: final corrected submission.

Speaker cue:
Demonstrate that technical work and governance milestones are synchronized.

## Slide 12: Ask from Panel and Q&A (1 min)

- Feedback needed:
  - appropriateness of current metrics and hypotheses
  - expected minimum evidence for proposal acceptance
  - any additional ethics constraints before data expansion
- End with concise close:
  This project aims to produce decision-grade evidence on when AI placement methods are worth their computational cost.

## Appendix A: Figure and Table Checklist

- Pareto plots from:
  - results/graphs/latency_cost_pareto_20260314_050837/
- Summary table excerpt from:
  - results/experiment_data/factorial_latency_cost_summary_20260314_050837.csv
- Ethics and integrity framing from:
  - ETHICS.md

## Appendix B: Dry-Run Checklist (Before 13 or 20 April)

- Confirm slide deck fits 12 to 15 minutes.
- Validate all numbers shown in slides against CSV values.
- Ensure every claim references at least one metric or artifact.
- Prepare one backup slide with methodology detail.
- Prepare one backup slide with limitations and next experiments.
