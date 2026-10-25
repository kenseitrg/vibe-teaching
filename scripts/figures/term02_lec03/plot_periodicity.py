"""Figure: Periodicity of water-layer reverberations (zero-offset view).

Left: normal-incidence raypath family of one reflector below a water
layer — the primary, then first-, second- and third-order reverberations,
each one bouncing one extra round trip in the water layer.
Middle: the resulting zero-offset trace. Every extra round trip adds the
same delay dt_w = 2 h_w / v_w and multiplies the amplitude by
R_bottom * R_surface (both < 1), producing a decaying, strictly periodic
train.
Right: the same idea compared with the wavelet length — the multiple
period of this example (~0.4 s) is much longer than the wavelet
(~0.08 s), so this is a long-period multiple: separate events. A short
water layer (e.g. h_w = 30 m -> dt_w = 0.04 s) would push the arrivals
inside one wavelet: short-period multiple, i.e. reverberation 'fog'.
"""

import numpy as np
import matplotlib.pyplot as plt

DT = 0.004
H_WATER, V_WATER = 300.0, 1480.0
R_SURF, R_BOT = -0.85, 0.4          # free-surface and water-bottom reflectivities
T0 = 0.55                            # two-way time of the primary below seabed


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
    for _ in range(max_order + 1):
        i0 = int(round(t_arr / DT))
        if i0 + len(wav) < nt:
            trace[i0:i0 + len(wav)] += amp * wav
        t_arr += dt_w
        amp *= R_BOT * R_SURF
    return trace, t, dt_w


trace, t, dt_w = build_trace()

fig = plt.figure(figsize=(13, 7))

# --- Left: raypath schematic -------------------------------------------------
ax1 = fig.add_axes((0.03, 0.14, 0.24, 0.72))
ax1.axhspan(0, H_WATER, color="#cfe8ff", alpha=0.85)
ax1.axhspan(H_WATER, 340, color="#d9c9a8", alpha=0.9)
ax1.axhline(0, color="k", lw=2)
ax1.axhline(H_WATER, color="saddlebrown", lw=2)
ax1.axhline(340, color="dimgray", lw=2)

xb = 70.0
order_color = ["darkblue", "crimson", "darkorange", "seagreen", "purple"]
for order in range(5):
    # zig-zag: source/receiver at x=0, extra bounces in the water layer
    xs = [0.0]
    zs = [0.0]
    for k in range(order):            # extra water round trips
        xs += [xb, xb]
        zs += [H_WATER, 0.0]
    xs += [xb]                        # final trip to the deep reflector
    zs += [340.0]
    ax1.plot(xs, zs, color=order_color[order], lw=1.8, alpha=0.9)
ax1.plot(0, 0, "*", ms=15, color="darkorange", zorder=5)
ax1.set_xlim(-30, 130)
ax1.set_ylim(340, -40)
ax1.set_xlabel("Offset (m)")
ax1.set_ylabel("Depth (m)")
ax1.set_title("Normal-incidence ray family\n(primary + reverberations)", fontsize=11)

# --- Middle: the zero-offset trace -------------------------------------------
ax2 = fig.add_axes((0.36, 0.14, 0.28, 0.72))
ax2.plot(trace, t, "k-", lw=1.0)
ax2.fill_betweenx(t, 0, trace, where=trace > 0, color="k", alpha=0.6)
ax2.set_ylim(2.6, 0)
ax2.set_xlim(-1.15, 1.15)
ax2.set_ylabel("Two-way time (s)")
ax2.set_xlabel("Amplitude")
ax2.set_title("Zero-offset trace:\nperiodic decaying train", fontsize=11)
for k in range(4):
    tk = T0 + k * dt_w
    ax2.axhline(tk, color="0.6", ls=":", lw=0.8)
    ax2.text(1.18, tk, f"$t_0 + {k}\\,\\Delta t_{{w}}$" if k else "$t_0$",
             fontsize=9, va="center", color="0.35")
ax2.text(-1.12, 0.18, f"$\\Delta t_w = 2h/v = {dt_w * 1e3:.0f}$ ms",
         fontsize=10, color="crimson",
         bbox=dict(fc="white", ec="crimson", alpha=0.85))

# --- Right: long- vs short-period --------------------------------------------
ax3 = fig.add_axes((0.70, 0.14, 0.27, 0.72))
nt = len(t)
short = np.zeros(nt)
dt_short = 2 * 30.0 / V_WATER        # 30 m water layer -> 40 ms period
wav = ricker(30, 41, DT)
t_arr, amp = T0, 1.0
for _ in range(60):
    i0 = int(round(t_arr / DT))
    if i0 + len(wav) >= nt:
        break
    short[i0:i0 + len(wav)] += amp * wav
    t_arr += dt_short
    amp *= 0.6
ax3.plot(short, t, "k-", lw=1.0)
ax3.fill_betweenx(t, 0, short, where=short > 0, color="k", alpha=0.6)
ax3.set_ylim(2.6, 0)
ax3.set_xlim(-1.15, 1.15)
ax3.set_xlabel("Amplitude")
ax3.set_title("Same physics, shallow water ($h=30$ m):\nshort-period 'fog'", fontsize=11)
ax3.text(0.02, 0.2, "$\\Delta t_w = 40$ ms\n$\\ll$ wavelet length\n$\\Rightarrow$ interference",
         fontsize=10, color="crimson", transform=ax3.transAxes,
         bbox=dict(fc="white", ec="crimson", alpha=0.85))

fig.suptitle("Periodicity: each water round trip adds $\\Delta t_w$ and multiplies "
             "the amplitude ($R_{bot}\\,R_{surf}$ per order)", fontsize=13)
fig.text(0.5, 0.02,
         "Left: one subsurface reflector generates a whole family of "
         "reverberations. Middle: long-period multiples appear as separate "
         "events.\nRight: in shallow water the same family collapses into "
         "short-period multiples that interfere with everything — deconvolution "
         "territory.",
         ha="center", fontsize=10, color="0.25")
fig.savefig("figures/term02_lec03/term02_lec03_periodicity.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec03_periodicity.png")
