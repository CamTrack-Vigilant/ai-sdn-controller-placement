#!/usr/bin/env python3
"""
Plot DQN 1,000-episode Training Convergence Curve
"""
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def main():
    metrics_path = Path(__file__).parent.parent / "results" / "pilot_metrics.json"
    with open(metrics_path, "r") as f:
        data = json.load(f)

    rewards = data["episode_rewards"]
    episodes = np.arange(1, len(rewards) + 1)
    
    # Calculate moving average
    window = 20
    moving_avg = np.convolve(rewards, np.ones(window)/window, mode='valid')

    plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)

    # Plot raw rewards and moving average
    ax.plot(episodes, rewards, alpha=0.35, color='#4A90E2', label='Raw Episode Reward')
    ax.plot(episodes[window-1:], moving_avg, color='#1A365D', linewidth=2.0, label=f'{window}-Episode Moving Average')

    ax.set_title('DQN Controller Placement Optimization — 1,000 Episode Convergence (Internet2 Topology)', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Training Episode', fontsize=11)
    ax.set_ylabel('Reward Score (Latency + Reliability)', fontsize=11)
    ax.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9)
    ax.set_ylim(min(rewards) - 0.5, max(rewards) + 0.5)

    plt.tight_layout()
    output_img = Path(__file__).parent.parent / "results" / "dqn_1000_episodes_convergence.png"
    plt.savefig(output_img)
    print(f"✓ Saved convergence plot to: {output_img}")

if __name__ == "__main__":
    main()
