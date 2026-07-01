"""
Velocity definitions figure for Term 1 Lecture 02.

Shows a three-layer earth model and compares the ray paths associated with
different velocity averages. The left panel draws the true refracted ray, the
vertical ray (average velocity) and the straight ray (RMS velocity). The right
panel plots interval, RMS and average velocity as functions of two-way time.

The script is self-contained and writes a single PNG to figures/term01_lec02/.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Model parameters: three horizontal layers
# ---------------------------------------------------------------------------
thickness = np.array([400.0, 400.0, 400.0])  # m
vint = np.array([1500.0, 2500.0, 3500.0])    # m/s

# Two-way interval traveltimes (seconds) and cumulative times
dt = 2.0 * thickness / vint
t_cum = np.cumsum(dt)
t_edges = np.concatenate(([0.0], t_cum))

# Depth at layer bottoms
z_cum = np.cumsum(thickness)
z_edges = np.concatenate(([0.0], z_cum))

# ---------------------------------------------------------------------------
# Compute average and RMS velocity at each interface
# ---------------------------------------------------------------------------
v_avg = np.zeros_like(t_cum)
for i in range(len(vint)):
    v_avg[i] = z_cum[i] / (t_cum[i] / 2.0)  # depth / one-way time

v_rms = np.zeros_like(t_cum)
for i in range(len(vint)):
    v_rms[i] = np.sqrt(np.sum(vint[: i + 1] ** 2 * dt[: i + 1]) / np.sum(dt[: i + 1]))

# Interval velocity as a piecewise-constant staircase for plotting
v_interval = np.repeat(vint, 2)
t_interval = np.zeros(2 * len(vint))
for i in range(len(vint)):
    t_interval[2 * i] = t_edges[i]
    t_interval[2 * i + 1] = t_edges[i + 1]

# ---------------------------------------------------------------------------
# True refracted ray using Snell's law
# ---------------------------------------------------------------------------
# Choose a small ray parameter so the ray stays near-vertical and clearly bends.
angle0 = np.deg2rad(10.0)  # incidence angle in layer 1
p = np.sin(angle0) / vint[0]  # ray parameter (s/m)

angles = np.zeros(len(vint))
for i in range(len(vint)):
    sin_theta = p * vint[i]
    # Clip to avoid numerical issues; small p guarantees sin_theta < 1.
    sin_theta = np.clip(sin_theta, -1.0, 1.0)
    angles[i] = np.arcsin(sin_theta)

# Horizontal displacement in each layer and cumulative ray coordinates
x_ray = [0.0]
t_ray = [0.0]
x = 0.0
for i in range(len(vint)):
    dx = thickness[i] * np.tan(angles[i])
    x += dx
    x_ray.extend([x, x])
    t_ray.extend([t_edges[i + 1], t_edges[i + 1]])

# Remove duplicate points and keep the ray monotonic in time.
x_ray = np.array(x_ray)
t_ray = np.array(t_ray)

# ---------------------------------------------------------------------------
# Straight path (RMS / straight-ray approximation) from surface to bottom point
# ---------------------------------------------------------------------------
x_bottom = x_ray[-1]
t_bottom = t_cum[-1]

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig, (ax_geo, ax_vel) = plt.subplots(1, 2, figsize=(12, 7))

# --- Left panel: earth model with ray paths --------------------------------
# Draw layers as horizontal bands
for i in range(len(thickness)):
    ax_geo.axhspan(t_edges[i], t_edges[i + 1], color=f"C{i}", alpha=0.25)
    ax_geo.text(0.08, 0.5 * (t_edges[i] + t_edges[i + 1]),
                f"$v_{{{i + 1}}} = {vint[i]:.0f}$ m/s",
                ha="left", va="center", fontsize=10)

# Plot rays
ax_geo.plot(x_ray, t_ray, "k-", lw=2, label="True refracted ray")
ax_geo.plot([0.0, 0.0], [0.0, t_bottom], "k--", lw=2, label="Vertical ray (average)")
ax_geo.plot([0.0, x_bottom], [0.0, t_bottom], "k-.", lw=2, label="Straight ray (RMS)")

# Source marker
ax_geo.plot(0.0, 0.0, "ko", markersize=8, zorder=5)
ax_geo.text(0.0, -0.03, "Source", ha="center", va="bottom", fontsize=9)

ax_geo.set_xlim(-0.02, 1.15 * x_bottom)
ax_geo.set_ylim(1.05 * t_bottom, -0.08)  # positive time points down
ax_geo.set_xlabel("Horizontal offset (m)", fontsize=11)
ax_geo.set_ylabel("Two-way time $t_0$ (s)", fontsize=11)
ax_geo.set_title("Ray paths in a three-layer model", fontsize=12)
ax_geo.grid(True, alpha=0.3)
ax_geo.legend(loc="upper right", fontsize=9)

# --- Right panel: velocity curves versus two-way time ----------------------
ax_vel.plot(v_interval, t_interval, "k-", lw=2, label="Interval velocity")
ax_vel.plot(v_avg, t_cum, "o-", color="C0", lw=2, markersize=7, label="Average velocity")
ax_vel.plot(v_rms, t_cum, "s-", color="C1", lw=2, markersize=7, label="RMS velocity")

# Layer boundaries as horizontal reference lines
for t in t_cum[:-1]:
    ax_vel.axhline(t, color="gray", ls=":", lw=0.8, alpha=0.7)

ax_vel.set_xlabel("Velocity (m/s)", fontsize=11)
ax_vel.set_ylabel("Two-way time $t_0$ (s)", fontsize=11)
ax_vel.set_title("Velocity curves for a three-layer model", fontsize=12)
ax_vel.legend(loc="upper right", fontsize=10)
ax_vel.grid(True, alpha=0.3)
ax_vel.set_xlim(0, 1.2 * np.max(v_interval))
ax_vel.set_ylim(1.05 * t_cum[-1], -0.05)  # positive time points down

plt.tight_layout()
plt.savefig("figures/term01_lec02/term01_lec02_velocity_definitions.png", dpi=200, bbox_inches="tight")
print("Saved figures/term01_lec02/term01_lec02_velocity_definitions.png")
