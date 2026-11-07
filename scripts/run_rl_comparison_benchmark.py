#!/usr/bin/env python3
"""
Side-by-Side RL Comparison Benchmark (Bandit RL vs. PyTorch DQN on Internet2, k=3)
==================================================================================
Created as part of the Local Antigravity Agent <-> Google AI Studio Cloud Agent
closed-loop collaboration (Turn 3 Action Item 2).
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from algorithms.ai.reinforcement_learning import (
    bandit_rl_controller_placement,
    dqn_controller_placement,
)
from evaluation.metrics import (
    average_controller_distance,
    control_plane_reliability_single_link_failure_cached,
)
from topology.canonical_topologies import load_topology_file


def main() -> int:
    graph_path = ROOT_DIR / "data" / "raw" / "topologies" / "Internet2.graphml"
    graph = load_topology_file(str(graph_path))
    k = 3
    seed = 42

    t0 = time.perf_counter()
    bandit_nodes, bandit_meta = bandit_rl_controller_placement(
        graph=graph,
        num_controllers=k,
        episodes=300,
        seed=seed,
        latency_weight=1.0,
        reliability_weight=0.25,
        seconds_per_episode_weight=0.25,
        return_metadata=True,
    )
    bandit_wall_ms = (time.perf_counter() - t0) * 1000.0
    bandit_lat = average_controller_distance(graph, bandit_nodes)
    bandit_rel = control_plane_reliability_single_link_failure_cached(graph, bandit_nodes)

    dqn_nodes, dqn_meta = dqn_controller_placement(
        graph=graph,
        num_controllers=k,
        episodes=200,
        seed=seed,
        return_metadata=True,
    )
    dqn_lat = average_controller_distance(graph, dqn_nodes)
    dqn_rel = control_plane_reliability_single_link_failure_cached(graph, dqn_nodes)

    summary = {
        "topology": "Internet2",
        "num_nodes": graph.number_of_nodes(),
        "num_edges": graph.number_of_edges(),
        "num_controllers": k,
        "seed": seed,
        "bandit_rl": {
            "selected_controllers": bandit_nodes,
            "average_latency_ms": round(bandit_lat, 4),
            "single_link_reliability": round(bandit_rel, 4),
            "training_wall_time_ms": round(bandit_wall_ms, 3),
            "metadata": bandit_meta,
        },
        "pytorch_dqn": {
            "selected_controllers": dqn_nodes,
            "average_latency_ms": round(dqn_lat, 4),
            "single_link_reliability": round(dqn_rel, 4),
            "training_time_sec": round(float(dqn_meta["training_time_sec"]), 4),
            "inference_time_ms": round(float(dqn_meta["inference_time_ms"]), 4),
            "metadata": dqn_meta,
        },
    }

    out_path = ROOT_DIR / "results" / "rl_comparison_benchmark.json"
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
