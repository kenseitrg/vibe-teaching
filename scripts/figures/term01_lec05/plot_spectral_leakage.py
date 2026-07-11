"""
Spectral leakage of a finite-windowed cosine.

A single cosine of frequency f0 observed through a finite rectangular window
has a sinc-shaped (Dirichlet) spectrum. When f0 is not an integer multiple of
the DFT frequency spacing 1/T, the spectral energy leaks into neighbouring
bins instead of being confined to a single frequency bin.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Figure settings ---
FIG_WIDTH = 10.0
FIG_HEIGHT = 6.0
DPI = 150
OUTPUT_PATH = "figures/term01_lec05/term01_lec05_spectral_leakage.png"

# --- Signal parameters ---
DT = 0.004          # sample interval, seconds (4 ms)
T = 2.0             # window length, seconds
N = int(T / DT)     # number of samples in the window (500)
F0 = 25.3           # cosine frequency, Hz (intentionally off-bin; spacing is 1/T = 0.5 Hz)
ZP_FACTOR = 16      # zero-padding factor for the smooth spectrum
N_ZP = N * ZP_FACTOR

DF = 1.0 / T        # DFT frequency spacing, Hz

# --- Colorblind-friendly palette ---
COLOR_COSINE = "#0072B2"    # blue
COLOR_WINDOW = "#999999"    # gray
COLOR_CONT = "#009E73"      # teal/green
COLOR_DFT = "#D55E00"       # vermillion
COLOR_F0 = "#333333"        # dark gray

# --- Time-domain cosine inside the finite window ---
t = np.arange(0, N) * DT
cosine = np.cos(2.0 * np.pi * F0 * t)

# --- Rectangular window for the middle panel (wider time axis) ---
T_WIDE_START = -0.5
T_WIDE_END = T + 0.5
t_window = np.linspace(T_WIDE_START, T_WIDE_END, 1000)
window = np.where((t_window >= 0.0) & (t_window < T), 1.0, 0.0)

# --- Frequency-domain spectra ---
# Plain DFT of the N-sample windowed cosine
X = np.fft.rfft(cosine)
f = np.fft.rfftfreq(N, DT)

# Zero-padded DFT for the smooth continuous spectrum
x_zp = np.zeros(N_ZP)
x_zp[:N] = cosine
X_zp = np.fft.rfft(x_zp)
f_zp = np.fft.rfftfreq(N_ZP, DT)

# Normalize by N/2 so the peak of the positive-frequency lobe is approximately 1
norm = N / 2.0
A = np.abs(X) / norm
A_zp = np.abs(X_zp) / norm

# Focus on the positive-frequency peak, 0-60 Hz
F_MAX = 60.0
mask = f <= F_MAX
mask_zp = f_zp <= F_MAX

# --- Plotting ---
fig, axes = plt.subplots(3, 1, figsize=(FIG_WIDTH, FIG_HEIGHT))

# Top panel: cosine inside the finite window
ax0 = axes[0]
ax0.axvspan(0.0, T, color="#E5E5E5", alpha=0.7, zorder=0, label="Observation window")
ax0.plot(
    t, cosine,
    color=COLOR_COSINE, linewidth=1.2, zorder=1,
    label=f"Cosine, $f_0$ = {F0} Hz, $T$ = {T} s",
)
ax0.set_xlabel("Time (s)")
ax0.set_ylabel("Amplitude")
ax0.set_title("Cosine wave inside finite window")
ax0.set_xlim(T_WIDE_START, T_WIDE_END)
ax0.grid(True, linestyle=":", alpha=0.6)
ax0.legend(loc="upper right")

# Middle panel: rectangular window
ax1 = axes[1]
ax1.plot(t_window, window, color=COLOR_WINDOW, linewidth=2.0)
ax1.fill_between(t_window, 0.0, window, color=COLOR_WINDOW, alpha=0.3)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Window amplitude")
ax1.set_title("Rectangular window")
ax1.set_xlim(T_WIDE_START, T_WIDE_END)
ax1.set_ylim(-0.1, 1.2)
ax1.grid(True, linestyle=":", alpha=0.6)

# Bottom panel: amplitude spectrum
ax2 = axes[2]
ax2.plot(
    f_zp[mask_zp], A_zp[mask_zp],
    color=COLOR_CONT, linewidth=2.0,
    label="Continuous spectrum (zero-padded FFT)",
)
ax2.plot(
    f[mask], A[mask],
    "o", color=COLOR_DFT, markersize=5.0,
    label="DFT samples",
)
ax2.axvline(
    F0, color=COLOR_F0, linestyle="--", linewidth=1.0,
    label=r"True frequency $f_0$",
)
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Amplitude")
ax2.set_title("Sinc-shaped spectrum; energy leaks into neighbouring bins")
ax2.set_xlim(0.0, F_MAX)
ax2.grid(True, linestyle=":", alpha=0.6)
ax2.legend(loc="upper right")

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=DPI, bbox_inches="tight")
plt.close()

print(f"Saved figure to {OUTPUT_PATH}")
print(f"Parameters: Δt = {DT*1000:.0f} ms, T = {T:.1f} s, N = {N}, f0 = {F0} Hz")
print(f"DFT spacing Δf = {DF:.1f} Hz, zero-padding factor = {ZP_FACTOR}x")
