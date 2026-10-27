---
title: "Tarantola (1984) — Inversion of seismic reflection data in the acoustic approximation"
status: draft
type: paper
source_file: wiki/sources/_raw_text/tarantola1984.txt
language: en
concepts:
  - full_waveform_inversion
tags: [fwi, history, adjoint-state, acoustic, gradient]
---

# Tarantola (1984) — Inversion of seismic reflection data in the acoustic approximation

GEOPHYSICS, VOL. 49, NO. 8 (AUGUST 1984); P. 1259–1266. Institut de Physique du Globe de Paris.

## Overview

The founding paper of full-waveform inversion for reflection seismic data. Solves the nonlinear inverse problem in the acoustic approximation by iterative gradient descent, and — crucially — shows that the expensive Fréchet derivatives (sensitivity of every data sample to every model cell) need not be computed explicitly: the gradient can be obtained by **correlating the forward-propagated wavefield with a back-propagated residual wavefield** (the adjoint-state idea, avant la lettre).

## Key takeaways

- **Nonlinear least squares on full seismograms:** the misfit is the L2 difference between recorded and synthetic data, where synthetics come from a numerical solution of the acoustic wave equation; iterated with gradient (steepest-descent) updates.
- **The gradient as a wavefield correlation:** for the acoustic case the update direction for the squared-slowness (impedance-related) parameter is obtained by zero-lag correlation in time of the source wavefield (time-differentiated) with the residual wavefield back-propagated from the receivers — one extra "migration-like" modelling per iteration instead of one forward problem *per model cell*.
- **Physical interpretation:** the first iterations perform "migration-like" updates (the reflected-energy part), while transmitted/diving energy contributes the tomographic (long-wavelength) part — Mora's later "migration + tomography" view.
- Tarantola's ambition was **direct estimation of physical earth properties**, not merely a better migration model — the vision behind modern multiparameter FWI.

## Relation to lecture notes

Historical anchor for Term 3 Lecture 07 §1–2 (the idea of full-wavefield inversion; the gradient as back-propagation of residuals — "RTM of the residual").

## Related sources

- [Lailly (1983)] — simultaneous, independent derivation (before-stack migrations as inverse problem).
- [Pratt (1999)](pratt1999_frequency_domain_fwi.md), [Jones (2019)](jones2019_fwi_mechanics_tutorial.md) — later developments.
