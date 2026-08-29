"""Central (centroid) frequency shift method for Q estimation.

For a Gaussian source spectrum with centroid f_c and variance sigma_f^2,
absorption exp(-pi f t / Q) shifts the centroid downward without changing
the variance:  f_c(t) = f_c(0) - (pi sigma_f^2 / Q) * t.
Measuring the slope of the centroid drift gives Q.

Left panel : Gaussian spectra at five traveltimes sliding down in
             frequency (Q = 60, sigma_f = 10 Hz, f_c(0) = 45 Hz).
Right panel: centroid vs traveltime for Q = 40, 60, 100 - straight lines
             whose slopes are -pi sigma_f^2 / Q.
"""

import os

import matplotlib.pyplot as plt
import numpy as np

FC0 = 45.0       # Hz, initial centroid
SIGMA_F = 10.0   # Hz, spectrum standard deviation
TIMES = np.array([0.0, 0.5, 1.0, 1.5, 2.0, 2.5])
Q_SHOW = 60.0
Q_SLOPES = [40.0, 60.0, 100.0]

C_SLOPES = ["#E69F00", "#0072B2", "#009E73"]


def gaussian_spectrum(f, fc, sigma):
    return np.exp(-(f - fc) ** 2 / (2 * sigma ** 2))


def main():
    fig, (ax_s, ax_c) = plt.subplots(1, 2, figsize=(10, 6))
    f = np.linspace(0, 90, 400)

    # --- sliding spectra ---
    cmap = plt.get_cmap("viridis")
    for i, t in enumerate(TIMES):
        fc = FC0 - np.pi * SIGMA_F ** 2 * t / Q_SHOW
        if fc < 10:
            break
        color = cmap(1 - i / len(TIMES))
        ax_s.plot(f, gaussian_spectrum(f, fc, SIGMA_F), color=color, lw=1.8,
                  label=f"t = {t:.1f} s,  $f_c$ = {fc:.0f} Hz")
        ax_s.annotate("", xy=(fc, 0.06), xytext=(FC0, 0.06),
                      arrowprops=dict(arrowstyle="->", color=color, lw=1.0))
    ax_s.set_xlabel("Frequency, Hz")
    ax_s.set_ylabel("Normalized amplitude")
    ax_s.set_title(f"Absorption slides a Gaussian spectrum down\n"
                   f"(Q = {Q_SHOW:.0f}, $\\sigma_f$ = {SIGMA_F:.0f} Hz, "
                   f"width unchanged)")
    ax_s.legend(fontsize=8.5, loc="upper right")
    ax_s.grid(alpha=0.3)

    # --- centroid vs time for three Q values ---
    t_axis = np.linspace(0, 2.5, 50)
    for q, color in zip(Q_SLOPES, C_SLOPES):
        fc = FC0 - np.pi * SIGMA_F ** 2 * t_axis / q
        slope = -np.pi * SIGMA_F ** 2 / q
        ax_c.plot(t_axis, fc, color=color, lw=2.2,
                  label=f"Q = {q:.0f} (slope {slope:.1f} Hz/s)")
    # sample "measurements" on the Q=60 line
    fc_meas = FC0 - np.pi * SIGMA_F ** 2 * TIMES / 60.0
    fc_meas += 0.5 * np.random.default_rng(7).standard_normal(TIMES.size)
    ax_c.plot(TIMES, fc_meas, "o", ms=6, color="#0072B2", mec="w",
              label="measurements (Q = 60, noisy)")
    ax_c.set_xlabel("Traveltime, s")
    ax_c.set_ylabel("Centroid frequency, Hz")
    ax_c.set_title("Centroid drifts linearly with time:\n"
                   "slope $= -\\pi\\,\\sigma_f^2/Q \\;\\Rightarrow\\; Q$")
    ax_c.legend(fontsize=9)
    ax_c.grid(alpha=0.3)

    fig.suptitle("Central frequency shift method (Quan & Harris, 1997): "
                 "robust, whole-spectrum, needs the analysis band",
                 fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    out = os.path.join("figures",
                       "term02_lec01", "term02_lec01_centroid_shift.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=150)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
