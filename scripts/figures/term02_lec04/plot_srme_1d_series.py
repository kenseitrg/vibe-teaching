"""Figure: 1D SRME — the multiple series from the feedback loop.

For a horizontal-layered medium at zero offset, a surface multiple is
built from primaries: travel times ADD and amplitudes MULTIPLY. The
measured data x(t) and the multiple-free response x0(t) obey the
feedback relation

    x(t) = x0(t) - x0(t) * x(t)

which rearranges to the removal series

    x0(t) = x(t) + x(t)*x(t) + x(t)*x(t)*x(t) + ...

The series operates on the impulse response (spikes): amplitudes of the
series terms are products of reflection coefficients and stay bounded.
For display, each panel is convolved with one wavelet — the wavelet
bookkeeping of real data (each convolution adds a wavelet) is the
subject of the NEXT figure.

Panel 1: the model's primary response x0 (three reflectors).
Panel 2: the measured data x = x0 - x0*x0 + x0*x0*x0 (feedback loop).
Panel 3: first removal term x*x — exactly the multiples of order >= 1,
         expressed through the data themselves.
Panel 4: convergence: partial sums of the series vs the true x0.
"""

import numpy as np
import matplotlib.pyplot as plt

DT, TMAX = 0.004, 2.5
REFL = [(0.40, 0.35), (1.05, 0.20), (1.80, 0.15)]   # (t0 [s], R)


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


NLONG = 2 * int(TMAX / DT)          # zero-padded length: no circular wraparound


def conv(a, b):
    """Linear convolution, truncated to NLONG samples (multiples that
    bounce beyond the record length simply leave the window)."""
    return np.convolve(a, b)[:NLONG]


nt = int(TMAX / DT)
t = np.arange(nt) * DT
wav = ricker(28, 45, DT)

x0 = np.zeros(NLONG)
for t0, R in REFL:
    x0[int(round(t0 / DT))] += R

# feedback construction of the data (spike domain)
m1 = -conv(x0, x0)
m2 = +conv(conv(x0, x0), x0)
m3 = -conv(conv(conv(x0, x0), x0), x0)
x = x0 + m1 + m2 + m3

# removal series applied to the DATA (spike domain)
t1 = conv(x, x)
t2 = conv(t1, x)
sum1 = x + t1
sum2 = x + t1 + t2

def show(spikes):
    tr = conv(spikes[:NLONG], wav)[:nt]   # convolve for display; truncate
    return tr / 0.35

err0 = np.linalg.norm(x[:nt] - x0[:nt]) / np.linalg.norm(x0[:nt])
err1 = np.linalg.norm(sum1[:nt] - x0[:nt]) / np.linalg.norm(x0[:nt])
err2 = np.linalg.norm(sum2[:nt] - x0[:nt]) / np.linalg.norm(x0[:nt])
print(f"relative multiple energy in data: {err0:.2f}")
print(f"after 1 series term: {err1:.3f}; after 2: {err2:.4f}")

fig, axes = plt.subplots(1, 4, figsize=(15.5, 7), sharey=True)
panels = [
    (axes[0], show(x0), "1. Multiple-free response $x_0$\n('the truth')", "seagreen"),
    (axes[1], show(x), "2. Measured data $x$\n($x_0$ + surface multiples)", "k"),
    (axes[2], show(t1), "3. First removal term\n$x * x$  (order-1+ multiples)", "crimson"),
    (axes[3], show(sum2 - x0), "4. Residual after two terms\n$(x + x{*}x + x{*}x{*}x) - x_0$", "royalblue"),
]
for ax, tr, title, color in panels:
    tr = tr / np.abs(tr).max() * 0.9
    ax.plot(tr, t, color=color, lw=1.0)
    ax.fill_betweenx(t, 0, tr, where=tr > 0, color=color, alpha=0.45)
    ax.set_title(title, fontsize=11)
    ax.set_xlabel("Amplitude")
    for t0, _ in REFL:
        ax.axhline(t0, color="0.87", lw=0.7)
    ax.axhline(0.80, color="crimson", lw=0.5, ls=":")
    ax.axhline(1.45, color="crimson", lw=0.5, ls=":")
    ax.set_xlim(-0.8, 1.0)

axes[0].set_ylabel("Two-way time (s)")
axes[0].set_ylim(TMAX, 0)
axes[1].text(0.30, 0.86, "order-1\nmultiple", fontsize=8.5, color="crimson")
axes[1].text(0.42, 1.50, "order-2", fontsize=8.5, color="crimson")
axes[3].text(0.28, 1.0, f"relative residual\n{err0:.0%} $\\to$ {err1:.0%} "
             f"$\\to$ {err2:.0%}", fontsize=9, color="royalblue",
             bbox=dict(fc="white", ec="royalblue", alpha=0.85))

# feedback diagram inset on panel 2
axi = axes[1].inset_axes([0.50, 0.60, 0.48, 0.30])
axi.set_xlim(0, 10)
axi.set_ylim(0, 6)
axi.axis("off")
axi.annotate("", xy=(3.2, 4.4), xytext=(1.0, 4.4),
             arrowprops=dict(arrowstyle="->", lw=1.4))
axi.text(2.1, 4.9, "$x_0$", fontsize=10, ha="center")
axi.add_patch(plt.Circle((4.6, 4.4), 0.8, fc="white", ec="crimson"))
axi.text(4.6, 4.4, "$r_0{=}{-}1$", fontsize=7, ha="center", va="center",
         color="crimson")
axi.annotate("", xy=(8.0, 4.4), xytext=(5.5, 4.4),
             arrowprops=dict(arrowstyle="->", lw=1.4))
axi.text(8.4, 4.4, "$+$", fontsize=11, ha="center", va="center")
axi.text(8.9, 5.1, "$x$", fontsize=10)
axi.annotate("", xy=(4.6, 1.3), xytext=(4.6, 3.5),
             arrowprops=dict(arrowstyle="->", lw=1.4, color="crimson"))
axi.text(5.0, 2.2, "each loop =\none more order", fontsize=7.5, color="crimson")
axi.set_title("feedback loop", fontsize=9)

fig.suptitle("1D SRME series: multiple removal by self-convolution of the "
             "input data", fontsize=14)
fig.text(0.5, 0.015,
         "The removal identity $x_0 = x + x{*}x + x{*}x{*}x + \\dots$ uses "
         "ONLY the measured data — no velocity model, no moveout. Each term "
         "adds one more order of multiples to the prediction (terms shown\n"
         "after convolution with one wavelet for display; the series itself "
         "operates on the impulse response — the wavelet problem is the next "
         "figure).",
         ha="center", fontsize=10, color="0.25")
fig.tight_layout(rect=(0, 0.05, 1, 0.93))
fig.savefig("figures/term02_lec04/term02_lec04_srme_1d_series.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec04_srme_1d_series.png")
