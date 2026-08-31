"""Spectral-ratio method for Q estimation.

Synthetic VSP-style example with true Q = 80. Two windows at t1 = 1.0 s and
t2 = 2.5 s contain wavelets whose spectra follow

    |A(f, t)| = g(t) * |S(f)| * exp(-pi f t / Q)

with a Ricker-like source spectrum S and mild multiplicative noise on the
spectra (5%) to mimic estimation noise.

Left panel : the two amplitude spectra - the later one is tilted toward
             low frequencies.
Right panel: the natural log of the spectral ratio vs frequency together
             with the least-squares straight line; the slope k gives
             Q = -pi*(t2-t1)/k.

The scatter of the points around the line is the method's weakness: the
ratio of two noisy spectra is noisy, and the fitted slope (hence Q)
inherits that noise.
"""

import os

import matplotlib.pyplot as plt
import numpy as np

Q_TRUE = 80.0
T1, T2 = 1.0, 2.5
F_DOM = 35.0
NOISE = 0.05          # 5% multiplicative spectral noise
F_MIN, F_MAX = 5, 90  # analysis band, Hz

C1, C2 = "#0072B2", "#D55E00"


def ricker_amplitude_spectrum(f, f_dom):
    """|Ricker wavelet| amplitude spectrum."""
    a = np.pi * f_dom ** 2
    return (2.0 / np.sqrt(np.pi)) * f ** 2 / a ** 1.5 * np.exp(-f ** 2 / a)


def main():
    rng = np.random.default_rng(3)
    f = np.linspace(0.1, 120, 300)
    s = ricker_amplitude_spectrum(f, F_DOM)

    a1 = s * np.exp(-np.pi * f * T1 / Q_TRUE) * (1.0 + NOISE * rng.standard_normal(f.size))
    a2 = s * np.exp(-np.pi * f * T2 / Q_TRUE) * (1.0 + NOISE * rng.standard_normal(f.size))

    band = (f >= F_MIN) & (f <= F_MAX)
    ratio = np.log(a2[band] / a1[band])
    # least-squares fit  ln(A2/A1) = k*f + b
    k, b = np.polyfit(f[band], ratio, 1)
    q_est = -np.pi * (T2 - T1) / k

    fig, (ax_s, ax_r) = plt.subplots(1, 2, figsize=(10, 6))

    # --- spectra ---
    ax_s.plot(f, a1 / a1.max(), color=C1, lw=2.0, label=f"window 1: t = {T1:.1f} s")
    ax_s.plot(f, a2 / a2.max(), color=C2, lw=2.0, label=f"window 2: t = {T2:.1f} s")
    ax_s.axvspan(F_MIN, F_MAX, color="0.92", zorder=0)
    ax_s.text((F_MIN + F_MAX) / 2, 1.03, "analysis band", ha="center",
              fontsize=9, color="0.35")
    ax_s.set_xlabel("Frequency, Hz")
    ax_s.set_ylabel("Normalized amplitude")
    ax_s.set_title("Two windowed spectra\n(later window tilted to low $f$)")
    ax_s.legend(fontsize=10)
    ax_s.grid(alpha=0.3)
    ax_s.set_xlim(0, 110)

    # --- log ratio + fit ---
    ax_r.plot(f[band], ratio, "o", ms=4, color="0.4",
              label=r"$\ln|A_2/A_1|$ (noisy ratio)")
    ax_r.plot(f[band], k * f[band] + b, color=C2, lw=2.2,
              label=f"least-squares fit: slope k = {k:.4f} s")
    ax_r.set_xlabel("Frequency, Hz")
    ax_r.set_ylabel(r"$\ln\,|A_2(f)/A_1(f)|$")
    ax_r.set_title(f"Straight line in frequency\n"
                   f"$Q = -\\pi\\,\\Delta t/k = {q_est:.0f}$  (true Q = {Q_TRUE:.0f})")
    ax_r.legend(fontsize=10)
    ax_r.grid(alpha=0.3)

    fig.suptitle("Spectral-ratio method: the ratio cancels the source, "
                 "the slope measures absorption", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    out = os.path.join("figures",
                       "term02_lec01", "term02_lec01_spectral_ratio.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=150)
    print(f"saved {out}; Q_est = {q_est:.1f}")


if __name__ == "__main__":
    main()
