---
title: "Gülünay (2003) — Seismic trace interpolation in the Fourier transform domain"
status: draft
type: paper
source_file: wiki/sources/_raw_text/10.1190@1.1543221.txt
language: en
concepts:
  - seismic_data_regularization
tags: [interpolation, fk, fourier, legacy, aliasing]
---

# Gülünay (2003) — Fourier-transform-domain trace interpolation

GEOPHYSICS, VOL. 68, NO. 1 (JANUARY-FEBRUARY 2003); P. 355–369. DOI: 10.1190/1.1543221.

## Overview

Trace interpolation applied directly in the **Fourier transform domain** (f–k or f–kx–ky), designed for spatially aliased data. It leverages FFTs and their cyclic properties, and designs the interpolation operator from the non-aliased low frequencies.

## Key takeaways

- Aliasing is inherent in common-offset and CMP domains even when shot/receiver domains are well sampled; large shot intervals compound it. Interpolation is the standard remedy.
- The method works in the f–k (or f–kx–ky) domain using fast Fourier transforms and their **cyclic properties** to interpolate spatially aliased data.
- The interpolation **operator is designed from the lower (non-aliased) frequencies** and is the same operator that fills periodically zeroed traces in the original data — again the low→high frequency prior idea.
- Has strong similarities to f–x prediction filtering (Spitz 1991) but with an elegant f–k representation (noted by Naghizadeh & Sacchi 2009).

## Relation to lecture notes

The anchor for Term 3 Lecture 06 §3.3 (F–K interpolation) — the Fourier-domain counterpart of Spitz f–x interpolation, sharing the low-frequency-prior strategy for aliasing.

## Related sources

- [Spitz (1991)](spitz1991_fx_interpolation.md) — the related f–x prediction-filter method.
- [Gülünay & Chambers (1997)](#) — generalized f–k domain trace interpolation (in `papers/regularization/`).
- [Zwartjes & Sacchi (2007)](zwartjes2006_fourier_reconstruction.md) — Fourier reconstruction context.
