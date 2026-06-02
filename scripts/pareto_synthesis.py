#!/usr/bin/env python3
"""
Pareto Front Synthesis for Phase 5/6 Bridge

Reads benchmark data, computes non-dominated set over minimization objectives:
  1) Latency L(P)
  2) Failure Disconnection = 1 - Reach_avg
  3) Complexity omega

Outputs:
  - Pareto-marked CSV
  - pareto_shortlist.json (Phase 6 Mininet replay candidates)
  - Static 3D PNG (matplotlib)
  - Interactive 3D HTML (plotly)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_records(input_path: Path) -> pd.DataFrame:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if input_path.suffix.lower() == ".csv":
        return pd.read_csv(input_path)

    if input_path.suffix.lower() in {".json", ".jsonl"}:
        if input_path.suffix.lower() == ".jsonl":
            records = [json.loads(line) for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]
            return pd.DataFrame(records)

        payload = json.loads(input_path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return pd.DataFrame(payload)
        if isinstance(payload, dict) and "records" in payload:
            return pd.DataFrame(payload["records"])
        raise ValueError("Unsupported JSON structure. Use list[dict] or {'records': [...]}.")

    raise ValueError("Unsupported input format. Use CSV, JSON, or JSONL.")


def non_dominated_mask(objectives: np.ndarray) -> np.ndarray:
    """
    Vectorized non-dominated sorting mask for minimization objectives.

    A point i is dominated if there exists j such that:
      objectives[j] <= objectives[i] in all dimensions
      and objectives[j] < objectives[i] in at least one dimension.
    """
    if objectives.ndim != 2:
        raise ValueError("Objectives must be a 2D array")

    less_equal = objectives[None, :, :] <= objectives[:, None, :]
    strictly_less = objectives[None, :, :] < objectives[:, None, :]
    domination_matrix = np.all(less_equal, axis=2) & np.any(strictly_less, axis=2)
    dominated = np.any(domination_matrix, axis=1)
    return ~dominated


def plot_static_3d(df: pd.DataFrame, output_path: Path) -> None:
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    dominated_df = df[~df["pareto_non_dominated"]]
    pareto_df = df[df["pareto_non_dominated"]]

    ax.scatter(
        dominated_df["latency_obj"],
        dominated_df["disconnection_obj"],
        dominated_df["omega_obj"],
        c="#b0b0b0",
        alpha=0.55,
        label="Dominated",
        s=28,
    )
    ax.scatter(
        pareto_df["latency_obj"],
        pareto_df["disconnection_obj"],
        pareto_df["omega_obj"],
        c="#d62728",
        alpha=0.95,
        label="Pareto",
        s=42,
    )

    ax.set_xlabel("Latency L(P)")
    ax.set_ylabel("Disconnection (1 - Reach_avg)")
    ax.set_zlabel("Complexity omega")
    ax.set_title("Pareto Frontier: Latency vs Disconnection vs Complexity")
    ax.legend(loc="upper right")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def plot_interactive_3d(df: pd.DataFrame, output_path: Path) -> None:
    try:
        import plotly.express as px
    except Exception as exc:  # pragma: no cover - optional dependency at runtime
        raise RuntimeError("Plotly is required for interactive visualization. Install plotly>=5.") from exc

    fig = px.scatter_3d(
        df,
        x="latency_obj",
        y="disconnection_obj",
        z="omega_obj",
        color="pareto_non_dominated",
        hover_data=[col for col in ["algorithm", "controllers", "trial"] if col in df.columns],
        title="Interactive Pareto Frontier",
        color_discrete_map={True: "#d62728", False: "#9a9a9a"},
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_path), include_plotlyjs="cdn")


def build_shortlist(df: pd.DataFrame, top_k: int) -> list[dict[str, Any]]:
    pareto_df = df[df["pareto_non_dominated"]].copy()
    sort_cols = ["latency_obj", "disconnection_obj", "omega_obj"]
    pareto_df = pareto_df.sort_values(sort_cols).head(top_k)

    shortlist_cols = [
        "algorithm",
        "controllers",
        "trial",
        "latency_obj",
        "disconnection_obj",
        "omega_obj",
        "average_distance",
        "control_plane_reliability",
        "runtime_ms",
    ]
    available_cols = [col for col in shortlist_cols if col in pareto_df.columns]
    return pareto_df[available_cols].to_dict(orient="records")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pareto synthesis over latency/reliability/runtime objectives")
    parser.add_argument(
        "--input",
        type=str,
        default=str(PROJECT_ROOT / "results" / "experiment_data" / "benchmark_latest.csv"),
        help="Input CSV/JSON/JSONL benchmark data",
    )
    parser.add_argument("--latency-col", type=str, default="average_distance")
    parser.add_argument("--reach-col", type=str, default="control_plane_reliability")
    parser.add_argument("--omega-col", type=str, default="runtime_ms")
    parser.add_argument("--top-k", type=int, default=10, help="Number of Pareto candidates for Phase 6 shortlist")
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(PROJECT_ROOT / "results" / "rl_analysis" / "pareto"),
        help="Output folder",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_records(input_path)

    required_cols = [args.latency_col, args.reach_col, args.omega_col]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in input data: {missing}")

    df = df.copy()
    df["latency_obj"] = pd.to_numeric(df[args.latency_col], errors="coerce")
    df["disconnection_obj"] = 1.0 - pd.to_numeric(df[args.reach_col], errors="coerce")
    df["omega_obj"] = pd.to_numeric(df[args.omega_col], errors="coerce")

    df = df.dropna(subset=["latency_obj", "disconnection_obj", "omega_obj"]).reset_index(drop=True)
    objectives = df[["latency_obj", "disconnection_obj", "omega_obj"]].to_numpy(dtype=np.float64)

    mask = non_dominated_mask(objectives)
    df["pareto_non_dominated"] = mask

    marked_csv = output_dir / "pareto_marked.csv"
    static_png = output_dir / "pareto_frontier_static.png"
    interactive_html = output_dir / "pareto_frontier_interactive.html"
    shortlist_json = output_dir / "pareto_shortlist.json"

    df.to_csv(marked_csv, index=False)
    plot_static_3d(df, static_png)
    plot_interactive_3d(df, interactive_html)

    shortlist = build_shortlist(df, top_k=args.top_k)
    shortlist_json.write_text(json.dumps(shortlist, indent=2), encoding="utf-8")

    print("Pareto synthesis complete.")
    print(f"Marked CSV: {marked_csv}")
    print(f"Static plot: {static_png}")
    print(f"Interactive plot: {interactive_html}")
    print(f"Shortlist JSON: {shortlist_json}")
    print(f"Non-dominated count: {int(mask.sum())} / {len(mask)}")


if __name__ == "__main__":
    main()
