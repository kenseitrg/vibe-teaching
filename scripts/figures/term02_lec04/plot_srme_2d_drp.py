"""Figure: SRME in 2D — every multiple is two primaries glued at a
downward reflection point (DRP).

For a target trace (source xs, receiver xr) each candidate DRP xk
splits the multiple into two primary-like legs:
    leg 1: shot at xs  -> reflection -> arrives at xk   (shot gather P)
    leg 2: "shot" at xk -> reflection -> arrives at xr  (receiver gather)
The multiple contribution at xk is the time-convolution of the two leg
traces. Summing (integrating) over ALL xk gives the predicted multiple
trace:   M(xr,xs) = -dx * sum_k P(xr,xk) * P(xk,xs)
The per-k integrand panel is the MULTIPLE CONTRIBUTION GATHER (MCG).

Panels:
 1. Model + raypath split for the target (xs=750 m, xr=1250 m), DRP
    highlighted at xk=1000 m; the 'virtual source' idea.
 2. Input shot gather at xs (primaries + surface multiples).
 3. MCG for the target trace: each event's apex marks the surface
    reflection point of that multiple path.
 4. Predicted multiple (MCG sum) vs actual multiples (data - primaries)
    for the target trace: kinematics match.
 5. Shot gather after model-and-subtract vs the true primary gather.

Physics: flat water bottom 300 m @ 1500 m/s (t_wb=0.4 s) and a deep
reflector 1200 m (t=1.2 s, V=2100). dx = 25 m, dt = 4 ms.
"""

import numpy as np
import matplotlib.pyplot as plt

DX, NX = 25.0, 61
X = (np.arange(NX)) * DX
DT, TMAX = 0.004, 2.6
NT = int(TMAX / DT)
F_DOM = 26.0
T_WB, V_WB = 0.40, 1500.0
T_D, V_D = 1.20, 2100.0
R_WB, R_D = 0.30, 0.18
IXS, IXR = 30, 50          # target shot / receiver indices


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


def hyperbolic_event(t0, v, amp, xs_positions):
    """Sparse impulse-response matrix (nrec, nshot) for one reflector."""
    M = np.zeros((NT, NX, NX)) // 1
    return None


def build_primary_matrix():
    """P0 impulse response as (NT, nrec, nshot) spike array."""
    P0 = np.zeros((NT, NX, NX))
    offs = X[None, :] - X[:, None]          # (nrec, nshot) receiver - shot
    for t0, v, R in [(T_WB, V_WB, R_WB), (T_D, V_D, R_D)]:
        t_arr = np.sqrt(t0 ** 2 + (offs / v) ** 2)
        idx = np.rint(t_arr / DT).astype(int)
        valid = idx < NT
        ridx, sidx = np.nonzero(valid)
        P0[idx[ridx, sidx], ridx, sidx] += R
    return P0


wav = ricker(F_DOM, 61, DT)
half = (len(wav) - 1) // 2
wav_zp = np.zeros(NT)
wav_zp[:half + 1] = wav[half:]
wav_zp[-half:] = wav[:half]
S = np.fft.rfft(wav_zp)
A = -np.conj(S) / (np.abs(S) ** 2 + 1e-3 * np.abs(S).max() ** 2)
A *= np.clip(np.abs(S) / (0.1 * np.abs(S).max()), 0.0, 1.0)

# --- impulse responses with surface multiples: per-frequency feedback ------
P0_imp = build_primary_matrix()
P0_f = np.fft.rfft(P0_imp, axis=0)              # (nf, nrec, nshot)

# --- explicit series construction of the data (operator physics) ----------
# The 2D SRME operator integrates over the surface; in this discrete
# teaching model the coupling is calibrated as C = 1/NX (the k-average),
# which absorbs the geometrical-spreading/obliquity factors that the
# surface operator + adaptive subtraction handle in production.
C = 1.0 / NX
M1_f = -C * np.einsum("fij,fjk->fik", P0_f, P0_f)
M1 = np.fft.irfft(M1_f, n=NT, axis=0)
M2_f = -C * np.einsum("fij,fjk->fik", np.fft.rfft(M1, axis=0), P0_f)
M2 = np.fft.irfft(M2_f, n=NT, axis=0)
P_imp = P0_imp + M1 + M2

# data with wavelet: convolve the impulse version with the wavelet
P = np.fft.irfft(np.fft.rfft(P_imp, axis=0) * S[:, None, None], n=NT, axis=0)

# SRME prediction from the DATA: M = A * C * P . P  (matrix product per f)
P_f = np.fft.rfft(P, axis=0)
M_f = np.empty_like(P_f)
for k in range(P_f.shape[0]):
    M_f[k] = A[k] * C * P_f[k] @ P_f[k]
M = np.fft.irfft(M_f, n=NT, axis=0)

# MCG for the target trace: integrand per k  (time, xk)
mcg = np.fft.irfft(A[:, None] * C * P_f[:, IXR, :] * P_f[:, :, IXS],
                   n=NT, axis=0)                # (NT, nrec=xk)

pred_trace = M[:, IXR, IXS]
true_mult_trace = P[:, IXR, IXS] - np.fft.irfft(
    np.fft.rfft(P0_imp, axis=0) * S[:, None, None], n=NT, axis=0)[:, IXR, IXS]
prim_trace = P[:, IXR, IXS] - pred_trace
p0_trace = np.fft.irfft(np.fft.rfft(P0_imp, axis=0) * S[:, None, None],
                        n=NT, axis=0)[:, IXR, IXS]

scale = lambda tr: tr / max(np.abs(tr).max(), 1e-12)

fig = plt.figure(figsize=(15.5, 9))
gs = fig.add_gridspec(2, 3, hspace=0.42, wspace=0.3)

# --- 1: model + DRP split ----------------------------------------------------
ax = fig.add_subplot(gs[0, 0])
ax.axhspan(0, 300, color="#cfe8ff", alpha=0.85)
ax.axhspan(300, 1400, color="#d9c9a8", alpha=0.9)
ax.axhline(0, color="k", lw=2)
ax.axhline(300, color="saddlebrown", lw=2)
ax.axhline(1200, color="dimgray", lw=2)
xs_, xr_, xk_ = X[IXS], X[IXR], X[40]
# leg 1: shot -> deep reflector -> DRP at surface
ax.plot([xs_, (xs_ + xk_) / 2, xk_], [0, 1200, 0], "-", color="crimson", lw=2)
# leg 2: virtual source at DRP -> water bottom -> receiver
ax.plot([xk_, (xk_ + xr_) / 2, xr_], [0, 300, 0], "--", color="darkorange", lw=2)
ax.plot(xs_, 0, "*", ms=15, color="darkorange", zorder=5)
ax.plot(xr_, 0, "v", ms=10, color="darkgreen", zorder=5)
ax.plot(xk_, 0, "o", ms=13, mfc="none", mec="crimson", mew=2.5, zorder=6)
ax.annotate("DRP = virtual source", xy=(xk_, 30), xytext=(xk_ - 260, 430),
            fontsize=10, color="crimson",
            arrowprops=dict(arrowstyle="->", color="crimson"))
ax.annotate("leg 1: a primary of\nthe shot gather", xy=(xs_ + 40, 900),
            xytext=(60, 760), fontsize=9, color="crimson",
            arrowprops=dict(arrowstyle="->", color="crimson"))
ax.annotate("leg 2: a 'primary' from\nthe virtual source", xy=(xk_ + 130, 380),
            xytext=(xk_ + 150, 640), fontsize=9, color="darkorange",
            arrowprops=dict(arrowstyle="->", color="darkorange"))
ax.set_xlabel("Lateral position (m)")
ax.set_ylabel("Depth (m)")
ax.set_ylim(1400, -60)
ax.set_title("1. Split the multiple\nat its downward reflection point")

# --- 2: input shot gather ------------------------------------------------------
ax = fig.add_subplot(gs[0, 1])
v = np.percentile(np.abs(P[:, :, IXS]), 99.5)
ax.imshow(P[:, :, IXS], extent=[X[0], X[-1], TMAX, 0], aspect="auto",
          cmap="gray", vmin=-v, vmax=v)
ax.set_xlabel("Receiver position (m)")
ax.set_ylabel("Time (s)")
ax.set_title("2. Input shot gather (xs = 750 m)\nprimaries + surface multiples")
ax.axhline(0.4, color="royalblue", ls=":", lw=1)
ax.axhline(0.8, color="crimson", ls=":", lw=1)
ax.axhline(1.2, color="royalblue", ls=":", lw=1)
ax.axhline(1.6, color="crimson", ls=":", lw=1)
ax.text(X[-1] + 15, 0.4, "WB prim.", fontsize=8, color="royalblue", va="center")
ax.text(X[-1] + 15, 0.8, "WB mult.", fontsize=8, color="crimson", va="center")
ax.text(X[-1] + 15, 1.2, "deep prim.", fontsize=8, color="royalblue", va="center")
ax.text(X[-1] + 15, 1.6, "peg-legs", fontsize=8, color="crimson", va="center")

# --- 3: MCG -------------------------------------------------------------------
ax = fig.add_subplot(gs[0, 2])
vm = np.percentile(np.abs(mcg), 99.5)
ax.imshow(mcg, extent=[X[0], X[-1], TMAX, 0], aspect="auto", cmap="gray",
          vmin=-vm, vmax=vm)
ax.set_xlabel("DRP position xk (m)")
ax.set_ylabel("Time (s)")
ax.set_title("3. Multiple contribution gather\nfor target trace (xs, xr)")
ax.plot(X[40], 0.82, "o", ms=14, mfc="none", mec="crimson", mew=2.2)
ax.annotate("apex = surface\nreflection point", xy=(X[40], 0.84),
            xytext=(X[6], 1.3), fontsize=9, color="crimson",
            arrowprops=dict(arrowstyle="->", color="crimson"))

# --- 4: predicted vs actual multiple trace ------------------------------------
ax = fig.add_subplot(gs[1, 0])
ax.plot(scale(pred_trace), np.arange(NT) * DT, "crimson", lw=1.0,
        label="predicted  $-A\\, dx\\, \\sum_k P(x_r,x_k)P(x_k,x_s)$")
ax.plot(scale(true_mult_trace), np.arange(NT) * DT, "k", lw=0.7, alpha=0.8,
        label="actual multiples (data $-$ primaries)")
ax.set_ylim(TMAX, 0)
ax.set_xlim(-1.1, 1.1)
ax.set_xlabel("Normalized amplitude")
ax.set_ylabel("Time (s)")
ax.set_title("4. Target trace (xr = 1250 m):\nprediction vs actual")
ax.legend(fontsize=8, loc="lower right")
res = np.linalg.norm(pred_trace - true_mult_trace) / np.linalg.norm(true_mult_trace)
ax.text(0.03, 0.06, f"relative mismatch: {res:.0%}", transform=ax.transAxes,
        fontsize=9, color="crimson",
        bbox=dict(fc="white", ec="crimson", alpha=0.85))

# --- 5: subtraction ------------------------------------------------------------
ax = fig.add_subplot(gs[1, 1])
after = P[:, :, IXS] - M[:, :, IXS]
ax.imshow(after, extent=[X[0], X[-1], TMAX, 0], aspect="auto", cmap="gray",
          vmin=-v, vmax=v)
ax.set_xlabel("Receiver position (m)")
ax.set_ylabel("Time (s)")
ax.set_title("5. Shot gather after\nmodel-and-subtract")

ax = fig.add_subplot(gs[1, 2])
true_prim_gather = np.fft.irfft(np.fft.rfft(P0_imp, axis=0) * S[:, None, None],
                                n=NT, axis=0)[:, :, IXS]
ax.imshow(true_prim_gather, extent=[X[0], X[-1], TMAX, 0], aspect="auto",
          cmap="gray", vmin=-v, vmax=v)
ax.set_xlabel("Receiver position (m)")
ax.set_ylabel("Time (s)")
ax.set_title("... vs true primaries\n('the truth')")

fig.suptitle("2D SRME: predict the multiple by convolving the shot gather with "
             "the receiver gather, integrated over all downward reflection "
             "points", fontsize=13.5)
fig.text(0.5, 0.012,
         "No velocity model is used anywhere: the data act as the multiple "
         "prediction operator. The prediction matches the actual multiples "
         "kinematically; residual amplitude/wavelet errors are the job of "
         "adaptive subtraction.",
         ha="center", fontsize=10, color="0.25")
fig.savefig("figures/term02_lec04/term02_lec04_srme_2d_drp.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec04_srme_2d_drp.png")
print(f"target-trace prediction mismatch: {res:.1%}")
