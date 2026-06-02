#!/usr/bin/env python3
"""Run the phase workflow end-to-end.

This wrapper executes the stability audit first, then runs Pareto synthesis on
a user-supplied benchmark CSV/JSON/JSONL file. It is designed to be run
from the project virtual environment:

    python3 scripts/run_full_workflow.py

The script uses the current Python interpreter for both child steps so it
inherits the active venv automatically.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


def _run_step(command: list[str], label: str) -> None:
    print(f"\n[{label}] {' '.join(command)}")
    subprocess.run(command, cwd=PROJECT_ROOT, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the stability audit and Pareto synthesis workflow")
    parser.add_argument(
        "--episodes",
        type=int,
        default=1000,
        help="Episode count forwarded to the stability audit script",
    )
    parser.add_argument(
        "--benchmark-input",
        type=str,
        default="",
        help="Benchmark CSV/JSON/JSONL input for Pareto synthesis. Required unless --skip-pareto is set.",
    )
    parser.add_argument(
        "--omega-col",
        type=str,
        default="controller_load_std",
        help="Column used as the omega objective in Pareto synthesis",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=10,
        help="Number of Pareto shortlist entries to keep",
    )
    parser.add_argument(
        "--skip-stability-audit",
        action="store_true",
        help="Skip the stability audit step",
    )
    parser.add_argument(
        "--skip-pareto",
        action="store_true",
        help="Skip the Pareto synthesis step",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.skip_stability_audit and args.skip_pareto:
        print("Nothing to do: both workflow steps are disabled.", file=sys.stderr)
        return 2

    if not args.skip_pareto and not args.benchmark_input.strip():
        print(
            "--benchmark-input is required unless --skip-pareto is set.",
            file=sys.stderr,
        )
        return 2

    if not args.skip_stability_audit:
        stability_cmd = [sys.executable, str(SCRIPTS_DIR / "run_stability_audit.py"), "--episodes", str(args.episodes)]
        _run_step(stability_cmd, "stability-audit")

    if not args.skip_pareto:
        benchmark_input = Path(args.benchmark_input)
        pareto_cmd = [
            sys.executable,
            str(SCRIPTS_DIR / "pareto_synthesis.py"),
            "--input",
            str(benchmark_input),
            "--omega-col",
            args.omega_col,
            "--top-k",
            str(args.top_k),
        ]
        _run_step(pareto_cmd, "pareto-synthesis")

    print("\nWorkflow complete.")
    if not args.skip_pareto:
        print(f"Pareto outputs: {PROJECT_ROOT / 'results' / 'rl_analysis' / 'pareto'}")
    if not args.skip_stability_audit:
        print(f"Stability outputs: {PROJECT_ROOT / 'results' / 'rl_analysis' / 'stability_audit'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())