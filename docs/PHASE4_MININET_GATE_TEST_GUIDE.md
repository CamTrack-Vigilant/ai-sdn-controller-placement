# Phase 4 Mininet Overhead Test: Execution Guide

**Document Date:** May 19, 2026  
**Purpose:** Execute the "2-Second Gate Test" to validate Mininet integration feasibility for Phase 5 DRL training

---

## Overview

The `test_mininet_overhead.py` script performs an isolated, microsecond-instrumented validation of Mininet execution overhead. It:

1. **Builds the Internet2 canonical topology** (11 nodes, 18 edges) inside Mininet
2. **Maps k=3 controllers** to random node positions
3. **Generates a sub-second traffic burst** (0.2 second iperf3 flow) to simulate active network state
4. **Tracks 4 execution phases** with millisecond precision:
   - **Phase A**: Topology instantiation (network object creation)
   - **Phase B**: Controller binding + `net.start()` (switch and controller initialization)
   - **Phase C**: Traffic generation (iperf3 burst)
   - **Phase D**: Cleanup and teardown (environment reset)
5. **Compares total overhead to a 2000 ms budget** and produces a PASS/WARN decision

---

## Decision Rule

| Total Overhead | Decision | Recommendation |
|---|---|---|
| < 2000 ms | ✅ **APPROVED** | Use Mininet in Phase 5 full factorial runs |
| ≥ 2000 ms | ⚠️ **DEFERRED** | Defer Mininet to Phase 6 validation on Pareto subset only |

---

## Prerequisites

### System Requirements
- **Linux** (Ubuntu 20.04+ or equivalent; NOT Windows WSL1)
- **Root privileges** (required for Mininet namespace and OVS management)
- **Mininet** installed: `sudo apt install mininet`
- **OpenFlow switch support**: `sudo apt install openvswitch-switch`
- **iperf3**: `sudo apt install iperf3`

### Software Stack
```bash
# Verify Mininet installation
sudo python3 -c "from mininet.net import Mininet; print('✓ Mininet OK')"

# Verify OVS
sudo ovs-vsctl --version

# Verify iperf3
iperf3 --version
```

---

## Execution Instructions

### Quick Start (Recommended)

```bash
cd /home/pro/Desktop/ai-sdn-controller-placement

# Run 3 trials (default, ~3-5 minutes total)
sudo python3 scripts/test_mininet_overhead.py --trials 3
```

### Extended Validation (5 trials, higher confidence)

```bash
# Run 5 trials with verbose debugging
sudo python3 scripts/test_mininet_overhead.py --trials 5 --verbose
```

### Custom Controller Count

```bash
# Test with k=2 or k=5 controllers
sudo python3 scripts/test_mininet_overhead.py --trials 3 --k 2
```

---

## Expected Output

### Success Case (Overhead < 2000 ms)

```
================================================================================
PHASE 4 MININET OVERHEAD VALIDATION ('2-Second Gate Test')
================================================================================

Test Configuration:
  - Topology: Internet2 (11 nodes, 18 edges)
  - Controllers per trial: k=3
  - Number of trials: 3
  - Decision threshold: 2000 ms (per episode)
  - Traffic burst duration: 0.2 seconds (sub-second)

--------------------------------------------------------------------------------

[TRIAL 1/3]

  Phase Breakdown:
    Phase A (Topo Instantiation):     248.34 ms
    Phase B (Controller + Start):     156.78 ms
    Phase C (Traffic Burst):          201.45 ms
    Phase D (Cleanup + Teardown):     187.92 ms
    ─────────────────────────────────────
    TOTAL OVERHEAD:                   794.49 ms

  ✅ WITHIN BUDGET: 794.49 ms / 2000 ms (39.7%)

[TRIAL 2/3]
  ... (similar format)

================================================================================
AGGREGATE RESULTS
================================================================================

Successful Trials: 3/3

Aggregate Timing (across 3 trials):
  Phase A (Topo):       245.12 ms (avg)
  Phase B (Controller): 158.34 ms (avg)
  Phase C (Traffic):    203.67 ms (avg)
  Phase D (Cleanup):    189.45 ms (avg)
  ─────────────────────────────────────
  Total (avg):          796.58 ms
  Total (min):          794.49 ms
  Total (max):          798.73 ms
  Variability:            4.24 ms

================================================================================

DECISION: ✅ APPROVED FOR PHASE 5
STATUS: PASS

RECOMMENDATION:
  Mininet overhead is within budget. Proceed with Mininet integration in Phase 5 
  (July) full factorial runs. Expect ~1–1.5 hours total for 18 cells × 1000 episodes.

================================================================================

Results saved to: results/mininet_overhead_validation.json
```

### Warning Case (Overhead ≥ 2000 ms)

```
================================================================================
AGGREGATE RESULTS
================================================================================

...

  Total (avg):          2156.34 ms
  Total (max):          2389.12 ms

================================================================================

DECISION: ⚠️  CONDITIONALLY APPROVED (DEFER TO PHASE 6)
STATUS: WARN

RECOMMENDATION:
  2/3 trials exceeded 2000 ms threshold. Recommend deferring Mininet to Phase 6 
  validation on Pareto subset only. Phase 5: Use graph-based metrics (shortest-path 
  latency, reachability). Phase 6: Validate top 5 Pareto solutions via Mininet.

================================================================================

Results saved to: results/mininet_overhead_validation.json
```

---

## Interpreting Results

### Phase Breakdown Analysis

**Phase A: Topology Instantiation (Expected: 150–300 ms)**
- Time to create 11 switches + 11 hosts + 18 links in Mininet data structures
- **What varies:** Host system load, OVS daemon availability
- **If > 400 ms:** System overloaded or OVS not responsive; try rebooting

**Phase B: Controller Binding + Start (Expected: 100–200 ms)**
- Time to instantiate RemoteController objects and call `net.start()`
- Includes OpenFlow switch startup and controller connection negotiation
- **What varies:** Number of switches, timeout settings, controller availability
- **If > 300 ms:** Controller negotiation delayed; check if port 6633–6635 is available

**Phase C: Traffic Generation (Expected: 150–300 ms)**
- Time to start iperf3 server on destination host and run 0.2s client burst
- **What varies:** Host process startup overhead, network stack response
- **If > 400 ms:** Host traffic generation slow; network emulation contending with system load

**Phase D: Cleanup (Expected: 100–250 ms)**
- Time to tear down network, kill OVS processes, reset virtual interfaces
- **What varies:** Number of lingering processes, interface cleanup latency
- **If > 400 ms:** Cleanup blocking; may indicate stale processes from previous runs

### Decision Logic

| Finding | Implication | Action |
|---|---|---|
| **Total < 1000 ms** | Very low overhead | ✅ **Highly confident** in Mininet integration. Use in Phase 5 with minimal concern. |
| **1000–1500 ms** | Moderate overhead | ✅ **Confident**. Mininet adds ~1 sec per episode; 18 cells × 1000 episodes ≈ 5 hours (acceptable). |
| **1500–2000 ms** | Approaching threshold | ⚠️ **Marginal**. Mininet usable but tight. Phase 5 full run will take ~6–7 hours. Consider limiting to 500 episodes per cell in Phase 5. |
| **2000–3000 ms** | Over threshold | ⚠️ **Deferred**. Use MVE: graph-based Phase 5, Mininet validation on subset in Phase 6. |
| **> 3000 ms** | Severe overhead | 🔴 **Not recommended**. Mininet unsuitable for online DRL. Use graph-only throughout. |

---

## Phase 4 Decision Gates (Before May 25)

### Gate 1: Mininet PoC Validation (By May 22)

**Check:**
- [ ] Script runs successfully with `sudo python3 scripts/test_mininet_overhead.py --trials 3`
- [ ] All 3 trials complete without exceptions
- [ ] `results/mininet_overhead_validation.json` is generated
- [ ] Total overhead is < 2000 ms (PASS) or marginal (WARN)

**Output:**
```bash
# Check the decision
cat results/mininet_overhead_validation.json | grep '"decision"'
# Expected: "decision": "PASS" or "decision": "WARN"
```

### Gate 2: Phase 5 Readiness Decision (By May 25)

**If PASS:**
- ✅ Confirm Mininet integration in Phase 5 formal defense
- Proceed with Phase 5 planning (Jul 06) assuming Mininet is available

**If WARN:**
- ⚠️ Notify supervisor of conditional approval
- Plan MVE fallback: Phase 5 graph-based, Phase 6 Mininet validation
- Prepare graph-based latency/reliability metric pipeline as primary Phase 5 deliverable

---

## Troubleshooting

### Script Fails: "ModuleNotFoundError: No module named 'mininet'"

```bash
# Mininet not installed
sudo apt update
sudo apt install mininet
sudo python3 -m pip install mininet  # Fallback if apt fails
```

### Script Fails: "This script requires root privileges"

```bash
# Not running with sudo
sudo python3 scripts/test_mininet_overhead.py --trials 3
```

### Trial Hangs or Times Out (> 10 minutes for 3 trials)

```bash
# Kill stuck Mininet processes and reset
sudo pkill -9 mininet
sudo pkill -9 mn-vhost
sudo ovs-vsctl show  # Check for stale bridges
sudo ovs-vsctl del-br ovs-system 2>/dev/null || true  # Force cleanup
sudo systemctl restart openvswitch-switch
```

Then retry the script.

### Trial Succeeds but Variability is Very High (> 500 ms spread)

- **Cause:** System load or CPU throttling
- **Fix:** Close other applications, disable frequency scaling (if safe on test machine)
```bash
sudo cpupower frequency-set -g performance  # Max CPU frequency (requires cpupower-utils)
```

### iperf3 Traffic Generation Fails (but script continues)

```
[DEBUG] Traffic generation exception (non-fatal): ...
```

- This is **OK**. The script logs traffic errors as non-fatal so Mininet overhead is still measured.
- The critical timing (Phases A, B, D) is unaffected.

---

## Recording Results for Proposal Defense

Save this output as evidence for your formal defense (P4, May 18–25):

```bash
# Generate a timestamped summary
sudo python3 scripts/test_mininet_overhead.py --trials 5 | tee ~/mininet_gate_test_$(date +%Y%m%d_%H%M%S).log

# Copy the JSON results to your docs folder
cp results/mininet_overhead_validation.json docs/phase4_gate_test_results.json

# View the decision
python3 -c "import json; d=json.load(open('results/mininet_overhead_validation.json')); print(f\"Decision: {d['decision']}\"); print(f\"Total Avg: {d['aggregate']['total_avg_ms']:.1f} ms\")"
```

---

## Next Steps

### If PASS (Overhead < 2000 ms)
1. ✅ Confirm in formal defense: "Mininet integration approved for Phase 5"
2. **Phase 5 (Jul 06):** Integrate Mininet into the DRL training loop
   - Create a wrapper that instantiates Mininet once, then runs multiple DRL episodes inside the network
   - Measure real-world latency from Mininet traffic (not just graph-based shortest-path)
3. **Phase 6 (Aug):** Report comparative results with graph-based metrics to validate overhead assumptions

### If WARN (Overhead 1500–2000 ms) or DEFERRED (> 2000 ms)
1. ⚠️ Present MVE plan in formal defense:
   - Phase 5: Graph-based optimization (latency via shortest-path, reliability via reachability)
   - Phase 6: Selective Mininet validation on top Pareto solutions
2. **Phase 5 (Jul 06):** Focus on graph-based factorial runs (18 cells × 1000 episodes ≈ 20 minutes)
3. **Phase 6 (Aug):** Run top 5 Pareto placements through Mininet for validation

---

## Document Versions

| Date | Version | Author | Status |
|---|---|---|---|
| May 19, 2026 | 1.0 | Honours Research Team | Initial release |

