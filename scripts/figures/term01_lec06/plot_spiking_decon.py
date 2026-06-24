"""
Spiking deconvolution on a synthetic trace.

Top row: input trace, embedded wavelet (causal, minimum-phase-like),
         input amplitude spectrum.
Bottom row: deconvolved output (mode="full", time-aligned), recovered
            wavelet (operator@wavelet), output amplitude spectrum.

Uses the same clean causal-wavelet design as plot_predictive_decon.py.
"""

import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import solve


def causal_wavelet(n: int, dt: float, f0: float = 25.0,
                   alpha: float = 60.0) -> np.ndarray:
    """
    Causal one-sided wavelet with peak at time zero.

        w(t) = exp(-alpha * t) * cos(2 * pi * f0 * t),   t >= 0
    """
    tw = np.arange(n) * dt
    w = np.exp(-alpha * tw) * np.cos(2 * np.pi * f0 * tw)
    w[0] = 1.0
    return w / np.max(np.abs(w))


def wiener_spiking_operator(x: np.ndarray, n_op: int,
                            eps: float) -> np.ndarray:
    """Design a Wiener spiking deconvolution operator (minimum delay)."""
    n = len(x)
    acorr = np.correlate(x, x, mode="full")[n - 1:]   # lags 0 … n-1
    R = np.array([[acorr[abs(i - j)] for j in range(n_op)] for i in range(n_op)])
    R += eps * np.eye(n_op) * acorr[0]
    d = np.zeros(n_op)
    d[0] = acorr[0]
    f = solve(R, d)
    return f


def amplitude_spectrum(
    sig: np.ndarray, dt: float
) -> tuple[np.ndarray, np.ndarray]:
    nfft = max(512, len(sig))
    spec = np.abs(np.fft.rfft(sig, n=nfft))
    freq = np.fft.rfftfreq(nfft, dt)
    return freq, spec


def main() -> None:
    # ----- Parameters ---------------------------------------------------
    dt = 0.004                         # sampling interval (s)
    n_trace = 400                      # number of trace samples
    t_trace = np.arange(n_trace) * dt

    # Causal wavelet (same family as predictive-decon figure)
    n_w = 32                           # 128 ms @ 4 ms
    w = causal_wavelet(n_w, dt, f0=25.0, alpha=60.0)

    # Reflectivity — sparse spikes at known times
    np.random.seed(3)
    r = np.zeros(n_trace)
    spike_times = [0.12, 0.28, 0.42, 0.55, 0.72, 0.88]
    for t in spike_times:
        idx = int(round(t / dt))
        if 0 <= idx < n_trace:
            r[idx] = np.random.choice([-1, 1]) * np.random.uniform(0.4, 1.0)

    # Trace = reflectivity * wavelet + noise
    x = np.convolve(r, w, mode="full")[:n_trace]
    x += 0.02 * np.random.randn(n_trace)

    # ----- Spiking deconvolution ---------------------------------------
    n_op = 32
    f = wiener_spiking_operator(x, n_op=n_op, eps=0.01)

    # Apply operator with full convolution and keep time-aligned portion
    y = np.convolve(x, f, mode="full")[:n_trace]

    # Recovered wavelet = operator applied to the embedded wavelet
    recovered = np.convolve(w, f, mode="full")[:80]

    # ----- Plot ---------------------------------------------------------
    t_w = np.arange(len(w)) * dt * 1000
    t_rec = np.arange(len(recovered)) * dt * 1000

    fig, axes = plt.subplots(2, 3, figsize=(13, 6))

    # --- Row 0 ----------------------------------------------------------
    # Input trace
    ax = axes[0, 0]
    ax.plot(t_trace, x, "C0-", lw=0.9)
    ax.set_title("Input trace")
    ax.set_ylabel("Amplitude")
    ax.grid(True, alpha=0.3)

    # Embedded wavelet
    ax = axes[0, 1]
    ax.plot(t_w, w, "C0-", lw=0.9)
    ax.fill_between(t_w, w, alpha=0.3)
    ax.set_title("Embedded wavelet (causal)")
    ax.grid(True, alpha=0.3)

    # Input amplitude spectrum
    ax = axes[0, 2]
    freq, spec = amplitude_spectrum(x, dt)
    ax.plot(freq, 20 * np.log10(spec + 1e-12), "C0-", lw=0.9)
    ax.set_title("Input amplitude spectrum")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("dB")
    ax.set_xlim(0, 125)
    ax.grid(True, alpha=0.3)

    # --- Row 1 ----------------------------------------------------------
    # Deconvolved trace
    ax = axes[1, 0]
    ax.plot(t_trace, y, "C2-", lw=0.9)
    ax.set_title("After spiking deconvolution")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.grid(True, alpha=0.3)

    # Recovered (compressed) wavelet
    ax = axes[1, 1]
    ax.plot(t_rec, recovered, "C2-", lw=0.9)
    ax.fill_between(t_rec, recovered, alpha=0.3, color="C2")
    ax.axvline(x=0, color="k", ls="--", alpha=0.4)
    ax.set_title("Recovered wavelet (compressed)")
    ax.set_xlabel("Time (ms)")
    ax.grid(True, alpha=0.3)

    # Output amplitude spectrum
    ax = axes[1, 2]
    freq, spec = amplitude_spectrum(y, dt)
    ax.plot(freq, 20 * np.log10(spec + 1e-12), "C2-", lw=0.9)
    ax.set_title("Output amplitude spectrum")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("dB")
    ax.set_xlim(0, 125)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig("figures/term01_lec06/term01_lec06_spiking_decon.png",
                dpi=200)
    plt.close(fig)
    print("Saved figures/term01_lec06/term01_lec06_spiking_decon.png")


if __name__ == "__main__":
    main()
