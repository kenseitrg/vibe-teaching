"""
Effect of prewhitening on the deterministic inverse-filter spectrum.
"""

import matplotlib.pyplot as plt
import numpy as np


def wavelet_spectrum(dt: float, nfft: int):
    """Return frequencies and a synthetic minimum-phase-like amplitude spectrum."""
    f = np.fft.rfftfreq(nfft, dt)
    # Band-pass with notches
    amp = np.ones_like(f)
    # Ghost/source notches
    for fn in [0, 80, 160]:
        amp *= 1 - 0.9 * np.exp(-((f - fn) ** 2) / (2 * 6 ** 2))
    amp[f > 90] *= np.exp(-(f[f > 90] - 90) / 20)
    amp[f < 8] *= np.exp(-(8 - f[f < 8]) / 3)
    amp = np.maximum(amp, 0.05)
    return f, amp


def main():
    dt = 0.004
    nfft = 1024
    f, W = wavelet_spectrum(dt, nfft)

    # Inverse operators
    F_no_pw = 1.0 / W
    eps = 0.15
    F_pw = W / (W ** 2 + eps ** 2)

    # Clip for display
    F_no_pw = np.clip(F_no_pw, 0, 10)
    F_pw = np.clip(F_pw, 0, 10)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(f, F_no_pw, "--", label="Without prewhitening", lw=2)
    ax.plot(f, F_pw, label=f"With prewhitening ($\\varepsilon^2={eps**2:.3f}$)", lw=2)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Inverse-filter gain $|F(f)|$")
    ax.set_title("Prewhitening stabilizes spectral division")
    ax.set_xlim(0, 200)
    ax.set_ylim(0, 10)
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig("figures/term01_lec06/term01_lec06_prewhitening.png", dpi=200)
    plt.close(fig)
    print("Saved figures/term01_lec06/term01_lec06_prewhitening.png")


if __name__ == "__main__":
    main()
