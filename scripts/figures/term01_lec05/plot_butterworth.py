"""
Butterworth low-pass amplitude responses for orders n = 2, 4, and 8.

Cutoff frequency fc = 60 Hz, sample interval dt = 4 ms (Nyquist = 125 Hz).
All three curves pass through -3 dB at fc. Higher order gives a steeper
roll-off in the transition band but produces a longer impulse response and
more ringing in the time domain.

Analytic expression:
    |H(f)| = 1 / sqrt(1 + (f/fc)^(2n))

The amplitude is converted to decibels: 20 * log10(|H(f)|).
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Figure settings ---
FIG_WIDTH = 10.0
FIG_HEIGHT = 6.0
DPI = 150
OUTPUT_PATH = "figures/term01_lec05/term01_lec05_butterworth.png"

# --- Filter parameters ---
DT = 0.004          # sample interval, seconds (4 ms)
FS = 1.0 / DT       # sampling frequency, Hz
F_NYQUIST = FS / 2  # Nyquist frequency, 125 Hz
F_CUTOFF = 60.0     # cutoff frequency, Hz

ORDERS = [2, 4, 8]  # Butterworth filter orders

# Okabe-Ito colourblind-friendly palette
COLORS = ["#0072B2", "#D55E00", "#009E73"]  # blue, vermilion, teal


def butterworth_response(f, fc, n):
    """Return the analytic Butterworth low-pass amplitude response in dB."""
    amplitude = 1.0 / np.sqrt(1.0 + (f / fc) ** (2 * n))
    return 20.0 * np.log10(amplitude)


# --- Compute frequency axis and responses ---
freq = np.linspace(0.0, F_NYQUIST, 2000)

responses = {}
for n in ORDERS:
    responses[n] = butterworth_response(freq, F_CUTOFF, n)

# --- Plotting ---
fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))

# Shade the passband (0 to fc)
ax.axvspan(0.0, F_CUTOFF, color="gray", alpha=0.08, zorder=0, label="_nolegend_")

# Reference lines
ax.axhline(-3.0, color="gray", linestyle="--", linewidth=0.8, alpha=0.7,
           label="_nolegend_")
ax.axvline(F_CUTOFF, color="gray", linestyle="--", linewidth=0.8, alpha=0.7,
           label="_nolegend_")

# Amplitude responses for each order
for n, color in zip(ORDERS, COLORS):
    ax.plot(freq, responses[n], color=color, linewidth=2.0,
            label=f"$n = {n}$")

# Axes
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Amplitude (dB)")
ax.set_title("Butterworth low-pass filter — amplitude response")
ax.set_xlim(0.0, F_NYQUIST)
ax.set_ylim(-60.0, 0.0)
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend(fontsize=12, loc="lower left")

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=DPI, bbox_inches="tight")
plt.close()

print(f"Saved figure to {OUTPUT_PATH}")
print(f"Parameters: dt = {DT*1000:.0f} ms, fs = {FS:.0f} Hz, "
      f"f_Nyquist = {F_NYQUIST:.0f} Hz, f_cutoff = {F_CUTOFF:.0f} Hz")
print(f"Butterworth orders: {ORDERS}")
for n in ORDERS:
    amp_90 = butterworth_response(90.0, F_CUTOFF, n)
    amp_120 = butterworth_response(120.0, F_CUTOFF, n)
    print(f"  n={n}: at 90 Hz = {amp_90:.1f} dB, at 120 Hz = {amp_120:.1f} dB")
