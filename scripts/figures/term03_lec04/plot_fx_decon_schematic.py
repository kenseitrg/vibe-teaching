"""
FX-deconvolution principle (schematic).

Three-panel figure:
  (a) Six traces with a linear dipping event (same wavelet, shifted in
      time by dt = dx / v_app per trace) plus random noise.
  (b) Signal in the complex plane at a fixed frequency f: the complex
      amplitudes X_n = W * exp(-j n dphi) rotate by a CONSTANT phase
      increment from trace to trace -- a complex exponential, which a
      prediction filter can capture (dashed: predicted next value).
  (c) Random noise in the complex plane: no phase pattern, hence
      unpredictable -- it goes to the residual.

Trace colours in (a) match point colours in (b) so students can follow
"trace n -> point X_n".
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

# ════════════════════════════════════════════════════════════════════
# Figure settings
# ════════════════════════════════════════════════════════════════════
FIG_WIDTH = 13.0
FIG_HEIGHT = 5.0
DPI = 150
OUTPUT_PATH = "figures/term03_lec04/term03_lec04_fx_decon_schematic.png"

COL_SIGNAL = "#0072B2"   # blue
COL_NOISE  = "#777777"   # grey
COL_PRED   = "#D55E00"   # vermillion (prediction)
COL_ACCENT = "#CC79A7"   # rose (phase arc)

# ════════════════════════════════════════════════════════════════════
# Data parameters
# ════════════════════════════════════════════════════════════════════
N_TRACES = 6
DX = 50.0              # trace spacing (m)
V_APP = 1500.0         # apparent velocity of the dipping event (m/s)
DT_SHIFT = DX / V_APP  # time shift per trace (s) = 33.3 ms

DT = 0.002             # sample interval (s)
T_MAX = 0.5            # trace length (s)
T0 = 0.15              # event time on first trace (s)
F0 = 25.0              # Ricker peak frequency (Hz)
NOISE_AMP = 0.15
SEED = 7

# Phase increment per trace at the display frequency (schematic value;
# in reality dphi = 2 pi f dx / v_app)
DPHI = np.deg2rad(40.0)

# Trace colours: graded blues (light -> dark) so trace n matches point n
def blue_shade(i, n):
    base = np.array([0.0, 0.45, 0.70])        # Okabe-Ito blue
    white = np.array([1.0, 1.0, 1.0])
    frac = 0.55 * (1.0 - i / max(n - 1, 1))   # first trace lightest
    return tuple(base * (1 - frac) + white * frac)

TRACE_COLORS = [blue_shade(i, N_TRACES) for i in range(N_TRACES)]


# ════════════════════════════════════════════════════════════════════
# Helper
# ════════════════════════════════════════════════════════════════════

def ricker(f0, dt, duration=0.16):
    t = np.arange(-duration / 2, duration / 2 + dt, dt)
    tau = np.pi * f0 * t
    return t, (1.0 - 2.0 * tau ** 2) * np.exp(-tau ** 2)


def make_traces():
    """Return (time, traces) — list of 1-D arrays, one per trace."""
    rng = np.random.RandomState(SEED)
    time = np.arange(0, T_MAX + DT, DT)
    t_w, wlet = ricker(F0, DT)
    traces = []
    for n in range(N_TRACES):
        tr = NOISE_AMP * rng.randn(len(time))
        t_peak = T0 + n * DT_SHIFT
        idx = int(round(t_peak / DT))
        half = len(wlet) // 2
        lo, hi = idx - half, idx + half + 1
        if 0 <= lo and hi <= len(time):
            tr[lo:hi] += wlet
        traces.append(tr)
    return time, traces


# ════════════════════════════════════════════════════════════════════
# Build data
# ════════════════════════════════════════════════════════════════════
time, traces = make_traces()

# Complex amplitudes: signal points on the unit circle
angles = -np.arange(N_TRACES) * DPHI          # rotate clockwise (e^{-jn dphi})
X_sig = np.exp(1j * angles)

# Noise points: random phase and amplitude
rng = np.random.RandomState(SEED + 1)
X_noise = rng.uniform(0.2, 0.9, N_TRACES) * \
          np.exp(1j * rng.uniform(0, 2 * np.pi, N_TRACES))


# ════════════════════════════════════════════════════════════════════
# Plotting
# ════════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
gs = fig.add_gridspec(1, 3, width_ratios=[1.15, 1.0, 1.0], wspace=0.30)

# ── Panel (a): wiggle traces ────────────────────────────────────────
axa = fig.add_subplot(gs[0])
WIG_SCALE = 0.32                            # deflection in trace units

for n, tr in enumerate(traces):
    axa.plot(n + WIG_SCALE * tr, time, color=TRACE_COLORS[n], lw=1.2)
    axa.fill_betweenx(time, n, n + WIG_SCALE * tr,
                      where=(WIG_SCALE * tr > 0),
                      color=TRACE_COLORS[n], alpha=0.55, lw=0)
    # mark the wavelet peak
    t_peak = T0 + n * DT_SHIFT
    axa.plot(n, t_peak, "o", ms=4, color=TRACE_COLORS[n], zorder=5)

# dashed line through the peaks = linear moveout
peak_t = T0 + np.arange(N_TRACES) * DT_SHIFT
axa.plot(np.arange(N_TRACES), peak_t, "--", color="k", lw=1.0, alpha=0.6)

axa.annotate(
    "same wavelet,\nshifted in time\n(linear moveout)",
    xy=(2.0, T0 + 2 * DT_SHIFT), xytext=(3.1, 0.08),
    fontsize=8, ha="left", va="center",
    arrowprops=dict(arrowstyle="->", color="k", lw=0.9),
)

axa.set_ylim(T_MAX, 0)                       # time increases downward
axa.set_xlim(-0.6, N_TRACES - 0.4)
axa.set_xticks(range(N_TRACES))
axa.set_xticklabels([f"{n}" for n in range(N_TRACES)], fontsize=9)
axa.set_xlabel("trace index n", fontsize=10)
axa.set_ylabel("time (s)", fontsize=10)
axa.set_title("(a) t–x domain: dipping event + noise", fontsize=10, pad=8)

# ── Panel (b): signal in the complex plane ──────────────────────────
axb = fig.add_subplot(gs[1], aspect="equal")

# unit circle
th = np.linspace(0, 2 * np.pi, 300)
axb.plot(np.cos(th), np.sin(th), color="#cccccc", lw=1.0)
axb.axhline(0, color="k", lw=0.4, alpha=0.5)
axb.axvline(0, color="k", lw=0.4, alpha=0.5)

# arrows + points for traces 0..4 (known)
for n in range(N_TRACES - 1):
    z = X_sig[n]
    axb.annotate("", xy=(z.real, z.imag), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="->", color=TRACE_COLORS[n],
                                 lw=1.6))
    axb.plot(z.real, z.imag, "o", ms=7, color=TRACE_COLORS[n], zorder=5)
    axb.annotate(f"$X_{n}$", xy=(z.real, z.imag),
                 xytext=(1.18 * z.real, 1.18 * z.imag),
                 fontsize=9, ha="center", va="center",
                 color=TRACE_COLORS[n])

# predicted next point X_5 (dashed)
z5 = X_sig[N_TRACES - 1]
axb.annotate("", xy=(z5.real, z5.imag), xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color=COL_PRED, lw=1.6,
                             linestyle="--"))
axb.plot(z5.real, z5.imag, "o", ms=8, mfc="none", mec=COL_PRED,
         mew=1.8, zorder=5)
axb.annotate("predicted $X_5$", xy=(z5.real, z5.imag),
             xytext=(z5.real - 0.15, z5.imag - 0.28),
             fontsize=8.5, color=COL_PRED, ha="center", va="top")

# phase-increment arc between X_0 and X_1
a0 = np.rad2deg(np.angle(X_sig[0]))
a1 = np.rad2deg(np.angle(X_sig[1]))
axb.add_patch(Arc((0, 0), 0.9, 0.9, angle=0,
                  theta1=min(a0, a1), theta2=max(a0, a1),
                  color=COL_ACCENT, lw=1.8))
mid = np.deg2rad((a0 + a1) / 2)
axb.annotate(r"$\Delta\phi$", xy=(0.45 * np.cos(mid), 0.45 * np.sin(mid)),
             xytext=(0.72, 0.35), fontsize=11, color=COL_ACCENT,
             ha="center", va="center",
             arrowprops=dict(arrowstyle="->", color=COL_ACCENT, lw=1.0))

axb.text(0, -1.75, "constant phase step per trace\n"
                   r"$\Delta\phi = 2\pi f \Delta x / v_{app}$"
                   "  →  predictable",
         fontsize=8.5, ha="center", va="top", color=COL_SIGNAL)

axb.set_xlim(-1.45, 1.45)
axb.set_ylim(-1.55, 1.55)
axb.set_xticks([])
axb.set_yticks([])
axb.text(1.50, -0.08, "Re", fontsize=10, ha="left", va="center")
axb.text(0.08, 1.58, "Im", fontsize=10, ha="center", va="bottom")
axb.set_title("(b) signal at fixed f: complex exponential", fontsize=10,
              pad=8)

# ── Panel (c): noise in the complex plane ───────────────────────────
axc = fig.add_subplot(gs[2], aspect="equal")

axc.plot(np.cos(th), np.sin(th), color="#cccccc", lw=1.0)
axc.axhline(0, color="k", lw=0.4, alpha=0.5)
axc.axvline(0, color="k", lw=0.4, alpha=0.5)

for n in range(N_TRACES):
    z = X_noise[n]
    axc.annotate("", xy=(z.real, z.imag), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="->", color=COL_NOISE,
                                 lw=1.2, alpha=0.7))
    axc.plot(z.real, z.imag, "o", ms=6, color=COL_NOISE, zorder=5)

axc.text(0, -1.75, "no phase pattern  →  unpredictable\n"
                   "→  goes to the residual",
         fontsize=8.5, ha="center", va="top", color=COL_NOISE)

axc.set_xlim(-1.45, 1.45)
axc.set_ylim(-1.55, 1.55)
axc.set_xticks([])
axc.set_yticks([])
axc.text(1.50, -0.08, "Re", fontsize=10, ha="left", va="center")
axc.text(0.08, 1.58, "Im", fontsize=10, ha="center", va="bottom")
axc.set_title("(c) noise at fixed f: random phases", fontsize=10, pad=8)

fig.suptitle("FX-deconvolution principle", fontsize=13,
             fontweight="bold", y=1.02)

plt.savefig(OUTPUT_PATH, dpi=DPI, bbox_inches="tight")
plt.close()

print(f"Saved figure to {OUTPUT_PATH}")
print(f"Traces: {N_TRACES}, dx = {DX:.0f} m, v_app = {V_APP:.0f} m/s, "
      f"shift/trace = {DT_SHIFT*1000:.1f} ms")
print(f"Ricker f0 = {F0:.0f} Hz, noise amp = {NOISE_AMP}")
print(f"Phase increment dphi = {np.rad2deg(DPHI):.0f} deg per trace")
