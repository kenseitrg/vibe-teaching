---
title: Diving-wave tomography
status: draft
sources:
  - law_trad_comparison_of_refraction_inversion_methods
  - hill_introduction_to_seismic_processing_ch22
  - term03_lecture02_statics_and_kinematics_presentation
tags: [tomography, refraction, statics, near-surface]
---

# Diving-wave tomography

Diving-wave tomography (also called turning-ray tomography or tomostatics) uses the first arrivals that turn back to the surface in a continuous velocity gradient to estimate a near-surface velocity model.

## How it differs from layered refraction methods

- **Layered refraction statics** assumes discrete velocity interfaces and solves for layer thickness and velocity using delay times or generalized reciprocals.
- **Diving-wave tomography** treats the near surface as a grid of cells with smooth velocity variations. Rays are traced through the grid and the model is updated to match observed first-arrival times.

## Governing equations

- The ray path is governed by the ray equations or by the **Eikonal equation**, which relates traveltime to the local slowness model.
- Inversion is usually linearized and solved iteratively: model the traveltimes, compare with picks, back-project the residuals along ray paths, and update the velocity grid.

## Strengths and weaknesses

- Strengths: can handle velocity gradients, complex near-surface geology, and gradual lateral changes; does not require discrete refractors.
- Weaknesses: requires sufficiently long offsets to capture turning rays; can be unstable where ray coverage is low (edges, gaps); solutions are non-unique and depend on smoothing and starting model.

## Relation to statics

The output velocity model is used to compute trace-by-trace time shifts (statics) that bring the data to a flat datum. Because the model is continuous, it can also be used directly in depth migration instead of conventional statics.
