#!/usr/bin/env python3
"""
Dynamic Topology Churn & Break-Even Amortization Experiment
===========================================================
Designed in Turn 5 by the Google AI Studio Cloud Agent and implemented/executed
by the Local Antigravity Agent (`Workflow 2: Closed-Loop Experimental Design`).

Evaluates when a pre-trained PyTorch DQN's fast online forward-pass inference
(tau_inf) amortizes its upfront offline training cost (omega_train) compared
against re-running Greedy K-Center, Spatial K-Means, and Genetic Algorithm
from scratch across T_churn = 100 dynamic link-churn events on Internet2 (N=20, k=3)
and ATT-MPLS (N=21, k=3) across 5 random seeds (seeds = [42, 43, 44, 45, 46]).
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

import networkx as nx
import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from algorithms.ai.genetic_algorithm import genetic_controller_placement
from algorithms.ai.reinforcement_learning import dqn_controller_placement
from algorithms.baseline.greedy_placement import greedy_k_center_placement
from algorithms.baseline.kmeans_placement import kmeans_controller_placement
from evaluation.metrics import (
    average_controller_distance,
    control_plane_reliability_single_link_failure_cached,
)
from topology.canonical_topologies import load_canonical_topology


def _graph_hash(graph: nx.Graph) -> str:
    edges_repr = sorted(
        (min(str(u), str(v)), max(str(u), str(v)), round(float(d.get("weight", 1.0)), 4))
        for u, v, d in graph.edges(data=True)
    )
    return hashlib.sha256(json.dumps(edges_repr).encode("utf-8")).hexdigest()[:12]


def _step_link_churn(
    base_graph: nx.Graph,
    active_links: List[Tuple[str, str]],
    inactive_links: List[Tuple[str, str]],
    rng: random.Random,
) -> Tuple[nx.Graph, List[Tuple[str, str]], List[Tuple[str, str]]]:
    """
    Execute one dynamic link-churn step (single random non-bridge link removal
    and single random link restoration) while preserving graph connectivity.
    """
    temp_active = list(active_links)
    temp_inactive = list(inactive_links)

    # Identify candidate active links whose removal keeps G_t connected
    current_g = nx.Graph()
    current_g.add_nodes_from(base_graph.nodes(data=True))
    for u, v in temp_active:
        current_g.add_edge(u, v, **base_graph[u][v])

    bridges = set(nx.bridges(current_g))
    removable = [
        e for e in temp_active if e not in bridges and (e[1], e[0]) not in bridges
    ]

    removed_edge = None
    if removable:
        removed_edge = rng.choice(removable)
        temp_active.remove(removed_edge)

    if temp_inactive:
        restored_edge = rng.choice(temp_inactive)
        temp_inactive.remove(restored_edge)
        temp_active.append(restored_edge)

    if removed_edge is not None:
        temp_inactive.append(removed_edge)

    g_t = nx.Graph()
    g_t.add_nodes_from(base_graph.nodes(data=True))
    for u, v in temp_active:
        g_t.add_edge(u, v, **base_graph[u][v])

    return g_t, temp_active, temp_inactive


def main() -> int:
    topologies = ["Internet2", "ATT-MPLS"]
    k = 3
    seeds = [42, 43, 44, 45, 46]
    t_churn = 100
    dqn_train_episodes = 200

    models_dir = ROOT_DIR / "results" / "dqn_models"
    models_dir.mkdir(parents=True, exist_ok=True)

    run_records: List[Dict[str, Any]] = []
    summary_rows: List[Dict[str, Any]] = []

    for topo_name in topologies:
        for seed in seeds:
            base_graph = load_canonical_topology(topo_name, seed=seed)
            # Ensure string node labels
            if not all(isinstance(n, str) for n in base_graph.nodes):
                mapping = {n: f"n{n}" for n in base_graph.nodes}
                base_graph = nx.relabel_nodes(base_graph, mapping)

            model_path = models_dir / f"{topo_name}_k{k}_seed{seed}.pth"

            # Phase 1: Upfront Offline DQN Training on Base Graph
            _, dqn_train_meta = dqn_controller_placement(
                graph=base_graph,
                num_controllers=k,
                episodes=dqn_train_episodes,
                seed=seed,
                save_model_path=str(model_path),
                return_metadata=True,
            )
            dqn_initial_omega_train_sec = float(dqn_train_meta["training_time_sec"])
            dqn_initial_omega_train_ms = dqn_initial_omega_train_sec * 1000.0

            rng = random.Random(seed)
            active_links: List[Tuple[str, str]] = [
                (str(u), str(v)) for u, v in base_graph.edges()
            ]
            inactive_links: List[Tuple[str, str]] = []

            epochs_data: List[Dict[str, Any]] = []
            algo_latencies: Dict[str, List[float]] = {
                "DQN": [],
                "Greedy_K_Center": [],
                "K_Means": [],
                "GA": [],
            }
            algo_reliabilities: Dict[str, List[float]] = {
                "DQN": [],
                "Greedy_K_Center": [],
                "K_Means": [],
                "GA": [],
            }
            algo_decision_times_ms: Dict[str, List[float]] = {
                "DQN": [],
                "Greedy_K_Center": [],
                "K_Means": [],
                "GA": [],
            }

            # Phase 2: Dynamic Link-Churn Loop (T_churn = 100 epochs)
            for epoch_id in range(t_churn):
                if epoch_id == 0:
                    g_t = base_graph.copy()
                else:
                    g_t, active_links, inactive_links = _step_link_churn(
                        base_graph, active_links, inactive_links, rng
                    )

                # 1. Pre-trained PyTorch DQN (Inference Only, episodes=0)
                dqn_nodes, dqn_inf_meta = dqn_controller_placement(
                    graph=g_t,
                    num_controllers=k,
                    episodes=0,
                    seed=seed,
                    load_model_path=str(model_path),
                    return_metadata=True,
                )
                dqn_tau_ms = float(dqn_inf_meta["inference_time_ms"])
                dqn_lat = average_controller_distance(g_t, dqn_nodes)
                dqn_rel = (
                    control_plane_reliability_single_link_failure_cached(g_t, dqn_nodes)
                    * 100.0
                )

                # 2. Greedy K-Center (Re-run from scratch)
                t0 = time.perf_counter()
                greedy_nodes = greedy_k_center_placement(g_t, k)
                greedy_tau_ms = (time.perf_counter() - t0) * 1000.0
                greedy_lat = average_controller_distance(g_t, greedy_nodes)
                greedy_rel = (
                    control_plane_reliability_single_link_failure_cached(
                        g_t, greedy_nodes
                    )
                    * 100.0
                )

                # 3. Spatial K-Means (Re-run from scratch)
                t0 = time.perf_counter()
                kmeans_nodes = kmeans_controller_placement(g_t, k, random_state=seed)
                kmeans_tau_ms = (time.perf_counter() - t0) * 1000.0
                kmeans_lat = average_controller_distance(g_t, kmeans_nodes)
                kmeans_rel = (
                    control_plane_reliability_single_link_failure_cached(
                        g_t, kmeans_nodes
                    )
                    * 100.0
                )

                # 4. Genetic Algorithm (Re-run from scratch, pop=24, gen=25 for online response)
                t0 = time.perf_counter()
                ga_nodes = genetic_controller_placement(
                    g_t, k, population_size=24, generations=25, seed=seed
                )
                ga_tau_ms = (time.perf_counter() - t0) * 1000.0
                ga_lat = average_controller_distance(g_t, ga_nodes)
                ga_rel = (
                    control_plane_reliability_single_link_failure_cached(g_t, ga_nodes)
                    * 100.0
                )

                for name, lat, rel, tau in [
                    ("DQN", dqn_lat, dqn_rel, dqn_tau_ms),
                    ("Greedy_K_Center", greedy_lat, greedy_rel, greedy_tau_ms),
                    ("K_Means", kmeans_lat, kmeans_rel, kmeans_tau_ms),
                    ("GA", ga_lat, ga_rel, ga_tau_ms),
                ]:
                    algo_latencies[name].append(lat)
                    algo_reliabilities[name].append(rel)
                    algo_decision_times_ms[name].append(tau)

                # Store representative epoch snapshots (first 3 and last epoch to keep JSON clean)
                if epoch_id in (0, 1, 2, t_churn - 1):
                    epochs_data.append(
                        {
                            "epoch_id": epoch_id,
                            "num_active_links": len(active_links),
                            "graph_hash": _graph_hash(g_t),
                            "algorithms": {
                                "DQN": {
                                    "controllers": dqn_nodes,
                                    "mean_latency_L_P_t_ms": round(dqn_lat, 4),
                                    "reliability_N_1_P_t_percent": round(dqn_rel, 2),
                                    "decision_time_tau_t_ms": round(dqn_tau_ms, 4),
                                },
                                "Greedy_K_Center": {
                                    "controllers": greedy_nodes,
                                    "mean_latency_L_P_t_ms": round(greedy_lat, 4),
                                    "reliability_N_1_P_t_percent": round(greedy_rel, 2),
                                    "decision_time_tau_t_ms": round(greedy_tau_ms, 4),
                                },
                                "K_Means": {
                                    "controllers": kmeans_nodes,
                                    "mean_latency_L_P_t_ms": round(kmeans_lat, 4),
                                    "reliability_N_1_P_t_percent": round(kmeans_rel, 2),
                                    "decision_time_tau_t_ms": round(kmeans_tau_ms, 4),
                                },
                                "GA": {
                                    "controllers": ga_nodes,
                                    "mean_latency_L_P_t_ms": round(ga_lat, 4),
                                    "reliability_N_1_P_t_percent": round(ga_rel, 2),
                                    "decision_time_tau_t_ms": round(ga_tau_ms, 4),
                                },
                            },
                        }
                    )

            mean_dqn_tau_ms = float(np.mean(algo_decision_times_ms["DQN"]))
            cumulative_results: Dict[str, Any] = {}

            for algo in ["DQN", "Greedy_K_Center", "K_Means", "GA"]:
                mean_tau = float(np.mean(algo_decision_times_ms[algo]))
                total_inf_ms = float(np.sum(algo_decision_times_ms[algo]))
                omega_total_ms = (
                    dqn_initial_omega_train_ms + total_inf_ms
                    if algo == "DQN"
                    else total_inf_ms
                )
                entry: Dict[str, Any] = {
                    "mean_decision_time_tau_ms": round(mean_tau, 4),
                    "cumulative_compute_time_ms_Omega_algo": round(omega_total_ms, 3),
                    "average_latency_over_churn_ms": round(
                        float(np.mean(algo_latencies[algo])), 4
                    ),
                    "std_latency_over_churn_ms": round(
                        float(np.std(algo_latencies[algo])), 4
                    ),
                    "average_reliability_over_churn_percent": round(
                        float(np.mean(algo_reliabilities[algo])), 2
                    ),
                }
                if algo != "DQN":
                    delta_tau = mean_tau - mean_dqn_tau_ms
                    if delta_tau > 1e-6:
                        t_star = int(math.ceil(dqn_initial_omega_train_ms / delta_tau))
                    else:
                        t_star = None
                    entry["break_even_horizon_T_star_vs_DQN"] = t_star

                cumulative_results[algo] = entry
                summary_rows.append(
                    {
                        "topology": topo_name,
                        "num_nodes": base_graph.number_of_nodes(),
                        "num_controllers": k,
                        "seed": seed,
                        "t_churn_epochs": t_churn,
                        "algorithm": algo,
                        "initial_omega_train_ms": round(
                            dqn_initial_omega_train_ms if algo == "DQN" else 0.0, 3
                        ),
                        "mean_tau_inf_ms": round(mean_tau, 4),
                        "cumulative_omega_100_epochs_ms": round(omega_total_ms, 3),
                        "mean_churn_latency_ms": round(
                            float(np.mean(algo_latencies[algo])), 4
                        ),
                        "mean_churn_reliability_pct": round(
                            float(np.mean(algo_reliabilities[algo])), 2
                        ),
                        "break_even_T_star_epochs": entry.get(
                            "break_even_horizon_T_star_vs_DQN"
                        ),
                    }
                )

            run_records.append(
                {
                    "topology_name": topo_name,
                    "num_nodes": base_graph.number_of_nodes(),
                    "num_edges": base_graph.number_of_edges(),
                    "num_controllers_k": k,
                    "seed": seed,
                    "total_churn_epochs_T_churn": t_churn,
                    "dqn_initial_omega_train_sec": round(
                        dqn_initial_omega_train_sec, 4
                    ),
                    "dqn_initial_omega_train_ms": round(
                        dqn_initial_omega_train_ms, 2
                    ),
                    "sampled_epochs": epochs_data,
                    "cumulative_results": cumulative_results,
                }
            )
            print(
                f"[OK] {topo_name} (seed={seed}, T={t_churn}): "
                f"DQN train={dqn_initial_omega_train_ms:.1f}ms, inf={mean_dqn_tau_ms:.4f}ms | "
                f"T* vs GA={cumulative_results['GA']['break_even_horizon_T_star_vs_DQN']} epochs, "
                f"T* vs K-Means={cumulative_results['K_Means']['break_even_horizon_T_star_vs_DQN']} epochs"
            )

    out_json = ROOT_DIR / "results" / "dynamic_churn_benchmark.json"
    out_json.write_text(json.dumps(run_records, indent=2), encoding="utf-8")

    out_csv = ROOT_DIR / "results" / "experiment_data" / "dynamic_churn_summary.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"\n[SUCCESS] Wrote {out_json.relative_to(ROOT_DIR)} and {out_csv.relative_to(ROOT_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

