# CHAPTER FIVE

# 5.0 CONCLUSION

## 5.1 SUMMARY OF MAIN FINDINGS

This mini-dissertation benchmarked five controller placement strategies—Random Baseline, Greedy $K$-Center, Spatial $K$-Means Clustering, Genetic Algorithm (GA), and PyTorch Deep $Q$-Network (DQN) / multi-armed reinforcement learning—across canonical wide-area networks (Internet2 and ATT-MPLS) and synthetic topology families (Barabási-Albert scale-free and Waxman spatial graphs at scales $N \in \{20, 50\}$ and controller budgets $k \in \{2, 3, 5\}$). Each method was evaluated across switch-to-controller propagation latency $L(P)$, single-link failure survivability $Reach_{avg}(P)$, offline training overhead $\omega_{\text{train}}$, online execution/inference latency $\tau_{\text{inf}}$, and emulated Mininet round-trip time (RTT).

The primary empirical findings are as follows:

1. DQN Convergence and Multi-Seed Stability: On the 20-node Internet2 topology ($k=3$), the 1,000-episode PyTorch DQN run converged within 20 episodes, achieving a grand training mean reward of $13.055 \pm 0.589$ and a final 10-episode average reward of $13.199$ (`results/pilot_metrics.json`). Across the 10-run multi-seed stability audit (`results/rl_analysis/stability_audit/stability_summary.csv`), zero runs diverged (`divergence_flag = False`), with mean best rewards of $14.194 \pm 0.063$ on Internet2 and $14.854 \pm 0.395$ on ATT-MPLS.
2. Factorial Latency and ANOVA Results: Across the 300-observation synthetic factorial dataset (`60 cells x 5 seeds`), multi-factor ANOVA confirmed a statistically significant main effect of algorithm family ($F(4, 240) = 118.90, p < 0.0001$). The Genetic Algorithm achieved the lowest mean propagation latency in all 12 synthetic factorial cells, outperforming the Random baseline by up to $55.29\%$ on Waxman ($N=20, k=5$, $1.879\text{ ms}$) and $39.26\%$ on Barabási-Albert ($N=20, k=3$, $4.321\text{ ms}$).
3. Offline Training Overhead ($\omega_{\text{train}}$) vs. Online Inference Latency ($\tau_{\text{inf}}$): Once trained, a single greedy forward pass through the PyTorch `DQNetwork` requires only $\tau_{\text{inf}} = 0.021\text{--}0.029\text{ ms}$, which is comparable to Greedy $K$-Center ($0.026\text{--}0.207\text{ ms}$) and faster than $K$-Means ($3.19\text{--}8.14\text{ ms}$) or GA ($12.88\text{--}75.87\text{ ms}$). However, for a static network deployment where no pre-trained policy exists for the target topology, training incurs $\omega_{\text{train}} = 21.26\text{ s}$ for 1,000 DQN episodes ($58.3\text{--}1086.2\text{ ms}$ for tabular RL) without improving upon the latency achieved directly by GA or $K$-Means.
4. Topology-Dependent Heuristic Performance and $N-1$ Survivability: Greedy $K$-Center remained on the latency-cost Pareto frontier across all 12 synthetic cells and performed best on scale-free Barabási-Albert topologies, whereas $K$-Means closely tracked GA on spatially embedded Waxman graphs. Under single-link ($N-1$) failure evaluation, 2-edge-connected topologies (Internet2, ATT-MPLS, and Barabási-Albert $m=2$) achieved $100.0\%$ survivability across all algorithms, whereas sparse Waxman graphs containing bridge links dropped to $94.47\%\text{--}98.79\%$.
5. Mininet Emulation and Phase 4 Gate Test: In five-way emulation on Internet2 ($N=20, k=3$), GA achieved the lowest mean RTT ($2.718\text{ ms}$), followed by $K$-Means ($2.852\text{ ms}$ mean RTT; $5.764\text{ ms}$ worst-case RTT), Greedy $K$-Center ($2.934\text{ ms}$), Bandit RL / DQN ($3.056\text{ ms}$), and Random ($3.374\text{ ms}$). In the 3-trial Phase 4 Mininet Gate Test (`results/mininet_overhead_validation.json`), active online loop execution averaged $889.82\text{ ms}$ while OS teardown in Phase D added $1,985.68\text{ ms}$, yielding a full lifecycle overhead of $2,875.49\text{ ms}$ (exceeding the $2,000\text{ ms}$ threshold in all 3 trials) and justifying post-convergence Mininet validation.
6. Dynamic Topology Churn and Break-Even Amortization ($T_{\text{break}}$): Across 1,000 dynamic link-churn states ($5\text{ seeds} \times 100\text{ epochs}$ on Internet2 and ATT-MPLS at $k=3$, `results/experiment_data/dynamic_churn_summary.csv`), pre-trained PyTorch DQN inference ($\tau_{\text{inf}} = 0.0213\text{--}0.0257\text{ ms/epoch}$) amortized its 200-episode cached training cost ($\omega_{\text{train}} = 772.79\text{--}921.69\text{ ms}$) after a mean of $T_{\text{break}} = 59.0\text{--}65.2\text{ epochs}$ against GA and $T_{\text{break}} = 145.8\text{--}207.6\text{ epochs}$ against $K$-Means, although classical heuristics maintained lower post-churn propagation latency.

## 5.2 CONTRIBUTIONS TO KNOWLEDGE

1. Methodological Separation of Training and Inference Costs: Demonstrated how separating offline training time ($\omega_{\text{train}}$) from online inference time ($\tau_{\text{inf}}$) alongside $N-1$ link-failure survivability clarifies the operational trade-off between heuristics and reinforcement learning.
2. Statistical and Structural Characterization of the CPP ($N \le 50$): Quantified the main effects of algorithm family ($F(4, 240) = 118.90$), topology family ($F(1, 240) = 249.21$), node scale ($F(1, 240) = 502.64$), and controller budget ($F(2, 240) = 114.93$) across 300 multi-seed observations.
3. Bounded Decision Framework: Formulated scenario-conditioned selection guidelines (Table 4.7 and Figure 4.6) strictly bounded to the tested static WAN regime ($N \le 50$).

## 5.3 PRACTICAL RECOMMENDATIONS FOR NETWORK ENGINEERS

Within static wide-area networks up to $N = 50$ nodes:

1. Use Spatial $K$-Means Clustering ($3.19\text{--}8.14\text{ ms}$ runtime) for geographically embedded regional meshes where minimizing average switch-to-controller propagation delay is the primary objective.
2. Use Greedy $K$-Center ($0.026\text{--}0.207\text{ ms}$ runtime) for scale-free hub-and-spoke backbones or compute-constrained management planes requiring sub-millisecond placement calculation.
3. Use Genetic Algorithms ($12.9\text{--}75.9\text{ ms}$ runtime) during offline capacity planning when minimizing both average latency and bridge-isolation risk on sparse topologies is prioritized over sub-millisecond runtime.
4. Reserve Deep Reinforcement Learning for future evaluation in non-stationary environments where a pre-trained policy's fast forward-pass inference ($\tau_{\text{inf}} = 0.021\text{--}0.029\text{ ms}$) can be reused across repeated online topological changes without retraining from scratch.

## 5.4 FUTURE RESEARCH DIRECTIONS

1. Online Topology Churn and Dynamic Traffic Traces: Extending the benchmark to evaluate time-varying NetFlow traffic loads and sequential link/node churn in Mininet to test whether pre-trained DRL policies amortize their offline training cost during live switch migration.
2. Graph Neural Networks (GNNs) for Scale Generalization: Replacing the fixed-dimension MLP ($N \to 64 \to 64 \to N$) with Graph Convolutional or Graph Attention Networks capable of zero-shot inference across variable graph sizes ($N \in [100, 500]$).
3. Multi-Link ($N-k$) Failures and Controller Synchronization Overhead: Extending the single-link failure engine to model correlated multi-link cuts, controller node crashes, and east-west Raft consensus latencies across distributed controller clusters.
