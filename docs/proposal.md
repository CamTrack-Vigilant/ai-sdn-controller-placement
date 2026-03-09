# Research Proposal

## Title

AI-Driven Controller Placement Optimization in Multi-Site Software Defined Networks

## Problem Statement

Controller placement has a direct impact on SDN control-plane latency, scalability,
and resilience. In multi-site deployments, static placement policies may underperform
under varying traffic and topology constraints.

## Objectives

- Build a reproducible benchmark for controller placement in multi-site SDN.
- Compare baseline methods (random, greedy, clustering) with AI approaches.
- Measure latency, load balance, and resilience under failures.

## Methodology

1. Generate synthetic multi-site topologies.
2. Run multiple placement algorithms over repeated trials.
3. Evaluate outcomes with common SDN controller placement metrics.
4. Analyze trade-offs and identify best-performing strategies by scenario.

## Expected Deliverables

- Reusable experiment runner and metrics pipeline.
- Comparative performance plots and benchmark CSV data.
- Research report summarizing findings and limitations.
