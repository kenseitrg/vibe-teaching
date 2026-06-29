# Slide outline — Term 1 Lecture 03
## Advanced Statics and the Link to Velocity Analysis

---

# Title

**Advanced Statics and the Link to Velocity Analysis**

Term 1, Lecture 03

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

**Figure:** `figures/term01_lec03/term01_lec03_layer_replacement.png`

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

**Figure:** `figures/term01_lec03/term01_lec03_crosscorrelation_statics.png`

---

# Surface-consistent 4-component model

Total residual static for a trace:

$$\Delta t_{ijkl} = s_i + r_j + h_k + c_l + \text{noise}$$

- $s_i$: source static
- $r_j$: receiver static
- $h_k$: offset-class residual moveout
- $c_l$: CMP structural term (geology)

The $c_l$ term must be removed before solving; otherwise structure is absorbed into statics.

**Figure:** `figures/term01_lec03/term01_lec03_four_component_model.png`

---

# Least-squares formulation

Measured shifts $\mathbf{d}$; unknown components $\mathbf{m}$.

$$\mathbf{d} = G \mathbf{m} + \boldsymbol{\epsilon}$$

Minimize:

$$\Phi(\mathbf{m}) = \| \mathbf{d} - G \mathbf{m} \|^2$$

$G^\top G$ is large and nearly singular — direct inversion is impractical.

---

# Gauss–Seidel solution

Update one component class at a time while holding others fixed.

Example: update source statics

$$s_i^{(n+1)} = \frac{1}{N_i} \sum_{\text{traces with source } i} \left( d_{ijkl} - r_j^{(n)} - h_k^{(n)} - c_l^{(n)} \right)$$

Then receivers, offsets, CMPs. Repeat sweeps until convergence.

Typically 4–5 sweeps.

**Figure:** `figures/term01_lec03/term01_lec03_gauss_seidel.png`

---

# Long-wavelength statics bias velocity analysis

Long-wavelength static shifts the whole CMP gather by $\Delta t$:

$$t^2(x) = (t_0 + \Delta t)^2 + \frac{x^2}{V^2}$$

Velocity analysis fits:

$$t^2(x) = t_0^2 + \frac{x^2}{V_\text{apparent}^2}$$

Wrong $t_0$ forces wrong $V_\text{apparent}$.

**Figure:** `figures/term01_lec03/term01_lec03_statics_velocity_bias.png`

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
- long-wavelength shift is applied later as a final static.

**Figure:** `figures/term01_lec03/term01_lec03_floating_datum.png`

---

# Practical computation

For each trace:

$$\Delta t_\text{total} = s_i + r_j + \Delta t_\text{long-wavelength}$$

Then:

- $\Delta t_\text{floating} = s_i + r_j$ (short wavelength)
- $\Delta t_\text{final} = \Delta t_\text{smoothed}$ (long wavelength)

Process from floating datum for NMO, velocity analysis, residual statics.
Apply final static after velocities are stable.

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
