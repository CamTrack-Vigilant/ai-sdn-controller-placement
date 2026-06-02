#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import shlex
import socket
import subprocess
import sys
import threading
import time
import shutil
from typing import Any

import networkx as nx

from algorithms.baseline.greedy_placement import greedy_k_center_placement
from evaluation.metrics import average_controller_distance
from evaluation.telemetry import sample_process_telemetry_to_csv
from topology.canonical_topologies import load_canonical_topology


def _project_root() -> Path:
    return Path(__file__).resolve().parent


def _normalize_graph(graph: nx.Graph) -> nx.Graph:
    if graph.is_directed():
        graph = nx.Graph(graph)
    else:
        graph = graph.copy()

    ordered_nodes = sorted(graph.nodes(), key=lambda node: str(node))
    relabel_map = {node: f"n{idx}" for idx, node in enumerate(ordered_nodes)}
    graph = nx.relabel_nodes(graph, relabel_map)

    for u, v, data in graph.edges(data=True):
        try:
            data["weight"] = max(0.1, float(data.get("weight", 1.0)))
        except (TypeError, ValueError):
            data["weight"] = 1.0

    return graph


def _load_internet2_graph(seed: int) -> nx.Graph:
    """Load Internet2 from JSON if present, else canonical loader (GraphML/GML/fallback)."""
    root = _project_root()
    topology_dir = root / "data" / "raw" / "topologies"
    json_candidates = [
        topology_dir / "internet2.json",
        topology_dir / "Internet2.json",
    ]

    for json_path in json_candidates:
        if not json_path.exists():
            continue

        payload = json.loads(json_path.read_text(encoding="utf-8"))
        graph = nx.node_link_graph(payload)
        graph = _normalize_graph(graph)
        graph.graph["name"] = "Internet2"
        graph.graph["source"] = str(json_path)
        return graph

    return load_canonical_topology("Internet2", seed=seed)


def _wait_for_port(host: str, port: int, timeout_s: float) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            if sock.connect_ex((host, port)) == 0:
                return True
        time.sleep(0.2)
    return False


def _run_mininet_cleanup() -> None:
    cleanup = subprocess.run(
        ["sudo", "mn", "-c"],
        capture_output=True,
        text=True,
        check=False,
    )
    if cleanup.returncode != 0:
        print("[WARN] Mininet cleanup failed. Run manually: sudo mn -c", file=sys.stderr)
        if cleanup.stderr:
            print(cleanup.stderr.strip(), file=sys.stderr)


def _resolve_controller_cmd(controller_cmd: str, root: Path) -> list[str]:
    parts = shlex.split(controller_cmd)
    if not parts:
        raise ValueError("Controller command is empty")

    executable = parts[0]
    if shutil.which(executable):
        return parts

    fallback_candidates = [
        root / "venv310" / "bin" / executable,
        root / "venv" / "bin" / executable,
    ]
    for candidate in fallback_candidates:
        if candidate.exists() and candidate.is_file():
            parts[0] = str(candidate)
            return parts

    return parts


def _build_topology(graph: nx.Graph, controller_nodes: list[str]):
    from mininet.link import TCLink
    from mininet.topo import Topo

    node_labels = [str(node) for node in graph.nodes]
    node_to_idx = {node: idx for idx, node in enumerate(node_labels, start=1)}

    class Internet2PlacementTopo(Topo):
        def build(self) -> None:
            for node in node_labels:
                idx = node_to_idx[node]
                switch_name = f"s{idx}"
                host_name = f"h{idx}"
                self.addSwitch(switch_name)
                self.addHost(host_name)
                self.addLink(host_name, switch_name, cls=TCLink, delay="0.10ms")

                if node in controller_nodes:
                    ctrl_host = f"ctrl{idx}"
                    self.addHost(ctrl_host)
                    self.addLink(ctrl_host, switch_name, cls=TCLink, delay="0.10ms")

            for u, v, data in graph.edges(data=True):
                delay_ms = max(0.1, float(data.get("weight", 1.0)))
                self.addLink(
                    f"s{node_to_idx[str(u)]}",
                    f"s{node_to_idx[str(v)]}",
                    cls=TCLink,
                    delay=f"{delay_ms:.2f}ms",
                )

    return Internet2PlacementTopo


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Execute baseline Internet2 factorial cell: greedy k-center placement, "
            "Mininet run, and Ryu PID telemetry."
        )
    )
    parser.add_argument("--k", type=int, default=3, help="Controller budget (default: 3)")
    parser.add_argument(
        "--topology",
        type=str,
        default="internet2",
        choices=["internet2"],
        help="Topology selector (currently supports: internet2).",
    )
    parser.add_argument("--seed", type=int, default=42, help="Deterministic seed (default: 42)")
    parser.add_argument("--controller-port", type=int, default=6653)
    parser.add_argument("--controller-ready-timeout", type=float, default=20.0)
    parser.add_argument("--telemetry-interval", type=float, default=0.5)
    parser.add_argument(
        "--telemetry-output",
        type=str,
        default="results/experiment_data/baseline_telemetry_internet2.csv",
    )
    parser.add_argument(
        "--summary-output",
        type=str,
        default="results/experiment_data/baseline_internet2_summary.csv",
    )
    parser.add_argument(
        "--controller-cmd",
        type=str,
        default="ryu-manager ryu.app.simple_switch_13",
        help="Controller launch command.",
    )
    parser.add_argument(
        "--clean-on-exit",
        action="store_true",
        help="Always run sudo mn -c at exit.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = _project_root()

    telemetry_csv = root / args.telemetry_output
    summary_csv = root / args.summary_output
    ryu_log_path = root / "results" / "experiment_data" / "baseline_ryu_internet2.log"
    summary_csv.parent.mkdir(parents=True, exist_ok=True)
    telemetry_csv.parent.mkdir(parents=True, exist_ok=True)

    graph = _load_internet2_graph(seed=args.seed)
    controller_nodes = greedy_k_center_placement(graph, args.k)

    print(f"[INFO] Topology: {graph.graph.get('name', 'Internet2')}")
    print(f"[INFO] Nodes={graph.number_of_nodes()} Edges={graph.number_of_edges()}")
    print(f"[INFO] Greedy k-center placements (k={args.k}): {controller_nodes}")

    from mininet.net import Mininet
    from mininet.node import OVSSwitch, RemoteController

    topo_cls = _build_topology(graph, controller_nodes)

    # Clear any lingering Mininet state before creating a fresh topology.
    _run_mininet_cleanup()

    ryu_log_handle = ryu_log_path.open("w", encoding="utf-8")
    ryu_cmd = _resolve_controller_cmd(args.controller_cmd, root)
    ryu_proc = subprocess.Popen(
        ryu_cmd,
        cwd=root,
        stdout=ryu_log_handle,
        stderr=subprocess.STDOUT,
    )

    stop_event = threading.Event()
    telemetry_thread = threading.Thread(
        target=sample_process_telemetry_to_csv,
        kwargs={
            "pid": ryu_proc.pid,
            "output_csv_path": telemetry_csv,
            "sample_interval_s": args.telemetry_interval,
            "stop_event": stop_event,
        },
        daemon=True,
    )
    telemetry_thread.start()

    net: Mininet | None = None
    ping_loss = float("nan")
    run_start = time.perf_counter()
    failed = False

    try:
        if not _wait_for_port("127.0.0.1", args.controller_port, args.controller_ready_timeout):
            raise RuntimeError("Ryu controller did not become ready on time")

        net = Mininet(
            topo=topo_cls(),
            switch=OVSSwitch,
            controller=None,
            autoSetMacs=True,
            build=False,
        )
        net.addController(
            "c0",
            controller=RemoteController,
            ip="127.0.0.1",
            port=args.controller_port,
        )

        net.build()
        net.start()

        ping_loss = float(net.pingAll(timeout=1))
        print(f"[INFO] Ping loss: {ping_loss:.2f}%")

    except Exception:
        failed = True
        raise
    finally:
        if net is not None:
            try:
                net.stop()
            except Exception:
                failed = True

        stop_event.set()
        telemetry_thread.join(timeout=max(2.0, args.telemetry_interval * 4))

        if ryu_proc.poll() is None:
            ryu_proc.terminate()
            try:
                ryu_proc.wait(timeout=8)
            except subprocess.TimeoutExpired:
                ryu_proc.kill()

        ryu_log_handle.close()

        if failed or args.clean_on_exit:
            _run_mininet_cleanup()

    runtime_s = time.perf_counter() - run_start
    reachability_ratio = max(0.0, 1.0 - (ping_loss / 100.0))
    latency_l = average_controller_distance(graph, controller_nodes)

    # Derive simple telemetry aggregates from the sampled CSV.
    cpu_values: list[float] = []
    rss_values: list[float] = []
    with telemetry_csv.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            try:
                cpu_values.append(float(row["cpu_percent"]))
                rss_values.append(float(row["rss_memory_mb"]))
            except (ValueError, TypeError):
                continue

    mean_cpu = sum(cpu_values) / len(cpu_values) if cpu_values else 0.0
    max_rss = max(rss_values) if rss_values else 0.0

    summary_row: dict[str, Any] = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "topology": str(graph.graph.get("name", "Internet2")),
        "topology_source": str(graph.graph.get("source", "synthetic_fallback")),
        "seed": int(args.seed),
        "k": int(args.k),
        "controller_nodes": ";".join(str(node) for node in controller_nodes),
        "latency_l": float(latency_l),
        "reachability_r_avg": float(reachability_ratio),
        "ping_loss_percent": float(ping_loss),
        "tau_runtime_seconds": float(runtime_s),
        "ryu_pid": int(ryu_proc.pid),
        "telemetry_mean_cpu_percent": float(mean_cpu),
        "telemetry_max_rss_mb": float(max_rss),
        "telemetry_csv": str(telemetry_csv),
    }

    write_header = not summary_csv.exists()
    with summary_csv.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary_row.keys()))
        if write_header:
            writer.writeheader()
        writer.writerow(summary_row)

    print("[INFO] Baseline execution complete")
    print(f"[INFO] Telemetry CSV: {telemetry_csv}")
    print(f"[INFO] Summary CSV: {summary_csv}")
    print(f"[INFO] Tau (seconds): {runtime_s:.4f}")
    print(f"[INFO] Reachability R_avg: {reachability_ratio:.4f}")
    print(f"[INFO] Latency l: {latency_l:.4f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
