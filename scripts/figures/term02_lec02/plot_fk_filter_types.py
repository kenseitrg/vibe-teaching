"""Figure 5: FK filter masks and a dip-filter application.

Top row: the four standard masks of Section 4 in the (f, k) plane --
k-cut (anti-alias), dip-pass fan, narrow dip-reject, polygonal with
low-frequency protection. Bottom row: applying the dip fan to the
running-example gather -- input, output, difference. The difference panel
is the QC instrument: it must contain linear noise and nothing
reflection-shaped.
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


def taper_edge(mask, coord, lo, hi):
    """Cosine taper of `mask` from 1 inside [lo, hi] to 0 outside (1-D helper
    applied along one axis at a time via broadcasting)."""
    ramp = np.ones_like(coord)
    inside = (coord >= lo) & (coord <= hi)
    ramp[inside] = 1.0
    below = coord < lo
    width = max(abs(hi - lo), 1e-12)
    ramp[below] = 0.5 * (1 + np.cos(np.pi * np.clip((coord[below] - lo) / width, -1, 0)))
    above = coord > hi
    ramp[above] = 0.5 * (1 + np.cos(np.pi * np.clip((coord[above] - hi) / width, 0, 1)))
    return ramp


def build_masks(f, k_cpt):
    """Four standard FK masks on the (f, k) grid. f in Hz (>=0), k in
    cycles/trace. Returns dict of masks with soft tapered edges."""
    F, K = np.meshgrid(f, k_cpt, indexing='ij')
    p_eff = np.where(F > 1.0, K / np.maximum(F, 1.0) / DX, 0.0)   # s/m
    masks = {}

    # 1. k-cut: pass |k| < 0.25 cyc/trace, taper to 0.35
    masks['k-cut (anti-alias)'] = taper_edge(np.ones_like(K), k_cpt, -0.25, 0.25)[None, :] * np.ones_like(K)

    # 2. dip-pass fan: pass |p| < 0.45 ms/m (beyond steepest reflection dip)
    fan = np.clip((0.60e-3 - np.abs(p_eff)) / 0.15e-3, 0, 1)
    fan[F < 1.0] = 1.0                      # do not filter near-zero freq
    masks['dip-pass fan'] = fan

    # 3. narrow dip-reject around the air-blast slope p = 1/600 s/m
    reject = np.clip(1 - np.abs(np.abs(p_eff) - 1 / AB_V) / 0.15e-3, 0, 1)
    masks['narrow dip-reject'] = 1.0 - reject * (F > 3.0)

    # 4. polygonal: reject steep noise cone only below 30 Hz (low-f protection)
    steep = np.clip((np.abs(p_eff) - 0.8e-3) / 0.2e-3, 0, 1)
    lfp = np.clip((30.0 - F) / 8.0, 0, 1)   # reject strength fades by 30 Hz
    masks['polygonal + low-f protection'] = 1.0 - steep * lfp
    return masks


def fk_transform(data):
    """Forward FK with the e^{-i2pi(ft-kx)} convention (slope p -> k=pf)."""
    return np.fft.ifft(np.fft.fft(data, axis=0), axis=1)


def fk_inverse(spec):
    """Exact inverse of fk_transform."""
    return np.real(np.fft.ifft(np.fft.fft(spec, axis=1), axis=0))


def fk_amp_db(data, fmax=100.0):
    """FK amplitude in dB (0 = panel max), positive frequencies only."""
    amp = np.abs(np.fft.fftshift(fk_transform(data)))
    f = np.fft.fftshift(np.fft.fftfreq(data.shape[0], d=DT))
    k = np.fft.fftshift(np.fft.fftfreq(NX, d=DX)) * DX   # cycles/trace
    sel = (f >= 0) & (f <= fmax)
    db = 20 * np.log10(amp[sel] / amp.max() + 1e-6)
    return db, f[sel], k


def main():
    data, t, x = make_gather()
    nt = len(t)
    f_full = np.fft.fftfreq(nt, d=DT)
    k_full = np.fft.fftfreq(NX, d=DX) * DX          # cycles/trace

    # masks on the full (signed) f grid, applied in the unshifted layout
    F, K = np.meshgrid(f_full, k_full, indexing='ij')
    p_eff = np.where(np.abs(F) > 1.0, K / np.maximum(np.abs(F), 1.0) / DX, 0.0)
    fan = np.clip((0.60e-3 - np.abs(p_eff)) / 0.15e-3, 0, 1)
    fan[np.abs(F) < 1.0] = 1.0

    spec = fk_transform(data)
    data_out = fk_inverse(spec * fan)
    diff = data - data_out

    # ---- plotting: 4 masks on top (3 cols each); below them, the QC triplet
    # input / output / difference as t-x panels (row 2) with the FK spectra
    # of exactly the same three datasets (row 3), column-aligned
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(3, 12, height_ratios=[1.0, 1.05, 0.85])

    f_ax = np.fft.fftshift(f_full)
    k_ax = np.fft.fftshift(k_full)
    sel = (f_ax >= 0) & (f_ax <= 100)
    masks_plot = build_masks(f_ax[sel], k_ax)
    for i, (name, m) in enumerate(masks_plot.items()):
        ax = fig.add_subplot(gs[0, 3 * i:3 * i + 3])
        ax.pcolormesh(k_ax, f_ax[sel], m, cmap='RdBu', vmin=0, vmax=1,
                      shading='auto')
        ax.set(title=name, xlabel='k (cyc/trace)', ylabel='f (Hz)')

    clip = np.percentile(np.abs(data), 99.5)
    qc = [(data, 'input'), (data_out, 'output (dip fan)'),
          (diff, 'difference = noise model')]
    for i, (d, name) in enumerate(qc):
        ax = fig.add_subplot(gs[1, 4 * i:4 * i + 4])
        ax.imshow(d, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
                  extent=[x[0], x[-1], t[-1], 0])
        ax.set(title=name, xlabel='offset x (m)', ylabel='t (s)' if i == 0 else '')

    fk_axes = []
    for i, (d, name) in enumerate(qc):
        db, fq, kq = fk_amp_db(d)
        ax = fig.add_subplot(gs[2, 4 * i:4 * i + 4])
        fk_axes.append(ax)
        last_im = ax.pcolormesh(kq, fq, db, cmap='magma', vmin=-50, vmax=0,
                                shading='auto')
        ax.set(title='FK: ' + name, xlabel='k (cyc/trace)',
               ylabel='f (Hz)' if i == 0 else '')
    fig.colorbar(last_im, ax=fk_axes[-1], label='amplitude (dB)', pad=0.02)
    fig.suptitle('FK filter masks (top) and dip-fan application with QC:\n'
                 'input, output, difference -- in t-x and in FK',
                 y=0.995)
    fig.tight_layout()
    fig.savefig('figures/term02_lec02/term02_lec02_fk_filter_types.png',
                dpi=150)
    print('wrote term02_lec02_fk_filter_types.png')


if __name__ == '__main__':
    main()
