#!/usr/bin/env python3
"""
Figure: Four types of seismic data sorts (gathers).

2x2 grid of wiggle-trace panels:
  (a) Shot gather (common source)      — traces from one shot, ordered by receiver.
  (b) Receiver gather (common receiver) — traces recorded at one receiver,
                                         ordered by source.
  (c) CMP gather (common midpoint)      — traces sharing the same midpoint,
                                         ordered by offset.
  (d) Common-offset gather              — traces sharing the same offset,
                                         ordered by midpoint.

Synthetic data: two flat horizontal reflectors in a constant-velocity
medium (1800 m/s, t0=0.6 s  and  2400 m/s, t0=1.0 s).  Each trace is
a 20 Hz Ricker wavelet placed at the hyperbolic moveout time.

Output: figures/term01_lec01/term01_lec01_data_sorts.png

Pedagogical intention: show students that the same recorded dataset can be
reorganised into different gather types, each useful for different processing
steps (velocity analysis → CMP, statics → receiver gather, noise attenuation →
shot gather, AVO → common-offset gather, etc.).
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════
#  Parameters
# ═══════════════════════════════════════════════════════════════════════
DT = 0.004           # time sample interval (s)
N_SAMPLES = 400      # trace length (1.6 s)
T_MAX = N_SAMPLES * DT
F_DOM = 20.0         # Ricker wavelet dominant frequency (Hz)

# Two flat horizontal reflectors: (interval velocity m/s, t0 s)
LAYERS = [
    (1800.0, 0.6),
    (2400.0, 1.0),
]

# ═══════════════════════════════════════════════════════════════════════
#  Helpers
# ═══════════════════════════════════════════════════════════════════════

def ricker_wavelet(dt: float, fdom: float,
                   length: float = 0.3):
    """Return (time_array, normalised_Ricker_wavelet)."""
    t = np.arange(-length / 2, length / 2, dt)
    arg = (np.pi * fdom * t) ** 2
    w = (1.0 - 2.0 * arg) * np.exp(-arg)
    return t, w / np.max(np.abs(w))


def make_trace(offset: float, dt: float, n_samples: int,
               layers: list, wavelet: np.ndarray,
               whalf: int) -> np.ndarray:
    """Synthetic trace for one source–receiver offset.

    For each (v, t0) in *layers*, places the *wavelet* at the
    hyperbolic two-way time  t(x) = sqrt(t0^2 + (x/v)^2).
    """
    trace = np.zeros(n_samples)
    for v, t0 in layers:
        tx = np.sqrt(t0 ** 2 + (offset / v) ** 2)
        idx = int(round(tx / dt))
        start = max(0, idx - whalf)
        end = min(n_samples, start + len(wavelet))
        trace[start:end] += wavelet[:end - start]
    return trace


def build_gather(offsets: np.ndarray) -> np.ndarray:
    """Return (N_offsets, N_SAMPLES) gather of synthetic traces."""
    _, w = ricker_wavelet(DT, F_DOM)
    whalf = len(w) // 2
    return np.array([
        make_trace(off, DT, N_SAMPLES, LAYERS, w, whalf)
        for off in offsets
    ])


def plot_wiggle(ax, gather, xvals, xlabel, title, subtitle, color):
    """Wiggle-trace display on *ax*."""
    n_tr, n_samp = gather.shape
    t_axis = np.arange(n_samp) * DT

    for i in range(n_tr):
        tr = gather[i]
        peak = np.max(np.abs(tr))
        if peak > 1e-12:
            tr = tr / peak
        ax.plot(i + tr, t_axis, color=color, lw=0.5)
        ax.fill_betweenx(t_axis, i, i + tr,
                         where=(tr > 0),
                         color=color, alpha=0.20, lw=0)

    ax.set_ylim(T_MAX, 0)
    ax.set_xlim(-0.5, n_tr - 0.5)
    ax.set_title(title, fontsize=11, fontweight="bold", loc="left")
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel("Time (s)", fontsize=8)
    ax.tick_params(labelsize=7)
    ax.grid(True, alpha=0.15, axis="y")

    # Selected x-tick labels
    n_lab = min(5, n_tr)
    tick_idx = np.linspace(0, n_tr - 1, n_lab).astype(int)
    ax.set_xticks(tick_idx)
    ax.set_xticklabels([f"{xvals[i]:.0f}" for i in tick_idx])

    # Sorting-principle subtitle at the bottom of the panel
    # (inside the axes, above the x-axis).  No reflections at late times
    # (deepest event is ~1.0 s, T_MAX = 1.6 s), so text won't obscure data.
    ax.text(0.5, 0.02, subtitle, transform=ax.transAxes,
            fontsize=7.5, ha="center", va="bottom", style="italic",
            color="gray")

# ═══════════════════════════════════════════════════════════════════════
#  Build each gather
# ═══════════════════════════════════════════════════════════════════════

# --- (a) Shot gather (common source) ---------------------------------
#   Source fixed at 100 m; receivers spread to the right.
SRC_A = 100.0                                                    # m
RCV_A = np.arange(125.0, 626.0, 25.0)                            # m
OFF_A = RCV_A - SRC_A                                             # 25..500 m
GATH_A = build_gather(OFF_A)

# --- (b) Receiver gather (common receiver) ---------------------------
#   Receiver fixed at 500 m; sources spread to the left.
RCV_B = 500.0                                                    # m
SRC_B = np.arange(480.0, -5.0, -25.0)                            # m (descending)
OFF_B = RCV_B - SRC_B                                             # 20..500 m
GATH_B = build_gather(OFF_B)

# --- (c) CMP gather (common midpoint) --------------------------------
#   One midpoint; traces sorted by increasing offset.
OFF_C = np.arange(25.0, 526.0, 25.0)                              # m
GATH_C = build_gather(OFF_C)
CMP_C = 300.0                                                     # m (annotation)

# --- (d) Common-offset gather ---------------------------------------
#   Fixed offset; traces spread across different midpoints.
FIX_OFF_D = 200.0                                                 # m
MID_D = np.arange(150.0, 551.0, 25.0)                             # m
OFF_D = np.full_like(MID_D, FIX_OFF_D)
GATH_D = build_gather(OFF_D)

# ═══════════════════════════════════════════════════════════════════════
#  Figure
# ═══════════════════════════════════════════════════════════════════════
COLORS = ["#2166ac", "#1b7837", "#b2182b", "#762a83"]

fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharey=True)
fig.subplots_adjust(hspace=0.35, wspace=0.10, left=0.07,
                    right=0.98, bottom=0.10, top=0.96)

# --- Panel (a): Shot gather ------------------------------------------
plot_wiggle(
    axes[0, 0], GATH_A, RCV_A,
    xlabel="Receiver position (m)",
    title="(a)  Shot gather",
    subtitle="Common source — traces from one shot, ordered by receiver",
    color=COLORS[0],
)

# Mark the source position on the panel
axes[0, 0].annotate(
    "★ Source\n100 m", xy=(0.03, 0.92), xycoords="axes fraction",
    fontsize=7.5, color="#d7191c", fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.25", fc="white",
              ec="#d7191c", alpha=0.85),
)

# --- Panel (b): Receiver gather --------------------------------------
plot_wiggle(
    axes[0, 1], GATH_B, SRC_B,
    xlabel="Source position (m)",
    title="(b)  Receiver gather",
    subtitle="Common receiver — traces at one receiver, ordered by source",
    color=COLORS[1],
)

axes[0, 1].annotate(
    "▼ Receiver\n500 m", xy=(0.88, 0.92), xycoords="axes fraction",
    fontsize=7.5, color="#d7191c", fontweight="bold",
    ha="center",
    bbox=dict(boxstyle="round,pad=0.25", fc="white",
              ec="#d7191c", alpha=0.85),
)

# --- Panel (c): CMP gather -------------------------------------------
plot_wiggle(
    axes[1, 0], GATH_C, OFF_C,
    xlabel="Offset (m)",
    title="(c)  CMP gather",
    subtitle="Common midpoint — traces with same midpoint, ordered by offset",
    color=COLORS[2],
)

axes[1, 0].annotate(
    f"CMP = {CMP_C:.0f} m", xy=(0.03, 0.92), xycoords="axes fraction",
    fontsize=7.5, color=COLORS[2], fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.25", fc="white",
              ec=COLORS[2], alpha=0.85),
)

# --- Panel (d): Common-offset gather ---------------------------------
plot_wiggle(
    axes[1, 1], GATH_D, MID_D,
    xlabel="Midpoint (m)",
    title="(d)  Common-offset gather",
    subtitle=f"Same offset ({FIX_OFF_D:.0f} m) — traces ordered by midpoint",
    color=COLORS[3],
)

axes[1, 1].annotate(
    f"Offset = {FIX_OFF_D:.0f} m",
    xy=(0.03, 0.92), xycoords="axes fraction",
    fontsize=7.5, color=COLORS[3], fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.25", fc="white",
              ec=COLORS[3], alpha=0.85),
)

# --- Save -------------------------------------------------------------
out_dir = Path("figures/term01_lec01")
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "term01_lec01_data_sorts.png"
fig.savefig(out_path, dpi=150)
plt.close(fig)
print(f"Saved: {out_path}")
