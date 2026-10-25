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

All ray paths are specular: on horizontal interfaces the reflection law
(angle in = angle out) means every bounce point is the horizontal midpoint
of its two neighbours. With source at 200 m and receiver at 1100 m the
bounce points come out at x = 425, 650, 875 m, so every path is
mirror-symmetric about the source-receiver midpoint at 650 m.
"""

import numpy as np
import matplotlib.pyplot as plt

SEABED_DEPTH, DEEP_DEPTH = 300.0, 1200.0  # m
X_SRC, X_REC = 200.0, 1100.0              # m


def specular_x(n_bounces, x_src=X_SRC, x_rec=X_REC):
    """Lateral positions of specular bounce points on horizontal interfaces.

    The reflection law (angle in = angle out) requires each bounce point to
    sit at the horizontal midpoint of its neighbours, with the source and
    receiver at the ends:  2*x_i = x_{i-1} + x_{i+1}.  That linear system is
    tridiagonal; for flat interfaces its solution is evenly spaced points
    (e.g. 200..1100 with 3 bounces -> 425, 650, 875).
    """
    A = np.zeros((n_bounces, n_bounces))
    b = np.zeros(n_bounces)
    for i in range(n_bounces):
        A[i, i] = 2.0
        if i > 0:
            A[i, i - 1] = -1.0
        else:
            b[i] = x_src
        if i < n_bounces - 1:
            A[i, i + 1] = -1.0
        else:
            b[i] = x_rec
    return np.linalg.solve(A, b)

fig, axes = plt.subplots(1, 4, figsize=(14, 6), sharex=True, sharey=True)

titles = [
    "Primary\n(one upward reflection)",
    "Water-bottom multiple\n(downward: surface)",
    "Peg-leg multiple\n(downward: surface)",
    "Internal multiple\n(downward: interbed)",
]

# Each path is a list of (x, z) vertices, plus indices of downward points.
# Every path has three specular bounces at the same lateral positions
# (425, 650, 875 m); only the reflecting interface at each bounce differs.
xb = specular_x(3)                     # -> (425, 650, 875) m

paths = []

# 1) Primary: one upward reflection at the deep reflector (midpoint of
#    source and receiver).
paths.append(([(X_SRC, 0), (xb[1], DEEP_DEPTH), (X_REC, 0)], []))

# 2) Water-bottom multiple: seabed up -> surface down -> seabed up.
#    Bounce 2 is the downward surface bounce.
paths.append(([(X_SRC, 0), (xb[0], SEABED_DEPTH), (xb[1], 0),
               (xb[2], SEABED_DEPTH), (X_REC, 0)], [2]))

# 3) Peg-leg: deep reflector up -> surface down -> seabed up.
paths.append(([(X_SRC, 0), (xb[0], DEEP_DEPTH), (xb[1], 0),
               (xb[2], SEABED_DEPTH), (X_REC, 0)], [2]))

# 4) Internal multiple: deep reflector up -> seabed DOWN -> deep reflector up.
paths.append(([(X_SRC, 0), (xb[0], DEEP_DEPTH), (xb[1], SEABED_DEPTH),
               (xb[2], DEEP_DEPTH), (X_REC, 0)], [2]))

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
    ax.plot(X_SRC, 0, "*", ms=16, color="darkorange", zorder=4)
    ax.plot(X_REC, 0, "v", ms=10, color="darkgreen", zorder=4)

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
