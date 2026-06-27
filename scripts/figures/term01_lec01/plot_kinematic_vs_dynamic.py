#!/usr/bin/env python3
"""
Figure: Kinematic vs Dynamic problems in seismic data processing.

Two-panel layout:
  (Left)  Kinematic panel — synthetic CMP gather with a single hyperbolic
          reflection of constant amplitude.  Annotations highlight the goal
          of placing reflection energy at the correct time and spatial
          position (NMO correction, static corrections, migration).
  (Right) Dynamic panel — the same gather geometry but with offset-dependent
          amplitude variations (AVO-style).  Annotations highlight the goal
          of recovering true relative amplitudes (gain, deconvolution,
          Q-compensation, demultiple).

Pedagogical intention: show students that seismic processing has two
complementary themes — positioning (kinematic) and amplitude recovery
(dynamic) — and that both are needed for accurate imaging and inversion.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
DT = 0.004             # time sampling (s)
N_SAMPLES = 512        # number of time samples
T_MAX = N_SAMPLES * DT # total time (s)
F_DOM = 25.0           # dominant wavelet frequency (Hz)
V1 = 2000.0            # velocity of first layer (m/s)
T0 = 1.0               # zero-offset two-way time (s)

OFFSETS = np.linspace(50, 2500, 36)  # m, 36 offsets
N_TRACES = len(OFFSETS)

# ---------------------------------------------------------------------------
# Helper: simple Ricker wavelet
# ---------------------------------------------------------------------------
def ricker_wavelet(dt: float, fdom: float, length: float = 0.3) -> np.ndarray:
    """Return a Ricker (Mexican-hat) wavelet sampled at *dt* with dominant
    frequency *fdom* and total length *length* seconds."""
    t = np.arange(-length / 2, length / 2, dt)
    arg = (np.pi * fdom * t) ** 2
    w = (1.0 - 2.0 * arg) * np.exp(-arg)
    return t, w / np.max(np.abs(w))


# ---------------------------------------------------------------------------
# Build synthetic gather
# ---------------------------------------------------------------------------
def build_gather(offsets: np.ndarray, v: float, t0: float,
                 amplitude_func=None) -> np.ndarray:
    """Create a synthetic CMP gather with one hyperbolic reflection.

    *amplitude_func* : callable(offset_m) -> amplitude scaling factor.
    If None, amplitude is constant (=1.0).
    Returns array of shape (N_TRACES, N_SAMPLES).
    """
    dt = DT
    n_samp = N_SAMPLES
    t_axis = np.arange(n_samp) * dt

    w_t, w = ricker_wavelet(dt, F_DOM)

    gather = np.zeros((len(offsets), n_samp))

    for i, x in enumerate(offsets):
        # Two-way time for this offset (hyperbolic moveout)
        t_x = np.sqrt(t0 ** 2 + (x / v) ** 2)
        idx = int(round(t_x / dt))

        amp = 1.0 if amplitude_func is None else amplitude_func(x)
        trace = np.zeros(n_samp)
        # Place wavelet at the reflection time
        nw = len(w)
        start = max(0, idx - nw // 2)
        end = min(n_samp, start + nw)
        sl = slice(start, end)
        trace[sl] = amp * w[:end - start]
        gather[i, :] = trace

    return gather


# ---------------------------------------------------------------------------
# Plot a single gather as wiggles
# ---------------------------------------------------------------------------
def plot_gather(ax, gather: np.ndarray, offsets: np.ndarray,
                title: str, color: str = "C0",
                label_offsets: bool = True):
    """Wiggle-trace display of a CMP gather."""
    n_tr, n_samp = gather.shape
    t_axis = np.arange(n_samp) * DT

    # Normalise each trace for display
    for i in range(n_tr):
        tr = gather[i, :]
        peak = np.max(np.abs(tr))
        if peak > 1e-12:
            tr = tr / peak
        ax.plot(i + tr, t_axis, color=color, lw=0.5)
        # Fill positive lobes
        ax.fill_betweenx(t_axis, i, i + tr,
                         where=(tr > 0), color=color, alpha=0.3, lw=0)

    ax.set_ylim(T_MAX, 0)
    if label_offsets:
        # Label a few offset values
        tick_idx = np.linspace(0, n_tr - 1, 5).astype(int)
        ax.set_xticks(tick_idx)
        ax.set_xticklabels([f"{offsets[i]:.0f}" for i in tick_idx])
    else:
        ax.set_xticks([])

    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_ylabel("Time (s)")
    ax.grid(True, alpha=0.2, axis="y")
    ax.tick_params(labelsize=9)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    # --- Kinematic gather: constant amplitude -------------------------------
    gather_kin = build_gather(OFFSETS, V1, T0, amplitude_func=None)

    # --- Dynamic gather: offset-dependent amplitude (AVO effect) ------------
    def avo_amplitude(x):
        """Simple AVO-like amplitude variation: decreasing with offset."""
        return np.exp(-x / 1500)  # decays from 1.0 to ~0.19 at 2500 m

    gather_dyn = build_gather(OFFSETS, V1, T0, amplitude_func=avo_amplitude)

    # -------------------------------------------------------------------
    # Figure: two panels side-by-side
    # -------------------------------------------------------------------
    fig, (ax_kin, ax_dyn) = plt.subplots(1, 2, figsize=(10, 5.5),
                                         sharey=True)

    # --- Left panel: Kinematic -----------------------------------------
    plot_gather(ax_kin, gather_kin, OFFSETS,
                title="Kinematic: Positioning", color="C0")

    # Annotation box explaining kinematic
    ax_kin.annotate(
        "", xy=(15, 1.4), xytext=(15, 0.9),
        arrowprops=dict(arrowstyle="<->", color="C3", lw=1.5)
    )
    ax_kin.text(0.5, 0.70,
                "NMO correction:\nflatten the event",
                transform=ax_kin.transAxes, fontsize=8,
                color="C3", va="top", ha="center",
                bbox=dict(boxstyle="round,pad=0.3",
                          facecolor="white", edgecolor="C3", alpha=0.85))

    ax_kin.text(0.03, 0.08, "Statics", transform=ax_kin.transAxes,
                fontsize=8, color="C2", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2",
                          facecolor="white", edgecolor="C2", alpha=0.8))
    ax_kin.text(0.55, 0.08, "Migration", transform=ax_kin.transAxes,
                fontsize=8, color="C2", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.2",
                          facecolor="white", edgecolor="C2", alpha=0.8))

    ax_kin.text(0.5, -0.12,
                "Goal: place reflection energy at the correct\n"
                "time and spatial position",
                transform=ax_kin.transAxes, fontsize=9,
                ha="center", va="top", style="italic")

    # --- Right panel: Dynamic ------------------------------------------
    plot_gather(ax_dyn, gather_dyn, OFFSETS,
                title="Dynamic: Amplitudes", color="C1")

    # Annotations for dynamic corrections
    annotations_dyn = [
        (0.02, 0.92, "Gain (spherical\ndivergence correction)", "C3"),
        (0.02, 0.75, "Deconvolution\n(wavelet compression)", "C4"),
        (0.65, 0.92, "Q compensation\n(absorption)", "C2"),
        (0.65, 0.75, "Demultiple\n(multiple attenuation)", "C5"),
    ]
    for xx, yy, txt, clr in annotations_dyn:
        ax_dyn.text(xx, yy, txt, transform=ax_dyn.transAxes,
                    fontsize=7.5, color=clr,
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                              edgecolor=clr, alpha=0.85))

    # Arrow showing amplitude variation
    ax_dyn.annotate(
        "", xy=(0.15, 0.35), xytext=(0.85, 0.35),
        arrowprops=dict(arrowstyle="->", color="grey", lw=1.2,
                        linestyle="dashed"),
        transform=ax_dyn.transAxes
    )
    ax_dyn.text(0.5, 0.38, "Amplitude varies with offset",
                transform=ax_dyn.transAxes, fontsize=7.5,
                ha="center", va="bottom", color="grey", style="italic")

    ax_dyn.text(0.5, -0.12,
                "Goal: recover true relative amplitudes\n"
                "for lithology interpretation & inversion",
                transform=ax_dyn.transAxes, fontsize=9,
                ha="center", va="top", style="italic")

    # --- Shared x-axis label after panels are drawn ---
    fig.text(0.5, 0.01, "Offset (m)", ha="center", fontsize=10)

    # --- Final adjustments ---
    fig.tight_layout(rect=[0, 0.06, 1, 1])

    # --- Save ---
    out_dir = Path("figures/term01_lec01")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "term01_lec01_kinematic_vs_dynamic.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
