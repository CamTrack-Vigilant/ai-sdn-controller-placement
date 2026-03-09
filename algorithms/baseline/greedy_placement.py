from __future__ import annotations

from typing import List

import networkx as nx


def greedy_k_center_placement(graph: nx.Graph, num_controllers: int) -> List[str]:
    """Farthest-first greedy placement (k-center style)."""
    if num_controllers <= 0:
        raise ValueError("num_controllers must be greater than zero")

    nodes = list(graph.nodes)
    if num_controllers > len(nodes):
        raise ValueError("num_controllers cannot exceed number of nodes")

    first_controller = max(nodes, key=lambda n: graph.degree[n])
    controllers = [first_controller]

    while len(controllers) < num_controllers:
        distances = nx.multi_source_dijkstra_path_length(graph, controllers, weight="weight")

        candidate = None
        farthest_distance = -1.0
        for node in nodes:
            if node in controllers:
                continue
            node_distance = distances.get(node, float("inf"))
            if node_distance > farthest_distance:
                farthest_distance = node_distance
                candidate = node

        if candidate is None:
            break
        controllers.append(candidate)

    return controllers
