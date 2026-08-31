"""Compensation modes on synthetic data: phase-only vs amplitude+phase.

Three reflectors (Ricker 30 Hz wavelets) at 1.0, 2.0, 3.0 s are propagated
through a constant-Q medium (Q = 60, reference frequency 30 Hz) and then
corrected in two modes:

  raw            - as recorded (absorbed, dispersed)
  phase-only     - exact dispersion undo: stable, sharpens and re-centres
                   the wavelet but does not restore amplitudes
  amplitude+phase - full inverse Q with a stabilized amplitude operator
                   (gain limit 20 dB): also restores spectral tilt

The reference trace (no absorption) is shown for comparison.
Notice on the raw traces: weaker, longer, late-peak wavelets growing with
traveltime; the phase-only trace fixes shape/timing; the full correction
additionally recovers the high frequencies that survived.
"""

import os

import matplotlib.pyplot as plt
import numpy as np

Q = 60.0
F_REF = 30.0
GAIN_LIMIT_DB = 20.0
DT = 0.002
T_MAX = 4.0
NFFT = 4096
REFLECTORS = [1.0, 2.0, 3.0]      # s, two-way times

GAMMA = np.arctan(1.0 / Q) / np.pi
SIGMA2 = np.exp(-(0.23 * GAIN_LIMIT_DB + 1.63))


def ricker_wavelet(f_dom, n=121):
    t = (np.arange(n) - n / 2) * DT
    a = f_dom ** 2
    return (1 - 2 * a * t ** 2) * np.exp(-a * t ** 2)


def make_reflectivity_trace():
    """Zero trace with three Ricker wavelets at the reflector times."""
    trace = np.zeros(NFFT)
    n = 121
    w = ricker_wavelet(F_REF, n)
    for t0 in REFLECTORS:
        i0 = int(round(t0 / DT)) - n // 2
        trace[i0:i0 + n] += w
    return trace


def forward_q_trace(trace):
    """Apply the (nonstationary) earth Q filter reflector by reflector."""
    freq = np.fft.rfftfreq(NFFT, d=DT)
    out = np.zeros(NFFT)
    for t0 in REFLECTORS:
        # isolate the reflector's wavelet
        seg = np.zeros(NFFT)
        n = 121
        i0 = int(round(t0 / DT)) - n // 2
        seg[i0:i0 + n] = ricker_wavelet(F_REF, n)
        spec = np.fft.rfft(seg, n=NFFT)
        amp = np.exp(-np.pi * freq * t0 / Q)
        with np.errstate(divide="ignore", invalid="ignore"):
            delay = t0 * ((np.abs(freq) / F_REF) ** (-GAMMA) - 1.0)
        delay = np.where(freq == 0, 0.0, delay)
        out += np.fft.irfft(spec * amp * np.exp(-2j * np.pi * freq * delay),
                            n=NFFT)
    return out, freq


def inverse_q(trace, freq, mode):
    """Apply inverse Q in the chosen mode (approximately, per event).

    For teaching we apply the operator centred on each reflector time -
    exactly how a layered/segmented implementation works.
    """
    out = np.zeros_like(trace)
    for t0 in REFLECTORS:
        # window the event
        half = int(0.25 / DT)
        i0 = int(round(t0 / DT))
        seg = np.zeros(NFFT)
        lo, hi = max(0, i0 - half), min(len(trace), i0 + half)
        seg[lo:hi] = trace[lo:hi]
        spec = np.fft.rfft(seg, n=NFFT)

        # phase operator: undo the dispersion delay
        with np.errstate(divide="ignore", invalid="ignore"):
            delay = t0 * ((np.abs(freq) / F_REF) ** (-GAMMA) - 1.0)
        delay = np.where(freq == 0, 0.0, delay)
        phase = np.exp(+2j * np.pi * freq * delay)

        # amplitude operator: inverse attenuation, stabilized (Wang 2006)
        lam_a = np.exp(-np.pi * freq * t0 / Q)
        amp = (lam_a + SIGMA2) / (lam_a ** 2 + SIGMA2) if mode == "full" \
            else np.ones_like(lam_a)

        corrected = spec * phase * amp
        out[lo:hi] += np.fft.irfft(corrected, n=NFFT)[lo:hi]
    return out


def draw_trace(ax, trace, x0, color, label, scale=1.0):
    t_axis = np.arange(len(trace)) * DT
    norm = np.max(np.abs(trace))
    disp = scale * trace / (norm + 1e-12)
    ax.plot(x0 + disp, t_axis, color=color, lw=1.0)
    ax.fill_betweenx(t_axis, x0, x0 + disp, where=disp > 0,
                     color=color, alpha=0.5)
    ax.text(x0, T_MAX + 0.08, label, ha="center", fontsize=9, color=color)


def main():
    ref = make_reflectivity_trace()
    absorbed, freq = forward_q_trace(ref)
    phase_only = inverse_q(absorbed, freq, "phase")
    full = inverse_q(absorbed, freq, "full")

    fig, ax = plt.subplots(figsize=(10, 6))
    for i, t0 in enumerate(REFLECTORS):
        ax.axhline(t0, color="0.9", lw=0.7, zorder=0)

    draw_trace(ax, ref, 0.0, "0.6", "reference\n(no absorption)")
    draw_trace(ax, absorbed, 2.5, "#0072B2", "absorbed\n(raw)")
    draw_trace(ax, phase_only, 5.0, "#009E73", "phase-only\n(stable)")
    draw_trace(ax, full, 7.5, "#D55E00",
               f"amplitude+phase\n({GAIN_LIMIT_DB:.0f} dB limit)")

    ax.set_xlim(-1.0, 8.7)
    ax.set_ylim(T_MAX + 0.25, 0)
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_ylabel("Two-way time, s")
    ax.set_title(f"Q-compensation modes, Q = {Q:.0f}: "
                 "three reflectors, 30 Hz Ricker wavelets\n"
                 "phase-only fixes stretching/delay; "
                 "amplitude+phase also restores bandwidth")
    for t0 in REFLECTORS:
        ax.text(-0.9, t0 - 0.07, f"t = {t0:.1f} s", fontsize=8, color="0.4")

    out = os.path.join("figures",
                       "term02_lec01", "term02_lec01_compensation_modes.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=150)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
