"""
Dipole illustration: (a, b) vs (b, a) with same amplitude spectrum.
Shows that minimum-phase dipole is front-loaded.
"""

import matplotlib.pyplot as plt
import numpy as np


def main():
    dt = 0.004
    a, b = 0.8, 0.3

    # Time-domain dipoles
    t = np.array([0, dt])
    dipole_min = np.array([a, b])
    dipole_max = np.array([b, a])

    # Amplitude spectra
    f = np.linspace(0, 125, 500)
    omega = 2 * np.pi * f
    W_min = np.abs(a + b * np.exp(-1j * omega * dt))
    W_max = np.abs(b + a * np.exp(-1j * omega * dt))

    fig = plt.figure(figsize=(10, 4))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.4])

    ax0 = fig.add_subplot(gs[0, 0])
    ax0.stem(t * 1000, dipole_min, basefmt=" ")
    ax0.set_title("Minimum-phase dipole\n$(a,b)$, $|a|>|b|$")
    ax0.set_xlabel("Time (ms)")
    ax0.set_ylabel("Amplitude")
    ax0.set_ylim(0, 1.0)
    ax0.grid(True, alpha=0.3)

    ax1 = fig.add_subplot(gs[0, 1])
    ax1.stem(t * 1000, dipole_max, basefmt=" ")
    ax1.set_title("Maximum-phase dipole\n$(b,a)$, $|b|<|a|$")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylim(0, 1.0)
    ax1.grid(True, alpha=0.3)

    ax2 = fig.add_subplot(gs[0, 2])
    ax2.plot(f, W_min, label="minimum-phase $(a,b)$", lw=2)
    ax2.plot(f, W_max, "--", label="maximum-phase $(b,a)$", lw=2)
    ax2.set_title("Amplitude spectra (identical)")
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("$|W(f)|$")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig("figures/term01_lec06/term01_lec06_dipoles.png", dpi=200)
    plt.close(fig)
    print("Saved figures/term01_lec06/term01_lec06_dipoles.png")


if __name__ == "__main__":
    main()
