"""
Aliasing of a high-frequency cosine sampled below the Nyquist rate.

A 150 Hz cosine is sampled at 4 ms (fs = 250 Hz, fN = 125 Hz). Because the
signal frequency lies above the Nyquist frequency, the samples are identical to
those of a 100 Hz cosine. The spectrum shows the high-frequency energy folded
back into the principal band, appearing at the alias frequency of 100 Hz.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Figure settings ---
FIG_WIDTH = 10.0
FIG_HEIGHT = 6.0
DPI = 150
OUTPUT_PATH = "figures/term01_lec05/term01_lec05_aliasing.png"

# --- Signal parameters ---
DT = 0.004              # sample interval, seconds (4 ms)
FS = 1.0 / DT           # sampling frequency, Hz
F_N = FS / 2.0          # Nyquist frequency, Hz
T = 2.0                 # full window length for DFT, seconds
N = int(T / DT)         # number of samples for the DFT (500)
F_TRUE = 150.0          # true cosine frequency, Hz
F_ALIAS = FS - F_TRUE   # aliased frequency, Hz (100 Hz)

# --- Time-domain display window ---
T_START = 0.0
T_END = 0.06            # short window so the 150 Hz oscillation is visible

# --- Colorblind-friendly palette ---
COLOR_TRUE = "#0072B2"      # blue
COLOR_ALIAS = "#D55E00"     # vermillion
COLOR_SAMPLES = "#333333"   # dark gray
COLOR_NYQUIST = "#999999"   # gray
COLOR_BAND = "#E5E5E5"      # light gray shading

# --- Fine time axis for the continuous cosines ---
t_fine = np.linspace(T_START, T_END, 1000)
signal_true = np.cos(2.0 * np.pi * F_TRUE * t_fine)
signal_alias = np.cos(2.0 * np.pi * F_ALIAS * t_fine)

# --- Sample points ---
n_samples = int(np.floor(T_END / DT)) + 1
t_sample = np.arange(n_samples) * DT
x_sample = np.cos(2.0 * np.pi * F_TRUE * t_sample)

# --- Full-window signal for DFT ---
t_full = np.arange(N) * DT
x_full = np.cos(2.0 * np.pi * F_TRUE * t_full)

# DFT amplitude spectrum (single-sided, normalized)
X = np.fft.rfft(x_full)
freq = np.fft.rfftfreq(N, DT)
amp = np.abs(X) / (N / 2.0)     # normalize so a cosine peak is ~1

# --- Plotting ---
fig, axes = plt.subplots(2, 1, figsize=(FIG_WIDTH, FIG_HEIGHT))

# Top panel: time-domain aliasing
ax0 = axes[0]
ax0.plot(
    t_fine, signal_true,
    color=COLOR_TRUE, linewidth=1.0,
    label=f"{F_TRUE:.0f} Hz true signal",
)
ax0.plot(
    t_fine, signal_alias,
    color=COLOR_ALIAS, linewidth=2.5, linestyle="--",
    label=f"{F_ALIAS:.0f} Hz alias",
)
ax0.plot(
    t_sample, x_sample,
    "o", color=COLOR_SAMPLES, markersize=6.0,
    label=f"Samples at $\\Delta t$ = {DT*1000:.0f} ms",
)
ax0.set_xlabel("Time (s)")
ax0.set_ylabel("Amplitude")
ax0.set_title(
    f"A {F_TRUE:.0f} Hz cosine sampled at {DT*1000:.0f} ms looks like a {F_ALIAS:.0f} Hz cosine"
)
ax0.set_xlim(T_START, T_END)
ax0.set_ylim(-1.15, 1.15)
ax0.grid(True, linestyle=":", alpha=0.6)
ax0.legend(loc="upper right")

# Bottom panel: frequency-domain folding
ax1 = axes[1]
ax1.plot(
    freq, amp,
    color=COLOR_ALIAS, linewidth=2.0,
    label=f"Alias $f$ = {F_ALIAS:.0f} Hz",
)
ax1.axvline(
    F_TRUE, color=COLOR_TRUE, linestyle="--", linewidth=1.5,
    label=f"True frequency $f$ = {F_TRUE:.0f} Hz",
)
ax1.axvline(
    F_N, color=COLOR_NYQUIST, linestyle="--", linewidth=1.5,
    label=f"Nyquist $f_N$ = {F_N:.0f} Hz",
)
ax1.axvspan(0.0, F_N, color=COLOR_BAND, alpha=0.4, label="Principal band")
ax1.set_xlabel("Frequency (Hz)")
ax1.set_ylabel("Amplitude")
ax1.set_title(
    f"Spectrum folding: {F_TRUE:.0f} Hz energy appears at {F_ALIAS:.0f} Hz"
)
ax1.set_xlim(0.0, 175.0)
ax1.grid(True, linestyle=":", alpha=0.6)
ax1.legend(loc="upper right")

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=DPI, bbox_inches="tight")
plt.close()

print(f"Saved figure to {OUTPUT_PATH}")
print(f"Parameters: Δt = {DT*1000:.0f} ms, fs = {FS:.0f} Hz, fN = {F_N:.0f} Hz")
print(f"True frequency = {F_TRUE:.0f} Hz, alias frequency = {F_ALIAS:.0f} Hz")
print(f"DFT window: T = {T:.1f} s, N = {N} samples")
