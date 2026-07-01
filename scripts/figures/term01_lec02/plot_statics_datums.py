"""
Statics datums and replacement velocity figure for Term 1 Lecture 02.

Draws a cross-section showing surface elevation, a low-velocity weathering
layer, an intermediate datum close to the base of weathering, and a final
reference datum placed above the highest surface elevation. The arrows show the
direction of the static shift applied to the data: first down from the surface
to the intermediate datum, then up from the intermediate datum to the final datum.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Simple 2-D model
# ---------------------------------------------------------------------------
x = np.linspace(0.0, 4000.0, 200)

# Surface elevation (m)
elevation = 50.0 + 30.0 * np.sin(2.0 * np.pi * x / 4000.0)
max_elevation = np.max(elevation)

# Base of weathering (m below surface)
base_weathering = elevation - 80.0 - 40.0 * np.sin(2.0 * np.pi * x / 2000.0)

# Datums
intermediate_datum = np.full_like(x, np.mean(base_weathering) - 20.0)
# Final datum is placed above the highest surface elevation so that the total
# shift to the final datum has the desired sign after the intermediate datum.
final_datum = np.full_like(x, max_elevation + 30.0)

# Velocities
v_weathering = 800.0   # m/s
v_replacement = 1800.0 # m/s

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 5))

# Fill regions
ax.fill_between(x, elevation, base_weathering, color="C0", alpha=0.3,
                label=f"Weathering layer ($v_w$ = {v_weathering:.0f} m/s)")
ax.fill_between(x, base_weathering, -200.0, color="C1", alpha=0.2,
                label=f"Replacement layer ($v_r$ = {v_replacement:.0f} m/s)")

# Boundaries
ax.plot(x, elevation, "k-", lw=1.5, label="Surface")
ax.plot(x, base_weathering, "k--", lw=1.5, label="Base of weathering")
ax.plot(x, intermediate_datum, "C2-", lw=2, label="Intermediate datum")
ax.plot(x, final_datum, "C3-", lw=2, label="Final datum")

# Vertical-ray schematic at two surface locations
for x0 in [800.0, 2800.0]:
    # Offset the two arrows horizontally so they do not overlap.
    # The down arrow is drawn slightly to the left, the up arrow slightly to the right.
    x_down = x0 - 60.0
    x_up = x0 + 60.0

    i_down = np.argmin(np.abs(x - x_down))
    i_up = np.argmin(np.abs(x - x_up))

    surf_down = elevation[i_down]
    interm_down = intermediate_datum[i_down]
    surf_up = elevation[i_up]
    interm_up = intermediate_datum[i_up]
    final_up = final_datum[i_up]

    # Arrow 1: surface -> intermediate datum (downward data shift)
    ax.annotate("", xy=(x_down, interm_down), xytext=(x_down, surf_down),
                arrowprops=dict(arrowstyle="->", color="C2", lw=2.0))
    # Arrow 2: intermediate datum -> final datum (upward data shift)
    ax.annotate("", xy=(x_up, final_up), xytext=(x_up, interm_up),
                arrowprops=dict(arrowstyle="->", color="C3", lw=2.0))

    # Labels for the two shift components, placed on opposite sides of the arrows
    ax.text(x_down - 90.0, 0.5 * (surf_down + interm_down), "down", fontsize=9, color="C2",
            fontweight="bold", ha="right", va="center")
    ax.text(x_up + 90.0, 0.5 * (interm_up + final_up), "up", fontsize=9, color="C3",
            fontweight="bold", ha="left", va="center")

ax.set_xlim(x[0], x[-1])
ax.set_ylim(np.min(base_weathering) - 30.0, max_elevation + 50.0)
ax.set_xlabel("Surface position (m)", fontsize=11)
ax.set_ylabel("Elevation (m)", fontsize=11)
ax.set_title("Field statics: datums, weathering layer and replacement velocity", fontsize=12)
ax.legend(loc="lower right", fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("figures/term01_lec02/term01_lec02_statics_datums.png", dpi=200, bbox_inches="tight")
print("Saved figures/term01_lec02/term01_lec02_statics_datums.png")
