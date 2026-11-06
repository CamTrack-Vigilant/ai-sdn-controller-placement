from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
import itertools
import json
import math
from pathlib import Path
import random
import time
from typing import List, Tuple

import networkx as nx
import numpy as np

from evaluation.metrics import (
    average_controller_distance,
    control_plane_reliability_single_link_failure,
    control_plane_reliability_single_link_failure_cached,
)


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
    return_metadata: bool = False,
) -> List[str] | tuple[List[str], dict[str, int | float | None]]:
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
    best_reward_history: list[float] = []
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
        best_reward_history.append(best_reward)
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
    convergence_episode = next(
        (
            index + 1
            for index, reward in enumerate(best_reward_history)
            if best_reward - reward <= 1e-12
        ),
        None,
    )

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

    if return_metadata:
        return list(best_action), {
            "iterations_budget": int(episodes),
            "convergence_iteration": convergence_episode,
            "final_best_reward": float(best_reward),
            "num_actions": int(len(action_list)),
        }

    return list(best_action)


def dqn_controller_placement(
    graph: nx.Graph,
    num_controllers: int,
    episodes: int = 200,
    learning_rate: float = 0.001,
    gamma: float = 0.99,
    batch_size: int = 32,
    replay_capacity: int = 10000,
    epsilon_start: float = 1.0,
    epsilon_end: float = 0.05,
    epsilon_decay: float = 0.995,
    seed: int = 42,
    return_metadata: bool = False,
) -> List[str] | Tuple[List[str], dict]:
    """
    Multi-controller PyTorch Deep Q-Network (DQN) placement algorithm.
    Architecture: MLP Input(N) -> Linear(64, ReLU) -> Linear(64, ReLU) -> Output(N).
    Selects k distinct controller nodes sequentially per episode and evaluates both
    offline training time (s) and online single forward-pass inference latency (ms).
    """
    import torch
    import torch.nn as nn
    import torch.optim as optim

    if num_controllers <= 0:
        raise ValueError("num_controllers must be greater than zero")
    nodes = list(graph.nodes)
    num_nodes = len(nodes)
    if num_controllers > num_nodes:
        raise ValueError("num_controllers cannot exceed number of nodes")

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    device = torch.device("cpu")

    class _DQN(nn.Module):
        def __init__(self, n_in: int, n_out: int):
            super().__init__()
            self.fc1 = nn.Linear(n_in, 64)
            self.fc2 = nn.Linear(64, 64)
            self.fc3 = nn.Linear(64, n_out)
            self.relu = nn.ReLU()

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.fc3(self.relu(self.fc2(self.relu(self.fc1(x)))))

    q_net = _DQN(num_nodes, num_nodes).to(device)
    target_net = _DQN(num_nodes, num_nodes).to(device)
    target_net.load_state_dict(q_net.state_dict())
    optimizer = optim.Adam(q_net.parameters(), lr=learning_rate)
    loss_fn = nn.MSELoss()
    replay_buffer: deque = deque(maxlen=replay_capacity)

    # Precompute worst-case single-node distance for normalized reward scaling
    all_pairs = dict(nx.all_pairs_dijkstra_path_length(graph, weight="weight"))
    max_avg_dist = max(
        float(np.mean(list(dist_map.values()))) for dist_map in all_pairs.values()
    )
    max_avg_dist = max(max_avg_dist, 1e-6)

    # Structural feature vector (normalized degree centrality) blended with placement mask
    degrees = np.array([graph.degree[n] for n in nodes], dtype=np.float32)
    norm_degrees = degrees / max(float(np.max(degrees)), 1.0)

    epsilon = epsilon_start
    best_controllers: List[str] = nodes[:num_controllers]
    best_reward = float("-inf")
    update_steps = 0

    t_train_start = time.perf_counter()
    for _ in range(episodes):
        selected_indices: List[int] = []
        mask = np.zeros(num_nodes, dtype=np.float32)
        state = norm_degrees.copy()

        for step_idx in range(num_controllers):
            available = [i for i in range(num_nodes) if i not in selected_indices]
            if random.random() < epsilon:
                action = random.choice(available)
            else:
                with torch.no_grad():
                    s_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
                    q_vals = q_net(s_tensor).squeeze(0).cpu().numpy()
                    q_vals[selected_indices] = -1e9
                    action = int(np.argmax(q_vals))

            selected_indices.append(action)
            mask[action] = 1.0
            next_state = 0.5 * norm_degrees + 0.5 * mask
            done = step_idx == (num_controllers - 1)

            current_nodes = [nodes[i] for i in selected_indices]
            avg_lat = _average_distance_from_all_pairs(all_pairs, nodes, tuple(current_nodes))
            rel = control_plane_reliability_single_link_failure_cached(graph, current_nodes)
            reward = float(10.0 * ((max_avg_dist - avg_lat) / max_avg_dist) + 5.0 * rel)

            if done and reward > best_reward:
                best_reward = reward
                best_controllers = list(current_nodes)

            replay_buffer.append((state, action, reward, next_state, float(done)))
            state = next_state

            if len(replay_buffer) >= batch_size:
                batch = random.sample(replay_buffer, batch_size)
                b_s, b_a, b_r, b_ns, b_d = zip(*batch)
                s_t = torch.tensor(np.array(b_s), dtype=torch.float32, device=device)
                a_t = torch.tensor(b_a, dtype=torch.int64, device=device)
                r_t = torch.tensor(b_r, dtype=torch.float32, device=device)
                ns_t = torch.tensor(np.array(b_ns), dtype=torch.float32, device=device)
                d_t = torch.tensor(b_d, dtype=torch.float32, device=device)

                q_pred = q_net(s_t).gather(1, a_t.unsqueeze(1)).squeeze(1)
                with torch.no_grad():
                    q_next = target_net(ns_t).max(dim=1)[0]
                    q_target = r_t + (1.0 - d_t) * gamma * q_next

                loss = loss_fn(q_pred, q_target)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                update_steps += 1
                if update_steps % 100 == 0:
                    target_net.load_state_dict(q_net.state_dict())

        epsilon = max(epsilon_end, epsilon * epsilon_decay)

    training_time_sec = time.perf_counter() - t_train_start

    # Measure online single forward-pass inference latency (top-k Q-value selection)
    q_net.eval()
    eval_state = torch.tensor(norm_degrees, dtype=torch.float32, device=device).unsqueeze(0)
    with torch.no_grad():
        for _ in range(10):
            _ = torch.topk(q_net(eval_state), k=num_controllers, dim=1)
        t_inf_start = time.perf_counter()
        for _ in range(100):
            topk_indices = torch.topk(q_net(eval_state), k=num_controllers, dim=1).indices.squeeze(0)
        inference_time_ms = ((time.perf_counter() - t_inf_start) / 100.0) * 1000.0

    inferred_controllers = [nodes[int(i)] for i in topk_indices.tolist()]
    inferred_lat = _average_distance_from_all_pairs(all_pairs, nodes, tuple(inferred_controllers))
    inferred_rel = control_plane_reliability_single_link_failure_cached(graph, inferred_controllers)
    inferred_reward = float(10.0 * ((max_avg_dist - inferred_lat) / max_avg_dist) + 5.0 * inferred_rel)
    if inferred_reward >= best_reward:
        best_controllers = inferred_controllers

    if return_metadata:
        return best_controllers, {
            "episodes": episodes,
            "training_time_sec": float(training_time_sec),
            "omega_sec_per_episode": float(training_time_sec / max(episodes, 1)),
            "inference_time_ms": float(inference_time_ms),
            "final_best_reward": float(max(best_reward, inferred_reward)),
        }
    return best_controllers

