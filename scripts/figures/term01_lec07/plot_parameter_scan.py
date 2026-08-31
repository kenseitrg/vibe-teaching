"""
Parameter scan: prediction gap and operator length for predictive deconvolution.

Layout:
  Row 0 (top): reflectivity, primary trace (no reverberations),
               trace with reverberations (input to deconvolution).
  Rows 1-3:    deconvolution results for gap = [1, 5, 15] samples
               and operator length = [20, 60, 120] samples.
  All panels in rows 1-3 share a common y-axis range so the effects of
  parameter choice are directly comparable.
"""

import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import solve


def causal_wavelet(n, dt, f0=25.0, alpha=60.0):
    """Causal one-sided wavelet peaked at t=0."""
    tw = np.arange(n) * dt
    w = np.exp(-alpha * tw) * np.cos(2 * np.pi * f0 * tw)
    w[0] = 1.0
    return w / np.max(np.abs(w))


def design_pef(acorr, gap, n_op, eps):
    """
    Design a prediction-error filter (Wiener-Levinson style).

    PEF = [1, 0, ..., 0, -h0, -h1, ..., -h_{n_op-1}]
    where the unit coefficient sits at lag 0, zeros from 1 to gap-1,
    and the prediction filter h occupies lags gap .. gap+n_op-1.
    """
    n = len(acorr)
    # Build Toeplitz autocorrelation matrix
    R = np.zeros((n_op, n_op))
    for i in range(n_op):
        for j in range(n_op):
            R[i, j] = acorr[abs(i - j)]
    R += eps * np.eye(n_op) * acorr[0]

    # Right-hand side: acorr at lags gap … gap + n_op - 1
    rhs = acorr[gap: gap + n_op]
    h = solve(R, rhs)

    pef = np.zeros(gap + n_op)
    pef[0] = 1.0
    pef[gap:] = -h
    return pef


def apply_filter(x, h):
    """Full convolution, trimmed to input length."""
    return np.convolve(x, h, mode="full")[:len(x)]


def main():
    dt = 0.004
    n_samples = 350
    t = np.arange(n_samples) * dt
    np.random.seed(1)

    # ------------------------------------------------------------------
    # 1.  Synthetic model
    # ------------------------------------------------------------------
    # Reflectivity
    ref_times = [0.20, 0.45, 0.70]
    ref_amplitudes = [1.0, -0.7, 0.6]
    r = np.zeros(n_samples)
    for rt, ra in zip(ref_times, ref_amplitudes):
        r[int(round(rt / dt))] = ra

    # Wavelet
    nw = 16
    w = causal_wavelet(nw, dt, f0=25.0, alpha=60.0)

    # Primary (no reverberations)
    prim = np.convolve(r, w, mode="full")[:n_samples]

    # Reverberation train: several delayed, scaled copies (water-layer multiples)
    period = 15                     # two-way time in samples (60 ms)
    coeff = -0.65                   # reflection coefficient
    reverb = np.zeros(n_samples)
    tmp = prim.copy()
    for k in range(1, 4):           # first three multiples
        delay = k * period
        if delay >= n_samples:
            break
        reverb[delay:] += (coeff ** k) * prim[:n_samples - delay]

    noise = 0.035 * np.random.randn(n_samples)
    x = prim + reverb + noise       # input trace with reverberations

    # ------------------------------------------------------------------
    # 2.  Deconvolution parameter scan
    # ------------------------------------------------------------------
    # gap=1: spiking deconvolution (compress the wavelet)
    # gap=period: predictive deconvolution tuned to the reverberation period
    # gap=2*period: longer-gap predictive deconvolution (multiples, little wavelet compression)
    gaps = [1, 15, 30]
    lengths = [20, 60, 120]
    eps = 0.005

    # Compute autocorrelation once
    ac = np.correlate(x, x, mode="full")[n_samples - 1:]

    results = {}   # (gap, n_op) -> deconvolved trace
    global_min, global_max = np.inf, -np.inf

    for gap in gaps:
        for n_op in lengths:
            pef = design_pef(ac, gap, n_op, eps)
            y = apply_filter(x, pef)
            results[(gap, n_op)] = y
            lo, hi = y.min(), y.max()
            if lo < global_min:
                global_min = lo
            if hi > global_max:
                global_max = hi

    # Symmetric common y-range for all deconvolution panels
    y_lim = max(abs(global_min), abs(global_max)) * 1.05

    # ------------------------------------------------------------------
    # 3.  Plotting
    # ------------------------------------------------------------------
    fig = plt.figure(figsize=(12, 9.5), constrained_layout=True)
    gs = fig.add_gridspec(4, 3, hspace=0.35, wspace=0.25)

    # ---- Row 0: Inputs ----
    input_data = [
        (r, "Input reflectivity", "#1f77b4"),
        (prim, "Primary trace (no reverberations)", "#2ca02c"),
        (x, "Trace with reverberations (input to decon)", "#d62728"),
    ]
    for col, (data, title, color) in enumerate(input_data):
        ax = fig.add_subplot(gs[0, col])
        ax.plot(t, data, color=color, lw=1.2)
        for rt in ref_times:
            ax.axvline(rt, color="gray", ls="--", alpha=0.35)
        ax.set_title(title, fontsize=9, fontweight="bold")
        ax.set_xlim(0, t[-1])
        ax.set_ylim(-1.25, 1.4)
        ax.grid(True, alpha=0.3)
        if col == 0:
            ax.set_ylabel("Amplitude", fontsize=8)
        else:
            ax.tick_params(labelleft=False)

    # ---- Rows 1-3: Parameter scan ----
    for i, gap in enumerate(gaps):
        for j, n_op in enumerate(lengths):
            ax = fig.add_subplot(gs[i + 1, j])
            y = results[(gap, n_op)]
            ax.plot(t, y, "C0-", lw=0.9)
            for rt in ref_times:
                ax.axvline(rt, color="gray", ls="--", alpha=0.3)
            ax.set_ylim(-y_lim, y_lim)
            ax.set_xlim(0, t[-1])
            ax.grid(True, alpha=0.25)
            ax.tick_params(labelsize=7)
            # Row label on the leftmost column
            if j == 0:
                if gap == 1:
                    label = "gap=1 (spiking)"
                elif gap == period:
                    label = f"gap={gap} (reverberation)"
                else:
                    label = f"gap={gap} (long-gap predictive)"
                ax.set_ylabel(label, fontsize=9, fontweight="bold")
            # Column label on the top row
            if i == 0:
                ax.set_title(f"length={n_op}", fontsize=9, fontweight="bold")
            if i == len(gaps) - 1:
                ax.set_xlabel("Time (s)", fontsize=8)
            if j > 0:
                ax.tick_params(labelleft=False)

    # Overall title
    fig.suptitle(
        "Predictive deconvolution — prediction gap vs. operator length",
        fontsize=13, fontweight="bold",
    )
    out = "figures/term01_lec07/term01_lec07_parameter_scan.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
