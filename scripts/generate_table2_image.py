#!/usr/bin/env python3
"""
Generate Publication-Grade Image for Table II: Mininet OpenFlow Control-Plane RTT & Reliability
"""
from pathlib import Path
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def main():
    data = [
        ["Genetic Algorithm", "['n1', 'n15', 'n16']", "2.718 ms", "6.903 ms", "100.0%", "1st (Lowest Avg)"],
        ["K-Means", "['n1', 'n16', 'n9']", "2.852 ms", "5.764 ms", "100.0%", "2nd (Best Worst-Case)"],
        ["Greedy K-Center", "['n1', 'n10', 'n6']", "2.934 ms", "6.664 ms", "100.0%", "3rd"],
        ["Bandit RL / DQN", "['n1', 'n10', 'n5']", "3.056 ms", "6.718 ms", "100.0%", "4th"],
        ["Random Baseline", "['n13', 'n0', 'n18']", "3.374 ms", "6.944 ms", "100.0%", "5th (Baseline)"],
    ]

    columns = [
        "Placement Strategy",
        "Selected Controllers",
        "Avg Control RTT",
        "Worst-Case RTT",
        "N-1 Reliability",
        "Emulation Rank"
    ]

    fig, ax = plt.subplots(figsize=(10.0, 4.0), dpi=300)
    ax.axis('off')

    # Title
    fig.suptitle(
        "TABLE II: MININET OPENFLOW CONTROL-PLANE RTT & RELIABILITY MEASUREMENTS",
        fontsize=11,
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
    table.set_fontsize(9.5)
    table.scale(1.1, 1.8)

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
            if row % 2 == 0:
                cell.set_facecolor('#F7FAFC')
            else:
                cell.set_facecolor('#FFFFFF')

            # Highlight Best Placement
            if row == 1 and col == 0:
                cell.get_text().set_fontweight('bold')
                cell.get_text().set_color('#0D9488')

            if row == 1 and col == 2:
                cell.get_text().set_fontweight('bold')
                cell.get_text().set_color('#0D9488')

            # Highlight RTT Rank
            if col == 5:
                cell.get_text().set_fontweight('bold')
                if row == 1:
                    cell.get_text().set_color('#D97706')
                elif row == 2:
                    cell.get_text().set_color('#4B5563')
                else:
                    cell.get_text().set_color('#9CA3AF')

    plt.tight_layout()
    output_dir = PROJECT_ROOT / "docs" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "mininet_rtt_table.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    print(f"✓ Proposal-aligned Table II image successfully generated at: {output_path}")

if __name__ == "__main__":
    main()
