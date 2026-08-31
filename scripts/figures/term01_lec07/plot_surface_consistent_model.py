"""
Schematic figure for the surface-consistent model.
Four-factor model: source, receiver, offset, CDP.
Source/receiver = near-surface effects to compensate.
Offset/CDP = geological response to preserve.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def main():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_aspect("auto")
    ax.axis("off")

    # --- Geometry constants ---
    surface_y = 5.0
    shallow_reflector_y = 3.8
    deep_reflector_y = 2.2
    source_x, receiver_x = 2.0, 8.0

    # --- Surface line, source, receiver ---
    ax.plot([0.5, 9.5], [surface_y, surface_y], "k-", lw=2)
    ax.scatter(
        [source_x, receiver_x],
        [surface_y, surface_y],
        s=200,
        c=["#4C72B0", "#DD8452"],
        edgecolors="black",
        linewidths=0.5,
        zorder=5,
    )
    ax.text(
        source_x, surface_y + 0.4, "Source $s$",
        ha="center", fontsize=12, fontweight="bold",
    )
    ax.text(
        receiver_x, surface_y + 0.4, "Receiver $r$",
        ha="center", fontsize=12, fontweight="bold",
    )

    # --- Subsurface reflectors ---
    for y, label in [(shallow_reflector_y, "Shallow"), (deep_reflector_y, "Deep")]:
        ax.plot([0, 10], [y, y], "k--", alpha=0.25, lw=1.5)
        ax.text(9.7, y - 0.2, label, fontsize=8, alpha=0.5, ha="right", va="top")

    # --- Ray paths ---
    mid_x = (source_x + receiver_x) / 2  # = 5.0

    # Deep reflector ray (prominent)
    ax.plot(
        [source_x, mid_x, receiver_x],
        [surface_y, deep_reflector_y, surface_y],
        "#C44E52", lw=2.5, alpha=0.85,
    )

    # (Only the deep reflector ray is shown to keep the schematic clean.)

    # --- Midpoint label ---
    ax.plot(mid_x, deep_reflector_y, "k+", markersize=8, alpha=0.3)
    ax.text(mid_x, deep_reflector_y - 0.3, "CDP", fontsize=9, alpha=0.5, ha="center")

    # --- Boxes for the four factors ---
    box_width = 1.8
    box_height = 0.85
    box_y = 0.25

    # Evenly spaced across the x-axis
    x_centers = np.linspace(1.4, 8.6, 4)  # four equally spaced centres

    labels_box = [
        "Source factor\n$s_s(t)$",
        "Receiver factor\n$r_r(t)$",
        "Offset factor\n$h_h(t)$",
        "CDP factor\n$c_c(t)$",
    ]
    # Source/receiver: muted, offset/CDP: bold & saturated
    colors = ["#4C72B0", "#DD8452", "#8E44AD", "#1B7F3A"]
    alphas = [0.20, 0.20, 0.55, 0.55]
    linewidths = [1.0, 1.0, 2.8, 2.8]

    for i, (xc, label, color, alpha, lw) in enumerate(
        zip(x_centers, labels_box, colors, alphas, linewidths)
    ):
        x = xc - box_width / 2
        rect = mpatches.FancyBboxPatch(
            (x, box_y),
            box_width,
            box_height,
            boxstyle="round,pad=0.08",
            facecolor=color,
            alpha=alpha,
            edgecolor=color,
            linewidth=lw,
        )
        ax.add_patch(rect)
        ax.text(
            xc,
            box_y + box_height / 2,
            label,
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold" if i >= 2 else "normal",
        )

    # Put a subtle star/icon on offset & CDP boxes to draw the eye
    for xc in [x_centers[2], x_centers[3]]:
        ax.text(
            xc, box_y + box_height + 0.08,
            "★",
            ha="center", va="bottom", fontsize=9, color="#555555", alpha=0.6,
        )

    # --- Group brackets ---
    bracket_y = 1.7
    tick_len = 0.25

    # Group 1: Source + Receiver
    g1_l = x_centers[0] - box_width / 2
    g1_r = x_centers[1] + box_width / 2
    # Draw bracket: horizontal line + small ticks at ends pointing down
    ax.plot([g1_l, g1_r], [bracket_y, bracket_y], "k-", lw=1.5)
    ax.plot([g1_l, g1_l], [bracket_y, bracket_y - tick_len], "k-", lw=1.5)
    ax.plot([g1_r, g1_r], [bracket_y, bracket_y - tick_len], "k-", lw=1.5)
    ax.text(
        (g1_l + g1_r) / 2, bracket_y + 0.12,
        "Near-surface effects\n(compensate)",
        ha="center", va="bottom", fontsize=9, fontstyle="italic",
        color="#4C72B0",
    )

    # Group 2: Offset + CDP
    g2_l = x_centers[2] - box_width / 2
    g2_r = x_centers[3] + box_width / 2
    ax.plot([g2_l, g2_r], [bracket_y, bracket_y], "k-", lw=1.5)
    ax.plot([g2_l, g2_l], [bracket_y, bracket_y - tick_len], "k-", lw=1.5)
    ax.plot([g2_r, g2_r], [bracket_y, bracket_y - tick_len], "k-", lw=1.5)
    ax.text(
        (g2_l + g2_r) / 2, bracket_y + 0.12,
        "Geological response\n(preserve)",
        ha="center", va="bottom", fontsize=9, fontstyle="italic",
        color="#8E44AD",
    )

    # (No separate trace-wavelet box; the equation is stated in the caption.)

    # --- Title ---
    ax.set_title(
        "Surface-consistent four-factor model",
        fontsize=14, pad=15, fontweight="bold",
    )

    fig.tight_layout()
    out = "figures/term01_lec07/term01_lec07_surface_consistent_model.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
