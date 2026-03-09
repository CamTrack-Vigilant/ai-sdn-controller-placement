from __future__ import annotations

from typing import Dict, Iterable

import networkx as nx
import numpy as np


def _distance_map(graph: nx.Graph, controllers: list[str]) -> Dict[str, float]:
    return {str(node): distance for node, distance in nx.multi_source_dijkstra_path_length(graph, controllers, weight="weight").items()}


def average_controller_distance(graph: nx.Graph, controllers: Iterable[str]) -> float:
    controller_list = list(controllers)
    if not controller_list:
        return float("inf")

    distances = _distance_map(graph, controller_list)
    values = [distances.get(str(node), float("inf")) for node in graph.nodes]
    finite_values = [value for value in values if np.isfinite(value)]
    return float(np.mean(finite_values)) if finite_values else float("inf")


def worst_case_controller_distance(graph: nx.Graph, controllers: Iterable[str]) -> float:
    controller_list = list(controllers)
    if not controller_list:
        return float("inf")

    distances = _distance_map(graph, controller_list)
    values = [distances.get(str(node), float("inf")) for node in graph.nodes]
    finite_values = [value for value in values if np.isfinite(value)]
    return float(np.max(finite_values)) if finite_values else float("inf")


def controller_load_std(graph: nx.Graph, controllers: Iterable[str]) -> float:
    controller_list = list(controllers)
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
    controller_list = list(controllers)
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
    controller_list = [str(controller) for controller in controllers]
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


def summarize_metrics(graph: nx.Graph, controllers: Iterable[str]) -> Dict[str, float]:
    controller_list = list(controllers)
    return {
        "average_distance": average_controller_distance(graph, controller_list),
        "worst_case_distance": worst_case_controller_distance(graph, controller_list),
        "controller_load_std": controller_load_std(graph, controller_list),
        "resilience_ratio": resilience_ratio_single_failure(graph, controller_list),
        "control_plane_reliability": control_plane_reliability_single_link_failure(graph, controller_list),
    }
