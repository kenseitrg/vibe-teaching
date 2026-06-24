"""
Deterministic deconvolution of a known minimum-phase wavelet.
Shows wavelet, inverse filter, and deconvolution output.
"""

import matplotlib.pyplot as plt
import numpy as np


def design_minimum_phase_wavelet(n: int, dt: float) -> np.ndarray:
    """Design a smooth band-limited minimum-phase wavelet by spectral factorization."""
    nfft = 16 * n
    freqs = np.fft.rfftfreq(nfft, dt)
    # Very smooth band-pass amplitude spectrum to reduce sidelobes
    amp = np.ones_like(freqs)
    # Cosine tapers: 5-15 Hz low-cut, 50-70 Hz high-cut
    amp *= 0.5 * (1 - np.cos(np.pi * np.clip((freqs - 5) / 10, 0, 1)))
    amp *= 0.5 * (1 + np.cos(np.pi * np.clip((freqs - 50) / 20, 0, 1)))
    amp = np.maximum(amp, 0.02)

    # Spectral factorization: take log amplitude, compute minimum-phase spectrum
    # via Hilbert transform, then inverse FFT.
    log_amp = np.log(amp)
    # Hilbert transform of log amplitude gives minimum-phase phase
    phase = -np.imag(np.fft.ifft(1j * np.sign(np.fft.fftfreq(nfft)) * np.fft.fft(
        np.concatenate([log_amp, log_amp[-2:0:-1]])  # full even spectrum
    )))
    # Build full complex spectrum (amplitude is symmetric, phase is antisymmetric)
    full_amp = np.concatenate([amp, amp[-2:0:-1]])
    full_phase = np.concatenate([phase[:len(amp)], -phase[len(amp)-2:0:-1]])
    spec_full = full_amp * np.exp(1j * full_phase)
    mp = np.fft.ifft(spec_full).real
    mp = mp[:n]
    mp = mp / np.max(np.abs(mp))
    return mp


def main():
    dt = 0.004
    n = 80
    eps = 0.10  # stronger prewhitening reduces sidelobe energy

    w = design_minimum_phase_wavelet(n, dt)

    # Fourier-domain deterministic inverse with prewhitening
    nfft = 1024
    W = np.fft.rfft(w, n=nfft)
    power = np.max(np.abs(W) ** 2)
    F = np.conj(W) / (np.abs(W) ** 2 + (eps ** 2) * power)
    inv = np.fft.irfft(F, n=nfft)
    # Keep enough of the causal inverse for a clean display
    inv = inv[:120]

    # Deconvolution output = convolution of wavelet with inverse filter.
    # For a causal minimum-phase wavelet and causal inverse, the spike is at time zero.
    out = np.convolve(w, inv, mode="full")
    out = out[:160]

    t_w = np.arange(len(w)) * dt * 1000
    t_inv = np.arange(len(inv)) * dt * 1000
    t_out = np.arange(len(out)) * dt * 1000

    fig, axes = plt.subplots(1, 3, figsize=(11, 3.5))

    ax = axes[0]
    ax.plot(t_w, w, "C0-")
    ax.fill_between(t_w, w, alpha=0.3)
    ax.set_title("Known minimum-phase wavelet $w(t)$")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Amplitude")
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    ax.plot(t_inv, inv, "C3-")
    ax.fill_between(t_inv, inv, alpha=0.3, color="C3")
    ax.set_title("Inverse filter $f(t)$")
    ax.set_xlabel("Time (ms)")
    ax.grid(True, alpha=0.3)

    ax = axes[2]
    ax.plot(t_out, out, "C2-")
    ax.fill_between(t_out, out, alpha=0.3, color="C2")
    ax.axvline(x=0, color="k", ls="--", alpha=0.4)
    ax.set_title("$w(t) * f(t)$")
    ax.set_xlabel("Time (ms)")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig("figures/term01_lec06/term01_lec06_deterministic_decon.png", dpi=200)
    plt.close(fig)
    print("Saved figures/term01_lec06/term01_lec06_deterministic_decon.png")


if __name__ == "__main__":
    main()
