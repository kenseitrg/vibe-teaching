"""
Synthetic comparison: trace-by-trace vs. surface-consistent deconvolution.
"""

import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import solve


def make_trace_with_variable_wavelet(n, dt, wavelets):
    """
    Build traces with the same reflectivity but different source/receiver wavelets.
    wavelets: dict (shot, receiver) -> wavelet array
    """
    np.random.seed(2)
    r = np.zeros(n)
    for t in [0.15, 0.30, 0.45, 0.60]:
        idx = int(round(t / dt))
        r[idx] = np.random.choice([-1, 1]) * np.random.uniform(0.5, 1.0)

    traces = []
    geometry = []
    for (s, r_idx), w in wavelets.items():
        x = np.convolve(r, w, mode="full")[:n]
        x += 0.05 * np.random.randn(n)
        traces.append(x)
        geometry.append((s, r_idx))
    return r, traces, geometry


def trace_by_trace_decon(traces, n_op, eps):
    """Design a separate spiking operator per trace."""
    out = []
    for x in traces:
        acorr = np.correlate(x, x, mode="full")
        acorr = acorr[len(x) - 1:]
        R = np.zeros((n_op, n_op))
        for i in range(n_op):
            for j in range(n_op):
                R[i, j] = acorr[abs(i - j)]
        R += eps * np.eye(n_op) * acorr[0]
        d = np.zeros(n_op)
        d[0] = acorr[0]
        f = solve(R, d)
        out.append(np.convolve(x, f, mode="same"))
    return out


def surface_consistent_decon(traces, geometry, n_op, eps):
    """
    Simplified surface-consistent decon: estimate one source and one receiver wavelet
    by averaging autocorrelations over shots/receivers.
    """
    n = len(traces[0])
    shots = sorted({g[0] for g in geometry})
    recs = sorted({g[1] for g in geometry})

    # Accumulate autocorrelations per shot and per receiver
    shot_ac = {s: np.zeros(2 * n - 1) for s in shots}
    rec_ac = {r: np.zeros(2 * n - 1) for r in recs}
    shot_count = {s: 0 for s in shots}
    rec_count = {r: 0 for r in recs}

    for x, (s, r) in zip(traces, geometry):
        ac = np.correlate(x, x, mode="full")
        shot_ac[s] += ac
        rec_ac[r] += ac
        shot_count[s] += 1
        rec_count[r] += 1

    for s in shots:
        shot_ac[s] /= max(shot_count[s], 1)
    for r in recs:
        rec_ac[r] /= max(rec_count[r], 1)

    # Build an average operator from combined shot+receiver autocorrelations
    out = []
    for x, (s, r) in zip(traces, geometry):
        ac = shot_ac[s] + rec_ac[r]
        ac = ac[n - 1:]  # lags 0..
        R = np.zeros((n_op, n_op))
        for i in range(n_op):
            for j in range(n_op):
                R[i, j] = ac[abs(i - j)]
        R += eps * np.eye(n_op) * ac[0]
        d = np.zeros(n_op)
        d[0] = ac[0]
        f = solve(R, d)
        out.append(np.convolve(x, f, mode="same"))
    return out


def main():
    dt = 0.004
    n = 300
    t = np.arange(n) * dt

    # Two shots, two receivers -> four traces
    wavelets = {
        (0, 0): np.exp(-30 * np.arange(50) * dt) * np.sin(2 * np.pi * 22 * np.arange(50) * dt),
        (0, 1): np.exp(-35 * np.arange(50) * dt) * np.sin(2 * np.pi * 24 * np.arange(50) * dt),
        (1, 0): np.exp(-25 * np.arange(50) * dt) * np.sin(2 * np.pi * 20 * np.arange(50) * dt),
        (1, 1): np.exp(-40 * np.arange(50) * dt) * np.sin(2 * np.pi * 26 * np.arange(50) * dt),
    }
    for k in wavelets:
        wavelets[k] /= np.max(np.abs(wavelets[k]))

    r, traces, geometry = make_trace_with_variable_wavelet(n, dt, wavelets)
    y_tbt = trace_by_trace_decon(traces, n_op=30, eps=0.05)
    y_sc = surface_consistent_decon(traces, geometry, n_op=30, eps=0.05)

    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True, sharey=True)

    for i, (x, g) in enumerate(zip(y_tbt, geometry)):
        axes[0].plot(t, x + i * 1.5, label=f"S{g[0]}-R{g[1]}" if i == 0 else "")
    axes[0].set_title("Trace-by-trace deconvolution (operators vary)")
    axes[0].set_ylabel("Trace index (offset)")
    axes[0].set_yticks([])
    axes[0].grid(True, alpha=0.3)

    for i, x in enumerate(y_sc):
        axes[1].plot(t, x + i * 1.5)
    axes[1].set_title("Surface-consistent deconvolution (stable operators)")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Trace index (offset)")
    axes[1].set_yticks([])
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()
    out = "figures/term01_lec07/term01_lec07_surface_consistent_example.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
