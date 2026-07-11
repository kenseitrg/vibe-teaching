"""
Amplitude spectra of low-pass, high-pass, band-pass, and notch filters.

Each panel shows the linear amplitude response of a 4th-order Butterworth
filter designed for seismic data sampled at 4 ms (Nyquist = 125 Hz). The
passband frequency regions are shaded lightly; the smooth slopes between the
passband and the stopband are the transition bands.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# --- Figure settings ---
FIG_WIDTH = 10.0
FIG_HEIGHT = 6.0
DPI = 150
OUTPUT_PATH = "figures/term01_lec05/term01_lec05_filter_types.png"

# --- Sampling and filter parameters ---
DT = 0.004          # sample interval, seconds (4 ms)
FS = 1.0 / DT       # sampling frequency, Hz
F_N = FS / 2.0      # Nyquist frequency, Hz
ORDER = 4           # Butterworth filter order

# Colorblind-friendly Okabe-Ito palette (one colour per subplot)
COLORS = {
    "Low-pass": "#0072B2",    # blue
    "High-pass": "#D55E00",   # vermilion
    "Band-pass": "#009E73",   # teal/green
    "Notch": "#CC79A7",       # pink
}

# Filter definitions: (title, btype, critical frequency/frequencies in Hz)
FILTERS = [
    ("Low-pass", "low", 50.0),
    ("High-pass", "high", 60.0),
    ("Band-pass", "band", (20.0, 60.0)),
    ("Notch", "bandstop", (45.0, 55.0)),
]


def design_response(btype, cutoff_hz, order=ORDER, fs=FS, fn=F_N):
    """Design a Butterworth filter and return its frequency response."""
    # Normalise cutoff(s) by the Nyquist frequency, as required by scipy.signal.butter
    if isinstance(cutoff_hz, tuple):
        wn = (cutoff_hz[0] / fn, cutoff_hz[1] / fn)
    else:
        wn = cutoff_hz / fn

    b, a = signal.butter(order, wn, btype=btype)
    freq, h = signal.freqz(b, a, worN=8192, fs=fs)
    amplitude = np.abs(h)
    return freq, amplitude


def shade_passband(ax, title, cutoff, fn=F_N, color=None):
    """Add a light shaded region for the filter passband."""
    if color is None:
        color = COLORS[title]

    if title == "Low-pass":
        ax.axvspan(0.0, cutoff, color=color, alpha=0.15, zorder=0)
    elif title == "High-pass":
        ax.axvspan(cutoff, fn, color=color, alpha=0.15, zorder=0)
    elif title == "Band-pass":
        ax.axvspan(cutoff[0], cutoff[1], color=color, alpha=0.15, zorder=0)
    elif title == "Notch":
        ax.axvspan(0.0, cutoff[0], color=color, alpha=0.15, zorder=0)
        ax.axvspan(cutoff[1], fn, color=color, alpha=0.15, zorder=0)


# --- Plotting ---
fig, axes = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(FIG_WIDTH, FIG_HEIGHT))
axes = axes.flatten()

for ax, (title, btype, cutoff) in zip(axes, FILTERS):
    color = COLORS[title]
    freq, amp = design_response(btype, cutoff)

    # Passband shading behind the curve
    shade_passband(ax, title, cutoff, color=color)

    # Amplitude response
    ax.plot(freq, amp, color=color, linewidth=2.0, zorder=1)

    ax.set_title(title)
    ax.set_xlim(0.0, F_N)
    ax.set_ylim(0.0, 1.05)
    ax.grid(True, linestyle=":", alpha=0.6)

# Shared axis labels
for ax in axes[2:]:  # bottom row
    ax.set_xlabel("Frequency (Hz)")
for ax in axes[::2]:  # left column
    ax.set_ylabel("Amplitude")

fig.suptitle("Amplitude spectra of common filter types")
plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=DPI, bbox_inches="tight")
plt.close()

print(f"Saved figure to {OUTPUT_PATH}")
print(f"Parameters: Δt = {DT*1000:.0f} ms, fs = {FS:.0f} Hz, fN = {F_N:.0f} Hz")
for title, btype, cutoff in FILTERS:
    print(f"  {title}: {cutoff} Hz")
