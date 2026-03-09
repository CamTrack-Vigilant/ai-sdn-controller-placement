from __future__ import annotations

import random
from typing import List

import networkx as nx


def random_controller_placement(
    graph: nx.Graph,
    num_controllers: int,
    seed: int | None = None,
) -> List[str]:
    if num_controllers <= 0:
        raise ValueError("num_controllers must be greater than zero")

    nodes = list(graph.nodes)
    if num_controllers > len(nodes):
        raise ValueError("num_controllers cannot exceed number of nodes")

    rng = random.Random(seed)
    return rng.sample(nodes, num_controllers)
