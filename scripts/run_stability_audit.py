#!/usr/bin/env python3
"""
Phase 5 Stability Audit Protocol

Runs fixed-hyperparameter DQN stability experiments over:
  - Topologies: Internet2, ATT-MPLS
  - Seeds: [42, 123, 256, 512, 1024]
  - Episodes: 1000

Outputs:
  - Episode logs (JSONL)
  - Run summaries (CSV + JSON)

This script is graph-only by design (Phase 5), with no Mininet dependency.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import time
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim

PROJECT_ROOT = Path(__file__).resolve().parents[1]

import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from evaluation.metrics import (  # noqa: E402
    average_controller_distance,
    control_plane_reliability_single_link_failure_cached,
    precompute_reliability_cache,
)
from topology.canonical_topologies import load_canonical_topology  # noqa: E402


FIXED_SEEDS = [42, 123, 256, 512, 1024]
FIXED_TOPOLOGIES = ["Internet2", "ATT-MPLS"]


@dataclass
class RunSummary:
    topology: str
    seed: int
    episodes: int
    learning_rate: float
    batch_size: int
    gamma: float
    rolling_mean_reward_last100: float
    reward_variance_last200: float
    final_best_reward: float
    final_epsilon: float
    normalized_action_entropy: float
    final_latency: float
    final_reliability: float
    final_omega_ms_per_episode: float
    divergence_flag: bool
    divergence_reason: str


class DQNetwork(nn.Module):
    def __init__(self, input_size: int, output_size: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, output_size),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class ReplayBuffer:
    def __init__(self, capacity: int):
        self.buffer: deque = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int, device: torch.device):
        batch_size = min(batch_size, len(self.buffer))
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            torch.tensor(np.array(states), dtype=torch.float32, device=device),
            torch.tensor(actions, dtype=torch.int64, device=device),
            torch.tensor(rewards, dtype=torch.float32, device=device),
            torch.tensor(np.array(next_states), dtype=torch.float32, device=device),
            torch.tensor(dones, dtype=torch.float32, device=device),
        )

    def __len__(self) -> int:
        return len(self.buffer)


class GraphPlacementEnv:
    def __init__(self, graph):
        self.graph = graph
        self.nodes = [str(n) for n in graph.nodes()]
        self.num_nodes = len(self.nodes)
        self.controller = self.nodes[0]
        self.steps = 0
        self.max_steps = 10

        self.max_latency = self._max_latency_baseline()
        precompute_reliability_cache(graph)

    def _max_latency_baseline(self) -> float:
        latencies = []
        for node in self.nodes:
            latencies.append(average_controller_distance(self.graph, [node]))
        finite = [v for v in latencies if np.isfinite(v)]
        return max(finite) if finite else 1.0

    def reset(self, rng: random.Random) -> np.ndarray:
        self.controller = rng.choice(self.nodes)
        self.steps = 0
        return self._state()

    def _state(self) -> np.ndarray:
        vec = np.zeros(self.num_nodes, dtype=np.float32)
        vec[self.nodes.index(self.controller)] = 1.0
        return vec

    def step(self, action_idx: int) -> tuple[np.ndarray, float, bool, dict[str, float]]:
        self.steps += 1
        if 0 <= action_idx < self.num_nodes:
            self.controller = self.nodes[action_idx]

        latency = average_controller_distance(self.graph, [self.controller])
        latency_norm = latency / max(self.max_latency, 1e-9)
        reliability = control_plane_reliability_single_link_failure_cached(self.graph, [self.controller])

        # Reward aligns with study objective: minimize latency, maximize reliability.
        reward = -(latency_norm) + (2.0 * reliability) - (10.0 if reliability < 0.8 else 0.0)

        done = self.steps >= self.max_steps
        return self._state(), float(reward), done, {
            "latency": float(latency),
            "reliability": float(reliability),
        }


def _normalized_entropy(action_counts: np.ndarray) -> float:
    total = float(np.sum(action_counts))
    if total <= 0:
        return 0.0
    probs = action_counts / total
    probs = probs[probs > 0]
    if probs.size == 0:
        return 0.0
    entropy = -np.sum(probs * np.log2(probs))
    max_entropy = math.log2(len(action_counts)) if len(action_counts) > 1 else 1.0
    return float(entropy / max(max_entropy, 1e-9))


def _rolling_mean(values: list[float], window: int) -> float:
    if not values:
        return 0.0
    arr = np.array(values[-window:], dtype=np.float64)
    return float(arr.mean())


def run_single_stability_audit(
    topology_name: str,
    seed: int,
    episodes: int,
    learning_rate: float,
    batch_size: int,
    gamma: float,
    replay_memory_size: int,
    target_update_frequency: int,
    epsilon_start: float,
    epsilon_end: float,
    epsilon_decay: float,
    event_log_path: Path,
) -> RunSummary:
    torch.manual_seed(seed)
    np.random.seed(seed)
    rng = random.Random(seed)

    graph = load_canonical_topology(topology_name, seed=seed)
    env = GraphPlacementEnv(graph)

    device = torch.device("cpu")
    state_size = env.num_nodes
    action_size = env.num_nodes

    q_net = DQNetwork(state_size, action_size).to(device)
    target_net = DQNetwork(state_size, action_size).to(device)
    target_net.load_state_dict(q_net.state_dict())
    optimizer = optim.Adam(q_net.parameters(), lr=learning_rate)

    memory = ReplayBuffer(replay_memory_size)
    epsilon = epsilon_start

    best_reward = float("-inf")
    episode_rewards: list[float] = []
    action_counts = np.zeros(action_size, dtype=np.int64)
    last_latency = float("inf")
    last_reliability = 0.0

    event_log_path.parent.mkdir(parents=True, exist_ok=True)
    run_start = time.perf_counter()
    with event_log_path.open("a", encoding="utf-8") as event_log:
        for episode in range(1, episodes + 1):
            state = env.reset(rng)
            ep_reward = 0.0

            for _ in range(env.max_steps):
                if rng.random() < epsilon:
                    action = rng.randint(0, action_size - 1)
                else:
                    with torch.no_grad():
                        qvals = q_net(torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0))
                        action = int(torch.argmax(qvals, dim=1).item())

                action_counts[action] += 1

                next_state, reward, done, info = env.step(action)
                ep_reward += reward
                last_latency = info["latency"]
                last_reliability = info["reliability"]

                memory.push(state, action, reward, next_state, done)
                state = next_state

                if len(memory) >= batch_size:
                    s, a, r, ns, d = memory.sample(batch_size, device)
                    q_values = q_net(s).gather(1, a.unsqueeze(1)).squeeze(1)
                    with torch.no_grad():
                        next_q = target_net(ns).max(dim=1)[0]
                        target = r + (1.0 - d) * gamma * next_q
                    loss = nn.MSELoss()(q_values, target)
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                if done:
                    break

            episode_rewards.append(float(ep_reward))
            best_reward = max(best_reward, ep_reward)
            epsilon = max(epsilon_end, epsilon * epsilon_decay)

            if episode % target_update_frequency == 0:
                target_net.load_state_dict(q_net.state_dict())

            if episode == 1 or episode % 25 == 0 or episode == episodes:
                record = {
                    "event": "episode",
                    "topology": topology_name,
                    "seed": seed,
                    "episode": episode,
                    "reward": float(ep_reward),
                    "rolling_mean_50": _rolling_mean(episode_rewards, 50),
                    "best_reward": float(best_reward),
                    "epsilon": float(epsilon),
                    "action_entropy": _normalized_entropy(action_counts),
                    "latency": float(last_latency),
                    "reliability": float(last_reliability),
                }
                event_log.write(json.dumps(record, sort_keys=True) + "\n")

    reward_arr = np.array(episode_rewards, dtype=np.float64)
    reward_var_last200 = float(np.var(reward_arr[-200:])) if reward_arr.size else float("inf")
    rolling_last100 = _rolling_mean(episode_rewards, 100)
    entropy = _normalized_entropy(action_counts)

    divergence_flag = False
    divergence_reason = "stable"
    if np.isnan(reward_arr).any() or np.isinf(reward_arr).any():
        divergence_flag = True
        divergence_reason = "nan_or_inf_reward"
    elif reward_var_last200 > 50.0:
        divergence_flag = True
        divergence_reason = "high_reward_variance_last200"
    elif rolling_last100 < -50.0:
        divergence_flag = True
        divergence_reason = "reward_collapse_last100"

    run_elapsed_s = time.perf_counter() - run_start
    omega_ms = float((run_elapsed_s / max(episodes, 1)) * 1000.0)

    return RunSummary(
        topology=topology_name,
        seed=seed,
        episodes=episodes,
        learning_rate=learning_rate,
        batch_size=batch_size,
        gamma=gamma,
        rolling_mean_reward_last100=rolling_last100,
        reward_variance_last200=reward_var_last200,
        final_best_reward=float(best_reward),
        final_epsilon=float(epsilon),
        normalized_action_entropy=entropy,
        final_latency=float(last_latency),
        final_reliability=float(last_reliability),
        final_omega_ms_per_episode=omega_ms,
        divergence_flag=divergence_flag,
        divergence_reason=divergence_reason,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run 5-seed DQN stability audit across canonical topologies")
    parser.add_argument("--episodes", type=int, default=1000, help="Episodes per run (default: 1000)")
    parser.add_argument(
        "--topologies",
        type=str,
        default=",".join(FIXED_TOPOLOGIES),
        help="Comma-separated topology names (default: Internet2,ATT-MPLS)",
    )
    parser.add_argument(
        "--seeds",
        type=str,
        default=",".join(str(seed) for seed in FIXED_SEEDS),
        help="Comma-separated fixed seeds",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(PROJECT_ROOT / "results" / "rl_analysis" / "stability_audit"),
        help="Output directory for summaries/logs",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    config_path = PROJECT_ROOT / "configs" / "experiment_config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    hp = config.get("rl_hyperparameters", {})

    # Enforce fixed Farahi parameters.
    learning_rate = 0.001
    batch_size = 32
    gamma = 0.99

    replay_memory_size = int(hp.get("replay_memory_size", 10000))
    target_update_frequency = int(hp.get("target_update_frequency", 100))
    epsilon_start = float(hp.get("epsilon_start", 1.0))
    epsilon_end = float(hp.get("epsilon_end", 0.05))
    epsilon_decay = float(hp.get("epsilon_decay", 0.995))

    topologies = [name.strip() for name in args.topologies.split(",") if name.strip()]
    seeds = [int(value.strip()) for value in args.seeds.split(",") if value.strip()]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    event_log_path = output_dir / "training_events.jsonl"
    if event_log_path.exists():
        event_log_path.unlink()

    summaries: list[RunSummary] = []
    for topology_name in topologies:
        for seed in seeds:
            summary = run_single_stability_audit(
                topology_name=topology_name,
                seed=seed,
                episodes=args.episodes,
                learning_rate=learning_rate,
                batch_size=batch_size,
                gamma=gamma,
                replay_memory_size=replay_memory_size,
                target_update_frequency=target_update_frequency,
                epsilon_start=epsilon_start,
                epsilon_end=epsilon_end,
                epsilon_decay=epsilon_decay,
                event_log_path=event_log_path,
            )
            summaries.append(summary)
            print(
                f"[done] topology={summary.topology} seed={summary.seed} "
                f"best={summary.final_best_reward:.4f} entropy={summary.normalized_action_entropy:.4f} "
                f"divergence={summary.divergence_flag}"
            )

    summary_records = [asdict(item) for item in summaries]
    summary_df = pd.DataFrame(summary_records)

    summary_csv = output_dir / "stability_summary.csv"
    summary_json = output_dir / "stability_summary.json"
    grouped_csv = output_dir / "stability_grouped_by_topology.csv"

    summary_df.to_csv(summary_csv, index=False)
    summary_json.write_text(json.dumps(summary_records, indent=2), encoding="utf-8")

    grouped = (
        summary_df.groupby("topology")
        .agg(
            runs=("seed", "count"),
            mean_best_reward=("final_best_reward", "mean"),
            std_best_reward=("final_best_reward", "std"),
            mean_entropy=("normalized_action_entropy", "mean"),
            mean_rolling_reward_last100=("rolling_mean_reward_last100", "mean"),
            mean_latency=("final_latency", "mean"),
            mean_reliability=("final_reliability", "mean"),
            divergence_runs=("divergence_flag", "sum"),
        )
        .reset_index()
    )
    grouped.to_csv(grouped_csv, index=False)

    print("\n=== Stability Audit Completed ===")
    print(f"Summary CSV: {summary_csv}")
    print(f"Summary JSON: {summary_json}")
    print(f"Grouped CSV: {grouped_csv}")
    print(f"Episode log: {event_log_path}")


if __name__ == "__main__":
    main()
