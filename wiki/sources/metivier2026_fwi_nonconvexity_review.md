---
title: "Métivier & Brossier (2026) — A comprehensive review of strategies to mitigate non-convexity in full waveform inversion"
status: draft
type: paper
source_file: wiki/sources/_raw_text/ggag376.txt
language: en
concepts:
  - full_waveform_inversion
  - fwi_cycle_skipping
tags: [fwi, nonlinearity, cycle-skipping, review, optimal-transport, wri, frequency-continuation]
---

# Métivier & Brossier (2026) — Review of strategies to mitigate non-convexity in FWI

GEOPHYS. J. INT. (2026) 247, 1–38. DOI: 10.1093/gji/ggag376. Open access (CC-BY 4.0). ISTerre, Univ. Grenoble Alpes.

## Overview

An invited review of ~40 years of research on the central obstacle of FWI: the **non-convexity** of the misfit function caused by the nonlinear model→data mapping. All mitigation strategies are cast in one framework: solve a **cascade of relaxed FWI problems** $\mathcal{F}[r_i]$, where a relaxation parameter $r_i$ adds temporary degrees of freedom or simplifies the problem, then progressively relax toward the original full-bandwidth, full-physics problem.

## Key takeaways

- **Why naive FWI failed historically:** nonlinearity (cycle skipping from oscillatory signals), lack of sensitivity to large-scale velocity structure from short-offset reflections, huge scale (gridding at the smallest wavelength), dependence on local optimization → dependence on the initial model. Famous 1991 Symes & Carazzone quote: least-squares FWI "as a velocity estimation procedure … must be regarded as a failure." Gauthier et al. (1986): gradient methods cannot recover low spatial frequencies from short-offset reflections.
- **Method families** (the review's classification):
  1. **Multiscale / frequency continuation** (Bunks et al. 1995): band-pass cascade from low to high frequencies — low frequencies oscillate less, so the L2 misfit has fewer local minima. Time-offset windowing (early arrivals first, then later phases; Shipp & Singh 2002) is the same relaxation idea.
  2. **Misfit-function modifications** (Luo & Schuster 1991 onward): cross-correlation traveltime, deconvolution, instantaneous phase, dynamic time warping, optimal transport (OT), Lp norms; two-pass practice — one robust misfit for the background model, then L2.
  3. **Model extension**: extended reflectivity/space-shift (MVA, FWIME, RWI, JFWI), scale separation between smooth background (macro model) and reflectivity.
  4. **Wavefield/source extension**: WRI (van Leeuwen & Herrmann 2013), extended source (Wang et al.) — fit data with an inaccurate model by relaxing the source, with convex quadratic penalties.
  5. **Receiver extension**: relaxed receiver positions (very recent).
- **Which are used on field data:** multiscale + windowing underpin essentially all field applications; misfit modifications (OT, AWI-like) and WRI/extended source are transitioning to practice; most other extensions remain at the research stage.
- FWI now spans global seismology to medical imaging; at exploration scale it tends toward a "rational replacement for the entire seismic data processing stream" (echoing Symes' phrase), including FWI imaging replacing conventional imaging and elastic FWI supplementing AVO.

## Relation to lecture notes

Source for Term 3 Lecture 07 §2 (problem formulation, non-linearity, and the work-arounds overview). The summary diagram (Fig. 2) maps the whole research landscape.

## Related sources

- [Jones (2019)](jones2019_fwi_mechanics_tutorial.md) — mechanics-level tutorial.
- [Virieux & Operto (2009)] and Virieux et al. (2017) tutorials referenced within — classic overviews.
