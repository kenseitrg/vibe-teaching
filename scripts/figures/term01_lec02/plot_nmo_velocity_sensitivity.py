"""
NMO velocity sensitivity figure for Term 1 Lecture 02.

Demonstrates under-correction (velocity too high), correct correction, and
over-correction (velocity too low) for a single reflection hyperbola.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
t0 = 1.0            # zero-offset two-way time (s)
v_true = 2000.0     # true NMO velocity (m/s)
offsets = np.linspace(0.0, 3000.0, 60)

# Ricker wavelet
def ricker(t, f=25.0):
    t = np.asarray(t)
    pi2f2 = (np.pi * f) ** 2
    return (1.0 - 2.0 * pi2f2 * t ** 2) * np.exp(-pi2f2 * t ** 2)

# ---------------------------------------------------------------------------
# Build a small synthetic gather and apply three different velocities
# ---------------------------------------------------------------------------
def make_gather(t0, vnmo, offsets, dt=0.004, nt=400):
    times = np.arange(nt) * dt
    gather = np.zeros((nt, len(offsets)))
    wavelet_t = np.arange(-0.05, 0.05 + dt, dt)
    tx = np.sqrt(t0 ** 2 + (offsets / vnmo) ** 2)
    for ix, t_x in enumerate(tx):
        shift = t_x - t0
        shifted = np.interp(wavelet_t + shift, wavelet_t, ricker(wavelet_t))
        idx = np.round((t0 + wavelet_t) / dt).astype(int)
        valid = (idx >= 0) & (idx < nt)
        gather[idx[valid], ix] += shifted[valid]
    return times, gather

def apply_nmo(gather, times, offsets, v_used):
    nx = len(offsets)
    nt = len(times)
    out = np.zeros_like(gather)
    for ix, x in enumerate(offsets):
        for it0, t0 in enumerate(times):
            shift = np.sqrt(t0 ** 2 + (x / v_used) ** 2) - t0
            t_in = t0 + shift
            out[it0, ix] = np.interp(t_in, times, gather[:, ix])
    return out

times, raw = make_gather(t0, v_true, offsets)

# Velocity multipliers relative to true velocity
labels = ["Velocity too high\n(under-correction)", "Correct velocity", "Velocity too low\n(over-correction)"]
mults = [1.15, 1.00, 0.85]

fig, axes = plt.subplots(1, 3, figsize=(13, 4.5), sharey=True)
vm = 0.8 * np.max(np.abs(raw))

for ax, mult, label in zip(axes, mults, labels):
    corrected = apply_nmo(raw, times, offsets, mult * v_true)
    ax.imshow(corrected, aspect="auto",
              extent=[offsets[0], offsets[-1], times[-1], times[0]],
              cmap="seismic", vmin=-vm, vmax=vm, interpolation="bilinear")
    ax.axhline(t0, color="k", linestyle="--", lw=1.0, alpha=0.6)
    ax.set_xlabel("Offset (m)", fontsize=10)
    ax.set_title(label, fontsize=10)
    ax.grid(True, alpha=0.3)

axes[0].set_ylabel("Two-way time (s)", fontsize=11)
axes[0].invert_yaxis()

plt.suptitle(f"Effect of wrong NMO velocity (true $V_{{NMO}}$ = {v_true:.0f} m/s)",
             fontsize=12, y=1.02)
plt.tight_layout()
plt.savefig("figures/term01_lec02/term01_lec02_nmo_under_over.png", dpi=200, bbox_inches="tight")
print("Saved figures/term01_lec02/term01_lec02_nmo_under_over.png")
