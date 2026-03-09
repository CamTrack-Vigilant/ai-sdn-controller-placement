# Experiment Configs

Use `experiment_config.json` to set topology, experiment, and output parameters.

Run with:

```bash
python experiments/experiment_runner.py --config configs/experiment_config.json
```

Optional CLI overrides still work, for example:

```bash
python experiments/experiment_runner.py --config configs/experiment_config.json --controllers 4 --trials 10
```
