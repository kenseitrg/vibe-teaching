"""
Self-contained demo: Wiener spiking deconvolution as matrix operations.

Run with:
    uv run python scripts/figures/term01_lec07/demo_wiener_matrix.py
"""

import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import solve


def make_wavelet(n: int, dt: float, fdom: float = 22.0) -> np.ndarray:
    """Causal minimum-phase-like wavelet."""
    t = np.arange(n) * dt
    w = np.exp(-28 * t) * np.sin(2 * np.pi * fdom * t)
    w /= np.max(np.abs(w))
    return w


def wiener_spiking_operator(trace: np.ndarray, n_op: int, eps: float = 0.01) -> np.ndarray:
    """
    Design a Wiener spiking-deconvolution operator from a trace.

    Builds and solves the normal equations R f = d explicitly.
    """
    n = len(trace)
    acorr = np.correlate(trace, trace, mode="full")
    acorr = acorr[n - 1:]  # lags 0, 1, ..., n-1

    # Toeplitz autocorrelation matrix
    R = np.zeros((n_op, n_op))
    for i in range(n_op):
        for j in range(n_op):
            R[i, j] = acorr[abs(i - j)]

    # Prewhitening
    R += eps * np.eye(n_op) * acorr[0]

    # Desired output: spike at lag 0
    d = np.zeros(n_op)
    d[0] = acorr[0]

    f = solve(R, d)
    return f, R, d


def main():
    dt = 0.004
    n = 400
    t = np.arange(n) * dt

    np.random.seed(7)
    r = np.zeros(n)
    for time in [0.12, 0.28, 0.44, 0.60, 0.76]:
        idx = int(round(time / dt))
        r[idx] = np.random.choice([-1, 1]) * np.random.uniform(0.4, 1.0)

    w = make_wavelet(60, dt, fdom=22.0)
    x = np.convolve(r, w, mode="full")[:n]
    x += 0.03 * np.random.randn(n)

    n_op = 40
    f, R, d = wiener_spiking_operator(x, n_op, eps=0.02)
    y = np.convolve(x, f, mode="same")

    fig = plt.figure(figsize=(12, 5))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.2, 1, 1])

    ax0 = fig.add_subplot(gs[0, 0])
    ax0.plot(t, x, "C0-", label="Input trace")
    ax0.plot(t, y, "C2-", label="After spiking decon")
    ax0.set_xlabel("Time (s)")
    ax0.set_ylabel("Amplitude")
    ax0.set_title("Trace before and after deconvolution")
    ax0.legend()
    ax0.grid(True, alpha=0.3)

    ax1 = fig.add_subplot(gs[0, 1])
    im = ax1.imshow(R, cmap="RdBu_r", aspect="auto")
    ax1.set_title("Toeplitz autocorrelation matrix R")
    ax1.set_xlabel("Column")
    ax1.set_ylabel("Row")
    plt.colorbar(im, ax=ax1, fraction=0.046)

    ax2 = fig.add_subplot(gs[0, 2])
    tf = np.arange(len(f)) * dt * 1000
    ax2.stem(tf, f, basefmt=" ")
    ax2.set_title("Wiener spiking operator")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Amplitude")
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    out = "figures/term01_lec07/term01_lec07_demo_wiener_matrix.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
