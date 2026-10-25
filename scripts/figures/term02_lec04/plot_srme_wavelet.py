"""Figure: What the SRME convolutions do to the wavelet.

With a real source signature s(t), the measured data are
p = x0 * s (one wavelet per event). The naive prediction -p*p carries
TWO wavelets (s*s): it is longer in time and narrower in band than the
true multiple. Formally each convolution step must be pre-scaled by the
SURFACE OPERATOR a(t) = -[s(t)]^-1 (an inverse-source filter):

    p0 = p - a*p*p + a*a*p*p*p - ...

Top: the wavelet s, its self-convolution s*s (what the naive prediction
carries), and the Wiener inverse s^-1 (spiking filter with prewhitening).
Middle: true multiple vs naive prediction vs corrected prediction, as
traces: the naive one is smeared (wrong wavelet), the corrected one
matches event-by-event.
Bottom: amplitude spectra of the same three — the naive prediction has
lost the high frequencies (spectrum squared); the corrected prediction
restores them.

This figure is the reason SRME output is always subtracted by an
ADAPTIVE filter rather than directly (next section of the lecture).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_toeplitz

DT, TMAX = 0.004, 2.0
REFL = [(0.40, 0.35), (1.05, 0.20)]     # (t0 [s], R)

def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


def wiener_inverse(wav, n=80, eps=0.02):
    """Filter approximating 1/w(t) for a symmetric wavelet (prewhitened).

    Desired output: a spike aligned with the wavelet centre, so the
    cross-correlation term of the Wiener equations is the wavelet itself.
    """
    r = np.correlate(wav, wav, mode="full")[len(wav) - 1:]
    r = np.concatenate([r, np.zeros(max(0, n - len(r)))])[:n]
    rhs = np.zeros(n)
    rhs[:len(wav)] = wav                 # phi_dx for a symmetric wavelet
    a = solve_toeplitz(r, rhs)
    return a / (1 + eps)


nt = int(TMAX / DT)
t = np.arange(nt) * DT
wav = ricker(26, 61, DT)
inv_w = wiener_inverse(wav, n=80, eps=0.02)

# spike-domain model
def place(spikes, wav):
    """Convolve spikes with a wavelet keeping event times (wavelet centred
    on each spike) — avoids the half-wavelet shift of np.convolve."""
    half = (len(wav) - 1) // 2
    out = np.zeros(len(spikes) + len(wav))
    for i, a in enumerate(spikes):
        if a != 0.0:
            out[i:i + len(wav)] += a * wav
    return out[half:half + len(spikes)]


x0 = np.zeros(nt)
for t0, R in REFL:
    x0[int(round(t0 / DT))] += R

p0 = place(x0, wav)                                 # multiple-free data
x2 = np.convolve(x0, x0)[:nt]                       # spike square: times add,
m_true = -place(x2, wav)                            # amplitudes multiply
p = p0 + m_true                                     # data + order-1 multiple
scale_true = np.abs(m_true).max()

naive = -np.convolve(p, p)[:nt]                       # -p*p (two wavelets)
# surface operator in the frequency domain: a = -[s]^-1, stabilized.
# Use a periodically centred (zero-phase) copy of the wavelet so the
# operator introduces no time shift.
wav_zp = np.zeros(nt)
half = (len(wav) - 1) // 2
wav_zp[:half + 1] = wav[half:]        # right half from t=0
wav_zp[-half:] = wav[:half]           # left half wrapped to negative times
S = np.fft.rfft(wav_zp, n=nt)
A = -np.conj(S) / (np.abs(S) ** 2 + 0.001 * np.abs(S).max() ** 2)
P = np.fft.rfft(p)
corrected = np.fft.irfft(P * P * A, n=nt)             # a*p*p


def scale_match_residual(true, pred, win=(0.70, 0.92)):
    """Residual after best scalar scaling, in a window around the 0.8 s
    first-order multiple (isolates the wavelet-shape comparison from the
    higher-order cross terms that p*p also legitimately predicts)."""
    m = (t >= win[0]) & (t <= win[1])
    alpha = np.dot(true[m], pred[m]) / np.dot(pred[m], pred[m])
    return np.linalg.norm(true[m] - alpha * pred[m]) / np.linalg.norm(true[m]), alpha


res_naive, _ = scale_match_residual(m_true, naive)
res_corr, _ = scale_match_residual(m_true, corrected)
print(f"wavelet-shape mismatch, naive prediction:   {res_naive:.2f}")
print(f"wavelet-shape mismatch, corrected operator: {res_corr:.2f}")

# normalize for display only
naive /= np.abs(naive).max() / scale_true
corrected /= np.abs(corrected).max() / scale_true

fig = plt.figure(figsize=(13.5, 9))
gs = fig.add_gridspec(3, 3, hspace=0.5, wspace=0.32)

# top row: wavelet bookkeeping
ax = fig.add_subplot(gs[0, 0])
ax.plot(np.arange(len(wav)) * DT * 1e3 - (len(wav) - 1) / 2 * DT * 1e3, wav, "k")
ax.set_title("Source wavelet $s$\n(carried by the data)")
ax.set_xlabel("Time (ms)")

ax = fig.add_subplot(gs[0, 1])
ww = np.convolve(wav, wav)
ax.plot(np.arange(len(ww)) * DT * 1e3 - (len(ww) - 1) / 2 * DT * 1e3, ww, "crimson")
ax.set_title("$s * s$ — what $p{*}p$ carries\n(two wavelets: smeared)")
ax.set_xlabel("Time (ms)")

ax = fig.add_subplot(gs[0, 2])
ax.plot(np.arange(len(inv_w)) * DT * 1e3, inv_w, "seagreen")
ax.set_title("Surface operator $a \\approx -[s]^{-1}$\n(Wiener inverse + prewhitening)")
ax.set_xlabel("Time (ms)")

# middle row: predictions vs truth
lim = (0.55, 1.95)
mask = (t >= lim[0]) & (t <= lim[1])
for k, (tr, lbl, c) in enumerate([
        (m_true, "true multiple $-x_0{*}x_0{*}s$", "k"),
        (naive, "naive prediction $-p{*}p$", "crimson"),
        (corrected, "corrected $a{*}p{*}p$", "seagreen")]):
    ax = fig.add_subplot(gs[1, k])
    ax.plot(tr[mask], t[mask], color=c, lw=1.1)
    ax.fill_betweenx(t[mask], 0, tr[mask], where=tr[mask] > 0, color=c, alpha=0.4)
    ax.set_title(lbl, fontsize=10.5)
    ax.set_ylim(lim[1], lim[0])
    ax.set_xlim(-1.2 * scale_true, 1.2 * scale_true)
    if k == 0:
        ax.set_ylabel("Time (s)")

# bottom row: spectra
freqs = np.fft.rfftfreq(nt, DT)
for k, (tr, lbl, c) in enumerate([
        (m_true, "true multiple", "k"),
        (naive, "naive: $|S|^2$ — band lost", "crimson"),
        (corrected, "corrected: $|S|$ restored", "seagreen")]):
    ax = fig.add_subplot(gs[2, k])
    spec = np.abs(np.fft.rfft(tr))
    ax.plot(freqs, spec / spec.max(), color=c, lw=1.4)
    ax.set_xlim(0, 80)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_title(f"spectrum: {lbl}", fontsize=10.5)

fig.suptitle("Each SRME convolution multiplies the spectrum by S(f): without the "
             "surface operator the prediction carries the wrong wavelet",
             fontsize=13.5)
fig.text(0.5, 0.015,
         "In practice s(t) is imperfectly known and the operator cannot fix "
         "directivity/3D effects either — so the last step of SRME is never a "
         "direct subtraction,\nbut an ADAPTIVE subtraction that estimates the "
         "matching filter from the data (final section of the lecture).",
         ha="center", fontsize=10, color="0.25")
fig.savefig("figures/term02_lec04/term02_lec04_srme_wavelet.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec04_srme_wavelet.png")
