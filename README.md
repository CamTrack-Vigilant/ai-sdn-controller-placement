# ai-sdn-controller-placement

AI-Driven Controller Placement Optimization in Multi-Site Software Defined Networks.

This project provides a practical research scaffold to compare baseline and AI-driven
controller placement strategies across synthetic multi-site SDN topologies.

## Researcher Purpose

I am using this project as a formal scientific inquiry, not only a software build.
My academic identity in this work is to act as a reproducible, evidence-driven
researcher who tests trade-offs between latency, resilience, and computational cost
under controlled conditions.

This means I commit to:

- framing each run around explicit research questions and hypotheses
- using repeatable experiment settings (seeded trials, fixed topology matrices)
- reporting strengths, limitations, and uncertainty rather than only best results
- keeping methodological quality central, because poor research design is unethical

## Working Title and Proposed Research Summary

Working Title:
Multi-Objective Evaluation of AI-Driven Controller Placement in Multi-Site Software Defined Networks: Balancing Performance, Resilience, and Computational Cost

Proposed Research Summary:
This study investigates how controller placement strategies in multi-site software-defined networks should be evaluated when latency, resilience, and computational cost are treated as linked objectives rather than isolated metrics. The project compares baseline methods (random, greedy k-center, and k-means) against AI-driven approaches (genetic search and bandit-based reinforcement learning) across controlled synthetic topologies generated using Barabasi-Albert and Waxman models. A factorial experiment design is used to vary topology family, node scale, and controller budget while preserving reproducibility through fixed seeds and repeated trials. Outcomes are assessed using average controller distance, convergence behavior, runtime cost, and reliability-oriented indicators, with Pareto analysis used to identify practical trade-off fronts. The intended contribution is a reproducible evidence base that clarifies when AI-driven placement is genuinely beneficial, when heuristics remain competitive, and how topology characteristics influence that decision.

## Honours Programme Milestone Alignment (2026)

| Milestone | Programme Date | Project Deliverable |
| --- | --- | --- |
| Working title and summary | Monday, 09 March 2026 | Working title and summary recorded in this README |
| Draft proposal presentation slot | Monday, 13 April 2026 or Monday, 20 April 2026 | Draft proposal slides with problem, methods, pilot evidence |
| Proposal ethics protocol to supervisors | Friday, 17 April 2026 | Complete ethics application package for supervisory review |
| Signed ethics protocol to Faculty Ethics Committee | Monday, 27 April 2026 | Revised and signed ethics protocol submission |
| Proposal presentation slot | Monday, 18 May 2026 or Monday, 25 May 2026 | Formal proposal presentation |
| Progress presentation slot | Monday, 06 July 2026 or Monday, 13 July 2026 | Mid-year progress evidence and updated plan |
| 2nd progress or mock exam presentation | Monday, 28 September 2026 | Mock-exam level presentation and defense rehearsal |
| Draft dissertation submission window | 26 to 30 October 2026 | Draft mini-dissertation for pre-final review |
| Final presentation and prototype demo window | 04 to 06 November 2026 | Final oral and prototype demonstration |
| Final corrected dissertation submission window | 09 to 13 November 2026 | Corrected mini-dissertation and associated outputs |
| Paper requirement linked to project | Final submission stage | Research paper derived from dissertation work |

## Deadline-Focused Action Plan (From 17 March 2026)

- 17 March to 31 March: complete full factorial simulations, convergence analysis, and seed stability checks.
- 01 April to 10 April: finalize proposal narrative, methods justification, and initial results tables.
- 11 April to 20 April: prepare and deliver draft proposal presentation in assigned slot.
- 14 April to 17 April: compile and submit ethics protocol package to supervisors.
- 18 April to 26 April: implement supervisor revisions and collect required signatures.
- 27 April onward: proceed only with approved protocol boundaries for any non-synthetic data activity.

## SMART Research Goals (Next Simulation Cycle)

Cycle window: 17 March 2026 to 31 March 2026

1. Goal 1: Complete the full factorial latency-cost benchmark.
    Specific: Run all scenarios in the BA and Waxman matrix using the factorial runner.
    Measurable: Produce one raw CSV (300 rows), one summary CSV (60 rows), one best-per-scenario CSV (12 rows), and 12 Pareto plots.
    Achievable: The script and parameters already exist in scripts/run_factorial_latency_cost_matrix.py.
    Relevant: Directly supports comparison of baseline and AI placements in this study.
    Time-bound: Complete by 22 March 2026.

2. Goal 2: Evaluate convergence behavior for AI methods.
    Specific: Compare genetic and bandit-RL convergence using iterations_to_converge across all scenarios.
    Measurable: Generate a convergence table covering all 12 scenarios for both AI algorithms.
    Achievable: Convergence metadata is already captured by the current algorithm implementations.
    Relevant: Supports claims about optimization efficiency, not just final latency values.
    Time-bound: Complete by 25 March 2026.

3. Goal 3: Test result stability across seeds.
    Specific: Repeat the factorial run with three base seeds (42, 142, 242).
    Measurable: Report whether top-2 efficiency rankings remain stable in at least 9 out of 12 scenarios.
    Achievable: Only base-seed override is required in existing scripts.
    Relevant: Strengthens reliability and reproducibility claims.
    Time-bound: Complete by 29 March 2026.

4. Goal 4: Produce a supervisor-ready interpretation mapped to hypotheses.
    Specific: Write a concise interpretation of findings mapped to H1 (performance), H2 (efficiency), and H3 (topology sensitivity).
    Measurable: One evidence-based summary section grounded in generated CSV outputs.
    Achievable: Outputs from Goals 1 to 3 provide the needed evidence.
    Relevant: Converts experimental outputs into research argument quality.
    Time-bound: Complete by 31 March 2026.

5. Goal 5: Submit a complete ethics protocol package for supervisory review.
    Specific: Compile ethics form, project summary, data-handling plan, and integrity checks for supervisor review.
    Measurable: One submission package delivered by the interim ethics date.
    Achievable: Core technical methodology and data plan are already documented in README and ETHICS log.
    Relevant: Required for formal faculty ethics pathway and lawful data handling.
    Time-bound: Complete by 17 April 2026.

6. Goal 6: Deliver a draft proposal presentation with evidence-backed methods.
    Specific: Prepare slides covering problem statement, literature gap, methodology, pilot results, and ethics readiness.
    Measurable: One complete deck delivered in the April draft presentation slot.
    Achievable: Current experiment outputs support a defensible pilot evidence section.
    Relevant: Critical gate before full proposal and progression presentations.
    Time-bound: Complete by 13 April 2026 (or assigned backup slot on 20 April 2026).

## Weekly Time Management Audit (Coursework + Research)

Target workload per week:

- Coursework: 18 to 22 hours
- Research project: 12 to 15 hours
- Reflection and buffer: 2 to 3 hours

Recommended schedule:

| Day | Time Block | Primary Focus | Expected Output |
| --- | --- | --- | --- |
| Monday | 18:00-20:00 | Weekly planning and backlog review | Updated run plan and priorities |
| Tuesday | 19:00-21:30 | Coursework reading and assignments | Notes and assignment progress |
| Wednesday | 18:30-21:00 | Simulation execution block | Completed experiment runs |
| Thursday | 19:00-21:00 | Coursework consolidation | Study summaries and revisions |
| Friday | 17:30-20:00 | Data analysis and figure checks | Cleaned tables and draft visuals |
| Saturday | 09:00-12:00 | Deep research work (writing/methods) | Draft methods/results updates |
| Sunday | 17:00-18:30 | Ethics, integrity, and weekly reflection | Updated ETHICS log and next-week risks |

Audit rules to keep balance realistic:

- If coursework deadlines increase, reduce research run volume before reducing sleep.
- Reserve at least one protected 2-hour deep-work block for research each week.
- End each week with a 15-minute check: what was planned, done, deferred, and why.
- Use ETHICS.md as a live integrity and quality-control record.

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
