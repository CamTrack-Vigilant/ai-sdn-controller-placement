from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
import random
import re
from typing import Dict, Iterable
import warnings

import networkx as nx
import numpy as np


@dataclass
class SimulationResult:
    average_rtt_ms: float
    worst_rtt_ms: float
    per_node_latency_ms: Dict[str, float]


def _parse_ping_avg_ms(output: str) -> float | None:
    """Extract average RTT from Linux ping output."""
    patterns = [
        r"=\s*[\d\.]+/([\d\.]+)/[\d\.]+/[\d\.]+\s*ms",
        r"min/avg/max(?:/mdev|/stddev)?\s*=\s*[\d\.]+/([\d\.]+)/",
    ]
    for pattern in patterns:
        match = re.search(pattern, output)
        if match:
            return float(match.group(1))
    return None


def run_synthetic_latency_simulation(
    graph: nx.Graph,
    controllers: Iterable[str],
    base_link_delay_ms: float = 2.0,
    jitter_ms: float = 0.5,
    seed: int | None = 42,
) -> SimulationResult:
    """Approximate control-plane RTT using weighted shortest paths."""
    controller_list = list(controllers)
    if not controller_list:
        raise ValueError("controllers must not be empty")

    rng = random.Random(seed)
    distances = nx.multi_source_dijkstra_path_length(graph, controller_list, weight="weight")

    per_node: dict[str, float] = {}
    for node in graph.nodes:
        hop_distance = distances.get(node, float("inf"))
        if hop_distance == float("inf"):
            per_node[str(node)] = float("inf")
            continue
        jitter = rng.uniform(-jitter_ms, jitter_ms)
        per_node[str(node)] = max(0.0, hop_distance * base_link_delay_ms + jitter)

    finite_values = [value for value in per_node.values() if np.isfinite(value)]
    average_rtt = float(np.mean(finite_values)) if finite_values else float("inf")
    worst_rtt = float(np.max(finite_values)) if finite_values else float("inf")
    return SimulationResult(average_rtt_ms=average_rtt, worst_rtt_ms=worst_rtt, per_node_latency_ms=per_node)


def _run_mininet_latency_simulation(
    graph: nx.Graph,
    controllers: list[str],
    base_link_delay_ms: float,
    ping_count: int,
    timeout_s: int,
) -> SimulationResult:
    """Build a Mininet topology from the graph and measure host RTTs."""
    try:
        TCLink = import_module("mininet.link").TCLink
        Mininet = import_module("mininet.net").Mininet
        OVSSwitch = import_module("mininet.node").OVSSwitch
        Topo = import_module("mininet.topo").Topo
    except Exception as exc:  # pragma: no cover - depends on host environment
        raise RuntimeError("Mininet is unavailable in this environment") from exc

    node_labels = [str(node) for node in graph.nodes]
    node_to_index = {node: idx for idx, node in enumerate(node_labels, start=1)}

    class GraphTopo(Topo):
        def build(self):
            for node in node_labels:
                idx = node_to_index[node]
                switch_name = f"s{idx}"
                host_name = f"h{idx}"
                self.addSwitch(switch_name, failMode="standalone")
                self.addHost(host_name)
                self.addLink(host_name, switch_name, cls=TCLink, delay="0.10ms")

            for u, v, data in graph.edges(data=True):
                delay_ms = max(0.10, float(data.get("weight", 1.0)) * base_link_delay_ms)
                self.addLink(
                    f"s{node_to_index[str(u)]}",
                    f"s{node_to_index[str(v)]}",
                    cls=TCLink,
                    delay=f"{delay_ms:.2f}ms",
                )

    net = Mininet(
        topo=GraphTopo(),
        switch=OVSSwitch,
        controller=None,
        autoSetMacs=True,
        build=False,
    )

    try:
        net.build()
        net.start()

        host_by_node = {
            node: net.get(f"h{node_to_index[node]}")
            for node in node_labels
        }

        missing_controllers = [controller for controller in controllers if controller not in host_by_node]
        if missing_controllers:
            raise ValueError(f"Controller nodes not found in graph: {missing_controllers}")

        per_node: dict[str, float] = {}
        for node in node_labels:
            if node in controllers:
                per_node[node] = 0.0
                continue

            src_host = host_by_node[node]
            best_rtt = float("inf")

            for controller in controllers:
                dst_host = host_by_node[controller]
                ping_output = src_host.cmd(
                    f"ping -c {ping_count} -W {timeout_s} {dst_host.IP()}"
                )
                avg_rtt = _parse_ping_avg_ms(ping_output)
                if avg_rtt is None:
                    continue
                best_rtt = min(best_rtt, avg_rtt)

            per_node[node] = best_rtt

        finite_values = [value for value in per_node.values() if np.isfinite(value)]
        average_rtt = float(np.mean(finite_values)) if finite_values else float("inf")
        worst_rtt = float(np.max(finite_values)) if finite_values else float("inf")
        return SimulationResult(
            average_rtt_ms=average_rtt,
            worst_rtt_ms=worst_rtt,
            per_node_latency_ms=per_node,
        )
    finally:  # pragma: no cover - depends on host environment
        try:
            net.stop()
        except Exception:
            pass


def run_mininet_simulation(
    graph: nx.Graph,
    controllers: Iterable[str],
    base_link_delay_ms: float = 2.0,
    jitter_ms: float = 0.5,
    seed: int | None = 42,
    ping_count: int = 2,
    timeout_s: int = 1,
    fallback_to_synthetic: bool = True,
) -> SimulationResult:
    """
    Run Mininet-backed RTT simulation.

    Falls back to synthetic latency simulation if Mininet is unavailable or execution fails,
    unless fallback_to_synthetic is False.
    """
    controller_list = [str(controller) for controller in controllers]
    if not controller_list:
        raise ValueError("controllers must not be empty")

    try:
        return _run_mininet_latency_simulation(
            graph=graph,
            controllers=controller_list,
            base_link_delay_ms=base_link_delay_ms,
            ping_count=ping_count,
            timeout_s=timeout_s,
        )
    except Exception as exc:
        if not fallback_to_synthetic:
            raise

        warnings.warn(
            f"Mininet simulation unavailable ({exc}). Falling back to synthetic simulation.",
            RuntimeWarning,
            stacklevel=2,
        )
        return run_synthetic_latency_simulation(
            graph=graph,
            controllers=controller_list,
            base_link_delay_ms=base_link_delay_ms,
            jitter_ms=jitter_ms,
            seed=seed,
        )
