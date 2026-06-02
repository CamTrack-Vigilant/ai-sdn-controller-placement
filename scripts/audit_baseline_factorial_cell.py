#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import mean
from typing import Any


def _to_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value: str) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Decision-grade audit for first baseline Internet2 run.")
    parser.add_argument("--telemetry-csv", default="results/experiment_data/baseline_telemetry_internet2.csv")
    parser.add_argument("--summary-csv", default="results/experiment_data/baseline_internet2_summary.csv")
    parser.add_argument("--full-runs", type=int, default=540, help="Total run count for projected full experiment.")
    parser.add_argument("--cell-count", type=int, default=18, help="Factorial cells count.")
    parser.add_argument("--stability-window", type=int, default=5)
    parser.add_argument("--cv-threshold", type=float, default=0.10)
    return parser.parse_args()


def _detect_stability(elapsed: list[float], cpu: list[float], rss: list[float], window: int, cv_threshold: float) -> dict[str, float | bool | None]:
    if len(elapsed) < window:
        return {
            "stable": False,
            "start_s": None,
            "cpu_cv": None,
            "rss_cv": None,
        }

    for i in range(window - 1, len(elapsed)):
        c = cpu[i - window + 1 : i + 1]
        r = rss[i - window + 1 : i + 1]
        c_mean = mean(c) if c else 0.0
        r_mean = mean(r) if r else 0.0
        c_std = (sum((x - c_mean) ** 2 for x in c) / len(c)) ** 0.5 if c else 0.0
        r_std = (sum((x - r_mean) ** 2 for x in r) / len(r)) ** 0.5 if r else 0.0
        c_cv = c_std / c_mean if c_mean > 0 else 0.0
        r_cv = r_std / r_mean if r_mean > 0 else 0.0
        if c_cv <= cv_threshold and r_cv <= cv_threshold:
            return {
                "stable": True,
                "start_s": elapsed[i - window + 1],
                "cpu_cv": c_cv,
                "rss_cv": r_cv,
            }

    return {
        "stable": False,
        "start_s": None,
        "cpu_cv": None,
        "rss_cv": None,
    }


def _read_telemetry(path: Path) -> dict[str, Any]:
    elapsed: list[float] = []
    cpu: list[float] = []
    rss: list[float] = []
    unavailable_count = 0

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if row.get("status") == "process_unavailable":
                unavailable_count += 1
            e = _to_float(row.get("elapsed_s", ""))
            c = _to_float(row.get("cpu_percent", ""))
            r = _to_float(row.get("rss_memory_mb", ""))
            if e is None or c is None or r is None:
                continue
            elapsed.append(e)
            cpu.append(c)
            rss.append(r)

    if not elapsed:
        raise RuntimeError("Telemetry CSV contains no valid numeric samples.")

    return {
        "samples": len(elapsed),
        "duration_s": max(elapsed),
        "mean_cpu": mean(cpu),
        "max_cpu": max(cpu),
        "mean_rss": mean(rss),
        "max_rss": max(rss),
        "unavailable_count": unavailable_count,
        "elapsed": elapsed,
        "cpu": cpu,
        "rss": rss,
    }


def _read_latest_summary(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    if not rows:
        raise RuntimeError("Summary CSV is empty.")
    row = rows[-1]

    return {
        "timestamp_utc": row.get("timestamp_utc", ""),
        "topology": row.get("topology", ""),
        "topology_source": row.get("topology_source", ""),
        "seed": _to_int(row.get("seed", "")),
        "k": _to_int(row.get("k", "")),
        "controller_nodes_raw": row.get("controller_nodes", ""),
        "controller_nodes": [x for x in (row.get("controller_nodes", "").split(";") if row.get("controller_nodes") else []) if x],
        "latency_l": _to_float(row.get("latency_l", "")),
        "reachability_r_avg": _to_float(row.get("reachability_r_avg", "")),
        "ping_loss_percent": _to_float(row.get("ping_loss_percent", "")),
        "tau_runtime_seconds": _to_float(row.get("tau_runtime_seconds", "")),
    }


def _quality_score(telemetry: dict[str, Any], stability: dict[str, Any], summary: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    notes: list[str] = []

    # Telemetry completeness (2 pts)
    if telemetry["samples"] >= 10 and telemetry["unavailable_count"] == 0:
        score += 2.0
    elif telemetry["samples"] >= 5:
        score += 1.0
        notes.append("Telemetry sample count is low for strong stability inference.")
    else:
        notes.append("Very few telemetry samples recorded.")

    # Stability quality (2 pts)
    if stability["stable"]:
        score += 2.0
    else:
        notes.append("No stable CPU/RSS window found under current CV threshold.")

    # Ping/reachability consistency (2 pts)
    ping = summary["ping_loss_percent"]
    r_avg = summary["reachability_r_avg"]
    if ping is not None and r_avg is not None and abs(r_avg - max(0.0, 1.0 - ping / 100.0)) < 1e-9:
        score += 2.0
    else:
        notes.append("R_avg does not match ping-loss-derived expectation from this script.")

    # Seed determinism metadata (2 pts)
    if summary["seed"] == 42 and summary["controller_nodes"] and summary["k"] is not None and len(summary["controller_nodes"]) == summary["k"]:
        score += 2.0
    else:
        notes.append("Seed/k/controller_nodes metadata is incomplete for determinism claims.")

    # Runtime/batch planning usefulness (2 pts)
    if summary["tau_runtime_seconds"] is not None and summary["tau_runtime_seconds"] > 0:
        score += 2.0
    else:
        notes.append("Missing tau runtime; cannot project full batch timing reliably.")

    return round(score, 2), notes


def main() -> int:
    args = parse_args()
    telemetry_path = Path(args.telemetry_csv)
    summary_path = Path(args.summary_csv)

    if not telemetry_path.exists() or not summary_path.exists():
        missing = []
        if not telemetry_path.exists():
            missing.append(str(telemetry_path))
        if not summary_path.exists():
            missing.append(str(summary_path))
        raise FileNotFoundError("Missing required artifact(s): " + ", ".join(missing))

    telemetry = _read_telemetry(telemetry_path)
    summary = _read_latest_summary(summary_path)
    stability = _detect_stability(
        elapsed=telemetry["elapsed"],
        cpu=telemetry["cpu"],
        rss=telemetry["rss"],
        window=max(2, args.stability_window),
        cv_threshold=max(0.0, args.cv_threshold),
    )

    quality_score, quality_notes = _quality_score(telemetry, stability, summary)

    tau = summary["tau_runtime_seconds"] or 0.0
    full_seconds = tau * args.full_runs
    full_hours = full_seconds / 3600.0
    cells_seconds = tau * args.cell_count
    cells_minutes = cells_seconds / 60.0

    print("=== Factorial Cell Audit Report ===")
    print(f"Telemetry samples: {telemetry['samples']}")
    print(f"Telemetry duration (s): {telemetry['duration_s']:.3f}")
    print(f"Mean CPU (%): {telemetry['mean_cpu']:.3f} | Max CPU (%): {telemetry['max_cpu']:.3f}")
    print(f"Mean RSS (MB): {telemetry['mean_rss']:.3f} | Max RSS (MB): {telemetry['max_rss']:.3f}")
    print(f"Process unavailable rows: {telemetry['unavailable_count']}")

    if stability["stable"]:
        print(f"Stability detected: YES at t={stability['start_s']:.3f}s (CPU CV={stability['cpu_cv']:.4f}, RSS CV={stability['rss_cv']:.4f})")
    else:
        print("Stability detected: NO under current thresholds")

    print(f"Topology: {summary['topology']} | Source: {summary['topology_source']}")
    print(f"Seed: {summary['seed']} | k: {summary['k']} | Controllers: {summary['controller_nodes_raw']}")
    print(f"Latency l: {summary['latency_l']}")
    print(f"Reachability R_avg: {summary['reachability_r_avg']} | ping_loss_percent: {summary['ping_loss_percent']}")
    print(f"Tau runtime seconds: {summary['tau_runtime_seconds']}")

    print(f"Projected full {args.full_runs}-run time: {full_hours:.2f} hours ({full_seconds:.0f} s)")
    print(f"Projected {args.cell_count}-cell single-pass time: {cells_minutes:.2f} minutes ({cells_seconds:.0f} s)")

    print(f"Data Quality Score: {quality_score}/10")
    if quality_notes:
        print("Quality Notes:")
        for note in quality_notes:
            print(f"- {note}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
