---
title: Static corrections
status: draft
sources:
  - hutchinson_link_1984_surface_consistency
  - cgg_odt01_data_analysis_part1
  - noble_2020_whats_the_datum
  - jones_2012_incorporating_near_surface_velocity_anomalies
tags:
  - statics
  - near-surface
  - datum
---

# Static corrections

**Static corrections** are trace-constant time shifts that compensate for near-surface traveltime variations such as elevation changes and weathering-layer thickness/velocity anomalies.

## Components

For land data, Jones (2012) decomposes near-surface statics into:

- **High spatial frequency (HF)** surface-consistent source and receiver components from rapid topography and rapid near-surface velocity variation.
- **Low spatial frequency (LF)** CMP-consistent component to move all traces in a CMP to a common flat processing datum at the CMP elevation.
- **Very high frequency (VHF)** jitter removed by residual statics.

## Key datums

- **Client datum**: final flat datum for delivery.
- **Intermediate datum**: often near the base of weathering.
- **Floating datum**: smoothed version of topography used during NMO/velocity analysis.
- **Final flat velocity datum**: for migration velocity model, often above the highest topography.

## Replacement velocity

The velocity used to replace the weathered layer when moving data to a datum. A low replacement velocity gives large statics; a high replacement velocity gives small statics.

## Related concepts

- [Floating datum](floating_datum.md)
- [Residual statics](residual_statics.md)
- [Layer replacement](layer_replacement.md)

## Lectures

- [Term 1 Lecture 02 — Kinematics, Velocities and Field Statics](../lecture_ready/term01_lec02_kinematics_and_field_statics.md)
- [Term 1 Lecture 03 — Advanced Statics and the Link to Velocity Analysis](../lecture_ready/term01_lec03_advanced_statics_and_velocity_link.md)
