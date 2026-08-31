"""
Term 3 Lecture 05 — Figure 6: Seismic data and its spectrum before/after deghosting.

Pedagogical point
-----------------
The source and receiver ghosts are comb filters  G(f) = 1 - exp(-i 2 pi f tau)
that carve deep spectral NOTCHES at  f_n = n v_w/(2d).  In the time domain the
ghosts add delayed, polarity-reversed echoes that make the trace ringy.
Deghosting removes both effects: the notches are filled (the spectrum becomes
smooth and broadband) and the trace cleans up.

Model
-----
A broadband MINIMUM-PHASE source wavelet (Ormsby amplitude spectrum, corners
10/30/160/200 Hz, made causal via the cepstral minimum-phase reconstruction) is
convolved with a sparse reflectivity (a few clear events), then contaminated with
a SOURCE ghost (6 m depth -> notches at 125, 250, ... Hz) and a RECEIVER ghost
(12 m depth -> notches at 62.5, 125, 187.5, ... Hz).  In band this gives two
clear notches at 62.5 and 125 Hz.  "After deghosting" is the clean (ghost-free)
data.  A broadband wavelet is used so that BOTH notches sit inside the band and
their filling is clearly visible (a narrow-band pulse would have little energy at
125 Hz, so that notch could not be seen to fill).

Self-contained: numpy + matplotlib only.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

COL_BEFORE = "#0072B2"   # blue
COL_AFTER = "#D55E00"    # vermillion
NOTCH = [62.5, 125.0]    # in-band ghost notch frequencies (Hz)
CORNERS = (10, 30, 160, 200)   # Ormsby corners (Hz): flat band 30-160 Hz


def ormsby_amp(freq, f1, f2, f3, f4):
    """Trapezoidal (Ormsby) amplitude spectrum."""
    A = np.zeros_like(freq)
    A[(freq >= f2) & (freq <= f3)] = 1.0
    m = (freq >= f1) & (freq < f2)
    A[m] = (freq[m] - f1) / (f2 - f1)
    m = (freq > f3) & (freq <= f4)
    A[m] = (f4 - freq[m]) / (f4 - f3)
    return A


def minimum_phase(w, N):
    """Causal minimum-phase reconstruction (homomorphic/cepstral).

    Preserves |FFT(w)|; returns a length-N front-loaded sequence whose phase is
    the minimum phase  -Hilbert{ ln|W| }.
    """
    W = np.fft.fft(w, n=N)
    eps = np.max(np.abs(W)) * 1e-9
    c = np.fft.ifft(np.log(np.maximum(np.abs(W), eps))).real   # real cepstrum
    c_mp = np.zeros(N)
    c_mp[0] = c[0]
    c_mp[1:N // 2] = 2 * c[1:N // 2]
    c_mp[N // 2] = c[N // 2]
    return np.fft.ifft(np.exp(np.fft.fft(c_mp))).real


def ormsby_minphase(t, corners):
    """Broadband minimum-phase Ormsby wavelet (causal, front-loaded)."""
    N = len(t)
    freq = np.fft.rfftfreq(N, dt)
    A = ormsby_amp(freq, *corners)
    w_zp = np.fft.fftshift(np.fft.irfft(A, n=N))   # zero-phase version
    return minimum_phase(w_zp, N)[:N]


# ---------------------------------------------------------------------------
# Build the seismic trace (clean) and its ghosted version
# ---------------------------------------------------------------------------
dt = 0.001                       # 1 ms
t = np.arange(0, 0.6, dt)
N = len(t)

src = ormsby_minphase(t, CORNERS)          # broadband minimum-phase source pulse
src /= np.max(np.abs(src))

# sparse reflectivity -> a few clear reflection events
refl = np.zeros(N)
for tt, aa in [(0.07, 1.0), (0.16, -0.7), (0.26, 0.9), (0.37, -0.55), (0.48, 0.65)]:
    refl[int(tt / dt)] = aa

clean = np.convolve(refl, src, "full")[:N]      # ghost-free trace

# ghosts as comb filters in the frequency domain
v_w = 1500.0
tau_s = 2 * 6.0 / v_w            # source ghost delay (6 m)  -> 8 ms
tau_r = 2 * 12.0 / v_w           # receiver ghost delay (12 m) -> 16 ms
f = np.fft.rfftfreq(N, dt)
G = (1 - np.exp(-1j * 2 * np.pi * f * tau_s)) * \
    (1 - np.exp(-1j * 2 * np.pi * f * tau_r))
ghosted = np.fft.irfft(np.fft.rfft(clean) * G, n=N)

# spectra
spec_before = np.abs(np.fft.rfft(ghosted))
spec_after = np.abs(np.fft.rfft(clean))

# normalise each trace/spectrum to its own peak (focus on the shape change)
ghosted_n = ghosted / np.max(np.abs(ghosted))
clean_n = clean / np.max(np.abs(clean))
spec_before_n = spec_before / spec_before.max()
spec_after_n = spec_after / spec_after.max()

# ---------------------------------------------------------------------------
# Figure: 2x2  (rows = before/after ; cols = time/spectrum)
# ---------------------------------------------------------------------------
t_ms = t * 1000.0
fig, axes = plt.subplots(2, 2, figsize=(10, 6.2))
ax_bt, ax_bs = axes[0]           # before: time, spectrum
ax_ct, ax_cs = axes[1]           # after:  time, spectrum

fmax = 180.0
fmask = f <= fmax

# ---- (a) before, time domain ---------------------------------------------
ax_bt.plot(t_ms, ghosted_n, color=COL_BEFORE, lw=1.0)
ax_bt.axhline(0, color="grey", lw=0.5)
ax_bt.set_title("(a) Before deghosting — seismic trace", fontsize=10,
                loc="left", color=COL_BEFORE)
ax_bt.set_ylabel("Amplitude")

# ---- (c) after, time domain ----------------------------------------------
ax_ct.plot(t_ms, clean_n, color=COL_AFTER, lw=1.0)
ax_ct.axhline(0, color="grey", lw=0.5)
ax_ct.set_title("(c) After deghosting — seismic trace", fontsize=10,
                loc="left", color=COL_AFTER)
ax_ct.set_xlabel("Time (ms)")
ax_ct.set_ylabel("Amplitude")

for ax in (ax_bt, ax_ct):
    ax.set_xlim(0, 560)
    ax.set_ylim(-1.15, 1.15)

# ---- (b) before, spectrum (with notches) ---------------------------------
ax_bs.plot(f[fmask], spec_before_n[fmask], color=COL_BEFORE, lw=1.2)
for fn in NOTCH:
    ax_bs.axvline(fn, color="grey", ls="--", lw=0.8, alpha=0.7)
    ax_bs.annotate(f"{fn:g} Hz", (fn, 1.02), textcoords="offset points",
                   xytext=(0, 4), ha="center", fontsize=8, color="dimgrey")
ax_bs.set_title("(b) Before — amplitude spectrum (ghost notches)",
                fontsize=10, loc="left", color=COL_BEFORE)
ax_bs.set_ylabel("Amplitude spectrum")

# ---- (d) after, spectrum (smooth) ----------------------------------------
ax_cs.plot(f[fmask], spec_after_n[fmask], color=COL_AFTER, lw=1.2)
for fn in NOTCH:
    ax_cs.axvline(fn, color="grey", ls="--", lw=0.8, alpha=0.7)
ax_cs.set_title("(d) After — amplitude spectrum (notches filled)",
                fontsize=10, loc="left", color=COL_AFTER)
ax_cs.set_xlabel("Frequency (Hz)")
ax_cs.set_ylabel("Amplitude spectrum")

for ax in (ax_bs, ax_cs):
    ax.set_xlim(0, fmax)
    ax.set_ylim(0, 1.18)

fig.suptitle(
    "Deghosting fills the ghost notches and cleans the trace: source ghost "
    "(6 m) + receiver ghost (12 m) carve notches at 62.5 and 125 Hz",
    fontsize=11,
)
fig.tight_layout(rect=[0, 0, 1, 0.94])

# ---------------------------------------------------------------------------
# Save + diagnostics
# ---------------------------------------------------------------------------
out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       "..", "..", "..",
                                       "figures", "term03_lec05"))
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "term03_lec05_deghosting_data.png")
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"Saved figure to {out_path}")
for fn in NOTCH:
    i = np.argmin(np.abs(f - fn))
    print(f"notch {fn:g} Hz: before={spec_before_n[i]:.3f} after={spec_after_n[i]:.3f}")
pk = np.argmax(np.abs(src))
print(f"source wavelet peak at {t[pk]*1000:.1f} ms (causal, minimum phase)")
