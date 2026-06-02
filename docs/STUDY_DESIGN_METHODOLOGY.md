# Study Design and Methodology
## AI-Driven Controller Placement Optimization in Multi-Site SDN

**Research Institution:** University of Zululand, Faculty of Science, Agriculture & Engineering  
**Program:** Honors (B.Sc.) Computer Science  
**Principal Investigator:** Thabang Mhlokoma  
**Date:** April 28, 2026  
**Status:** Active (Phase 2-3 Execution)

---

## 1. Study Design Overview

### 1.1 Research Design Classification

**Study Type:** Comparative Empirical Research with Factorial Experimental Design  
**Paradigm:** Quantitative, Reproducible, Computer-Based Simulation  
**Duration:** February – November 2026 (40 weeks)  
**Sample Unit:** Algorithm-Topology-Scale Combinations (Simulated Controller Placements)  
**Allocation Method:** Full Factorial Design with Blocked Randomization

### 1.2 Primary Research Question

In multi-site synthetic SDN topologies $G=(V,E)$, do AI-driven controller placement methods provide superior multi-objective decision quality compared with baseline heuristics when latency $L(P)$ (ms), reliability $Reach_{avg}$ (dimensionless), and complexity $\omega$ (s/episode) are evaluated jointly?

### 1.3 Core Hypothesis

**Null Hypothesis (H₀):**  
AI-driven methods (DQN/DRL) produce no statistically significant improvement in multi-objective performance (latency, reliability, computational cost combined) compared to deterministic baseline methods (Greedy k-center, Random, Baseline heuristics) across representative topologies.

**Alternative Hypothesis (H₁):**  
AI-driven methods achieve statistically and operationally significant improvements in multi-objective performance that justify computational cost overhead, measured as non-dominated positions in the 3D Pareto frontier (latency, reliability, complexity).

### 1.4 Study Objectives

| Objective | Metric | Success Criterion |
|-----------|--------|-------------------|
| **Obj 1:** Establish reproducible SDN testbed | Successful baseline execution | Baseline algorithm completes ≥5 trials with <5% metric variance |
| **Obj 2:** Compare AI vs. Heuristic methods | Effect size (latency, reliability) | AI shows ±10% latency variance, reliability ≥0.95 |
| **Obj 3:** Quantify complexity trade-offs | Runtime $\omega$ (s/episode) | Compute cost vs. gain ratio documented for each method |
| **Obj 4:** Identify Pareto-optimal placements | Non-dominated set size | ≥3 methods present on Pareto frontier per topology-scale cell |
| **Obj 5:** Validate scalability & stability | Cross-scenario rank stability | Method rankings remain consistent across ≥80% of scenarios |

---

## 2. Experimental Design Structure

### 2.1 Factorial Design Matrix

This study employs a **Full Factorial Experimental Design** where multiple independent variables (factors) are systematically varied to measure their joint effects on outcome variables.

#### 2.1.1 Independent Variables (Factors)

| Factor | Levels | Values | Rationale |
|--------|--------|--------|-----------|
| **Algorithm (A)** | 4 | Greedy k-center, DQN, Random, Baseline | Compare AI vs. deterministic methods |
| **Topology (T)** | 3 | Internet2 (11 nodes), ATT-MPLS (21 nodes), Synthetic BA (15 nodes) | Test canonical real-world + synthetic |
| **Controller Budget (K)** | 3 | k=2, k=3, k=5 | Standard placement configurations |
| **Network Scale (S)** | 2 | Medium (11-15 nodes), Large (21 nodes) | Assess scalability behavior |
| **Random Seed (R)** | 30 | Seeds: {42, 100, 200, ..., 2900} | Statistical power via replication |

**Total Factorial Combinations:** 4 × 3 × 3 × 2 × 30 = **2,160 experimental cells**

#### 2.1.2 Dependent Variables (Outcomes)

| Outcome | Definition | Unit | Range | Collection Method |
|---------|-----------|------|-------|-------------------|
| **Latency** $L(P)$ | Mean controller distance (hops) | ms | 1–10 | Graph-based path computation |
| **Reliability** $Reach_{avg}$ | Control-plane reachability after single-link failure | dimensionless | 0–1 | Exhaustive link removal test |
| **Complexity** $\omega$ | Algorithm runtime per placement decision | s/episode | 10⁻⁵–10 | Instrumented wall-clock timing |
| **Convergence** | Episodes to reach 95% of best-found latency | episodes | 50–1000 | Training history tracking |
| **Load Balance** | Std. Dev. of controller load distribution | - | 0–1 | Controller assignment histogram |

#### 2.1.3 Control Variables (Held Constant)

| Variable | Value | Purpose |
|----------|-------|---------|
| **Random Seed Base** | 42 (primary), deterministic increments | Reproducibility anchor |
| **Topology Seed** | Deterministic per topology | Fixed topology structure |
| **Optimization Objective** | Weighted: latency 1.0, reliability 0.25 | Consistent reward signal |
| **DQN Architecture** | Input(n) → FC(64) → FC(64) → Output(n) | Uniform neural network |
| **Evaluation Environment** | Mininet + Ryu SDN controller | Standardized simulation |
| **Inference Mode** | Greedy (deterministic policy) after training | No exploration during measurement |

### 2.2 Study Design Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│         FACTORIAL EXPERIMENTAL STRUCTURE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FACTOR 1: Algorithm Selection (A)                              │
│  ├─ A1: Greedy k-center (baseline heuristic)                    │
│  ├─ A2: DQN (deep Q-learning, AI-driven)                        │
│  ├─ A3: Random placement (lower bound)                          │
│  └─ A4: Baseline heuristic variant                              │
│                                                                 │
│  FACTOR 2: Topology Type (T)                                    │
│  ├─ T1: Internet2 real backbone (11 nodes)      ← Canonical    │
│  ├─ T2: ATT-MPLS real backbone (21 nodes)      ← Canonical    │
│  └─ T3: Synthetic Barabasi-Albert (15 nodes)   ← Generalize   │
│                                                                 │
│  FACTOR 3: Controller Budget (K)                                │
│  ├─ K1: k=2 controllers                                         │
│  ├─ K2: k=3 controllers                                         │
│  └─ K3: k=5 controllers                                         │
│                                                                 │
│  FACTOR 4: Network Scale (S)                                    │
│  ├─ S1: Medium (≤15 nodes)                                      │
│  └─ S2: Large (≥20 nodes)                                       │
│                                                                 │
│  FACTOR 5: Random Seed Replication (R) [30 seeds]              │
│  ├─ R1: Seed = 42 (primary anchor)                              │
│  ├─ R2: Seed = 142                                              │
│  ├─ ...                                                         │
│  └─ R30: Seed = 2942                                            │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  FULL FACTORIAL: 4 × 3 × 3 × 2 × 30 = 2,160 combinations      │
│  Per-cell trials: 5 independent algorithm runs                 │
│  Total datapoints: 2,160 × 5 = 10,800 observations             │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Blocked Randomization Strategy

To minimize thermal and computational drift, experiments are executed in **18 thermal-safe blocks**:

```
Block Structure (18 segments × 60 trials/block = 1,080 trials per seed):
├─ Segment 1-3:   Algorithm A1 (Greedy) across all topologies
├─ Segment 4-6:   Algorithm A2 (DQN) across all topologies
├─ Segment 7-9:   Algorithm A3 (Random) across all topologies
├─ Segment 10-12: Algorithm A4 (Baseline variant) across all topologies
├─ Segment 13-18: Sensitivity analysis + convergence sweeps
└─ [60-second thermal cooldown between segments]
```

**Rationale:** Keeps CPU temperature <60°C, ensures fair wall-clock timing measurement, supports resumable execution after interruption.

---

## 3. Sample Size and Allocation

### 3.1 Sample Size Calculation

The sample size is determined by **pilot-validated computational feasibility** rather than statistical power alone.

#### 3.1.1 Pilot Study Evidence

- **Pilot Completion:** Phase 1 (February 2026) ✅ Complete
- **Pilot Result:** $\omega_{pilot} = 0.0226$ seconds/episode (measured on x86_64 CPU)
- **Pilot Trials:** 50 DQN episodes on single Internet2 topology
- **Inference:** Full factorial matrix is computationally tractable

#### 3.1.2 Full Study Sample Calculation

```
Sample Composition:

Primary Factorial Cells: 4 algorithms × 3 topologies × 3 budgets × 2 scales
  = 72 unique experimental conditions

Replication Factor: 30 random seeds × 5 trials per seed
  = 150 samples per experimental cell

Total Observations: 72 × 150 = 10,800 datapoints

Projected Compute Time:
  - Per trial: ~0.0226 s/episode (pilot validated)
  - Trials per seed: 72 × 5 = 360 trials
  - Time per seed: 360 × 0.0226 s ≈ 8.1 seconds
  - 30 seeds: 30 × 8.1 s ≈ 243 seconds ≈ 4.05 minutes
  - Full matrix (with overhead): ~18 hours wall-clock time
```

#### 3.1.3 Statistical Power Justification

| Metric | Method | Effect Size | Desired Power | N Required |
|--------|--------|-------------|---------------|-----------| 
| Latency | ANOVA | Cohen's f=0.25 | 0.80 | 30+ per cell |
| Reliability | Chi-square | w=0.30 | 0.80 | 25+ per cell |
| Complexity | t-test | Cohen's d=0.50 | 0.90 | 66+ per cell |

**Actual N per cell:** 150 > 66 ✅ **Sufficient statistical power**

### 3.2 Allocation to Groups

#### 3.2.1 Algorithm Allocation

```
Group A1 (Greedy k-center):
  - Sample size: 2,700 placements (25% of total)
  - Role: Baseline heuristic, computational efficiency anchor
  - Deterministic: No randomness in algorithm, only topology seed variation

Group A2 (DQN/Deep Q-Learning):
  - Sample size: 2,700 placements (25% of total)
  - Role: AI-driven primary intervention
  - Stochastic: Random seed controls neural network initialization
  - Training epochs per trial: 1,000 episodes (per pilot config)

Group A3 (Random Placement):
  - Sample size: 2,700 placements (25% of total)
  - Role: Lower bound performance reference
  - Deterministic random: Seeded via topology seed

Group A4 (Baseline Heuristic Variant):
  - Sample size: 2,700 placements (25% of total)
  - Role: Comparative heuristic, robustness check
  - Heuristic: Variation of classical k-center (e.g., medoid-based)
```

#### 3.2.2 Topology Allocation

```
Internet2 (Canonical Real Backbone, 11 nodes):
  - Assignments: 1/3 of all 10,800 observations = 3,600 placements
  - Controller budgets: k ∈ {2, 3, 5}
  - Seeds: 30 independent replicates
  - Rationale: Golden-standard reference (Heller et al. 2012)

ATT-MPLS (Canonical Real Backbone, 21 nodes):
  - Assignments: 1/3 of all 10,800 observations = 3,600 placements
  - Controller budgets: k ∈ {2, 3, 5}
  - Seeds: 30 independent replicates
  - Rationale: Larger scale, different graph structure

Synthetic Barabasi-Albert (15 nodes, medium):
  - Assignments: 1/3 of all 10,800 observations = 3,600 placements
  - Controller budgets: k ∈ {2, 3, 5}
  - Seeds: 30 independent replicates
  - Rationale: Generalization, robustness to synthetic distributions
```

#### 3.2.3 Seed Allocation (Randomization Schedule)

```
Primary Seed: 42 (Seed_0)
  └─ Baseline validation, full telemetry capture

Sweep Seeds: 42 + 100×i for i = 0, 1, ..., 29
  ├─ Seed_1 = 142
  ├─ Seed_2 = 242
  ├─ ...
  └─ Seed_30 = 2942

Rationale:
  - Deterministic, auditable, reproducible
  - Stride of 100 ensures distinct random states
  - 30 replicates provide robust statistical inference
  - Primary seed (42) reserved for intensive telemetry
```

---

## 4. Research Procedures & Protocols

### 4.1 Baseline (Pre-Experiment) Procedures

#### 4.1.1 Environment Setup (February 2026, Phase 1)

```
Step 1: Repository Initialization ✅
  ├─ Clone ai-sdn-controller-placement repository
  ├─ Install dependencies: PyTorch, NetworkX, Mininet, Ryu
  ├─ Verify smoke test: Import all modules, run hello-world topology
  └─ Output: ENVIRONMENT_CHECK.log

Step 2: Topology Data Ingest ✅
  ├─ Load Internet2 (11-node real graph)
  ├─ Load ATT-MPLS (21-node real graph)
  ├─ Generate Barabasi-Albert (15-node, seed=42)
  ├─ Validate: Check connectivity, diameter, clustering coeff.
  └─ Output: topology_validation_report.csv

Step 3: Baseline Algorithm Validation ✅
  ├─ Run Greedy k-center on each topology (k=3, seed=42)
  ├─ Measure: latency, reliability, runtime
  ├─ Compare to literature baselines (Heller et al. 2012)
  ├─ Target: ±10% agreement with literature
  └─ Output: baseline_validation.json

Step 4: DQN Configuration & Pilot ✅
  ├─ Initialize DQN with config from experiment_config.json
  ├─ Run 50-episode pilot on Internet2 (seed=42)
  ├─ Measure: convergence speed, final latency, CPU utilization
  ├─ Target: <0.03 s/episode average runtime
  └─ Output: pilot_metrics.json, PILOT_RUN_REPORT.md
```

#### 4.1.2 Quality Assurance Checklist

| Item | Status | Verification |
|------|--------|-------------|
| Dependencies installed | ✅ | `import torch; import mininet; import ryu` succeed |
| Topology data validated | ✅ | All graphs connected, node counts match |
| Baseline algorithm works | ✅ | Greedy produces consistent placements |
| DQN model initializes | ✅ | Network weights properly seeded |
| Output directories writable | ✅ | CSV and log files created successfully |
| Telemetry collection active | ✅ | CPU/memory sampling functions operational |

### 4.2 Experimental Execution Procedures

#### 4.2.1 Per-Trial Protocol (Repeated 10,800 times across factorial matrix)

```
For each [Algorithm, Topology, k, Seed] combination:

┌─ Trial Setup ────────────────────────────────┐
│ 1. Initialize topology with deterministic    │
│    seed (topology_seed = [topology_id, seed])│
│ 2. Load controller placement algorithm       │
│ 3. Open instrumentation (telemetry thread)   │
└──────────────────────────────────────────────┘
       ↓
┌─ Algorithm Execution ─────────────────────────┐
│ IF Algorithm = Greedy k-center:               │
│   • Run farthest-first heuristic in O(nk)    │
│   • Return deterministic placement            │
│ ELSE IF Algorithm = DQN:                      │
│   • Initialize DQN network                    │
│   • Train for 1,000 episodes                  │
│   • Extract greedy policy (no exploration)    │
│   • Return learned placement                  │
│ ELSE IF Algorithm = Random:                   │
│   • Uniformly sample k nodes from V           │
│   • Return random placement                   │
│ END IF                                        │
│ [Record: wall-clock time ω]                   │
└──────────────────────────────────────────────┘
       ↓
┌─ Measurement Phase ───────────────────────────┐
│ For the resulting placement P:                │
│                                               │
│ 1. Latency L(P):                              │
│    • Compute shortest-path distance from      │
│      each node to nearest controller in P     │
│    • Average across all nodes                 │
│    • Units: milliseconds (hops × 1ms/hop)    │
│                                               │
│ 2. Reliability R_avg(P) via:                  │
│    Exhaustive single-link failure:            │
│      FOR each link e in E:                    │
│        • Remove link e from topology          │
│        • Check: Is every node reachable?      │
│        • Record: reachable_count              │
│      r_avg = reachable_count / |E|            │
│    Units: [0,1], 1.0 = fully resilient       │
│                                               │
│ 3. Complexity ω:                              │
│    • Elapsed wall-clock time from Step 1      │
│    • For Greedy: ~0.00002 s                   │
│    • For DQN: ~0.0226 s (pilot baseline)      │
│    • Units: seconds/episode                   │
│                                               │
│ 4. Load Balance:                              │
│    • Count nodes → controllers assignments    │
│    • StdDev of assignment distribution        │
│    • Units: dimensionless, 0=perfect balance  │
│                                               │
│ 5. Convergence (DQN only):                    │
│    • Track reward per training episode        │
│    • Find: iterations to reach 95% final      │
│    • Units: episode count                     │
│                                               │
└──────────────────────────────────────────────┘
       ↓
┌─ Data Recording ──────────────────────────────┐
│ CSV Row Format:                               │
│ algorithm, topology, k, seed, latency_ms,    │
│ reliability_ravg, complexity_s, load_std,    │
│ convergence_episodes, timestamp_utc           │
│                                               │
│ File: results/experiment_data/               │
│       [algorithm]_[topology].csv              │
│                                               │
│ Telemetry CSV (optional for Greedy baseline): │
│ timestamp_utc, elapsed_s, pid, cpu_percent,   │
│ rss_memory_mb, status                         │
│                                               │
└──────────────────────────────────────────────┘
```

#### 4.2.2 Blocked Execution Schedule

The 10,800 trials are executed in **18 thermal-safe segments** with mandatory cooldown:

```
SEGMENT ALLOCATION (30 seeds × 36 trials/segment = 1,080 total per seed):

Seed 42 (Primary, intensive telemetry):
├─ Segment 1-3:   Greedy k-center (all topologies)        [8.1 min]
├─ Segment 4-6:   DQN training (all topologies)          [815 min = 13.6 hrs] ⚠️
├─ [300s cooldown]
├─ Segment 7-9:   Random placement (all topologies)      [12 min]
├─ [300s cooldown]
├─ Segment 10-12: Baseline variant (all topologies)      [8.1 min]
├─ [300s cooldown]
├─ Segment 13-18: Sensitivity + convergence sweeps       [varies]
└─ Total time: ~18 hours (seed 42 alone, CPU-bound)

Seed 142, 242, ..., 2942 (Remaining 29 seeds):
├─ Parallel execution where possible (multiple machines)
├─ Sequential execution on single machine:
│  └─ 29 seeds × 18 hours/seed = 522 hours = 21.75 days
│     BUT: Most operations are non-blocking → Use async dispatch
├─ Recommended schedule:
│  └─ Dispatch 3 seeds per day on background processes
│  └─ Total calendar time: 10 days (April 28 - May 8)
└─ Total cumulative CPU time: 522 hours
```

#### 4.2.3 Quality Control During Execution

| Checkpoint | Frequency | Check | Action if Failed |
|------------|-----------|-------|------------------|
| Segment completion | Per segment | CSV written, row count ≥95 | Retry segment |
| Outlier detection | Per 100 rows | Latency within [0.5, 15] ms | Flag for review |
| Memory usage | Per hour | RSS < 2GB | Pause and cool down |
| Disk space | Per 50MB | Remaining > 10GB | Archive old logs |
| Crash recovery | On restart | Check segment manifest | Resume from checkpoint |

### 4.3 Post-Experiment Procedures

#### 4.3.1 Data Aggregation (May 2026, Phase 5)

```
Step 1: CSV Consolidation
  ├─ Read all algorithm_topology.csv files from results/experiment_data/
  ├─ Combine into single master dataframe (10,800 rows)
  ├─ Validate: No duplicates, all expected factor combinations present
  └─ Output: experiment_master.csv

Step 2: Pareto Front Identification
  FOR each [topology, k] cell:
    • Extract all [algorithm, latency, reliability, complexity] tuples
    • Identify non-dominated solutions:
      - Solution X dominates Solution Y if X ≤ Y on all 3 axes
    • Record domination count per algorithm
  └─ Output: pareto_analysis.json

Step 3: Summary Statistics
  GROUPBY [algorithm, topology, k]:
    • Mean latency (ms), Std. Dev.
    • Mean reliability, Std. Dev.
    • Mean complexity (s), Std. Dev.
    • Rank (1=best latency, etc.)
  └─ Output: summary_statistics.csv

Step 4: Cross-Scenario Stability Analysis
  • Compute rank correlation of algorithms across scenarios
  • Test: Do algorithm rankings change significantly?
  • Output: stability_matrix.csv
```

---

## 5. Measurement and Data Collection

### 5.1 Primary Metrics

#### 5.1.1 Latency $L(P)$ – Milliseconds

**Definition:**
$$L(P) = \frac{1}{|V|} \sum_{v_i \in V} \min_{c \in P} d(v_i, c)$$

Where $d(v_i, c)$ is the shortest-path distance in hops, converted to milliseconds as $1 \text{ hop} \approx 1 \text{ ms}$ (standard SDN assumption).

**Measurement Protocol:**
1. Compute all-pairs shortest-path distances using Floyd-Warshall (offline)
2. For each node $v_i$, find minimum distance to any controller in placement $P$
3. Average across all nodes
4. Report to 4 decimal places (e.g., 2.8932 ms)

**Collection Method:** Graph-based (no simulation required for algorithmic latency)

**Expected Range:** 1.0–15.0 ms (depends on topology density and controller budget)

#### 5.1.2 Reliability $R_{avg}(P)$ – Dimensionless [0, 1]

**Definition (Control-Plane Survivability):**
$$R_{avg}(P) = \frac{1}{|E|} \sum_{e \in E} I[\text{all nodes reachable after removing } e]$$

Where $I[\cdot]$ is the indicator function (1 if condition true, 0 otherwise).

**Measurement Protocol:**
1. For each link $e = (u, v)$ in edge set $E$:
   - Temporarily remove link $e$ from topology
   - Check: Can every node in $V$ reach at least one controller in $P$ via shortest path?
   - If YES → count as 1, if NO → count as 0
2. Average the indicator values across all links
3. Report as decimal [0.0, 1.0]

**Collection Method:** Exhaustive graph-theoretic simulation

**Interpretation:**
- $R_{avg} = 1.0$: Placement is fully survivable (no single-link failure isolates any node)
- $R_{avg} = 0.5$: Half of link failures still leave all nodes reachable
- $R_{avg} = 0.0$: Any single link failure disconnects at least one node

**Expected Range:** 0.85–1.0 for well-designed placements

#### 5.1.3 Complexity $\omega$ – Seconds per Episode

**Definition:**
$$\omega = \text{wall-clock time (seconds)} \div \text{number of episodes or iterations}$$

**Measurement Protocol:**
1. Record $t_{start}$ = high-resolution clock time (nanoseconds) at algorithm start
2. Execute algorithm (iterations as defined per method):
   - Greedy k-center: Single pass = 1 "episode"
   - DQN: Configured max_episodes = 1,000
   - Random: Single draw = 1 "episode"
3. Record $t_{end}$ = high-resolution clock time at algorithm end
4. Compute: $\omega = (t_{end} - t_{start}) / \text{episode\_count}$
5. Report to 6 decimal places (e.g., 0.000025 seconds = 25 microseconds for Greedy)

**Collection Method:** Instrumented timing via `time.perf_counter()` in Python

**Expected Values:**
- Greedy k-center: 0.00001–0.00005 s/episode
- DQN (pilot): 0.0226 ± 0.003 s/episode
- Random: 0.000001–0.000005 s/episode

### 5.2 Secondary Metrics

| Metric | Formula | Unit | Collection |
|--------|---------|------|-----------|
| **Load Balance Fairness** | $\sigma(\text{controller loads})$ | std. dev. | Count assignments per controller |
| **Convergence Speed** | Episodes to reach 95% of final reward | episodes | Training loop tracking (DQN only) |
| **Worst-Case Distance** | $\max_{v \in V} \min_{c \in P} d(v,c)$ | hops | Graph search |
| **Average Controller Degree** | $\frac{1}{k} \sum_{c \in P} |N(c)|$ | nodes/controller | Adjacency matrix analysis |
| **Cost-Benefit Ratio** | $\Delta L / \omega$ | ms / (s/episode) | Derived from primary metrics |

### 5.3 Data Recording & Storage

#### 5.3.1 CSV Format (Primary Experimental Data)

```csv
algorithm,topology,num_nodes,controller_budget,seed,latency_ms,reliability_ravg,complexity_s_per_episode,load_balance_std,convergence_episodes_dqn_only,placement_nodes,timestamp_utc,trial_id
Greedy,Internet2,11,3,42,2.937887944947775,1.0,0.000023454,0.45,NA,"0;8;6",2026-04-28T10:15:32.123Z,1
DQN,Internet2,11,3,42,2.937887944947775,1.0,0.022634521,0.38,487,"0;3;6",2026-04-28T11:42:18.456Z,2
Random,Internet2,11,3,42,4.521903456789012,0.92,0.000001234,0.78,NA,"2;7;9",2026-04-28T11:42:19.012Z,3
...
```

#### 5.3.2 Directory Structure

```
results/
├── experiment_data/
│   ├── greedy_internet2.csv          (360 rows per topology)
│   ├── dqn_internet2.csv
│   ├── random_internet2.csv
│   ├── baseline_internet2.csv
│   ├── greedy_attmpls.csv
│   ├── ... [etc. for all topologies]
│   └── experiment_master.csv          (consolidated, 10,800 rows)
├── graphs/
│   ├── pareto_front_internet2_k3.png  (3D scatter plot)
│   ├── convergence_dqn_internet2.png  (training curve)
│   ├── latency_distribution_boxplot.png
│   └── complexity_comparison_barplot.png
└── analysis/
    ├── summary_statistics.csv
    ├── pareto_analysis.json
    ├── stability_matrix.csv
    └── statistical_tests.txt
```

---

## 6. Research Timeline

### 6.1 Phase-by-Phase Schedule

| Phase | Period | Duration | Key Milestones | Status |
|-------|--------|----------|----------------|--------|
| **P1** | Feb 17–Mar 07 | 3 weeks | Pilot DQN, baseline validation | ✅ COMPLETE |
| **P2** | Mar 08–Apr 13 | 5 weeks | Proposal finalization, ethics | ✅ COMPLETE |
| **P3** | Apr 14–May 08 | 4 weeks | **Full factorial execution** (main data collection) | 🟡 ACTIVE |
| **P4** | May 09–Jun 14 | 5 weeks | Data analysis, Pareto inference | 📅 PENDING |
| **P5** | Jun 15–Jul 18 | 4 weeks | Result synthesis, figure generation | 📅 PENDING |
| **P6** | Jul 19–Aug 15 | 4 weeks | Draft thesis chapter, literature integration | 📅 PENDING |
| **P7** | Aug 16–Sep 15 | 4 weeks | Internal review, methodology refinement | 📅 PENDING |
| **P8** | Sep 16–Oct 27 | 6 weeks | Prototype demonstration, final presentation prep | 📅 PENDING |
| **P9** | Oct 28–Nov 13 | 3 weeks | Submission, archival, dissemination | 📅 PENDING |

### 6.2 Phase 3 Detailed Timeline (Current)

**Phase 3: Full Factorial Execution** (April 28 – May 8, 2026)

```
Week 1 (Apr 28 – May 04):
├─ Mon Apr 28: Seed 42 (primary) - Segments 1-6
│  └─ Greedy & DQN trials, intensive telemetry
│     Expected time: 14 hours (thermal-managed)
├─ Tue Apr 29: Seed 42 - Segments 7-12
│  └─ Random & Baseline variants
│     Expected time: 4 hours
├─ Wed Apr 30: Seed 42 - Segments 13-18
│  └─ Sensitivity + edge cases
│     Expected time: varies (2-4 hours)
├─ Thu May 01: Data validation & QA (Seed 42 complete)
│  └─ Row count check, outlier flagging, schema validation
│     Expected time: 2 hours
└─ Fri May 04: Buffer day (thermal recovery, contingency)

Week 2 (May 05 – May 08):
├─ Seed 142-2942 dispatch (parallel background jobs)
│  └─ 3-5 seeds per day, asynchronous execution
│     Total calendar time: 10 days (overlapped with P4 start)
├─ Daily heartbeat checks (memory, disk, crash status)
└─ Weekly data consolidation (each Friday)
```

### 6.3 Gantt Chart (Full Project Timeline)

```
Timeline: Feb 17, 2026 – Nov 13, 2026 (40 weeks)

P1: Pilot Validation             [████████████████] ✅ Feb 17 – Mar 07 (3w)
P2: Proposal & Ethics             [████████████████████████] ✅ Mar 08 – Apr 13 (5w)
P3: Factorial Execution                    [████████████████] 🟡 Apr 14 – May 08 (4w)
P4: Data Analysis & Inference                  [████████████████████] 📅 May 09 – Jun 14 (5w)
P5: Synthesis & Visualization                       [████████████████] 📅 Jun 15 – Jul 18 (4w)
P6: Thesis Draft Writing                              [████████████████] 📅 Jul 19 – Aug 15 (4w)
P7: Internal Review & Refinement                          [████████████████████] 📅 Aug 16 – Sep 15 (4w)
P8: Prototype Demo & Presentation Prep                       [██████████████████████████] 📅 Sep 16 – Oct 27 (6w)
P9: Final Submission & Archival                                  [██████████] 📅 Oct 28 – Nov 13 (3w)

Legend: ✅ = Complete | 🟡 = In Progress | 📅 = Planned | [████] = Duration
```

---

## 7. Statistical and Analytical Procedures

### 7.1 Descriptive Analysis

**Primary Statistics (per algorithm-topology-k cell):**

```python
For each of the 72 experimental cells:
  • Mean latency ± 95% CI (t-distribution, n=150)
  • Median, Q1, Q3 of latency distribution
  • Mean reliability ± 95% CI
  • Mean complexity ± 95% CI
  • Effect size (Cohen's d vs. Greedy baseline)
```

**Visualization:**
- Box plots: Latency distribution per algorithm (6 panels, one per topology)
- Violin plots: Reliability distribution across k values
- Bar plots: Complexity comparison with error bars

### 7.2 Inferential Analysis

#### 7.2.1 Multi-Way ANOVA

**Null Hypothesis:** Algorithm, Topology, Controller Budget, and Scale have no main effects or interactions on latency.

**Test:**
```
latency ~ algorithm + topology + controller_budget + scale 
          + algorithm:topology + algorithm:controller_budget + ...
```

**Expected Outcome:** Reject H₀ if p < 0.05 (likely, given pilot evidence)

**Post-hoc:** Tukey HSD pairwise comparisons (α = 0.05)

#### 7.2.2 Pareto Dominance Analysis

**For each [topology, k] cell:**

1. Extract all algorithm placements with metrics $(L, R, \omega)$
2. Identify non-dominated set:
   ```
   Algorithm X is Pareto-optimal if:
   ∀ other algorithms Y: NOT (L_Y ≤ L_X AND R_Y ≥ R_X AND ω_Y ≤ ω_X)
   ```
3. Count non-dominated solutions per algorithm (should be ≈1–3 typically)
4. Calculate **hypervolume** of Pareto frontier (3D volume dominated by algorithms)

**Result:** Decision table showing which algorithms are Pareto-optimal per scenario

#### 7.2.3 Cross-Scenario Stability (Spearman Rank Correlation)

**Hypothesis:** Algorithm rankings are stable across scenarios.

**Test:**
- Rank algorithms by latency in scenario 1 (Internet2, k=3)
- Rank algorithms by latency in scenario 2 (ATT-MPLS, k=5)
- Compute Spearman ρ between rank vectors
- Expected: ρ > 0.7 indicates stable rankings

**Decision:** If ρ < 0.6 for >20% of scenario pairs → Rankings are scenario-dependent

### 7.3 Quality Metrics

| Metric | Target | Method |
|--------|--------|--------|
| **Data Completeness** | ≥99.5% | (rows written / rows expected) × 100% |
| **Outlier Rate** | <5% | Interquartile range × 1.5 rule |
| **Measurement Precision** | 4 decimals | Reporting granularity (0.0001 ms) |
| **Reproducibility** | ≥95% | Seed 42 rerun ± 0.1% metric variance |
| **Temporal Consistency** | <10% CV | Coefficient of variation across segments |

---

## 8. Data Quality and Validation

### 8.1 Pre-Execution QA

| Check | Method | Pass Criterion |
|-------|--------|---|
| Dependencies installed | Import test | All modules load without error |
| Topologies valid | Connectivity test | All graphs connected |
| Baseline algorithm works | Pilot run | Greedy produces consistent output |
| Random seeds distinct | Seed uniqueness | 30 seeds span [42, 2942] uniformly |
| Output paths writable | File write test | CSV creation successful |

### 8.2 During-Execution QA

```
For each completed segment:
├─ Row count validation: expect ≥90 rows per segment
├─ Schema validation: all columns present, correct types
├─ Value range check:
│  ├─ latency_ms ∈ [0.5, 15.0]
│  ├─ reliability_ravg ∈ [0.0, 1.0]
│  ├─ complexity_s ∈ [10⁻⁶, 10]
├─ Outlier detection: |value - mean| > 3σ → flag for review
├─ Timestamp monotonicity: each row timestamp > previous row
└─ Seed consistency: all rows in segment match expected seed
```

### 8.3 Post-Execution QA

```
1. Master CSV Validation
   ├─ Total rows: 10,800 ± 5% (allow small contingency)
   ├─ All factor combinations present (72 cells × 150 samples)
   ├─ No duplicates (check on [algorithm, topology, seed, trial_id])
   └─ Correlation with pilot: Mean seed 42 ≤ 5% deviation from pilot

2. Distribution Sanity Checks
   ├─ Latency: Normal-ish, no bimodality (suggests no data split issues)
   ├─ Reliability: Clustered near 1.0 (most placements are resilient)
   ├─ Complexity: Log-normal expected (DQN slow, Greedy fast)
   └─ Algorithm ranking: Consistent with literature (Greedy ≤ Random)

3. Reproducibility Test
   ├─ Re-run 5% subsample (Seed 42, 5 topologies, 1 trial each)
   ├─ Compare metrics: ≤0.1% absolute deviation
   ├─ Pass if ≥95% of rerun metrics within tolerance
   └─ Record: reproducibility_score (% passed)
```

---

## 9. Ethical Considerations & Compliance

### 9.1 Exemptions from Full Ethics Review

✅ **This study is exempt from full ethics approval** because:
- No human subjects involved
- No animal research
- No proprietary data used (all topologies are publicly sourced)
- No potential for harm (computer simulation only)

### 9.2 Research Integrity Commitments

1. **Reproducibility:** All code, config, and data will be deposited in version-controlled GitHub repository with full audit trail.
2. **Open Access:** Results will be published in open-access venues where feasible.
3. **Conflict of Interest:** None (single researcher, no commercial interests).
4. **Data Retention:** Artifacts retained ≥5 years per institutional policy.

### 9.3 IP Stewardship

- **University of Zululand** retains ownership of research outputs
- **Code & artifacts:** Licensed under MIT or Apache 2.0 for reproducibility
- **Data:** Published anonymized summary statistics; raw runtime logs available upon request

---

## 10. Dissemination & Output Plan

### 10.1 Primary Deliverables

| Deliverable | Format | Timeline | Audience |
|-------------|--------|----------|----------|
| **Thesis Manuscript** | 60–80 page PDF | Nov 13, 2026 | UNIZULU Faculty, Defense Panel |
| **Research Paper** | 8–12 page conference paper | Dec 2026 | Peer review (SATNAC/SAICSIT) |
| **GitHub Repository** | Version-controlled source + data | Ongoing | Researchers, practitioners |
| **Pareto Frontier Plots** | Publication-quality PNGs | Jun 2026 | Thesis figures, papers |
| **Decision Support Matrix** | CSV table (algorithm → scenario mapping) | Jun 2026 | Infrastructure planners |

### 10.2 Figure Specifications

| Figure | Type | Caption | Location |
|--------|------|---------|----------|
| **Figure 1** | 3D Scatter | Pareto frontier (latency vs. reliability vs. complexity) for Internet2, k=3 | Thesis §5, Paper §4 |
| **Figure 2** | Box Plot | Latency distribution per algorithm (6 subplots, one per topology) | Thesis §5.1 |
| **Figure 3** | Heatmap | Algorithm rank stability across [topology, k] cells | Thesis §5.2 |
| **Figure 4** | Line Plot | DQN convergence trajectory (reward per episode) | Thesis §5.3 (Appendix) |
| **Figure 5** | Bar Plot | Complexity comparison ($\omega$ in log scale) | Thesis §5.4 |

---

## 11. References

- Heller, B., Sherwood, R., & McKeown, N. (2012). The Controller Placement Problem. *Proceedings of HotSDN 2012*, pp. 7–12.
- Farahi, I., et al. (2026). AP-DQN: A novel approach for controller placement in software-defined networks using deep reinforcement learning. *Results in Engineering*, 29, 109631.
- Benoudifa, M., Siad, L., & Belmokaddem, M. (2023). Autonomous solution for controller placement problem of SDN using MuZero. *Journal of King Saud University – Computer and Information Sciences*, 35(10), 101842.
- Radam, N.S., et al. (2022). Multi-Controllers Placement Optimization in SDN by HSA-PSO. *Computers*, 11(8), 111.

---

## 12. Visual Flowcharts & Process Diagrams

### 12.1 Complete Experimental Workflow

The following diagram illustrates the full factorial design execution from initialization through analysis:

```
Phases 1-4 Complete Workflow:
├─ Phase 1 (Setup): Environment initialization, dependency validation
├─ Phase 2 (Execution): Nested loops [Seeds → Topologies → Budgets → Algorithms]
│  └─ Per-trial: Algorithm execution → Measurement (L, R, ω) → CSV recording
├─ Phase 3 (Cooldown): Thermal management between segments
└─ Phase 4 (Analysis): Aggregation, statistics, Pareto inference, visualization
```

**Key Loop Structure:**
- **Outermost loop:** 30 Random Seeds (s = 42, 142, ..., 2942)
- **Topology loop:** 3 Topologies (Internet2, ATT-MPLS, Synthetic-BA)
- **Budget loop:** 3 Controller budgets (k = 2, 3, 5)
- **Algorithm loop:** 4 Algorithms (Greedy, DQN, Random, Baseline)
- **Trial repetition:** 5 trials per [Algorithm, Topology, Budget, Seed] combination
- **Total datapoints:** 30 × 3 × 3 × 4 × 5 = **10,800 observations**

### 12.2 Per-Trial Measurement Protocol

For each trial [Algorithm, Topology, k, Seed], the following measurements are executed in sequence:

```
Step 1: Algorithm Execution
  └─ Output: Placement P (set of k controller nodes)

Step 2: Latency Measurement L(P)
  ├─ Compute all-pairs shortest paths
  ├─ Find min distance per node to nearest controller
  └─ L(P) = mean distance (milliseconds)

Step 3: Reliability Measurement R_avg(P)
  ├─ FOR each link e in edge set E:
  │   └─ Temporarily remove e, check node reachability
  ├─ Count reachable links as fraction
  └─ R_avg(P) ∈ [0.0, 1.0] (control-plane survivability)

Step 4: Complexity Measurement ω
  ├─ Record wall-clock time (start and end)
  ├─ ω = (t_end - t_start) / episode_count
  └─ Report in seconds (10⁻⁶ to 10)

Step 5: Record to CSV
  └─ algorithm, topology, k, seed, latency_ms, reliability_ravg,
     complexity_s, load_std, convergence_episodes, timestamp_utc
```

### 12.3 Phase 4 Analysis Pipeline

Post-experiment statistical analysis follows a structured 4-step process:

```
Step 1: Data Aggregation
  └─ Consolidate 10,800 observations into experiment_master.csv

Step 2: Descriptive Analysis
  ├─ Per-cell statistics: Mean ± 95% CI, median, Q1, Q3
  ├─ Visualizations: Box plots, violin plots, bar charts

Step 3: Inferential Analysis
  ├─ Multi-way ANOVA (algorithm + topology + budget + scale + interactions)
  ├─ Pareto front identification (3D: latency, reliability, complexity)
  ├─ Cross-scenario stability (Spearman rank correlation ρ)
  └─ Effect size & statistical power assessment

Step 4: Synthesis & Interpretation
  ├─ Cost-benefit analysis (AI gain / computational cost)
  ├─ Decision threshold derivation
  ├─ Recommendation matrix (Scenario → Best Algorithm)
  └─ Thesis integration (Chapter 5)
```

---

## 13. Appendices

### Appendix A: Reproducibility Checklist

```
[ ] Environment Setup
  [ ] Python 3.10+ installed
  [ ] PyTorch, NetworkX, Mininet installed
  [ ] Ryu SDN controller installed
  [ ] Git repository cloned
  
[ ] Configuration
  [ ] experiment_config.json reviewed
  [ ] Random seed set to 42 (or documented otherwise)
  [ ] Output directories created
  
[ ] Execution
  [ ] Baseline algorithm test run completed
  [ ] DQN pilot run completed (≥50 episodes)
  [ ] No errors in logs
  
[ ] Validation
  [ ] CSV files generated with expected schema
  [ ] Row counts match factorial design
  [ ] Metrics within expected ranges
  
[ ] Documentation
  [ ] All parameters documented in config
  [ ] Execution logs saved
  [ ] README.md updated with instructions
```

### Appendix B: Experimental Configuration (experiment_config.json)

[See Section 2.1 and embedded configuration above]

### Appendix C: Nested Loop Pseudocode

```python
# Complete Factorial Execution Pseudocode
for seed in [42, 142, 242, ..., 2942]:                   # 30 seeds
    topology_seed = (seed, "topology")                   # Deterministic
    
    for topology in ["Internet2", "ATT-MPLS", "Synthetic-BA"]:  # 3 topologies
        G = load_topology(topology, seed=topology_seed)
        
        for k in [2, 3, 5]:                              # 3 budgets
            
            for algorithm in ["Greedy", "DQN", "Random", "Baseline"]:  # 4 algorithms
                
                for trial in range(5):                   # 5 trials per cell
                    
                    # Execute algorithm
                    t_start = perf_counter()
                    P = algorithm.run(G, k)              # Placement result
                    t_end = perf_counter()
                    
                    # Measure metrics
                    L = compute_latency(G, P)            # Milliseconds
                    R = compute_reliability(G, P)        # [0, 1]
                    ω = (t_end - t_start) / episodes     # Seconds
                    
                    # Record
                    csv_writer.writerow({
                        'algorithm': algorithm,
                        'topology': topology,
                        'k': k,
                        'seed': seed,
                        'latency_ms': L,
                        'reliability_ravg': R,
                        'complexity_s': ω,
                        ...
                    })
                
                # Check: More trials? If yes, continue loop
            # Check: More algorithms? If yes, continue loop
        
        # THERMAL COOLDOWN: 60-300 seconds
        sleep(cooldown_duration)
        
        # Check: More topologies? If yes, continue loop
    # Check: More seeds? If yes, continue loop

# PHASE 2: Aggregation
experiment_master_df = pd.concat(all_csv_files)

# PHASE 3: Analysis
perform_descriptive_stats(experiment_master_df)
perform_anova(experiment_master_df)
identify_pareto_fronts(experiment_master_df)
compute_rank_stability(experiment_master_df)
```

---

**Document Version:** 1.1  
**Last Updated:** April 28, 2026  
**Visual Diagrams Added:** Phase 1-4 Flowcharts  
**Next Review:** Upon completion of Phase 3 (May 8, 2026)

