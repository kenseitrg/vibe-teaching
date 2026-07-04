#!/usr/bin/env python3
"""
Dipping-reflector geometry explaining V_stack = V / cos(theta).

Inspired by the classic image-source construction: the source S is reflected
across the dipping reflector to give S'. The reflected path S-I-R equals the
straight line S'R. Decomposing S'R into a leg perpendicular to the reflector
(the zero-offset path, V t0) and a leg parallel to the reflector (the effective
offset, x cos theta) gives the hyperbolic moveout law and the cos(theta) factor.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

# Parameters
theta_deg = 20.0
theta = np.deg2rad(theta_deg)
v = 2000.0          # m/s
z = 1000.0          # m, normal distance from midpoint to reflector
x = 2000.0          # m, full source-receiver offset

s, c = np.sin(theta), np.cos(theta)
tan = s / c

# Reflector: y = d + x_surface * tan(theta); d = z / cos(theta)
d = z / c

def reflector_y(xs):
    return d + xs * tan

# Surface points
M = np.array([0.0, 0.0])
S = np.array([-x / 2.0, 0.0])
R = np.array([x / 2.0, 0.0])

# Reflection point (normal incidence from midpoint)
P = np.array([-z * s, z * c])

# Mirror image of S across the reflector
# Reflector line: s*x - c*y + d*c = 0, normal vector (s, -c)
dist = s * S[0] - c * S[1] + d * c
S_prime = S - 2.0 * dist * np.array([s, -c])

# Reflected ray intersection: line S' + t*(R-S') hits the reflector
dir_SR = R - S_prime
t = (d + S_prime[0] * tan - S_prime[1]) / (dir_SR[1] - dir_SR[0] * tan)
I = S_prime + t * dir_SR

# Unit vectors aligned with the reflector
parallel_dir = np.array([c, s])            # along the reflector (down-dip)
normal_dir = np.array([-s, c])           # perpendicular to reflector, pointing upward

# Decompose S'R into normal and parallel components
a = np.dot(R - S_prime, normal_dir)        # = -V*t0 (negative because S' is below)
b = np.dot(R - S_prime, parallel_dir)      # = x * cos(theta)

# Right-angle corner Q: move from S' along the normal by amount a
Q = S_prime + a * normal_dir

# Sanity checks
assert np.allclose(np.dot(R - Q, normal_dir), 0.0, atol=1e-6)
assert np.allclose(np.linalg.norm(R - Q), b, atol=1.0)
assert np.allclose(np.linalg.norm(S_prime - Q), abs(a), atol=1.0)

# Traveltimes
t0 = 2.0 * z / v
t = np.linalg.norm(S_prime - R) / v

# Figure
fig, ax = plt.subplots(figsize=(10, 7))

# Surface and reflector
ax.plot([-2500.0, 2500.0], [0.0, 0.0], "k-", lw=1.5, label="Surface")
ax.plot([-2200.0, 2200.0], reflector_y(np.array([-2200.0, 2200.0])), "C1-", lw=2.5, label="Dipping reflector")

# Normal-incidence ray from M to P
ax.plot([M[0], P[0]], [M[1], P[1]], "C1:", lw=1.5, alpha=0.7)

# Source, receiver, midpoint
ax.plot(*S, "ko", markersize=8)
ax.plot(*R, "ko", markersize=8)
ax.plot(*M, "ko", markersize=6)
ax.text(S[0] - 80, S[1] - 80, "S", fontsize=14, ha="center", va="top")
ax.text(R[0] + 80, R[1] - 80, "R", fontsize=14, ha="center", va="top")
ax.text(M[0] + 80, M[1] - 80, "M", fontsize=14, ha="center", va="top")

# Reflected path S-I-R
ax.plot([S[0], I[0]], [S[1], I[1]], "C0-", lw=1.5, alpha=0.8)
ax.plot([I[0], R[0]], [I[1], R[1]], "C0-", lw=1.5, alpha=0.8)

# Image source S' and equivalent straight path S'R
ax.plot(*S_prime, "C2o", markersize=8)
ax.text(S_prime[0] - 120, S_prime[1] + 80, "S'", fontsize=14, color="C2", ha="center")
ax.plot([S_prime[0], R[0]], [S_prime[1], R[1]], "C2--", lw=2.0, label="Equivalent path $S'R$")

# Right triangle S'-Q-R
ax.plot([S_prime[0], Q[0]], [S_prime[1], Q[1]], "C3-", lw=2.5)
ax.plot([Q[0], R[0]], [Q[1], R[1]], "C3-", lw=2.5)
ax.plot(*Q, "C3s", markersize=7)

# Right-angle marker at Q
mark_len = 70.0
u1 = -normal_dir   # from Q toward S' (down along normal)
u2 = -parallel_dir # from Q toward R (up-dip along reflector)
seg1 = Q + mark_len * u1
seg2 = Q + mark_len * u2
ax.plot([seg1[0], seg1[0] + mark_len * u2[0]], [seg1[1], seg1[1] + mark_len * u2[1]], "C3-", lw=1.2)
ax.plot([seg2[0], seg2[0] + mark_len * u1[0]], [seg2[1], seg2[1] + mark_len * u1[1]], "C3-", lw=1.2)

# Offset x on the surface
ax.annotate("", xy=R, xytext=S, arrowprops=dict(arrowstyle="<->", color="k", lw=1.2))
ax.text(M[0], M[1] - 160, "$x$", fontsize=14, ha="center", va="top")

# Label triangle sides
mid_normal = 0.5 * (S_prime + Q)
ax.text(mid_normal[0] - 180, mid_normal[1] + 80, "$V t_0$", fontsize=14, color="C3", ha="right", va="center")

mid_parallel = 0.5 * (Q + R)
ax.text(mid_parallel[0] + 80, mid_parallel[1] - 80, "$x \\cos\\theta$", fontsize=14, color="C3", ha="center", va="top")

mid_hyp = 0.5 * (S_prime + R)
ax.text(mid_hyp[0] - 180, mid_hyp[1] - 80, "$V t$", fontsize=14, color="C2", ha="center", va="top")

# Dip angle arc
arc_center = np.array([-1300.0, reflector_y(-1300.0)])
ax.plot([arc_center[0], arc_center[0] + 500], [arc_center[1], arc_center[1]], "k--", lw=0.8)
ax.plot([arc_center[0], arc_center[0] + 500 * c], [arc_center[1], arc_center[1] + 500 * s], "C1-", lw=1.0)
arc = Arc(arc_center, 500, 500, angle=0.0, theta1=0.0, theta2=theta_deg, color="k", lw=1.0)
ax.add_patch(arc)
ax.text(arc_center[0] + 320, arc_center[1] - 80, f"$\\theta = {theta_deg}°$", fontsize=12, ha="center")

# Formula box
ax.text(
    0.98, 0.02,
    r"$(Vt)^2 = (Vt_0)^2 + (x\cos\theta)^2$" + "\n" + r"$\Rightarrow V_\mathrm{stack} = V / \cos\theta$",
    transform=ax.transAxes,
    fontsize=14,
    verticalalignment="bottom",
    horizontalalignment="right",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="gray", alpha=0.95),
)

ax.set_aspect("equal")
ax.set_xlim(-2600, 2600)
ax.set_ylim(2200, -900)  # 0 at top, depth downward; include full right triangle above surface
ax.set_xlabel("Distance (m)", fontsize=12)
ax.set_ylabel("Depth (m)", fontsize=12)
ax.set_title("Dipping reflector: why stacking velocity is $V / \\cos\\theta$", fontsize=15, pad=20)
ax.legend(loc="upper right", fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
out_path = "figures/term01_lec02/term01_lec02_dip_moveout_cosine.png"
plt.savefig(out_path, dpi=300, bbox_inches="tight")
print(f"Saved {out_path}")
