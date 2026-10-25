"""Figure: Raypath anatomy of multiples.

Four schematic ray paths side by side, all recorded at the same receiver:
  1) a primary from a deep reflector (one upward reflection),
  2) a water-bottom (free-surface) multiple: source -> bottom -> surface
     -> bottom -> receiver (one downward reflection at the sea surface),
  3) a peg-leg: source -> deep reflector -> surface -> bottom -> receiver
     (one downward reflection, two different upward reflectors),
  4) an internal (interbed) multiple: both extra reflections happen below
     the surface, inside the subsurface.

Downward reflection points are marked with a red circle: that marker is
the defining feature of a multiple. The caption reminds the student that
all four events arrive with the same wavelet in the same frequency band.
"""

import numpy as np
import matplotlib.pyplot as plt

WATER_V, H_WATER = 1480.0, 300.0          # m/s, m
SEABED_DEPTH, DEEP_DEPTH = 300.0, 1200.0  # m

fig, axes = plt.subplots(1, 4, figsize=(14, 6), sharex=True, sharey=True)

titles = [
    "Primary\n(one upward reflection)",
    "Water-bottom multiple\n(downward: surface)",
    "Peg-leg multiple\n(downward: surface)",
    "Internal multiple\n(downward: interbed)",
]

# Each path is a list of (x, z) vertices, plus indices of downward points.
paths = []

# 1) Primary: source at x=200, deep reflector at 1200 m, receiver at x=1100.
paths.append(([(200, 0), (650, DEEP_DEPTH), (1100, 0)], []))

# 2) Water-bottom multiple: down to seabed, up to surface, down to seabed,
#    up to receiver.
xb1 = 200 + (1100 - 200) / 3.0
paths.append(([(200, 0), (xb1, SEABED_DEPTH), (200 + 2 * (1100 - 200) / 3.0, 0),
               (1100 - (1100 - 200) / 3.0, SEABED_DEPTH), (1100, 0)], [2]))

# 3) Peg-leg: deep reflector -> surface -> seabed -> receiver.
xb2 = 200 + (1100 - 200) / 3.0
paths.append(([(200, 0), (200 + (1100 - 200) / 3.0, DEEP_DEPTH), (xb2, 0),
               (200 + 2 * (1100 - 200) / 3.0, SEABED_DEPTH), (1100, 0)], [2]))

# 4) Internal multiple: deep reflector -> seabed (downward!) -> deep
#    reflector -> receiver.
xi = 200 + (1100 - 200) / 3.0
paths.append(([(200, 0), (xi, DEEP_DEPTH), (200 + (1100 - 200) / 2.0, SEABED_DEPTH),
               (200 + 2 * (1100 - 200) / 3.0, DEEP_DEPTH), (1100, 0)], [2]))

for ax, title, (path, down_idx) in zip(axes, titles, paths):
    # Layer background
    ax.axhspan(0, SEABED_DEPTH, color="#cfe8ff", alpha=0.8, zorder=0)
    ax.axhspan(SEABED_DEPTH, 1400, color="#d9c9a8", alpha=0.9, zorder=0)

    # Interfaces
    ax.axhline(0, color="k", lw=2)
    ax.axhline(SEABED_DEPTH, color="saddlebrown", lw=2)
    ax.axhline(DEEP_DEPTH, color="dimgray", lw=2)

    # Ray path
    px, pz = zip(*path)
    ax.plot(px, pz, "-", color="crimson", lw=2.2, zorder=3)

    # Downward-reflection markers
    for i in down_idx:
        ax.plot(path[i][0], path[i][1], "o", ms=13, mfc="none", mec="crimson",
                mew=2.5, zorder=4)

    # Source and receiver
    ax.plot(200, 0, "*", ms=16, color="darkorange", zorder=4)
    ax.plot(1100, 0, "v", ms=10, color="darkgreen", zorder=4)

    ax.set_title(title, fontsize=11)
    ax.set_xlim(100, 1200)
    ax.set_ylim(1400, -60)          # depth axis pointing down
    ax.set_xlabel("Lateral position (m)")

axes[0].set_ylabel("Depth (m)")
fig.suptitle("Anatomy of multiples: red circles mark the downward reflection(s)",
             fontsize=13)
fig.text(0.5, 0.015,
         "A primary has exactly one upward reflection. A multiple has at least one "
         "extra downward reflection —\nat the free surface (multiple 2, 3) or "
         "inside the subsurface (multiple 4). All events share the same wavelet.",
         ha="center", fontsize=10, color="0.25")
fig.tight_layout(rect=(0, 0.05, 1, 0.95))
fig.savefig("figures/term02_lec03/term02_lec03_multiple_raypaths.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec03_multiple_raypaths.png")
