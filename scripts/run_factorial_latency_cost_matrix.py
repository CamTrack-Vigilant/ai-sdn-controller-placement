from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import sys
import time

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from algorithms.ai.genetic_algorithm import genetic_controller_placement
from algorithms.ai.reinforcement_learning import bandit_rl_controller_placement
from algorithms.baseline.greedy_placement import greedy_k_center_placement
from algorithms.baseline.kmeans_placement import kmeans_controller_placement
from algorithms.baseline.random_placement import random_controller_placement
from evaluation.metrics import average_controller_distance
from topology.synthetic_topology_models import SyntheticTopologyConfig, generate_synthetic_topology


def parse_int_list(raw: str) -> list[int]:
    values = [int(chunk.strip()) for chunk in raw.split(",") if chunk.strip()]
    if not values:
        raise ValueError("Expected at least one integer")
    return values


def parse_model_list(raw: str) -> list[str]:
    aliases = {
        "ba": "barabasi_albert",
        "barabasi": "barabasi_albert",
        "barabasi_albert": "barabasi_albert",
        "barabasi-albert": "barabasi_albert",
        "waxman": "waxman",
    }

    parsed = []
    for chunk in raw.split(","):
        candidate = chunk.strip().lower()
        if not candidate:
            continue
        if candidate not in aliases:
            raise ValueError(f"Unsupported topology model: {candidate}")
        parsed.append(aliases[candidate])

    if not parsed:
        raise ValueError("Expected at least one topology model")

    # Preserve order while removing duplicates.
    seen: set[str] = set()
    deduped = []
    for model in parsed:
        if model in seen:
            continue
        seen.add(model)
        deduped.append(model)
    return deduped


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run factorial latency-vs-compute experiments for SDN controller placement "
            "across Barabasi-Albert and Waxman synthetic topologies."
        )
    )
    parser.add_argument(
        "--topology-models",
        type=str,
        default="barabasi_albert,waxman",
        help="Comma-separated topology models: barabasi_albert,waxman",
    )
    parser.add_argument(
        "--node-scales",
        type=str,
        default="20,50,100",
        help="Comma-separated node counts",
    )
    parser.add_argument(
        "--controllers",
        type=str,
        default="3,5",
        help="Comma-separated controller budgets",
    )
    parser.add_argument("--trials", type=int, default=5, help="Trials per scenario")
    parser.add_argument("--base-seed", type=int, default=42)

    parser.add_argument("--ba-m", type=int, default=2, help="Barabasi-Albert attachment degree")
    parser.add_argument("--waxman-alpha", type=float, default=0.4)
    parser.add_argument("--waxman-beta", type=float, default=0.1)
    parser.add_argument("--waxman-max-attempts", type=int, default=24)

    parser.add_argument("--ga-population-size", type=int, default=40)
    parser.add_argument("--ga-generations", type=int, default=50)
    parser.add_argument("--ga-mutation-rate", type=float, default=0.15)
    parser.add_argument("--ga-tournament-size", type=int, default=3)

    parser.add_argument("--mab-episodes", type=int, default=300)
    parser.add_argument("--mab-epsilon", type=float, default=0.2)
    parser.add_argument("--mab-candidate-pool-size", type=int, default=64)
    parser.add_argument("--mab-latency-weight", type=float, default=1.0)
    parser.add_argument("--mab-reliability-weight", type=float, default=0.25)

    parser.add_argument(
        "--warmup-runs",
        type=int,
        default=1,
        help="Unrecorded warm-up runs per algorithm/scenario to reduce startup bias",
    )
    parser.add_argument("--data-dir", type=str, default="results/experiment_data")
    parser.add_argument("--graph-dir", type=str, default="results/graphs")
    return parser.parse_args()


def _run_algorithm_once(
    algorithm_name: str,
    graph,
    num_controllers: int,
    trial_seed: int,
    args: argparse.Namespace,
) -> tuple[list[str], dict[str, int | float | None]]:
    if algorithm_name == "random":
        controllers = random_controller_placement(graph, num_controllers, seed=trial_seed)
        return controllers, {"iterations_budget": 1, "convergence_iteration": 1}

    if algorithm_name == "greedy_k_center":
        controllers = greedy_k_center_placement(graph, num_controllers)
        return controllers, {"iterations_budget": 1, "convergence_iteration": 1}

    if algorithm_name == "kmeans":
        controllers = kmeans_controller_placement(graph, num_controllers, random_state=trial_seed)
        return controllers, {"iterations_budget": 1, "convergence_iteration": 1}

    if algorithm_name == "genetic":
        controllers, metadata = genetic_controller_placement(
            graph,
            num_controllers,
            population_size=args.ga_population_size,
            generations=args.ga_generations,
            mutation_rate=args.ga_mutation_rate,
            tournament_size=args.ga_tournament_size,
            seed=trial_seed,
            return_metadata=True,
        )
        return controllers, metadata

    if algorithm_name == "bandit_rl":
        controllers, metadata = bandit_rl_controller_placement(
            graph,
            num_controllers,
            episodes=args.mab_episodes,
            epsilon=args.mab_epsilon,
            candidate_pool_size=args.mab_candidate_pool_size,
            seed=trial_seed,
            latency_weight=args.mab_latency_weight,
            reliability_weight=args.mab_reliability_weight,
            return_metadata=True,
        )
        return controllers, metadata

    raise ValueError(f"Unknown algorithm: {algorithm_name}")


def _min_max_normalize(series: pd.Series) -> pd.Series:
    min_value = float(series.min())
    max_value = float(series.max())
    if max_value - min_value <= 1e-12:
        return pd.Series([0.0] * len(series), index=series.index)
    return (series - min_value) / (max_value - min_value)


def _pareto_optimal_mask(frame: pd.DataFrame, latency_col: str, runtime_col: str) -> list[bool]:
    points = frame[[latency_col, runtime_col]].to_numpy()
    mask: list[bool] = []

    for idx, point in enumerate(points):
        dominated = False
        for jdx, competitor in enumerate(points):
            if idx == jdx:
                continue
            dominates = (
                competitor[0] <= point[0]
                and competitor[1] <= point[1]
                and (competitor[0] < point[0] or competitor[1] < point[1])
            )
            if dominates:
                dominated = True
                break
        mask.append(not dominated)

    return mask


def _bootstrap_mean_diff_ci(
    values_a: np.ndarray,
    values_b: np.ndarray,
    confidence: float = 0.95,
    n_bootstrap: int = 2000,
    seed: int = 12345,
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)

    a = np.asarray(values_a, dtype=float)
    b = np.asarray(values_b, dtype=float)
    if a.size == 0 or b.size == 0:
        return float("nan"), float("nan")

    samples_a = rng.choice(a, size=(n_bootstrap, a.size), replace=True)
    samples_b = rng.choice(b, size=(n_bootstrap, b.size), replace=True)
    diffs = samples_a.mean(axis=1) - samples_b.mean(axis=1)

    alpha = 1.0 - confidence
    lower = float(np.quantile(diffs, alpha / 2.0))
    upper = float(np.quantile(diffs, 1.0 - alpha / 2.0))
    return lower, upper


def _cliffs_delta(values_a: np.ndarray, values_b: np.ndarray) -> float:
    a = np.asarray(values_a, dtype=float)
    b = np.asarray(values_b, dtype=float)
    if a.size == 0 or b.size == 0:
        return float("nan")

    greater = 0
    lesser = 0
    for left in a:
        for right in b:
            if left > right:
                greater += 1
            elif left < right:
                lesser += 1

    total = a.size * b.size
    if total == 0:
        return float("nan")
    return float((greater - lesser) / total)


def _cliffs_delta_magnitude(delta: float) -> str:
    abs_delta = abs(delta)
    if abs_delta < 0.147:
        return "negligible"
    if abs_delta < 0.33:
        return "small"
    if abs_delta < 0.474:
        return "medium"
    return "large"


def build_summary_table(raw_df: pd.DataFrame) -> pd.DataFrame:
    summary_df = (
        raw_df.groupby(
            ["topology_model", "node_count", "controller_budget", "algorithm"], as_index=False
        )
        .agg(
            avg_latency_mean=("avg_latency", "mean"),
            avg_latency_std=("avg_latency", "std"),
            runtime_ms_mean=("runtime_ms", "mean"),
            runtime_ms_std=("runtime_ms", "std"),
            iterations_budget_mean=("iterations_budget", "mean"),
            iterations_to_converge_mean=("iterations_to_converge", "mean"),
        )
        .sort_values(["topology_model", "node_count", "controller_budget", "avg_latency_mean"])
        .reset_index(drop=True)
    )

    summary_df["avg_latency_std"] = summary_df["avg_latency_std"].fillna(0.0)
    summary_df["runtime_ms_std"] = summary_df["runtime_ms_std"].fillna(0.0)
    summary_df["latency_runtime_product"] = summary_df["avg_latency_mean"] * summary_df["runtime_ms_mean"]

    scenario_frames: list[pd.DataFrame] = []
    for _, group in summary_df.groupby(["topology_model", "node_count", "controller_budget"], sort=False):
        scenario = group.copy()

        random_rows = scenario[scenario["algorithm"] == "random"]
        if not random_rows.empty:
            random_latency = float(random_rows["avg_latency_mean"].iloc[0])
            if random_latency > 0:
                scenario["latency_gain_vs_random_pct"] = (
                    (random_latency - scenario["avg_latency_mean"]) / random_latency
                ) * 100.0
            else:
                scenario["latency_gain_vs_random_pct"] = 0.0
        else:
            scenario["latency_gain_vs_random_pct"] = float("nan")

        latency_norm = _min_max_normalize(scenario["avg_latency_mean"])
        runtime_norm = _min_max_normalize(scenario["runtime_ms_mean"])
        scenario["efficiency_score"] = 0.5 * latency_norm + 0.5 * runtime_norm
        scenario["efficiency_rank"] = scenario["efficiency_score"].rank(method="min").astype(int)
        scenario["is_pareto_optimal"] = _pareto_optimal_mask(
            scenario,
            latency_col="avg_latency_mean",
            runtime_col="runtime_ms_mean",
        )

        scenario_frames.append(scenario)

    return pd.concat(scenario_frames, ignore_index=True)


def build_statistical_comparison_table(
    raw_df: pd.DataFrame,
    baseline_algorithm: str = "random",
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    group_cols = ["topology_model", "node_count", "controller_budget"]

    for scenario_index, (scenario_key, group) in enumerate(raw_df.groupby(group_cols, sort=False), start=1):
        topology_model, node_count, controller_budget = scenario_key

        baseline_rows = group[group["algorithm"] == baseline_algorithm]
        if baseline_rows.empty:
            continue

        baseline_latency = baseline_rows["avg_latency"].to_numpy(dtype=float)
        baseline_runtime = baseline_rows["runtime_ms"].to_numpy(dtype=float)

        for algorithm, algorithm_rows in group.groupby("algorithm", sort=False):
            if algorithm == baseline_algorithm:
                continue

            algo_latency = algorithm_rows["avg_latency"].to_numpy(dtype=float)
            algo_runtime = algorithm_rows["runtime_ms"].to_numpy(dtype=float)

            latency_gain_vs_baseline_mean = float(np.mean(baseline_latency) - np.mean(algo_latency))
            runtime_penalty_vs_baseline_mean = float(np.mean(algo_runtime) - np.mean(baseline_runtime))

            latency_ci_low, latency_ci_high = _bootstrap_mean_diff_ci(
                baseline_latency,
                algo_latency,
                seed=1000 + scenario_index,
            )
            runtime_ci_low, runtime_ci_high = _bootstrap_mean_diff_ci(
                algo_runtime,
                baseline_runtime,
                seed=2000 + scenario_index,
            )

            latency_delta = _cliffs_delta(algo_latency, baseline_latency)
            runtime_delta = _cliffs_delta(algo_runtime, baseline_runtime)

            rows.append(
                {
                    "topology_model": topology_model,
                    "node_count": int(node_count),
                    "controller_budget": int(controller_budget),
                    "algorithm": str(algorithm),
                    "baseline_algorithm": baseline_algorithm,
                    "trials_algorithm": int(len(algo_latency)),
                    "trials_baseline": int(len(baseline_latency)),
                    "latency_gain_vs_baseline_mean": latency_gain_vs_baseline_mean,
                    "latency_gain_ci95_low": latency_ci_low,
                    "latency_gain_ci95_high": latency_ci_high,
                    "runtime_penalty_vs_baseline_mean": runtime_penalty_vs_baseline_mean,
                    "runtime_penalty_ci95_low": runtime_ci_low,
                    "runtime_penalty_ci95_high": runtime_ci_high,
                    "latency_cliffs_delta_alg_vs_baseline": latency_delta,
                    "latency_cliffs_magnitude": _cliffs_delta_magnitude(latency_delta),
                    "runtime_cliffs_delta_alg_vs_baseline": runtime_delta,
                    "runtime_cliffs_magnitude": _cliffs_delta_magnitude(runtime_delta),
                }
            )

    if not rows:
        raise RuntimeError("No statistical comparison rows generated.")

    return pd.DataFrame(rows).sort_values(group_cols + ["algorithm"]).reset_index(drop=True)


def plot_pareto_by_scenario(summary_df: pd.DataFrame, output_dir: Path, timestamp: str) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    colors = {
        "random": "#7D8597",
        "greedy_k_center": "#277DA1",
        "kmeans": "#4D908E",
        "genetic": "#F9844A",
        "bandit_rl": "#F94144",
    }

    saved_paths: list[Path] = []
    group_cols = ["topology_model", "node_count", "controller_budget"]

    for (topology_model, node_count, controller_budget), scenario in summary_df.groupby(group_cols):
        fig, ax = plt.subplots(figsize=(8.5, 5.2))

        for _, row in scenario.iterrows():
            algorithm = str(row["algorithm"])
            color = colors.get(algorithm, "#1D3557")
            marker = "*" if bool(row["is_pareto_optimal"]) else "o"
            size = 180 if marker == "*" else 90

            ax.scatter(
                float(row["runtime_ms_mean"]),
                float(row["avg_latency_mean"]),
                color=color,
                marker=marker,
                s=size,
                alpha=0.9,
                edgecolors="black",
                linewidths=0.7,
            )
            ax.annotate(
                algorithm,
                (float(row["runtime_ms_mean"]), float(row["avg_latency_mean"])),
                xytext=(4, 4),
                textcoords="offset points",
                fontsize=8,
            )

        pareto_points = scenario[scenario["is_pareto_optimal"]].sort_values("runtime_ms_mean")
        if len(pareto_points) >= 2:
            ax.plot(
                pareto_points["runtime_ms_mean"],
                pareto_points["avg_latency_mean"],
                color="black",
                linestyle="--",
                linewidth=1.2,
                alpha=0.85,
                label="Pareto frontier",
            )

        ax.set_xscale("log")
        ax.set_xlabel("Runtime (ms, log scale)")
        ax.set_ylabel("Average Controller-to-Switch Distance")
        ax.set_title(
            f"Latency-Cost Pareto: {topology_model}, n={node_count}, k={controller_budget}",
        )
        ax.grid(alpha=0.35, linestyle="--")

        output_path = output_dir / (
            f"latency_cost_pareto_{topology_model}_n{node_count}_k{controller_budget}_{timestamp}.png"
        )
        fig.tight_layout()
        fig.savefig(output_path, dpi=180)
        plt.close(fig)
        saved_paths.append(output_path)

    return saved_paths


def main() -> None:
    args = parse_args()

    topology_models = parse_model_list(args.topology_models)
    node_scales = parse_int_list(args.node_scales)
    controller_budgets = parse_int_list(args.controllers)

    algorithms = ["random", "greedy_k_center", "kmeans", "genetic", "bandit_rl"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    data_dir = PROJECT_ROOT / args.data_dir
    graph_dir = PROJECT_ROOT / args.graph_dir
    data_dir.mkdir(parents=True, exist_ok=True)
    graph_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, object]] = []
    scenario_counter = 0

    for topology_model in topology_models:
        for node_count in node_scales:
            for controller_budget in controller_budgets:
                if controller_budget > node_count:
                    continue

                scenario_counter += 1
                topology_seed = args.base_seed + scenario_counter * 997
                scenario_name = f"{topology_model}_n{node_count}_k{controller_budget}"

                graph = generate_synthetic_topology(
                    SyntheticTopologyConfig(
                        model=topology_model,
                        num_nodes=node_count,
                        seed=topology_seed,
                        ba_m=args.ba_m,
                        waxman_alpha=args.waxman_alpha,
                        waxman_beta=args.waxman_beta,
                        max_regeneration_attempts=args.waxman_max_attempts,
                    )
                )

                if args.warmup_runs > 0:
                    for algorithm_name in algorithms:
                        for warmup_index in range(args.warmup_runs):
                            warmup_seed = (
                                args.base_seed
                                + scenario_counter * 30011
                                + warmup_index * 997
                                + len(algorithm_name)
                            )
                            _run_algorithm_once(
                                algorithm_name=algorithm_name,
                                graph=graph,
                                num_controllers=controller_budget,
                                trial_seed=warmup_seed,
                                args=args,
                            )

                for trial in range(1, args.trials + 1):
                    trial_seed = args.base_seed + scenario_counter * 10007 + trial * 131

                    for algorithm_name in algorithms:
                        start_time = time.perf_counter()
                        controllers, metadata = _run_algorithm_once(
                            algorithm_name=algorithm_name,
                            graph=graph,
                            num_controllers=controller_budget,
                            trial_seed=trial_seed,
                            args=args,
                        )
                        runtime_ms = (time.perf_counter() - start_time) * 1000.0
                        avg_latency = average_controller_distance(graph, controllers)

                        rows.append(
                            {
                                "scenario": scenario_name,
                                "topology_model": topology_model,
                                "node_count": int(node_count),
                                "controller_budget": int(controller_budget),
                                "trial": int(trial),
                                "algorithm": algorithm_name,
                                "avg_latency": float(avg_latency),
                                "runtime_ms": float(runtime_ms),
                                "iterations_budget": int(metadata.get("iterations_budget", 1)),
                                "iterations_to_converge": metadata.get("convergence_iteration"),
                                "topology_seed": int(topology_seed),
                                "trial_seed": int(trial_seed),
                                "controllers": ";".join(map(str, controllers)),
                            }
                        )

    if not rows:
        raise RuntimeError("No experiment rows generated. Check matrix parameters.")

    raw_df = pd.DataFrame(rows)
    summary_df = build_summary_table(raw_df)
    stats_df = build_statistical_comparison_table(raw_df)

    best_df = (
        summary_df.sort_values(
            ["topology_model", "node_count", "controller_budget", "efficiency_rank", "avg_latency_mean"]
        )
        .groupby(["topology_model", "node_count", "controller_budget"], as_index=False)
        .head(1)
        .reset_index(drop=True)
    )

    raw_csv = data_dir / f"factorial_latency_cost_raw_{timestamp}.csv"
    summary_csv = data_dir / f"factorial_latency_cost_summary_{timestamp}.csv"
    best_csv = data_dir / f"factorial_latency_cost_best_{timestamp}.csv"
    stats_csv = data_dir / f"factorial_latency_cost_stats_{timestamp}.csv"

    raw_df.to_csv(raw_csv, index=False)
    summary_df.to_csv(summary_csv, index=False)
    best_df.to_csv(best_csv, index=False)
    stats_df.to_csv(stats_csv, index=False)

    pareto_dir = graph_dir / f"latency_cost_pareto_{timestamp}"
    pareto_plots = plot_pareto_by_scenario(summary_df, pareto_dir, timestamp)

    print(f"Scenarios evaluated: {summary_df[['topology_model', 'node_count', 'controller_budget']].drop_duplicates().shape[0]}")
    print(f"Raw output: {raw_csv}")
    print(f"Summary output: {summary_csv}")
    print(f"Best-per-scenario output: {best_csv}")
    print(f"Statistical comparison output: {stats_csv}")
    print(f"Pareto plots generated: {len(pareto_plots)}")
    if pareto_plots:
        print(f"Pareto output directory: {pareto_dir}")


if __name__ == "__main__":
    main()
