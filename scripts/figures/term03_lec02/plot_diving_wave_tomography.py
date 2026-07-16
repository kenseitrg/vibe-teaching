"""
Diving-wave tomography: starting model, rays, and updated tomographic model.

Output: figures/term03_lec02/term03_lec02_diving_wave_tomography.png
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

COLORS = ["#0173B2", "#DE8F05", "#029E73", "#D55E00", "#CC79A7", "#F0E442"]

# Grid
nz, nx = 60, 100
z = np.linspace(0, 500, nz)  # depth in m
x = np.linspace(0, 5000, nx)  # horizontal in m
Z, X = np.meshgrid(z, x, indexing="ij")

# Starting model: v = v0 + k*z, v0 = 500 m/s, k = 2.5 m/s per m
v0 = 500.0
k = 2.5
v_start = v0 + k * Z

# True model has a low-velocity channel at x ~ 2000-3000 m, shallow
v_true = v_start.copy()
channel = ((X > 2000) & (X < 3500) & (Z < 120))
v_true[channel] *= 0.7

# Tomographic update: smooth version of the true model (after regularization)
from scipy.ndimage import gaussian_filter
v_update = gaussian_filter(v_true, sigma=(2, 5))

# Ray tracing for a diving wave in a v(z) medium: x(p) = integral p v / sqrt(1 - p^2 v^2) dz
# Use a constant gradient v = v0 + k*z; ray parameter p = sin(theta)/v
# For a source at x_s, turning depth where p*v_max = 1.
def diving_ray_x(xs, p, vz, z):
    """Return (x, z) arrays for a diving ray from source xs in a v(z) medium.

    The ray is traced downward until p*v(z) approaches 1 (the turning point),
    then reflected upward.  This avoids the singularity at the turning point
    and keeps the ray inside the model bounds.
    """
    # Turning index: last valid depth before p*vz would exceed 1
    valid = p * vz < 0.999
    if not np.any(valid):
        return np.array([xs]), np.array([z[0]])
    turn_idx = np.where(valid)[0][-1]
    if turn_idx < 2:
        return np.array([xs]), np.array([z[0]])

    theta = np.arcsin(np.clip(p * vz[: turn_idx + 1], -1, 1))
    dx_dz = np.tan(theta)
    x_down = np.zeros(turn_idx + 1)
    x_down[0] = xs
    for i in range(1, turn_idx + 1):
        dz = z[i] - z[i - 1]
        x_down[i] = x_down[i - 1] + 0.5 * (dx_dz[i] + dx_dz[i - 1]) * dz

    x_turn = x_down[-1]
    # Downward branch + mirrored upward branch (exclude duplicate turning point)
    z_ray = np.concatenate([z[: turn_idx + 1], z[turn_idx - 1 :: -1]])
    x_ray = np.concatenate([x_down, 2 * x_turn - x_down[-2 :: -1]])

    return x_ray, z_ray

# 1D starting velocity profile (same at every x)
vz_start = v0 + k * z

source_positions = [500, 1500, 2500, 3500]
# Ray parameters for a few takeoff angles; smaller p = steeper ray, deeper turn.
ray_specs = [
    (1.0 / 1462.0, "white", r"$20^{\circ}$"),   # turn ~ z = 385 m
    (1.0 / 871.0, COLORS[0], r"$35^{\circ}$"),  # turn ~ z = 148 m
    (1.0 / 653.0, COLORS[1], r"$50^{\circ}$"),  # turn ~ z = 61 m
]

fig, axes = plt.subplots(1, 2, figsize=(10, 6), dpi=150)

# Starting model with rays
ax = axes[0]
im = ax.pcolormesh(X, Z, v_start, shading="auto", cmap="viridis", vmin=400, vmax=2000)
for p, color, label in ray_specs:
    for xs in source_positions:
        x_ray, z_ray = diving_ray_x(xs, p, vz_start, z)
        ax.plot(x_ray, z_ray, color=color, lw=1.2, alpha=0.9, label=label if xs == source_positions[0] else "")
ax.set_xlim(x.min(), x.max())
ax.set_ylim(z.max(), z.min())
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Depth (m)")
ax.set_title("Starting model and diving rays")
ax.legend(title="Takeoff angle", loc="lower right", fontsize=8, title_fontsize=8)
cb = plt.colorbar(im, ax=ax, label="Velocity (m/s)")

# Updated tomographic model
ax = axes[1]
im = ax.pcolormesh(X, Z, v_update, shading="auto", cmap="viridis", vmin=400, vmax=2000)
# Overlay coverage mask (where v_update is well constrained: away from edges)
coverage = np.ones_like(v_update)
coverage[:, :15] = 0.3
coverage[:, -15:] = 0.3
ax.contour(X, Z, coverage, levels=[0.5], colors="white", linestyles="--", linewidths=0.8)
ax.invert_yaxis()
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Depth (m)")
ax.set_title("Tomographic update (dashed = poor coverage)")
cb = plt.colorbar(im, ax=ax, label="Velocity (m/s)")

plt.tight_layout()
plt.savefig("figures/term03_lec02/term03_lec02_diving_wave_tomography.png", dpi=150, bbox_inches="tight")
plt.close()
