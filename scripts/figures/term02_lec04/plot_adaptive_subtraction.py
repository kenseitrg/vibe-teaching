"""Figure: Adaptive subtraction — the Wiener matching filter.

Left: the workflow diagram: in local space-time windows, estimate a
short filter a(t) that matches the multiple MODEL to the DATA (Wiener
normal equations: autocorrelation of the model x cross-correlation of
data and model), convolve, subtract.

Right: a worked 1D example. The data contain a primary overlapping a
multiple; the predicted model has the right kinematics but the wrong
amplitude (x1.4), a 6 ms delay and a slightly different wavelet.
Top: direct subtraction leaves a large residual. Bottom: the Wiener
matching filter (11 samples, one window) absorbs amplitude + phase +
wavelet error; subtraction removes the multiple and keeps the primary.

The same engine closes the loop of every model-driven noise method:
SRME, surface-wave removal (Term 3), modeled diffractions, 4D matching.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_toeplitz

DT, TMAX = 0.004, 1.6
NT = int(TMAX / DT)
T_PRIM, T_MULT = 0.62, 0.80          # arrival times (they overlap)


def ricker(f_dom, n, dt, delay=0.0):
    t = (np.arange(n) - (n - 1) / 2) * dt + delay
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


t = np.arange(NT) * DT

# "true" events
prim = np.zeros(NT)
i0 = int(round(T_PRIM / DT))
prim[i0 - 25:i0 + 26] += ricker(30, 51, DT)
mult = np.zeros(NT)
i0 = int(round(T_MULT / DT))
mult[i0 - 30:i0 + 31] += 0.8 * ricker(24, 61, DT)     # lower frequency
data = prim + mult

# imperfect model: amplitude x1.4, +6 ms delay, wavelet 22 Hz
model = np.zeros(NT)
i0 = int(round((T_MULT + 0.006) / DT))
model[i0 - 25:i0 + 26] += 0.8 * 1.4 * ricker(22, 51, DT)

# --- direct vs adaptive subtraction -------------------------------------------
direct = data - model

def match_filter(d, m, n=11, eps=0.05):
    """Wiener matching filter: min || d - a*m ||^2 (prewhitened)."""
    rmm = np.correlate(m, m, mode="full")[len(m) - 1:]
    rmm = np.concatenate([rmm, np.zeros(n)])[:n]
    rdm = np.correlate(d, m, mode="full")[len(m) - 1:]
    rdm = np.concatenate([rdm, np.zeros(n)])[:n]
    rmm = rmm * (1.0 + eps)
    return solve_toeplitz(rmm, rdm)


a = match_filter(data, model, n=11)
adapted = np.convolve(model, a)[:NT]
adaptive = data - adapted
res_direct = np.linalg.norm(direct - prim) / np.linalg.norm(prim)
res_adapt = np.linalg.norm(adaptive - prim) / np.linalg.norm(prim)
print(f"primary damage, direct subtraction: {res_direct:.2f}")
print(f"primary damage, adaptive subtraction: {res_adapt:.2f}")

fig = plt.figure(figsize=(15.5, 8))

# --- workflow diagram ----------------------------------------------------------
axd = fig.add_axes((0.03, 0.52, 0.30, 0.42))
axd.set_xlim(0, 10)
axd.set_ylim(0, 10)
axd.axis("off")


def box(x, y, w, h, text, fc="white", ec="0.3"):
    axd.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec=ec, lw=1.5))
    axd.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9)


def arrow(x1, y1, x2, y2):
    axd.annotate("", xy=(x2, y2), xytext=(x1, y1),
                 arrowprops=dict(arrowstyle="->", lw=1.4, color="0.3"))


box(0.3, 7.6, 3.0, 1.6, "DATA\n$d$ (primaries + multiples)")
box(6.7, 7.6, 3.0, 1.6, "multiple MODEL\n$m$ (SRME prediction)", fc="#ffe9e5",
    ec="crimson")
box(3.9, 5.4, 2.2, 1.4, "local windows\n(space, time)")
box(0.6, 3.2, 3.4, 1.4, "ACF(m), CCF(d,m)\nin window")
box(5.4, 3.2, 3.4, 1.4, "solve Wiener\n$R_{mm} a = r_{dm}$")
box(3.3, 1.2, 3.4, 1.4, "subtract\n$d - a * m$")
arrow(1.8, 7.6, 4.4, 6.8)
arrow(8.2, 7.6, 5.6, 6.8)
arrow(4.4, 5.4, 2.3, 4.6)
arrow(5.6, 5.4, 7.1, 4.6)
arrow(4.0, 3.2, 5.4, 3.9)
arrow(7.1, 3.2, 5.6, 3.9)
arrow(5.0, 1.2, 5.0, 0.3)
axd.text(5.0, 0.1, "OUTPUT: primaries", ha="center", fontsize=10,
         color="seagreen", fontweight="bold")
axd.set_title("adaptive subtraction workflow", fontsize=11)
axd.text(0.1, 9.7, "parameters: filter length, window sizes,\n"
         "prewhitening, L1/L2 choice", fontsize=9, color="0.35")

# --- traces ---------------------------------------------------------------------
gs = fig.add_gridspec(2, 2, left=0.40, right=0.98, top=0.92, bottom=0.08,
                      hspace=0.35, wspace=0.25)
panels = [
    (gs[0, 0], [(data, "k", "data $d$"), (model, "crimson", "model $m$ (wrong amp/phase)")],
     "inputs in the window"),
    (gs[0, 1], [(direct, "royalblue", f"direct $d-m$: damage {res_direct:.0%}"),
                (prim, "0.6", "true primary (reference)")],
     "direct subtraction fails"),
    (gs[1, 0], [(adapted, "crimson", "adapted model $a*m$"),
                (mult, "0.6", "true multiple (reference)")],
     "matched model vs true multiple"),
    (gs[1, 1], [(adaptive, "seagreen", f"adaptive $d-a*m$: damage {res_adapt:.0%}"),
                (prim, "0.6", "true primary (reference)")],
     "adaptive subtraction keeps the primary"),
]
for gs_slot, curves, title in panels:
    ax = fig.add_subplot(gs_slot)
    for tr, c, lbl in curves:
        ax.plot(tr, t, color=c, lw=1.1, label=lbl)
    ax.set_ylim(1.15, 0.30)
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylabel("Time (s)")
    ax.set_title(title, fontsize=10.5)
    ax.legend(fontsize=8, loc="lower right")
    ax.axhspan(0.52, 0.92, color="0.95")

fig.suptitle("Adaptive subtraction = Wiener matching filter in local windows "
             "(Term 1 Lec 06 equations, new job)", fontsize=14)
fig.savefig("figures/term02_lec04/term02_lec04_adaptive_subtraction.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec04_adaptive_subtraction.png")
