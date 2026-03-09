# ai-sdn-controller-placement

AI-Driven Controller Placement Optimization in Multi-Site Software Defined Networks.

This project provides a practical research scaffold to compare baseline and AI-driven
controller placement strategies across synthetic multi-site SDN topologies.

## Project Structure

```text
ai-sdn-controller-placement
├── README.md
├── requirements.txt
├── .gitignore
├── data
│   ├── raw
│   └── processed
├── configs
│   └── experiment_config.json
├── logs
├── docs
│   ├── proposal.md
│   ├── literature_review.md
│   └── research_notes.md
├── topology
│   └── network_topology.py
├── algorithms
│   ├── baseline
│   │   ├── random_placement.py
│   │   ├── greedy_placement.py
│   │   └── kmeans_placement.py
│   └── ai
│       ├── genetic_algorithm.py
│       └── reinforcement_learning.py
├── simulation
│   └── mininet_simulation.py
├── evaluation
│   ├── metrics.py
│   └── performance_analysis.py
├── experiments
│   └── experiment_runner.py
├── scripts
│   ├── plot_rl_training_log.py
│   └── stress_test_latency_reliability.py
├── tests
│   ├── test_experiment_config.py
│   ├── test_pareto_frontier.py
│   ├── test_reliability_metric.py
│   └── test_rl_logging.py
└── results
    ├── graphs
    └── experiment_data
```

## Quick Start

1. Create and activate a virtual environment.
2. Install dependencies.
3. Run experiments.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python experiments/experiment_runner.py --config configs/experiment_config.json
```

You can still override config values at runtime, for example:

```bash
python experiments/experiment_runner.py --config configs/experiment_config.json --controllers 4 --trials 10
```

The RL baseline supports reward shaping with a composite objective:

`reward = -(latency_weight * average_distance) + (reliability_weight * control_plane_reliability)`

Default weights are configured in `configs/experiment_config.json` under `rl_objective`.

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## Outputs

- CSV result files are written to `results/experiment_data`.
- Metric comparison plots are written to `results/graphs`.
- Run logs are written to `logs/`.
- RL training traces are written to `logs/rl_training.jsonl` (configurable).

Core benchmark metrics include:

- `average_distance`
- `worst_case_distance`
- `controller_load_std`
- `resilience_ratio` (controller failure degradation)
- `control_plane_reliability` (node-to-controller reachability under single-link failures)

To plot RL training progression for the latest run:

```bash
python scripts/plot_rl_training_log.py --input logs/rl_training.jsonl --output-dir results/graphs
```

To run a matrix stress test and generate a latency-vs-reliability scatter plot:

```bash
python scripts/stress_test_latency_reliability.py --sites 2,3,4 --controllers 2,3,5 --trials 3
```

This stress test now also exports a Pareto-front CSV (`stress_test_pareto_*.csv`) where
latency is minimized and reliability is maximized per scenario.

It additionally exports:

- `stress_test_pareto_ranked_*.csv`: Pareto points ranked by normalized ideal-point distance.
- `stress_test_best_compromise_*.csv`: one rank-1 compromise point per scenario.

## Optional Mininet Backend

- `simulation/mininet_simulation.py` includes `run_mininet_simulation(...)` for RTT measurement on a real Mininet topology built from the NetworkX graph.
- If Mininet is unavailable or fails at runtime, the function automatically falls back to `run_synthetic_latency_simulation(...)` by default.
- To enforce Mininet-only behavior, call with `fallback_to_synthetic=False`.

Example:

```python
from simulation.mininet_simulation import run_mininet_simulation

result = run_mininet_simulation(graph, controllers, fallback_to_synthetic=True)
print(result.average_rtt_ms, result.worst_rtt_ms)
```

## Recommended Workflow

1. Define: Build or load the graph in `topology/` (and keep external inputs in `data/raw/`).
2. Measure: Run `algorithms/baseline/random_placement.py` to establish floor performance.
3. Optimize: Train and evaluate `algorithms/ai/reinforcement_learning.py` placement behavior.
4. Validate: Run `simulation/mininet_simulation.py` to compare theoretical and virtual-network latency.
5. Visualize: Use `evaluation/performance_analysis.py` to generate plots in `results/graphs/`.

## Next Research Steps

- Replace synthetic simulation with Mininet-backed traffic experiments.
- Add additional RL policies and hyperparameter sweeps.
- Evaluate robustness under controller and link failures.
