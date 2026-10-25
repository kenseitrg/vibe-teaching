"""Figure: L2 vs L1 adaptive subtraction, and the filter-length trap.

Top row — the norm choice. The data contain a primary that interferes
with a multiple; the model predicts the multiple with small errors.
  L2 (least squares) minimizes total residual energy: where the primary
  overlaps the multiple, the filter compromises between fitting the
  multiple and annihilating the primary -> primary is damaged.
  L1 minimizes absolute residuals, treating the interference samples as
  outliers -> the primary survives. Solved as iteratively re-weighted
  least squares (same trick as the high-resolution Radon transform).

Bottom row — the filter-length trap (the raw deck's closing demo):
with a GOOD model, short and long filters both work (the filter has
nothing wrong to fix). With a BAD model (wrong kinematics), a SHORT
filter cannot fix it (residual multiples stay) — and a LONG filter
starts shaping the bad model into the DATA, eating primaries. Rule:
the filter should be long enough for the wavelet error, no longer.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_toeplitz

DT, TMAX = 0.004, 1.4
NT = int(TMAX / DT)
t = np.arange(NT) * DT
T_P, T_M = 0.60, 0.64               # overlapping primary and multiple


def ricker(f_dom, n, dt):
    tt = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * tt) ** 2) * np.exp(-(np.pi * f_dom * tt) ** 2)


def event(t0, f, amp):
    tr = np.zeros(NT)
    i0 = int(round(t0 / DT))
    w = ricker(f, 51, DT)
    tr[i0 - 25:i0 + 26] += amp * w
    return tr


prim = event(T_P, 30, 1.0)
mult = event(T_M, 26, 0.9)
data = prim + mult
# model nearly right (2 ms, amp, same frequency): the interesting case is
# NOT a bad model but the L2 norm exploiting a long filter at the overlap
model = event(T_M + 0.002, 26, 0.95)


def l2_filter(d, m, n=15, eps=0.02):
    rmm = np.correlate(m, m, "full")[len(m) - 1:]
    rdm = np.correlate(d, m, "full")[len(m) - 1:]
    rmm = np.concatenate([rmm, np.zeros(n)])[:n] * (1 + eps)
    rdm = np.concatenate([rdm, np.zeros(n)])[:n]
    return solve_toeplitz(rmm, rdm)


def l1_filter(d, m, n=15, niter=12, delta_frac=0.1):
    """IRLS for min sum |d - a*m|: at each iteration solve the weighted
    LS problem  sum r_i^2 / (|r_i^(k)| + delta)  — i.e. weights
    W_i = 1/(|residual| + delta) on the data equations."""
    a = l2_filter(d, m, n)
    for _ in range(niter):
        r = d - np.convolve(m, a)[:NT]
        delta = delta_frac * np.std(r) + 1e-12
        w = 1.0 / (np.abs(r) + delta)               # L1 IRLS weights
        mw = m * np.sqrt(w)
        dw = d * np.sqrt(w)
        rmm = np.correlate(mw, mw, "full")[len(m) - 1:]
        rdm = np.correlate(dw, mw, "full")[len(m) - 1:]
        rmm = np.concatenate([rmm, np.zeros(n)])[:n] * 1.02
        rdm = np.concatenate([rdm, np.zeros(n)])[:n]
        a = solve_toeplitz(rmm, rdm)
    return a


def subtract(d, m, a):
    return d - np.convolve(m, a)[:NT]


out_l2 = subtract(data, model, l2_filter(data, model, n=60))
out_l1 = subtract(data, model, l1_filter(data, model, n=60))
dmg = lambda out: np.linalg.norm(out - prim) / np.linalg.norm(prim)
print(f"L2 primary damage: {dmg(out_l2):.2f}   L1: {dmg(out_l1):.2f}")

# filter-length trap: bad model (kinematics wrong by 12 ms)
bad_model = event(T_M + 0.012, 24, 0.9)
outs = {}
for name, mdl in [("good model", model), ("bad model", bad_model)]:
    for n, lbl in [(5, "short filter (5)"), (80, "long filter (80)")]:
        a = l2_filter(data, mdl, n=n)
        outs[(name, lbl)] = subtract(data, mdl, a)

fig, axes = plt.subplots(2, 4, figsize=(16, 8), sharey=True)

ax = axes[0, 0]
ax.plot(data, t, "k", lw=1.0)
ax.plot(prim, t, "seagreen", lw=0.8, alpha=0.8, ls="--")
ax.set_title("data: primary (green dashed)\ninterfering with multiple")
ax.text(1.15, 0.66, "overlap\nzone", fontsize=9, color="crimson")

ax = axes[0, 1]
ax.plot(model, t, "crimson", lw=1.0)
ax.set_title("multiple model\n(small amp/phase errors)")

for ax, out, name, c in [(axes[0, 2], out_l2, "L2 subtraction", "royalblue"),
                         (axes[0, 3], out_l1, "L1 subtraction", "seagreen")]:
    ax.plot(out, t, c, lw=1.0)
    ax.plot(prim, t, "0.55", lw=0.8, ls="--")
    ax.set_title(f"{name}\nprimary damage: {dmg(out):.0%}",
                 color=c)

# bottom row: filter-length trap
order = [("good model", "short filter (5)"), ("good model", "long filter (80)"),
         ("bad model", "short filter (5)"), ("bad model", "long filter (80)")]
for ax, key in zip(axes[1], order):
    out = outs[key]
    mdl = model if key[0] == "good model" else bad_model
    res = np.linalg.norm(out - prim) / np.linalg.norm(prim)
    ax.plot(out, t, "royalblue", lw=1.0)
    ax.plot(prim, t, "0.55", lw=0.8, ls="--")
    resid_mult = np.linalg.norm(out - prim) / np.linalg.norm(mult)
    ax.set_title(f"{key[0]}, {key[1]}\nerror vs truth: {res:.0%}",
                 fontsize=10)
    if key[0] == "bad model" and "long" in key[1]:
        ax.annotate("long filter + bad model\n= shaping the model into\n"
                    "the data: primary eaten", xy=(0.35, T_P),
                    xytext=(-2.1, 0.95), fontsize=9, color="crimson",
                    arrowprops=dict(arrowstyle="->", color="crimson"))

for ax in axes.flat:
    ax.set_ylim(1.15, 0.25)
    ax.set_xlim(-2.4, 2.4)
    ax.set_xlabel("Amplitude")
axes[0, 0].set_ylabel("Time (s)")
axes[1, 0].set_ylabel("Time (s)")

fig.suptitle("Adaptive subtraction parameters II: the norm (L2 vs L1) and the "
             "filter length (the raw deck's closing demo)", fontsize=14)
fig.text(0.5, 0.012,
         "L2 assumes the output has minimum energy — exactly wrong where a "
         "primary interferes. L1 tolerates the interference samples as "
         "outliers. Filter length: long enough to fix wavelet errors, short\n"
         "enough that it cannot fit primaries with a bad model — with a good "
         "model even a long filter is safe (bottom left).",
         ha="center", fontsize=10, color="0.25")
fig.tight_layout(rect=(0, 0.045, 1, 0.93))
fig.savefig("figures/term02_lec04/term02_lec04_l1_vs_l2.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec04_l1_vs_l2.png")
