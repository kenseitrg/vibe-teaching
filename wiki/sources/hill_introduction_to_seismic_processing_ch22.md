---
title: Hill — Introduction to Seismic Processing, Chapter 22: Statics
status: draft
source_type: textbook
authors: Steve J. Hill
year: 2020
url: https://doi.org/10.1190/1.9781560803690
lectures:
  - term03_lec02
related_concepts:
  - static_corrections
  - residual_statics
  - velocity_analysis
  - floating_datum
  - diving_wave_tomography
tags: [statics, textbook, near-surface, velocity, residual-statics]
---

# Hill — Introduction to Seismic Processing, Chapter 22: Statics

Chapter 22 of *Introduction to Seismic Processing* (SEG) by Steve J. Hill.

## Main message

Statics are time shifts applied to individual traces to simulate acquisition on a flat surface with a uniform near-surface velocity. Uncompensated statics degrade structure, stack quality, and stacking-velocity estimates.

## Chapter topics

- **Elevation statics**: lateral elevation changes create time shifts that can map into false synclines or faults if not removed before migration.
- **Near-surface statics**: lateral velocity variations in the weathering layer, permafrost, karst, etc., cause trace-independent time delays. The surface-consistency assumption holds because near-surface rays are nearly vertical when the weathering layer is slow.
- **Manifestations in CMP gathers**: statics appear as time-independent shifts after NMO; they reduce stack power, lower signal-to-noise ratio, and smear stacked reflections in time.
- **Statics and stacking velocities**: a near-surface low-velocity channel can increase the estimated NMO velocity, while a high-velocity anomaly can decrease it. Statics must be re-estimated iteratively with updated velocities.
- **Field statics**: two-layer model (weathering velocity, elevation velocity, weathering thickness, datum elevation); refraction statics use first-arrival slopes to estimate refractor velocities and depths.
- **Tomostatics**: turning-ray tomography inverts first-arrival times for a continuous near-surface velocity model. Solutions are non-unique and depend on the algorithm and smoothing.
- **Residual statics**: surface-consistent time shifts estimated from reflection correlation, typically applied after field statics and NMO correction.
- **Migration / migration-velocity-analysis statics**: a sufficiently detailed near-surface velocity model lets depth migration handle statics; in practice, acquisition sampling is too coarse, so statics are removed before migration. Migration velocity analysis on a shallow reference horizon can also supply near-surface interval velocities for static shifts.

## Relation to lecture notes

Core supporting textbook for Term 3 Lecture 2: all statics–velocity–imaging links.

## Related concepts

- [Static corrections](../concepts/static_corrections.md)
- [Residual statics](../concepts/residual_statics.md)
- [Velocity analysis](../concepts/velocity_analysis.md)
- [Floating datum](../concepts/floating_datum.md)
- [Diving-wave tomography](../concepts/diving_wave_tomography.md)
