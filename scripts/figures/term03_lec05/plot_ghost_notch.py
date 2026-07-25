"""
Term 3 Lecture 05 — Figure 3: Ghost notches (depth and offset dependence).

Pedagogical point
-----------------
A marine ghost (source or receiver) is a two-path interference filter.  The
direct upgoing wave and its sea-surface reflection (reflection coefficient
R ~ -1, delayed by the two-way traveltime to the surface) combine as

    G(f) = 1 - exp(-i 2*pi*f*dt),     dt = 2*d*cos(theta) / v_w

with amplitude spectrum

    |G(f)| = 2 * |sin(pi * f * dt)|.

This produces spectral NOTCHES (zeros) at

    f_n = n * v_w / (2 * d * cos(theta)),     n = 0, 1, 2, ...

Two consequences, shown in the two panels:

(a) DEPTH sets the notch frequency.  Doubling the sensor depth halves the
    notch spacing.  Here 6 m gives a first notch at 125 Hz, while 12 m moves
    it down to 62.5 Hz.  The contrasting depths make the shift very visible.

(b) OFFSET shifts the notches higher.  At non-zero propagation angle theta
    the delay shrinks by cos(theta), so the notches move to HIGHER frequency.
    This is why a 1-D deghosting operator designed for vertical incidence
    misaligns with the real notches at far offsets.

Self-contained: numpy + matplotlib only.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import viridis

V_W = 1500.0  # water velocity (m/s)


def ghost_amplitude(freqs, depth, theta_deg=0.0):
    """Amplitude spectrum |G(f)| = 2|sin(pi f dt)| of a single ghost.

    depth : sensor (source or receiver) depth below sea surface, metres.
    theta_deg : propagation angle from vertical, degrees.
    """
    theta = np.deg2rad(theta_deg)
    delay = 2.0 * depth * np.cos(theta) / V_W   # two-way ghost delay (s)
    return 2.0 * np.abs(np.sin(np.pi * freqs * delay))


def first_notch(depth, theta_deg=0.0):
    """First non-zero notch frequency f_1 = v_w / (2 d cos theta)."""
    theta = np.deg2rad(theta_deg)
    return V_W / (2.0 * depth * np.cos(theta))


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
# Wong colorblind-safe palette for the depth panel.
COL_SHALLOW = "#D55E00"   # 6 m  (vermillion)
COL_DEEP = "#0072B2"      # 12 m (blue)

freqs = np.linspace(0.0, 260.0, 6000)  # fine grid to resolve the oscillations

fig, (ax_d, ax_a) = plt.subplots(1, 2, figsize=(10, 6))

# ---- Panel (a): effect of depth (vertical incidence) ----------------------
for depth, col in ((6, COL_SHALLOW), (12, COL_DEEP)):
    amp = ghost_amplitude(freqs, depth, theta_deg=0.0)
    f1 = first_notch(depth)
    ax_d.plot(freqs, amp, color=col, lw=1.8,
              label=f"depth = {depth} m  (1st notch {f1:g} Hz)")
    # mark the first notch
    ax_d.axvline(f1, color=col, ls="--", lw=1.0, alpha=0.7)
    ax_d.annotate(f"{f1:g} Hz", (f1, 2.0), textcoords="offset points",
                  xytext=(0, -12), ha="center", fontsize=9, color=col,
                  fontweight="bold")

ax_d.set_xlim(0, 260)
ax_d.set_ylim(0, 2.25)
ax_d.set_xlabel("Frequency (Hz)")
ax_d.set_ylabel(r"Ghost amplitude $|G(f)|$")
ax_d.set_title("(a) Depth sets the notch frequency\n(vertical incidence)",
               fontsize=11)
ax_d.legend(loc="lower right", fontsize=9, framealpha=0.9)
ax_d.text(0.02, 0.97, r"$f_n = \dfrac{n\,v_w}{2d}$",
          transform=ax_d.transAxes, ha="left", va="top", fontsize=11,
          bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="grey", lw=0.8))

# ---- Panel (b): effect of offset angle (depth = 12 m) ---------------------
depth_b = 12.0
angles = [0, 30, 60]                       # propagation angles from vertical
cols = [viridis(x) for x in (0.15, 0.55, 0.90)]  # light->dark = small->large angle

for theta, col in zip(angles, cols):
    amp = ghost_amplitude(freqs, depth_b, theta_deg=theta)
    f1 = first_notch(depth_b, theta)
    ax_a.plot(freqs, amp, color=col, lw=1.8,
              label=rf"$\theta$ = {theta}$^\circ$  (1st notch {f1:.0f} Hz)")
    ax_a.axvline(f1, color=col, ls="--", lw=1.0, alpha=0.7)
    ax_a.annotate(f"{f1:.0f}", (f1, 0.18), textcoords="offset points",
                  xytext=(0, -12), ha="center", fontsize=8.5, color=col,
                  fontweight="bold")

# arrow showing the notch migrating to higher frequency with offset
ax_a.annotate("", xy=(120, 1.55), xytext=(66, 1.55),
              arrowprops=dict(arrowstyle="-|>", color="black", lw=1.4))
ax_a.text(93, 1.62, "notch shifts higher\nwith increasing offset",
          ha="center", va="bottom", fontsize=8.5)

ax_a.set_xlim(0, 170)
ax_a.set_ylim(0, 2.25)
ax_a.set_xlabel("Frequency (Hz)")
ax_a.set_ylabel(r"Ghost amplitude $|G(f)|$")
ax_a.set_title("(b) Offset shifts the notches higher\n(depth = 12 m)",
               fontsize=11)
ax_a.legend(loc="upper right", fontsize=9, framealpha=0.9)

fig.suptitle(
    r"Ghost notches: $f_n = n\,v_w / (2d\cos\theta)$ — deeper sensors move "
    r"notches down; larger offsets move them up",
    fontsize=12, y=1.02,
)
fig.tight_layout()

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
out_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                       "figures", "term03_lec05")
out_dir = os.path.abspath(out_dir)
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "term03_lec05_ghost_notch.png")
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"Saved figure to {out_path}")
