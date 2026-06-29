"""
Gauss–Seidel iteration for the 4-component surface-consistent model.

Shows convergence of the RMS residual over iterations, with annotation
explaining the algorithm cycle (source → receiver → offset → CMP).

Undergraduate seismic data processing — Term 1 Lecture 03.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Simulate convergence behaviour --------------------------------------
# We don't run a real Gauss-Seidel solver; we generate realistic-looking
# convergence curves that match the textbook behaviour (Hatton et al.):
# rapid decay in the first 4-5 iterations, then plateau.

n_iterations = 10

# True residual norm (no noise) would approach 0. We add a noise floor.
noise_floor = 0.002  # residual level where noise dominates

# Generate two curves: one for a well-behaved dataset, one for a noisy one
rms_clean = 0.10 * np.exp(-np.arange(n_iterations) * 1.2) + 0.002
rms_noisy = 0.10 * np.exp(-np.arange(n_iterations) * 1.0) + 0.010

# Add a little random jitter
np.random.seed(3)
rms_clean += 0.003 * np.random.randn(n_iterations)
rms_noisy += 0.004 * np.random.randn(n_iterations)

# Ensure monotonic (Gauss-Seidel is monotonic in residual)
rms_clean = np.minimum.accumulate(rms_clean)
rms_noisy = np.minimum.accumulate(rms_noisy)

# --- Plot ----------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 5))
fig.suptitle('Gauss–Seidel iteration for surface-consistent statics',
             fontsize=14)

# Main convergence curve
ax.plot(np.arange(1, n_iterations + 1), rms_clean * 1000,
        'C0-o', linewidth=2, markersize=7, label='Clean data')
ax.plot(np.arange(1, n_iterations + 1), rms_noisy * 1000,
        'C1-s', linewidth=2, markersize=7, label='Noisy data',
        alpha=0.7)

# Mark 4-5 sweeps region
ax.axvspan(4.5, 5.5, color='lightgreen', alpha=0.15)
ax.annotate('Convergence\ntypically in\n4–5 sweeps',
            xy=(5, 0.5), xytext=(6.5, 3.5),
            fontsize=10, color='green',
            arrowprops=dict(arrowstyle='->', color='green'),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen',
                      alpha=0.5))

ax.set_xlabel('Iteration (sweep number)')
ax.set_ylabel('RMS residual (ms)')
ax.set_xticks(np.arange(1, n_iterations + 1))
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 11)

# --- Inset explaining the cycle ------------------------------------------
inset_ax = fig.add_axes([0.55, 0.18, 0.35, 0.32])
inset_ax.set_xlim(0, 1)
inset_ax.set_ylim(0, 1)
inset_ax.axis('off')

# Draw the cycle as text
cycle_text = ("One iteration (sweep):\n"
              "1. Update sources $s_i$\n"
              "2. Update receivers $r_j$\n"
              "3. Update offset terms $h_k$\n"
              "4. Update CMP terms $c_l$")
inset_ax.text(0.15, 0.85, cycle_text, fontsize=8.5, va='top',
              fontfamily='monospace',
              bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow',
                        edgecolor='grey'))

# Draw a simple cycle arrow
inset_ax.annotate('', xy=(0.85, 0.15), xytext=(0.15, 0.15),
                  arrowprops=dict(arrowstyle='->', color='C0', lw=1.5))
inset_ax.text(0.5, 0.08, 'repeat until convergence',
              ha='center', fontsize=7.5, style='italic', color='grey')

plt.savefig('figures/term01_lec03/term01_lec03_gauss_seidel.png',
            dpi=150, bbox_inches='tight')
plt.close()
print('Saved: term01_lec03_gauss_seidel.png')
