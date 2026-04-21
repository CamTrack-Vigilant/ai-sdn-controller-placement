#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(
        description=(
            "Push-button Linux/WSL2 benchmark entrypoint: runs environment preflight "
            "then launches experiment_runner with forwarded arguments."
        )
    )
    parser.add_argument(
        "--skip-preflight",
        action="store_true",
        help="Skip env_check.py (not recommended for decision-grade runs).",
    )
    args, remaining = parser.parse_known_args()
    return args, remaining


def run_preflight() -> None:
    preflight_cmd = [sys.executable, str(PROJECT_ROOT / "env_check.py")]
    result = subprocess.run(preflight_cmd, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        raise SystemExit(
            "Preflight failed. Fix env_check findings (Linux + Mininet + Ryu + PyYAML) before running decision-grade benchmarks."
        )


def run_benchmark(forwarded_args: list[str]) -> int:
    cmd = [sys.executable, str(PROJECT_ROOT / "experiments" / "experiment_runner.py"), *forwarded_args]
    return subprocess.run(cmd, cwd=PROJECT_ROOT).returncode


def main() -> int:
    args, forwarded_args = parse_args()

    if not args.skip_preflight:
        run_preflight()

    return run_benchmark(forwarded_args)


if __name__ == "__main__":
    raise SystemExit(main())
