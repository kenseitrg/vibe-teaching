---
title: "Naghizadeh & Sacchi (2009) — f-x adaptive seismic-trace interpolation"
status: draft
type: paper
source_file: wiki/sources/_raw_text/naghizadeh2009.txt
language: en
concepts:
  - seismic_data_regularization
tags: [interpolation, fx, prediction-filter, adaptive, legacy]
---

# Naghizadeh & Sacchi (2009) — Adaptive f-x interpolation

GEOPHYSICS, VOL. 74, NO. 1 (JANUARY-FEBRUARY 2009); P. V9–V16. DOI: 10.1190/1.3008547. University of Alberta.

## Overview

An adaptive extension of Spitz (1991) f–x interpolation that estimates **local prediction filters** efficiently with a recursive least-squares (RLS) algorithm and a forgetting factor, avoiding the cost of re-estimating a filter for every data window.

## Key takeaways

- Reviews modifications to Spitz (1991): Porsani (1999) half-step prediction filter; Gülünay (2003) elegant f–x representation; Naghizadeh & Sacchi (2007) handling of data gaps.
- Signal model: a finite number of waveforms with **constant dip**, validated by windowing. Contrasts with local Radon (Sacchi et al. 2004) and curvelet (Herrmann & Hennenfent 2008) methods, which define local operators *without* needing windowing — an attractive property versus non-local Fourier operators.
- Uses **RLS with a forgetting factor** so the local prediction filter for the current window is updated from neighbouring windows rather than recomputed.
- Low-frequency prediction filters interpolate high frequencies via the Spitz reconstruction step.

## Relation to lecture notes

Supports Term 3 Lecture 06 §3.2 (F–X interpolation, adaptive variant) and the §2/§6 discussion of the windowing assumption and the contrast with local Radon/curvelet operators.

## Related sources

- [Spitz (1991)](spitz1991_fx_interpolation.md) — the base f–x interpolation method.
- [Gülünay (2003)](gulunay2003_ft_interpolation.md) — Fourier-domain interpolation cited as a related f–x scheme.
