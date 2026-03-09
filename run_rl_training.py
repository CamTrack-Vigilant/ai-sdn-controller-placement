#!/usr/bin/env python3
"""
Entry point script for running RL controller placement training.
This script ensures the project root is in the Python path.
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Now import and run the RL module
from algorithms.ai.reinforcement_learning import bandit_rl_controller_placement
from topology.network_topology import TopologyConfig, generate_multi_site_topology


def main():
    """Run RL training with default configuration."""
    print("Initializing RL Controller Placement Training...")
    
    # Create a sample multi-site topology
    print("Building network topology...")
    config = TopologyConfig(
        num_sites=3,
        nodes_per_site=5,
        intra_site_degree=3,
        inter_site_links=2,
        seed=42
    )
    
    topology = generate_multi_site_topology(config)
    print(f"  Nodes: {topology.number_of_nodes()}")
    print(f"  Edges: {topology.number_of_edges()}")
    
    # Configure training
    num_controllers = 3
    episodes = 500
    latency_weight = 0.6
    reliability_weight = 0.4
    log_path = "results/rl_training/training_log.jsonl"
    
    print(f"\nTraining Configuration:")
    print(f"  Controllers: {num_controllers}")
    print(f"  Episodes: {episodes}")
    print(f"  Latency weight: {latency_weight}")
    print(f"  Reliability weight: {reliability_weight}")
    print(f"  Log path: {log_path}")
    
    # Create log directory
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Train the agent
    print("\nStarting bandit RL training...")
    best_placement = bandit_rl_controller_placement(
        graph=topology,
        num_controllers=num_controllers,
        episodes=episodes,
        latency_weight=latency_weight,
        reliability_weight=reliability_weight,
        log_path=log_path,
        log_every=50,
        run_label="demo_run"
    )
    
    print("\n✓ Training complete!")
    print(f"  Best placement found: {best_placement}")
    print(f"  Training logs: {log_path}")
    
    return best_placement


if __name__ == "__main__":
    main()
