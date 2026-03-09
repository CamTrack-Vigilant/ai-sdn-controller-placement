from __future__ import annotations

import random
from typing import List, Tuple

import networkx as nx


def _placement_score(
    all_pairs: dict,
    nodes: list[str],
    placement: Tuple[str, ...],
) -> float:
    total_distance = 0.0
    for node in nodes:
        total_distance += min(all_pairs[node].get(controller, float("inf")) for controller in placement)
    avg_distance = total_distance / len(nodes)
    return -avg_distance


def _crossover(
    parent_a: Tuple[str, ...],
    parent_b: Tuple[str, ...],
    num_controllers: int,
    nodes: list[str],
    rng: random.Random,
) -> Tuple[str, ...]:
    if num_controllers == 1:
        return parent_a

    split = rng.randint(1, num_controllers - 1)
    child = list(parent_a[:split])
    for gene in parent_b:
        if gene not in child:
            child.append(gene)
        if len(child) == num_controllers:
            break

    if len(child) < num_controllers:
        remaining = [node for node in nodes if node not in child]
        rng.shuffle(remaining)
        child.extend(remaining[: num_controllers - len(child)])

    return tuple(sorted(child))


def _mutate(
    individual: Tuple[str, ...],
    mutation_rate: float,
    nodes: list[str],
    rng: random.Random,
) -> Tuple[str, ...]:
    if rng.random() >= mutation_rate:
        return individual

    genes = list(individual)
    replace_idx = rng.randrange(len(genes))
    options = [node for node in nodes if node not in genes]
    if options:
        genes[replace_idx] = rng.choice(options)
    return tuple(sorted(genes))


def genetic_controller_placement(
    graph: nx.Graph,
    num_controllers: int,
    population_size: int = 40,
    generations: int = 50,
    mutation_rate: float = 0.15,
    tournament_size: int = 3,
    seed: int | None = 42,
) -> List[str]:
    if num_controllers <= 0:
        raise ValueError("num_controllers must be greater than zero")

    nodes = list(graph.nodes)
    if num_controllers > len(nodes):
        raise ValueError("num_controllers cannot exceed number of nodes")

    rng = random.Random(seed)
    all_pairs = dict(nx.all_pairs_dijkstra_path_length(graph, weight="weight"))

    population = [tuple(sorted(rng.sample(nodes, num_controllers))) for _ in range(population_size)]

    for _ in range(generations):
        scores = {individual: _placement_score(all_pairs, nodes, individual) for individual in population}
        elite = max(population, key=lambda individual: scores[individual])

        new_population = [elite]
        while len(new_population) < population_size:
            contenders_a = rng.sample(population, min(tournament_size, len(population)))
            contenders_b = rng.sample(population, min(tournament_size, len(population)))
            parent_a = max(contenders_a, key=lambda individual: scores[individual])
            parent_b = max(contenders_b, key=lambda individual: scores[individual])

            child = _crossover(parent_a, parent_b, num_controllers, nodes, rng)
            child = _mutate(child, mutation_rate, nodes, rng)
            new_population.append(child)

        population = new_population

    final_scores = {individual: _placement_score(all_pairs, nodes, individual) for individual in population}
    best = max(population, key=lambda individual: final_scores[individual])
    return list(best)
