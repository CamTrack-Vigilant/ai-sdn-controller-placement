from __future__ import annotations

from functools import partial
from inspect import signature
import random
from pathlib import Path
import time
from typing import Any, Callable, Dict, List

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from evaluation.metrics import summarize_metrics

AlgorithmFn = Callable[..., List[str]]


def _invoke_algorithm(
    algorithm: AlgorithmFn,
    graph: nx.Graph,
    num_controllers: int,
    trial_seed: int,
) -> tuple[List[str], dict[str, Any]]:
    params = signature(algorithm).parameters
    kwargs = {}
    if "seed" in params:
        kwargs["seed"] = trial_seed
    if "random_state" in params:
        kwargs["random_state"] = trial_seed
    if "return_metadata" in params:
        kwargs["return_metadata"] = True

    result = algorithm(graph, num_controllers, **kwargs)
    if isinstance(result, tuple) and len(result) == 2:
        controllers, metadata = result
        return list(controllers), dict(metadata)

    return list(result), {}


def run_algorithm_benchmark(
    graph: nx.Graph,
    num_controllers: int,
    algorithms: Dict[str, AlgorithmFn],
    trials: int = 5,
    seed: int = 42,
) -> pd.DataFrame:
    rng = random.Random(seed)
    rows = []

    for trial in range(1, trials + 1):
        trial_seed = rng.randint(0, 10**9)
        for algorithm_name, algorithm in algorithms.items():
            start_time = time.perf_counter()
            controllers, metadata = _invoke_algorithm(algorithm, graph, num_controllers, trial_seed)
            runtime_ms = (time.perf_counter() - start_time) * 1000.0

            iterations_budget = metadata.get("iterations_budget", 1)
            convergence_iteration = metadata.get("convergence_iteration", 1)

            metric_row = summarize_metrics(graph, controllers)
            metric_row.update(
                {
                    "trial": trial,
                    "algorithm": algorithm_name,
                    "controllers": ";".join(map(str, controllers)),
                    "runtime_ms": float(runtime_ms),
                    "iterations_budget": int(iterations_budget) if iterations_budget is not None else 1,
                    "iterations_to_converge": (
                        int(convergence_iteration)
                        if convergence_iteration is not None
                        else None
                    ),
                }
            )
            rows.append(metric_row)

    return pd.DataFrame(rows)


def plot_metric_comparison(df: pd.DataFrame, metric: str, output_path: Path) -> None:
    if metric not in df.columns:
        raise ValueError(f"Unknown metric: {metric}")

    grouped = df.groupby("algorithm")[metric]
    means = grouped.mean().sort_values()
    stds = grouped.std().fillna(0.0).reindex(means.index)

    fig, ax = plt.subplots(figsize=(9, 5))
    means.plot(kind="bar", yerr=stds, capsize=4, ax=ax, color="#2A9D8F")
    ax.set_title(f"{metric} by Algorithm")
    ax.set_xlabel("Algorithm")
    ax.set_ylabel(metric)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def default_algorithm_suite(
    bandit_kwargs: Dict[str, Any] | None = None,
) -> Dict[str, AlgorithmFn]:
    from algorithms.ai.genetic_algorithm import genetic_controller_placement
    from algorithms.ai.reinforcement_learning import bandit_rl_controller_placement
    from algorithms.baseline.greedy_placement import greedy_k_center_placement
    from algorithms.baseline.kmeans_placement import kmeans_controller_placement
    from algorithms.baseline.random_placement import random_controller_placement

    bandit_algorithm: AlgorithmFn = bandit_rl_controller_placement
    if bandit_kwargs:
        bandit_algorithm = partial(bandit_rl_controller_placement, **bandit_kwargs)

    return {
        "random": random_controller_placement,
        "greedy_k_center": greedy_k_center_placement,
        "kmeans": kmeans_controller_placement,
        "genetic": genetic_controller_placement,
        "bandit_rl": bandit_algorithm,
    }
