"""Figure 7: Why reflections become ellipses in tau-p.

Left: a single reflection hyperbola (split-spread, symmetric offsets) with
its tangent lines -- every tangent is a (locally) linear event with slope p
and intercept tau = t - p x. Right: the slant-stack (tau-p) image of the
hyperbola: the tangents focus one by one onto the ellipse
tau(p) = t0 sqrt(1 - p^2 V^2), which closes at p = +/-1/V. For comparison,
true linear noise focuses to points far beyond the ellipse (air blast at
1.67 ms/m; ground roll at 3.33 ms/m, off-scale).
"""

import numpy as np
import matplotlib.pyplot as plt

DT, DX = 0.004, 12.5
NX, TMAX = 241, 2.4                 # split spread: x from -1500 to +1500 m
T0, V = 1.0, 2500.0                 # hyperbola: t(x) = sqrt(t0^2 + (x/V)^2)
PMAX = 2.0e-3                       # p axis +/- 2 ms/m


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


def make_gather():
    nt = int(TMAX / DT) + 1
    t = np.arange(nt) * DT
    x = (np.arange(NX) - (NX - 1) / 2) * DX       # symmetric offsets
    wav = ricker(30, 51, DT)
    data = np.zeros((nt, NX))
    times = np.sqrt(T0**2 + (x / V) ** 2)
    for j, tj in enumerate(times):
        i0 = int(np.floor(tj / DT))
        frac = tj / DT - i0
        for off, wt in ((0, 1 - frac), (1, frac)):
            start = i0 + off - (len(wav) - 1) // 2
            lo, hi = max(0, start), min(nt, start + len(wav))
            if hi > lo:
                data[lo:hi, j] += wt * wav[lo - start:hi - start]
    return data, t, x


def slant_stack(data, t, x, p_vals):
    nt = len(t)
    u = np.zeros((nt, len(p_vals)))
    for ip, p in enumerate(p_vals):
        for j in range(len(x)):
            u[:, ip] += np.interp(t + p * x[j], t, data[:, j],
                                  left=0.0, right=0.0)
    return u / len(x)


def main():
    data, t, x = make_gather()
    p_vals = np.linspace(-PMAX, PMAX, 601)
    u = slant_stack(data, t, x, p_vals)

    # tangents of the hyperbola: slope p(x) = x/(V^2 t), intercept tau = t - p x
    x_tan = np.linspace(-1400, 1400, 7)
    t_tan = np.sqrt(T0**2 + (x_tan / V) ** 2)
    p_tan = x_tan / (V**2 * t_tan)
    tau_tan = t_tan - p_tan * x_tan

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    clip = np.percentile(np.abs(data), 99.5)
    axes[0].imshow(data, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
                   extent=[x[0], x[-1], t[-1], 0])
    xx = np.array([x[0], x[-1]])
    for xt, pt, tau_t in zip(x_tan, p_tan, tau_tan):
        axes[0].plot(xx, tau_t + pt * xx, color='crimson', lw=1.0, alpha=0.85)
        axes[0].plot(xt, np.sqrt(T0**2 + (xt / V) ** 2), 'o', color='w',
                     mfc='crimson', ms=5)
    axes[0].set(title='hyperbola = family of tangents\n(each tangent = local '
                'linear event)', xlabel='x (m)', ylabel='t (s)')

    uplot = np.abs(u) / np.abs(u).max()
    axes[1].imshow(20 * np.log10(uplot.T + 1e-3), aspect='auto', cmap='magma',
                   vmin=-25, vmax=0, origin='lower',
                   extent=[0, t[-1], -PMAX * 1e3, PMAX * 1e3])
    p_th = np.linspace(-1 / V, 1 / V, 200)
    axes[1].plot(T0 * np.sqrt(1 - (p_th * V) ** 2), p_th * 1e3, 'w-', lw=2)
    axes[1].plot(tau_tan, p_tan * 1e3, 'o', color='w', mfc='crimson', ms=6)
    axes[1].annotate('apex (t0, 0)', xy=(T0, 0.0), xytext=(1.45, -0.75),
                     color='w', arrowprops=dict(arrowstyle='->', color='w'))
    axes[1].annotate(r'closes at $p=\pm 1/V$' + f' = {1/V*1e3:.2f} ms/m',
                     xy=(0.02, 1 / V * 1e3), xytext=(0.28, 1.55), color='w',
                     arrowprops=dict(arrowstyle='->', color='w'))
    axes[1].annotate('linear noise focuses\nBEYOND the ellipse:\n'
                     'air blast at 1.67 ms/m', xy=(0.30, 1.67), xytext=(1.3, 1.72),
                     color='w', fontsize=9,
                     arrowprops=dict(arrowstyle='->', color='w'))
    axes[1].set(title='tau-p: tangents focus onto the ellipse\n'
                r'$\tau(p)=t_0\sqrt{1-p^2V^2}$',
                xlabel=r'$\tau$ (s)', ylabel='p (ms/m)')
    fig.tight_layout()
    fig.savefig('figures/term02_lec02/term02_lec02_taup_ellipse.png', dpi=150)
    print('wrote term02_lec02_taup_ellipse.png')


if __name__ == '__main__':
    main()
