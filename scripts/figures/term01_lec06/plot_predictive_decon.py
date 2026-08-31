"""
Predictive deconvolution with different prediction gaps.

Panels (top to bottom):
  1. Input reflectivity (sparse spike series)
  2. Synthetic trace: each spike excites a causal wavelet, followed by one
     water-layer reverberation delayed by the two-way travel time.
  3. Spiking deconvolution (gap = 1 sample, short operator):
     wavelets are compressed to spikes but reverberations remain.
  4. Predictive deconvolution (gap = reverberation period):
     wavelets are preserved while reverberations are suppressed.

Compare panels 3 and 4 to see how the choice of gap controls whether the
filter targets the wavelet or the reverberation.
"""

import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import solve


def causal_wavelet(n: int, dt: float, f0: float = 25.0,
                   alpha: float = 60.0) -> np.ndarray:
    """
    Causal one-sided wavelet with peak at time zero.

        w(t) = exp(-alpha * t) * cos(2 * pi * f0 * t),   t >= 0

    The wavelet is purely causal (no energy before t = 0), its peak sits
    at the first sample, and it decays quickly so that its duration is
    shorter than the reverberation period used in the synthetic trace.
    """
    tw = np.arange(n) * dt
    w = np.exp(-alpha * tw) * np.cos(2 * np.pi * f0 * tw)
    w[0] = 1.0  # ensure clean peak at the first sample
    return w / np.max(np.abs(w))


def design_prediction_error_filter(x: np.ndarray, gap: int,
                                   n_op: int,
                                   eps: float = 0.005) -> np.ndarray:
    """
    Design a prediction-error filter (Wiener-Levinson).

    The PEF has the form

        p = [1, 0, ..., 0, -h0, -h1, ..., -h_{n_op-1}]

    where the unit coefficient sits at lag 0 and the prediction filter h
    occupies lags *gap* … *gap* + *n_op* - 1.

    Parameters
    ----------
    x : array, shape (N,)
        Input trace.
    gap : int
        Prediction gap in samples.
    n_op : int
        Number of coefficients in the prediction filter.
    eps : float
        Prewhitening level (fraction of the zero-lag autocorrelation).

    Returns
    -------
    pef : array, shape (gap + n_op,)
        Prediction-error filter coefficients.
    """
    n = len(x)
    ac = np.correlate(x, x, mode="full")[n - 1:]   # lags 0, 1, ..., n-1

    # Toeplitz autocorrelation matrix
    R = np.zeros((n_op, n_op))
    for i in range(n_op):
        for j in range(n_op):
            R[i, j] = ac[abs(i - j)]

    # Prewhitening on the diagonal
    R += eps * np.eye(n_op) * ac[0]

    # Right-hand side: autocorrelation at lags gap … gap + n_op - 1
    rhs = ac[gap: gap + n_op]
    h = solve(R, rhs)

    # Assemble the prediction-error filter
    pef = np.zeros(gap + n_op)
    pef[0] = 1.0
    pef[gap:] = -h
    return pef


def apply_filter(x: np.ndarray, h: np.ndarray) -> np.ndarray:
    """
    Apply a causal filter with numpy's full convolution and return the
    first len(x) samples (which are time-aligned with the input).
    """
    return np.convolve(x, h, mode="full")[:len(x)]


def main() -> None:
    # ----- Parameters ---------------------------------------------------
    dt = 0.004                         # sampling interval (s)
    n = 400                            # number of samples
    t = np.arange(n) * dt              # time axis (s)

    # Wavelet
    nw = 16                            # wavelet length (samples)
    w = causal_wavelet(nw, dt, f0=25.0, alpha=60.0)

    # Reflectivity
    spike_times = np.array([0.20, 0.45, 0.70])   # times (s)
    spike_indices = (spike_times / dt).astype(int)
    r = np.zeros(n)
    r[spike_indices] = [1.0, -0.7, 0.6]

    # Primary trace
    prim = np.convolve(r, w, mode="full")[:n]

    # Reverberation: a single delayed, scaled copy of the primary
    period = 15                        # water-layer two-way time (samples, 60 ms)
    coeff = -0.65                      # reflection coefficient
    reverb = np.zeros(n)
    reverb[period:] += coeff * prim[:n - period]

    np.random.seed(42)
    noise = 0.005 * np.random.randn(n)
    x = prim + reverb + noise

    # ----- Deconvolution ------------------------------------------------
    # Spiking: gap = 1 sample, short operator leaves reverberations visible
    pef_spike = design_prediction_error_filter(x, gap=1, n_op=12, eps=0.005)
    y_spike = apply_filter(x, pef_spike)

    # Predictive: gap = reverberation period
    pef_pred = design_prediction_error_filter(x, gap=period, n_op=20, eps=0.005)
    y_pred = apply_filter(x, pef_pred)

    # ----- Plot ---------------------------------------------------------
    fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True, sharey=True)

    panels = [
        (r,       "Input reflectivity"),
        (x,       "Input trace with reverberations"),
        (y_spike, f"Gap = 1 sample (spiking, {len(pef_spike)-1}-coefficient operator)"),
        (y_pred,  f"Gap = {period} samples (reverberation period, "
                  f"{len(pef_pred)-1}-coefficient operator)"),
    ]

    for ax, (y, lab) in zip(axes, panels):
        ax.plot(t, y, "C0-", lw=0.9)
        ax.set_ylabel("Amplitude")
        ax.set_title(lab, fontsize=10)
        ax.grid(True, alpha=0.3)

        # Vertical dashed lines at true spike times
        for st in spike_times:
            ax.axvline(st, color="gray", ls="--", alpha=0.35)

    axes[-1].set_xlabel("Time (s)")
    axes[-1].set_xlim(0, t[-1])

    fig.tight_layout()
    fig.savefig("figures/term01_lec06/term01_lec06_predictive_decon.png",
                dpi=200)
    plt.close(fig)
    print("Saved figures/term01_lec06/term01_lec06_predictive_decon.png")


if __name__ == "__main__":
    main()
