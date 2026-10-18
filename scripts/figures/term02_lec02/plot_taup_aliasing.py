"""Figure 9: Aliasing artifacts in the tau-p domain.

Left: the running-example gather slant-stacked with too-coarse p sampling
(dp = 0.2 ms/m, violating dp <= 1/(2 x_max f_max)): artifacts appear as
energy at opposite-sign p and very large tau. Right: with fine p sampling
plus a temporal low-pass filter (the cheap fix), the panel shows the
expected picture: three reflection ellipses and focused linear noise.
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

    # coarse p sampling (41 values over +/-4 ms/m -> dp = 0.2 ms/m: aliased)
    p_coarse = np.linspace(-PMAX, PMAX, 41)
    u_coarse = slant_stack(data, t, x, p_coarse)

    # cheap fix: low-pass (anti-alias) filter, then fine p sampling
    sos = butter(4, 25.0, 'low', fs=1 / DT, output='sos')
    data_lp = sosfiltfilt(sos, data, axis=0)
    p_fine = np.linspace(-PMAX, PMAX, 801)      # dp = 10 us/m: adequate
    u_fine = slant_stack(data_lp, t, x, p_fine)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)
    for ax, u, pv, title in [
            (axes[0], u_coarse, p_coarse,
             'coarse dp = 0.2 ms/m:\nartifacts at opposite-sign p, large tau'),
            (axes[1], u_fine, p_fine,
             'fine dp = 10 us/m + 25 Hz low-pass:\nellipses + focused noise')]:
        a = np.abs(u) / np.abs(u_fine).max()
        ax.imshow(20 * np.log10(a.T + 1e-3), aspect='auto', cmap='magma',
                  vmin=-35, vmax=0, origin='lower',
                  extent=[0, t[-1], pv[0] * 1e3, pv[-1] * 1e3])
        ax.set(title=title, xlabel=r'$\tau$ (s)')
    axes[0].set_ylabel('p (ms/m)')

    # annotations
    axes[0].annotate('spurious energy,\nopposite-sign p', xy=(2.6, -1.9),
                     xytext=(1.15, -3.4), color='w',
                     arrowprops=dict(arrowstyle='->', color='w'))
    axes[0].annotate('very large tau', xy=(2.85, 2.6), xytext=(1.3, 3.3),
                     color='w', arrowprops=dict(arrowstyle='->', color='w'))
    # expected locations in the clean panel
    for p_ms, lbl, c in [(1 / AB_V * 1e3, 'air blast', 'w'),
                         (-1 / AB_V * 1e3, '', 'w'),
                         (1 / GR_V * 1e3, 'ground roll', 'w'),
                         (-1 / GR_V * 1e3, '', 'w')]:
        axes[1].axhline(p_ms, color=c, ls=':', lw=0.8, alpha=0.7)
        if lbl:
            axes[1].text(2.95, p_ms + 0.12, lbl, color='w', fontsize=9,
                         ha='right')
    for (t0, v), c in zip(REFLECTIONS, ['w'] * 3):
        axes[1].plot([t0, t0], [-1 / v * 1e3, 1 / v * 1e3], color=c, lw=1.2,
                     alpha=0.9)
    axes[1].text(0.82, 0.0, 'ellipses close\nby |p| = 1/V', color='w',
                 fontsize=9, ha='left', va='center')
    fig.tight_layout()
    fig.savefig('figures/term02_lec02/term02_lec02_taup_aliasing.png',
                dpi=150)
    print('wrote term02_lec02_taup_aliasing.png')


if __name__ == '__main__':
    main()
