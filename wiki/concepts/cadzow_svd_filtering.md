---
title: SVD and Cadzow filtering
status: draft
sources:
  - cadzow_best_practice
tags: [svd, cadzow, eigenvalue-filter, rank-reduction, random-noise, stationary-noise, signal-subspace]
---

# SVD and Cadzow filtering

SVD (Singular Value Decomposition) and Cadzow filtering are **rank-reduction** methods for noise attenuation. The core idea is that seismic signal lives in a low-dimensional subspace, while random noise fills a high-dimensional subspace.

## SVD on a trace matrix

Organize $M$ traces (each of length $N$) as columns of an $N \times M$ data matrix $\mathbf{D}$:

$$ \mathbf{D} = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^T $$

- $\mathbf{U}$: left singular vectors (trace-shaped basis functions).
- $\mathbf{V}$: right singular vectors (spatial patterns across traces).
- $\boldsymbol{\Sigma}$: diagonal matrix of singular values $\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_r > 0$.

**Noise attenuation**: keep only the $K$ largest singular values and reconstruct:

$$ \mathbf{D}_\text{denoised} = \sum_{i=1}^K \sigma_i \mathbf{u}_i \mathbf{v}_i^T $$

The truncated singular values ($\sigma_{K+1} \dots \sigma_r$) are assumed to represent random noise.

## Two SVD filtering strategies

The same SVD decomposition supports two opposite strategies depending on the noise type:

### Strategy 1: Remove random noise — keep the largest singular values

If the signal is low-rank and the noise is random (incoherent), the singular-value spectrum shows a **knee**: large values for signal, small values for random noise. Keep the $K$ largest singular values and discard the rest.

- For a single dipping event, $K = 1$ captures it perfectly.
- For multiple events with different dips, $K$ equals the number of distinct events.
- Random noise raises all singular values slightly; the knee becomes less distinct but is usually still visible.

### Strategy 2: Remove strong stationary noise — discard the largest singular values

When the record contains **strong stationary noise** — coherent, repeatable energy that is consistent across traces (e.g., ground roll, machine vibration, power-line hum, repetitive cultural noise) — the situation is reversed. The stationary noise has high energy and high spatial coherence, so it dominates the **first few (largest) singular values**. The signal and random noise occupy the remaining smaller singular values.

In this case, **discard the largest singular components and keep the rest**:

$$ \mathbf{D}_\text{denoised} = \sum_{i=K+1}^{r} \sigma_i \mathbf{u}_i \mathbf{v}_i^T $$

where $K$ singular values corresponding to the stationary noise are removed.

**When this works well:**

- The noise is much stronger than the signal (high energy in the first few components).
- The noise is spatially coherent and approximately stationary across the analysis window.
- The signal and noise occupy **different** parts of the singular-value spectrum.

**Limitations:**

- If signal and noise overlap in the singular-value spectrum, removing the top components also removes signal.
- The approach assumes the noise is stationary within the analysis window — if the noise character changes trace to trace, it spreads across more singular values and cannot be cleanly separated.

## Cadzow filtering (Hankel-SVD)

Raw SVD operates on the trace matrix directly. **Cadzow filtering** is typically applied in the **F-X domain**: the input to the Hankel-SVD transform is not the raw seismic gather but the **FX spectrum of a chosen analysis window**.

The workflow:

1. Select a spatial window of $M$ adjacent traces.
2. Fourier-transform each trace in time, obtaining complex amplitudes $X_n(f)$ at each frequency $f$.
3. For each frequency $f$, form a Hankel matrix $\mathbf{H}(f)$ from the spatial sequence $X_0(f), X_1(f), \dots, X_{M-1}(f)$. A Hankel matrix has constant skew-diagonals.
4. Compute SVD of $\mathbf{H}(f)$ and truncate to rank $K$.
5. Flatten the rank-truncated Hankel matrix back to a 1D sequence by averaging along the anti-diagonals.
6. Inverse-Fourier-transform back to the time domain.

**Why the FK domain**: a single plane wave at frequency $f$ produces a rank-1 Hankel matrix in the F-X domain. Multiple plane waves produce a rank-$p$ Hankel matrix. By forcing low rank per frequency, we keep only the plane-wave structure and discard the noise — which appears as energy spread across all singular values.

## KL transform

The Karhunen-Loève (KL) transform decomposes the data into uncorrelated random vectors. For a zero-mean data matrix, KL is mathematically equivalent to performing SVD on the covariance matrix $\mathbf{D}^T \mathbf{D}$. The KL components are the right singular vectors, ranked by eigenvalue. Truncating KL components is the same as SVD rank truncation of the covariance matrix.

## Practical notes

- Because Cadzow operates per-frequency in the F-X domain, the analysis window is defined in the **spatial** dimension (number of traces), not in time. The time dimension is handled by the Fourier transform.
- The window is typically applied to **flattened** gathers (after NMO or a dip scan) so that events are approximately horizontal — this minimizes the rank of the signal subspace at each frequency.
- The spatial window length (number of traces) creates a trade-off: longer windows capture more of the wavelet character but increase the rank of the signal subspace and may span varying dips.
- Over-aggressive rank truncation damages AVO and removes weak events.

## Connection to other methods

- **FX-deconvolution**: Cadzow in the F-X domain is equivalent to F-X deconvolution under certain conditions.
- **FK filtering**: a single plane wave occupies one point in FK space; rank-1 SVD captures exactly that.
- **Median filtering**: SVD is a generalization — median is robust to outliers, SVD is optimal for Gaussian noise.

## Related concepts

- [FX-deconvolution](fx_deconvolution.md)
- [Seismic noise](seismic_noise.md)
- [Wiener filter](wiener_filter.md)
- [Frequency filtering](frequency_filtering.md)
- [Curvelet transform](curvelet_transform.md)

## Sources

- [Cadzow Best Practice](../sources/cadzow_best_practice.md)
- [CGG ODT02 De-noise](../sources/cgg_odt02_denoise.md)
