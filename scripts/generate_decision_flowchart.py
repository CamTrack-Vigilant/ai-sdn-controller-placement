#!/usr/bin/env python3
"""
Generate Publication-Grade Decision Flowchart Figure (Fig. 2)
Aligned with SATNAC Reviewer Feedback:
  - Bounded to experimental scale N <= 50
  - Cautious framing of dynamic churn / failure recovery as future/adaptive candidate
"""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def main():
    fig, ax = plt.subplots(figsize=(8.5, 8.0), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor('#FAFBFD')

    # 1. Top Box: Network Deployment Scenario
    top_box = patches.FancyBboxPatch(
        (3.0, 8.0), 4.0, 1.3,
        boxstyle="round,pad=0.1,rounding_size=0.25",
        linewidth=2.5, edgecolor='#1E3A5F', facecolor='#FFFFFF'
    )
    ax.add_patch(top_box)
    ax.text(5.0, 8.65, "Network Deployment\nScenario", ha='center', va='center',
            fontsize=14, fontweight='bold', color='#0F172A', fontname='DejaVu Sans')

    # Arrow from Top Box to Diamond
    ax.annotate("", xy=(5.0, 7.15), xytext=(5.0, 7.95),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.5", lw=2.5, color='#1E3A5F'))

    # 2. Center Diamond: Decision Condition (N <= 50)
    diamond_coords = [(5.0, 7.15), (6.9, 5.4), (5.0, 3.65), (3.1, 5.4)]
    diamond = patches.Polygon(diamond_coords, closed=True, linewidth=2.5,
                              edgecolor='#1E3A5F', facecolor='#FFFFFF')
    ax.add_patch(diamond)
    ax.text(5.0, 5.4, "Is the\ntopology\nstatic or\npredictable\n(N \u2264 50)?",
            ha='center', va='center', fontsize=12.5, fontweight='bold',
            color='#0F172A', fontname='DejaVu Sans')

    # Left Branch (YES)
    ax.plot([3.1, 2.2, 2.2], [5.4, 5.4, 3.35], lw=2.5, color='#1E3A5F')
    ax.annotate("", xy=(2.2, 3.15), xytext=(2.2, 3.45),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.5", lw=2.5, color='#1E3A5F'))
    ax.text(2.65, 5.65, "YES", ha='center', va='center', fontsize=12, fontweight='bold', color='#0F172A')

    # Right Branch (NO)
    ax.plot([6.9, 7.8, 7.8], [5.4, 5.4, 3.35], lw=2.5, color='#1E3A5F')
    ax.annotate("", xy=(7.8, 3.15), xytext=(7.8, 3.45),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.5", lw=2.5, color='#1E3A5F'))
    ax.text(8.15, 4.7, "NO\n(Dynamic Churn /\nMulti-Constraint\nFailure Scenarios)",
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#0F172A',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#FAFBFD', edgecolor='none'))

    # 3. Bottom-Left Box: Heuristics / GA
    left_box = patches.FancyBboxPatch(
        (0.5, 0.6), 3.4, 2.4,
        boxstyle="round,pad=0.1,rounding_size=0.2",
        linewidth=1.5, edgecolor='#059669', facecolor='#10B981'
    )
    ax.add_patch(left_box)
    ax.text(2.2, 1.8, "Deploy K-Means or\nGreedy K-Center\n(or GA for Offline Optimal)\n\n(Compute Overhead < 5 ms,\n100% N-1 Survivability)",
            ha='center', va='center', fontsize=11, fontweight='bold', color='#FFFFFF', fontname='DejaVu Sans')

    # 4. Bottom-Right Box: Adaptive DRL Candidate
    right_box = patches.FancyBboxPatch(
        (6.1, 0.6), 3.4, 2.4,
        boxstyle="round,pad=0.1,rounding_size=0.2",
        linewidth=1.5, edgecolor='#0E7490', facecolor='#158096'
    )
    ax.add_patch(right_box)
    ax.text(7.8, 1.8, "Candidate for Adaptive\nPyTorch DRL / GNN\n\n(Requires Amortization of\n\u03c9 = 0.0213 s/ep Tax Across\nDynamic State Transitions)",
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#FFFFFF', fontname='DejaVu Sans')

    plt.tight_layout()
    output_path = PROJECT_ROOT / "docs" / "figures" / "decision_framework_flowchart.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    print(f"✓ Regenerated decision flowchart (N <= 50) at: {output_path}")

if __name__ == "__main__":
    main()

