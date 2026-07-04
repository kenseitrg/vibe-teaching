#!/usr/bin/env python3
"""
Layer replacement workflow for long-wavelength statics correction.

Demonstrates how a laterally varying near-surface velocity distorts the
traveltime of a geologically flat reflector, and how layer replacement
with a smooth interval velocity can correct most of the distortion.

Physical model:
  - A single flat reflector at constant depth (z0 = 500 m).
  - True interval velocity v_true = v_smooth + v_random:
      * v_smooth: long-wavelength variation recoverable by velocity analysis
      * v_random: short-wavelength random variations not recoverable
  - Velocity analysis returns v_int = v_smooth (captures the smooth trend).
  - Layer replacement converts to depth using v_int, smooths the depth
    (geological constraint), and converts back to time using a constant
    replacement velocity v_rep derived from v_int.

Workflow (6 panels):
  (a) Model — flat reflector with velocity color fill in the overburden.
  (b) Velocity profiles — v_true, v_int, and v_rep.
  (c) Raw traveltimes t_obs = 2 z0 / v_true — distorted by all variations.
  (d) Depth estimates — z_est (from v_int) and z_smooth (geologically smoothed).
  (e) Corrected traveltimes t_new = 2 z_smooth / v_rep vs raw t_obs.
  (f) Static correction Δt = t_obs - t_new.

Undergraduate seismic data processing — Term 1 Lecture 03.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# =========================================================================
# Model parameters
# =========================================================================
rng = np.random.default_rng(42)

nx = 200                              # number of CMP positions
x = np.linspace(0, 5000, nx)          # CMP positions (m)
dx = x[1] - x[0]                      # 25 m
z0 = 500.0                            # Flat reflector depth (m)
v0 = 2000.0                           # Mean background velocity (m/s)

# --- Smooth, long-wavelength velocity variation (recoverable by velocity analysis)
# Gaussian low-velocity anomaly in the middle + gentle sinusoidal trend
dv_gauss = -160.0                      # Gaussian amplitude (m/s)
sigma_gauss = 800.0                    # Gaussian width (m)
v_smooth = v0 + dv_gauss * np.exp(-((x - 2500) ** 2) / (2 * sigma_gauss ** 2))
v_smooth += 40.0 * np.sin(2 * np.pi * x / 3500)   # long-wavelength trend
v_smooth = np.clip(v_smooth, 1750, 2200)

# --- Short-wavelength random variation (not recoverable by velocity analysis)
# Generate white noise and smooth with a short kernel
white = rng.normal(size=nx)
v_random = gaussian_filter1d(white, sigma=3, mode='reflect')   # correlation ~75 m
# High-pass filter: remove any residual long-wavelength trend
v_random_lowfreq = gaussian_filter1d(v_random, sigma=30, mode='reflect')
v_random = v_random - v_random_lowfreq
# Force exact zero mean
v_random = v_random - np.mean(v_random)
# Scale to small amplitude (std ~22 m/s)
v_random = v_random / np.std(v_random) * 22.0

# --- True velocity = smooth + random
v_true = v_smooth + v_random
v_true = np.clip(v_true, 1700, 2250)

# --- Velocity analysis result: captures the smooth component exactly
v_int = v_smooth.copy()

# --- Replacement velocity: derived from the smooth velocity estimate
v_rep = float(np.mean(v_int))          # constant (~1960 m/s)


# =========================================================================
# Workflow computation
# =========================================================================

# Raw traveltimes from the flat reflector  t_obs = 2 * z0 / v_true
t_obs = 2.0 * z0 / v_true                     # (s)

# Depth conversion using the smooth interval velocity
z_est = 0.5 * v_int * t_obs                    # (m)

# Apply geological smoothing to the depth surface (remove remaining random wiggles)
# Strong smoothing emulates the geological constraint (well tie, regional interpretation)
z_smooth = gaussian_filter1d(z_est, sigma=25, mode='nearest')   # (m)  ~625 m correlation length

# Corrected traveltimes (using the replacement velocity)
t_new = 2.0 * z_smooth / v_rep                 # (s)

# Static correction = raw - corrected
static = t_obs - t_new                         # (s)


# =========================================================================
# Diagnostics
# =========================================================================
t_obs_range_ms = 1000.0 * (t_obs.max() - t_obs.min())
t_new_range_ms = 1000.0 * (t_new.max() - t_new.min())
z_est_rms = np.sqrt(np.mean((z_est - z0) ** 2))
z_smooth_rms = np.sqrt(np.mean((z_smooth - z0) ** 2))
static_range_ms = 1000.0 * (static.max() - static.min())

print("===== Layer replacement figure diagnostics =====")
print(f"v0           = {v0:.0f} m/s")
print(f"v_smooth     range: {v_smooth.max()-v_smooth.min():.0f} m/s")
print(f"v_true       range: {v_true.max()-v_true.min():.0f} m/s")
print(f"v_random     std:   {np.std(v_random):.1f} m/s")
print(f"v_int        = v_smooth  (velocity analysis recovers smooth part)")
print(f"v_rep        = {v_rep:.0f} m/s  (mean of v_int)")
print(f"t_obs        range: {t_obs_range_ms:.1f} ms")
print(f"t_new        range: {t_new_range_ms:.1f} ms")
print(f"z_est        RMS deviation from z0: {z_est_rms:.1f} m")
print(f"z_smooth     RMS deviation from z0: {z_smooth_rms:.1f} m")
print(f"static       range: {static_range_ms:.1f} ms")
print("================================================")


# =========================================================================
# Plot — 3 rows x 2 columns
# =========================================================================
fig, axes = plt.subplots(3, 2, figsize=(12, 10.5))
fig.suptitle('Layer replacement workflow for long-wavelength statics',
             fontsize=14, fontweight='bold')

# Colour palette (colourblind-friendly — Tol / Wong palette)
C_VTRUE   = '#E66100'   # orange
C_VINT    = '#5D3A9B'   # purple
C_VREP    = '#000000'   # black (dashed)
C_TOBS    = '#E66100'   # orange
C_TNEW    = '#0072B2'   # blue
C_ZEST    = '#888888'   # grey
C_ZSMOOTH = '#009E73'   # teal-green
C_STATIC  = '#CC79A7'   # pink


# ---- Panel (a): Model with velocity colour fill --------------------------
ax = axes[0, 0]

# 2-D mesh for the overburden, color-coded by interval velocity
depth_mesh = np.linspace(0, z0, 40)
Xm, Ym = np.meshgrid(x, depth_mesh)
# Velocity is depth-independent in this simplified model
Vm = np.tile(v_true, (len(depth_mesh), 1))

cf = ax.pcolormesh(Xm, Ym, Vm, shading='gouraud',
                   cmap='coolwarm', alpha=0.85)
cbar = fig.colorbar(cf, ax=ax, shrink=0.7, pad=0.02)
cbar.set_label('Interval velocity (m/s)', fontsize=8)

# Reflector line
ax.plot(x, np.full_like(x, z0), 'k-', linewidth=2.5,
        label=f'Reflector at {z0} m')

ax.set_xlabel('CMP position (m)')
ax.set_ylabel('Depth (m)')
ax.set_title('(a) Model: flat reflector + variable velocity', fontsize=10)
ax.invert_yaxis()
ax.legend(fontsize=8, loc='lower left')
ax.grid(True, alpha=0.3)


# ---- Panel (b): Velocity profiles ---------------------------------------
ax = axes[0, 1]
ax.plot(x, v_true, '-', color=C_VTRUE, linewidth=1.2,
        label=r'$v_{\rm true}$ (actual)')
ax.plot(x, v_int, '--', color=C_VINT, linewidth=2.5,
        label=r'$v_{\rm int}$ (velocity analysis)')
ax.axhline(y=v_rep, color=C_VREP, linestyle=':', linewidth=2, alpha=0.7,
           label=r'$v_{\rm rep}$ (replacement)')
ax.set_xlabel('CMP position (m)')
ax.set_ylabel('Interval velocity (m/s)')
ylim_lo = min(v_true.min(), v_int.min()) - 20
ylim_hi = max(v_true.max(), v_int.max()) + 20
ax.set_ylim(ylim_lo, ylim_hi)
ax.set_title('(b) True, estimated, and replacement velocity', fontsize=10)
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)


# ---- Panel (c): Raw traveltimes -----------------------------------------
ax = axes[1, 0]
ax.plot(x, t_obs, '-', color=C_TOBS, linewidth=2.5,
        label=r'$t_{\rm obs} = 2\,z_0 / v_{\rm true}$')

# Annotations highlighting key features
# Main push-down from the low-velocity zone
trough_idx = np.argmax(t_obs)
trough_x = x[trough_idx]
trough_t = t_obs[trough_idx]
ax.annotate('Anomaly creates\npush-down anomaly',
            xy=(trough_x, trough_t),
            xytext=(trough_x + 1100, trough_t + 0.020),
            arrowprops=dict(arrowstyle='->', color='gray', lw=1.2),
            fontsize=7.5, color='gray', fontweight='bold',
            horizontalalignment='left')
# Small random wiggles annotation
wiggle_idx = np.argmax(np.abs(np.diff(t_obs)))
wiggle_x = x[wiggle_idx]
wiggle_t = t_obs[wiggle_idx]
ax.annotate('Random wiggles from\nshort-wavelength\nvelocity variations',
            xy=(wiggle_x, wiggle_t),
            xytext=(max(wiggle_x - 1500, 100), wiggle_t + 0.030),
            arrowprops=dict(arrowstyle='->', color='gray', lw=1.0, ls='--'),
            fontsize=7.0, color='gray', fontstyle='italic',
            horizontalalignment='right')

ax.set_xlabel('CMP position (m)')
ax.set_ylabel('Two-way time (s)')
ax.set_title('(c) Raw traveltimes', fontsize=10)
ax.invert_yaxis()
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)


# ---- Panel (d): Depth estimates -----------------------------------------
ax = axes[1, 1]
ax.plot(x, z_est, '-', color=C_ZEST, linewidth=1.2,
        label=r'$z_{\rm est} = \frac{1}{2} v_{\rm int} t_{\rm obs}$')
ax.plot(x, z_smooth, '-', color=C_ZSMOOTH, linewidth=2.5,
        label=r'$z_{\rm smooth}$ (geologically constrained)')
ax.axhline(y=z0, color='k', linestyle=':', linewidth=1, alpha=0.5,
           label=f'True depth = {z0} m')
ax.set_xlabel('CMP position (m)')
ax.set_ylabel('Depth (m)')
ax.set_title('(d) Depth conversion & geological smoothing', fontsize=10)
ax.legend(fontsize=7, loc='lower right')
ax.grid(True, alpha=0.3)
ax.set_ylim(z0 - 10, z0 + 10)


# ---- Panel (e): Corrected traveltimes -----------------------------------
ax = axes[2, 0]
ax.plot(x, t_obs, '-', color=C_TOBS, linewidth=1.2, alpha=0.5,
        label=(rf'$t_{{\rm obs}}$ (raw, range {t_obs_range_ms:.1f} ms)'))
ax.plot(x, t_new, '-', color=C_TNEW, linewidth=2.5,
        label=(rf'$t_{{\rm new}}$ (corrected, range {t_new_range_ms:.1f} ms)'))
ax.set_xlabel('CMP position (m)')
ax.set_ylabel('Two-way time (s)')
ax.set_title('(e) Corrected traveltimes', fontsize=10)
ax.invert_yaxis()
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)


# ---- Panel (f): Static correction ---------------------------------------
ax = axes[2, 1]
ax.plot(x, 1000.0 * static, '-', color=C_STATIC, linewidth=2.5,
        label=r'$\Delta t = t_{\rm obs} - t_{\rm new}$')
ax.fill_between(x, 1000.0 * static, 0, where=(static >= 0),
                color=C_STATIC, alpha=0.25,
                label='Positive (push-down)')
ax.fill_between(x, 1000.0 * static, 0, where=(static < 0),
                color=C_TNEW, alpha=0.25,
                label='Negative (pull-up)')
ax.axhline(y=0, color='k', linestyle=':', linewidth=0.8)
ax.set_xlabel('CMP position (m)')
ax.set_ylabel('Static correction (ms)')
ax.set_title('(f) Layer-replacement statics', fontsize=10)
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)


# =========================================================================
# Finalise
# =========================================================================
plt.tight_layout()
plt.savefig('figures/term01_lec03/term01_lec03_layer_replacement.png',
            dpi=150, bbox_inches='tight')
plt.close()
print('Saved: figures/term01_lec03/term01_lec03_layer_replacement.png')
