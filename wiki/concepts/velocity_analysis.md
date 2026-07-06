---
title: Velocity analysis
status: draft
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - cgg_odt01_data_analysis_part2
  - jones_2012_incorporating_near_surface_velocity_anomalies
  - margrave_2006_methods_of_seismic_data_processing
  - li_1999_introduction_to_residual_statics_analysis
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

## Stacking velocity as a best-fit hyperbola

Margrave (Chapter 7) defines **stacking velocity** $V_s$ as the velocity parameter that produces the best-fit hyperbola to the actual traveltime curve on a CMP gather. The precise meaning of "best fit" depends on the software, and $V_s$ is a function of the maximum offset used in the analysis. If the maximum offset changes, the stacking velocity can change even for the same reflector. For flat, horizontally layered media with no lateral velocity variation, $V_s$ closely approximates the RMS velocity.

## Bias from statics

Long-wavelength statics shift the whole CMP gather in time. The events remain hyperbolic but have the wrong $t_0$, while the curvature — the $x^2$ term — is unchanged. Velocity analysis fits the same curvature to a hyperbola with the wrong zero-offset time, which biases the velocity estimate (Li, 1999, Chapter 1; Margrave, Chapter 7). This is one reason floating datums are used. Margrave describes this as a chicken-and-egg problem: velocity analysis requires statics corrections first, while residual statics work best when residual NMO is minimal. The practical solution is iterative refinement of velocities and statics, often with a floating datum between the iterations.

## Relation to lecture notes

Core topic in [Term 1 Lecture 03 — Kinematics, Velocities and Field Statics](../lecture_ready/term01_lec03_kinematics_and_field_statics.md).
