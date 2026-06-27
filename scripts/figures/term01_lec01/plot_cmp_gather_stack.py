#!/usr/bin/env python3
"""
Figure: CMP gather and stack — geometry, hyperbolic moveout, NMO correction,
and stacking.

Three panels:
  (Left)   Shot/receiver geometry for one CMP — multiple source–receiver
           pairs sharing the same midpoint above a horizontal reflector.
  (Middle) Synthetic CMP gather before NMO correction, showing hyperbolic
           reflection events (primary and first-order multiple).
  (Right)  NMO-corrected gather with the primary flattened, and the resulting
           stacked trace on the right.

Pedagogical intention: illustrate the fundamental CMP concept — that different
source–receiver pairs sample the same subsurface point — and show how NMO
correction aligns them for constructive stacking while multiples (with
different moveout) are attenuated in the stack.

Output: figures/term01_lec01/term01_lec01_cmp_gather_stack.png
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
DT = 0.004              # time sampling interval (s)
N_SAMPLES = 700         # number of time samples
T_MAX = N_SAMPLES * DT  # total recording time (s)
F_DOM = 20.0            # dominant wavelet frequency (Hz)

# Two-layer model
V1 = 2000.0             # velocity of layer 1 (m/s)
T0_PRIMARY = 1.0        # zero-offset two-way time for primary (s)

# Multiple parameters — a shallow interbed or peg-leg multiple travelling
# through a lower-velocity layer, so it has a different (lower) NMO velocity
# than the primary.  When NMO correction uses the primary velocity, the
# multiple remains undercorrected and is attenuated by stacking.
V_MULTIPLE = 1500.0     # apparent NMO velocity of the multiple (m/s)
T0_MULTIPLE = 1.8       # zero-offset two-way time for the multiple (s)

# Acquisition geometry for the CMP
OFFSETS = np.linspace(50, 2000, 20)  # offsets (m), 20 traces
N_TRACES = len(OFFSETS)

# NMO correction velocity (equal to layer 1 velocity for the primary)
V_NMO = V1

# Stretch mute threshold (fractional) — set generously so the
# pedagogical point (flattened primary, undercorrected multiple)
# is visually clear across the full offset range.
STRETCH_MUTE = 0.50


# ---------------------------------------------------------------------------
# Helper: Ricker wavelet
# ---------------------------------------------------------------------------
def ricker_wavelet(dt: float, fdom: float, length: float = 0.3):
    """Generate a Ricker (Mexican-hat) wavelet.

    Parameters
    ----------
    dt : float
        Time sampling interval (s).
    fdom : float
        Dominant frequency (Hz).
    length : float
        Total wavelet length (s).

    Returns
    -------
    t : np.ndarray
        Time axis for the wavelet.
    w : np.ndarray
        Normalised wavelet amplitudes (peak amplitude = 1).
    """
    t = np.arange(-length / 2, length / 2, dt)
    arg = (np.pi * fdom * t) ** 2
    w = (1.0 - 2.0 * arg) * np.exp(-arg)
    return t, w / np.max(np.abs(w))


# ---------------------------------------------------------------------------
# Build synthetic CMP gather with primary and multiple events
# ---------------------------------------------------------------------------
def build_cmp_gather(offsets: np.ndarray) -> np.ndarray:
    """Create a synthetic CMP gather with two hyperbolic reflection events.

    Parameters
    ----------
    offsets : np.ndarray
        Source–receiver offsets (m).

    Returns
    -------
    gather : np.ndarray, shape (N_TRACES, N_SAMPLES)
        Synthetic CMP gather.
    """
    dt = DT
    n_samp = N_SAMPLES
    _, wavelet = ricker_wavelet(dt, F_DOM)
    nw = len(wavelet)

    gather = np.zeros((len(offsets), n_samp))

    # Event definitions: (t0, v_nmo, relative_amplitude)
    events = [
        (T0_PRIMARY, V1, 1.0),         # primary reflection
        (T0_MULTIPLE, V_MULTIPLE, 0.5), # multiple (lower amplitude, lower velocity)
    ]

    for i, x in enumerate(offsets):
        trace = np.zeros(n_samp)
        for t0, v, amp in events:
            # Hyperbolic traveltime
            t_x = np.sqrt(t0 ** 2 + (x / v) ** 2)
            idx = int(round(t_x / dt))
            # Place wavelet at the calculated sample position
            start = max(0, idx - nw // 2)
            end = min(n_samp, start + nw)
            trace[start:end] += amp * wavelet[:end - start]
        gather[i, :] = trace
    return gather


# ---------------------------------------------------------------------------
# NMO correction
# ---------------------------------------------------------------------------
def apply_nmo(gather: np.ndarray, offsets: np.ndarray,
              v_nmo: float, dt: float,
              stretch_mute: float = STRETCH_MUTE) -> np.ndarray:
    """Apply normal-moveout (NMO) correction to a CMP gather.

    Uses nearest-neighbour mapping from the original trace (at time t_x)
    to the corrected trace (at time t0).  A stretch mute zeros out samples
    where the stretch factor (t_x - t0) / t0 exceeds *stretch_mute*.

    Parameters
    ----------
    gather : np.ndarray, shape (N_TRACES, N_SAMPLES)
        Input CMP gather.
    offsets : np.ndarray
        Source–receiver offsets (m).
    v_nmo : float
        NMO velocity (m/s).
    dt : float
        Time sampling interval (s).
    stretch_mute : float
        Maximum allowable stretch fraction. Samples with larger stretch
        are muted (set to zero).

    Returns
    -------
    corrected : np.ndarray, shape (N_TRACES, N_SAMPLES)
        NMO-corrected gather.
    """
    n_tr, n_samp = gather.shape
    t_axis = np.arange(n_samp) * dt
    corrected = np.zeros_like(gather)

    for i, x in enumerate(offsets):
        for j in range(n_samp):
            t0 = t_axis[j]
            if t0 <= 0:
                continue
            t_x = np.sqrt(t0 ** 2 + (x / v_nmo) ** 2)
            # Stretch check
            stretch = (t_x - t0) / t0
            if stretch > stretch_mute:
                continue  # leave as zero (muted)
            idx = int(round(t_x / dt))
            if 0 <= idx < n_samp:
                corrected[i, j] = gather[i, idx]
    return corrected


# ---------------------------------------------------------------------------
# Wiggle-trace plotting
# ---------------------------------------------------------------------------
def plot_wiggle_gather(ax, gather, offsets, dt, title, color="C0",
                       label_offsets=True, stack_trace=None):
    """Plot a CMP gather as wiggles with variable-area fill.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axis to plot on.
    gather : np.ndarray, shape (N_TRACES, N_SAMPLES)
        Gather data.
    offsets : np.ndarray
        Offsets for x-axis labelling.
    dt : float
        Time sampling interval (s).
    title : str
        Subplot title.
    color : str
        Line colour.
    label_offsets : bool
        If True, show offset labels on the x-axis.
    stack_trace : np.ndarray or None
        If provided, plot this vertical trace on the right side of the
        gather as a stacked-result indicator.
    """
    n_tr, n_samp = gather.shape
    t_axis = np.arange(n_samp) * dt

    # Normalise each trace for display
    display = np.zeros_like(gather)
    for i in range(n_tr):
        tr = gather[i, :]
        peak = np.max(np.abs(tr))
        if peak > 1e-12:
            display[i, :] = tr / peak

    # Determine x-axis range
    # Leave room for stack trace if shown
    x_max = n_tr + (2.5 if stack_trace is not None else 0.5)

    # Plot wiggles
    for i in range(n_tr):
        ax.plot(i + display[i, :], t_axis, color=color, lw=0.4, zorder=3)
        # Variable-area fill (positive lobes)
        ax.fill_betweenx(t_axis, i, i + display[i, :],
                         where=(display[i, :] > 0),
                         color=color, alpha=0.30, lw=0, zorder=2)

    # Stack trace overlay
    if stack_trace is not None:
        stack_x = n_tr + 0.8
        st = stack_trace / np.max(np.abs(stack_trace)) * 0.8
        ax.plot(stack_x + st, t_axis, color="black", lw=1.2, zorder=4)
        ax.fill_betweenx(t_axis, stack_x, stack_x + st,
                         where=(st > 0), color="black", alpha=0.30,
                         lw=0, zorder=2)
        ax.axvline(x=stack_x, color="grey", lw=0.6, linestyle="--", zorder=1)
        ax.text(stack_x, T_MAX + 0.12, "Stack", ha="center",
                fontsize=7, fontweight="bold", color="black", zorder=5)

    ax.set_xlim(-0.5, x_max)
    ax.set_ylim(T_MAX, 0)

    if label_offsets:
        tick_idx = np.linspace(0, n_tr - 1, 5).astype(int)
        ax.set_xticks(tick_idx)
        ax.set_xticklabels([f"{offsets[i]:.0f}" for i in tick_idx])
    else:
        ax.set_xticks([])

    ax.set_title(title, fontsize=10, fontweight="bold", pad=6)
    ax.set_ylabel("Time (s)", fontsize=9)
    ax.grid(True, alpha=0.15, axis="y")
    ax.tick_params(labelsize=8)


# ---------------------------------------------------------------------------
# Panel 1: CMP geometry schematic
# ---------------------------------------------------------------------------
def draw_geometry_panel(ax):
    """Draw shot/receiver geometry for one CMP location."""
    ax.set_xlim(-1500, 1500)
    ax.set_ylim(-180, 1100)
    ax.set_aspect("equal")
    ax.axis("off")

    # --- Surface ---
    ax.axhline(y=0, color="#8B4513", linewidth=2.5, zorder=2)
    ax.text(1400, 30, "Surface", fontsize=8, color="#8B4513",
            ha="right", va="bottom", style="italic")

    # --- Reflector at depth ---
    depth = 850  # m (chosen for visual clarity)
    ax.axhline(y=depth, color="#666666", linewidth=1.8, linestyle="--", zorder=2)
    ax.text(1400, depth - 25, "Reflector", fontsize=8, color="#666666",
            ha="right", va="top", style="italic")

    # --- Layer-velocity annotations ---
    ax.text(-1350, depth / 2, r"$V_1 = 2000$ m/s (primary)", fontsize=7.5,
            color="#444444", style="italic",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                      edgecolor="none", alpha=0.8))
    ax.text(-1350, depth / 2 - 80, r"$V_\mathrm{mult} = 1500$ m/s (multiple)",
            fontsize=7.5, color="#C44E52", style="italic",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                      edgecolor="none", alpha=0.8))

    # --- CMP marker (vertical dashed line) ---
    ax.axvline(x=0, color="black", linewidth=0.7, linestyle=":", alpha=0.4, zorder=1)
    ax.plot(0, 0, marker="v", color="black", markersize=8, zorder=6)
    ax.text(0, -35, "CMP", fontsize=9, ha="center", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                      edgecolor="black", alpha=0.9))

    # --- Representative source-receiver pairs ---
    pair_offsets = [300, 800, 1400, 2000]
    colors = plt.cm.viridis(np.linspace(0.25, 0.85, len(pair_offsets)))

    for idx, x_off in enumerate(pair_offsets):
        src_x = -x_off / 2
        rcv_x = x_off / 2
        clr = colors[idx]

        # Source (star)
        ax.plot(src_x, 0, marker="*", color=clr, markersize=14, zorder=7)
        # Receiver (triangle)
        ax.plot(rcv_x, 0, marker="v", color=clr, markersize=11, zorder=7)

        # Ray paths: source -> reflection point (x=0, y=depth) -> receiver
        ax.plot([src_x, 0, rcv_x], [0, depth, 0],
                color=clr, linewidth=0.9, alpha=0.55, zorder=3)

    # --- Sources / Receivers group labels ---
    ax.text(-750, -120, "Sources", fontsize=8, ha="center",
            color="#8B0000", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                      edgecolor="#8B0000", alpha=0.85))
    ax.text(750, -120, "Receivers", fontsize=8, ha="center",
            color="#006400", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                      edgecolor="#006400", alpha=0.85))

    # --- Reflection point ---
    ax.plot(0, depth, marker="o", color="orange", markersize=10, zorder=8,
            markeredgecolor="black", markeredgewidth=0.5)
    ax.annotate("Reflection\npoint", xy=(0, depth), xytext=(100, depth - 50),
                fontsize=7, color="orange", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="orange", lw=1.0),
                zorder=9)

    # --- Offset annotation on one pair ---
    mid_idx = len(pair_offsets) // 2
    x_off_mid = pair_offsets[mid_idx]
    src_mid = -x_off_mid / 2
    rcv_mid = x_off_mid / 2

    ax.annotate("", xy=(rcv_mid, -70), xytext=(src_mid, -70),
                arrowprops=dict(arrowstyle="<->", color="grey", lw=1.0),
                zorder=5)
    ax.text(0, -85, f"Offset = {x_off_mid} m", ha="center",
            fontsize=7, color="grey")

    # --- Title ---
    ax.text(0, 1070, "CMP Geometry", ha="center", fontsize=10,
            fontweight="bold", color="black")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    # Build synthetic gathers
    gather_raw = build_cmp_gather(OFFSETS)
    gather_nmo = apply_nmo(gather_raw, OFFSETS, V_NMO, DT)

    # Stacked trace (mean of NMO-corrected gather)
    stacked = np.mean(gather_nmo, axis=0)

    # -------------------------------------------------------------------
    # Figure layout
    # -------------------------------------------------------------------
    fig = plt.figure(figsize=(15, 5.8))
    gs = fig.add_gridspec(
        1, 3,
        width_ratios=[1.15, 1.0, 1.15],
        left=0.04, right=0.97, bottom=0.10, top=0.90,
        wspace=0.22,
    )

    # Colour palette for the two gather panels
    C_RAW = "#3B6BA5"    # blue for raw gather
    C_NMO = "#55A868"    # green for NMO-corrected

    # ---- Panel 1: Geometry -------------------------------------------
    ax1 = fig.add_subplot(gs[0])
    draw_geometry_panel(ax1)

    # ---- Panel 2: CMP gather before NMO ------------------------------
    ax2 = fig.add_subplot(gs[1])
    plot_wiggle_gather(ax2, gather_raw, OFFSETS, DT,
                       title="CMP Gather (Before NMO)",
                       color=C_RAW)

    # Annotate primary event
    mid_idx = N_TRACES // 2
    ax2.annotate(
        "Primary\nreflection",
        xy=(mid_idx, T0_PRIMARY),
        xytext=(mid_idx + 6, T0_PRIMARY - 0.7),
        fontsize=7, color=C_RAW, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=C_RAW, lw=0.8),
        zorder=10,
    )
    # Annotate multiple event
    ax2.annotate(
        "First-order\nmultiple",
        xy=(mid_idx, T0_MULTIPLE),
        xytext=(mid_idx + 6, T0_MULTIPLE - 0.7),
        fontsize=7, color="#C44E52", fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#C44E52", lw=0.8),
        zorder=10,
    )

    ax2.set_xlabel("Offset (m)", fontsize=9)

    # ---- Panel 3: After NMO + Stack ----------------------------------
    ax3 = fig.add_subplot(gs[2])
    plot_wiggle_gather(ax3, gather_nmo, OFFSETS, DT,
                       title="After NMO Correction + Stack",
                       color=C_NMO,
                       stack_trace=stacked)

    # Annotate flattened primary
    ax3.annotate(
        "Primary\n(flattened)",
        xy=(mid_idx, T0_PRIMARY),
        xytext=(mid_idx + 6, T0_PRIMARY - 0.5),
        fontsize=7, color=C_NMO, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=C_NMO, lw=0.8),
        zorder=10,
    )
    # Annotate undercorrected multiple
    ax3.annotate(
        "Multiple\n(undercorrected)",
        xy=(mid_idx, T0_MULTIPLE),
        xytext=(mid_idx + 6, T0_MULTIPLE - 0.7),
        fontsize=7, color="#C44E52", fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#C44E52", lw=0.8),
        zorder=10,
    )

    ax3.set_xlabel("Offset (m)", fontsize=9)

    # ---- Figure-level title ----
    fig.suptitle("CMP Gather and Stack",
                 fontsize=13, fontweight="bold", y=0.98)

    # -------------------------------------------------------------------
    # Save
    # -------------------------------------------------------------------
    out_dir = Path("figures/term01_lec01")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "term01_lec01_cmp_gather_stack.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Saved: {out_path}")

    # Quick validation
    print(f"  Figure size: {fig.get_size_inches()[0]:.1f}\u2033 "
          f"\u00d7 {fig.get_size_inches()[1]:.1f}\u2033")
    print(f"  Raw gather  range: [{gather_raw.min():.3f}, {gather_raw.max():.3f}]")
    print(f"  NMO gather  range: [{gather_nmo.min():.3f}, {gather_nmo.max():.3f}]")
    print(f"  Stack trace range: [{stacked.min():.3f}, {stacked.max():.3f}]")


if __name__ == "__main__":
    main()
