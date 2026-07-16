---
title: Sysoev — Statics and Kinematic Corrections
status: draft
source_type: course_notes
authors: A. P. Sysoev
year: 2011
url: null
lectures:
  - term03_lec02
related_concepts:
  - static_corrections
  - effective_velocity
  - velocity_analysis
  - floating_datum
  - residual_statics
tags: [statics, russian, velocity, near-surface, kinematic-corrections]
---

# Sysoev — Statics and Kinematic Corrections

Sysoev, A. P., 2011, *Прикладные задачи компенсации неоднородности верхней части разреза при обработке и интерпретации сейсмических данных* (Applied problems of compensating near-surface heterogeneity in seismic processing and interpretation), Novosibirsk: INGG SB RAS, 90 p.

## Main message

The monograph analyzes the limits of the static-correction model and proposes more rigorous kinematic corrections for variable topography and submerged high-velocity anomalies.

## Chapter 4 — Compensation of variable topography

- Static corrections for elevation are widely used but are physically justified only for a thin low-velocity weathering layer where rays are nearly vertical.
- For variable topography, shifting traces by a constant time distorts the effective (stacking) velocity: the estimated velocity becomes correlated with the elevation.
- Depth estimates from the biased effective velocity can be off by tens of metres even for modest elevation changes.
- The paper derives a reduction formula to correct effective velocities back to the observation surface, and a kinematic redatuming method that computes trace-dependent time corrections using a two-layer model and average / RMS velocities. Model tests show that kinematic compensation is far more accurate than static shifts for large topographic variation.

## Chapter 5 — Submerged high-velocity anomalies (permafrost)

- A high-velocity layer such as permafrost is a **submerged** heterogeneity; it is not correctly described by source/receiver statics alone.
- Residual statics algorithms will absorb part of the anomaly into source/receiver shifts and part into CMP structural/velocity terms, producing biased estimates of both statics and velocity.
- The anomaly is diagnosed by correlated variations in zero-offset time and effective velocity of reflections below the anomaly.
- A replacement-statics approach can approximately compensate the anomaly by replacing the variable-thickness high-velocity layer with a constant-velocity layer, but this is only valid for small offsets and weakly curved boundaries.
- The chapter stresses the **low-frequency ambiguity** between statics and kinematic parameters: constant, linear, and quadratic spatial components of source/receiver statics trade off with CMP time and curvature terms within the aperture of the acquisition.

## Notes on the source

The raw text is OCR output from a 93-page Russian monograph and contains repeated and truncated passages; the summary above is based on the readable portions of Chapters 4 and 5.

## Relation to lecture notes

Supports Term 3 Lecture 2: effective velocity, floating/flat datum, statics–velocity coupling, and the fundamental ambiguity between long-wavelength statics and kinematic parameters.

## Related concepts

- [Static corrections](../concepts/static_corrections.md)
- [Effective velocity](../concepts/effective_velocity.md)
- [Velocity analysis](../concepts/velocity_analysis.md)
- [Floating datum](../concepts/floating_datum.md)
- [Residual statics](../concepts/residual_statics.md)
