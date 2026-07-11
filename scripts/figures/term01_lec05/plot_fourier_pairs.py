"""
Ricker wavelet and its amplitude spectrum: continuous versus DFT.

This figure shows a 25 Hz Ricker wavelet in time and its amplitude spectrum.
The smooth curve is the continuous (analytic) amplitude spectrum. The DFT
samples that curve at the discrete frequencies f_k = k/T, where T is the
window length. A longer window gives finer frequency spacing:
    T = 2.0 s  ->  Delta f = 1/T = 0.5 Hz
    T = 0.5 s  ->  Delta f = 1/T = 2.0 Hz
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Figure settings ---
FIG_WIDTH = 10.0   # inches
FIG_HEIGHT = 6.0   # inches
DPI = 150
OUTPUT_PATH = "figures/term01_lec05/term01_lec05_fourier_pairs.png"

# --- Seismic / signal parameters ---
DT = 0.004          # sample interval, seconds (4 ms)
FP = 25.0           # Ricker peak frequency, Hz
T_FULL = 2.0        # full window length, seconds
T_CROP = 0.5        # cropped window length, seconds
N_FULL = int(T_FULL / DT)   # 500 samples
N_CROP = int(T_CROP / DT)   # 125 samples

# Center the Ricker pulse in both windows
T_CENTER = 0.5 * T_FULL     # 1.0 s


def ricker(t, fp, t_center):
    """Ricker wavelet centered at t_center with peak frequency fp."""
    tau = t - t_center
    a = np.pi * fp * tau
    return (1.0 - 2.0 * a**2) * np.exp(-a**2)


# --- Time-domain wavelets ---
t_full = np.linspace(0.0, T_FULL - DT, N_FULL)
t_crop = np.linspace(
    T_CENTER - 0.5 * T_CROP,
    T_CENTER + 0.5 * T_CROP - DT,
    N_CROP,
)

w_full = ricker(t_full, FP, T_CENTER)
w_crop = ricker(t_crop, FP, T_CENTER)

# --- Frequency-domain spectra ---
# Continuous analytic amplitude spectrum, proportional to f^2 exp(-f^2/fp^2)
f = np.linspace(0.0, 100.0, 1000)
A_continuous = f**2 * np.exp(-f**2 / FP**2)
A_continuous = A_continuous / np.max(A_continuous)  # normalize to peak = 1

# DFT of the full window (one-sided), normalized to its own peak
W_full = np.fft.rfft(w_full)
f_full = np.fft.rfftfreq(N_FULL, DT)
A_full = np.abs(W_full)
A_full = A_full / np.max(A_full)
mask_full = f_full <= 100.0

# DFT of the cropped window (one-sided), normalized to its own peak
W_crop = np.fft.rfft(w_crop)
f_crop = np.fft.rfftfreq(N_CROP, DT)
A_crop = np.abs(W_crop)
A_crop = A_crop / np.max(A_crop)
mask_crop = f_crop <= 100.0

# --- Plotting ---
fig, axes = plt.subplots(2, 1, figsize=(FIG_WIDTH, FIG_HEIGHT))

# Top panel: time-domain wavelet
ax_time = axes[0]
ax_time.plot(
    t_full, w_full,
    color="#BBBBBB", linewidth=1.0,
    label="Full window, $T$ = 2.0 s",
)
ax_time.plot(
    t_crop, w_crop,
    color="#0072B2", linewidth=2.5,
    label="Cropped window, $T$ = 0.5 s",
)
ax_time.set_xlabel("Time (s)")
ax_time.set_ylabel("Amplitude")
ax_time.set_title(r"Ricker wavelet, $f_p$ = 25 Hz, $\Delta t$ = 4 ms")
ax_time.grid(True, linestyle=":", alpha=0.6)
ax_time.legend(loc="upper right")

# Bottom panel: amplitude spectrum
ax_freq = axes[1]
ax_freq.plot(
    f, A_continuous,
    color="#0072B2", linewidth=2.0,
    label="Ricker amplitude spectrum (continuous)",
)
ax_freq.plot(
    f_full[mask_full], A_full[mask_full],
    "o", color="#D55E00", markersize=4.5,
    label=r"DFT, $T$ = 2.0 s, $\Delta f$ = 0.5 Hz",
)
ax_freq.plot(
    f_crop[mask_crop], A_crop[mask_crop],
    "s", color="#009E73", markersize=7.0,
    label=r"DFT, $T$ = 0.5 s, $\Delta f$ = 2.0 Hz",
)
ax_freq.set_xlabel("Frequency (Hz)")
ax_freq.set_ylabel("Amplitude")
ax_freq.set_title(r"DFT samples the continuous spectrum at $f_k = k/T$")
ax_freq.set_xlim(0.0, 100.0)
ax_freq.grid(True, linestyle=":", alpha=0.6)
ax_freq.legend(loc="upper right")

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=DPI, bbox_inches="tight")
plt.close()

print(f"Saved figure to {OUTPUT_PATH}")
print(f"Parameters: Δt = {DT*1000:.0f} ms, fp = {FP:.0f} Hz, "
      f"T_full = {T_FULL:.1f} s, T_crop = {T_CROP:.1f} s")
print(f"DFT frequency spacing: full = {1.0/T_FULL:.1f} Hz, "
      f"cropped = {1.0/T_CROP:.1f} Hz")
