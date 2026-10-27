---
title: "Jones (2019) — Tutorial: the mechanics of waveform inversion"
status: draft
type: paper
source_file: wiki/sources/_raw_text/jones2019.txt
language: en
concepts:
  - full_waveform_inversion
  - fwi_cycle_skipping
tags: [fwi, tutorial, gradient, rtm, misfit, cycle-skipping]
---

# Jones (2019) — Tutorial: the mechanics of waveform inversion

FIRST BREAK, VOL. 37, MAY 2019, P. 31–43. DOI: 10.3997/1365-2397.2019017. ION Geophysical.

## Overview

An accessible tutorial on how full-waveform inversion actually works mechanically, aimed at practicing geophysicists. The central pedagogical idea: FWI reuses the **RTM engine**. Migration asks "where did this reflection come from?"; FWI asks "where did this *velocity error* come from?" — both are answered by combining a forward-propagated source wavefield with a back-propagated wavefield at receiver positions (an imaging condition), then iterating with gradient descent.

## Key takeaways

- **Why rays fail:** ray-based tomography uses only traveltimes (high-frequency approximation) and resolves features only larger than about 5× the dominant wavelength (Fresnel-zone resolving length). Waveform inversion uses phase + amplitude of the full signal and can resolve **sub-wavelength** features.
- **Objective function:** least-squares misfit $C(m) = \sum\sum\sum [d_0 - d(m)]^2$ summed over shots, traces, samples. The model update needs the **gradient** $\partial C/\partial m$ and ideally the **Hessian** $[\partial^2 C/\partial m^2]^{-1}$; the Hessian is impractical, so iterative approximate inverses (steepest descent, non-linear conjugate gradient, line search for step length) are used.
- **Gradient as imaging condition:** back-propagate the data residual (the "adjoint source") and correlate/convolve it with the second time derivative of the forward source wavefield scaled by $-2v^{-3}$. Requires a good **source wavelet estimate** — non-trivial on land.
- **Gradient components:** the total gradient decomposes into (a) the direct/diving-wave "banana" sensitivity kernel, (b) the migration-like elliptical reflection arc, and (c) RTM cross-talk "rabbit ears" that reach deeper than the diving wave. In practice, refraction (diving-wave) FWI updates the shallow model to ~⅓ of max offset; reflection FWI (rabbit ears, extended conditions) updates deeper.
- **Cycle skipping:** if the starting model mis-predicts arrival times by more than ~half a period, the L2 misfit has local minima and FWI converges to a wrong model. Mitigations: better starting model (ray tomography), low frequencies (<2 Hz for subsalt), or alternative residuals — adaptive waveform inversion (matching filter → spike), time/phase-shift residuals (cross-correlation, "adjustive FWI"), phase-only, optimal transport.
- **Frequency and cost:** cost of RTM-style modelling scales with $f_{\max}^4$, so starting low is also **cost-effective**, not only cycle-skip-avoiding.
- **Workflow:** (1) ghost-free wavelet estimate; (2) cycle-skip-avoiding update (ray tomography or traveltime/adaptive residual); (3) shallow refraction FWI with increasing bandwidth; (4) deeper reflection FWI (may need demultipled data). Two-way modelling reproduces ghosts and multiples, so they can stay in the data for full-physics FWI.
- FWI models are also used as **constraints for impedance inversion** and FWI velocity derivatives as **reflectivity images** (FWI imaging).

## Relation to lecture notes

Primary source for Term 3 Lecture 07 (Introduction to FWI): problem formulation, gradient, optimization, cycle skipping (Figures 3, 5, 6, 7, 9, 10 of the paper are reused in the lecture).

## Related sources

- [Tarantola (1984)](tarantola1984_inversion_acoustic.md) — original formulation of the gradient method.
- [Pratt (1999)](pratt1999_frequency_domain_fwi.md) — frequency-domain view, resolution, starting-model requirement.
- [Métivier & Brossier review](metivier2026_fwi_nonconvexity_review.md) — systematic taxonomy of non-linearity mitigations.
