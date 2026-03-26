# Research Proposal

## Title

Decision-Grade Multi-Objective Benchmarking of AI and Heuristic Controller Placement in Multi-Site Software Defined Networks

## Executive Summary

In multi-site SDN deployments, controller placement decisions affect network latency, reliability, and operational cost. Yet published comparisons of placement methods often prioritize single metrics (latency) while downplaying computational burden, topology-dependent behavior, and multi-objective trade-offs. This creates an infrastructure decision gap: when is AI-driven optimization genuinely superior to baseline heuristics, and when is the added computational cost unjustified?

This study provides reproducible, multi-objective evidence through controlled benchmarking. It compares baseline methods (random, greedy k-center, k-means) and AI-driven approaches (genetic algorithm, bandit reinforcement learning) across varied topology families and scales, with joint evaluation of latency, runtime, reliability, and convergence behavior. The result is scenario-conditioned method selection guidance: conditions under which AI is justified, conditions under which heuristics suffice, and practical trade-off frameworks for real deployments.

## Problem Statement and Research Questions

In multi-site SDN controller placement, method claims are frequently made from single metrics (typically latency), even though deployment decisions require joint interpretation of latency, reliability, runtime cost, and optimization burden. This creates a decision-risk gap: teams can over-adopt complex AI methods without clear evidence that gains remain defensible once computational and robustness constraints are included.

Primary research question:

- In multi-site synthetic SDN topologies, do AI-driven controller placement methods provide superior multi-objective decision quality compared with baseline heuristics when latency, control-plane reliability, runtime, and convergence burden are evaluated jointly?

Supporting research questions:

- Under fixed topology families, node scales, and controller budgets, what is the effect size of AI methods versus baseline heuristics on average controller-switch latency and control-plane reliability?
- After accounting for runtime cost and convergence burden, which algorithms remain practically superior and Pareto-efficient for planning use cases?
- How stable are algorithm rankings across topology families and scale levels, and where do rankings shift enough to require scenario-conditioned method selection guidance?

## Objectives

- Build a reproducible benchmark for controller placement in multi-site SDN.
- Compare baseline methods (random, greedy, clustering) with AI approaches.
- Measure latency, load balance, and resilience under failures.

## Methodology

Research paradigm and design:

- Paradigm: post-positivist (positivist family), suitable for hypothesis testing with measurable outcomes.
- Design: computational factorial experiment with repeated trials across topology family, node scale, and controller budget.

Method steps:

1. Generate synthetic multi-site topologies.
2. Run baseline and AI placement algorithms over repeated seeded trials.
3. Evaluate latency, reliability, runtime, and convergence metrics.
4. Analyze trade-offs with Pareto and efficiency ranking by scenario.
5. Report statistical evidence (confidence intervals, bootstrap contrasts, effect sizes) for key comparisons.

Sample-size and inference note:

- Pilot runs use smaller trial counts for instrumentation checks.
- Confirmatory runs increase trials per scenario to support stable estimates and defensible statistical interpretation.

## Expected Deliverables

- Reusable experiment runner and metrics pipeline.
- Comparative performance plots and benchmark CSV data.
- Research report summarizing findings and limitations.
