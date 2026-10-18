"""Figure 3: Reflections as tangent fans in FK; ground roll as a wedge.

Left: the running-example gather with three offset windows (near, mid,
far) on the shallow reflection and their local tangent dips -- flat
near the source, steepening with offset toward the asymptote 1/V.
Right: FK amplitude spectrum. Each windowed segment maps to a
color-matched radial line k = p f; together the tangents sweep out the
reflection fan between the f-axis and the steep far-offset edge. The
ground roll is a steep, low-frequency wedge whose upper frequencies
wrap around +/-k_N (spatial aliasing, Section 3). The FK display floor
is -30 dB so the fan is not drowned in background speckle.

The gather parameters are identical to all term02_lec02 figure scripts.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

# --- running-example parameters (same in all term02_lec02 scripts) ---
DT, DX, NX, TMAX = 0.004, 25.0, 60, 3.0
REFLECTIONS = [(0.8, 2200.0), (1.4, 2600.0), (2.0, 3000.0)]
GR_V, GR_AMP = 300.0, 2.5
AB_V, AB_AMP = 600.0, 1.5

DB_MIN = -30.0                  # FK display floor (hides background speckle)
HALO = [pe.withStroke(linewidth=3.5, foreground='black')]
WINDOWS = [                     # (offset [m], name, color) -- same colors in
    (150, 'near', 'deepskyblue'),   # t-x and in FK, so each segment is
    (700, 'mid', 'orange'),         # traceable to its radial line
    (1300, 'far', 'red'),
]


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
    """Reflections + ground roll + air blast + random noise (the
    lecture's running example, Section 1.3 of the notes)."""
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

    fig, axes = plt.subplots(1, 2, figsize=(12, 6), layout='constrained')

    # ---- left: t-x with the three offset windows and tangent dips
    clip = np.percentile(np.abs(data), 99.5)
    axes[0].imshow(data, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
                   extent=[x[0], x[-1], t[-1], 0])
    t0, v = REFLECTIONS[0]                       # the shallow reflection
    for xw, name, color in WINDOWS:
        tt = np.sqrt(t0**2 + (xw / v) ** 2)
        p_loc = xw / (v * v * tt)                # tangent slope dt/dx, s/m
        axes[0].add_patch(plt.Rectangle((xw - 75, tt - 0.20), 150, 0.40,
                                        fill=False, edgecolor=color, lw=1.5))
        axes[0].plot([xw - 180, xw + 180],
                     [tt - p_loc * 180, tt + p_loc * 180], color=color, lw=2)
        axes[0].text(xw, tt + 0.24, f'{name}\np = {p_loc*1e3:.2f} ms/m',
                     color=color, ha='center', va='bottom', fontsize=8.5)
    axes[0].set(title='t-x: tangent segments of the shallow reflection',
                xlabel='offset x (m)', ylabel='time t (s)')

    # ---- right: FK spectrum with the color-matched radial lines
    ax = axes[1]
    db = 20 * np.log10(amp[sel] / amp[sel].max() + 1e-6)
    im = ax.pcolormesh(k_ax, f_ax[sel], db, cmap='viridis', vmin=DB_MIN,
                       vmax=0, shading='auto')

    def radial_end(p):
        """Where the line k = p f leaves the panel (k = 0.5 or f = 100)."""
        f_exit = 0.5 / (abs(p) * DX)
        return (abs(p) * fmax_plot * DX, fmax_plot) if f_exit > fmax_plot \
            else (0.5, f_exit)

    for xw, name, color in WINDOWS:
        tt = np.sqrt(t0**2 + (xw / v) ** 2)
        p_loc = xw / (v * v * tt)
        k_end, f_end = radial_end(p_loc)
        ax.plot([0.0, k_end], [0.0, f_end], '--', color=color, lw=1.8,
                path_effects=HALO)
        ax.text(k_end - 0.015, min(f_end - 6, 92), name, color=color,
                ha='right', va='top', fontsize=9, path_effects=HALO)

    # fan edge: the steepest tangent = farthest trace, slope -> 1/V
    p_max = x[-1] / (v**2 * np.sqrt(t0**2 + (x[-1] / v) ** 2))
    for p in (p_max, -p_max):
        k_end, f_end = radial_end(p)
        ax.plot([0.0, k_end], [0.0, f_end], 'w--', lw=1.0, alpha=0.9)
    ax.text(0.22, 22, f'fan edge ($p_\\max$ = {p_max*1e3:.2f} ms/m)',
            color='w', fontsize=8.5, path_effects=HALO)

    ax.annotate('reflection fan', xy=(0.12, 58), xytext=(-0.42, 88),
                color='w', fontsize=9, path_effects=HALO,
                arrowprops=dict(arrowstyle='->', color='w'))
    ax.annotate('ground-roll wedge\n(wraps around $\\pm k_N$)',
                xy=(-0.40, 13), xytext=(-0.47, 45), color='w', fontsize=8.5,
                path_effects=HALO,
                arrowprops=dict(arrowstyle='->', color='w'))
    ax.set(title='FK: each segment $\\to$ its radial line $k = pf$',
           xlabel='k (cycles/trace)', ylabel='f (Hz)')
    fig.colorbar(im, ax=ax, label='amplitude (dB)')

    fig.savefig('figures/term02_lec02/term02_lec02_fk_reflection_fan.png',
                dpi=150)
    print('wrote term02_lec02_fk_reflection_fan.png')


if __name__ == '__main__':
    main()
