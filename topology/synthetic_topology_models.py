from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Literal

import networkx as nx


SyntheticModel = Literal["barabasi_albert", "waxman"]


@dataclass(frozen=True)
class SyntheticTopologyConfig:
    model: SyntheticModel = "barabasi_albert"
    num_nodes: int = 50
    seed: int | None = 42
    ba_m: int = 2
    waxman_alpha: float = 0.4
    waxman_beta: float = 0.1
    max_regeneration_attempts: int = 24


def _edge_weight_from_coordinates(
    graph: nx.Graph,
    node_u: str,
    node_v: str,
    min_weight: float = 0.05,
    scale: float = 10.0,
) -> float:
    ux = float(graph.nodes[node_u].get("x", 0.0))
    uy = float(graph.nodes[node_u].get("y", 0.0))
    vx = float(graph.nodes[node_v].get("x", 0.0))
    vy = float(graph.nodes[node_v].get("y", 0.0))
    euclidean = math.hypot(ux - vx, uy - vy)
    return max(min_weight, euclidean * scale)


def _set_weighted_edges_from_coordinates(graph: nx.Graph) -> None:
    for node_u, node_v in graph.edges:
        graph.edges[node_u, node_v]["weight"] = _edge_weight_from_coordinates(graph, node_u, node_v)


def _closest_inter_component_edge(
    graph: nx.Graph,
    component_a: set[str],
    component_b: set[str],
) -> tuple[str, str, float]:
    best_u = None
    best_v = None
    best_distance = float("inf")

    for node_u in component_a:
        ux = float(graph.nodes[node_u].get("x", 0.0))
        uy = float(graph.nodes[node_u].get("y", 0.0))
        for node_v in component_b:
            vx = float(graph.nodes[node_v].get("x", 0.0))
            vy = float(graph.nodes[node_v].get("y", 0.0))
            distance = math.hypot(ux - vx, uy - vy)
            if distance < best_distance:
                best_distance = distance
                best_u = node_u
                best_v = node_v

    if best_u is None or best_v is None:
        raise RuntimeError("Unable to bridge disconnected components")

    return best_u, best_v, best_distance


def _ensure_connected(graph: nx.Graph) -> nx.Graph:
    if graph.number_of_nodes() == 0 or nx.is_connected(graph):
        return graph

    graph = graph.copy()
    components = [set(component) for component in nx.connected_components(graph)]
    components.sort(key=len, reverse=True)

    anchor = components[0]
    for next_component in components[1:]:
        node_u, node_v, _ = _closest_inter_component_edge(graph, anchor, next_component)
        graph.add_edge(node_u, node_v, link_type="bridge")
        anchor = anchor.union(next_component)

    _set_weighted_edges_from_coordinates(graph)
    return graph


def generate_barabasi_albert_topology(
    num_nodes: int,
    seed: int | None = 42,
    ba_m: int = 2,
) -> nx.Graph:
    if num_nodes < 2:
        raise ValueError("num_nodes must be at least 2")

    attachment_degree = max(1, min(ba_m, num_nodes - 1))
    base_graph = nx.barabasi_albert_graph(num_nodes, attachment_degree, seed=seed)

    spring_seed = seed if seed is not None else 42
    layout = nx.spring_layout(base_graph, seed=spring_seed)

    graph = nx.Graph()
    for node in base_graph.nodes:
        x, y = layout[node]
        graph.add_node(f"n{node}", x=float(x), y=float(y), topology_model="barabasi_albert")

    for node_u, node_v in base_graph.edges:
        graph.add_edge(f"n{node_u}", f"n{node_v}", link_type="model")

    _set_weighted_edges_from_coordinates(graph)
    return graph


def generate_waxman_topology(
    num_nodes: int,
    seed: int | None = 42,
    alpha: float = 0.4,
    beta: float = 0.1,
    max_regeneration_attempts: int = 24,
) -> nx.Graph:
    if num_nodes < 2:
        raise ValueError("num_nodes must be at least 2")

    if alpha <= 0 or beta <= 0:
        raise ValueError("alpha and beta must be positive")

    for attempt in range(max_regeneration_attempts):
        attempt_seed = None if seed is None else seed + attempt
        base_graph = nx.waxman_graph(num_nodes, alpha=alpha, beta=beta, seed=attempt_seed)

        graph = nx.Graph()
        for node, data in base_graph.nodes(data=True):
            pos = data.get("pos") or (0.0, 0.0)
            graph.add_node(
                f"n{node}",
                x=float(pos[0]),
                y=float(pos[1]),
                topology_model="waxman",
            )

        for node_u, node_v in base_graph.edges:
            graph.add_edge(f"n{node_u}", f"n{node_v}", link_type="model")

        graph = _ensure_connected(graph)
        if nx.is_connected(graph):
            return graph

    raise RuntimeError("Failed to generate a connected Waxman topology")


def generate_synthetic_topology(config: SyntheticTopologyConfig) -> nx.Graph:
    if config.model == "barabasi_albert":
        return generate_barabasi_albert_topology(
            num_nodes=config.num_nodes,
            seed=config.seed,
            ba_m=config.ba_m,
        )

    if config.model == "waxman":
        return generate_waxman_topology(
            num_nodes=config.num_nodes,
            seed=config.seed,
            alpha=config.waxman_alpha,
            beta=config.waxman_beta,
            max_regeneration_attempts=config.max_regeneration_attempts,
        )

    raise ValueError(f"Unsupported synthetic model: {config.model}")
