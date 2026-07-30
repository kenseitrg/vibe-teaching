"""
Term 3 Lecture 06 — Figure 6: convergence of ALFT matching pursuit (Sec. 4.4).

Pedagogical point
-----------------
The anti-leakage Fourier transform (ALFT) estimates the spatial spectrum by
MATCHING PURSUIT with a Fourier dictionary: at every iteration it takes the
non-uniform DFT of the current residual, selects the SINGLE strongest
wavenumber component, and subtracts it.  Repeating this "peeling" concentrates
the model on the few dominant components; the accumulated selections form the
final sparse spectrum used for reconstruction.

To make the convergence tangible we use the simplest possible data: a sum of
three complex harmonics with well-separated, UNEQUAL amplitudes, sampled at
IRREGULAR spatial positions.  The true spectrum is therefore exactly three
spikes, so we can watch the algorithm find them one by one:

  * iteration 0 -- the input data; the residual is the full signal and its
    spectrum is already smeared with leakage by the irregular sampling;
  * iteration 1 -- the strongest harmonic is captured; the residual is still
    large and its spectrum is full of leakage sidelobes (because the Fourier
    basis is non-orthogonal on the irregular grid);
  * iteration 3 -- all three true spikes have been captured; the residual has
    collapsed to a few percent of its starting energy;
  * iteration 8 -- converged; the residual is essentially zero and the
    accumulated spectrum matches the true three spikes.

The unequal amplitudes are deliberate: matching pursuit peels strongest-first,
so the big spike is found first and the small ones later.  Only POSITIVE
wavenumbers are displayed -- the data are a sum of complex exponentials, so the
spectrum is one-sided and showing k >= 0 keeps the panels uncluttered.

Layout: 4 rows (the input at iteration 0, then iterations 1, 3, 8) x 3 columns:
  (a) spatial residual  -- the irregular samples that remain to be explained;
  (b) residual spectrum -- its non-uniform DFT, losing its peaks as we peel;
  (c) accumulated spectrum vs. the true spectrum (faint markers) -- the sparse
      model that converges onto the three true spikes.

Self-contained: numpy + scipy + matplotlib only.
"""

import os

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Data: three complex harmonics, sampled at irregular positions
# ---------------------------------------------------------------------------
N = 50                       # number of irregular spatial samples
L = 1.0                      # spatial aperture (normalised units)
JITTER = 0.30                # jitter as a fraction of the mean sample spacing
K_TRUE = np.array([3.0, 7.0, 12.0])      # true wavenumbers (cycles / aperture)
AMPS = np.array([1.0, 0.7, 0.5])         # unequal -> strongest peeled first
RNG = np.random.default_rng(1)

# irregular sample positions: regular grid + bounded random jitter
x_reg = (np.arange(N) + 0.5) / N * L
jitter = JITTER / N
x = np.sort(np.clip(x_reg + RNG.uniform(-jitter, jitter, N), 0.0, L))

# random phases so the signal does not look pathologically symmetric
phases = RNG.uniform(-np.pi, np.pi, len(K_TRUE))
signal = np.sum(
    AMPS[:, None] * np.exp(1j * (2 * np.pi * K_TRUE[:, None] * x[None, :] + phases[:, None])),
    axis=0,
)

# sample weights ~ 1 / sampling density (midpoint spacing between samples)
x_pad = np.concatenate([[0.0], 0.5 * (x[:-1] + x[1:]), [L]])
weights = np.diff(x_pad)
weights /= weights.sum()

# ---------------------------------------------------------------------------
# Non-uniform DFT and matching-pursuit ALFT
# ---------------------------------------------------------------------------
K_TEST = np.arange(0.0, 16.01, 0.02)     # positive test wavenumbers, fine grid


def non_uniform_dft(residual):
    """Weighted non-uniform DFT of `residual` at every test wavenumber."""
    steering = np.exp(-1j * 2 * np.pi * K_TEST[:, None] * x[None, :])
    return steering @ (weights * residual)


def run_alft(n_iters):
    """Run matching-pursuit ALFT, returning per-iteration snapshots.

    Returns a list of snapshots; index 0 is the input (iteration 0) and index
    i >= 1 is the state after iteration i.  Each snapshot has:
      residual      -- spatial residual after this iteration
      resid_spectrum-- non-uniform DFT of that residual
      selected_k    -- wavenumber selected on this iteration
      accum         -- dict {k: complex amplitude} accumulated so far
    """
    residual = signal.copy()
    accum = {}
    # iteration 0: the input itself, before any peeling
    first_spectrum = non_uniform_dft(residual)
    snapshots = [
        {
            "residual": residual.copy(),
            "resid_spectrum": first_spectrum.copy(),
            "selected_k": K_TEST[np.argmax(np.abs(first_spectrum))],
            "accum": {},
        }
    ]
    for _ in range(n_iters):
        spectrum = non_uniform_dft(residual)
        k_star = K_TEST[np.argmax(np.abs(spectrum))]
        # least-squares amplitude for this single component on the irregular grid
        basis = np.exp(1j * 2 * np.pi * k_star * x)
        amp = np.sum(weights * residual * np.conj(basis)) / np.sum(weights * np.abs(basis) ** 2)
        accum[k_star] = accum.get(k_star, 0.0) + amp
        residual = residual - amp * basis
        snapshots.append(
            {
                "residual": residual.copy(),
                "resid_spectrum": non_uniform_dft(residual),
                "selected_k": k_star,
                "accum": dict(accum),
            }
        )
    return snapshots


SHOW_ITERS = [0, 1, 3, 8]
snapshots = run_alft(max(SHOW_ITERS))
chosen = [snapshots[i] for i in SHOW_ITERS]

# initial (iteration 0) residual spectrum, for a consistent column (b) y-limit
initial_resid_spectrum = non_uniform_dft(signal)

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
COL_TITLES = [
    "(a) Spatial residual",
    "(b) Spectrum of residual",
    "(c) Accumulated spectrum",
]

# shared y-limits per column keep the shrinking / growing visually honest
resid_lim = 1.1 * np.max(np.abs(signal))
spec_lim = 1.1 * np.max(np.abs(initial_resid_spectrum))
accum_lim = 1.1 * np.max(AMPS)

cmap = plt.get_cmap("viridis")
row_colors = [cmap(v) for v in (0.12, 0.38, 0.62, 0.88)]   # darker -> lighter down the rows
select_color = "#d62728"                                    # red: newly selected component

fig, axes = plt.subplots(4, 3, figsize=(10, 9.5), sharex="col")
fig.subplots_adjust(hspace=0.55, wspace=0.30, left=0.07, right=0.98, top=0.93, bottom=0.06)

for row, (snap, it, color) in enumerate(zip(chosen, SHOW_ITERS, row_colors)):
    # ---- (a) spatial residual: irregular samples that remain ----
    ax = axes[row, 0]
    ax.scatter(x, snap["residual"].real, s=22, color=color, edgecolor="k",
               linewidth=0.4, zorder=3, label="residual samples")
    ax.axhline(0.0, color="0.6", linewidth=0.6, zorder=1)
    ax.set_ylim(-resid_lim, resid_lim)
    rms = np.sqrt(np.mean(np.abs(snap["residual"]) ** 2))
    rms0 = np.sqrt(np.mean(np.abs(signal) ** 2))
    ax.text(0.02, 0.95, f"RMS = {100 * rms / rms0:.1f}%",
            transform=ax.transAxes, va="top", ha="left", fontsize=8,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="0.7", alpha=0.85))

    # ---- (b) spectrum of the residual ----
    ax = axes[row, 1]
    ax.plot(K_TEST, np.abs(snap["resid_spectrum"]), color=color, linewidth=1.3)
    ax.scatter([snap["selected_k"]], [np.max(np.abs(snap["resid_spectrum"]))],
               marker="v", color=select_color, s=40, zorder=4,
               label="next picked")
    ax.set_ylim(0, spec_lim)

    # ---- (c) accumulated spectrum vs. true spectrum ----
    ax = axes[row, 2]
    # true spectrum as faint reference markers
    ax.scatter(K_TRUE, AMPS, marker="o", facecolor="none", edgecolor="0.45",
               s=70, linewidth=1.3, zorder=2, label="true spectrum")
    # accumulated selections as stems (none yet at iteration 0)
    ks = np.array(sorted(snap["accum"]))
    if ks.size:
        amps = np.abs(np.array([snap["accum"][k] for k in ks]))
        markerline, stemlines, baseline = ax.stem(
            ks, amps, linefmt="-", markerfmt="o", basefmt=" "
        )
        plt.setp(stemlines, color=color, linewidth=1.3)
        plt.setp(markerline, color=color, markersize=5, markeredgecolor="k",
                 markeredgewidth=0.4)
    ax.set_ylim(0, accum_lim)

    # ---- row label ----
    label = "input\n(iter 0)" if it == 0 else f"iteration {it}"
    axes[row, 0].text(-0.32, 0.5, label, transform=axes[row, 0].transAxes,
                      rotation=90, va="center", ha="center", fontsize=10,
                      fontweight="bold")

# ---- shared cosmetics ----
for col in range(3):
    axes[-1, col].set_xlabel("spatial position $x$" if col == 0 else "wavenumber $k$ (cycles / aperture)")
    axes[0, col].set_title(COL_TITLES[col], fontsize=11)

for ax in axes[:, 0]:
    ax.set_ylabel("residual amplitude")
for ax in axes[:, 1]:
    ax.set_ylabel("|spectrum|")
for ax in axes[:, 2]:
    ax.set_ylabel("|amplitude|")

for ax in axes[:, 0]:
    ax.set_xlim(0, L)
for ax in axes[:, 1:].ravel():
    ax.set_xlim(0, 16)

# a single combined legend
handles = [
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=cmap(0.5),
               markeredgecolor="k", markersize=7, label="residual / accumulated"),
    plt.Line2D([0], [0], marker="v", color="w", markerfacecolor=select_color,
               markersize=8, label="newly picked component"),
    plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="none",
               markeredgecolor="0.45", markersize=9, markeredgewidth=1.3,
               label="true spectrum"),
]
fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False,
           fontsize=9, bbox_to_anchor=(0.5, -0.005))

fig.suptitle("ALFT matching pursuit: peeling the spectrum converges on the true components",
             fontsize=12, y=0.97)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "figures", "term03_lec06")
OUT_DIR = os.path.abspath(OUT_DIR)
os.makedirs(OUT_DIR, exist_ok=True)
out_path = os.path.join(OUT_DIR, "term03_lec06_alft_iteration.png")
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"wrote {out_path}")
