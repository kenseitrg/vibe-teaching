"""
Term 3 Lecture 05 — Figure 4: De-bubble (before vs. after), time and frequency.

Pedagogical point
-----------------
An airgun source signature is not a single pulse: the oscillating air bubble
re-radiates the primary pulse several times, each echo delayed by the bubble
period Tb and weaker by a decay factor r.  We model this cleanly:

    clean source (Berlage) :  p(t) = t^n exp(-alpha t) sin(2 pi f0 t),  t >= 0
    bubble pulse train      :  g(t) = sum_k r^k delta(t - k Tb)
    recorded signature      :  s(t) = (p * g)(t) = sum_k r^k p(t - k Tb)

De-bubble applies the inverse of g(t), removing the echoes and recovering the
clean Berlage pulse p(t).  In the two domains:

  * TIME domain      : the decaying bubble TAIL is removed -> compact wavelet.
  * FREQUENCY domain : the bubble is a comb filter |G(f)| with ripples spaced
                       by 1/Tb; de-bubble flattens the ripple -> smooth spectrum.

Self-contained: numpy + matplotlib only.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# Wong colorblind-safe palette.
COL_BEFORE = "#0072B2"   # blue
COL_AFTER = "#D55E00"    # vermillion

# Berlage parameters (positive-dominant, compact source pulse) and bubble model.
F0, ALPHA, N = 30.0, 100.0, 1
TB, DECAY, K = 0.055, 0.5, 5


def berlage(t, f0=F0, alpha=ALPHA, n=N):
    """Causal Berlage wavelet: t^n exp(-alpha t) sin(2 pi f0 t) for t>=0."""
    w = np.zeros_like(t)
    m = t >= 0
    w[m] = (t[m] ** n) * np.exp(-alpha * t[m]) * np.sin(2 * np.pi * f0 * t[m])
    return w


# ---------------------------------------------------------------------------
# Build the wavelets (BOTH on the same amplitude scale)
# ---------------------------------------------------------------------------
dt = 0.0005                 # 0.5 ms sampling
T = 1.0                     # 1 s grid (zero-padded for fine frequency resolution)
t = np.arange(0, T, dt)

primary = berlage(t)
norm_t = np.max(np.abs(primary))     # single normalisation shared by both traces

after = primary / norm_t             # clean de-bubbled source, unit peak

before = np.zeros_like(t)            # source signature WITH bubble tail
for k in range(K + 1):
    before += (DECAY ** k) * berlage(t - k * TB) / norm_t

primary_end = t[np.where(np.abs(after) > 0.01)[0][-1]]   # end of clean pulse

# ---------------------------------------------------------------------------
# Amplitude spectra (same scale: normalise by the clean spectrum peak)
# ---------------------------------------------------------------------------
freq = np.fft.rfftfreq(len(t), dt)
spec_after = np.abs(np.fft.rfft(after))
spec_before = np.abs(np.fft.rfft(before))
norm_f = spec_after.max()
spec_after /= norm_f
spec_before /= norm_f              # = clean x |G(f)| -> ripples around it

fmax = 125.0
fmask = freq <= fmax
spec_ymax = 1.12 * spec_before[fmask].max()

# A prominent ripple peak to annotate (largest before-peak between 25 and 45 Hz).
band = (freq >= 25) & (freq <= 45)
rip_idx = np.where(band)[0][np.argmax(spec_before[band])]

# Data-driven time-axis limits (nothing gets clipped).
ylo = min(before.min(), after.min())
yhi = max(before.max(), after.max())
ypad = 0.18 * max(abs(ylo), abs(yhi))
t_ylim = (ylo - ypad, yhi + ypad)

# ---------------------------------------------------------------------------
# Figure: 2x2 grid  (rows = before/after ; cols = time/frequency)
# ---------------------------------------------------------------------------
t_ms = t * 1000.0
fig, axes = plt.subplots(2, 2, figsize=(10, 6.2))
ax_bt, ax_bs = axes[0]      # before: time, spectrum
ax_at, ax_as = axes[1]      # after:  time, spectrum

# ---- (a) before, time domain ---------------------------------------------
ax_bt.plot(t_ms, before, color=COL_BEFORE, lw=1.4)
ax_bt.axvspan(primary_end * 1000, 300, color=COL_BEFORE, alpha=0.10)
ax_bt.axhline(0, color="grey", lw=0.5)
ax_bt.annotate("bubble tail\n(removed by de-bubble)",
               xy=(0.5 * (primary_end * 1000 + 300), t_ylim[1] * 0.86),
               ha="center", va="top", fontsize=8.5, color=COL_BEFORE)
ax_bt.set_title("(a) Before de-bubble — time domain", fontsize=10,
                loc="left", color=COL_BEFORE)

# ---- (c) after, time domain ----------------------------------------------
ax_at.plot(t_ms, after, color=COL_AFTER, lw=1.4)
ax_at.axhline(0, color="grey", lw=0.5)
ax_at.set_title("(c) After de-bubble — time domain", fontsize=10,
                loc="left", color=COL_AFTER)
ax_at.set_xlabel("Time (ms)")

for ax in (ax_bt, ax_at):          # shared time axes
    ax.set_xlim(-10, 300)
    ax.set_ylim(*t_ylim)
    ax.set_ylabel("Amplitude")

# ---- (b) before, amplitude spectrum --------------------------------------
ax_bs.plot(freq[fmask], spec_before[fmask], color=COL_BEFORE, lw=1.4)
ax_bs.annotate("bubble ripple", xy=(freq[rip_idx], spec_before[rip_idx]),
               xytext=(0.78 * fmax, 0.80 * spec_ymax), ha="center",
               fontsize=8.5, color=COL_BEFORE,
               arrowprops=dict(arrowstyle="-|>", color=COL_BEFORE, lw=1.0))
ax_bs.set_title("(b) Before de-bubble — amplitude spectrum", fontsize=10,
                loc="left", color=COL_BEFORE)

# ---- (d) after, amplitude spectrum ---------------------------------------
ax_as.plot(freq[fmask], spec_after[fmask], color=COL_AFTER, lw=1.4)
ax_as.set_title("(d) After de-bubble — amplitude spectrum", fontsize=10,
                loc="left", color=COL_AFTER)
ax_as.set_xlabel("Frequency (Hz)")

for ax in (ax_bs, ax_as):          # shared frequency axes
    ax.set_xlim(0, fmax)
    ax.set_ylim(0, spec_ymax)
    ax.set_ylabel("Amplitude spectrum")

fig.suptitle(
    "De-bubble: removing the airgun bubble compresses the wavelet (time) "
    "and flattens the spectral ripple (frequency)",
    fontsize=11.5,
)
fig.tight_layout(rect=[0, 0, 1, 0.94])

# ---------------------------------------------------------------------------
# Save + diagnostics
# ---------------------------------------------------------------------------
out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       "..", "..", "..",
                                       "figures", "term03_lec05"))
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "term03_lec05_debubble.png")
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"Saved figure to {out_path}")
print(f"time ylim: ({t_ylim[0]:.2f}, {t_ylim[1]:.2f})  "
      f"after range [{after.min():.2f},{after.max():.2f}]  "
      f"before range [{before.min():.2f},{before.max():.2f}]")
print(f"spectrum ylim: (0, {spec_ymax:.2f})  "
      f"ripple peak idx freq={freq[rip_idx]:.1f} Hz val={spec_before[rip_idx]:.2f}")
