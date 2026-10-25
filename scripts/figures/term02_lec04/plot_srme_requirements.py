"""Figure: SRME data requirements — near offsets and regular sampling.

The prediction integrates over ALL surface positions: whatever data are
missing from the integral is missing from the prediction. Two classic
degradation modes, using the same 2-layer engine as the 2D DRP figure:

  Row 1 — reference: prediction from complete data (mismatch 8%).
  Row 2 — near-offset gap (150 m, typical streamer): the MCG loses its
          flat/short legs; the prediction of shallow reverberations is
          too weak; the subtraction leaves residuals at early times.
  Row 3 — every second shot missing (coarse shooting / aliasing): the
          MCG loses every other column; missing interference terms
          create artifact energy in the prediction and a noisier
          subtraction.

Columns: input data available to the operator (shot gather), MCG for
the target trace, predicted vs actual multiple (target trace),
subtraction residual of the target trace (numbers annotated).
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
IXS, IXR = 30, 50
C = 1.0 / NX


def ricker(f_dom, n, dt):
    t = (np.arange(n) - (n - 1) / 2) * dt
    return (1 - 2 * (np.pi * f_dom * t) ** 2) * np.exp(-(np.pi * f_dom * t) ** 2)


def build_primary_matrix():
    P0 = np.zeros((NT, NX, NX))
    offs = X[None, :] - X[:, None]
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

# complete data (truth for comparison)
P0_imp = build_primary_matrix()
P0_f = np.fft.rfft(P0_imp, axis=0)
M1_f = -C * np.einsum("fij,fjk->fik", P0_f, P0_f)
M1 = np.fft.irfft(M1_f, n=NT, axis=0)
M2_f = -C * np.einsum("fij,fjk->fik", np.fft.rfft(M1, axis=0), P0_f)
M2 = np.fft.irfft(M2_f, n=NT, axis=0)
P_full = np.fft.irfft(np.fft.rfft(P0_imp + M1 + M2, axis=0) * S[:, None, None],
                      n=NT, axis=0)
P0_w = np.fft.irfft(P0_f * S[:, None, None], n=NT, axis=0)
true_mult = P_full - P0_w


def predict(P):
    Pf = np.fft.rfft(P, axis=0)
    M_f = np.empty_like(Pf)
    for k in range(Pf.shape[0]):
        M_f[k] = A[k] * C * Pf[k] @ Pf[k]
    M = np.fft.irfft(M_f, n=NT, axis=0)
    mcg = np.fft.irfft(A[:, None] * C * Pf[:, IXR, :] * Pf[:, :, IXS], n=NT,
                       axis=0)
    return M, mcg


def with_gap(P, n_off=6):
    """Zero the first n_off near-offset traces in every shot gather."""
    Pg = P.copy()
    offs_idx = np.arange(NX)
    mask = np.abs(offs_idx[None, :] - offs_idx[:, None]) <= n_off
    Pg[:, mask] = 0.0
    return Pg


def decimate_shots(P):
    Pd = P.copy()
    Pd[:, :, 1::2] = 0.0
    return Pd

cases = [
    ("complete data (reference)", P_full, "row1"),
    ("near-offset gap: 150 m missing", with_gap(P_full), "row2"),
    ("every 2nd shot missing", decimate_shots(P_full), "row3"),
]

fig, axes = plt.subplots(3, 4, figsize=(16, 10))
t_ax = np.arange(NT) * DT

for row, (name, P_case, _) in enumerate(cases):
    M, mcg = predict(P_case)
    v = np.percentile(np.abs(P_full[:, :, IXS]), 99.5)
    vm = np.percentile(np.abs(mcg), 99.5)

    ax = axes[row, 0]
    ax.imshow(P_case[:, :, IXS], extent=[X[0], X[-1], TMAX, 0], aspect="auto",
              cmap="gray", vmin=-v, vmax=v)
    if row == 1:
        ax.axvspan(X[IXS - 6], X[IXS + 6], color="crimson", alpha=0.15)
        ax.text(X[IXS] - 130, 2.35, "gap", color="crimson", fontsize=9)
    ax.set_ylabel("Time (s)")
    ax.set_title(f"operator data ({name})", fontsize=10)

    ax = axes[row, 1]
    ax.imshow(mcg, extent=[X[0], X[-1], TMAX, 0], aspect="auto", cmap="gray",
              vmin=-vm, vmax=vm)
    ax.set_title("MCG of target trace", fontsize=10)
    if row == 2:
        for k in range(1, NX, 2):
            ax.axvline(X[k], color="crimson", alpha=0.08, lw=1)

    ax = axes[row, 2]
    sc = max(np.abs(true_mult[:, IXR, IXS]).max(), 1e-12)
    ax.plot(M[:, IXR, IXS] / sc, t_ax, "crimson", lw=0.9, label="predicted")
    ax.plot(true_mult[:, IXR, IXS] / sc, t_ax, "k", lw=0.6, alpha=0.75,
            label="actual")
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(TMAX, 0)
    ax.legend(fontsize=8, loc="upper right")
    ax.set_title("target trace: predicted vs actual", fontsize=10)
    if row == 0:
        ax.legend(fontsize=8, loc="lower right")

    ax = axes[row, 3]
    resid = true_mult[:, IXR, IXS] - M[:, IXR, IXS]
    rel = np.linalg.norm(resid) / np.linalg.norm(true_mult[:, IXR, IXS])
    ax.plot(resid / sc, t_ax, "royalblue", lw=0.8)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(TMAX, 0)
    ax.set_title(f"prediction error: {rel:.0%}", fontsize=10, color="royalblue")
    if row == 0:
        print(f"reference mismatch: {rel:.1%}")

for ax in axes[2]:
    ax.set_xlabel("m / position (m)")
axes[2, 0].set_xlabel("Receiver position (m)")
axes[2, 1].set_xlabel("DRP position xk (m)")
axes[2, 2].set_xlabel("Normalized amplitude")
axes[2, 3].set_xlabel("Normalized amplitude")

fig.suptitle("SRME is an integral over the surface: missing data = missing "
             "prediction", fontsize=14)
fig.text(0.5, 0.012,
         "Near offsets feed the shallow reverberation prediction (their legs "
         "are the short, flat MCG contributions); missing shots create "
         "aliasing-type artifacts. Production fixes: reciprocity, near-offset\n"
         "reconstruction (Radon extrapolation), shot interpolation / 5D "
         "regularization BEFORE SRME — the price of a fully data-driven method.",
         ha="center", fontsize=10, color="0.25")
fig.tight_layout(rect=(0, 0.04, 1, 0.94))
fig.savefig("figures/term02_lec04/term02_lec04_srme_requirements.png",
            dpi=150, bbox_inches="tight")
print("saved term02_lec04_srme_requirements.png")
