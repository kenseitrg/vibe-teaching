"""
Velocity spectrum / semblance figure for Term 1 Lecture 02.

Builds a synthetic CMP gather with three reflection events, computes a
semblance-based velocity spectrum, and overlays the picked velocity trend.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Acquisition parameters
# ---------------------------------------------------------------------------
offsets = np.linspace(0.0, 3000.0, 40)
dt = 0.004
nt = 400
times = np.arange(nt) * dt

# Three reflectors: (t0, vnmo, amplitude)
reflectors = [
    (0.45, 1700.0, 1.0),
    (0.85, 2000.0, -0.8),
    (1.35, 2300.0, 0.6),
]

# Ricker wavelet
wavelet_t = np.arange(-0.05, 0.05 + dt, dt)


def ricker(t, f=25.0):
    t = np.asarray(t)
    pi2f2 = (np.pi * f) ** 2
    return (1.0 - 2.0 * pi2f2 * t ** 2) * np.exp(-pi2f2 * t ** 2)


# ---------------------------------------------------------------------------
# Build synthetic CMP gather
# ---------------------------------------------------------------------------
gather = np.zeros((nt, len(offsets)))
for t0, vnmo, amp in reflectors:
    tx = np.sqrt(t0 ** 2 + (offsets / vnmo) ** 2)
    for ix, t_x in enumerate(tx):
        shift = t_x - t0
        shifted = np.interp(wavelet_t + shift, wavelet_t, ricker(wavelet_t))
        idx = np.round((t0 + wavelet_t) / dt).astype(int)
        valid = (idx >= 0) & (idx < nt)
        gather[idx[valid], ix] += amp * shifted[valid]

# Add a small amount of random noise
np.random.seed(42)
gather += 0.03 * np.max(np.abs(gather)) * np.random.randn(*gather.shape)

# ---------------------------------------------------------------------------
# Velocity spectrum grid
# ---------------------------------------------------------------------------
v_min, v_max, nv = 1400.0, 3200.0, 80
velocities = np.linspace(v_min, v_max, nv)
# Time windows for semblance (centred on each sample)
hw = 3  # half window in samples

semblance = np.zeros((nt, nv))

for it0, t0 in enumerate(times):
    # Window around t0
    iw_start = max(0, it0 - hw)
    iw_end = min(nt, it0 + hw + 1)
    if iw_end - iw_start < 3:
        continue
    win_data = gather[iw_start:iw_end, :]  # (time_window, offsets)

    for iv, v in enumerate(velocities):
        # NMO shift for each offset at this t0
        shifts = np.sqrt(t0 ** 2 + (offsets / v) ** 2) - t0
        shifted_indices = np.round((iw_start + np.arange(win_data.shape[0]))[:, None] * dt
                                    - shifts[None, :]) / dt
        shifted_indices = shifted_indices.astype(int)
        valid = (shifted_indices >= 0) & (shifted_indices < nt)

        # Gather shifted window values
        n_offset = len(offsets)
        aligned = np.zeros((win_data.shape[0], n_offset))
        aligned[valid] = gather[shifted_indices[valid], np.arange(n_offset)[None, :].repeat(win_data.shape[0], axis=0)[valid]]

        # Semblance over the time window
        stacked = np.sum(aligned, axis=1)
        numerator = np.sum(stacked ** 2)
        denominator = n_offset * np.sum(aligned ** 2)
        if denominator > 1e-12:
            semblance[it0, iv] = numerator / denominator

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

vm = 0.8 * np.max(np.abs(gather))

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
ax.legend(loc="lower right", fontsize=9)
ax.grid(True, alpha=0.3)

plt.suptitle("Velocity analysis: scanning hyperbolae and measuring coherence",
             fontsize=12, y=1.02)
plt.tight_layout()
plt.savefig("figures/term01_lec02/term01_lec02_velocity_spectrum.png", dpi=200, bbox_inches="tight")
print("Saved figures/term01_lec02/term01_lec02_velocity_spectrum.png")
