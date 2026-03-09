from __future__ import annotations

from datetime import datetime, timezone
import itertools
import json
import math
from pathlib import Path
import random
from typing import List, Tuple

import networkx as nx

from evaluation.metrics import control_plane_reliability_single_link_failure


def _average_distance_from_all_pairs(
    all_pairs: dict,
    nodes: list[str],
    placement: Tuple[str, ...],
) -> float:
    total = 0.0
    for node in nodes:
        total += min(all_pairs[node].get(controller, float("inf")) for controller in placement)
    return total / len(nodes)


def _composite_reward(
    average_distance: float,
    reliability: float,
    latency_weight: float,
    reliability_weight: float,
) -> float:
    return -(latency_weight * average_distance) + (reliability_weight * reliability)


def _append_jsonl(log_path: str, records: list[dict]) -> None:
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")


def bandit_rl_controller_placement(
    graph: nx.Graph,
    num_controllers: int,
    episodes: int = 300,
    epsilon: float = 0.2,
    candidate_pool_size: int = 64,
    seed: int | None = 42,
    log_path: str | None = None,
    log_every: int = 25,
    run_label: str | None = None,
    latency_weight: float = 1.0,
    reliability_weight: float = 0.0,
) -> List[str]:
    """Epsilon-greedy bandit baseline for adaptive controller placement."""
    if num_controllers <= 0:
        raise ValueError("num_controllers must be greater than zero")

    if log_every <= 0:
        raise ValueError("log_every must be greater than zero")

    if latency_weight < 0:
        raise ValueError("latency_weight must be non-negative")

    if reliability_weight < 0:
        raise ValueError("reliability_weight must be non-negative")

    nodes = list(graph.nodes)
    if num_controllers > len(nodes):
        raise ValueError("num_controllers cannot exceed number of nodes")

    rng = random.Random(seed)
    all_pairs = dict(nx.all_pairs_dijkstra_path_length(graph, weight="weight"))

    sorted_by_degree = sorted(nodes, key=lambda node: graph.degree[node], reverse=True)
    actions: set[Tuple[str, ...]] = {tuple(sorted(sorted_by_degree[:num_controllers]))}

    max_unique_actions = math.comb(len(nodes), num_controllers)
    target_size = min(max_unique_actions, max(8, min(candidate_pool_size, len(nodes) * 4)))

    attempts = 0
    max_attempts = max(64, target_size * 20)
    while len(actions) < target_size:
        actions.add(tuple(sorted(rng.sample(nodes, num_controllers))))
        attempts += 1
        if attempts >= max_attempts:
            # Deterministic fallback avoids long collision tails near saturation.
            for combo in itertools.combinations(nodes, num_controllers):
                actions.add(tuple(sorted(combo)))
                if len(actions) >= target_size:
                    break
            break

    action_list = list(actions)

    action_avg_distances = {
        action: _average_distance_from_all_pairs(all_pairs, nodes, action)
        for action in action_list
    }
    action_reliabilities = {
        action: control_plane_reliability_single_link_failure(graph, action)
        for action in action_list
    }
    action_rewards = {
        action: _composite_reward(
            average_distance=action_avg_distances[action],
            reliability=action_reliabilities[action],
            latency_weight=latency_weight,
            reliability_weight=reliability_weight,
        )
        for action in action_list
    }

    q_values = {action: 0.0 for action in action_list}
    visits = {action: 0 for action in action_list}

    run_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')}-{rng.randint(0, 999999):06d}"
    effective_label = run_label or "bandit_rl"
    epsilon_value = epsilon
    best_reward = float("-inf")
    event_records: list[dict] = []

    if log_path:
        event_records.append(
            {
                "event": "run_start",
                "run_id": run_id,
                "label": effective_label,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "num_nodes": len(nodes),
                "num_actions": len(action_list),
                "num_controllers": num_controllers,
                "episodes": episodes,
                "epsilon_start": epsilon,
                "seed": seed,
                "latency_weight": latency_weight,
                "reliability_weight": reliability_weight,
            }
        )

    for episode in range(1, episodes + 1):
        if rng.random() < epsilon_value:
            action = rng.choice(action_list)
        else:
            action = max(action_list, key=lambda a: q_values[a])

        reward = action_rewards[action]
        best_reward = max(best_reward, reward)
        visits[action] += 1
        q_values[action] += (reward - q_values[action]) / visits[action]
        epsilon_value = max(0.01, epsilon_value * 0.995)

        if log_path and (episode == 1 or episode == episodes or episode % log_every == 0):
            event_records.append(
                {
                    "event": "episode",
                    "run_id": run_id,
                    "label": effective_label,
                    "episode": episode,
                    "reward": reward,
                    "best_reward": best_reward,
                    "epsilon": epsilon_value,
                    "selected_action": list(action),
                    "selected_action_avg_distance": action_avg_distances[action],
                    "selected_action_reliability": action_reliabilities[action],
                    "selected_action_q": q_values[action],
                    "selected_action_visits": visits[action],
                }
            )

    best_action = max(action_list, key=lambda action: q_values[action])

    if log_path:
        top_actions = sorted(action_list, key=lambda action: q_values[action], reverse=True)[:5]
        event_records.append(
            {
                "event": "run_end",
                "run_id": run_id,
                "label": effective_label,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "final_epsilon": epsilon_value,
                "best_action": list(best_action),
                "best_action_q": q_values[best_action],
                "best_action_avg_distance": action_avg_distances[best_action],
                "best_action_reliability": action_reliabilities[best_action],
                "top_actions": [
                    {
                        "controllers": list(action),
                        "q_value": q_values[action],
                        "average_distance": action_avg_distances[action],
                        "reliability": action_reliabilities[action],
                        "reward": action_rewards[action],
                        "visits": visits[action],
                    }
                    for action in top_actions
                ],
            }
        )
        _append_jsonl(log_path, event_records)

    return list(best_action)
