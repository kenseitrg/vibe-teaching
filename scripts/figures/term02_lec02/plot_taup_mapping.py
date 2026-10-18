"""Figure 7: Slant stacking -- how events map into tau-p.

Left: three linear events in t-x, with the summation trajectory (white)
highlighted on one event only. Middle: after LMO with the slope that
matches that event, it is flat -- the sum over offsets then spikes. Right:
the tau-p panel, gather-style (p horizontal, tau down): each linear event
focuses to one point at (p0, tau0).
"""

import numpy as np
import matplotlib.pyplot as plt

DT, DX, NX, TMAX = 0.004, 12.5, 121, 1.6
EVENTS = [                 # (intercept tau0 [s], slope p [ms/m])
    (0.10, 0.30),
    (0.42, 0.55),
    (0.20, -0.45),
]


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


def make_gather():
    nt = int(TMAX / DT) + 1
    t = np.arange(nt) * DT
    x = np.arange(1, NX + 1) * DX
    wav = ricker(25, 51, DT)
    data = np.zeros((nt, NX))
    for tau0, p_ms in EVENTS:
        times = tau0 + p_ms * 1e-3 * x
        for j, tj in enumerate(times):
            i0 = int(np.floor(tj / DT))
            frac = tj / DT - i0
            for off, wt in ((0, 1 - frac), (1, frac)):
                start = i0 + off - (len(wav) - 1) // 2
                lo = max(0, start)
                hi = min(nt, start + len(wav))
                if hi > lo:
                    data[lo:hi, j] += wt * wav[lo - start:hi - start]
    return data, t, x


def slant_stack(data, t, x, p_vals):
    """Forward tau-p: u(tau, p) = sum_j d(tau + p x_j, x_j), linear interp."""
    nt = len(t)
    u = np.zeros((nt, len(p_vals)))
    for ip, p in enumerate(p_vals):
        for j in range(len(x)):
            u[:, ip] += np.interp(t + p * x[j], t, data[:, j],
                                  left=0.0, right=0.0)
    return u / len(x)


def main():
    data, t, x = make_gather()
    tau_m, p_m = EVENTS[1]                  # the event that gets flattened
    p_match = p_m * 1e-3                    # its slope [s/m]

    # LMO-corrected gather with the matching slope
    lmo = np.zeros_like(data)
    for j in range(len(x)):
        lmo[:, j] = np.interp(t + p_match * x[j], t, data[:, j],
                              left=0.0, right=0.0)

    # 481 samples: grid step 0.005 ms/m hits all three event slopes exactly
    p_vals = np.linspace(-1.2e-3, 1.2e-3, 481)      # fine enough (no p-alias)
    u = slant_stack(data, t, x, p_vals)

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.6), sharey=True)
    clip = np.percentile(np.abs(data), 99.5)

    # t-x: only the flattened event carries the summation line
    axes[0].imshow(data, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
                   extent=[x[0], x[-1], t[-1], 0])
    xx = np.array([x[0], x[-1]])           # trimmed to the actual offsets
    axes[0].plot(xx, tau_m + p_match * xx, 'w-', lw=2.2, alpha=0.9)
    axes[0].set_ylim(t[-1], 0)             # no white space above t = 0
    axes[0].set(title=f't-x: summation line (white)\non the event with '
                f'p = {p_m:.2f} ms/m', xlabel='x (m)', ylabel='t (s)')

    axes[1].imshow(lmo, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
                   extent=[x[0], x[-1], t[-1], 0])
    axes[1].axhline(tau_m, color='w', ls='--', lw=1.2)
    axes[1].set(title='after LMO with matching p:\nevent flat, sums in phase',
                xlabel='x (m)', ylabel=r'$\tau$ (s)')

    # tau-p, gather-style: p horizontal, tau down (as Figures 8-9);
    # markers at (p0, tau0) sit exactly on the focused points
    uplot = np.abs(u) / np.abs(u).max()
    axes[2].imshow(20 * np.log10(uplot + 1e-3), aspect='auto', cmap='magma',
                   vmin=-40, vmax=0, extent=[p_vals[0] * 1e3,
                                             p_vals[-1] * 1e3, t[-1], 0])
    for tau0, p_ms in EVENTS:
        axes[2].plot(p_ms, tau0, 'wo', ms=7, mfc='none', mew=2)
        axes[2].annotate(f'({tau0:.2f} s, {p_ms:+.2f})', (p_ms, tau0),
                         textcoords='offset points', xytext=(12, 8),
                         color='w', fontsize=9)
    axes[2].set(title='tau-p: linear events -> points',
                xlabel='p (ms/m)', ylabel=r'$\tau$ (s)')
    fig.tight_layout()
    fig.savefig('figures/term02_lec02/term02_lec02_taup_mapping.png',
                dpi=150)
    print('wrote term02_lec02_taup_mapping.png')


if __name__ == '__main__':
    main()
