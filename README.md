# AI-Driven Controller Placement Optimization in Multi-Site Software Defined Networks

A high-performance React application for decision-grade, multi-objective benchmarking and visualization of AI and heuristic controller placement in Software Defined Networks (SDN).

## Overview

When should network engineers adopt AI-driven optimization methods (such as Genetic Algorithms or Reinforcement Learning) for controller placement in Software Defined Networks, and when are simpler, faster heuristic approaches (such as Greedy k-Center) sufficient?

This application provides an interactive decision workbench and benchmarking suite to investigate trade-offs between:
- **Control-plane Latency**: Average and worst-case shortest path delay from OpenFlow switches to assigned controllers.
- **Resilience & Reliability**: N-1 controller failure degradation ratio and single-link failure reachability percentage.
- **Computational Cost & Real-Time Agility**: Algorithmic runtime, convergence iterations, and Pareto compromise ranking.

---

## Key Features

1. **Interactive Benchmark Lab**:
   - Canonical reference backbones: Internet2 (11 nodes) and AT&T MPLS (21 nodes) from Heller et al. (2012).
   - Synthetic network models: Barabási-Albert (scale-free preferential attachment), Waxman (geographic random graph), and Multi-Site Ring & Mesh topologies.
   - Interactive SVG Network Visualizer with node inspection, controller halo domains, and switch allocation.
   - **Interactive Fault Injection**: Click any link to simulate link severing, or click a controller to simulate crash failure, and watch metrics recompute dynamically.

2. **Full Algorithmic Placement Suite**:
   - **Greedy k-Center**: 2-approximation farthest-first heuristic (Gonzalez 1985, Heller 2012).
   - **Genetic Algorithm (GA)**: Multi-generation evolutionary search with elitism, tournament selection, crossover, and mutation.
   - **Bandit RL / AP-DQN Policy**: Multi-armed bandit reinforcement learning with epsilon-decay exploration and composite reward shaping.
   - **k-Means Clustering**: Spatial coordinate clustering with centroid-to-node mapping.
   - **Random Placement**: Stochastic floor baseline for statistical contrast.

3. **Multi-Objective Pareto Decision Frontier**:
   - Identification of non-dominated Pareto-optimal placements.
   - Normalized Euclidean distance ranking from the ideal point $(L_{\min}, R_{\max})$.
   - 2D and 3D trade-off views (Latency vs. Reliability, Latency vs. Solver Runtime).

4. **Factorial Benchmark Matrix (60 Scenarios)**:
   - Complete pre-computed experimental dataset across Barabási-Albert and Waxman topologies ($N \in \{20, 50, 100\}$, $k \in \{3, 5\}$).
   - Interactive sorting, filtering, and SPSS/GENSTAT compatible CSV export.

5. **Deductive Research Hub**:
   - Empirical validation of Hypotheses H1 (Latency Superiority), H2 (Computational Efficiency), and H3 (Topology Sensitivity).
   - IEEE-formatted literature references (Heller, Gonzalez, Farahi, Barabási, Waxman).
   - Technical Stack Defense (Section 8.4.1).

---

## Technical Stack

- **Framework**: React 19 + TypeScript
- **Bundler & Server**: Vite (listening on `0.0.0.0:3000`)
- **Styling**: Tailwind CSS v4
- **Icons**: Lucide React
- **Algorithms**: Pure TypeScript graph algorithms with deterministic Mulberry32 pseudo-random generator

## Getting Started

```bash
npm install
npm run dev
```

Visit `http://localhost:3000` to interact with the application.
