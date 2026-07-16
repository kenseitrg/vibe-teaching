---
title: Law and Trad — Comparison of Refraction Inversion Methods
status: draft
source_type: paper
authors: Bernard Law, Daniel Trad
year: 2017
url: https://doi.org/10.1190/1.9781560803690.ch22
lectures:
  - term03_lec02
related_concepts:
  - static_corrections
  - velocity_analysis
  - first_break_picking
  - diving_wave_tomography
tags: [refraction, tomography, statics, first-breaks, inversion]
---

# Law and Trad — Comparison of Refraction Inversion Methods

CREWES Research Report — Volume 29 (2017), "Comparison of refraction inversion methods" by Bernard Law and Daniel Trad.

## Main message

Near-surface weathering statics are traditionally derived from first-arrival refraction times. This report reviews and compares the principal inversion families and shows how they can be harmonized with surface-consistent residual statics from deeper reflection data.

## Methods compared

- **Delay-time / generalized reciprocal methods** (Gardner, Barry, Hagedoorn, Palmer): layer-based, fast, but assume velocity increasing with depth and slow lateral variation.
- **Generalized Linear Inversion (GLI)** (Hampson & Russell): solves for layer thickness and velocity perturbations via least-squares; stable but still limited to layered models.
- **Turning-ray refraction tomography** (White, Zhu et al.): discretizes the near surface into cells and traces diving rays or solves the Eikonal equation; can handle gradients and complex geology, but suffers from low ray-density instability at edges and depends on starting model / smoothing.
- **Full-waveform inversion (FWI)**: uses the full wavefield, not just traveltimes; can resolve shorter wavelengths but requires low-frequency data, wide aperture, and careful preprocessing.

## Key takeaways

- Ray-based methods (GLI and tomography) require the velocity model to vary slowly; they are limited by the high-frequency asymptotic approximation.
- Turning-ray tomography images more complex near-surface structure than layered methods, but model quality depends on ray coverage, grid size, and smoothing.
- Both GLI and tomography can be improved by adding **model weight** and **data weight** terms derived from smoothed surface-consistent reflection residual statics. This couples the near-surface velocity model to the reflection stack response.
- The nonlinear optimization workflow alternates between refraction inversion, residual statics computation, and model updating until the model is consistent with both first-arrival and reflection data.
- A Hussar 2D field example shows that the modified cost function produces long-wavelength statics that agree better with reflection data than conventional refraction statics alone.

## Relation to lecture notes

Supports Term 3 Lecture 2: first-break methods, diving-wave tomography, long-period statics, and the link between refraction-derived near-surface models and stacking velocities.

## Related concepts

- [Static corrections](../concepts/static_corrections.md)
- [Velocity analysis](../concepts/velocity_analysis.md)
- [First-break picking](../concepts/first_break_picking.md)
- [Diving-wave tomography](../concepts/diving_wave_tomography.md)
