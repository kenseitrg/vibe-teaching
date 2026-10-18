"""Figure 5: the four standard FK filter masks.

One mask per panel, in the (f, k) plane of the running example
(dx = 25 m, so k_N = 0.5 cyc/trace). Blue = pass, red = reject,
cosine-tapered transitions between (the 2-D Gibbs remedy). Dashed
guides mark each mask's design boundaries: the k_cut of the
anti-alias cut, the slope limits of the dip-pass fan, the air-blast
slope of the narrow dip-reject, and the 30 Hz floor of the polygonal
mask with low-frequency protection: the reject wedge is bounded
by 30 Hz (where the noise lives), and a corridor around k = 0 at
very low f is left unattenuated -- a dip cut that pinches to the
origin would otherwise remove the very low frequencies near zero
wavenumber.

The application of the dip fan to the gather is a separate figure
(plot_fk_filter_application.py).
"""

import numpy as np
import matplotlib.pyplot as plt

# --- running-example parameters (same in all term02_lec02 scripts) ---
DT, DX, NX, TMAX = 0.004, 25.0, 60, 3.0
AB_V = 600.0                     # air-blast velocity (m/s)

F_PLOT = np.linspace(0.0, 100.0, 401)      # display grid, Hz
K_PLOT = np.linspace(-0.5, 0.5, 401)       # display grid, cyc/trace


def taper_edge(coord, lo, hi):
    """Cosine taper of the mask from 1 inside [lo, hi] to 0 outside
    (1-D helper broadcast along one axis)."""
    ramp = np.ones_like(coord)
    below, above = coord < lo, coord > hi
    width = max(abs(hi - lo), 1e-12)
    ramp[below] = 0.5 * (1 + np.cos(np.pi * np.clip((coord[below] - lo) / width, -1, 0)))
    ramp[above] = 0.5 * (1 + np.cos(np.pi * np.clip((coord[above] - hi) / width, 0, 1)))
    return ramp


def build_masks(f, k_cpt):
    """Four standard FK masks on the (f, k) grid. f in Hz (>= 0), k in
    cycles/trace. Returns an ordered list of (title, mask, guides,
    labels); guides are (kind, value) pairs for the dashed design
    guides, labels are (x, f, ha, text) annotation tuples."""
    F, K = np.meshgrid(f, k_cpt, indexing='ij')
    p_eff = np.where(F > 1.0, K / np.maximum(F, 1.0) / DX, 0.0)   # s/m
    items = []

    # 1. k-cut: pass |k| <= 0.25 cyc/trace, tapered towards the k_N edges
    kcut = taper_edge(k_cpt, -0.25, 0.25)[None, :] * np.ones_like(K)
    items.append(('1. k-cut (anti-alias)', kcut,
                  [('v', -0.25), ('v', 0.25)],
                  [(-0.02, 88, 'right', '$|k| = 0.25$ cyc/trace')]))

    # 2. dip-pass fan: full pass for |p| < 0.45 ms/m (beyond the steepest
    #    reflection dip), full reject beyond 0.60 ms/m, taper between
    fan = np.clip((0.60e-3 - np.abs(p_eff)) / 0.15e-3, 0, 1)
    fan[F < 1.0] = 1.0                      # do not filter near-zero freq
    items.append(('2. dip-pass fan', fan,
                  [('p', 0.45e-3), ('p', 0.60e-3)],
                  [(-0.47, 88, 'left',
                    'fan edges:\n$p = 0.45$ and $0.60$ ms/m')]))

    # 3. narrow dip-reject around the air-blast slope p = 1/600 s/m
    reject = np.clip(1 - np.abs(np.abs(p_eff) - 1 / AB_V) / 0.15e-3, 0, 1)
    items.append(('3. narrow dip-reject', 1.0 - reject * (F > 3.0),
                  [('p', 1 / AB_V - 0.15e-3), ('p', 1 / AB_V + 0.15e-3)],
                  [(0.0, 55, 'center',
                    'air blast:\n$p \\approx 1/%d$ s/m' % AB_V)]))

    # 4. polygonal + low-f protection: reject the steep (ground-roll)
    #    wedge only below 30 Hz (the noise's (dip, f) combination), and
    #    keep a protected corridor around k = 0 at very low f -- the fan
    #    pinches to the origin there and would cut the very low
    #    frequencies near zero wavenumber
    steep = np.clip((np.abs(p_eff) - 0.8e-3) / 0.2e-3, 0, 1)
    lfp = np.clip((30.0 - F) / 8.0, 0, 1)   # reject strength fades by 30 Hz
    k_corr = np.clip((0.18 - np.abs(K)) / 0.10, 0, 1)  # corridor around k=0
    f_corr = np.clip((14.0 - F) / 6.0, 0, 1)           # only below ~14 Hz
    items.append(('4. polygonal + low-f protection',
                  1.0 - steep * lfp * (1.0 - k_corr * f_corr),
                  [('p', 0.8e-3), ('p', 1.0e-3), ('h', 30.0),
                   ('kv', (0.10, 14.0))],
                  [(0.0, 62, 'center', 'steep dips rejected\nbelow 30 Hz'),
                   (0.0, 10, 'center', 'low-f corridor')]))
    return items


def radial_segment(p):
    """Endpoints (k, f) of the radial line k = p f dx from the origin to
    the panel boundary."""
    f_top = 0.5 / (abs(p) * DX)             # f where |k| reaches 0.5
    if f_top <= F_PLOT[-1]:
        return [0.0, p * f_top * DX], [0.0, f_top]
    return [0.0, p * F_PLOT[-1] * DX], [0.0, F_PLOT[-1]]


def draw_guides(ax, guides):
    for kind, val in guides:
        if kind == 'v':
            ax.axvline(val, color='0.15', ls='--', lw=1.0)
        elif kind == 'h':
            ax.axhline(val, color='0.15', ls='--', lw=1.0)
        elif kind == 'kv':               # short vertical segment, f = 0..ftop
            kval, ftop = val
            for sign in (1.0, -1.0):
                ax.plot([sign * kval] * 2, [0.0, ftop], color='0.15',
                        ls='--', lw=1.0)
        elif kind == 'p':
            for sign in (1.0, -1.0):
                kk, ff = radial_segment(sign * val)
                ax.plot(kk, ff, color='0.15', ls='--', lw=1.0)


def main():
    items = build_masks(F_PLOT, K_PLOT)
    fig, axes = plt.subplots(2, 2, figsize=(10, 7.5), layout='constrained')
    bbox = dict(facecolor='white', alpha=0.85, edgecolor='none', pad=1.5)

    for ax, (name, mask, guides, labels) in zip(axes.ravel(), items):
        im = ax.pcolormesh(K_PLOT, F_PLOT, mask, cmap='RdBu', vmin=0, vmax=1,
                           shading='auto')
        draw_guides(ax, guides)
        for lx, lf, ha, txt in labels:
            ax.text(lx, lf, txt, fontsize=9, ha=ha, va='top', color='0.15',
                    bbox=bbox)
        ax.set(title=name, xlabel='k (cyc/trace)', ylabel='f (Hz)',
               xlim=(-0.5, 0.5), ylim=(0, 100))

    fig.colorbar(im, ax=axes, shrink=0.85, pad=0.02,
                 label='mask value (1 = pass, 0 = reject)')
    fig.suptitle('The four standard FK filter masks: pass (blue), '
                 'reject (red), tapered edges')
    fig.savefig('figures/term02_lec02/term02_lec02_fk_filter_types.png',
                dpi=150)
    print('wrote term02_lec02_fk_filter_types.png')


if __name__ == '__main__':
    main()
