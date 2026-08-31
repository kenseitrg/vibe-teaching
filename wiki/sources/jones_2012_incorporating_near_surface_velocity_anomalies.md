---
title: Jones (2012) — Incorporating near-surface velocity anomalies in pre-stack depth migration models
status: reviewed
type: journal article
source_file: papers/statics/Jones - Near Surface.pdf
language: en
pages: 12
lectures:
  - term03_lec02
concepts:
  - static_corrections
  - seismic_velocities
  - velocity_analysis
related_concepts:
  - static_corrections
  - seismic_velocities
  - velocity_analysis
  - near_surface_velocity_model
  - migration_datum
tags: [statics, near-surface, floating-datum, velocity-anomaly, tomography, fwi]
---

# Jones (2012) — Incorporating near-surface velocity anomalies in pre-stack depth migration models

Tutorial article by Ian F. Jones, *First Break*, Vol. 30, March 2012.

## Main message

Unresolved near-surface velocity anomalies degrade deeper imaging. Conventional time processing (NMO / PreSTM) assumes a 1-D velocity-time function per CMP and cannot compensate for short-wavelength lateral anomalies. The article reviews practical methods and the emerging role of waveform inversion.

## Key concepts

### Sources of statics for land data

A static is a time shift applied to a trace to accommodate:
- a shift from true surface elevation to a processing datum, or
- travel-time distortion from an unresolved velocity anomaly.

Components of the near-surface static (Figure 8):
- **High spatial frequency (HF)**: surface-consistent source and receiver components from rapid topography and rapid near-surface velocity variation.
- **Low spatial frequency (LF)**: CMP-consistent component to move all traces in a CMP from shot/receiver elevations to a common flat processing datum at the CMP elevation.
- **Very high frequency (VHF)**: residual jitter removed by residual statics.

### Datums

- **Floating datum**: specific to each individual CMP gather, locally flat, designed so that moveout looks hyperbolic within the gather after the traces are moved to it.
- **Final flat datum**: for migration velocity model, often above the highest topography, with constant replacement velocity between it and the floating datum.
- For pre-stack migration, one may not want to apply all static corrections because they can introduce near-surface image distortions.

### Why statics bias velocity analysis

NMO/PreSTM treats all traces in a CMP as if they propagated in a 1-D earth model containing the anomaly. Far-offset raypaths that do not encounter the anomaly are still corrected with the CMP's velocity, causing overcorrection or undercorrection. Conventional velocity analysis is biased to flatten the far offsets, producing a slight push-down on mid-offsets.

### Practical methods for near-surface anomalies

1. Conventional tomography when moveout error is measurable on gathers.
2. Manual picking of geobody geometry + trial velocity when gathers are not usable.
3. Deeper geometric distortion (pull-up/push-down) to infer the anomaly.
4. Refraction tomography (turning/diving rays).
5. Waveform inversion (FWI) for highest resolution.

## Relation to lecture notes

Directly supports Term 1 Lecture 04: floating datum, statics–velocity analysis interaction, and residual statics.
