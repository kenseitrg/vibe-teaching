"""
Term 3 Lecture 05 — Figure 7: Dual-sensor (PZ) deghosting principle.

Pedagogical point
-----------------
A dual-sensor streamer records pressure P (hydrophone) and vertical particle
velocity Vz (geophone).  For a plane wave the two are related by the acoustic
impedance, but with OPPOSITE sign for upgoing vs downgoing waves:

    upgoing primary  :  P and Vz have the SAME sign
    downgoing ghost  :  P and Vz have OPPOSITE signs

(the ghost is the primary reflected off the sea surface, R ~ -1).  Therefore the
scaled sum  P + Vz  reinforces the primary (same sign -> x2) and cancels the
ghost (opposite sign -> 0).  This removes the receiver ghost without an inverse
filter and without the spectral-notch problem of 1-D deghosting.

Model (illustrative): a Ricker primary at 50 ms and its ghost delayed by 40 ms
(at 90 ms).  pressure = primary + ghost (ghost same/positive phase on P);
scaled velocity = primary - ghost (ghost opposite phase on Vz); sum = 2 x primary.

Self-contained: numpy + matplotlib only.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

COL_P = "#0072B2"      # primary — blue
COL_G = "#D55E00"      # ghost — vermillion
COL_TRACE = "black"

# ---------------------------------------------------------------------------
# Traces
# ---------------------------------------------------------------------------
dt = 0.001
t = np.arange(0, 0.16, dt)
t_ms = t * 1000.0


def ricker(t, t0, f0=30.0):
    u = t - t0
    a = (np.pi * f0 * u) ** 2
    return (1 - 2 * a) * np.exp(-a)


t1, tau = 0.05, 0.04          # primary 50 ms, ghost delay 40 ms -> ghost 90 ms
w_prim = ricker(t, t1)
w_ghost = ricker(t, t1 + tau)

P = w_prim + w_ghost          # pressure: ghost same (positive) phase
Vz = w_prim - w_ghost         # scaled velocity: ghost opposite phase
S = P + Vz                    # sum: ghost cancels, primary x2

t1_ms, tg_ms = t1 * 1000, (t1 + tau) * 1000

# ---------------------------------------------------------------------------
# Figure: three stacked traces (pressure, velocity, sum)
# ---------------------------------------------------------------------------
fig, (ax_p, ax_v, ax_s) = plt.subplots(
    3, 1, sharex=True, figsize=(10, 6.5),
    gridspec_kw={"hspace": 0.45},
)

panels = [
    (ax_p, P, "(a) Hydrophone — pressure $P$"),
    (ax_v, Vz, "(b) Geophone — vertical velocity $V_z$ (scaled)"),
    (ax_s, S, "(c) Sum $P + V_z$ — deghosted output"),
]

for axx, tr, title in panels:
    axx.plot(t_ms, tr, color=COL_TRACE, lw=1.2)
    axx.axhline(0, color="grey", lw=0.5)
    for tt in (t1_ms, tg_ms):
        axx.axvline(tt, color="grey", ls=":", lw=0.7, alpha=0.6)
    axx.set_title(title, fontsize=9.5, loc="left")
    axx.set_xlim(0, 140)
    axx.set_ylim(-2.3, 2.5)
    axx.set_yticks([])
ax_s.set_xlabel("Time (ms)")

# annotations: primary (+) and ghost (+/-) on each panel
def mark(axx, x, y, text, color, dy):
    axx.annotate(text, xy=(x, y), xytext=(x, y + dy),
                 ha="center", fontsize=8.5, color=color,
                 arrowprops=dict(arrowstyle="-", color=color, lw=0.7, alpha=0.7))

# (a) pressure: primary +1, ghost +1 (both positive phase)
mark(ax_p, t1_ms, 1.0, "primary (+)", COL_P, 0.7)
mark(ax_p, tg_ms, 1.0, "ghost (+)", COL_G, 0.7)
# (b) velocity: primary +1, ghost -1 (opposite phase)
mark(ax_v, t1_ms, 1.0, "primary (+)", COL_P, 0.7)
mark(ax_v, tg_ms, -1.0, "ghost ($-$)", COL_G, -0.7)
# (c) sum: primary x2, ghost cancelled
mark(ax_s, t1_ms, 2.0, "primary ($\\times 2$)", COL_P, 0.35)
ax_s.annotate("ghost cancelled", xy=(tg_ms, 0.0), xytext=(tg_ms, -1.4),
              ha="center", fontsize=8.5, color=COL_G,
              arrowprops=dict(arrowstyle="-|>", color=COL_G, lw=0.8))

fig.suptitle(
    "Dual-sensor (PZ) deghosting: the ghost has opposite polarity on the "
    "pressure and velocity sensors, so $P + V_z$ cancels it",
    fontsize=11.5,
)

# ---------------------------------------------------------------------------
# Save + diagnostics
# ---------------------------------------------------------------------------
out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       "..", "..", "..",
                                       "figures", "term03_lec05"))
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "term03_lec05_pz_deghosting.png")
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"Saved figure to {out_path}")
ip = np.argmin(np.abs(t - t1)); ig = np.argmin(np.abs(t - (t1 + tau)))
print(f"primary: P={P[ip]:+.2f} Vz={Vz[ip]:+.2f} Sum={S[ip]:+.2f}")
print(f"ghost:   P={P[ig]:+.2f} Vz={Vz[ig]:+.2f} Sum={S[ig]:+.2f}")
print(f"max|Sum - 2*primary| = {np.max(np.abs(S - 2*w_prim)):.1e}")
