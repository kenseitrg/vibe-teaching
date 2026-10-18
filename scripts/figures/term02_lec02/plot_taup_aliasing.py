"""Figure 9: Aliasing artifacts in the tau-p domain.

Left: the running-example input gather. Middle: slant-stacked with
too-coarse p sampling (dp = 0.4 ms/m, violating dp <= 1/(2 x_max f_max)):
artifacts appear as energy at opposite-sign p and very large tau. Right:
with fine p sampling plus a temporal low-pass filter (the cheap fix), the
panel shows the expected picture: three reflection ellipses and focused
linear noise. Tau-p panels are drawn gather-style (p horizontal, tau down)
like Figure 8, on one shared dB scale (reference: the clean panel's
maximum). The display window (-27 to -5 dB) keeps the aliased energy
(peaking near -22 dB) visible while the interpolation ripple (below
-26 dB) stays dark; only the two brightest noise foci clip at the top.
"""

import numpy as np
from scipy.signal import butter, sosfiltfilt
import matplotlib.pyplot as plt

# --- running-example parameters (same in all term02_lec02 scripts) ---
DT, DX, NX, TMAX = 0.004, 25.0, 60, 3.0
REFLECTIONS = [(0.8, 2200.0), (1.4, 2600.0), (2.0, 3000.0)]
GR_V, GR_AMP = 300.0, 2.5
AB_V, AB_AMP = 600.0, 1.5
PMAX = 4.0e-3                     # p axis +/- 4 ms/m


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


def main():
    data, t, x = make_gather()

    # coarse p sampling (21 values over +/-4 ms/m -> dp = 0.4 ms/m: aliased)
    p_coarse = np.linspace(-PMAX, PMAX, 21)
    u_coarse = slant_stack(data, t, x, p_coarse)

    # cheap fix: low-pass (anti-alias) filter, then fine p sampling
    sos = butter(4, 25.0, 'low', fs=1 / DT, output='sos')
    data_lp = sosfiltfilt(sos, data, axis=0)
    p_fine = np.linspace(-PMAX, PMAX, 801)      # dp = 10 us/m: adequate
    u_fine = slant_stack(data_lp, t, x, p_fine)

    fig, axes = plt.subplots(1, 3, figsize=(14, 5.8), sharey=True,
                             gridspec_kw={'width_ratios': [1, 1, 1]})

    # --- input gather (t-x), same scaling convention as the other figures
    clip = np.percentile(np.abs(data), 99.5)
    axes[0].imshow(data, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
                   extent=[x[0], x[-1], t[-1], 0])
    for onset, v, lbl in [(0.05, GR_V, 'ground roll'),
                          (0.10, AB_V, 'air blast')]:
        x_end = min(x[-1], (TMAX - onset) * v)   # clip line to the record
        axes[0].plot([x[0], x_end], [onset + x[0] / v, onset + x_end / v],
                     ':', color='w', lw=1.0, alpha=0.8)
        x_lbl = (1.55 - onset) * v               # label just above the line
        axes[0].text(x_lbl, 1.48, lbl, color='w', fontsize=8.5)
    axes[0].set_ylim(t[-1], 0)                   # panels fill the full area
    axes[0].set(title='input gather (t-x)', xlabel='offset x (m)',
                ylabel='t (s)')

    # --- tau-p panels, gather-style: p horizontal, tau down (as Fig. 8);
    # one shared dB scale referenced to the clean panel's maximum: the
    # window [-27, -5] dB puts the aliased energy (peaks near -22 dB) at
    # ~20% of the range, keeps the interpolation ripple (< -26 dB) dark,
    # and clips only the two noise foci at the top of the range
    ref = np.abs(u_fine).max()
    for ax, u, pv, title in [
            (axes[1], u_coarse, p_coarse,
             'coarse $\\Delta p$ = 0.4 ms/m (aliased):\n'
             'artifacts at opposite-sign p, large $\\tau$'),
            (axes[2], u_fine, p_fine,
             'fine $\\Delta p$ = 10 $\\mu$s/m + 25 Hz low-pass:\n'
             'expected picture')]:
        ax.imshow(20 * np.log10(np.abs(u) / ref + 1e-6),
                  aspect='auto', cmap='magma', vmin=-30, vmax=-5,
                  extent=[pv[0] * 1e3, pv[-1] * 1e3, t[-1], 0])
        ax.set(title=title, xlabel='p (ms/m)')
    axes[1].set_ylabel(r'$\tau$ (s)')

    # annotations on the aliased panel (artifacts: p < 0, tau beyond events)
    axes[1].annotate('spurious energy:\nopposite-sign p', xy=(-1.6, 1.16),
                     xytext=(-3.9, 0.75), color='w', fontsize=9,
                     arrowprops=dict(arrowstyle='->', color='w'))
    axes[1].annotate('leaked energy at\nvery large $\\tau$', xy=(-0.4, 2.94),
                     xytext=(-3.9, 1.85), color='w', fontsize=9,
                     arrowprops=dict(arrowstyle='->', color='w'))

    # expected locations in the clean panel: ellipses + noise foci
    for (t0, v) in REFLECTIONS:
        p_th = np.linspace(-1 / v, 1 / v, 200)
        axes[2].plot(p_th * 1e3, t0 * np.sqrt(1 - (p_th * v) ** 2), 'w--',
                     lw=1.2, alpha=0.9)
    axes[2].annotate('reflection ellipses\n(apex at $\\tau = t_0$)',
                     xy=(-0.2, 1.2), xytext=(-2.55, 1.85), color='w',
                     fontsize=9, va='top',
                     arrowprops=dict(arrowstyle='->', color='w'))
    for p_ms, tau0 in [(1 / GR_V * 1e3, 0.05), (1 / AB_V * 1e3, 0.10)]:
        axes[2].plot(p_ms, tau0, 'o', ms=9, mfc='none', mew=1.4, color='w')
    axes[2].annotate('ground roll focus', xy=(3.28, 0.09), xytext=(2.0, 0.75),
                     color='w', fontsize=9,
                     arrowprops=dict(arrowstyle='->', color='w'))
    axes[2].annotate('air blast focus', xy=(1.60, 0.14), xytext=(0.45, 0.75),
                     color='w', fontsize=9,
                     arrowprops=dict(arrowstyle='->', color='w'))

    fig.tight_layout()
    fig.savefig('figures/term02_lec02/term02_lec02_taup_aliasing.png',
                dpi=150)
    print('wrote term02_lec02_taup_aliasing.png')


if __name__ == '__main__':
    main()
