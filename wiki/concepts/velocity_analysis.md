---
title: Velocity analysis
status: draft
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - cgg_odt01_data_analysis_part2
  - jones_2012_incorporating_near_surface_velocity_anomalies
tags:
  - velocity
  - semblance
  - stacking
---

# Velocity analysis

**Velocity analysis** estimates the stacking or NMO velocity by scanning candidate hyperbolae on CMP gathers and measuring coherence. The result is a velocity spectrum: a 2-D panel with zero-offset time on the vertical axis and velocity on the horizontal axis.

## How it works

For each trial pair $(t_0, V)$:

1. Compute the NMO shift for every offset.
2. Align samples along the corresponding hyperbola.
3. Measure coherence, for example with semblance.

Bright peaks in the spectrum mark velocities that flatten the gather.

## Semblance

Semblance is the preferred coherence measure because it is robust to amplitude variations:

$$
S(t_0, V) = \frac{1}{M} \frac{\sum_\tau \left[ \sum_{i=1}^{M} u_i(\tau - \Delta t_i) \right]^2}{\sum_\tau \sum_{i=1}^{M} u_i^2(\tau - \Delta t_i)},
$$

where $M$ is the number of offsets. Semblance ranges from 0 to 1 and is high only when aligned traces are coherent.

## Vertical and horizontal spectra

- A **vertical velocity spectrum** is computed at one CMP location.
- **Horizontal** or horizon-consistent spectra show velocity variations along a line or around a picked horizon.

## Bias from statics

Long-wavelength statics shift the whole CMP gather in time. The events remain hyperbolic but have the wrong $t_0$, which biases the velocity estimate. This is one reason floating datums are used.

## Relation to lecture notes

Core topic in [Term 1 Lecture 02 — Kinematics, Velocities and Field Statics](../lecture_ready/term01_lec02_kinematics_and_field_statics.md).
