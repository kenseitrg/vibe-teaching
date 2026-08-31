---
title: Near-surface velocity model
status: draft
sources:
  - davletkhanov_nsm_and_velocity
  - velocity_artefacts
  - jones_2012_incorporating_near_surface_velocity_anomalies
  - law_trad_comparison_of_refraction_inversion_methods
  - hill_introduction_to_seismic_processing_ch22
tags: [near-surface, velocity, statics, model]
---

# Near-surface velocity model

A near-surface velocity model describes the seismic velocities in the shallow subsurface (typically the weathering layer, unconsolidated sediments, and any permafrost or karst bodies). It is used to compute static corrections, design migration datums, and build the starting model for deeper velocity analysis.

## Sources of information

- **First-break refraction**: traveltimes of head waves and diving waves constrain the shallow velocity structure.
- **Uphole times**: direct measurements of vertical traveltime in shot holes give weathering-layer velocity.
- **Surface geology and topography**: lithology and elevation guide the model and the choice of datum.
- **Migration velocity analysis**: shallow reflection velocities can be inverted for interval velocities above a reference horizon.
- **Full-waveform inversion**: uses the full wavefield to obtain higher-resolution shallow models.

## Why it is hard to estimate

- Acquisition sampling is usually too coarse to capture small-scale near-surface heterogeneity.
- The weathering layer is highly variable laterally and can change with time (rainfall, temperature).
- Refraction and tomography methods are non-unique; different models can predict the same first-arrival times.
- A model that is adequate for statics may still be too coarse for accurate depth migration.

## Impact on processing

- Errors in the near-surface model cause residual statics, biased stacking velocities, and false structural anomalies.
- A reliable model allows the processor to choose between conventional static corrections and wave-equation datuming / depth migration.
- The model also determines how long-wavelength near-surface variations should be split between statics and the deeper velocity model.
