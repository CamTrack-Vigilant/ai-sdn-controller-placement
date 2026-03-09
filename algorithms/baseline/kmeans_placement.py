from __future__ import annotations

from typing import List

import networkx as nx
import numpy as np
from sklearn.cluster import KMeans


def _node_coordinates(graph: nx.Graph) -> tuple[list[str], np.ndarray]:
    nodes = list(graph.nodes)
    if all("x" in graph.nodes[node] and "y" in graph.nodes[node] for node in nodes):
        coords = np.array([[graph.nodes[node]["x"], graph.nodes[node]["y"]] for node in nodes], dtype=float)
    else:
        layout = nx.spring_layout(graph, seed=42)
        coords = np.array([layout[node] for node in nodes], dtype=float)
    return nodes, coords


def kmeans_controller_placement(
    graph: nx.Graph,
    num_controllers: int,
    random_state: int | None = 42,
) -> List[str]:
    if num_controllers <= 0:
        raise ValueError("num_controllers must be greater than zero")

    if num_controllers > graph.number_of_nodes():
        raise ValueError("num_controllers cannot exceed number of nodes")

    nodes, coords = _node_coordinates(graph)

    model = KMeans(n_clusters=num_controllers, n_init=10, random_state=random_state)
    model.fit(coords)

    placements: list[str] = []
    for centroid in model.cluster_centers_:
        distances = np.linalg.norm(coords - centroid, axis=1)
        for idx in np.argsort(distances):
            candidate = nodes[int(idx)]
            if candidate not in placements:
                placements.append(candidate)
                break

    return placements
