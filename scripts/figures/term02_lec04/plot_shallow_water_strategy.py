"""Figure: The shallow-water demultiple strategy — tools in combination.

In very shallow water (h ~ 50 m) the water-layer period (~67 ms) is
shorter than a wavelet: reverberations are short-period 'fog' (tau-p
predictive decon territory), while deeper surface multiples are
long-period events (SRME territory). No single tool cleans both.

Zero-offset trace walked through the staged workflow (after EET 06 /
the raw deck's Gulf of Suez example):
  stage 0 - input: seabed primary + deep primaries + water-layer
            reverberations (short-period) + one long-period surface
            multiple of the deep reflector;
  stage 1 - tau-p predictive decon (gap = water period): the
            reverberation fog collapses, primaries sharpen,
            long-period multiple untouched;
  stage 2 - SRME-style prediction (a * p * p) + adaptive subtraction:
            the long-period multiple goes.

Bottom: the production chain (EET 06): swell noise / bad traces ->
decon + deghosting -> FK (post-critical water-bottom events) ->
predictive decon (water layer) -> shot interpolation + near-offset
reconstruction -> SRME -> Radon demultiple (residuals).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_toeplitz

DT, TMAX = 0.004, 2.2
NT = int(TMAX / DT)
T = np.arange(NT) * DT
H, VW = 50.0, 1500.0
DT0 = 2 * H / VW                     # 66.7 ms water period
GAP = int(round(DT0 / DT))           # 17 samples


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


def place(tr, t0, amp, f=30):
    i0 = int(round(t0 / DT))
    w = ricker(f, 41, DT)
    lo, hi = max(0, i0 - 20), min(NT, i0 + 21)
    if hi > lo:
        tr[lo:hi] += amp * w[lo - (i0 - 20):hi - (i0 - 20)]
    return tr


# --- stage 0: the input ---------------------------------------------------------
seabed = np.zeros(NT); place(seabed, 0.0667, 0.9, 35)
deep = np.zeros(NT)
for t0, a in [(1.05, 1.0), (1.55, 0.7)]:
    place(deep, t0, a, 30)

reverb = np.zeros(NT)                 # short-period fog under every event
for base_t0, base_a in [(0.0667, 0.9), (1.05, 1.0), (1.55, 0.7)]:
    for n in range(1, 12):
        place(reverb, base_t0 + n * DT0, base_a * 0.62 ** n, 30)

long_mult = np.zeros(NT)              # long-period surface multiple
place(long_mult, 2.10, 0.45, 30)      # deep(1.05) + seabed-and-back path

data = seabed + deep + reverb + long_mult
truth = seabed + deep

# --- stage 1: tau-p predictive deconvolution (here: on the zero-offset trace) --
def pred_decon(trace, gap, n=60, eps=0.03):
    rxx = np.correlate(trace, trace, "full")[len(trace) - 1:]
    rxx = np.concatenate([rxx, np.zeros(gap + n + 1)])
    R = rxx[:n] * (1 + eps)
    rhs = rxx[gap:gap + n]
    h = solve_toeplitz(R, rhs)
    hd = np.zeros(gap + n)
    hd[gap:] = h
    return trace - np.convolve(trace, hd)[:NT]


after_decon = pred_decon(data, GAP)

# --- stage 2: SRME-style prediction + adaptive subtraction ---------------------
# EET 06 recipe: the water-bottom primary is muted before SRME (its multiples
# were already handled by predictive decon; leaving it in would make the
# self-convolution re-predict the water-bottom family and corrupt the
# subtraction).
pred_input = after_decon.copy()
pred_input[T < 0.18] = 0.0            # mute water-bottom primary + direct
wav = ricker(30, 41, DT)
W = np.fft.rfft(wav, n=NT)
A = -np.conj(W) / (np.abs(W) ** 2 + 1e-3 * np.abs(W).max() ** 2)
A *= np.clip(np.abs(W) / (0.1 * np.abs(W).max()), 0.0, 1.0)
Pf = np.fft.rfft(pred_input)
pred = np.fft.irfft(A * Pf * Pf, n=NT)
pred[T < 0.18] = 0.0


def match_subtract(d, m, n=15, eps=0.02, win=(1.85, 2.25)):
    """Wiener matching filter designed inside a time window."""
    msk = (T >= win[0]) & (T <= win[1])
    rmm = np.correlate(m * msk, m * msk, "full")[len(m) - 1:]
    rdm = np.correlate(d * msk, m * msk, "full")[len(m) - 1:]
    rmm = np.concatenate([rmm, np.zeros(n)])[:n] * (1 + eps)
    rdm = np.concatenate([rdm, np.zeros(n)])[:n]
    a = solve_toeplitz(rmm, rdm)
    adapted = np.convolve(m, a)[:NT]
    # apply the subtraction only inside (a tapered version of) the window —
    # the prediction outside it is not trustworthy (squared reverb residue)
    out = d.copy()
    tp = np.clip((T - (win[0] - 0.1)) / 0.1, 0, 1) * np.clip((win[1] + 0.1 - T) / 0.1, 0, 1)
    out -= adapted * tp
    return out


final = match_subtract(after_decon, pred, n=30)

rms = lambda a: float(np.sqrt(np.mean(a ** 2)))
err0 = rms(data - truth) / rms(truth)
err1 = rms(after_decon - truth) / rms(truth)
err2 = rms(final - truth) / rms(truth)
print(f"multiple content: input {err0:.0%} -> after tau-p decon {err1:.0%} "
      f"-> after SRME+adaptive {err2:.0%}")

# --- plot ------------------------------------------------------------------------
fig, axes = plt.subplots(1, 4, figsize=(15, 7.5), sharey=True)
stages = [
    (data, "stage 0: input\nshort-period fog +\nlong-period multiple", "k"),
    (after_decon, "stage 1: tau-p pred. decon\nfog collapsed;\nlong-period remains", "royalblue"),
    (pred / max(np.abs(pred).max(), 1e-12) * np.abs(data).max(),
     "stage 2a: SRME prediction\nof the long-period\nsurface multiple", "crimson"),
    (final, "stage 2b: adaptive\nsubtraction -> primaries", "seagreen"),
]
for ax, (tr, title, c) in zip(axes, stages):
    trn = tr / np.abs(data).max()
    ax.plot(trn, T, color=c, lw=0.9)
    ax.fill_betweenx(T, 0, trn, where=trn > 0, color=c, alpha=0.4)
    ax.set_title(title, fontsize=10.5)
    ax.set_xlabel("Amplitude")
    ax.set_xlim(-1.2, 1.2)
axes[0].set_ylabel("Time (s)")
axes[0].set_ylim(TMAX, 0)
axes[0].annotate("reverb fog", xy=(0.35, 0.35), xytext=(-1.1, 0.6), fontsize=9,
                 color="crimson", arrowprops=dict(arrowstyle="->", color="crimson"))
axes[0].annotate("long-period\nmultiple", xy=(0.28, 2.10), xytext=(-1.15, 1.72),
                 fontsize=9, color="crimson",
                 arrowprops=dict(arrowstyle="->", color="crimson"))
axes[3].text(0.05, 0.05, f"multiple content:\n{err0:.0%} -> {err1:.0%} -> {err2:.0%}",
             transform=axes[3].transAxes, fontsize=10, color="seagreen",
             bbox=dict(fc="white", ec="seagreen", alpha=0.85))

# production chain strip
chain = ["swell noise,\nbad traces", "wavelet decon\n+ deghosting",
         "FK: post-critical\nwater-bottom", "pred. decon\n(water layer)",
         "shot interp. +\nnear offsets", "SRME", "Radon\n(residuals)"]
for k, step in enumerate(chain):
    fig.text(0.045 + k * 0.132, 0.015, step, fontsize=8, ha="center",
             va="bottom", color="0.15",
             bbox=dict(boxstyle="round,pad=0.35", fc="#f2f2f2", ec="0.6"))
    if k < len(chain) - 1:
        fig.text(0.045 + k * 0.132 + 0.055, 0.032, r"$\rightarrow$", fontsize=11,
                 ha="center", va="center", color="0.4")

fig.suptitle("Shallow water: no single tool wins — the demultiple chain "
             "(after EET 06, Gulf of Suez example)", fontsize=14)
fig.tight_layout(rect=(0, 0.10, 1, 0.94))
fig.savefig("figures/term02_lec04/term02_lec04_shallow_water_strategy.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec04_shallow_water_strategy.png")
