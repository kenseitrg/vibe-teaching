"""Figure 2: Plane waves in t-x and their FK radial lines.

Left: three linear events (plane waves) at dx = 12.5 m -- two gentle
dips (p = 0.25 and 0.50 ms/m, reflection-like) and one steep,
air-blast-like event (p = 1.5 ms/m). Right: the FK amplitude
spectrum. Each unaliased event is one clean radial line k = p f
through the origin. The steep event's line reaches the k = +0.5
cyc/trace edge at f_alias = 26.7 Hz and wraps around to k = -0.5:
above f_alias its energy re-enters the spectrum from the opposite
edge, appearing as an apparent dip of the opposite sign -- spatial
aliasing, Section 3's subject.
"""

import numpy as np
import matplotlib.pyplot as plt

DT, DX = 0.004, 12.5
NX, TMAX = 97, 1.85
F_DOM = 30.0                     # Hz (band ~15-50 Hz, fills the FK display)
EVENTS = [                       # (intercept tau0 [s], slope p [ms/m])
    (0.20, 0.25),
    (0.55, 0.50),
    (0.05, 1.50),
]
FMAX_PLOT = 50.0                 # Hz, top of the FK display
KN = 0.5                         # cyc/trace, spatial Nyquist at this dx
DB_MIN = -30.0                  # display floor: hides numerical artifacts
C_ALIAS = 'red'                 # guide color reserved for the aliased event
C_CLEAN = 'black'               # guide color for the unaliased events
BBOX = dict(facecolor='white', alpha=0.75, edgecolor='none', pad=1.5)


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
    data = sum(build_event(t, x, tau0, p_ms) for tau0, p_ms in EVENTS)

    amp = fk_amp(data)
    f_ax = np.fft.fftshift(np.fft.fftfreq(nt, d=DT))
    k_ax = np.fft.fftshift(np.fft.fftfreq(NX, d=DX)) * DX   # cycles/trace
    sel = (f_ax >= 0) & (f_ax <= FMAX_PLOT)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), layout='constrained')

    # ---- left: t-x panel with the event slopes and apparent velocities
    clip = np.percentile(np.abs(data), 99.5)
    axes[0].imshow(data, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
                   extent=[0, x[-1], t[-1], 0])
    v_labels = [(80, 0.115, 'V = 4000 m/s'), (620, 0.72, 'V = 2000 m/s'),
                (350, 0.50, 'V = 667 m/s')]
    for (tau0, p_ms), (vx, vt, txt) in zip(EVENTS, v_labels):
        axes[0].plot(x, tau0 + p_ms * 1e-3 * x, color='crimson', lw=1.2,
                     alpha=0.8)
        axes[0].text(vx, vt, txt, color='crimson', fontsize=8.5)
    axes[0].set_ylim(t[-1], 0)
    axes[0].set(title='t-x: three plane waves '
                      f'($\\Delta x$ = {DX:g} m)',
                xlabel='x (m)', ylabel='t (s)')

    # ---- right: FK spectrum with radial-line guides
    ax = axes[1]
    db = 20 * np.log10(amp[sel] / amp[sel].max() + 1e-6)
    im = ax.pcolormesh(k_ax, f_ax[sel], db, cmap='viridis', vmin=DB_MIN,
                       vmax=0, shading='auto')

    def k_of_f(f_hz, p_ms):
        return p_ms * 1e-3 * f_hz * DX            # k = p f, cyc/trace

    # unaliased events: one clean radial line each, inside the panel
    for p_ms in (0.25, 0.50):
        ax.plot([0.0, k_of_f(FMAX_PLOT, p_ms)], [0.0, FMAX_PLOT], '--',
                color=C_CLEAN, lw=1.2)
        ax.text(k_of_f(FMAX_PLOT, p_ms) - 0.015, 47.0, f'p = {p_ms:.2f}',
                color=C_CLEAN, ha='right', fontsize=9, bbox=BBOX)

    # aliased event: true segment up to the k_N edge, then the wrapped
    # continuation k_apparent = p f dx - 1 re-entering from -k_N
    p_al = EVENTS[2][1]
    f_alias = KN / (p_al * 1e-3 * DX)             # 26.7 Hz
    ax.plot([0.0, KN], [0.0, f_alias], '--', color=C_ALIAS, lw=1.4)
    ax.plot([-KN, k_of_f(FMAX_PLOT, p_al) - 1.0], [f_alias, FMAX_PLOT],
            '--', color=C_ALIAS, lw=1.4)
    ax.plot([KN, -KN], [f_alias, f_alias], 'o', color=C_ALIAS, ms=4)
    ax.text(0.26, 8.5, f'p = {p_al:.2f}', color=C_ALIAS, fontsize=9,
            bbox=BBOX)
    ax.text(0.49, 29.5, f'$f_\\mathrm{{alias}}$ = {f_alias:.1f} Hz',
            color=C_ALIAS, ha='right', fontsize=8.5, bbox=BBOX)
    ax.text(-0.44, 46.0, 'wrapped:\napparent dip flips', color=C_ALIAS,
            fontsize=8.5, bbox=BBOX)
    ax.legend(handles=[plt.Line2D([], [], ls='--', color=C_CLEAN, lw=1.2,
                                  label='unaliased: one radial line'),
                       plt.Line2D([], [], ls='--', color=C_ALIAS, lw=1.4,
                                  label='aliased: wraps at $\\pm k_N$')],
              loc='lower left', fontsize=8, framealpha=0.8)
    ax.set(title='FK spectrum: p = k/f radial lines',
           xlabel='k (cycles/trace)', ylabel='f (Hz)')
    fig.colorbar(im, ax=ax, label='amplitude (dB)')

    fig.savefig('figures/term02_lec02/term02_lec02_fk_plane_wave.png',
                dpi=150)
    print('wrote term02_lec02_fk_plane_wave.png')


if __name__ == '__main__':
    main()
