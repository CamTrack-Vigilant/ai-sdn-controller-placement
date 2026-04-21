import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


def pareto_efficient(points: np.ndarray) -> np.ndarray:
    """Pareto mask for min latency, max reliability, min cost."""
    n = points.shape[0]
    efficient = np.ones(n, dtype=bool)

    for i in range(n):
        if not efficient[i]:
            continue
        for j in range(n):
            if i == j:
                continue
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
    labels = [
        "Random Placement",
        "Heller (2012) - K-Center",
        "Radam (2022) - HSA-PSO",
        "Farahi (2026) - AP-DQN",
        "Proposed AI Method",
    ]

    # [Latency, Reliability, Cost]
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

    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 14,
            "axes.labelsize": 14,
            "axes.titlesize": 14,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
        }
    )

    # Exact proposal footprint size
    fig = plt.figure(figsize=(3.5, 2.5))
    ax = fig.add_subplot(111, projection="3d")

    # Main scatter with requested styling
    ax.scatter(
        data[:, 0],
        data[:, 1],
        data[:, 2],
        c="#1f77b4",
        s=150,
        edgecolor="white",
        linewidth=1.2,
        alpha=0.97,
        label="Methods",
    )

    # Pareto surface
    if pareto_points.shape[0] >= 3:
        ax.plot_trisurf(
            pareto_points[:, 0],
            pareto_points[:, 1],
            pareto_points[:, 2],
            cmap="viridis",
            alpha=0.35,
            linewidth=0.4,
            edgecolor=(0.3, 0.3, 0.3, 0.45),
            antialiased=True,
        )

    # Highlight efficient points with same white edge-lining style
    ax.scatter(
        pareto_points[:, 0],
        pareto_points[:, 1],
        pareto_points[:, 2],
        c="#d62728",
        s=150,
        marker="D",
        edgecolor="white",
        linewidth=1.2,
        alpha=1.0,
        label="Pareto-efficient",
    )

    # Shortened axis labels avoid clipping at strict 3.5" x 2.5" print size.
    # Suppress projected 3D labels (they clip in very small print canvases).
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_zlabel("")

    ax.set_ylim(0.0, 1.0)
    ax.set_yticks(np.linspace(0.0, 1.0, 6))

    # Ensure inverted latency axis is explicit and visible
    ax.set_xlim(90, 15)
    ax.invert_xaxis()

    # Subtle grid
    ax.xaxis._axinfo["grid"]["linewidth"] = 0.35
    ax.yaxis._axinfo["grid"]["linewidth"] = 0.35
    ax.zaxis._axinfo["grid"]["linewidth"] = 0.35
    ax.xaxis._axinfo["grid"]["color"] = (0.75, 0.75, 0.75, 0.32)
    ax.yaxis._axinfo["grid"]["color"] = (0.75, 0.75, 0.75, 0.32)
    ax.zaxis._axinfo["grid"]["color"] = (0.75, 0.75, 0.75, 0.32)

    # Trade-off perspective
    ax.view_init(elev=24, azim=132)

    # Omit title to maximize usable label space in 3.5" x 2.5" footprint.
    ax.set_title("")

    # No colorbar (requested)

    # Tight margins for proposal placement
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)

    # Figure-level labels remain visible without clipping or overlap.
    fig.text(0.44, 0.01, "Latency (ms) [inverted]", ha="center", va="bottom", fontsize=14)
    fig.text(0.98, 0.50, "Comp. Cost Units", ha="center", va="center", rotation=90, fontsize=14)
    fig.text(0.06, 0.56, "Reliability (0-1)", ha="center", va="center", rotation=90, fontsize=14)

    output_path = "SDN_Pareto_3D_Print.png"
    # Tight bounding box with small pad preserves labels while maximizing occupied area.
    plt.savefig(output_path, dpi=300, bbox_inches="tight", pad_inches=0.05)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
