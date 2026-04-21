# Running Project Modules

This guide explains how to run the different modules in this project.

## Citing This Work

If you use code, benchmarks, or results from this project in your research, please cite it as follows:

**BibTeX Format**:
```bibtex
@mastersthesis{buthelezi2026sdn,
  author = {Buthelezi, Thabang Nhlokoma},
  title = {Multi-Objective Evaluation of {AI}-Driven Controller Placement in Multi-Site {SDN}: 
           Balancing Performance, Reliability, and Computational Cost},
  school = {University of Zululand},
  year = {2026},
  type = {BSc Honours Thesis},
  note = {Available at \url{https://github.com/CamTrack-Vigilant/ai-sdn-controller-placement}}
}
```

**IEEE Format**:
```
[#] T. N. Buthelezi, "Multi-objective evaluation of AI-driven controller placement in multi-site SDN: 
Balancing performance, reliability, and computational cost," BSc Honours Thesis, University of Zululand, 
South Africa, 2026. [Online]. Available: https://github.com/CamTrack-Vigilant/ai-sdn-controller-placement
```

**APA Format**:
```
Buthelezi, T. N. (2026). Multi-objective evaluation of AI-driven controller placement in multi-site SDN: 
Balancing performance, reliability, and computational cost [Unpublished masters thesis]. University of 
Zululand. https://github.com/CamTrack-Vigilant/ai-sdn-controller-placement
```

### Using Code & Benchmarks from This Project

If you reuse code modules, benchmark framework, or experimental design from this project:

1. **Cite the project** using one of the formats above
2. **Acknowledge the reproduction**: "Code and benchmarking framework adapted from Buthelezi (2026)"
3. **Link to the repository**: Include the GitHub URL or DOI (if available)
4. **Preserve licenses**: Follow the project license (see LICENSE file)

---

## Quick Start

### Option 1: Use the Entry Point Scripts (Recommended)

Run modules using the provided entry point scripts from the project root:

```bash
# Activate virtual environment
.venv\Scripts\activate   # Windows
source .venv/bin/activate   # Linux/Mac

# Run RL training
python run_rl_training.py
```

## Linux/WSL2 Decision-Grade Benchmark Flow

Use this path for final Honours evidence collection.

### Ubuntu/WSL2 setup

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip mininet
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Ensure `ryu-manager` is available in your active environment before strict runs.

### Push-button preflight + benchmark

```bash
source .venv/bin/activate
python scripts/run_linux_ready_benchmark.py --config configs/experiment_config.json --trials 30 --strict-decision-grade
```

This command executes:

- `env_check.py` preflight (unless `--skip-preflight` is passed)
- `experiments/experiment_runner.py` with your forwarded arguments

### Run modes

- `decision_grade`: set `--strict-decision-grade` and use trial counts in multiples of 30.
- `non_decision_grade`: default mode for exploratory or development runs.

If strict mode is enabled and trials are not a positive multiple of 30, execution fails fast with remediation guidance.

### Expected outputs

- Benchmark CSV in `results/experiment_data/benchmark_<timestamp>.csv`
- Manifest JSON in `results/experiment_data/manifest.json`
- Timestamped manifest in `results/experiment_data/manifest_<timestamp>.json`
- Metric plots in `results/graphs/`

### Option 2: Run as Module from Project Root

```bash
# Activate virtual environment
.venv\Scripts\activate

# Run any module using Python's -m flag
python -m algorithms.ai.reinforcement_learning
python -m experiments.run_experiments
python -m tests.test_reinforcement_learning
```

### Option 3: Set PYTHONPATH

```bash
# Windows PowerShell
$env:PYTHONPATH = "C:\...\ai-sdn-controller-placement"
python algorithms/ai/reinforcement_learning.py

# Linux/Mac
export PYTHONPATH=/path/to/ai-sdn-controller-placement
python algorithms/ai/reinforcement_learning.py
```

## Why This Matters

The project uses **absolute imports** like:

```python
from evaluation.metrics import control_plane_reliability_single_link_failure
from topology.network_topology import generate_multi_site_topology
```

These imports expect the project root to be in Python's module search path. Running a script directly (e.g., `python algorithms/ai/reinforcement_learning.py`) from inside a subdirectory will fail with `ModuleNotFoundError`.

## Available Entry Scripts

- **`run_rl_training.py`**: Train RL agent for controller placement
  - Uses bandit-based epsilon-greedy algorithm
  - Configurable topology, episodes, and reward weights
  - Logs training progress to JSONL

- **[scripts/run_factorial_latency_cost_matrix.py](scripts/run_factorial_latency_cost_matrix.py)**: Run full factorial latency-cost benchmark
  - Compares baseline and AI algorithms across topology families and scales
  - Exports raw, summary, best-per-scenario, and statistical comparison CSV files
  - Generates Pareto frontier plots per scenario

## Running Tests

Always run tests from the project root:

```bash
# Activate venv
.venv\Scripts\activate

# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_reinforcement_learning.py

# Run with verbose output
python -m pytest -v tests/
```

## Data Integrity & Cleaning

This section documents data collection tools, validation procedures, and integrity checks used to ensure analysis-ready datasets for hypothesis testing.

### Data Collection Tools & Digital Logging

**Primary Data Source**: Algorithmic outputs from scripted Python experiments (not manual logging or external databases).

**Data Collection Scripts**:

| Script | Purpose | Output Format | Integrity Controls |
|--------|---------|---------------|-------------------|
| [scripts/run_factorial_latency_cost_matrix.py](scripts/run_factorial_latency_cost_matrix.py) | Benchmark all algorithms across factorial scenario matrix | CSV (raw, summary, best-per-scenario) | Fixed seeds, algorithm-specific logging, runtime validation |
| [experiments/experiment_runner.py](experiments/experiment_runner.py) | Execute single scenario with repeated trials | CSV rows per algorithm-trial combination | Deterministic seed generation, metric validation |
| `run_rl_training.py` | Train RL bandit agent with reward logging | JSONL (structured training log) | Episode counter, episode completion status, seed traceability |
| `analyze_rl_logs.py` | Aggregate RL training logs into scenario-level summaries | CSV aggregated RL metrics | Episode filtering (exclude early episodes), convergence validation |

**Data Collection Workflow**:

1. **Pre-Collection Validation** (Pilot phase, Section 8.7):
   - Run 4 representative scenarios with 5 trials each (20 total scenario-algorithm-trial combinations).
   - Validate: all algorithms complete, metrics are non-null, CSV structure is correct, reproducibility (re-run same seed produces identical output).
   - Gate decision: If all checks pass → proceed to full factorial experiment. If checks fail → debug and re-run pilot.

2. **During-Collection Monitoring**:
   - Real-time CSV integrity checks (Section 8.7a): after each algorithm completes within a scenario, verify row was written with all columns populated.
   - Runtime tracking: capture start time and end time for each algorithm; flag runtimes > 3× median for same algorithm/scenario as potential anomalies (system load interference).
   - Log file rotation: if logs exceed 100 MB, archive to timestamped backup and start new log file (prevents disk-space strain).

3. **Post-Collection Validation** (Data Validation Protocol, Section 8.7a):
   - Load all scenario output CSVs into pandas DataFrame.
   - Verify: no duplicate rows (same algorithm, trial, scenario), all required columns present, no rows with >30% NaN values.
   - Cross-scenario consistency checks (e.g., latency should generally improve as controllers increase; topology model shouldn't cause extreme ranking inversions).
   - Export validation report: `results/data_validation_report.md` with row counts, missing data summary, outlier flags, constraint violations.

### Data Validation Checklist (Pre-Analysis)

Before conducting inferential statistics or hypothesis testing on raw trial data:

- ✓ **CSV Schema Validation**: Confirm all expected columns present; no extraneous columns.
- ✓ **Metric Range Checks**: 
  - average_distance ∈ [0, 200] ms (typical for latencies in synthetic networks)
  - resilience_ratio ∈ [0, 1] (bounded proportion)
  - runtime_seconds ∈ [0.01, 300] second (no zero-time runs, no 10+ minute runs for synthetic scenarios)
- ✓ **Logical Consistency**:
  - average_distance ≤ worst_case_distance (fundamental constraint)
  - For same algorithm, same scenario: mean(runtime) ≈ median(runtime) ±50% (flags extreme outliers if >100% deviation)
- ✓ **Seed Traceability**: Every row includes topology_seed and trial_seed for reproducibility verification.
- ✓ **Missing Data Inventory**: If ≥5% of expected trials are missing per algorithm per scenario, flag for re-run.
- ✓ **Outlier Documentation**: If outliers are retained, document in results narrative (e.g., "Trial X excluded due to algorithm timeout").

### Reproducibility & Audit Trail

**Fixed Seed Governance**:

All stochastic elements use deterministic seeding:
- **Topology generation**: base_seed (e.g., 42) fixed per scenario; independent random graphs use fixed seed → identical topology on re-run.
- **Trial randomness**: Each trial uses distinct seed generated from base seed via `rng.randint(0, 10^9)` → statistically independent but reproducible trial sequence.
- **Algorithm randomization**: Algorithms accepting seed parameter (genetic, RL) receive trial_seed → deterministic execution given seed.

**Example Reproducibility Protocol**:

```bash
# Run 1 (original data collection)
python scripts/run_factorial_latency_cost_matrix.py \
  --topology-families barabasi_albert,waxman \
  --node-scales 12,24,36,48 \
  --controller-budgets 3,4,5 \
  --trials 20 \
  --seed 42 \
  --output-dir results/experiment_data/seed_42_trial20

# Run 2 (verification re-run, identical configuration)
python scripts/run_factorial_latency_cost_matrix.py \
  --topology-families barabasi_albert,waxman \
  --node-scales 12,24,36,48 \
  --controller-budgets 3,4,5 \
  --trials 20 \
  --seed 42 \
  --output-dir results/experiment_data/seed_42_trial20_verification

# Compare outputs (expect bit-identical CSVs)
diff results/experiment_data/seed_42_trial20/*.csv \
     results/experiment_data/seed_42_trial20_verification/*.csv
# Expected output: no differences (diff returns exit code 0)
```

### Data Retention & Archival

- **Raw trial data**: Retained in `results/experiment_data/*.csv` (retained for proposal tenure, for audit, and for potential future meta-analysis).
- **Analysis scripts**: Version-controlled in [evaluation/](evaluation) and [scripts/](scripts) directories; git history preserves all analysis iterations.
- **Intermediate outputs** (plots, logs): Retained in [results/](results) subdirectories corresponding to experiment run date/ID.
- **Long-term archival**: Upon thesis submission, raw data and scripts archived to institutional repository (per UNIZULU data-retention policy); accessible for 3+ years for verification.

### Data Issues Encountered log

Log any data quality issues encountered during collection and how they were resolved:

| Date | Issue | Impact | Resolution | Status |
|------|-------|--------|-----------|--------|
| TBD | (to be populated during collection) | | | |

---

## Common Issues

### ModuleNotFoundError: No module named 'networkx' (or other dependency)

**Solution**: Activate the virtual environment:

```bash
.venv\Scripts\activate   # Windows
source .venv/bin/activate   # Linux/Mac
```

### ModuleNotFoundError: No module named 'evaluation'

**Solution**: Run from project root or use one of the methods above to add project root to PYTHONPATH.

### ImportError: cannot import name 'ClassName'

**Solution**: Check that the class/function actually exists in the module. Use entry scripts that import only what's implemented.
