---
title: Floating datum
status: draft
sources:
  - noble_2020_whats_the_datum
  - jones_2012_incorporating_near_surface_velocity_anomalies
  - hatton_worthington_makin_1986_seismic_data_processing
tags:
  - statics
  - floating-datum
  - velocity-analysis
  - datum
---

# Floating datum

A **floating datum** is a reference surface that follows the long-wavelength statics trend instead of being a flat plane. It is used during NMO and velocity analysis so that reflection events remain hyperbolic and close to their true zero-offset times.

## Why it is needed

Long-wavelength statics shift the entire CMP gather by a constant time. The events remain hyperbolic, but with the wrong $t_0$:

$$
t^2(x) = (t_0 + \Delta t)^2 + \frac{x^2}{V^2}.
$$

If velocity analysis fits $t^2(x) = t_0^2 + x^2/V_\text{apparent}^2$ to shifted data, the apparent velocity $V_\text{apparent}$ is biased. The bias occurs because the wrong $t_0$ forces the hyperbola to stretch or compress in a way that mimics a velocity error.

## Definition

The floating datum is a smoothed version of the total static surface. It is locally flat within a CMP gather but follows the long-wavelength trend across the survey.

## Computation from total statics

$$
\Delta t_\text{floating} = \Delta t_\text{total} - \Delta t_\text{smoothed},
$$

where $\Delta t_\text{smoothed}$ is a long-wavelength (low-spatial-frequency) version of the total static. The smoothed part is applied later as a final static to a flat datum.

## Effect

- After floating-datum correction, events in a CMP gather are hyperbolic and near their true $t_0$.
- Velocity analysis gives unbiased velocity picks.
- The long-wavelength shift is applied only after velocities are known.

## Relation to lecture notes

Central concept in Term 1 Lecture 03: Advanced Statics and the Link to Velocity Analysis.
