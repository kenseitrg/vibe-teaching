"""Figure 4: Spatial aliasing of the ground-roll event (300 m/s, 6-25 Hz).

The running example's ground roll recorded at two trace spacings.
Left, dx = 4 m: f_alias = 37.5 Hz lies above the band -- the spacing
satisfies the design rule dx < V/(2 f_max) of Section 3.3, nothing
wraps, and the FK energy is one clean radial line k = f/V. Right,
dx = 25 m: f_alias = 6 Hz -- the per-trace delay (83 ms) exceeds one
period, the apparent dip flips trace to trace, and in FK the energy
wraps into a sawtooth of parallel segments crossing the whole k band
-- exactly where the reflection dips live. A zoom inset in the t-x
panel shows the trace-to-trace arrival stepping. Only positive
temporal frequencies are displayed.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

DT, TMAX, XMAX = 0.004, 3.6, 1000.0
V_APP, F_DOM = 300.0, 14.0        # ground roll of the running example
HALO = [pe.withStroke(linewidth=3.5, foreground='black')]
DB_MIN, FMAX_FK, F_BAND = -30.0, 40.0, 27.0   # display floor / f top / band


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


def make_event(dx):
    """The linear event d(t,x) = s(t - x/V) at trace spacing dx."""
    nx = int(XMAX / dx)
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


def wrap_guides(ax, dx, f_alias):
    """True radial line (white) up to the band or f_alias, whichever
    comes first, then wrapped segments (red): k = p f - n."""
    pdx = dx / V_APP                       # k (cyc/trace) = pdx * f
    f_true = min(f_alias, F_BAND, FMAX_FK)
    ax.plot([0.0, pdx * f_true], [0.0, f_true], '--', color='w', lw=1.6,
            path_effects=HALO)
    n = 1
    while 2 * f_alias * (n - 0.5) < min(F_BAND, FMAX_FK):
        f_lo = 2 * f_alias * (n - 0.5)
        f_hi = min(2 * f_alias * (n + 0.5), F_BAND, FMAX_FK)
        ax.plot([pdx * f_lo - n, pdx * f_hi - n], [f_lo, f_hi], '--',
                color='red', lw=1.6, path_effects=HALO)
        n += 1


def main():
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), layout='constrained',
                             gridspec_kw=dict(height_ratios=[1.0, 1.05]))
    fk_ims = []
    for col, (dx, f_alias) in enumerate([(4.0, 37.5), (25.0, 6.0)]):
        data, t, x = make_event(dx)
        nt, nx = data.shape

        # ---- t-x panel
        ax = axes[0, col]
        clip = np.percentile(np.abs(data), 99.5)
        ax.imshow(data, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
                  extent=[0, x[-1], t[-1], 0])
        ax.plot([0, XMAX], [0.06, 0.06 + XMAX / V_APP], '--', color='crimson',
                lw=1.2)
        ax.set(title=rf't-x, $\Delta x$ = {dx:g} m', xlabel='x (m)',
               ylabel='t (s)')
        if col == 1:
            ax.text(30, 3.32, '$\\Delta t$ = 83 ms/trace $\\approx$ 1 period:'
                    '\napparent dip flips trace-to-trace',
                    color='crimson', fontsize=8.5, va='bottom')
            # zoom inset on the arrival stepping
            ins = ax.inset_axes([0.55, 0.50, 0.42, 0.44])
            j0, j1 = np.searchsorted(x, (380, 570))
            i0, i1 = np.searchsorted(t, (1.30, 1.95))
            sub = data[i0:i1, j0:j1]
            ins.imshow(sub, aspect='auto', cmap='gray',
                       vmin=-clip, vmax=clip, extent=[x[j0], x[j1 - 1],
                                                      t[i1 - 1], t[i0]])
            xs, ts = x[j0:j1], 0.06 + x[j0:j1] / V_APP
            ins.plot(xs, ts, '--', color='crimson', lw=1.0)
            ins.plot(xs, ts, 'o', color='crimson', mfc='none', mec='crimson',
                     ms=4, mew=1.0)
            ins.tick_params(labelsize=7)
            ins.set_title('zoom: true arrivals', fontsize=8, color='crimson')
            ax.indicate_inset_zoom(ins, edgecolor='crimson')

        # ---- FK panel
        ax = axes[1, col]
        amp = fk_amp(data)
        f_ax = np.fft.fftshift(np.fft.fftfreq(nt, d=DT))
        k_ax = np.fft.fftshift(np.fft.fftfreq(nx, d=dx)) * dx  # cyc/trace
        sel = (f_ax >= 0) & (f_ax <= FMAX_FK)
        db = 20 * np.log10(amp[sel] / amp[sel].max() + 1e-6)
        fk_ims.append(ax.pcolormesh(k_ax, f_ax[sel], db, cmap='viridis',
                                    vmin=DB_MIN, vmax=0, shading='auto'))
        wrap_guides(ax, dx, f_alias)
        ax.text(0.5, 2.0, '$k_N$', color='w', fontsize=8, ha='right',
                path_effects=HALO)
        ax.text(-0.5, 2.0, '$-k_N$', color='w', fontsize=8, ha='left',
                path_effects=HALO)
        ax.set(title=rf'FK, $\Delta x$ = {dx:g} m', xlabel='k (cycles/trace)',
               ylabel='f (Hz)')
        if col == 0:
            ax.text(-0.49, 38.5, 'no wrap: one radial line\n'
                    '($f_\\mathrm{alias}$ = 37.5 Hz above the band)',
                    color='w', fontsize=8.5, va='top', path_effects=HALO)
        else:
            ax.axhline(f_alias, color='w', ls=':', lw=1.0)
            ax.text(-0.49, f_alias + 1.0,
                    f'$f_\\mathrm{{alias}}$ = {f_alias:g} Hz', color='w',
                    fontsize=8.5, path_effects=HALO)
            ax.text(0.06, 33.5, 'wraps every 12 Hz:\na sawtooth across k',
                    color='red', fontsize=8.5, path_effects=HALO)
    fig.colorbar(fk_ims[0], ax=axes[1], shrink=0.85, pad=0.02,
                 label='amplitude (dB)')

    fig.savefig('figures/term02_lec02/term02_lec02_spatial_aliasing.png',
                dpi=150)
    print('wrote term02_lec02_spatial_aliasing.png')


if __name__ == '__main__':
    main()
