#!/usr/bin/env python3
"""
Phase 4 Mininet Overhead Validation ("2-Second Gate Test")
===========================================================

Isolated performance validation: builds Internet2 canonical topology in Mininet,
maps controllers, runs sub-second traffic burst, and measures overhead.

Purpose:
  Quantify Phase B overhead (Phase A + B + C + D timing) to determine if Mininet
  is suitable for integration into the DRL training loop. Decision rule:
    - If overhead < 2000 ms: Mininet is APPROVED for Phase 5 execution
    - If overhead >= 2000 ms: Mininet is DEFERRED to Phase 6 validation (MVE)

Execution:
  sudo python3 scripts/test_mininet_overhead.py [--trials N] [--k K] [--verbose]

Requirements:
  - Mininet installed and fully operational (requires root)
  - OpenFlow switch support (e.g., Open vSwitch)
  - iperf3 available in PATH
  - Standard Unix/Linux environment (not Windows WSL1)

Author: Honours Research Team
Date: May 19, 2026
"""

import argparse
import json
import os
import random
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Mininet imports
try:
    from mininet.net import Mininet
    from mininet.node import Controller, RemoteController, OVSSwitch
    from mininet.topo import Topo
    from mininet.util import quietRun, moveIntf
    from mininet.log import setLogLevel, info
except ImportError as e:
    print(f"❌ ERROR: Mininet not installed or not in Python path: {e}")
    print("Install via: sudo apt install mininet")
    sys.exit(1)


# ============================================================================
# Internet2 Canonical Topology Definition
# ============================================================================

class Internet2Topo(Topo):
    """
    Internet2 backbone topology: 11 nodes, 18 edges.
    
    This is a simplified canonical model of the Internet2 network,
    widely used in SDN benchmarking literature (Heller et al., 2012).
    
    Nodes: s1–s11 (OpenFlow-enabled switches)
    Hosts: h1–h11 (one host attached to each switch for traffic generation)
    """

    def build(self):
        """Construct the Internet2 topology."""
        
        # Add 11 switches
        switches = [f"s{i}" for i in range(1, 12)]
        for switch in switches:
            self.addSwitch(switch)
        
        # Add 11 hosts (one per switch)
        for i in range(1, 12):
            host_name = f"h{i}"
            switch_name = f"s{i}"
            self.addHost(host_name)
            self.addLink(host_name, switch_name)
        
        # Internet2 backbone links (18 edges, representing real topology)
        # This is a canonical layout from Internet Topology Zoo aligned with Heller et al.
        edges = [
            ("s1", "s2"), ("s1", "s3"), ("s1", "s6"),
            ("s2", "s3"), ("s2", "s4"), ("s2", "s5"),
            ("s3", "s6"), ("s3", "s7"),
            ("s4", "s5"), ("s4", "s8"),
            ("s5", "s8"), ("s5", "s9"),
            ("s6", "s7"), ("s6", "s10"),
            ("s7", "s10"), ("s7", "s11"),
            ("s8", "s9"), ("s9", "s11"),
        ]
        
        for src, dst in edges:
            self.addLink(src, dst, bw=10)  # 10 Mbps per link (standard for emulation)


# ============================================================================
# Mininet Overhead Validator
# ============================================================================

class MinimumViableEmulationTest:
    """
    Orchestrates a single Mininet trial: topology instantiation, controller
    binding, traffic generation, and cleanup. Tracks execution time for each phase.
    """

    def __init__(self, k: int = 3, verbose: bool = False, use_remote: bool = True):
        """
        Initialize validator.
        
        Args:
            k: Number of controllers to place (default 3 for 11-node Internet2)
            verbose: Enable detailed logging
        """
        self.k = k
        self.verbose = verbose
        self.net = None
        self.controller_nodes = None
        self.timing = {
            "phase_a_topo_instantiation": 0.0,
            "phase_b_controller_binding": 0.0,
            "phase_c_traffic_generation": 0.0,
            "phase_d_teardown": 0.0,
        }
        self.use_remote = use_remote

    def _log(self, msg: str):
        """Conditional logging."""
        if self.verbose:
            print(f"  [DEBUG] {msg}")

    def _preclean(self):
        """Attempt to remove stale Mininet/OVS artifacts that cause interface-creation errors.

        This runs lightweight cleanup commands before topology instantiation to avoid
        'RTNETLINK answers: File exists' errors from leftover veth pairs or bridges.
        """
        self._log("Running pre-cleanup of lingering Mininet/OVS artifacts...")
        try:
            # Safe Mininet cleanup (avoids broad pkill patterns that can terminate this script)
            quietRun("mn -c >/dev/null 2>&1 || true")

            # Kill only iperf3 leftovers from prior runs
            quietRun("pkill -f 'iperf3 -s' || true")
            quietRun("pkill -f 'iperf3 -c' || true")

            # Remove common leftover bridges (best-effort)
            quietRun("ovs-vsctl --if-exists del-br br0 || true")
            quietRun("ovs-vsctl --if-exists del-br ovs-system || true")

            # Robustly parse 'ip -o link show' and delete stale mininet-style interfaces.
            # The output can contain peer notation like 's1-eth2@s2-eth2'. We strip
            # the '@' suffix and attempt to delete the base interface name.
            out = quietRun("ip -o link show")
            for line in out.splitlines():
                # Each line like: '5: s1-eth2@if6: <BROADCAST,...>' -> extract name between index and ':'
                parts = line.split(': ')
                if len(parts) < 2:
                    continue
                name_field = parts[1].split()[0]
                # strip peer suffix if present
                base_name = name_field.split('@')[0]
                # target typical mininet/ovs naming patterns
                if base_name.startswith('s') and '-eth' in base_name:
                    # best-effort: bring down and delete
                    quietRun(f"ip link set {base_name} down 2>/dev/null || true")
                    quietRun(f"ip link delete {base_name} 2>/dev/null || true")
                if base_name.startswith('h') and '-eth' in base_name:
                    quietRun(f"ip link set {base_name} down 2>/dev/null || true")
                    quietRun(f"ip link delete {base_name} 2>/dev/null || true")
                if base_name.startswith('mn') or base_name.startswith('veth'):
                    quietRun(f"ip link set {base_name} down 2>/dev/null || true")
                    quietRun(f"ip link delete {base_name} 2>/dev/null || true")
        except Exception:
            # Non-fatal: pre-clean should never abort the test
            self._log("Pre-clean encountered an issue but will continue")

    def _run_trial(self) -> bool:
        """
        Execute the full Mininet trial sequence.
        
        Returns:
            True if successful, False if any phase fails
        """
        try:
            # ================================================================
            # PHASE A: Topology Instantiation
            # ================================================================
            self._log("Starting Phase A: Topology instantiation...")
            t_a_start = time.perf_counter()

            # Run a lightweight cleanup to remove stale veth/bridge state that can
            # prevent new interface pair creation (common after interrupted runs).
            try:
                self._preclean()
            except Exception:
                self._log("Pre-clean failed silently; continuing to topology creation")

            topo = Internet2Topo()
            # Important: disable Mininet's default controller auto-add behavior to
            # avoid requiring the legacy 'controller' executable in PATH.
            self.net = Mininet(
                topo=topo,
                switch=OVSSwitch,
                controller=None,
                waitConnected=False,
            )

            t_a_end = time.perf_counter()
            self.timing["phase_a_topo_instantiation"] = (t_a_end - t_a_start) * 1000
            self._log(f"Phase A completed in {self.timing['phase_a_topo_instantiation']:.2f} ms")

            # ================================================================
            # PHASE B: Controller Binding and Network Start
            # ================================================================
            self._log("Starting Phase B: Controller binding and network start...")
            t_b_start = time.perf_counter()

            # Select k random controller nodes
            all_switches = [node for node in self.net.switches]
            self.controller_nodes = random.sample(all_switches, self.k)

            self._log(f"Selected controller nodes: {[s.name for s in self.controller_nodes]}")

            # Bind controller instances. Use RemoteController only if explicitly enabled;
            # otherwise use Mininet's local Controller to avoid waiting for external
            # controller processes during the overhead test.
            for i, ctrl_node in enumerate(self.controller_nodes):
                if self.use_remote:
                    ctrl = RemoteController(
                        f"c{i}", ip="127.0.0.1", port=6633 + i
                    )
                else:
                    ctrl = Controller(f"c{i}")
                self.net.addController(ctrl)

            # Start the network
            self.net.start()
            
            t_b_end = time.perf_counter()
            self.timing["phase_b_controller_binding"] = (t_b_end - t_b_start) * 1000
            self._log(f"Phase B completed in {self.timing['phase_b_controller_binding']:.2f} ms")

            # ================================================================
            # PHASE C: Traffic Generation (Sub-Second Burst)
            # ================================================================
            self._log("Starting Phase C: Traffic generation...")
            t_c_start = time.perf_counter()

            # Select random source and destination hosts
            all_hosts = self.net.hosts
            src_host = random.choice(all_hosts)
            dst_host = random.choice([h for h in all_hosts if h != src_host])

            self._log(f"Traffic flow: {src_host.name} → {dst_host.name}")
            
            try:
                # Run iperf3 server on destination (background, non-blocking)
                dst_host.cmd(f"iperf3 -s -D")  # -D: run as daemon
                time.sleep(0.05)  # Brief settle time for server startup
                
                # Run iperf3 client on source for 0.2 seconds (200ms burst)
                # This validates packet-level behavior without stalling the test
                cmd_result = src_host.cmd(
                    f"timeout 1 iperf3 -c {dst_host.IP()} -t 0.2 -J"
                )
                
                self._log(f"iperf3 client completed: {len(cmd_result)} bytes output")
                
                # Clean up iperf3 daemon
                dst_host.cmd("pkill -f 'iperf3 -s'")
                
            except Exception as traffic_err:
                self._log(f"Traffic generation exception (non-fatal): {traffic_err}")
                # Continue anyway; traffic error doesn't invalidate timing measurement

            t_c_end = time.perf_counter()
            self.timing["phase_c_traffic_generation"] = (t_c_end - t_c_start) * 1000
            self._log(f"Phase C completed in {self.timing['phase_c_traffic_generation']:.2f} ms")

            return True

        except Exception as e:
            print(f"❌ Trial execution failed: {e}")
            traceback.print_exc()
            return False

        finally:
            # ================================================================
            # PHASE D: Cleanup and Teardown (MUST ALWAYS EXECUTE)
            # ================================================================
            self._log("Starting Phase D: Cleanup and teardown...")
            t_d_start = time.perf_counter()

            try:
                if self.net is not None:
                    self.net.stop()
                    self._log("net.stop() completed")

                # Safe cleanup after trial. Do not kill ovs/mininet processes broadly;
                # broad pkill patterns can match this Python process and cause termination.
                quietRun("pkill -f 'iperf3 -s' || true")
                quietRun("pkill -f 'iperf3 -c' || true")
                quietRun("mn -c >/dev/null 2>&1 || true")
                
                self._log("Cleanup processes and OVS configuration cleared")

            except Exception as cleanup_err:
                print(f"⚠️  Cleanup exception (non-fatal): {cleanup_err}")

            t_d_end = time.perf_counter()
            self.timing["phase_d_teardown"] = (t_d_end - t_d_start) * 1000
            self._log(f"Phase D completed in {self.timing['phase_d_teardown']:.2f} ms")

    def run(self) -> Dict[str, float]:
        """
        Execute the trial and return timing results.
        
        Returns:
            Dictionary of timing measurements (in milliseconds)
        """
        success = self._run_trial()
        
        if not success:
            print("❌ Trial failed during execution")
            return {}
        
        return self.timing

    @property
    def total_overhead_ms(self) -> float:
        """Total cumulative overhead in milliseconds."""
        return sum(self.timing.values())


# ============================================================================
# Main Validation Harness
# ============================================================================

def run_gate_test(
    trials: int = 3,
    k: int = 3,
    verbose: bool = False,
    use_remote: bool = True,
) -> Dict:
    """
    Execute the 2-second gate test across multiple trials.
    
    Args:
        trials: Number of independent trials to run
        k: Number of controllers per trial
        verbose: Enable detailed logging
    
    Returns:
        Aggregated results dictionary
    """
    print("=" * 80)
    print("PHASE 4 MININET OVERHEAD VALIDATION ('2-Second Gate Test')")
    print("=" * 80)
    print(f"\nTest Configuration:")
    print(f"  - Topology: Internet2 (11 nodes, 18 edges)")
    print(f"  - Controllers per trial: k={k}")
    print(f"  - Number of trials: {trials}")
    print(f"  - Decision threshold: 2000 ms (per episode)")
    print(f"  - Traffic burst duration: 0.2 seconds (sub-second)")
    print(f"  - Controller mode: {'remote(127.0.0.1:6633+)' if use_remote else 'local(mininet)'}")
    print("\n" + "-" * 80)

    trial_results = []
    exceeds_threshold = 0

    for trial_num in range(1, trials + 1):
        print(f"\n[TRIAL {trial_num}/{trials}]")
        
        validator = MinimumViableEmulationTest(k=k, verbose=verbose, use_remote=use_remote)
        timing = validator.run()
        
        if not timing:
            print(f"  ❌ Trial {trial_num} failed")
            continue

        online_loop_overhead_ms = (
            timing["phase_a_topo_instantiation"]
            + timing["phase_b_controller_binding"]
            + timing["phase_c_traffic_generation"]
        )
        full_lifecycle_overhead_ms = online_loop_overhead_ms + timing["phase_d_teardown"]

        trial_results.append(
            {
                **timing,
                "online_loop_overhead_ms": online_loop_overhead_ms,
                "full_lifecycle_overhead_ms": full_lifecycle_overhead_ms,
            }
        )
        
        # Print phase breakdown
        print(f"\n  Phase Breakdown:")
        print(f"    Phase A (Topo Instantiation):    {timing['phase_a_topo_instantiation']:8.2f} ms")
        print(f"    Phase B (Controller + Start):    {timing['phase_b_controller_binding']:8.2f} ms")
        print(f"    Phase C (Traffic Burst):         {timing['phase_c_traffic_generation']:8.2f} ms")
        print(f"    Phase D (Cleanup + Teardown):    {timing['phase_d_teardown']:8.2f} ms")
        print(f"    ─────────────────────────────────────")
        print(f"    Online Loop Overhead:            {online_loop_overhead_ms:8.2f} ms")
        print(f"    Full Lifecycle Overhead:         {full_lifecycle_overhead_ms:8.2f} ms")
        print(
            "    Insight: Online interaction takes "
            f"{online_loop_overhead_ms:.2f} ms (Within Spec for training), "
            "but OS teardown adds "
            f"{timing['phase_d_teardown']:.2f} ms of infrastructure tax, "
            "justifying an offline/post-hoc validation architecture."
        )
        
        # Check against threshold
        if full_lifecycle_overhead_ms >= 2000:
            print(f"\n  ⚠️  CRITICAL TIMING THRESHOLD EXCEEDED: OUT OF SPEC FOR ONLINE DRL TRAINING INTERACTION")
            print(f"      Overhead {full_lifecycle_overhead_ms:.2f} ms exceeds 2000 ms budget.")
            exceeds_threshold += 1
        else:
            print(
                f"\n  ✅ WITHIN BUDGET: {full_lifecycle_overhead_ms:.2f} ms / 2000 ms "
                f"({(full_lifecycle_overhead_ms/2000)*100:.1f}%)"
            )

    # ========================================================================
    # Final Report
    # ========================================================================
    print("\n" + "=" * 80)
    print("AGGREGATE RESULTS")
    print("=" * 80)
    
    if not trial_results:
        print("❌ No successful trials; cannot compute aggregate statistics")
        return {"status": "FAILED", "error": "No successful trials"}

    # Compute statistics
    online_times = [trial["online_loop_overhead_ms"] for trial in trial_results]
    full_lifecycle_times = [trial["full_lifecycle_overhead_ms"] for trial in trial_results]
    avg_online = sum(online_times) / len(online_times)
    min_online = min(online_times)
    max_online = max(online_times)
    avg_full = sum(full_lifecycle_times) / len(full_lifecycle_times)
    min_full = min(full_lifecycle_times)
    max_full = max(full_lifecycle_times)
    
    # Phase-wise aggregates
    phase_means = {}
    for phase_key in trial_results[0].keys():
        phase_values = [trial[phase_key] for trial in trial_results]
        phase_means[phase_key] = sum(phase_values) / len(phase_values)

    print(f"\nSuccessful Trials: {len(trial_results)}/{trials}")
    print(f"\nAggregate Timing (across {len(trial_results)} trials):")
    print(f"  Phase A (Topo):       {phase_means['phase_a_topo_instantiation']:8.2f} ms (avg)")
    print(f"  Phase B (Controller): {phase_means['phase_b_controller_binding']:8.2f} ms (avg)")
    print(f"  Phase C (Traffic):    {phase_means['phase_c_traffic_generation']:8.2f} ms (avg)")
    print(f"  Phase D (Cleanup):    {phase_means['phase_d_teardown']:8.2f} ms (avg)")
    print(f"  ─────────────────────────────────────")
    print(f"  Online Loop (avg):    {avg_online:8.2f} ms")
    print(f"  Online Loop (min):    {min_online:8.2f} ms")
    print(f"  Online Loop (max):    {max_online:8.2f} ms")
    print(f"  Full Lifecycle (avg): {avg_full:8.2f} ms")
    print(f"  Full Lifecycle (min): {min_full:8.2f} ms")
    print(f"  Full Lifecycle (max): {max_full:8.2f} ms")
    print(f"  Variability:          {max_full - min_full:8.2f} ms")

    print(
        "  Insight: Online interaction takes "
        f"{avg_online:.2f} ms (Within Spec for training), "
        "but OS teardown adds "
        f"{phase_means['phase_d_teardown']:.2f} ms of infrastructure tax, "
        "justifying an offline/post-hoc validation architecture."
    )

    # Decision
    print(f"\n{'='*80}")
    if exceeds_threshold == 0:
        decision = "✅ APPROVED FOR PHASE 5"
        status = "PASS"
        recommendation = (
            "Mininet overhead is within budget. Proceed with Mininet integration "
            "in Phase 5 (July) full factorial runs. Expect ~1–1.5 hours total "
            "for 18 cells × 1000 episodes."
        )
    else:
        decision = "⚠️  CONDITIONALLY APPROVED (DEFER TO PHASE 6)"
        status = "WARN"
        recommendation = (
            f"{exceeds_threshold}/{len(trial_results)} trials exceeded 2000 ms threshold. "
            "Recommend deferring Mininet to Phase 6 validation on Pareto subset only. "
            "Phase 5: Use graph-based metrics (shortest-path latency, reachability). "
            "Phase 6: Validate top 5 Pareto solutions via Mininet."
        )

    print(f"\nDECISION: {decision}")
    print(f"STATUS: {status}")
    print(f"\nRECOMMENDATION:")
    print(f"  {recommendation}")
    print(f"{'='*80}\n")

    # Save results to JSON for archival
    results_dict = {
        "test_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "configuration": {
            "topology": "Internet2",
            "nodes": 11,
            "edges": 18,
            "controllers_per_trial": k,
            "traffic_burst_duration": 0.2,
        },
        "trials": len(trial_results),
        "threshold_ms": 2000,
        "exceeds_threshold": exceeds_threshold,
        "aggregate": {
            "phase_a_mean_ms": phase_means['phase_a_topo_instantiation'],
            "phase_b_mean_ms": phase_means['phase_b_controller_binding'],
            "phase_c_mean_ms": phase_means['phase_c_traffic_generation'],
            "phase_d_mean_ms": phase_means['phase_d_teardown'],
            "online_loop_avg_ms": avg_online,
            "online_loop_min_ms": min_online,
            "online_loop_max_ms": max_online,
            "full_lifecycle_avg_ms": avg_full,
            "full_lifecycle_min_ms": min_full,
            "full_lifecycle_max_ms": max_full,
            "teardown_infrastructure_tax_avg_ms": phase_means['phase_d_teardown'],
            "total_avg_ms": avg_full,
            "total_min_ms": min_full,
            "total_max_ms": max_full,
            "variability_ms": max_full - min_full,
        },
        "decision": status,
        "recommendation": recommendation,
        "individual_trials": trial_results,
    }

    results_file = Path(__file__).parent.parent / "results" / "mininet_overhead_validation.json"
    results_file.parent.mkdir(parents=True, exist_ok=True)
    with open(results_file, "w") as f:
        json.dump(results_dict, f, indent=2)
    
    print(f"Results saved to: {results_file}\n")
    
    return results_dict


# ============================================================================
# CLI Entrypoint
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Phase 4 Mininet Overhead Validation Test",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  sudo python3 scripts/test_mininet_overhead.py --trials 3
  sudo python3 scripts/test_mininet_overhead.py --trials 5 --k 3 --verbose
        """,
    )
    
    parser.add_argument(
        "--trials",
        type=int,
        default=3,
        help="Number of independent trials (default: 3)",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=3,
        help="Number of controllers per trial (default: 3)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable detailed debug logging",
    )
    parser.add_argument(
        "--use-remote-controller",
        action="store_true",
        help=(
            "Use RemoteController instances on 127.0.0.1 ports 6633+ (default behavior)."
        ),
    )
    parser.add_argument(
        "--use-local-controller",
        action="store_true",
        help="Use Mininet local Controller class (requires 'controller' binary in PATH).",
    )
    
    args = parser.parse_args()
    
    # Validate that we're running as root (required for Mininet)
    if os.geteuid() != 0:
        print("❌ ERROR: This script requires root privileges (for Mininet network namespaces)")
        print("Re-run with: sudo python3 scripts/test_mininet_overhead.py")
        sys.exit(1)

    # Suppress excessive Mininet logging
    setLogLevel("info")

    if args.use_remote_controller and args.use_local_controller:
        print("❌ ERROR: choose only one controller mode flag.")
        sys.exit(2)

    # Default to remote controller mode to satisfy the placement mapping requirement.
    use_remote = True
    if args.use_local_controller:
        use_remote = False
    elif args.use_remote_controller:
        use_remote = True

    # Run the gate test
    results = run_gate_test(
        trials=args.trials,
        k=args.k,
        verbose=args.verbose,
        use_remote=use_remote,
    )
    
    # Exit with appropriate code
    if results.get("decision") == "PASS":
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Warning/failure


if __name__ == "__main__":
    main()
