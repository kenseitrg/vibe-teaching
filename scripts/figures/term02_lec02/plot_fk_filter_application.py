"""Figure 6: the dip-pass fan applied to the running gather, with QC.

Top row: input gather, filtered output, and the difference (the noise
model) in t-x. Bottom row: the FK amplitude spectra of exactly these
three panels, with the applied fan edge overlaid (dashed). The applied
mask is mask 2 of the previous figure: full pass for |p| < 0.45 ms/m
(beyond the steepest reflection dip), full reject beyond 0.60 ms/m,
cosine taper between, pass at near-zero frequency. The difference panel
is the QC instrument: it must contain the linear noise and nothing
reflection-shaped.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- running-example parameters (same in all term02_lec02 scripts) ---
DT, DX, NX, TMAX = 0.004, 25.0, 60, 3.0
REFLECTIONS = [(0.8, 2200.0), (1.4, 2600.0), (2.0, 3000.0)]
GR_V, GR_AMP = 300.0, 2.5
AB_V, AB_AMP = 600.0, 1.5

P_PASS, P_REJECT = 0.45e-3, 0.60e-3        # dip-fan design slopes, s/m


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


def dip_fan(f, k):
    """The applied mask on any (f, k) grid: pass |p| < 0.45 ms/m."""
    p_eff = k / np.maximum(np.abs(f), 1.0) / DX
    fan = np.clip((P_REJECT - np.abs(p_eff)) / (P_REJECT - P_PASS), 0, 1)
    fan[np.abs(f) < 1.0] = 1.0
    return fan


def main():
    data, t, x = make_gather()
    nt = len(t)
    f_full = np.fft.fftfreq(nt, d=DT)
    k_full = np.fft.fftfreq(NX, d=DX) * DX          # cycles/trace

    # apply the fan on the full (signed) grids, in the unshifted layout
    F, K = np.meshgrid(f_full, k_full, indexing='ij')
    spec = fk_transform(data)
    data_out = fk_inverse(spec * dip_fan(F, K))
    diff = data - data_out

    fig = plt.figure(figsize=(13, 7.5), layout='constrained')
    gs = fig.add_gridspec(2, 3, height_ratios=[1.0, 0.85])

    # top row: the QC triplet in t-x
    clip = np.percentile(np.abs(data), 99.5)
    qc = [(data, 'input'), (data_out, 'output (dip fan)'),
          (diff, 'difference = noise model')]
    for i, (d, name) in enumerate(qc):
        ax = fig.add_subplot(gs[0, i])
        ax.imshow(d, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
                  extent=[x[0], x[-1], t[-1], 0])
        ax.set(title=name, xlabel='offset x (m)',
               ylabel='t (s)' if i == 0 else '')

    # bottom row: FK spectra of exactly the same three panels
    fk_axes = []
    for i, (d, name) in enumerate(qc):
        db, fq, kq = fk_amp_db(d)
        ax = fig.add_subplot(gs[1, i])
        fk_axes.append(ax)
        last_im = ax.pcolormesh(kq, fq, db, cmap='magma', vmin=-50, vmax=0,
                                shading='auto')
        Fq, Kq = np.meshgrid(fq, kq, indexing='ij')
        ax.contour(Kq, Fq, dip_fan(Fq, Kq), levels=[0.5], colors='white',
                   linewidths=1.4, linestyles='--')
        ax.set(title='FK: ' + name, xlabel='k (cyc/trace)',
               ylabel='f (Hz)' if i == 0 else '', ylim=(0, 100))
        if i == 0:
            ax.text(0.34, 17, 'fan edge', color='white', fontsize=8)
    fig.colorbar(last_im, ax=fk_axes, shrink=0.9, pad=0.02,
                 label='amplitude (dB)')

    fig.suptitle('Dip-fan FK filter on the running gather:\n'
                 'before / after / difference in t-x (top) and in FK '
                 '(bottom, fan edge dashed)')
    fig.savefig('figures/term02_lec02/term02_lec02_fk_filter_application.png',
                dpi=150)
    print('wrote term02_lec02_fk_filter_application.png')


if __name__ == '__main__':
    main()
