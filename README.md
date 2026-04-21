# ai-sdn-controller-placement

**AI-Driven Controller Placement Optimization in Multi-Site Software Defined Networks**

## Research Context: Why Network Engineers Remain Skeptical

This project investigates a critical infrastructure decision gap: when should network engineers adopt AI-driven optimization methods for controller placement in Software Defined Networks, and when are simpler, faster heuristic approaches sufficient?

Recent advances in artificial intelligence and metaheuristic optimization have generated optimistic claims about improving infrastructure performance. Yet published comparisons often emphasize performance on isolated metrics (latency) while downplaying computational cost, topology-dependent behavior, or robustness under real-world constraints. This creates methodological risk for infrastructure teams: a method that appears optimal in one metric may be computationally infeasible or unstable under realistic conditions.

This project provides a reproducible research scaffold to answer this question through controlled, multi-objective evaluation of controller placement strategies across varied SDN deployment scenarios.

---

## Researcher Purpose and Academic Identity

I am using this project as a formal scientific inquiry, not only a software build.
My academic identity in this work is to act as a reproducible, evidence-driven
researcher who tests trade-offs between latency, resilience, and computational cost
under controlled conditions.

This means I commit to:

- framing each run around explicit research questions and hypotheses
- using repeatable experiment settings (seeded trials, fixed topology matrices)
- reporting strengths, limitations, and uncertainty rather than only best results
- keeping methodological quality central, because poor research design is unethical

---

## Literature Discovery Strategy: How This Research Was Positioned

This project is grounded in a systematic literature review using best practices in research methodology. For complete documentation, see [Advanced Search Documentation](docs/proposal.md) in the research proposal.

### Literature Foundation

**Key insight**: The literature on SDN controller placement is fragmented and single-metric focused. While many studies claim that AI methods improve latency, few simultaneously evaluate computational cost, multi-objective trade-offs, or robustness across topology families.

**Research gap identified**: There is no unified, reproducible benchmarking framework that evaluates all method families (random, greedy, clustering, genetic, reinforcement learning) under identical conditions with joint reporting of latency, runtime, convergence, and reliability.

### How We Positioned This Work

1. **Citation Pearl Growing Method**: Identified foundational "seed" papers (Heller et al. 2012, Gonzalez 1985) and traced citation paths forward and backward to discover related works across three method families (heuristics, genetic algorithms, reinforcement learning).

2. **Boolean Search Strings**: Used systematic keyword searches across IEEE Xplore, ACM Digital Library, and Google Scholar:
   - `("SDN" OR "Software Defined Network*") AND ("Controller Placement") AND ("Algorithm*" OR "Optimiz*")`
   - `("Controller Placement") AND ("Genetic Algorithm*" OR "Evolutionary Algorithm*")`
   - `("SDN") AND ("Reinforcement Learning" OR "Bandit" OR "Q-Learning")`

3. **Literature Gap Analysis**: Documented three specific gaps:
   - **Reproducibility**: No standard for benchmarking methodology
   - **Scalability**: Evaluation mostly on small topologies (20-100 nodes); behavior at scale unknown
   - **Multi-Objective**: Studies treat latency, cost, and reliability as separate concerns, not unified

4. **Research Positioning**: This project directly addresses all three gaps by:
   - Providing a reproducible, open-source benchmarking pipeline
   - Evaluating across multiple topology families and scales
   - Reporting latency, runtime, convergence, and reliability jointly

### References and Bibliography

All sources used in this project are documented in centralized, IEEE-standardized format:
- **[references.md](references.md)**: Authoritative bibliography with complete citation metadata
- **[REFERENCE_MANAGEMENT_WORKFLOW.md](docs/REFERENCE_MANAGEMENT_WORKFLOW.md)**: Protocol for citation practices and plagiarism prevention

Every claim about prior work is attributed with numbered citations [1]-[8] that correspond to formal references.

---

## Working Title and Proposed Research Summary

Working Title:
Decision-Grade Multi-Objective Benchmarking of AI and Heuristic Controller Placement in Multi-Site Software Defined Networks

Proposed Research Summary:
This study investigates how controller placement strategies in multi-site software-defined networks should be evaluated when latency, resilience, and computational cost are treated as linked objectives rather than isolated metrics. The project compares baseline methods (random, greedy k-center, and k-means) against AI-driven approaches (genetic search and bandit-based reinforcement learning) across controlled synthetic topologies generated using Barabasi-Albert and Waxman models. A factorial experiment design is used to vary topology family, node scale, and controller budget while preserving reproducibility through fixed seeds and repeated trials. Outcomes are assessed using average controller distance, convergence behavior, runtime cost, and reliability-oriented indicators, with Pareto analysis used to identify practical trade-off fronts. The intended contribution is a reproducible evidence base that clarifies when AI-driven placement is genuinely beneficial, when heuristics remain competitive, and how topology characteristics influence that decision.

## Methodological Positioning (Masterclass-Aligned)

- Paradigm: post-positivist quantitative inquiry (positivist family).
- Design type: computational factorial experiment with repeated trials.
- Research logic: deductive hypothesis testing with explicit baseline comparison.

Why this is appropriate for this project:

- The core questions ask whether one method outperforms another on measurable outcomes.
- The codebase supports controlled variable manipulation (topology model, scale, controller budget).
- The pipeline supports inferential interpretation with repeated stochastic trials and seed-traceable outputs.

Quantitative analysis standards used in this repository:

- Descriptive statistics (mean, standard deviation, confidence intervals).
- Pairwise contrasts against baseline methods using bootstrap confidence intervals.
- Practical effect-size reporting to avoid over-reliance on p-value style claims.
- Pareto and efficiency-rank analysis for multi-objective decision quality.

Qualitative scope note:

- No interviews or observations are in the current synthetic-only phase.
- If expert interviews are added later, coding/thematic analysis and trustworthiness checks will be executed only after formal ethics approval.

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

Default weights are configured in [configs/experiment_config.json](configs/experiment_config.json) under `rl_objective`.

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## Outputs

- CSV result files are written to [results/experiment_data](results/experiment_data).
- Metric comparison plots are written to [results/graphs](results/graphs).
- Run logs are written to [logs/](logs).
- RL training traces are written to [logs/rl_training.jsonl](logs/rl_training.jsonl) (configurable).

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

Factorial latency-cost runs export complementary statistical evidence files in [results/experiment_data](results/experiment_data):

- `factorial_latency_cost_raw_*.csv`: all algorithm-trial observations.
- `factorial_latency_cost_summary_*.csv`: scenario-level descriptive summaries.
- `factorial_latency_cost_best_*.csv`: best compromise method per scenario.
- `factorial_latency_cost_stats_*.csv`: scenario-level pairwise contrasts, confidence intervals, and effect sizes.

## Data Collection & Analysis Standards

This project is designed to meet academic research standards for data integrity, reproducibility, and analysis rigor. All data collection processes are documented and validated according to March 31st Data Collection & Analysis Excellence standards.

### Sampling Methodology

**Two-stage sampling strategy**:
- **Non-probability purposive sampling** (topology selection): Deliberate selection of Barabasi-Albert and Waxman topology models across defined node scales (12, 24, 36, 48 nodes/site) to maximize informational richness and support theoretical investigation.
- **Probability sampling** (trial replication): Within each scenario, repeated stochastic trials using independent random seeds enable unbiased estimation of algorithm behavior distribution and valid statistical inference.

**Sample size justification**: Target of 20–30 trials per algorithm per scenario (~7,200 total observations across 3 seed sets) provides:
- ±5–7 ms margin of error for latency estimates (95% CI)
- 75–80% statistical power to detect medium effect sizes (Cohen's d ≈ 0.6–0.7)
- Rank stability validation across independent seed conditions

For complete justification, see [Sample Size Calculation and Statistical Power Rationale](docs/proposal.md) in the research proposal.

### Pilot Testing & Quality Assurance

All experiments undergo systematic **pilot testing** before confirmatory data collection:
- **Pilot phase**: 4 representative scenarios, 5 trials each (20 scenario-algorithm combinations)
- **Validation checks**: Script syntax, metric generation, CSV integrity, seed reproducibility, algorithm parameter calibration
- **Decision gate**: If all checks pass → proceed to full factorial experiment; if checks fail → debug and re-run

For detailed pilot procedures, see [Pilot Testing Procedure](docs/proposal.md) in the research proposal.

### Data Validation Protocol

Systematic procedures to detect and handle data quality issues:

**During Collection**:
- Real-time CSV integrity validation (metrics are non-null, logically consistent)
- Seed traceability checks (every row includes topology_seed and trial_seed)
- Runtime outlier flagging (runtimes > 3s MAD flagged for investigation)

**Post-Collection**:
- CSV schema verification (column presence, data types)
- Metric range checks (average_distance ∈ [0–200], resilience_ratio ∈ [0–1])
- Logical consistency (average_distance ≤ worst_case_distance)
- Missing data inventory (flag if ≥5% missing per algorithm/scenario)

**Outlier handling policy**: Outliers retained with documentation unless confirmed data errors; sensitivity analysis reports results with/without outliers.

For complete protocol, see [Data Validation Protocol](docs/proposal.md) in the research proposal.

### Reproducibility Controls

**Fixed random seeds**: Every stochastic element uses deterministic seeding for reproducibility.
- Topology generation: base_seed (e.g., 42) fixed per scenario
- Trial sequences: each trial receives distinct, deterministically generated seed
- Algorithms: genetic and RL algorithms accept seed parameter → deterministic execution

**Verification**: Re-run identical experiment configuration with identical seed; expect bit-identical outputs (diff < 1% floating-point tolerance).

See [RUNNING.md - Reproducibility & Audit Trail](RUNNING.md#reproducibility--audit-trail) for exact verification protocol.

### Statistical Analysis & SPSS/GENSTAT Compatibility

All inferential statistics are conducted using Python (Pandas, NumPy, SciPy) with transparent, open-source implementations. For departmental verification, analysis outputs are formatted for compatibility with standard statistical software:

- **CSV Tables for SPSS/GENSTAT Import**: Scenario summaries, pairwise comparisons, and raw trial data formatted as .csv files with consistent encoding (UTF-8, period decimal separator).
- **Statistical Documentation**: Summary statistics table (PDF) formatted for manual transcription if supervisor prefers native SPSS/GENSTAT verification.
- **Data Dictionary**: Complete documentation of every column (data type, units, valid ranges, interpretation).

**Verification Workflow**: Departmental supervisor (if independent verification requested) can import exports into SPSS/GENSTAT and re-compute descriptive statistics to confirm Python-generated values match (tolerance: ±0.01%).

For complete specification, see [Inferential Statistics & Departmental Verification Protocol (SPSS/GENSTAT Compatibility)](docs/proposal.md) in the research proposal.

### Data Integrity & Cleaning

For detailed data collection tools, digital logging methods, validation checklists, and archival procedures, see:
- **[RUNNING.md - Data Integrity & Cleaning](RUNNING.md#data-integrity--cleaning)**: Technical implementation of validation procedures, data collection tools inventory, and reproducibility protocols.
- **[Pilot Testing Procedure](docs/proposal.md)**: Multi-step validation before confirmatory data collection.
- **[Data Validation Protocol](docs/proposal.md)**: Outlier handling, missing data policies, and CSV integrity verification.

---

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

1. Define: Build or load the graph in [topology/](topology) (and keep external inputs in [data/raw/](data/raw)).
2. Measure: Run [algorithms/baseline/random_placement.py](algorithms/baseline/random_placement.py) to establish floor performance.
3. Optimize: Train and evaluate [algorithms/ai/reinforcement_learning.py](algorithms/ai/reinforcement_learning.py) placement behavior.
4. Validate: Run [simulation/mininet_simulation.py](simulation/mininet_simulation.py) to compare theoretical and virtual-network latency.
5. Visualize: Use [evaluation/performance_analysis.py](evaluation/performance_analysis.py) to generate plots in [results/graphs/](results/graphs).

## Next Research Steps

- Replace synthetic simulation with Mininet-backed traffic experiments.
- Add additional RL policies and hyperparameter sweeps.
- Evaluate robustness under controller and link failures.
