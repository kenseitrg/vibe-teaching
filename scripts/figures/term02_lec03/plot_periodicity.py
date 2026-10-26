"""Figure: Periodicity of water-layer reverberations (zero-offset view).

Two synthetic zero-offset traces. Left: a water layer of thickness h_w
over the seabed traps energy in reverberations — every round trip adds the
same delay dt_w = 2 h_w / v_w and multiplies the amplitude by
R_bottom * R_surface (both < 1), producing a decaying, strictly periodic
train of separate events (long-period multiples).
Right: the same physics with a shallow water layer (h_w = 30 m ->
dt_w = 0.04 s): the multiple period is shorter than the wavelet, so the
arrivals interfere — short-period reverberation 'fog'.
"""

import numpy as np
import matplotlib.pyplot as plt

DT = 0.004
H_WATER, V_WATER = 300.0, 1480.0
R_SURF, R_BOT = -1.0, 0.4           # free-surface and water-bottom reflectivities
T0 = 0.55                            # two-way time of the primary event


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


def build_trace(max_order=4):
    """Primary plus surface reverberations of order 1..max_order."""
    dt_w = 2 * H_WATER / V_WATER
    nt = int(2.6 / DT)
    trace = np.zeros(nt)
    t = np.arange(nt) * DT
    wav = ricker(30, 41, DT)
    amp = 1.0
    t_arr = T0
    half = (len(wav) - 1) // 2          # place the wavelet peak at t_arr
    for _ in range(max_order + 1):
        i0 = int(round(t_arr / DT)) - half
        if i0 >= 0 and i0 + len(wav) < nt:
            trace[i0:i0 + len(wav)] += amp * wav
        t_arr += dt_w
        amp *= R_BOT * R_SURF
    return trace, t, dt_w


trace, t, dt_w = build_trace()

fig = plt.figure(figsize=(10, 6.5))

# --- Left: the zero-offset trace ---------------------------------------------
ax1 = fig.add_axes((0.09, 0.13, 0.36, 0.74))
ax1.plot(trace, t, "k-", lw=1.0)
ax1.fill_betweenx(t, 0, trace, where=trace > 0, color="k", alpha=0.6)
ax1.set_ylim(2.6, 0)
ax1.set_xlim(-1.15, 1.15)
ax1.set_ylabel("Two-way time (s)")
ax1.set_xlabel("Amplitude")
ax1.set_title("Zero-offset trace ($h_w = 300$ m):\nperiodic decaying train",
              fontsize=11)
for k in range(4):
    tk = T0 + k * dt_w
    ax1.axhline(tk, color="0.6", ls=":", lw=0.8)
    ax1.text(1.18, tk, f"$t_0 + {k}\\,\\Delta t_{{w}}$" if k else "$t_0$",
             fontsize=9, va="center", color="0.35")
ax1.text(-1.12, 0.18, f"$\\Delta t_w = 2h_w/v_w = {dt_w * 1e3:.0f}$ ms",
         fontsize=10, color="crimson",
         bbox=dict(fc="white", ec="crimson", alpha=0.85))

# --- Right: long- vs short-period --------------------------------------------
ax2 = fig.add_axes((0.56, 0.13, 0.36, 0.74))
nt = len(t)
short = np.zeros(nt)
dt_short = 2 * 30.0 / V_WATER        # 30 m water layer -> 40 ms period
wav = ricker(30, 41, DT)
half = (len(wav) - 1) // 2           # place the wavelet peak at t_arr
t_arr, amp = T0, 1.0
for _ in range(60):
    i0 = int(round(t_arr / DT)) - half
    if i0 < 0 or i0 + len(wav) >= nt:
        break
    short[i0:i0 + len(wav)] += amp * wav
    t_arr += dt_short
    amp *= 0.6
ax2.plot(short, t, "k-", lw=1.0)
ax2.fill_betweenx(t, 0, short, where=short > 0, color="k", alpha=0.6)
ax2.set_ylim(2.6, 0)
ax2.set_xlim(-1.15, 1.15)
ax2.set_xlabel("Amplitude")
ax2.set_title("Same physics, shallow water ($h_w = 30$ m):\nshort-period 'fog'",
              fontsize=11)
ax2.text(0.02, 0.2, "$\\Delta t_w = 40$ ms\n$\\ll$ wavelet length\n$\\Rightarrow$ interference",
         fontsize=10, color="crimson", transform=ax2.transAxes,
         bbox=dict(fc="white", ec="crimson", alpha=0.85))

fig.suptitle("Periodicity: each water round trip adds $\\Delta t_w$ and multiplies "
             "the amplitude ($R_{bot}\\,R_{surf}$ per order)", fontsize=13)
fig.text(0.5, 0.02,
         "Left: long-period multiples appear as separate events, one per water "
         "round trip.\nRight: in shallow water the same train collapses into "
         "short-period multiples that interfere with everything — deconvolution "
         "territory.",
         ha="center", fontsize=10, color="0.25")
fig.savefig("figures/term02_lec03/term02_lec03_periodicity.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec03_periodicity.png")
