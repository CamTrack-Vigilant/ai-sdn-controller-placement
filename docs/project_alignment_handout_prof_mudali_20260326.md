# Project Alignment Handout (Prof. Mudali)

## Project Identity (Supervisor-Facing)

**Final working title**
Decision-Grade Multi-Objective Benchmarking of AI and Heuristic Controller Placement in Multi-Site Software Defined Networks

**Core contribution type**
Evaluation methodology and decision framework contribution, supported by a reproducible benchmark artifact.

**One-sentence problem framing**
In multi-site SDN planning, does evaluating AI and heuristic controller placement methods jointly on latency, control-plane reliability, runtime, and convergence produce more defensible method-selection guidance than latency-only comparisons?

## Workshop Alignment Verdict

1. Contribution to knowledge: **Pass**
- Clear gap: existing studies are fragmented and often single-metric.
- Clear contribution: one controlled and reproducible benchmark pipeline with multi-objective reporting and scenario-conditioned recommendations.

2. Researchability and measurable variables: **Pass**
- Variables are explicit and measurable: latency, reliability, runtime, convergence.
- Independent factors are explicit: topology family, node scale, controller budget, algorithm class.

3. Feasibility in Honours timeline: **Pass (with execution discipline)**
- Existing scripts already generate benchmark CSVs, Pareto outputs, and statistical contrasts.
- Existing test suite passed in current environment.

4. Focus and framing quality: **Conditional pass**
- Framing is now decision-grade and multi-objective.
- Final oral defense should avoid language implying "AI is always better" and foreground conditional recommendations.

## Tightened Research Questions

**Primary RQ**
In multi-site synthetic SDN topologies, do AI-driven controller placement methods provide superior multi-objective decision quality compared with baseline heuristics when latency, control-plane reliability, runtime, and convergence burden are evaluated jointly?

**Supporting RQ1 (Performance and Robustness)**
Under fixed topology families, node scales, and controller budgets, what is the effect size of AI methods versus baseline heuristics on average controller-switch latency and control-plane reliability?

**Supporting RQ2 (Computational Efficiency)**
After accounting for runtime cost and convergence burden, which algorithms remain practically superior and Pareto-efficient for planning use cases?

**Supporting RQ3 (Generalization Boundaries)**
How stable are algorithm rankings across topology families and scale levels, and where do rankings shift enough to require scenario-conditioned method selection guidance?

## What Was Strengthened in the Codebase

1. Shared benchmark rows now include runtime and convergence metadata.
2. Stress-test summaries now aggregate runtime and convergence alongside latency and reliability.
3. Correlation export now includes latency/reliability, latency/runtime, and reliability/runtime views.

## Defense Talking Points (Concise)

1. This is not "AI model building"; it is decision-quality research on method selection under operational constraints.
2. The novelty is methodological integration: baseline + AI under identical conditions, with reproducible outputs and trade-off evidence.
3. The expected outcome is conditional guidance:
- when AI is justified,
- when heuristics are sufficient,
- and where topology/scale shifts the recommendation.

## Meeting-Ready Actions Completed

1. Stress-test outputs were regenerated with the updated runtime/convergence-aware pipeline.
2. A slide-ready summary table (best compromise per scenario) was prepared in `docs/meeting_slide_pack_20260326.md`.
3. A ranking-change slide was prepared using topology-family/scale factorial results, including the observed shift at node_count=20 and controller_budget=5.
4. A backup slide section with limitations and external-validity boundaries was prepared in `docs/meeting_slide_pack_20260326.md`.
