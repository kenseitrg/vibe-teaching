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
def diving_ray_x(xs, p, vz):
    """Return x(z) for a diving ray from source xs with ray parameter p in a v(z) medium."""
    theta = np.arcsin(np.clip(p * vz, -1, 1))
    dx_dz = np.tan(theta)
    x_ray = np.zeros_like(z)
    x_ray[0] = xs
    for i in range(1, len(z)):
        dz = z[i] - z[i - 1]
        x_ray[i] = x_ray[i - 1] + 0.5 * (dx_dz[i] + dx_dz[i - 1]) * dz
    return x_ray

# 1D starting velocity profile (same at every x)
vz_start = v0 + k * z

# Choose a few rays
source_positions = [500, 1500, 2500, 3500]
p = 1.0 / 1700.0  # turning depth around z ~ 480 m

fig, axes = plt.subplots(1, 2, figsize=(10, 6), dpi=150)

# Starting model with rays
ax = axes[0]
im = ax.pcolormesh(X, Z, v_start, shading="auto", cmap="viridis", vmin=400, vmax=2000)
for xs in source_positions:
    x_ray = diving_ray_x(xs, p, vz_start)
    ax.plot(x_ray, z, color="white", lw=0.8, alpha=0.7)
ax.invert_yaxis()
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Depth (m)")
ax.set_title("Starting model and diving rays")
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
