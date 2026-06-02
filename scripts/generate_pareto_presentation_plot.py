#!/usr/bin/env python3
"""Generate presentation-ready Pareto visualizations from shortlist JSON.

Outputs:
 - results/graphs/pareto_presentation.png
 - results/graphs/pareto_presentation.html (interactive if plotly available)
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHORTLIST = ROOT / "results" / "rl_analysis" / "pareto" / "pareto_shortlist.json"
OUT_DIR = ROOT / "results" / "graphs"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_shortlist(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    data = load_shortlist(SHORTLIST)
    if not data:
        print("No shortlist data found.")
        return 2

    latency = []
    reliability = []
    omega = []
    labels = []

    for entry in data:
        latency.append(float(entry.get("latency_obj", entry.get("average_distance", float('nan')))))
        reliability.append(float(entry.get("control_plane_reliability", 0.0)))
        omega.append(float(entry.get("omega_obj", entry.get("runtime_ms", float('nan')))))
        labels.append(f"{entry.get('algorithm')}:{entry.get('controllers')} (t{entry.get('trial')})")

    # convert to floats and simple lists
    latency = [float(x) for x in latency]
    reliability = [float(x) for x in reliability]
    omega = [float(x) for x in omega]

    # Convert omega assumed ms -> seconds if values look large (>1)
    if max(omega) > 10.0:
        omega_sec = [v / 1000.0 for v in omega]
    else:
        omega_sec = omega

    # Create Matplotlib static scatter (2D projection: latency vs omega, color by reliability)
    try:
        import matplotlib.pyplot as plt
        sc = plt.scatter(latency, omega_sec, c=reliability, cmap="viridis", s=80, edgecolors='k')
        plt.colorbar(sc, label="Control Plane Reliability")
        plt.xlabel("Latency (ms)")
        plt.ylabel("Complexity ω (s/episode)")
        plt.title("Pareto Shortlist: Latency vs Complexity (color=Reliability)")
        for i, txt in enumerate(labels):
            plt.annotate(txt, (latency[i], omega_sec[i]), textcoords="offset points", xytext=(5,5), fontsize=8)
        out_png = OUT_DIR / "pareto_presentation.png"
        plt.tight_layout()
        plt.savefig(out_png, dpi=200)
        plt.close()
        print(f"Saved static Pareto plot: {out_png}")
    except Exception as exc:
        print(f"Matplotlib plotting failed: {exc}")

    # Create Plotly interactive 3D scatter if available
    try:
        import plotly.graph_objects as go
        fig = go.Figure(
            data=go.Scatter3d(
                x=latency,
                y=reliability,
                z=omega_sec,
                mode='markers+text',
                text=labels,
                marker=dict(size=6, color=reliability, colorscale='Viridis', showscale=True),
            )
        )
        fig.update_layout(scene=dict(xaxis_title='Latency (ms)', yaxis_title='Reliability', zaxis_title='Complexity ω (s/episode)'), title='3D Pareto Shortlist')
        out_html = OUT_DIR / "pareto_presentation.html"
        fig.write_html(str(out_html))
        print(f"Saved interactive Pareto plot: {out_html}")
    except Exception as exc:
        print(f"Plotly interactive plot unavailable: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
