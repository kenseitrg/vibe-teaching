---
title: Migration datum
status: draft
sources:
  - velocity_artefacts
  - noble_2020_whats_the_datum
  - jones_2012_incorporating_near_surface_velocity_anomalies
  - hill_introduction_to_seismic_processing_ch22
tags: [migration, datum, statics, near-surface]
---

# Migration datum

The migration datum is the reference surface to which seismic data are corrected before prestack or poststack migration. It is typically a flat surface chosen above the highest topography, and the interval between the acquisition surface and the datum is filled with a replacement velocity.

## Why the datum matters

- Migration assumes that sources and receivers lie on a single reference surface.
- If the datum is not handled correctly, near-surface time distortions are mapped into the migrated image as false structure or poor focusing.
- The choice of datum and replacement velocity affects both time and depth structural interpretation.

## Common datum choices

- **Acquisition surface / topography**: no static shift needed, but migration must handle topography.
- **Floating datum**: a smoothed surface close to the actual topography; keeps CMP moveout approximately hyperbolic and is used for velocity analysis and NMO.
- **Final flat datum**: a single elevation chosen for delivery; requires replacement velocity between the floating datum and the flat datum.
- **Intermediate datum**: a horizon near the base of the weathering layer used in refraction statics workflows.

## Replacement velocity

- The replacement velocity is the velocity assigned to the material between the datum and the acquisition surface.
- A low replacement velocity gives large static corrections; a high replacement velocity gives small corrections.
- The wrong replacement velocity can leave subtle but visible long-wavelength structural errors.

## Practical issues

- Once stacked and migrated, a datum correction cannot be simply undone because the data have been NMO-corrected, muted, and migrated.
- For complex near-surface areas, wave-equation datuming or depth migration with a detailed near-surface model is preferred over simple static shifts.
