---
title: "Tang et al. (2017) — 5D MPFI and its application in SRME for large-offset coil data"
status: draft
type: paper
source_file: wiki/sources/_raw_text/tang2017.txt
language: en
concepts:
  - seismic_data_regularization
  - anti_leakage_fourier_transform
tags: [regularization, 5d, mpfi, srme, acquisition, dual-coil]
---

# Tang et al. (2017) — 5D MPFI for SRME on dual-coil data

SEG Technical Program Expanded Abstracts 2017. DOI: 10.1190/segam2017-17680141.1. WesternGeco.

## Overview

Applies **5D matching-pursuit Fourier interpolation (MPFI)** to multivessel circular ("dual-coil") wide-azimuth, long-offset acquisition, specifically to feed surface-related multiple elimination (SRME). Dual-coil data give richer azimuth and longer offsets, but large-offset coverage is less uniform than the dominant azimuths, so regularization is essential.

## Key takeaways

- Dual-coil (multivessel circular) acquisition improves imaging of complex subsalt structures via full-azimuth, long-offset coverage.
- Large-offset coverage is generally **less uniform** than the dominant azimuths in traditional wide-/narrow-azimuth data — an irregularity that degrades SRME and imaging.
- 5D MPFI regularizes the data across all spatial axes, improving the input to SRME for large-offset coil data.

## Relation to lecture notes

A concrete application for Term 3 Lecture 06 §5.4 (5D MPFI extensions) and a real-world tie back to §1 (regularization is needed so that SRME and migration work). Demonstrates the offset/azimuth irregularity that 5D regularization addresses.

## Related sources

- [Schonewille et al. (2013)](schonewille2013_mpfi_priors.md) — MPFI methodology with priors.
- [Trad (2009)](trad2009_5d_interpolation.md) — 5D interpolation rationale.
- [Xu et al. (2010)](xu2010_antileakage_fourier_transform.md) — high-dimensional ALFT basis of MPFI.
