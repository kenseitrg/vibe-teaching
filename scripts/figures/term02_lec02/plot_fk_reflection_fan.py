"""Figure 3: Reflections as tangent fans in FK; ground roll as a wedge.

Left: the running-example gather with near/mid/far offset windows and the
local tangent dips of a reflection inside each window. Right: FK amplitude
spectrum. Reflection energy fills a fan between the steepest near-offset
dips and the flat asymptote; ground roll is a steep, low-frequency wedge
whose upper frequencies wrap around +/-k_N (spatial aliasing, Section 3).

The gather parameters are identical to all term02_lec02 figure scripts.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- running-example parameters (same in all term02_lec02 scripts) ---
DT, DX, NX, TMAX = 0.004, 25.0, 60, 3.0
REFLECTIONS = [(0.8, 2200.0), (1.4, 2600.0), (2.0, 3000.0)]
GR_V, GR_AMP = 300.0, 2.5
AB_V, AB_AMP = 600.0, 1.5


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
    """Reflections + ground roll + air blast + random noise (same as Fig. 1)."""
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


def fk_amp(data):
    """FK amplitude, convention e^{-i2pi(ft-kx)}: event of slope p -> line k=pf."""
    F = np.fft.fft(data, axis=0)
    D = np.fft.ifft(F, axis=1)
    return np.abs(np.fft.fftshift(D))


def main():
    data, t, x = make_gather()
    nt = len(t)
    amp = fk_amp(data)
    f_ax = np.fft.fftshift(np.fft.fftfreq(nt, d=DT))
    k_ax = np.fft.fftshift(np.fft.fftfreq(NX, d=DX)) * DX    # cycles/trace
    fmax_plot = 100.0
    sel = (f_ax >= 0) & (f_ax <= fmax_plot)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    clip = np.percentile(np.abs(data), 99.5)
    axes[0].imshow(data, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
                   extent=[x[0], x[-1], t[-1], 0])
    # offset windows with local tangent dips of the shallow reflection
    t0, v = REFLECTIONS[0]
    for xw, c in [(150, 'royalblue'), (700, 'seagreen'), (1300, 'crimson')]:
        tt = np.sqrt(t0**2 + (xw / v) ** 2)
        p_loc = xw / (v * v * tt)                     # tangent slope dt/dx
        axes[0].add_patch(plt.Rectangle((xw - 75, 0.38), 150, 0.55,
                                        fill=False, edgecolor=c, lw=1.4))
        axes[0].plot([xw - 200, xw + 200],
                     [tt - p_loc * 200, tt + p_loc * 200], color=c, lw=2)
        axes[0].text(xw, 0.33, f'p={p_loc*1e3:.2f} ms/m', color=c,
                     ha='center', fontsize=9)
    axes[0].set(title='t-x with near/mid/far tangent dips',
                xlabel='offset x (m)', ylabel='time t (s)')

    db = 20 * np.log10(amp[sel] / amp[sel].max() + 1e-6)
    im = axes[1].pcolormesh(k_ax, f_ax[sel], db, cmap='magma',
                            vmin=-50, vmax=0, shading='auto')
    p_steep = x[-1] / (v**2 * np.sqrt(t0**2 + (x[-1] / v) ** 2))
    for p in (p_steep, -p_steep):
        axes[1].plot([-p * DX * fmax_plot, p * DX * fmax_plot],
                     [0, fmax_plot], 'w--', lw=1.0)
    axes[1].annotate('reflection fan', xy=(25, 55), xytext=(2, 88),
                     color='w', arrowprops=dict(arrowstyle='->', color='w'))
    axes[1].annotate('ground-roll wedge\n(wraps around +/-0.5)',
                     xy=(-0.42, 12), xytext=(-0.48, 55), color='crimson',
                     arrowprops=dict(arrowstyle='->', color='crimson'))
    axes[1].text(p_steep * DX * fmax_plot * 0.95, fmax_plot * 0.9,
                 f'p={p_steep*1e3:.2f}', color='w', ha='right')
    axes[1].set(title='FK spectrum: fans and wedge',
                xlabel='k (cycles/trace)', ylabel='f (Hz)')
    fig.colorbar(im, ax=axes[1], label='amplitude (dB)')
    fig.tight_layout()
    fig.savefig('figures/term02_lec02/term02_lec02_fk_reflection_fan.png',
                dpi=150)
    print('wrote term02_lec02_fk_reflection_fan.png')


if __name__ == '__main__':
    main()
