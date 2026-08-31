"""
Gibbs phenomenon: sharp frequency cutoffs produce ringing in the time domain.

This figure has two parts:

1. Left panel: Fourier series reconstruction of an ideal low-pass boxcar. As
   more cosine terms are added, the partial sums converge toward the boxcar,
   but the overshoot/ringing near the abrupt cutoff (the Gibbs phenomenon)
   remains visible.

2. Right panel: three low-pass filters and their symmetric impulse responses.
   All filters are designed manually in the frequency domain and converted to
   the time domain via inverse FFT. The ideal boxcar has the strongest
   ringing; the steep-slope filter has a narrow transition band and still
   rings; the smooth-slope filter has a wide transition band and much less
   ringing.

Sampling parameters: Δt = 4 ms, fs = 250 Hz, fN = 125 Hz, low-pass cutoff
fc = 50 Hz.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# --- Figure settings ---
FIG_WIDTH = 15.0
FIG_HEIGHT = 6.0
DPI = 150
OUTPUT_PATH = "figures/term01_lec05/term01_lec05_gibbs.png"

# --- Seismic sampling parameters ---
DT = 0.004          # sample interval (4 ms)
FS = 1.0 / DT       # sampling frequency (250 Hz)
F_N = FS / 2.0      # Nyquist frequency (125 Hz)
F_C = 50.0          # low-pass cutoff frequency (Hz)

# --- Impulse response length ---
N_FFT = 201         # number of samples (odd for symmetric center)

# --- Colorblind-friendly palette ---
COLOR_TARGET = "#000000"       # black for the ideal boxcar target
COLOR_BOXCAR = "#0072B2"       # blue (ideal boxcar / sinc)
COLOR_SHARP = "#D55E00"        # vermilion (sharp slope)
COLOR_SMOOTH = "#009E73"       # teal (smooth slope)
COLOR_PASSBAND = "#E5E5E5"     # light gray for passband shading


def boxcar_fourier_series(f, N_terms, f_c, f_n):
    """
    Partial Fourier series reconstruction of an ideal boxcar low-pass
    response defined on [-f_n, f_n] with cutoff f_c.

    The series is
        H_N(f) = f_c/f_n + Σ_{k=1}^{N} (2/(kπ)) sin(kπ f_c/f_n) cos(kπ f/f_n).
    """
    # DC term a0/2
    h = np.full_like(f, f_c / f_n)

    # Cosine terms
    for k in range(1, N_terms + 1):
        a_k = (2.0 / (k * np.pi)) * np.sin(k * np.pi * f_c / f_n)
        h += a_k * np.cos(k * np.pi * f / f_n)

    return h


def design_filter_freqdomain(f_c, f_stop, fs, n_fft):
    """
    Design a low-pass filter in the frequency domain.

    The filter is defined as:
        H(f) = 1              for |f| <= f_c
        H(f) = cosine taper   for f_c < |f| < f_stop
        H(f) = 0              for |f| >= f_stop

    The taper is a raised cosine (Hann-like) for a smooth transition.
    Returns the impulse response (centered, symmetric) via inverse FFT.
    """
    freq = np.fft.fftfreq(n_fft, d=1.0/fs)
    H = np.zeros(n_fft, dtype=complex)

    for i, f in enumerate(np.abs(freq)):
        if f <= f_c:
            H[i] = 1.0
        elif f < f_stop:
            # Cosine taper from 1 to 0 over [f_c, f_stop]
            t = (f - f_c) / (f_stop - f_c)
            H[i] = 0.5 * (1.0 + np.cos(np.pi * t))
        else:
            H[i] = 0.0

    # Inverse FFT to get impulse response
    h = np.fft.ifft(H).real
    h = np.fft.fftshift(h)  # center the impulse response

    return h


def design_ideal_boxcar(f_c, fs, n_fft):
    """
    Design an ideal boxcar low-pass filter in the frequency domain.
    Returns the impulse response (centered, symmetric) via inverse FFT.
    """
    freq = np.fft.fftfreq(n_fft, d=1.0/fs)
    H = np.where(np.abs(freq) <= f_c, 1.0, 0.0)

    h = np.fft.ifft(H).real
    h = np.fft.fftshift(h)

    return h


# --- Build the figure ---
fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
gs_outer = GridSpec(1, 2, figure=fig, width_ratios=[1, 1.8], wspace=0.28)

# -------------------------------------------------------------------------
# Left panel: Fourier series approximation of a boxcar
# -------------------------------------------------------------------------
ax_left = fig.add_subplot(gs_outer[0, 0])

f_left = np.linspace(-F_N, F_N, 2000)

# Plot the target boxcar as dark horizontal segments with vertical transitions
ax_left.plot([-F_N, -F_C], [0, 0], color=COLOR_TARGET, linewidth=2.0,
             label="Boxcar target")
ax_left.plot([-F_C, -F_C], [0, 1], color=COLOR_TARGET, linewidth=2.0)
ax_left.plot([-F_C, F_C], [1, 1], color=COLOR_TARGET, linewidth=2.0)
ax_left.plot([F_C, F_C], [1, 0], color=COLOR_TARGET, linewidth=2.0)
ax_left.plot([F_C, F_N], [0, 0], color=COLOR_TARGET, linewidth=2.0)

# Overlay partial sums with progressively darker colors
N_terms_list = [5, 15, 45, 100]
blues = plt.get_cmap("Blues")
partial_sum_colors = [blues(0.40), blues(0.55), blues(0.70), blues(0.90)]

for N_terms, color in zip(N_terms_list, partial_sum_colors):
    H_partial = boxcar_fourier_series(f_left, N_terms, F_C, F_N)
    ax_left.plot(f_left, H_partial, color=color, linewidth=1.5,
                 label=f"N = {N_terms} terms")

ax_left.set_xlim(-F_N, F_N)
ax_left.set_ylim(-0.2, 1.2)
ax_left.set_xlabel("Frequency (Hz)")
ax_left.set_ylabel("Amplitude")
ax_left.set_title("Fourier series approximation of a boxcar")
ax_left.grid(True, linestyle=":", alpha=0.6)
ax_left.legend(loc="upper right", fontsize=8)

# -------------------------------------------------------------------------
# Right panel: 3 rows × 2 columns
# Left column: amplitude response; Right column: impulse response
# -------------------------------------------------------------------------
gs_right = gs_outer[0, 1].subgridspec(3, 2, hspace=0.45, wspace=0.25)

# Common time axis for all impulse responses
n_time = np.arange(N_FFT)
t_time = n_time * DT  # time in seconds

# --- Row 1: Ideal boxcar (sharp cutoff) ---
ax_freq1 = fig.add_subplot(gs_right[0, 0])
ax_time1 = fig.add_subplot(gs_right[0, 1])

h_ideal = design_ideal_boxcar(F_C, FS, N_FFT)
freq_axis = np.fft.fftfreq(N_FFT, d=1.0/FS)
freq_shifted = np.fft.fftshift(freq_axis)
H_ideal_shifted = np.fft.fftshift(np.fft.fft(h_ideal))

ax_freq1.axvspan(0, F_C, color=COLOR_PASSBAND, alpha=0.4)
ax_freq1.plot(freq_shifted, np.abs(H_ideal_shifted), color=COLOR_BOXCAR,
              linewidth=2.0)
ax_freq1.set_xlim(0, F_N)
ax_freq1.set_ylim(0, 1.05)
ax_freq1.set_title("Ideal boxcar (sharp cutoff)")
ax_freq1.set_ylabel("Amplitude")
ax_freq1.grid(True, linestyle=":", alpha=0.6)

ax_time1.plot(t_time, h_ideal, color=COLOR_BOXCAR, linewidth=1.2)
ax_time1.set_xlim(0, t_time[-1])
ax_time1.set_title("Truncated sinc impulse response")
ax_time1.set_ylabel("Amplitude")
ax_time1.grid(True, linestyle=":", alpha=0.6)

# --- Row 2: Sharp slope (narrow transition band) ---
ax_freq2 = fig.add_subplot(gs_right[1, 0])
ax_time2 = fig.add_subplot(gs_right[1, 1])

h_sharp = design_filter_freqdomain(F_C, F_C + 5.0, FS, N_FFT)  # 50-55 Hz
H_sharp_shifted = np.fft.fftshift(np.fft.fft(h_sharp))

ax_freq2.axvspan(0, F_C, color=COLOR_PASSBAND, alpha=0.4)
ax_freq2.plot(freq_shifted, np.abs(H_sharp_shifted), color=COLOR_SHARP,
              linewidth=2.0)
ax_freq2.set_xlim(0, F_N)
ax_freq2.set_ylim(0, 1.05)
ax_freq2.set_title("Sharp slope")
ax_freq2.set_ylabel("Amplitude")
ax_freq2.grid(True, linestyle=":", alpha=0.6)

ax_time2.plot(t_time, h_sharp, color=COLOR_SHARP, linewidth=1.2)
ax_time2.set_xlim(0, t_time[-1])
ax_time2.set_title("Impulse response")
ax_time2.set_ylabel("Amplitude")
ax_time2.grid(True, linestyle=":", alpha=0.6)

# --- Row 3: Smooth slope (wide transition band) ---
ax_freq3 = fig.add_subplot(gs_right[2, 0])
ax_time3 = fig.add_subplot(gs_right[2, 1])

h_smooth = design_filter_freqdomain(F_C, F_C + 30.0, FS, N_FFT)  # 50-80 Hz
H_smooth_shifted = np.fft.fftshift(np.fft.fft(h_smooth))

ax_freq3.axvspan(0, F_C, color=COLOR_PASSBAND, alpha=0.4)
ax_freq3.plot(freq_shifted, np.abs(H_smooth_shifted), color=COLOR_SMOOTH,
              linewidth=2.0)
ax_freq3.set_xlim(0, F_N)
ax_freq3.set_ylim(0, 1.05)
ax_freq3.set_title("Smooth slope")
ax_freq3.set_xlabel("Frequency (Hz)")
ax_freq3.set_ylabel("Amplitude")
ax_freq3.grid(True, linestyle=":", alpha=0.6)

ax_time3.plot(t_time, h_smooth, color=COLOR_SMOOTH, linewidth=1.2)
ax_time3.set_xlim(0, t_time[-1])
ax_time3.set_title("Impulse response")
ax_time3.set_xlabel("Time (s)")
ax_time3.set_ylabel("Amplitude")
ax_time3.grid(True, linestyle=":", alpha=0.6)

fig.suptitle(
    "Gibbs phenomenon: sharp frequency cutoffs produce time-domain ringing",
    fontsize=12,
    y=0.98,
)

plt.savefig(OUTPUT_PATH, dpi=DPI, bbox_inches="tight")
plt.close()

print(f"Saved figure to {OUTPUT_PATH}")
print(f"Parameters: Δt = {DT*1000:.0f} ms, fs = {FS:.0f} Hz, "
      f"fN = {F_N:.0f} Hz, fc = {F_C:.0f} Hz")
print(f"Impulse response length: {N_FFT} samples")
print(f"Sharp slope: {F_C:.0f}-{F_C+5:.0f} Hz transition")
print(f"Smooth slope: {F_C:.0f}-{F_C+30:.0f} Hz transition")
