"""
Velocity spectrum / semblance figure for Term 1 Lecture 02.

Builds a synthetic CMP gather with three reflection events, computes a
semblance-based velocity spectrum by flattening the gather with a range of
trial velocities, and overlays the picked velocity trend.

The script is self-contained and writes a single PNG to figures/term01_lec02/.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Acquisition parameters
# ---------------------------------------------------------------------------
nx = 60
xmax = 2000.0                   # m — consistent with Figure 3/4
offsets = np.linspace(0.0, xmax, nx)
dt = 0.004
nt = 500                        # 2.0 s time window
times = np.arange(nt) * dt

# Three reflectors: (t0, vnmo, amplitude)
reflectors = [
    (0.45, 1700.0, 1.0),
    (0.85, 2000.0, -0.8),
    (1.35, 2300.0, 0.6),
]

# Ricker wavelet
wavelet_t = np.arange(-0.08, 0.08 + dt, dt)


def ricker(t, f=18.0):
    t = np.asarray(t)
    pi2f2 = (np.pi * f) ** 2
    return (1.0 - 2.0 * pi2f2 * t ** 2) * np.exp(-pi2f2 * t ** 2)


# ---------------------------------------------------------------------------
# Build synthetic CMP gather with wavelets placed on the hyperbolae
# ---------------------------------------------------------------------------
gather = np.zeros((nt, nx))
for t0, vnmo, amp in reflectors:
    tx = np.sqrt(t0 ** 2 + (offsets / vnmo) ** 2)
    for ix, t_x in enumerate(tx):
        for tw in wavelet_t:
            t_abs = t_x + tw
            it = int(round(t_abs / dt))
            if 0 <= it < nt:
                gather[it, ix] += amp * ricker(tw, f=18.0)

# Add a small amount of random noise
np.random.seed(42)
gather += 0.03 * np.max(np.abs(gather)) * np.random.randn(*gather.shape)


# ---------------------------------------------------------------------------
# Helper: apply NMO correction for a given velocity
# ---------------------------------------------------------------------------
def apply_nmo(gather, times, offsets, v_used):
    out = np.zeros_like(gather)
    for ix, x in enumerate(offsets):
        t_in = np.sqrt(times ** 2 + (x / v_used) ** 2)
        out[:, ix] = np.interp(t_in, times, gather[:, ix], left=0, right=0)
    return out


# ---------------------------------------------------------------------------
# Velocity spectrum grid
# ---------------------------------------------------------------------------
v_min, v_max, nv = 1400.0, 3200.0, 80
velocities = np.linspace(v_min, v_max, nv)

# Time window for semblance (centred on each output sample)
hw = 3  # half window in samples

semblance = np.zeros((nt, nv))

for iv, v in enumerate(velocities):
    # Flatten the gather with the trial velocity
    flattened = apply_nmo(gather, times, offsets, v)

    for it0 in range(nt):
        iw_start = max(0, it0 - hw)
        iw_end = min(nt, it0 + hw + 1)
        win = flattened[iw_start:iw_end, :]
        if win.shape[0] < 3:
            continue

        stacked = np.sum(win, axis=1)
        numerator = np.sum(stacked ** 2)
        denominator = nx * np.sum(win ** 2)
        if denominator > 1e-12:
            semblance[it0, iv] = numerator / denominator

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

vm = 0.8 * np.max(np.abs(gather))
t_display_max = 1.9

# CMP gather
ax = axes[0]
ax.imshow(gather, aspect="auto",
          extent=[offsets[0], offsets[-1], times[-1], times[0]],
          cmap="seismic", vmin=-vm, vmax=vm, interpolation="bilinear")
for t0, vnmo, _ in reflectors:
    tx = np.sqrt(t0 ** 2 + (offsets / vnmo) ** 2)
    ax.plot(offsets, tx, "k--", lw=1.5, alpha=0.7)
ax.set_xlabel("Offset (m)", fontsize=11)
ax.set_ylabel("Two-way time (s)", fontsize=11)
ax.set_title("(a) Synthetic CMP gather", fontsize=11)
ax.set_ylim(t_display_max, 0.0)
ax.grid(True, alpha=0.3)

# Velocity spectrum
ax = axes[1]
ax.imshow(semblance, aspect="auto",
          extent=[velocities[0], velocities[-1], times[-1], times[0]],
          cmap="hot", vmin=0.0, vmax=1.0, interpolation="bilinear")
# Overlay true / picked trend
ax.plot([r[1] for r in reflectors], [r[0] for r in reflectors], "co", markersize=8,
        markeredgecolor="white", markeredgewidth=1.5, label="Picked velocities")
ax.set_xlabel("Velocity (m/s)", fontsize=11)
ax.set_title("(b) Semblance velocity spectrum", fontsize=11)
ax.set_ylim(t_display_max, 0.0)
ax.legend(loc="lower right", fontsize=9)
ax.grid(True, alpha=0.3)

plt.suptitle("Velocity analysis: scanning hyperbolae and measuring coherence",
             fontsize=12, y=1.02)
plt.tight_layout()
plt.savefig("figures/term01_lec02/term01_lec02_velocity_spectrum.png", dpi=200, bbox_inches="tight")
print("Saved figures/term01_lec02/term01_lec02_velocity_spectrum.png")
