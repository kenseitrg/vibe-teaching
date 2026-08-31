"""
Term 3 Lecture 05 — Figure 9: Receiver and Q effects on the wavelet spectrum.

Pedagogical point
-----------------
Two land-specific effects shape (and band-limit) the recorded wavelet spectrum:

  * Geophone (receiver) response.  A moving-coil geophone is a damped harmonic
    oscillator with natural frequency f0 (~10 Hz) and damping h (~0.7).  Its
    velocity response  |H(f)| = r^2 / sqrt((1-r^2)^2 + (2 h r)^2),  r = f/f0,
    is flat above f0 but rolls off at 12 dB/octave below f0 — so it SUPPRESSES
    the low frequencies that broadband processing tries to recover.

  * Absorption (Q).  The earth attenuates high frequencies:
    A(f,t) = exp(-pi f t / Q).  On a dB plot this is a straight negative slope
    that steepens with travel time t — progressive high-frequency loss.

The recorded wavelet spectrum is the source spectrum multiplied by both, so the
geophone carves off the low end and Q carves off the high end, leaving a
narrow, low-frequency-peaked band.

Panel (a) shows the two effects as transfer functions; panel (b) shows their
combined effect on a broadband source wavelet spectrum.

Self-contained: numpy + matplotlib only.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

COL_GEO = "#0072B2"    # geophone — blue
COL_Q = "#D55E00"      # Q absorption — vermillion
COL_REF = "#888888"    # reference source spectrum — grey
COL_REC = "black"      # recorded wavelet spectrum — black

# parameters
F0, H = 10.0, 0.7      # geophone natural frequency (Hz), damping
Q, T = 30.0, 1.0       # quality factor, two-way time (s)
DB_FLOOR = 1e-3        # amplitude floor -> -60 dB


def geophone(f, f0=F0, h=H):
    """Moving-coil geophone velocity response magnitude."""
    r = np.asarray(f) / f0
    return r ** 2 / np.sqrt((1 - r ** 2) ** 2 + (2 * h * r) ** 2)


def q_absorption(f, q=Q, t=T):
    """Earth absorption amplitude  exp(-pi f t / Q)."""
    return np.exp(-np.pi * np.asarray(f) * t / q)


def ormsby_amp(f, f1, f2, f3, f4):
    """Ormsby (trapezoidal) amplitude spectrum, peak = 1."""
    A = np.zeros_like(np.asarray(f, float))
    A[(f >= f2) & (f <= f3)] = 1.0
    m = (f >= f1) & (f < f2)
    A[m] = (f[m] - f1) / (f2 - f1)
    m = (f > f3) & (f <= f4)
    A[m] = (f4 - f[m]) / (f4 - f3)
    return A


def db(amp):
    return 20 * np.log10(np.maximum(amp, DB_FLOOR))


# frequency axis
f = np.linspace(0.1, 120.0, 4000)

geo = geophone(f)
qabs = q_absorption(f)
ref = ormsby_amp(f, 3, 8, 80, 110)      # broadband (de-bubbled) source spectrum
rec = ref * geo * qabs                  # recorded wavelet spectrum

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(10, 4.4))

# ---- (a) the two effects as transfer functions ---------------------------
ax_a.plot(f, db(geo), color=COL_GEO, lw=1.8, label="geophone response")
ax_a.plot(f, db(qabs), color=COL_Q, lw=1.8, label="Q absorption  ($t=1$ s, $Q=30$)")
ax_a.axvline(F0, color="grey", ls="--", lw=0.9)
ax_a.annotate("$f_0 = 10$ Hz", (F0, 4.5), textcoords="offset points",
              xytext=(4, 0), fontsize=8.5, color="dimgrey")
ax_a.annotate("12 dB/octave\nrolloff", xy=(4, db(geophone(np.array([4.0]))[0])),
              xytext=(20, -32), fontsize=8.5, color=COL_GEO, ha="center",
              arrowprops=dict(arrowstyle="-|>", color=COL_GEO, lw=1.0))
ax_a.annotate("progressive\nhigh-frequency loss", xy=(70, db(q_absorption(np.array([70.0]))[0])),
              xytext=(58, -22), fontsize=8.5, color=COL_Q, ha="center",
              arrowprops=dict(arrowstyle="-|>", color=COL_Q, lw=1.0))
ax_a.set_title("(a) Receiver and absorption effects", fontsize=10, loc="left")
ax_a.set_xlabel("Frequency (Hz)")
ax_a.set_ylabel("Amplitude (dB)")
ax_a.set_xlim(0, 120)
ax_a.set_ylim(-55, 6)
ax_a.legend(fontsize=8.5, loc="lower left")

# ---- (b) combined effect on the wavelet spectrum -------------------------
ax_b.plot(f, db(ref), color=COL_REF, lw=1.6, ls="--",
          label="source wavelet (broadband)")
ax_b.plot(f, db(rec), color=COL_REC, lw=1.9,
          label="recorded  ($\\times$ geophone $\\times$ Q)")
# shade the regions removed by each effect
ax_b.axvspan(0, F0, color=COL_GEO, alpha=0.08)
ax_b.axvspan(45, 120, color=COL_Q, alpha=0.08)
ax_b.annotate("geophone\nsuppresses low $f$", xy=(8, -6), xytext=(20, -22),
              fontsize=8.5, color=COL_GEO, ha="center",
              arrowprops=dict(arrowstyle="-|>", color=COL_GEO, lw=1.0))
ax_b.annotate("Q absorbs\nhigh $f$", xy=(60, db(rec[np.argmin(np.abs(f-60))])),
              xytext=(78, -22), fontsize=8.5, color=COL_Q, ha="center",
              arrowprops=dict(arrowstyle="-|>", color=COL_Q, lw=1.0))
ax_b.set_title("(b) Effect on the recorded wavelet spectrum", fontsize=10, loc="left")
ax_b.set_xlabel("Frequency (Hz)")
ax_b.set_ylabel("Amplitude (dB)")
ax_b.set_xlim(0, 120)
ax_b.set_ylim(-55, 6)
ax_b.legend(fontsize=8.5, loc="lower left")

fig.tight_layout()

# ---------------------------------------------------------------------------
# Save + diagnostics
# ---------------------------------------------------------------------------
out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       "..", "..", "..",
                                       "figures", "term03_lec05"))
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "term03_lec05_receiver_q_spectrum.png")
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"Saved figure to {out_path}")

ipk = np.argmax(rec)
print(f"recorded spectrum peak: {f[ipk]:.1f} Hz at {db(rec[ipk]):.1f} dB")
for ff in (5, 10, 20, 40, 60, 80):
    i = np.argmin(np.abs(f - ff))
    print(f"  f={ff:3d} Hz: ref={db(ref[i]):6.1f} dB  recorded={db(rec[i]):6.1f} dB")
