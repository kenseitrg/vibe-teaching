"""
NMO stretch and mute figure for Term 1 Lecture 02.

Shows how a constant-frequency wavelet is stretched at far offsets after NMO
correction, plots the stretch factor as a function of offset and time, and
indicates the typical mute zone used before stack.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
t0 = 1.0          # zero-offset time of the event (s)
vnmo = 2000.0     # m/s
f0 = 25.0         # dominant wavelet frequency (Hz)
offsets = np.linspace(0.0, 3000.0, 100)

# ---------------------------------------------------------------------------
# Stretch factor: dt_in / dt0 for a fixed output sample t0
# NMO correction maps input time t = sqrt(t0^2 + x^2/V^2) to output time t0.
# Therefore dt/dt0 = t0 / t.
# ---------------------------------------------------------------------------
t = np.sqrt(t0 ** 2 + (offsets / vnmo) ** 2)
stretch = t / t0                         # > 1
fractional_stretch = (t - t0) / t0 * 100  # percent

# Wavelet before and after NMO at two offsets
wavelet_t = np.linspace(-0.06, 0.06, 300)

def ricker(t, f):
    pi2f2 = (np.pi * f) ** 2
    return (1.0 - 2.0 * pi2f2 * t ** 2) * np.exp(-pi2f2 * t ** 2)

near_off = 200.0
far_off = 2800.0

# Raw wavelet is the same at both offsets (same source signature)
w_raw = ricker(wavelet_t, f0)

# After NMO the wavelet is stretched by the local stretch factor
near_stretch = np.sqrt(t0 ** 2 + (near_off / vnmo) ** 2) / t0
far_stretch = np.sqrt(t0 ** 2 + (far_off / vnmo) ** 2) / t0
w_near = ricker(wavelet_t / near_stretch, f0)
w_far = ricker(wavelet_t / far_stretch, f0)

# ---------------------------------------------------------------------------
# Build a 2-D stretch-factor map for (t0, x)
# ---------------------------------------------------------------------------
t0_grid = np.linspace(0.3, 1.6, 200)
X, T0 = np.meshgrid(offsets, t0_grid)
T = np.sqrt(T0 ** 2 + (X / vnmo) ** 2)
STRETCH_MAP = (T - T0) / T0 * 100.0

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(12, 7))

# Wavelet comparison
ax_w = fig.add_axes([0.08, 0.55, 0.40, 0.40])
ax_w.plot(wavelet_t * 1000, w_raw, "k-", lw=2, label="Raw (all offsets)")
ax_w.plot(wavelet_t * 1000, w_near, "C0-", lw=2, label=f"After NMO, {near_off:.0f} m")
ax_w.plot(wavelet_t * 1000, w_far, "C1-", lw=2, label=f"After NMO, {far_off:.0f} m")
ax_w.set_xlabel("Time (ms)", fontsize=10)
ax_w.set_ylabel("Amplitude", fontsize=10)
ax_w.set_title("Wavelet shape after NMO correction", fontsize=11)
ax_w.legend(loc="upper right", fontsize=9)
ax_w.grid(True, alpha=0.3)

# Stretch factor line plot
ax_sf = fig.add_axes([0.55, 0.55, 0.40, 0.40])
ax_sf.plot(offsets, fractional_stretch, "k-", lw=2)
ax_sf.axhline(20.0, color="C3", linestyle="--", lw=2, label="Typical mute threshold")
ax_sf.fill_between(offsets, 20.0, 100.0, color="C3", alpha=0.15)
ax_sf.set_xlabel("Offset (m)", fontsize=10)
ax_sf.set_ylabel("Fractional stretch (%)", fontsize=10)
ax_sf.set_title(f"NMO stretch for $t_0$ = {t0:.1f} s, $V_{{NMO}}$ = {vnmo:.0f} m/s", fontsize=11)
ax_sf.legend(loc="lower right", fontsize=9)
ax_sf.grid(True, alpha=0.3)
ax_sf.set_ylim(0, 80)

# 2-D stretch map with mute corridor
ax_map = fig.add_axes([0.08, 0.08, 0.87, 0.40])
im = ax_map.imshow(STRETCH_MAP, aspect="auto", origin="lower",
                   extent=[offsets[0], offsets[-1], t0_grid[0], t0_grid[-1]],
                   cmap="YlOrRd", vmin=0, vmax=80)
ax_map.contour(X, T0, STRETCH_MAP, levels=[20.0], colors="white", linestyles="--", linewidths=2)
ax_map.set_xlabel("Offset (m)", fontsize=11)
ax_map.set_ylabel("Zero-offset time $t_0$ (s)", fontsize=11)
ax_map.set_title("Stretch factor (%) versus offset and time; mute corridor at 20%", fontsize=11)
cbar = plt.colorbar(im, ax=ax_map, fraction=0.04, pad=0.02)
cbar.set_label("Fractional stretch (%)", fontsize=10)

plt.savefig("figures/term01_lec02/term01_lec02_nmo_stretch_mute.png", dpi=200, bbox_inches="tight")
print("Saved figures/term01_lec02/term01_lec02_nmo_stretch_mute.png")
