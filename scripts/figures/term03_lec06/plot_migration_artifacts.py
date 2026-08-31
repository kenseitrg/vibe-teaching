"""
Term 3 Lecture 06 — Figure 1: Migration impulse response with and without
regularization, for a point diffractor and for a flat horizon.

Pedagogical point
-----------------
Kirchhoff migration forms an image by summing the recorded wavefield over an
aperture of input traces,

    I(m) = sum_i  w_i * x( t_i(m), x_i ),

which approximates an integral over a continuous aperture.

* Point diffractor.  With a DENSE, REGULAR aperture the contributions interfere
  constructively at the diffractor and destructively elsewhere, so the impulse
  response is a clean, focused point.  With a SPARSE / IRREGULAR aperture the
  destructive cancellation away from the diffractor breaks down and energy
  "leaks" along the operator surface -> prominent tails and smearing.

* Flat horizon.  The same physics applies to a simple flat reflector.  A regular
  aperture reconstructs a clean, continuous, flat event at the correct depth; an
  irregular aperture contaminates it with scattered artifacts and a rough
  background, i.e. false structure that has no geological meaning.

In both rows the two panels migrate the SAME number of traces; only the trace
PLACEMENT differs (even grid vs. uniform-random positions with realistic gaps
and clusters).  The artifacts are not noise -- they are the signature of an
incomplete aperture summation, and regularization (reconstructing the wavefield
onto a regular grid) removes them.

Self-contained: numpy + matplotlib only.
"""

import os

import numpy as np
from matplotlib.colors import TwoSlopeNorm

# ---------------------------------------------------------------------------
# Physical model
# ---------------------------------------------------------------------------
V = 2000.0                 # constant velocity (m/s)
X0, Z0 = 1500.0, 900.0     # point diffractor position (m)
Z_REF = 900.0              # flat reflector depth (m)
F0 = 25.0                  # Ricker dominant frequency (Hz)

# Aperture extent along the surface (m)
AP_MIN, AP_MAX = 0.0, 3000.0

# Image grid
NX, NZ = 200, 150
IMG_X = np.linspace(400.0, 2600.0, NX)      # image x (m)
IMG_Z = np.linspace(100.0, 1500.0, NZ)      # image depth (m)
EXTENT = [IMG_X[0], IMG_X[-1], IMG_Z[-1], IMG_Z[0]]   # (xmin,xmax,zmax,zmin)


def wavelet(t):
    """Zero-phase Ricker wavelet evaluated at time(s) t (s)."""
    a = np.pi * F0 * t
    return (1.0 - 2.0 * a**2) * np.exp(-(a**2))


def two_way_time(x_surf, xm, zm):
    """Two-way traveltime from surface position x_surf to image point (xm, zm).

    Zero-offset (source == receiver at the surface), constant velocity.
    Returns an array of shape (n_traces, nx, nz).
    """
    return 2.0 * np.sqrt((x_surf[..., None, None] - xm[None, :, None]) ** 2
                         + zm[None, None, :] ** 2) / V


def aperture_weights(x_surf):
    """Cosine taper across the aperture so edge effects do not dominate."""
    frac = (x_surf - AP_MIN) / (AP_MAX - AP_MIN)      # 0..1
    return 0.5 - 0.5 * np.cos(2.0 * np.pi * frac)     # 0 at edges, 1 centre


def migrate(x_surf, t_data):
    """Kirchhoff migration image.

    I(xm, zm) = sum_i w_i * wavelet( t_model(x_i; xm, zm) - t_data(x_i) )

    t_data : per-trace arrival time of the event being migrated (s).
    """
    x_surf = np.asarray(x_surf, dtype=float)
    t_data = np.asarray(t_data, dtype=float)

    t_mod = two_way_time(x_surf, IMG_X, IMG_Z)          # (Ni, Nx, Nz)
    w = aperture_weights(x_surf)                        # (Ni,)

    arg = t_mod - t_data[:, None, None]                 # time residual (s)
    img = (wavelet(arg) * w[:, None, None]).sum(axis=0)  # (Nx, Nz)
    return img.T                                        # (Nz, Nx) -> depth rows


# Per-trace data arrival times for the two models.
def diffraction_time(x_surf):
    """Diffraction traveltime of the point diffractor at surface position x."""
    return 2.0 * np.sqrt((x_surf - X0) ** 2 + Z0**2) / V


def flat_reflection_time(x_surf):
    """Reflection traveltime of a flat horizon (constant across traces)."""
    return np.full(np.asarray(x_surf).shape, 2.0 * Z_REF / V)


# ---------------------------------------------------------------------------
# Two aperture samplings -- SAME number of traces; only the placement differs.
# ---------------------------------------------------------------------------
rng = np.random.default_rng(7)

N_TRACES = 241                     # identical trace count in both columns

# Regular: dense, evenly spaced grid -- the target of regularization.
x_regular = np.linspace(AP_MIN, AP_MAX, N_TRACES)

# Irregular: the same number of traces at random positions.  Uniform-random
# placement naturally produces the clusters and gaps of a real acquisition
# (obstacles, permit boundaries), so the aperture is non-uniform and gappy.
x_irregular = np.sort(rng.uniform(AP_MIN, AP_MAX, N_TRACES))

# Migrate both models on both apertures.
img_diff_irr = migrate(x_irregular, diffraction_time(x_irregular))
img_diff_reg = migrate(x_regular, diffraction_time(x_regular))
img_hor_irr = migrate(x_irregular, flat_reflection_time(x_irregular))
img_hor_reg = migrate(x_regular, flat_reflection_time(x_regular))


def clip_for(*imgs, pct=99.5):
    """Shared symmetric colour clip at a high percentile (seismic display)."""
    all_abs = np.concatenate([np.abs(i).ravel() for i in imgs])
    return np.percentile(all_abs, pct)


vmax_diff = clip_for(img_diff_irr, img_diff_reg)
vmax_hor = clip_for(img_hor_irr, img_hor_reg)

# ---------------------------------------------------------------------------
# Figure (2x2): rows = model, columns = aperture
# ---------------------------------------------------------------------------
import matplotlib.pyplot as plt

COL = "seismic"

fig, axes = plt.subplots(2, 2, figsize=(10, 8.6), sharex=True, sharey=True)

panels = [
    # (ax, image, title, vmax, kind)
    (axes[0, 0], img_diff_irr, "(a) Point diffractor — irregular aperture",
     vmax_diff, "diffractor"),
    (axes[0, 1], img_diff_reg, "(b) Point diffractor — regular aperture",
     vmax_diff, "diffractor"),
    (axes[1, 0], img_hor_irr, "(c) Flat horizon — irregular aperture",
     vmax_hor, "horizon"),
    (axes[1, 1], img_hor_reg, "(d) Flat horizon — regular aperture",
     vmax_hor, "horizon"),
]

for ax, img, title, vmax, kind in panels:
    norm = TwoSlopeNorm(vmin=-vmax, vcenter=0.0, vmax=vmax)
    ax.imshow(img, extent=EXTENT, cmap=COL, norm=norm, aspect="auto",
              interpolation="bilinear")
    if kind == "diffractor":
        ax.plot(X0, Z0, marker="*", ms=14, mfc="black", mec="black", mew=0.8,
                zorder=5)
    else:
        ax.axhline(Z_REF, color="black", ls="--", lw=1.2, alpha=0.9, zorder=5)
        ax.text(IMG_X[1], Z_REF - 45, "true horizon", color="black",
                fontsize=8.5, va="bottom", ha="left", fontweight="bold")
    ax.set_title(title, fontsize=10.5)

axes[1, 0].set_xlabel("Midpoint position (m)")
axes[1, 1].set_xlabel("Midpoint position (m)")
axes[0, 0].set_ylabel("Depth (m)")
axes[1, 0].set_ylabel("Depth (m)")

fig.tight_layout()

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
out_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                       "figures", "term03_lec06")
out_dir = os.path.abspath(out_dir)
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "term03_lec06_migration_artifacts.png")
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"Saved figure to {out_path}")
