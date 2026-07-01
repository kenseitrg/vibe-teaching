"""
NMO velocity sensitivity figure for Term 1 Lecture 02.

Demonstrates under-correction (velocity too high), correct correction, and
over-correction (velocity too low) for a single reflection hyperbola. The NMO
correction is applied numerically by mapping each output zero-offset sample to
the corresponding offset time, which naturally produces wavelet stretch at far
offsets.

The script is self-contained and writes a single PNG to figures/term01_lec02/.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
t0 = 1.0            # zero-offset two-way time (s)
v_true = 2000.0     # true NMO velocity (m/s)
nx = 60
xmax = 2000.0       # m — chosen so the event is fully visible after correction
offsets = np.linspace(0.0, xmax, nx)

dt = 0.004
nt = 500            # 2.0 s time window
times = np.arange(nt) * dt

# Ricker wavelet
def ricker(t, f=18.0):
    t = np.asarray(t)
    pi2f2 = (np.pi * f) ** 2
    return (1.0 - 2.0 * pi2f2 * t ** 2) * np.exp(-pi2f2 * t ** 2)

wavelet_t = np.arange(-0.08, 0.08 + dt, dt)

# ---------------------------------------------------------------------------
# Build a small synthetic gather with the wavelet centred on the hyperbola
# ---------------------------------------------------------------------------
def make_gather(t0, vnmo, offsets):
    gather = np.zeros((nt, len(offsets)))
    tx = np.sqrt(t0 ** 2 + (offsets / vnmo) ** 2)
    for ix, t_x in enumerate(tx):
        for tw in wavelet_t:
            t_abs = t_x + tw
            it = int(round(t_abs / dt))
            if 0 <= it < nt:
                gather[it, ix] += ricker(tw, f=18.0)
    return gather

def apply_nmo(gather, times, offsets, v_used):
    out = np.zeros_like(gather)
    for ix, x in enumerate(offsets):
        t_in = np.sqrt(times ** 2 + (x / v_used) ** 2)
        out[:, ix] = np.interp(t_in, times, gather[:, ix], left=0, right=0)
    return out

raw = make_gather(t0, v_true, offsets)

# Velocity multipliers relative to true velocity
labels = ["Velocity too high\n(under-correction)", "Correct velocity", "Velocity too low\n(over-correction)"]
mults = [1.15, 1.00, 0.85]

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(13, 4.5), sharey=True)
vm = 0.8 * np.max(np.abs(raw))

t_display_max = 1.65

for ax, mult, label in zip(axes, mults, labels):
    corrected = apply_nmo(raw, times, offsets, mult * v_true)
    ax.imshow(corrected, aspect="auto",
              extent=[offsets[0], offsets[-1], times[-1], times[0]],
              cmap="seismic", vmin=-vm, vmax=vm, interpolation="bilinear")
    ax.axhline(t0, color="k", linestyle="--", lw=1.0, alpha=0.6)
    ax.set_xlabel("Offset (m)", fontsize=10)
    ax.set_title(label, fontsize=10)
    ax.set_ylim(t_display_max, 0.0)
    ax.grid(True, alpha=0.3)

axes[0].set_ylabel("Two-way time (s)", fontsize=11)

plt.suptitle(f"Effect of wrong NMO velocity (true $V_{{\\mathrm{{NMO}}}}$ = {v_true:.0f} m/s)",
             fontsize=12, y=1.02)
plt.tight_layout()
plt.savefig("figures/term01_lec02/term01_lec02_nmo_under_over.png", dpi=200, bbox_inches="tight")
print("Saved figures/term01_lec02/term01_lec02_nmo_under_over.png")
