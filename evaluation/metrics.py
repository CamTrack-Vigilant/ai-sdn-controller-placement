from __future__ import annotations

from hashlib import sha256
from typing import Any, Dict, Iterable

import networkx as nx
import numpy as np


def _match_controllers(graph: nx.Graph, controllers: Iterable[Any]) -> list:
    """Return a list of controller node objects that exist in `graph`.

    Tries to match controllers to the graph's node objects using several
    strategies so callers may pass ints or strings interchangeably.
    """
    nodes_set = set(graph.nodes())

    # 1) Direct match
    matched = [c for c in controllers if c in nodes_set]
    if matched:
        return matched

    # 2) Match by stringified node labels -> return original node objects
    str_to_node = {str(n): n for n in graph.nodes()}
    matched = [str_to_node[s] for s in map(str, controllers) if s in str_to_node]
    if matched:
        return matched

    # 3) Try int conversion for string-like controllers
    matched = []
    for c in controllers:
        try:
            num = int(c)
        except Exception:
            continue
        if num in nodes_set:
            matched.append(num)
    return matched


# Global reliability cache keyed by topology fingerprint.
# Each entry stores component-label matrices for all single-link failure states.
RELIABILITY_CACHE: dict[str, dict[str, Any]] = {}


def _topology_key(graph: nx.Graph) -> str:
    """Build a stable cache key from sorted nodes and edges."""
    nodes = tuple(sorted(str(node) for node in graph.nodes()))
    edges = tuple(
        sorted(
            (min(str(u), str(v)), max(str(u), str(v)))
            for u, v in graph.edges()
        )
    )
    payload = repr((nodes, edges)).encode("utf-8")
    return sha256(payload).hexdigest()


def precompute_reliability_cache(graph: nx.Graph) -> str:
    """
    Precompute N-1 failure connectivity labels for a topology exactly once.

    Cached structure:
      - node_order: list[str]
      - node_index: dict[str, int]
      - edge_order: list[tuple[node, node]]
      - component_labels: np.ndarray[int32] shape (num_edges, num_nodes)
    """
    cache_key = _topology_key(graph)
    if cache_key in RELIABILITY_CACHE:
        return cache_key

    node_order = [str(node) for node in graph.nodes()]
    node_index = {node: idx for idx, node in enumerate(node_order)}
    edge_order = list(graph.edges())

    num_edges = len(edge_order)
    num_nodes = len(node_order)
    component_labels = np.full((num_edges, num_nodes), -1, dtype=np.int32)

    for edge_idx, (edge_u, edge_v) in enumerate(edge_order):
        failed_graph = graph.copy()
        failed_graph.remove_edge(edge_u, edge_v)

        for comp_id, component in enumerate(nx.connected_components(failed_graph)):
            for node in component:
                component_labels[edge_idx, node_index[str(node)]] = comp_id

    RELIABILITY_CACHE[cache_key] = {
        "node_order": node_order,
        "node_index": node_index,
        "edge_order": edge_order,
        "component_labels": component_labels,
    }
    return cache_key


def _distance_map(graph: nx.Graph, controllers: Iterable[Any]) -> Dict[str, float]:
    sources = _match_controllers(graph, controllers)
    if not sources:
        return {}
    return {str(node): distance for node, distance in nx.multi_source_dijkstra_path_length(graph, sources, weight="weight").items()}


def average_controller_distance(graph: nx.Graph, controllers: Iterable[str]) -> float:
    controller_list = _match_controllers(graph, controllers)
    if not controller_list:
        return float("inf")

    distances = _distance_map(graph, controller_list)
    values = [distances.get(str(node), float("inf")) for node in graph.nodes]
    finite_values = [value for value in values if np.isfinite(value)]
    return float(np.mean(finite_values)) if finite_values else float("inf")


def worst_case_controller_distance(graph: nx.Graph, controllers: Iterable[str]) -> float:
    controller_list = _match_controllers(graph, controllers)
    if not controller_list:
        return float("inf")

    distances = _distance_map(graph, controller_list)
    values = [distances.get(str(node), float("inf")) for node in graph.nodes]
    finite_values = [value for value in values if np.isfinite(value)]
    return float(np.max(finite_values)) if finite_values else float("inf")


def controller_load_std(graph: nx.Graph, controllers: Iterable[str]) -> float:
    controller_list = _match_controllers(graph, controllers)
    if not controller_list:
        return float("inf")

    controller_distances = {
        controller: nx.single_source_dijkstra_path_length(graph, controller, weight="weight")
        for controller in controller_list
    }

    loads = {controller: 0 for controller in controller_list}
    for node in graph.nodes:
        best_controller = min(
            controller_list,
            key=lambda controller: controller_distances[controller].get(node, float("inf")),
        )
        loads[best_controller] += 1

    return float(np.std(list(loads.values())))


def resilience_ratio_single_failure(graph: nx.Graph, controllers: Iterable[str]) -> float:
    """Average degradation ratio after one controller failure at a time."""
    controller_list = _match_controllers(graph, controllers)
    if len(controller_list) <= 1:
        return 1.0

    baseline = average_controller_distance(graph, controller_list)
    if not np.isfinite(baseline) or baseline == 0:
        return float("inf")

    degradations = []
    for failed in controller_list:
        remaining = [controller for controller in controller_list if controller != failed]
        degraded = average_controller_distance(graph, remaining)
        degradations.append(degraded / baseline)

    return float(np.mean(degradations))


def control_plane_reliability_single_link_failure(
    graph: nx.Graph,
    controllers: Iterable[str],
) -> float:
    """
    Estimate control-plane reliability under single-link failures.

    For each edge failure, compute the fraction of nodes that can still reach at
    least one controller. Return the mean fraction across all single-link failures.
    A value of 1.0 means all nodes remain controller-reachable for every edge loss.
    """
    controller_list = _match_controllers(graph, controllers)
    if not controller_list:
        return 0.0

    if graph.number_of_nodes() == 0:
        return 1.0

    if graph.number_of_edges() == 0:
        reachable_without_failures = nx.multi_source_dijkstra_path_length(
            graph,
            controller_list,
            weight="weight",
        )
        return float(len(reachable_without_failures) / graph.number_of_nodes())

    reachability_ratios: list[float] = []
    for edge_u, edge_v in graph.edges:
        failed_graph = graph.copy()
        failed_graph.remove_edge(edge_u, edge_v)

        reachable = nx.multi_source_dijkstra_path_length(
            failed_graph,
            controller_list,
            weight="weight",
        )
        reachability_ratios.append(len(reachable) / graph.number_of_nodes())

    return float(np.mean(reachability_ratios))


def control_plane_reliability_single_link_failure_cached(
    graph: nx.Graph,
    controllers: Iterable[str],
) -> float:
    """
    Cached N-1 reliability query using precomputed component labels.

    This avoids per-call graph copying and shortest-path recomputation by turning
    reliability evaluation into vectorized NumPy operations.
    """
    controller_list = [str(controller) for controller in controllers]
    if not controller_list:
        return 0.0

    if graph.number_of_nodes() == 0:
        return 1.0

    # Preserve original edge-case behavior for edgeless graphs.
    if graph.number_of_edges() == 0:
        unique_controllers = {str(controller) for controller in controller_list}
        return float(len(unique_controllers & {str(node) for node in graph.nodes()}) / graph.number_of_nodes())

    cache_key = precompute_reliability_cache(graph)
    cache_entry = RELIABILITY_CACHE[cache_key]
    node_index = cache_entry["node_index"]
    component_labels: np.ndarray = cache_entry["component_labels"]

    controller_idx = [node_index[node] for node in controller_list if node in node_index]
    if not controller_idx:
        return 0.0

    # labels shape: (E, N), controller labels shape: (E, K)
    controller_labels = component_labels[:, controller_idx]
    reachable_mask = (component_labels[:, :, None] == controller_labels[:, None, :]).any(axis=2)

    # For each edge-failure row, reachable ratio is fraction of reachable nodes.
    per_failure_ratio = reachable_mask.mean(axis=1)
    return float(np.mean(per_failure_ratio))


def assert_cache_parity(
    graph: nx.Graph,
    controllers: Iterable[str],
    tolerance: float = 1e-9,
) -> float:
    """Assert cached and non-cached reliability computations match within tolerance."""
    baseline = control_plane_reliability_single_link_failure(graph, controllers)
    cached = control_plane_reliability_single_link_failure_cached(graph, controllers)
    delta = abs(baseline - cached)
    if delta > tolerance:
        raise AssertionError(
            f"Reliability cache parity check failed: baseline={baseline:.12f}, "
            f"cached={cached:.12f}, delta={delta:.12f}, tolerance={tolerance}"
        )
    return delta


def summarize_metrics(
    graph: nx.Graph,
    controllers: Iterable[str],
    use_cached_reliability: bool = True,
) -> Dict[str, float]:
    controller_list = list(controllers)
    reliability_fn = (
        control_plane_reliability_single_link_failure_cached
        if use_cached_reliability
        else control_plane_reliability_single_link_failure
    )
    return {
        "average_distance": average_controller_distance(graph, controller_list),
        "worst_case_distance": worst_case_controller_distance(graph, controller_list),
        "controller_load_std": controller_load_std(graph, controller_list),
        "resilience_ratio": resilience_ratio_single_failure(graph, controller_list),
        "control_plane_reliability": reliability_fn(graph, controller_list),
    }
