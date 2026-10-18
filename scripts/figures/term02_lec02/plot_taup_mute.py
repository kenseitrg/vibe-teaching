"""Figure 9: Filtering in tau-p -- a p-mute with QC panels.

Left: the tau-p panel of the running-example gather with a tapered mute
beyond |p| = 0.6 ms/m (past the reflection ellipses, inside the linear
noise). Middle: the gather after mute + inverse transform (adjoint with the
rho filter, Section 8). Right: the difference panel -- the noise model that
was removed: ground roll and air blast, no reflection arcs.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- running-example parameters (same in all term02_lec02 scripts) ---
DT, DX, NX, TMAX = 0.004, 25.0, 60, 3.0
REFLECTIONS = [(0.8, 2200.0), (1.4, 2600.0), (2.0, 3000.0)]
GR_V, GR_AMP = 300.0, 2.5
AB_V, AB_AMP = 600.0, 1.5
PMAX = 4.0e-3


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


def add_event(data, times, wav, amp):
    """Add wavelet `wav` CENTERED at times[j] on trace j (linear
    interpolation between samples; clipped at the record boundaries)."""
    nt, wlen = data.shape[0], len(wav)
    half = (wlen - 1) // 2
    for j, tj in enumerate(times):
        i0 = int(np.floor(tj / DT))
        frac = tj / DT - i0
        for off, w in ((0, 1 - frac), (1, frac)):
            start = i0 + off - half
            lo, hi = max(0, start), min(nt, start + wlen)
            if hi > lo:
                data[lo:hi, j] += amp * wav[lo - start:hi - start] * w



def make_gather(seed=7):
    nt = int(TMAX / DT) + 1
    t = np.arange(nt) * DT
    x = np.arange(1, NX + 1) * DX
    data = np.zeros((nt, NX))
    wav_r, wav_gr, wav_ab = ricker(25, 61, DT), ricker(14, 121, DT), ricker(20, 91, DT)
    for (t0, v), a in zip(REFLECTIONS, (1.0, 0.8, 0.6)):
        add_event(data, np.sqrt(t0**2 + (x / v) ** 2), wav_r, a)
    add_event(data, 0.05 + x / GR_V, wav_gr, GR_AMP)
    add_event(data, 0.10 + x / AB_V, wav_ab, AB_AMP)
    data += 0.08 * np.random.default_rng(seed).standard_normal(data.shape)
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
    """Per-trace frequency-domain ramp |f| (the rho filter of Section 8),
    normalized to unity at Nyquist."""
    nt = traces.shape[0]
    f = np.fft.fftfreq(nt, d=dt)
    ramp = np.abs(f) / np.abs(f).max()
    return np.real(np.fft.ifft(np.fft.fft(traces, axis=0) * ramp[:, None], axis=0))


def adjoint(u, t, x, p_vals):
    """Inverse slant stack: d(t, x) = sum_p u(t - p x, p) dp."""
    nt = len(t)
    dp = p_vals[1] - p_vals[0]
    out = np.zeros((nt, len(x)))
    for j in range(len(x)):
        acc = np.zeros(nt)
        for ip, p in enumerate(p_vals):
            acc += np.interp(t - p * x[j], t, u[:, ip], left=0.0, right=0.0)
        out[:, j] = acc * dp * 1e3     # scale to data amplitude
    return out


def main():
    data, t, x = make_gather()
    p_vals = np.linspace(-PMAX, PMAX, 801)
    u = slant_stack(data, t, x, p_vals)

    # tapered p-mute: keep |p| < 0.6 ms/m, taper off by 0.9 ms/m
    p_ms = p_vals * 1e3
    mute = np.clip((0.9 - np.abs(p_ms)) / 0.3, 0, 1)
    u_muted = u * mute[None, :]

    # inverse (adjoint + rho filter), normalized to input amplitude
    rec = adjoint(rho_filter(u_muted, DT), t, x, p_vals)
    rec *= np.percentile(np.abs(data), 99.5) / np.percentile(np.abs(rec), 99.5)
    diff = data - rec

    fig, axes = plt.subplots(1, 3, figsize=(14, 6),
                             gridspec_kw={'width_ratios': [1, 1, 1]})
    a = np.abs(u) / np.abs(u).max()
    axes[0].imshow(20 * np.log10(a.T + 1e-3), aspect='auto', cmap='magma',
                   vmin=-35, vmax=0, origin='lower',
                   extent=[0, t[-1], -PMAX * 1e3, PMAX * 1e3])
    axes[0].fill_between([0, t[-1]], [0.6, 0.6], [PMAX * 1e3, PMAX * 1e3],
                         color='crimson', alpha=0.25)
    axes[0].fill_between([0, t[-1]], [-PMAX * 1e3, -PMAX * 1e3], [-0.6, -0.6],
                         color='crimson', alpha=0.25)
    axes[0].set(title='tau-p input + mute zone\n(keep |p| < 0.6 ms/m)',
                xlabel=r'$\tau$ (s)', ylabel='p (ms/m)')

    clip = np.percentile(np.abs(data), 99.5)
    for ax, d, name in [(axes[1], rec, 'after mute + inverse\n(adjoint + rho)'),
                        (axes[2], diff, 'difference = noise model')]:
        ax.imshow(d, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
                  extent=[x[0], x[-1], t[-1], 0])
        ax.set(title=name, xlabel='offset x (m)')
    axes[1].set_ylabel('t (s)')
    fig.tight_layout()
    fig.savefig('figures/term02_lec02/term02_lec02_taup_mute.png', dpi=150)
    print('wrote term02_lec02_taup_mute.png')


if __name__ == '__main__':
    main()
