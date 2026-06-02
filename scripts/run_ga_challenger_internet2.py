#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import itertools
from pathlib import Path
import sys
import time
from typing import Any

import networkx as nx

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from algorithms.ai.genetic_algorithm import genetic_controller_placement
from algorithms.baseline.greedy_placement import greedy_k_center_placement
from evaluation.metrics import (
    average_controller_distance,
    control_plane_reliability_single_link_failure,
    worst_case_controller_distance,
)
from evaluation.telemetry import ResourceMonitor
from topology.canonical_topologies import load_canonical_topology


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run first GA challenger against greedy baseline on Internet2 synthetic fallback parity.",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--ga-population", type=int, default=50)
    parser.add_argument("--ga-generations", type=int, default=100)
    parser.add_argument("--ga-mutation-rate", type=float, default=0.15)
    parser.add_argument("--ga-tournament-size", type=int, default=3)
    parser.add_argument("--telemetry-interval", type=float, default=0.05)
    parser.add_argument(
        "--repeat-count",
        type=int,
        default=100,
        help="Repeat each algorithm this many times to stabilize telemetry for short runtimes.",
    )
    parser.add_argument(
        "--output-csv",
        default="results/experiment_data/ga_challenger_internet2.csv",
    )
    return parser.parse_args()


def _run_with_monitor(func, *, telemetry_interval: float, repeat_count: int) -> tuple[Any, float, float, float, int, str, float]:
    monitor = ResourceMonitor.for_algorithm(sample_interval_s=telemetry_interval)
    monitor.start()
    start = time.perf_counter()
    result = None
    for _ in range(repeat_count):
        result = func()
    elapsed_total = time.perf_counter() - start
    snapshot = monitor.stop()
    return (
        result,
        elapsed_total,
        snapshot.cpu_percent,
        snapshot.rss_memory_mb,
        snapshot.samples,
        snapshot.status,
        elapsed_total / max(1, repeat_count),
    )


def _exhaustive_optimum_worst_case(graph, k: int) -> tuple[list[int], float]:
    best_val = None
    best_combo = None
    nodes = list(graph.nodes())
    for combo in itertools.combinations(nodes, k):
        val = worst_case_controller_distance(graph, combo)
        if best_val is None or val < best_val:
            best_val = val
            best_combo = combo
    return list(best_combo) if best_combo is not None else [], float(best_val if best_val is not None else float("inf"))


def _first_hit_generation(history: list[list[Any]], target: list[Any]) -> int | None:
    target_list = [str(node) for node in target]
    for index, placement in enumerate(history, start=1):
        if [str(node) for node in placement] == target_list:
            return index
    return None


def main() -> int:
    args = parse_args()

    graph = load_canonical_topology("Internet2", seed=args.seed)
    if any(not isinstance(node, str) for node in graph.nodes):
        graph = nx.relabel_nodes(graph, {node: str(node) for node in graph.nodes})

    greedy_result = _run_with_monitor(
        lambda: greedy_k_center_placement(graph, args.k),
        telemetry_interval=args.telemetry_interval,
        repeat_count=args.repeat_count,
    )
    ga_result = _run_with_monitor(
        lambda: genetic_controller_placement(
            graph,
            args.k,
            population_size=args.ga_population,
            generations=args.ga_generations,
            mutation_rate=args.ga_mutation_rate,
            tournament_size=args.ga_tournament_size,
            seed=args.seed,
            return_metadata=True,
        ),
        telemetry_interval=args.telemetry_interval,
        repeat_count=args.repeat_count,
    )

    greedy_nodes = list(greedy_result[0])
    ga_payload = ga_result[0]
    ga_nodes = list(ga_payload[0])
    ga_metadata: dict[str, Any] = ga_payload[1]

    greedy_l = average_controller_distance(graph, greedy_nodes)
    ga_l = average_controller_distance(graph, ga_nodes)

    greedy_r = control_plane_reliability_single_link_failure(graph, greedy_nodes)
    ga_r = control_plane_reliability_single_link_failure(graph, ga_nodes)

    optimum_nodes, optimum_worst = _exhaustive_optimum_worst_case(graph, args.k)
    ga_first_hit_generation = _first_hit_generation(
        ga_metadata.get("best_placement_history", []),
        optimum_nodes,
    )

    rows = [
        {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "algorithm": "greedy_k_center",
            "topology": str(graph.graph.get("name", "Internet2")),
            "topology_source": str(graph.graph.get("source", "synthetic_fallback")),
            "seed": args.seed,
            "k": args.k,
            "placement": ";".join(str(node) for node in greedy_nodes),
            "latency_l": greedy_l,
            "reliability_r_avg": greedy_r,
            "tau_runtime_seconds": greedy_result[1],
            "tau_runtime_seconds_per_run": greedy_result[6],
            "telemetry_mean_cpu_percent": greedy_result[2],
            "telemetry_peak_rss_mb": greedy_result[3],
            "telemetry_samples": greedy_result[4],
            "telemetry_status": greedy_result[5],
            "repeat_count": args.repeat_count,
            "ga_population": args.ga_population,
            "ga_generations": args.ga_generations,
            "ga_mutation_rate": args.ga_mutation_rate,
            "ga_tournament_size": args.ga_tournament_size,
            "exhaustive_optimum_worst_case_nodes": ";".join(str(node) for node in optimum_nodes),
            "exhaustive_optimum_worst_case_distance": optimum_worst,
            "first_hit_optimum_generation": ga_first_hit_generation,
        },
        {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "algorithm": "genetic_algorithm",
            "topology": str(graph.graph.get("name", "Internet2")),
            "topology_source": str(graph.graph.get("source", "synthetic_fallback")),
            "seed": args.seed,
            "k": args.k,
            "placement": ";".join(str(node) for node in ga_nodes),
            "latency_l": ga_l,
            "reliability_r_avg": ga_r,
            "tau_runtime_seconds": ga_result[1],
            "tau_runtime_seconds_per_run": ga_result[6],
            "telemetry_mean_cpu_percent": ga_result[2],
            "telemetry_peak_rss_mb": ga_result[3],
            "telemetry_samples": ga_result[4],
            "telemetry_status": ga_result[5],
            "repeat_count": args.repeat_count,
            "ga_population": args.ga_population,
            "ga_generations": args.ga_generations,
            "ga_mutation_rate": args.ga_mutation_rate,
            "ga_tournament_size": args.ga_tournament_size,
            "exhaustive_optimum_worst_case_nodes": ";".join(str(node) for node in optimum_nodes),
            "exhaustive_optimum_worst_case_distance": optimum_worst,
            "first_hit_optimum_generation": ga_first_hit_generation,
        },
    ]

    output_path = Path(args.output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print("[INFO] GA challenger completed")
    print(f"[INFO] Output CSV: {output_path}")
    print(f"[INFO] Greedy placement: {greedy_nodes} | latency={greedy_l:.6f} | reliability={greedy_r:.6f} | tau_per_run={greedy_result[6]:.6f}s")
    print(f"[INFO] GA placement: {ga_nodes} | latency={ga_l:.6f} | reliability={ga_r:.6f} | tau_per_run={ga_result[6]:.6f}s")
    print(f"[INFO] GA first optimum hit generation: {ga_first_hit_generation}")
    print(f"[INFO] Exhaustive worst-case optimum nodes: {optimum_nodes} | worst_case_distance={optimum_worst:.6f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
