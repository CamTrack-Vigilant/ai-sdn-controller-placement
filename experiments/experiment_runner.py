from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import logging
import platform
from pathlib import Path
import subprocess
import sys
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from evaluation.performance_analysis import (  # noqa: E402
    default_algorithm_suite,
    plot_metric_comparison,
    run_algorithm_benchmark,
)
from topology.network_topology import TopologyConfig, generate_multi_site_topology, summarize_topology  # noqa: E402


DEFAULT_CONFIG: dict[str, Any] = {
    "topology": {
        "num_sites": 4,
        "nodes_per_site": 12,
        "intra_site_degree": 4,
        "rewiring_prob": 0.2,
        "inter_site_links": 2,
        "seed": 42,
    },
    "experiment": {
        "num_controllers": 3,
        "trials": 5,
        "seed": 42,
        "metrics_to_plot": [
            "average_distance",
            "worst_case_distance",
            "controller_load_std",
            "resilience_ratio",
            "control_plane_reliability",
        ],
    },
    "outputs": {
        "data_dir": "results/experiment_data",
        "graph_dir": "results/graphs",
        "logs_dir": "logs",
    },
    "rl_logging": {
        "enabled": True,
        "file_name": "rl_training.jsonl",
        "log_every": 25,
    },
    "rl_objective": {
        "latency_weight": 1.0,
        "reliability_weight": 0.25,
        "seconds_per_episode_weight": 0.25,
    },
}


def _deep_merge(base: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    suffix = config_path.suffix.lower()
    if suffix == ".json":
        return json.loads(config_path.read_text(encoding="utf-8"))

    if suffix in {".yaml", ".yml"}:
        try:
            import yaml
        except Exception as exc:  # pragma: no cover - optional dependency
            raise RuntimeError(
                "YAML config requested but PyYAML is not installed. "
                "Install it with: pip install pyyaml"
            ) from exc
        return yaml.safe_load(config_path.read_text(encoding="utf-8"))

    raise ValueError("Unsupported config format. Use .json, .yaml, or .yml")


def setup_logging(logs_dir: Path, level: str, log_file: str | None = None) -> Path:
    logs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = Path(log_file) if log_file else logs_dir / f"experiment_runner_{timestamp}.log"

    handlers = [
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ]
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=handlers,
        force=True,
    )
    return log_path


def _compute_config_hash(config: dict[str, Any]) -> str:
    canonical = json.dumps(config, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _resolve_git_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        value = result.stdout.strip()
        return value or None
    except Exception:
        return None


def enforce_decision_grade_trials(*, trials: int, strict_enabled: bool) -> tuple[bool, str]:
    if not strict_enabled:
        return True, "Strict enforcement disabled (non-decision-grade mode)."

    if trials <= 0:
        return False, "Strict mode requires a positive trial count."

    if trials % 30 != 0:
        return (
            False,
            (
                f"Strict decision-grade mode requires trials to be a multiple of 30. "
                f"Received trials={trials}. Use --trials 30 (or 60/90/...) or disable strict mode."
            ),
        )

    return True, f"Strict decision-grade enforcement passed for trials={trials}."


def write_manifest(
    *,
    data_dir: Path,
    timestamp: str,
    run_id: str,
    run_mode: str,
    config: dict[str, Any],
    random_seed: int,
    trials: int,
    strict_decision_grade_enabled: bool,
    strict_enforcement_passed: bool,
    strict_enforcement_reason: str,
) -> Path:
    data_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "run_id": run_id,
        "run_mode": run_mode,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python_version": platform.python_version(),
        "system_os": f"{platform.system()} {platform.release()}",
        "git_commit_hash": _resolve_git_commit(),
        "random_seed": int(random_seed),
        "config_hash": _compute_config_hash(config),
        "suite_runs": int(trials),
        "suite_size_target": 30,
        "completed_30_run_suites": int(trials) // 30,
        "strict_decision_grade": {
            "enabled": bool(strict_decision_grade_enabled),
            "passed": bool(strict_enforcement_passed),
            "reason": strict_enforcement_reason,
        },
        "config": config,
    }

    latest_manifest_path = data_dir / "manifest.json"
    latest_manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    timestamped_manifest_path = data_dir / f"manifest_{timestamp}.json"
    timestamped_manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    return latest_manifest_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run SDN controller placement benchmark experiments")
    parser.add_argument(
        "--config",
        type=str,
        default=str(PROJECT_ROOT / "configs" / "experiment_config.json"),
        help="Path to .json/.yaml experiment config",
    )
    parser.add_argument("--sites", type=int, default=None, help="Override number of sites")
    parser.add_argument("--nodes-per-site", type=int, default=None, help="Override nodes per site")
    parser.add_argument("--controllers", type=int, default=None, help="Override controllers to place")
    parser.add_argument("--trials", type=int, default=None, help="Override benchmark trials")
    parser.add_argument("--seed", type=int, default=None, help="Override random seed")
    parser.add_argument(
        "--metrics",
        type=str,
        default=None,
        help="Comma-separated metric names to plot",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="Logging level (DEBUG, INFO, WARNING, ERROR)",
    )
    parser.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="Optional explicit log file path",
    )
    parser.add_argument(
        "--strict-decision-grade",
        action="store_true",
        help=(
            "Enable decision-grade enforcement. When enabled, trials must be a positive multiple "
            "of 30 or execution fails fast."
        ),
    )
    return parser.parse_args()


def resolve_config(args: argparse.Namespace) -> dict[str, Any]:
    config = copy.deepcopy(DEFAULT_CONFIG)

    if args.config:
        file_config = load_config(Path(args.config))
        if file_config:
            config = _deep_merge(config, file_config)

    if args.sites is not None:
        config["topology"]["num_sites"] = args.sites
    if args.nodes_per_site is not None:
        config["topology"]["nodes_per_site"] = args.nodes_per_site
    if args.controllers is not None:
        config["experiment"]["num_controllers"] = args.controllers
    if args.trials is not None:
        config["experiment"]["trials"] = args.trials
    if args.seed is not None:
        config["experiment"]["seed"] = args.seed
        config["topology"]["seed"] = args.seed

    if args.metrics is not None:
        parsed_metrics = [metric.strip() for metric in args.metrics.split(",") if metric.strip()]
        if parsed_metrics:
            config["experiment"]["metrics_to_plot"] = parsed_metrics

    return config


def main() -> None:
    args = parse_args()
    config = resolve_config(args)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    logs_dir = PROJECT_ROOT / config["outputs"]["logs_dir"]
    log_path = setup_logging(logs_dir=logs_dir, level=args.log_level, log_file=args.log_file)
    logger = logging.getLogger(__name__)

    logger.info("Loaded experiment config: %s", json.dumps(config, indent=2))
    logger.info("Writing run log to: %s", log_path)

    topology_cfg = TopologyConfig(**config["topology"])
    experiment_cfg = config["experiment"]
    outputs_cfg = config["outputs"]
    rl_logging_cfg = config.get("rl_logging", {})
    rl_objective_cfg = config.get("rl_objective", {})

    strict_passed, strict_reason = enforce_decision_grade_trials(
        trials=int(experiment_cfg["trials"]),
        strict_enabled=bool(args.strict_decision_grade),
    )
    if not strict_passed:
        logger.error("Strict decision-grade enforcement failed: %s", strict_reason)
        raise ValueError(strict_reason)

    run_id = f"benchmark_{timestamp}"
    run_mode = "decision_grade" if bool(args.strict_decision_grade) else "non_decision_grade"
    logger.info("Run mode: %s", run_mode)
    logger.info("Strict decision-grade enforcement: %s", strict_reason)

    latency_weight = float(rl_objective_cfg.get("latency_weight", 1.0))
    reliability_weight = float(rl_objective_cfg.get("reliability_weight", 0.0))

    bandit_kwargs: dict[str, Any] = {
        "latency_weight": latency_weight,
        "reliability_weight": reliability_weight,
    }

    if bool(rl_logging_cfg.get("enabled", True)):
        rl_file_name = str(rl_logging_cfg.get("file_name", "rl_training.jsonl"))
        rl_log_path = Path(rl_file_name)
        if not rl_log_path.is_absolute():
            rl_log_path = logs_dir / rl_log_path

        bandit_kwargs.update({
            "log_path": str(rl_log_path),
            "log_every": int(rl_logging_cfg.get("log_every", 25)),
            "run_label": run_id,
        })
        logger.info("Bandit RL training logs: %s", rl_log_path)
        logger.info(
            "Bandit RL objective weights: latency=%s reliability=%s",
            latency_weight,
            reliability_weight,
        )
    else:
        logger.info(
            "Bandit RL objective weights: latency=%s reliability=%s (logging disabled)",
            latency_weight,
            reliability_weight,
        )

    topology = generate_multi_site_topology(topology_cfg)
    summary_stats = summarize_topology(topology)
    logger.info("Topology summary: %s", summary_stats)

    print("Topology summary:", summary_stats)

    benchmark_df = run_algorithm_benchmark(
        graph=topology,
        num_controllers=int(experiment_cfg["num_controllers"]),
        algorithms=default_algorithm_suite(bandit_kwargs=bandit_kwargs),
        trials=int(experiment_cfg["trials"]),
        seed=int(experiment_cfg["seed"]),
    )

    data_dir = PROJECT_ROOT / outputs_cfg["data_dir"]
    graph_dir = PROJECT_ROOT / outputs_cfg["graph_dir"]
    data_dir.mkdir(parents=True, exist_ok=True)
    graph_dir.mkdir(parents=True, exist_ok=True)

    csv_path = data_dir / f"benchmark_{timestamp}.csv"
    benchmark_df.to_csv(csv_path, index=False)

    manifest_path = write_manifest(
        data_dir=data_dir,
        timestamp=timestamp,
        run_id=run_id,
        run_mode=run_mode,
        config=config,
        random_seed=int(experiment_cfg["seed"]),
        trials=int(experiment_cfg["trials"]),
        strict_decision_grade_enabled=bool(args.strict_decision_grade),
        strict_enforcement_passed=strict_passed,
        strict_enforcement_reason=strict_reason,
    )

    metrics_to_plot = list(experiment_cfg["metrics_to_plot"])

    for metric in metrics_to_plot:
        output_path = graph_dir / f"{metric}_{timestamp}.png"
        plot_metric_comparison(benchmark_df, metric, output_path)

    summary = benchmark_df.groupby("algorithm")[metrics_to_plot].mean()
    sort_metric = "average_distance" if "average_distance" in summary.columns else metrics_to_plot[0]
    summary = summary.sort_values(sort_metric)

    print("\nAverage metrics by algorithm:")
    print(summary.to_string(float_format=lambda value: f"{value:.4f}"))
    print(f"\nSaved benchmark CSV: {csv_path}")
    print(f"Saved manifest JSON: {manifest_path}")
    print(f"Saved plots directory: {graph_dir}")
    print(f"Saved log file: {log_path}")

    logger.info("Saved benchmark CSV: %s", csv_path)
    logger.info("Saved manifest JSON: %s", manifest_path)
    logger.info("Saved plots directory: %s", graph_dir)
    logger.info("Average metrics by algorithm:\n%s", summary.to_string(float_format=lambda value: f"{value:.4f}"))


if __name__ == "__main__":
    main()
