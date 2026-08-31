---
title: Seismic data regularization
status: draft
sources:
  - trad2009_5d_interpolation
  - abma2005_interpolation_comparison
  - xu2010_antileakage_fourier_transform
  - tang2017_5d_mpfi_srme
tags: [regularization, interpolation, migration, acquisition, 5d, ovt]
---

# Seismic data regularization

Regularization maps seismic traces recorded on an **irregular, sparse acquisition grid** onto a **regular, densely sampled grid**. It is a standard pre-processing step before algorithms that assume regular sampling — most importantly migration and surface-related multiple elimination (SRME).

## Why it is needed

Many modern algorithms assume the input is sampled on a regular grid with no aliasing in the spatial directions:

- **Migration.** Kirchhoff and wave-equation migration sum energy along operator surfaces. If the input traces are irregular or coarse, the migration impulse response develops artifacts — the familiar "tails" and smearing — because the summation is incomplete and aliased. Regularizing the input suppresses these artifacts.
- **SRME and other multi-channel processes.** 3D SRME, AVO/AVAz analysis, and stacking all degrade when traces are missing or irregularly placed.

As Trad (2009) puts it: the only perfect solution is to acquire well-sampled data; everything else treats the symptoms. But we usually cannot return to the field, so we regularize.

## Regularization vs interpolation

The two terms are often used interchangeably, but the emphasis differs:

- **Regularization** — the primary goal: produce a *regularly sampled* dataset (a consistent grid of bins, offsets, azimuths) so that downstream algorithms behave correctly. The output locations are fixed by the chosen grid, not by where data are missing.
- **Interpolation** — filling in *missing* traces at specific locations. Interpolation is sometimes a beneficial side effect, and is occasionally the explicit goal (e.g. densifying data so that a noise-attenuation step can handle aliased noise).

Most modern "interpolation" algorithms are really regularization engines.

## What "regular" means depends on the problem

The target grid is defined by the **migration domain**:

- **Offset migration** → data should be regular in midpoint and offset.
- **OVT / COV migration** → data should be regular in offset-vector tiles (midpoint × offset-x × offset-y), preserving azimuth. See [OVT / COV panels](ovt_cov_panels.md).

## Dimensionality of the transform

The number of spatial axes used by the regularization transform is the defining feature of modern methods:

| Dim. | Axes used | What it preserves | Limitation |
|------|-----------|-------------------|------------|
| 3D | inline, crossline, time | structural dip | cannot fill missing offsets |
| 4D | + offset | offset gaps filled | all azimuths at a given offset are mixed/averaged |
| 5D | + azimuth (or offset-x, offset-y) | azimuth **and** AVO/AVAz | best gap filling; most expensive |

> **Naming pitfall.** "4D/5D" here counts the axes of the data cube (spatial + time). It has nothing to do with *4D time-lapse* seismic.

5D regularization uses every spatial axis, so it has the most information for both preserving azimuth/AVO and filling gaps. It is the state of the art (Trad 2009; Xu et al. 2010; Tang et al. 2017).

## Method families

1. **Continuation / Kirchhoff operators** — integrate along traveltimes from a velocity model. Velocity-dependent; weak at near offsets; can create artifacts in complex structure.
2. **Prediction filters (legacy)** — T–X, [F–X (Spitz 1991)](../sources/spitz1991_fx_interpolation.md), [F–K (Gülünay 2003)](../sources/gulunay2003_ft_interpolation.md). Assume locally linear, stationary events.
3. **Sparse Fourier reconstruction (modern)** — estimate a sparse spatial Fourier spectrum and invert it onto the target grid. The core idea is [matching pursuit](matching_pursuit.md) with a Fourier dictionary, made robust by the [anti-leakage Fourier transform](anti_leakage_fourier_transform.md).
4. **Sparse Radon reconstruction** — the same sparsity idea but in the Radon domain. See [Radon interpolation](radon_interpolation.md).

Every method rests on an assumption that the data are *sparse or simple in some transform domain*. The art is choosing the domain that best matches the data.

## Related concepts

- [Spatial spectral leakage](spatial_spectral_leakage.md)
- [Anti-leakage Fourier transform](anti_leakage_fourier_transform.md)
- [Matching pursuit](matching_pursuit.md)
- [Non-uniform Fourier transform](nonuniform_fourier_transform.md)
- [Radon interpolation](radon_interpolation.md)
- [OVT / COV panels](ovt_cov_panels.md)
- [Aliasing](aliasing.md)

## Sources

- Trad (2009) — five-dimensional interpolation; motivation from migration, AVO/AVAz, and acquisition constraints.
- Abma & Kabir (2005) — comparison of interpolation methods and the assumptions each makes.
- Xu, Zhang & Lambaré (2010) — anti-leakage Fourier transform generalized to higher dimensions.
- Tang et al. (2017) — 5D matching-pursuit Fourier interpolation applied to SRME for dual-coil data.
