"""Velocity dispersion from absorption: Futterman vs Wang (Kjartansson).

Left panel : phase velocity ratio v(f)/v(f_ref) for Q = 50, f_ref = 100 Hz.
             - Futterman (logarithmic law, practical anchored form):
                 v(f)/v(f_ref) = 1 / (1 + (1/(pi*Q)) * ln(f_ref/f))
             - Wang / Kjartansson (power law):
                 v(f)/v(f_ref) = (f/f_ref)**gamma,  gamma = arctan(1/Q)/pi
             Lighter curves show Q = 25 and Q = 100 (power law) to make
             the 1/Q scaling visible.
Right panel: the resulting delay of a low-frequency component relative to
             the reference frequency over t0 = 2 s of travel time,
             dt(f) = t0 * ((f/f_ref)**(-gamma) - 1) - tens of milliseconds,
             which is exactly the wavelet stretch seen on real data.
"""

import os

import matplotlib.pyplot as plt
import numpy as np

Q_MAIN = 50.0
F_REF = 100.0
T0 = 2.0  # s, reference travel time for the delay panel

C_MAIN = "#0072B2"   # blue
C_ALT = "#D55E00"    # vermillion
C_LIGHT = ["#56B4E9", "#E69F00"]  # lighter shades for Q = 25 / 100


def gamma_of_q(q):
    """Kjartansson exponent: gamma = arctan(1/Q)/pi ~ 1/(pi Q)."""
    return np.arctan(1.0 / q) / np.pi


def futterman_ratio(f, q, f_ref):
    """Anchored Futterman velocity ratio (Hargreaves & Calvert form)."""
    return 1.0 / (1.0 + np.log(f_ref / f) / (np.pi * q))


def wang_ratio(f, q, f_ref):
    """Kjartansson / Wang power-law velocity ratio."""
    return (f / f_ref) ** gamma_of_q(q)


def main():
    f = np.logspace(np.log10(2), np.log10(200), 400)

    fig, (ax_v, ax_d) = plt.subplots(1, 2, figsize=(10, 6))

    # --- velocity ratios ---
    ax_v.plot(f, futterman_ratio(f, Q_MAIN, F_REF), color=C_MAIN, lw=2.4,
              label=f"Futterman (log law), Q = {Q_MAIN:.0f}")
    ax_v.plot(f, wang_ratio(f, Q_MAIN, F_REF), color=C_ALT, lw=2.4, ls="--",
              label=f"Wang / Kjartansson (power law), Q = {Q_MAIN:.0f}")
    for q, color in zip([25.0, 100.0], C_LIGHT):
        ax_v.plot(f, wang_ratio(f, q, F_REF), color=color, lw=1.3, alpha=0.85,
                  label=f"power law, Q = {q:.0f}")
    ax_v.axhline(1.0, color="gray", lw=0.8)
    ax_v.axvline(F_REF, color="gray", ls=":", lw=1)
    ax_v.text(F_REF, 1.036, " $f_{ref}$", fontsize=9, color="gray")

    # annotate one decade of change
    dv = (wang_ratio(100.0, Q_MAIN, F_REF) - wang_ratio(10.0, Q_MAIN, F_REF))
    ax_v.annotate(f"$\\Delta v/v \\approx {100 * dv:.1f}\\%$ per decade",
                  xy=(10, wang_ratio(10.0, Q_MAIN, F_REF)),
                  xytext=(2.6, 0.955), fontsize=10, color=C_ALT,
                  arrowprops=dict(arrowstyle="->", color=C_ALT))
    ax_v.set_xscale("log")
    ax_v.set_xlabel("Frequency, Hz")
    ax_v.set_ylabel("$v(f)\\,/\\,v(f_{ref})$")
    ax_v.set_title(f"Velocity dispersion (higher $f$ travels faster)\n"
                   f"Q = {Q_MAIN:.0f}, $f_{{ref}}$ = {F_REF:.0f} Hz")
    ax_v.legend(fontsize=9, loc="lower right")
    ax_v.grid(alpha=0.3, which="both")

    # --- delay of low frequencies ---
    for q, color, lw, ls in [(Q_MAIN, C_ALT, 2.4, "-"),
                             (25.0, C_LIGHT[0], 1.4, "--"),
                             (100.0, C_LIGHT[1], 1.4, "--")]:
        delay_ms = 1e3 * T0 * ((f / F_REF) ** (-gamma_of_q(q)) - 1.0)
        ax_d.plot(f, delay_ms, color=color, lw=lw, ls=ls,
                  label=f"Q = {q:.0f}")
    ax_d.axhline(0, color="gray", lw=0.8)
    ax_d.axvline(F_REF, color="gray", ls=":", lw=1)
    ax_d.annotate("low frequencies lag\n(wavelet stretches, peak goes late)",
                  xy=(10, 1e3 * T0 * ((10 / F_REF) ** (-gamma_of_q(Q_MAIN)) - 1)),
                  xytext=(3, 55), fontsize=10, color=C_ALT,
                  arrowprops=dict(arrowstyle="->", color=C_ALT))
    ax_d.set_xscale("log")
    ax_d.set_xlabel("Frequency, Hz")
    ax_d.set_ylabel(f"Delay vs $f_{{ref}}$ over $t_0$ = {T0:.0f} s, ms")
    ax_d.set_title("Consequence: frequency-dependent delay\n"
                   "(pure phase effect - unconditionally correctable)")
    ax_d.legend(fontsize=9)
    ax_d.grid(alpha=0.3, which="both")

    fig.suptitle("Dispersion required by causality: "
                 "Futterman's and Wang's laws nearly coincide", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    out = os.path.join("figures",
                       "term02_lec01", "term02_lec01_velocity_dispersion.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=150)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
