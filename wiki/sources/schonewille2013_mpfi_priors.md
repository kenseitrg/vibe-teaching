---
title: "Schonewille et al. (2013) — Matching pursuit Fourier interpolation using priors derived from a second data set"
status: draft
type: paper
source_file: wiki/sources/_raw_text/schonewille2013.txt
language: en
concepts:
  - anti_leakage_fourier_transform
tags: [regularization, mpfi, matching-pursuit, priors, interpolation]
---

# Schonewille et al. (2013) — MPFI with priors from a second dataset

SEG Expanded Abstracts. WesternGeco.

## Overview

Matching-pursuit Fourier interpolation (MPFI) is a beyond-aliasing interpolation method for single-component seismic data. Its anti-aliasing capability normally relies on priors derived from the data's own low frequencies. This paper investigates deriving the prior from a **separate, more densely sampled dataset** instead, and shows a significant uplift.

## Key takeaways

- Seismic data are typically irregularly and sparsely sampled in the spatial coordinates, degrading further processing; MPFI reconstructs them via Fourier matching pursuit.
- Standard MPFI dealiases high frequencies using priors from the **lower frequencies of the same data**.
- Using a prior from a **second dataset** (more densely sampled) improves anti-aliasing. Practical cases: **dense-over/sparse-under** acquisitions and **time-lapse** data.
- Tests decimate an existing dataset, derive the prior from the non-decimated version, and use it to interpolate the decimated data — giving a clear uplift over self-derived priors.

## Relation to lecture notes

The anchor for Term 3 Lecture 06 §5.2 (using separate datasets for priors) — a modern extension of the ALFT/MPFI family.

## Related sources

- [Schonewille et al. (2009)](schonewille2009_aa_alft.md) — anti-alias ALFT (the self-derived-prior predecessor).
- [Xu et al. (2010)](xu2010_antileakage_fourier_transform.md) — base ALFT.
- [Tang et al. (2017)](tang2017_5d_mpfi_srme.md) — 5D MPFI application.
