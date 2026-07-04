---
title: Li (1999) — Residual statics analysis using prestack equivalent offset migration (Chapters 1–2)
status: reviewed
type: thesis
source_file: papers/statics/Li-MSc-1999.pdf
language: en
pages: 16-49
concepts:
  - residual_statics
  - static_corrections
  - floating_datum
  - velocity_analysis
  - common_midpoint
  - seismic_data_sorts
tags: [residual-statics, surface-consistent, cross-correlation, gauss-seidel, reference-trace, NMO, floating-datum]
---

# Li (1999) — Residual statics analysis using prestack equivalent offset migration (Chapters 1–2)

M.Sc. thesis by Xinxiang Li, University of Calgary, supervised by John C. Bancroft. Chapters 1 and 2 provide an introductory but detailed overview of residual statics analysis: the underlying assumptions, the conventional workflow, and the mathematical structure of the surface-consistent decomposition.

## Main message

Residual statics analysis is a three-step process: form reference traces that are as free as possible of near-surface traveltime errors, estimate trace-to-reference time shifts by cross-correlation, and decompose those shifts into surface-consistent source and receiver statics. The validity of the whole procedure rests on the assumptions that the near-surface effect is a pure, time-invariant, surface-consistent traveltime shift.

## Chapter 1 — Introduction to residual statics analysis

### The near-surface problem

The near-surface weathering layer changes seismic wave properties more dramatically than deeper layers. Although the near surface acts as an amplitude/phase filter, its most serious effect in processing is the traveltime anomaly. Decades of practice show that near-surface effects can be virtually corrected by estimating and removing these traveltime anomalies.

### Three basic assumptions

1. **Frequency and amplitude independent.** The anomaly is treated as a pure time shift, not as a frequency- or amplitude-dependent filter.
2. **Time-invariant.** The shift is the same for all reflection times on a trace. This is the defining distinction between *static* and *dynamic* corrections such as NMO.
3. **Surface-consistent.** The static on a trace is the sum of a source static and a receiver static. The same source static is shared by every trace in a shot record; the same receiver static is shared by every trace recorded at that receiver.

### Why surface consistency is physically reasonable

In the near-surface weathering layers, velocities are much lower than in deeper layers. By Snell’s law, ray paths in these low-velocity layers are forced toward the vertical. For reflection energy from a target at depth, the rays that enter or leave the surface at a given location therefore have very similar traveltimes through the near surface. This makes the source-side and receiver-side traveltime contributions largely independent of where the ray goes in the deeper subsurface.

Li notes that the assumption weakens when near-surface velocities are not much lower than deeper velocities, but the corresponding traveltime anomalies are also smaller. He also notes that the surface-consistent assumption is not just a simplification: it is a constraint on the estimated traveltime distortions, and it helps prevent statics solutions from absorbing unrelated errors.

### Field statics

- **Elevation statics**: compensate for elevation differences between the datum and the source/receiver locations. If uphole times are unavailable, the choice of weathering/replacement velocity dominates the result.
- **Refraction statics**: use first-break times to estimate velocities and thicknesses of near-surface layers. Quality depends on first-break picking; high redundancy improves the statistical reliability.
- **Uphole statics**: use uphole times and hole depths when shots are buried.

The magnitude of elevation and refraction statics can differ significantly depending on datum and replacement-velocity choices.

### Residual statics

- Field statics usually leave residual errors. Residual statics correct the short-wavelength remainder that field statics cannot resolve.
- Residual statics are **relative** shifts between closely located traces. They are plus-minus errors around the long-wavelength trend and are expected to have zero mean.
- A constant bulk shift does not change event continuity but does change stacking velocities. This is why floating datums are used: they reduce the change in absolute traveltime and keep NMO velocities more reliable.

### Historical context

Li traces the development from early methods (Hileman et al., 1968; Garotta and Michon, 1968; Disher and Naquin, 1969) through the comprehensive formulations of Taner et al. (1974) and Wiggins et al. (1976). The Wiggins et al. conclusion — that residual statics can resolve short-wavelength distortions but long-wavelength trends are limited by spread length — is highlighted.

He also notes that many methods (e.g., Ronen and Claerbout, 1985) iterate the reference-trace update with stack-power maximization, and that methods using migration concepts (Tjan et al., 1994; Larner, 1998) can reduce dependence on NMO velocity and cable length.

## Chapter 2 — Principles of residual statics analysis

### Three-step methodology

1. **Form reference traces** with reduced traveltime errors.
2. **Estimate time shifts** between each trace and its reference by cross-correlation.
3. **Decompose** the estimated shifts into surface-consistent source and receiver statics.

The algorithms for each step can be chosen independently in principle, but in practice steps 1 and 3 are coupled: if reference traces are built after NMO, the decomposition must account for residual NMO errors.

### Reference traces

- **Internal references**: selected from the same data set (e.g., another trace in the same CMP gather after NMO).
- **External references**: formed from the data but not directly selected as traces (e.g., stacked sections, f-x filtered common-offset sections, migration/de-migration model data).

CMP stacked traces are the most common external model. The thesis method uses equivalent-offset prestack migration (EOM) to form external reference traces before NMO correction and with minimal velocity dependence.

### NMO correction: advantages and limitations

Advantages:
- The original goal of residual statics is a good stack, and NMO is needed for stacking.
- NMO makes traces more similar, so reference traces are easier to form.
- Dynamic offsets are much larger than residual statics; NMO reduces them to residual NMO scale.

Limitations:
- Assumes hyperbolic CMP moveout, which can fail in complex structures.
- Requires velocity information, which may be unreliable when statics are large.
- NMO is a dynamic (time-variant) operation and slightly violates the time-invariance assumption of statics (e.g., NMO stretch).

### Cross-correlation

- Cross-correlation is the standard tool for estimating time shifts between a trace and a reference.
- Normalized cross-correlation $R_N$ ranges from $-1$ to $1$ and measures both the shift and the similarity of the two traces.
- The time-shift range should be limited, and the dominant frequency should be low enough to avoid multiple correlation maxima (cycle skipping). Low-pass filtering and reducing the maximum lag help.
- Interpolation of the correlation peak is needed for accurate sub-sample shifts.

### Correlation domains

Following Taner et al. (1974), the four data sorts give different dynamic/static influences on traveltime differences (Table 2-1):

| Domain | Dip | Velocity | Source static | Receiver static |
|--------|-----|----------|---------------|-----------------|
| Common receiver | ✔ | ✔ | ✔ | ✖ |
| Common source | ✔ | ✔ | ✖ | ✔ |
| Common offset | ✔ | ✖ | ✔ | ✔ |
| Common midpoint | ✖ | ✔ | ✔ | ✔ |

Dip and velocity effects are usually long-wavelength; source and receiver statics are short-wavelength. In shot or receiver gathers, cross-correlation can directly estimate receiver or source statics if the long-wavelength content is removed. In CMP or common-offset gathers, surface-consistent decomposition is needed.

### Trace windowing for correlation

- Choose a window with high signal-to-noise ratio and strong, stable events.
- The window must be long enough to contain several recognizable events and many times longer than the maximum expected shift.
- Avoid the shallow, NMO-stretched part of NMO-corrected traces.
- The specific length is data-dependent; Li does not recommend a fixed numerical window length.

### Decomposition procedure

#### Initial model

For a trace with source $i$ and receiver $j$:

$$
\Delta T_{SR} = \Delta T_S + \Delta T_R + \text{error}.
$$

If the error is small compared with the statics, the measured shifts can be decomposed into source and receiver statics. This gives an over-determined linear system with $N_S + N_R$ unknowns and $N_S \times N_R$ equations, but it is also under-constrained because one can add a constant to all source statics and subtract it from all receiver statics without changing the fit.

#### Subsurface-consistent (geological structure) term

Adding a subsurface-consistent term $\Delta T_G$ for each CMP gives:

$$
\Delta T_{ij} = \Delta T_{S_i} + \Delta T_{R_j} + \Delta T_{G_k} + \text{error}.
$$

This is the four-component model (source, receiver, CMP structure, residual NMO). It is also over-determined and under-constrained. The under-constrained nature means that some long-wavelength content can leak between the components unless constraints are applied.

#### After NMO correction

If reference traces are built from NMO-corrected data, residual NMO (RNMO) must be included as an offset-squared term:

$$
\Delta T_{ij} = \Delta T_{S_i} + \Delta T_{R_j} + \Delta T_{G_k} + E_{\text{NMO}} \, SR_{ij}^2 + \text{error}.
$$

Offset-dependent errors can also exist before NMO when the surface-consistent assumption weakens (large offsets or high near-surface velocities).

### Iterative techniques

- **Gauss–Seidel decomposition**: update source, receiver, and CMP terms one class at a time while holding the others fixed. The updated values are used immediately, which accelerates convergence but can introduce instability.
- **Reference-trace updating**: re-form reference traces after each round of statics is applied (e.g., Ronen and Claerbout’s stack-power maximization).
- **Velocity updating**: alternate between velocity analysis and residual statics estimation. Better velocity → better reference traces → better statics → better velocity.
- **Convergence limitations**: even with iterations, long-wavelength content cannot be resolved if the cable length is too short or CDP fold is too low. Migration-based methods can improve reliability by using the larger migration aperture.

## Relation to lecture notes

Supports Term 1 Lecture 03 — Advanced Statics and the Link to Velocity Analysis. Provides physical justification for the surface-consistent assumption, detailed discussion of the three-step residual-statics workflow, cross-correlation considerations, and the under-constrained nature of the Gauss–Seidel decomposition.
