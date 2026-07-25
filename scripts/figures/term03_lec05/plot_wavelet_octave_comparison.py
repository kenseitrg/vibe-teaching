"""
Term 3 Lecture 05 — Figure 1: Wavelet comparison across octave counts.

Pedagogical point
-----------------
Broadband seismic data is defined by the number of *octaves* of usable
bandwidth.  High frequencies control the central-lobe width (vertical
resolution); low frequencies control the side-lobe amplitude (event
isolation).  To isolate the effect of adding low octaves, all three
wavelets here share the SAME highest frequencies (64-80 Hz high end) and
differ only in how far the band extends toward low frequency.

We use zero-phase Ormsby wavelets (trapezoidal amplitude spectrum with four
corner frequencies f1 < f2 < f3 < f4).  Lowering f1 adds low octaves:
the central lobe narrows slightly and, more dramatically, the side lobes
collapse.  This is the visual definition of "broadband".

Octave count is log2(f3 / f1):
    6 octaves : f1 = 1  Hz  (broadband target, ~1-64 Hz)
    3 octaves : f1 = 8  Hz  (intermediate)
    2 octaves : f1 = 16 Hz  (conventional data)
All three use f3 = 64 Hz, f4 = 80 Hz.

Self-contained: numpy + matplotlib only.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Ormsby (trapezoidal-spectrum) zero-phase wavelet
# ---------------------------------------------------------------------------
def ormsby_wavelet(f_corners, dt, t_half):
    """Return a zero-phase Ormsby wavelet.

    Parameters
    ----------
    f_corners : tuple (f1, f2, f3, f4)
        Trapezoid corners in Hz: low ramp f1->f2, flat top f2->f3,
        high ramp f3->f4.
    dt : float
        Sampling interval in seconds.
    t_half : float
        Half-length of the returned time window in seconds.

    Returns
    -------
    t_ms : ndarray  -- two-sided time axis in milliseconds
    wavelet : ndarray -- zero-phase wavelet, peak-normalised to 1
    freqs : ndarray -- one-sided frequency axis in Hz
    amp : ndarray -- amplitude spectrum (trapezoid), peak = 1
    """
    f1, f2, f3, f4 = f_corners
    t = np.arange(-t_half, t_half + dt, dt)
    n = len(t)
    freqs = np.fft.rfftfreq(n, dt)

    # Build the trapezoidal amplitude spectrum.
    amp = np.zeros_like(freqs)
    amp[(freqs >= f2) & (freqs <= f3)] = 1.0
    m = (freqs >= f1) & (freqs < f2)
    amp[m] = (freqs[m] - f1) / (f2 - f1)
    m = (freqs > f3) & (freqs <= f4)
    amp[m] = (f4 - freqs[m]) / (f4 - f3)

    # Zero phase: keep amplitude, set phase to zero, inverse FFT.
    wavelet = np.fft.irfft(amp, n=n)
    wavelet = np.fft.fftshift(wavelet)          # centre the peak at t = 0
    wavelet /= np.max(np.abs(wavelet))           # normalise peak to 1
    return t * 1000.0, wavelet, freqs, amp


# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------
dt = 0.001          # 1 ms sampling
t_half = 0.200      # +/- 200 ms window

# (label, corners, color).  Ordered top -> bottom from conventional to broadband.
# Wong colorblind-safe palette.
cases = [
    ("2 octaves  (conventional)",  (16, 24, 64, 80), "#CC79A7"),
    ("3 octaves  (intermediate)",  (8,  12, 64, 80), "#E69F00"),
    ("6 octaves  (broadband)",     (1,  2,  64, 80), "#0072B2"),
]

fig, axes = plt.subplots(
    len(cases), 2, figsize=(10, 6),
    gridspec_kw={"width_ratios": [1.0, 1.1], "hspace": 0.5, "wspace": 0.25},
)

f_shared_lo, f_shared_hi = 64, 80   # the high end shared by every wavelet

for row, (label, corners, color) in enumerate(cases):
    f1, f2, f3, f4 = corners
    t_ms, w, freqs, amp = ormsby_wavelet(corners, dt, t_half)
    octaves = np.log2(f3 / f1)

    # ---- Left: time-domain wavelet --------------------------------------
    ax_t = axes[row, 0]
    ax_t.plot(t_ms, w, color=color, lw=1.8)
    ax_t.axhline(0, color="grey", lw=0.6, zorder=0)
    ax_t.axvline(0, color="grey", lw=0.6, ls=":")
    ax_t.set_xlim(-130, 130)
    ax_t.set_ylim(-0.55, 1.12)
    ax_t.set_ylabel("Amplitude\n(normalised)")
    ax_t.set_title(f"{label}", loc="left", fontsize=11, fontweight="bold",
                   color=color)
    ax_t.text(0.98, 0.92, f"~{octaves:.0f} octaves\n$f_1$ = {f1} Hz",
              transform=ax_t.transAxes, ha="right", va="top", fontsize=9,
              bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=color, lw=1))
    if row == len(cases) - 1:
        ax_t.set_xlabel("Two-way time (ms)")

    # ---- Right: amplitude spectrum --------------------------------------
    ax_f = axes[row, 1]
    ax_f.fill_between(freqs, amp, color=color, alpha=0.25)
    ax_f.plot(freqs, amp, color=color, lw=1.8)
    # shade the high-frequency band shared by all three wavelets
    ax_f.axvspan(f_shared_lo, f_shared_hi, color="lightgrey", alpha=0.5,
                 zorder=0)
    ax_f.scatter([f1, f2, f3, f4], [0, 1, 1, 0], color=color, s=22, zorder=5)
    ax_f.annotate(f"$f_1$={f1}", (f1, 0), textcoords="offset points",
                  xytext=(0, -14), ha="center", fontsize=8, color=color)
    ax_f.set_xlim(0, 100)
    ax_f.set_ylim(0, 1.15)
    ax_f.set_ylabel("Amplitude\nspectrum")
    if row == 0:
        ax_f.annotate("shared high end\n(64-80 Hz, identical)",
                      (72, 1.0), textcoords="offset points",
                      xytext=(6, -6), ha="left", va="top", fontsize=8,
                      color="dimgrey")
    if row == len(cases) - 1:
        ax_f.set_xlabel("Frequency (Hz)")

fig.suptitle(
    "Broadband wavelet comparison: with the high end fixed (64-80 Hz), adding low octaves\n"
    "keeps the central lobe (resolution) nearly constant but collapses the side lobes (better isolation)",
    fontsize=12, y=1.00,
)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
out_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                       "figures", "term03_lec05")
out_dir = os.path.abspath(out_dir)
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "term03_lec05_wavelet_octave_comparison.png")
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"Saved figure to {out_path}")
