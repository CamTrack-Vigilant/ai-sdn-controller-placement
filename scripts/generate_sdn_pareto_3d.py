import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 - needed for 3D projection


def pareto_efficient(points: np.ndarray) -> np.ndarray:
    """Return boolean mask of Pareto-efficient points for min latency, max reliability, min cost."""
    n = points.shape[0]
    efficient = np.ones(n, dtype=bool)

    for i in range(n):
        if not efficient[i]:
            continue

        for j in range(n):
            if i == j:
                continue

            # Domination test in mixed objective space:
            # latency (min), reliability (max), cost (min)
            dominates = (
                (points[j, 0] <= points[i, 0])
                and (points[j, 1] >= points[i, 1])
                and (points[j, 2] <= points[i, 2])
                and (
                    (points[j, 0] < points[i, 0])
                    or (points[j, 1] > points[i, 1])
                    or (points[j, 2] < points[i, 2])
                )
            )

            if dominates:
                efficient[i] = False
                break

    return efficient


def main() -> None:
    # Synthetic benchmark data for SDN Controller Placement
    labels = [
        "Random Placement",
        "Heller (2012) - K-Center",
        "Radam (2022) - HSA-PSO",
        "Farahi (2026) - AP-DQN",
        "Proposed AI Method",
    ]

    # Columns: [Latency (ms), Reliability (0-1), Cost (units)]
    data = np.array(
        [
            [85, 0.45, 10],
            [48, 0.88, 25],
            [20, 0.88, 65],
            [36, 0.82, 80],
            [32, 0.91, 75],
        ],
        dtype=float,
    )

    pareto_mask = pareto_efficient(data)
    pareto_points = data[pareto_mask]
    pareto_labels = [labels[i] for i in range(len(labels)) if pareto_mask[i]]

    # Academic style settings
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 11,
            "axes.labelsize": 12,
            "axes.titlesize": 13,
            "legend.fontsize": 9,
        }
    )

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    # Scatter all methods
    all_scatter = ax.scatter(
        data[:, 0],
        data[:, 1],
        data[:, 2],
        c=np.linspace(0, 1, len(data)),
        cmap="magma",
        s=90,
        edgecolor="black",
        linewidth=0.7,
        alpha=0.95,
        label="Methods",
    )

    # Label points
    for i, name in enumerate(labels):
        ax.text(
            data[i, 0] + 1.2,
            data[i, 1] + 0.01,
            data[i, 2] + 1.2,
            name,
            fontsize=8,
            zorder=20,
        )

    # Pareto frontier surface through efficient points
    # (triangulated surface in objective space)
    if pareto_points.shape[0] >= 3:
        ax.plot_trisurf(
            pareto_points[:, 0],
            pareto_points[:, 1],
            pareto_points[:, 2],
            cmap="viridis",
            alpha=0.38,
            linewidth=0.5,
            edgecolor="#4d4d4d",
            antialiased=True,
        )

    # Highlight Pareto-efficient points
    ax.scatter(
        pareto_points[:, 0],
        pareto_points[:, 1],
        pareto_points[:, 2],
        marker="D",
        s=130,
        c="#00A6D6",
        edgecolor="black",
        linewidth=0.9,
        alpha=1.0,
        label="Pareto-efficient points",
    )

    # Axes labels and limits
    ax.set_xlabel("Average Propagation Latency (ms)", labelpad=12)
    ax.set_ylabel("Control Plane Reliability Score", labelpad=12)
    ax.set_zlabel("Computational Cost (CPU/GPU Units)", labelpad=12)

    ax.set_ylim(0.0, 1.0)
    ax.set_yticks(np.linspace(0.0, 1.0, 6))

    # Invert latency axis so lower latency appears better (to the right/front perspective)
    ax.invert_xaxis()

    # Subtle gridlines
    ax.xaxis._axinfo["grid"]["linewidth"] = 0.5
    ax.yaxis._axinfo["grid"]["linewidth"] = 0.5
    ax.zaxis._axinfo["grid"]["linewidth"] = 0.5
    ax.xaxis._axinfo["grid"]["color"] = (0.75, 0.75, 0.75, 0.35)
    ax.yaxis._axinfo["grid"]["color"] = (0.75, 0.75, 0.75, 0.35)
    ax.zaxis._axinfo["grid"]["color"] = (0.75, 0.75, 0.75, 0.35)

    # Viewing angle to show latency-cost trade-off clearly
    ax.view_init(elev=24, azim=132)

    title = (
        "3D Pareto Frontier for SDN Controller Placement\n"
        "(Latency \u2193, Reliability \u2191, Computational Cost \u2193)"
    )
    ax.set_title(title, pad=18)

    # Legend
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.03), frameon=True)

    # Optional colorbar for method encoding
    cbar = fig.colorbar(all_scatter, ax=ax, pad=0.1, shrink=0.65)
    cbar.set_label("Method index (benchmark ordering)", rotation=90)

    output_path = "SDN_Pareto_3D.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {output_path}")
    print("Pareto-efficient methods:")
    for method in pareto_labels:
        print(f" - {method}")


if __name__ == "__main__":
    main()
