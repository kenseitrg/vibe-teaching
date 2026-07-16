---
title: Davletkhanov — Near-Surface Model and Velocity
status: draft
source_type: thesis
authors: Rishat Talgatovich Davletkhanov
year: 2017
url: null
lectures:
  - term03_lec02
related_concepts:
  - static_corrections
  - velocity_analysis
  - effective_velocity
  - seismic_velocities
tags: [near-surface, statics, velocity, effective-velocity, velocity-model]
---

# Davletkhanov — Near-Surface Model and Velocity

Dissertation (кандидат физико-математических наук), Moscow State University, 2017: "Коррекция сейсмических записей за влияние верхней части разреза с сохранением кинематики отражённых волн, соответствующих пластовой модели среды" (Correction of seismic records for the influence of the near-surface while preserving the kinematics of reflected waves corresponding to a layered earth model).

## Main message

Conventional static corrections can distort the very velocity estimates they are meant to prepare. The dissertation identifies which spatial wavelengths of near-surface heterogeneity should be treated as statics and which must be built into the velocity model.

## Key findings

- **Medium- and long-wavelength near-surface heterogeneity** (topography, weathering variations, permafrost) biases kinematic inversion and RMS/effective-velocity estimates if it is handled only by static shifts.
- **Short-wavelength heterogeneity** should still be removed by static corrections; including it in the velocity model makes the model non-smooth and worsens migration results.
- The distortion is demonstrated on 2D and 3D synthetic data and on a 3D real-data case from West Siberia.
- Two remedies are proposed:
  1. **Kinematic-dynamic transformation**: a wave-equation-based redatuming that preserves reflection kinematics.
  2. **Hyperboloid + trend parameterization**: the CMP reflection traveltime is parameterized as a hyperbola plus a low-frequency trend of static corrections, giving a nearly unbiased depth-velocity model.
- The work emphasizes the ill-posed separation of surface and subsurface factors in conventional statics + NMO velocity analysis.

## Relation to lecture notes

Supports Term 3 Lecture 2: link between statics and stacking velocities, effective velocity, and why inaccurate near-surface models create velocity artifacts.

## Related concepts

- [Static corrections](../concepts/static_corrections.md)
- [Velocity analysis](../concepts/velocity_analysis.md)
- [Effective velocity](../concepts/effective_velocity.md)
- [Seismic velocities](../concepts/seismic_velocities.md)
