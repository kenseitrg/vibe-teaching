"""
Figure 04 for Term 1 Lecture 02: Surface-consistent amplitude correction (SCAC).

Illustrates how the four-factor surface-consistent amplitude model
    A_ij = S_i * R_j * G_k * M_l
separates source and receiver amplitude anomalies from the geological
amplitude trend (CMP-to-CMP variations and offset-dependent AVO decay).

Layout (3 rows x 3 columns):
  Row 0 — Before SCAC: CMP gathers corrupted by random source/receiver anomalies.
  Row 1 — After SCAC:  same gathers after median-based SCAC correction.
  Row 2 — RMS amplitude vs offset curves (before dashed, after solid).

Coloured vertical bands highlight traces sharing a common source (blue)
or common receiver (orange), showing how each trace carries both
imprints.  The RMS amplitude vs offset curves below confirm the
correction quality.

Parameters:
  Ricker wavelet 30 Hz, dt = 4 ms
  3 CMP locations with geology factors G = [1.0, 0.6, 1.4]
  20 sources and 20 receivers with log-uniform random factors (range 0.3-1.8)
  Offsets 25-1975 m, 40 traces per gather
  Three reflections at 0.30, 0.70, 1.10 s
  Mild AVO-like offset decay (M_l): 1.0 at near offset -> 0.6 at far offset
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path


# ===========================================================================
# 1. Acquisition and model parameters
# ===========================================================================
dt = 0.004                 # sample interval (s)
f_dom = 30.0               # Ricker wavelet dominant frequency (Hz)
t_max = 1.5                # record length (s)
t_display = 1.35           # y-axis display limit (s)

# Reflections: (t0 in s, RMS velocity in m/s, relative strength)
reflections = [
    (0.30, 1800, 1.00),    # shallow event
    (0.70, 2200, 0.50),    # mid event
    (1.10, 2600, 0.25),    # deep event
]

# CMP geology terms (G_k) — different base amplitude levels per CMP
G_factors = np.array([1.0, 0.6, 1.4])
cmp_labels = ["CMP 1", "CMP 2", "CMP 3"]
n_cmp = 3

# Offset sampling
n_traces = 40
offsets = np.linspace(25, 1975, n_traces)      # 40 offsets, 25-1975 m
trace_spacing = offsets[1] - offsets[0]          # 50 m

# Source and receiver surface-consistent factors
rng = np.random.default_rng(42)
n_sources = 20
n_receivers = 20

# Log-uniform distributions for realistic coupling variability
# Wider range (0.3-1.8) makes the amplitude anomalies clearly visible
# while staying physically plausible for a land survey
S_true = np.exp(rng.uniform(np.log(0.3), np.log(1.8), n_sources))
R_true = np.exp(rng.uniform(np.log(0.3), np.log(1.8), n_receivers))

# Offset-dependent amplitude decay (M_l) — gentle decay from 1.0 to 0.6
M_factors = 1.0 - 0.4 * (offsets / offsets[-1])


# ===========================================================================
# 2. Helper functions
# ===========================================================================
def ricker_wavelet(f, dt, length=0.20):
    """
    Return a zero-phase Ricker wavelet and its time axis.

    Parameters
    ----------
    f : float
        Dominant frequency (Hz).
    dt : float
        Sample interval (s).
    length : float
        Total length of the wavelet (s).

    Returns
    -------
    t : ndarray
        Time axis for the wavelet.
    w : ndarray
        Wavelet amplitudes (peak-normalised).
    """
    t = np.arange(-length / 2, length / 2 + dt / 2, dt)
    t2 = t.copy()
    t2[np.isclose(t2, 0)] = 1e-12
    w = (1.0 - 2.0 * (np.pi * f * t2) ** 2) * np.exp(-(np.pi * f * t2) ** 2)
    return t / np.max(np.abs(w)), w / np.max(np.abs(w))


def nmo_time(t0, x, v_rms):
    """Two-way travel time with normal moveout for offset x."""
    return np.sqrt(t0 ** 2 + (x / v_rms) ** 2)


def source_index(cmp_k, trace_i):
    """Return source index for a given CMP and trace number (balanced design).

    Each source appears exactly twice per CMP gather, giving 6 traces
    per source across the 3 CMPs.  This balanced sampling lets the
    median-based SCAC estimation recover the factors accurately.
    """
    return (trace_i // 2 + cmp_k * 8) % n_sources


def receiver_index(cmp_k, trace_i):
    """Return receiver index for a given CMP and trace number.

    Each receiver appears exactly twice per CMP gather, giving 6 traces
    per receiver across the 3 CMPs.
    """
    return (trace_i + cmp_k * 5) % n_receivers


# ===========================================================================
# 3. Build synthetic CMP gathers
# ===========================================================================
time_axis = np.arange(0, t_max, dt)
n_samples = len(time_axis)

# Ricker wavelet (normalised to unit peak amplitude)
t_wave, wavelet = ricker_wavelet(f_dom, dt)

# Storage arrays
before = np.zeros((n_cmp, n_traces, n_samples))   # before SCAC
after = np.zeros((n_cmp, n_traces, n_samples))    # after SCAC
src_idx = np.zeros((n_cmp, n_traces), dtype=int)
rec_idx = np.zeros((n_cmp, n_traces), dtype=int)

for k in range(n_cmp):
    for i in range(n_traces):
        s_idx = source_index(k, i)
        r_idx = receiver_index(k, i)
        src_idx[k, i] = s_idx
        rec_idx[k, i] = r_idx

        x = offsets[i]
        # Geological trend: CMP factor * offset decay
        geo_factor = G_factors[k] * M_factors[i]

        # Build the reflection sequence for this trace
        trace = np.zeros(n_samples)
        for t0, v, strength in reflections:
            t_nmo = nmo_time(t0, x, v)
            if t_nmo >= t_max:
                continue
            trace += strength * geo_factor * np.interp(
                time_axis, t_wave + t_nmo, wavelet
            )

        # Apply surface-consistent source and receiver anomalies
        trace *= S_true[s_idx] * R_true[r_idx]

        # Add a small amount of random noise
        noise_std = 0.003
        trace += rng.normal(0, noise_std, n_samples)

        before[k, i, :] = trace


# ===========================================================================
# 4. SCAC estimation via median-based Gauss-Seidel in log space
# ===========================================================================
# The four-factor model is multiplicative:  RMS = S_i * R_j * G_k * M_l
# In log space this becomes additive, and we solve iteratively using
# the median to reject outliers.  This is the standard Gauss-Seidel
# approach used in production SCAC codes, but with medians instead of means.

# Flatten the RMS data into a single vector for easy indexing
n_total = n_cmp * n_traces
rms_flat = np.array([
    np.sqrt(np.mean(before[k, i, :] ** 2))
    for k in range(n_cmp) for i in range(n_traces)
])
logA = np.log(rms_flat)

# Index arrays (flat): which source, receiver, CMP, offset for each trace
src_flat = src_idx.flatten()
rec_flat = rec_idx.flatten()
cmp_flat = np.repeat(np.arange(n_cmp), n_traces)
off_flat = np.tile(np.arange(n_traces), n_cmp)

# Initialise all factors to zero in log space
logS = np.zeros(n_sources)
logR = np.zeros(n_receivers)
logG = np.zeros(n_cmp)
logM = np.zeros(n_traces)

# Gauss-Seidel iteration: update each factor using the current estimates
# of the other factors, then centre to remove the mean ambiguity.
for iteration in range(8):
    # --- Update source terms ---
    for s in range(n_sources):
        mask = (src_flat == s)
        residual = logA[mask] - logR[rec_flat[mask]] - logG[cmp_flat[mask]] - logM[off_flat[mask]]
        logS[s] = np.median(residual)
    logS -= np.mean(logS)               # centre to remove overall scale ambiguity

    # --- Update receiver terms ---
    for r in range(n_receivers):
        mask = (rec_flat == r)
        residual = logA[mask] - logS[src_flat[mask]] - logG[cmp_flat[mask]] - logM[off_flat[mask]]
        logR[r] = np.median(residual)
    logR -= np.mean(logR)

    # --- Update CMP (geology) terms ---
    for k in range(n_cmp):
        mask = (cmp_flat == k)
        residual = logA[mask] - logS[src_flat[mask]] - logR[rec_flat[mask]] - logM[off_flat[mask]]
        logG[k] = np.median(residual)
    logG -= np.mean(logG)

    # --- Update offset terms ---
    for l in range(n_traces):
        mask = (off_flat == l)
        residual = logA[mask] - logS[src_flat[mask]] - logR[rec_flat[mask]] - logG[cmp_flat[mask]]
        logM[l] = np.median(residual)
    logM -= np.mean(logM)

# Convert back to linear space
S_est = np.exp(logS)
R_est = np.exp(logR)
G_est = np.exp(logG)
M_est = np.exp(logM)

# Corrected gathers: divide out estimated source and receiver factors only,
# preserving the geological trend (G_k * M_l)
for k in range(n_cmp):
    for i in range(n_traces):
        s = src_idx[k, i]
        r = rec_idx[k, i]
        after[k, i, :] = before[k, i, :] / (S_est[s] * R_est[r])

# Print diagnostic information
print("=" * 60)
print("SCAC estimation diagnostics")
print("=" * 60)
print(f"True S range: {S_true.min():.3f} .. {S_true.max():.3f}")
print(f"Est  S range: {S_est.min():.3f} .. {S_est.max():.3f}")
print(f"S correlation: {np.corrcoef(S_true, S_est)[0, 1]:.3f}")
print(f"\nTrue R range: {R_true.min():.3f} .. {R_true.max():.3f}")
print(f"Est  R range: {R_est.min():.3f} .. {R_est.max():.3f}")
print(f"R correlation: {np.corrcoef(R_true, R_est)[0, 1]:.3f}")
print(f"\nEstimated G: {np.round(G_est, 3)}  (true: {G_factors})")
print(f"Correction S_est * R_est restores the geological G_k * M_l trend.")


# ===========================================================================
# 5. Plotting helper: wiggle display with positive fill
# ===========================================================================
def plot_wiggle_gather(ax, traces, offsets, time, scale, title,
                       fill_color="#56B4E9", line_color="black",
                       linewidth=0.4, time_limits=(0, t_display)):
    """
    Plot a CMP gather as wiggle traces with positive-amplitude fill.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
    traces : ndarray (n_traces, n_samples)
    offsets : ndarray (n_traces,)
    time : ndarray (n_samples,)
    scale : float
        Amplitude scaling factor (offset units per amplitude unit).
        Same scale ensures before/after panels are directly comparable.
    title : str
        Panel title.
    fill_color : str
        Color for positive-amplitude fill.
    line_color : str
        Color for wiggle lines.
    """
    # Select time range for display
    t_min, t_max_disp = time_limits
    idx_start = np.searchsorted(time, t_min)
    idx_end = np.searchsorted(time, t_max_disp)
    t_disp = time[idx_start:idx_end]
    traces_disp = traces[:, idx_start:idx_end]

    for i in range(len(offsets)):
        x_center = offsets[i]
        disp = x_center + traces_disp[i, :] * scale
        ax.plot(disp, t_disp, color=line_color, linewidth=linewidth)
        ax.fill_betweenx(
            t_disp, x_center, disp,
            where=(disp > x_center),
            color=fill_color, alpha=0.55, linewidth=0,
        )

    margin = 0.03 * (offsets[-1] - offsets[0])
    ax.set_xlim(offsets[0] - margin, offsets[-1] + margin)
    ax.set_ylim(t_max_disp, t_min)                # time increasing downward
    ax.set_title(title, fontsize=10, fontweight="bold", pad=6)
    ax.set_xlabel("Offset (m)", fontsize=8)
    ax.set_ylabel("Time (s)", fontsize=8)


def add_rms_overlay(ax, traces, offsets, time, y_anchor=1.28,
                    color="#D55E00", linewidth=2.5, max_width=350):
    """
    Overlay a thick RMS-amplitude curve on a wiggle gather panel.

    Draws a continuous red line whose horizontal deviation from each trace
    position is proportional to the trace's RMS amplitude.  Small vertical
    ticks connect the curve to the trace positions for visual clarity.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
    traces : ndarray (n_traces, n_samples)
    offsets : ndarray (n_traces,)
    time : ndarray (n_samples,) — used for display limit checks
    y_anchor : float
        Fixed y-position for the RMS curve (s).
    color : str
        Line color.
    linewidth : float
        Line width.
    max_width : float
        Maximum horizontal extent of the RMS curve (m).
    """
    rms = np.array([np.sqrt(np.mean(traces[i, :] ** 2)) for i in range(len(offsets))])
    rms_norm = rms / np.max(rms) * max_width
    x_curve = offsets + rms_norm

    # Thick red curve showing RMS amplitude vs offset
    ax.plot(x_curve, np.full(len(offsets), y_anchor),
            color=color, linewidth=linewidth, alpha=0.85, zorder=5)

    # Subtle vertical ticks at each trace centre
    ax.vlines(x_curve, y_anchor - 0.012, y_anchor + 0.012,
              colors=color, linewidths=0.7, alpha=0.4, zorder=4)

    # Label for the RMS curve
    ax.text(offsets[-1] + max_width * 0.1, y_anchor, "RMS",
            fontsize=7, color=color, fontweight="bold", va="center", zorder=6)


def highlight_traces(ax, offsets, trace_indices, color, alpha=0.25, width_frac=0.8):
    """
    Draw semi-transparent vertical bands behind specified traces.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
    offsets : ndarray
        Offset positions of all traces.
    trace_indices : array-like
        Indices of traces to highlight.
    color : str
        Color for the highlight bands.
    alpha : float
        Transparency level.
    width_frac : float
        Fraction of trace spacing used for band width.
    """
    trace_spacing = offsets[1] - offsets[0]
    half_width = trace_spacing * width_frac / 2
    for i in trace_indices:
        ax.axvspan(offsets[i] - half_width, offsets[i] + half_width,
                   color=color, alpha=alpha, zorder=1)


# ===========================================================================
# 6. Create the 3 x 3 figure
# ===========================================================================
fig, axes = plt.subplots(
    3, 3, figsize=(12, 10),
    gridspec_kw={"height_ratios": [2, 2, 1.3]},
    constrained_layout=True,
)

# Colorblind-friendly CMP palette (Wong 2011)
cmp_colors = ["#0072B2", "#D55E00", "#009E73"]   # blue, vermillion, green

# -----------------------------------------------------------------------
# Compute a common amplitude scale per CMP for fair before/after comparison
# -----------------------------------------------------------------------
scales = np.zeros(n_cmp)
for k in range(n_cmp):
    combined = np.concatenate([before[k].ravel(), after[k].ravel()])
    p95 = np.percentile(np.abs(combined), 95)
    scales[k] = 0.75 * trace_spacing / p95 if p95 > 0 else 1.0
    print(f"CMP {k+1}: p95 = {p95:.4f}, scale = {scales[k]:.1f}")

# -----------------------------------------------------------------------
# Row 0 — Before SCAC (wiggle gathers with erratic amplitudes)
# -----------------------------------------------------------------------
for k in range(n_cmp):
    ax = axes[0, k]
    # Highlight common-source and common-receiver traces behind the wiggles
    src_traces = np.where(src_idx[k] == 1)[0]
    rec_traces = np.where(rec_idx[k] == 1)[0]
    highlight_traces(ax, offsets, src_traces, "#56B4E9", alpha=0.25)
    highlight_traces(ax, offsets, rec_traces, "#E69F00", alpha=0.25)
    plot_wiggle_gather(ax, before[k], offsets, time_axis, scales[k],
                       f"{cmp_labels[k]} — Before")

# -----------------------------------------------------------------------
# Row 1 — After SCAC (same gathers, anomalies suppressed)
# -----------------------------------------------------------------------
for k in range(n_cmp):
    ax = axes[1, k]
    # Highlight common-source and common-receiver traces behind the wiggles
    src_traces = np.where(src_idx[k] == 1)[0]
    rec_traces = np.where(rec_idx[k] == 1)[0]
    highlight_traces(ax, offsets, src_traces, "#56B4E9", alpha=0.25)
    highlight_traces(ax, offsets, rec_traces, "#E69F00", alpha=0.25)
    plot_wiggle_gather(ax, after[k], offsets, time_axis, scales[k],
                       f"{cmp_labels[k]} — After",
                       fill_color="#009E73")

# -----------------------------------------------------------------------
# Row 2 — RMS amplitude vs offset curves
# -----------------------------------------------------------------------
for k in range(n_cmp):
    ax = axes[2, k]

    rms_before_k = np.array([
        np.sqrt(np.mean(before[k, i, :] ** 2)) for i in range(n_traces)
    ])
    rms_after_k = np.array([
        np.sqrt(np.mean(after[k, i, :] ** 2)) for i in range(n_traces)
    ])

    # Before: dashed, lighter
    ax.plot(offsets, rms_before_k, linestyle="--", linewidth=1.3,
            color=cmp_colors[k], alpha=0.5,
            label="Before correction")
    # After: solid, full colour
    ax.plot(offsets, rms_after_k, linestyle="-", linewidth=2.0,
            color=cmp_colors[k],
            label="After correction")

    ax.set_title(cmp_labels[k], fontsize=10, fontweight="bold", pad=6)
    ax.set_xlabel("Offset (m)", fontsize=8)
    ax.set_ylabel("RMS Amplitude", fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7, loc="upper right")

# -----------------------------------------------------------------------
# Figure title
# -----------------------------------------------------------------------
fig.suptitle(
    "Surface-consistent amplitude correction",
    fontsize=13,
    fontweight="bold",
    y=0.99,
)

# -----------------------------------------------------------------------
# Legend for trace highlighting
# -----------------------------------------------------------------------
legend_patches = [
    mpatches.Patch(color="#56B4E9", alpha=0.4, label="Common source"),
    mpatches.Patch(color="#E69F00", alpha=0.4, label="Common receiver"),
]
fig.legend(handles=legend_patches, loc="lower center", ncol=2,
           fontsize=9, title="Highlighted traces", title_fontsize=10,
           framealpha=0.9)

# -----------------------------------------------------------------------
# 7. Save the figure
# -----------------------------------------------------------------------
out = Path("figures/term01_lec02/term01_lec02_surface_consistent_amplitude.png")
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
plt.close(fig)

print(f"\nSaved: {out.resolve()}")
print(
    "Figure 04: Surface-consistent amplitude correction. "
    "Top row: CMP gathers with erratic source/receiver amplitude anomalies. "
    "Middle row: same gathers after median-based SCAC correction — the "
    "anomalies are suppressed and the smooth AVO trend is restored. "
    "Bottom row: RMS amplitude vs offset curves (dashed = before, "
    "solid = after).  Coloured vertical bands highlight traces sharing a "
    "common source (blue) or common receiver (orange)."
)
