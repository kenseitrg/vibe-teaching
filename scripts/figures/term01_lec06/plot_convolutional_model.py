"""
Generate the convolutional-model figure for Lecture 6.

Shows: reflectivity series, embedded wavelet, and resulting seismic trace.
"""

import matplotlib.pyplot as plt
import numpy as np


def make_wavelet(dt: float, fdom: float = 25.0) -> np.ndarray:
    """Minimum-phase-like Ricker-style wavelet (simplified)."""
    t = np.arange(-0.05, 0.15 + dt, dt)
    # A causal minimum-phase-looking wavelet: damped sinusoid
    w = np.exp(-60 * t) * np.sin(2 * np.pi * fdom * t)
    w[t < 0] = 0.0
    w = w / np.max(np.abs(w))
    return t, w


def main():
    dt = 0.004  # 4 ms
    n_samples = 300
    t_trace = np.arange(n_samples) * dt

    # Sparse reflectivity
    np.random.seed(7)
    r = np.zeros(n_samples)
    spike_times = [0.15, 0.28, 0.42, 0.55, 0.72, 0.88]
    spike_amps = [0.9, -0.5, 0.7, -0.3, 0.6, -0.4]
    for st, sa in zip(spike_times, spike_amps):
        idx = int(round(st / dt))
        if 0 <= idx < n_samples:
            r[idx] = sa

    # Wavelet
    t_w, w = make_wavelet(dt)
    nw = len(w)

    # Trace = convolution, trimmed to trace length
    x = np.convolve(r, w, mode="full")[:n_samples]

    fig, axes = plt.subplots(3, 1, figsize=(9, 6), sharex=True)

    # Reflectivity
    ax = axes[0]
    ax.stem(t_trace, r, basefmt=" ", linefmt="C3-", markerfmt="C3o")
    ax.set_ylabel("Amplitude")
    ax.set_title("Reflectivity $r(t)$")
    ax.set_ylim(-1.1, 1.1)
    ax.grid(True, alpha=0.3)

    # Wavelet
    ax = axes[1]
    ax.plot(t_w, w, "C0-")
    ax.fill_between(t_w, w, alpha=0.3)
    ax.set_ylabel("Amplitude")
    ax.set_title("Embedded wavelet $w(t)$")
    ax.set_ylim(-1.1, 1.1)
    ax.grid(True, alpha=0.3)

    # Trace
    ax = axes[2]
    ax.plot(t_trace, x, "C2-")
    ax.fill_between(t_trace, x, alpha=0.3)
    ax.set_ylabel("Amplitude")
    ax.set_xlabel("Time (s)")
    ax.set_title("Seismic trace $x(t) = w(t) * r(t)$")
    ax.set_xlim(0, t_trace[-1])
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig("figures/term01_lec06/term01_lec06_convolutional_model.png", dpi=200)
    plt.close(fig)
    print("Saved figures/term01_lec06/term01_lec06_convolutional_model.png")


if __name__ == "__main__":
    main()
