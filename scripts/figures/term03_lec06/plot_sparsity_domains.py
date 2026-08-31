"""
Term 3 Lecture 06 — Figure 3: the same data in three transform domains,
illustrating the unifying sparsity principle (Sec. 2.2).

Pedagogical point
-----------------
Every interpolation/regularization method succeeds by assuming the data have a
COMPACT representation in some transform domain, then reconstructing from that
compact model.  The methods differ only in which domain they choose.  This
figure shows ONE dataset -- three linear events of different dip -- in three
domains:

  (a) Time-space (t-x): the three events overlap and cross, so the data look
      complex.
  (b) F-K: a linear event t = tau + p*x maps to a single DIP (a line through
      the origin, k = -p*f), so the spectrum has only a few dominant
      components.
  (c) Linear Radon (tau-p): the same event focuses to a SINGLE POINT at its
      intercept tau and slowness p.

What looks like a complicated, overlapping wavefield in (a) is just three
coefficients in (b) or (c).  Interpolation = keep the few large coefficients in
such a domain, discard the rest, and transform back onto a regular grid.

Note: we use LINEAR events deliberately.  Hyperbolic CMP reflections do NOT
behave like (b) -- a hyperbola smears across a continuum of wavenumbers -- which
is exactly why F-K methods assume (locally) linear events (Sec. 3.3).

Self-contained: numpy + scipy + matplotlib only.
"""

import os

import numpy as np
from scipy.interpolate import RegularGridInterpolator

# ---------------------------------------------------------------------------
# Data: three linear events  t = tau + p*x
# ---------------------------------------------------------------------------
NX = 128                      # number of traces / spatial samples
X_MAX = 2000.0                # spatial extent (m)
DT = 0.002                    # time sampling (s)
NT = 600                      # number of time samples (0 .. ~1.2 s)
F0 = 30.0                     # Ricker dominant frequency (Hz)

x_axis = np.linspace(0.0, X_MAX, NX)
dx = x_axis[1] - x_axis[0]
time_axis = np.arange(NT) * DT

# (intercept tau [s], slowness p [s/m], amplitude)
EVENTS = [
    (0.15, 0.0004, 1.00),     # dipping one way   (~2500 m/s apparent)
    (0.60, 0.0000, 0.80),     # horizontal
    (1.05, -0.0004, 0.90),    # dipping the other way
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
# (b) F-K spectrum
# ---------------------------------------------------------------------------
FK = np.fft.fftshift(np.fft.fft2(D))          # shape (k, f)
k_axis = np.fft.fftshift(np.fft.fftfreq(NX, dx))        # cycles / m
f_axis = np.fft.fftshift(np.fft.fftfreq(NT, DT))        # Hz

mag = np.abs(FK).T                            # rows = f, cols = k
pos = f_axis >= 0
F_MAX = 80.0                                  # focus on the wavelet band
fmask = pos & (f_axis <= F_MAX)
f_disp = f_axis[fmask]
mag_disp = mag[fmask, :]
db = 20.0 * np.log10(mag_disp / mag_disp.max() + 1e-12)

# ---------------------------------------------------------------------------
# (c) Linear Radon transform  R(tau, p) = sum_i x_i(tau + p*x_i)
# ---------------------------------------------------------------------------
P_MAX = 0.0006                      # slowness range (s/m)  = +/-0.6 ms/m
NP = 200
p_axis = np.linspace(-P_MAX, P_MAX, NP)
tau_axis = time_axis

interp = RegularGridInterpolator((x_axis, time_axis), D, method="linear",
                                 bounds_error=False, fill_value=0.0)
pts_x = np.broadcast_to(x_axis[:, None], (NX, tau_axis.size))
R = np.zeros((tau_axis.size, NP))
for j, p in enumerate(p_axis):
    pts_t = tau_axis[None, :] + p * x_axis[:, None]
    pts = np.stack([pts_x, pts_t], axis=-1).reshape(-1, 2)
    R[:, j] = interp(pts).reshape(NX, tau_axis.size).sum(axis=0)

# Diagnostics: where are the Radon peaks?
print(f"data             : {NX} traces x {NT} samples, dx={dx:.1f} m, dt={DT*1e3:.0f} ms")
for tau, p, amp in EVENTS:
    print(f"  event amp {amp:.2f}: tau={tau:.2f} s, p={p*1e3:+.3f} ms/m")
peak = np.unravel_index(np.argmax(R), R.shape)
print(f"Radon max        : {R.max():.0f} at tau={tau_axis[peak[0]]:.3f} s, "
      f"p={p_axis[peak[1]]*1e3:+.3f} ms/m")

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
import matplotlib.pyplot as plt

fig, (ax_t, ax_fk, ax_r) = plt.subplots(1, 3, figsize=(12, 4.8),
                                        layout="constrained")

# ---- (a) time-space --------------------------------------------------------
vt = np.abs(D).max()
ax_t.imshow(D.T, aspect="auto", cmap="seismic", vmin=-vt, vmax=vt,
            extent=[x_axis[0], x_axis[-1], time_axis[-1], time_axis[0]],
            interpolation="bilinear")
ax_t.set_xlabel("Position x (m)")
ax_t.set_ylabel("Time (s)")
ax_t.set_title("(a) Time–space domain", fontsize=10.5)

# ---- (b) F-K ---------------------------------------------------------------
ax_fk.imshow(db, aspect="auto", cmap="inferno", vmin=-60, vmax=0,
             extent=[k_axis[0], k_axis[-1], f_disp[0], f_disp[-1]],
             origin="lower", interpolation="bilinear")
# mark the three event dips: k = -p*f
ff = np.array([0.0, F_MAX])
for tau, p, amp in EVENTS:
    ax_fk.plot(-p * ff, ff, color="cyan", ls="--", lw=0.9, alpha=0.7)
ax_fk.set_xlabel("Wavenumber k (cycles/m)")
ax_fk.set_ylabel("Frequency f (Hz)")
ax_fk.set_title("(b) F–K domain", fontsize=10.5)

# ---- (c) linear Radon ------------------------------------------------------
vr = np.percentile(R, 99)
ax_r.imshow(R, aspect="auto", cmap="inferno", vmin=0, vmax=vr,
            extent=[p_axis[0] * 1e3, p_axis[-1] * 1e3,
                    tau_axis[-1], tau_axis[0]],
            interpolation="bilinear")
# mark the three focused peaks
for tau, p, amp in EVENTS:
    ax_r.plot(p * 1e3, tau, "o", mfc="none", mec="cyan", ms=7, mew=1.2)
ax_r.set_xlabel("Slowness p (ms/m)")
ax_r.set_ylabel("Intercept τ (s)")
ax_r.set_title("(c) Linear Radon (τ–p) domain", fontsize=10.5)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
out_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                       "figures", "term03_lec06")
out_dir = os.path.abspath(out_dir)
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "term03_lec06_sparsity_domains.png")
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"Saved figure to {out_path}")
