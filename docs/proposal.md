# Research Proposal

## Title

AI-Driven Controller Placement Optimization in Multi-Site Software Defined Networks

## Executive Summary

In multi-site SDN deployments, controller placement decisions affect network latency, reliability, and operational cost. Yet published comparisons of placement methods often prioritize single metrics (latency) while downplaying computational burden, topology-dependent behavior, and multi-objective trade-offs. This creates an infrastructure decision gap: when is AI-driven optimization genuinely superior to baseline heuristics, and when is the added computational cost unjustified?

This study provides reproducible, multi-objective evidence through controlled benchmarking. It compares baseline methods (random, greedy k-center, k-means) and AI-driven approaches (genetic algorithm, bandit reinforcement learning) across varied topology families and scales, with joint evaluation of latency, runtime, reliability, and convergence behavior. The result is scenario-conditioned method selection guidance: conditions under which AI is justified, conditions under which heuristics suffice, and practical trade-off frameworks for real deployments.

## Problem Statement and Research Questions

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
