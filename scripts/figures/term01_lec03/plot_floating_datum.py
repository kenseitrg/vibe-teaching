"""
Floating datum concept illustration.

Top panel:
  - Rugged topography (surface elevation)
  - Total statics (black solid)
  - Smoothed long-wavelength static (red dashed)
  - Floating-datum correction = total - smoothed (blue shaded)
Bottom panel:
  - CMP gather before correction (hyperbola shifted)
  - CMP gather after floating-datum correction (hyperbola at correct t0)
  - Annotation indicating long-wavelength part applied later.

Undergraduate seismic data processing — Term 1 Lecture 03.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Parameters -----------------------------------------------------------
nx = 150
x = np.linspace(0, 5000, nx)        # CMP positions (m)

# Surface elevation with gentle topography + a rugged short-wavelength bump
np.random.seed(42)
elevation = 40 * np.sin(0.0003 * 2 * np.pi * x) + \
            15 * np.sin(0.002 * 2 * np.pi * x) + \
            5 * np.random.randn(nx)

# Total statics proportional to elevation + weathering variations
weathering = 10 * np.sin(0.001 * 2 * np.pi * x) + \
             3 * np.random.randn(nx)
total_static = 0.7 * elevation + weathering   # rough proxy (ms)

# Smoothed static (long-wavelength component)
smoothing_window = 31
kernel = np.ones(smoothing_window) / smoothing_window
smoothed_static = np.convolve(total_static, kernel, mode='same')
smoothed_static[:smoothing_window // 2] = smoothed_static[smoothing_window // 2]
smoothed_static[-(smoothing_window // 2):] = smoothed_static[-(smoothing_window // 2)]

# Floating-datum correction = total - smoothed
floating_correction = total_static - smoothed_static

# --- Bottom: CMP gather illustration -------------------------------------
dt = 0.002
t_max = 2.0
t = np.arange(0, t_max, dt)
n_offsets = 25
offsets = np.linspace(100, 2500, n_offsets)

t0_true = 1.0
v_nmo = 2000.0

# Static shift applied to this specific CMP (pick a value)
shift_example = 45.0 / 1000  # 45 ms in seconds

t_true_curve = np.sqrt(t0_true**2 + (offsets / v_nmo)**2)
t_shifted_curve = np.sqrt((t0_true + shift_example)**2 + (offsets / v_nmo)**2)

# Create synthetic wiggles
def make_gather(times, offsets, t_vec, f0=25.0):
    nt = len(t_vec)
    no = len(offsets)
    gather = np.zeros((nt, no))
    wavelet_len = int(0.2 / dt)
    for k in range(no):
        idx = np.argmin(np.abs(t_vec - times[k]))
        start = max(0, idx - wavelet_len // 2)
        end = min(nt, idx + wavelet_len // 2)
        tau = t_vec[:end - start] - times[k]
        w = (1 - 2 * (np.pi * f0 * tau) ** 2) * \
            np.exp(-(np.pi * f0 * tau) ** 2)
        gather[start:end, k] = w[:end - start]
    return gather

gather_shifted = make_gather(t_shifted_curve, offsets, t)
gather_corrected = make_gather(t_true_curve, offsets, t)

# --- Plot ----------------------------------------------------------------
fig = plt.figure(figsize=(10, 7))
fig.suptitle('Floating datum concept', fontsize=14)

# Top panel
ax1 = plt.subplot(2, 1, 1)

# Plot components
ax1.plot(x, total_static, 'k-', linewidth=1.8, label='Total static')
ax1.plot(x, smoothed_static, 'r--', linewidth=2.5,
         label='Long-wavelength (smoothed)')
ax1.fill_between(x, floating_correction, 0,
                 where=(floating_correction > 0),
                 color='C0', alpha=0.3, label='Floating-datum correction')
ax1.fill_between(x, floating_correction, 0,
                 where=(floating_correction < 0),
                 color='C0', alpha=0.3)  # same colour for negative
# Add a second shaded region for the long-wavelength part
ax1.fill_between(x, smoothed_static, 0,
                 color='red', alpha=0.08, label='Long-wavelength (applied later)')

ax1.set_xlabel('CMP position (m)')
ax1.set_ylabel('Static shift (ms)')
ax1.set_title('(a) Statics decomposition')
ax1.legend(fontsize=8, loc='upper right')
ax1.grid(True, alpha=0.3)

# Mark CMP location used in bottom panel
cmp_mid = nx // 2  # approximately index 75
ax1.axvline(x=x[cmp_mid], color='grey', linestyle=':', linewidth=0.8,
            label='CMP for panel (b)')

# Bottom panel: two sub-panels side-by-side
ax2 = plt.subplot(2, 2, 3)
skip = 2
for k in range(0, n_offsets, skip):
    with np.errstate(divide='ignore', invalid='ignore'):
        amp = np.max(np.abs(gather_shifted[:, k]))
        norm = gather_shifted[:, k] / amp if amp > 0 else gather_shifted[:, k]
    ax2.plot(offsets[k] + norm * 300, t, 'grey', linewidth=0.5, alpha=0.7)
ax2.plot(offsets, t_shifted_curve, 'r-', linewidth=2,
         label=f'Shifted ($\\Delta t = {shift_example*1000:.0f}$ ms)')
ax2.plot(offsets, t_true_curve, 'k--', linewidth=1.5, label='True $t_0$')
ax2.set_xlabel('Offset (m)')
ax2.set_ylabel('Time (s)')
ax2.set_title('(b) Before floating datum')
ax2.invert_yaxis()
ax2.legend(fontsize=7)
ax2.grid(True, alpha=0.3)

ax3 = plt.subplot(2, 2, 4)
for k in range(0, n_offsets, skip):
    with np.errstate(divide='ignore', invalid='ignore'):
        amp = np.max(np.abs(gather_corrected[:, k]))
        norm = gather_corrected[:, k] / amp if amp > 0 else gather_corrected[:, k]
    ax3.plot(offsets[k] + norm * 300, t, 'C0', linewidth=0.5, alpha=0.7)
ax3.plot(offsets, t_true_curve, 'C0-', linewidth=2,
         label=f'Floating-datum corrected')
ax3.axhline(y=t0_true, color='grey', linestyle=':', linewidth=0.8)
ax3.set_xlabel('Offset (m)')
ax3.set_ylabel('Time (s)')
ax3.set_title('(c) After floating datum')
ax3.invert_yaxis()
ax3.legend(fontsize=7)
ax3.grid(True, alpha=0.3)

# Add annotation between (b) and (c)
fig.text(0.5, 0.31,
         'Floating-datum correction:\n'
         'remove short-wavelength (blue)\n'
         'keep long-wavelength (red) for later',
         ha='center', fontsize=10, style='italic', color='grey',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.tight_layout()
plt.savefig('figures/term01_lec03/term01_lec03_floating_datum.png',
            dpi=150, bbox_inches='tight')
plt.close()
print('Saved: term01_lec03_floating_datum.png')
