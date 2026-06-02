#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import mean

import matplotlib.pyplot as plt


def _to_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot baseline hardware cost (tau proxy) over time from telemetry CSV.",
    )
    parser.add_argument(
        "--telemetry-csv",
        default="results/experiment_data/baseline_telemetry_internet2.csv",
        help="Path to baseline telemetry CSV.",
    )
    parser.add_argument(
        "--output",
        default="results/graphs/baseline_tau_internet2.png",
        help="Path for generated figure.",
    )
    parser.add_argument(
        "--stability-window",
        type=int,
        default=5,
        help="Window size (samples) used to detect stabilization.",
    )
    parser.add_argument(
        "--cv-threshold",
        type=float,
        default=0.10,
        help="Coefficient of variation threshold to mark stable interval.",
    )
    return parser.parse_args()


def detect_stability(elapsed: list[float], cpu: list[float], rss: list[float], window: int, cv_threshold: float) -> float | None:
    if len(elapsed) < window:
        return None

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
            return elapsed[i - window + 1]

    return None


def main() -> int:
    args = parse_args()
    telemetry_path = Path(args.telemetry_csv)
    output_path = Path(args.output)

    if not telemetry_path.exists():
        raise FileNotFoundError(f"Telemetry CSV not found: {telemetry_path}")

    elapsed_s: list[float] = []
    cpu_percent: list[float] = []
    rss_mb: list[float] = []

    with telemetry_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            e = _to_float(row.get("elapsed_s", ""))
            c = _to_float(row.get("cpu_percent", ""))
            r = _to_float(row.get("rss_memory_mb", ""))
            if e is None or c is None or r is None:
                continue
            elapsed_s.append(e)
            cpu_percent.append(c)
            rss_mb.append(r)

    if not elapsed_s:
        raise RuntimeError("No numeric telemetry samples found in CSV.")

    stable_t = detect_stability(
        elapsed=elapsed_s,
        cpu=cpu_percent,
        rss=rss_mb,
        window=max(2, args.stability_window),
        cv_threshold=max(0.0, args.cv_threshold),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax1 = plt.subplots(figsize=(11, 5.5))
    ax2 = ax1.twinx()

    ax1.plot(elapsed_s, cpu_percent, color="#0B6E4F", linewidth=2, label="CPU %")
    ax2.plot(elapsed_s, rss_mb, color="#C84B31", linewidth=2, label="RSS MB")

    if stable_t is not None:
        ax1.axvline(stable_t, color="#222222", linestyle="--", linewidth=1.2, label="Stability start")

    ax1.set_title("Internet2 Baseline Controller Hardware Cost Over Time")
    ax1.set_xlabel("Elapsed Time (s)")
    ax1.set_ylabel("CPU Utilization (%)", color="#0B6E4F")
    ax2.set_ylabel("Memory RSS (MB)", color="#C84B31")
    ax1.grid(True, alpha=0.25)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)

    print(f"[INFO] Figure saved to {output_path}")
    if stable_t is not None:
        print(f"[INFO] Estimated stabilization starts at t={stable_t:.3f}s")
    else:
        print("[INFO] No stabilization point found under current thresholds")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
