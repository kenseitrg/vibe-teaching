#!/usr/bin/env python3
"""
Figure: Idealized reflectivity series, band-limited seismic response,
and realistic recorded trace with noise, a multiple, and acquisition effects.

Three panels:
  (a) Reflectivity series — spikes at two-way travel times of a 1D layered
      model with three interfaces.
  (b) Ideal seismic trace — convolution of a 25 Hz Ricker wavelet with the
      reflectivity series (band-limited primaries only).
  (c) Recorded trace — ideal response + first-order free-surface multiple
      + band-limited noise + low-cut filter simulating instrument response.

Pedagogical intention: show students that the recorded seismogram differs
substantially from the simple textbook convolutional model.  The additional
components (multiple, noise, acquisition filter) must be accounted for
during processing.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from pathlib import Path


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def ricker(t: np.ndarray, f0: float = 25.0) -> np.ndarray:
    """Ricker (Mexican-hat) wavelet with peak frequency *f0* (Hz)."""
    pft = np.pi * f0 * t
    return (1.0 - 2.0 * pft ** 2) * np.exp(-pft ** 2)


def band_limited_noise(n: int, dt: float = 0.002,
                       flow: float = 5.0, fhigh: float = 80.0,
                       order: int = 4, seed: int = 42) -> np.ndarray:
    """Coloured noise obtained by bandpass filtering white noise.

    Real seismic noise is not white — it tends to have most energy in
    the signal band (approx. 5–80 Hz).  This helper produces a more
    realistic noise realisation.
    """
    rng = np.random.default_rng(seed)
    fs = 1.0 / dt
    nyq = 0.5 * fs
    b, a = butter(order, [flow / nyq, fhigh / nyq], btype="band")
    noise = rng.normal(size=n)
    noise = filtfilt(b, a, noise)
    return noise / np.std(noise)


def low_cut_filter(x: np.ndarray, dt: float = 0.002,
                   fcut: float = 10.0, order: int = 2) -> np.ndarray:
    """Apply a low-cut (high-pass) Butterworth filter.

    Simulates the geophone / instrument transfer function that attenuates
    very-low-frequency energy (common in real acquisition systems).
    """
    fs = 1.0 / dt
    nyq = 0.5 * fs
    b, a = butter(order, fcut / nyq, btype="high")
    return filtfilt(b, a, x)


def spike_train(t: np.ndarray, dt: float,
                times: list, amps: list) -> np.ndarray:
    """Place zero-duration spikes at given *times* with given *amps*."""
    r = np.zeros_like(t)
    for ti, ai in zip(times, amps):
        idx = int(round(ti / dt))
        if 0 <= idx < len(t):
            r[idx] = ai
    return r


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # --- Time axis ---
    dt = 0.002           # 2 ms sample interval
    n_samples = 600      # 1.2 s trace length
    t = np.arange(n_samples) * dt

    # --- 1D layered model (three interfaces) ---
    #
    #  Layer   v (m/s)   top depth (m)   two-way time (s)
    #    1      1500          0             0.000
    #    2      1800        150             0.200
    #    3      3000        350             0.422
    #    4      2500        650             0.622
    #
    # Reflection coefficients (constant density assumed):
    #   r1 = (1800-1500)/(1800+1500) ≈ +0.091
    #   r2 = (3000-1800)/(3000+1800) ≈ +0.250
    #   r3 = (2500-3000)/(2500+3000) ≈ -0.091

    primary_times = [0.200, 0.422, 0.622]
    primary_amps  = [0.090, 0.250, -0.090]

    # --- Panel (a): reflectivity series (primaries only) ---
    reflectivity = spike_train(t, dt, primary_times, primary_amps)

    # --- Wavelet ---
    tw = np.arange(-0.1, 0.1501, dt)    # -100 .. +150 ms
    f0 = 25.0                            # peak frequency (Hz)
    wavelet = ricker(tw, f0)
    wavelet /= np.max(np.abs(wavelet))   # normalise to unit amplitude

    # --- Panel (b): ideal seismic trace (primaries only) ---
    ideal_trace = np.convolve(reflectivity, wavelet, mode="full")[:n_samples]

    # --- Panel (c): recorded trace (ideal + multiple + noise + filter) ---
    #
    # 1. First-order free-surface multiple of the strongest reflector (r2).
    #    Ray path: surface ↓ interface 2 ↑ surface ↓ interface 2 ↑ surface
    #    Travel time = 2 × t2 = 0.844 s
    #    Amplitude  = r2 × (-1) × r2 = -r2² ≈ -0.0625
    r2 = primary_amps[1]
    mult_time = 2.0 * primary_times[1]   # 0.844 s
    mult_amp = -r2 ** 2
    mult_spike = spike_train(t, dt, [mult_time], [mult_amp])
    multiple_trace = np.convolve(mult_spike, wavelet, mode="full")[:n_samples]

    recorded = ideal_trace + multiple_trace

    # 2. Add band-limited (coloured) noise
    noise = band_limited_noise(n_samples, dt=dt, seed=42)
    noise_scale = 0.10 * np.std(ideal_trace)
    recorded = recorded + noise * noise_scale

    # 3. Acquisition low-cut filter (simulates geophone / instrument response)
    recorded = low_cut_filter(recorded, dt=dt, fcut=10.0, order=2)

    # --- Plot ---
    fig, axes = plt.subplots(3, 1, figsize=(10, 7), sharex=True)
    ylim = (-0.40, 0.40)

    # (a) Reflectivity
    ax = axes[0]
    ax.stem(t, reflectivity, linefmt="C0-", markerfmt="C0o", basefmt="gray")
    ax.set_ylabel("Reflection\ncoefficient")
    ax.set_title("(a)  Reflectivity series $r(t)$  —  1D layered model",
                 loc="left", fontsize=11)
    ax.set_ylim(ylim)
    ax.grid(True, alpha=0.3)
    for ts, amp in zip(primary_times, primary_amps):
        ax.annotate(f"$r={amp:+.3f}$", xy=(ts, amp),
                    xytext=(6, 12), textcoords="offset points", fontsize=8,
                    arrowprops=dict(arrowstyle="->", color="gray", lw=0.7))

    # (b) Ideal seismic trace
    ax = axes[1]
    ax.plot(t, ideal_trace, "C1-", lw=1.2)
    ax.fill_between(t, ideal_trace, alpha=0.25, color="C1")
    ax.set_ylabel("Amplitude")
    ax.set_title("(b)  Ideal seismic trace  $x(t) = w(t) * r(t)$",
                 loc="left", fontsize=11)
    ax.set_ylim(ylim)
    ax.grid(True, alpha=0.3)

    # (c) Recorded trace
    ax = axes[2]
    ax.plot(t, recorded, "C2-", lw=1.0)
    ax.fill_between(t, recorded, alpha=0.25, color="C2")
    ax.set_ylabel("Amplitude")
    ax.set_xlabel("Time (s)")
    ax.set_title("(c)  Recorded trace  =  ideal + noise + multiple "
                 "+ acquisition effects",
                 loc="left", fontsize=11)
    ax.set_ylim(ylim)
    ax.grid(True, alpha=0.3)

    # Highlight the multiple arrival
    ax.annotate("First-order\nfree-surface\nmultiple",
                xy=(mult_time, recorded[int(mult_time / dt)]),
                xytext=(mult_time + 0.12, 0.25),
                fontsize=8, color="C3",
                arrowprops=dict(arrowstyle="->", color="C3", lw=0.8))

    fig.tight_layout()

    # --- Save ---
    out_dir = Path("figures/term01_lec01")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "term01_lec01_idealized_vs_recorded_trace.png"
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
