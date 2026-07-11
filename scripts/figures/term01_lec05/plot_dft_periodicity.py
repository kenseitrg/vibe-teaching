"""
DFT periodicity and real-signal symmetry for a real seismic trace.

This figure illustrates two fundamental properties of the DFT of a real-valued
seismic trace:

1. Periodicity: the DFT spectrum repeats every N bins, i.e. X[k + N] = X[k].
2. Complex-conjugate symmetry: for a real trace, X[-k] = X*[k], so the real
   part is even and the imaginary part is odd.

Parameters
----------
Delta t = 0.004 s  (4 ms sample interval)
T       = 2.0 s    (record window length)
N       = 500      (number of samples)
f_c     = 25 Hz    (Berlage / damped-sinusoid center frequency)
alpha   = 8.0 s^-1 (exponential envelope decay)
n       = 1        (t^n rise, n = 1 gives a causal pulse starting at 0)
f_N     = 125 Hz   (Nyquist frequency)
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Figure settings ---
FIG_WIDTH = 10.0
FIG_HEIGHT = 6.0
DPI = 150
OUTPUT_PATH = "figures/term01_lec05/term01_lec05_dft_periodicity.png"

# --- Seismic / signal parameters ---
DT = 0.004          # sample interval, seconds (4 ms)
T = 2.0             # window length, seconds
N = int(T / DT)     # number of samples (500)
FC = 25.0           # Berlage / damped-sinusoid center frequency, Hz
F_N = 1.0 / (2.0 * DT)  # Nyquist frequency, Hz
DF = 1.0 / T        # DFT frequency spacing, Hz
N_ORDER = 1         # t^n factor (n = 1 keeps the pulse causal and zero at t = 0)
ALPHA = 8.0         # exponential envelope decay, s^-1 (pulse decays to near zero before T)

# Colorblind-friendly palette
COLOR_WAVELET = "#0072B2"    # blue
COLOR_REPEAT = "#BBBBBB"     # light gray for periodic repeats
COLOR_IMAG = "#D55E00"       # vermillion for imaginary part
COLOR_DARK = "#333333"       # dark gray for reference lines


def berlage(t, fc, n_order, alpha):
    """Causal Berlage wavelet (t^n * exp(-alpha t) * sin(2 pi fc t))."""
    w = np.zeros_like(t)
    causal = t >= 0.0
    w[causal] = (t[causal] ** n_order) * np.exp(-alpha * t[causal]) * np.sin(2.0 * np.pi * fc * t[causal])
    return w


# --- Time-domain Berlage / damped-sinusoid wavelet ---
t = np.linspace(0.0, T - DT, N)
w = berlage(t, FC, N_ORDER, ALPHA)
w = w / np.max(np.abs(w))  # normalize peak amplitude to unity

# --- DFT of the real trace ---
X = np.fft.fft(w)

# --- Prepare the figure ---
fig, axes = plt.subplots(3, 1, figsize=(FIG_WIDTH, FIG_HEIGHT), sharex=False)

# Top panel: time-domain Berlage wavelet
ax0 = axes[0]
ax0.plot(t, w, color=COLOR_WAVELET, linewidth=1.5)
ax0.set_xlabel("Time (s)")
ax0.set_ylabel("Amplitude")
ax0.set_title(r"Real-valued seismic pulse (Berlage wavelet, $f_c$ = 25 Hz)")
ax0.grid(True, linestyle=":", alpha=0.6)
ax0.set_xlim(0.0, T)

# Middle panel: DFT periodicity of the amplitude spectrum
ax1 = axes[1]

# Plot two full periods of the amplitude spectrum, f = -2 f_N to +2 f_N
k_periods = np.arange(-N, N + 1)
bin_index = ((k_periods % N) + N) % N
amp_periods = np.abs(X[bin_index])
freq_periods = k_periods * DF

ax1.plot(
    freq_periods,
    amp_periods,
    color=COLOR_REPEAT,
    linewidth=1.0,
    label="Periodic repeats",
)

# Highlight the principal period, k = 0 to N (0 to 2 f_N)
k_principal = np.arange(0, N + 1)
amp_principal = np.abs(X[k_principal % N])
freq_principal = k_principal * DF
ax1.plot(
    freq_principal,
    amp_principal,
    color=COLOR_WAVELET,
    linewidth=2.5,
    label="Principal period",
)

# Mark period boundaries with subtle vertical dashed lines
for boundary in (-2 * F_N, -F_N, 0, F_N, 2 * F_N):
    ax1.axvline(boundary, color=COLOR_DARK, linestyle="--", linewidth=0.8, alpha=0.5)

ax1.set_xlabel("Frequency (Hz)")
ax1.set_ylabel(r"Amplitude $|X[k]|$")
ax1.set_title(r"DFT periodicity: $X[k+N] = X[k]$")
ax1.set_xlim(-2 * F_N, 2 * F_N)
ax1.set_xticks(
    [-2 * F_N, -3 * F_N / 2, -F_N, -F_N / 2, 0, F_N / 2, F_N, 3 * F_N / 2, 2 * F_N]
)
ax1.set_xticklabels(
    ["$-2f_N$", "$-3f_N/2$", "$-f_N$", "$-f_N/2$", "0", "$f_N/2$", "$f_N$", "$3f_N/2$", "$2f_N$"]
)
ax1.grid(True, linestyle=":", alpha=0.6)
ax1.legend(loc="upper right")

# Bottom panel: centered real and imaginary parts
ax2 = axes[2]

# Shift the DFT so frequencies run from -f_N to f_N - Delta f
X_shifted = np.fft.fftshift(X)
k_centered = np.arange(-N // 2, N // 2)
freq_centered = k_centered * DF

ax2.plot(
    freq_centered,
    X_shifted.real,
    color=COLOR_WAVELET,
    linestyle="-",
    linewidth=2.0,
    label="Real part",
)
ax2.plot(
    freq_centered,
    X_shifted.imag,
    color=COLOR_IMAG,
    linestyle="--",
    linewidth=2.0,
    label="Imaginary part",
)

# Mark DC, Nyquist and half-Nyquist positions
for boundary in (-F_N, -F_N / 2, 0, F_N / 2, F_N):
    ax2.axvline(boundary, color=COLOR_DARK, linestyle="--", linewidth=0.8, alpha=0.5)

ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Spectrum value")
ax2.set_title(r"Real-signal symmetry: $X[-k] = X^*[k]$")
ax2.set_xlim(-F_N, F_N)
ax2.set_xticks([-F_N, -F_N / 2, 0, F_N / 2, F_N])
ax2.set_xticklabels(["$-f_N$", "$-f_N/2$", "0", "$f_N/2$", "$f_N$"])
ax2.grid(True, linestyle=":", alpha=0.6)
ax2.legend(loc="upper right")

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=DPI, bbox_inches="tight")
plt.close()

print(f"Saved figure to {OUTPUT_PATH}")
print(f"Parameters: Delta t = {DT*1000:.0f} ms, T = {T:.1f} s, N = {N}, f_c = {FC:.0f} Hz")
print(f"Berlage: n = {N_ORDER}, alpha = {ALPHA:.1f} s^-1")
print(f"Nyquist frequency f_N = {F_N:.0f} Hz, frequency spacing Delta f = {DF:.1f} Hz")
