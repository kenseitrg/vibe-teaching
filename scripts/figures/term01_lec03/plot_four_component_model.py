"""
Four-component surface-consistent decomposition of residual statics.

Shows 5 panels:
  s_i: source static (constant per source index)
  r_j: receiver static (constant per receiver index)
  h_k: offset-dependent residual moveout
  c_l: CMP structural term (geology)
  Total = sum of components

Undergraduate seismic data processing — Term 1 Lecture 03.
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Make synthetic component values --------------------------------------
n_sources = 12
n_receivers = 12
n_offsets = 10
n_cmps = 12

# Source statics: random with spatial trend
np.random.seed(7)
s_i = 0.008 * np.sin(np.linspace(0, np.pi, n_sources)) + \
      0.003 * np.random.randn(n_sources)

# Receiver statics: random with some short-wavelength variation
r_j = 0.010 * np.sin(np.linspace(0, 2 * np.pi, n_receivers) + 0.5) + \
      0.004 * np.random.randn(n_receivers)

# Offset residual moveout: small parabolic curve
h_k = 0.005 * (np.linspace(-1, 1, n_offsets)) ** 2 - 0.002
h_k += 0.001 * np.random.randn(n_offsets)

# CMP structural term: a gently dipping layer
c_l = 0.03 * np.linspace(0, 1, n_cmps)

# Total for a specific combination (e.g., source=3, receiver=5, offset=4, cmp=7)
# We'll construct a 3-D-ish total surface for display:
# Fix offset index = 4 (mid-offset), vary source and CMP
offset_fixed = 5
total = np.zeros((n_sources, n_cmps))
for i in range(n_sources):
    for l in range(n_cmps):
        total[i, l] = s_i[i] + r_j[l % n_receivers] + \
                      h_k[offset_fixed] + c_l[l]

# Also compute total for a fixed source and receiver to show offset dependence
source_fixed = 3
receiver_fixed = 5
total_offset = np.zeros(n_offsets)
for k in range(n_offsets):
    total_offset[k] = s_i[source_fixed] + r_j[receiver_fixed] + \
                      h_k[k] + c_l[source_fixed]  # pick CMP near source

# --- Plot ----------------------------------------------------------------
fig, axes = plt.subplots(2, 3, figsize=(12, 7))
fig.suptitle('Surface-consistent 4-component decomposition of residual statics',
             fontsize=14, y=1.02)

# Flatten axes for easy indexing
ax = axes.flat

# (1) Source statics
ax[0].bar(range(n_sources), s_i * 1000, color='C0', alpha=0.8)
ax[0].set_xlabel('Source index $i$')
ax[0].set_ylabel('$s_i$ (ms)')
ax[0].set_title('Source static $s_i$')
ax[0].grid(True, alpha=0.3)

# (2) Receiver statics
ax[1].bar(range(n_receivers), r_j * 1000, color='C1', alpha=0.8)
ax[1].set_xlabel('Receiver index $j$')
ax[1].set_ylabel('$r_j$ (ms)')
ax[1].set_title('Receiver static $r_j$')
ax[1].grid(True, alpha=0.3)

# (3) Offset residual moveout
offsets = np.linspace(0, 3000, n_offsets)
ax[2].plot(offsets, h_k * 1000, 'C2-o', linewidth=1.8, markersize=6)
ax[2].axhline(0, color='grey', linestyle=':', linewidth=0.8)
ax[2].set_xlabel('Offset (m)')
ax[2].set_ylabel('$h_k$ (ms)')
ax[2].set_title('Offset term $h_k$')
ax[2].grid(True, alpha=0.3)

# (4) CMP structural term
ax[3].plot(range(n_cmps), c_l * 1000, 'C3-s', linewidth=1.8, markersize=6)
ax[3].set_xlabel('CMP index $l$')
ax[3].set_ylabel('$c_l$ (ms)')
ax[3].set_title('CMP structure $c_l$ (geology)')
ax[3].grid(True, alpha=0.3)

# (5) Total for fixed offset, varying source and CMP
im = ax[4].imshow(total * 1000, aspect='auto', origin='lower',
                   cmap='RdBu_r', interpolation='nearest')
ax[4].set_xlabel('CMP index $l$')
ax[4].set_ylabel('Source index $i$')
ax[4].set_title('Total $\\Delta t_{ijkl}$ (fixed offset)')
plt.colorbar(im, ax=ax[4], label='ms', shrink=0.8)

# (6) Total with offset dependence for fixed source/receiver
ax[5].plot(offsets, total_offset * 1000, 'k-o', linewidth=1.8,
           markersize=6, markerfacecolor='white')
ax[5].set_xlabel('Offset (m)')
ax[5].set_ylabel('$\\Delta t$ (ms)')
ax[5].set_title(f'Total (source={source_fixed+1}, receiver={receiver_fixed+1})')
ax[5].grid(True, alpha=0.3)

# Hide unused subplot (2x3 = 6, we use all 6)
plt.tight_layout()
plt.savefig('figures/term01_lec03/term01_lec03_four_component_model.png',
            dpi=150, bbox_inches='tight')
plt.close()
print('Saved: term01_lec03_four_component_model.png')
