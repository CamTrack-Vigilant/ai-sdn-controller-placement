#!/usr/bin/env python3
"""
Section 8.4.4: DQN Pilot Training Loop
========================================

Deep Q-Network training on Internet2 canonical topology.
Implements the Technical Stack Defense hyperparameters from Section 8.4.1:
  - learning_rate: 0.001
  - batch_size: 32
  - gamma: 0.99
  - max_episodes: 1000 (pilot uses 50)
  - replay_memory: 10,000

Validates end-to-end pipeline: proposal → config → topology → DQN training → metrics.json
"""

import json
import random
import sys
import time
from collections import deque
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from topology.canonical_topologies import load_canonical_topology


# ============================================================================
# Configuration Loading (Section 8.4.1 → Code)
# ============================================================================

def load_config() -> Dict:
    """Load experiment configuration from experiment_config.json."""
    config_path = Path(__file__).parent.parent / "configs" / "experiment_config.json"
    with open(config_path, "r") as f:
        return json.load(f)


CONFIG = load_config()
RL_CONFIG = CONFIG.get("rl_hyperparameters", {})

LEARNING_RATE = RL_CONFIG.get("learning_rate", 0.001)
BATCH_SIZE = RL_CONFIG.get("batch_size", 32)
GAMMA = RL_CONFIG.get("gamma", 0.99)
REPLAY_MEMORY_SIZE = RL_CONFIG.get("replay_memory_size", 10000)
TARGET_UPDATE_FREQ = RL_CONFIG.get("target_update_frequency", 100)
EPSILON_START = RL_CONFIG.get("epsilon_start", 1.0)
EPSILON_END = RL_CONFIG.get("epsilon_end", 0.05)
EPSILON_DECAY = RL_CONFIG.get("epsilon_decay", 0.995)

# Pilot constants (override max_episodes for quick validation)
PILOT_EPISODES = 50
DEVICE = torch.device("cpu")


# ============================================================================
# Network Architecture
# ============================================================================

class DQNetwork(nn.Module):
    """
    Deep Q-Network with 2 hidden layers (64 neurons each).
    Input: state (node encoding)
    Output: Q-values for each action (controller placement)
    """

    def __init__(self, input_size: int, output_size: int):
        super().__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, output_size)
        self.relu = nn.ReLU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through network."""
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x


# ============================================================================
# Replay Buffer
# ============================================================================

class ReplayBuffer:
    """Experience replay buffer (size: 10,000 from Farahi spec)."""

    def __init__(self, capacity: int = 10000):
        self.buffer = deque(maxlen=capacity)
        self.capacity = capacity

    def push(self, state, action, reward, next_state, done):
        """Add experience to buffer."""
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int) -> Tuple:
        """Sample random batch from buffer."""
        batch = random.sample(self.buffer, min(batch_size, len(self.buffer)))
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            torch.tensor(states, dtype=torch.float32, device=DEVICE),
            torch.tensor(actions, dtype=torch.int64, device=DEVICE),
            torch.tensor(rewards, dtype=torch.float32, device=DEVICE),
            torch.tensor(next_states, dtype=torch.float32, device=DEVICE),
            torch.tensor(dones, dtype=torch.float32, device=DEVICE),
        )

    def __len__(self):
        return len(self.buffer)


# ============================================================================
# Environment: Controller Placement on Internet2
# ============================================================================

class ControllerPlacementEnv:
    """
    Simple environment for controller placement on Internet2.
    State: one-hot encoding of current controller position
    Action: place controller on a specific node
    Reward: based on latency and reliability
    """

    def __init__(self, graph):
        self.graph = graph
        self.num_nodes = graph.number_of_nodes()
        self.nodes = list(graph.nodes())
        
        # Pre-compute latency baseline
        self.max_latency = self._compute_max_avg_distance()
        
        # Tracking
        self.current_controller = None
        self.step_count = 0
        self.episode_rewards = []

    def _compute_max_avg_distance(self) -> float:
        """Compute worst-case average distance for normalization."""
        import networkx as nx
        max_avg = 0.0
        for node in self.graph.nodes():
            lengths = nx.single_source_shortest_path_length(self.graph, node)
            avg_dist = np.mean(list(lengths.values())) if lengths else 0.0
            max_avg = max(max_avg, avg_dist)
        return max_avg if max_avg > 0 else 1.0

    def _compute_latency(self, controller_node: str) -> float:
        """
        Compute average latency: mean shortest path from controller to all nodes.
        Normalized by max_latency.
        """
        import networkx as nx
        lengths = nx.single_source_shortest_path_length(self.graph, controller_node)
        avg_dist = np.mean(list(lengths.values())) if lengths else 0.0
        return avg_dist / self.max_latency

    def _compute_reliability(self, controller_node: str) -> float:
        """
        Compute reliability: fraction of nodes reachable from controller.
        For a connected graph, this is typically 1.0; in pilot, always 1.0.
        """
        import networkx as nx
        reachable = len(nx.descendants(self.graph, controller_node)) + 1  # +1 for self
        return reachable / self.num_nodes

    def reset(self) -> np.ndarray:
        """Reset environment and return initial state."""
        self.current_controller = random.choice(self.nodes)
        self.step_count = 0
        self.episode_rewards = []
        return self._state_to_vector()

    def _state_to_vector(self) -> np.ndarray:
        """Convert controller node to one-hot vector."""
        state = np.zeros(self.num_nodes, dtype=np.float32)
        node_idx = self.nodes.index(self.current_controller)
        state[node_idx] = 1.0
        return state

    def step(self, action: int) -> Tuple[np.ndarray, float, bool]:
        """
        Execute action (move controller to new node).
        Return: (next_state, reward, done)
        """
        self.step_count += 1
        
        # Action: select controller node
        if 0 <= action < self.num_nodes:
            self.current_controller = self.nodes[action]
        
        # Compute metrics
        latency = self._compute_latency(self.current_controller)
        reliability = self._compute_reliability(self.current_controller)
        
        # Reward logic (Section 8.4.1 specifications)
        latency_score = -(latency)  # Negative latency is good
        reliability_score = reliability * 2  # Amplified reliability reward
        penalty = -10.0 if reliability < 0.8 else 0.0  # Harsh penalty for low reliability
        
        reward = latency_score + reliability_score + penalty
        
        # Episode terminates after fixed steps (proof of concept)
        done = self.step_count >= 10
        
        self.episode_rewards.append(reward)
        next_state = self._state_to_vector()
        
        return next_state, reward, done


# ============================================================================
# DQN Agent
# ============================================================================

class DQNAgent:
    """Deep Q-Network agent for controller placement."""

    def __init__(self, state_size: int, action_size: int):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = EPSILON_START
        
        # Networks
        self.q_network = DQNetwork(state_size, action_size).to(DEVICE)
        self.target_network = DQNetwork(state_size, action_size).to(DEVICE)
        self.target_network.load_state_dict(self.q_network.state_dict())
        
        # Optimizer
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=LEARNING_RATE)
        
        # Replay buffer
        self.memory = ReplayBuffer(REPLAY_MEMORY_SIZE)
        
        # Tracking
        self.update_count = 0

    def remember(self, state, action, reward, next_state, done):
        """Store experience in replay buffer."""
        self.memory.push(state, action, reward, next_state, done)

    def act(self, state: np.ndarray) -> int:
        """Epsilon-greedy action selection."""
        if np.random.random() < self.epsilon:
            return random.randint(0, self.action_size - 1)
        
        state_tensor = torch.tensor(state, dtype=torch.float32, device=DEVICE).unsqueeze(0)
        with torch.no_grad():
            q_values = self.q_network(state_tensor)
        return q_values.argmax(dim=1).item()

    def replay(self, batch_size: int):
        """Train on batch from replay buffer."""
        if len(self.memory) < batch_size:
            return
        
        states, actions, rewards, next_states, dones = self.memory.sample(batch_size)
        
        # Current Q-values
        q_values = self.q_network(states)
        q_values = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)
        
        # Target Q-values
        with torch.no_grad():
            next_q_values = self.target_network(next_states).max(dim=1)[0]
            target_q_values = rewards + (1 - dones) * GAMMA * next_q_values
        
        # Loss
        loss = nn.MSELoss()(q_values, target_q_values)
        
        # Backprop
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Update target network periodically
        self.update_count += 1
        if self.update_count % TARGET_UPDATE_FREQ == 0:
            self.target_network.load_state_dict(self.q_network.state_dict())
        
        return loss.item()

    def decay_epsilon(self):
        """Decay exploration rate."""
        self.epsilon = max(EPSILON_END, self.epsilon * EPSILON_DECAY)


# ============================================================================
# Training Loop
# ============================================================================

def train_pilot():
    """Run pilot DQN training (50 episodes)."""
    print("\n" + "=" * 70)
    print("DQN PILOT TRAINING (Section 8.4.4)")
    print("=" * 70)
    
    # Load topology
    print("\n[1/4] Loading Internet2 topology...")
    G = load_canonical_topology("Internet2", seed=42)
    print(f"  ✓ Loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    # Create environment and agent
    print("\n[2/4] Initializing environment and agent...")
    env = ControllerPlacementEnv(G)
    agent = DQNAgent(state_size=G.number_of_nodes(), action_size=G.number_of_nodes())
    print(f"  ✓ DQN Network: Input(11) -> Hidden(64) -> Hidden(64) -> Output(11)")
    print(f"  ✓ Replay Buffer: {REPLAY_MEMORY_SIZE} capacity")
    print(f"  ✓ Hyperparameters: LR={LEARNING_RATE}, γ={GAMMA}, batch={BATCH_SIZE}")
    
    # Training loop
    print(f"\n[3/4] Training for {PILOT_EPISODES} episodes...")
    episode_rewards = []
    start_time = time.time()
    
    for episode in range(PILOT_EPISODES):
        state = env.reset()
        episode_reward = 0
        done = False
        
        while not done:
            # Agent selects action
            action = agent.act(state)
            
            # Environment step
            next_state, reward, done = env.step(action)
            episode_reward += reward
            
            # Store in replay buffer
            agent.remember(state, action, reward, next_state, done)
            
            # Train on batch
            if len(agent.memory) >= BATCH_SIZE:
                agent.replay(BATCH_SIZE)
            
            state = next_state
        
        # Decay exploration
        agent.decay_epsilon()
        episode_rewards.append(episode_reward)
        
        # Progress
        if (episode + 1) % 10 == 0:
            avg_reward = np.mean(episode_rewards[-10:])
            print(f"  Episode {episode + 1:3d}/{PILOT_EPISODES}: avg_reward={avg_reward:8.3f}, ε={agent.epsilon:.3f}")
    
    elapsed = time.time() - start_time
    
    # Summary
    print("\n[4/4] Pilot training complete!")
    print(f"  ✓ Elapsed time: {elapsed:.1f}s ({elapsed/PILOT_EPISODES:.2f}s/episode)")
    print(f"  ✓ Final avg reward: {np.mean(episode_rewards[-10:]):.3f}")
    print(f"  ✓ Best episode: {max(episode_rewards):.3f}")
    print(f"  ✓ Worst episode: {min(episode_rewards):.3f}")
    
    # Save metrics
    print("\n[EXPORTING] Writing pilot_metrics.json...")
    output_path = Path(__file__).parent.parent / "results" / "pilot_metrics.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    metrics = {
        "metadata": {
            "pilot_episodes": PILOT_EPISODES,
            "total_steps": sum(env.step_count for _ in range(PILOT_EPISODES)),
            "elapsed_seconds": elapsed,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "hyperparameters": {
            "learning_rate": LEARNING_RATE,
            "batch_size": BATCH_SIZE,
            "gamma": GAMMA,
            "replay_memory_size": REPLAY_MEMORY_SIZE,
            "target_update_frequency": TARGET_UPDATE_FREQ,
            "epsilon_start": EPSILON_START,
            "epsilon_end": EPSILON_END,
            "epsilon_decay": EPSILON_DECAY
        },
        "topology": {
            "name": "Internet2",
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "seed": 42
        },
        "episode_rewards": episode_rewards,
        "statistics": {
            "mean_reward": float(np.mean(episode_rewards)),
            "std_reward": float(np.std(episode_rewards)),
            "max_reward": float(np.max(episode_rewards)),
            "min_reward": float(np.min(episode_rewards)),
            "final_10_episode_avg": float(np.mean(episode_rewards[-10:]))
        }
    }
    
    with open(output_path, "w") as f:
        json.dump(metrics, f, indent=2)
    
    print(f"  ✓ Metrics saved: {output_path}")
    print("\n" + "=" * 70)
    print("PILOT RUN SUCCESSFUL")
    print("=" * 70 + "\n")
    
    return metrics


if __name__ == "__main__":
    metrics = train_pilot()
