from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re
import sys
from typing import Any

import matplotlib.pyplot as plt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot RL training trace from JSONL logs")
    parser.add_argument(
        "--input",
        type=str,
        default="logs/rl_training.jsonl",
        help="Path to RL JSONL log file",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="results/graphs",
        help="Directory for generated plot and CSV",
    )
    parser.add_argument(
        "--run-id",
        type=str,
        default=None,
        help="Optional run_id to plot; defaults to the latest run in the file",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default="rl_training",
        help="Filename prefix for generated outputs",
    )
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        parent = path.parent if str(path.parent) else Path(".")
        candidates = sorted(parent.glob("*.jsonl")) if parent.exists() else []
        candidate_text = "\n".join(f"- {candidate}" for candidate in candidates[:10])
        if not candidate_text:
            candidate_text = "- (no .jsonl files found)"

        message = (
            f"Log file not found: {path}\n"
            "Generate RL logs first by running an experiment, for example:\n"
            "  python experiments/experiment_runner.py --config configs/experiment_config.json --trials 1\n"
            "Then rerun this script, or pass --input with an existing file.\n"
            f"Available .jsonl files in {parent}:\n"
            f"{candidate_text}"
        )
        raise FileNotFoundError(message)

    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        records.append(json.loads(line))
    return records


def choose_run_id(records: list[dict[str, Any]], explicit_run_id: str | None) -> str:
    run_ids = [record.get("run_id") for record in records if record.get("run_id")]
    if not run_ids:
        raise ValueError("No run_id values found in log file")

    if explicit_run_id:
        if explicit_run_id not in set(run_ids):
            raise ValueError(f"run_id not found in log file: {explicit_run_id}")
        return explicit_run_id

    # Pick the most recent run_start record if present, else the last run_id in file order.
    for record in reversed(records):
        if record.get("event") == "run_start" and record.get("run_id"):
            return str(record["run_id"])

    return str(run_ids[-1])


def sanitize_filename_part(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


def plot_episode_metrics(episode_records: list[dict[str, Any]], output_path: Path) -> None:
    episodes = [int(record["episode"]) for record in episode_records]
    rewards = [float(record["reward"]) for record in episode_records]
    best_rewards = [float(record["best_reward"]) for record in episode_records]
    epsilons = [float(record["epsilon"]) for record in episode_records]

    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    axes[0].plot(episodes, rewards, marker="o", linewidth=1.2, label="Reward")
    axes[0].plot(episodes, best_rewards, marker="s", linewidth=1.2, label="Best Reward")
    axes[0].set_ylabel("Reward")
    axes[0].set_title("Bandit RL Reward Trajectory")
    axes[0].grid(alpha=0.3, linestyle="--")
    axes[0].legend()

    axes[1].plot(episodes, epsilons, marker="o", color="#E76F51", linewidth=1.2)
    axes[1].set_xlabel("Episode")
    axes[1].set_ylabel("Epsilon")
    axes[1].set_title("Exploration Decay")
    axes[1].grid(alpha=0.3, linestyle="--")

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def write_episode_csv(episode_records: list[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "episode",
            "reward",
            "best_reward",
            "epsilon",
            "selected_action_q",
            "selected_action_visits",
            "selected_action",
        ])
        for record in episode_records:
            writer.writerow([
                record.get("episode"),
                record.get("reward"),
                record.get("best_reward"),
                record.get("epsilon"),
                record.get("selected_action_q"),
                record.get("selected_action_visits"),
                json.dumps(record.get("selected_action")),
            ])


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    try:
        records = load_jsonl(input_path)
        run_id = choose_run_id(records, args.run_id)

        episode_records = [
            record
            for record in records
            if record.get("run_id") == run_id and record.get("event") == "episode"
        ]
        episode_records.sort(key=lambda record: int(record["episode"]))

        if not episode_records:
            raise ValueError(f"No episode records found for run_id={run_id}")

        safe_run_id = sanitize_filename_part(run_id)
        plot_path = output_dir / f"{args.prefix}_{safe_run_id}.png"
        csv_path = output_dir / f"{args.prefix}_{safe_run_id}.csv"

        plot_episode_metrics(episode_records, plot_path)
        write_episode_csv(episode_records, csv_path)

        print(f"Plotted run_id: {run_id}")
        print(f"Saved plot: {plot_path}")
        print(f"Saved episode CSV: {csv_path}")
        return 0
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
