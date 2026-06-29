"""
Layer replacement workflow for long-wavelength statics correction.

Generates a 2×2 figure showing:
  (a) Picked horizon distorted in time by a near-surface anomaly.
  (b) Horizon converted to depth using picked interval velocities.
  (c) Smoothed depth horizon (geology without anomaly).
  (d) Corrected (flattened) horizon in time after applying layer-replacement statics.

Undergraduate seismic data processing — Term 1 Lecture 03.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Parameters -----------------------------------------------------------
nx = 100                          # number of CMPs
x = np.linspace(0, 5000, nx)      # CMP positions (m)

# Background geology: a slightly dipping horizon dipping to the right
t0_background = 0.8 + 0.4 * (x / 5000)   # seconds

# Near-surface anomaly: a Gaussian push-down centred at x = 2500 m
anomaly_amplitude = 0.25          # seconds (peak distortion)
anomaly_width = 600               # m
anomaly = -anomaly_amplitude * np.exp(-((x - 2500) ** 2) / (2 * anomaly_width ** 2))

# Distorted horizon (observed in time after initial statics)
t_observed = t0_background + anomaly

# Picked interval velocity for depth conversion (m/s)
v_int = 2200.0

# Convert observed horizon to depth
z_observed = 0.5 * v_int * t_observed   # z = v * t / 2

# Smooth the depth horizon (simple moving average filter)
smoothing_window = 21  # number of CMPs in window
kernel = np.ones(smoothing_window) / smoothing_window
z_smoothed = np.convolve(z_observed, kernel, mode='same')
# Edge handling: extend first/last values
z_smoothed[:smoothing_window // 2] = z_smoothed[smoothing_window // 2]
z_smoothed[-(smoothing_window // 2):] = z_smoothed[-(smoothing_window // 2)]

# Convert smoothed depth back to time
t_smoothed = 2 * z_smoothed / v_int

# The static correction = original time - smoothed time
static_correction = t_observed - t_smoothed

# Corrected horizon after applying layer replacement
t_corrected = t_observed - static_correction

# --- Plot ----------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(10, 6))
fig.suptitle('Layer replacement workflow', fontsize=14, y=1.02)

# (a) Distorted horizon in time
ax = axes[0, 0]
ax.plot(x, t_observed, 'k-', linewidth=2, label='Observed horizon')
ax.fill_between(x, t_observed, t_observed - 0.02,
                color='grey', alpha=0.2)
ax.plot(x, t0_background, 'k--', linewidth=1, label='True geology (unknown)')
ax.set_xlabel('CMP position (m)')
ax.set_ylabel('Two-way time (s)')
ax.set_title('(a) Picked horizon in time')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
ax.invert_yaxis()

# (b) Horizon in depth
ax = axes[0, 1]
ax.plot(x, z_observed, 'k-', linewidth=2, label='Depth from picks')
ax.fill_between(x, 0, z_observed, color='lightblue', alpha=0.3,
                label=f'$V_\\mathrm{{int}}$ = {v_int} m/s')
ax.set_xlabel('CMP position (m)')
ax.set_ylabel('Depth (m)')
ax.set_title('(b) Converted to depth')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# (c) Smoothed depth horizon
ax = axes[1, 0]
ax.plot(x, z_observed, 'lightgrey', linewidth=1.5, label='Original depth')
ax.plot(x, z_smoothed, 'r-', linewidth=2.5, label='Smoothed depth')
ax.fill_between(x, z_smoothed, z_observed,
                color='red', alpha=0.15, label='Anomaly removed')
ax.set_xlabel('CMP position (m)')
ax.set_ylabel('Depth (m)')
ax.set_title('(c) Smoothed depth surface')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# (d) Corrected horizon in time
ax = axes[1, 1]
ax.plot(x, t_corrected, 'g-', linewidth=2.5, label='Corrected horizon')
ax.plot(x, t0_background, 'k--', linewidth=1, label='True geology')
ax.fill_between(x, t_corrected, t_corrected - 0.02,
                color='green', alpha=0.2)
ax.set_xlabel('CMP position (m)')
ax.set_ylabel('Two-way time (s)')
ax.set_title('(d) After layer-replacement statics')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)
ax.invert_yaxis()

plt.tight_layout()
plt.savefig('figures/term01_lec03/term01_lec03_layer_replacement.png',
            dpi=150, bbox_inches='tight')
plt.close()
print('Saved: term01_lec03_layer_replacement.png')
