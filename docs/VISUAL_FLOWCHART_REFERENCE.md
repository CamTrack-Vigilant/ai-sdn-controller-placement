# Visual Flowchart Reference Guide
## Study Design & Experimental Workflow Diagrams

**Project:** AI-Driven Controller Placement Optimization in Multi-Site SDN  
**Date:** April 28, 2026  
**Document Version:** 1.0

---

## 📊 Diagram Overview

This document provides a quick reference to all visual flowcharts and their relationships in your research workflow.

### Diagram 1: Complete Experimental Workflow (Phase 1-4)

**Purpose:** High-level overview of the entire study from environment setup through analysis.

**Scope:** Shows all four phases:
- ✅ **Phase 1:** Environment setup, dependency validation, baseline checks
- 🟡 **Phase 3:** Factorial execution with nested loops (30 seeds × 3 topologies × 3 budgets × 4 algorithms × 5 trials)
- 📊 **Phase 4:** Data aggregation, statistical analysis, result synthesis
- ✍️ **Output:** Thesis integration

**Key Elements:**
- Nested factorial loop structure with decision points
- Algorithm selection branching (Greedy, DQN, Random, Baseline)
- Thermal cooldown management (60-300 seconds)
- Phase transitions and conditional checks

**When to Reference:** 
- For understanding end-to-end project flow
- When presenting to supervisors or defense panel
- For project status updates (which phase are we in?)

**CSV Output:**
```
results/experiment_data/
├── greedy_internet2.csv (360 rows)
├── dqn_internet2.csv (360 rows)
├── random_internet2.csv (360 rows)
├── baseline_internet2.csv (360 rows)
├── ... [similar for ATT-MPLS, Synthetic-BA]
└── experiment_master.csv (10,800 rows consolidated)
```

---

### Diagram 2: Per-Trial Measurement Protocol

**Purpose:** Detail the exact steps executed for each individual trial within the factorial matrix.

**Scope:** Single [Algorithm, Topology, k, Seed] cell with 5 trials.

**Steps Executed per Trial:**

1. **Algorithm Execution**
   - Input: Topology G=(V,E), controller budget k
   - Output: Placement P (set of k controller nodes)
   - Runtime: Measured as ω

2. **Latency Measurement L(P)**
   ```
   L(P) = (1/|V|) × Σ min_distance(v_i, P)
   Units: milliseconds
   Range: 1.0–15.0 ms (typical)
   ```

3. **Reliability Measurement R_avg(P)**
   ```
   FOR each link e in E:
       Remove e, check if all nodes reachable from P
       Count as 1 (reachable) or 0 (isolated)
   R_avg = count / |E|
   Units: [0.0, 1.0]
   Range: 0.85–1.0 (well-designed placements)
   ```

4. **Complexity Measurement ω**
   ```
   ω = (t_end - t_start) / episode_count
   Units: seconds per episode
   Typical ranges:
     - Greedy: 0.00001–0.00005 s
     - DQN: 0.0226 ± 0.003 s
     - Random: 0.000001–0.000005 s
   ```

5. **Secondary Metrics**
   - Load balance fairness: σ(controller_loads)
   - Convergence speed: Episodes to 95% (DQN only)
   - Worst-case distance: max d_i
   - Cost-benefit ratio: ΔL / ω

6. **CSV Recording**
   ```csv
   algorithm,topology,k,seed,latency_ms,reliability_ravg,complexity_s,...
   DQN,Internet2,3,42,2.9379,1.0,0.0226,...
   ```

**When to Reference:**
- When implementing the trial execution code
- When troubleshooting metric calculations
- For understanding how data is generated

**Expected Timing per Trial:**
- Greedy: ~0.1 seconds (fast)
- DQN: ~25-30 seconds (training overhead)
- Random: ~0.001 seconds (instant)
- Measurement & I/O: ~1 second
- **Total per trial:** ~1-30 seconds depending on algorithm

---

### Diagram 3: Phase 4 Analysis Pipeline

**Purpose:** Detail post-experiment statistical analysis and interpretation workflow.

**Scope:** May 9 – June 14, 2026 (after all 10,800 trials completed).

**Analysis Steps:**

#### Step 1: Data Aggregation
```
Input: 72 algorithm_topology.csv files
  ├─ greedy_internet2.csv (360 rows)
  ├─ dqn_internet2.csv (360 rows)
  ├─ random_internet2.csv (360 rows)
  ├─ baseline_internet2.csv (360 rows)
  └─ ... [all algorithm-topology combinations]
  
Output: experiment_master.csv (10,800 rows)
  └─ Columns: algorithm, topology, k, seed, latency_ms, 
              reliability_ravg, complexity_s, load_std,
              convergence_episodes, placement_nodes, timestamp_utc
```

#### Step 2: Descriptive Statistics
```
Groupby [algorithm, topology, k]: 72 unique cells × 150 samples/cell

For each cell, compute:
  • Mean latency ± 95% CI (t-distribution)
  • Median, Q1, Q3 of latency distribution
  • Boxplot visualizations (6 panels, one per topology)
  
  • Mean reliability ± 95% CI
  • Violin plots (reliability by k value)
  
  • Mean complexity ± CI
  • Bar charts (complexity, log-scale with error bars)
```

#### Step 3: Inferential Analysis

**A) Multi-Way ANOVA**
```
Model: latency ~ algorithm + topology + controller_budget 
                  + scale + algorithm:topology 
                  + algorithm:controller_budget + ...

Null Hypothesis (H₀): 
  Algorithm has no effect on latency (and other factors)

Test:
  α = 0.05 (significance level)
  Expected: p < 0.05 → Reject H₀
  
Post-hoc:
  Tukey HSD pairwise comparisons (α = 0.05)
```

**B) Pareto Front Analysis (3D)**
```
For each [topology, k] cell:

1. Extract all placements: {(L_i, R_i, ω_i) for each algorithm}

2. Identify non-dominated solutions:
   Solution X dominates Solution Y if:
     • L_X ≤ L_Y (lower latency is better)
     • R_X ≥ R_Y (higher reliability is better)  
     • ω_X ≤ ω_Y (lower complexity is better)
   
3. Pareto-optimal = not dominated by any other solution

4. Output:
   • Count of Pareto solutions per algorithm (typically 1-3)
   • Hypervolume (3D volume dominated by algorithm)
   • Recommendation per scenario
```

**C) Cross-Scenario Stability (Spearman ρ)**
```
Scenario 1: Internet2, k=3   → Algorithm ranking [A1, A2, A3, A4]
Scenario 2: ATT-MPLS, k=5   → Algorithm ranking [A_?, A_?, A_?, A_?]
Scenario N: Synthetic, k=2  → ...

Spearman Rank Correlation (ρ) between scenario pairs:
  • ρ > 0.7: Rankings are stable (method generalizes)
  • 0.6 < ρ ≤ 0.7: Moderate stability
  • ρ < 0.6: Rankings scenario-dependent (context matters)

Output: Rank correlation heatmap (scenarios × scenarios)
```

#### Step 4: Synthesis & Interpretation

**Decision Questions:**
1. Which algorithms are Pareto-optimal? (On the frontier, not dominated)
2. Are algorithm rankings stable across scenarios? (Spearman ρ test)
3. Is AI computational cost (ω) justified by latency gains? (Cost-benefit)
4. Which scenario favors which algorithm? (Recommendation matrix)

**Cost-Benefit Analysis:**
```
For each algorithm pair comparison (e.g., DQN vs. Greedy):

Gain = ΔL = L_Greedy - L_DQN    (latency improvement, ms)
Cost = Δω = ω_DQN - ω_Greedy    (computational overhead, s)
Ratio = Gain / Cost              (improvement per second of compute)

Decision Threshold:
  IF Ratio > threshold → AI worth the computational cost
  IF Ratio < threshold → Greedy preferred (faster, sufficient latency)
```

**Output: Recommendation Matrix**
```
┌──────────────────────────────────────────────┐
│ Topology  │ k │ Scale │ Recommendation      │
├──────────────────────────────────────────────┤
│ Internet2 │ 3 │ Med   │ Greedy (low ω)      │
│ Internet2 │ 5 │ Med   │ DQN (gain ≥ cost)   │
│ ATT-MPLS  │ 3 │ Large │ Baseline (stable)   │
│ Synthetic │ 2 │ Med   │ Tie (~equal perf)   │
└──────────────────────────────────────────────┘
```

**When to Reference:**
- During Phase 4 (May-June) analysis execution
- When writing thesis results chapter
- For understanding statistical significance vs. practical significance
- When justifying recommendations to stakeholders

**Deliverables:**
- `experiment_master.csv` (10,800 rows with all metrics)
- `summary_statistics.csv` (72 rows, per-cell aggregates)
- `pareto_analysis.json` (domination relationships)
- Publication-quality figures (5 key plots)

---

### Diagram 4: Factorial Design Matrix Structure

**Purpose:** Visual representation of the balanced experimental design and factor combinations.

**Scope:** All 2,160 unique experimental cells (72 × 30 seeds).

**Factor Breakdown:**

| Factor | Levels | Combinations | Example Values |
|--------|--------|--------------|---|
| **Algorithm (A)** | 4 | 4 | Greedy, DQN, Random, Baseline |
| **Topology (T)** | 3 | 4×3 = 12 | Internet2 (11n), ATT-MPLS (21n), Synthetic-BA (15n) |
| **Budget (K)** | 3 | 12×3 = 36 | k=2, k=3, k=5 |
| **Scale (S)** | 2 | 36×2 = 72 | Medium (≤15n), Large (≥20n) |
| **Seed (R)** | 30 | 72×30 = **2,160** | 42, 142, 242, ..., 2942 |
| **Trials/Cell** | 5 | 2,160×5 = **10,800** | (Repeated execution) |

**Example Experimental Cell:**
```
A2 (DQN) × T1 (Internet2) × K2 (k=3) × S1 (Medium) × R1 (Seed=42)
└─ 5 independent trials per cell
   └─ Each trial generates 1 CSV row (latency, reliability, complexity, ...)
```

**Design Properties:**
- ✅ **Balanced:** Equal replication per cell (5 trials/cell)
- ✅ **Full Factorial:** All 4×3×3×2 = 72 combinations with all 30 seeds
- ✅ **Randomized:** Deterministic seed progression for reproducibility
- ✅ **Interaction Detection:** Factorial structure allows main effects + interactions

**When to Reference:**
- When planning execution schedule (which cells to run first?)
- When calculating expected compute time
- For understanding statistical power (N=150 per cell)
- In methodology section of thesis

**Total Datapoints:** 10,800 observations for statistical inference

---

## 🔄 Workflow Integration

```
┌─────────────────────────────────────────────────────────────┐
│ COMPLETE EXPERIMENTAL WORKFLOW (Diagram 1)                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Phase 1: Setup                                              │
│ └─ Validate environment, run baseline, DQN pilot           │
│                                                             │
│ Phase 3: Factorial Execution (Nested loops)                │
│ ├─ FOR each seed in [42, 142, ..., 2942]:     (Diagram 4)  │
│ │ ├─ FOR each topology in [Internet2, ...]:   (Diagram 4)  │
│ │ │ ├─ FOR each k in [2, 3, 5]:               (Diagram 4)  │
│ │ │ │ └─ FOR each algorithm in [Greedy, ...]: (Diagram 4)  │
│ │ │ │   └─ Execute 5 trials per cell          (Diagram 2)  │
│ │ │ │       └─ Measure L(P), R_avg(P), ω      (Diagram 2)  │
│ │ │ │       └─ Record to CSV                   (Diagram 2)  │
│ │ │ │                                          (Diagram 1)  │
│ │ │ └─ [Thermal cooldown: 60-300s]                        │
│ │ │                                          (Diagram 1)  │
│ │ └─ [Next topology]                         (Diagram 1)  │
│ │                                          (Diagram 1)  │
│ └─ [Next seed]                             (Diagram 1)  │
│                                                             │
│ Phase 4: Post-Experiment Analysis             (Diagram 3)  │
│ ├─ Aggregate 10,800 rows into master CSV                  │
│ ├─ Descriptive statistics (means, CIs, plots)              │
│ ├─ Inferential analysis (ANOVA, Pareto, stability)         │
│ ├─ Synthesis (cost-benefit, recommendations)               │
│ └─ Thesis integration (Chapter 5)                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Quick Reference Checklist

### Before Phase 3 Execution:
- [ ] Review Diagram 1 (complete workflow) for phase understanding
- [ ] Review Diagram 4 (factorial matrix) for design structure
- [ ] Confirm: 10,800 total trials expected (2,160 cells × 5 trials)

### During Phase 3 Execution:
- [ ] Use Diagram 2 (per-trial protocol) for measurement implementation
- [ ] Verify each CSV row has: algorithm, topology, k, seed, latency, reliability, complexity
- [ ] Monitor thermal cooldown (60-300s) per Diagram 1

### During Phase 4 Analysis:
- [ ] Use Diagram 3 (analysis pipeline) for structured inference
- [ ] Follow order: Aggregation → Descriptive → Inferential → Synthesis
- [ ] Generate 5 key figures and recommendation matrix

---

## 📚 Related Documents

| Document | Purpose | Location |
|----------|---------|----------|
| **STUDY_DESIGN_METHODOLOGY.md** | Full methodological details | docs/ |
| **experiment_config.json** | Configuration parameters | configs/ |
| **proposal.md** | Proposal with theoretical framework | docs/ |
| **RESEARCH_LOG.md** | Pilot results & progress log | Project root |

---

**Version:** 1.0  
**Created:** April 28, 2026  
**Last Updated:** April 28, 2026  
**Status:** Ready for Phase 3 execution

