---
title: Residual statics
status: draft
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - jones_2012_incorporating_near_surface_velocity_anomalies
tags:
  - statics
  - residual-statics
  - surface-consistent
  - gauss-seidel
---

# Residual statics

**Residual statics** are trace-constant time shifts left after field statics and layer replacement. They are estimated from the reflection data itself because the near-surface model is never perfect.

## Why residuals remain

- Limitations of the near-surface velocity model.
- Short-wavelength heterogeneity (karst, small dunes, loose soil).
- Picking errors in refraction or tomographic statics.
- Noise.

## Cross-correlation with a reference trace

A common first step:

1. Build a reference trace, usually a stacked pilot trace from neighbouring CMPs.
2. Cross-correlate each trace in the CMP gather with the reference.
3. The lag of the maximum correlation is the estimated time shift.
4. Apply quality control: correlation threshold, consistency checks.

Limitations:
- Assumes hyperbolic moveout has already been removed.
- Cycle skipping when shifts exceed half a period.
- Reference trace itself may be biased.

## Surface-consistent 4-component model

The total residual static for a trace can be decomposed into four components (Hatton, Worthington & Makin, Section 5.10):

$$
\Delta t_{ijkl} = s_i + r_j + h_k + c_l + \text{noise},
$$

where

- $s_i$ = source-side residual static,
- $r_j$ = receiver-side residual static,
- $h_k$ = offset-class residual moveout,
- $c_l$ = CMP structural term (geology, not a static).

In practice the $c_l$ term is removed before solving because it represents structure, not a time shift.

## Least-squares formulation

For all measured time shifts $\mathbf{d}$, the unknown components $\mathbf{m}$ are related by a design matrix $G$:

$$
\mathbf{d} = G \mathbf{m} + \text{noise}.
$$

The least-squares solution minimizes

$$
\| \mathbf{d} - G \mathbf{m} \|^2.
$$

Because $G^\top G$ is large and singular, direct inversion is impractical.

## Gauss–Seidel solution

A Gauss–Seidel iteration updates one component class at a time while holding the others fixed. For example, to update source statics:

$$
s_i^{(n+1)} = \frac{1}{N_i} \sum_{\text{traces with source } i} \left( d_{ijkl} - r_j^{(n)} - h_k^{(n)} - c_l^{(n)} \right).
$$

Then update receivers, offset classes, and CMP terms in turn. Hatton reports convergence in 4–5 iterations for typical profiles.

## Relation to lecture notes

Core material for Term 1 Lecture 03: Advanced Statics and the Link to Velocity Analysis.
