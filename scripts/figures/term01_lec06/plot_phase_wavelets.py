"""
Minimum-phase, zero-phase, and maximum-phase wavelets
with the same amplitude spectrum.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import minimum_phase


def design_bandpass_wavelet(dt: float, n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Design minimum-, zero-, and maximum-phase wavelets with the same amplitude spectrum."""
    nfft = 8 * n
    freqs = np.fft.rfftfreq(nfft, dt)
    # Smooth strictly-positive band-pass amplitude spectrum
    amp = np.ones_like(freqs)
    # Low-cut ramp 5-15 Hz
    amp *= 0.5 * (1 - np.cos(np.pi * np.clip((freqs - 5) / 10, 0, 1)))
    # High-cut ramp 55-75 Hz
    amp *= 0.5 * (1 + np.cos(np.pi * np.clip((freqs - 55) / 20, 0, 1)))
    # Add a small floor to keep spectrum strictly positive
    amp = np.maximum(amp, 0.02)

    # Zero-phase wavelet
    spec = np.zeros(nfft // 2 + 1, dtype=complex)
    spec[: len(amp)] = amp
    zp_full = np.fft.irfft(spec, n=nfft)
    zp = np.roll(zp_full, n // 2)[:n]

    # Minimum-phase wavelet: spectral factorization via scipy
    # Build a zero-phase FIR with the desired amplitude spectrum and odd length
    h = np.fft.irfft(amp, n=nfft)
    h = np.roll(h, nfft // 2)
    # Window to desired length and force symmetry
    h_win = h[nfft // 2 - n // 2 : nfft // 2 + n // 2]
    h_win = np.roll(h_win, len(h_win) // 2)
    h_win = np.convolve(h_win, h_win[::-1], mode="full")  # make zero-phase autocorrelation-like
    h_win = h_win[len(h_win) // 2 - n // 2 : len(h_win) // 2 + n // 2]
    # Now h_win is a zero-phase filter; compute its minimum-phase equivalent
    mp = minimum_phase(h_win, method="homomorphic", n_fft=8 * n, half=False)
    mp = mp[:n]

    # Maximum-phase = time-reversed minimum phase
    maxp = mp[::-1].copy()

    return zp, mp, maxp


def main():
    dt = 0.004
    n = 128
    t = (np.arange(n) - n // 2) * dt

    zp, mp, maxp = design_bandpass_wavelet(dt, n)

    # Normalize for display
    mp = mp / np.max(np.abs(mp))
    maxp = maxp / np.max(np.abs(maxp))
    zp = zp / np.max(np.abs(zp))

    fig, axes = plt.subplots(3, 1, figsize=(9, 6), sharex=True, sharey=True)

    for ax, w, title, color in zip(
        axes,
        [mp, zp, maxp],
        ["Minimum-phase", "Zero-phase", "Maximum-phase"],
        ["C0", "C1", "C2"],
    ):
        ax.plot(t * 1000, w, color=color)
        ax.fill_between(t * 1000, w, alpha=0.3, color=color)
        ax.set_ylabel("Amplitude")
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-1.1, 1.1)

    axes[-1].set_xlabel("Time (ms)")
    axes[-1].set_xlim(t[0] * 1000, t[-1] * 1000)

    fig.tight_layout()
    fig.savefig("figures/term01_lec06/term01_lec06_phase_wavelets.png", dpi=200)
    plt.close(fig)
    print("Saved figures/term01_lec06/term01_lec06_phase_wavelets.png")


if __name__ == "__main__":
    main()
