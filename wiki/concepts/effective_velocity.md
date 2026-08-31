---
title: Effective velocity
status: draft
sources:
  - davletkhanov_nsm_and_velocity
  - sysoev_statics
  - velocity_artefacts
  - jones_2012_incorporating_near_surface_velocity_anomalies
tags: [velocity, statics, near-surface, datum]
---

# Effective velocity

Effective velocity is the stacking or NMO velocity that best flattens reflection moveout in a CMP gather after static corrections have been applied. It is an empirical estimate of the average velocity along the ray path, not necessarily the true interval velocity.

## How statics bias effective velocity

- A constant time shift (static) changes the zero-offset time $t_0$ but leaves the moveout curvature unchanged.
- Fitting the same curvature to a hyperbola with the wrong $t_0$ shifts the estimated velocity.
- A long-wavelength static that varies spatially can make effective velocities appear correlated with topography or near-surface anomalies.
- Elevation redatuming to a flat datum changes $t_0$ and therefore biases the effective velocity unless the datum is chosen carefully.

## Correcting the bias

- Redatuming sources and receivers to a **locally constant level** within each CMP preserves the hyperbolic moveout and gives a velocity closer to the true average velocity.
- Reduction formulas can convert velocities measured from one datum to another when the near-surface thickness and velocity are known.
- For large topographic relief, a full kinematic redatuming or wave-equation datuming is more accurate than a simple static shift.

## Practical importance

- Biased effective velocities lead to wrong depth conversion and false structural features.
- The effect is largest for shallow horizons (small $t_0$) and for large near-surface time shifts.
- Distinguishing between true velocity variation and statics-induced velocity variation is a central problem in land processing.
