"""Figure: High-resolution parabolic Radon (sparse inversion).

Top row: iteration strip of the IRLS (iteratively re-weighted least
squares) solution — the LS panel (iteration 0) smears each event across
many curvatures; each iteration re-weights the model norm so large
coefficients survive and small ones are crushed, focusing the panel
while keeping the data fit.

Bottom row: demultiple comparison. Muting |residual| > 20 ms in the LS
panel leaves smeared multiple energy inside the kept zone -> residual
multiples leak into the output. The high-resolution panel separates the
families cleanly -> far cleaner subtraction.

Objective being minimized (Cauchy sparseness norm):
  J(m) = || d - L^T m ||^2  +  lambda * sum_q ln(1 + m_q^2 / sigma^2)
solved by re-weighting: each iteration solves a damped normal system
with weight w_q = 1 / (1 + m_q^2/sigma^2) and a decreasing lambda.
"""

import numpy as np
import matplotlib.pyplot as plt

DT, TMAX = 0.004, 2.6
DX, XMAX = 25.0, 3000.0
NQ = 69
Q_LABEL = np.linspace(-40, 300, NQ)         # residual moveout (ms) at far offset
BAND = (5.0, 90.0)

EVENTS = [  # (t0 [s], residual at far offset [ms], amplitude)
    (0.55, -10, 1.0), (1.15, -5, 0.9), (1.80, 0, 0.8),
    (0.90, 60, 0.7), (1.60, 105, 0.55),
]

SIGMA_FRAC = 0.3        # Cauchy sigma as fraction of max|m| per frequency
LAM0, LAM_DECAY = 1e-3, 0.6
NITER = 40
SNAP_ITERS = (0, 1, 2, 5, 10, 40)


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


def make_post_nmo():
    nt = int(TMAX / DT)
    x = np.arange(0, XMAX + DX, DX)
    data = np.zeros((nt, len(x)))
    wav = ricker(30, 41, DT)
    for t0, res_ms, amp in EVENTS:
        q = res_ms * 1e-3 / XMAX**2
        for j, xj in enumerate(x):
            tj = t0 + q * xj**2
            i0 = int(np.floor(tj / DT))
            frac = tj / DT - i0
            for off, wt in ((0, 1 - frac), (1, frac)):
                s = i0 + off - 20
                lo, hi = max(0, s), min(nt, s + 41)
                if hi > lo:
                    data[lo:hi, j] += amp * wt * wav[lo - s:hi - s]
    return data, x


data, x = make_post_nmo()
nt, nx = data.shape
D = np.fft.rfft(data, axis=0)
freqs = np.fft.rfftfreq(nt, DT)
q_axis = Q_LABEL * 1e-3 / XMAX**2
nf = len(freqs)


def L_op(f):
    return np.exp(2j * np.pi * f * np.outer(q_axis, x**2))


M_ls = np.zeros((NQ, nf), dtype=complex)
M_hr = np.zeros((NQ, nf), dtype=complex)
snaps = {it: np.zeros((NQ, nf), dtype=complex) for it in SNAP_ITERS}

for k, f in enumerate(freqs):
    if not (BAND[0] <= f <= BAND[1]):
        continue
    L = L_op(f)
    d = D[k, :]
    m0, *_ = np.linalg.lstsq(L.T, d, rcond=1e-8)   # LS start (iteration 0)
    M_ls[:, k] = m0
    G = L.conj() @ L.T
    rhs = L.conj() @ d
    mh = m0.copy()
    lam = LAM0 * np.trace(G).real / NQ
    for it in range(1, NITER + 1):
        sig = SIGMA_FRAC * np.max(np.abs(mh)) + 1e-20
        w = 1.0 / (1.0 + (np.abs(mh) / sig) ** 2)   # Cauchy IRLS weights
        mh = np.linalg.solve(G + lam * np.diag(w), rhs)
        lam *= LAM_DECAY                            # continuation
        if it in snaps:
            snaps[it][:, k] = mh
    M_hr[:, k] = mh


def panel_to_time(M):
    Mf = np.zeros((NQ, nt), dtype=complex)
    Mf[:, :nf] = M
    return np.fft.irfft(Mf, n=nt, axis=1)


def data_recon(M):
    Drec = np.zeros((nf, nx), dtype=complex)
    for k, f in enumerate(freqs):
        if BAND[0] <= f <= BAND[1]:
            Drec[k, :] = L_op(f).T @ M[:, k]
    return np.fft.irfft(Drec, n=nt, axis=0)


rms = lambda a: float(np.sqrt(np.mean(a ** 2)))
print(f"LS residual: {rms(data - data_recon(M_ls)) / rms(data) * 100:.1f}%")
print(f"HR residual: {rms(data - data_recon(M_hr)) / rms(data) * 100:.1f}%")


def mute_and_recon(M):
    keep = np.where(np.abs(Q_LABEL) <= 20)[0]
    Mk = np.zeros_like(M)
    Mk[keep, :] = M[keep, :]
    return data_recon(Mk)


prim_ls = mute_and_recon(M_ls)
prim_hr = mute_and_recon(M_hr)

# --- plot ----------------------------------------------------------------------
fig = plt.figure(figsize=(15, 9))
gs = fig.add_gridspec(2, 6, height_ratios=(1, 1.25), hspace=0.35, wspace=0.25)

v = np.percentile(np.abs(data), 99.5)
vp = np.percentile(np.abs(panel_to_time(M_ls)), 99.5)

# iteration strip
for i, it in enumerate(SNAP_ITERS):
    ax = fig.add_subplot(gs[0, i])
    ax.imshow(panel_to_time(snaps[it]).T, extent=[Q_LABEL[0], Q_LABEL[-1], TMAX, 0],
              aspect="auto", cmap="gray", vmin=-vp, vmax=vp)
    ax.set_title(f"iteration {it}", fontsize=10)
    if i == 0:
        ax.set_ylabel("Time (s)")
        ax.text(0.03, 0.95, "LS panel:\nsmeared", transform=ax.transAxes,
                fontsize=9, va="top", color="crimson")
    if it == SNAP_ITERS[-1]:
        ax.text(0.03, 0.95, "focused:\nHR panel", transform=ax.transAxes,
                fontsize=9, va="top", color="seagreen")
    ax.set_xlabel("Residual moveout (ms)")

# bottom row: panels + demultiple results
axp = fig.add_subplot(gs[1, 0])
axp.imshow(panel_to_time(M_ls).T, extent=[Q_LABEL[0], Q_LABEL[-1], TMAX, 0],
           aspect="auto", cmap="gray", vmin=-vp, vmax=vp)
axp.set_title("LS panel\n(smearing leaks multiples\ninto the kept zone)")
axp.set_ylabel("Time (s)")

axq = fig.add_subplot(gs[1, 1])
axq.imshow(panel_to_time(M_hr).T, extent=[Q_LABEL[0], Q_LABEL[-1], TMAX, 0],
           aspect="auto", cmap="gray", vmin=-vp, vmax=vp)
axq.set_title("HR panel\n(same data, sparse model)")

for axm in (axp, axq):
    axm.axvline(-20, color="crimson", ls="--", lw=1.4)
    axm.axvline(20, color="crimson", ls="--", lw=1.4)
    axm.set_xlabel("Residual moveout (ms)")

ax1 = fig.add_subplot(gs[1, 2])
ax1.imshow(data, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
           vmin=-v, vmax=v)
ax1.set_title("Input (after NMO)")

ax2 = fig.add_subplot(gs[1, 3])
ax2.imshow(prim_ls, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
           vmin=-v, vmax=v)
ax2.set_title("Demultiple from LS panel\n(residual multiple leakage)")

ax3 = fig.add_subplot(gs[1, 4])
ax3.imshow(prim_hr, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
           vmin=-v, vmax=v)
ax3.set_title("Demultiple from HR panel\n(clean primaries)")

ax4 = fig.add_subplot(gs[1, 5])
ax4.imshow(prim_ls - prim_hr, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
           vmin=-v, vmax=v)
ax4.set_title("Difference:\nwhat sparseness bought")

for ax in (ax1, ax2, ax3, ax4):
    ax.set_xlabel("Offset (m)")

fig.suptitle("High-resolution Radon: same data, same physics — a sparse model "
             "norm focuses the panel and stops mute leakage", fontsize=14)
fig.savefig("figures/term02_lec03/term02_lec03_highres_radon.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec03_highres_radon.png")
