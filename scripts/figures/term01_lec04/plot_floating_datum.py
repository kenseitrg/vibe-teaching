"""
Floating datum concept illustration.

Top panel (a) — elevation domain:
  - Rugged topography (surface elevation)
  - Flat final/client datum below the lowest topography
  - Smoothed floating datum following the long-wavelength topography
  - Three CMP locations with semi-transparent local datum bands
  - One highlighted surface point (shot or receiver) shared by several CMPs.
    Curved arrows point from the shared surface location to each local datum
    band, showing that the same surface point has different statics depending
    on which local CMP datum is used.

Bottom panel (b) — statics decomposition:
  - Total statics (black solid)
  - Smoothed long-wavelength static (red dashed)
  - Floating-datum correction = total - smoothed (blue shaded)
  - The three CMP locations from panel (a) are marked.

Undergraduate seismic data processing — Term 1 Lecture 04.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Parameters -----------------------------------------------------------
nx = 150
x = np.linspace(0, 5000, nx)        # Surface / CMP positions (m)

# Replacement velocity used to convert elevation differences to static shifts
v_replace = 2000.0                  # m/s

# Surface elevation with large, gentle topography + rugged short-wavelength bumps
np.random.seed(42)
elevation = (150 * np.sin(0.0003 * 2 * np.pi * x) +
             50 * np.sin(0.0015 * 2 * np.pi * x) +
             18 * np.random.randn(nx))
elevation = elevation - elevation.min()   # lowest point at 0 m

# Final flat datum below the lowest topography
final_datum_elev = -80.0            # m

# Total static = time from surface to final flat datum (ms)
total_static = (elevation - final_datum_elev) / v_replace * 1000.0

# Smoothed static (long-wavelength component)
smoothing_window = 31
kernel = np.ones(smoothing_window) / smoothing_window
smoothed_static = np.convolve(total_static, kernel, mode='same')
smoothed_static[:smoothing_window // 2] = smoothed_static[smoothing_window // 2]
smoothed_static[-(smoothing_window // 2):] = smoothed_static[-(smoothing_window // 2)]

# Floating-datum correction = total - smoothed
floating_correction = total_static - smoothed_static

# Floating datum elevation derived from the smoothed static
floating_elev = final_datum_elev + smoothed_static * v_replace / 1000.0

# Three CMP locations for local datums
cmp_positions = np.array([1200.0, 2500.0, 3800.0])
cmp_indices = np.array([np.argmin(np.abs(x - xp)) for xp in cmp_positions])

# Local datum bands: vertical thickness and horizontal extent
band_thickness = 22.0      # m
local_half_width = 650.0   # m

# Highlighted surface point shared by several CMPs
shared_x = 2500.0
shared_idx = np.argmin(np.abs(x - shared_x))

# --- Plot ----------------------------------------------------------------
fig = plt.figure(figsize=(10, 7.5))
fig.suptitle('Floating datum concept', fontsize=14)

# --- Panel (a): elevation domain -----------------------------------------
ax1 = plt.subplot(2, 1, 1)

# Surface elevation
ax1.plot(x, elevation, 'k-', linewidth=1.8, label='Surface elevation')

# Final flat datum
ax1.axhline(y=final_datum_elev, color='C3', linewidth=2.2,
            linestyle='-', label='Final flat datum')

# Floating datum (smoothed long-wavelength surface)
ax1.plot(x, floating_elev, 'r--', linewidth=2.5,
         label='Floating datum')

# Local CMP datum bands (semi-transparent blue rectangles)
for idx in cmp_indices:
    x_left = x[idx] - local_half_width
    x_right = x[idx] + local_half_width
    y_center = floating_elev[idx]
    rect = plt.Rectangle((x_left, y_center - band_thickness / 2),
                         x_right - x_left, band_thickness,
                         color='C0', alpha=0.25, zorder=1)
    ax1.add_patch(rect)
    # Outline edges
    ax1.plot([x_left, x_right],
             [y_center - band_thickness / 2, y_center - band_thickness / 2],
             color='C0', linewidth=1.0)
    ax1.plot([x_left, x_right],
             [y_center + band_thickness / 2, y_center + band_thickness / 2],
             color='C0', linewidth=1.0)

# Label the local CMP datum bands (placed in open area on the left)
ax1.text(150,
         floating_elev[np.argmin(np.abs(x - cmp_positions[0]))] - 80,
         'Local CMP datum bands', color='C0', fontsize=9, va='top',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                   edgecolor='C0', alpha=0.9))

# Highlight shared surface point (shot or receiver)
ax1.plot(shared_x, elevation[shared_idx], 'ko', markersize=8,
         markerfacecolor='white', markeredgewidth=1.5,
         label='Shared shot / receiver')

# Short arrows from shared surface point to each local CMP datum band
for k, idx in enumerate(cmp_indices):
    y_center = floating_elev[idx]
    # stagger arrow landing points horizontally so they are clearly separate
    x_target = shared_x + (k - 1) * 100
    ax1.annotate('', xy=(x_target, y_center - band_thickness / 2),
                 xytext=(x_target, elevation[shared_idx]),
                 arrowprops=dict(arrowstyle='->', color='C0', lw=1.5))

# Annotation to the right of the arrows
ax1.text(shared_x + 280,
         (elevation[shared_idx] + floating_elev[cmp_indices[1]]) / 2 - 10,
         'Same surface point,\ndifferent statics', color='C0', fontsize=8,
         va='center',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                   edgecolor='C0', alpha=0.9))

# Mark CMP locations on the surface
for idx in cmp_indices:
    ax1.plot(x[idx], elevation[idx], 'C0^', markersize=8,
             markeredgecolor='black', markeredgewidth=0.8)

ax1.set_xlabel('Surface position (m)')
ax1.set_ylabel('Elevation (m)')
ax1.set_title('(a) Elevation domain: local CMP datum bands and a shared surface point')
ax1.legend(fontsize=8, loc='lower right')
ax1.grid(True, alpha=0.3)
ax1.invert_yaxis()

# --- Panel (b): statics decomposition ------------------------------------
ax2 = plt.subplot(2, 1, 2)

ax2.plot(x, total_static, 'k-', linewidth=1.8, label='Total static')
ax2.plot(x, smoothed_static, 'r--', linewidth=2.5,
         label='Long-wavelength (smoothed)')
ax2.fill_between(x, floating_correction, 0,
                 where=(floating_correction > 0),
                 color='C0', alpha=0.3, label='Floating-datum correction')
ax2.fill_between(x, floating_correction, 0,
                 where=(floating_correction < 0),
                 color='C0', alpha=0.3)  # same colour for negative
ax2.fill_between(x, smoothed_static, 0,
                 color='red', alpha=0.08,
                 label='Long-wavelength (applied later)')

# Mark the three CMP locations
for idx in cmp_indices:
    ax2.axvline(x=x[idx], color='grey', linestyle=':', linewidth=0.8)

# Label one of the CMP lines
ax2.text(x[cmp_indices[1]] + 80, np.max(total_static) * 0.9,
         'CMP locations', color='grey', fontsize=9, rotation=90, va='top')

ax2.set_xlabel('CMP position (m)')
ax2.set_ylabel('Static shift (ms)')
ax2.set_title('(b) Statics decomposition')
ax2.legend(fontsize=8, loc='upper right')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/term01_lec04/term01_lec04_floating_datum.png',
            dpi=150, bbox_inches='tight')
plt.close()
print('Saved: term01_lec04_floating_datum.png')
