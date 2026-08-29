"""Pulse propagation in a constant-Q medium (Kjartansson model).

A 30 Hz Ricker wavelet is propagated to increasing two-way traveltimes
through a medium with Q = 60 using the constant-Q operator

    U(f, t) = U(f, 0) * exp(-pi f t / Q)            (amplitude decay)
                        * exp(-2*pi*i*f*dt(f))      (dispersion delay)

    dt(f)  = t * ((f / f_ref) ** (-gamma) - 1),  gamma = arctan(1/Q)/pi

with f_ref = 30 Hz. Each trace shows the wavelet recorded at its
traveltime: the wavelet is centred where the reference frequency arrives
(dashed line); lower frequencies travel slower, so the low-frequency tail
lags below the line - the wavelet stretches and its peak drifts late.

Left panel : the wavelet at four traveltimes (each normalized to its peak;
             the true peak amplitude relative to the shallowest trace is
             annotated above each panel).
Right panels: the corresponding amplitude spectra (dB) - the centroid
             frequency (dotted lines) slides toward low frequencies as
             traveltime grows.
"""

import os

import matplotlib.pyplot as plt
import numpy as np

Q = 60.0
F_REF = 30.0
GAMMA = np.arctan(1.0 / Q) / np.pi  # Kjartansson exponent ~ 1/(pi*Q)

DT = 0.002          # s, sampling interval
T_MAX = 4.2         # s, panel length
NFFT = 8192
NW = 121            # wavelet length, samples

TRAVELTIMES = [0.5, 1.5, 2.5, 3.5]
CMAP = plt.get_cmap("viridis")
COLORS = [CMAP(i / max(len(TRAVELTIMES) - 1, 1)) for i in range(len(TRAVELTIMES))]


def ricker_wavelet(f_dom, n=NW):
    """Ricker wavelet with dominant frequency f_dom, n samples, dt = DT."""
    t = (np.arange(n) - n / 2) * DT
    a = f_dom ** 2
    return (1 - 2 * a * t ** 2) * np.exp(-a * t ** 2)


def propagate_q(spectrum, freq, t, q=Q, f_ref=F_REF):
    """Apply the constant-Q earth filter for two-way traveltime t.

    Amplitude: exp(-pi f t / q).
    Phase: frequency-dependent delay dt(f) = t*((f/f_ref)**(-gamma) - 1),
    i.e. every frequency slower than the reference arrives proportionally
    later (velocity dispersion, Kjartansson power law v ~ f**gamma).
    """
    amp = np.exp(-np.pi * freq * t / q)
    with np.errstate(divide="ignore", invalid="ignore"):
        delay = t * ((np.abs(freq) / f_ref) ** (-GAMMA) - 1.0)
    delay = np.where(freq > 0, delay, 0.0)
    phase = np.exp(-2j * np.pi * freq * delay)
    return spectrum * amp * phase


def absorbed_trace(t0, freq, n):
    """Wavelet recorded at two-way traveltime t0.

    The source wavelet is centred at t0 - the arrival time of the
    reference frequency - and then filtered with the constant-Q operator
    for traveltime t0. The result straddles the dashed reference line:
    high frequencies on it, low frequencies lagging below.
    """
    src = np.zeros(NFFT)
    i0 = int(round(t0 / DT)) - NW // 2
    src[i0:i0 + NW] = ricker_wavelet(F_REF)
    spec = propagate_q(np.fft.rfft(src, n=NFFT), freq, t0)
    return np.fft.irfft(spec, n=NFFT)[:n]


def main():
    n = int(T_MAX / DT)
    t_axis = np.arange(n) * DT
    freq = np.fft.rfftfreq(NFFT, d=DT)

    fig = plt.figure(figsize=(10, 6), constrained_layout=True)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.0])
    ax_tr = fig.add_subplot(gs[:, 0])
    ax_sp = [fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[1, 1])]

    # --- wavelet panels: one vertical trace per traveltime ---
    traces = [absorbed_trace(tt, freq, n) for tt in TRAVELTIMES]
    peaks = [np.max(np.abs(tr)) for tr in traces]

    for i, (tt, color) in enumerate(zip(TRAVELTIMES, COLORS)):
        display = traces[i] / peaks[i]
        x0 = 1.7 * (i + 1)   # earliest traveltime on the left

        # zero-amplitude axis and reference arrival time of f_ref
        ax_tr.axvline(x0, color="0.85", lw=0.7, zorder=0)
        ax_tr.plot([x0 - 0.9, x0 + 0.9], [tt, tt], ls="--", color="0.45",
                   lw=1.0, zorder=1)

        ax_tr.plot(x0 + 0.75 * display, t_axis, color=color, lw=1.1, zorder=2)
        ax_tr.fill_betweenx(t_axis, x0, x0 + 0.75 * display,
                            where=display > 0, color=color, alpha=0.45,
                            zorder=2)

        # header: traveltime and true amplitude relative to shallowest
        ratio = peaks[0] / peaks[i]
        label = f"t = {tt:.1f} s" + ("" if i == 0 else f"\n({ratio:.0f}x weaker)")
        ax_tr.text(x0, -0.06, label, ha="center", va="bottom", fontsize=9,
                   color=color)

    ax_tr.set_xlim(-0.4, 7.3)
    ax_tr.set_ylim(T_MAX, 0)
    ax_tr.set_xticks([])
    ax_tr.set_ylabel("Two-way time, s")

    # small caption inside the panel bottom (instead of a title, which
    # would overlap the per-trace header labels above the axes)
    ax_tr.text(3.45, 4.12,
               "each panel normalized to its peak; "
               "dashed line: arrival of $f_{ref}$",
               fontsize=8.5, color="0.35", ha="center")

    # --- spectra panels (amplitude spectrum is shift-invariant) ---
    f_mask = (freq > 0) & (freq < 120)
    src_spec = np.fft.rfft(ricker_wavelet(F_REF), n=NFFT)
    for i, (tt, color) in enumerate(zip(TRAVELTIMES, COLORS)):
        spec = propagate_q(src_spec, freq, tt)
        amp = np.abs(spec)
        db = 20 * np.log10(amp / np.max(amp) + 1e-12)
        ax = ax_sp[i // 2]
        ax.plot(freq[f_mask], db[f_mask], color=color, lw=1.4,
                label=f"t = {tt:.1f} s")
        fc = np.sum(freq * amp) / np.sum(amp)
        ax.axvline(fc, color=color, ls=":", lw=1.2)

    for ax in ax_sp:
        ax.set_xlim(0, 100)
        ax.set_ylim(-70, 3)
        ax.set_xlabel("Frequency, Hz")
        ax.grid(alpha=0.3)
        ax.legend(fontsize=9)
    ax_sp[0].set_ylabel("Amplitude, dB")
    ax_sp[1].set_ylabel("Amplitude, dB")
    ax_sp[0].set_title("Amplitude spectra (normalized)\n"
                       "dotted lines: centroid frequency")

    fig.suptitle(f"Constant-Q propagation, Q = {Q:.0f}, reference {F_REF:.0f} Hz: "
                 "amplitude loss, spectral shift and wavelet stretching",
                 fontsize=12)

    # annotate the lagging low-frequency tail on the deepest (rightmost) trace
    ax_tr.annotate("low-$f$ tail lags\n(wavelet stretches)",
                   xy=(6.8 + 0.30, TRAVELTIMES[-1] + 0.12),
                   xytext=(3.6, 3.8), fontsize=9,
                   color="0.25", ha="center",
                   arrowprops=dict(arrowstyle="->", color="0.25"))
    out = os.path.join("figures",
                       "term02_lec01", "term02_lec01_pulse_broadening.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=150)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
