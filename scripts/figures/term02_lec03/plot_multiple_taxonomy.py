"""Figure: Classification of multiples — a two-axis taxonomy.

Left column — by location of the extra downward reflection:
  * surface-related: at least one downward reflection at the free
    (sea) surface. Definition test: 'disappears if the surface were
    removed'. Includes water-bottom multiples, peg-legs and surface
    multiples of deeper reflectors.
  * internal (interbed): all downward reflections below the surface.

Right column — by period (relative to the wavelet length):
  * long-period: separate, individually visible events (~>50 ms);
    handled by move-out methods (Radon) and prediction (SRME).
  * short-period: reverberations hidden inside one wavelet length;
    handled statistically by (predictive) deconvolution.

Each card carries a mini raypath icon (red circle = downward
reflection) and the typical treatment. The two axes are independent:
a water-bottom multiple can be short- or long-period depending on
water depth.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis("off")


def card(cx, cy, w, h, title, body, color):
    box = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                         boxstyle="round,pad=0.12", fc="white", ec=color, lw=2.2)
    ax.add_patch(box)
    ax.text(cx, cy + h / 2 - 0.42, title, ha="center", va="top",
            fontsize=12.5, fontweight="bold", color=color)
    ax.text(cx - w / 2 + 0.3, cy + h / 2 - 1.15, body, ha="left", va="top",
            fontsize=10.5, color="0.15")


def ray_icon(cx, cy, internal=False, short=False):
    """Mini raypath icon: source -> reflector (-> internal bounce) -> receiver."""
    ax.plot([cx - 0.55, cx, cx + 0.55], [cy + 0.5, cy - 0.45, cy + 0.5],
            color="crimson", lw=1.8)
    ax.plot([cx - 0.55, cx + 0.55], [cy + 0.5, cy + 0.5], "o", ms=0)  # keep limits
    if internal:
        ax.plot([cx - 0.55, cx + 0.1, cx + 0.55],
                [cy + 0.5, cy - 0.75, cy + 0.5], color="crimson", lw=1.4, alpha=0.6)
        ax.plot(cx + 0.1, cy - 0.75, "o", ms=9, mfc="none", mec="crimson", mew=2)
    ax.plot(cx, cy - 0.45, "o", ms=9, mfc="none", mec="crimson", mew=2)
    if short:
        for dx in (-0.9, -0.3, 0.3, 0.9):
            ax.plot([cx + dx - 0.12, cx + dx, cx + dx + 0.12],
                    [cy - 0.95, cy - 0.75, cy - 0.95], color="0.4", lw=1.2)


# headers
ax.text(3.0, 9.6, "Axis 1 — where is the extra downward reflection?",
        ha="center", fontsize=13, fontweight="bold", color="0.2")
ax.text(9.0, 9.6, "Axis 2 — what is the period?",
        ha="center", fontsize=13, fontweight="bold", color="0.2")

card(3.0, 6.7, 5.4, 4.4,
     "Surface-related",
     "\u2022 downward reflection at the free surface ($r_0 \\approx -1$)\n"
     "\u2022 water-bottom multiples, peg-legs, reverberations,\n"
     "   surface multiples of deeper reflectors\n"
     "\u2022 strongest family (sea surface is a perfect mirror)\n"
     "\u2022 targets: Radon demultiple, SRME", "crimson")
ray_icon(1.5, 5.6)

card(3.0, 2.6, 5.4, 3.6,
     "Internal (interbed)",
     "\u2022 all downward reflections inside the subsurface\n"
     "\u2022 weaker, but stacks and migrates like primaries\n"
     "\u2022 named by the shallowest downward reflection\n"
     "\u2022 targets: special tools (beyond this course)", "darkorange")
ray_icon(1.5, 1.6, internal=True)

card(9.0, 6.7, 5.4, 4.4,
     "Long-period  (~> 50 ms)",
     "\u2022 separation > wavelet length: separate events\n"
     "\u2022 'deterministic': individually predictable/removable\n"
     "\u2022 deep water, strong water bottom\n"
     "\u2022 targets: Radon demultiple, SRME", "royalblue")
ray_icon(7.5, 5.6)

card(9.0, 2.6, 5.4, 3.6,
     "Short-period  (< wavelet)",
     "\u2022 reverberations hidden inside one wavelet\n"
     "\u2022 interfere with primaries: 'statistical' effect,\n"
     "   acts like a transmission filter\n"
     "\u2022 shallow water, finely layered overburden\n"
     "\u2022 targets: predictive deconvolution ($\\tau$-$p$)", "seagreen")
ray_icon(7.5, 1.6, short=True)

ax.annotate("", xy=(6.0, 0.2), xytext=(6.0, 9.4),
            arrowprops=dict(arrowstyle="-", color="0.6", lw=1.2, ls=":"))

fig.suptitle("Multiple taxonomy: two independent axes — every demultiple method "
             "targets one cell", fontsize=14)
fig.text(0.5, 0.015,
         "Example: a water-bottom reverberation in 40 m of water is "
         "surface-related AND short-period -> tau-p predictive decon; the same "
         "family in 400 m of water is\nsurface-related AND long-period -> Radon "
         "demultiple / SRME. Internal multiples need other tools entirely.",
         ha="center", fontsize=10, color="0.25")
fig.savefig("figures/term02_lec03/term02_lec03_multiple_taxonomy.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec03_multiple_taxonomy.png")
