"""
Multichannel vs single-trace first-break picking.

Output: figures/term03_lec02/term03_lec02_multichannel_picking.png
"""

import numpy as np
import matplotlib.pyplot as plt

COLORS = ["#0173B2", "#DE8F05", "#029E73", "#D55E00", "#CC79A7", "#F0E442"]

# 40 receivers, offset from 0 to 3000 m
n = 40
x = np.linspace(0, 3000, n)
v_head = 1800  # m/s head-wave velocity
noise_amp = 8  # ms
np.random.seed(10)
noise = np.random.randn(n) * noise_amp
# True first-break time
picks_true = x / v_head + 0.050

# Single-trace picks: add outliers and noise
picks_single = picks_true + noise / 1000.0
# Add two bad outliers
picks_single[8] += 0.040
picks_single[28] -= 0.035

# Multichannel picks: fit a line, reject outliers, re-pick in a window
# Here we simulate the result of a multichannel workflow: mostly clean, outliers removed
coefs = np.polyfit(x, picks_single, 1)
fit_line = np.polyval(coefs, x)
residual = np.abs(picks_single - fit_line)
tol = 0.020  # 20 ms tolerance
picks_multi = picks_single.copy()
picks_multi[residual > tol] = np.nan  # rejected outliers, then re-picked near the line
# For display, replace rejected points by the line value plus small noise
picks_multi[np.isnan(picks_multi)] = fit_line[np.isnan(picks_multi)] + np.random.randn(np.sum(np.isnan(picks_multi))) * 0.003

fig, axes = plt.subplots(1, 2, figsize=(10, 6), dpi=150)

# Single-trace
ax = axes[0]
ax.plot(x, picks_true * 1000, color=COLORS[0], lw=2, label="True first break")
ax.plot(x, picks_single * 1000, "o", color=COLORS[3], ms=4, label="Single-trace picks")
ax.set_xlabel("Offset (m)")
ax.set_ylabel("First-break time (ms)")
ax.set_title("Single-trace picking")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
ax.set_xlim(0, 3000)

# Multichannel
ax = axes[1]
ax.plot(x, picks_true * 1000, color=COLORS[0], lw=2, label="True first break")
ax.plot(x, picks_multi * 1000, "o", color=COLORS[2], ms=4, label="Multichannel picks")
ax.plot(x, fit_line * 1000, "--", color=COLORS[1], lw=1.5, label="Fitted moveout")
ax.set_xlabel("Offset (m)")
ax.set_ylabel("First-break time (ms)")
ax.set_title("Multichannel picking")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
ax.set_xlim(0, 3000)

plt.tight_layout()
plt.savefig("figures/term03_lec02/term03_lec02_multichannel_picking.png", dpi=150, bbox_inches="tight")
plt.close()
