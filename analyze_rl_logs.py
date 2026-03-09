#!/usr/bin/env python3
"""
Analyze RL training logs and visualize convergence metrics.
"""
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def load_training_log(log_path: str) -> list[dict]:
    """Load JSONL training log and extract episode events."""
    episodes = []
    run_info = None
    run_summary = None
    
    with open(log_path, 'r') as f:
        for line in f:
            record = json.loads(line.strip())
            if record['event'] == 'run_start':
                run_info = record
            elif record['event'] == 'episode':
                episodes.append(record)
            elif record['event'] == 'run_end':
                run_summary = record
    
    return episodes, run_info, run_summary


def analyze_convergence(episodes: list[dict]) -> dict:
    """Analyze convergence metrics from training episodes."""
    episode_nums = [e['episode'] for e in episodes]
    rewards = [e['reward'] for e in episodes]
    best_rewards = [e['best_reward'] for e in episodes]
    q_values = [e['selected_action_q'] for e in episodes]
    epsilons = [e['epsilon'] for e in episodes]
    avg_distances = [e['selected_action_avg_distance'] for e in episodes]
    reliabilities = [e['selected_action_reliability'] for e in episodes]
    visits = [e['selected_action_visits'] for e in episodes]
    
    # Calculate convergence metrics
    convergence_episode = None
    best_reward_final = best_rewards[-1]
    
    # Find when best reward stabilized (within 5% for 50 episodes)
    threshold = abs(best_reward_final * 0.05)
    for i in range(50, len(best_rewards)):
        window = best_rewards[i-50:i]
        if all(abs(r - best_reward_final) <= threshold for r in window):
            convergence_episode = episode_nums[i-50]
            break
    
    # Calculate improvement rate
    initial_reward = rewards[0]
    final_reward = best_reward_final
    improvement = ((final_reward - initial_reward) / abs(initial_reward)) * 100
    
    return {
        'episode_nums': episode_nums,
        'rewards': rewards,
        'best_rewards': best_rewards,
        'q_values': q_values,
        'epsilons': epsilons,
        'avg_distances': avg_distances,
        'reliabilities': reliabilities,
        'visits': visits,
        'convergence_episode': convergence_episode,
        'initial_reward': initial_reward,
        'final_reward': final_reward,
        'improvement_pct': improvement,
    }


def print_summary(run_info: dict, run_summary: dict, metrics: dict):
    """Print training summary statistics."""
    print("=" * 70)
    print("RL TRAINING ANALYSIS SUMMARY")
    print("=" * 70)
    
    print(f"\n📊 Run Configuration:")
    print(f"  Run ID: {run_info['run_id']}")
    print(f"  Label: {run_info['label']}")
    print(f"  Topology: {run_info['num_nodes']} nodes, {run_info['num_controllers']} controllers")
    print(f"  Episodes: {run_info['episodes']}")
    print(f"  Action Space: {run_info['num_actions']} possible placements")
    print(f"  Weights: Latency={run_info['latency_weight']}, Reliability={run_info['reliability_weight']}")
    print(f"  Exploration: ε = {run_info['epsilon_start']} → {run_summary['final_epsilon']:.4f}")
    
    print(f"\n🎯 Convergence Metrics:")
    print(f"  Initial Reward: {metrics['initial_reward']:.4f}")
    print(f"  Final Reward: {metrics['final_reward']:.4f}")
    print(f"  Improvement: {metrics['improvement_pct']:.2f}%")
    if metrics['convergence_episode']:
        print(f"  Converged at: Episode {metrics['convergence_episode']}")
    else:
        print(f"  Converged at: Not fully converged (still improving)")
    
    print(f"\n🏆 Best Solution Found:")
    best_action = run_summary['best_action']
    print(f"  Controllers: {best_action}")
    print(f"  Average Distance: {run_summary['best_action_avg_distance']:.4f}")
    print(f"  Reliability: {run_summary['best_action_reliability']:.6f}")
    print(f"  Q-value: {run_summary['best_action_q']:.4f}")
    
    print(f"\n📈 Top 5 Alternative Placements:")
    for i, action in enumerate(run_summary['top_actions'][:5], 1):
        print(f"  {i}. {action['controllers']}")
        print(f"     Distance={action['average_distance']:.4f}, "
              f"Reliability={action['reliability']:.6f}, "
              f"Visited={action['visits']} times")
    
    print("\n" + "=" * 70)


def plot_convergence(metrics: dict, run_info: dict, output_path: str):
    """Create comprehensive convergence visualization."""
    fig, axes = plt.subplots(3, 2, figsize=(14, 10))
    fig.suptitle(f"RL Training Convergence Analysis - {run_info['label']}", 
                 fontsize=14, fontweight='bold')
    
    episodes = metrics['episode_nums']
    
    # 1. Reward Progression
    ax = axes[0, 0]
    ax.plot(episodes, metrics['rewards'], 'o-', alpha=0.3, markersize=2, 
            label='Episode Reward', color='lightblue')
    ax.plot(episodes, metrics['best_rewards'], '-', linewidth=2, 
            label='Best Reward', color='darkblue')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Reward')
    ax.set_title('Reward Convergence')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    if metrics['convergence_episode']:
        ax.axvline(metrics['convergence_episode'], color='red', linestyle='--', 
                   alpha=0.5, label=f"Converged: Ep {metrics['convergence_episode']}")
    
    # 2. Q-value Evolution
    ax = axes[0, 1]
    ax.plot(episodes, metrics['q_values'], 'o-', markersize=2, color='green', alpha=0.6)
    ax.set_xlabel('Episode')
    ax.set_ylabel('Q-value')
    ax.set_title('Q-value Evolution')
    ax.grid(True, alpha=0.3)
    
    # 3. Epsilon Decay (Exploration-Exploitation)
    ax = axes[1, 0]
    ax.plot(episodes, metrics['epsilons'], '-', linewidth=2, color='purple')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Epsilon (ε)')
    ax.set_title('Exploration Rate Decay')
    ax.grid(True, alpha=0.3)
    ax.axhline(0.1, color='red', linestyle='--', alpha=0.3, 
               label='Low exploration threshold')
    ax.legend()
    
    # 4. Average Distance Progression
    ax = axes[1, 1]
    ax.plot(episodes, metrics['avg_distances'], 'o-', markersize=2, 
            color='orange', alpha=0.6)
    ax.set_xlabel('Episode')
    ax.set_ylabel('Average Distance')
    ax.set_title('Network Latency Optimization')
    ax.grid(True, alpha=0.3)
    
    # 5. Action Visits (Exploitation Pattern)
    ax = axes[2, 0]
    ax.plot(episodes, metrics['visits'], '-', linewidth=1.5, color='brown')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Visit Count')
    ax.set_title('Action Selection Frequency')
    ax.grid(True, alpha=0.3)
    
    # 6. Reliability Consistency
    ax = axes[2, 1]
    ax.plot(episodes, metrics['reliabilities'], 'o-', markersize=2, 
            color='teal', alpha=0.6)
    ax.set_xlabel('Episode')
    ax.set_ylabel('Reliability')
    ax.set_title('Control Plane Reliability')
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0.99, 1.0])
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n📊 Convergence plot saved: {output_path}")
    
    return fig


def plot_reward_distribution(episodes: list[dict], output_path: str):
    """Plot reward distribution over training."""
    rewards = [e['reward'] for e in episodes]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Histogram
    ax1.hist(rewards, bins=30, edgecolor='black', alpha=0.7, color='steelblue')
    ax1.set_xlabel('Reward')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Reward Distribution')
    ax1.axvline(np.mean(rewards), color='red', linestyle='--', 
                label=f'Mean: {np.mean(rewards):.4f}')
    ax1.axvline(np.median(rewards), color='green', linestyle='--', 
                label=f'Median: {np.median(rewards):.4f}')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Box plot by quartile
    quartiles = np.array_split(rewards, 4)
    ax2.boxplot(quartiles, labels=['Q1', 'Q2', 'Q3', 'Q4'])
    ax2.set_xlabel('Training Quartile')
    ax2.set_ylabel('Reward')
    ax2.set_title('Reward Distribution by Training Phase')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"📊 Reward distribution plot saved: {output_path}")


def main():
    """Main analysis pipeline."""
    log_path = "results/rl_training/training_log.jsonl"
    
    if not Path(log_path).exists():
        print(f"❌ Training log not found: {log_path}")
        return
    
    print(f"📖 Loading training log: {log_path}\n")
    
    # Load and parse log (use last run if multiple)
    episodes, run_info, run_summary = load_training_log(log_path)
    
    print(f"✓ Loaded {len(episodes)} episode records")
    
    # Analyze convergence
    print("🔍 Analyzing convergence metrics...")
    metrics = analyze_convergence(episodes)
    
    # Print summary
    print_summary(run_info, run_summary, metrics)
    
    # Create output directory
    output_dir = Path("results/rl_analysis")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate visualizations
    print("\n📈 Generating visualizations...")
    plot_convergence(metrics, run_info, str(output_dir / "convergence_analysis.png"))
    plot_reward_distribution(episodes, str(output_dir / "reward_distribution.png"))
    
    print(f"\n✅ Analysis complete! Results saved to: {output_dir}/")


if __name__ == "__main__":
    main()
