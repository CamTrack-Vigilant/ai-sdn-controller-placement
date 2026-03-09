from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Dict, Optional, Tuple

import networkx as nx
import numpy as np


@dataclass(frozen=True)
class TopologyConfig:
    num_sites: int = 4
    nodes_per_site: int = 12
    intra_site_degree: int = 4
    rewiring_prob: float = 0.2
    inter_site_links: int = 2
    seed: Optional[int] = 42


def _site_center(site_index: int, num_sites: int, radius: float = 100.0) -> Tuple[float, float]:
    angle = (2.0 * math.pi * site_index) / max(1, num_sites)
    return radius * math.cos(angle), radius * math.sin(angle)


def _normalized_degree(nodes_per_site: int, requested_degree: int) -> int:
    degree = max(2, requested_degree)
    degree = min(degree, nodes_per_site - 1)
    if degree % 2 != 0:
        degree -= 1
    return max(2, degree)


def generate_multi_site_topology(config: TopologyConfig) -> nx.Graph:
    """Generate a connected multi-site topology with weighted links."""
    rng = random.Random(config.seed)
    np_rng = np.random.default_rng(config.seed)

    graph = nx.Graph()
    nodes_by_site: Dict[int, list[str]] = {}

    for site in range(config.num_sites):
        center_x, center_y = _site_center(site, config.num_sites)

        if config.nodes_per_site < 4:
            local_graph = nx.complete_graph(config.nodes_per_site)
        else:
            local_graph = nx.connected_watts_strogatz_graph(
                n=config.nodes_per_site,
                k=_normalized_degree(config.nodes_per_site, config.intra_site_degree),
                p=config.rewiring_prob,
                seed=rng.randint(0, 10**9),
            )

        mapping = {node: f"s{site}-n{node}" for node in local_graph.nodes}
        local_graph = nx.relabel_nodes(local_graph, mapping)
        site_nodes = list(local_graph.nodes)
        nodes_by_site[site] = site_nodes

        for node in site_nodes:
            graph.add_node(
                node,
                site=site,
                x=float(center_x + np_rng.normal(0.0, 8.0)),
                y=float(center_y + np_rng.normal(0.0, 8.0)),
            )

        for u, v in local_graph.edges:
            graph.add_edge(u, v, weight=rng.uniform(0.8, 1.6), link_type="intra_site")

    for site in range(config.num_sites):
        next_site = (site + 1) % config.num_sites
        left_nodes = nodes_by_site[site]
        right_nodes = nodes_by_site[next_site]

        links_added = 0
        attempts = 0
        max_attempts = max(10, config.inter_site_links * 10)

        while links_added < config.inter_site_links and attempts < max_attempts:
            u = rng.choice(left_nodes)
            v = rng.choice(right_nodes)
            attempts += 1
            if graph.has_edge(u, v):
                continue
            graph.add_edge(u, v, weight=rng.uniform(1.8, 3.8), link_type="inter_site")
            links_added += 1

    return graph


def get_node_positions(graph: nx.Graph) -> Dict[str, Tuple[float, float]]:
    """Return node coordinates from attributes, or compute a fallback layout."""
    if all("x" in graph.nodes[node] and "y" in graph.nodes[node] for node in graph.nodes):
        return {
            str(node): (float(graph.nodes[node]["x"]), float(graph.nodes[node]["y"]))
            for node in graph.nodes
        }

    layout = nx.spring_layout(graph, seed=42)
    return {str(node): (float(pos[0]), float(pos[1])) for node, pos in layout.items()}


def summarize_topology(graph: nx.Graph) -> dict:
    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "connected": nx.is_connected(graph),
        "density": nx.density(graph),
    }


if __name__ == "__main__":
    topology = generate_multi_site_topology(TopologyConfig())
    print(summarize_topology(topology))
