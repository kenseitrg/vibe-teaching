#!/usr/bin/env python3
"""
Figure: 2D acquisition geometry and fold build-up.

Illustrates end-on 2D seismic acquisition geometry (marine or land).
Three consecutive shots are shown with their receiver spreads, source–
receiver midpoints, and offset labels.  A combined CMP grid below the
geometry rows shows how midpoints from different shots interleave at
half the receiver spacing.  The bottom panel plots the fold profile
along the line to show the characteristic trapezoidal build-up.

Realistic parameters:
  Shot interval      = 25 m
  Receiver interval  = 12.5 m
  Number of receivers per shot = 24
  Minimum offset     = 12.5 m
  Maximum offset     = 300 m

Pedagogical intention: give students a visual, geometric understanding of
2D end-on acquisition — how the spread rolls, where midpoints fall, and
how fold builds up from the edges to a constant level in the middle of
the survey.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path


# ---------------------------------------------------------------------------
# Acquisition parameters
# ---------------------------------------------------------------------------
REC_INTERVAL = 12.5          # receiver spacing (m)
SHOT_INTERVAL = 25.0         # source spacing (m)
N_RECEIVERS = 24             # live channels per shot
MIN_OFFSET = 12.5            # distance from source to nearest receiver (m)
MAX_OFFSET = MIN_OFFSET + (N_RECEIVERS - 1) * REC_INTERVAL  # 300 m
CMP_INTERVAL = REC_INTERVAL / 2   # 6.25 m

# Colours for the three shots (colorblind-friendly palette)
SHOT_COLORS = ["#4C72B0", "#55A868", "#DD8452"]   # blue, green, orange
FOLD_COLOR = "#3B6BA5"      # blue for fold profile
ANNOT_COLOR = "#444444"     # dark grey for annotation text

# ---------------------------------------------------------------------------
# Helper: draw a pair of aligned midpoints to illustrate CMP spacing
# ---------------------------------------------------------------------------
def annotate_cmp_spacing(ax, x1, y, text, color=ANNOT_COLOR, fontsize=8):
    """Place a horizontal bracket with label between x1 and x1 + CMP_INTERVAL."""
    dx = CMP_INTERVAL
    # small ticks at the two CMP positions
    ax.plot([x1, x1], [y - 0.08, y + 0.08], color=color, lw=1.0)
    ax.plot([x1 + dx, x1 + dx], [y - 0.08, y + 0.08], color=color, lw=1.0)
    # horizontal line spanning the interval
    ax.plot([x1, x1 + dx], [y, y], color=color, lw=1.0)
    # arrow heads
    ax.annotate("", xy=(x1 + dx * 0.95, y), xytext=(x1 + dx * 0.05, y),
                arrowprops=dict(arrowstyle="<->", color=color, lw=1.0))
    # label
    ax.text(x1 + dx / 2, y - 0.22, text, ha="center", va="top",
            fontsize=fontsize, color=color)


# ---------------------------------------------------------------------------
# Compute receiver and midpoint positions for one shot
# ---------------------------------------------------------------------------
def shot_geometry(source_x):
    """Return (receiver_x, midpoint_x) arrays for a single shot."""
    offsets = MIN_OFFSET + np.arange(N_RECEIVERS) * REC_INTERVAL
    receiver_x = source_x + offsets
    midpoint_x = (source_x + receiver_x) / 2.0
    return receiver_x, midpoint_x


# ---------------------------------------------------------------------------
# Compute fold profile for a line of shots
# ---------------------------------------------------------------------------
def compute_fold(n_shots=20):
    """Return (cmp_centers, fold) arrays.

    Fires *n_shots* shots starting at x=0 with SHOT_INTERVAL spacing.
    Each shot contributes N_RECEIVERS traces whose midpoints are binned
    at CMP_INTERVAL spacing.
    """
    shot_pos = np.arange(n_shots) * SHOT_INTERVAL
    all_midpoints = []
    for s in shot_pos:
        _, mid_x = shot_geometry(s)
        all_midpoints.append(mid_x)

    all_midpoints = np.concatenate(all_midpoints)

    # Define CMP bin boundaries (centres at multiples of CMP_INTERVAL)
    x_min = all_midpoints.min() - CMP_INTERVAL / 2
    x_max = all_midpoints.max() + CMP_INTERVAL / 2
    bin_edges = np.arange(x_min, x_max + CMP_INTERVAL, CMP_INTERVAL)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    fold, _ = np.histogram(all_midpoints, bins=bin_edges)
    return bin_centers, fold


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    # ---- Three shot positions for the cartoon ----------------------------
    shot_positions = np.arange(3) * SHOT_INTERVAL  # [0, 25, 50]

    # Pre-compute geometry for each shot
    all_rec_x = []
    all_mid_x = []
    for s in shot_positions:
        rec_x, mid_x = shot_geometry(s)
        all_rec_x.append(rec_x)
        all_mid_x.append(mid_x)

    # ---- Figure layout ---------------------------------------------------
    fig = plt.figure(figsize=(12, 7))
    gs = gridspec.GridSpec(2, 1, height_ratios=[2.0, 1.0],
                           hspace=0.30, bottom=0.10, top=0.94,
                           left=0.08, right=0.96)

    ax_geom = fig.add_subplot(gs[0])
    ax_fold = fig.add_subplot(gs[1])

    # X limits cover all three shots, padded
    x_pad = 30
    x_min = shot_positions[0] - x_pad
    x_max = shot_positions[-1] + MAX_OFFSET + x_pad

    # ======================================================================
    # GEOMETRY CARTOON
    # ======================================================================
    ax_geom.set_xlim(x_min, x_max)
    ax_geom.set_ylim(0, 6.0)
    # Do NOT use equal aspect — the x-range is ~500 m while y-range is ~6 units,
    # so equal aspect would produce an impractically wide figure.
    ax_geom.set_aspect("auto")
    ax_geom.axis("off")

    # Vertical lanes for each shot row + combined midpoints row
    y_shots = [5.0, 3.6, 2.2]       # y-centre of each shot row
    y_combined = 0.85                # y-centre of combined-midpoint row
    y_survey_line = 0.0              # ground line

    # Draw survey line at the bottom
    ax_geom.plot([x_min, x_max], [y_survey_line, y_survey_line],
                 color="#888888", lw=1.5, zorder=1)
    ax_geom.text(x_max - 5, y_survey_line, "Survey line",
                 ha="right", va="bottom", fontsize=7, color="#888888",
                 fontstyle="italic", zorder=1)

    # ---- Draw each shot row ---------------------------------------------
    for i in range(3):
        y = y_shots[i]
        s_x = shot_positions[i]
        r_x = all_rec_x[i]
        m_x = all_mid_x[i]
        color = SHOT_COLORS[i]

        # Source marker
        ax_geom.plot(s_x, y, marker=(5, 1, 0), markersize=14,
                     color=color, markeredgecolor="white", markeredgewidth=0.8,
                     zorder=5, linestyle="none")
        ax_geom.text(s_x - 3, y + 0.35, f"S{i+1}", ha="center", va="bottom",
                     fontsize=10, fontweight="bold", color=color, zorder=5)

        # Receiver markers (show every 4th receiver to avoid clutter)
        plot_every = 2
        for j in range(0, N_RECEIVERS, plot_every):
            rx = r_x[j]
            ax_geom.plot(rx, y, marker="v", markersize=6,
                         color=color, markeredgecolor="white",
                         markeredgewidth=0.5, zorder=4, linestyle="none")

        # Label first and last receiver
        ax_geom.text(r_x[0] - 2, y - 0.35, f"R₁", ha="center", va="top",
                     fontsize=7, color=color)
        ax_geom.text(r_x[-1] + 2, y - 0.35, f"R_{N_RECEIVERS}", ha="center",
                     va="top", fontsize=7, color=color)

        # Connecting dashed lines from source to first and last receiver
        ax_geom.plot([s_x, r_x[0]], [y, y], color=color, lw=0.8,
                     linestyle=":", zorder=2)
        ax_geom.plot([s_x, r_x[-1]], [y, y], color=color, lw=0.8,
                     linestyle=":", zorder=2)

        # Midpoint dots along the survey-line row (lifted slightly above y=0)
        y_mid = 0.15
        ax_geom.plot(m_x, [y_mid] * len(m_x), marker="o", markersize=4,
                     color=color, markeredgecolor="none",
                     alpha=0.7, zorder=6, linestyle="none")

    # ---- Annotations for shot 1 (lowest shot row, i=2) -------------------
    y_annot = y_shots[2]
    s1_x = shot_positions[2]
    r1_x = all_rec_x[2]

    # Minimum offset
    ax_geom.annotate(
        "", xy=(r1_x[0], y_annot), xytext=(s1_x, y_annot),
        arrowprops=dict(arrowstyle="<->", color=ANNOT_COLOR, lw=1.2),
        zorder=7)
    ax_geom.text((s1_x + r1_x[0]) / 2, y_annot + 0.30,
                 f"Min offset\n{MIN_OFFSET:.0f} m",
                 ha="center", va="bottom", fontsize=7.5, color=ANNOT_COLOR,
                 fontweight="bold")

    # Maximum offset
    ax_geom.annotate(
        "", xy=(r1_x[-1], y_annot), xytext=(s1_x, y_annot),
        arrowprops=dict(arrowstyle="<->", color=ANNOT_COLOR, lw=1.2),
        zorder=7)
    # Place text above the right side of the spread
    ax_geom.text((s1_x + r1_x[-1]) / 2, y_annot + 0.30,
                 f"Max offset\n{MAX_OFFSET:.0f} m",
                 ha="center", va="bottom", fontsize=7.5, color=ANNOT_COLOR,
                 fontweight="bold")

    # Receiver interval (between first two receivers of shot 1)
    rx_riv = s1_x + MIN_OFFSET + np.array([0, 1]) * REC_INTERVAL
    ax_geom.annotate(
        "", xy=(rx_riv[1], y_annot - 0.45), xytext=(rx_riv[0], y_annot - 0.45),
        arrowprops=dict(arrowstyle="<->", color=ANNOT_COLOR, lw=1.0),
        zorder=7)
    ax_geom.text(rx_riv[0] + REC_INTERVAL / 2, y_annot - 0.70,
                 f"Rec. interval\n{REC_INTERVAL:.0f} m",
                 ha="center", va="top", fontsize=7.5, color=ANNOT_COLOR,
                 fontweight="bold")

    # Shot interval (horizontal arrow between S1 at x=0 and S2 at x=25)
    y_si = y_shots[2] - 0.70   # below the lowest shot row
    ax_geom.annotate(
        "", xy=(shot_positions[1], y_si), xytext=(shot_positions[0], y_si),
        arrowprops=dict(arrowstyle="<->", color=ANNOT_COLOR, lw=1.2),
        zorder=7)
    ax_geom.text(SHOT_INTERVAL / 2, y_si - 0.25,
                 f"Shot interval\n{SHOT_INTERVAL:.0f} m",
                 ha="center", va="top", fontsize=7.5,
                 color=ANNOT_COLOR, fontweight="bold")

    # ---- Combined CMP row -----------------------------------------------
    y_mid_row = y_combined

    # Collect all midpoints from all 3 shots
    all_m_x_flat = np.concatenate(all_mid_x)

    # Draw all midpoints, color-coded by shot
    for i in range(3):
        m_x = all_mid_x[i]
        ax_geom.plot(m_x, [y_mid_row] * len(m_x), marker="o", markersize=5,
                     color=SHOT_COLORS[i], markeredgecolor="white",
                     markeredgewidth=0.3, alpha=0.9, zorder=6,
                     linestyle="none")

    # Label the combined CMP row
    ax_geom.text(x_max - 5, y_mid_row, "CMP positions",
                 ha="right", va="center", fontsize=7, color="#888888",
                 fontstyle="italic", zorder=1)

    # CMP spacing annotation on the combined row
    # Find the first two distinct midpoints
    unique_mid = np.sort(np.unique(np.round(all_m_x_flat / CMP_INTERVAL) * CMP_INTERVAL))
    if len(unique_mid) >= 2:
        x1 = unique_mid[0]
        annotate_cmp_spacing(ax_geom, x1, y_mid_row - 0.45,
                             f"CMP spacing\n{CMP_INTERVAL:.2f} m",
                             fontsize=7.5)

    # ---- Legend ----------------------------------------------------------
    legend_elements = [
        plt.Line2D([0], [0], marker=(5, 1, 0), color="w",
                   markerfacecolor="#555555", markersize=10,
                   label="Source", markeredgecolor="white",
                   markeredgewidth=0.8),
        plt.Line2D([0], [0], marker="v", color="w",
                   markerfacecolor="#555555", markersize=8,
                   label="Receiver", markeredgecolor="white",
                   markeredgewidth=0.5),
        plt.Line2D([0], [0], marker="o", color="w",
                   markerfacecolor="#555555", markersize=6,
                   label="Midpoint (CMP)"),
    ]
    leg = ax_geom.legend(handles=legend_elements, loc="upper left",
                         fontsize=8, framealpha=0.9,
                         bbox_to_anchor=(0.0, 1.02), ncol=3)
    leg.get_frame().set_linewidth(0.5)

    # ---- Title -----------------------------------------------------------
    ax_geom.text(
        (x_min + x_max) / 2, 5.85,
        "2D End-On Acquisition Geometry",
        ha="center", va="center", fontsize=13, fontweight="bold",
        color="#333333", zorder=8)

    # ======================================================================
    # FOLD PROFILE
    # ======================================================================
    cmp_centers, fold = compute_fold(n_shots=20)

    # Find the full-fold level (stable plateau in the middle)
    full_fold = int(np.median(fold[len(fold)//4: -len(fold)//4]))

    # Mask fold data to the visible x-range (matching geometry panel)
    mask = (cmp_centers >= x_min) & (cmp_centers <= x_max)
    cmp_centers_masked = cmp_centers[mask]
    fold_masked = fold[mask]

    # Bar chart
    ax_fold.bar(cmp_centers_masked, fold_masked, width=CMP_INTERVAL * 0.85,
                color=FOLD_COLOR, alpha=0.85, edgecolor="white",
                linewidth=0.3, zorder=3)

    # Reference line for full-fold level
    ax_fold.axhline(full_fold, color="#C44E52", linestyle="--", lw=1.0,
                    zorder=4)
    # Place the fold-annotation text inside the visible area (top-right corner)
    ax_fold.text(x_max - 10, full_fold + 0.4,
                 f"Full fold = {full_fold}",
                 fontsize=8, color="#C44E52", va="bottom", ha="right",
                 fontweight="bold")

    # Labels
    ax_fold.set_xlabel("Position along line (m)", fontsize=10)
    ax_fold.set_ylabel("Fold", fontsize=10)
    # Set fold x-range to match geometry panel
    ax_fold.set_xlim(x_min, x_max)
    y_fold_max = fold.max() + 2
    ax_fold.set_ylim(0, y_fold_max)
    ax_fold.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax_fold.grid(axis="y", alpha=0.3, linestyle=":")
    ax_fold.set_title("Fold Profile", fontsize=11, fontweight="bold",
                      pad=6)

    # ======================================================================
    # SAVE
    # ======================================================================
    out_dir = Path("figures/term01_lec01")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "term01_lec01_2d_acquisition_geometry.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)
    print(f"Saved: {out_path}")

    # Print key parameters for verification
    print(f"  Shot interval:      {SHOT_INTERVAL:.0f} m")
    print(f"  Receiver interval:  {REC_INTERVAL:.1f} m")
    print(f"  Receivers/shot:     {N_RECEIVERS}")
    print(f"  Min offset:         {MIN_OFFSET:.1f} m")
    print(f"  Max offset:         {MAX_OFFSET:.0f} m")
    print(f"  CMP spacing:        {CMP_INTERVAL:.2f} m")
    print(f"  Full fold (20 shots): {full_fold}")


if __name__ == "__main__":
    main()
