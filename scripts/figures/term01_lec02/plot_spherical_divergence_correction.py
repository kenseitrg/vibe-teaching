"""
Figure 02 for Term 1 Lecture 02: Spherical divergence correction.

Caption:
    Common-shot synthetic gather before (left) and after (right) applying
    a t^2 geometric-spreading correction.  Top panels show wiggle traces of
    the raw gather, whose amplitudes decay because of spherical spreading,
    and of the corrected gather, in which the deep reflections are restored
    to amplitudes comparable to the shallow ones.  Bottom panels plot the
    RMS amplitude of each gather as a function of time, making the decay
    and the compensation easy to see.

"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ---------------------------------------------------------------------------
# 1. Acquisition / model parameters (realistic near-surface numbers)
# ---------------------------------------------------------------------------
velocity = 2000.0          # m/s, near-surface / shallow-sediment velocity
offset_min = 0.0           # m
offset_max = 3000.0        # m
n_traces = 60              # number of traces in the shot gather
dt = 0.004                 # s, sample interval (4 ms)
t_max = 2.0                # s, maximum record time

# Reflector zero-offset two-way times (s) and reflection coefficients.
# Each reflector is shown as a short time band to give a clear hyperbola.
reflectors = [
    (0.20, 0.30),   # shallow reflection
    (0.60, 0.70),   # mid reflection
    (1.00, 1.10),   # deep reflection
]
reflector_amplitudes = [0.5, 0.4, 0.3]  # arbitrary reflection strengths

# Direct-wave parameters (linear arrival, first break)
direct_amplitude = 0.5

# Ricker wavelet
f_dom = 30.0               # Hz, dominant frequency

# ---------------------------------------------------------------------------
# 2. Helper functions
# ---------------------------------------------------------------------------
def ricker_wavelet(f, dt, t_len=None):
    """
    Return a zero-phase Ricker wavelet sampled at dt.
    f: dominant frequency (Hz)
    dt: sample interval (s)
    t_len: total wavelet length (s); default covers +/- 2.5 periods.
    """
    if t_len is None:
        t_len = 2.5 / f
    t = np.arange(-t_len / 2, t_len / 2 + dt, dt)
    # Avoid division by zero at t=0 by shifting tiny values
    t2 = t.copy()
    t2[np.isclose(t2, 0)] = 1e-12
    wavelet = (1.0 - 2.0 * (np.pi * f * t2) ** 2) * np.exp(
        -(np.pi * f * t2) ** 2
    )
    return t, wavelet


def hyperbolic_time(t0, offset, velocity):
    """Two-way reflection time for a horizontal reflector."""
    return np.sqrt(t0 ** 2 + (offset / velocity) ** 2)


def build_trace(offset, time_axis, wavelet, t_wave):
    """
    Build a single synthetic trace by adding a direct arrival and
    hyperbolic reflections, then applying a 1/t^2 spherical-divergence decay.

    The synthetic model uses a 1/t^2 amplitude decay because the standard
    deterministic correction shown in this lecture is the t^2 gain.  Using
    1/t^2 in the model makes the correction restore the original reflection
    amplitudes, which is the clearest way to illustrate the idea for students.
    A small time floor prevents the amplitude from diverging at t=0.
    """
    trace = np.zeros_like(time_axis)

    # Direct arrival (linear moveout, first break)
    t_direct = offset / velocity
    if t_direct < time_axis[-1]:
        trace += direct_amplitude * np.interp(
            time_axis, t_wave + t_direct, wavelet
        )

    # Reflected arrivals (hyperbolic moveout)
    for (t0_start, t0_end), amp in zip(reflectors, reflector_amplitudes):
        # Use the midpoint of the reflector band as the nominal t0
        t0 = 0.5 * (t0_start + t0_end)
        t_refl = hyperbolic_time(t0, offset, velocity)
        trace += amp * np.interp(time_axis, t_wave + t_refl, wavelet)

    # Geometric spreading / spherical divergence: amplitude ~ 1/t^2.
    # A time floor avoids the unphysical singularity at t=0 and keeps the
    # very early first breaks from completely dominating the display.
    t_floor = 0.3  # s
    t_safe = np.maximum(time_axis, t_floor)
    trace = trace / (t_safe ** 2)

    return trace


def apply_spherical_divergence_correction(trace, time_axis, power=2.0):
    """
    Apply a deterministic time-dependent gain of the form t^power.
    The same time floor used in the decay is applied here so that the
    correction is stable at early times and restores the original amplitudes.
    """
    t_floor = 0.3  # s, must match the decay floor
    t_safe = np.maximum(time_axis, t_floor)
    gain = t_safe ** power
    return trace * gain


def rms_amplitude(trace, window_samples):
    """Running RMS amplitude in a sliding window."""
    half = window_samples // 2
    out = np.full_like(trace, np.nan)
    n = len(trace)
    for i in range(n):
        left = max(0, i - half)
        right = min(n, i + half + 1)
        chunk = trace[left:right]
        out[i] = np.sqrt(np.mean(chunk ** 2))
    return out


def plot_wiggle_gather(ax, data, offsets, time_axis, trace_scale, title):
    """
    Plot a shot gather as wiggle traces.

    data: 2D array (n_times, n_traces)
    offsets: 1D array of offset values
    time_axis: 1D array of time values
    trace_scale: scale factor (offset units per amplitude unit) so that the
                 largest corrected wiggle fits inside one trace spacing.
    title: plot title
    """
    for j, x in enumerate(offsets):
        trace = data[:, j]
        x_wiggle = x + trace * trace_scale
        ax.plot(x_wiggle, time_axis, color="black", linewidth=0.6)
        ax.fill_betweenx(
            time_axis, x, x_wiggle, where=(trace >= 0), color="C0", alpha=0.7
        )

    margin = 0.05 * (offsets[-1] - offsets[0])
    ax.set_xlim(offsets[0] - margin, offsets[-1] + margin)
    ax.set_ylim(time_axis[-1], 0.0)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_xlabel("Offset (m)", fontsize=10)
    ax.set_ylabel("Time (s)", fontsize=10)


# ---------------------------------------------------------------------------
# 3. Build the synthetic shot gather
# ---------------------------------------------------------------------------
time_axis = np.arange(0.0, t_max + dt, dt)
offsets = np.linspace(offset_min, offset_max, n_traces)
t_wave, wavelet = ricker_wavelet(f_dom, dt)

raw_gather = np.zeros((len(time_axis), n_traces))
for j, off in enumerate(offsets):
    raw_gather[:, j] = build_trace(off, time_axis, wavelet, t_wave)

corrected_gather = np.zeros_like(raw_gather)
for j in range(n_traces):
    corrected_gather[:, j] = apply_spherical_divergence_correction(
        raw_gather[:, j], time_axis, power=2.0
    )

# ---------------------------------------------------------------------------
# 4. Compute RMS amplitude curves for the lower diagnostic panels
# ---------------------------------------------------------------------------
window_samples = int(0.05 / dt)  # 50 ms running window
raw_rms = np.mean(
    np.array([rms_amplitude(raw_gather[:, j], window_samples) for j in range(n_traces)]),
    axis=0,
)
corrected_rms = np.mean(
    np.array([rms_amplitude(corrected_gather[:, j], window_samples) for j in range(n_traces)]),
    axis=0,
)

# ---------------------------------------------------------------------------
# 5. Plotting
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(
    2, 2,
    figsize=(10, 7),
    gridspec_kw={"height_ratios": [2, 1]},
    constrained_layout=True,
)

# Choose a trace scale so that the largest corrected wiggle fills about
# 70% of one trace spacing.  The same scale is used for both panels so the
# amplitude comparison is honest: deep events are small in the raw gather and
# restored in the corrected gather.
trace_spacing = offsets[1] - offsets[0]
max_amp_corrected = np.max(np.abs(corrected_gather))
trace_scale = 0.5 * trace_spacing / max_amp_corrected

plot_wiggle_gather(
    axes[0, 0], raw_gather, offsets, time_axis, trace_scale,
    "Before correction (raw)"
)
plot_wiggle_gather(
    axes[0, 1], corrected_gather, offsets, time_axis, trace_scale,
    "After t$^2$ correction"
)

# Lower diagnostic panels: RMS amplitude vs time
axes[1, 0].plot(raw_rms, time_axis, color="C0", linewidth=2)
axes[1, 0].set_xlabel("Mean RMS amplitude", fontsize=10)
axes[1, 0].set_ylabel("Time (s)", fontsize=10)
axes[1, 0].set_ylim(time_axis[-1], 0.0)
axes[1, 0].set_title("Amplitude decay in raw gather", fontsize=11)
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot(corrected_rms, time_axis, color="C1", linewidth=2)
axes[1, 1].set_xlabel("Mean RMS amplitude", fontsize=10)
axes[1, 1].set_ylabel("Time (s)", fontsize=10)
axes[1, 1].set_ylim(time_axis[-1], 0.0)
axes[1, 1].set_title("Amplitude after t$^2$ gain", fontsize=11)
axes[1, 1].grid(True, alpha=0.3)

# ---------------------------------------------------------------------------
# 6. Save the figure
# ---------------------------------------------------------------------------
out = Path("figures/term01_lec02/term01_lec02_spherical_divergence_correction.png")
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
plt.close(fig)

print(f"Saved: {out.resolve()}")
print(
    "Figure 02: Common-shot synthetic gather before and after t^2 "
    "geometric-spreading correction, with RMS amplitude diagnostic panels."
)
