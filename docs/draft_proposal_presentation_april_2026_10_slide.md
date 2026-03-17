# Draft Proposal Presentation (10-Slide Version)

## Delivery Plan

- Target duration: 10 to 12 minutes
- Presentation slot: 13 April 2026 or 20 April 2026
- Core objective: Present a defensible, ethics-aligned proposal with pilot evidence

## Slide 1: Title and Purpose (0:45)

- Working title:
  Multi-Objective Evaluation of AI-Driven Controller Placement in Multi-Site Software Defined Networks: Balancing Performance, Resilience, and Computational Cost
- Purpose statement:
  Evaluate when AI placement methods are truly beneficial relative to classical baselines under controlled conditions.

## Slide 2: Problem and Motivation (1:00)

- Controller placement decisions influence latency, resilience, and operational cost.
- Single-metric optimization creates weak real-world guidance.
- Need: a fair multi-objective comparison framework.

## Slide 3: Research Gap and Question (1:00)

- Gap: many studies report improvements without exposing compute-cost trade-offs.
- Gap: limited topology-conditioned evidence.
- Primary question:
  In multi-site SDN scenarios, do AI-driven controller placement methods outperform baseline methods while remaining efficient and reliable?

## Slide 4: Hypotheses and Contributions (1:00)

- H1: AI methods can improve latency relative to baselines in selected scenarios.
- H2: latency gains must be evaluated together with runtime and convergence effort.
- H3: topology family and scale affect algorithm ranking.
- Contributions: reproducible benchmark, efficiency frontier, topology-sensitive evidence.

## Slide 5: Methodology Design (1:15)

- Topology models: Barabasi-Albert and Waxman.
- Algorithms: random, greedy k-center, k-means, genetic, bandit RL.
- Experimental structure: factorial matrix over topology, node count, and controller budget.
- Reproducibility controls: fixed seeds, repeated trials, scripted execution.

## Slide 6: Metrics and Decision Logic (1:00)

- Metrics:
  - average latency proxy (controller distance)
  - runtime cost (ms)
  - convergence iteration metadata (AI methods)
- Decision logic:
  - Pareto-optimality for latency versus cost
  - efficiency ranking per scenario

## Slide 7: Pilot Results Snapshot (1:45)

Data source:
results/experiment_data/factorial_latency_cost_summary_20260314_050837.csv

- Barabasi-Albert, n=20, k=3:
  - genetic: lowest latency (4.923), moderate runtime (~41.116 ms)
  - greedy: near-competitive latency (5.299), very low runtime (~0.141 ms)
- Waxman, n=20, k=3:
  - genetic: best latency (3.393)
  - k-means: second latency (4.066), lower runtime than genetic in this pilot
- bandit RL is runtime-intensive in both pilot scenarios.

## Slide 8: Ethics and Integrity Controls (1:00)

- Ethical design mandate: poor design is unethical.
- Controls in place:
  - reproducibility and validity checks
  - attribution and anti-plagiarism protocol
  - strict data-protection rule for non-synthetic data
- Deadline gates:
  - 17 April 2026: ethics package to supervisors
  - 27 April 2026: signed ethics submission to faculty committee

## Slide 9: Timeline and Delivery Plan (0:45)

- 13/20 April: draft proposal presentation
- 18/25 May: formal proposal presentation
- 06/13 July: progress presentation
- 28 September: mock exam or second progress presentation
- 26 to 30 October: draft dissertation submission
- 04 to 06 November: final presentation or prototype demo
- 09 to 13 November: final corrected submission

## Slide 10: Closing and Feedback Requests (0:30)

- Request panel feedback on:
  - adequacy of metrics and hypotheses
  - minimum evidence expected for proposal approval
  - additional constraints for ethics readiness
- Closing line:
  The project aims to produce decision-grade evidence on when AI controller placement is worth its computational cost.

## Backup Slides (Optional)

- Backup A: detailed algorithm parameter table
- Backup B: limitations and threat-to-validity matrix
- Backup C: detailed ethics workflow and approval boundary
