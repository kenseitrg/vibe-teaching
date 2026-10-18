"""Figure 10: Filtering in tau-p -- a p-mute with QC panels.

Modified running example: the air blast is low-frequency (6 Hz dominant,
bandwidth ending at ~12 Hz = V_ab/(2 dx) -- right at the aliasing
threshold), hence UNALIASED at dx = 25 m; the ground roll (14 Hz >> 6 Hz
fold) stays aliased. Left: the input gather. Then its tau-p panel
(gather-style: p horizontal, tau down) with a tapered mute beyond
|p| = 0.6 ms/m, the gather after mute + inverse transform (adjoint with
the rho filter, Section 8), and the difference panel -- the removed noise.
The unaliased air blast focuses tightly at p = 1/V and vanishes
completely; the aliased ground roll leaks into the keep zone (its
wrapped 10-16 Hz components stack at |p| < 0.6) and leaves residuals:
dip filtering needs unaliased (or low-passed) data.
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
    wav_r = ricker(25, 61, DT)
    wav_gr = ricker(14, 121, DT)   # 8-20 Hz >> 6 Hz fold: ALIASED at dx=25
    # air blast at 6 Hz: bandwidth ends at ~12 Hz = V_ab/(2 dx) -- exactly
    # the aliasing threshold, so this event is UNALIASED at dx = 25 m
    wav_ab = ricker(6, 301, DT)
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
    clip = np.percentile(np.abs(data), 99.5)
    rec *= clip / np.percentile(np.abs(rec), 99.5)
    diff = data - rec

    fig, axes = plt.subplots(1, 4, figsize=(16.5, 5.8), sharey=True)

    # input gather (t-x), same scaling convention as the other figures;
    # dotted lines mark the two noise events (air blast = the unaliased one)
    axes[0].imshow(data, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
                   extent=[x[0], x[-1], t[-1], 0])
    for onset, v, lbl, xt, yt in [(0.05, GR_V, 'ground roll', 400, 1.02),
                                  (0.10, AB_V, 'air blast', 870, 1.05)]:
        x_end = min(x[-1], (TMAX - onset) * v)   # clip line to the record
        axes[0].plot([x[0], x_end], [onset + x[0] / v, onset + x_end / v],
                     ':', color='w', lw=1.0, alpha=0.8)
        axes[0].text(xt, yt, lbl, color='w', fontsize=8.5)
    axes[0].set_ylim(t[-1], 0)                   # panels fill the full area
    axes[0].set(title='input gather (t-x)', xlabel='offset x (m)',
                ylabel='t (s)')

    # tau-p panel, gather-style: p horizontal, tau down (as Figures 7-9);
    # own-max dB scale with the -25 dB floor above the interpolation ripple
    a = np.abs(u) / np.abs(u).max()
    axes[1].imshow(20 * np.log10(a + 1e-3), aspect='auto', cmap='magma',
                   vmin=-25, vmax=0,
                   extent=[-PMAX * 1e3, PMAX * 1e3, t[-1], 0])
    axes[1].axvspan(-PMAX * 1e3, -0.6, color='crimson', alpha=0.25)
    axes[1].axvspan(0.6, PMAX * 1e3, color='crimson', alpha=0.25)
    axes[1].set(title='tau-p + mute zone\n(keep |p| < 0.6 ms/m)',
                xlabel='p (ms/m)', ylabel=r'$\tau$ (s)')

    for ax, d, name in [(axes[2], rec, 'after mute + inverse\n(adjoint + rho)'),
                        (axes[3], diff, 'difference = noise model')]:
        ax.imshow(d, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
                  extent=[x[0], x[-1], t[-1], 0])
        ax.set(title=name, xlabel='offset x (m)')
    axes[2].set_ylabel('t (s)')

    # the teaching point: unaliased noise vanishes, aliased noise lingers
    axes[2].annotate('residual ground roll:\nwrapped frequencies stack\n'
                     'inside |p| < 0.6', xy=(675, 2.30), xytext=(880, 1.62),
                     color='w', fontsize=9,
                     arrowprops=dict(arrowstyle='->', color='w'))
    axes[3].text(700, 2.18, 'ground roll (partly)', color='w', fontsize=8.5)
    axes[3].text(950, 1.55, 'air blast (fully)', color='w', fontsize=8.5)
    fig.tight_layout()
    fig.savefig('figures/term02_lec02/term02_lec02_taup_mute.png', dpi=150)
    print('wrote term02_lec02_taup_mute.png')


if __name__ == '__main__':
    main()
