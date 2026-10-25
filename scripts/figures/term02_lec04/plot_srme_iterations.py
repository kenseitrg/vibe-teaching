"""Figure: Iterative SRME — one multiple order per iteration.

The implicit relation p0 = p - a*p0*p can be solved by fixed-point
iteration:

    p0^(0) = p  (the data as first guess)
    p0^(i+1) = p - a * p0^(i) * p

Each iteration removes one more order of surface multiples. The figure
shows a 4-reflectivity model (including a moderately strong water
bottom): data p, estimates after iterations 1, 2, 3, 5, the true
multiple-free response, and the removed-multiples estimate
m^(i) = a * p0^(i-1) * p at iteration 3.

Convergence read-out: relative residual of primaries per iteration
(prints to stdout; annotated on the figure).
"""

import numpy as np
import matplotlib.pyplot as plt

DT, TMAX = 0.004, 2.6
REFL = [(0.35, 0.20), (0.95, 0.10), (1.55, 0.08), (2.05, 0.05)]


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


nt = int(TMAX / DT)
t = np.arange(nt) * DT
wav = ricker(26, 61, DT)
half = (len(wav) - 1) // 2

# zero-phase wavelet spectrum (periodic centring)
wav_zp = np.zeros(nt)
wav_zp[:half + 1] = wav[half:]
wav_zp[-half:] = wav[:half]
S = np.fft.rfft(wav_zp)
A = -np.conj(S) / (np.abs(S) ** 2 + 1e-3 * np.abs(S).max() ** 2)
# band-limit the operator: taper to zero where the wavelet has no energy
# (outside the usable band the deconvolution would amplify noise and the
# fixed-point iteration would diverge — standard practice in SRME)
A *= np.clip(np.abs(S) / (0.1 * np.abs(S).max()), 0.0, 1.0)


def place(spikes):
    out = np.zeros(nt)
    for i, a in enumerate(spikes):
        if a != 0.0:
            lo, hi = max(0, i - half), min(nt, i + half + 1)
            out[lo:hi] += a * wav[lo - (i - half):hi - (i - half)]
    return out


# spike-domain impulse responses
x0 = np.zeros(nt)
for t0, R in REFL:
    x0[int(round(t0 / DT))] += R

# data with all surface multiples: X = X0 / (1 + X0) in the frequency
# domain (spike domain, zero phase => real spectra)
X0 = np.fft.rfft(np.roll(x0, 0))  # spikes already 'centred' at their times
X = X0 / (1.0 + X0)
x = np.fft.irfft(X, n=nt)          # impulse response with multiples
p = place(x)                       # measured data (one wavelet per event)
p0_true = place(x0)

# iterative SRME in the frequency domain with the surface operator
P = np.fft.rfft(p)
p0_est = p.copy()
ests, mults = {}, {}
for it in range(1, 6):
    M = A * np.fft.rfft(p0_est) * P
    m_it = np.fft.irfft(M, n=nt)
    p0_est = p - m_it
    ests[it] = p0_est.copy()
    mults[it] = m_it

res = {0: np.linalg.norm(p - p0_true) / np.linalg.norm(p0_true)}
for it in range(1, 6):
    res[it] = np.linalg.norm(ests[it] - p0_true) / np.linalg.norm(p0_true)
print("relative residual per iteration:", {k: round(v, 3) for k, v in res.items()})

fig, axes = plt.subplots(2, 3, figsize=(15, 8.5), sharex=True, sharey=True)
show = [(0, 0, p, "data $p$ (all orders)", "k"),
        (0, 1, ests[1], "iteration 1\n(order-1 removed)", "royalblue"),
        (0, 2, ests[2], "iteration 2", "royalblue"),
        (1, 0, ests[5], "iteration 5", "royalblue"),
        (1, 1, p0_true, "true primaries $p_0$", "seagreen"),
        (1, 2, mults[3], "multiples estimate\n(iteration 3)", "crimson")]
for r, c, tr, title, color in show:
    ax = axes[r, c]
    trn = tr / np.abs(p0_true).max()
    ax.plot(trn, t, color=color, lw=0.9)
    ax.fill_betweenx(t, 0, trn, where=trn > 0, color=color, alpha=0.4)
    ax.set_title(title, fontsize=11)
    ax.set_ylim(TMAX, 0)
    ax.set_xlim(-1.1, 1.3)
    for t0, _ in REFL:
        ax.axhline(t0, color="0.88", lw=0.7)
    if c == 0:
        ax.set_ylabel("Two-way time (s)")
    if r == 1:
        ax.set_xlabel("Amplitude")

axes[0, 0].text(0.55, 1.35, "multiples:\n0.70, 1.30, 1.65,\n1.90, ...",
                fontsize=8.5, color="crimson")
axes[0, 0].annotate("water bottom\nmultiple", xy=(0.62, 0.70), xytext=(0.7, 0.35),
                    fontsize=8.5, color="crimson",
                    arrowprops=dict(arrowstyle="->", color="crimson"))

err_txt = "residual: " + " $\\to$ ".join(f"{res[i]:.0%}" for i in [0, 1, 2, 5])
axes[1, 1].text(0.05, 0.62, err_txt, fontsize=10, color="royalblue",
                transform=axes[1, 1].transAxes,
                bbox=dict(fc="white", ec="royalblue", alpha=0.85))

fig.suptitle("Iterative SRME: $p_0^{(i+1)} = p - a * p_0^{(i)} * p$ — "
             "each pass strips one more order of surface multiples", fontsize=14)
fig.text(0.5, 0.015,
         "Fully data-driven: no velocity model, no NMO, no moveout "
         "discrimination. The only external ingredient is the source "
         "signature, absorbed in the surface operator a(t) (previous figure) —\n"
         "and whatever a(t) gets wrong is handled by adaptive subtraction "
         "(final figure of the lecture).",
         ha="center", fontsize=10, color="0.25")
fig.tight_layout(rect=(0, 0.045, 1, 0.93))
fig.savefig("figures/term02_lec04/term02_lec04_srme_iterations.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec04_srme_iterations.png")
