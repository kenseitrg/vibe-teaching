---
title: Matching pursuit
status: draft
sources:
  - tropp2007_omp
  - xu2010_antileakage_fourier_transform
tags: [sparse-recovery, matching-pursuit, omp, regularization, signal-processing]
---

# Matching pursuit

Matching pursuit (MP) is a greedy algorithm that builds a **sparse** representation of a signal as a sum of a few atoms chosen from a (usually over-complete) **dictionary**. In seismic [regularization](seismic_data_regularization.md) the dictionary is the set of Fourier basis functions, and matching pursuit is the engine inside the [anti-leakage Fourier transform](anti_leakage_fourier_transform.md).

## The idea

Given data $d$ and a dictionary of atoms $\{g_k\}$, find a small set of atoms whose weighted sum approximates $d$:

$$d \approx \sum_{j} c_j\, g_{k_j}.$$

Matching pursuit builds this one atom at a time:

1. Compute the correlation (inner product) of the current **residual** $r$ with every atom.
2. Pick the atom $g_{k^\*}$ with the **largest** correlation — it best explains the remaining energy.
3. Subtract its contribution from the residual: $r \leftarrow r - c\,g_{k^\*}$.
4. Repeat until the residual is small enough.

Because each step removes the energy just explained, the crosstalk (leakage) between non-orthogonal atoms is cleaned up iteratively. This is exactly why ALFT defeats [spectral leakage](spatial_spectral_leakage.md) on irregular grids.

## Variants

- **Basic matching pursuit (MP)** — the procedure above. Simple, but the same atom can be re-selected and convergence can be slow.
- **Orthogonal matching pursuit (OMP)** — after selecting an atom, re-solve a least-squares fit over *all* atoms chosen so far, so the residual is kept orthogonal to the selected subspace. OMP converges faster and, under suitable conditions on the dictionary, reliably recovers a signal with $m$ non-zero coefficients from $O(m\ln d)$ measurements (Tropp & Gilbert 2007).

OMP is the theoretically grounded version and underpins the "orthogonal matching pursuit" extensions used in modern regularization.

## Why it suits seismic data

Seismic wavefields are **sparse in the spatial Fourier domain** — a few dominant dips/events account for most of the energy at each temporal frequency. Matching pursuit exploits this sparsity directly: it concentrates the model on the few strongest components and leaves the rest as residual noise. The same logic applies with other dictionaries (e.g. Radon — see [Radon interpolation](radon_interpolation.md), or curvelets), which is the unifying "sparsity in a transform domain" view behind all modern reconstruction methods.

## Related concepts

- [Anti-leakage Fourier transform](anti_leakage_fourier_transform.md)
- [Spatial spectral leakage](spatial_spectral_leakage.md)
- [Radon interpolation](radon_interpolation.md)
- [Seismic data regularization](seismic_data_regularization.md)

## Sources

- Tropp & Gilbert (2007) — theory of signal recovery via orthogonal matching pursuit.
- Xu, Zhang & Lambaré (2010) — matching pursuit with a Fourier dictionary as the ALFT algorithm.
