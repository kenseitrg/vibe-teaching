#!/usr/bin/env python3
"""
Figure: Exploration workflow block diagram.

Illustrates the geological exploration (ГРР) lifecycle, showing seismic
processing as one stage in a larger chain.  The diagram emphasises that
seismic data is one of several inputs — alongside well data, geology
knowledge, and a priori information — that feed into interpretation and
geological modelling.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path


# ---------------------------------------------------------------------------
# Helper drawing functions
# ---------------------------------------------------------------------------

def _draw_box(ax, cx, cy, w, h, text, facecolor, edgecolor=None,
              textcolor="white", fontsize=10, fontweight="bold"):
    """Rounded rectangle with centred text."""
    box = mpatches.FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.12",
        facecolor=facecolor,
        edgecolor=edgecolor or facecolor,
        linewidth=1.5,
        zorder=3,
    )
    ax.add_patch(box)
    ax.text(cx, cy, text, ha="center", va="center",
            fontsize=fontsize, fontweight=fontweight,
            color=textcolor, zorder=4)
    return box


def _draw_arrow(ax, x1, y1, x2, y2, **kw):
    """Straight arrow from (x1, y1) to (x2, y2)."""
    props = dict(
        arrowstyle="-|>,head_width=0.30,head_length=0.18",
        linewidth=1.5,
        color="#444444",
        zorder=2,
    )
    props.update(kw)
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=props)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Figure & axes ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.set_aspect("equal")
    ax.axis("off")

    # Colour palette --------------------------------------------------------
    MAIN_BLUE   = "#3B6BA5"   # main workflow boxes
    INPUT_GREEN = "#5F8E3E"   # additional-data boxes
    FEEDBACK    = "#C06014"   # feedback loop
    BG_GRAY     = "#F0F0F0"   # subtle grouping background

    # ---- 1. Main workflow boxes (left-to-right) --------------------------

    bw, bh = 1.8, 0.85          # box width, height
    y_main = 4.2                 # vertical centre of main row
    # Six boxes spanning roughly 1.0 … 13.0
    x_centers = [1.0, 3.4, 5.8, 8.2, 10.6, 13.0]

    labels = [
        "Study of\nGeology",
        "Field\nAcquisition",
        "Seismic\nProcessing",
        "Interpretation",
        "Geological\nModeling",
        "Drilling",
    ]

    for xc, lab in zip(x_centers, labels):
        _draw_box(ax, xc, y_main, bw, bh, lab, MAIN_BLUE,
                  fontsize=10, fontweight="bold")

    # ---- 2. Connecting arrows between main boxes -------------------------

    for i in range(len(x_centers) - 1):
        x1 = x_centers[i] + bw / 2
        x2 = x_centers[i + 1] - bw / 2
        _draw_arrow(ax, x1, y_main, x2, y_main)

    # ---- 3. Feedback loop (Drilling → back to Geology) ------------------

    # Dashed curved arrow below the main row
    ax.annotate(
        "",
        xy=(x_centers[0], y_main - bh / 2),
        xytext=(x_centers[-1], y_main - bh / 2),
        arrowprops=dict(
            arrowstyle="-|>,head_width=0.35,head_length=0.22",
            linewidth=1.8,
            color=FEEDBACK,
            connectionstyle="arc3,rad=-0.55",
            linestyle="dashed",
            shrinkA=6,
            shrinkB=6,
        ),
        zorder=2,
    )

    # Feedback label
    ax.text(
        (x_centers[0] + x_centers[-1]) / 2, 1.85,
        "Drilling results refine geological understanding\n"
        "→ iterative exploration lifecycle",
        ha="center", va="top", fontsize=8, fontstyle="italic",
        color=FEEDBACK, zorder=4,
    )

    # ---- 4. Additional-input group --------------------------------------

    # Background rectangle to visually group the three input boxes
    iw, ih = 1.5, 0.60          # input-box size
    y_inp = 1.45                 # vertical centre of input row

    # Group background
    bg = mpatches.FancyBboxPatch(
        (5.55, y_inp - ih / 2 - 0.35),
        5.6, ih + 0.70,
        boxstyle="round,pad=0.15",
        facecolor=BG_GRAY,
        edgecolor="#CCCCCC",
        linewidth=1.0,
        zorder=1,
    )
    ax.add_patch(bg)

    # Group title
    ax.text(
        8.35, y_inp + ih / 2 + 0.38,
        "Additional data sources integrated with seismic data",
        ha="center", va="bottom", fontsize=9, fontstyle="italic",
        color="#555555", zorder=4,
    )

    # Three input boxes
    inp_x = [6.6, 8.35, 10.1]
    inp_lab = [
        "Well\ndata",
        "Geology\nknowledge",
        "A priori\ninformation",
    ]
    for xc, lab in zip(inp_x, inp_lab):
        _draw_box(ax, xc, y_inp, iw, ih, lab, INPUT_GREEN,
                  fontsize=9, fontweight="normal")

    # ---- 5. Arrows from additional inputs to main stages ------------------

    # Map each input box to the main-stage x it feeds into:
    #   Wells          → Interpretation
    #   Geology knowl. → Interpretation
    #   A priori       → Geological Modeling
    targets = [8.2, 8.2, 10.6]

    for ix, mx in zip(inp_x, targets):
        y_start = y_inp + ih / 2
        y_end   = y_main - bh / 2
        ax.annotate(
            "", xy=(mx, y_end), xytext=(ix, y_start),
            arrowprops=dict(
                arrowstyle="-|>,head_width=0.22,head_length=0.14",
                linewidth=1.2,
                color=INPUT_GREEN,
                connectionstyle="arc3,rad=0.15",
            ),
            zorder=2,
        )

    # ---- 6. Title / caption ----------------------------------------------

    ax.text(
        7.0, 5.65, "Geological Exploration Lifecycle",
        ha="center", va="center", fontsize=14, fontweight="bold",
        color="#333333", zorder=4,
    )
    ax.text(
        7.0, 5.25,
        "Seismic processing is one stage; seismic data is one of several inputs",
        ha="center", va="center", fontsize=9, fontstyle="italic",
        color="#666666", zorder=4,
    )

    # ---- Save ------------------------------------------------------------
    out_dir = Path("figures/term01_lec01")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "term01_lec01_exploration_workflow.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
