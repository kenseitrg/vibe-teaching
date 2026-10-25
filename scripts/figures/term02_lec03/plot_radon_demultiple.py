"""Figure: Parabolic Radon demultiple — the Hampson (1986) workflow.

Panels left to right:
  1. Input CMP gather (hyperbolic primaries + multiples).
  2. After NMO with a velocity chosen BETWEEN the primary and multiple
     stacking velocities: primaries slightly overcorrected (residual
     parabolas curving up), multiples undercorrected (curving down).
  3. Least-squares parabolic Radon panel: primaries focus at small
     residual moveout, multiples at large. The red dashed line is the
     mute boundary: keep |residual| < 20 ms, zero the rest.
  4. Inverse Radon of the kept zone, NMO removed -> estimated primaries.
  5. Difference: input minus output = the removed multiples.

What to notice: the far offsets are cleaned best (moveout difference is
largest there); the near offsets keep a residual because primaries and
multiples converge to the same traveltime at x -> 0. This motivates the
near-offset hard mute discussed in the limitations section.
"""

import numpy as np
import matplotlib.pyplot as plt

DT, TMAX = 0.004, 2.6
DX, XMAX = 25.0, 3000.0

# (label, t0 [s], stacking velocity [m/s], amplitude)
EVENTS = [
    ("primary 1", 0.55, 1900, 1.0),
    ("primary 2", 1.15, 2200, 0.9),
    ("primary 3", 1.80, 2450, 0.85),
    ("multiple 1", 0.90, 1600, 0.7),
    ("multiple 2", 1.60, 1720, 0.55),
    ("multiple 3", 2.25, 1780, 0.4),
]

VNMO = 2300.0        # NMO velocity between primary and multiple velocities
NQ = 69
Q_LABEL = np.linspace(-60, 320, NQ)     # residual moveout (ms) at far offset
BAND = (5.0, 90.0)
LAM = 1e-8


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


def make_cmp():
    nt = int(TMAX / DT)
    x = np.arange(0, XMAX + DX, DX)
    data = np.zeros((nt, len(x)))
    wav = ricker(30, 41, DT)
    for label, t0, v, amp in EVENTS:
        for j, xj in enumerate(x):
            tj = np.sqrt(t0**2 + (xj / v) ** 2)
            i0 = int(np.floor(tj / DT))
            frac = tj / DT - i0
            for off, wt in ((0, 1 - frac), (1, frac)):
                start = i0 + off - (len(wav) - 1) // 2
                lo, hi = max(0, start), min(nt, start + len(wav))
                if hi > lo:
                    data[lo:hi, j] += amp * wt * wav[lo - start:hi - start]
    return data, x


def nmo(data, x, v, inverse=False):
    """NMO correction (or its inverse) by spline interpolation of traces."""
    nt = data.shape[0]
    t = np.arange(nt) * DT
    out = np.zeros_like(data)
    for j, xj in enumerate(x):
        shift = np.sqrt(t**2 + (xj / v) ** 2) if not inverse else \
            np.sqrt(np.maximum(t**2 - (xj / v) ** 2, 0.0))
        out[:, j] = np.interp(t, shift, data[:, j], left=0.0)
    return out


def ls_parabolic_radon(dnmo, x):
    """Frequency-domain LS parabolic Radon: returns (nq, nf) complex panel."""
    nt, nx = dnmo.shape
    D = np.fft.rfft(dnmo, axis=0)
    freqs = np.fft.rfftfreq(nt, DT)
    q_axis = Q_LABEL * 1e-3 / XMAX**2
    M = np.zeros((len(q_axis), len(freqs)), dtype=complex)
    for k, f in enumerate(freqs):
        if not (BAND[0] <= f <= BAND[1]):
            continue
        L = np.exp(2j * np.pi * f * np.outer(q_axis, x**2))
        m, *_ = np.linalg.lstsq(L.T, D[k, :], rcond=LAM)
        M[:, k] = m
    return M, freqs, q_axis


def inv_radon(M, x, nt):
    """Data-space reconstruction d = L m per frequency, back to time."""
    freqs = np.fft.rfftfreq(nt, DT)
    Drec = np.zeros((len(freqs), len(x)), dtype=complex)
    q_axis = Q_LABEL * 1e-3 / XMAX**2
    for k, f in enumerate(freqs):
        if not (BAND[0] <= f <= BAND[1]):
            continue
        L = np.exp(2j * np.pi * f * np.outer(q_axis, x**2))
        Drec[k, :] = L.T @ M[:, k]
    return np.fft.irfft(Drec, n=nt, axis=0)


data, x = make_cmp()
dnmo = nmo(data, x, VNMO)
M, freqs, q_axis = ls_parabolic_radon(dnmo, x)

nt = data.shape[0]
radon_t = np.fft.irfft(
    np.pad(M, ((0, 0), (0, nt // 2 + 1 - M.shape[1]))), n=nt, axis=1)

# mute: keep small residual moveout
keep = np.zeros_like(M)
iq_keep = np.where(np.abs(Q_LABEL) <= 20)[0]
keep[iq_keep, :] = M[iq_keep, :]

prim_nmo = inv_radon(keep, x, data.shape[0])
prim = nmo(prim_nmo, x, VNMO, inverse=True)
removed = data - prim

fig, axes = plt.subplots(1, 5, figsize=(17, 6.2), sharey=True)
v = np.percentile(np.abs(data), 99.5)
vp = np.percentile(np.abs(radon_t), 99.5)

axes[0].imshow(data, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
               vmin=-v, vmax=v)
axes[0].set_title("1. Input CMP\n(primaries + multiples)")
axes[0].set_ylabel("Time (s)")

axes[1].imshow(dnmo, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
               vmin=-v, vmax=v)
axes[1].set_title(f"2. NMO @ {VNMO:.0f} m/s\n(between primary and multiple)")

axes[2].imshow(radon_t.T, extent=[Q_LABEL[0], Q_LABEL[-1], TMAX, 0], aspect="auto",
               cmap="gray", vmin=-vp, vmax=vp)
axes[2].axvline(-20, color="crimson", ls="--", lw=1.8)
axes[2].axvline(20, color="crimson", ls="--", lw=1.8)
axes[2].fill_betweenx([0, TMAX], 20, Q_LABEL[-1], color="crimson", alpha=0.12)
axes[2].fill_betweenx([0, TMAX], Q_LABEL[0], -20, color="crimson", alpha=0.12)
axes[2].text(60, 0.15, "muted\n(multiples)", color="crimson", fontsize=10)
axes[2].text(-48, 0.15, "kept\n(primaries)", color="royalblue", fontsize=10)
axes[2].set_title("3. LS parabolic Radon\n+ mute |residual| > 20 ms")
axes[2].set_xlabel("Residual moveout at 3000 m (ms)")

axes[3].imshow(prim, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
               vmin=-v, vmax=v)
axes[3].set_title("4. Inverse Radon +\ninverse NMO: primaries")

axes[4].imshow(removed, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
               vmin=-v, vmax=v)
axes[4].set_title("5. Removed\n(= 1 − 4)")

for ax in axes:
    ax.set_xlabel("Offset (m)")

fig.suptitle("Radon demultiple workflow (Hampson 1986): NMO -> parabolic Radon "
             "-> mute -> inverse", fontsize=14)
fig.text(0.5, 0.015,
         "Note how the far offsets are cleaned almost perfectly, while the near "
         "offsets retain residual multiple energy: at small offsets the moveout "
         "difference\nbetween primaries and multiples vanishes, and the mute in "
         "the Radon domain cannot help — the first limitation of the method family.",
         ha="center", fontsize=10, color="0.25")
fig.tight_layout(rect=(0, 0.05, 1, 0.92))
fig.savefig("figures/term02_lec03/term02_lec03_radon_demultiple.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec03_radon_demultiple.png")
