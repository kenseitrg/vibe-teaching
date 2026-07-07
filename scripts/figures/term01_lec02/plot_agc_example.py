"""
Figure 03 for Term 1 Lecture 02: Automatic Gain Control (AGC) and the
effect of window length.

Caption:
    Synthetic seismic trace built from a 30 Hz Ricker wavelet with three
    arrivals whose amplitudes decay with time.  The first panel shows the
    original trace and its envelope; the next four panels show the same
    trace after AGC with increasing window lengths (1 sample, ~one period,
    ~500 ms, and the whole trace).  The last panel overlays the
    four gain functions, illustrating that a short window flattens the
    envelope almost completely while a long window preserves the original
    trace shape and only changes the overall amplitude level.

Pedagogical note:
    AGC is a time-varying gain.  A short window equalizes everything it sees,
    erasing true amplitude differences, which is useful for display but not
    for amplitude-sensitive work such as AVO.  A long window keeps the
    original shape, making AGC behave more like a single scalar gain.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert
from pathlib import Path


# ---------------------------------------------------------------------------
# 1. Acquisition / model parameters
# ---------------------------------------------------------------------------
dt = 0.004            # s, sample interval (4 ms)
f_dom = 30.0          # Hz, dominant frequency of the Ricker wavelet
t_max = 1.5           # s, record length
noise_std = 0.001     # small random noise level

# Arrival times (s) and reflection coefficients (dimensionless).
# The deeper arrivals are deliberately weaker so that the raw trace shows a
# clear amplitude decay with time.
reflections = [
    (0.20, 1.00),    # strong shallow reflection
    (0.60, 0.35),    # weaker mid reflection
    (1.00, 0.12),    # even weaker deep reflection
]

# ---------------------------------------------------------------------------
# 2. Helper functions
# ---------------------------------------------------------------------------
def ricker_wavelet(f, dt, length=0.20):
    """
    Return a zero-phase Ricker wavelet and its time axis.

    f:      dominant frequency (Hz)
    dt:     sample interval (s)
    length: total length of the wavelet (s)
    """
    t = np.arange(-length / 2, length / 2 + dt / 2, dt)
    t2 = t.copy()
    t2[np.isclose(t2, 0)] = 1e-12
    wavelet = (1.0 - 2.0 * (np.pi * f * t2) ** 2) * np.exp(
        -(np.pi * f * t2) ** 2
    )
    return t, wavelet


def apply_agc(trace, window_samples, epsilon_factor=0.005):
    """
    Apply AGC using a sliding RMS window.

    The gain is the reciprocal of the local RMS amplitude, computed in a
    centered window of length `window_samples`.  To avoid a jagged-looking gain,
    the gain is evaluated at window centers spaced by half the window and then
    linearly interpolated to every sample.

    A small stabilization constant (epsilon) is added to prevent division by
    zero where the amplitude is very small.
    """
    n = len(trace)
    eps = epsilon_factor * np.max(np.abs(trace))

    # Make sure the window is odd and at least one sample long.
    if window_samples % 2 == 0:
        window_samples += 1
    half = window_samples // 2

    # 1. Running RMS amplitude in the centered window.
    rms = np.zeros(n)
    for i in range(n):
        left = max(0, i - half)
        right = min(n, i + half + 1)
        rms[i] = np.sqrt(np.mean(trace[left:right] ** 2))

    # 2. Evaluate gain at window centers and interpolate smoothly.
    if window_samples == 1:
        # The "window" is a single sample, so the RMS is just |trace|.
        centers = np.arange(n)
        gain_centers = 1.0 / (np.abs(trace[centers]) + eps)
    else:
        step = max(1, half)          # update roughly every half window
        centers = np.arange(0, n, step)
        if centers[-1] != n - 1:
            centers = np.append(centers, n - 1)
        gain_centers = 1.0 / (rms[centers] + eps)

    gain = np.interp(np.arange(n).astype(float), centers.astype(float), gain_centers)

    # 3. Apply the gain and return both the scaled trace and the gain function.
    return trace * gain, gain


def plot_trace_and_envelope(ax, time, trace, envelope, color, title, ylim):
    """
    Plot a trace (time on x-axis, amplitude on y-axis) and its analytic
    envelope on a given axis.  Time runs left to right, amplitude up/down.
    """
    ax.plot(time, trace, color=color, linewidth=1.0, label="Trace")
    ax.fill_between(time, -envelope, envelope, alpha=0.2, color=color, label="Envelope")

    ax.set_xlim(time[0], time[-1])
    ax.set_ylim(ylim)
    ax.set_title(title, fontsize=9, fontweight="bold")
    ax.set_xlabel("Time (s)", fontsize=8)
    ax.set_ylabel("Amplitude", fontsize=8)
    ax.grid(True, alpha=0.3)


# ---------------------------------------------------------------------------
# 3. Build the synthetic trace
# ---------------------------------------------------------------------------
rng = np.random.default_rng(42)
time_axis = np.arange(0.0, t_max + dt / 2, dt)

# Start with the Ricker wavelet and add the reflections.
t_wave, wavelet = ricker_wavelet(f_dom, dt)
trace = np.zeros_like(time_axis)
for t0, amp in reflections:
    trace += amp * np.interp(time_axis, t_wave + t0, wavelet)

# Add a gentle exponential decay with time to mimic spherical spreading /
# absorption, then add a small amount of random noise.
trace *= np.exp(-0.5 * time_axis)
trace += rng.normal(0.0, noise_std, size=time_axis.shape)

# Analytic envelope of the original trace.
envelope = np.abs(hilbert(trace))

# ---------------------------------------------------------------------------
# 4. Define the AGC windows and apply them
# ---------------------------------------------------------------------------
# Window lengths in seconds and in samples.
period = 1.0 / f_dom                         # dominant period of the Ricker
windows = [
    ("1 sample", 1),
    ("~3 periods", max(1, int(round(3 * period / dt)))),
    ("~500 ms", int(round(0.500 / dt))),  # about 500 ms (125 samples), covers multiple reflections
    ("whole trace", len(time_axis)),
]

# Colorblind-friendly palette.  Each AGC window gets a unique color that is
# reused in the gain-function overlay.
colors = {
    "1 sample": "#D55E00",      # orange-red
    "~3 periods": "#E69F00",     # orange
    "~500 ms": "#009E73",       # green
    "whole trace": "#0072B2",   # blue
}
original_color = "#333333"     # dark grey

agc_results = []
for label, n_samples in windows:
    if label == "whole trace":
        # For the whole-trace window, use a constant gain derived from the
        # RMS of the entire trace.  This cleanly illustrates that a full-length
        # window simply scales the trace by one scalar value, preserving all
        # relative amplitude relationships.
        eps = 0.005 * np.max(np.abs(trace))
        rms_whole = np.sqrt(np.mean(trace ** 2))
        gain_const = 1.0 / (rms_whole + eps)
        out = trace * gain_const
        gain = np.full_like(trace, gain_const)
    else:
        out, gain = apply_agc(trace, n_samples)
    out_envelope = np.abs(hilbert(out))
    agc_results.append((label, n_samples, out, out_envelope, gain, colors[label]))

# ---------------------------------------------------------------------------
# 5. Plotting
# ---------------------------------------------------------------------------
fig, ax_grid = plt.subplots(3, 2, figsize=(10, 9), constrained_layout=True)
axes = ax_grid.flatten()
fig.suptitle(
    "Automatic Gain Control (AGC): effect of window length",
    fontsize=12,
    fontweight="bold",
    y=0.98,
)

# Per-panel y-limits so each trace fills its panel vertically.
def _ylim(t):
    ymax = 1.3 * np.max(np.abs(t))
    return (-ymax, ymax)

# Row 0: original trace + envelope.
plot_trace_and_envelope(
    axes[0], time_axis, trace, envelope, original_color,
    "Original trace + envelope", _ylim(trace),
)
axes[0].legend(loc="upper right", fontsize=8)

# Rows 1–4: the four AGC windows (1 sample, ~3 periods, ~500 ms, whole trace).
for idx, (label, n_samples, out, out_env, gain, color) in enumerate(agc_results, start=1):
    window_ms = n_samples * dt * 1000
    sample_text = "1 sample" if n_samples == 1 else f"{n_samples} samples"
    title = f"AGC, {label}\n{sample_text} ({window_ms:.0f} ms)"
    plot_trace_and_envelope(
        axes[idx], time_axis, out, out_env, color, title, _ylim(out),
    )

# Row 5: gain functions (time on x-axis, gain on y-axis, linear scale).
ax_gain = axes[5]
for label, n_samples, out, out_env, gain, color in agc_results:
    sample_text = "1 sample" if n_samples == 1 else f"{n_samples} samples"
    ax_gain.plot(time_axis, gain, color=color, linewidth=1.5, label=f"{label} ({sample_text})")

ax_gain.set_xlim(0, t_max)
ax_gain.set_xlabel("Time (s)", fontsize=9)
ax_gain.set_ylabel("Gain", fontsize=9)
ax_gain.set_title("AGC gain functions", fontsize=10, fontweight="bold")
ax_gain.legend(loc="lower right", fontsize=8)
ax_gain.grid(True, alpha=0.3)

# ---------------------------------------------------------------------------
# 6. Save the figure
# ---------------------------------------------------------------------------
out = Path("figures/term01_lec02/term01_lec02_agc_example.png")
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=150, bbox_inches="tight")
plt.close(fig)

print(f"Saved: {out.resolve()}")
print(
    "Figure 03: AGC window-length trade-off.  Short windows (1 sample, one period) "
    "flatten the envelope and erase true amplitude differences; a long window "
    "(whole trace) preserves the original trace shape and only scales the overall "
    "RMS level."
)
