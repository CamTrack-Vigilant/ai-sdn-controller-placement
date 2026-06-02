#!/usr/bin/env python3
"""Validate Pareto shortlist candidates in Mininet against the multi-site benchmark graph.

The shortlist produced by `scripts/pareto_synthesis.py` is validated post-hoc on the
same 4-site by 12-node multi-site topology used by the benchmark family. This keeps
Phase 6 focused on packet-level verification while making the benchmark input and
topology source explicit.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from evaluation.metrics import average_controller_distance
from simulation.mininet_simulation import run_mininet_simulation
from topology.network_topology import TopologyConfig, generate_multi_site_topology


DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "experiment_config.json"
DEFAULT_SHORTLIST_PATH = PROJECT_ROOT / "results" / "rl_analysis" / "pareto" / "pareto_shortlist.json"
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "results" / "rl_analysis" / "pareto" / "pareto_shortlist_mininet_validation.json"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_topology_config(path: Path) -> TopologyConfig:
    payload = _load_json(path)
    topology_payload = payload.get("topology", payload)
    return TopologyConfig(
        num_sites=int(topology_payload.get("num_sites", 4)),
        nodes_per_site=int(topology_payload.get("nodes_per_site", 12)),
        intra_site_degree=int(topology_payload.get("intra_site_degree", 4)),
        rewiring_prob=float(topology_payload.get("rewiring_prob", 0.2)),
        inter_site_links=int(topology_payload.get("inter_site_links", 2)),
        seed=topology_payload.get("seed", 42),
    )


def _parse_controllers(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        return [chunk.strip() for chunk in value.split(";") if chunk.strip()]
    raise TypeError(f"Unsupported controller payload: {type(value)!r}")


def _load_shortlist(path: Path) -> list[dict[str, Any]]:
    payload = _load_json(path)
    if isinstance(payload, list):
        return [dict(entry) for entry in payload]
    if isinstance(payload, dict) and "shortlist" in payload:
        shortlist = payload["shortlist"]
        if isinstance(shortlist, list):
            return [dict(entry) for entry in shortlist]
    raise ValueError(f"Unsupported shortlist format in {path}")


def _unique_controller_sets(shortlist: list[dict[str, Any]]) -> list[tuple[str, ...]]:
    seen: set[tuple[str, ...]] = set()
    ordered: list[tuple[str, ...]] = []
    for entry in shortlist:
        controllers = tuple(_parse_controllers(entry.get("controllers", [])))
        if controllers in seen:
            continue
        seen.add(controllers)
        ordered.append(controllers)
    return ordered


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run phase-6 Mininet validation for Pareto shortlist candidates."
    )
    parser.add_argument(
        "--benchmark-input",
        type=str,
        required=True,
        help="Benchmark CSV/JSON/JSONL file used to generate the shortlist.",
    )
    parser.add_argument(
        "--shortlist-input",
        type=str,
        default=str(DEFAULT_SHORTLIST_PATH),
        help="Pareto shortlist JSON to validate.",
    )
    parser.add_argument(
        "--topology-config",
        type=str,
        default=str(DEFAULT_CONFIG_PATH),
        help="JSON file containing the multi-site topology config.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(DEFAULT_OUTPUT_PATH),
        help="Validation JSON output path.",
    )
    parser.add_argument(
        "--base-link-delay-ms",
        type=float,
        default=2.0,
        help="Base RTT multiplier used by the Mininet latency approximation.",
    )
    parser.add_argument(
        "--jitter-ms",
        type=float,
        default=0.5,
        help="Synthetic fallback jitter applied when Mininet is unavailable.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed forwarded to the latency simulation helper.",
    )
    parser.add_argument(
        "--allow-fallback",
        action="store_true",
        help="Fall back to synthetic latency simulation if Mininet execution fails.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    benchmark_input = Path(args.benchmark_input)
    shortlist_input = Path(args.shortlist_input)
    topology_config_path = Path(args.topology_config)
    output_path = Path(args.output)

    if not benchmark_input.exists():
        print(f"Benchmark input not found: {benchmark_input}", file=sys.stderr)
        return 2
    if not shortlist_input.exists():
        print(f"Shortlist input not found: {shortlist_input}", file=sys.stderr)
        return 2
    if not topology_config_path.exists():
        print(f"Topology config not found: {topology_config_path}", file=sys.stderr)
        return 2

    topology_config = _load_topology_config(topology_config_path)
    graph = generate_multi_site_topology(topology_config)
    shortlist = _load_shortlist(shortlist_input)
    unique_controller_sets = _unique_controller_sets(shortlist)

    print("PHASE 6 MININET SHORTLIST VALIDATION")
    print(f"Benchmark input: {benchmark_input}")
    print(f"Shortlist input: {shortlist_input}")
    print(f"Topology: {topology_config.num_sites} sites x {topology_config.nodes_per_site} nodes/site")
    print(f"Graph nodes: {graph.number_of_nodes()} edges: {graph.number_of_edges()}")
    print(f"Candidates: {len(shortlist)} entries ({len(unique_controller_sets)} unique controller sets)")

    if graph.number_of_nodes() != topology_config.num_sites * topology_config.nodes_per_site:
        print(
            "Topology size does not match the configured multi-site benchmark layout.",
            file=sys.stderr,
        )
        return 2

    benchmark_results: list[dict[str, Any]] = []
    for entry in shortlist:
        controllers = _parse_controllers(entry.get("controllers", []))
        missing = [controller for controller in controllers if controller not in graph]
        if missing:
            raise ValueError(
                f"Controller nodes not found in benchmark graph: {missing}. "
                "Check the topology config against the shortlist provenance."
            )

        mininet_result = run_mininet_simulation(
            graph=graph,
            controllers=controllers,
            base_link_delay_ms=args.base_link_delay_ms,
            jitter_ms=args.jitter_ms,
            seed=args.seed,
            fallback_to_synthetic=args.allow_fallback,
        )
        graph_latency = average_controller_distance(graph, controllers)

        benchmark_results.append(
            {
                "algorithm": entry.get("algorithm"),
                "controllers": controllers,
                "trial": entry.get("trial"),
                "graph_average_distance": float(graph_latency),
                "mininet_average_rtt_ms": float(mininet_result.average_rtt_ms),
                "mininet_worst_rtt_ms": float(mininet_result.worst_rtt_ms),
                "rtt_minus_graph_ms": float(mininet_result.average_rtt_ms - graph_latency),
                "source_entry": entry,
            }
        )

    best_result = min(benchmark_results, key=lambda item: item["mininet_average_rtt_ms"])
    insight = (
        f"Best Mininet RTT on the 48-node multi-site benchmark: {best_result['mininet_average_rtt_ms']:.3f} ms "
        f"for {best_result['algorithm']} with {len(best_result['controllers'])} controllers."
    )
    print(insight)

    output_payload = {
        "benchmark_input": str(benchmark_input),
        "shortlist_input": str(shortlist_input),
        "topology_config": asdict(topology_config),
        "graph": {
            "nodes": graph.number_of_nodes(),
            "edges": graph.number_of_edges(),
        },
        "insight": insight,
        "results": benchmark_results,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output_payload, indent=2), encoding="utf-8")
    print(f"Validation output: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())