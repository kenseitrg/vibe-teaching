"""
Term 3 Lecture 06 — Figure 4 (Section 3): legacy interpolation methods on
regularly vs. irregularly decimated data, bridging into spectral leakage.

Pedagogical point
-----------------
The prediction-filter methods of Sec. 3 (T-X, F-X, F-K) assume the data are
sampled REGULARLY.  We test all three on the same simple dataset as Fig. 3
(three linear events) under two decimations, each keeping ~half the traces:

  * REGULAR  -- every second trace removed.  The sampling mask is a periodic
    comb, so in the Fourier domain the spectrum is merely REPLICATED (clean,
    structured aliasing).  All three methods invert this well.
  * IRREGULAR -- a random half of the traces removed.  The mask is an aperiodic
    comb whose transform has sidelobes at every wavenumber; convolution with
    those sidelobes smears each component into many false ones (SPECTRAL
    LEAKAGE).  The DFT basis is no longer orthogonal on the irregular grid, and
    every method degrades.

This is the bridge to Sec. 4.2 (spectral leakage) and Sec. 4.4 (the
anti-leakage Fourier transform): the failure on irregular sampling is not
method-specific, it is fundamental, and it motivates sparse reconstruction.

Methods (distinct mechanisms):
  T-X        local dip scan + shift-and-sum of available neighbours.
  F-X        Spitz spatial prediction filter (low->high f/2 prior), with the
             missing traces recovered by constrained least-squares.
  F-K        Gulunay-style POCS: band-limit in f-k and re-insert known traces.

Self-contained: numpy + scipy + matplotlib only.
"""

import os

import numpy as np

# ---------------------------------------------------------------------------
# Data: three linear events  t = tau + p*x   (same model as Figure 3)
# ---------------------------------------------------------------------------
NX = 128
X_MAX = 2000.0
DT = 0.002
NT = 600
F0 = 20.0          # modest bandwidth so the decimated grid is ~un-aliased
N_EVENTS = 3

x_axis = np.linspace(0.0, X_MAX, NX)
dx = x_axis[1] - x_axis[0]
time_axis = np.arange(NT) * DT

# Three linear events.  The dips are kept gentle (and the intercepts centred)
# so that the events stay UN-ALIASED after decimation by two: the figure is
# about regular-vs-irregular sampling (spectral leakage), so aliasing is removed
# as a confound.  max|k| = max|p|*f_max stays below the decimated Nyquist.
EVENTS = [
    (0.30, 0.0002, 1.00),
    (0.50, 0.0000, 0.80),
    (0.70, -0.0002, 0.90),
]


def ricker(t):
    a = np.pi * F0 * t
    return (1.0 - 2.0 * a**2) * np.exp(-(a**2))


D = np.zeros((NX, NT))
for i, x in enumerate(x_axis):
    sig = np.zeros(NT)
    for tau, p, amp in EVENTS:
        sig += amp * ricker(time_axis - (tau + p * x))
    D[i, :] = sig

# ---------------------------------------------------------------------------
# Decimation masks (each keeps ~half the traces)
# ---------------------------------------------------------------------------
mask_regular = (np.arange(NX) % 2 == 0)          # every second trace

rng = np.random.default_rng(3)
keep = rng.permutation(NX)[: NX // 2]
mask_irregular = np.zeros(NX, dtype=bool)
mask_irregular[keep] = True

MASKS = {"Regular sampling": mask_regular, "Irregular sampling": mask_irregular}

# ---------------------------------------------------------------------------
# Diagnostics helper
# ---------------------------------------------------------------------------
def rms_error(recon, truth, missing):
    """RMS interpolation error over the missing traces, as % of truth RMS."""
    r = (recon - truth)[missing]
    denom = np.sqrt(np.mean(truth[missing] ** 2))
    return 100.0 * np.sqrt(np.mean(r**2)) / denom


# ---------------------------------------------------------------------------
# T-X interpolation: local dip scan + shift-and-sum
# ---------------------------------------------------------------------------
P_MAX = 0.0006
N_DIP = 49
P_SCAN = np.linspace(-P_MAX, P_MAX, N_DIP)
NEIGH = 12            # neighbour half-window, in traces
SEM_SMOOTH = 11       # time-smoothing window for the semblance


def tx_interpolate(data, known):
    out = data.copy()
    miss = np.where(~known)[0]
    for i in miss:
        xi = x_axis[i]
        # available neighbours within the window (fall back to nearest if few)
        cand = np.where(known & (np.abs(np.arange(NX) - i) <= NEIGH))[0]
        if cand.size < 2:
            cand = np.where(known)[0]
            cand = cand[np.argsort(np.abs(cand - i))][:4]
        xj = x_axis[cand]
        dj = data[cand, :]                                   # (n_neigh, NT)

        stack = np.empty((N_DIP, NT))
        sem = np.empty((N_DIP, NT))
        for ip, p in enumerate(P_SCAN):
            shift = p * (xj - xi)                            # (n_neigh,)
            s = np.empty_like(dj)
            for jj in range(cand.size):
                s[jj, :] = np.interp(time_axis + shift[jj], time_axis,
                                     dj[jj, :], left=0.0, right=0.0)
            num = s.sum(axis=0) ** 2
            den = cand.size * np.sum(s**2, axis=0)
            stack[ip, :] = s.mean(axis=0)
            with np.errstate(divide="ignore", invalid="ignore"):
                sem[ip, :] = np.where(den > 0, num / den, 0.0)

        # smooth semblance in time, pick the best dip per time sample
        kern = np.ones(SEM_SMOOTH) / SEM_SMOOTH
        sem_s = np.apply_along_axis(lambda v: np.convolve(v, kern, "same"),
                                    0, sem)
        best = np.argmax(sem_s, axis=0)                      # (NT,)
        out[i, :] = stack[best, np.arange(NT)]
    out[known] = data[known]
    return out


# ---------------------------------------------------------------------------
# F-X interpolation (Spitz): spatial prediction filter + constrained LS
# ---------------------------------------------------------------------------
M = N_EVENTS                       # prediction-filter order
EPS = 1e-6
F_LO, F_HI = 3.0, 45.0             # wavelet band to reconstruct (Hz)


def _predict_filter_ls(seq, order):
    """Least-squares forward prediction filter of a complex sequence.

    Finds a such that seq[n] ~= sum_{l=1..order} a[l-1] * seq[n-l].
    """
    n = seq.size
    if n <= order + 1:
        return np.zeros(order, dtype=complex)
    A = np.empty((n - order, order), dtype=complex)
    for l in range(1, order + 1):
        A[:, l - 1] = seq[order - l:n - l]
    b = seq[order:]
    a, *_ = np.linalg.lstsq(A, b, rcond=None)
    return a


def _predict_filter_gapped(col, known, order):
    """Prediction filter from irregularly available samples (least squares)."""
    pos = np.where(known)[0]
    pos_set = set(pos.tolist())
    rows, rhs = [], []
    for m in range(order, col.size):
        if m not in pos_set:
            continue
        if all((m - j) in pos_set for j in range(1, order + 1)):
            rows.append([col[m - j] for j in range(1, order + 1)])
            rhs.append(col[m])
    if len(rows) <= order:
        return np.zeros(order, dtype=complex)
    A = np.array(rows)
    b = np.array(rhs)
    a, *_ = np.linalg.lstsq(A, b, rcond=None)
    return a


def _reconstruct_column(col, known, a):
    """Recover the full spatial column given a prediction filter and knowns.

    Sets up the regular-grid prediction equations x[m] = sum_j a_j x[m-j] over
    the full trace, fixes the known samples, and solves the (banded) complex
    least-squares problem for the missing ones.
    """
    n = col.size
    order = a.size
    unknown = np.where(~known)[0]
    col_idx = -np.ones(n, dtype=int)
    col_idx[unknown] = np.arange(unknown.size)

    A_rows, b_rows = [], []
    for m in range(order, n):
        row = np.zeros(unknown.size, dtype=complex)
        rhs = 0.0 + 0.0j
        if col_idx[m] >= 0:
            row[col_idx[m]] += 1.0
        for j in range(1, order + 1):
            c = col_idx[m - j]
            if c >= 0:
                row[c] -= a[j - 1]
            else:
                rhs += a[j - 1] * col[m - j]
        A_rows.append(row)
        b_rows.append(rhs)
    A = np.array(A_rows)
    b = np.array(b_rows)
    u, *_ = np.linalg.lstsq(A, b, rcond=None)
    full = col.copy()
    full[unknown] = u
    return full


def fx_interpolate(data, known):
    XF = np.fft.fft(data, axis=1)                 # (NX, NT) over time
    n_even = int(known.sum())
    # Zero-pad available traces to 2*NT so that bin k of the padded transform is
    # exactly the spectrum at f_k/2 -- the Spitz low->high prior needs the
    # decimated data at f/2, and this reads it off with no interpolation error.
    zp = np.zeros((n_even, 2 * NT))
    zp[:, :NT] = data[known, :]
    XF_zp = np.fft.fft(zp, axis=1)                # (n_even, 2NT)

    regular = _is_regular(known)
    out_spec = XF.copy()                          # out-of-band stays as input
    df = 1.0 / (NT * DT)
    k_lo = max(1, int(round(F_LO / df)))
    k_hi = min(NT // 2, int(round(F_HI / df)))
    for k in range(k_lo, k_hi + 1):
        col = XF[:, k]
        if regular:
            y_half = XF_zp[:, k]                  # decimated data at f_k/2 (exact)
            a = _predict_filter_ls(y_half, M)
        else:
            a = _predict_filter_gapped(col, known, M)
        full = _reconstruct_column(col, known, a)
        out_spec[:, k] = full
        if k < NT // 2:
            out_spec[:, NT - k] = np.conj(full)

    out = np.fft.ifft(out_spec, axis=1).real
    out[known] = data[known]
    return out


def _is_regular(known):
    idx = np.where(known)[0]
    if idx.size < 2:
        return False
    d = np.diff(idx)
    return bool(np.all(d == d[0]))


# ---------------------------------------------------------------------------
# F-K interpolation (Gulunay-style POCS): band-limit in f-k, re-insert data
# ---------------------------------------------------------------------------
def fk_interpolate(data, known, n_iter=120):
    # Keep the central half of the wavenumber axis (= the decimated bandwidth).
    kx = np.fft.fftfreq(NX, d=dx)
    kmask = np.abs(kx) <= (0.25 / dx)             # central half = decimated Nyquist 1/(4 dx)

    est = data.copy()
    est[~known] = 0.0
    for _ in range(n_iter):
        FK = np.fft.fft2(est)
        FK[~kmask, :] = 0.0                        # band-limit in wavenumber
        model = np.fft.ifft2(FK).real
        est[~known] = model[~known]                # fill gaps from the model
        est[known] = data[known]                   # honour the data
    return est


# ---------------------------------------------------------------------------
# Run all methods on both scenarios
# ---------------------------------------------------------------------------
METHODS = [
    ("T–X", tx_interpolate),
    ("F–X (Spitz)", fx_interpolate),
    ("F–K (Gülünay)", fk_interpolate),
]

results = {}     # (scenario, method_name) -> reconstructed panel
errors = {}
inputs = {}
print(f"{'scenario':<20}{'method':<16}{'RMS err (% missing)':>20}")
for sc_name, mask in MASKS.items():
    missing = ~mask
    inp = D.copy()
    inp[missing] = 0.0
    inputs[sc_name] = inp
    print(f"{sc_name:<20}{'input':<16}{100 * missing.mean():>19.1f}% missing")
    for mname, mfunc in METHODS:
        rec = mfunc(D * mask[:, None], mask)
        results[(sc_name, mname)] = rec
        err = rms_error(rec, D, missing)
        errors[(sc_name, mname)] = err
        print(f"{sc_name:<20}{mname:<16}{err:>20.2f}")

# ---------------------------------------------------------------------------
# Figure: 2 x 4  (rows = scenario, cols = input / T-X / F-X / F-K)
# ---------------------------------------------------------------------------
import matplotlib.pyplot as plt

scenarios = list(MASKS.keys())
col_titles = ["Input (decimated)", "T–X", "F–X (Spitz)", "F–K (Gülünay)"]
n_keep = {sc: int(MASKS[sc].sum()) for sc in scenarios}

vmax = np.abs(D).max()
fig, axes = plt.subplots(2, 4, figsize=(13, 6.6), layout="constrained")

for r, sc in enumerate(scenarios):
    panels = [inputs[sc]] + [results[(sc, mn)] for mn, _ in METHODS]
    for c, panel in enumerate(panels):
        ax = axes[r, c]
        ax.imshow(panel.T, aspect="auto", cmap="seismic", vmin=-vmax, vmax=vmax,
                  extent=[x_axis[0], x_axis[-1], time_axis[-1], time_axis[0]],
                  interpolation="bilinear")
        if r == 0:
            ax.set_title(col_titles[c], fontsize=10.5)
        if c == 0:
            ax.set_ylabel(f"{sc}\nTime (s)", fontsize=10)
            ax.text(0.02, 0.03, f"kept {n_keep[sc]}/{NX}", transform=ax.transAxes,
                    fontsize=8, color="white",
                    bbox=dict(boxstyle="round,pad=0.2", fc="black", alpha=0.5))
        else:
            err = errors[(sc, col_titles[c])]
            ax.text(0.02, 0.03, f"RMS err {err:.1f}%", transform=ax.transAxes,
                    fontsize=8, color="white",
                    bbox=dict(boxstyle="round,pad=0.2", fc="black", alpha=0.5))
        if c == 0:
            ax.set_xlabel("Position x (m)", fontsize=9)
        else:
            ax.set_xlabel("Position x (m)", fontsize=9)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
out_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                       "figures", "term03_lec06")
out_dir = os.path.abspath(out_dir)
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "term03_lec06_interpolation_methods.png")
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"Saved figure to {out_path}")
