#!/usr/bin/env python3
"""
Figure: 2D end-on acquisition geometry and fold build-up.

Top panel: a clean, aligned cartoon of one shot with its receiver spread,
source–receiver pairs, and the resulting midpoint (CMP) positions on the
survey line.  All key dimensions are labelled explicitly.

A small inset above the main spread shows how three consecutive shots roll
along the line, illustrating the shot interval.

Bottom panel: corresponding fold profile, showing the characteristic
ramp-up to full fold.

Parameters:
  Shot interval      = 25 m
  Receiver interval  = 12.5 m
  Receivers/shot     = 24
  Min offset         = 12.5 m
  Max offset         = 300 m
  CMP spacing        = 6.25 m
  Full fold          = 6

Pedagogical intention: give students a precise, readable diagram of end-on
acquisition geometry and show why CMP spacing is half the receiver spacing.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ---------------------------------------------------------------------------
# Acquisition parameters
# ---------------------------------------------------------------------------
DX_REC = 12.5
DX_SHOT = 25.0
N_REC = 24
X_MIN_OFFSET = 12.5
X_MAX_OFFSET = X_MIN_OFFSET + (N_REC - 1) * DX_REC
DX_CMP = DX_REC / 2

COLOR_SHOT = "#DD8452"


def shot_geometry(src_x):
    """Return receiver and midpoint x-positions for one shot."""
    offsets = X_MIN_OFFSET + np.arange(N_REC) * DX_REC
    rec_x = src_x + offsets
    mid_x = (src_x + rec_x) / 2.0
    return rec_x, mid_x


def compute_fold(n_shots=30):
    """Return (cmp_centers, fold) for n_shots fired at DX_SHOT spacing."""
    src_positions = np.arange(n_shots) * DX_SHOT
    midpoints = np.concatenate([shot_geometry(s)[1] for s in src_positions])

    x_min = midpoints.min() - DX_CMP / 2
    x_max = midpoints.max() + DX_CMP / 2
    edges = np.arange(x_min, x_max + DX_CMP, DX_CMP)
    centers = (edges[:-1] + edges[1:]) / 2
    fold, _ = np.histogram(midpoints, bins=edges)
    return centers, fold


def draw_bracket(ax, x0, x1, y, text, color="#333333", fontsize=8,
                 text_offset=0.25, va="top"):
    """Draw a horizontal dimension bracket with centered label."""
    tick_h = 0.10
    ax.plot([x0, x0], [y - tick_h, y + tick_h], color=color, lw=1.0)
    ax.plot([x1, x1], [y - tick_h, y + tick_h], color=color, lw=1.0)
    ax.plot([x0, x1], [y, y], color=color, lw=1.0)
    ax.annotate("", xy=(x0 + (x1 - x0) * 0.92, y),
                xytext=(x0 + (x1 - x0) * 0.08, y),
                arrowprops=dict(arrowstyle="<->", color=color, lw=1.0))
    y_text = y - text_offset if va == "top" else y + text_offset
    ax.text((x0 + x1) / 2, y_text, text, ha="center", va=va,
            fontsize=fontsize, color=color, fontweight="bold")


def main():
    src_x = 25.0
    rec_x, mid_x = shot_geometry(src_x)

    fig, (ax_geom, ax_fold) = plt.subplots(
        2, 1, figsize=(12, 7.5),
        gridspec_kw={"height_ratios": [2.0, 1.0], "hspace": 0.30}
    )

    # ------------------------------------------------------------------
    # Geometry panel
    # ------------------------------------------------------------------
    ax_geom.set_xlim(-20, 380)
    ax_geom.set_ylim(-1.5, 5.0)
    ax_geom.axis("off")

    # Survey line at bottom
    ax_geom.axhline(y=0, color="#888888", lw=1.5, xmin=0.01, xmax=0.97)
    ax_geom.text(370, -0.15, "Survey line", ha="right", va="top",
                 fontsize=8, color="#888888", style="italic")

    y_spread = 2.0          # main shot-receiver spread row
    y_cmp = 0.35            # CMP row

    # --- Main shot spread ------------------------------------------------
    ax_geom.plot(src_x, y_spread, marker="*", color=COLOR_SHOT, markersize=18,
                 markeredgecolor="white", markeredgewidth=0.8, zorder=5)

    ax_geom.scatter(rec_x, np.full_like(rec_x, y_spread), marker="v", s=45,
                    color=COLOR_SHOT, edgecolors="white", linewidths=0.4,
                    zorder=4)

    # Dotted source-receiver guidelines
    ax_geom.plot([src_x, rec_x[0]], [y_spread, y_spread], color=COLOR_SHOT,
                 lw=0.8, linestyle=":", zorder=2)
    ax_geom.plot([src_x, rec_x[-1]], [y_spread, y_spread], color=COLOR_SHOT,
                 lw=0.8, linestyle=":", zorder=2)

    ax_geom.text(rec_x[0], y_spread - 0.35, "R₁", ha="center", va="top",
                 fontsize=8, color=COLOR_SHOT)
    ax_geom.text(rec_x[-1], y_spread - 0.35, f"R_{N_REC}", ha="center",
                 va="top", fontsize=8, color=COLOR_SHOT)

    # Offset annotations (different y levels to avoid overlap)
    draw_bracket(ax_geom, src_x, rec_x[0], y_spread + 0.50,
                 f"Min offset = {X_MIN_OFFSET:.1f} m",
                 text_offset=0.22)
    draw_bracket(ax_geom, src_x, rec_x[-1], y_spread + 1.10,
                 f"Max offset = {X_MAX_OFFSET:.0f} m",
                 text_offset=0.22)

    # Receiver interval below the spread
    draw_bracket(ax_geom, rec_x[0], rec_x[1], y_spread - 0.55,
                 f"Δx_rec = {DX_REC:.1f} m",
                 text_offset=0.20)

    # --- CMP positions ---------------------------------------------------
    ax_geom.scatter(mid_x, np.full_like(mid_x, y_cmp), marker="o", s=30,
                    color=COLOR_SHOT, edgecolors="white", linewidths=0.3,
                    zorder=6)
    ax_geom.text(370, y_cmp, "CMP positions", ha="right", va="center",
                 fontsize=8, color="#888888", style="italic")

    # CMP spacing bracket
    draw_bracket(ax_geom, mid_x[0], mid_x[1], y_cmp - 0.50,
                 f"Δx_CMP = {DX_CMP:.2f} m = Δx_rec / 2",
                 text_offset=0.20)

    # --- Rolling spread inset (three small shots above) ------------------
    y_roll = 4.2
    roll_src = np.array([0.0, DX_SHOT, 2 * DX_SHOT])
    for i, sx in enumerate(roll_src):
        ax_geom.plot(sx, y_roll, marker="*", color=COLOR_SHOT, markersize=12,
                     markeredgecolor="white", markeredgewidth=0.5, zorder=5)
        ax_geom.text(sx, y_roll + 0.30, f"S{i+1}", ha="center", va="bottom",
                     fontsize=9, fontweight="bold", color=COLOR_SHOT)

    draw_bracket(ax_geom, roll_src[0], roll_src[1], y_roll - 0.45,
                 f"Δx_shot = {DX_SHOT:.0f} m",
                 text_offset=0.18)
    ax_geom.text(roll_src[-1] + 12, y_roll, "Rolling spread",
                 ha="left", va="center",
                 fontsize=9, color="#555555", style="italic")

    # Legend
    legend_elements = [
        plt.Line2D([0], [0], marker="*", color="w", markerfacecolor="#555555",
                   markersize=12, label="Source", markeredgecolor="white"),
        plt.Line2D([0], [0], marker="v", color="w", markerfacecolor="#555555",
                   markersize=9, label="Receiver", markeredgecolor="white"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#555555",
                   markersize=7, label="Midpoint (CMP)"),
    ]
    ax_geom.legend(handles=legend_elements, loc="upper left", fontsize=9,
                   framealpha=0.95, ncol=3)

    ax_geom.set_title("2D End-On Acquisition Geometry", fontsize=13,
                      fontweight="bold", pad=10)

    # ------------------------------------------------------------------
    # Fold profile panel
    # ------------------------------------------------------------------
    cmp_centers, fold = compute_fold(n_shots=30)
    full_fold = int(np.max(fold))

    mask = (cmp_centers >= -20) & (cmp_centers <= 380)
    cmp_centers = cmp_centers[mask]
    fold = fold[mask]

    ax_fold.bar(cmp_centers, fold, width=DX_CMP * 0.85, color="#3B6BA5",
                alpha=0.85, edgecolor="white", linewidth=0.3)
    ax_fold.axhline(full_fold, color="#C44E52", linestyle="--", lw=1.0)
    ax_fold.text(360, full_fold + 0.5, f"Full fold = {full_fold}",
                 ha="right", va="bottom", fontsize=9, color="#C44E52",
                 fontweight="bold")

    ax_fold.set_xlabel("Position along line (m)", fontsize=10)
    ax_fold.set_ylabel("Fold", fontsize=10)
    ax_fold.set_xlim(-20, 380)
    ax_fold.set_ylim(0, full_fold + 2)
    ax_fold.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax_fold.grid(axis="y", alpha=0.3, linestyle=":")
    ax_fold.set_title("Fold Profile", fontsize=11, fontweight="bold", pad=6)

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------
    out_dir = Path("figures/term01_lec01")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "term01_lec01_2d_acquisition_geometry.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {out_path}")
    print(f"  Full fold = {full_fold}")


if __name__ == "__main__":
    main()
