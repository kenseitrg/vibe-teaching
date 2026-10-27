---
title: "Term 3 Lecture 07 — Introduction to Full-Waveform Inversion"
status: draft
lecture: term03_lec07
tags: [fwi, velocity-model-building, cycle-skipping, frequency-continuation, land, fwi-imaging]
sources:
  - jones2019_fwi_mechanics_tutorial
  - metivier2026_fwi_nonconvexity_review
  - pratt1999_frequency_domain_fwi
  - tarantola1984_inversion_acoustic
  - bohlen_fwi_lecture_series
  - zhang2015_land_data_fwi
  - wang2020_land_fwi_challenges
  - sheng2022_land_fwi_imaging
  - baldock2023_fwi_imaging
  - keating2016_anacoustic_fwi
  - cova2017_land_multicomponent_conditioning
---

# Term 3 Lecture 07 — Introduction to Full-Waveform Inversion

## Summary

A conceptual introduction to full-waveform inversion: why ray-based model building reaches a resolution wall, how FWI formulates model building as iterative waveform matching, why the problem is non-linear (cycle skipping) and what work-arounds exist, what FWI delivers in practice (high-resolution velocity models, FWI imaging, multiparameter potential), and the modern challenge list (cost vs frequency, starting models, land data, physics gaps, source and data quality). Math is kept light; the lecture relies on figures reused from the literature (plus one generated schematic).

## Key Concepts

1. **Ray resolution limit** — rays are a high-frequency approximation; traveltime tomography resolves only ≥ Fresnel-zone scale √(λL)
2. **FWI idea** — match full waveforms (phase + amplitude) by iteratively updating a gridded model through wave-equation modelling
3. **The FWI loop** — forward modelling → residual → adjoint back-propagation → gradient → line search → update
4. **Gradient = "RTM of the residual"** — imaging condition between source wavefield and back-propagated residual
5. **Wavenumber illumination** — |k| = (2f/v)·cos(θ/2): reflections update short wavelengths, diving waves long ones; offsets control θ
6. **Cycle skipping** — half-period criterion; oscillatory L2 misfit → local minima
7. **Work-arounds** — frequency continuation, time windowing, alternative misfits (traveltime, AWI, OT), extended methods (WRI), better starting models — all relaxations
8. **Advantages** — wavelength-scale resolution, FWI imaging (velocity derivative), multiparameter (elastic, anisotropy, Q) potential
9. **Challenges** — cost ∝ f⁴, starting-model quality, land specifics (topography, near surface, noise), elastic/viscoelastic physics, source signature, data quality

## Lecture Outline (~90 min; expanded version ≈ 100 min — trim candidates marked ⚠)

### 0. Why this lecture matters (5 min)

### 1. From rays to full wavefields (12–14 min)

- Recap of Terms 1–3 model building; when rays break down (anomaly ≈ wavelength → scattering)
- Resolution ladder: Fresnel zone vs wavelength; Pratt (1999) scale model
- FWI idea and history; FWI across 9 orders of magnitude

### 2. Problem formulation and taming non-linearity (32–38 min)

- The loop; objective function on 10⁷–10⁸ cells; local optimization only
- Gradient via back-propagation = RTM of the residual; gradient anatomy (banana, arcs, rabbit ears)
- Wavenumber illumination: reflections → high k, diving waves → low k; long offsets for deep updates
- Local descent on the misfit surface (toy 2-parameter picture)
- Cycle skipping: mechanism, half-period criterion, frequency table
- **Checkpoint 1** (2 min): 60 ms starting error — safe at 4 Hz? at 10 Hz?
- Work-arounds: (a) frequency continuation (field data-fit + Pratt multiscale), (b) windowing, (c) misfit modifications (traveltime, AWI, OT), (d) extended formulations (WRI), (e) starting models (land DFPD example)
- Unifying principle: everything is a relaxation
- ⚠ Trim candidates: gradient-impulse-response slide (merge into anatomy), scale-model-verdict (merge into resolution-floor)

### 3. What FWI buys you (18–20 min)

- BP 2004 resolution; Permian Basin (model + image + gather QC)
- FWI imaging: salt and West of Shetlands examples
- Multiparameter potential; parameter cross-talk; acoustic-vs-elastic test

### 4. Modern challenges (18–22 min)

- Cost ∝ f⁴ per iteration; grid/CFL reasoning; mitigations
- **Checkpoint 2** (2 min): 5→10 Hz — cost change? what else tightens?
- Starting models ↔ low frequencies (2 Hz vs 8 Hz band start)
- Land: the hard case — topography, near surface, noise conditioning (dual-domain), elasticity, coupling, offsets
- Land case studies: Inner Mongolia (DFPD FWI → WEMVA → RTM), onshore Mexico (DMFWI, Kirchhoff + RTM)
- Physics gaps: elasticity, anisotropy, absorption (Q + dispersion, wrong-Q artifacts)
- Source signature and amplitude fidelity; data quality and preprocessing (multiples can stay)

### 5. Summary and discussion (8–10 min)

## Figures

21 in notes / 26 in deck. Reused from papers/course materials (see notes captions for credits); one generated schematic:

| Figure | Source |
|--------|--------|
| ray_vs_waveform_resolution | Pratt (1999), Fig. 3 |
| fwi_applications_scales | Bohlen FWI course, Lec 4 slide 4 |
| fwi_workflow | Bohlen FWI course, Lec 2 slide 4 |
| gradient_formation | Jones (2019), Fig. 3 |
| gradient_impulse_response | Jones (2019), Fig. 9 |
| gradient_components | Jones (2019), Fig. 7 |
| wavenumber_illumination | **generated** (plot_wavenumber_illumination.py; after Sirgue & Pratt 2004) |
| cost_function_descent | Jones (2019), Fig. 6 |
| cycle_skipping | Jones (2019), Fig. 5 |
| data_fit_evolution | Bohlen Lec 4 slide 28 (after Habelitz 2017) |
| fwi_multiscale_resolution | Pratt (1999), Fig. 7 |
| land_cycle_skipping | Zhang & Dai (2015), Fig. 1 |
| bp2004_fwi_resolution | Zhang & Dai (2015), Fig. 7 |
| land_fwi_permian | Wang et al. (2020), Fig. 3 |
| land_fwi_gathers | Wang et al. (2020), Fig. 5 |
| fwi_imaging_vs_rtm | Baldock et al. (2023), Fig. 3 |
| fwi_imaging_clair | Baldock et al. (2023), Fig. 5 |
| acoustic_vs_elastic_fwi | Bohlen Lec 4 slide 10 (after Thiel 2018) |
| land_noise_conditioning | Wang et al. (2020), Fig. 2 |
| land_fwi_inner_mongolia | Zhang & Dai (2015), Figs. 8–9 (composite) |
| land_fwi_pemex_kirchhoff / _rtm | Sheng et al. (2022), Figs. 2–3 |
| total_gradient (deck only) | Jones (2019), Fig. 10 |

## Prerequisites

- Term 1: velocity analysis, statics; Term 3 Lec 02: tomography and velocity modeling; Term 1 Lec 05: spectra/frequency; Term 2 Lec 01: absorption and Q.
