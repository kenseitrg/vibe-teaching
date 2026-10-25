"""Figure: The moveout fingerprint of multiples in a CMP gather.

Left: CMP gather with two primaries and the first two orders of the
water-bottom multiple family. The multiples are delayed at zero offset
but arrive increasingly late at far offset: their stacking velocity is
lower than that of any primary reaching the same time, and each higher
order adds even more moveout (steeper dip).
Right: the moveout difference dt(x) between each event and the deepest
primary (same arrival time at zero offset is NOT the same arrival at far
offset). This residual is what move-out discrimination exploits.

Model: water 300 m @ 1480 m/s; sediment 1700 -> 2200 m/s (compaction);
primaries from 900 m and 1800 m depth. Multiples computed from layered
normal-incidence two-way times ( Dix-consistent hyperbolic moveout with
Vrms of their own propagation).
"""

import numpy as np
import matplotlib.pyplot as plt

DT, TMAX = 0.004, 3.2
DX, XMAX = 25.0, 3000.0

# (label, t0 [s], vrms [m/s], amplitude)
EVENTS = [
    ("water bottom",           0.41, 1480, 0.9),
    ("primary 1 (900 m)",      1.30, 1850, 1.0),
    ("primary 2 (1800 m)",     2.40, 2100, 1.0),
    ("WB multiple, order 1",   1.22, 1600, 0.55),
    ("WB multiple, order 2",   2.04, 1690, 0.35),
    ("WB multiple, order 3",   2.86, 1760, 0.22),
]


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


def make_gather():
    nt = int(TMAX / DT)
    t = np.arange(nt) * DT
    x = np.arange(0, XMAX + DX, DX)
    wav = ricker(28, 45, DT)
    data = np.zeros((nt, len(x)))
    curves = {}
    for label, t0, v, amp in EVENTS:
        times = np.sqrt(t0**2 + (x / v) ** 2)
        curves[label] = times
        for j, tj in enumerate(times):
            i0 = int(np.floor(tj / DT))
            frac = tj / DT - i0
            for off, wt in ((0, 1 - frac), (1, frac)):
                start = i0 + off - (len(wav) - 1) // 2
                lo, hi = max(0, start), min(nt, start + len(wav))
                if hi > lo:
                    data[lo:hi, j] += amp * wt * wav[lo - start:hi - start]
    return data, t, x, curves


data, t, x, curves = make_gather()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 7), gridspec_kw={"width_ratios": [1.55, 1]})

# --- CMP gather ---------------------------------------------------------------
vmax = np.percentile(np.abs(data), 99.5)
ax1.imshow(data, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
           vmin=-vmax, vmax=vmax)
prim_c, mult_c = "royalblue", "crimson"
for label, t0, v, amp in EVENTS:
    if "multiple" in label or label == "water bottom":
        c, ls = mult_c, "--"
    else:
        c, ls = prim_c, "-"
    ax1.plot(x, curves[label], ls, color=c, lw=1.8)
    ax1.text(x[-1] * 1.01, curves[label][-1], label, fontsize=8.5, color=c,
             va="center", ha="left")
ax1.set_xlim(0, XMAX * 1.28)
ax1.set_ylim(TMAX, 0)
ax1.set_xlabel("Offset (m)")
ax1.set_ylabel("Two-way time (s)")
ax1.set_title("CMP gather: primaries (blue) vs multiples (red dashed)")

# --- Moveout difference --------------------------------------------------------
ax2.axhline(0, color="0.5", lw=0.8)
t_ref = curves["primary 2 (1800 m)"]
for label, t0, v, amp in EVENTS:
    if label in ("water bottom", "primary 2 (1800 m)"):
        continue
    dt = curves[label] - curves[label][0]           # moveout relative to own t0
    dt_ref = t_ref - t_ref[0]                       # moveout of the deep primary
    c = mult_c if "multiple" in label else prim_c
    ax2.plot(x, (dt - dt_ref) * 1e3, color=c,
             ls="--" if "multiple" in label else "-", lw=1.8,
             label=label if "primary" not in label else None)
ax2.set_xlabel("Offset (m)")
ax2.set_ylabel("Differential moveout vs deep primary (ms)")
ax2.set_title("Same $t_0$, different moveout:\nthe discrimination signal")
ax2.legend(fontsize=8.5, loc="lower right")
ax2.set_xlim(0, XMAX)
ax2.grid(alpha=0.3)

fig.suptitle("Multiples travel more of their path in slow shallow layers: "
             "lower velocity, more moveout, steeper dip per order", fontsize=13)
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig("figures/term02_lec03/term02_lec03_multiple_moveout.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec03_multiple_moveout.png")
