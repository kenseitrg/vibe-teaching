"""
Replacement velocity choice figure for Term 1 Lecture 03.

Shows a flat surface with a variable-thickness weathering layer and two flat
sub-weathering reflectors. The four panels illustrate:
  (a) the earth model,
  (b) zero-offset traveltimes before static correction (anomaly is imprinted on all reflectors),
  (c) traveltimes after static correction with the correct replacement velocity (anomaly removed),
  (d) residual structural distortion when the replacement velocity is too low or too high.

The script is self-contained and writes a single PNG to figures/term01_lec03/.
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Model parameters
# ---------------------------------------------------------------------------
x = np.linspace(0.0, 4000.0, 300)

# Weathering thickness varies sinusoidally
h_mean = 40.0   # m
h_amp = 25.0    # m
h_w = h_mean + h_amp * np.sin(2.0 * np.pi * x / 4000.0)

# Surface elevation (flat) and reflector depths
z_surface = 0.0
z_base_weathering = h_w                    # reflector 1 (base of weathering)
z_shallow = 100.0                          # reflector 2 (flat)
z_deep = 200.0                             # reflector 3 (flat)

# Velocities
v_weathering = 800.0                       # m/s
v_shallow = 2500.0                         # m/s, layer between base of weathering and shallow reflector
v_deep = 3500.0                            # m/s, layer below shallow reflector
v_r_correct = v_shallow                    # correct replacement velocity is the velocity of the layer directly below weathering
v_r_low = 1500.0                           # m/s, too low
v_r_high = 5000.0                          # m/s, too high

# ---------------------------------------------------------------------------
# Traveltime calculations
# ---------------------------------------------------------------------------
def traveltimes(h_w, v_w, v_r, v_shallow, v_deep, z2, z3):
    """Zero-offset two-way traveltimes for the three reflectors."""
    t1 = 2.0 * h_w / v_r                                    # base of weathering
    t2 = 2.0 * h_w / v_r + 2.0 * (z2 - h_w) / v_shallow     # shallow reflector
    t3 = 2.0 * h_w / v_r + 2.0 * (z2 - h_w) / v_shallow + 2.0 * (z3 - z2) / v_deep  # deep reflector
    return t1, t2, t3

# Before correction: weathering velocity is used for the weathering column
t1_before, t2_before, t3_before = traveltimes(h_w, v_weathering, v_weathering, v_shallow, v_deep, z_shallow, z_deep)

# After correct correction: replace weathering with v_shallow
t1_correct, t2_correct, t3_correct = traveltimes(h_w, v_weathering, v_r_correct, v_shallow, v_deep, z_shallow, z_deep)

# After wrong corrections
_, t2_low, t3_low = traveltimes(h_w, v_weathering, v_r_low, v_shallow, v_deep, z_shallow, z_deep)
_, t2_high, t3_high = traveltimes(h_w, v_weathering, v_r_high, v_shallow, v_deep, z_shallow, z_deep)

x_offset = 2000.0  # far offset for which traveltimes are also computed

# RMS velocity for each surface position, used in the hyperbolic far-offset approximation
def rms_velocity(t_w, v_w, t_shallow, v_shallow, t_deep, v_deep):
    return np.sqrt((v_w**2 * t_w + v_shallow**2 * t_shallow + v_deep**2 * t_deep) / (t_w + t_shallow + t_deep))

def far_offset_time(t0, x_offset, v_rms):
    return np.sqrt(t0**2 + (x_offset / v_rms)**2)

# Before-correction zero-offset times and RMS velocities
before_times = [t1_before, t2_before, t3_before]
# RMS velocities for each reflector before correction
V_rms_before = []
for refl in [1, 2, 3]:
    t_w = 2.0 * h_w / v_weathering
    t_shallow = 2.0 * (z_shallow - h_w) / v_shallow if refl >= 2 else np.zeros_like(h_w)
    t_deep = 2.0 * (z_deep - z_shallow) / v_deep if refl >= 3 else np.zeros_like(h_w)
    V_rms_before.append(rms_velocity(t_w, v_weathering, t_shallow, v_shallow, t_deep, v_deep))

# Far-offset traveltimes before correction
t1_before_far = far_offset_time(t1_before, x_offset, V_rms_before[0])
t2_before_far = far_offset_time(t2_before, x_offset, V_rms_before[1])
t3_before_far = far_offset_time(t3_before, x_offset, V_rms_before[2])

# Corrected zero-offset times and RMS velocities
correct_times = [t1_correct, t2_correct, t3_correct]
V_rms_correct = []
for refl in [1, 2, 3]:
    t_w = 2.0 * h_w / v_r_correct
    t_shallow = 2.0 * (z_shallow - h_w) / v_shallow if refl >= 2 else np.zeros_like(h_w)
    t_deep = 2.0 * (z_deep - z_shallow) / v_deep if refl >= 3 else np.zeros_like(h_w)
    V_rms_correct.append(rms_velocity(t_w, v_r_correct, t_shallow, v_shallow, t_deep, v_deep))

t1_correct_far = far_offset_time(t1_correct, x_offset, V_rms_correct[0])
t2_correct_far = far_offset_time(t2_correct, x_offset, V_rms_correct[1])
t3_correct_far = far_offset_time(t3_correct, x_offset, V_rms_correct[2])

# Wrong-correction zero-offset times and RMS velocities (low and high v_r)
def corrected_rms_velocity(v_r, refl):
    t_w = 2.0 * h_w / v_r
    t_shallow = 2.0 * (z_shallow - h_w) / v_shallow if refl >= 2 else np.zeros_like(h_w)
    t_deep = 2.0 * (z_deep - z_shallow) / v_deep if refl >= 3 else np.zeros_like(h_w)
    return rms_velocity(t_w, v_r, t_shallow, v_shallow, t_deep, v_deep)

# Low v_r
V_rms_low_2 = corrected_rms_velocity(v_r_low, 2)
V_rms_low_3 = corrected_rms_velocity(v_r_low, 3)
t2_low_far = far_offset_time(t2_low, x_offset, V_rms_low_2)
t3_low_far = far_offset_time(t3_low, x_offset, V_rms_low_3)

# High v_r
V_rms_high_2 = corrected_rms_velocity(v_r_high, 2)
V_rms_high_3 = corrected_rms_velocity(v_r_high, 3)
t2_high_far = far_offset_time(t2_high, x_offset, V_rms_high_2)
t3_high_far = far_offset_time(t3_high, x_offset, V_rms_high_3)

# Residual distortion for the wrong-velocity cases (deviation from the mean traveltime)
def residual(t):
    return t - np.mean(t)

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(13, 9))

# (a) Earth model cross-section
ax = axes[0, 0]
ax.fill_between(x, z_surface, z_base_weathering, color="C0", alpha=0.3,
                label=f"Weathering ($v_w$ = {v_weathering:.0f} m/s)")
ax.fill_between(x, z_base_weathering, z_shallow, color="C1", alpha=0.2,
                label=f"Shallow layer ($v_1$ = {v_shallow:.0f} m/s)")
ax.fill_between(x, z_shallow, 250.0, color="C4", alpha=0.2,
                label=f"Deep layer ($v_2$ = {v_deep:.0f} m/s)")
ax.axhline(z_surface, color="k", lw=1.5, label="Surface")
ax.plot(x, z_base_weathering, "k--", lw=1.5, label="Base of weathering")
ax.axhline(z_shallow, color="C2", lw=1.5, linestyle="-", label="Shallow reflector")
ax.axhline(z_deep, color="C3", lw=1.5, linestyle="-", label="Deep reflector")
ax.set_xlim(x[0], x[-1])
ax.set_ylim(250.0, -10.0)
ax.set_xlabel("Surface position (m)", fontsize=11)
ax.set_ylabel("Depth (m)", fontsize=11)
ax.set_title("(a) Earth model", fontsize=12)
ax.legend(loc="lower right", fontsize=9)
ax.grid(True, alpha=0.3)

# (b) Before static correction
ax = axes[0, 1]
ax.plot(x, t2_before, "C2-", lw=2, label="Shallow reflector, near offset")
ax.plot(x, t3_before, "C3-", lw=2, label="Deep reflector, near offset")
ax.plot(x, t2_before_far, "C2--", lw=1.5, alpha=0.7, label="Shallow reflector, far offset")
ax.plot(x, t3_before_far, "C3--", lw=1.5, alpha=0.7, label="Deep reflector, far offset")
ax.set_xlabel("Surface position (m)", fontsize=11)
ax.set_ylabel("Two-way time (s)", fontsize=11)
ax.set_title("(b) Before static correction", fontsize=12)
ax.legend(loc="lower right", fontsize=9)
ax.grid(True, alpha=0.3)
ax.invert_yaxis()

# (c) After correct static correction
ax = axes[1, 0]
ax.plot(x, t2_correct, "C2-", lw=2, label="Shallow reflector, near offset")
ax.plot(x, t3_correct, "C3-", lw=2, label="Deep reflector, near offset")
ax.plot(x, t2_correct_far, "C2--", lw=1.5, alpha=0.7, label="Shallow reflector, far offset")
ax.plot(x, t3_correct_far, "C3--", lw=1.5, alpha=0.7, label="Deep reflector, far offset")
# Wrong-velocity traveltimes overlaid semi-transparent to stress the effect
ax.plot(x, t2_low_far, "C2:", lw=2.0, alpha=0.4, label="Shallow, far offset, wrong $v_\\mathrm{rep}$")
ax.plot(x, t2_high_far, "C2:", lw=2.0, alpha=0.4)
ax.plot(x, t3_low_far, "C3:", lw=2.0, alpha=0.4, label="Deep, far offset, wrong $v_\\mathrm{rep}$")
ax.plot(x, t3_high_far, "C3:", lw=2.0, alpha=0.4)
ax.set_xlabel("Surface position (m)", fontsize=11)
ax.set_ylabel("Two-way time (s)", fontsize=11)
ax.set_title("(c) After correct static correction ($v_\\mathrm{rep}$ = " + f"{v_r_correct:.0f} m/s)", fontsize=12)
ax.legend(loc="lower right", fontsize=8)
ax.grid(True, alpha=0.3)
ax.invert_yaxis()

# (d) Residual distortion for wrong replacement velocities
# Residual is computed as the difference between the wrong-velocity corrected traveltime
# and the correctly corrected traveltime. At far offsets the error is larger because the
# wrong replacement velocity also changes the RMS velocity and therefore the NMO moveout.
ax = axes[1, 1]
ax.plot(x, t2_low - t2_correct, "C2-", lw=2.5, label=f"Near offset, $v_\\mathrm{{rep}}$ = {v_r_low:.0f} m/s")
ax.plot(x, t2_high - t2_correct, "C3-", lw=2.5, label=f"Near offset, $v_\\mathrm{{rep}}$ = {v_r_high:.0f} m/s")
ax.plot(x, t2_low_far - t2_correct_far, "C2--", lw=2.0, alpha=0.8, label=f"Far offset, $v_\\mathrm{{rep}}$ = {v_r_low:.0f} m/s")
ax.plot(x, t2_high_far - t2_correct_far, "C3--", lw=2.0, alpha=0.8, label=f"Far offset, $v_\\mathrm{{rep}}$ = {v_r_high:.0f} m/s")
ax.axhline(0.0, color="gray", linestyle="-", lw=1.0)
ax.set_xlabel("Surface position (m)", fontsize=11)
ax.set_ylabel("Residual time (s)", fontsize=11)
ax.set_title("(d) Residual distortion from wrong $v_\\mathrm{rep}$", fontsize=12)
ax.legend(loc="upper right", fontsize=9)
ax.grid(True, alpha=0.3)
ax.invert_yaxis()

plt.suptitle("Effect of replacement velocity on static correction", fontsize=13, y=1.02)
plt.tight_layout()
plt.savefig("figures/term01_lec03/term01_lec03_replacement_velocity.png", dpi=200, bbox_inches="tight")
print("Saved figures/term01_lec03/term01_lec03_replacement_velocity.png")
