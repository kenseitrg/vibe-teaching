# Slide outline — Term 1 Lecture 04
## Advanced Statics and the Link to Velocity Analysis

---

# Title

**Advanced Statics and the Link to Velocity Analysis**

Term 1, Lecture 04

---

# Learning objectives

By the end of this lecture you should be able to:

- Explain when and why layer replacement is used.
- Describe residual-statics workflow: reference trace, cross-correlation, surface-consistent decomposition.
- State the 4-component model and sketch Gauss–Seidel iteration.
- Explain why long-wavelength statics bias velocity picks.
- Define the floating datum and compute it from total statics.

---

# When refraction statics are not enough

- Refraction / tomography only resolve what first arrivals illuminate.
- Unresolved anomalies remain when:
  - weathering is too deep or complex,
  - karst, dunes, loose sediments create rapid lateral changes,
  - well control is sparse.
- Result: long-wavelength pull-ups and push-downs on stacked sections.

---

# Layer replacement method

- Replace the real near-surface geology with a simpler velocity model.
- Goal: remove long-wavelength distortion so residual statics can handle the rest.

Workflow:

1. Pick a reference horizon in time.
2. Estimate interval velocity along the horizon.
3. Convert horizon to depth.
4. Smooth the depth surface.
5. Convert back to time.
6. Compute statics from original vs. smoothed surfaces.
7. Apply and QC.

**Figure:** `figures/term01_lec04/term01_lec04_layer_replacement.png`

---

# Layer replacement — what can go wrong

- Wrong replacement velocity.
- Over-smoothing removes real geology.
- Poor reference horizon corrupts the result.
- Anomaly below the replaced layer is not handled.

---

# Residual statics: why they remain

- Near-surface model is never perfect.
- Short-wavelength heterogeneity remains.
- Picking errors and noise remain.
- Residual statics are estimated from the reflection data itself.

---

# Cross-correlation with a reference trace

1. Build a reference (pilot) trace.
2. Cross-correlate each trace with the reference.
3. Lag of maximum correlation = time shift.
4. QC: correlation threshold, consistency checks.

Limitation: cycle skipping when shifts exceed half a period.

**Figure:** `figures/term01_lec04/term01_lec04_crosscorrelation_statics.png`

---

# Correlation domains

Different data sorts isolate different static/dynamic effects:

| Domain | Dip | Velocity | Source static | Receiver static |
|--------|-----|----------|---------------|-----------------|
| Common receiver | yes | yes | yes | no |
| Common source | yes | yes | no | yes |
| Common offset | yes | no | yes | yes |
| Common midpoint | no | yes | yes | yes |

- Common-receiver gather: source static can be isolated.
- Common-source gather: receiver static can be isolated.
- CMP / common-offset: both source and receiver statics appear; decomposition needed.
- Dip/velocity are usually long-wavelength; source/receiver statics are short-wavelength.

---

# Surface-consistent 4-component model

Total residual static for a trace:

$$\Delta t_{ijkl} = s_i + r_j + h_k + c_l + \text{noise}$$

- $s_i$: source static
- $r_j$: receiver static
- $h_k$: offset-class residual moveout
- $c_l$: CMP structural term (geology)

The $c_l$ term must be removed before solving; otherwise structure is absorbed into statics.

**Figure:** `figures/term01_lec04/term01_lec04_four_component_model.png`

---

# Least-squares formulation

Measured shifts $\mathbf{d}$; unknown components $\mathbf{m}$.

$$\mathbf{d} = G \mathbf{m} + \boldsymbol{\epsilon}$$

Minimize:

$$\Phi(\mathbf{m}) = \| \mathbf{d} - G \mathbf{m} \|^2$$

$G^\top G$ is large and nearly singular — direct inversion is impractical.

---

# Overdetermined and under-constrained

Two contradictory properties of the system:

- **Overdetermined**: many more traces than unknowns ($N_s \times N_r$ equations, $N_s + N_r$ source/receiver unknowns). Redundancy makes the solution robust.
- **Under-constrained**: not unique. Adding a constant to all sources and subtracting it from all receivers leaves every trace equation unchanged. Long-wavelength trends can leak between components.

This is why residual statics are forced to zero mean and long-wavelength trends are handled separately.

---

# Gauss–Seidel solution

Update one component class at a time while holding others fixed.

Example: update source statics

$$s_i^{(n+1)} = \frac{1}{N_i} \sum_{\text{traces with source } i} \left( d_{ijkl} - r_j^{(n)} - h_k^{(n)} - c_l^{(n)} \right)$$

Then receivers, offsets, CMPs. Repeat sweeps until convergence.

Typically 4–5 sweeps.

---

# Long-wavelength statics bias velocity analysis

A long-wavelength static shifts the whole CMP gather uniformly. The event stays hyperbolic with the **same velocity**, but the wrong $t_0$:

$$t^2(x) = (t_0 + \Delta t)^2 + \frac{x^2}{V^2}$$

If velocity picking is tied to the original $t_0$ (fixed-time or horizon-consistent picking), the best-fit hyperbola is forced to a different slope:

$$t^2(x) = t_0^2 + \frac{x^2}{V_\text{apparent}^2}$$

Result: $V_\text{apparent} \neq V_\text{true}$ even though the curvature never changed.

**Figure:** `figures/term01_lec04/term01_lec04_statics_velocity_bias.png`

Speaker notes:
- Show panel (a): true and shifted hyperbolae have identical curvature.
- Show panel (b): shifted semblance peak has the correct velocity but wrong $t_0$; fixing $t_0$ to the original value gives a biased velocity.
- Show panel (c): true and shifted data have the same slope in $t^2$–$x^2$; the biased fit has a steeper slope.

---

# Iterative statics–velocity workflow

1. Apply initial statics (field + layer replacement).
2. Pick velocities on a floating datum.
3. Apply residual statics.
4. Re-pick velocities.
5. Repeat until convergence.

---

# Floating datum

Apply only the short-wavelength part of total statics before velocity analysis.

$$\Delta t_\text{floating} = \Delta t_\text{total} - \Delta t_\text{smoothed}$$

After floating-datum correction:
- events are hyperbolic,
- $t_0$ values are near true,
- velocity analysis is unbiased,
- long-wavelength shift is applied later as a final static to the flat client datum.

The same shot or receiver location can belong to several CMPs, so its residual static depends on the local CMP datum.

**Figure:** `figures/term01_lec04/term01_lec04_floating_datum.png`

Speaker notes:
- Top panel: elevation view with final flat datum, floating datum, and local CMP datum bands.
- Point out that a shared surface point has different statics for different local CMP datums.
- Bottom panel: total static decomposed into long-wavelength (applied later) and floating-datum correction.

---

# Practical computation

A practical floating-datum workflow works directly on the estimated source and receiver static fields:

1. Smooth source and receiver static fields separately.
2. Interpolate smoothed fields to CMP locations and add them → total long-wavelength static per CMP.
3. For each trace in the CMP, subtract half of the long-wavelength static from both the source and receiver statics.
4. Apply the resulting residual corrections.

After this, each CMP sits on a locally flat surface near the recording surface, so reflectors remain hyperbolic and the large $t_0$ shift is avoided. The long-wavelength static is applied as a final static after velocities are stable.

---

# Summary

- Layer replacement handles long-wavelength statics that refraction methods miss.
- Residual statics are estimated from reflection data.
- Cross-correlation gives trace shifts but can cycle skip.
- 4-component model separates source, receiver, offset, and CMP terms.
- Gauss–Seidel solves the large least-squares problem iteratively.
- Long-wavelength statics bias velocity analysis by shifting $t_0$.
- Floating datum applies only short-wavelength statics so velocities are unbiased.

---

# Comprehension questions

1. Why can refraction statics leave long-wavelength residuals?
2. Which 4-component term represents geology, not a static?
3. Why does cycle skipping limit cross-correlation statics?
4. How does a long-wavelength static bias a velocity pick?
5. What problem does a floating datum solve?
