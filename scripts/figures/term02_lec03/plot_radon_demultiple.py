"""Figure: Parabolic Radon demultiple — the Hampson (1986) workflow.

Panels left to right:
  1. Input CMP gather (hyperbolic primaries + multiples).
  2. After NMO with a velocity chosen BETWEEN the primary and multiple
     stacking velocities: primaries ~flat to slightly overcorrected
     (residual 0...-45 ms), multiples undercorrected (+60...+110 ms,
     small enough that the residual moveout is still parabolic and the
     NMO stretch stays small).
  3. Least-squares parabolic Radon panel: primaries focus at small
     residual moveout, multiples at large. The red dashed line is the
     mute boundary: keep |residual| < 50 ms, zero the rest.
  4. Inverse Radon of the kept zone, NMO removed -> estimated primaries.
  5. Difference: input minus output = the removed multiples.

What to notice: the far offsets are cleaned best (moveout difference is
largest there); the near offsets keep a residual because primaries and
multiples converge to the same traveltime at x -> 0. This motivates the
near-offset hard mute discussed in the limitations section.

Data are synthesised directly in the frequency domain,
    d(f, x) = sum_events amp * W(f) * exp(-2i*pi*f*t0(x)),
t0(x) = sqrt(t0^2 + (x/v)^2), so every event lies exactly on its
hyperbola (per-sample picking would add timing jitter that biases the
Radon fit).
"""

import numpy as np
import matplotlib.pyplot as plt

DT, TMAX = 0.004, 2.6
DX, XMAX = 25.0, 2000.0

# (label, t0 [s], stacking velocity [m/s], amplitude)
EVENTS = [
    ("primary 1", 0.70, 2300, 1.0),
    ("primary 2", 1.50, 2500, 0.9),
    ("primary 3", 2.20, 2700, 0.85),
    ("multiple 1", 2.00, 1900, 0.7),
    ("multiple 2", 1.35, 1950, 0.55),
    ("multiple 3", 1.00, 2000, 0.4),
]

VNMO = 2300.0        # NMO velocity between primary and multiple velocities
Q_LABEL = np.arange(-60.0, 321.0, 5.0)     # residual moveout (ms) at far offset
BAND = (5.0, 90.0)
LAM_FRAC = 1e-2      # damping as fraction of ||G||^2
MUTE = 50.0          # [ms] half-width of the kept q-zone
F_DOM = 30.0         # [Hz] dominant frequency of the wavelet


def ricker(f_dom, n, dt):
    """Ricker wavelet, centred at sample (n - 1) / 2."""
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


# --- data: synthesised in the frequency domain (exact hyperbolas) ---------------
nt = int(TMAX / DT)
x = np.arange(0.0, XMAX + DX, DX)
nx = len(x)
freqs = np.fft.rfftfreq(nt, DT)
nf = len(freqs)
band = np.where((freqs >= BAND[0]) & (freqs <= BAND[1]))[0]

wav = ricker(F_DOM, 41, DT)
# spectrum re-centred at t = 0 (the time-domain wavelet starts at sample 0)
W = np.fft.rfft(wav, n=nt) * np.exp(2j * np.pi * freqs * 20 * DT)

data_f = np.zeros((nf, nx), dtype=complex)
for _, t0, v, amp in EVENTS:
    t0x = np.sqrt(t0 ** 2 + (x / v) ** 2)          # hyperbolic moveout
    for k in band:
        data_f[k, :] += amp * W[k] * np.exp(-2j * np.pi * freqs[k] * t0x)
data = np.fft.irfft(data_f, n=nt, axis=0)


def nmo(data, x, v, inverse=False):
    """NMO correction (or its exact inverse) by linear interpolation.

    Forward: output(t) = input(sqrt(t^2 + (x/v)^2)) — an event at
    t0x(x) = sqrt(t0^2 + (x/v)^2) lands flat at t0.
    Inverse: the exact opposite mapping, output(t) = input(sqrt(t^2 - (x/v)^2))
    for t >= x/v (zero otherwise), used to undo the correction.
    """
    t = np.arange(data.shape[0]) * DT
    out = np.zeros_like(data)
    for j, xj in enumerate(x):
        if not inverse:   # forward: read the input at the shifted time
            t_read = np.sqrt(t ** 2 + (xj / v) ** 2)
            out[:, j] = np.interp(t_read, t, data[:, j], left=0.0, right=0.0)
        else:             # inverse: undo the shift; no input maps to t < x/v
            ok = t >= xj / v
            t_read = np.sqrt(t[ok] ** 2 - (xj / v) ** 2)
            out[ok, j] = np.interp(t_read, t, data[:, j], left=0.0, right=0.0)
    return out


q_axis = Q_LABEL * 1e-3 / XMAX ** 2

# --- NMO with the velocity between primaries and multiples ----------------------
dnmo = nmo(data, x, VNMO)
Dnmo = np.fft.rfft(dnmo, axis=0)

# --- LS parabolic Radon panel of the NMO'd gather -------------------------------
# modeling: d(f) = L^T m(f),  L(q, x) = exp(-2i*pi*f*q*x^2)
M = np.zeros((len(q_axis), nf), dtype=complex)
Drec = np.zeros((nf, nx), dtype=complex)
for k in band:
    L = np.exp(-2j * np.pi * freqs[k] * np.outer(q_axis, x ** 2))
    G = L.conj() @ L.T
    M[:, k] = np.linalg.solve(
        G + LAM_FRAC * np.linalg.norm(G, 2) * np.eye(len(q_axis)),
        L.conj() @ Dnmo[k, :])
    Drec[k, :] = L.T @ M[:, k]

# QC: reconstruction residual of the full (unmuted) panel
rms = lambda a: float(np.sqrt(np.mean(a ** 2)))
print(f"LS Radon data-fit residual (vs NMO'd gather): "
      f"{rms(np.fft.irfft(Dnmo - Drec, n=nt, axis=0)) / rms(dnmo) * 100:.1f}%")


def to_time(Mc):
    """Inverse temporal FFT of a q-f panel."""
    Mf = np.zeros((len(q_axis), nt), dtype=complex)
    Mf[:, :nf] = Mc
    return np.fft.irfft(Mf, n=nt, axis=1)


radon_t = to_time(M)

# mute: keep small residual moveout
keep = np.where(np.abs(Q_LABEL)[:, None] <= MUTE, M, 0.0)

# inverse Radon of the kept zone -> NMO-domain primaries, then inverse NMO
# NOTE: M/keep columns are indexed by frequency index k (band holds those indices)
Drec = np.zeros((nf, nx), dtype=complex)
for k in band:
    L = np.exp(-2j * np.pi * freqs[k] * np.outer(q_axis, x ** 2))
    Drec[k, :] = L.T @ keep[:, k]
prim_nmo = np.fft.irfft(Drec, n=nt, axis=0)
prim = nmo(prim_nmo, x, VNMO, inverse=True)
removed = data - prim

# --- figure ---------------------------------------------------------------------
fig, axes = plt.subplots(1, 5, figsize=(17, 6.2), sharey=True)
v = np.percentile(np.abs(data), 99.5)
vp = np.percentile(np.abs(radon_t), 99.0)

axes[0].imshow(data, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
               vmin=-v, vmax=v)
axes[0].set_title("1. Input CMP\n(primaries + multiples)")
axes[0].set_ylabel("Time (s)")

axes[1].imshow(dnmo, extent=[0, XMAX, TMAX, 0], aspect="auto",
               cmap="gray", vmin=-v, vmax=v)
axes[1].set_title(f"2. NMO @ {VNMO:.0f} m/s\n(between primary and multiple)")

axes[2].imshow(radon_t.T, extent=[Q_LABEL[0], Q_LABEL[-1], TMAX, 0], aspect="auto",
               cmap="gray", vmin=-vp, vmax=vp)
axes[2].axvline(-MUTE, color="crimson", ls="--", lw=1.8)
axes[2].axvline(MUTE, color="crimson", ls="--", lw=1.8)
axes[2].fill_betweenx([0, TMAX], MUTE, Q_LABEL[-1], color="crimson", alpha=0.12)
axes[2].fill_betweenx([0, TMAX], Q_LABEL[0], -MUTE, color="crimson", alpha=0.12)
axes[2].text(90, 0.10, "muted\n(multiples)", color="crimson", fontsize=10)
axes[2].text(-55, 0.10, "kept\n(primaries)", color="royalblue", fontsize=10)
axes[2].set_title(f"3. LS parabolic Radon\n+ mute |residual| > {MUTE:.0f} ms")
axes[2].set_xlabel(f"Residual moveout at {XMAX:.0f} m (ms)")

axes[3].imshow(prim, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
               vmin=-v, vmax=v)
axes[3].set_title("4. Inverse Radon +\ninverse NMO: primaries")

axes[4].imshow(removed, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
               vmin=-v, vmax=v)
axes[4].set_title("5. Removed\n(= 1 − 4)")

for ax in axes:
    ax.set_xlabel("Offset (m)")
axes[2].set_xlabel(f"Residual moveout at {XMAX:.0f} m (ms)")

fig.suptitle("Radon demultiple workflow (Hampson 1986): NMO -> parabolic Radon "
             "-> mute -> inverse", fontsize=14)
fig.tight_layout(rect=(0, 0, 1, 0.92))
fig.savefig("figures/term02_lec03/term02_lec03_radon_demultiple.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec03_radon_demultiple.png")
