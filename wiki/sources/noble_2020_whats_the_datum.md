---
title: Noble (2020) — What's the Datum?
status: reviewed
type: conference presentation
source_file: papers/statics/What's the Datum.pdf
language: en
pages: 7
concepts:
  - static_corrections
  - seismic_velocities
tags: [statics, datum, replacement-velocity, floating-datum]
---

# Noble (2020) — What's the Datum?

Conference presentation by Jason L. Noble (Headwaters Seismic Processing) at GeoConvention 2020.

## Main message

Datum and replacement velocity are often treated as bulk shifts, but they have a measurable impact on structural reliability. The talk distinguishes several datums and explains how replacement velocity choices affect long-wavelength statics.

## Key definitions

- **Datum**: an elevation used as a reference surface for seismic data.
- **Client datum**: the final flat elevation datum to which the data are delivered.
- **Processing datum**: a datum used to perform processing steps (e.g., NMO) from.
- **Floating datum**: a smoothed surface through the actual topography; used so that NMO sees locally hyperbolic moveout.
- **Replacement velocity**: best estimate of vertical velocity in consolidated material below the weathering layer.

## Important points

- Seismic data are originally recorded to a datum of topography.
- Correcting to a flat client datum changes the zero-offset time $T_0$ but does not change the physical hyperbolic response, which can degrade NMO.
- A processing datum (topography or floating datum) keeps moveout closer to hyperbolic.
- Refraction statics can use an **intermediate datum** at the base of the weathering; the choice of final datum and replacement velocity can be changed later.
- Static correction $T = D/V$: low replacement velocity gives large static, high replacement velocity gives small static.
- The effect of wrong replacement velocity is subtle but visible on structure.
- You cannot simply undo the elevation correction on stacked data because the trace header CDP elevation is interpolated and the data have been affected by refraction/residual statics, mutes, NMO, migration, etc.

## Relation to lecture notes

Supports Term 1 Lecture 02 (field statics, datums, replacement velocity) and Term 1 Lecture 03 (floating datum, link between statics and velocity analysis).
