#!/usr/bin/env python3
"""
Figure: Acquisition and propagation effects — distortions added to the clean
geological signal.

Left panel: clean subsurface model with source, horizontal reflector, and
ray paths (primary reflections) recorded at surface receivers.
Right panel: eight distortion phenomena illustrated with simple cartoons —
source/receiver ghosts, array response, geometric spreading, absorption,
multiples, refractions, surface waves, and random noise.

Output: figures/term01_lec01/term01_lec01_distortions_overview.png
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path


# ──────────────────────────────────────────────────────────────────────
# Helper: draw the left panel — clean subsurface ray paths
# ──────────────────────────────────────────────────────────────────────
def draw_clean_subsurface(ax):
    """Draw source–reflector–receiver ray paths in a simple subsurface model."""
    # Normalised axes coordinates: [0,1] x [0,1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")

    # Colours
    surf_color = "#8B4513"  # brown
    refl_color = "#666666"  # dark grey
    ray_color = "#2c7bb6"   # blue
    src_color = "#d7191c"   # red
    rcv_color = "#1a9641"   # green

    # Geometry
    surface_y = 0.88
    reflector_y = 0.25
    src_x = 0.12
    rcv_xs = np.array([0.35, 0.48, 0.61, 0.74, 0.87])
    n_rcv = len(rcv_xs)

    # --- Surface line ---
    ax.axhline(y=surface_y, xmin=0.0, xmax=0.98, color=surf_color,
               linewidth=2.5, zorder=2)
    ax.text(0.88, surface_y + 0.02, "Surface", fontsize=8,
            color=surf_color, ha="left", va="bottom", style="italic")

    # --- Reflector ---
    ax.axhline(y=reflector_y, xmin=0.02, xmax=0.96, color=refl_color,
               linewidth=1.8, linestyle="--", zorder=2)
    ax.text(0.88, reflector_y - 0.02, "Reflector", fontsize=8,
            color=refl_color, ha="left", va="top", style="italic")

    # --- Source (star) ---
    ax.plot(src_x, surface_y, marker="*", color=src_color,
            markersize=16, zorder=10)
    ax.text(src_x, surface_y - 0.04, "Source", fontsize=8,
            color=src_color, ha="center", va="top", fontweight="bold")

    # --- Receivers (triangles) ---
    ax.scatter(rcv_xs, np.full(n_rcv, surface_y), marker="v",
               color=rcv_color, s=80, zorder=10)
    ax.text(0.60, surface_y + 0.06, "Receivers", fontsize=8,
            color=rcv_color, ha="center", va="bottom", fontweight="bold")

    # --- Reflection points on the reflector ---
    ref_xs = (src_x + rcv_xs) / 2.0
    ax.scatter(ref_xs, np.full(n_rcv, reflector_y), marker="o",
               color="orange", s=25, zorder=8, edgecolors="none")

    # --- Ray paths (source → reflector → receiver) ---
    for rx, rfx in zip(rcv_xs, ref_xs):
        # Source to reflection point
        ax.plot([src_x, rfx], [surface_y, reflector_y],
                color=ray_color, linewidth=1.2, alpha=0.7, zorder=3)
        # Reflection point to receiver
        ax.plot([rfx, rx], [reflector_y, surface_y],
                color=ray_color, linewidth=1.2, alpha=0.7, zorder=3)

    # --- Arrow heads on one representative ray path ---
    mid_idx = n_rcv // 2
    rfx_mid = ref_xs[mid_idx]
    rx_mid = rcv_xs[mid_idx]

    # Arrow from source toward reflector
    dx = rfx_mid - src_x
    dy = reflector_y - surface_y
    ax.arrow(src_x + 0.20 * dx, surface_y + 0.20 * dy,
             0.12 * dx, 0.12 * dy,
             head_width=0.02, head_length=0.02, fc=ray_color, ec=ray_color,
             linewidth=0.8, zorder=4)

    # Arrow from reflector toward receiver
    dx = rx_mid - rfx_mid
    dy = surface_y - reflector_y
    ax.arrow(rfx_mid + 0.20 * dx, reflector_y + 0.20 * dy,
             0.12 * dx, 0.12 * dy,
             head_width=0.02, head_length=0.02, fc=ray_color, ec=ray_color,
             linewidth=0.8, zorder=4)

    # --- Annotation box ---
    ax.text(0.5, 0.02, "Clean geological signal\n(primary reflections)",
            fontsize=9, ha="center", va="bottom",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#e0f3f8",
                      edgecolor=ray_color, linewidth=1.2),
            transform=ax.transData, zorder=20)


# ──────────────────────────────────────────────────────────────────────
# Helpers for the distortion icons (each draws inside a [0,1]x[0,1] axes)
# ──────────────────────────────────────────────────────────────────────
def draw_ghost(ax):
    """Source and receiver ghosts — extra arrivals from surface reflection."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Ghost", fontsize=8, pad=2)

    # Free surface at top
    ax.axhline(y=0.90, color="brown", linewidth=2)
    # Reflector at bottom
    ax.axhline(y=0.15, color="grey", linewidth=1.2, linestyle="--")

    # Source
    sx, sy = 0.25, 0.90
    ax.plot(sx, sy, marker="*", color="red", markersize=10, zorder=5)
    # Receiver
    rx, ry = 0.75, 0.90
    ax.plot(rx, ry, marker="v", color="green", markersize=8, zorder=5)

    # Primary ray: source → reflector → receiver
    ref_px = (sx + rx) / 2
    ax.plot([sx, ref_px, rx], [sy, 0.15, ry],
            color="blue", linewidth=1.2, label="Primary")

    # Ghost path: source → surface up → surface reflection point → reflector → receiver
    # Ghost goes up from source to a point on the surface, then reflects, then down to
    # a reflection point, then to receiver
    # Simpler: draw dashed line from source up to surface and back to reflector
    ghost_surf_x = sx - 0.08  # to the left of source
    ghost_ref_x = (ghost_surf_x + rx) / 2
    ax.plot([sx, ghost_surf_x, ghost_ref_x, rx],
            [sy, 1.0, 0.15, ry],
            color="red", linewidth=1.0, linestyle="--", label="Ghost")

    # Labels
    ax.text(0.5, 0.50, "Ghost paths", fontsize=6, ha="center",
            color="red", style="italic",
            bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.7))


def draw_array_response(ax):
    """Array response — receiver group directivity."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Array response", fontsize=8, pad=2)

    # Row of receivers
    rcv_x = np.linspace(0.15, 0.85, 5)
    rcv_y = 0.80
    ax.scatter(rcv_x, np.full_like(rcv_x, rcv_y), marker="v",
               color="green", s=30, zorder=5)

    # Incoming plane wave (from below)
    for offset in [-0.10, 0.0, 0.10]:
        wave_x = np.linspace(0.0, 1.0, 100)
        wave_y = 0.40 + offset + 0.06 * np.sin(2 * np.pi * 2 * wave_x)
        ax.plot(wave_x, wave_y, color="purple", linewidth=0.8, alpha=0.6)

    ax.annotate("", xy=(0.50, 0.05), xytext=(0.50, 0.30),
                arrowprops=dict(arrowstyle="->", color="purple", lw=1.5))
    ax.text(0.50, 0.03, "Wavefront", fontsize=6, ha="center",
            color="purple", style="italic")

    # Summation symbol
    ax.text(0.50, 0.55, "Σ", fontsize=16, ha="center", va="center",
            color="darkblue", fontweight="bold")

    # Directional pattern sketch (polar-like lobe)
    theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
    r_lobe = 0.15 * np.abs(np.sinc(3 * (theta) / np.pi))
    lobe_x = 0.50 + r_lobe * np.sin(theta)
    lobe_y = 0.80 - 0.15 + r_lobe * np.cos(theta)
    ax.plot(lobe_x, lobe_y, color="darkblue", linewidth=1.2)

    ax.text(0.50, 0.96, "Receiver group", fontsize=6, ha="center", va="top",
            color="green", style="italic")


def draw_spreading(ax):
    """Geometric spreading — spherical divergence."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Geometric\nspreading", fontsize=8, pad=2)

    # Source point
    sx, sy = 0.50, 0.50
    ax.plot(sx, sy, marker="*", color="red", markersize=10, zorder=5)

    # Concentric wavefronts (quarter circles upward)
    for i, r in enumerate([0.12, 0.25, 0.38, 0.50]):
        theta = np.linspace(-np.pi, 0, 100)
        arc_x = sx + r * np.cos(theta)
        arc_y = sy + r * np.sin(theta)
        # Clip to axes
        mask = (arc_x >= 0) & (arc_x <= 1) & (arc_y >= 0) & (arc_y <= 1)
        ax.plot(arc_x[mask], arc_y[mask], color="purple",
                linewidth=1.5 - 0.2 * i, alpha=0.8 - 0.15 * i, zorder=2)

    # Arrow showing amplitude decrease
    ax.annotate("", xy=(0.70, 0.12), xytext=(0.30, 0.12),
                arrowprops=dict(arrowstyle="->", color="grey", lw=1.0))
    ax.text(0.50, 0.08, "Amplitude ∝ 1/r", fontsize=6,
            ha="center", va="bottom", color="grey", style="italic")


def draw_absorption(ax):
    """Absorption (Q) — amplitude decay and frequency loss."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Absorption\n(Q)", fontsize=8, pad=2)

    # Wavelets at three positions showing decay and broadening
    t = np.linspace(0, 1, 200)
    centers = [0.25, 0.50, 0.75]
    amps = [1.0, 0.5, 0.2]
    freqs = [12, 8, 5]  # decreasing frequency content

    for cx, amp, freq in zip(centers, amps, freqs):
        # Gaussian envelope * sinusoid
        env = amp * np.exp(-20 * (t - cx) ** 2)
        wave = env * np.sin(2 * np.pi * freq * (t - cx))
        ax.plot(t, wave * 0.25 + 0.50, color="darkred", linewidth=1.2)

    # Arrow along path
    ax.annotate("", xy=(0.88, 0.50), xytext=(0.10, 0.50),
                arrowprops=dict(arrowstyle="->", color="grey", lw=0.8))
    ax.text(0.50, 0.95, "Propagation distance →", fontsize=6,
            ha="center", va="center", color="grey", style="italic")


def draw_multiples(ax):
    """Multiples — reverberations between interfaces."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Multiples", fontsize=8, pad=2)

    # Two reflectors
    ax.axhline(y=0.75, color="brown", linewidth=2)  # surface
    ax.axhline(y=0.50, color="grey", linewidth=1.2, linestyle="--")  # shallow reflector
    ax.axhline(y=0.15, color="grey", linewidth=1.2, linestyle="--")  # deep reflector

    # Source and receiver at surface
    sx, rx = 0.20, 0.80
    ax.plot(sx, 0.75, marker="*", color="red", markersize=8, zorder=5)
    ax.plot(rx, 0.75, marker="v", color="green", markersize=7, zorder=5)

    # Primary: source → deep → receiver
    ref_px = (sx + rx) / 2
    ax.plot([sx, ref_px, rx], [0.75, 0.15, 0.75],
            color="blue", linewidth=1.0, alpha=0.5)

    # Multiple: source → shallow → deep → shallow → receiver (peg-leg)
    # path: source → (shallow) → deep → (shallow) → receiver
    m1_x = (sx + ref_px) / 2
    m2_x = (ref_px + rx) / 2
    ax.plot([sx, m1_x, ref_px, m2_x, rx],
            [0.75, 0.50, 0.15, 0.50, 0.75],
            color="red", linewidth=1.2, linestyle="--")

    # Bounce point indicators
    ax.scatter(m1_x, 0.50, marker="o", s=15, color="red", zorder=6, edgecolors="none")
    ax.scatter(m2_x, 0.50, marker="o", s=15, color="red", zorder=6, edgecolors="none")

    ax.text(0.50, 0.88, "Peg-leg multiple", fontsize=6, ha="center",
            color="red", style="italic",
            bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.7))


def draw_refractions(ax):
    """Refractions (head waves) — energy travelling along interfaces."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Refractions", fontsize=8, pad=2)

    # Interface
    ax.axhline(y=0.40, color="grey", linewidth=1.5, linestyle="--")
    ax.text(0.90, 0.38, "v₁ < v₂", fontsize=6, ha="left", color="grey", style="italic")

    # Source
    sx = 0.15
    ax.plot(sx, 0.90, marker="*", color="red", markersize=8, zorder=5)

    # Incident ray at critical angle to interface
    cx1, cy1 = 0.20, 0.90
    cx2, cy2 = 0.50, 0.40
    # Along interface
    cx3, cy3 = 0.80, 0.40
    # Back up to receiver
    rx, ry = 0.88, 0.90

    ax.plot([sx, cx2], [0.90, cy2], color="orange", linewidth=1.3)
    ax.plot([cx2, cx3], [cy2, cy3], color="orange", linewidth=1.3)
    ax.plot([cx3, rx], [cy3, ry], color="orange", linewidth=1.3)

    # Critical angle indicator
    theta = np.linspace(0, 0.45, 30)  # approximate critical angle arc
    arc_x = cx2 + 0.06 * np.cos(theta)
    arc_y = cy2 + 0.06 * np.sin(theta)
    ax.plot(arc_x, arc_y, color="darkgreen", linewidth=0.8)
    ax.text(cx2 + 0.08, cy2 + 0.05, "θc", fontsize=7, color="darkgreen")

    # Head wave label
    ax.text(0.50, 0.18, "Head wave\n(refracted)", fontsize=6, ha="center",
            color="orange", style="italic",
            bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.7))

    # Velocity labels
    ax.text(0.05, 0.65, "v₁", fontsize=7, color="blue", style="italic")
    ax.text(0.05, 0.20, "v₂", fontsize=7, color="red", style="italic")

    # Receiver
    ax.plot(rx, ry, marker="v", color="green", markersize=7, zorder=5)


def draw_surface_waves(ax):
    """Surface waves — ground roll."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Surface waves\n(ground roll)", fontsize=8, pad=2)

    # Free surface
    ax.axhline(y=0.80, color="brown", linewidth=2)

    # Rayleigh-wave elliptical motion (particle displacement)
    t = np.linspace(0, 2 * np.pi, 50)
    for cx in np.linspace(0.15, 0.85, 7):
        # Vertical amplitude decreases with depth
        for depth_frac, amp_scale in [(0.0, 1.0), (0.15, 0.6), (0.30, 0.3)]:
            path_y = 0.80 - depth_frac
            # Retrograde ellipse: horizontal and vertical components
            rx_e = 0.02 * amp_scale
            ry_e = 0.025 * amp_scale
            ellipse_x = cx + rx_e * np.cos(t)
            ellipse_y = path_y + ry_e * np.sin(t)
            ax.plot(ellipse_x, ellipse_y, color="darkgreen", linewidth=0.5,
                    alpha=0.4 + 0.3 * (1 - depth_frac / 0.3))

    # Wavy surface disturbance
    x_surf = np.linspace(0, 1, 200)
    y_surf = 0.80 + 0.015 * np.sin(2 * np.pi * 3 * x_surf)
    ax.plot(x_surf, y_surf, color="darkgreen", linewidth=1.0, alpha=0.7)

    # Propagation arrow
    ax.annotate("", xy=(0.88, 0.60), xytext=(0.12, 0.60),
                arrowprops=dict(arrowstyle="->", color="darkgreen", lw=1.0))
    ax.text(0.50, 0.55, "Propagation", fontsize=6, ha="center",
            color="darkgreen", style="italic",
            bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.7))

    # Amplitude decay with depth
    ax.text(0.90, 0.15, "Amp ↓\nwith depth", fontsize=6, ha="center",
            color="grey", style="italic")


def draw_noise(ax):
    """Random noise — incoherent energy."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Random noise", fontsize=8, pad=2)

    np.random.seed(42)
    x = np.linspace(0, 1, 400)
    y = 0.50 + 0.30 * np.cumsum(np.random.randn(400) * 0.02)
    # Detrend
    y = 0.50 + 0.30 * (y - np.mean(y)) / np.std(y)
    ax.plot(x, y, color="grey", linewidth=0.8, alpha=0.8)

    # Fill below to emphasize noise floor
    ax.fill_between(x, 0.50, y, color="grey", alpha=0.15)

    ax.text(0.50, 0.90, "Incoherent\nbackground noise", fontsize=6, ha="center",
            color="grey", style="italic",
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8))


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────
def main():
    # Build figure with left panel + 4x2 grid for right panel
    fig = plt.figure(figsize=(12, 7))

    # Overall figure title
    fig.suptitle("Distortions added to the geological signal",
                 fontsize=14, fontweight="bold", y=0.98)

    # Grid: left column (subsurface) and right block (4 rows × 2 cols of icons)
    gs = fig.add_gridspec(1, 2, width_ratios=[0.38, 0.62],
                           left=0.04, right=0.97, top=0.90, bottom=0.05,
                           wspace=0.08)

    ax_left = fig.add_subplot(gs[0])
    draw_clean_subsurface(ax_left)

    # Sub-grid for the 8 distortion icons
    gs_right = gs[1].subgridspec(4, 2, hspace=0.45, wspace=0.08)

    distortion_panels = [
        (0, 0, draw_ghost),
        (0, 1, draw_array_response),
        (1, 0, draw_spreading),
        (1, 1, draw_absorption),
        (2, 0, draw_multiples),
        (2, 1, draw_refractions),
        (3, 0, draw_surface_waves),
        (3, 1, draw_noise),
    ]

    for row, col, draw_func in distortion_panels:
        ax = fig.add_subplot(gs_right[row, col])
        draw_func(ax)

    # Save
    out = Path("figures/term01_lec01/term01_lec01_distortions_overview.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
