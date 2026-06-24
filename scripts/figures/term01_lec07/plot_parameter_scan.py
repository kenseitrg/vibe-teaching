"""
Parameter scan: prediction gap and operator length for spiking deconvolution.
"""

import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import solve


def make_trace(n, dt):
    np.random.seed(1)
    r = np.zeros(n)
    for t in [0.20, 0.40, 0.60]:
        idx = int(round(t / dt))
        r[idx] = np.random.choice([-1, 1]) * np.random.uniform(0.6, 1.0)

    nw = 50
    t = np.arange(nw) * dt
    w = np.exp(-30 * t) * np.sin(2 * np.pi * 22 * t)
    w /= np.max(np.abs(w))
    x = np.convolve(r, w, mode="full")[:n]
    x += 0.03 * np.random.randn(n)
    return r, x


def spiking_op(x, n_op, eps):
    n = len(x)
    acorr = np.correlate(x, x, mode="full")
    acorr = acorr[n - 1:]
    R = np.zeros((n_op, n_op))
    for i in range(n_op):
        for j in range(n_op):
            R[i, j] = acorr[abs(i - j)]
    R += eps * np.eye(n_op) * acorr[0]
    d = np.zeros(n_op)
    d[0] = acorr[0]
    return solve(R, d)


def main():
    dt = 0.004
    n = 300
    t = np.arange(n) * dt
    r, x = make_trace(n, dt)

    gaps = [1, 5, 15]
    lengths = [20, 60, 120]
    eps = 0.02

    fig, axes = plt.subplots(len(gaps), len(lengths), figsize=(12, 7), sharex=True, sharey=True)

    for i, gap in enumerate(gaps):
        for j, n_op in enumerate(lengths):
            f = spiking_op(x, n_op=n_op, eps=eps)
            # Apply gap by zeroing first gap-1 samples
            f_applied = np.zeros_like(f)
            f_applied[gap - 1:] = f[gap - 1:]
            y = np.convolve(x, f_applied, mode="same")
            ax = axes[i, j]
            ax.plot(t, y, "C2-")
            ax.set_title(f"gap={gap}, length={n_op}")
            ax.grid(True, alpha=0.3)
            if i == len(gaps) - 1:
                ax.set_xlabel("Time (s)")
            if j == 0:
                ax.set_ylabel("Amplitude")

    fig.suptitle("Prediction gap vs. operator length scan", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    out = "figures/term01_lec07/term01_lec07_parameter_scan.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
