#!/usr/bin/env python3
"""
Repository Configuration Verification Script
Confirms alignment with Technical Stack Defense (Section 8.4.1, Methodology).

This script verifies that the repository configuration matches the finalized
research proposal hyperparameters and topology references:
  - DQN hyperparameters (Farahi et al. 2026 reference band)
  - Canonical topologies (Internet2 and ATT-MPLS per Heller et al. 2012)
  - Mininet + Iperf3 operationalization for packet-level realism
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict

# Import topology loader
sys.path.insert(0, str(Path(__file__).parent.parent))
from topology.canonical_topologies import load_canonical_topology, list_available_topologies


def load_config(config_path: Path) -> Dict[str, Any]:
    """Load experiment configuration from JSON."""
    with open(config_path, "r") as f:
        return json.load(f)


def verify_rl_hyperparameters(config: Dict[str, Any]) -> bool:
    """Verify that RL hyperparameters match Farahi et al. (2026) reference band."""
    print("\n" + "=" * 70)
    print("RL HYPERPARAMETER VERIFICATION (Farahi et al. 2026)")
    print("=" * 70)
    
    required_params = {
        "learning_rate": 0.001,
        "batch_size": 32,
        "gamma": 0.99,
        "max_episodes": 1000
    }
    
    rl_config = config.get("rl_hyperparameters", {})
    
    all_match = True
    for param, expected_value in required_params.items():
        actual_value = rl_config.get(param)
        status = "✓ MATCH" if actual_value == expected_value else "✗ MISMATCH"
        if actual_value != expected_value:
            all_match = False
        print(f"  {param:20s}: {actual_value:15} (expected: {expected_value}) {status}")
    
    return all_match


def verify_topology_config(config: Dict[str, Any], nx) -> bool:
    """Verify that topology configuration references canonical topologies."""
    print("\n" + "=" * 70)
    print("CANONICAL TOPOLOGY VERIFICATION (Heller et al. 2012)")
    print("=" * 70)
    
    topo_config = config.get("topology_config", {})
    primary_topologies = topo_config.get("primary_topologies", [])
    
    expected = ["Internet2", "ATT-MPLS"]
    all_present = all(topo in primary_topologies for topo in expected)
    status = "✓ CORRECT" if all_present else "✗ MISSING"
    
    print(f"  Primary topologies: {primary_topologies}")
    print(f"  Expected: {expected}")
    print(f"  Status: {status}")
    
    # Attempt to load topologies
    if nx is not None:
        print("\n  Topology Load Test:")
        try:
            for topo_name in expected:
                G = load_canonical_topology(topo_name, seed=42)
                print(f"    {topo_name:15s}: {G.number_of_nodes():3d} nodes, {G.number_of_edges():3d} edges, "
                      f"connected={nx.is_connected(G)}")
        except Exception as e:
            print(f"    ERROR loading topology: {e}")
            return False
    
    return all_present


def verify_simulation_config(config: Dict[str, Any]) -> bool:
    """Verify Mininet + Iperf3 simulation configuration."""
    print("\n" + "=" * 70)
    print("SIMULATION STACK VERIFICATION (Mininet + Iperf3)")
    print("=" * 70)
    
    sim_config = config.get("simulation", {})
    
    checks = {
        "emulator": "mininet",
        "traffic_generator": "iperf3"
    }
    
    all_match = True
    for key, expected in checks.items():
        actual = sim_config.get(key)
        status = "✓ MATCH" if actual == expected else "✗ MISMATCH"
        if actual != expected:
            all_match = False
        print(f"  {key:20s}: {actual:15} (expected: {expected}) {status}")
    
    return all_match


def verify_objective_weights(config: Dict[str, Any]) -> bool:
    """Verify RL objective function weights."""
    print("\n" + "=" * 70)
    print("RL OBJECTIVE FUNCTION VERIFICATION")
    print("=" * 70)
    
    rl_obj = config.get("rl_objective", {})
    
    checks = {
        "latency_weight": 1.0,
        "reliability_weight": 0.25,
        "seconds_per_episode_weight": 0.25
    }
    
    all_match = True
    for key, expected in checks.items():
        actual = rl_obj.get(key)
        status = "✓ MATCH" if actual == expected else "✗ MISMATCH"
        if actual != expected:
            all_match = False
        print(f"  {key:20s}: {actual:15} (expected: {expected}) {status}")
    
    return all_match


def verify_dependencies() -> bool:
    """Verify that required Python packages are installed."""
    print("\n" + "=" * 70)
    print("DEPENDENCY VERIFICATION")
    print("=" * 70)
    
    required_packages = {
        "torch": "Deep RL framework",
        "networkx": "Graph algorithms",
        "numpy": "Numerical computing",
        "matplotlib": "Visualization",
        "pandas": "Data analysis"
    }
    
    all_installed = True
    for package, description in required_packages.items():
        try:
            __import__(package)
            status = "✓ INSTALLED"
        except ImportError:
            status = "✗ MISSING"
            all_installed = False
        print(f"  {package:15s}: {description:30s} {status}")
    
    return all_installed


def main():
    """Run comprehensive verification."""
    print("\n")
    print("=" * 70)
    print("  PROPOSAL COMPLIANCE VERIFICATION")
    print("  Repository Synchronization with Technical Stack Defense")
    print("=" * 70)
    
    # Paths
    config_path = Path(__file__).parent.parent / "configs" / "experiment_config.json"
    
    if not config_path.exists():
        print(f"\n✗ ERROR: Config file not found at {config_path}")
        return False
    
    # Load config
    try:
        config = load_config(config_path)
    except json.JSONDecodeError as e:
        print(f"\n✗ ERROR: Invalid JSON in {config_path}: {e}")
        return False
    
    # Run verifications
    try:
        import networkx as nx  # Import here for topology verification
    except ImportError:
        print("\n⚠ WARNING: networkx not installed; skipping topology tests")
        nx = None
    
    results = {
        "RL Hyperparameters": verify_rl_hyperparameters(config),
        "Canonical Topologies": verify_topology_config(config, nx) if nx else None,
        "Simulation Stack": verify_simulation_config(config),
        "Objective Weights": verify_objective_weights(config),
        "Dependencies": verify_dependencies()
    }
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    for check, passed in results.items():
        if passed is None:
            status = "[SKIPPED]"
        elif passed:
            status = "[PASSED]"
        else:
            status = "[FAILED]"
        print(f"  {check:30s}: {status}")
    
    overall_pass = all(v for v in results.values() if v is not None)
    
    print("\n" + "=" * 70)
    if overall_pass:
        print("[OK] PROPOSAL COMPLIANCE: CONFIRMED")
        print("  Repository is synchronized with Technical Stack Defense (Section 8.4.1)")
        print("  All critical parameters match Farahi et al. (2026) reference band")
    else:
        print("[WARN] PROPOSAL COMPLIANCE: ISSUES DETECTED")
        print("  Review failed items above and update configuration as needed")
    print("=" * 70 + "\n")
    
    return overall_pass


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
