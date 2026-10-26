"""Figure: Three limitations of move-out demultiple methods.

Panel (a) — near offsets: differential moveout between a multiple and a
primary with the same t0 shrinks quadratically with offset. Below
~500 m offset the difference is smaller than half a wavelet length:
no filter can separate what does not differ. Practical consequence:
hard mute of the near-offset band after Radon demultiple.

Panel (b) — velocity inversion: a fast shallow layer over slower
sediments. After NMO with the primary velocity function, the surface
multiple is strongly undercorrected (190 ms at far offset — easy), but
the INTERNAL multiple of the slow layer is only mildly undercorrected
(~40 ms) — it moves out almost like a primary and leaks through any
move-out filter.

Panel (c) — AVO smearing: in the LS parabolic Radon panel a
constant-amplitude event focuses into a compact blob, but the same
event with AVO (amplitude decaying with offset) smears along the
curvature axis, because a variable-amplitude parabola is a SUM of
constant-amplitude ones. Smearing overlaps primaries and multiples in
the Radon domain -> leakage; the flip side is that Radon demultiple
also damages the AVO of primaries.
"""

import numpy as np
import matplotlib.pyplot as plt

DT, TMAX = 0.004, 2.6
DX, XMAX = 25.0, 3000.0
BAND = (5.0, 90.0)


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


fig = plt.figure(figsize=(15.5, 9.5))
gs = fig.add_gridspec(2, 4, hspace=0.42, wspace=0.3)

# ---------------- Panel (a): differential moveout vs offset -------------------
axa = fig.add_subplot(gs[0, :2])
x = np.arange(0, XMAX + DX, DX)
for t0, vp, vm, c, lbl in [
        (1.0, 2000, 1650, "crimson", "$V_p=2000$, $V_m=1650$ m/s"),
        (2.0, 2300, 1750, "darkorange", "$V_p=2300$, $V_m=1750$ m/s")]:
    dt_diff = (np.sqrt(t0**2 + (x / vm) ** 2)
               - np.sqrt(t0**2 + (x / vp) ** 2)) * 1e3
    axa.plot(x, dt_diff, color=c, lw=2.2, label=lbl)
axa.axhspan(0, 15, color="0.85", alpha=0.6)
axa.text(1750, 7, "below wavelet resolution (~15 ms)", fontsize=9, color="0.3")
axa.axvspan(0, 600, color="crimson", alpha=0.08)
axa.annotate("near offsets:\nno discrimination\n-> hard mute",
             xy=(350, 42), fontsize=10, color="crimson", ha="center")
axa.set_xlabel("Offset (m)")
axa.set_ylabel("Multiple arrives later than primary by (ms)")
axa.set_title("(a) The discrimination signal dies at near offsets")
axa.legend(fontsize=9)
axa.grid(alpha=0.3)
axa.set_xlim(0, XMAX)

# ---------------- Panel (b): velocity inversion -------------------------------
axv = fig.add_subplot(gs[0, 2])
depths = [0, 400, 900, 1400]
vels = [2000, 1500, 2300]
for i, (z0, z1, v) in enumerate(zip(depths[:-1], depths[1:], vels)):
    axv.fill_betweenx([z0, z1], 0, v, color=["#d9c9a8", "#cfe8ff", "#d9c9a8"][i])
    axv.text(v - 60, (z0 + z1) / 2, f"{v} m/s", ha="right", va="center", fontsize=9)
axv.plot([2000, 1500, 2300], [400, 400, 900], "o", ms=0)
axv.step([2000, 1500, 2300, 2300], [400, 400, 900, 1400], where="pre",
         color="k", lw=1.5)
axv.set_xlim(0, 2600)
axv.set_ylim(1400, 0)
axv.set_xlabel("Velocity (m/s)")
axv.set_ylabel("Depth (m)")
axv.set_title("(b) Model with velocity\ninversion (fast over slow)")
axv.annotate("inversion", xy=(1750, 400), xytext=(2100, 620), fontsize=10,
             color="crimson", arrowprops=dict(arrowstyle="->", color="crimson"))

# gather after NMO at primary velocities
nt = int(TMAX / DT)
t_ax = np.arange(nt) * DT
events = [  # (t0, V_event, amplitude, kind)  kind: p/s/im
    (0.400, 2000, 0.8, "p"),    # top of slow layer
    (1.067, 1705, 1.0, "p"),    # base of slow layer
    (1.733, 1954, 0.9, "p"),    # deep primary
    (1.733, 1629, 0.45, "im"),  # internal multiple of the slow layer
    (2.133, 1705, 0.5, "s"),    # surface multiple (2x trip to slow layer)
]
# primary velocity function for NMO (interp at event times)
vp_t = np.interp([e[0] for e in events if e[3] == "p"],
                 [0.4, 1.067, 1.733], [2000, 1705, 1954])
wav = ricker(30, 41, DT)
gather = np.zeros((nt, len(x)))
for (t0, v, amp, kind), vpn in zip(events, vp_t):
    for j, xj in enumerate(x):
        tj = np.sqrt(t0**2 + (xj / v) ** 2)          # event moveout
        tn = np.sqrt(t0**2 + (xj / vpn) ** 2)        # NMO-corrected time
        i0 = int(np.floor(tn / DT))
        frac = tn / DT - i0
        for off, wt in ((0, 1 - frac), (1, frac)):
            s = i0 + off - 20
            lo, hi = max(0, s), min(nt, s + 41)
            if hi > lo:
                gather[lo:hi, j] += amp * wt * wav[lo - s:hi - s]

axg = fig.add_subplot(gs[0, 3])
v = np.percentile(np.abs(gather), 99.5)
axg.imshow(gather, extent=[0, XMAX, TMAX, 0], aspect="auto", cmap="gray",
           vmin=-v, vmax=v)
axg.set_xlabel("Offset (m)")
axg.set_ylabel("Time (s)")
axg.set_title("(b) After NMO at primary\nvelocities")
axg.annotate("internal multiple:\nalmost flat -> leaks", xy=(2500, 1.75),
             xytext=(900, 2.35), fontsize=9, color="crimson",
             arrowprops=dict(arrowstyle="->", color="crimson"))
axg.annotate("surface multiple:\nstrongly curved -> removed", xy=(2800, 2.18),
             xytext=(700, 0.75), fontsize=9, color="seagreen",
             arrowprops=dict(arrowstyle="->", color="seagreen"))

# ---------------- Panel (c): AVO smear in the Radon panel ---------------------
Q_LABEL = np.linspace(-40, 300, 69)
q_axis = Q_LABEL * 1e-3 / XMAX**2
NQ = len(Q_LABEL)
# post-NMO gather: primary with AVO (residual -10 ms), multiple constant
# amplitude (residual +105 ms)
# synthesise in the frequency domain: exact parabolas, AVO = amplitude
# varying linearly with offset (per-sample picking would add timing jitter)
specs = [  # (t0, residual ms, amp at zero offset, amp at far offset)
    (0.9, -10, 1.0, 0.25),     # primary with AVO
    (1.6, 105, 0.7, 0.7),      # multiple, constant amplitude
]
freqs = np.fft.rfftfreq(nt, DT)
band = np.where((freqs >= BAND[0]) & (freqs <= BAND[1]))[0]
W = np.fft.rfft(wav, n=nt) * np.exp(2j * np.pi * freqs * 20 * DT)
avo_f = np.zeros((len(freqs), len(x)), dtype=complex)
for t0, res_ms, a0, a1 in specs:
    q = res_ms * 1e-3 / XMAX**2
    amp = a0 + (a1 - a0) * x / XMAX
    for k in band:
        avo_f[k, :] += amp * W[k] * np.exp(-2j * np.pi * freqs[k] * (t0 + q * x**2))

# damped least-squares inverse per frequency slice
LAM_FRAC = 1e-2
M = np.zeros((NQ, len(freqs)), dtype=complex)
Drec = np.zeros_like(avo_f)
for k in band:
    L = np.exp(-2j * np.pi * freqs[k] * np.outer(q_axis, x**2))
    G = L.conj() @ L.T
    M[:, k] = np.linalg.solve(
        G + LAM_FRAC * np.linalg.norm(G, 2) * np.eye(NQ),
        L.conj() @ avo_f[k, :])
    Drec[k, :] = L.T @ M[:, k]

Mf = np.zeros((NQ, nt), dtype=complex)
Mf[:, :len(freqs)] = M
radon_t = np.fft.irfft(Mf, n=nt, axis=1)
rms = lambda a: float(np.sqrt(np.mean(a**2)))
print(f"panel (c) LS data-fit residual: "
      f"{rms(np.fft.irfft(avo_f - Drec, n=nt, axis=1)) / rms(np.fft.irfft(avo_f, n=nt, axis=1)) * 100:.1f}%")

axc = fig.add_subplot(gs[1, :2])
vp2 = np.percentile(np.abs(radon_t), 99.5)
axc.imshow(radon_t.T, extent=[Q_LABEL[0], Q_LABEL[-1], TMAX, 0], aspect="auto",
           cmap="gray", vmin=-vp2, vmax=vp2)
axc.annotate("constant amplitude:\ncompact blob", xy=(105, 1.6),
             xytext=(150, 2.15), fontsize=10, color="seagreen",
             arrowprops=dict(arrowstyle="->", color="seagreen"))
axc.annotate("AVO: amplitude varies\nwith offset -> smearing", xy=(-10, 0.9),
             xytext=(-35, 0.42), fontsize=10, color="crimson",
             arrowprops=dict(arrowstyle="->", color="crimson"))
axc.set_xlabel("Residual moveout at 3000 m (ms)")
axc.set_ylabel("Time (s)")
axc.set_title("(c) AVO smears the event along the curvature axis")

axs = fig.add_subplot(gs[1, 2:], frameon=False)
axs.axis("off")
axs.text(0.0, 0.95,
         "What this means for the method family\n"
         "-------------------------------------\n"
         "1. Near offsets: no moveout difference -> data there is\n"
         "   simply muted, creating a gap (and gap -> imaging artifacts).\n\n"
         "2. Velocity inversions: internal multiples inherit nearly\n"
         "   primary-like kinematics -> they leak through every\n"
         "   move-out filter.\n\n"
         "3. Non-hyperbolicity (complex overburden, diffractions):\n"
         "   events do not focus to a point in ANY Radon domain\n"
         "   (they are not single parabolas).\n\n"
         "4. AVO: smearing overlaps families in the panel, and the\n"
         "   mute itself damages primary AVO.\n\n"
         "Conclusion: kinematic discrimination is cheap and effective\n"
         "where velocity increases with depth -- but none of its\n"
         "assumptions survives a hard geological case. That is what\n"
         "motivates the prediction family of Session 2.",
         va="top", fontsize=10.5, family="monospace")

fig.suptitle("Limitations of move-out (kinematic) demultiple methods",
             fontsize=14)
fig.savefig("figures/term02_lec03/term02_lec03_kinematic_limits.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec03_kinematic_limits.png")
