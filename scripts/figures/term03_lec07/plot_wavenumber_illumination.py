"""Wavenumber illumination in FWI: which spatial scales does each wave type update?

At a scattering point x, the model update contains the wavenumber vector
k = p_r - p_s (difference of the slowness vectors toward receiver and source),
with magnitude k = (2 f / v) * cos(theta/2), where theta is the illumination
angle between p_s and p_r (Sirgue & Pratt, 2004).

Two end members:
  - Reflection (back-scattered): p_s, p_r nearly parallel, theta ~ 0
    -> large |k| -> SHORT wavelength updates (reflectivity scale).
  - Transmission / diving wave: p_s, p_r nearly anti-parallel, theta ~ 180 deg
    -> small |k| -> LONG wavelength updates (tomographic scale).

Panel (a): the geometry (after Metivier & Brossier 2026, Fig. 1).
Panel (b): the two end-member cases and the wavelength each injects.

Self-contained: numpy + matplotlib only.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = (
    Path(__file__).resolve().parents[3] / "figures" / "term03_lec07" / "term03_lec07_wavenumber_illumination.png"
)

V_WATER = 1500.0  # m/s, reference velocity for the wavelength bars
F_DOM = 10.0      # Hz, dominant frequency used for the numeric examples


def draw_earth(ax):
    """Surface line and simple layering ticks."""
    ax.axhline(0.0, color="k", lw=2.0)
    for depth in np.linspace(0.06, 0.94, 5):
        ax.axhline(-depth, color="0.85", lw=0.8, zorder=0)


def case_geometry(theta_deg, source_x, receiv_x):
    """Return p_s, p_r unit vectors at the scattering point for a given
    illumination angle theta between them (both sources near the surface)."""
    # Bisector points from the scattering point up toward the midpoint of the
    # surface arc spanned by source and receiver; the two rays are rotated
    # +/- theta/2 from the horizontal direction toward their ends.
    mid = 0.5 * (source_x + receiv_x)
    bis = np.array([mid - 0.0, 0.0])  # placeholder, fixed below
    return bis


def main() -> None:
    fig = plt.figure(figsize=(10.0, 6.0), dpi=150)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.18)

    # ------------------------------------------------------------------
    # Panel (a): geometry
    # ------------------------------------------------------------------
    ax = fig.add_subplot(gs[0, 0])
    draw_earth(ax)
    ax.set_xlim(-0.62, 0.62)
    ax.set_ylim(-1.15, 0.28)
    ax.set_aspect("equal")
    ax.axis("off")

    # Surface positions and scattering point
    s_pos = np.array([-0.42, 0.0])
    r_pos = np.array([0.42, 0.0])
    x_pos = np.array([0.0, -0.62])

    # Ray directions from the scattering point toward S and R
    p_s = (s_pos - x_pos) / np.linalg.norm(s_pos - x_pos)
    p_r = (r_pos - x_pos) / np.linalg.norm(r_pos - x_pos)
    theta = np.degrees(np.arccos(np.clip(np.dot(p_s, p_r), -1.0, 1.0)))

    # Rays as dashed curves
    t = np.linspace(0.0, 1.0, 60)
    for end in (s_pos, r_pos):
        # gentle curvature for a visual ray path
        ctrl = 0.5 * (x_pos + end) + np.array([0.0, 0.12])
        curve = (
            (1 - t)[:, None] ** 2 * x_pos
            + 2 * ((1 - t) * t)[:, None] * ctrl
            + t[:, None] ** 2 * end
        )
        ax.plot(curve[:, 0], curve[:, 1], color="#0072B2", ls="--", lw=1.4)

    # Source and receiver markers
    ax.plot(*s_pos, marker="*", ms=16, color="#D55E00", mec="k", mew=0.6, zorder=5)
    ax.plot(*r_pos, marker="v", ms=10, color="#009E73", mec="k", mew=0.6, zorder=5)
    ax.text(s_pos[0] - 0.02, 0.09, "S (source)", ha="center", fontsize=11)
    ax.text(r_pos[0] + 0.02, 0.09, "R (receiver)", ha="center", fontsize=11)
    ax.plot(*x_pos, marker="o", ms=9, color="k", zorder=5)
    ax.text(x_pos[0] + 0.06, x_pos[1] - 0.10, "scattering point", fontsize=10)

    # Slowness vectors p_s, p_r at the scattering point
    for vec, name, color, shift in (
        (p_s, "$p_s$", "#D55E00", np.array([0.04, 0.0])),
        (p_r, "$p_r$", "#009E73", np.array([0.04, 0.0])),
    ):
        ax.annotate(
            "",
            xy=x_pos + shift + 0.34 * vec,
            xytext=x_pos + shift,
            arrowprops=dict(arrowstyle="-|>", color=color, lw=2.2),
        )
        ax.text(
            *(x_pos + shift + 0.40 * vec), name, color=color, fontsize=13, ha="center"
        )

    # Illumination angle arc between p_s and p_r
    ang_s = np.degrees(np.arctan2(p_s[1], p_s[0]))
    ang_r = np.degrees(np.arctan2(p_r[1], p_r[0]))
    arc = np.linspace(np.radians(ang_s), np.radians(ang_r), 50)
    ax.plot(
        0.17 * np.cos(arc) + x_pos[0],
        0.17 * np.sin(arc) + x_pos[1],
        color="0.3",
        lw=1.2,
    )
    bis_dir = (p_s + p_r) / np.linalg.norm(p_s + p_r)
    ax.text(
        *(x_pos + 0.27 * bis_dir), f"$\\theta = {theta:.0f}^\\circ$", fontsize=12, ha="center"
    )

    # Wavenumber vector k = p_r - p_s (up to scale, drawn from the point)
    k_vec = p_r - p_s
    k_vec = k_vec / np.linalg.norm(k_vec)
    ax.annotate(
        "",
        xy=x_pos + 0.42 * k_vec,
        xytext=x_pos,
        arrowprops=dict(arrowstyle="-|>", color="k", lw=2.4),
    )
    ax.text(*(x_pos + 0.50 * k_vec), "$k \\propto p_r - p_s$", fontsize=12, ha="center")

    ax.set_title("(a) Illumination geometry", fontsize=12)
    ax.text(
        0.0,
        -1.12,
        "$|k| = \\dfrac{2 f}{v}\\,\\cos\\dfrac{\\theta}{2}$",
        ha="center",
        fontsize=13,
    )

    # ------------------------------------------------------------------
    # Panel (b): end members
    # ------------------------------------------------------------------
    axb = fig.add_subplot(gs[0, 1])
    axb.set_xlim(0, 1)
    axb.set_ylim(0, 1)
    axb.axis("off")
    axb.set_title("(b) What each wave type updates", fontsize=12)

    lam_refl = V_WATER / F_DOM            # back-scattered: k = 2f/v -> lambda/2
    lam_div = V_WATER / F_DOM / 4.0       # near-transmitted: k ~ f/(2v) -> 2*lambda (illustrative)

    # --- top: reflection case ---
    y0 = 0.86
    axb.plot([0.06, 0.30], [y0, y0], color="k", lw=1.5)
    axb.plot(0.10, y0, marker="*", ms=11, color="#D55E00", mec="k", mew=0.5)
    axb.plot(0.26, y0, marker="v", ms=8, color="#009E73", mec="k", mew=0.5)
    xc = np.array([0.18, y0 - 0.42])
    for start in (np.array([0.10, y0]), np.array([0.26, y0])):
        axb.annotate(
            "",
            xy=xc,
            xytext=start,
            arrowprops=dict(arrowstyle="->", color="#0072B2", lw=1.6),
        )
    axb.plot(*xc, "o", ms=6, color="k")
    axb.annotate(
        "",
        xy=xc + np.array([0.10, 0.0]),
        xytext=xc + np.array([-0.10, 0.0]),
        arrowprops=dict(arrowstyle="<->", color="k", lw=1.6),
    )
    axb.text(
        0.52,
        y0 - 0.05,
        "reflection / back-scattering\n"
        r"$\theta \to 0^\circ$:  $\cos(\theta/2) \to 1$"
        "\n"
        rf"high $|k|$  $\Rightarrow$  short $\lambda \approx {lam_refl:.0f}$ m",
        fontsize=10.5,
        va="center",
    )

    # --- bottom: diving-wave case ---
    y1 = 0.34
    axb.plot([0.06, 0.30], [y1, y1], color="k", lw=1.5)
    axb.plot(0.10, y1, marker="*", ms=11, color="#D55E00", mec="k", mew=0.5)
    axb.plot(0.26, y1, marker="v", ms=8, color="#009E73", mec="k", mew=0.5)
    xd = np.array([0.18, y1 - 0.20])
    axb.annotate(
        "",
        xy=xd,
        xytext=np.array([0.10, y1]),
        arrowprops=dict(
            arrowstyle="->", color="#0072B2", lw=1.6, connectionstyle="arc3,rad=-0.35"
        ),
    )
    axb.annotate(
        "",
        xy=np.array([0.26, y1]),
        xytext=xd,
        arrowprops=dict(
            arrowstyle="->", color="#0072B2", lw=1.6, connectionstyle="arc3,rad=-0.35"
        ),
    )
    axb.plot(*xd, "o", ms=6, color="k")
    axb.annotate(
        "",
        xy=xd + np.array([0.085, 0.0]),
        xytext=xd + np.array([-0.085, 0.0]),
        arrowprops=dict(arrowstyle="<->", color="k", lw=1.6),
    )
    axb.text(
        0.52,
        y1 - 0.05,
        "diving / transmitted wave\n"
        r"$\theta \to 180^\circ$:  $\cos(\theta/2) \to 0$"
        "\n"
        rf"low $|k|$  $\Rightarrow$  long $\lambda \gtrsim {lam_div:.0f}$ m",
        fontsize=10.5,
        va="center",
    )

    fig.suptitle(
        "Wavenumber illumination in FWI (after Sirgue & Pratt 2004; Métivier & Brossier 2026)",
        fontsize=12,
        y=0.99,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150, bbox_inches="tight")
    print(f"saved {OUT}")


if __name__ == "__main__":
    main()
