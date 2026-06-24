"""
Schematic figure for the surface-consistent model.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def main():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # Source and receiver on surface
    ax.plot([1, 9], [5, 5], "k-", lw=2)
    ax.scatter([2, 8], [5, 5], s=200, c=["C0", "C1"], zorder=5)
    ax.text(2, 5.4, "Source $s$", ha="center", fontsize=11)
    ax.text(8, 5.4, "Receiver $r$", ha="center", fontsize=11)

    # Layers
    for y in [3.5, 2.0, 0.8]:
        ax.plot([0, 10], [y, y], "k--", alpha=0.4)

    # Ray paths
    ax.plot([2, 5, 8], [5, 2.0, 5], "C3-", lw=2)
    ax.plot([2, 4.5, 8], [5, 3.5, 5], "C2-", lw=1.5, alpha=0.6)

    # Boxes for factors
    boxes = [
        (0.5, 0.2, "Source factor $s_s(t)$", "C0"),
        (3.5, 0.2, "Receiver factor $r_r(t)$", "C1"),
        (6.0, 0.2, "Offset factor $h_h(t)$", "C4"),
        (8.2, 0.2, "CDP factor $c_c(t)$", "C5"),
    ]
    for x, y, label, color in boxes:
        rect = mpatches.FancyBboxPatch((x, y), 2.0, 0.6, boxstyle="round,pad=0.05", facecolor=color, alpha=0.2, edgecolor=color)
        ax.add_patch(rect)
        ax.text(x + 1.0, y + 0.3, label, ha="center", va="center", fontsize=9)

    ax.set_title("Surface-consistent factors multiply into the trace wavelet", fontsize=13)

    fig.tight_layout()
    out = "figures/term01_lec07/term01_lec07_surface_consistent_model.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
