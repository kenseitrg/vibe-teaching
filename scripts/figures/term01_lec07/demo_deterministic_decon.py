"""
Self-contained demo: deterministic deconvolution by spectral division.

Run with:
    uv run python scripts/figures/term01_lec07/demo_deterministic_decon.py
"""

import matplotlib.pyplot as plt
import numpy as np


def deterministic_decon(trace: np.ndarray, wavelet: np.ndarray, eps: float = 0.05) -> np.ndarray:
    """
    Deterministic deconvolution by prewhitened spectral division.

    Parameters
    ----------
    trace : 1-D array
        Input seismic trace.
    wavelet : 1-D array
        Known wavelet.
    eps : float
        Prewhitening level relative to the peak power of the wavelet.

    Returns
    -------
    decon : 1-D array
        Deconvolved trace (same length as trace).
    """
    n = len(trace)
    W = np.fft.rfft(wavelet, n=n)
    X = np.fft.rfft(trace, n=n)
    peak_power = np.max(np.abs(W) ** 2)

    # Prewhitened inverse filter
    F = np.conj(W) / (np.abs(W) ** 2 + eps ** 2 * peak_power)

    R = X * F
    decon = np.fft.irfft(R, n=n)
    return decon


def make_wavelet(n: int, dt: float, fdom: float = 22.0) -> np.ndarray:
    """Causal minimum-phase-like wavelet."""
    t = np.arange(n) * dt
    w = np.exp(-28 * t) * np.sin(2 * np.pi * fdom * t)
    w /= np.max(np.abs(w))
    return w


def main():
    dt = 0.004  # 4 ms
    n = 400
    t = np.arange(n) * dt

    # Synthetic reflectivity
    np.random.seed(5)
    r = np.zeros(n)
    for time in [0.12, 0.28, 0.44, 0.60, 0.76]:
        idx = int(round(time / dt))
        r[idx] = np.random.choice([-1, 1]) * np.random.uniform(0.4, 1.0)

    # Known wavelet
    n_w = 60
    w = make_wavelet(n_w, dt, fdom=22.0)

    # Build trace
    x = np.convolve(r, w, mode="full")[:n]
    x += 0.03 * np.random.randn(n)

    # Deconvolve with two prewhitening levels
    y_low = deterministic_decon(x, w, eps=0.01)
    y_high = deterministic_decon(x, w, eps=0.20)

    fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)

    axes[0].stem(t, r, basefmt=" ", linefmt="C3-", markerfmt="C3o")
    axes[0].set_title("Reflectivity")
    axes[0].set_ylabel("Amplitude")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(t, x, "C0-")
    axes[1].set_title("Input trace (wavelet + noise)")
    axes[1].set_ylabel("Amplitude")
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(t, y_low, "C2-")
    axes[2].set_title(r"Deconvolved ($\varepsilon = 0.01$): sharp but noisy")
    axes[2].set_ylabel("Amplitude")
    axes[2].grid(True, alpha=0.3)

    axes[3].plot(t, y_high, "C1-")
    axes[3].set_title(r"Deconvolved ($\varepsilon = 0.20$): stable but less compressed")
    axes[3].set_ylabel("Amplitude")
    axes[3].set_xlabel("Time (s)")
    axes[3].grid(True, alpha=0.3)

    fig.tight_layout()
    out = "figures/term01_lec07/term01_lec07_demo_deterministic_decon.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
