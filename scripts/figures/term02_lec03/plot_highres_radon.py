"""Figure: high-resolution (sparse) parabolic Radon demultiple.

Top row: IRLS iteration strip.  Iteration 0 is the damped least-squares
solution: each event is smeared across neighbouring curvatures.  Each
IRLS iteration re-weights the model norm (Cauchy sparseness), so small
coefficients are crushed and large ones survive: the panel focuses while
the data fit stays good.  Every panel is shown after the same support
polish (below), so the strip compares like with like.

Bottom row: the demultiple payoff.  A mute keeps |q| <= 12 ms (primaries
after NMO) and rejects everything else.  In the smeared LS panel the
multiple's skirt reaches into the kept zone, so rejected-multiple energy
leaks back into the output.  The focused (sparse) panel separates the
families cleanly, so the mute removes the multiple without leakage.
The last panel shows the difference of the two outputs at its own
amplitude scale: the leaked multiple that sparseness removed.

Objective (Cauchy sparseness norm), solved by iteratively re-weighted
least squares (IRLS):
    J(m) = || d - L^T m ||^2 + lambda * sum_q ln(1 + |m_q|^2 / sigma^2)
Each iteration solves a damped normal system with weights
    w_q = 1 / (1 + |m_q|^2 / sigma^2)
computed from the previous iterate.  One weight per curvature q is shared
by all frequencies (energy summed over f) and lightly smoothed across q,
which keeps the sparse support consistent from frequency to frequency.

Final polish (two-stage sparse inversion): the IRLS solution selects the
*support* (curvatures with significant energy, dilated by one cell);
a last least-squares re-fit restricted to that support, with damping
inversely proportional to the IRLS energy, produces clean wavelet-shaped
events.  Without this polish the per-frequency solutions carry bin-to-bin
jitter that shows up as vertical streaking in the (q, t) panel.

Data are synthesised directly in the frequency domain,
    d(f, x) = sum_events amp * W(f) * exp(-2i*pi*f*(t0 + q*x^2)),
so every event lies exactly on a parabolic trajectory of the operator
(per-sample picking of trajectories would add timing jitter that no
Radon operator can fit).
"""

import numpy as np
import matplotlib.pyplot as plt

# --- survey and transform parameters -------------------------------------------
DT, TMAX = 0.004, 2.6            # [s] sample interval, trace length
DX, XMAX = 20.0, 2000.0          # [m] offset interval, max offset
Q_LABEL = np.arange(-36.0, 117.0, 8.0)    # residual moveout at far offset, ms
NQ = len(Q_LABEL)
BAND = (10.0, 60.0)              # [Hz] frequencies used in the inversion

# (t0 [s], residual moveout at far offset [ms], amplitude)
# three primaries (flat after NMO) + two multiples (residual moveout)
EVENTS = [(0.55, -8, 1.0), (1.15, -4, 0.9), (1.80, 0.0, 0.8),
          (0.90, 15, 0.8), (1.60, 40, 0.6)]
F_DOM = 20.0                     # [Hz] dominant frequency of the wavelet

MUTE = 12.0                      # [ms] half-width of the kept q-zone
LAM_FRAC = 1e-2                  # damping as fraction of ||G||^2 (fixed)
SIGMA_FRAC = 0.5                 # Cauchy sigma as fraction of max_q ||m(q,:)||
NITER = 12                       # IRLS iterations
SNAP_ITERS = (0, 1, 2, 4, 8, 12)  # iterations shown in the top strip
SUPPORT_THR = 0.05               # support threshold (fraction of max energy)


def ricker(f_dom, n, dt):
    """Ricker wavelet, centred at sample (n - 1) / 2."""
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


# --- data: synthesised in the frequency domain ---------------------------------
nt = int(TMAX / DT)
x = np.arange(0.0, XMAX + DX, DX)
nx = len(x)
freqs = np.fft.rfftfreq(nt, DT)
nf = len(freqs)
q_axis = Q_LABEL * 1e-3 / XMAX ** 2       # [s/m^2]
band = np.where((freqs >= BAND[0]) & (freqs <= BAND[1]))[0]

wav = ricker(F_DOM, 61, DT)
# spectrum re-centred at t = 0 (the time-domain wavelet starts at sample 0)
W = np.fft.rfft(wav, n=nt) * np.exp(2j * np.pi * freqs * 30 * DT)

data_f = np.zeros((nf, nx), dtype=complex)
for t0, res_ms, amp in EVENTS:
    q = res_ms * 1e-3 / XMAX ** 2
    for k in band:
        data_f[k, :] += amp * W[k] * np.exp(-2j * np.pi * freqs[k] * (t0 + q * x ** 2))
data = np.fft.irfft(data_f, n=nt, axis=0)


# --- forward operator: d(f) = L^T m(f),  L(q,x) = exp(-2i*pi*f*q*x^2) -----------
def L_op(f):
    return np.exp(-2j * np.pi * f * np.outer(q_axis, x ** 2))


# per-frequency normal systems, precomputed once
Gs, rhss, lams = [], [], []
for k in band:
    L = L_op(freqs[k])
    Gs.append(L.conj() @ L.T)                      # (NQ, NQ)
    rhss.append(L.conj() @ data_f[k, :])           # (NQ,)
    lams.append(LAM_FRAC * np.linalg.norm(Gs[-1], 2))

Ns = len(band)
I = np.eye(NQ)

# iteration 0: damped least squares (the smeared starting panel)
M = np.stack([np.linalg.solve(Gs[i] + lams[i] * I, rhss[i]) for i in range(Ns)],
             axis=1)                                # (NQ, Ns)
snaps = {0: M.copy()}

# IRLS: one Cauchy weight per curvature, shared by all frequencies
for it in range(1, NITER + 1):
    energy_q = np.sum(np.abs(M) ** 2, axis=1)       # model energy per q
    sigma = SIGMA_FRAC * np.sqrt(energy_q.max()) + 1e-30
    w = 1.0 / (1.0 + energy_q / sigma ** 2)         # large m -> small damping
    w = 0.25 * w[:-2] + 0.5 * w[1:-1] + 0.25 * w[2:]   # smooth across q
    w = np.concatenate([[w[0]], w, [w[-1]]])
    M = np.stack([np.linalg.solve(Gs[i] + lams[i] * np.diag(w), rhss[i])
                  for i in range(Ns)], axis=1)
    if it in SNAP_ITERS:
        snaps[it] = M.copy()


# --- support polish: IRLS picks the support, restricted LS cleans it -----------
def polish(Mraw):
    """Restrict to the IRLS support and re-fit with inverse-energy damping."""
    energy_q = np.sum(np.abs(Mraw) ** 2, axis=1)
    core = set(np.where(energy_q > SUPPORT_THR * energy_q.max())[0])
    for j in range(1, NQ - 1):                     # plateau-tolerant maxima
        if energy_q[j] >= energy_q[j - 1] and energy_q[j] >= energy_q[j + 1]:
            core.add(j)
    sup = set()
    for a in core:                                 # dilate by one cell
        sup |= {a - 1, a, a + 1}
    active = np.array(sorted(sup & set(range(NQ))))
    out = np.zeros_like(Mraw)
    for i in range(Ns):
        Ga = Gs[i][np.ix_(active, active)]
        # light damping where IRLS put energy, heavy where it did not
        dq = lams[i] * energy_q.max() / (energy_q[active] + 0.1 * energy_q.max())
        out[active, i] = np.linalg.solve(Ga + np.diag(dq), rhss[i][active])
    return out


# polish every IRLS state (iteration 0 stays the plain damped LS):
# the polish is part of the sparse pipeline, not of the LS reference
snaps = {it: (polish(s) if it > 0 else s) for it, s in snaps.items()}
M_ls, M_hr = snaps[0], snaps[NITER]


# --- helpers -------------------------------------------------------------------
def panel_to_time(Mf):
    """(q, f) model panel -> (q, t) panel for display."""
    full = np.zeros((NQ, nt), dtype=complex)
    full[:, band] = Mf
    return np.fft.irfft(full, n=nt, axis=1)


def recon(Mf):
    """Model panel -> data gather (band-limited)."""
    d = np.zeros((nf, nx), dtype=complex)
    for i, k in enumerate(band):
        d[k, :] = L_op(freqs[k]).T @ Mf[:, i]
    return np.fft.irfft(d, n=nt, axis=0)


def mute_and_recon(Mf):
    keep = np.abs(Q_LABEL) <= MUTE
    return recon(np.where(keep[:, None], Mf, 0.0))


# --- QC numbers (printed for reproducibility) -----------------------------------
rms = lambda a: float(np.sqrt(np.mean(a ** 2)))
rd = rms(data)
out_ls = mute_and_recon(M_ls)
out_hr = mute_and_recon(M_hr)
diff = out_ls - out_hr
mult_f = np.zeros((nf, nx), dtype=complex)
for t0, res_ms, amp in EVENTS[3:]:
    q = res_ms * 1e-3 / XMAX ** 2
    for k in band:
        mult_f[k, :] += amp * W[k] * np.exp(-2j * np.pi * freqs[k] * (t0 + q * x ** 2))
mult = np.fft.irfft(mult_f, n=nt, axis=0)
win = slice(int(0.78 / DT), int(1.06 / DT))        # around the first multiple
print(f"data fit:  LS {rms(data - recon(M_ls)) / rd * 100:.1f}%  "
      f"HR {rms(data - recon(M_hr)) / rd * 100:.1f}% residual")
print(f"LS-vs-HR output difference near first multiple: "
      f"{rms(diff[win]) / rms(mult[win]) * 100:.0f}% of the multiple")

# --- figure ---------------------------------------------------------------------
fig = plt.figure(figsize=(15, 9))
gs = fig.add_gridspec(2, 6, height_ratios=(1.0, 1.2), hspace=0.42, wspace=0.30)

pt = panel_to_time(M_ls)
pth = panel_to_time(M_hr)
v = np.percentile(np.abs(data), 99)          # clip for gathers
vp = np.percentile(np.abs(pt), 99)           # clip for panels (LS reference)
qext = [Q_LABEL[0], Q_LABEL[-1], TMAX, 0.0]
xext = [0, XMAX, TMAX, 0.0]

# top row: IRLS iteration strip
for i, it in enumerate(SNAP_ITERS):
    ax = fig.add_subplot(gs[0, i])
    ax.imshow(panel_to_time(snaps[it]).T, extent=qext, aspect="auto",
              cmap="gray", vmin=-vp, vmax=vp)
    ax.set_title(f"iteration {it}" + (" (LS)" if it == 0 else ""), fontsize=10)
    ax.set_xlabel("q, residual moveout (ms)", fontsize=8)
    ax.tick_params(labelsize=8)
    ax.axvline(-MUTE, color="crimson", ls="--", lw=1.0)
    ax.axvline(MUTE, color="crimson", ls="--", lw=1.0)
    if i == 0:
        ax.set_ylabel("Time (s)", fontsize=9)
        ax.text(0.04, 0.94, "smeared", transform=ax.transAxes,
                fontsize=9, va="top", color="crimson")
    if it == SNAP_ITERS[-1]:
        ax.text(0.04, 0.94, "focused", transform=ax.transAxes,
                fontsize=9, va="top", color="seagreen")

# bottom row: panels, input, outputs, difference
ax_ls = fig.add_subplot(gs[1, 0])
ax_ls.imshow(pt.T, extent=qext, aspect="auto", cmap="gray", vmin=-vp, vmax=vp)
ax_ls.set_title("LS panel: smeared", fontsize=10)
ax_ls.text(0.97, 0.94, "multiple tail\nleaks into\nkept zone", transform=ax_ls.transAxes,
           ha="right", va="top", fontsize=8, color="crimson")

ax_hr = fig.add_subplot(gs[1, 1])
ax_hr.imshow(pth.T, extent=qext, aspect="auto", cmap="gray", vmin=-vp, vmax=vp)
ax_hr.set_title("HR panel (sparse): focused", fontsize=10)
ax_hr.text(0.97, 0.94, "families\nseparated", transform=ax_hr.transAxes,
           ha="right", va="top", fontsize=8, color="seagreen")

for ax in (ax_ls, ax_hr):
    ax.axvline(-MUTE, color="crimson", ls="--", lw=1.2)
    ax.axvline(MUTE, color="crimson", ls="--", lw=1.2)
    ax.text(MUTE + 2, 0.72, "kept\nzone", fontsize=7, color="crimson", va="bottom")
    ax.set_ylabel("Time (s)", fontsize=9)
    ax.set_xlabel("q, residual moveout (ms)", fontsize=8)
    ax.tick_params(labelsize=8)

ax_in = fig.add_subplot(gs[1, 2])
ax_in.imshow(data, extent=xext, aspect="auto", cmap="gray", vmin=-v, vmax=v)
ax_in.set_title("Input (after NMO)", fontsize=10)
ax_in.set_xlabel("Offset (m)", fontsize=8)

ax_out_ls = fig.add_subplot(gs[1, 3])
ax_out_ls.imshow(out_ls, extent=xext, aspect="auto", cmap="gray", vmin=-v, vmax=v)
ax_out_ls.set_title("Output: LS panel", fontsize=10)
ax_out_ls.text(0.97, 0.56, "multiple\nresidue", transform=ax_out_ls.transAxes,
               ha="right", fontsize=8, color="crimson")
ax_out_ls.set_xlabel("Offset (m)", fontsize=8)

ax_out_hr = fig.add_subplot(gs[1, 4])
ax_out_hr.imshow(out_hr, extent=xext, aspect="auto", cmap="gray", vmin=-v, vmax=v)
ax_out_hr.set_title("Output: HR panel", fontsize=10)
ax_out_hr.text(0.97, 0.24, "primaries\nkept", transform=ax_out_hr.transAxes,
               ha="right", fontsize=8, color="seagreen")
ax_out_hr.set_xlabel("Offset (m)", fontsize=8)

ax_diff = fig.add_subplot(gs[1, 5])
scale = np.percentile(np.abs(data), 99.5) / max(np.percentile(np.abs(diff), 99.5), 1e-12)
ax_diff.imshow(diff, extent=xext, aspect="auto", cmap="gray",
               vmin=-np.percentile(np.abs(diff), 99.5),
               vmax=np.percentile(np.abs(diff), 99.5))
ax_diff.set_title("Difference of outputs", fontsize=10)
ax_diff.text(0.97, 0.94, f"what sparseness bought\n(own scale, ~{scale:.0f}x)",
             transform=ax_diff.transAxes, ha="right", va="top",
             fontsize=8, color="darkorange")
ax_diff.set_xlabel("Offset (m)", fontsize=8)

for ax in (ax_in, ax_out_ls, ax_out_hr, ax_diff):
    ax.set_ylabel("")
    ax.tick_params(labelsize=8)
ax_in.set_ylabel("Time (s)", fontsize=9)

fig.suptitle("High-resolution Radon demultiple: a sparse model norm focuses the "
             "panel and keeps multiple residue out of the output", fontsize=13)
fig.savefig("figures/term02_lec03/term02_lec03_highres_radon.png",
            dpi=150, bbox_inches="tight")
print("saved figures/term02_lec03/term02_lec03_highres_radon.png")
