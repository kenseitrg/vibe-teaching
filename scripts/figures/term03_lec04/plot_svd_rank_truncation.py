"""
SVD rank truncation for noise attenuation.

Three-panel figure:
  (a) Noisy synthetic gather: 3 flat reflection events (each rank 1,
      total signal rank = 3) plus random noise.
  (b) Singular-value spectrum (log scale) showing a clear knee between
      the 3 large signal singular values and the noise floor.
  (c) Denoised gather after truncating to rank 3: only signal is kept.

Note: SVD rank truncation in the t-x domain works best when events are
flat (or nearly flat after NMO correction).  Dipping events are better
handled by Cadzow (Hankel-SVD) filtering in the F-X domain (Figure 10).
"""

import numpy as np
import matplotlib.pyplot as plt

# ════════════════════════════════════════════════════════════════════
# Figure settings
# ════════════════════════════════════════════════════════════════════
FIG_WIDTH = 13.0
FIG_HEIGHT = 4.5
DPI = 150
OUTPUT_PATH = "figures/term03_lec04/term03_lec04_svd_rank_truncation.png"

COL_SIGNAL = "#0072B2"   # blue
COL_NOISE  = "#D55E00"   # vermillion
COL_KNEE   = "#CC3311"   # red (truncation line)
COL_SHADE  = "#0072B2"   # blue (signal subspace shading)

# ════════════════════════════════════════════════════════════════════
# Data parameters
# ════════════════════════════════════════════════════════════════════
N_TRACES = 50
DT = 0.004            # 4 ms
T_MAX = 1.5           # s
N_SAMPLES = int(T_MAX / DT) + 1   # 376
F0 = 25.0             # Ricker peak frequency (Hz)
NOISE_AMP = 0.20
SEED = 42

# Three flat events: each contributes rank 1, so signal rank = 3.
# Flat events are the correct setup for t-x SVD: the method works best
# when events are horizontal (or nearly flat after NMO correction).
EVENTS = [
    {"t0": 0.35, "amp": 1.0},
    {"t0": 0.70, "amp": 0.7},
    {"t0": 1.10, "amp": 0.5},
]


# ════════════════════════════════════════════════════════════════════
# Helper
# ════════════════════════════════════════════════════════════════════

def ricker(f0, dt, duration=0.16):
    t = np.arange(-duration / 2, duration / 2 + dt, dt)
    tau = np.pi * f0 * t
    return t, (1.0 - 2.0 * tau ** 2) * np.exp(-tau ** 2)


# ════════════════════════════════════════════════════════════════════
# Build synthetic gather
# ════════════════════════════════════════════════════════════════════
time = np.arange(N_SAMPLES) * DT
t_w, wlet = ricker(F0, DT)
n_half = len(wlet) // 2

signal = np.zeros((N_SAMPLES, N_TRACES))
for ev in EVENTS:
    idx = int(round(ev["t0"] / DT))
    lo, hi = idx - n_half, idx + n_half + 1
    if 0 <= lo and hi <= N_SAMPLES:
        signal[lo:hi, :] += ev["amp"] * wlet[:, np.newaxis]

# Add random noise
rng = np.random.RandomState(SEED)
noise = NOISE_AMP * rng.randn(N_SAMPLES, N_TRACES)
gather = signal + noise


# ════════════════════════════════════════════════════════════════════
# SVD
# ════════════════════════════════════════════════════════════════════
U, sigma, Vt = np.linalg.svd(gather, full_matrices=False)

# Auto-detect knee: find largest drop in log(σ) relative to neighbours
log_sigma = np.log10(sigma)
# Compute second derivative of log spectrum to find the sharpest drop
# Use a simple approach: find where σ drops by more than a factor of 3
# from the previous value, after the initial decline
K_TRUNC = 3
for i in range(2, len(sigma) - 1):
    if sigma[i] > 0 and sigma[i + 1] > 0:
        ratio = sigma[i] / sigma[i + 1]
        if ratio > 2.5 and sigma[i] > sigma[0] * 0.05:
            K_TRUNC = i + 1
            break

# Rank-K truncation: D_K = U[:, :K] diag(sigma[:K]) Vt[:K, :]
gather_denoised = U[:, :K_TRUNC] @ np.diag(sigma[:K_TRUNC]) @ Vt[:K_TRUNC, :]


# ════════════════════════════════════════════════════════════════════
# Plotting
# ════════════════════════════════════════════════════════════════════
fig, (ax_a, ax_b, ax_c) = plt.subplots(
    1, 3, figsize=(FIG_WIDTH, FIG_HEIGHT),
    gridspec_kw={"width_ratios": [1.0, 0.8, 1.0], "wspace": 0.35},
)

# Shared color limits for both gathers
vmax = np.max(np.abs(gather)) * 0.25
vmin = -vmax
cmap = "RdBu"

# ── Panel (a): noisy input gather ───────────────────────────────────
ax_a.imshow(gather, aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax,
            extent=[0, N_TRACES - 1, T_MAX, 0])
ax_a.set_xlabel("Trace index", fontsize=10)
ax_a.set_ylabel("Time (s)", fontsize=10)
ax_a.set_title("(a) input: signal + noise", fontsize=10, pad=8)

# ── Panel (b): singular value spectrum ──────────────────────────────
n_sv = len(sigma)
idx = np.arange(1, n_sv + 1)

ax_b.plot(idx, sigma, "o-", color=COL_SIGNAL, markersize=4, lw=1.5)

# Truncation line
ax_b.axvline(K_TRUNC + 0.5, color=COL_KNEE, ls="--", lw=1.5, zorder=3)

# Shade signal subspace (left of truncation)
ax_b.axvspan(0.5, K_TRUNC + 0.5, color=COL_SHADE, alpha=0.10, zorder=0)
ax_b.axvspan(K_TRUNC + 0.5, n_sv + 0.5, color=COL_NOISE, alpha=0.08, zorder=0)

# Labels
ax_b.text(K_TRUNC / 2 + 0.5, sigma[0] * 0.45, "signal\nsubspace",
          fontsize=8, ha="center", va="center", color=COL_SHADE,
          fontweight="bold")
ax_b.text((K_TRUNC + n_sv) / 2 + 0.5, sigma[K_TRUNC] * 3.0,
          "noise\nsubspace",
          fontsize=8, ha="center", va="center", color=COL_NOISE,
          fontweight="bold")

ax_b.set_yscale("log")
ax_b.set_xlabel("Singular value index $i$", fontsize=10)
ax_b.set_ylabel(r"Singular value $\sigma_i$", fontsize=10)
ax_b.set_title(f"(b) singular values (keep top {K_TRUNC})", fontsize=10, pad=8)
ax_b.set_xlim(0.5, n_sv + 0.5)
ax_b.set_ylim(sigma[-1] * 0.5, sigma[0] * 2.0)
ax_b.grid(True, axis="y", ls=":", alpha=0.5)

# ── Panel (c): denoised gather ──────────────────────────────────────
ax_c.imshow(gather_denoised, aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax,
            extent=[0, N_TRACES - 1, T_MAX, 0])
ax_c.set_xlabel("Trace index", fontsize=10)
ax_c.set_ylabel("Time (s)", fontsize=10)
ax_c.set_title(f"(c) output: rank-{K_TRUNC} truncation", fontsize=10, pad=8)

fig.suptitle("SVD rank truncation for noise attenuation",
             fontsize=13, fontweight="bold", y=1.02)

plt.savefig(OUTPUT_PATH, dpi=DPI, bbox_inches="tight")
plt.close()

print(f"Saved figure to {OUTPUT_PATH}")
print(f"Gather: {N_SAMPLES} samples x {N_TRACES} traces, dt = {DT*1000:.0f} ms")
print(f"Events:")
for ev in EVENTS:
    print(f"  t0 = {ev['t0']:.2f} s, amp = {ev['amp']:.1f}")
print(f"Noise amp = {NOISE_AMP:.2f}, seed = {SEED}")
print(f"Auto-detected rank truncation K = {K_TRUNC}")
print(f"Top {min(K_TRUNC+2, n_sv)} SVs: "
      + ", ".join(f"{s:.1f}" for s in sigma[:min(K_TRUNC+2, n_sv)]))
