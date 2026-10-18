"""Figure 10: FK and f-p are one spectrum in two coordinate systems.

The running-example gather is recomputed at a fine trace spacing (dx = 4 m)
so that the linear noise is NOT spatially aliased and the mapping is not
confused by wraparound. Linear amplitude scale (clipped) keeps the display
clean. Top row: full FK spectrum with radial lines k = p f, and the f-p
spectrum (the same FK values resampled along those radial lines -- Fourier
slice theorem, U(f,p) = D(f, k=pf)). A radial fan in FK becomes a
horizontal band in f-p. Bottom row: zoom on the reflection region -- the
reflection fan (narrow on the full axes, its edge is set by the maximum
offset and the moveout velocity) opens into a readable band in f-p.
"""

import numpy as np
import matplotlib.pyplot as plt

# running-example geometry, oversampled spatially for this figure only
DT, DX, NX, TMAX = 0.004, 4.0, 375, 3.0
REFLECTIONS = [(0.8, 2200.0), (1.4, 2600.0), (2.0, 3000.0)]
GR_V, GR_AMP = 300.0, 2.5
AB_V, AB_AMP = 600.0, 1.5
FMAX_PLOT = 35.0
PMAX_PLOT = 4.0          # ms/m
PZOOM = 0.5              # ms/m, zoom row limit (past the fan edge)
KZOOM_CPT = 0.10         # cycles/trace, zoom row limit
LIN_CLIP = 0.45          # linear clip level (fraction of max amplitude):
                         # just above the reflection-band peak (~0.3 of max)
                         # so bands keep their brightness contrast while the
                         # noise floor (~0.01) stays dark


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


def main():
    data, t, x = make_gather()
    nt = len(t)
    x_max = x[-1]

    # FK spectrum (convention: slope-p event on line k = +p f)
    F = np.fft.fft(data, axis=0)
    D = np.fft.ifft(F, axis=1)
    amp = np.abs(np.fft.fftshift(D))
    f_ax = np.fft.fftshift(np.fft.fftfreq(nt, d=DT))
    k_ax = np.fft.fftshift(np.fft.fftfreq(NX, d=DX))     # cycles/m
    sel = (f_ax >= 0) & (f_ax <= FMAX_PLOT)
    fk = amp[sel]
    fq = f_ax[sel]
    k_cpt = k_ax * DX                                     # cycles/trace

    # f-p spectrum by the slice theorem: interpolate each f-row of FK onto
    # the radial points k = p f
    p_ax = np.linspace(-PMAX_PLOT, PMAX_PLOT, 321) * 1e-3     # s/m
    fp = np.zeros((len(fq), len(p_ax)))
    for i in range(len(fq)):
        fp[i] = np.interp(p_ax * fq[i], k_ax, fk[i], left=0.0, right=0.0)

    # reflection fan edge slopes: tangent dip at the far offset
    edges = [x_max / (v**2 * np.sqrt(t0**2 + (x_max / v) ** 2))
             for t0, v in REFLECTIONS]                        # s/m
    p_noise = [(1 / AB_V, 'air blast'), (1 / GR_V, 'ground roll')]

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    def show(ax, M, xc, pc, title, xlim):
        """Panel with linear-amplitude display and reference lines. Explicit
        xlim: the reference lines extend beyond the zoom range, and axes
        autoscaling would follow them."""
        im = ax.pcolormesh(xc, fq, np.clip(M / M.max(), 0, LIN_CLIP),
                           cmap='magma', vmin=0, vmax=LIN_CLIP,
                           shading='auto')
        is_fk = pc is None
        for p, lbl in [(e, '') for e in edges] + p_noise:
            if is_fk:
                ax.plot([-p * DX * FMAX_PLOT, p * DX * FMAX_PLOT],
                        [0, FMAX_PLOT], 'w--', lw=1.0, alpha=0.85)
            else:
                ax.axvline(p * 1e3, color='w', ls='--', lw=1.0, alpha=0.85)
        ax.set(title=title, xlabel='k (cycles/trace)' if is_fk else 'p (ms/m)',
               ylabel='f (Hz)')
        ax.set_xlim(xlim)
        ax.set_ylim(0, FMAX_PLOT)
        return im

    # top row: full axes
    im0 = show(axes[0, 0], fk, k_cpt, None,
               'FK (full range): radial lines k = p f',
               xlim=(k_cpt.min(), k_cpt.max()))
    for p, lbl in p_noise:
        axes[0, 0].text(p * DX * FMAX_PLOT * 0.93, FMAX_PLOT * 0.55, lbl,
                        color='w', rotation=60, fontsize=8, ha='right')
    im1 = show(axes[0, 1], fp, p_ax * 1e3, p_ax,
               'f-p (full range): the same lines -> bands',
               xlim=(p_ax.min() * 1e3, p_ax.max() * 1e3))
    for p, lbl in p_noise:
        axes[0, 1].text(p * 1e3 + 0.07, 2.5, lbl, color='w', fontsize=8,
                        rotation=90, va='bottom')

    # zoom boxes on the top row
    for ax, half_w in [(axes[0, 0], KZOOM_CPT), (axes[0, 1], PZOOM)]:
        ax.add_patch(plt.Rectangle((-half_w, 0), 2 * half_w, FMAX_PLOT,
                                    fill=False, edgecolor='w', lw=1.3))

    # bottom row: reflection region zoom
    kz = np.abs(k_cpt) <= KZOOM_CPT
    show(axes[1, 0], fk[:, kz], k_cpt[kz], None,
         'FK zoom: reflection fan', xlim=(-KZOOM_CPT, KZOOM_CPT))
    pz = np.abs(p_ax * 1e3) <= PZOOM
    show(axes[1, 1], fp[:, pz], p_ax[pz] * 1e3, p_ax[pz],
         'f-p zoom: the same fan as a band', xlim=(-PZOOM, PZOOM))
    for i, (t0, v) in enumerate(REFLECTIONS):
        axes[1, 0].plot([-edges[i] * DX * FMAX_PLOT,
                         edges[i] * DX * FMAX_PLOT], [0, FMAX_PLOT],
                        'w-', lw=1.4)
        axes[1, 1].axvline(edges[i] * 1e3, color='w', lw=1.4)
        axes[1, 1].axvline(-edges[i] * 1e3, color='w', lw=1.4)
    axes[1, 0].text(0.002, FMAX_PLOT * 0.12, 'fan edges:\ndeep (inner) to\n'
                    'shallow (outer)', color='w', fontsize=8)
    axes[1, 1].text(-edges[0] * 1e3 - 0.02, FMAX_PLOT * 0.12,
                    'fan = band between\np = 0 and the edges', color='w',
                    fontsize=8, ha='right')

    fig.colorbar(im0, ax=axes[0, 1], label='amplitude (linear, clipped)',
                 pad=0.02)
    fig.suptitle('One spectrum, two coordinate systems: FK and f-p\n'
                 '(linear amplitude; bottom row zooms the reflection fan)',
                 y=0.99)
    fig.tight_layout()
    fig.savefig('figures/term02_lec02/term02_lec02_fk_fp_connection.png',
                dpi=150)
    print('wrote term02_lec02_fk_fp_connection.png')


if __name__ == '__main__':
    main()
