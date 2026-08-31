---
title: "Zwartjes & Sacchi (2007) — Fourier reconstruction of nonuniformly sampled, aliased seismic data"
status: draft
type: paper
source_file: wiki/sources/_raw_text/zwartjes2006.txt
language: en
concepts:
  - seismic_data_regularization
  - spatial_spectral_leakage
  - nonuniform_fourier_transform
tags: [regularization, fourier, least-squares, anti-alias, sparse-inversion]
---

# Zwartjes & Sacchi (2007) — Fourier reconstruction of aliased data

GEOPHYSICS, VOL. 72, NO. 1 (JANUARY-FEBRUARY 2007); P. V21–V32. DOI: 10.1190/1.2399442.

## Overview

Presents a least-squares / minimum-weighted-norm Fourier reconstruction that handles nonuniform sampling and aliasing. Surveys the filter-based interpolation landscape and positions sparse Fourier inversion as a unifying framework.

## Key takeaways

- Surveys interpolation families: dip/semblance-weighted slant-stack scanning (Bardan 1987; Kao 1997); **f–x interpolation** (Spitz 1991) using predictability of stationary, non-dispersive planar events, with low-frequency filters predicting aliased high frequencies; f–x projection filters (Soubaras 1997); **t–x prediction-error filtering** (Claerbout & Nichols 1991; Crawley & Clapp 1999 for nonstationary data).
- Frames reconstruction as an inverse problem: estimate Fourier coefficients from nonuniform samples by least squares, stabilized with a minimum-weighted-norm (sparsity) constraint to handle aliasing and gaps.
- Establishes the contrast between Fourier-domain sparse inversion and Radon/curvelet methods (the latter are local and need no explicit windowing).

## Relation to lecture notes

Background for Term 3 Lecture 06 §3 (legacy T–X/F–X/F–K methods) and §4.2 (spectral leakage and least-squares Fourier estimation as the precursor to ALFT). Useful for the method-selection discussion (§6).

## Related sources

- [Xu et al. (2010)](xu2010_antileakage_fourier_transform.md) — ALFT as an iterative alternative to least-squares Fourier inversion.
- [Schonewille et al. (2009)](schonewille2009_aa_alft.md) — cites Zwartjes & Sacchi among high-resolution alternatives.
- [Trad et al. (2002)](trad2002_radon_interpolation.md) — the Radon-domain sparse-reconstruction counterpart.
