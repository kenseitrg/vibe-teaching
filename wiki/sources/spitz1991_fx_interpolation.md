---
title: "Spitz (1991) — Seismic trace interpolation in the F-X domain"
status: draft
type: paper
source_file: wiki/sources/_raw_text/spitz1991.txt
language: en
concepts:
  - seismic_data_regularization
tags: [interpolation, fx, prediction-filter, legacy, aliasing]
---

# Spitz (1991) — F-X trace interpolation

GEOPHYSICS, VOL. 56, NO. 6 (JUNE 1991); P. 785–794.

## Overview

The classic frequency-space (f–x) trace interpolation method. It exploits the **predictability of linear events** in the f–x domain: at each temporal frequency, a set of linear events is a sum of complex exponentials in space and is therefore predictable by a spatial prediction filter. Crucially, it can interpolate **aliased** data.

## Key takeaways

- Linear events are predictable in the f–x domain; a one-step spatial **prediction filter** $P(f)$ is estimated from the recorded traces at each frequency.
- Aliased high frequencies are interpolated using prediction-filter components derived from the **non-aliased low frequencies** — the method "unravels" aliased linear events by transferring the low-frequency predictability to high frequencies.
- Assumes a finite number of linear events with constant dip within the analysis window; the window validates the assumption.
- Handles noisy data formed of aliased events. Became the foundation for many later f–x interpolation schemes (Porsani 1999; Gülünay 2003; Naghizadeh & Sacchi).

## Relation to lecture notes

The anchor for Term 3 Lecture 06 §3.2 (F–X interpolation) and the prototype of the "low-frequency prior for high-frequency aliasing" idea that recurs in AA-ALFT and Radon interpolation.

## Related sources

- [Naghizadeh & Sacchi (2009)](naghizadeh2009_fx_adaptive.md) — adaptive (RLS) extension of Spitz interpolation.
- [Gülünay (2003)](gulunay2003_ft_interpolation.md) — Fourier-transform-domain (f–k) interpolation.
- [Zwartjes & Sacchi (2007)](zwartjes2006_fourier_reconstruction.md) — survey placing Spitz among filter-based methods.
