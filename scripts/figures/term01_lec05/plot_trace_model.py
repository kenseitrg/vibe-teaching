"""
Trace model: from a continuous analog signal to a finite digital trace.

This figure illustrates the two key steps that turn a continuous analog
seismic recording into the finite digital trace stored in the computer:

1. Sampling: keep only the values at regular intervals  Delta t .
2. Windowing: keep only a finite interval of length  T = N Delta t .

Parameters are typical for seismic reflection data:
    Delta t = 4 ms  (sample interval)
    T       = 2.0 s (record/window length)
    N       = 500   (number of samples in the window)
"""

import numpy as np
import matplotlib.pyplot as plt

# Figure parameters
FIG_WIDTH = 10.0   # inches
FIG_HEIGHT = 6.0   # inches
DPI = 150
OUTPUT_PATH = "figures/term01_lec05/term01_lec05_trace_model.png"

# Signal parameters (realistic for seismic data)
DT = 0.004          # sample interval, seconds (4 ms)
T = 2.0             # window length, seconds
N = int(T / DT)     # number of samples in the finite window (500)

FS_CONTINUOUS = 10000.0  # fine sampling rate for the smooth analog curve, Hz

# Total analog time axis: a bit longer than the window so students can see
# the window being selected in the last panel.
T_EXTRA = 0.5       # extra time on each side of the window, seconds
T_START = -T_EXTRA
T_END = T + T_EXTRA

# Component frequencies for the synthetic seismic-like trace (Hz)
F1 = 10.0
F2 = 25.0
F3 = 40.0

# Build the continuous analog signal
t_continuous = np.arange(T_START, T_END, 1.0 / FS_CONTINUOUS)
# Sum of a few sinusoids plus a very small linear amplitude trend
signal = (
    0.6 * np.sin(2 * np.pi * F1 * t_continuous)
    + 0.4 * np.sin(2 * np.pi * F2 * t_continuous)
    + 0.2 * np.sin(2 * np.pi * F3 * t_continuous)
    + 0.05 * (t_continuous / T)  # tiny trend
)

# Discrete sampling grid (extends beyond the final window for panel 2)
t_sampled = np.arange(T_START, T_END + DT, DT)
signal_sampled = (
    0.6 * np.sin(2 * np.pi * F1 * t_sampled)
    + 0.4 * np.sin(2 * np.pi * F2 * t_sampled)
    + 0.2 * np.sin(2 * np.pi * F3 * t_sampled)
    + 0.05 * (t_sampled / T)
)

# Finite digital trace: only the N samples inside [0, T)
t_digital = np.arange(0, T, DT)
signal_digital = (
    0.6 * np.sin(2 * np.pi * F1 * t_digital)
    + 0.4 * np.sin(2 * np.pi * F2 * t_digital)
    + 0.2 * np.sin(2 * np.pi * F3 * t_digital)
    + 0.05 * (t_digital / T)
)

# Colorblind-friendly colors (from Matplotlib's tab10, safe for color vision)
COLOR_CURVE = "#0072B2"      # blue
COLOR_LIGHT = "#BBBBBB"      # light gray for the background curve
COLOR_SAMPLES = "#D55E00"    # vermillion for sample points

# Create the figure with three stacked panels
fig, axes = plt.subplots(3, 1, figsize=(FIG_WIDTH, FIG_HEIGHT), sharex=True)
fig.suptitle(
    "From a continuous analog signal to a finite digital trace",
    fontsize=13,
    fontweight="bold",
)

# --- Panel 1: continuous analog signal ---
ax0 = axes[0]
ax0.plot(t_continuous, signal, color=COLOR_CURVE, linewidth=1.5, label="Analog signal")
ax0.set_ylabel("Amplitude")
ax0.set_title("Continuous analog signal")
ax0.set_xlim(T_START, T_END)
ax0.grid(True, linestyle=":", alpha=0.6)

# --- Panel 2: sampled signal ---
ax1 = axes[1]
# Background: the continuous curve in light gray
ax1.plot(t_continuous, signal, color=COLOR_LIGHT, linewidth=1.0, zorder=1)
# Overlay: discrete samples as stems + dots
markerline, stemlines, baseline = ax1.stem(
    t_sampled,
    signal_sampled,
    linefmt=COLOR_SAMPLES,
    markerfmt="o",
    basefmt="k-",
)
plt.setp(stemlines, "linewidth", 0.8, "alpha", 0.7)
plt.setp(markerline, "markersize", 3.5, "color", COLOR_SAMPLES)
ax1.set_ylabel("Amplitude")
ax1.set_title(r"Sampled signal, $\Delta t$ = 4 ms")
ax1.grid(True, linestyle=":", alpha=0.6)

# --- Panel 3: finite digital trace ---
ax2 = axes[2]
markerline, stemlines, baseline = ax2.stem(
    t_digital,
    signal_digital,
    linefmt=COLOR_SAMPLES,
    markerfmt="o",
    basefmt="k-",
)
plt.setp(stemlines, "linewidth", 1.0, "alpha", 0.8)
plt.setp(markerline, "markersize", 4.0, "color", COLOR_SAMPLES)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Amplitude")
ax2.set_title(r"Finite digital trace, $T$ = 2.0 s, $N$ = 500 samples")
ax2.grid(True, linestyle=":", alpha=0.6)

# Add a caption-like text below the figure
fig.text(
    0.5,
    0.01,
    (
        r"Sampling selects points at interval $\Delta t$; "
        r"the finite window selects only the interval of length $T = N\Delta t$."
    ),
    ha="center",
    fontsize=10,
    style="italic",
)

plt.tight_layout(rect=[0, 0.04, 1, 0.96])
plt.savefig(OUTPUT_PATH, dpi=DPI, bbox_inches="tight")
plt.close()

print(f"Saved figure to {OUTPUT_PATH}")
print(f"Parameters: Delta t = {DT*1000:.0f} ms, T = {T} s, N = {len(t_digital)} samples")
