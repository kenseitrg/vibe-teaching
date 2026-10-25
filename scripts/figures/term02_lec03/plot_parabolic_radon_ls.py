"""Figure: Parabolic Radon — adjoint vs least-squares inverse.

Top: a CMP gather after approximate NMO (velocity between primaries
and multiples). Residual moveout of every event is close to parabolic:
primaries slightly overcorrected (negative residual), multiples
undercorrected (positive residual).

Middle: the ADJOINT transform (stack along parabolas, m = L^H d).
Energy smears across curvatures and the reconstruction L m does NOT
reproduce the input — the operator pair (adjoint, stack) is not an
inverse pair.

Bottom: the LEAST-SQUARES inverse, m = (L^H L + lambda^2 I)^(-1) L^H d
per frequency slice. Events focus into small blobs and the
reconstruction matches the input to noise level.

What to notice: focusing in the Radon panel is not cosmetic — it is
what decides how cleanly a mute can separate primaries from multiples.
"""

import numpy as np
import matplotlib.pyplot as plt

DT, TMAX = 0.004, 2.4
DX, XMAX = 50.0, 3000.0
NQ = 69
Q_LABEL = np.linspace(-40, 300, NQ)            # residual Dt (ms) at far offset

# Events in the *post-NMO* domain: t(x) = t0 + q * x^2,
# with q expressed as residual moveout (s) at XMAX.
# (label, t0 [s], residual at far offset [ms], amplitude)
EVENTS = [
    ("primary 1", 0.55, -12, 1.0),
    ("primary 2", 1.15,  -6, 0.9),
    ("primary 3", 1.75,  -3, 0.8),
    ("multiple 1", 0.90, 60, 0.7),
    ("multiple 2", 1.60, 105, 0.55),
]


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


def make_post_nmo():
    nt = int(TMAX / DT)
    x = np.arange(0, XMAX + DX, DX)
    data = np.zeros((nt, len(x)))
    wav = ricker(30, 41, DT)
    for label, t0, res_ms, amp in EVENTS:
        q = (res_ms * 1e-3) / XMAX**2          # s / m^2
        for j, xj in enumerate(x):
            tj = t0 + q * xj**2
            i0 = int(np.floor(tj / DT))
            frac = tj / DT - i0
            for off, wt in ((0, 1 - frac), (1, frac)):
                start = i0 + off - (len(wav) - 1) // 2
                lo, hi = max(0, start), min(nt, start + len(wav))
                if hi > lo:
                    data[lo:hi, j] += amp * wt * wav[lo - start:hi - start]
    return data, x


data, x = make_post_nmo()
nt, nx = data.shape
D = np.fft.rfft(data, axis=0)
freqs = np.fft.rfftfreq(nt, DT)

# Radon curvatures expressed as residual moveout (ms at XMAX) -> q [s/m^2]
q_axis = Q_LABEL * 1e-3 / XMAX**2


def radon_ops(f):
    """Adjoint operator per frequency: L[q, x] = exp(i 2 pi f q x^2)."""
    return np.exp(2j * np.pi * f * np.outer(q_axis, x**2))


LAM = 1e-8                                    # SVD truncation threshold for
                                              # the stabilized LS inverse


M_adj = np.zeros((len(q_axis), len(freqs)), dtype=complex)
M_ls = np.zeros_like(M_adj)
for k, f in enumerate(freqs):
    if not (5.0 <= f <= 90.0):
        continue
    L = radon_ops(f)
    d = D[k, :]                               # (nx,)
    M_adj[:, k] = (L.conj() @ d) / nx         # scaled adjoint for display
    # Stabilized least-squares inverse: solve d = L^T m per frequency with
    # small singular values truncated (equivalent to damping lambda^2 I).
    m, *_ = np.linalg.lstsq(L.T, d, rcond=LAM)
    M_ls[:, k] = m


def to_time(M):
    """Inverse temporal FFT of a q-f panel; keep only signal band."""
    Mf = np.zeros((len(q_axis), nt), dtype=complex)
    Mf[:, :len(freqs)] = M
    rec = np.fft.irfft(Mf, n=nt, axis=1)
    return rec


def data_recon(M):
    """Data-space reconstruction d = L m per frequency, then inverse FFT.

    M is the (nq, nf) complex frequency-domain Radon panel.
    """
    Drec = np.zeros((len(freqs), nx), dtype=complex)
    for k, f in enumerate(freqs):
        if not (5.0 <= f <= 90.0):
            continue
        L = radon_ops(f)
        Drec[k, :] = L.T @ M[:, k]
    out = np.fft.irfft(Drec, n=nt, axis=0)
    return out


radj = to_time(M_adj)
rls = to_time(M_ls)
dadj = data_recon(M_adj)
dls = data_recon(M_ls)

rms = lambda a: float(np.sqrt(np.mean(a**2)))
print(f"adjoint reconstruction residual: {rms(data - dadj) / rms(data) * 100:.1f}%")
print(f"LS reconstruction residual:      {rms(data - dls) / rms(data) * 100:.1f}%")

fig, axes = plt.subplots(2, 3, figsize=(15, 8), gridspec_kw={"height_ratios": [1, 1]})
v = np.percentile(np.abs(data), 99.5)
vp = np.percentile(np.abs(rls), 99.5)

im = axes[0, 0].imshow(data, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
                       vmin=-v, vmax=v)
axes[0, 0].set_title("CMP after approx. NMO\n(primaries overcorrected, "
                     "multiples undercorrected)")
axes[0, 0].set_xlabel("Offset (m)")
axes[0, 0].set_ylabel("Time (s)")

axes[0, 1].imshow(radj.T, extent=[Q_LABEL[0], Q_LABEL[-1], TMAX, 0], aspect="auto",
                  cmap="gray", vmin=-vp, vmax=vp)
axes[0, 1].set_title("ADJOINT Radon panel\n(smearing across curvatures)")
axes[0, 1].set_xlabel("Residual moveout at 3000 m (ms)")

axes[0, 2].imshow(data - dadj, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
                  vmin=-v, vmax=v)
axes[0, 2].set_title("Adjoint reconstruction fails\n(residual ≫ 100% — NOT an inverse)")

axes[1, 1].imshow(rls.T, extent=[Q_LABEL[0], Q_LABEL[-1], TMAX, 0], aspect="auto",
                  cmap="gray", vmin=-vp, vmax=vp)
axes[1, 1].set_title("LEAST-SQUARES Radon panel\n(events focus into blobs)")
axes[1, 1].set_xlabel("Residual moveout at 3000 m (ms)")
axes[1, 1].set_ylabel("Time (s)")

axes[1, 2].imshow(data - dls, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
                  vmin=-v, vmax=v)
axes[1, 2].set_title(f"LS reconstruction residual\n"
                     f"{rms(data - dls) / rms(data) * 100:.0f}% — invertible")
axes[1, 0].imshow(data, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
                  vmin=-v, vmax=v)
axes[1, 0].set_title("Input (repeated for comparison)")
axes[1, 0].set_xlabel("Offset (m)")

# annotate event families in the LS panel
axes[1, 1].axvline(20, color="crimson", ls="--", lw=1.5)
axes[1, 1].text(25, 0.12, "primaries\n(q < 20 ms)", color="royalblue", fontsize=10)
axes[1, 1].text(180, 0.12, "multiples", color="crimson", fontsize=10)

fig.suptitle("Parabolic Radon: redefine the forward transform as the "
             "least-squares inverse of the adjoint", fontsize=14)
fig.text(0.5, 0.01,
         "Both panels describe the same data, but only the LS panel is a "
         "faithful (invertible) representation — the prerequisite for muting "
         "there and transforming back.",
         ha="center", fontsize=11, color="0.25")
fig.tight_layout(rect=(0, 0.035, 1, 0.93))
fig.savefig("figures/term02_lec03/term02_lec03_parabolic_radon_ls.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec03_parabolic_radon_ls.png")
