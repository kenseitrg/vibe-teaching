"""
Term 3 Lecture 06 — Figure 2: Irregular acquisition versus a regular target
grid in the CMP-offset domain (fold map), shown for a single inline.

Pedagogical point
-----------------
Downstream algorithms (common-offset migration, SRME, AVO) expect data on a
REGULAR grid of midpoint (CMP) and offset.  A real orthogonal land survey does
not deliver that.  Receiver lines and source lines are perpendicular, with
finite spreads and line/point spacings, so the number of traces falling in each
(CMP, offset) bin -- the FOLD -- is irregular, banded and gappy.

For a SINGLE INLINE the effect is especially clear: the traces that image that
inline come from a discrete set of receiver/source lines, so their offsets
cluster in bands (set by the line spacings) with gaps in between, and the fold
varies strongly along the line.  This is the input that common-offset migration
must regularize.

This figure shows the fold (trace count per CMP-offset bin) for one inline of:

  (a) a typical orthogonal land geometry
        receiver line spacing 300 m, receiver point interval 50 m
        source   line spacing 300 m, source   point interval 50 m
      -> an irregular, banded, gappy fold distribution; and

  (b) the regularized target for common-offset migration
      -> a clean, uniform regular grid: every (CMP, offset) bin filled to the
         same designed fold, independent of where the data were acquired.

The lower row collapses each fold map to its average fold per offset bin:

  (c) recorded fold -- varies strongly with offset (banded, decaying);
  (d) regularized fold -- flat, the uniform coverage common-offset migration
      requires.

The output grid (b) is fixed by the migration's requirements, not by where the
acquisition happens to be dense or missing.

Self-contained: numpy + matplotlib only.
"""

import os

import numpy as np

# ---------------------------------------------------------------------------
# Orthogonal land geometry
# ---------------------------------------------------------------------------
RL = 300.0          # receiver line spacing (crossline), m
RP = 50.0           # receiver point interval (inline), m
SL = 300.0          # source line spacing (inline), m
SP = 50.0           # source point interval (crossline), m

# Patch extents (kept modest so the finite-spread edges are clearly visible).
IL_MIN, IL_MAX = 0.0, 2400.0      # inline extent (receiver lines run inline)
XL_MIN, XL_MAX = 0.0, 1200.0      # crossline extent
MAX_OFFSET = 1500.0               # maximum recorded source-receiver offset, m

# The inline to display: a single crossline bin of midpoints.  The bin width is
# one receiver-line spacing, which averages enough traces for a smooth fold map
# while still showing the irregular, gappy offset coverage of the geometry.
MY_TARGET = (XL_MIN + XL_MAX) / 2.0   # inline centred in the patch (m)
XL_BIN = RL                            # crossline width of one inline bin (m)

# Build receiver and source point lists.
recv_x = np.arange(IL_MIN, IL_MAX + RP, RP)          # receivers along inline
recv_lines = np.arange(XL_MIN, XL_MAX + RL, RL)      # receiver line crossline pos
src_y = np.arange(XL_MIN, XL_MAX + SP, SP)           # sources along crossline
src_lines = np.arange(IL_MIN, IL_MAX + SL, SL)       # source line inline pos

RX, RY = np.meshgrid(recv_x, recv_lines)             # receiver coordinates
RX, RY = RX.ravel(), RY.ravel()
SX, SY = np.meshgrid(src_lines, src_y)               # source coordinates
SX, SY = SX.ravel(), SY.ravel()

# Pair every source with receivers within MAX_OFFSET (vectorised, in chunks to
# bound memory).  Accumulate midpoint (inline & crossline) and offset per trace.
mx_list, my_list, off_list = [], [], []
CHUNK = 64
for i0 in range(0, SX.size, CHUNK):
    sx = SX[i0:i0 + CHUNK, None]
    sy = SY[i0:i0 + CHUNK, None]
    dx = RX[None, :] - sx
    dy = RY[None, :] - sy
    off = np.sqrt(dx**2 + dy**2)
    mask = off <= MAX_OFFSET
    mx_list.append(((sx + RX[None, :]) / 2.0)[mask])   # midpoint inline
    my_list.append(((sy + RY[None, :]) / 2.0)[mask])   # midpoint crossline
    off_list.append(off[mask])

mx_all = np.concatenate(mx_list)
my_all = np.concatenate(my_list)
off_all = np.concatenate(off_list)

# Restrict to the single inline (midpoint crossline within the inline bin).
inline_mask = np.abs(my_all - MY_TARGET) <= XL_BIN / 2.0
mx = mx_all[inline_mask]
off = off_all[inline_mask]

# ---------------------------------------------------------------------------
# Fold map: trace count per (CMP-inline, offset) bin
# ---------------------------------------------------------------------------
CMP_BIN = 25.0        # CMP bin size (inline) = RP / 2, m
OFF_BIN = 50.0        # offset bin size, m

cmp_edges = np.arange(IL_MIN / 2, IL_MAX / 2 + CMP_BIN, CMP_BIN)
off_edges = np.arange(0.0, MAX_OFFSET + OFF_BIN, OFF_BIN)

fold, _, _ = np.histogram2d(mx, off, bins=[cmp_edges, off_edges])
# fold shape: (n_cmp, n_off)

# Diagnostics to tune the contrast.
pop = fold[fold > 0]
print(f"traces (inline)  : {mx.size:,}  (of {mx_all.size:,} total)")
print(f"inline           : my = {MY_TARGET:g} m, bin width {XL_BIN:g} m")
print(f"fold grid        : {fold.shape}  (CMP x offset)")
print(f"fold (populated) : min {pop.min():.0f}, max {pop.max():.0f}, "
      f"mean {pop.mean():.1f}, std {pop.std():.1f}")
print(f"empty bins       : {100 * (fold == 0).mean():.1f}%")
print(f"coeff. of var.   : {pop.std() / pop.mean():.2f}")

# ---------------------------------------------------------------------------
# Regularized target: uniform fold on a regular (CMP, offset) grid.
# ---------------------------------------------------------------------------
target_fold = int(np.round(np.median(pop)))          # designed uniform fold
regular = np.full_like(fold, target_fold, dtype=float)

# ---------------------------------------------------------------------------
# Average fold per offset bin (collapse the CMP axis): the total fold at each
# offset divided by the number of CMP bins, empty bins included.
# ---------------------------------------------------------------------------
avg_fold = fold.mean(axis=0)            # (n_off,) recorded
avg_regular = regular.mean(axis=0)      # (n_off,) uniform = target_fold

# ---------------------------------------------------------------------------
# Figure: 2x2.  Top row = fold maps; bottom row = average fold vs offset.
# Every panel's x-axis is offset, so all panels share x; each row shares its
# own y-axis (CMP for the maps, fold for the curves).
# ---------------------------------------------------------------------------
import matplotlib.pyplot as plt

COL_REC = "#D55E00"     # recorded / irregular (vermillion, Wong palette)
COL_REG = "#0072B2"     # regularized (blue, Wong palette)

cmp_centers = 0.5 * (cmp_edges[:-1] + cmp_edges[1:])
off_centers = 0.5 * (off_edges[:-1] + off_edges[1:])
EXTENT = [off_centers[0], off_centers[-1], cmp_centers[-1], cmp_centers[0]]

vmax = max(fold.max(), regular.max())

fig, axes = plt.subplots(
    2, 2, figsize=(10, 8.6), sharex="all", sharey="row",
    layout="constrained", gridspec_kw={"height_ratios": [1.5, 1.0]},
)
ax_a, ax_b = axes[0]
ax_c, ax_d = axes[1]

# ---- top row: fold maps ----------------------------------------------------
for ax, data, title in (
    (ax_a, fold, "(a) Orthogonal geometry\n(recorded fold, one inline)"),
    (ax_b, regular, "(b) Regularized target\n(common-offset migration)"),
):
    im = ax.imshow(data.T, origin="lower", aspect="auto", extent=EXTENT,
                   cmap="cividis", vmin=0, vmax=vmax, interpolation="nearest")
    ax.set_title(title, fontsize=10.5)

ax_a.set_ylabel("CMP / midpoint inline (m)")
fig.colorbar(im, ax=[ax_a, ax_b], label="Traces per CMP-offset bin (fold)",
             shrink=0.9)

# ---- bottom row: average fold vs offset ------------------------------------
ax_c.plot(off_centers, avg_fold, color=COL_REC, lw=1.8)
ax_d.plot(off_centers, avg_regular, color=COL_REG, lw=1.8)

ax_c.set_title("(c) Average fold vs offset \u2014 recorded", fontsize=10.5)
ax_d.set_title("(d) Average fold vs offset \u2014 regularized", fontsize=10.5)
ax_c.set_ylabel("Average fold per offset bin")
ax_c.set_xlabel("Offset (m)")
ax_d.set_xlabel("Offset (m)")
for ax in (ax_c, ax_d):
    ax.grid(True, alpha=0.3)

ymax = max(avg_fold.max(), avg_regular.max())
ax_c.set_ylim(0, ymax * 1.12)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
out_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                       "figures", "term03_lec06")
out_dir = os.path.abspath(out_dir)
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "term03_lec06_regular_vs_irregular.png")
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"Saved figure to {out_path}")
