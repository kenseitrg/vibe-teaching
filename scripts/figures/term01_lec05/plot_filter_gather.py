"""
Band-pass filtering of a synthetic CMP gather.

Shows a CMP gather contaminated by low-frequency ground roll noise
(top row) and the same gather after a 15-60 Hz band-pass filter
(bottom row).  Left column: time-domain gathers (variable-density).
Right column: average amplitude spectra (dB) with the filter passband
shaded in green.

Caption (to match lecture notes): "Band-pass filtering of a synthetic
CMP gather. Left: gather with low-frequency noise (ground roll).
Right: after filtering, the reflection events are visible while the
low-frequency noise is suppressed."

Seismic parameters are chosen to be realistic for a shallow-medium
crustal setting.
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# ──────────────────────────────────────────────────────────────────
# Figure settings
# ──────────────────────────────────────────────────────────────────
FIG_WIDTH = 12.0
FIG_HEIGHT = 8.0
DPI = 150
OUTPUT_PATH = "figures/term01_lec05/term01_lec05_filter_gather.png"

# ──────────────────────────────────────────────────────────────────
# Acquisition / sampling parameters
# ──────────────────────────────────────────────────────────────────
DT = 0.004            # sample interval, seconds (4 ms)
T_MAX = 2.0           # record length, seconds
N_SAMPLES = int(T_MAX / DT)  # 500 samples
FS = 1.0 / DT         # 250 Hz
F_N = FS / 2.0        # 125 Hz Nyquist

N_TRACES = 24
OFFSET_MIN = 100.0    # near offset, m
OFFSET_MAX = 2500.0   # far offset, m
offsets = np.linspace(OFFSET_MIN, OFFSET_MAX, N_TRACES)

# ──────────────────────────────────────────────────────────────────
# Reflection events: (t0, V_rms, amplitude)
# ──────────────────────────────────────────────────────────────────
EVENTS = [
    {"t0": 0.4, "vrms": 1800.0, "amp": 1.0},
    {"t0": 0.8, "vrms": 2200.0, "amp": 0.7},
    {"t0": 1.3, "vrms": 2600.0, "amp": 0.5},
]

REFLECTION_F0 = 30.0  # Ricker peak frequency for reflections, Hz

# ──────────────────────────────────────────────────────────────────
# Ground-roll (noise) parameters
# ──────────────────────────────────────────────────────────────────
GR_F0 = 5.0           # Ricker peak frequency for ground roll, Hz
GR_V_APP = 500.0      # apparent velocity of ground roll, m/s
GR_AMP = 0.6          # amplitude (relative to strongest reflection)
RANDOM_NOISE_AMP = 0.05  # small random noise (relative to strongest reflection)

# ──────────────────────────────────────────────────────────────────
# Filter parameters
# ──────────────────────────────────────────────────────────────────
FILTER_ORDER = 4
FILTER_LO = 15.0      # low-cut, Hz
FILTER_HI = 60.0      # high-cut, Hz


# ──────────────────────────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────────────────────────

def ricker_wavelet(f0, dt, duration=0.256):
    """Return a Ricker wavelet centred at t = 0.

    Parameters
    ----------
    f0 : float  – peak frequency (Hz)
    dt : float  – sample interval (s)
    duration : float – total wavelet length (s), made symmetric
    """
    t = np.arange(-duration / 2, duration / 2 + dt, dt)
    # Ricker wavelet: second derivative of a Gaussian
    t_mid = duration / 2
    tau = (1 - 2 * (np.pi * f0 * (t - t_mid)) ** 2) * \
          np.exp(-(np.pi * f0 * (t - t_mid)) ** 2)
    return t, tau


def hyperbolic_moveout(t0, vrms, offsets):
    """Compute NMO traveltime for each offset.

    Returns an array of traveltimes (one per offset).
    """
    return np.sqrt(t0 ** 2 + (offsets / vrms) ** 2)


def make_synthetic_gather():
    """Build a synthetic CMP gather with reflections + ground roll.

    Returns
    -------
    gather : ndarray, shape (N_SAMPLES, N_TRACES)
        The synthetic gather (time along axis 0, trace index along axis 1).
    time : ndarray, shape (N_SAMPLES,)
        Time axis in seconds.
    """
    time = np.arange(N_SAMPLES) * DT
    gather = np.zeros((N_SAMPLES, N_TRACES))

    # --- Reflections ---
    t_wav, wavelet = ricker_wavelet(REFLECTION_F0, DT)
    for event in EVENTS:
        t0 = event["t0"]
        vrms = event["vrms"]
        amp = event["amp"]
        traveltimes = hyperbolic_moveout(t0, vrms, offsets)

        for j in range(N_TRACES):
            # Find the sample closest to the hyperbolic traveltime
            idx = int(round(traveltimes[j] / DT))
            if 0 <= idx < N_SAMPLES:
                # Place the wavelet centred on that traveltime
                wav_start = idx - len(wavelet) // 2
                wav_end = wav_start + len(wavelet)
                if wav_start >= 0 and wav_end <= N_SAMPLES:
                    gather[wav_start:wav_end, j] += amp * wavelet

    # --- Ground roll (linear moveout, low-frequency) ---
    t_gr, gr_wavelet = ricker_wavelet(GR_F0, DT)
    for j in range(N_TRACES):
        x = offsets[j]
        t_arrival = x / GR_V_APP  # linear traveltime
        if t_arrival >= T_MAX:
            continue
        idx = int(round(t_arrival / DT))
        wav_start = idx - len(gr_wavelet) // 2
        wav_end = wav_start + len(gr_wavelet)
        if wav_start >= 0 and wav_end <= N_SAMPLES:
            # Ground roll amplitude decreases with offset (geometric spreading)
            # and is stronger at near offsets
            amp_factor = GR_AMP * (OFFSET_MAX / max(x, 1.0)) ** 0.5
            gather[wav_start:wav_end, j] += amp_factor * gr_wavelet

    # --- Small random noise ---
    np.random.seed(42)  # reproducible noise
    gather += RANDOM_NOISE_AMP * np.random.randn(N_SAMPLES, N_TRACES)

    return gather, time


def apply_bandpass(gather, lo, hi, order, fs):
    """Apply a Butterworth band-pass filter along each trace (axis 0).

    Uses zero-phase filtering (filtfilt) to avoid phase distortion.
    """
    nyquist = fs / 2.0
    b, a = signal.butter(order, [lo / nyquist, hi / nyquist], btype="band")
    filtered = np.zeros_like(gather)
    for j in range(gather.shape[1]):
        filtered[:, j] = signal.filtfilt(b, a, gather[:, j])
    return filtered


def amplitude_spectrum_dB(gather, fs):
    """Compute the average amplitude spectrum of a gather (in dB).

    Returns
    -------
    freq : 1-D array – frequency axis (Hz)
    avg_dB : 1-D array – average amplitude spectrum (dB re peak)
    """
    n_samples = gather.shape[0]
    nfft = 2 ** int(np.ceil(np.log2(n_samples)))  # next power of 2

    spectra = np.abs(np.fft.rfft(gather, n=nfft, axis=0))
    avg = spectra.mean(axis=1)
    freq = np.fft.rfftfreq(nfft, d=1.0 / fs)

    # Convert to dB (relative to peak)
    avg_max = avg.max()
    if avg_max > 0:
        avg_dB = 20.0 * np.log10(avg / avg_max)
    else:
        avg_dB = np.full_like(avg, -80.0)

    return freq, avg_dB


# ──────────────────────────────────────────────────────────────────
# Build the gather and apply filtering
# ──────────────────────────────────────────────────────────────────
gather, time = make_synthetic_gather()
filtered = apply_bandpass(gather, FILTER_LO, FILTER_HI, FILTER_ORDER, FS)

# Amplitude spectra
freq_orig, spec_orig = amplitude_spectrum_dB(gather, FS)
freq_filt, spec_filt = amplitude_spectrum_dB(filtered, FS)

# ──────────────────────────────────────────────────────────────────
# Plotting
# ──────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(FIG_WIDTH, FIG_HEIGHT),
                         gridspec_kw={"hspace": 0.40, "wspace": 0.35})

# Colour map for variable-density display
cmap = "RdBu"

# Shared color limits for the two gathers (brighter display)
vmax = np.max(np.abs(gather)) * 0.3
vmin = -vmax

# ---- Top-left: original gather ----
ax = axes[0, 0]
ax.imshow(gather, aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax,
          extent=[0, N_TRACES - 1, T_MAX, 0])
ax.set_xlabel("Trace index")
ax.set_ylabel("Time (s)")
ax.set_title("(a) Original CMP gather", fontsize=10, pad=8)
# Mark offsets on secondary x-axis (top)
ax2 = ax.secondary_xaxis("top")
ax2.set_xticks([0, N_TRACES // 2, N_TRACES - 1])
ax2.set_xticklabels([f"{int(OFFSET_MIN)}", f"{int(offsets[N_TRACES//2])}",
                      f"{int(OFFSET_MAX)}"])

# ---- Top-right: original spectrum ----
ax = axes[0, 1]
ax.plot(freq_orig, spec_orig, color="#0072B2", linewidth=1.5)
ax.axvspan(FILTER_LO, FILTER_HI, color="#009E73", alpha=0.18, zorder=0,
           label=f"Passband {FILTER_LO}–{FILTER_HI} Hz")
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Amplitude (dB)")
ax.set_title("(b) Average amplitude spectrum", fontsize=10, pad=8)
ax.set_xlim(0, F_N)
ax.set_ylim(-80, 5)
ax.grid(True, linestyle=":", alpha=0.5)
ax.legend(loc="lower right", fontsize=9)

# ---- Bottom-left: filtered gather ----
ax = axes[1, 0]
ax.imshow(filtered, aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax,
          extent=[0, N_TRACES - 1, T_MAX, 0])
ax.set_xlabel("Trace index")
ax.set_ylabel("Time (s)")
ax.set_title(f"(c) After band-pass filter ({FILTER_LO}–{FILTER_HI} Hz)",
             fontsize=10, pad=8)
ax2 = ax.secondary_xaxis("top")
ax2.set_xticks([0, N_TRACES // 2, N_TRACES - 1])
ax2.set_xticklabels([f"{int(OFFSET_MIN)}", f"{int(offsets[N_TRACES//2])}",
                      f"{int(OFFSET_MAX)}"])

# ---- Bottom-right: filtered spectrum ----
ax = axes[1, 1]
ax.plot(freq_filt, spec_filt, color="#D55E00", linewidth=1.5)
ax.axvspan(FILTER_LO, FILTER_HI, color="#009E73", alpha=0.18, zorder=0,
           label=f"Passband {FILTER_LO}–{FILTER_HI} Hz")
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Amplitude (dB)")
ax.set_title("(d) Average amplitude spectrum", fontsize=10, pad=8)
ax.set_xlim(0, F_N)
ax.set_ylim(-80, 5)
ax.grid(True, linestyle=":", alpha=0.5)
ax.legend(loc="lower right", fontsize=9)

fig.suptitle("Band-pass filtering of a synthetic CMP gather", fontsize=13,
             fontweight="bold", y=1.01)

plt.savefig(OUTPUT_PATH, dpi=DPI, bbox_inches="tight")
plt.close()

# ──────────────────────────────────────────────────────────────────
# Diagnostic output
# ──────────────────────────────────────────────────────────────────
print(f"Saved figure to {OUTPUT_PATH}")
print(f"Sampling: dt = {DT*1000:.0f} ms, fs = {FS:.0f} Hz, fN = {F_N:.0f} Hz")
print(f"Gather: {N_TRACES} traces, {N_SAMPLES} samples ({T_MAX} s)")
print(f"Offsets: {OFFSET_MIN:.0f} – {OFFSET_MAX:.0f} m")
print(f"Reflection events:")
for ev in EVENTS:
    print(f"  t0 = {ev['t0']:.1f} s, Vrms = {ev['vrms']:.0f} m/s, amp = {ev['amp']:.1f}")
print(f"Ground roll: f0 = {GR_F0:.0f} Hz, V_app = {GR_V_APP:.0f} m/s, amp = {GR_AMP:.1f}")
print(f"Filter: {FILTER_ORDER}th-order Butterworth, {FILTER_LO}–{FILTER_HI} Hz (zero-phase)")
