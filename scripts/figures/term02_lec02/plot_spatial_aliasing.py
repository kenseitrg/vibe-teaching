"""Figure 4: Spatial aliasing of a steep linear event.

The same ground-roll-like event (apparent velocity 500 m/s, ~8-40 Hz band)
recorded at two trace spacings. At dx = 6.25 m the spatial Nyquist
k_N = 1/(2 dx) is high enough: the event lies on one radial line in FK.
At dx = 25 m the alias frequency f_alias = V_app/(2 dx) = 10 Hz falls inside
the band: above it the apparent dip flips trace-to-trace and the FK energy
wraps repeatedly around +/-k_N into the reflection dips.
"""

import numpy as np
import matplotlib.pyplot as plt

DT = 0.004
TMAX = 1.6
V_APP = 500.0          # m/s
F_DOM = 18.0           # Hz, Ricker dominant frequency (band ~8-40 Hz)


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


def make_event(dx, xmax):
    nx = int(xmax / dx)
    x = np.arange(1, nx + 1) * dx
    nt = int(TMAX / DT) + 1
    t = np.arange(nt) * DT
    wav = ricker(F_DOM, 81, DT)
    data = np.zeros((nt, nx))
    times = 0.06 + x / V_APP
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


def fk_amp(data):
    F = np.fft.fft(data, axis=0)
    D = np.fft.ifft(F, axis=1)
    return np.abs(np.fft.fftshift(D))


def main():
    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    for col, (dx, label) in enumerate([(6.25, 'dx = 6.25 m  (f_alias = 40 Hz)'),
                                       (25.0, 'dx = 25 m  (f_alias = 10 Hz)')]):
        data, t, x = make_event(dx, 1500.0)
        nt, nx = data.shape
        clip = np.percentile(np.abs(data), 99.5)
        ax = axes[0, col]
        ax.imshow(data, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
                  extent=[0, x[-1], t[-1], 0])
        ax.set(title=f'{label}', xlabel='x (m)', ylabel='t (s)')
        if col == 1:
            ax.annotate('apparent dip flips\nabove f_alias = 10 Hz',
                        xy=(620, 0.62), xytext=(820, 1.25), color='crimson',
                        fontsize=9,
                        arrowprops=dict(arrowstyle='->', color='crimson'))

        amp = fk_amp(data)
        f_ax = np.fft.fftshift(np.fft.fftfreq(nt, d=DT))
        k_ax = np.fft.fftshift(np.fft.fftfreq(nx, d=dx)) * dx  # cycles/trace
        sel = f_ax <= 60
        db = 20 * np.log10(amp[sel] / amp[sel].max() + 1e-6)
        ax = axes[1, col]
        im = ax.pcolormesh(k_ax, f_ax[sel], db, cmap='magma', vmin=-45, vmax=0,
                           shading='auto')
        # true (unwrapped) radial line of the event
        p = 1.0 / V_APP
        ax.plot([-p * dx * 60, p * dx * 60], [0, 60], 'w--', lw=1.2)
        if col == 0:
            ax.text(0.02, 0.93, 'one radial line\nk = p f  (no wrap)',
                    transform=ax.transAxes, color='w', va='top', fontsize=9)
        else:
            ax.annotate('wrapped energy crosses\nthe whole k band',
                        xy=(-0.28, 33), xytext=(-0.48, 50), color='crimson',
                        arrowprops=dict(arrowstyle='->', color='crimson'))
        ax.set(title='FK at dx = %.2f m' % dx, xlabel='k (cycles/trace)',
               ylabel='f (Hz)')
    fig.tight_layout()
    fig.savefig('figures/term02_lec02/term02_lec02_spatial_aliasing.png',
                dpi=150)
    print('wrote term02_lec02_spatial_aliasing.png')


if __name__ == '__main__':
    main()
