"""Four classical models of Q, after Kjartansson (1979), Table 1.

Top panel   : Q(f) for the four model families over 1-200 Hz.
Bottom panel: the corresponding dispersion v(f)/v(1 Hz), with the causal
              families showing dispersion and the acausal ones none.

Families (normalized to Q = 50 at 30 Hz where a scale is needed):
  1. Frictional (Born 1941, White 1966): Q constant, v constant -
     but NONLINEAR and acausal: rejected for processing.
  2. Voigt-Ricker (viscous): Q proportional to frequency, v constant at
     low f - linear and causal but contradicts measurements (Q ~ f wrong).
  3. Kolsky-Futterman NCQ: Q nearly constant inside a band (idealized
     here as flat over 5-150 Hz with tapers), logarithmic dispersion.
  4. Kjartansson CQ: Q exactly constant at all frequencies, power-law
     dispersion v ~ f**gamma.

The seismic band (5-100 Hz) is shaded: inside it, families 3 and 4 are
nearly indistinguishable - the practical message of the figure.
"""

import os

import matplotlib.pyplot as plt
import numpy as np

F = np.logspace(0, np.log10(200), 500)  # 1 .. 200 Hz
F0 = 30.0    # normalization frequency
Q0 = 50.0    # normalization value
BAND = (5.0, 100.0)

C_FRICTION = "#999999"
C_VOIGT = "#E69F00"
C_NCO = "#0072B2"
C_CQ = "#D55E00"


def gamma_of_q(q):
    return np.arctan(1.0 / q) / np.pi


def q_frictional(f):
    return np.full_like(f, Q0)


def q_voigt(f):
    return Q0 * f / F0  # Q proportional to frequency


def q_nco(f, lo=2.0, hi=150.0, width=0.35):
    """Near-constant Q inside [lo, hi] with log-frequency tapers."""
    q = np.full_like(f, Q0)
    below = f < lo
    above = f > hi
    q[below] = Q0 * (f[below] / lo) ** 2
    q[above] = Q0 * (f[above] / hi) ** 0.5
    return q


def q_cq(f):
    return np.full_like(f, Q0)


def v_ratio_from_q(f, q, gamma_exponent=None):
    """Dispersion law: v(f)/v(1 Hz) for the causal constant/near-const-Q.

    Uses the power law with the local gamma implied by Q; for the Voigt
    family (Q ~ f) low frequencies are non-dispersive: v const at low f.
    """
    g = gamma_of_q(q) if gamma_exponent is None else gamma_exponent
    return (f / 1.0) ** g


def main():
    fig, (ax_q, ax_v) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    # ---- Q(f) ----
    ax_q.plot(F, q_frictional(F), color=C_FRICTION, lw=2.0, ls=(0, (4, 2)),
              label="Frictional (Born, White): const Q - but nonlinear, acausal")
    ax_q.plot(F, q_voigt(F), color=C_VOIGT, lw=2.2,
              label="Voigt-Ricker: $Q \\propto f$ - contradicts measurements")
    ax_q.plot(F, q_nco(F), color=C_NCO, lw=2.2,
              label="Kolsky-Futterman NCQ: near-const Q in band + cutoff")
    ax_q.plot(F, q_cq(F), color=C_CQ, lw=2.2, ls="--",
              label="Kjartansson CQ: exactly constant Q")
    ax_q.set_xscale("log")
    ax_q.set_yscale("log")
    ax_q.set_ylabel("Quality factor  $Q(f)$")
    ax_q.set_ylim(1, 1000)
    ax_q.set_title("Four classical attenuation models (Kjartansson 1979, Table 1)")
    ax_q.legend(fontsize=9, loc="upper left")
    ax_q.grid(alpha=0.3, which="both")
    ax_q.axvspan(*BAND, color="0.85", zorder=0)
    ax_q.text(np.sqrt(BAND[0] * BAND[1]), 1.3, "seismic band",
              ha="center", fontsize=9, color="0.35")

    # ---- v(f) ----
    # frictional: no dispersion at all (acausal choice)
    ax_v.plot(F, np.ones_like(F), color=C_FRICTION, lw=2.0, ls=(0, (4, 2)),
              label="Frictional: no dispersion (acausal)")
    # Voigt-Ricker: dispersion concentrated at high frequency, flat at low f
    v_voigt = 1.0 + 0.06 * (np.clip(F - 20.0, 0, None) / 180.0) ** 2
    ax_v.plot(F, v_voigt, color=C_VOIGT, lw=2.2,
              label="Voigt-Ricker: non-dispersive at low $f$")
    # NCQ: Futterman log law anchored at 30 Hz, normalized to v(1 Hz) = 1
    a = 1.0 / (np.pi * Q0)
    v_futt = 1.0 / (1.0 + a * np.log(F0 / F))
    v_nco = v_futt / v_futt[0]
    ax_v.plot(F, v_nco, color=C_NCO, lw=2.2,
              label="NCQ: logarithmic dispersion")
    # CQ: power law
    g = gamma_of_q(Q0)
    ax_v.plot(F, (F / 1.0) ** g, color=C_CQ, lw=2.2, ls="--",
              label="CQ: power law  $v \\propto f^{\\gamma}$")
    ax_v.set_xscale("log")
    ax_v.set_xlabel("Frequency, Hz")
    ax_v.set_ylabel("$v(f)\\,/\\,v(1\\,$Hz$)$")
    ax_v.set_ylim(0.99, 1.10)
    ax_v.legend(fontsize=9, loc="upper left")
    ax_v.grid(alpha=0.3, which="both")
    ax_v.axvspan(*BAND, color="0.85", zorder=0)

    fig.suptitle("Inside the seismic band the NCQ and CQ models nearly "
                 "coincide - causal consistency is what matters",
                 fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    out = os.path.join("figures",
                       "term02_lec01", "term02_lec01_q_models.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=150)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
