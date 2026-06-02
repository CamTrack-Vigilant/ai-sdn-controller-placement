#!/usr/bin/env python3
"""Run reliability sweep on multi-site synthetic topology seeds and check Internet2.

Outputs a JSON report at results/rl_analysis/pareto/pareto_shortlist_reliability_sweep.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "results" / "rl_analysis" / "pareto" / "pareto_shortlist_reliability_sweep.json"
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from topology.network_topology import TopologyConfig, generate_multi_site_topology
from evaluation.metrics import control_plane_reliability_single_link_failure_cached
from scripts.generate_pareto_presentation_plot import load_shortlist
from algorithms.baseline.greedy_placement import greedy_k_center_placement

SEEDS = [42, 123, 456, 789, 999]


def run_sweep() -> dict:
    shortlist = load_shortlist(ROOT / "results" / "rl_analysis" / "pareto" / "pareto_shortlist.json")
    unique_sets = []
    for entry in shortlist:
        controllers = entry.get("controllers")
        if isinstance(controllers, str):
            controllers = [c.strip() for c in controllers.split(";") if c.strip()]
        unique_sets.append({"algorithm": entry.get("algorithm"), "controllers": controllers, "trial": entry.get("trial")})

    results = {"sweep": [], "internet2": {}}

    for seed in SEEDS:
        tcfg = TopologyConfig(num_sites=4, nodes_per_site=12, intra_site_degree=4, inter_site_links=2, seed=seed)
        graph = generate_multi_site_topology(tcfg)
        seed_row = {"seed": seed, "checks": []}
        for entry in unique_sets:
            controllers = entry["controllers"]
            reliability = control_plane_reliability_single_link_failure_cached(graph, controllers)
            seed_row["checks"].append({"algorithm": entry["algorithm"], "trial": entry["trial"], "controllers": controllers, "reliability": float(reliability)})
        results["sweep"].append(seed_row)

    # If any reliability < 1.0, record and return
    any_non1 = any(any(check["reliability"] < 1.0 for check in seed_row["checks"]) for seed_row in results["sweep"])

    if not any_non1:
        # Run Internet2 check
        try:
            from run_baseline_internet2 import _load_internet2_graph
            graph_i2 = _load_internet2_graph(seed=42)
            internet2_checks = []
            for entry in unique_sets:
                controller_budget = len(entry["controllers"]) if entry["controllers"] else 0
                internet2_controllers = greedy_k_center_placement(graph_i2, controller_budget)
                reliability = control_plane_reliability_single_link_failure_cached(graph_i2, internet2_controllers)
                internet2_checks.append(
                    {
                        "algorithm": entry["algorithm"],
                        "controller_budget": controller_budget,
                        "shortlist_controllers": entry["controllers"],
                        "internet2_controllers": internet2_controllers,
                        "reliability": float(reliability),
                    }
                )
            results["internet2"] = {"checked": True, "checks": internet2_checks}
        except Exception as exc:
            results["internet2"] = {"checked": False, "error": str(exc)}

    OUT_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote reliability sweep report to {OUT_PATH}")
    return results


if __name__ == "__main__":
    run_sweep()
