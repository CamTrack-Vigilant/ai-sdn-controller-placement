#!/usr/bin/env python3
"""
Generate Publication-Grade Image for Table I: Complete Proposal-Aligned Benchmark Matrix
Includes Canonical (Internet2, ATT-MPLS) and Synthetic (BA, Waxman) Topologies,
3-Axis Metrics (Latency, N-1 Reliability, Runtime, Complexity Tax ω).
"""
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def main():
    data = [
        ["Internet2 (Canonical)", "20", "3", "K-Means / GA", "1.403 ms", "100.0%", "0.031 ms", "0.0000s"],
        ["Internet2 (Canonical)", "20", "5", "Greedy / GA", "0.960 ms", "100.0%", "0.031 ms", "0.0000s"],
        ["ATT-MPLS (Canonical)", "21", "3", "Genetic Algorithm", "2.320 ms", "100.0%", "0.043 ms", "0.0000s"],
        ["ATT-MPLS (Canonical)", "21", "5", "Genetic Algorithm", "1.828 ms", "100.0%", "0.046 ms", "0.0000s"],
        ["Barabási-Albert", "20", "3", "K-Means", "2.177 ms", "100.0%", "0.049 ms", "0.0000s"],
        ["Barabási-Albert", "50", "3", "K-Means", "4.863 ms", "100.0%", "0.037 ms", "0.0000s"],
        ["Waxman", "20", "3", "Greedy K-Center", "2.640 ms", "96.1%", "0.031 ms", "0.0000s"],
        ["Waxman", "50", "3", "K-Means / GA", "7.707 ms", "97.6%", "0.074 ms", "0.0000s"],
        ["DQN / DRL Stack", "20", "3", "PyTorch DQN", "1.420 ms", "100.0%", "21,260 ms", "0.0213s"],
    ]

    columns = [
        "Topology Model",
        "Nodes (N)",
        "Budget (k)",
        "Best Algorithm",
        "Avg Latency L(P)",
        "N-1 Reliability",
        "Runtime (ms)",
        "Complexity Tax ω"
    ]

    fig, ax = plt.subplots(figsize=(11, 4.8), dpi=300)
    ax.axis('off')

    # Title
    fig.suptitle(
        "TABLE I: COMPLETE PROPOSAL-ALIGNED MULTI-OBJECTIVE BENCHMARK MATRIX",
        fontsize=11.5,
        fontweight='bold',
        fontname='DejaVu Sans',
        y=0.96,
        color='#1A365D'
    )

    # Render Table
    table = ax.table(
        cellText=data,
        colLabels=columns,
        loc='center',
        cellLoc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.1, 1.7)

    # Style Header & Cells
    for key, cell in table.get_celld().items():
        row, col = key
        cell.set_edgecolor('#CBD5E0')
        cell.set_linewidth(0.8)
        
        if row == 0:
            cell.set_facecolor('#1A365D')
            cell.get_text().set_color('white')
            cell.get_text().set_fontweight('bold')
            cell.get_text().set_fontsize(9.5)
        else:
            if row == len(data):  # Highlight DRL Row
                cell.set_facecolor('#FEF3C7')
                cell.get_text().set_fontweight('bold')
            elif row % 2 == 0:
                cell.set_facecolor('#F7FAFC')
            else:
                cell.set_facecolor('#FFFFFF')

            # Highlight Best Algorithm column
            if col == 3 and row != len(data):
                cell.get_text().set_fontweight('bold')
                cell.get_text().set_color('#0D9488')

            # Highlight Reliability column
            if col == 5:
                cell.get_text().set_fontweight('bold')
                cell.get_text().set_color('#2563EB')

    plt.tight_layout()
    output_dir = PROJECT_ROOT / "docs" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "factorial_benchmark_table.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    print(f"✓ Proposal-aligned Table I image successfully generated at: {output_path}")

if __name__ == "__main__":
    main()
