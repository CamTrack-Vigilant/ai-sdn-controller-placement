# APPENDICES

## APPENDIX A: DETAILED EXPERIMENTAL CONFIGURATIONS & HYPERPARAMETERS

The entire benchmarking pipeline is configured via a centralized, immutable JSON configuration manifest (`configs/experiment_config.json`). The complete parameter schema governing reproduction is provided below:

```json
{
  "project_name": "ai-sdn-controller-placement",
  "version": "1.0.0",
  "seed": 42,
  "hardware_constraints": {
    "cpu_governor": "performance",
    "cooldown_seconds": 10,
    "max_memory_mb": 8192
  },
  "topology_config": {
    "canonical": [
      {
        "name": "Internet2",
        "nodes": 11,
        "edges": 18,
        "source": "Heller et al. (2012)"
      },
      {
        "name": "ATT-MPLS",
        "nodes": 21,
        "edges": 54,
        "source": "Internet Topology Zoo (Knight et al., 2011)"
      }
    ],
    "synthetic": {
      "barabasi_albert": {
        "m": 2,
        "scales": [20, 50]
      },
      "waxman": {
        "alpha": 0.5,
        "beta": 0.2,
        "scales": [20, 50]
      }
    }
  },
  "controller_budgets": [2, 3, 5],
  "rl_hyperparameters": {
    "architecture": "MLP",
    "hidden_layers": [64, 64],
    "learning_rate": 0.001,
    "batch_size": 32,
    "gamma": 0.99,
    "max_episodes": 1000,
    "replay_memory_capacity": 10000,
    "epsilon_start": 1.0,
    "epsilon_end": 0.05,
    "epsilon_decay": 0.995,
    "target_network_update_freq": 10,
    "reward_weights": {
      "latency_weight": 10.0,
      "reliability_weight": 5.0,
      "duplicate_penalty": 20.0
    }
  },
  "genetic_algorithm_config": {
    "population_size": 50,
    "generations": 50,
    "crossover_probability": 0.8,
    "mutation_probability": 0.15,
    "elitism_count": 2
  },
  "mininet_emulation": {
    "openflow_version": "OpenFlow13",
    "switch_type": "OVSSwitch",
    "controller_ip": "127.0.0.1",
    "base_controller_port": 6633,
    "ping_count": 100,
    "gate_test_threshold_ms": 2000
  }
}
```

---

## APPENDIX B: EXTENDED LATENCY, RELIABILITY, AND COMPLEXITY DATA TABLES

Table B.1 compiles the complete experimental results for all 12 cells in the Factorial Benchmark Matrix ($N \in \{20, 50\}$, $k \in \{2, 3, 5\}$, Barabási-Albert and Waxman topologies), comparing all five algorithmic paradigms across average latency, single-link reliability, and computational execution time.

### Table B.1: Complete Factorial Benchmark Matrix Performance Metrics Across All Configurations

| Topology Model | Scale ($N$) | Budget ($k$) | Algorithm | Mean Latency ($L(P)$ ms) | Single-Link Reliability ($Reach_{avg}$) | Mean Runtime ($\omega$ ms) | Pareto Optimal? |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| **Barabási-Albert** | 20 | 2 | Random Baseline | 7.121 | 1.000 | 0.018 | Yes |
| **Barabási-Albert** | 20 | 2 | Greedy $K$-Center | 6.083 | 1.000 | 0.029 | **Yes** |
| **Barabási-Albert** | 20 | 2 | $K$-Means Clustering | 7.885 | 1.000 | 3.988 | No |
| **Barabási-Albert** | 20 | 2 | Genetic Algorithm | **5.810** | 1.000 | 25.944 | **Yes** |
| **Barabási-Albert** | 20 | 2 | PyTorch DQN | 6.028 | 1.000 | 149.928 | No |
| **Barabási-Albert** | 20 | 3 | Random Baseline | 7.113 | 1.000 | 0.020 | Yes |
| **Barabási-Albert** | 20 | 3 | Greedy $K$-Center | 5.751 | 1.000 | 0.057 | **Yes** |
| **Barabási-Albert** | 20 | 3 | $K$-Means Clustering | 5.005 | 1.000 | 4.028 | **Yes** |
| **Barabási-Albert** | 20 | 3 | Genetic Algorithm | **4.321** | 1.000 | 28.776 | **Yes** |
| **Barabási-Albert** | 20 | 3 | PyTorch DQN | 4.558 | 1.000 | 157.571 | No |
| **Barabási-Albert** | 20 | 5 | Random Baseline | 4.258 | 1.000 | 0.021 | Yes |
| **Barabási-Albert** | 20 | 5 | Greedy $K$-Center | 3.726 | 1.000 | 0.098 | **Yes** |
| **Barabási-Albert** | 20 | 5 | $K$-Means Clustering | 3.559 | 1.000 | 5.204 | **Yes** |
| **Barabási-Albert** | 20 | 5 | Genetic Algorithm | **3.216** | 1.000 | 35.693 | **Yes** |
| **Barabási-Albert** | 20 | 5 | PyTorch DQN | 3.610 | 1.000 | 160.022 | No |
| **Barabási-Albert** | 50 | 2 | Random Baseline | 7.993 | 1.000 | 0.021 | Yes |
| **Barabási-Albert** | 50 | 2 | Greedy $K$-Center | 5.631 | 1.000 | 0.067 | **Yes** |
| **Barabási-Albert** | 50 | 2 | $K$-Means Clustering | 7.374 | 1.000 | 4.052 | No |
| **Barabási-Albert** | 50 | 2 | Genetic Algorithm | **5.134** | 1.000 | 50.765 | **Yes** |
| **Barabási-Albert** | 50 | 2 | PyTorch DQN | **5.134** | 1.000 | 1068.596 | No |
| **Barabási-Albert** | 50 | 3 | Random Baseline | 6.209 | 1.000 | 0.025 | Yes |
| **Barabási-Albert** | 50 | 3 | Greedy $K$-Center | 4.959 | 1.000 | 0.159 | **Yes** |
| **Barabási-Albert** | 50 | 3 | $K$-Means Clustering | 5.044 | 1.000 | 5.256 | No |
| **Barabási-Albert** | 50 | 3 | Genetic Algorithm | **4.247** | 1.000 | 62.427 | **Yes** |
| **Barabási-Albert** | 50 | 3 | PyTorch DQN | 4.650 | 1.000 | 1064.514 | No |
| **Barabási-Albert** | 50 | 5 | Random Baseline | 5.264 | 1.000 | 0.021 | Yes |
| **Barabási-Albert** | 50 | 5 | Greedy $K$-Center | 4.203 | 1.000 | 0.207 | **Yes** |
| **Barabási-Albert** | 50 | 5 | $K$-Means Clustering | 4.890 | 1.000 | 5.258 | No |
| **Barabási-Albert** | 50 | 5 | Genetic Algorithm | **3.553** | 1.000 | 74.937 | **Yes** |
| **Barabási-Albert** | 50 | 5 | PyTorch DQN | 4.004 | 1.000 | 1086.206 | No |
| **Waxman Spatial** | 20 | 2 | Random Baseline | 6.584 | 1.000 | 0.020 | Yes |
| **Waxman Spatial** | 20 | 2 | Greedy $K$-Center | 4.922 | 1.000 | 0.026 | **Yes** |
| **Waxman Spatial** | 20 | 2 | $K$-Means Clustering | 4.043 | 1.000 | 3.397 | **Yes** |
| **Waxman Spatial** | 20 | 2 | Genetic Algorithm | **3.715** | 1.000 | 26.258 | **Yes** |
| **Waxman Spatial** | 20 | 2 | PyTorch DQN | 3.779 | 1.000 | 60.329 | No |
| **Waxman Spatial** | 20 | 3 | Random Baseline | 5.024 | 1.000 | 0.018 | Yes |
| **Waxman Spatial** | 20 | 3 | Greedy $K$-Center | 3.526 | 1.000 | 0.043 | **Yes** |
| **Waxman Spatial** | 20 | 3 | $K$-Means Clustering | 3.953 | 1.000 | 4.493 | No |
| **Waxman Spatial** | 20 | 3 | Genetic Algorithm | **2.432** | 1.000 | 33.125 | **Yes** |
| **Waxman Spatial** | 20 | 3 | PyTorch DQN | 2.517 | 1.000 | 58.335 | No |
| **Waxman Spatial** | 20 | 5 | Random Baseline | 4.202 | 1.000 | 0.022 | Yes |
| **Waxman Spatial** | 20 | 5 | Greedy $K$-Center | 2.769 | 1.000 | 0.079 | **Yes** |
| **Waxman Spatial** | 20 | 5 | $K$-Means Clustering | 1.998 | 1.000 | 4.573 | **Yes** |
| **Waxman Spatial** | 20 | 5 | Genetic Algorithm | **1.879** | 1.000 | 35.792 | **Yes** |
| **Waxman Spatial** | 20 | 5 | PyTorch DQN | 1.997 | 1.000 | 63.375 | No |
| **Waxman Spatial** | 50 | 2 | Random Baseline | 19.436 | 1.000 | 0.022 | Yes |
| **Waxman Spatial** | 50 | 2 | Greedy $K$-Center | 17.057 | 1.000 | 0.059 | **Yes** |
| **Waxman Spatial** | 50 | 2 | $K$-Means Clustering | 25.525 | 0.950 | 3.976 | No |
| **Waxman Spatial** | 50 | 2 | Genetic Algorithm | **10.604** | 1.000 | 50.245 | **Yes** |
| **Waxman Spatial** | 50 | 2 | PyTorch DQN | 11.432 | 1.000 | 396.982 | No |
| **Waxman Spatial** | 50 | 3 | Random Baseline | 10.872 | 1.000 | 0.020 | Yes |
| **Waxman Spatial** | 50 | 3 | Greedy $K$-Center | 8.842 | 1.000 | 0.086 | **Yes** |
| **Waxman Spatial** | 50 | 3 | $K$-Means Clustering | 8.879 | 1.000 | 4.452 | No |
| **Waxman Spatial** | 50 | 3 | Genetic Algorithm | **5.921** | 1.000 | 58.388 | **Yes** |
| **Waxman Spatial** | 50 | 3 | PyTorch DQN | 7.287 | 1.000 | 438.198 | No |
| **Waxman Spatial** | 50 | 5 | Random Baseline | 6.975 | 1.000 | 0.020 | Yes |
| **Waxman Spatial** | 50 | 5 | Greedy $K$-Center | 6.940 | 1.000 | 0.172 | **Yes** |
| **Waxman Spatial** | 50 | 5 | $K$-Means Clustering | 6.883 | 1.000 | 5.223 | **Yes** |
| **Waxman Spatial** | 50 | 5 | Genetic Algorithm | **4.772** | 1.000 | 75.866 | **Yes** |
| **Waxman Spatial** | 50 | 5 | PyTorch DQN | 5.322 | 1.000 | 533.085 | No |

---

## APPENDIX C: MININET EMULATION TEST HARNESS CODE

The following Python listing provides the core execution harness (`scripts/run_mininet_demo.py`) utilized to instantiate synthesized controller placements inside Mininet and measure live OpenFlow ping Round-Trip Times:

```python
"""
Mininet Live OpenFlow Emulation Harness for Controller Placement Benchmarking.
Evaluates empirical ICMP control-plane RTT on canonical Internet2 topology.
"""
from __future__ import annotations
import sys
import json
import time
from pathlib import Path

# Legacy NumPy alias compatibility shim
try:
    import numpy as np
    for _alias, _target in [("bool", bool), ("int", int), ("float", float)]:
        if not hasattr(np, _alias):
            setattr(np, _alias, _target)
except Exception:
    pass

from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.link import TCLink
from mininet.log import setLogLevel

from topology.canonical_topologies import load_canonical_topology
from algorithms.baseline.greedy_placement import greedy_k_center_placement
from algorithms.baseline.kmeans_placement import kmeans_controller_placement
from algorithms.baseline.random_placement import random_controller_placement

def run_mininet_placement_trial(G, placement_nodes, k=3, ping_count=100):
    net = Mininet(topo=None, build=False, link=TCLink, switch=OVSSwitch)
    
    # 1. Spawn controllers on distinct localhost ports
    controllers = {}
    for idx, c_node in enumerate(placement_nodes):
        c_name = f"c{idx+1}"
        c_port = 6633 + idx
        controllers[c_node] = net.addController(
            c_name, controller=RemoteController, ip="127.0.0.1", port=c_port
        )
        
    # 2. Add switches and attached end-hosts
    switches = {}
    hosts = {}
    node_to_idx = {node: f"s{i+1}" for i, node in enumerate(G.nodes())}
    
    for node in G.nodes():
        sw_name = node_to_idx[node]
        switches[node] = net.addSwitch(sw_name, protocols="OpenFlow13")
        h_name = f"h{sw_name[1:]}"
        hosts[node] = net.addHost(h_name, ip=f"10.0.0.{sw_name[1:]}/24")
        net.addLink(hosts[node], switches[node], delay="0.1ms")
        
    # 3. Add inter-switch links with shortest-path propagation delay
    for u, v, data in G.edges(data=True):
        delay_ms = data.get("delay", 1.0)
        net.addLink(switches[u], switches[v], delay=f"{delay_ms:.2f}ms")
        
    # 4. Build and start network
    net.build()
    for c in controllers.values():
        c.start()
    for sw in switches.values():
        sw.start(list(controllers.values()))
        
    net.staticArp()
    
    # 5. Measure ping RTT from each host to designated controller site host
    rtt_measurements = []
    for node, host in hosts.items():
        # Find closest controller in placement
        closest_c = min(placement_nodes, key=lambda c: nx.shortest_path_length(G, node, c, weight="weight"))
        target_host = hosts[closest_c]
        
        # Ping target host
        ping_out = host.cmd(f"ping -c 3 -W 1 {target_host.IP()}")
        # Parse average RTT from ping summary
        for line in ping_out.splitlines():
            if "rtt min/avg/max/mdev" in line:
                avg_rtt = float(line.split("/")[4])
                rtt_measurements.append(avg_rtt)
                break
                
    net.stop()
    
    mean_rtt = float(np.mean(rtt_measurements)) if rtt_measurements else 0.0
    worst_rtt = float(np.max(rtt_measurements)) if rtt_measurements else 0.0
    return mean_rtt, worst_rtt
```
