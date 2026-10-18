"""Figure 1: Noise taxonomy — the lecture's running example.

A synthetic shot gather with the three noise families discussed in Section 1:
reflection hyperbolas (signal), source-generated linear noise (ground roll and
air blast), and random background noise. The same gather (same parameters)
reappears in Figures 3, 5, 8, 9 and 10 of the notes.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- running-example parameters (shared by all term02_lec02 figure scripts) ---
DT = 0.004          # s, time sample interval
DX = 25.0           # m, trace spacing
NX = 60             # traces
TMAX = 3.0          # s
REFLECTIONS = [     # (t0 [s], Vrms [m/s], amplitude)
    (0.8, 2200.0, 1.00),
    (1.4, 2600.0, 0.80),
    (2.0, 3000.0, 0.60),
]
GR_V = 300.0        # m/s, ground-roll apparent velocity
GR_AMP = 2.5        # ground roll is strong
AB_V = 600.0        # m/s, air-blast apparent velocity
AB_AMP = 1.5


def ricker(f_dom, n, dt):
    """Ricker wavelet of dominant frequency f_dom, n samples at interval dt."""
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
    """Build the running-example shot gather: reflections + ground roll +
    air blast + random noise. Returns (data, t, x)."""
    nt = int(TMAX / DT) + 1
    t = np.arange(nt) * DT
    x = np.arange(1, NX + 1) * DX
    data = np.zeros((nt, NX))
    wav_r = ricker(25, 61, DT)                     # reflections: ~12-50 Hz
    wav_gr = ricker(14, 121, DT)                   # ground roll: ~6-25 Hz
    wav_ab = ricker(20, 91, DT)                    # air blast
    for t0, v, a in REFLECTIONS:                   # hyperbolic reflections
        tt = np.sqrt(t0**2 + (x / v) ** 2)
        add_event(data, tt, wav_r, a)
    add_event(data, 0.05 + x / GR_V, wav_gr, GR_AMP)   # ground roll
    add_event(data, 0.10 + x / AB_V, wav_ab, AB_AMP)   # air blast
    rng = np.random.default_rng(seed)
    data += 0.08 * rng.standard_normal(data.shape)            # random noise
    return data, t, x


def main():
    data, t, x = make_gather()
    fig, ax = plt.subplots(figsize=(10, 6))
    clip = np.percentile(np.abs(data), 99.5)
    ax.imshow(data, aspect='auto', cmap='gray', vmin=-clip, vmax=clip,
              extent=[x[0], x[-1], t[-1], 0], interpolation='bilinear')
    # label the event families
    ax.annotate('ground roll\n(300 m/s, 6-25 Hz)', xy=(700, 1.15),
                xytext=(980, 2.35), color='crimson', fontsize=10,
                arrowprops=dict(arrowstyle='->', color='crimson'))
    ax.annotate('air blast (600 m/s)', xy=(1150, 0.72),
                xytext=(1230, 1.5), color='darkorange', fontsize=10,
                arrowprops=dict(arrowstyle='->', color='darkorange'))
    ax.annotate('reflections', xy=(500, 0.86), xytext=(90, 0.35),
                color='royalblue', fontsize=10,
                arrowprops=dict(arrowstyle='->', color='royalblue'))
    ax.annotate('reflections', xy=(350, 1.47), xytext=(90, 0.35),
                color='royalblue', fontsize=10,
                arrowprops=dict(arrowstyle='->', color='royalblue'))
    ax.annotate('random noise', xy=(1300, 2.75), xytext=(950, 2.75),
                color='dimgray', fontsize=10,
                arrowprops=dict(arrowstyle='->', color='dimgray'))
    ax.set_xlabel('offset x (m)')
    ax.set_ylabel('time t (s)')
    ax.set_title('Running example: shot gather with coherent and random noise')
    fig.tight_layout()
    fig.savefig('figures/term02_lec02/term02_lec02_noise_types.png', dpi=150)
    print('wrote term02_lec02_noise_types.png')


if __name__ == '__main__':
    main()
