"""Figure: The multiple period varies with offset — and tau-p fixes it.

Left: raypaths of a water-layer reverberation for increasing emergence
angle. One round trip in the water layer along a slanted path is
LONGER than the vertical round trip: dt(p) = dt_0 / cos(theta), with
sin(theta) = p * v_w.

Middle: what this does to a CMP gather. The reverberation train from a
deeper primary: at near offsets the train repeats with the vertical
period dt_0; at far offsets every arrival of the family follows its own
hyperbola and the local period stretches. A single prediction gap
cannot match all offsets at once — the limitation of predictive
deconvolution in x-t.

Right: in the tau-p domain every p-trace contains ONE propagation angle
per event family, so the period is constant along the trace:
dt_tau(p) = dt_0 * sqrt(1 - p^2 v_w^2)   (intercept-time period),
a known, analytic function of p. Predictive deconvolution can then be
applied trace-by-trace in tau-p (next figure).
"""

import numpy as np
import matplotlib.pyplot as plt

H, VW = 100.0, 1500.0
DT0 = 2 * H / VW                     # vertical round trip = 0.1333 s
DT = 0.002
TMAX = 2.2
F_DOM = 40.0


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


fig = plt.figure(figsize=(15, 6.5))

# --- left: raypaths ----------------------------------------------------------
ax1 = fig.add_axes((0.03, 0.16, 0.24, 0.66))
ax1.axhspan(0, H, color="#cfe8ff", alpha=0.85)
ax1.axhspan(H, 150, color="#d9c9a8", alpha=0.9)
ax1.axhline(0, color="k", lw=2)
ax1.axhline(H, color="saddlebrown", lw=2)
angles = [5, 25, 45, 60]
colors = plt.cm.viridis(np.linspace(0.1, 0.85, len(angles)))
for c, th in zip(colors, angles):
    xw = H * np.tan(np.radians(th))
    xs = np.array([0, xw, 0, xw, 0])
    zs = np.array([0, H, 0, H, 0])
    ax1.plot(xs, zs, color=c, lw=1.8)
    ax1.plot([-xw / 2], [-8], "o", ms=0)
    ax1.text(xs[-1] + 8, 8, f"{th}$^\\circ$", fontsize=8, color=c, va="center")
ax1.plot(0, 0, "*", ms=14, color="darkorange", zorder=5)
ax1.set_xlim(-15, 260)
ax1.set_ylim(150, -25)
ax1.set_xlabel("Offset (m)")
ax1.set_ylabel("Depth (m)")
ax1.set_title("One water round trip,\nfour emergence angles", fontsize=11)

# --- middle: reverberation train in a CMP -------------------------------------
ax2 = fig.add_axes((0.33, 0.16, 0.32, 0.66))
nt = int(TMAX / DT)
t = np.arange(nt) * DT
offsets = [0, 900, 1800]      # m
cols = ["k", "darkblue", "crimson"]
wav = ricker(F_DOM, 41, DT)
traces = {}
for xoff, col in zip(offsets, cols):
    tr = np.zeros(nt)
    # deep primary + water reverberations; each arrival follows a hyperbola
    # with water velocity; zero-offset times t0 + n*dt0(p=0)
    n_arr = 9
    for n in range(n_arr):
        t0 = 0.5 + n * DT0
        amp = 0.75 ** n
        tj = np.sqrt(t0**2 + (xoff / VW) ** 2)
        i0 = int(round(tj / DT))
        if i0 + len(wav) < nt:
            tr[i0:i0 + len(wav)] += amp * wav
    traces[xoff] = tr
    ax2.plot(0.55 * tr / max(np.abs(tr).max(), 1e-12) + xoff / 1800, t, color=col, lw=0.9)

for xoff, col, lbl in zip(offsets, cols,
                          ["x = 0", "x = 900 m", "x = 1800 m"]):
    # local period annotation
    if xoff == 0:
        y1, y2 = 0.5, 0.5 + DT0
    else:
        y1 = np.sqrt(0.5**2 + (xoff / VW) ** 2)
        y2 = np.sqrt((0.5 + DT0) ** 2 + (xoff / VW) ** 2)
    ax2.annotate("", xy=(xoff / 1800 - 0.28, y2), xytext=(xoff / 1800 - 0.28, y1),
                 arrowprops=dict(arrowstyle="<->", color=col))
    ax2.text(xoff / 1800 - 0.33, (y1 + y2) / 2,
             f"{(y2 - y1) * 1e3:.0f} ms", rotation=90, va="center",
             ha="right", fontsize=8.5, color=col)
ax2.set_xlim(-0.75, 1.35)
ax2.set_ylim(TMAX, 0)
ax2.set_yticks([])
ax2.set_xticks([0, 0.5, 1.0])
ax2.set_xticklabels(["0", "900", "1800"])
ax2.set_xlabel("Offset (m)")
ax2.set_title("Reverberation train vs offset:\nperiod stretches at far offsets",
              fontsize=11)

# --- right: period in intercept time tau --------------------------------------
ax3 = fig.add_axes((0.72, 0.16, 0.25, 0.66))
p = np.linspace(0, 1 / VW * 0.999, 400)          # s/m
dt_tau = DT0 * np.sqrt(1 - (p * VW) ** 2)
ax3.plot(p * 1e3, dt_tau * 1e3, lw=2.4, color="seagreen")
ax3.axhline(DT0 * 1e3, color="0.6", ls=":")
ax3.text(0.62, DT0 * 1e3 + 1, "$\\Delta t_0$ (vertical)", fontsize=9, color="0.4")
ax3.set_xlabel("Ray parameter p (ms/m)")
ax3.set_ylabel("Intercept-time period $\\Delta\\tau(p)$ (ms)")
ax3.set_title("In tau-p the period is a known\nfunction of p — constant per trace",
              fontsize=11)
ax3.grid(alpha=0.3)
ax3.text(0.08, 100,
         "$\\Delta\\tau(p) = \\Delta t_0\\,\\sqrt{1 - p^2 v_w^2}$",
         fontsize=12, color="seagreen",
         bbox=dict(fc="white", ec="seagreen", alpha=0.9))

fig.suptitle("Why predictive deconvolution fails at offset — and why tau-p "
             "repairs it", fontsize=14)
fig.text(0.5, 0.02,
         "Same water layer, same physics, three coordinate systems. In x-t the "
         "period is offset-dependent (middle); in tau-p it collapses to one "
         "analytic curve (right),\nso ONE prediction gap per p-trace removes "
         "the whole reverberation family (demonstrated in the next figure).",
         ha="center", fontsize=10, color="0.25")
fig.savefig("figures/term02_lec04/term02_lec04_period_vs_offset.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec04_period_vs_offset.png")
