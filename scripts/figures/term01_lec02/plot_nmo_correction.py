"""
NMO correction figure for Term 1 Lecture 02.

Creates a synthetic CMP gather with three flat reflectors, applies the correct
NMO correction by mapping each zero-offset sample to the corresponding offset
time, and displays the raw gather and the flattened gather. The nonlinear
mapping naturally stretches the wavelet at far offsets, which is visible in the
NMO-corrected panel.

The script is self-contained and writes a single PNG to figures/term01_lec02/.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Acquisition / model parameters
# ---------------------------------------------------------------------------
nx = 60                         # number of offsets
xmax = 2000.0                   # maximum offset (m) — chosen so the hyperbolae do not cross
offsets = np.linspace(0.0, xmax, nx)
dt = 0.004                      # sample interval (s)
nt = 600                        # number of time samples (2.4 s window)
times = np.arange(nt) * dt

# Three reflectors: (t0 in s, NMO velocity in m/s, amplitude)
reflectors = [
    (0.4, 1800.0, 1.0),
    (1.0, 2200.0, -0.7),
    (1.6, 2600.0, 0.5),
]

# Ricker wavelet
def ricker(t, f=18.0):
    t = np.asarray(t)
    pi2f2 = (np.pi * f) ** 2
    return (1.0 - 2.0 * pi2f2 * t ** 2) * np.exp(-pi2f2 * t ** 2)

wavelet_t = np.arange(-0.08, 0.08 + dt, dt)

# ---------------------------------------------------------------------------
# NMO velocity as a function of t0 (interpolated from reflector picks)
# ---------------------------------------------------------------------------
t0_picks = np.array([r[0] for r in reflectors])
v_picks = np.array([r[1] for r in reflectors])

def vnmo_of_t0(t0):
    return np.interp(t0, t0_picks, v_picks, left=v_picks[0], right=v_picks[-1])

# ---------------------------------------------------------------------------
# Build the raw CMP gather
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

# ---------------------------------------------------------------------------
# Apply NMO correction: for each output t0 and offset x, sample the input at
# t = sqrt(t0^2 + x^2 / V(t0)^2). This is the inverse of the NMO mapping.
# ---------------------------------------------------------------------------
gather_nmo = np.zeros_like(gather)
for ix, x in enumerate(offsets):
    t_in = np.sqrt(times ** 2 + (x / vnmo_of_t0(times)) ** 2)
    gather_nmo[:, ix] = np.interp(t_in, times, gather[:, ix], left=0, right=0)

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

vm = 0.8 * np.max(np.abs(gather))
# Display window that comfortably contains all events
t_display_max = 2.0

ax = axes[0]
im = ax.imshow(gather, aspect="auto", extent=[offsets[0], offsets[-1], times[-1], times[0]],
               cmap="seismic", vmin=-vm, vmax=vm, interpolation="bilinear")
for t0, vnmo, _ in reflectors:
    tx = np.sqrt(t0 ** 2 + (offsets / vnmo) ** 2)
    ax.plot(offsets, tx, "k--", lw=1.5, alpha=0.7)
ax.set_xlabel("Offset (m)", fontsize=11)
ax.set_ylabel("Two-way time (s)", fontsize=11)
ax.set_title("(a) Raw CMP gather", fontsize=11)
ax.set_ylim(t_display_max, 0.0)
ax.grid(True, alpha=0.3)

ax = axes[1]
ax.imshow(gather_nmo, aspect="auto", extent=[offsets[0], offsets[-1], times[-1], times[0]],
          cmap="seismic", vmin=-vm, vmax=vm, interpolation="bilinear")
for t0, _, _ in reflectors:
    ax.axhline(t0, color="k", linestyle="--", lw=1.5, alpha=0.7)
ax.set_xlabel("Offset (m)", fontsize=11)
ax.set_title("(b) After NMO correction", fontsize=11)
ax.set_ylim(t_display_max, 0.0)
ax.grid(True, alpha=0.3)

plt.suptitle("Normal-moveout correction flattens reflection hyperbolae", fontsize=12, y=1.02)
plt.tight_layout()
plt.savefig("figures/term01_lec02/term01_lec02_nmo_correction.png", dpi=200, bbox_inches="tight")
print("Saved figures/term01_lec02/term01_lec02_nmo_correction.png")
