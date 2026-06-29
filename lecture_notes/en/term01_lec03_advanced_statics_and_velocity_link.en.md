---
title: Term 1 Lecture 03 — Advanced Statics and the Link to Velocity Analysis
status: draft
term: 01
lecture: 03
---

# Advanced Statics and the Link to Velocity Analysis

## Learning objectives

By the end of this lecture you should be able to:

- Explain when and why the layer-replacement method is used for long-wavelength statics.
- Describe the workflow of residual statics: pick a reference trace, cross-correlate, solve a surface-consistent decomposition.
- State the 4-component model (source, receiver, offset, CMP) and sketch the Gauss–Seidel solution idea.
- Explain why long-wavelength static shifts bias velocity picks even though the gather remains hyperbolic.
- Define the floating datum and show how to compute corrections from total statics.

## Prerequisites

- Term 1 Lecture 02: NMO, velocity analysis, field statics, refraction statics.
- CMP geometry and stacking.
- Basic linear algebra: systems of equations, iterative solution.

## 1. Layer replacement method for long-wavelength statics

### 1.1 When refraction statics are not enough

Refraction and tomographic statics build a near-surface model from first arrivals. They work well when the near surface is illuminated by diving or head waves, but they can leave unresolved anomalies when:

- the weathering layer is too deep or too complex for first arrivals to sample it,
- karst, dunes, or loose sediments create rapid lateral changes,
- well control is sparse or absent,
- the anomaly is below the depth reached by refraction rays.

The remaining long-wavelength distortions show up on stacked sections as pull-ups or push-downs that follow the near-surface geology rather than the deeper structure.

### 1.2 Core idea

The **layer replacement** (or *layer stripping*) method replaces the real near-surface geology with a simpler velocity model. The goal is to remove the long-wavelength time distortion so that the remaining corrections are short-wavelength and can be handled by residual statics or tomography.

Conceptually, we pick a reference horizon that should be flat or gently dipping, measure how much it is distorted by the overburden, and compute the time shifts that would flatten it.

### 1.3 Typical workflow

1. **Pick a reference horizon** in two-way time on the stacked section or on a preliminary migration.
2. **Run horizontal velocity analysis** along the horizon to estimate $V_\text{nmo}(x,y)$ and $V_\text{int}(x,y)$.
3. **Convert the horizon from time to depth** using the picked velocities.
4. **Smooth the depth surface** and tie it to wells if available.
5. **Convert the smoothed surface back to time**.
6. **Estimate a replacement velocity** for the layer being replaced.
7. **Compute long-wavelength static corrections** from the difference between the original and smoothed time/depth surfaces.
8. **Apply statics and QC** by re-picking the reference horizon.

![Layer replacement workflow](figures/term01_lec03/term01_lec03_layer_replacement.png){width=90%}

**Figure 1.** *Layer replacement workflow. A reference horizon is picked in time, converted to depth, smoothed, and converted back to time. The difference between original and smoothed surfaces gives the long-wavelength static correction.*

### 1.4 What can go wrong

- **Wrong replacement velocity**: the depth-to-time conversion is wrong, so the computed statics are wrong.
- **Over-smoothing**: real structure is removed along with the static.
- **Poor reference horizon**: if the picked horizon is not continuous or is itself faulted, the whole correction is corrupted.
- **Anomaly below the replaced layer**: layer replacement only handles distortions caused by the layer being replaced.

## 2. Residual statics

### 2.1 Why residuals remain

Even after careful field statics and layer replacement, small uncorrected time shifts usually remain. Causes include:

- limitations of the near-surface velocity model,
- short-wavelength heterogeneity (small karst features, loose soil patches),
- picking errors in first arrivals,
- noise.

These remaining shifts are called **residual statics**. They are usually smaller than field statics but can still destroy stacking coherence if not corrected.

### 2.2 Cross-correlation with a reference trace

The simplest residual-statics method works trace by trace:

1. Build a **reference trace** (also called a pilot trace). This is often the stack of the CMP gather itself or a stack of neighbouring CMPs.
2. Cross-correlate each trace of the gather with the reference trace.
3. The lag of the maximum correlation gives an estimate of the time shift for that trace.
4. Apply quality control: reject shifts with low correlation coefficient or large inconsistencies.

![Cross-correlation statics](figures/term01_lec03/term01_lec03_crosscorrelation_statics.png){width=90%}

**Figure 2.** *Residual statics by cross-correlation. Each trace in the CMP gather is correlated with a reference trace. The lag of the correlation peak gives the time shift.*

Cross-correlation works well when shifts are small compared with the wavelet period. When shifts exceed about half a period, the method can **cycle skip**: the correlation peak locks onto the wrong cycle of the wavelet. This is why residual statics are usually applied after an initial NMO correction and after the largest field statics have been removed.

### 2.3 From trace shifts to surface-consistent components

A single measured shift for a trace contains several physical effects:

- a source-side residual static,
- a receiver-side residual static,
- an offset-dependent residual moveout,
- a structural term tied to the CMP location.

The structural term is geology, not a static, so it should not be removed. The other terms are separated by solving a linear system.

## 3. The surface-consistent 4-component model

### 3.1 Decomposition

For a trace with source $i$, receiver $j$, offset class $k$, and CMP $l$, the total residual static is written as (Hatton, Worthington & Makin, Section 5.10):

$$
\Delta t_{ijkl} = s_i + r_j + h_k + c_l + \text{noise},
$$

where

- $s_i$ = source-side residual static,
- $r_j$ = receiver-side residual static,
- $h_k$ = offset-class residual moveout,
- $c_l$ = CMP structural term.

The $c_l$ term represents the true geology at the CMP location. It must be removed before solving for the statics; otherwise the static solution would absorb structure and distort the section.

![4-component model](figures/term01_lec03/term01_lec03_four_component_model.png){width=90%}

**Figure 3.** *Four-component decomposition of a residual time shift. The total shift is the sum of a source static, a receiver static, an offset-dependent residual moveout, and a CMP structural term.*

### 3.2 Design matrix and least-squares problem

If we collect many measured time shifts $\mathbf{d}$ (one per trace), the unknown components $\mathbf{m}$ are related by a design matrix $G$:

$$
\mathbf{d} = G \mathbf{m} + \boldsymbol{\epsilon},
$$

where $\boldsymbol{\epsilon}$ is noise. Each row of $G$ has ones in the columns corresponding to the source, receiver, offset class, and CMP of that trace, and zeros elsewhere.

The least-squares solution minimizes

$$
\Phi(\mathbf{m}) = \| \mathbf{d} - G \mathbf{m} \|^2.
$$

In principle the normal equations are

$$
G^\top G \, \mathbf{m} = G^\top \mathbf{d}.
$$

For a realistic seismic line the matrix $G^\top G$ is enormous and close to singular, so direct inversion is impossible.

### 3.3 Gauss–Seidel iteration

A practical solution is **Gauss–Seidel iteration**: update one component class at a time while holding the others fixed. For example, to update the source statics in iteration $n+1$:

$$
s_i^{(n+1)} = \frac{1}{N_i} \sum_{\text{traces with source } i} \left( d_{ijkl} - r_j^{(n)} - h_k^{(n)} - c_l^{(n)} \right),
$$

where $N_i$ is the number of traces with source $i$. Then update receivers, offset classes, and CMP terms in turn. Each update is just an average over the appropriate traces, which is why Gauss–Seidel is natural here.

Hatton reports that 4–5 sweeps are usually enough for convergence on a typical 2-D seismic profile.

![Gauss–Seidel](figures/term01_lec03/term01_lec03_gauss_seidel.png){width=90%}

**Figure 4.** *Gauss–Seidel iteration for the 4-component model. The algorithm cycles through source, receiver, offset, and CMP classes, updating one class at a time while holding the others fixed.*

### 3.4 Quality control

After solving, check:

- are the estimated source and receiver statics spatially smooth?
- do the offset terms look like a small residual moveout?
- does the stack improve after applying the statics?
- are the CMP terms geologically plausible?

## 4. The link between statics and velocity analysis

### 4.1 Long-wavelength statics bias velocity picks

Long-wavelength statics shift the **whole CMP gather** by a constant time $\Delta t$. The reflection events remain hyperbolic, but with the wrong zero-offset time:

$$
t^2(x) = (t_0 + \Delta t)^2 + \frac{x^2}{V^2}.
$$

Velocity analysis, however, tries to fit the standard hyperbola

$$
t^2(x) = t_0^2 + \frac{x^2}{V_\text{apparent}^2}.
$$

Because the $t_0$ in the model is wrong, the best-fit velocity $V_\text{apparent}$ is also wrong. This is the central problem: a long-wavelength static does **not** destroy hyperbolicity, but it places the hyperbola at the wrong time, which forces a biased velocity pick.

![Statics bias velocity analysis](figures/term01_lec03/term01_lec03_statics_velocity_bias.png){width=90%}

**Figure 5.** *Long-wavelength statics shift the whole CMP gather by a constant time. The events remain hyperbolic, but velocity analysis fits them with a wrong $t_0$ and therefore picks a biased velocity.*

### 4.2 Why we need statics before good velocities

Reliable velocity analysis requires hyperbolic events at the correct $t_0$. If static shifts are present, the events are hyperbolic but at the wrong $t_0$, so the picked velocities are biased. Biased velocities, in turn, prevent a clean NMO correction and make residual statics harder to estimate.

This creates an iterative workflow:

1. Apply initial statics (field + layer replacement).
2. Pick velocities on a floating datum.
3. Apply residual statics with the new velocity.
4. Re-pick velocities.
5. Repeat until convergence.

### 4.3 Floating datum as the solution

The **floating datum** solves the problem by applying only the short-wavelength part of the total statics before velocity analysis. It is defined as a smoothed version of the total static surface:

$$
\Delta t_\text{floating} = \Delta t_\text{total} - \Delta t_\text{smoothed},
$$

where $\Delta t_\text{smoothed}$ is the long-wavelength component. The smoothed part is applied later as a final static to a flat datum.

After floating-datum correction:
- events in each CMP gather are hyperbolic,
- their $t_0$ values are close to the true zero-offset times,
- velocity analysis gives unbiased picks,
- the long-wavelength shift is applied only after velocities are known.

![Floating datum](figures/term01_lec03/term01_lec03_floating_datum.png){width=90%}

**Figure 6.** *Floating datum concept. The total static is split into a long-wavelength part (applied later to a flat datum) and a short-wavelength part (floating-datum correction) that preserves hyperbolic moveout for velocity analysis.*

### 4.4 Practical computation

For each trace:

$$
\Delta t_\text{total} = s_i + r_j + \Delta t_\text{long-wavelength},
$$

where $s_i$ and $r_j$ are the high-frequency source and receiver statics. The long-wavelength component is obtained by spatial smoothing of the total static field. Then:

$$
\Delta t_\text{floating} = s_i + r_j,
$$

and

$$
\Delta t_\text{final} = \Delta t_\text{smoothed}.
$$

The data are processed from the floating datum for NMO, velocity analysis, and residual statics. After the velocity model is stable, the final static $\Delta t_\text{final}$ is applied to move everything to the flat client datum.

## Summary

- Layer replacement handles long-wavelength statics that refraction methods cannot resolve.
- Residual statics are estimated from reflection data after field statics and layer replacement.
- Cross-correlation with a reference trace gives trace shifts but can cycle skip for large shifts.
- The 4-component surface-consistent model separates source, receiver, offset, and CMP contributions.
- Gauss–Seidel iteration solves the large least-squares problem by updating one component class at a time.
- Long-wavelength statics shift whole CMP gathers and bias velocity analysis because the hyperbola is fitted with the wrong $t_0$.
- A floating datum applies only short-wavelength statics so that velocity analysis is unbiased; the long-wavelength part is applied later.

## Comprehension questions

1. Why can refraction statics leave long-wavelength residuals that require layer replacement?
2. In the 4-component model, which component should represent geology rather than a static shift, and why?
3. Why does cycle skipping limit cross-correlation residual statics when shifts are large?
4. How does a long-wavelength static shift on a CMP gather bias a semblance velocity pick?
5. What problem does a floating datum solve, and how is it computed from total statics?

## Further reading

- Hatton, Worthington & Makin (1986), *Seismic Data Processing: Theory and Practice*, Section 5.10 — residual statics as a general linear inverse problem.
- Noble (2020), *What's the Datum?* — client datum, processing datum, floating datum.
- Jones (2012), *Incorporating near-surface velocity anomalies in pre-stack depth migration models* — statics components, floating datum, and velocity-analysis bias.
