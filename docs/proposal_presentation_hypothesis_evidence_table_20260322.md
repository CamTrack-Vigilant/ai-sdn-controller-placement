# Hypothesis Evidence Table for Proposal Deck

Benchmark run timestamp: 2026-03-22 05:22:49

Source files:
- results/experiment_data/factorial_latency_cost_stats_20260322_052249.csv
- results/experiment_data/factorial_latency_cost_summary_20260322_052249.csv
- results/experiment_data/factorial_latency_cost_best_20260322_052249.csv

## H1, H2, H3 Evidence Summary

| Hypothesis | Operational test in this benchmark | Observed evidence (12 scenarios) | Interpretation for proposal deck | Status for this dataset |
| --- | --- | --- | --- | --- |
| H1 Performance: AI methods reduce latency vs baselines under constraints | AI vs random latency gain and AI vs strongest non-AI latency comparison | Genetic latency gain > 0 in 12/12 scenarios with CI lower bound > 0 in 12/12; Bandit RL latency gain > 0 in 12/12 with CI lower bound > 0 in 12/12; best AI latency beats best non-AI latency in 12/12 | Strong evidence that AI methods improve latency in this matrix. | Supported for latency component; full under-constraints claim remains partial because this run did not include reliability metric columns. |
| H2 Efficiency: latency gains must be judged with runtime and convergence burden | Runtime penalty vs random and best-compromise method selection | Genetic runtime penalty > 0 in 12/12 with CI lower bound > 0 in 12/12; Bandit RL runtime penalty > 0 in 12/12 with CI lower bound > 0 in 12/12; AI is best compromise in 10/12 scenarios (non-AI wins 2/12) | AI improves latency but pays measurable runtime cost; superiority is conditional once efficiency is considered. | Supported |
| H3 Topology/scale sensitivity: rankings vary by scenario | Best-per-scenario algorithm identity across topology and scale cells | Best algorithm set includes both genetic and greedy_k_center; greedy_k_center wins in 2/12 scenarios (barabasi_albert n=20 k=3 and waxman n=20 k=5), genetic wins in 10/12 | No universal winner across all scenario cells; method suitability depends on scenario structure. | Supported |

## Scenario-specific points to cite in slides

- AI best-compromise dominance is high but not absolute: 10 out of 12 scenarios.
- Non-AI wins are concentrated in small-node scenarios (n=20), indicating potential scale and budget interaction effects.
- The most conservative claim for the proposal deck is: AI has consistent latency advantages in this benchmark, but deployment recommendation must include compute-efficiency and scenario context.

## Suggested one-line deck statements

- H1: Across all 12 factorial scenarios, AI methods achieved statistically positive latency gains over random and outperformed the strongest non-AI latency baseline.
- H2: Every AI latency gain came with a runtime penalty, and non-AI remained the best compromise in selected scenarios, confirming conditional rather than universal AI superiority.
- H3: Winner identity changed across topology and scale cells, supporting scenario-conditioned controller placement policy.

## Analytical Discussion Injection for Deck Narrative

Interpret the 12/12 pattern analytically:

The genetic algorithm's consistent latency advantage is theoretically coherent with complex SDN placement dynamics. Greedy methods commit to locally good controller positions and do not revisit those choices, so early decisions can lock in suboptimal global structures. Genetic optimization uses stochastic exploration and recombination across multiple candidate placements, which increases the chance of escaping local minima and discovering globally improved controller sets in heterogeneous graphs.

Explain the small-scale anomaly:

Heuristics remain competitive in small graphs because the search space is comparatively small and the topology has lower structural heterogeneity. Under these conditions, clustering and constructive rules can approximate near-optimal solutions quickly. As graph size and heterogeneity increase, local assignment logic loses global coordination quality, and stochastic global search becomes more beneficial.

UNIZULU-aligned methodological language:

These findings are not based on isolated point estimates. Inferential power is strengthened through confidence intervals and bootstrap contrasts, while methodological rigor is supported through repeated seeded trials, reproducible scripts, and auditable exports.

Synthesis and formal recommendation:

The evidence supports conditional adoption rather than blanket AI preference. Where controller placement is planned offline and latency quality has durable operational impact, genetic optimization should be preferred despite runtime overhead. Where rapid or low-cost reconfiguration is required, heuristics should be used as operational defaults, with AI re-optimization triggered when network scale or performance drift crosses predefined thresholds.

## Limitations to place in small print

- This factorial run was latency-cost focused; reliability constraints were not included in the exported stats table.
- Reliability triangulation should be added from reliability-enabled benchmark outputs before final dissertation-level claim locking.
