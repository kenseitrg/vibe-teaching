"""
First-break picking attributes on a noisy synthetic trace.

Output: figures/term03_lec02/term03_lec02_first_break_picking.png
"""

import numpy as np
import matplotlib.pyplot as plt

# Colorblind-friendly palette
COLORS = ["#0173B2", "#DE8F05", "#029E73", "#D55E00", "#CC79A7", "#F0E442"]

# Time axis (s), dt = 2 ms
dt = 0.002
t = np.arange(0, 0.5, dt)
n = len(t)

# True first break at ~0.12 s
t_fb = 0.12
idx_fb = int(t_fb / dt)

# Ricker wavelet
def ricker(f, t0):
    t_shifted = t - t0
    return (1 - 2 * (np.pi * f * t_shifted) ** 2) * np.exp(-(np.pi * f * t_shifted) ** 2)

# Signal: bandlimited pulse starting at first break, with a few later reflections
signal = np.zeros_like(t)
signal += ricker(20, t_fb)
signal += 0.4 * ricker(20, 0.22)
signal += 0.25 * ricker(20, 0.31)

# Noise
np.random.seed(42)
noise = 0.06 * np.random.randn(n)
noise[:idx_fb] *= 1.5  # stronger noise before first break
trace = signal + noise

# STA/LTA
sta_window = int(0.010 / dt)  # 10 ms short-term
lta_window = int(0.080 / dt)  # 80 ms long-term
sta = np.zeros(n)
lta = np.ones(n) * 1e-6
ratio = np.zeros(n)
for i in range(lta_window, n):
    sta[i] = np.mean(trace[i - sta_window:i] ** 2)
    lta[i] = np.mean(trace[i - lta_window:i] ** 2)
    ratio[i] = sta[i] / lta[i]

# Envelope via Hilbert transform
from scipy.signal import hilbert
envelope = np.abs(hilbert(trace))

fig, axes = plt.subplots(3, 1, figsize=(10, 6), sharex=True, dpi=150)

# Raw trace
ax = axes[0]
ax.plot(t, trace, color=COLORS[0], lw=0.8)
ax.axvline(t_fb, color=COLORS[3], ls="--", lw=1.5, label="True first break")
ax.set_ylabel("Amplitude")
ax.set_title("Raw trace")
ax.legend(loc="upper right")
ax.set_xlim(0, 0.45)
ax.grid(alpha=0.3)

# STA/LTA ratio
ax = axes[1]
ax.plot(t, ratio, color=COLORS[1], lw=1.2)
ax.set_ylabel("STA/LTA")
ax.set_title("STA/LTA ratio")
ax.grid(alpha=0.3)

# Envelope
ax = axes[2]
ax.plot(t, envelope, color=COLORS[2], lw=1.2)
ax.set_ylabel("Envelope")
ax.set_xlabel("Time (s)")
ax.set_title("Trace envelope")
ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("figures/term03_lec02/term03_lec02_first_break_picking.png", dpi=150, bbox_inches="tight")
plt.close()
