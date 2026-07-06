"""
Refraction geometry and delay-time figure for Term 1 Lecture 03.

Draws a two-layer refraction model with a low-velocity weathering layer over a
higher-velocity half-space. Shows direct, critically refracted and reflected
ray paths, and marks the crossover offset and the delay time at a receiver.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Two-layer model
# ---------------------------------------------------------------------------
v1 = 800.0       # weathering velocity (m/s)
v2 = 2000.0      # sub-weathering velocity (m/s)
h = 100.0        # weathering thickness (m)

# Critical angle
theta_c = np.arcsin(v1 / v2)

# Source and receiver positions
src = 0.0
rec = 1500.0

# Refracted ray geometry
# Source down to interface at x = h * tan(theta_c)
x_down = src + h * np.tan(theta_c)
# Horizontal segment along interface
x_up = rec - h * np.tan(theta_c)

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 5))

# Layers
xmax = 2200.0
ax.axhspan(-h, 0.0, color="C0", alpha=0.25, label="Weathering ($v_1$ = %.0f m/s)" % v1)
ax.axhspan(-400.0, -h, color="C1", alpha=0.25, label="Bedrock ($v_2$ = %.0f m/s)" % v2)

# Interfaces
ax.axhline(0.0, color="k", lw=1.5)
ax.axhline(-h, color="k", linestyle="--", lw=1.5)

# Direct ray
ax.plot([src, rec], [0.0, 0.0], "C3-", lw=2, label="Direct ray")

# refracted ray
ax.plot([src, x_down], [0.0, -h], "C2-", lw=2)
ax.plot([x_down, x_up], [-h, -h], "C2-", lw=2)
ax.plot([x_up, rec], [-h, 0.0], "C2-", lw=2, label="Refracted ray")

# vertical-ray statics reference (vertical traveltime through weathering)
ax.plot([rec, rec], [0.0, -h], "k:", lw=1.5)

# Source / receiver markers
ax.plot(src, 0.0, "ko", markersize=8)
ax.plot(rec, 0.0, "k^", markersize=8)
ax.text(src, 20.0, "Source", ha="center", fontsize=9)
ax.text(rec, 20.0, "Receiver", ha="center", fontsize=9)

# Delay time annotation
ax.annotate(r"Delay time $\delta t$", xy=(rec + 30.0, -0.5 * h), fontsize=10,
            color="k", ha="left", va="center")

# Crossover distance
x_cross = 2.0 * h * np.sqrt((v2 + v1) / (v2 - v1))
ax.axvline(x_cross, color="C4", linestyle="-.", lw=1.5, alpha=0.7)
ax.text(x_cross + 30.0, -h - 30.0, "Crossover\noffset", fontsize=9, color="C4")

ax.set_xlim(-100.0, xmax)
ax.set_ylim(-300.0, 80.0)
ax.set_xlabel("Distance (m)", fontsize=11)
ax.set_ylabel("Depth (m)", fontsize=11)
ax.set_title("Two-layer refraction model and delay-time geometry", fontsize=12)
ax.legend(loc="lower right", fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("figures/term01_lec03/term01_lec03_refraction_geometry.png", dpi=200, bbox_inches="tight")
print("Saved figures/term01_lec03/term01_lec03_refraction_geometry.png")
