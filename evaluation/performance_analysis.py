from __future__ import annotations

from functools import partial
from inspect import signature
import random
from pathlib import Path
import threading
import time
from typing import Any, Callable, Dict, List

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from evaluation.metrics import summarize_metrics
from evaluation.telemetry import ResourceMonitor

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
            try:
                algorithm_monitor = ResourceMonitor.for_algorithm(
                    sample_interval_s=0.1,
                    thread_native_id=threading.get_native_id(),
                )
            except Exception:
                algorithm_monitor = ResourceMonitor.unavailable(status="algorithm_monitor_error")

            try:
                ryu_monitor = ResourceMonitor.for_ryu(sample_interval_s=0.1)
            except Exception:
                ryu_monitor = ResourceMonitor.unavailable(status="controller_monitor_error")

            try:
                algorithm_monitor.start()
            except Exception:
                algorithm_monitor = ResourceMonitor.unavailable(status="algorithm_monitor_error")

            try:
                ryu_monitor.start()
            except Exception:
                ryu_monitor = ResourceMonitor.unavailable(status="controller_monitor_error")

            start_time = time.perf_counter()
            controllers, metadata = _invoke_algorithm(algorithm, graph, num_controllers, trial_seed)
            runtime_ms = (time.perf_counter() - start_time) * 1000.0

            try:
                algorithm_telemetry = algorithm_monitor.stop()
            except Exception:
                algorithm_telemetry = ResourceMonitor.unavailable(status="algorithm_monitor_error").stop()

            try:
                ryu_telemetry = ryu_monitor.stop()
            except Exception:
                ryu_telemetry = ResourceMonitor.unavailable(status="controller_monitor_error").stop()

            iterations_budget = metadata.get("iterations_budget", 1)
            convergence_iteration = metadata.get("convergence_iteration", 1)

            metric_row = summarize_metrics(graph, controllers)
            metric_row.update(
                {
                    "trial": trial,
                    "algorithm": algorithm_name,
                    "controllers": ";".join(map(str, controllers)),
                    "runtime_ms": float(runtime_ms),
                    "algorithm_telemetry_status": str(algorithm_telemetry.status),
                    "algorithm_cpu_percent": float(algorithm_telemetry.cpu_percent),
                    "algorithm_thread_cpu_percent": (
                        float(algorithm_telemetry.thread_cpu_percent)
                        if algorithm_telemetry.thread_cpu_percent is not None
                        else None
                    ),
                    "algorithm_rss_memory_mb": float(algorithm_telemetry.rss_memory_mb),
                    "algorithm_io_read_bytes": int(algorithm_telemetry.io_read_bytes),
                    "algorithm_io_write_bytes": int(algorithm_telemetry.io_write_bytes),
                    "controller_telemetry_status": str(ryu_telemetry.status),
                    "ryu_process_found": bool(ryu_telemetry.process_found),
                    "ryu_cpu_percent": (
                        float(ryu_telemetry.cpu_percent)
                        if ryu_telemetry.process_found
                        else None
                    ),
                    "ryu_rss_memory_mb": (
                        float(ryu_telemetry.rss_memory_mb)
                        if ryu_telemetry.process_found
                        else None
                    ),
                    "ryu_io_read_bytes": (
                        int(ryu_telemetry.io_read_bytes)
                        if ryu_telemetry.process_found
                        else None
                    ),
                    "ryu_io_write_bytes": (
                        int(ryu_telemetry.io_write_bytes)
                        if ryu_telemetry.process_found
                        else None
                    ),
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
