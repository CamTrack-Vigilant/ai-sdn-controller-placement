# Running Project Modules

This guide explains how to run the different modules in this project.

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
