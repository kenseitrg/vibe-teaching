"""
Marginal effective velocity as the zero-offset slope of the t^2 vs x^2 curve.

Output: figures/term03_lec02/term03_lec02_marginal_effective_velocity.png
"""

import numpy as np
import matplotlib.pyplot as plt

COLORS = ["#0173B2", "#DE8F05", "#029E73", "#D55E00", "#CC79A7", "#F0E442"]

# Non-hyperbolic traveltime
t0 = 0.5
v_nmo = 2000
x = np.linspace(0, 3000, 200)
eps = 5e-15
t_true = np.sqrt(t0**2 + x**2 / v_nmo**2 + eps * x**4)

x2 = x**2
t2 = t_true**2

# Marginal effective velocity: slope at origin
slope = (t2[1] - t2[0]) / (x2[1] - x2[0])
v_marg = 1.0 / np.sqrt(slope)

# Effective velocity over full range (for comparison)
A = np.vstack([np.ones_like(x2), x2]).T
coeff, *_ = np.linalg.lstsq(A, t2, rcond=None)
v_eff = 1.0 / np.sqrt(coeff[1])

fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
ax.plot(x2 / 1e6, t2, color=COLORS[0], lw=2, label="True $t^2(x^2)$")
ax.plot(x2 / 1e6, coeff[0] + coeff[1] * x2, "--", color=COLORS[2], lw=2, label=f"Best fit over full range, $V_{{eff}}$={v_eff:.0f} m/s")

# Tangent at origin: passes through (0, t0^2) with slope = 1/v_marg^2
t2_tangent = t0**2 + slope * x2
ax.plot(x2 / 1e6, t2_tangent, ":", color=COLORS[3], lw=2, label=f"Tangent at zero offset, $V_{{marg}}$={v_marg:.0f} m/s")

ax.set_xlabel("$x^2$ ($10^6$ m$^2$)")
ax.set_ylabel("$t^2$ (s$^2$)")
ax.set_title("Marginal effective velocity is the slope at $x=0$")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
ax.set_xlim(0, x2[-1] / 1e6)
ax.text(
    0.97, 0.23,
    r"$t^2 = t_0^2 + \dfrac{x^2}{v^2} + \varepsilon x^4$" + "\n"
    r"($\varepsilon \neq 0$ gives non-hyperbolic moveout)",
    transform=ax.transAxes,
    fontsize=11,
    ha="right",
    va="bottom",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.9, edgecolor="gray"),
)

plt.tight_layout()
plt.savefig("figures/term03_lec02/term03_lec02_marginal_effective_velocity.png", dpi=150, bbox_inches="tight")
plt.close()
