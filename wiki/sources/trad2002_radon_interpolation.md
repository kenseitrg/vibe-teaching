---
title: "Trad, Ulrych & Sacchi (2002) — Accurate interpolation with high-resolution time-variant Radon transforms"
status: draft
type: paper
source_file: wiki/sources/_raw_text/trad2002.txt
language: en
concepts:
  - radon_interpolation
  - radon_transform
tags: [radon, interpolation, sparse-inversion, hyperbolic-radon, regularization]
---

# Trad, Ulrych & Sacchi (2002) — High-resolution time-variant Radon interpolation

GEOPHYSICS, VOL. 67, NO. 2 (MARCH-APRIL 2002); P. R61–R65. DOI: 10.1190/1.1468626. UBC / University of Alberta.

## Overview

Shows that a **sparse hyperbolic Radon transform** can extend aperture, filter noise, and fill gaps, and presents a practical high-resolution implementation. An elliptical Radon transform does the analogous job for slant-stack sections. The difficulty is the time-variant kernel, which the authors tame with an irregularly sampled velocity model space and sparse matrices.

## Key takeaways

- The Radon transform is an effective interpolator (citing Kabir & Verschuur 1995; Sacchi & Ulrych 1995). A hyperbolic RT on a clean, large-aperture CMP gather gives a sparse model; with gaps/noise, **forcing sparseness** (Thorson & Claerbout 1985) improves the result.
- **Hyperbolic vs parabolic:** parabolic sparse RT on NMO-corrected gathers is computationally efficient and good for aperture extension/gap filling; the true hyperbolic RT better approximates reflections at **large moveout/large offsets** (common in marine data).
- **Time-variant kernel** rules out fast Levinson recursion; use iterative solvers (conjugate gradient, LSQR) that yield an approximate solution each iteration and can be stopped early.
- **Efficient model space:** define the model on an **irregularly sampled velocity space** to minimize unknowns — a central trace carrying a velocity trend from semblance analysis, plus neighbouring perturbation traces; **variable spacing** outperforms constant spacing. Use sparse matrices.
- **Aliasing relaxation:** an irregularly sampled Radon space relaxes the minimum-sampling condition needed to avoid aliasing (Trad & Ulrych 1999).
- Hyperbolic RT → accurate interpolation in CMP gathers; elliptical RT → attenuates sampling artifacts in slant-stack sections.

## Relation to lecture notes

The primary reference for Term 3 Lecture 06 §5.1 (Radon-domain reconstruction): the "replace Fourier with Radon" idea, the hyperbolic-vs-parabolic trade-off, sparse inversion, and the aliasing-relaxation property.

## Related sources

- [Feng et al. (2022)](feng2022_cnn_radon.md) — modern CNN-prior extension of high-resolution Radon interpolation.
- [Zwartjes & Sacchi (2007)](zwartjes2006_fourier_reconstruction.md) — the Fourier-side sparse-reconstruction contrast.
