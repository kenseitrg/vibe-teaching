"""Quality factor Q: two equivalent definitions.

Left panel : fractional energy loss per cycle for Q = 50 and Q = 200,
            and the exponential energy decay with the number of cycles.
Right panel: the resulting amplitude decay exp(-pi*N/Q) versus the number
            of cycles, on a logarithmic scale.

The figure illustrates that "loss per cycle is constant" is equivalent to
exponential decay in the number of cycles (hence in travel time), and that
a modest per-cycle loss compounds to near-total loss over a seismic path.
"""

import os

import matplotlib.pyplot as plt
import numpy as np

Q_VALUES = [50, 200]
COLORS = ["#0072B2", "#E69F00"]  # colorblind-friendly pair


def energy_loss_per_cycle(ax):
    """Bar-style comparison of the per-cycle energy loss for two Q values."""
    for q, color in zip(Q_VALUES, COLORS):
        loss_fraction = 1.0 - np.exp(-2.0 * np.pi / q)
        # energy remaining after N cycles: E_N / E_0 = exp(-2*pi*N/Q)
        n = np.arange(0, 61)
        energy = np.exp(-2.0 * np.pi * n / q)
        ax.plot(n, energy, color=color, lw=2.2,
                label=f"Q = {q}  ({100 * loss_fraction:.1f}% lost per cycle)")
    ax.axhline(1 / np.e, color="gray", ls=":", lw=1)
    ax.text(60, 1 / np.e, " 1/e", va="center", fontsize=9, color="gray")
    ax.set_xlabel("Number of cycles N")
    ax.set_ylabel("Remaining energy  $E_N / E_0$")
    ax.set_title("Energy decay with the number of cycles\n"
                 "$E_N/E_0 = \\exp(-2\\pi N/Q)$")
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(alpha=0.3)
    # annotate a seismic-scale path: 1000 cycles
    ax.annotate("1000 cycles at 50 Hz over 10 s\nnot shown — energy long gone",
                xy=(60, 0.0), xytext=(28, 0.45), fontsize=9, color="0.35",
                arrowprops=dict(arrowstyle="->", color="0.35"))


def amplitude_decay(ax):
    """Amplitude decay vs number of cycles, log scale."""
    n = np.arange(0, 201)
    for q, color in zip(Q_VALUES, COLORS):
        amp = np.exp(-np.pi * n / q)
        ax.semilogy(n, amp, color=color, lw=2.2, label=f"Q = {q}")
    ax.axhline(1e-2, color="gray", ls=":", lw=1)
    ax.text(200, 1.25e-2, "-40 dB", ha="right", fontsize=9, color="gray")
    ax.axhline(1e-3, color="gray", ls=":", lw=1)
    ax.text(200, 1.25e-3, "-60 dB", ha="right", fontsize=9, color="gray")
    ax.set_xlabel("Number of cycles N")
    ax.set_ylabel("Amplitude  $A/A_0$")
    ax.set_title("Amplitude decay  $A/A_0 = \\exp(-\\pi N/Q)$")
    ax.legend(loc="lower left", fontsize=10)
    ax.grid(alpha=0.3, which="both")


def main():
    fig, axes = plt.subplots(1, 2, figsize=(10, 6))
    energy_loss_per_cycle(axes[0])
    amplitude_decay(axes[1])
    fig.suptitle("Quality factor Q: loss per cycle  $Q = 2\\pi\\,E/\\Delta E$",
                 fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    out = os.path.join("figures",
                       "term02_lec01", "term02_lec01_q_definition.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out, dpi=150)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
