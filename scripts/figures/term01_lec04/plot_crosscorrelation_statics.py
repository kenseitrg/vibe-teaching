"""
Cross-correlation residual statics estimation.

Shows:
  Top panel: a reference trace and a shifted trace.
  Bottom panel: cross-correlation function with the lag of the
  maximum correlation marked as the estimated static shift.

Undergraduate seismic data processing — Term 1 Lecture 04.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Parameters -----------------------------------------------------------
dt = 0.002                # time sampling (s)
t_max = 1.0               # trace duration (s)
t = np.arange(0, t_max, dt)
nt = len(t)

# Wavelet: Ricker (Mexican hat) pulse
f0 = 25.0                 # dominant frequency (Hz)
tau = t - 0.3             # centre wavelet at 0.3 s
wavelet = (1 - 2 * (np.pi * f0 * tau) ** 2) * \
          np.exp(-(np.pi * f0 * tau) ** 2)
wavelet = wavelet / np.max(np.abs(wavelet))   # normalise

# Reference trace: add a little noise
np.random.seed(42)
ref_trace = wavelet.copy()

# Shifted trace: static shift of 10 samples = 20 ms
true_shift_samples = 10
true_shift_time = true_shift_samples * dt  # 0.020 s
shifted_trace = np.roll(wavelet, true_shift_samples)
# Zero-pad the rolled part
if true_shift_samples > 0:
    shifted_trace[:true_shift_samples] = 0
else:
    shifted_trace[true_shift_samples:] = 0
# Add a bit of random noise
shifted_trace += 0.05 * np.random.randn(nt)

# --- Cross-correlation ----------------------------------------------------
corr = np.correlate(ref_trace, shifted_trace, mode='same')
lags = (np.arange(nt) - nt // 2) * dt
lag_samples = np.arange(nt) - nt // 2

# Find peak correlation lag
peak_idx = np.argmax(corr)
estimated_shift = lags[peak_idx]
estimated_shift_samples = lag_samples[peak_idx]

# --- Plot ----------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5),
                                gridspec_kw={'height_ratios': [1, 1]})
fig.suptitle('Residual statics by cross-correlation', fontsize=14)

# Top: traces
ax1.plot(t, ref_trace, 'k-', linewidth=1.8, label='Reference trace')
ax1.plot(t, shifted_trace, 'C0-', linewidth=1.2, alpha=0.8,
         label='Shifted trace')
ax1.axvline(x=0.3, color='grey', linestyle=':', linewidth=0.8)
ax1.axvline(x=0.3 + true_shift_time, color='C0', linestyle=':',
            linewidth=0.8)
ax1.annotate(f'True shift = {true_shift_time*1000:.0f} ms',
             xy=(0.3 + true_shift_time, 0.5),
             xytext=(0.3 + true_shift_time + 0.08, 0.7),
             fontsize=9, color='C0',
             arrowprops=dict(arrowstyle='->', color='C0'))
ax1.set_xlim(0.1, 0.6)
ax1.set_ylabel('Amplitude')
ax1.legend(fontsize=9, loc='upper right')
ax1.grid(True, alpha=0.3)

# Annotate individual trace labels
ax1.text(0.18, -0.8, 'Reference trace', fontsize=8, color='black',
         rotation=90, va='bottom', alpha=0.6)
ax1.text(0.18 + true_shift_time, -0.8, 'Shifted trace', fontsize=8,
         color='C0', rotation=90, va='bottom', alpha=0.6)

# Bottom: cross-correlation
ax2.plot(lags, corr, 'k-', linewidth=1.5)
# Mark the peak
ax2.axvline(x=estimated_shift, color='C0', linestyle='--', linewidth=1.5)
ax2.scatter(estimated_shift, corr[peak_idx], color='C0', s=60, zorder=5)
ax2.text(estimated_shift + 0.01, corr[peak_idx] * 0.95,
         f'Peak at {estimated_shift*1000:.0f} ms\n'
         f'(estimated static)',
         fontsize=9, color='C0', va='bottom')
ax2.axvline(x=0, color='grey', linestyle=':', linewidth=0.8,
            label='Zero lag')
ax2.set_xlabel('Lag (s)')
ax2.set_ylabel('Cross-correlation')
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figures/term01_lec04/term01_lec04_crosscorrelation_statics.png',
            dpi=150, bbox_inches='tight')
plt.close()
print('Saved: term01_lec04_crosscorrelation_statics.png')
