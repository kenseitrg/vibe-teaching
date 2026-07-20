"""
Schematic FK plane showing signal/noise overlap.

Single-panel diagram illustrating why FK fan filters cannot perfectly
separate ground roll from reflections.  All fans emanate from the
origin (k = 0, f = 0) because linear events through the origin in
t-x map to lines through the origin in FK (k = f / v_app).

- Blue fan: reflection energy (|k| <= f/500).  The fan opens wide
  because steep dips and far-offset hyperbola flanks have LOW
  apparent velocity.
- Orange cone: ground roll (f/900 <= |k| <= f/350), broadened by
  dispersion.
- Red wedges: the overlap, where no dip filter can separate them.
- Rose dashed line: a fan-filter cut (700 m/s) with its two failure
  modes - hatched "signal lost" region and "noise leaks through".
- Grey speckle: random noise filling the entire plane.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D

# ════════════════════════════════════════════════════════════════════
# Figure settings
# ════════════════════════════════════════════════════════════════════
FIG_WIDTH = 11.0
FIG_HEIGHT = 6.5
DPI = 150
OUTPUT_PATH = "figures/term03_lec04/term03_lec04_fk_overlap.png"

# Okabe–Ito palette
COL_SIGNAL   = "#0072B2"   # blue
COL_NOISE    = "#D55E00"   # vermillion
COL_OVERLAP  = "#CC3311"   # red (overlap)
COL_FILTER   = "#CC79A7"   # rose (fan filter)
COL_RANDOM   = "#999999"   # grey (random noise)
COL_BG       = "#F5F5F5"   # light background

# Axes limits
K_MAX = 100.0          # cycles/km
F_MAX = 50.0           # Hz (0 at bottom)

# Velocities defining the fans (apparent velocity, m/s)
V_SIG_EDGE = 500.0     # steepest reflection dip (lowest apparent v)
V_GR_FAST  = 900.0     # fastest ground roll (inner cone edge)
V_GR_SLOW  = 350.0     # slowest ground roll (outer cone edge)
V_FAN      = 700.0     # fan-filter cut

# Frequency extents of the energy bands
F_SIG_HI = 50.0        # reflections extend to top of plot
F_GR_HI  = 35.0        # ground roll dies out above 35 Hz
F_OVL_HI = 35.0        # overlap exists where both bands exist

# Random noise speckle
N_SPECKLE = 400
SPECKLE_SEED = 42


# ════════════════════════════════════════════════════════════════════
# Geometry helpers
# ════════════════════════════════════════════════════════════════════

def f_to_k(f, v_app):
    """Wavenumber in cycles/km given frequency (Hz) and apparent velocity (m/s)."""
    return f / v_app * 1000.0


def fan_polygon(v_edge, f_max, f_min=0.0):
    """Symmetric fan around the f-axis: |k| <= f / v_edge.

    Emanates from the origin when f_min = 0.
    """
    return np.array([
        [-f_to_k(f_min, v_edge), f_min],
        [-f_to_k(f_max, v_edge), f_max],
        [ f_to_k(f_max, v_edge), f_max],
        [ f_to_k(f_min, v_edge), f_min],
    ])


def cone_polygons(v_fast, v_slow, f_max, f_min=0.0):
    """Two mirrored cone bands: f/v_fast <= |k| <= f/v_slow.

    Returns [right_band, left_band].  v_fast gives the inner edge
    (smaller |k|), v_slow the outer edge (larger |k|).
    """
    right = np.array([
        [f_to_k(f_min, v_fast), f_min],
        [f_to_k(f_max, v_fast), f_max],
        [f_to_k(f_max, v_slow), f_max],
        [f_to_k(f_min, v_slow), f_min],
    ])
    left = right * [-1.0, 1.0]
    return [right, left]


# ════════════════════════════════════════════════════════════════════
# Plotting
# ════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
ax.set_xlim(-K_MAX, K_MAX)
ax.set_ylim(0, F_MAX)
ax.set_xlabel("Wavenumber (cycles/km)", fontsize=11)
ax.set_ylabel("Frequency (Hz)", fontsize=11)
ax.set_title("Signal and noise overlap in FK domain",
             fontsize=13, fontweight="bold", pad=12)
ax.set_facecolor(COL_BG)

# ── Random noise speckle ────────────────────────────────────────────
rng = np.random.RandomState(SPECKLE_SEED)
ax.scatter(rng.uniform(-K_MAX, K_MAX, N_SPECKLE),
           rng.uniform(0, F_MAX, N_SPECKLE),
           s=1.5, color=COL_RANDOM, alpha=0.4, zorder=1)

# ── Signal fan (blue), apex at origin ───────────────────────────────
ax.add_patch(Polygon(fan_polygon(V_SIG_EDGE, F_SIG_HI),
                     closed=True, facecolor=COL_SIGNAL, alpha=0.20,
                     edgecolor=COL_SIGNAL, linewidth=1.5, zorder=2))

ax.text(48, 43, "reflections",
        fontsize=10, color=COL_SIGNAL, fontweight="bold",
        ha="center", va="center", zorder=6)
ax.annotate(
    "steep dips & far offsets\n→ low apparent velocity",
    xy=(f_to_k(40, V_SIG_EDGE), 40),
    xytext=(30, 27),
    fontsize=8, color=COL_SIGNAL, ha="left", va="center",
    arrowprops=dict(arrowstyle="->", color=COL_SIGNAL, lw=0.9),
    zorder=6,
)

# ── Ground roll cone (orange), two mirrored bands from origin ──────
for poly in cone_polygons(V_GR_FAST, V_GR_SLOW, F_GR_HI):
    ax.add_patch(Polygon(poly, closed=True, facecolor=COL_NOISE,
                         alpha=0.20, edgecolor=COL_NOISE,
                         linewidth=1.5, zorder=2))

ax.text(-46, 16, "ground roll",
        fontsize=10, color=COL_NOISE, fontweight="bold",
        ha="center", va="center", zorder=6)
ax.annotate(
    "broad cone\n(dispersion)",
    xy=(-f_to_k(28, V_GR_SLOW), 28),
    xytext=(-45, 38),
    fontsize=8, color=COL_NOISE, ha="center", va="center",
    arrowprops=dict(arrowstyle="->", color=COL_NOISE, lw=0.9),
    zorder=6,
)

# ── Overlap wedges (red): f/900 <= |k| <= f/500, f = 0..35 ─────────
for poly in cone_polygons(V_GR_FAST, V_SIG_EDGE, F_OVL_HI):
    ax.add_patch(Polygon(poly, closed=True, facecolor=COL_OVERLAP,
                         alpha=0.40, edgecolor=COL_OVERLAP,
                         linewidth=1.2, zorder=3))

ax.annotate(
    "overlap:\ninseparable",
    xy=(f_to_k(18, 650), 18),
    xytext=(52, 12),
    fontsize=9, color=COL_OVERLAP, fontweight="bold",
    ha="left", va="center",
    arrowprops=dict(arrowstyle="->", color=COL_OVERLAP, lw=1.2),
    zorder=6,
)

# ── Fan filter cut lines (rose dashed) ──────────────────────────────
f_line = np.linspace(0, F_MAX, 200)
k_fan = f_to_k(f_line, V_FAN)
ax.plot( k_fan, f_line, "--", color=COL_FILTER, linewidth=2.0, zorder=5)
ax.plot(-k_fan, f_line, "--", color=COL_FILTER, linewidth=2.0, zorder=5)

ax.annotate(
    "fan filter cut\n(v = 700 m/s)",
    xy=(f_to_k(15, V_FAN), 15),
    xytext=(55, 6),
    fontsize=8, color=COL_FILTER, fontweight="bold",
    ha="left", va="center",
    arrowprops=dict(arrowstyle="->", color=COL_FILTER, lw=1.0),
    zorder=6,
)

# ── "Signal lost" hatch: between cut and signal edge, above GR band ─
# Region f/700 <= |k| <= f/500 for f = 35..50 Hz (pure signal zone)
for poly in cone_polygons(V_FAN, V_SIG_EDGE, F_SIG_HI, f_min=F_GR_HI):
    ax.add_patch(Polygon(poly, closed=True, facecolor="none",
                         edgecolor=COL_SIGNAL, linewidth=0,
                         hatch="///", alpha=0.7, zorder=4))

ax.annotate(
    "signal energy\nlost",
    xy=(f_to_k(42, 600), 42),
    xytext=(12, 46),
    fontsize=8, color=COL_SIGNAL, fontweight="bold",
    arrowprops=dict(arrowstyle="->", color=COL_SIGNAL, lw=1.2),
    ha="left", va="center", zorder=6,
)

# ── "Noise leaks through": fast GR energy inside the pass zone ─────
# Region f/900 <= |k| <= f/700 (passes the cut) — left side arrow
ax.annotate(
    "noise leaks\nthrough",
    xy=(-f_to_k(25, 800), 25),
    xytext=(-70, 30),
    fontsize=8, color=COL_NOISE, fontweight="bold",
    arrowprops=dict(arrowstyle="->", color=COL_NOISE, lw=1.2),
    ha="center", va="center", zorder=6,
)

# ── Random noise label ──────────────────────────────────────────────
ax.text(-45, 45.5, "random noise fills entire plane",
        fontsize=8, color="#666666", fontstyle="italic",
        ha="center", va="center", zorder=6)

# ── Top axis: apparent velocity scale ───────────────────────────────
velocities = [500, 700, 900, 1500, 3000]
ax_top = ax.secondary_xaxis("top")
ax_top.set_xlim(-K_MAX, K_MAX)
ax_top.set_xticks([f_to_k(F_MAX, v) for v in velocities])
ax_top.set_xticklabels([f"{v}" for v in velocities], fontsize=8)
ax_top.set_xlabel("Apparent velocity (m/s)", fontsize=9)

# ── Axes cross at origin ────────────────────────────────────────────
ax.axvline(0, color="k", linewidth=0.4, alpha=0.5, zorder=1)
ax.axhline(0, color="k", linewidth=0.4, alpha=0.5, zorder=1)

# ── Legend ──────────────────────────────────────────────────────────
legend_handles = [
    Line2D([0], [0], marker="s", color="w", markerfacecolor=COL_SIGNAL,
           markersize=10, alpha=0.5, label="reflections"),
    Line2D([0], [0], marker="s", color="w", markerfacecolor=COL_NOISE,
           markersize=10, alpha=0.5, label="ground roll"),
    Line2D([0], [0], marker="s", color="w", markerfacecolor=COL_OVERLAP,
           markersize=10, alpha=0.6, label="overlap (inseparable)"),
    Line2D([0], [0], color=COL_FILTER, linestyle="--", linewidth=2,
           label="fan filter"),
]
ax.legend(handles=legend_handles, loc="lower left", fontsize=8.5,
          framealpha=0.9, edgecolor="#cccccc")

plt.savefig(OUTPUT_PATH, dpi=DPI, bbox_inches="tight")
plt.close()

print(f"Saved figure to {OUTPUT_PATH}")
print(f"Axes: k = ±{K_MAX:.0f} cycles/km, f = 0–{F_MAX:.0f} Hz (0 at bottom)")
print(f"Signal fan:  |k| <= f/{V_SIG_EDGE:.0f}, f = 0–{F_SIG_HI:.0f} Hz")
print(f"Ground roll: f/{V_GR_FAST:.0f} <= |k| <= f/{V_GR_SLOW:.0f}, f = 0–{F_GR_HI:.0f} Hz")
print(f"Overlap:     f/{V_GR_FAST:.0f} <= |k| <= f/{V_SIG_EDGE:.0f}, f = 0–{F_OVL_HI:.0f} Hz")
print(f"Fan filter cut: v = {V_FAN:.0f} m/s")
