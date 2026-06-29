"""
NMO correction figure for Term 1 Lecture 02.

Creates a synthetic CMP gather with three flat reflectors, applies the correct
NMO correction, and displays the raw gather, the applied correction, and the
flattened gather.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Acquisition / model parameters
# ---------------------------------------------------------------------------
nx = 60                         # number of offsets
xmax = 3000.0                   # maximum offset (m)
offsets = np.linspace(0.0, xmax, nx)
dt = 0.004                      # sample interval (s)
nt = 500                        # number of time samples
times = np.arange(nt) * dt

# Three reflectors: (t0 in s, NMO velocity in m/s, amplitude)
reflectors = [
    (0.4, 1800.0, 1.0),
    (0.8, 2200.0, -0.7),
    (1.3, 2500.0, 0.5),
]

# Ricker wavelet
def ricker(t, f=25.0):
    t = np.asarray(t)
    pi2f2 = (np.pi * f) ** 2
    return (1.0 - 2.0 * pi2f2 * t ** 2) * np.exp(-pi2f2 * t ** 2)

# ---------------------------------------------------------------------------
# Build the raw CMP gather
# ---------------------------------------------------------------------------
gather = np.zeros((nt, nx))
wavelet_t = np.arange(-0.05, 0.05 + dt, dt)
for t0, vnmo, amp in reflectors:
    tx = np.sqrt(t0 ** 2 + (offsets / vnmo) ** 2)
    for ix, t_x in enumerate(tx):
        shift = t_x - t0
        shifted = np.interp(wavelet_t + shift, wavelet_t, ricker(wavelet_t))
        idx = np.round((t0 + wavelet_t) / dt).astype(int)
        valid = (idx >= 0) & (idx < nt)
        gather[idx[valid], ix] += amp * shifted[valid]

# ---------------------------------------------------------------------------
# Apply NMO correction (inverse stretch by mapping each sample to t0)
# ---------------------------------------------------------------------------
gather_nmo = np.zeros_like(gather)
for ix, x in enumerate(offsets):
    for t0, vnmo, _ in reflectors:
        # NMO shift for this zero-offset time
        shift = np.sqrt(t0 ** 2 + (x / vnmo) ** 2) - t0
    # General mapping: for each output sample t0, take input at t = t0 + shift
    for it0, t0 in enumerate(times):
        shift = 0.0
        for _t0, vnmo, _ in reflectors:
            if abs(t0 - _t0) < 0.05:
                shift = np.sqrt(t0 ** 2 + (x / vnmo) ** 2) - t0
                break
        # If no reflector nearby, use local velocity from linear interpolation of vnmo(t0)
        if shift == 0.0 and t0 > 0:
            # Interpolate NMO velocity as function of t0 from reflector picks
            vnmo_t0 = np.interp(t0, [r[0] for r in reflectors], [r[1] for r in reflectors])
            shift = np.sqrt(t0 ** 2 + (x / vnmo_t0) ** 2) - t0
        t_in = t0 + shift
        gather_nmo[it0, ix] = np.interp(t_in, times, gather[:, ix])

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

vm = 0.8 * np.max(np.abs(gather))

ax = axes[0]
ax.imshow(gather, aspect="auto", extent=[offsets[0], offsets[-1], times[-1], times[0]],
          cmap="seismic", vmin=-vm, vmax=vm, interpolation="bilinear")
for t0, vnmo, _ in reflectors:
    tx = np.sqrt(t0 ** 2 + (offsets / vnmo) ** 2)
    ax.plot(offsets, tx, "k--", lw=1.5, alpha=0.7)
ax.set_xlabel("Offset (m)", fontsize=11)
ax.set_ylabel("Two-way time (s)", fontsize=11)
ax.set_title("(a) Raw CMP gather", fontsize=11)
ax.grid(True, alpha=0.3)

ax = axes[1]
ax.imshow(gather_nmo, aspect="auto", extent=[offsets[0], offsets[-1], times[-1], times[0]],
          cmap="seismic", vmin=-vm, vmax=vm, interpolation="bilinear")
for t0, _, _ in reflectors:
    ax.axhline(t0, color="k", linestyle="--", lw=1.5, alpha=0.7)
ax.set_xlabel("Offset (m)", fontsize=11)
ax.set_title("(b) After NMO correction", fontsize=11)
ax.grid(True, alpha=0.3)

plt.suptitle("Normal-moveout correction flattens reflection hyperbolae", fontsize=12, y=1.02)
plt.tight_layout()
plt.savefig("figures/term01_lec02/term01_lec02_nmo_correction.png", dpi=200, bbox_inches="tight")
print("Saved figures/term01_lec02/term01_lec02_nmo_correction.png")
