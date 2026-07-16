---
title: Term 3 Lecture 02 — Statics and Velocity Modeling
status: draft
term: 03
lecture: 02
---

# Statics and Velocity Modeling

## Learning objectives

By the end of this lecture you should be able to:

- Describe first-break picking as the input to refraction-based near-surface model building.
- Compare single-trace pickers (STA/LTA, threshold, envelope) with multichannel methods and explain why the latter are more robust.
- Sketch the diving-wave tomography workflow: picks, rays, slowness model, residuals, and QC.
- Distinguish short-period statics (restore hyperbolicity) from long-period statics (bias velocities).
- Define effective velocity and marginal effective velocity and explain how statics change them.
- Explain why statics and velocity model compete for the same near-surface time distortions.
- Choose between a flat datum, a floating datum, and a smooth-surface datum for imaging.
- Diagnose inaccurate near-surface velocities from residual non-hyperbolic moveout and structural anomalies.

## Prerequisites

- Term 1 Lecture 03: NMO, velocity analysis, field statics, refraction statics.
- Term 1 Lecture 04: residual statics, surface-consistent decomposition, floating datum, velocity bias from statics.
- Basic integral calculus and linear algebra: line integrals, matrices, least squares.

## 0. Why this lecture matters

After Term 1 we know how to estimate NMO velocities and how to apply field and residual statics. In practice, however, the two problems are coupled. The near-surface model determines the statics, the statics determine the effective velocity, and the effective velocity feeds the migration that produces the image. A mistake in any step leaks into the others.

This lecture is about that coupling. We will go from the raw input to near-surface model building (first-break picking and diving-wave tomography), through the effect of statics on velocity estimation, to the choice of datum for imaging. The main message is: **statics and velocity model are two ways to describe the same near-surface time distortion, and you cannot fully correct the same feature with both.**

## 1. First-break picking and near-surface model building

### 1.1 Recap: near-surface building methods

Near-surface model building methods fall into two families (Law & Trad, 2017; Hill, Chapter 22):

- **Layered refraction methods** (delay-time, Hagedoorn, GRM, GLI) assume discrete refracting horizons and estimate layer thickness and velocity from first-break times. These were covered in Term 1 Lecture 3.
- **Diving-wave tomography** treats the near surface as a continuous grid of slowness (inverse velocity) and uses rays that turn back to the surface in a smooth gradient. This is the focus of the present lecture.
- **Full-waveform inversion (FWI)** uses the full wavefield, not only traveltimes; it is more powerful but also more demanding.

All of them share the same starting point: **first-break picks** (*первые вступления / первые преломлённые волны*).

### 1.2 First-break picking algorithms

A first-break pick is the time at which the first coherent seismic energy arrives on a trace. On land this is usually the direct wave or the head wave from the base of the weathering layer. Manual picking is accurate but impractical for large surveys; automatic picking is standard.

**Single-trace pickers** (*одноканальные алгоритмы*):

- **Amplitude threshold** (*пороговый детектор*): the first time the absolute amplitude exceeds a chosen level. Fast but sensitive to noise spikes and to source-strength variations.
- **STA/LTA** (*short-term average over long-term average*): the ratio of average energy in a short window to average energy in a long window jumps when the signal arrives. More robust than a simple threshold because it adapts to the local noise level.
- **Envelope / instantaneous amplitude** (*огибающая*): the analytic-signal envelope rises smoothly at the onset. It is less sensitive to phase and side lobes than the raw trace.
- **Entropy, fractal dimension, or variogram** attributes: these measure the statistical character of the trace and detect the transition from noise to signal.

Figure 1 shows the three most common attributes on a noisy trace.

![First-break picking algorithms](figures/term03_lec02/term03_lec02_first_break_picking.png){width=90%}

**Figure 1.** *First-break picking attributes on a single trace. Top: raw trace with true first break. Middle: STA/LTA ratio. Bottom: trace envelope. The pick is the time where the attribute rises above a threshold or reaches a maximum gradient.*

### 1.3 Why single-trace pickers are not enough

Single-trace pickers have two weaknesses:

1. They ignore spatial consistency. A noise spike on one trace can be mis-picked as a first break, while a weak but genuine first break may be missed.
2. They cannot tell whether a late or early pick is physically plausible. The moveout of first breaks across a gather is approximately linear (or hyperbolic for diving waves), so a pick far from the expected moveout is likely wrong.

**Multichannel picking** (*многоканальное пикирование*) solves this by using the whole shot gather or receiver gather at once. A common workflow is (Sabbione & Velis, 2010; FBPicking):

1. Make an initial trace-by-trace pick.
2. Fit a refraction line or a smooth moveout to the picks.
3. Reject statistical outliers and re-pick traces inside a tolerance window around the fitted moveout.
4. Refit with a narrower window and repeat until the picks are stable.
5. Mark traces that still cannot be matched as bad or dead.

Multichannel methods are generally preferable because they use the physical model of the first arrival rather than treating each trace in isolation.

![Multichannel picking](figures/term03_lec02/term03_lec02_multichannel_picking.png){width=90%}

**Figure 2.** *Multichannel picking. Left: single-trace picks (red crosses) include outliers. Right: after fitting a smooth moveout and re-picking within a tolerance window, the picks are spatially consistent.*

### 1.4 Diving-wave tomography: the big picture

Diving-wave tomography (*томография по ныряющим волнам*), also called turning-ray or tomostatics, is the most common modern refraction method. Instead of assuming discrete layers, it models the near surface as a grid of cells with smoothly varying velocity. Rays that leave the source and turn back to the surface are used to constrain the model.

The key physical fact is that, in a velocity that increases continuously with depth, a ray will bend until its ray parameter becomes zero and then return to the surface. The traveltime of that diving ray is an integral of slowness along the curved path.

### 1.5 Governing equations

The ray path is governed by the **Eikonal equation** (*уравнение эйконала*):

$$
\left( \frac{\partial t}{\partial x} \right)^2 + \left( \frac{\partial t}{\partial z} \right)^2 = s^2(x,z),
$$

where $t(x,z)$ is the traveltime field and $s(x,z)=1/v(x,z)$ is the slowness. The equation says that the gradient of traveltime is the local slowness vector. It is the high-frequency approximation of the wave equation and is the basis for most traveltime tomography.

For a single diving ray, the observed first-break time is the line integral of slowness along the ray:

$$
t = \int_\text{ray} s(l)\, dl .
$$

If we perturb the slowness model by a small amount $\delta s(x,z)$, the traveltime changes by approximately

$$
\delta t \approx \int_\text{ray} \delta s(l)\, dl .
$$

This is the linearization that makes tomography practical: the relation between model perturbations and traveltime residuals is approximately linear.

### 1.6 Linearized tomographic system

Divide the near-surface model into cells. For each ray $i$ and each cell $j$, let $L_{ij}$ be the length of ray $i$ inside cell $j$. Then the traveltime residual $\delta t_i$ for ray $i$ is

$$
\delta t_i = \sum_j L_{ij}\, \delta s_j .
$$

Collecting all rays and cells gives a matrix equation:

$$
\delta \mathbf{t} = L \, \delta \mathbf{s} .
$$

Here $L$ is the **ray-path length matrix** (*матрица длин лучей*), $\delta \mathbf{t}$ is the vector of observed minus predicted traveltimes, and $\delta \mathbf{s}$ is the vector of unknown slowness perturbations. This is the linearized tomographic system; a detailed derivation is given in `lecture_notes/derivations/tomographic_system_derivation.en.md`.

Because the problem is usually underdetermined and ill-posed, we solve it with regularized least squares:

$$
\min_{\delta \mathbf{s}} \left\| \delta \mathbf{t} - L\, \delta \mathbf{s} \right\|^2 + \lambda \left\| D \, \delta \mathbf{s} \right\|^2,
$$

where the second term penalizes rough models (e.g., a Laplacian smoothness operator $D$) and $\lambda$ controls the trade-off between fitting data and model simplicity.

### 1.7 Iterative workflow

Diving-wave tomography is almost always iterative:

1. **Start model**: a smooth 1-D velocity increasing with depth, or a layered refraction result.
2. **Trace rays** or solve the Eikonal equation from every source to every receiver.
3. **Compute residuals** $\delta \mathbf{t} = \mathbf{t}_\text{observed} - \mathbf{t}_\text{predicted}$.
4. **Solve** the regularized linear system for $\delta \mathbf{s}$.
5. **Update** the model: $s_\text{new} = s_\text{old} + \delta s$.
6. **Repeat** until residuals stop improving.

### 1.8 Quality metrics

A tomographic model must be checked with several independent measures (Hill, Chapter 22; Law & Trad, 2017):

- **Data residual**: the RMS difference between observed and predicted first-break times. A residual of 20–30 ms is often acceptable for statics; lower is better.
- **Ray coverage**: parts of the model with few rays are poorly constrained. Coverage maps show where the model is reliable.
- **Checkerboard test**: add a known pattern to the model, compute synthetic traveltimes, invert, and check whether the pattern is recovered. If not, the model is too smooth or the ray coverage is inadequate.
- **Geological plausibility**: velocities should increase smoothly with depth and match uphole information where available.
- **Stack response**: the final test is whether the model produces good statics — flat gathers, coherent stacks, and geologically reasonable structure.

![Diving-wave tomography](figures/term03_lec02/term03_lec02_diving_wave_tomography.png){width=90%}

**Figure 3.** *Diving-wave tomography. Left: a smooth starting model with diving rays turning back to the surface. Right: the updated tomographic model after several iterations. Darker cells have better ray coverage; light cells are poorly constrained.*

## 2. Statics and velocity estimation

### 2.1 Recap: short-period vs. long-period statics

In Term 1 Lecture 4 we divided statics by wavelength:

- **Short-period (high-frequency) statics** (*короткопериодная статика*) vary rapidly from source to source or receiver to receiver. They destroy the hyperbolicity of reflections on a CMP gather because each trace has a different time shift. Residual statics methods are designed to remove them.
- **Long-period (low-frequency) statics** (*длиннопериодная статика*) vary slowly across the survey. They leave the reflection events hyperbolic but shift the whole gather in time, which biases the velocity picked by velocity analysis.

This distinction is central to the rest of the lecture.

### 2.2 Effective velocity

**Effective velocity** (*эффективная скорость*), also called stacking or NMO velocity in this context, is the velocity that best flattens the reflection moveout on a CMP gather after statics have been applied. It is not the same as interval velocity; it is an empirical fit to the traveltime curve.

Mathematically, for a finite offset range $0 \le x \le x_\text{max}$ the effective velocity is the $V$ that minimizes

$$
\Phi(V) = \sum_{x} \left[ t(x) - \sqrt{t_0^2 + x^2/V^2} \right]^2 .
$$

The best-fit hyperbola depends on the maximum offset used. If you change $x_\text{max}$, you change the part of the traveltime curve that is fit, and the effective velocity can change even though the true geology has not.

![Effective velocity](figures/term03_lec02/term03_lec02_effective_velocity.png){width=90%}

**Figure 4.** *Effective velocity. The red traveltime curve is non-hyperbolic. The blue and green hyperbolae are the best fits for two different offset ranges. Each fit gives a different effective velocity.*

### 2.3 Marginal effective velocity

The **marginal effective velocity** (*предельная эффективная скорость*) is the limit of the effective velocity as the offset range shrinks to zero. It is the slope of the $t^2$ vs. $x^2$ curve at the origin:

$$
V_\text{marg}^2 = \left. \frac{dx^2}{d(t^2)} \right|_{x \to 0} .
$$

For a purely hyperbolic event this is exactly the NMO velocity. For a real event with non-hyperbolic moveout (e.g., from anisotropy or from a complex near surface), the marginal effective velocity is the local slope at zero offset. It is the velocity that would be measured with very short offsets and is often the target of velocity analysis near the well location.

![Marginal effective velocity](figures/term03_lec02/term03_lec02_marginal_effective_velocity.png){width=90%}

**Figure 5.** *Marginal effective velocity. The red curve is the true $t^2(x^2)$. The marginal effective velocity is the slope of the straight-line tangent at the origin (blue). A fit over a finite offset range (green) gives a different effective velocity.*

### 2.4 How statics change effective velocities

A constant static shift $\Delta t$ changes the zero-offset time from $t_0$ to $t_0+\Delta t$ but leaves the moveout curvature unchanged. The traveltime becomes

$$
t^2(x) = (t_0 + \Delta t)^2 + \frac{x^2}{V^2} .
$$

When velocity analysis fits the same curvature to a hyperbola, it implicitly uses the wrong $t_0$. The result is a biased velocity. For a shallow horizon with small $t_0$ the bias is large; for a deep horizon the same static shift matters less.

If the static varies spatially, the bias is not uniform. A low-velocity channel under part of the line creates a long-wavelength static that correlates with the CMP position. The effective velocity will then vary along the line in a way that tracks the near surface, not the deeper geology (Sysoev, 2011, Chapter 4; Davletkhanov).

A more detailed relationship is given by Sysoev (Chapter 4). If a long-wavelength static correction $c(x)$ has been under- or over-applied, the apparent zero-offset time and the apparent velocity of a reflector below the anomaly become

$$
t_{0,3}(x) = t_0(x) + 2c(x),
$$

$$
V_3^2(x) = \frac{1}{\left[ t_0(x) + 2c(x) \right] \left[ \frac{1}{t_0(x)V^2(x)} + \frac{c''(x)}{2} \right]} .
$$

The second derivative $c''(x)$ means that the curvature of the static field, not just its magnitude, controls the velocity bias. A gently sloping static shifts $t_0$ but barely changes $V$; a rapidly curved static also distorts the apparent velocity.

![Statics bias on velocity spectrum](figures/term03_lec02/term03_lec02_statics_velocity_bias.png){width=90%}

**Figure 6.** *Effect of long-wavelength statics on a velocity spectrum. Left: correct velocity spectrum with a single peak at $V_\text{nmo}$. Right: after a long-wavelength static shift, the peak moves to a different velocity because $t_0$ has changed while the curvature has not.*

### 2.5 Datum choice and velocity estimation

Velocity analysis is usually performed from a **floating datum** (*плавающий уровень*) or a **smooth-surface datum** (*гладкая поверхность*). A flat datum far above the surface would require large static corrections and would distort the effective velocities. A floating datum stays close to the smoothed topography and keeps the moveout approximately hyperbolic.

However, a CMP floating datum applies different total statics to different traces in the same CMP: each trace is shifted by the source and receiver statics that bring it to the local CMP datum. This is no longer strictly surface-consistent. The effective velocity measured from a floating datum is therefore affected by the local topography in a way that is hard to remove later. We will return to this point when we discuss imaging.

## 3. Statics and imaging

### 3.1 Statics vs. imaging: the vertical-ray assumption

Static corrections are based on a crucial assumption: **the near-surface traveltime is independent of offset and can be represented by a source-side plus a receiver-side time shift.** This is equivalent to assuming vertical raypaths through the near surface.

The assumption is reasonable because the strong velocity contrast at the base of the weathering layer bends rays toward the vertical inside the low-velocity layer. It is also approximate: for large offsets or strong lateral velocity gradients the near-surface path is not vertical, and a single time shift cannot describe it.

Imaging, by contrast, uses true ray tracing or wave-equation propagation. It does not assume vertical rays; it accounts for the actual refraction at layer boundaries. This means that statics and imaging are two different physical approximations of the same near-surface time distortion.

### 3.2 The fundamental trade-off

If a near-surface feature is corrected by statics, it is **removed from the data** as a trace-constant shift. A subsequent migration velocity analysis cannot recover it because it is no longer present in the traveltimes. Conversely, if a feature is left in the data so that the migration velocity model can account for it, then statics should not remove it.

The practical rule is:

- **Short-wavelength, surface-consistent features** (source and receiver statics) are best handled by statics because they are not resolvable by the deeper velocity model.
- **Long-wavelength, kinematic features** (smooth elevation, gradual weathering changes) can be handled by either statics or the velocity model, but not both. The choice depends on the imaging workflow.

For a good final image, the near-surface velocity model must be accurate enough that the migration can focus the reflections. Statics alone cannot achieve this if the rays are significantly non-vertical (Jones, 2012; Hill, Chapter 22).

### 3.3 Datum choices for imaging

Three datums are commonly used for migration:

- **Flat datum** (*плоский уровень*) far above the highest topography. Requires large replacement statics; may distort velocities if the replacement velocity is wrong.
- **Floating datum** (*плавающий уровень*) close to the smoothed topography. Keeps NMO hyperbolic but breaks surface consistency because each trace in a CMP has a different total static.
- **Smooth-surface datum** (*гладкая поверхность*) with surface-consistent corrections. Sources and receivers are moved to a smooth reference surface while preserving the source and receiver statics. This is the preferred modern approach for prestack depth migration.

![Datum choice](figures/term03_lec02/term03_lec02_datum_choice.png){width=90%}

**Figure 7.** *Datum choices. Left: flat datum requires large static shifts and may distort velocities. Middle: floating datum keeps moveout hyperbolic but breaks surface consistency. Right: smooth surface datum preserves surface-consistent source/receiver statics while giving a smooth reference for migration.*

### 3.4 Why surface consistency matters at the smooth surface

A surface-consistent static is the sum of a source contribution and a receiver contribution. If we move the data to a smooth surface while keeping these contributions separate, the physical meaning of the correction is preserved: each source and each receiver has a single time shift.

A CMP floating datum, by contrast, computes the total static for each trace as the sum of the source and receiver shifts at the actual source and receiver positions, then interpolates to a smooth CMP datum. The result is trace-dependent: two traces in the same CMP can have different source and receiver combinations, so their total statics differ. This is not surface-consistent and can cause subtle imaging artifacts.

The recommended workflow for complex near surface is therefore:

1. Build a detailed near-surface velocity model from first-break tomography.
2. Move sources and receivers to a smooth surface using the tomographic model and surface-consistent statics.
3. Estimate the deeper migration velocity model from the redatumed data.
4. Migrate from the smooth surface.

## 4. Effects of inaccurate near-surface velocity model

### 4.1 Offset-dependent errors

An inaccurate near-surface velocity model affects different offsets differently. Near-offset traces are mostly sensitive to the vertical traveltime through the near surface; far-offset traces are also sensitive to the lateral velocity gradient because their raypaths are longer and more oblique.

This means that a wrong near-surface model will leave **residual non-hyperbolic moveout** after NMO correction. The near offsets may be flat while the far offsets still curve, or vice versa. The residual moveout is not a simple function of offset squared, so it cannot be removed by a single NMO velocity.

### 4.2 Structural anomalies

A near-surface error that is not correctly represented in the velocity model will be mapped into the image as a false structural anomaly. For example, a low-velocity pocket in the weathering layer delays the reflections below it. If the velocity model does not know about this pocket, the migrated image will show a **pull-down** (*провал*); if the model overestimates the delay, it will show a **push-up** (*всплеск*).

These anomalies follow the near-surface pattern, not the deeper geology. They are often visible as long-wavelength undulations on horizontal slices that correlate with topography or weathering thickness.

![Near-surface velocity error](figures/term03_lec02/term03_lec02_near_surface_velocity_error.png){width=90%}

**Figure 8.** *Inaccurate near-surface velocity model. Left: a low-velocity pocket in the weathering layer. Center: the NMO-corrected gather has residual non-hyperbolic moveout. Right: the migrated section shows a false structural pull-down below the pocket.*

### 4.3 Migration defocusing

If the near-surface velocity is wrong, the migration operator does not focus reflections correctly. The error is largest where the near-surface velocity changes rapidly and where the offset range is wide. Prestack depth migration with a detailed near-surface model is the most robust way to avoid this, but it requires that the model be accurate.

A practical QC is to compare common-offset or angle gathers after migration. If the near-surface model is correct, all offsets should be flat. If the model is wrong, residual moveout appears on the far offsets first.

### 4.4 Interaction with residual statics

Residual statics and near-surface velocity errors can look similar on a CMP gather: both produce misalignment. The difference is that residual statics are usually short-wavelength and surface-consistent, while near-surface velocity errors are long-wavelength and offset-dependent. The diagnostic workflow is:

1. Apply the best available near-surface model and statics.
2. Check for residual NMO on gathers. If the moveout is hyperbolic, a residual velocity or static shift is likely. If it is non-hyperbolic, the near-surface model is probably wrong.
3. Check maps of source and receiver residual statics. If they are geologically plausible (same sign in nearby locations), the statics solution is reasonable.
4. Update the near-surface model or the migration velocity model and iterate.

## 5. Summary

- First-break picking is the input to all refraction-based near-surface methods. Multichannel picking is more robust than single-trace pickers because it enforces spatial consistency.
- Diving-wave tomography uses the Eikonal equation and a linearized ray-path system to estimate a smooth near-surface velocity model. QC requires data residuals, ray coverage, and checkerboard tests.
- Short-period statics restore hyperbolicity; long-period statics bias effective velocities because they change $t_0$ while leaving curvature unchanged.
- Effective velocity is the best-fit hyperbola for a finite offset range; marginal effective velocity is the zero-offset slope of the $t^2(x^2)$ curve.
- Statics and imaging are two physical approximations of the same near-surface distortion. What statics removes is unavailable to the velocity model, and vice versa.
- For migration, a smooth-surface datum with surface-consistent corrections is preferable to a CMP floating datum because it preserves the physical meaning of source and receiver statics.
- Inaccurate near-surface velocities produce offset-dependent residual moveout, false structural anomalies, and migration defocusing.

## Suggested reading and sources

- Law & Trad (2017) — comparison of refraction inversion methods; `wiki/sources/law_trad_comparison_of_refraction_inversion_methods.md`.
- Davletkhanov — near-surface model and velocity estimation; `wiki/sources/davletkhanov_nsm_and_velocity.md`.
- Sabbione & Velis (2010) / FBPicking — first-break picking algorithms; `wiki/sources/fbpicking.md`.
- Hill (Chapter 22) — statics and their effects on stacking velocities and imaging; `wiki/sources/hill_introduction_to_seismic_processing_ch22.md`.
- Sysoev (2011, Chapters 4–5) — effective velocity and compensation of variable topography; `wiki/sources/sysoev_statics.md`.
- Jones (2012) — near-surface anomalies in prestack depth migration; `wiki/sources/jones_2012_incorporating_near_surface_velocity_anomalies.md`.
- Noble (2020) — datums and replacement velocity; `wiki/sources/noble_2020_whats_the_datum.md`.
- Velocity artefacts — near-surface velocity errors and structural artifacts; `wiki/sources/velocity_artefacts.md`.
- Tomographic system derivation: `lecture_notes/derivations/tomographic_system_derivation.en.md`.
