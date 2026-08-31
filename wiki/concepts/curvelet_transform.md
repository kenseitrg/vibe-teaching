---
title: Curvelet transform
status: draft
sources:
  - hennenfent2006_curvelet_intro
  - hennenfent2011_interpretative_noise
  - herrmann2007_curvelet_multiple_separation
  - kustowski2013_curvelet_model_guided
  - demanet_ying_mirror_extended
tags: [curvelet, multiscale, sparse-representation, noise-attenuation, transform-domain]
---

# Curvelet transform

The curvelet transform is a multiscale, multidirectional expansion that represents images (or seismic gathers) as a sum of basis functions called **curvelets**. Unlike wavelets, which are point-like and only capture scale-position, curvelets are elongated — they capture orientation as well.

## Tiling the FK plane

Curvelets tile the frequency-wavenumber ($f$-$k_x$-$k_y$) plane in a natural way:

- **Radial division** (scales): concentric rings divide the plane by frequency band.
- **Angular division** (directions): each ring is split into wedges, with finer angular sampling at higher frequencies.

This matches the "parabolic scaling law": at scale $j$, a curvelet has length $\approx 2^{-j/2}$ and width $\approx 2^{-j}$, making it long and thin at fine scales — ideal for representing linear and curved seismic events.

## Why curvelets for seismic data

- **Sparsity**: a clean seismic reflection panel has few large curvelet coefficients and many near-zero ones. Random noise spreads its energy across all coefficients.
- **Directionality**: curvelets align with dipping events. A single curvelet coefficient "explains" an entire local linear segment.
- **Curved events**: unlike FK (which assumes perfect linearity), curvelets accommodate curvature through their directional tiling.

## Noise attenuation workflow

1. Transform the data to the curvelet domain.
2. Estimate the noise level per scale-direction panel.
3. Threshold or suppress small coefficients (those likely to be noise).
4. Inverse-transform to recover the denoised data.

## Adaptive subtraction in curvelet domain

For separating signal from coherent noise (e.g., multiples from primaries):

- Transform signal and noise panels separately.
- Design adaptive filters per curvelet scale-direction panel.
- Because each panel contains relatively simple kinematics, the adaptive filter can be shorter and more stable.

## Advantages

- Handles curved events (not just linear dips).
- Preserves amplitude and phase better than boxcar FK filters.
- Works with irregular sampling (curvelets are frame elements, not tied to grid points).

## Limitations

- Computationally expensive compared to FK or FX methods.
- Requires careful parameter selection (number of scales, angular divisions, threshold).
- If the signal and noise overlap in the curvelet domain, separation becomes difficult.

## Related concepts

- [Seismic noise](seismic_noise.md)
- [Frequency filtering](frequency_filtering.md)
- [Radon transform](radon_transform.md)
- [Adaptive subtraction](adaptive_subtraction.md)
- [FX-deconvolution](fx_deconvolution.md)
- [SVD / Cadzow filtering](cadzow_svd_filtering.md)

## Sources

- [Hennenfent & Herrmann (2006) — Curvelet introduction.](../sources/hennenfent2006_curvelet_intro.md)
- [Hennenfent & Herrmann (2011) — Interpretative noise attenuation.](../sources/hennenfent2011_interpretative_noise.md)
- [Herrmann et al. (2007) — Curvelet multiple separation.](../sources/herrmann2007_curvelet_multiple_separation.md)
- [Kustowski et al. (2013) — Curvelet model-guided denoising.](../sources/kustowski2013_curvelet_model_guided.md)
- [Demanet & Ying (2007) — Mirror-extended curvelets.](../sources/demanet_ying_mirror_extended.md)
