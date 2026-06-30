---
title: Layer replacement method
status: draft
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - jones_2012_incorporating_near_surface_velocity_anomalies
  - margrave_2006_methods_of_seismic_data_processing
tags:
  - statics
  - layer-replacement
  - long-wavelength-statics
  - near-surface
---

# Layer replacement method

The **layer replacement** (or *layer stripping*) method is used when refraction statics and near-surface model building cannot fully resolve long-wavelength statics caused by the overburden. It is common in areas with complex near-surface geology, karst, dunes, or salt diapirs near the surface.

## When is it needed?

- Refraction methods only resolve what first arrivals illuminate.
- Some anomalies are below the penetration depth of refraction rays.
- Well control may be sparse or absent.
- Long-wavelength time distortions remain on stacked sections.

## Core idea

Replace the real near-surface geology with a simpler velocity model so that the remaining statics are short-wavelength and can be handled by residual statics or tomography.

## Typical workflow

1. Pick a reference horizon in two-way time.
2. Perform horizontal velocity analysis along the horizon to estimate $V_\text{nmo}(x)$ and $V_\text{int}(x)$.
3. Convert the picked horizon from time to depth using the interval velocities.
4. Smooth the depth surface (and tie to wells if available).
5. Convert the smoothed depth surface back to time.
6. Estimate a replacement velocity for the layer being replaced.
7. Compute long-wavelength static corrections from the difference between original and smoothed surfaces.
8. Apply statics and QC by re-picking the reference horizon.

Margrave (Chapter 5) connects this to the general statics model: the bulk, long-wavelength component of the total static should be removed from the data early and saved for a final datum shift, so that NMO, residual statics, and velocity analysis are not biased by large bulk shifts.

## Risks and pitfalls

- Wrong replacement velocity produces wrong statics.
- Over-smoothing removes real geology.
- A poor reference horizon corrupts the whole result.
- The method assumes the anomaly is in the layer being replaced, not below it.

## Relation to lecture notes

Supports Term 1 Lecture 03: Advanced Statics and the Link to Velocity Analysis.
