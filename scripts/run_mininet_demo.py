#!/usr/bin/env python3
"""
Run Mininet / Emulated Latency Benchmark across Algorithms on Internet2 Canonical Topology
"""
import sys
from pathlib import Path
import json

# Compatibility shim for legacy pandas/scipy expecting NumPy < 1.20 deprecated aliases
try:
    import numpy as np
    for _alias, _target in [("bool", bool), ("int", int), ("float", float)]:
        if not hasattr(np, _alias):
            setattr(np, _alias, _target)
except Exception:
    pass

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from topology.canonical_topologies import load_canonical_topology
from algorithms.baseline.greedy_placement import greedy_k_center_placement
from algorithms.baseline.kmeans_placement import kmeans_controller_placement
from algorithms.baseline.random_placement import random_controller_placement
from simulation.mininet_simulation import run_mininet_simulation

def main():
    print("=" * 60)
    print("MININET / EMULATED SDN CONTROLLER PLACEMENT BENCHMARK")
    print("=" * 60)
    
    graph = load_canonical_topology("Internet2")
    num_controllers = 3
    print(f"Topology: Internet2 ({graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges)")
    print(f"Controller Budget (k): {num_controllers}\n")

    algorithms = {
        "Random": random_controller_placement(graph, num_controllers, seed=42),
        "Greedy K-Center": greedy_k_center_placement(graph, num_controllers),
        "K-Means": kmeans_controller_placement(graph, num_controllers, random_state=42),
    }

    results = {}
    for name, placement in algorithms.items():
        print(f"Running simulation for {name} Placement: {placement}...")
        sim_res = run_mininet_simulation(graph, placement, base_link_delay_ms=2.0, fallback_to_synthetic=True)
        results[name] = {
            "placement": placement,
            "avg_rtt_ms": round(sim_res.average_rtt_ms, 3),
            "worst_rtt_ms": round(sim_res.worst_rtt_ms, 3)
        }
        print(f"  ✓ Avg RTT: {sim_res.average_rtt_ms:.3f} ms | Worst RTT: {sim_res.worst_rtt_ms:.3f} ms\n")

    output_file = PROJECT_ROOT / "results" / "mininet_simulation_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"✓ Saved Mininet simulation results to: {output_file}")

if __name__ == "__main__":
    main()
