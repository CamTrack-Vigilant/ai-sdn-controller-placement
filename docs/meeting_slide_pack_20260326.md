# Meeting Slide Pack (2026-03-26)

## Regenerated Outputs

- Stress raw: results/experiment_data/stress_test_raw_20260326_021046.csv
- Stress summary: results/experiment_data/stress_test_summary_20260326_021046.csv
- Stress best compromise: results/experiment_data/stress_test_best_compromise_20260326_021046.csv
- Stress correlation: results/experiment_data/stress_test_correlation_20260326_021046.csv
- Stress scatter: results/graphs/latency_vs_reliability_20260326_021046.png
- Factorial summary: results/experiment_data/factorial_latency_cost_summary_20260326_021307.csv
- Factorial best: results/experiment_data/factorial_latency_cost_best_20260326_021307.csv
- Factorial Pareto plots: results/graphs/latency_cost_pareto_20260326_021307

## Slide 1: Stress-Test Summary Table (Best Compromise per Scenario)

| scenario | algorithm | average_distance | runtime_ms | iterations_to_converge |
| --- | --- | --- | --- | --- |
| sites2_k2 | genetic | 1.520 | 58.96 | 18.3 |
| sites2_k3 | bandit_rl | 1.266 | 570.77 | 7.0 |
| sites2_k5 | genetic | 0.999 | 124.09 | 28.3 |
| sites3_k2 | genetic | 2.549 | 102.70 | 12.0 |
| sites3_k3 | genetic | 1.614 | 109.04 | 30.0 |
| sites3_k5 | genetic | 1.228 | 146.40 | 35.3 |
| sites4_k2 | genetic | 2.772 | 112.18 | 20.0 |
| sites4_k3 | genetic | 2.330 | 131.32 | 37.7 |
| sites4_k5 | genetic | 1.531 | 179.87 | 47.3 |

### Short interpretation
- In this run, control-plane reliability is saturated at 1.0 for all best-compromise points, so differentiation is currently driven by latency and runtime/convergence.

## Slide 2: Ranking Changes Across Topology Families/Scales

### Winner by Topology Family, Node Scale, and Controller Budget

| topology_model | node_count | controller_budget | algorithm | efficiency_score |
| --- | --- | --- | --- | --- |
| barabasi_albert | 20 | 3 | genetic | 0.1045 |
| waxman | 20 | 3 | genetic | 0.3194 |
| barabasi_albert | 20 | 5 | genetic | 0.1469 |
| waxman | 20 | 5 | greedy_k_center | 0.2192 |
| barabasi_albert | 50 | 3 | genetic | 0.0367 |
| waxman | 50 | 3 | genetic | 0.0922 |
| barabasi_albert | 50 | 5 | genetic | 0.0512 |
| waxman | 50 | 5 | genetic | 0.1226 |
| barabasi_albert | 100 | 3 | genetic | 0.0173 |
| waxman | 100 | 3 | genetic | 0.0164 |
| barabasi_albert | 100 | 5 | genetic | 0.0215 |
| waxman | 100 | 5 | genetic | 0.0191 |

### Where Rankings Change

| node_count | controller_budget | winners | ranking_shift |
| --- | --- | --- | --- |
| 20 | 3 | genetic | No |
| 20 | 5 | genetic, greedy_k_center | Yes |
| 50 | 3 | genetic | No |
| 50 | 5 | genetic | No |
| 100 | 3 | genetic | No |
| 100 | 5 | genetic | No |

Interpretation line for slide:
- Ranking behavior is mostly stable (genetic dominates most scenarios), with one observed cross-topology shift at node_count=20 and controller_budget=5 (barabasi_albert: genetic vs waxman: greedy_k_center).

## Slide 3 (Backup): Limitations and External Validity Boundaries

- Synthetic topology scope only (barabasi_albert and waxman); findings should be validated on real operational topologies.
- Reliability metric currently models single-link failures; correlated or multi-failure behavior is not yet modeled.
- Runtime measurements are host-dependent and should be interpreted comparatively within the same execution environment.
- Bandit RL and genetic settings are fixed for this run; broader hyperparameter sweeps may change relative rankings.
- Current recommendation is scenario-conditioned, not universal; avoid claims that AI methods are always superior.
