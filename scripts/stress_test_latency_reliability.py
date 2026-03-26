from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import pandas as pd

from evaluation.pareto import (
    mark_latency_reliability_pareto,
    rank_latency_reliability_compromise,
    select_best_latency_reliability_compromise,
)
from evaluation.performance_analysis import default_algorithm_suite, run_algorithm_benchmark
from topology.network_topology import TopologyConfig, generate_multi_site_topology


def parse_int_list(raw: str) -> list[int]:
    values = [int(chunk.strip()) for chunk in raw.split(",") if chunk.strip()]
    if not values:
        raise ValueError("Expected at least one integer in list")
    return values


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run latency vs reliability stress tests across topology/controller matrices"
    )
    parser.add_argument("--sites", type=str, default="2,3,4", help="Comma-separated site counts")
    parser.add_argument(
        "--controllers",
        type=str,
        default="2,3,5",
        help="Comma-separated controller counts",
    )
    parser.add_argument("--nodes-per-site", type=int, default=12)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--base-seed", type=int, default=42)
    parser.add_argument("--data-dir", type=str, default="results/experiment_data")
    parser.add_argument("--graph-dir", type=str, default="results/graphs")
    parser.add_argument("--rl-latency-weight", type=float, default=1.0)
    parser.add_argument("--rl-reliability-weight", type=float, default=0.25)
    return parser.parse_args()


def plot_scatter(
    aggregated_df: pd.DataFrame,
    output_path: Path,
    pareto_df: pd.DataFrame | None = None,
    best_compromise_df: pd.DataFrame | None = None,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 6))

    for algorithm, group in aggregated_df.groupby("algorithm"):
        ax.scatter(
            group["average_distance"],
            group["control_plane_reliability"],
            label=algorithm,
            alpha=0.85,
            s=55,
        )

    if pareto_df is not None and not pareto_df.empty:
        ax.scatter(
            pareto_df["average_distance"],
            pareto_df["control_plane_reliability"],
            marker="*",
            s=160,
            color="black",
            alpha=0.9,
            label="Pareto frontier",
        )

    if best_compromise_df is not None and not best_compromise_df.empty:
        ax.scatter(
            best_compromise_df["average_distance"],
            best_compromise_df["control_plane_reliability"],
            marker="X",
            s=170,
            color="#D62828",
            alpha=0.95,
            label="Best compromise",
        )

    ax.set_xlabel("Average Distance (lower is better)")
    ax.set_ylabel("Control Plane Reliability (higher is better)")
    ax.set_title("Latency vs Reliability Stress Test")
    ax.grid(alpha=0.35, linestyle="--")
    ax.legend(title="Algorithm")

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def build_correlation_table(aggregated_df: pd.DataFrame) -> pd.DataFrame:
    def safe_corr(frame: pd.DataFrame, x_col: str, y_col: str) -> float:
        x = frame[x_col]
        y = frame[y_col]
        if len(frame) < 2 or x.nunique(dropna=True) < 2 or y.nunique(dropna=True) < 2:
            return float("nan")
        return float(x.corr(y))

    rows: list[dict[str, float | str | int]] = []

    overall_latency_reliability_corr = safe_corr(
        aggregated_df,
        "average_distance",
        "control_plane_reliability",
    )
    overall_latency_runtime_corr = safe_corr(
        aggregated_df,
        "average_distance",
        "runtime_ms",
    )
    overall_reliability_runtime_corr = safe_corr(
        aggregated_df,
        "control_plane_reliability",
        "runtime_ms",
    )

    rows.append(
        {
            "algorithm": "__overall__",
            "points": int(len(aggregated_df)),
            "pearson_corr_latency_vs_reliability": float(overall_latency_reliability_corr),
            "pearson_corr_latency_vs_runtime": float(overall_latency_runtime_corr),
            "pearson_corr_reliability_vs_runtime": float(overall_reliability_runtime_corr),
        }
    )

    for algorithm, group in aggregated_df.groupby("algorithm"):
        latency_reliability_corr = safe_corr(group, "average_distance", "control_plane_reliability")
        latency_runtime_corr = safe_corr(group, "average_distance", "runtime_ms")
        reliability_runtime_corr = safe_corr(group, "control_plane_reliability", "runtime_ms")
        rows.append(
            {
                "algorithm": algorithm,
                "points": int(len(group)),
                "pearson_corr_latency_vs_reliability": float(latency_reliability_corr),
                "pearson_corr_latency_vs_runtime": float(latency_runtime_corr),
                "pearson_corr_reliability_vs_runtime": float(reliability_runtime_corr),
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()

    sites = parse_int_list(args.sites)
    controllers = parse_int_list(args.controllers)

    data_dir = PROJECT_ROOT / args.data_dir
    graph_dir = PROJECT_ROOT / args.graph_dir
    data_dir.mkdir(parents=True, exist_ok=True)
    graph_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    raw_frames: list[pd.DataFrame] = []
    scenario_index = 0

    bandit_kwargs = {
        "latency_weight": float(args.rl_latency_weight),
        "reliability_weight": float(args.rl_reliability_weight),
    }

    for num_sites in sites:
        for num_controllers in controllers:
            scenario_index += 1
            topology_seed = args.base_seed + scenario_index * 997
            trial_seed = args.base_seed + scenario_index * 53
            scenario_name = f"sites{num_sites}_k{num_controllers}"

            topology = generate_multi_site_topology(
                TopologyConfig(
                    num_sites=num_sites,
                    nodes_per_site=args.nodes_per_site,
                    seed=topology_seed,
                )
            )

            benchmark_df = run_algorithm_benchmark(
                graph=topology,
                num_controllers=num_controllers,
                algorithms=default_algorithm_suite(bandit_kwargs=bandit_kwargs),
                trials=args.trials,
                seed=trial_seed,
            )
            benchmark_df["scenario"] = scenario_name
            benchmark_df["num_sites"] = num_sites
            benchmark_df["nodes_per_site"] = args.nodes_per_site
            benchmark_df["num_controllers"] = num_controllers
            benchmark_df["topology_seed"] = topology_seed
            benchmark_df["trial_seed"] = trial_seed
            raw_frames.append(benchmark_df)

    raw_df = pd.concat(raw_frames, ignore_index=True)

    aggregated_df = (
        raw_df.groupby(["scenario", "num_sites", "num_controllers", "algorithm"], as_index=False)[
            [
                "average_distance",
                "control_plane_reliability",
                "resilience_ratio",
                "worst_case_distance",
                "controller_load_std",
                "runtime_ms",
                "iterations_budget",
                "iterations_to_converge",
            ]
        ]
        .mean()
        .sort_values(["scenario", "average_distance", "control_plane_reliability"])
    )

    aggregated_df = mark_latency_reliability_pareto(
        aggregated_df,
        group_cols=["scenario"],
        latency_col="average_distance",
        reliability_col="control_plane_reliability",
    )
    pareto_df = (
        aggregated_df[aggregated_df["is_pareto_optimal"]]
        .copy()
        .sort_values(["scenario", "average_distance", "control_plane_reliability"])
    )
    pareto_ranked_df = rank_latency_reliability_compromise(
        pareto_df,
        group_cols=["scenario"],
        latency_col="average_distance",
        reliability_col="control_plane_reliability",
    )
    best_compromise_df = select_best_latency_reliability_compromise(
        pareto_df,
        group_cols=["scenario"],
        latency_col="average_distance",
        reliability_col="control_plane_reliability",
    )

    correlation_df = build_correlation_table(aggregated_df)

    raw_csv_path = data_dir / f"stress_test_raw_{timestamp}.csv"
    agg_csv_path = data_dir / f"stress_test_summary_{timestamp}.csv"
    pareto_csv_path = data_dir / f"stress_test_pareto_{timestamp}.csv"
    pareto_ranked_csv_path = data_dir / f"stress_test_pareto_ranked_{timestamp}.csv"
    best_compromise_csv_path = data_dir / f"stress_test_best_compromise_{timestamp}.csv"
    corr_csv_path = data_dir / f"stress_test_correlation_{timestamp}.csv"
    scatter_path = graph_dir / f"latency_vs_reliability_{timestamp}.png"

    raw_df.to_csv(raw_csv_path, index=False)
    aggregated_df.to_csv(agg_csv_path, index=False)
    pareto_df.to_csv(pareto_csv_path, index=False)
    pareto_ranked_df.to_csv(pareto_ranked_csv_path, index=False)
    best_compromise_df.to_csv(best_compromise_csv_path, index=False)
    correlation_df.to_csv(corr_csv_path, index=False)
    plot_scatter(
        aggregated_df,
        scatter_path,
        pareto_df=pareto_df,
        best_compromise_df=best_compromise_df,
    )

    overall_latency_reliability_corr = float(
        correlation_df.loc[
            correlation_df["algorithm"] == "__overall__",
            "pearson_corr_latency_vs_reliability",
        ].iloc[0]
    )
    overall_latency_runtime_corr = float(
        correlation_df.loc[
            correlation_df["algorithm"] == "__overall__",
            "pearson_corr_latency_vs_runtime",
        ].iloc[0]
    )
    overall_reliability_runtime_corr = float(
        correlation_df.loc[
            correlation_df["algorithm"] == "__overall__",
            "pearson_corr_reliability_vs_runtime",
        ].iloc[0]
    )

    print(f"Scenarios run: {len(sites) * len(controllers)}")
    print(f"Raw results CSV: {raw_csv_path}")
    print(f"Summary CSV: {agg_csv_path}")
    print(f"Pareto CSV: {pareto_csv_path}")
    print(f"Pareto ranked CSV: {pareto_ranked_csv_path}")
    print(f"Best compromise CSV: {best_compromise_csv_path}")
    print(f"Correlation CSV: {corr_csv_path}")
    print(f"Scatter plot: {scatter_path}")
    print(f"Pareto points: {len(pareto_df)}")
    print(f"Best-compromise points: {len(best_compromise_df)}")
    print(f"Overall latency/reliability Pearson correlation: {overall_latency_reliability_corr:.4f}")
    print(f"Overall latency/runtime Pearson correlation: {overall_latency_runtime_corr:.4f}")
    print(f"Overall reliability/runtime Pearson correlation: {overall_reliability_runtime_corr:.4f}")


if __name__ == "__main__":
    main()
