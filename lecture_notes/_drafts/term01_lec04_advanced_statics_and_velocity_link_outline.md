# Term 1 Lecture 04 — Advanced Statics and the Link to Velocity Analysis

## Scope

This is the second half of the original "kinematics and statics" lecture. It covers:

1. Layer replacement method for long-wavelength statics.
2. Residual statics: from cross-correlation with a reference trace to the 4-component surface-consistent model and Gauss–Seidel solution.
3. Link between statics corrections and velocity analysis: how large time shifts cause errors in velocity estimation, why good velocities require hyperbolic events, and the floating-datum solution.

Lecture 03 must be covered first: velocity models, NMO, velocity analysis, field statics, and refraction-based near-surface model building.

## Learning objectives

By the end of this lecture students should be able to:

- Explain when and why the layer-replacement method is used for long-wavelength statics.
- Describe the workflow of residual statics: pick reference trace, cross-correlate, solve surface-consistent decomposition.
- State the 4-component model (source, receiver, offset, CMP) and sketch the Gauss–Seidel solution idea.
- Explain why large static shifts bias velocity picks and why statics must be solved before reliable velocity analysis.
- Define the floating datum and show how to compute corrections from total statics.

## Prerequisites

- Term 1 Lecture 03: NMO, velocity analysis, field statics, refraction statics.
- CMP geometry and stacking.
- Basic linear algebra: systems of equations, iterative solution.

## Timing (90 minutes)

| Section | Time | Notes |
|---------|------|-------|
| 1. Layer replacement | 20 min | Motivation, workflow, example |
| 2. Residual statics overview | 10 min | Why residuals remain, reference trace |
| 3. Cross-correlation residual statics | 15 min | Picking time shifts |
| 4. Surface-consistent 4-component model | 25 min | Decomposition, Gauss–Seidel |
| 5. Statics and velocity analysis link | 15 min | Bias, hyperbolic events, need for statics |
| 6. Floating datum | 5 min | Definition, computation from total statics |
| Total | 90 min | Tight; derivation of Gauss–Seidel must be concise |

## Section 1 — Layer replacement method for long-wavelength statics

- Motivation: refraction methods cannot always resolve all near-surface anomalies, especially when no well control exists.
- Core idea: replace the near-surface geology with a simpler velocity model so that the remaining statics are short-wavelength.
- Typical workflow:
  1. Pick a reference horizon in time.
  2. Run horizontal velocity analysis along the horizon: estimate $V_\text{nmo}(x,y)$ and $V_\text{int}(x,y)$.
  3. Convert the horizon from time to depth using the picked velocities.
  4. Smooth the depth surface and tie to wells if available.
  5. Convert the smoothed surface back to time.
  6. Estimate a replacement velocity.
  7. Compute long-wavelength static corrections from the difference between original and smoothed time/depth surfaces.
  8. Apply statics and QC by re-picking the reference horizon.
- What can go wrong: wrong replacement velocity, over-smoothing, poor reference horizon.
- Figure needed: cross-section showing distorted horizon, depth conversion, smoothing, back-conversion, static correction.

## Section 2 — Why residual statics remain

- After field statics and layer replacement, small uncorrected time shifts remain.
- Causes: limitations of near-surface model, short-wavelength heterogeneity, picking errors, noise.
- Residual statics must be estimated from the reflection data itself.
- Reference trace: stacked pilot trace or pilot trace from adjacent CMPs.

## Section 3 — Cross-correlation with a reference trace

- For each trace in a CMP gather, cross-correlate with the reference trace.
- Lag of the maximum correlation gives a time shift estimate.
- Quality control: correlation coefficient threshold, consistency checks.
- Limitations: assumes a hyperbolic moveout has already been removed, cycle skipping when shifts exceed half a period.
- Figure needed: trace + reference trace + cross-correlation function with peak marked.

## Section 4 — Surface-consistent 4-component decomposition

- The total residual static for a trace is decomposed into four components:
  $$ \Delta t_{ijkl} = s_i + r_j + h_k + c_l + \text{noise} $$
  where $i$ = source, $j$ = receiver, $k$ = offset class, $l$ = CMP.
- Physical interpretation of each component:
  - $s_i$: source-side residual static.
  - $r_j$: receiver-side residual static.
  - $h_k$: offset-dependent residual moveout (not always used as a static).
  - $c_l$: CMP structural term (geology, not static; often removed before solving).
- Design matrix $G$ relates observed shifts to unknown components.
- Least-squares formulation:
  $$ \min_{\mathbf{m}} \| \mathbf{d} - G\mathbf{m} \|^2 $$
- Gauss–Seidel iteration: update one component class at a time while holding others fixed.
- Why Gauss–Seidel is natural here: each update is a simple mean over the relevant traces.
- Figure needed: small example of a design matrix.

## Section 5 — Link between statics and velocity analysis

- Long-wavelength statics shift the whole CMP gather by a constant time $\Delta t$.
- The events remain hyperbolic, but with the wrong zero-offset time:
  $$ t^2(x) = (t_0 + \Delta t)^2 + \frac{x^2}{V^2} $$
  is not the same as fitting
  $$ t^2(x) = t_0^2 + \frac{x^2}{V_\text{apparent}^2}. $$
- Expanding shows that a wrong $t_0$ forces the velocity analysis to pick a wrong $V_\text{apparent}$.
- Therefore long-wavelength statics bias velocity picks even though the gather still looks hyperbolic.
- The solution is to keep events close to their recorded times while still making them hyperbolic.
- This is the role of an intermediate/floating datum.
- Iterative workflow:
  1. Apply floating-datum corrections (short-wavelength part of total statics).
  2. Run velocity analysis; events are hyperbolic and near their true $t_0$.
  3. Apply residual statics if needed.
  4. Apply the long-wavelength static to move data to the final flat datum.

## Section 6 — Floating datum

- Definition: a datum that follows the long-wavelength statics trend instead of being a flat plane.
- Purpose: preserve hyperbolic moveout for velocity analysis while still removing short-wavelength statics.
- Computation from total statics:
  - Total static = source static + receiver static + long-wavelength component.
  - Floating-datum correction = total static minus a smoothed (long-wavelength) version of itself.
  - The smoothed part is applied later as a final static.
- Key insight: events are hyperbolic after floating-datum correction, so velocity analysis is unbiased; the long-wavelength shift is applied only after velocities are known.
- Figure needed: cross-section showing flat final datum vs. floating datum; correction terms; gather before/after floating-datum correction.

## Figures to generate

| Figure | Script | Output |
|--------|--------|--------|
| Layer replacement workflow | `plot_layer_replacement.py` | `term01_lec04_layer_replacement.png` |
| Cross-correlation statics | `plot_crosscorrelation_statics.py` | `term01_lec04_crosscorrelation_statics.png` |
| 4-component decomposition example | `plot_four_component_model.py` | `term01_lec04_four_component_model.png` |
| Statics bias velocity analysis | `plot_statics_velocity_bias.py` | `term01_lec04_statics_velocity_bias.png` |
| Floating datum | `plot_floating_datum.py` | `term01_lec04_floating_datum.png` |

## Key equations to include

- 4-component residual statics model.
- Least-squares objective for surface-consistent decomposition.
- Gauss–Seidel update for one component class.
- Floating-datum correction from total statics.

## Comprehension questions

1. Why can refraction statics leave long-wavelength residuals that require layer replacement?
2. In the 4-component model, which component should represent geology rather than a static shift, and why?
3. Why does cycle skipping limit cross-correlation residual statics when shifts are large?
4. How does a residual static shift on the near-offset traces bias a semblance velocity pick?
5. What problem does a floating datum solve, and how is it computed from total statics?

## Sources to cite

- Hatton, Worthington & Makin (1986), *Seismic Data Processing: Theory and Practice* — residual statics, surface-consistent model.
- CGG ODT01A Data Analysis Part 2 — statics and velocity analysis interaction.
- Existing slide deck `slides/raw/term01_lecture02_kinematics.pptx`.
- Existing lecture plan `slides/raw/plan_term01_lecture02_kinematics.docx`.

## Open questions for instructor

- Should the 4-component model derivation be in the lecture notes or in a separate derivation document?
- Do you want a full numerical Gauss–Seidel example, or only the conceptual update formula?
- Should floating datum be introduced before or after residual statics in the lecture?
