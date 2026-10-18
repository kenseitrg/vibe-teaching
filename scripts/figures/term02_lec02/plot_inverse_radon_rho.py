"""Figure 11: Inverse Radon -- adjoint alone vs adjoint + rho filter.

Top: a simple gather of four linear events; its round trip through tau-p
via the plain adjoint (smeared, low-frequency-biased wavelets); and via the
adjoint preceded by the rho filter (per-p-trace ramp |f|), which restores
the waveform. Bottom: a single time slice (t = 0.2 s) comparing the three:
the adjoint broadens and tilts the peaks; the rho-filtered inversion
recovers compact wavelets.
"""

import numpy as np
import matplotlib.pyplot as plt

DT, DX, NX, TMAX = 0.004, 12.5, 121, 1.2
EVENTS = [                 # (intercept tau0 [s], slope p [ms/m])
    (0.10, 0.30),
    (0.18, 0.55),
    (0.12, -0.40),
    (0.32, -0.40),
]
T_SLICE = 0.2              # s, slice for the bottom panel


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
    nt = len(t)
    u = np.zeros((nt, len(p_vals)))
    for ip, p in enumerate(p_vals):
        for j in range(len(x)):
            u[:, ip] += np.interp(t + p * x[j], t, data[:, j],
                                  left=0.0, right=0.0)
    return u / len(x)


def rho_filter(traces, dt):
    """Per-trace frequency-domain ramp |f|, normalized at Nyquist."""
    nt = traces.shape[0]
    f = np.fft.fftfreq(nt, d=dt)
    ramp = np.abs(f) / np.abs(f).max()
    return np.real(np.fft.ifft(np.fft.fft(traces, axis=0) * ramp[:, None],
                               axis=0))


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

    fig = plt.figure(figsize=(13, 7))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.25, 1])
    clip = np.percentile(np.abs(data), 99.5)
    panels = [(data, 'input'),
              (rec_adj, 'round trip, adjoint only\n(smeared, LF-biased)'),
              (rec_rho, 'adjoint + rho filter (|f| ramp)\nwaveforms restored')]
    for i, (d, name) in enumerate(panels):
        ax = fig.add_subplot(gs[0, i])
        ax.imshow(d, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
                  extent=[0, x[-1], t[-1], 0])
        ax.axhline(T_SLICE, color='crimson', lw=1.2, ls='--', alpha=0.9)
        ax.set(title=name, xlabel='x (m)')
        if i == 0:
            ax.set_ylabel('t (s)')

    ax = fig.add_subplot(gs[1, :])
    i_sl = int(round(T_SLICE / DT))
    for d, name, c in [(data, 'input', 'k'), (rec_adj, 'adjoint', 'crimson'),
                       (rec_rho, 'adjoint + rho', 'seagreen')]:
        ax.plot(x, d[i_sl] / np.abs(d[i_sl]).max(), color=c, lw=1.4,
                label=name, alpha=0.85)
    ax.set(title=f'time slice t = {T_SLICE} s (normalized)',
           xlabel='x (m)', ylabel='amplitude')
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig('figures/term02_lec02/term02_lec02_inverse_radon_rho.png',
                dpi=150)
    print('wrote term02_lec02_inverse_radon_rho.png')


if __name__ == '__main__':
    main()
