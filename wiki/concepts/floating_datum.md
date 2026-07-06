---
title: Floating datum
status: draft
sources:
  - noble_2020_whats_the_datum
  - jones_2012_incorporating_near_surface_velocity_anomalies
  - hatton_worthington_makin_1986_seismic_data_processing
  - margrave_2006_methods_of_seismic_data_processing
  - li_1999_introduction_to_residual_statics_analysis
tags:
  - statics
  - floating-datum
  - velocity-analysis
  - datum
---

# Floating datum

A **floating datum** is a reference surface that follows the long-wavelength statics trend instead of being a flat plane. It is used during NMO and velocity analysis so that reflection events remain hyperbolic and close to their true zero-offset times.

## Why it is needed

Long-wavelength statics shift the entire CMP gather by a constant time. The events remain hyperbolic, but their zero-offset time $t_0$ is wrong while the curvature — the $x^2$ term — is unchanged:

$$
t^2(x) = (t_0 + \Delta t)^2 + \frac{x^2}{V^2}.
$$

If velocity analysis fits $t^2(x) = t_0^2 + x^2/V_\text{apparent}^2$ to shifted data, the apparent velocity $V_\text{apparent}$ is biased. The bias occurs because the wrong $t_0$ forces the hyperbola to stretch or compress in a way that mimics a velocity error, even though the curvature itself has not changed. Margrave emphasizes this is a **chicken-and-egg problem**: velocity analysis needs statics corrections first, but residual statics work best when residual NMO is minimal, so the data are usually improved by iterations of velocity analysis and residual statics.

Li (1999, Chapter 1) frames this in terms of the **relativity of residual statics**: residual statics are relative shifts between closely located traces and are expected to have zero mean. A constant bulk shift does not change event continuity but does change stacking velocities, which is why a floating datum is used to keep the absolute $t_0$ close to the true value during velocity analysis.

## Definition

The floating datum is a smoothed version of the total static surface. It is locally flat within a CMP gather but follows the long-wavelength trend across the survey.

## Computation from total statics

A practical floating-datum workflow works directly on the estimated source and receiver static fields:

1. **Smooth the source and receiver static fields** separately to obtain long-wavelength components $S^\text{LW}$ and $R^\text{LW}$.
2. **Interpolate the smoothed fields to each CMP location** $x_l$ and add them to get the total long-wavelength static at that CMP:
   $$
   \Delta t_\text{long-wavelength}(l) = S^\text{LW}(x_l) + R^\text{LW}(x_l).
   $$
3. **For each trace in CMP $l$, subtract half of this long-wavelength component from both the source and receiver statics**:
   $$
   s_i^\text{res}(l) = s_i - \frac{1}{2}\Delta t_\text{long-wavelength}(l), \qquad
   r_j^\text{res}(l) = r_j - \frac{1}{2}\Delta t_\text{long-wavelength}(l).
   $$
   Because the long-wavelength component is removed in the CMP domain, the residual source and receiver statics are no longer strictly surface-consistent: a given physical source or receiver may now carry different values for different CMP gathers.
4. **Apply the resulting residual corrections** to the traces.

The long-wavelength component is saved and applied later as a final static to the flat client datum after the velocity model is stable.

## Effect

- After floating-datum correction, each CMP gather sits on a locally flat surface close to the recording surface.
- Events in a CMP gather are hyperbolic and near their true $t_0$.
- Velocity analysis gives unbiased velocity picks because the large bulk $t_0$ shift has been removed.
- The long-wavelength shift is applied only after velocities are known.
- Margrave's recommendation is to keep the bulk static small during processing by removing the mean and applying the final shift to the interpretation datum at the end of the flow.

## Relation to lecture notes

Central concept in Term 1 Lecture 04: Advanced Statics and the Link to Velocity Analysis.
