"""
Effective velocity: best-fit hyperbola for different offset ranges.

Output: figures/term03_lec02/term03_lec02_effective_velocity.png
"""

import numpy as np
import matplotlib.pyplot as plt

COLORS = ["#0173B2", "#DE8F05", "#029E73", "#D55E00", "#CC79A7", "#F0E442"]

# True traveltime with non-hyperbolic moveout (e.g., vertical velocity gradient)
t0 = 0.5  # s
v_nmo = 2000  # m/s
x = np.linspace(0, 3000, 200)
# Add a small non-hyperbolic term: t^2 = t0^2 + x^2/v^2 + epsilon*x^4
# eps is chosen so the non-hyperbolic term is a small but visible perturbation.
eps = 5e-15
t_true = np.sqrt(t0**2 + x**2 / v_nmo**2 + eps * x**4)

fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
ax.plot(x, t_true * 1000, color=COLORS[0], lw=2, label="True traveltime")

for xmax, color in [(1000, COLORS[1]), (3000, COLORS[2])]:
    mask = x <= xmax
    # Linearized fit to t^2 vs x^2 in the chosen range
    A = np.vstack([np.ones_like(x[mask]), x[mask]**2]).T
    b = t_true[mask]**2
    coeff, *_ = np.linalg.lstsq(A, b, rcond=None)
    v_eff = 1.0 / np.sqrt(coeff[1])
    t_fit = np.sqrt(np.maximum(coeff[0] + x**2 / v_eff**2, 0))
    ax.plot(x, t_fit * 1000, "--", color=color, lw=2, label=f"Fit xmax={xmax} m, $V_{{eff}}$={v_eff:.0f} m/s")
    ax.axvline(xmax, color=color, ls=":", lw=1, alpha=0.7)

ax.set_xlabel("Offset (m)")
ax.set_ylabel("Traveltime (ms)")
ax.set_title("Effective velocity depends on the offset range")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
ax.set_xlim(0, 3000)
ax.set_ylim(0, t_true[-1] * 1000 * 1.05)
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
plt.savefig("figures/term03_lec02/term03_lec02_effective_velocity.png", dpi=150, bbox_inches="tight")
plt.close()
