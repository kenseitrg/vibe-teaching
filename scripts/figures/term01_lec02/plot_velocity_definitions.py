"""
Velocity definitions figure for Term 1 Lecture 02.

Shows a simple three-layer model and compares interval, average, RMS and NMO
velocities as functions of two-way time.  Each velocity definition is tied to a
different ray assumption, which is drawn schematically in the top panel.

The script is self-contained and writes a single PNG to figures/term01_lec02/.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# ---------------------------------------------------------------------------
# Model parameters: three horizontal layers
# ---------------------------------------------------------------------------
thickness = np.array([200.0, 300.0, 500.0])   # m
vint = np.array([1500.0, 2000.0, 2500.0])       # m/s

# Two-way interval traveltimes (seconds)
dt = 2.0 * thickness / vint
# Cumulative two-way time at layer bottoms
t_cum = np.cumsum(dt)
t_edges = np.concatenate(([0.0], t_cum))
# Depth at layer bottoms
z_cum = np.cumsum(thickness)
z_edges = np.concatenate(([0.0], z_cum))

# ---------------------------------------------------------------------------
# Compute velocity curves versus two-way time
# ---------------------------------------------------------------------------
# Interval velocity: piecewise constant per layer
v_interval = np.repeat(vint, 2)
t_interval = np.zeros(2 * len(vint))
for i in range(len(vint)):
    t_interval[2 * i] = t_edges[i]
    t_interval[2 * i + 1] = t_edges[i + 1]

# Average velocity at each interface
v_avg = np.zeros_like(t_cum)
for i in range(len(vint)):
    v_avg[i] = z_cum[i] / (t_cum[i] / 2.0)  # depth / one-way time

# RMS velocity at each interface
v_rms = np.zeros_like(t_cum)
for i in range(len(vint)):
    v_rms[i] = np.sqrt(np.sum(vint[: i + 1] ** 2 * dt[: i + 1]) / np.sum(dt[: i + 1]))

# Dix NMO velocity at each interface (for horizontal layers)
v_nmo = np.zeros_like(t_cum)
v_nmo[0] = vint[0]
for i in range(1, len(vint)):
    # Dix formula: V_nmo,i^2 * t_i - V_nmo,i-1^2 * t_{i-1} = V_int,i^2 * (t_i - t_{i-1})
    t0_prev = t_cum[i - 1]
    t0_curr = t_cum[i]
    v_nmo[i] = np.sqrt((v_nmo[i - 1] ** 2 * t0_prev + vint[i] ** 2 * (t0_curr - t0_prev)) / t0_curr)

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(12, 7))

# Top panel: layered model with ray assumptions
ax_geo = fig.add_axes([0.08, 0.55, 0.40, 0.40])
# Draw layers
for i in range(len(thickness)):
    ax_geo.axhspan(z_edges[i], z_edges[i + 1], color=f"C{i}", alpha=0.25)
    ax_geo.text(0.52, 0.5 * (z_edges[i] + z_edges[i + 1]),
                f"$v_{{{i + 1}}} = {vint[i]:.0f}$ m/s",
                ha="center", va="center", fontsize=10, transform=ax_geo.transData)

# Surface source position
src_x, src_z = 0.0, 0.0
ax_geo.plot(src_x, src_z, "ko", markersize=8, zorder=5)
ax_geo.text(src_x - 0.15, src_z + 20, "Source", ha="right", va="bottom", fontsize=9)

# Ray assumptions (schematic, not to scale horizontally)
# 1. Vertical ray for average velocity
x_vert = 0.15
ax_geo.plot([src_x, src_x], [src_z, z_cum[-1]], "k--", lw=1.5, label="Average: vertical ray")
ax_geo.annotate("Average", xy=(src_x + 0.05, 0.5 * z_cum[-1]), fontsize=9)

# 2. Straight ray for RMS (small-offset approximation)
ax_geo.plot([src_x, src_x + 0.35], [src_z, z_cum[-1]], "k-.", lw=1.5)
ax_geo.annotate("RMS: straight ray", xy=(src_x + 0.22, 0.6 * z_cum[-1]), fontsize=9)

# 3. Hyperbolic / curved ray for NMO
x_curve = np.linspace(src_x, src_x + 0.55, 50)
z_curve = z_cum[-1] * (1 - np.exp(-4.0 * x_curve))
ax_geo.plot(x_curve, z_curve, "k-", lw=1.5)
ax_geo.annotate("NMO: hyperbolic moveout", xy=(src_x + 0.35, 0.25 * z_cum[-1]), fontsize=9)

ax_geo.set_xlim(-0.1, 0.7)
ax_geo.set_ylim(z_cum[-1] + 50, -30)
ax_geo.set_xlabel("Horizontal distance (schematic)", fontsize=10)
ax_geo.set_ylabel("Depth (m)", fontsize=10)
ax_geo.set_title("Ray assumptions for different velocity definitions", fontsize=11)
ax_geo.grid(True, alpha=0.3)

# Bottom panel: velocity versus two-way time
ax_vel = fig.add_axes([0.55, 0.12, 0.40, 0.80])
ax_vel.plot(t_interval, v_interval, "k-", lw=2, label="Interval velocity")
ax_vel.plot(t_cum, v_avg, "o-", color="C0", lw=2, markersize=6, label="Average velocity")
ax_vel.plot(t_cum, v_rms, "s-", color="C1", lw=2, markersize=6, label="RMS velocity")
ax_vel.plot(t_cum, v_nmo, "^-", color="C2", lw=2, markersize=6, label="NMO velocity")

ax_vel.set_xlabel("Two-way time $t_0$ (s)", fontsize=11)
ax_vel.set_ylabel("Velocity (m/s)", fontsize=11)
ax_vel.set_title("Velocity curves for a three-layer model", fontsize=11)
ax_vel.legend(loc="lower right", fontsize=9)
ax_vel.grid(True, alpha=0.3)
ax_vel.set_xlim(0, 1.05 * t_cum[-1])
ax_vel.set_ylim(0, 1.2 * np.max(v_interval))

plt.savefig("figures/term01_lec02/term01_lec02_velocity_definitions.png", dpi=200, bbox_inches="tight")
print("Saved figures/term01_lec02/term01_lec02_velocity_definitions.png")
