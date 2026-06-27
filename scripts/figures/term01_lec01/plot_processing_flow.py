#!/usr/bin/env python3
"""
Figure: Four-phase seismic data processing flow.

A flowchart illustrating the main stages of a typical seismic processing
workflow taught in this course:

  1. Preprocessing   – data loading, geometry assignment, QC, brute stack
  2. Kinematic       – statics, velocity analysis, NMO correction
  3. Dynamic         – noise attenuation, demultiple, deconvolution,
                       amplitude correction, regularisation
  4. Imaging         – migration, post-migration conditioning

A curved double-headed arrow on the right side indicates that phases 2 and 3
can iterate (e.g., improved velocities after demultiple or noise attenuation).

Pedagogical intention: give students a bird's-eye view of the entire
processing sequence, emphasising that kinematic (positioning) and dynamic
(amplitude) corrections are coupled and often require iterative refinement.
"""

import matplotlib.pyplot as plt
from pathlib import Path


# ---------------------------------------------------------------------------
# Colour palette (light fill colours, dark text)
# ---------------------------------------------------------------------------
PHASE_COLORS = {
    1: "#D6EAF8",   # light blue   – Preprocessing
    2: "#D5F5E3",   # light green  – Kinematic
    3: "#FDEBD0",   # light orange – Dynamic
    4: "#FADBD8",   # light red    – Imaging
}
TEXT_COLOR = "#2C3E50"
ARROW_COLOR = "#555555"
LOOP_COLOR = "#8A6E4E"


# ---------------------------------------------------------------------------
# Helper: draw a simple rectangular box (not rounded)
# ---------------------------------------------------------------------------
def draw_box(ax, x_left, y_bottom, width, height, color, title, items,
             title_fontsize=10, item_fontsize=8.5):
    """Draw a rectangle filled with *color* containing a title and bullet
    items.  Coordinates are in axes data units."""
    # Main rectangle — simple, no rounding, solid border
    box = plt.Rectangle(
        (x_left, y_bottom), width, height,
        facecolor=color, edgecolor="black", linewidth=1.5,
        zorder=2,
    )
    ax.add_patch(box)

    # Phase title (left-aligned with small margin from top-left corner)
    ax.text(
        x_left + 0.15, y_bottom + height - 0.18, title,
        ha="left", va="top", fontsize=title_fontsize,
        fontweight="bold", color=TEXT_COLOR, zorder=3,
    )

    # Bullet items (evenly distributed below the title)
    n = len(items)
    item_area_top = y_bottom + height - 0.30   # leave room for title
    item_area_bottom = y_bottom + 0.05         # small bottom margin
    item_area_height = item_area_top - item_area_bottom

    for i, item in enumerate(items):
        y = item_area_top - (i + 0.5) * item_area_height / n
        ax.text(
            x_left + 0.30, y, f"• {item}",
            ha="left", va="center", fontsize=item_fontsize,
            color=TEXT_COLOR, zorder=3,
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    # ---- Phase data: (title_text, items_list) ----
    phases = [
        ("Preprocessing", [
            "Data loading",
            "Geometry assignment",
            "Quality control",
            "Brute stack",
        ]),
        ("Kinematic processing", [
            "Static corrections",
            "Velocity analysis",
            "NMO correction",
        ]),
        ("Dynamic processing", [
            "Noise attenuation",
            "Demultiple",
            "Deconvolution",
            "Amplitude correction",
            "Regularisation",
        ]),
        ("Imaging", [
            "Migration",
            "Post-migration conditioning",
        ]),
    ]

    # ---- Layout parameters (axes in data coords: 0–10 for both axes) ----
    BOX_WIDTH = 6.0
    BOX_X_LEFT = 2.0          # centres the box at x=5

    # Box y-ranges as required by the spec
    box_y_ranges = [
        (8.0, 9.2),   # Preprocessing
        (6.0, 7.2),   # Kinematic
        (4.0, 5.2),   # Dynamic
        (2.0, 3.2),   # Imaging
    ]

    # ---- Build figure ----
    fig, ax = plt.subplots(1, 1, figsize=(8, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_facecolor("white")

    # ---- Draw boxes ----
    box_centers = []
    for idx, (label, items) in enumerate(phases):
        y_bottom, y_top = box_y_ranges[idx]
        height = y_top - y_bottom
        draw_box(ax, BOX_X_LEFT, y_bottom, BOX_WIDTH, height,
                 PHASE_COLORS[idx + 1], f"{idx + 1}   {label}", items)
        box_centers.append((BOX_X_LEFT + BOX_WIDTH / 2,
                            (y_bottom + y_top) / 2))

    # ---- Downward straight arrows between boxes ----
    arrow_x = BOX_X_LEFT + BOX_WIDTH / 2   # x = 5
    for i in range(len(phases) - 1):
        y_start = box_y_ranges[i][0]         # bottom of this box
        y_end = box_y_ranges[i + 1][1]       # top of next box
        ax.annotate(
            "", xy=(arrow_x, y_end), xytext=(arrow_x, y_start),
            arrowprops=dict(arrowstyle="->", color=ARROW_COLOR, lw=1.8),
            zorder=4,
        )

    # ---- Curved loop arrows between Phase 2 (Kinematic) and Phase 3 (Dynamic) ----
    x_right = BOX_X_LEFT + BOX_WIDTH          # x = 8
    y2 = box_centers[1][1]                     # ~6.6
    y3 = box_centers[2][1]                     # ~4.6

    # Upward arrow: Dynamic → Kinematic (curving to the right)
    ax.annotate(
        "", xy=(x_right + 0.30, y2), xytext=(x_right + 0.30, y3),
        arrowprops=dict(
            arrowstyle="->", color=LOOP_COLOR, lw=1.5,
            connectionstyle="arc3,rad=-0.5",
            linestyle="dashed",
        ),
        zorder=4,
    )

    # Downward arrow: Kinematic → Dynamic (curving to the right)
    ax.annotate(
        "", xy=(x_right + 0.70, y3), xytext=(x_right + 0.70, y2),
        arrowprops=dict(
            arrowstyle="->", color=LOOP_COLOR, lw=1.5,
            connectionstyle="arc3,rad=-0.5",
            linestyle="dashed",
        ),
        zorder=4,
    )

    # "Iterate" label between the two arc paths
    label_x = x_right + 0.50
    label_y = (y2 + y3) / 2
    ax.text(
        label_x, label_y, "Iterate",
        ha="center", va="center", fontsize=9, color=LOOP_COLOR,
        fontstyle="italic", fontweight="bold",
        bbox=dict(boxstyle="round,pad=3",
                  facecolor="white", edgecolor=LOOP_COLOR, alpha=0.9),
        zorder=6,
    )

    # ---- Title (above Box 1, within xlim/ylim 0–10) ----
    ax.text(
        5.0, 9.65, "Seismic Data Processing Flow",
        ha="center", va="top", fontsize=14, fontweight="bold",
        color=TEXT_COLOR, zorder=5,
    )

    # ---- Caption (below Box 4, within xlim/ylim 0–10) ----
    ax.text(
        5.0, 1.55,
        "Phases 2 and 3 are often iterated — improved velocities after\n"
        "demultiple or noise attenuation lead to a better image.",
        ha="center", va="bottom", fontsize=9, fontstyle="italic",
        color="#666666", zorder=5,
    )

    # ---- Save ----
    out_dir = Path("figures/term01_lec01")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "term01_lec01_processing_flow.png"
    fig.savefig(out_path, dpi=150, facecolor="white")
    plt.close(fig)
    print(f"Saved: {out_path}   (8\") × 10\") @ 150 DPI)")


if __name__ == "__main__":
    main()
