"""Figure 2: Plane waves in t-x and their FK radial lines.

Left: three linear events (plane waves) of different dips in t-x.
Right: the FK amplitude spectrum: each event maps to a radial line through
the origin with p = k/f (slope relation of Section 2.2). The steepest event
(p = 0.8 ms/m) reaches exactly +0.5 cycles/trace at 50 Hz -- the spatial
Nyquist of this sampling: no steeper dip could be represented unaliased.
"""

import numpy as np
import matplotlib.pyplot as plt

DT, DX = 0.004, 12.5
NX, TMAX = 121, 1.8
F_DOM = 30.0                     # Hz (band ~15-50 Hz, fills the FK display)
EVENTS = [                       # (intercept tau0 [s], slope p [ms/m], amp)
    (0.10, 0.25, 1.0),
    (0.42, 0.50, 1.0),
    (0.20, 0.80, 1.0),
]
FMAX_PLOT = 50.0                 # Hz, top of the FK display


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


def build_event(t, x, tau0, p_ms, amp=1.0):
    """One linear event d(t,x) = amp * s(t - p x) with a Ricker wavelet s,
    centered on the arrival times."""
    nt, wav = len(t), ricker(F_DOM, 51, DT)
    data = np.zeros((nt, NX))
    times = tau0 + p_ms * 1e-3 * x
    for j, tj in enumerate(times):
        i0 = int(np.floor(tj / DT))
        frac = tj / DT - i0
        for off, wt in ((0, 1 - frac), (1, frac)):
            start = i0 + off - (len(wav) - 1) // 2
            lo, hi = max(0, start), min(nt, start + len(wav))
            if hi > lo:
                data[lo:hi, j] += wt * amp * wav[lo - start:hi - start]
    return data


def fk_amp(data):
    """2-D FK amplitude with the e^{-i2pi(ft - kx)} convention so that a
    positive-slope event lands on the line k = +p f."""
    F = np.fft.fft(data, axis=0)          # over t: e^{-i2pi f t}
    D = np.fft.ifft(F, axis=1)            # over x: e^{+i2pi k x}
    return np.abs(np.fft.fftshift(D))


def main():
    nt = int(TMAX / DT) + 1
    t = np.arange(nt) * DT
    x = np.arange(NX) * DX
    data = sum(build_event(t, x, tau0, p_ms) for tau0, p_ms, _ in EVENTS)

    amp = fk_amp(data)
    f_ax = np.fft.fftshift(np.fft.fftfreq(nt, d=DT))
    k_ax = np.fft.fftshift(np.fft.fftfreq(NX, d=DX)) * DX   # cycles/trace
    sel = (f_ax >= 0) & (f_ax <= FMAX_PLOT)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
    clip = np.percentile(np.abs(data), 99.5)
    axes[0].imshow(data, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
                   extent=[0, x[-1], t[-1], 0])
    for tau0, p_ms, _ in EVENTS:
        axes[0].plot(x, tau0 + p_ms * 1e-3 * x, color='crimson', lw=1.2,
                     alpha=0.8)
    axes[0].set_ylim(t[-1], 0)
    axes[0].set(title='t-x: three plane waves', xlabel='x (m)', ylabel='t (s)')

    db = 20 * np.log10(amp[sel] / amp[sel].max() + 1e-6)
    im = axes[1].pcolormesh(k_ax, f_ax[sel], db, cmap='magma',
                            vmin=-45, vmax=0, shading='auto')
    for _, p_ms, _ in EVENTS:
        k_end = p_ms * 1e-3 * FMAX_PLOT * DX          # k = p f, cyc/trace
        axes[1].plot([0, k_end], [0, FMAX_PLOT], 'w--', lw=1.0, alpha=0.85)
        axes[1].text(k_end * 0.93, FMAX_PLOT * 0.90, f'p={p_ms:.2f}',
                     color='w', ha='right', fontsize=9)
    axes[1].text(-0.49, 47, 'p=0.80 ends at k=+0.5\n(spatial Nyquist at '
                 'this dx)', color='w', fontsize=8, va='top')
    axes[1].set(title='FK spectrum: p = k/f radial lines',
                xlabel='k (cycles/trace)', ylabel='f (Hz)')
    fig.colorbar(im, ax=axes[1], label='amplitude (dB)')
    fig.tight_layout()
    fig.savefig('figures/term02_lec02/term02_lec02_fk_plane_wave.png', dpi=150)
    print('wrote term02_lec02_fk_plane_wave.png')


if __name__ == '__main__':
    main()
