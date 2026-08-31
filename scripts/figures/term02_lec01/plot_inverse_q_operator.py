"""The inverse-Q amplitude operator: instability and stabilization.

Heat maps of the amplitude compensation operator in the (t, f) plane,
Q = 50, frequencies 0-100 Hz, traveltimes 0-4 s.

Left : raw inverse operator  g(t, f) = exp(pi f t / Q)  shown in dB with
       display clipping at +60 dB. True values at the top-right corner
       reach exp(pi*100*4/50) ~ 10^11 - the numerical instability.
Right: Wang's (2006) stabilized operator
           Lambda = (Lambda_a + sigma^2) / (Lambda_a^2 + sigma^2),
           Lambda_a = exp(-pi f t / Q),
       with the stabilization factor computed from a gain limit of
       G_lim = 20 dB:  sigma^2 = exp(-(0.23*G_lim + 1.63)).
       Full boost where signal survives, graceful taper where it has died.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm  # noqa: F401  (import check)
from matplotlib import cm

Q = 50.0
GAIN_LIMIT_DB = 20.0
F_MAX = 100.0   # Hz
T_MAX = 4.0     # s

T = np.linspace(0.0, T_MAX, 400)
F = np.linspace(0.0, F_MAX, 400)
TT, FF = np.meshgrid(T, F, indexing="ij")

LAMBDA_A = np.exp(-np.pi * FF * TT / Q)          # forward attenuation
G_RAW = 1.0 / LAMBDA_A                            # raw inverse: exp(+pi f t/Q)
SIGMA2 = np.exp(-(0.23 * GAIN_LIMIT_DB + 1.63))   # Wang (2006), eq. 27
G_STAB = (LAMBDA_A + SIGMA2) / (LAMBDA_A ** 2 + SIGMA2)


def db(x):
    return 20.0 * np.log10(x + 1e-12)


def main():
    fig, axes = plt.subplots(1, 2, figsize=(10, 6))

    # --- raw operator ---
    pc0 = axes[0].pcolormesh(F, T, np.clip(db(G_RAW), -10, 60),
                             cmap=cm.viridis, shading="auto")
    fig.colorbar(pc0, ax=axes[0], label="gain, dB (clipped at +60 dB)")
    axes[0].set_title("Raw amplitude operator  $e^{\\pi f t/Q}$\n"
                      "an exponential wall: values reach $10^{11}$ - unstable")
    axes[0].set_xlabel("Frequency, Hz")
    axes[0].set_ylabel("Traveltime, s")
    # contour of the raw +40 dB line: far inside the panel
    axes[0].contour(F, T, db(G_RAW), levels=[20, 40], colors="w",
                    linewidths=1.0, linestyles=":")

    # --- stabilized operator ---
    pc1 = axes[1].pcolormesh(F, T, np.clip(db(G_STAB), -40, 25),
                             cmap=cm.viridis, shading="auto")
    fig.colorbar(pc1, ax=axes[1], label="gain, dB")
    axes[1].set_title(f"Stabilized operator (gain limit {GAIN_LIMIT_DB:.0f} dB,"
                      f" $\\sigma^2$ = {SIGMA2:.1e})\n"
                      "full boost where signal lives, taper beyond")
    axes[1].set_xlabel("Frequency, Hz")
    axes[1].set_ylabel("Traveltime, s")
    axes[1].contour(F, T, db(G_STAB), levels=[0, 10],
                    colors="w", linewidths=1.0, linestyles=":")

    # annotate the "signal has died" boundary on the right panel: the
    # +3 dB contour of the stabilized gain hugs the region where the
    # forward attenuation equals the stabilization level
    axes[1].annotate("beyond this line the signal is below noise:\n"
                     "the filter refuses to boost (taper $\\to$ 0)",
                     xy=(78, 3.2), xytext=(30, 3.35), fontsize=9, color="w",
                     arrowprops=dict(arrowstyle="->", color="w"))

    fig.suptitle("Inverse-Q amplitude compensation in the (t, f) plane, "
                 f"Q = {Q:.0f}: why stabilization is mandatory", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    out = os.path.join("figures",
                       "term02_lec01", "term02_lec01_inverse_q_operator.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=150)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
