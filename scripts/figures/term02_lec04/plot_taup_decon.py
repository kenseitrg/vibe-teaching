"""Figure: Predictive deconvolution in the tau-p domain.

Top: CMP/shot gather with a water layer: seabed primary, deep primary,
and the reverberation family (every arrival repeats with the vertical
period dt0 = 2h/v at zero offset). In x-t the period varies with
offset (previous figure), so one prediction gap cannot serve all
traces.

The recipe: (1) forward tau-p (LS, per frequency); (2) on each p-trace
the period is constant, dt_tau(p) = dt0*sqrt(1 - p^2 v_w^2) — apply
per-trace predictive deconvolution with that gap; (3) mute the large-p
traces beyond the deepest primary's ray parameter; (4) inverse tau-p.

Panels: input gather; tau-p panel (before); after per-p decon +
p-mute; back in x-t: result and removed energy. Bottom: the ACF of a
far-offset trace (smeared, offset-dependent periods) vs the ACF of a
p-trace (clean periodicity at the known gap) — why the filter design
works in tau-p and fails in x-t.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_toeplitz

DT, TMAX = 0.004, 2.4
DX, XMAX = 12.5, 2000.0
H, VW = 100.0, 1500.0
DT0 = 2 * H / VW                        # 0.1333 s vertical period
P_MAX_MUTE = 1.05 / 2400.0              # mute just beyond deepest primary tip p=1/2400
GAP_EXTRA = 2                           # extra samples of gap (practice)
OP_LEN = 30                             # prediction operator length (~120 ms)

NT = int(TMAX / DT)
X = np.arange(0, XMAX + DX, DX)
NX = len(X)
T = np.arange(NT) * DT


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


def minphase_wavelet(f_dom, n, dt):
    """Minimum-phase wavelet (Ricker convolved with a one-pole decay) —
    the stationarity/minimum-phase assumption of Wiener deconvolution."""
    tt = np.arange(n) * dt
    w = np.convolve(ricker(f_dom, n // 2 + 1, dt), np.exp(-tt * 60.0))[:n]
    return w / np.abs(w).max()


def add_event(data, t0, v, amp, wav):
    for j, xj in enumerate(X):
        tj = np.sqrt(t0 ** 2 + (xj / v) ** 2)
        i0 = int(np.floor(tj / DT))
        frac = tj / DT - i0
        for off, wt in ((0, 1 - frac), (1, frac)):
            s = i0 + off - (len(wav) - 1) // 2
            lo, hi = max(0, s), min(NT, s + len(wav))
            if hi > lo:
                data[lo:hi, j] += amp * wt * wav[lo - s:hi - s]


wav = minphase_wavelet(35, 61, DT)
gather = np.zeros((NT, NX))
# seabed primary + deep primary
add_event(gather, 0.1333, VW, 0.9, wav)
add_event(gather, 1.10, 2400, 1.0, wav)
# water-layer reverberations attached to both primaries (5 orders)
for base_t0, base_amp in [(0.1333, 0.9), (1.10, 1.0)]:
    for n in range(1, 6):
        add_event(gather, base_t0 + n * DT0, VW, base_amp * 0.72 ** n, wav)

# --- tau-p machinery: slant stack + rho-filtered back projection ----------
# Forward: scaled adjoint (slant stack) — physical, event-like panel traces.
# Inverse: adjoint modeling with the rho filter (|f| ramp), i.e. filtered
# back projection — the same round trip as Term 2 Lecture 02.
P_AXIS = np.arange(0.0, 1.15 / VW, 0.01 / VW)   # dense; slightly beyond 1/v
NP_ = len(P_AXIS)


def taup_forward(d):
    """Slant stack: U(p, tau) = (1/NX) sum_x d(tau + p x, x).

    Linear interpolation of each trace onto the shifted time grid; samples
    shifted out of the record are zero.
    """
    U = np.zeros((NP_, NT))
    for ip, p in enumerate(P_AXIS):
        acc = np.zeros(NT)
        for j, xj in enumerate(X):
            acc += np.interp(T, T + p * xj, d[:, j], left=0.0, right=0.0)
        U[ip] = acc / NX
    return U


def taup_inverse(U):
    """Least-squares inverse of the slant stack: per frequency solve
    d = argmin || U - L.conj() d ||^2  (damped), i.e. invert the adjoint —
    the same 'redefine the transform as an LS inverse' trick as the
    parabolic Radon lecture figure."""
    freqs = np.fft.rfftfreq(NT, DT)
    Uf = np.fft.rfft(U * NX, axis=1) * DT   # undo the 1/NX scaling, grid units
    Df = np.zeros((len(freqs), NX), dtype=complex)
    for k, f in enumerate(freqs):
        if f < 2.0 or f > 100.0:
            continue
        L = np.exp(-2j * np.pi * f * np.outer(P_AXIS, X))
        rhs = L.T @ Uf[:, k]
        G = L.T @ L.conj()
        lam2 = (0.02 * np.trace(G).real / NX) ** 2
        Df[k, :] = np.linalg.solve(G + lam2 * np.eye(NX), rhs)
    return np.fft.irfft(Df, n=NT, axis=0) * DX / DT / NX   # grid-unit cleanup


def pred_decon(trace, gap_samples, n=OP_LEN, eps=0.05):
    """Prediction-error deconvolution with the given prediction gap.

    The prediction filter h predicts x[k] from x[k-gap-n+1..k-gap];
    its output must be aligned with the gap delay, otherwise the
    'predictor' would also see the current sample (spiking decon).
    """
    rxx = np.correlate(trace, trace, "full")[len(trace) - 1:]
    rxx = np.concatenate([rxx, np.zeros(gap_samples + n + 1)])
    R = rxx[:n] * (1 + eps)
    rhs = rxx[gap_samples:gap_samples + n]
    h = solve_toeplitz(R, rhs)
    h_delayed = np.zeros(gap_samples + n)
    h_delayed[gap_samples:] = h
    pred = np.convolve(trace, h_delayed)[:len(trace)]
    return trace - pred


U = taup_forward(gather)
U_decon = U.copy()
imute = np.searchsorted(P_AXIS, P_MAX_MUTE)
panel_norm = np.linalg.norm(U)
for ip, p in enumerate(P_AXIS):
    if ip >= imute:
        continue                      # muted p range: leave (zeroed below)
    tr = U[ip]
    if np.linalg.norm(tr) < 1e-8 * panel_norm:
        continue
    gap = int(round(DT0 * np.sqrt(1 - (p * VW) ** 2) / DT))
    trd = pred_decon(tr, gap)
    if np.all(np.isfinite(trd)):
        U_decon[ip] = trd
# p-mute
U_decon[imute:, :] = 0.0

# rho-filter gain calibration: round-trip the un-deconvolved panel once and
# correct the (deterministic) back-projection gain so amplitudes match.
rec0 = taup_inverse(U)
gain = np.linalg.norm(gather) / max(np.linalg.norm(rec0), 1e-12)
taup_inverse_cal = lambda Uu: taup_inverse(Uu) * gain
result = taup_inverse_cal(U_decon)
removed = gather - result

# ACF comparison: far-offset trace vs a p-trace
def acf(tr, nlag=500):
    return np.correlate(tr, tr, "full")[len(tr) - 1:len(tr) + nlag] / \
        (np.correlate(tr, tr, "full")[len(tr) - 1] + 1e-20)


acf_xt = acf(gather[:, -1])
tr_p = U[10]                            # a p-trace of the slant-stack panel
acf_p = acf(tr_p)

# --- plot -----------------------------------------------------------------------
fig = plt.figure(figsize=(16, 9))
gs = fig.add_gridspec(2, 4, hspace=0.42, wspace=0.3)

v = np.percentile(np.abs(gather), 99.5)
ax = fig.add_subplot(gs[0, 0])
ax.imshow(gather, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
          vmin=-v, vmax=v)
ax.set_xlabel("Offset (m)")
ax.set_ylabel("Time (s)")
ax.set_title("input gather:\nreverberating water layer", fontsize=10.5)
ax.axhline(0.19, color="royalblue", ls=":", lw=1)
ax.text(XMAX * 0.55, 0.05, "water-bottom family\n(seabed + reverbs)", fontsize=8.5,
        color="royalblue")
ax.text(XMAX * 0.55, 1.32, "deep primary\n+ its reverbs", fontsize=8.5,
        color="royalblue")

ax = fig.add_subplot(gs[0, 1])
vv = np.percentile(np.abs(U), 99.5)
ax.imshow(U, extent=[P_AXIS[0] * 1e3, P_AXIS[-1] * 1e3, TMAX, 0],
          aspect="auto", cmap="gray", vmin=-vv, vmax=vv)
ax.set_xlabel("p (ms/m)")
ax.set_ylabel(r"Intercept time $\tau$ (s)")
ax.set_title("tau-p (slant stack):\nhyperbolas -> ellipses", fontsize=10.5)
ax.axvline(P_MAX_MUTE * 1e3, color="crimson", ls="--", lw=1.5)
ax.text(P_MAX_MUTE * 1e3 + 0.01, 1.7, "p-mute", color="crimson", fontsize=9,
        rotation=90)

ax = fig.add_subplot(gs[0, 2])
vvd = np.percentile(np.abs(U_decon), 99.5)
ax.imshow(U_decon, extent=[P_AXIS[0] * 1e3, P_AXIS[-1] * 1e3, TMAX, 0],
          aspect="auto", cmap="gray", vmin=-vvd, vmax=vvd)
ax.set_xlabel("p (ms/m)")
ax.set_ylabel(r"Intercept time $\tau$ (s)")
ax.set_title("after per-p predictive decon\n+ p-mute: reverbs gone", fontsize=10.5)

# p-traces before/after at three p values
ax = fig.add_subplot(gs[0, 3])
for k, (ip, col) in enumerate([(15, "crimson"), (45, "darkorange"),
                               (80, "seagreen")]):
    trb = U[ip] / (np.abs(U[ip]).max() + 1e-12)
    tra = U_decon[ip] / (np.abs(U[ip]).max() + 1e-12)
    ax.plot(0.9 * trb + 3 - k, T, color=col, lw=0.8, alpha=0.55)
    ax.plot(0.9 * tra + 3 - k, T, color=col, lw=1.1)
    gap_ms = DT0 * np.sqrt(1 - (P_AXIS[ip] * VW) ** 2) * 1e3
    ax.text(3 - k + 0.35, 2.28, f"p={P_AXIS[ip]*1e3:.2f}\ngap {gap_ms:.0f} ms",
            fontsize=7.5, color=col, ha="center")
ax.set_xlim(-0.6, 3.9)
ax.set_ylim(TMAX, 0)
ax.set_yticks([])
ax.set_title("p-traces before (faint)\nand after (bold) decon", fontsize=10.5)

# bottom row: ACF evidence + workflow + fine print
ax = fig.add_subplot(gs[1, 0])
lags = np.arange(len(acf_xt)) * DT * 1e3
ax.plot(lags, acf_xt, "k", lw=1.0)
ax.set_xlim(0, 700)
ax.set_xlabel("Lag (ms)")
ax.set_ylabel("Normalized ACF")
ax.set_title("ACF of far-offset trace (x-t):\nperiod smeared ~135-165 ms",
             fontsize=10.5)
for lag_ms in [135, 270, 405, 540]:
    ax.axvline(lag_ms, color="crimson", ls=":", lw=1)

ax = fig.add_subplot(gs[1, 1])
lags = np.arange(len(acf_p)) * DT * 1e3
ax.plot(lags, acf_p, "seagreen", lw=1.0)
ax.set_xlim(0, 700)
ax.set_xlabel("Lag (ms)")
ax.set_title("ACF of one p-trace:\nclean periodicity at dt(p)", fontsize=10.5)
p_mid = P_AXIS[45]
gap_ms = DT0 * np.sqrt(1 - (p_mid * VW) ** 2) * 1e3
for k in range(1, 5):
    ax.axvline(k * gap_ms, color="seagreen", ls=":", lw=1)
ax.text(0.45, 0.82, f"p = {p_mid*1e3:.2f} ms/m\n" + r"$\Delta\tau(p)$ = "
        f"{gap_ms:.0f} ms", transform=ax.transAxes, fontsize=9,
        bbox=dict(fc="white", ec="seagreen", alpha=0.85))

ax = fig.add_subplot(gs[1, 2:])
ax.axis("off")
ax.text(0.0, 0.97,
        "workflow and the fine print\n"
        "---------------------------\n"
        "x-t gather  ->  tau-p (slant stack)  ->  per-trace predictive\n"
        "decon with gap = dt0*sqrt(1 - p^2 v_w^2)  ->  p-mute  ->  inverse\n"
        "tau-p (the same LS machinery as the Radon demultiple figure).\n\n"
        "1. The gap tracks the analytic period: constant per p, known from\n"
        "   water depth - no picking on the data.\n"
        "2. p-mute protects against steep noise beyond the reflection family\n"
        "   (and against the ellipse tips of the water-bottom events).\n"
        "3. Assumes the multiple generator is LOCALLY FLAT (1D): dipping\n"
        "   water bottoms break the constant-period-per-p assumption.\n"
        "4. Wiener assumptions (Term 1 Lec 06) still apply: stationary,\n"
        "   minimum phase, additive white noise.\n\n"
        "=> the tool of choice for short-period water reverberations;\n"
        "   structural generators and long-period multiples need SRME.",
        va="top", fontsize=10, family="monospace")

fig.suptitle("tau-p predictive deconvolution: organize by ray parameter, "
             "deconvolve with the analytic period", fontsize=14)
fig.savefig("figures/term02_lec04/term02_lec04_taup_decon.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec04_taup_decon.png")
