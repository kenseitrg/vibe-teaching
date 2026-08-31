---
title: Residual statics
status: draft
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - jones_2012_incorporating_near_surface_velocity_anomalies
  - margrave_2006_methods_of_seismic_data_processing
  - li_1999_introduction_to_residual_statics_analysis
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

The surface-consistent form is justified by the physics of the near surface. A sharp velocity contrast at the base of the weathering layer forces rays from many subsurface reflection points to become nearly vertical as they pass through the low-velocity near surface. Because the rays are almost vertical, the traveltime spent in the near surface depends mainly on where a ray enters or leaves the surface, not on the deeper reflection point. The source-side contribution therefore depends only on the source location $i$, and the receiver-side contribution depends only on the receiver location $j$.

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

## Wiggins et al. linear model

Margrave (Chapter 5, page 5-19) gives the Wiggins, Larner & Wisecup (1976) model for the total traveltime of a trace from shot $i$ into receiver $j$ in CMP $k$:

$$
T_{ij} = S_i + R_j + G_k + M_k X_{ij}^2,
$$

where $S_i$ is the source static, $R_j$ the receiver static, $G_k$ the structure term, $M_k X_{ij}^2$ an approximate residual NMO term, and $X_{ij}$ the offset. The residual shift $\delta T_{ij}$ is measured by cross-correlation against a pilot trace. The model is written as an overdetermined linear system

$$
A \mathbf{p} = \mathbf{f},
\qquad
\mathbf{p} = (A^T A)^{-1} A^T \mathbf{f},
$$

and solved iteratively because $A$ is large and sparse.

## Resolution limits and constraints

A fundamental result of Wiggins et al. is that the linear system can **only resolve statics trends whose spatial wavelength is shorter than about a spread length**. Trends much longer than the spread length are not reliably recovered and, unless constrained, will leak into the source/receiver/structure solutions. For this reason residual statics solutions are usually forced to zero mean; the long-wavelength part is handled by field statics, layer replacement, or a floating datum. After the long-wavelength component is removed in the CMP domain, the remaining source and receiver residual statics are no longer strictly surface-consistent because a given source or receiver may carry different values for different CMP gathers.

## Practical considerations

Margrave lists several practical controls:

- **NMO removal**: residual statics work best when residual NMO is already small. The linear model assumes the residual NMO is constant with time, so iterations of velocity analysis and residual statics are common.
- **Correlation window**: choose a window that follows a package of strong, continuous reflectors. It should be long enough for a stable correlation but avoid first arrivals (so it cannot start too shallow) and avoid multiples (so it cannot extend too deep). It should also avoid shallow, structurally complex intervals and low-frequency "ringy" data that can cause cycle skipping.
- **Correlation length**: must be large enough to span the expected sum of source, receiver, structure, and residual-NMO shifts; too small causes poor solutions, too large increases cost and cycle skipping.
- **Pilot traces**: traces are correlated against a pilot trace (e.g., a stack of adjacent CMPs) rather than against every other trace. Better pilot traces improve the solution but can also bias it toward the pilot.
- **Data preparation**: data are often bandpass filtered, AGC'd, or F-K filtered to build the statics solution, but the computed shifts are applied to the unfiltered data.
- **Application order**: because statics are computed from moveout-corrected data, they are most properly applied after NMO; sometimes they are applied before NMO to improve velocity analysis or prestack migration.

## Quality control

After solving, check that the estimated source and receiver statics are geophysically consistent. In nearby spatial locations they should usually have the same sign (both positive or both negative). The exception is a buried source, where the source and receiver statics may legitimately have different signs.

## Gauss–Seidel solution

A Gauss–Seidel iteration updates one component class at a time while holding the others fixed. For example, to update source statics:

$$
s_i^{(n+1)} = \frac{1}{N_i} \sum_{\text{traces with source } i} \left( d_{ijkl} - r_j^{(n)} - h_k^{(n)} - c_l^{(n)} \right).
$$

Then update receivers, offset classes, and CMP terms in turn. Hatton reports convergence in 4–5 iterations for typical profiles.

Li (1999, Chapter 2) emphasizes that the system is **over-determined** (far more traces than source/receiver/CMP locations) but also **under-constrained** (adding a constant to all sources and subtracting it from all receivers leaves the fit unchanged). This is why constraints such as zero mean are applied and why long-wavelength content cannot be recovered reliably.

## Relation to lecture notes

Core material for Term 1 Lecture 04: Advanced Statics and the Link to Velocity Analysis.
