"""Figure 12: the inverse Radon rho filter, in t-x and in tau-p.

Top row: the t-x round trip -- input, adjoint-only reconstruction
(smeared, low-frequency-flavored), adjoint + rho filter. Middle row:
the same three datasets viewed in tau-p (the round trips are
forward-transformed back) -- where the input's linear events are
focused points on an empty background, so the adjoint's 1/|f| smear
cannot hide along event lines (the demo structure of the reference
notebook). The rho filter (per-p-trace |f| ramp, Gaussian-tapered
toward Nyquist) restores the points. Bottom: a tau slice (tau = 0.55
s) across p on a common amplitude scale: without rho the spikes lose
height and broaden; with rho the input slice is recovered.
"""

import numpy as np
import matplotlib.pyplot as plt

DT, DX, NX, TMAX = 0.004, 12.5, 121, 1.6
F_DOM = 15.0             # Hz -- low enough that the 1/|f| bias bites
EVENTS = [                 # (intercept tau0 [s], slope p [ms/m])
    (0.55, 0.30),          # three events on one tau row: the slice cuts
    (0.55, 0.55),          # all three peaks cleanly; tau0 chosen so no
    (0.55, -0.35),         # event is clipped at the record edges
    (1.05, -0.35),         # far in tau: contributes tails to the slice
]
T_SLICE = 0.55             # s, tau-slice for the bottom panel


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


def make_gather():
    nt = int(TMAX / DT) + 1
    t = np.arange(nt) * DT
    x = np.arange(1, NX + 1) * DX
    wav = ricker(F_DOM, 81, DT)
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
    nt = len(t)
    u = np.zeros((nt, len(p_vals)))
    for ip, p in enumerate(p_vals):
        for j in range(len(x)):
            u[:, ip] += np.interp(t + p * x[j], t, data[:, j],
                                  left=0.0, right=0.0)
    return u / len(x)


def rho_filter(traces, dt):
    """Per-p-trace rho filter: |f| ramp with a gentle Gaussian taper
    toward Nyquist (exp(-(f/f_N)^2)), which keeps interpolation noise in
    the top octave from being boosted -- the taper is critical for a
    clean result. Real-FFT form, as in the reference notebook."""
    nt = traces.shape[0]
    freqs = np.fft.rfftfreq(nt, d=dt)
    ramp = np.abs(freqs) / (8 * np.pi)       # |w| = 2*pi*|f|, scaled
    taper = np.exp(-(freqs / freqs.max()) ** 2)
    F = np.fft.rfft(traces, axis=0)
    return np.fft.irfft(F * (ramp * taper)[:, None], n=nt, axis=0)


def adjoint(u, t, x, p_vals, scale):
    nt = len(t)
    dp = p_vals[1] - p_vals[0]
    out = np.zeros((nt, len(x)))
    for j in range(len(x)):
        acc = np.zeros(nt)
        for ip, p in enumerate(p_vals):
            acc += np.interp(t - p * x[j], t, u[:, ip], left=0.0, right=0.0)
        out[:, j] = acc * dp * scale
    return out


def match_scale(target, rec):
    """Normalize reconstruction amplitude to the target (the overall Radon
    constant is arbitrary; shape comparison is the point)."""
    return rec * (np.percentile(np.abs(target), 99.9) /
                  np.percentile(np.abs(rec), 99.9))


def main():
    data, t, x = make_gather()
    p_vals = np.linspace(-2.0e-3, 2.0e-3, 601)   # dp = 6.7 us/m: adequate
    u = slant_stack(data, t, x, p_vals)

    rec_adj = match_scale(data, adjoint(u, t, x, p_vals, 1e3))
    rec_rho = match_scale(data, adjoint(rho_filter(u, DT), t, x, p_vals, 1e3))

    # forward-transform both round trips back to tau-p, where the input
    # events are focused points on an empty background and the 1/|f|
    # smear of the plain adjoint is impossible to miss
    u_rt_adj = slant_stack(rec_adj, t, x, p_vals)
    u_rt_rho = slant_stack(rec_rho, t, x, p_vals)

    # display window: events at |p| <= 0.55 ms/m, tau 0.55 and 1.05 s
    j0, j1 = np.searchsorted(p_vals * 1e3, (-0.8, 0.8))
    i0d, i1 = int(round(0.35 / DT)), int(round(1.25 / DT)) + 1
    p_ms = p_vals * 1e3

    fig = plt.figure(figsize=(13, 10), layout='constrained')
    gs = fig.add_gridspec(3, 3, height_ratios=[1.0, 1.0, 0.7])

    # ---- top row: the t-x round trip
    clip_tx = np.percentile(np.abs(data), 99.5)
    tx = [(data, 'input'),
          (rec_adj, 'without rho (adjoint only)'),
          (rec_rho, 'with rho filter')]
    for i, (d, name) in enumerate(tx):
        ax = fig.add_subplot(gs[0, i])
        ax.imshow(d, aspect='auto', cmap='gray', vmin=-clip_tx, vmax=clip_tx,
                  extent=[x[0], x[-1], t[-1], 0])
        ax.set(title=name, xlabel='x (m)')
        if i == 0:
            ax.set_ylabel('t (s)')

    # ---- middle row: the same three datasets in tau-p (round trips
    #      forward-transformed back, so the smear cannot hide)
    panels = [
        (u[i0d:i1, j0:j1], 'in tau-p: focused points',
         0.6 * np.abs(u[i0d:i1, j0:j1]).max()),
        (u_rt_adj[i0d:i1, j0:j1], 'in tau-p: smeared along tau',
         np.percentile(np.abs(u_rt_adj[i0d:i1, j0:j1]), 99.5)),
        (u_rt_rho[i0d:i1, j0:j1], 'in tau-p: restored',
         np.percentile(np.abs(u_rt_rho[i0d:i1, j0:j1]), 99.5)),
    ]
    for i, (d, name, clip) in enumerate(panels):
        ax = fig.add_subplot(gs[1, i])
        ax.imshow(d, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
                  extent=[p_ms[j0], p_ms[j1], i1 * DT, i0d * DT])
        ax.axhline(T_SLICE, color='crimson', lw=1.2, ls='--', alpha=0.9)
        ax.set(title=name, xlabel='p (ms/m)')
        if i == 0:
            ax.set_ylabel(r'$\tau$ (s)')

    ax = fig.add_subplot(gs[2, :])
    i_sl = int(round(T_SLICE / DT))
    scale = np.abs(u[i_sl, j0:j1]).max()      # common amplitude scale
    for d, name, c in [(u, 'input', 'k'),
                       (u_rt_adj, 'without rho', 'crimson'),
                       (u_rt_rho, 'with rho', 'seagreen')]:
        ax.plot(p_ms[j0:j1], d[i_sl, j0:j1] / scale, color=c, lw=1.4,
                label=name, alpha=0.85)
    ax.set(title=rf'tau slice $\tau$ = {T_SLICE} s (common scale)',
           xlabel='p (ms/m)', ylabel='amplitude')
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(alpha=0.3)
    fig.savefig('figures/term02_lec02/term02_lec02_inverse_radon_rho.png',
                dpi=150)
    print('wrote term02_lec02_inverse_radon_rho.png')


if __name__ == '__main__':
    main()
