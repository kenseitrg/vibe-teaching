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

Almost every residual-statics method follows the same three-step workflow (Li, 1999, Chapter 2):

1. **Form reference traces** that are as free as possible of near-surface traveltime errors.
2. **Estimate time shifts** between each trace and its reference by cross-correlation.
3. **Decompose** the estimated shifts into surface-consistent source and receiver statics.

The following sections examine each step and the practical issues that arise.

### 2.1 Why residuals remain

Even after careful field statics and layer replacement, small uncorrected time shifts usually remain. Causes include:

- limitations of the near-surface velocity model,
- short-wavelength heterogeneity (small karst features, loose soil patches),
- picking errors in first arrivals,
- noise.

These remaining shifts are called **residual statics**. They are usually smaller than field statics but can still destroy stacking coherence if not corrected.

### 2.2 Cross-correlation with a reference trace

The simplest residual-statics method works trace by trace:

1. Build a **reference trace** (also called a pilot trace). This is often the stack of the CMP gather itself or a stack of neighbouring CMPs. External references formed from stacked or filtered data are common; internal references selected from the same gather are also possible.
2. Cross-correlate each trace of the gather with the reference trace.
3. The lag of the maximum correlation gives an estimate of the time shift for that trace.
4. Apply quality control: reject shifts with low correlation coefficient or large inconsistencies.

![Cross-correlation statics](figures/term01_lec03/term01_lec03_crosscorrelation_statics.png){width=90%}

**Figure 2.** *Residual statics by cross-correlation. Each trace in the CMP gather is correlated with a reference trace. The lag of the correlation peak gives the time shift.*

Cross-correlation works well when shifts are small compared with the wavelet period. When shifts exceed about half a period, the method can **cycle skip**: the correlation peak locks onto the wrong cycle of the wavelet. This is why residual statics are usually applied after an initial NMO correction and after the largest field statics have been removed.

### 2.2.1 Correlation domains

Cross-correlation can be performed in different data domains, and each domain isolates different combinations of static and dynamic effects. The following table (after Li, 1999, Table 2-1) summarizes which factors contribute to the traveltime difference between two traces in each domain:

| Domain | Dip | Velocity | Source static | Receiver static |
|--------|-----|----------|---------------|-----------------|
| Common receiver | yes | yes | yes | no |
| Common source | yes | yes | no | yes |
| Common offset | yes | no | yes | yes |
| Common midpoint | no | yes | yes | yes |

In a common-receiver gather, the receiver static is shared by both traces and cancels out, so the remaining traveltime difference is dominated by the source static (plus dip and velocity effects). In a common-source gather, the source static cancels and the receiver static can be isolated. In a CMP or common-offset gather, both source and receiver statics appear together and must be separated by surface-consistent decomposition. Dip and velocity effects are usually long-wavelength, while source and receiver statics are the short-wavelength signal we want to estimate.

### 2.3 Wiggins et al. surface-consistent model

A more robust approach models the total traveltime of a trace as the sum of surface-consistent components:

$$
T_{ij} = S_i + R_j + G_k + M_k X_{ij}^2,
$$

where

- $S_i$ = source static,
- $R_j$ = receiver static,
- $G_k$ = structure term at CMP $k$,
- $M_k X_{ij}^2$ = residual normal-moveout term,
- $X_{ij}$ = offset of the trace from source $i$ to receiver $j$.

The surface-consistent form follows from the physics of the near surface. A sharp velocity contrast at the base of the weathering layer forces rays from many subsurface reflection points to become nearly vertical as they pass through the low-velocity near surface. Because the rays are almost vertical, the traveltime spent in the near surface is essentially the same for any ray that enters or leaves the surface at a given location. The source-side contribution therefore depends only on the source location $i$, and the receiver-side contribution depends only on the receiver location $j$.

The residual shift $\delta T_{ij}$ is measured by cross-correlation against a **pilot trace** (a reference trace, usually a stack of adjacent CMPs). The measured shifts for all traces form an overdetermined linear system

$$
A \mathbf{p} = \mathbf{f},
$$

which is solved iteratively because $A$ is large and sparse.

A fundamental result from Wiggins, Larner & Wisecup (1976) is that the linear system can **only resolve statics trends whose spatial wavelength is shorter than about a spread length**. Longer-wavelength trends will leak into the source, receiver, and structure solutions unless they are constrained. For this reason residual statics are usually forced to zero mean; the long-wavelength component is handled by field statics, layer replacement, or a floating datum.

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

### 3.2.1 Overdetermined and under-constrained

The surface-consistent system has two seemingly contradictory properties (Li, 1999, Chapter 2):

- **Overdetermined.** There are far more traces than unknowns. For example, with $N_s$ sources and $N_r$ receivers there are $N_s \times N_r$ traces but only $N_s + N_r$ source and receiver statics. This redundancy makes the least-squares solution statistically robust.
- **Under-constrained.** The solution is not unique. If we add a constant $c$ to every source static and subtract the same constant $c$ from every receiver static, every trace equation $s_i + r_j$ is unchanged. The same kind of ambiguity applies to long-wavelength trends: a smooth source trend can be traded for a smooth receiver trend without changing the fit. This is why residual statics are forced to zero mean and why the long-wavelength component is handled separately by field statics, layer replacement, or a floating datum.

### 3.3 Gauss–Seidel iteration

A practical solution is **Gauss–Seidel iteration**: update one component class at a time while holding the others fixed. For example, to update the source statics in iteration $n+1$:

$$
s_i^{(n+1)} = \frac{1}{N_i} \sum_{\text{traces with source } i} \left( d_{ijkl} - r_j^{(n)} - h_k^{(n)} - c_l^{(n)} \right),
$$

where $N_i$ is the number of traces with source $i$. Then update receivers, offset classes, and CMP terms in turn. Each update is just an average over the appropriate traces, which is why Gauss–Seidel is natural here.

Hatton reports that 4–5 sweeps are usually enough for convergence on a typical 2-D seismic profile. The step-by-step construction of the design matrix and the full Gauss–Seidel sweep are derived in `lecture_notes/derivations/gauss_seidel_residual_statics_derivation.en.md`. The result is order-dependent because the model is underdetermined for very long wavelengths, so constraints such as zero mean are applied before the Gauss–Seidel sweeps begin.

### 3.4 Quality control

After solving, check:

- are the estimated source and receiver statics geophysically consistent? In nearby spatial locations they should have the same sign (both positive or both negative). The exception is a buried source, where the source and receiver statics may legitimately have different signs.
- do the offset terms look like a small residual moveout?
- does the stack improve after applying the statics?
- are the CMP terms geologically plausible?

Several practical controls strongly affect the residual-statics solution:

- **Correlation window.** The window should be long enough to capture a package of strong, continuous reflectors, but short enough to avoid shallow, structurally complex intervals and low-frequency, ringy data that can cause cycle skipping. It should also avoid first arrivals (so it cannot start too shallow) and avoid multiples (so it cannot extend too deep). After NMO correction, the shallow part of a trace is usually stretched and distorted, so it is also a poor choice for the correlation window. A window following a package of strong, continuous reflectors is often best.
- **Correlation length.** The maximum number of lags computed on the trace-to-trace cross-correlations must be large enough to span the expected sum of source, receiver, structure, and residual-NMO shifts. Too small a length causes a poor solution; too large increases cost and cycle skipping.
- **Pilot traces.** Traces are correlated against a pilot trace rather than against every other trace. The pilot is usually the best current stack of adjacent CMPs. Better pilots improve the solution but can also bias it toward the pilot, so external pilot traces are sometimes used.
- **Data preparation.** Data are often bandpass filtered, AGC'd, or F–K filtered to build the statics solution, but the computed shifts are applied to the unfiltered data.
- **Application order.** Because statics are computed from moveout-corrected data, they are most properly applied after NMO. Sometimes they are applied before NMO to improve velocity analysis or for prestack migration.

## 4. The link between statics and velocity analysis

### 4.1 Long-wavelength statics bias velocity picks

![Long-wavelength statics and velocity bias](figures/term01_lec03/term01_lec03_velocity_and_statics.png){width=90%}

**Figure 4.** *Long-wavelength statics and velocity bias. Top: topography, floating datum, locally constant datum, and constant datum with ray paths to a reflecting boundary. Bottom: recorded CMP traveltime curve, traveltime curve computed from a floating datum, and traveltime curve computed from a constant datum. A long-wavelength static shifts the whole gather, changing $t_0$ without changing the curvature, which biases velocity analysis.*

Long-wavelength statics shift the **whole CMP gather** by a constant time $\Delta t$. The reflection event now has a different zero-offset time, $t_0 + \Delta t$, but its curvature — the term proportional to $x^2$ — remains the same. Because the curvature is unchanged while $t_0$ is wrong, velocity analysis fits the same curvature to a hyperbola with an incorrect zero-offset time, and the best-fit velocity $V_\text{apparent}$ is forced away from the true velocity. This is the root cause of the velocity bias.

Mathematically, the shifted gather follows

$$
t^2(x) = (t_0 + \Delta t)^2 + \frac{x^2}{V^2},
$$

while velocity analysis tries to fit the standard hyperbola

$$
t^2(x) = t_0^2 + \frac{x^2}{V_\text{apparent}^2}.
$$

Because the $t_0$ in the model is wrong, the best-fit velocity $V_\text{apparent}$ is also wrong. This is the central problem: a long-wavelength static does **not** destroy hyperbolicity, but it places the hyperbola at the wrong time, which forces a biased velocity pick.

![Statics bias velocity analysis](figures/term01_lec03/term01_lec03_statics_velocity_bias.png){width=90%}

**Figure 5.** *Long-wavelength statics shift the whole CMP gather uniformly, so the event remains hyperbolic with the correct NMO velocity but a wrong $t_0$. If velocity picking is tied to the original $t_0$ (horizon-consistent or fixed-time picking), the best-fit velocity at that constrained $t_0$ is biased. (a) CMP gather: true hyperbola ($t_0=0.40$ s, $V=2000$ m/s) and static-shifted hyperbola ($t_0=0.55$ s, same $V$). (b) Semblance spectra: the shifted peak has the correct velocity but wrong $t_0$; the biased pick at the original $t_0$ gives $V_\text{apparent}=1867$ m/s. (c) In the $t^2$–$x^2$ domain the true and shifted data have the same slope (same velocity), while a fit forced through the original $t_0^2$ has a steeper slope — the velocity bias.*

### 4.2 Why we need statics before good velocities

Reliable velocity analysis requires hyperbolic events at the correct $t_0$. If static shifts are present, the events are hyperbolic but at the wrong $t_0$, so the picked velocities are biased. Biased velocities, in turn, prevent a clean NMO correction and make residual statics harder to estimate.

This is a **chicken-and-egg problem**: velocity analysis requires statics corrections first, but residual statics work best when residual NMO is already minimal. The practical workflow is therefore iterative:

1. Apply initial statics (field + layer replacement).
2. Pick velocities on a floating datum.
3. Apply residual statics with the new velocity.
4. Re-pick velocities.
5. Repeat until convergence.

During this iteration, **large bulk (long-wavelength) shifts should be kept out of the data**. A common practice is to remove the mean from the statics solution and save it to be applied as the final shift to the interpretation datum. This keeps NMO, residual statics, and velocity analysis from being biased by a bulk time shift.

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

In practice, the datum should be a smoothed version of the topography and the replacement velocity should be an average near-surface velocity. Keeping the bulk static small during processing protects the velocity model; the final shift to the flat client datum is applied only after the velocities are stable.

![Floating datum](figures/term01_lec03/term01_lec03_floating_datum.png){width=90%}

**Figure 6.** *Floating datum concept. (a) Depth domain: the rugged surface is reduced to a smoothed floating datum, while each CMP is processed on a short, locally flat datum near the recording surface. A single shot or receiver location can belong to several CMPs and therefore carries a different static correction for each local datum. (b) Statics decomposition: the total static is split into a long-wavelength part (applied later to the final flat datum) and a short-wavelength part (floating-datum correction) that preserves hyperbolic moveout for velocity analysis.*

### 4.4 Practical computation

A practical floating-datum workflow works directly on the estimated source and receiver static fields:

1. **Smooth the source and receiver static fields** separately to obtain their long-wavelength components, $S_i^\text{LW}$ and $R_j^\text{LW}$.

2. **Interpolate the smoothed fields to each CMP location** and add them. This gives the total long-wavelength static at CMP $l$:
   $$
   \Delta t_\text{long-wavelength}(l) = S^\text{LW}(x_l) + R^\text{LW}(x_l),
   $$
   where $x_l$ is the CMP location.

3. **For each trace in CMP $l$, subtract half of this long-wavelength component from both the source and receiver statics**:
   $$
   s_i^\text{res}(l) = s_i - \frac{1}{2}\Delta t_\text{long-wavelength}(l),
   $$
   $$
   r_j^\text{res}(l) = r_j - \frac{1}{2}\Delta t_\text{long-wavelength}(l).
   $$
   The residual source and receiver statics are now tied to each CMP, so a given physical source or receiver may carry different values for different CMP gathers.

4. **Apply the resulting residual corrections** to the traces.

After this step, each CMP gather is placed on a locally flat surface close to the recording surface. Reflectors inside a gather can still be treated as hyperbolic, but the large $t_0$ shift associated with the long-wavelength static has been removed. This protects velocity analysis from a bulk time shift and keeps the NMO hyperbola close to its true zero-offset time. The data are then processed from this floating datum for NMO, velocity analysis, and residual statics. After the velocity model is stable, the full long-wavelength static $\Delta t_\text{long-wavelength}$ is applied as a final static to move the data to the flat client datum.

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
