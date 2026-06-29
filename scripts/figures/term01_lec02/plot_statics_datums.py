"""
Statics datums and replacement velocity figure for Term 1 Lecture 02.

Draws a cross-section showing surface elevation, a low-velocity weathering
layer, an intermediate datum close to the base of weathering, and a final
reference datum.  Illustrates the vertical-ray assumption and the replacement
velocity used below the intermediate datum.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# ---------------------------------------------------------------------------
# Simple 2-D model
# ---------------------------------------------------------------------------
x = np.linspace(0.0, 4000.0, 200)

# Surface elevation (m)
elevation = 50.0 + 30.0 * np.sin(2.0 * np.pi * x / 4000.0)

# Base of weathering (m below surface)
base_weathering = elevation - 80.0 - 40.0 * np.sin(2.0 * np.pi * x / 2000.0)

# Datums
intermediate_datum = np.full_like(x, np.mean(base_weathering) - 20.0)
final_datum = np.full_like(x, 0.0)

# Velocities
v_weathering = 800.0   # m/s
v_replacement = 1800.0 # m/s

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 5))

# Fill regions
ax.fill_between(x, elevation, base_weathering, color="C0", alpha=0.3,
                label="Weathering layer ($v_w$ = %.0f m/s)" % v_weathering)
ax.fill_between(x, base_weathering, -200.0, color="C1", alpha=0.2,
                label="Replacement layer ($v_r$ = %.0f m/s)" % v_replacement)

# Boundaries
ax.plot(x, elevation, "k-", lw=1.5, label="Surface")
ax.plot(x, base_weathering, "k--", lw=1.5, label="Base of weathering")
ax.plot(x, intermediate_datum, "C2-", lw=2, label="Intermediate datum")
ax.plot(x, final_datum, "C3-", lw=2, label="Final datum")

# Vertical-ray schematic at two surface locations
for x0 in [800.0, 2800.0]:
    i = np.argmin(np.abs(x - x0))
    surf = elevation[i]
    bow = base_weathering[i]
    interm = intermediate_datum[i]
    final = final_datum[i]

    # Downward arrows: surface -> intermediate datum -> final datum
    ax.annotate("", xy=(x0, interm), xytext=(x0, surf),
                arrowprops=dict(arrowstyle="->", color="k", lw=1.5))
    ax.annotate("", xy=(x0, final), xytext=(x0, interm),
                arrowprops=dict(arrowstyle="->", color="k", lw=1.5))

    # Labels
    ax.text(x0 + 60.0, 0.5 * (surf + interm), "$t_w$", fontsize=10, color="k")
    ax.text(x0 + 60.0, 0.5 * (interm + final), "$t_r$", fontsize=10, color="k")

ax.set_xlim(x[0], x[-1])
ax.set_ylim(-120.0, 110.0)
ax.set_xlabel("Surface position (m)", fontsize=11)
ax.set_ylabel("Elevation (m)", fontsize=11)
ax.set_title("Field statics: datums, weathering layer and replacement velocity", fontsize=12)
ax.legend(loc="lower right", fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("figures/term01_lec02/term01_lec02_statics_datums.png", dpi=200, bbox_inches="tight")
print("Saved figures/term01_lec02/term01_lec02_statics_datums.png")
