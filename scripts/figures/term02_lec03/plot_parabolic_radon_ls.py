"""Figure: Parabolic Radon — adjoint vs least-squares inverse.

Top: a CMP gather after approximate NMO (velocity between primaries
and multiples). Primaries are properly NMO corrected (flat); multiples
are undercorrected and keep residual moveout that is close to parabolic.

Middle: the ADJOINT transform (stack along parabolas, m = L^H d).
Energy smears across curvatures and the reconstruction L m does NOT
reproduce the input — the operator pair (adjoint, reverse adjoint) is
not an inverse pair.

Bottom: the LEAST-SQUARES inverse, m = (L^H L + lambda I)^(-1) L^H d
per frequency slice. Events focus into small blobs and the
reconstruction matches the input to a few percent.

What to notice: focusing in the Radon panel is not cosmetic — it is
what decides how cleanly a mute can separate primaries from multiples.

Data are synthesised directly in the frequency domain,
    d(f, x) = sum_events amp * W(f) * exp(-2i*pi*f*(t0 + q*x^2)),
so every event lies exactly on a parabolic trajectory of the operator
(per-sample picking of trajectories would add timing jitter that no
Radon operator can fit).
"""

import numpy as np
import matplotlib.pyplot as plt

DT, TMAX = 0.004, 2.4
DX, XMAX = 50.0, 3000.0
Q_LABEL = np.linspace(-40, 300, 69)            # residual Dt (ms) at far offset

# Events in the *post-NMO* domain: t(x) = t0 + q * x^2,
# with q expressed as residual moveout (ms) at XMAX.
# (label, t0 [s], residual at far offset [ms], amplitude)
EVENTS = [
    ("primary 1", 0.55, -10, 1.0),
    ("primary 2", 1.15,  -5, 0.9),
    ("primary 3", 1.75,   0, 0.8),
    ("multiple 1", 0.90, 60, 0.7),
    ("multiple 2", 1.60, 105, 0.55),
]
F_DOM = 30.0                     # [Hz] dominant frequency of the wavelet
BAND = (5.0, 90.0)               # [Hz] frequencies used in the inversion
LAM_FRAC = 1e-4                  # damping as fraction of ||G||^2


def ricker(f_dom, n, dt):
    """Ricker wavelet, centred at sample (n - 1) / 2."""
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


# --- data: synthesised in the frequency domain ---------------------------------
nt = int(TMAX / DT)
x = np.arange(0.0, XMAX + DX, DX)
nx = len(x)
freqs = np.fft.rfftfreq(nt, DT)
nf = len(freqs)
q_axis = Q_LABEL * 1e-3 / XMAX ** 2       # [s/m^2]
band = np.where((freqs >= BAND[0]) & (freqs <= BAND[1]))[0]

wav = ricker(F_DOM, 41, DT)
# spectrum re-centred at t = 0 (the time-domain wavelet starts at sample 0)
W = np.fft.rfft(wav, n=nt) * np.exp(2j * np.pi * freqs * 20 * DT)

data_f = np.zeros((nf, nx), dtype=complex)
for _, t0, res_ms, amp in EVENTS:
    q = res_ms * 1e-3 / XMAX ** 2
    for k in band:
        data_f[k, :] += amp * W[k] * np.exp(-2j * np.pi * freqs[k] * (t0 + q * x ** 2))
data = np.fft.irfft(data_f, n=nt, axis=0)


# --- forward operator: d(f) = L^T m(f),  L(q,x) = exp(-2i*pi*f*q*x^2) -----------
def L_op(f):
    return np.exp(-2j * np.pi * f * np.outer(q_axis, x ** 2))


# adjoint panel (scaled by 1/nx for display) and damped LS panel
M_adj = np.zeros((len(q_axis), nf), dtype=complex)
M_ls = np.zeros_like(M_adj)
for k in band:
    L = L_op(freqs[k])
    G = L.conj() @ L.T
    M_adj[:, k] = (L.conj() @ data_f[k, :]) / nx
    M_ls[:, k] = np.linalg.solve(
        G + LAM_FRAC * np.linalg.norm(G, 2) * np.eye(len(q_axis)),
        L.conj() @ data_f[k, :])


def to_time(M):
    """Inverse temporal FFT of a q-f panel; keep only signal band."""
    Mf = np.zeros((len(q_axis), nt), dtype=complex)
    Mf[:, :nf] = M
    return np.fft.irfft(Mf, n=nt, axis=1)


def data_recon(M):
    """Data-space reconstruction d = L^T m per frequency, then inverse FFT."""
    Drec = np.zeros((nf, nx), dtype=complex)
    for k in band:
        Drec[k, :] = L_op(freqs[k]).T @ M[:, k]
    return np.fft.irfft(Drec, n=nt, axis=0)


radj = to_time(M_adj)
rls = to_time(M_ls)
dadj = data_recon(M_adj)
dls = data_recon(M_ls)

rms = lambda a: float(np.sqrt(np.mean(a**2)))
res_adj = rms(data - dadj) / rms(data) * 100
res_ls = rms(data - dls) / rms(data) * 100
print(f"adjoint reconstruction residual: {res_adj:.1f}%")
print(f"LS reconstruction residual:      {res_ls:.1f}%")

# --- figure ---------------------------------------------------------------------
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
v = np.percentile(np.abs(data), 99.5)
vp_adj = np.percentile(np.abs(radj), 99.5)   # per-panel clips: the raw adjoint
vp_ls = np.percentile(np.abs(rls), 99.5)     # overshoots LS amplitudes ~17x
QZOOM = (-40.0, 150.0)           # display range of the q axis (ms)
qext = [QZOOM[0], QZOOM[1], TMAX, 0.0]
# keep only the displayed q range: with the full 69-sample axis (-40..300 ms)
# imshow would compress it into the extent and displace every event visually
qdisp = (Q_LABEL >= QZOOM[0]) & (Q_LABEL <= QZOOM[1])
xext = [0, XMAX, TMAX, 0.0]

axes[0, 0].imshow(data, extent=xext, aspect="auto", cmap="gray", vmin=-v, vmax=v)
axes[0, 0].set_title("CMP after approx. NMO\n(primaries flat, multiples "
                     "undercorrected)")
axes[0, 0].set_xlabel("Offset (m)")
axes[0, 0].set_ylabel("Time (s)")

axes[0, 1].imshow(radj[qdisp].T, extent=qext, aspect="auto", cmap="gray",
                  vmin=-vp_adj, vmax=vp_adj)
axes[0, 1].set_title("ADJOINT Radon panel\n(smearing across curvatures)")
axes[0, 1].set_xlabel("Residual moveout at 3000 m (ms)")

axes[0, 2].imshow(data - dadj, extent=xext, aspect="auto", cmap="gray",
                  vmin=-v, vmax=v)
axes[0, 2].set_title(f"Adjoint reconstruction fails\n"
                     f"residual = {res_adj:.0f}% of data — NOT an inverse")
axes[0, 2].set_xlabel("Offset (m)")

axes[1, 0].imshow(data, extent=xext, aspect="auto", cmap="gray", vmin=-v, vmax=v)
axes[1, 0].set_title("Input (repeated for comparison)")
axes[1, 0].set_xlabel("Offset (m)")
axes[1, 0].set_ylabel("Time (s)")

axes[1, 1].imshow(rls[qdisp].T, extent=qext, aspect="auto", cmap="gray",
                  vmin=-vp_ls, vmax=vp_ls)
axes[1, 1].set_title("LEAST-SQUARES Radon panel\n(events focus into blobs)")
axes[1, 1].set_xlabel("Residual moveout at 3000 m (ms)")

axes[1, 2].imshow(data - dls, extent=xext, aspect="auto", cmap="gray",
                  vmin=-v, vmax=v)
axes[1, 2].set_title(f"LS reconstruction residual\n"
                     f"{res_ls:.1f}% of data — invertible")
axes[1, 2].set_xlabel("Offset (m)")

# annotate event families in the LS panel. Arrows point at the focused
# blobs (EVENTS above: primaries at q = -10..0 ms, multiples at 60/105 ms);
# each label sits on its own side of the q = 20 ms mute line.
axes[1, 1].axvline(20, color="crimson", ls="--", lw=1.5)
axes[1, 1].annotate("primaries\n(q < 20 ms)", xy=(-10, 1.15), xytext=(-38, 0.85),
                    color="royalblue", fontsize=10, ha="left", va="center",
                    arrowprops=dict(arrowstyle="->", color="royalblue", lw=1.2))
axes[1, 1].annotate("multiples", xy=(105, 1.60), xytext=(122, 2.18),
                    color="crimson", fontsize=10, ha="center",
                    arrowprops=dict(arrowstyle="->", color="crimson", lw=1.2))

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
