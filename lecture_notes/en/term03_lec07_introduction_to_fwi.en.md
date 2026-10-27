---
title: Term 3 Lecture 07 — Introduction to Full-Waveform Inversion
status: draft
term: 03
lecture: 07
---

# Introduction to Full-Waveform Inversion

## Learning objectives

By the end of this lecture you should be able to:

- Explain why ray-based model building (stacking analysis, traveltime tomography) has a resolution floor, and state how that floor scales with wavelength and propagation distance (Fresnel zone).
- Describe the idea of full-waveform inversion (FWI): iteratively update a gridded earth model so that synthetic seismograms — computed by solving the wave equation — match the recorded data in phase **and** amplitude.
- Walk through one FWI iteration: forward modelling, residual, gradient, line search, model update — and explain why the gradient is computed by "back-propagating the residual," i.e. with the same machinery as reverse-time migration.
- Explain, with the half-period criterion, why FWI is non-linear, what cycle skipping is, and how to recognize it in the first iterations.
- List the standard work-arounds for non-linearity: frequency continuation (multiscale), time windowing, alternative misfit functions (traveltime, adaptive, optimal transport), extended formulations, and better starting models.
- State the practical advantages of FWI: wavelength-scale resolution, FWI imaging as a byproduct, and the potential for multiparameter estimation ($V_s$, density, anisotropy, $Q$) — with the cross-talk caveat.
- Describe the main modern challenges: computational cost and its steep scaling with frequency, the dependence on low frequencies and a good starting model, land-specific difficulties (topography, near surface, noise, elastic effects), absorption, source-signature and coupling issues, and data quality.
- Judge from data-fit panels and image gathers whether an FWI run is converging correctly.

## Prerequisites

- Term 1 Lecture 04/05: velocity analysis, stacking velocities and their limitations.
- Term 3 Lecture 02: tomography, velocity model building, migrated-image QC.
- Term 1 Lecture 05: frequency, bandwidth, and low-frequency content of seismic data.
- Term 2 Lecture 01: absorption and the quality factor $Q$.
- Helpful (not required): Term 3 Lecture 05 broadband processing — why low frequencies are hard to record.

## 0. Why this lecture matters

Everything this course has built so far — statics, velocities, deconvolution, noise attenuation, regularization — serves two products: an accurate **velocity model** and a focused **image**. The model-building tools we covered (semblance analysis, tomography) are powerful but coarse: they see the subsurface through the smooth lens of traveltimes. Yet the questions that matter at the end of the processing chain — a thin reservoir, a small fault, a gas pocket, the inside of a salt body — are exactly the questions where smooth models give up.

**Full-waveform inversion (FWI)** is the industry's answer to that gap: use the *entire recorded waveform* — every phase, every wiggle, amplitudes included — as data for the velocity model. It is the most ambitious data-fitting scheme in our toolbox, and over the last two decades it has gone from an academic dream to the standard model-building step in marine imaging. It is also a cautionary tale about non-linearity: FWI fails in instructive, predictable ways, and understanding *why* it fails is the best introduction to how it works.

This lecture is deliberately conceptual. We will meet only a handful of equations, and we will lean on figures from the literature: the mechanics (Jones 2019), the classic verification experiment (Pratt 1999), the research landscape (Métivier & Brossier 2026), land case studies (Zhang & Dai 2015; Wang et al. 2020), and FWI imaging examples (Baldock et al. 2023).

## 1. From rays to full wavefields

### 1.1 What our model-building tools actually see

Recall the model-building ladder from Term 3 Lecture 02:

- **Semblance / stacking analysis** sees reflection *moveout*: it recovers a smooth $V_\text{rms}$ trend, with resolution set by gather aperture and bandwidth — at best hundreds of metres of lateral smoothing.
- **Refraction and reflection traveltime tomography** sees *picked times*: it divides the model into cells and rays, and back-projects time errors along ray paths. It can resolve structures, but only down to a size floor set by the physics of rays (next section).

Both are **ray methods**: they assume the wavefront can be represented locally by a plane wave following Snell's law. That assumption is a *high-frequency approximation* — it holds only when the velocity varies gently on the scale of a seismic wavelength.

### 1.2 When rays break down

Here is the thought experiment from Jones (2019). A low-frequency sound wave meets an irregularly shaped boulder whose size is comparable to the wavelength. As the wave passes, *the entire boulder vibrates and re-radiates energy in all directions* — it becomes a secondary source. Trying to apply Snell's law at each point of the corrugated boulder surface is meaningless: the interaction is not refraction but **diffraction (scattering)**.

The rule of thumb:

- Velocity anomaly size $\gg$ wavelength → rays and Snell's law work; traveltime tomography can see it.
- Anomaly size $\lesssim$ wavelength → scattering dominates; only a method that *models the wavefield itself* can describe what happened — and only such a method can invert for it.

### 1.3 The resolution floor of ray tomography

The classical result (Williamson 1991; Pratt et al. 2002): traveltime tomography resolves features no smaller than about the width of the **first Fresnel zone** — the footprint of the finite-frequency wavefront around the geometric ray. For wavelength $\lambda$ and propagation distance $L$:

$$ \text{resolving length} \;\approx\; \sqrt{\lambda L}. $$

Waveform inversion, by contrast, uses the phase and amplitude of the wavetrain and can resolve structures on the order of $\lambda$ — and, when reflections and multiples participate, somewhat below it.

Pratt (1999) demonstrated this on a laboratory **physical scale model**: a crosswell survey shot across an epoxy-resin block with embedded targets (a semi-circular low-velocity channel, a dipping interface, a small fault). Because the "field data" were acquired in a controlled experiment, the true model is known exactly.

![](figures/term03_lec07/term03_lec07_ray_vs_waveform_resolution.png){width=85%}

**Figure 1.** *The resolution gap between ray tomography and waveform inversion, from a controlled crosswell experiment (Pratt 1999, Geophysics; reproduced for teaching). (a) The true velocity model of the epoxy-resin scale block (55 × 120 m at 1:1000 scale): layered velocities 2.3–3.0 km/s, a semicircular low-velocity channel, a dipping interface and a small fault. (b) Curved-ray traveltime tomography from picked first arrivals: the broad layering survives, but the channel is barely a smudge and the fault is invisible. The bars beside the panels mark the dominant wavelength $\lambda$ and the Fresnel-zone width $\sqrt{\lambda L}$ — the intrinsic resolution floor of the ray method.*

Keep the numbers in mind for a moment: in this experiment $\lambda \approx 5$ m and $L \approx 50$ m, so ray tomography cannot see much below $\sqrt{5 \times 50} \approx 15$ m — three times coarser than the wavelength. The same ratio applies at field scale: with $\lambda \approx 50$ m and $L \approx 5$ km, the ray-tomography floor is roughly 500 m, while FWI targets 50 m.

### 1.4 The FWI idea

**Full-waveform inversion** (Lailly 1983; Tarantola 1984) turns model building into a data-fitting problem with full physics:

> Start from an initial earth model. Solve the wave equation numerically to make synthetic shot gathers. Compare them wiggle-for-wiggle with the field data. Compute how the model should change to reduce the mismatch. Update. Repeat.

Everything the modelling physics contains — diving waves, reflections, diffractions, even multiples — participates in the update. Nothing is picked, nothing is windowed into "events" by hand (though we will see that judicious windowing helps convergence). The data are the full seismograms.

Two remarks before we go on:

- **History.** Tarantola's 1984 formulation was, in principle, a recipe for direct physical-property estimation. In practice, 1980s computing could not run it at field scale, and researchers concluded the least-squares waveform problem was "a failure" as a velocity-estimation procedure (Symes & Carazzone 1991). It took ~25 years — better solvers, low-frequency broadband sources, long offsets, and massive computing — to make FWI routine (Plessix 2009; Sirgue et al. 2010; Virieux et al. 2017).
- **Scale.** FWI is not one technique but a family spanning nine orders of magnitude in scale: medical ultrasound, non-destructive testing, near-surface, exploration, crustal and global seismology (Figure 2). The equations barely change; the data, frequencies and geometries do.

![](figures/term03_lec07/term03_lec07_fwi_applications_scales.png){width=95%}

**Figure 2.** *FWI applications across spatial scales (Bohlen, KIT Full Waveform Inversion course, Lecture 4; course material, WS 2021/22). From millimetre (medical imaging) to thousand-kilometre (global seismology) targets, the same idea — match modelled and observed waveforms — is applied to P-waves, P/S waves, and surface waves.*

## 2. Problem formulation and taming non-linearity

### 2.1 The FWI loop

![](figures/term03_lec07/term03_lec07_fwi_workflow.png){width=95%}

**Figure 3.** *The FWI procedure as a loop (Bohlen, KIT FWI course, Lecture 2). The initial model $m_0$ enters forward modelling; the synthetic data are compared with field data through a misfit $E(m)$; the misfit gradient $\partial E/\partial m$ is computed with adjoint (back-propagation) modelling; an optimization step produces the next model $m_{i+1}$. In practice the header of this loop also includes the choices of shots, frequencies, and time windows to invert.*

One iteration, in words:

1. **Forward modelling.** For each source, solve the (two-way) wave equation in the current model $m$ and record synthetics at the receiver positions.
2. **Misfit.** Quantify the mismatch between observed and synthetic data — classically the least-squares norm of the residual.
3. **Gradient.** Compute, for every model cell, the direction in which changing the model decreases the misfit.
4. **Line search.** Decide how far to step along that direction.
5. **Update and repeat** until the data are fit (or the budget runs out).

### 2.2 The objective function and the size of the problem

The classic misfit is the squared residual, summed over shots, traces and time samples:

$$ C(m) \;=\; \sum_\text{shots}\sum_\text{traces}\sum_\text{samples} \left[\, d_\text{obs} - d_\text{cal}[m] \,\right]^2 , $$

where $m$ is the model (a velocity value in *every* grid cell) and $d_\text{cal}[m]$ — the synthetic data — depends on $m$ through the wave-equation solution. The catch is that this dependence is violently **non-linear**: change the velocity in one cell and the entire wavefield downstream — every reflection, every diffraction it generates — changes.

Grasp the size: a 3D model of 1000 km² to 10 km depth at 100 m cells is $10^7$ cells; at 25 m cells, $10^9$. Each may carry several parameters ($V_p$, $V_s$, $\rho$, anisotropy $\varepsilon, \delta$, $Q$). We cannot evaluate $C(m)$ for "all possible models" the way semblance scans a small number of stacking velocities. We can only afford a **local, iterative strategy**: stand at the current model, ask which downhill direction reduces the misfit, take a measured step, and hope the terrain cooperates.

### 2.3 The gradient: back-propagating the residual

The heart of FWI — and the reason it became affordable — is that the gradient $\partial C/\partial m$ can be computed without ever building sensitivity matrices. Following Tarantola (1984):

- Forward-model the **source wavefield** from the source position;
- **Back-propagate the residual** (observed minus modelled data) from the receiver positions — this is exactly what reverse-time migration (RTM) does with the recorded data;
- Correlate the two wavefields in time at every subsurface point.

The result looks like a **migration image of the residual**. This is the single most useful mental model of FWI:

> **FWI = migrate the data residual, interpret the migrated residual as a velocity update.**

![](figures/term03_lec07/term03_lec07_gradient_formation.png){width=80%}

**Figure 4.** *Formation of the gradient (Jones 2019, First Break; reproduced for teaching). Snapshots of the forward-propagated source wavefield (top) and the back-propagated residual (bottom): where and when the two wavefields coincide, their time correlation builds the gradient contribution. For the acoustic velocity parameter the source-side field enters through its second time derivative, scaled by $v^{-3}$. The residual acts as the "adjoint source" of a reverse-time migration.*

Because the gradient is built by a migration engine, single experiments produce migration-like noise — impulse-response arcs — and the useful signal emerges only after summing many shots, just as a migrated image focuses only after summing the survey.

![](figures/term03_lec07/term03_lec07_gradient_impulse_response.png){width=95%}

**Figure 5.** *The gradient as a migration impulse response (Jones 2019, First Break; synthetic data courtesy of Chevron). (a) A residual gather reduced to a single wavelet (offset 5 km, ~3.7 s). (b) Its gradient contribution: an RTM-like impulse response from source (star) to receiver (triangle). (c) The full residual shot gather. (d) Its gradient contribution — a superposition of impulse responses. Only the sum over all shots of the survey focuses into a meaningful update direction.*

The summed gradient decomposes into physically meaningful parts (Figure 6): the **diving-wave "banana"** — the tomographic sensitivity kernel along the refracted path; the **reflection arc** — the migration-like part; and the RTM **cross-talk "rabbit ears"** — non-physical terms that, unlike in imaging, are *useful* here: they reach deeper than the diving wave and help update the model below the penetration depth of refractions.

![](figures/term03_lec07/term03_lec07_gradient_components.png){width=80%}

**Figure 6.** *Components of the FWI gradient (Jones 2019, First Break; courtesy of Chao Wang, ION). (a) Direct/diving-wave "banana" kernel — updates the shallow tomographic velocities; (b) the migration-like reflection arc; (c) cross-talk "rabbit ears" that extend below the diving-wave depth. In production FWI these components are often separated and inverted in sequence: refraction FWI first (shallow, to about one third of maximum offset), reflection FWI after (deeper).*

### 2.4 Which wavenumbers does FWI update?

One question is left hanging by the gradient anatomy: *why* do diving waves update the long-wavelength (tomographic) part of the model and reflections the short-wavelength part? The answer is a single elegant relation. At a scattering point, the model update contains the wavenumber vector that is the **difference of the two slowness vectors** pointing from the scattering point back toward the source and the receiver (Figure 7). Its magnitude is

$$ |k| \;=\; \frac{2 f}{v}\,\cos\frac{\theta}{2}, $$

where $\theta$ is the **illumination angle** between those two directions (Sirgue & Pratt 2004). Now take the two end members:

- **Reflection (back-scattering):** source and receiver both sit above the scattering point — the two directions are nearly *parallel*, $\theta \to 0$, $\cos(\theta/2) \to 1$: the update carries the **maximum wavenumber** $2f/v$ — half the wavelength. Reflections build the short-wavelength, reflectivity-scale part of the model.
- **Diving wave (near-transmission):** the wave passes *through* the point — the two directions are nearly *anti-parallel*, $\theta \to 180°$, $\cos(\theta/2) \to 0$: the update carries only **long wavelengths**. Diving waves build the smooth, tomographic background.

This single picture ties the lecture together: it explains the gradient anatomy of Figure 6, the practice of doing refraction FWI first and reflection FWI after (§2.7), the resolution claims of §1.3 and §3.1, and — with offset controlling $\theta$ — why long offsets are essential for FWI: only they provide near-transmitted illumination that updates the deep background.

![](figures/term03_lec07/term03_lec07_wavenumber_illumination.png){width=95%}

**Figure 7.** *Wavenumber illumination in FWI (after Sirgue & Pratt 2004; Métivier & Brossier 2026). (a) At a scattering point, the update direction is the difference of the slowness vectors toward source and receiver; its magnitude is set by the illumination angle $\theta$. (b) End members: reflections ($\theta \to 0$) inject short wavelengths — reflectivity scale; diving/transmitted waves ($\theta \to 180°$) inject long wavelengths — tomographic scale. Long offsets give near-transmitted ($\theta$ large) illumination, which is why they matter for updating the deep background.*

### 2.5 Local optimization on a complicated surface

Given the gradient, a line search picks the step length; repeated gradient + line-search cycles descend the misfit surface (steepest descent; in practice non-linear conjugate gradients or quasi-Newton schemes such as L-BFGS). Figure 7 visualizes this on a toy two-parameter problem: the misfit valley, the gradient direction at the starting model, the line-search minimum along that direction, and the next iteration.

![](figures/term03_lec07/term03_lec07_cost_function_descent.png){width=95%}

**Figure 8.** *Iterative descent on the misfit surface (Jones 2019, First Break; adapted from Shewchuk 1994). (a) Misfit contours for two model parameters: start (blue), gradient direction (dashed), global minimum (green). (b) Misfit along the gradient direction — the line search finds its minimum (yellow). (c–d) Stepping to the line minimum and recomputing the gradient: repeated orthogonal turns walk down the valley. A real FWI problem is the same picture in $10^7$-dimensional space — with the crucial caveat that the surface is *not* one smooth bowl, as the next figure shows.*

### 2.6 Non-linearity and cycle skipping

Here is the fundamental difficulty. Seismic wavelets oscillate. If the starting model is wrong enough that a modelled event arrives **more than half a period late or early**, then the least-squares residual can be reduced by sliding the modelled wavelet onto the *neighbouring* cycle of the observed wavelet — a wrong model that locally fits "well" (Figure 9). The inversion then converges happily to a **local minimum**: a model with the right data *cycle-skipped*, i.e. systematically wrong by a whole period. This failure mode is **cycle skipping** (Warner et al. 2013).

![](figures/term03_lec07/term03_lec07_cycle_skipping.png){width=80%}

**Figure 9.** *Cycle skipping (Jones 2019, First Break; reproduced for teaching). Top: observed (yellow) and modelled (blue) wavelets for increasing time shifts; the residual grows with the shift. Bottom: the resulting cost function versus time-shift error — oscillatory, with a global minimum at zero shift but local minima near ±1 period. If the starting-model error exceeds half a period (the fourth trace), the descent heads for the wrong valley: the "cycle skip" case. Lower frequencies stretch the period and smooth the cost function — the basis of the multiscale strategy.*

The practical criterion (Pratt 1999; Gauthier et al. 1986):

$$ |\Delta t| \;<\; \frac{T}{2} \;=\; \frac{1}{2 f} , $$

the starting model must predict the data **within half a period** of the dominant frequency being inverted. Numbers make this vivid:

| Dominant frequency | Half period | Required time accuracy |
|--------------------|-------------|------------------------|
| 20 Hz | 25 ms | ~25 ms along the whole ray path |
| 5 Hz | 100 ms | ~100 ms |
| 2 Hz | 250 ms | ~250 ms |

At 20 Hz the starting model must be right to tens of milliseconds over kilometres of path — a demanding, tomography-grade model. At 2 Hz, a crude model suffices. **Low frequencies are forgiving; high frequencies are strict.** This single fact organizes most of the next subsection — and much of FWI practice.

> **Checkpoint 1 (2 minutes — discuss with a neighbour).**
> Your starting model predicts arrival times with an rms error of 60 ms, and the lowest usable signal frequency is 4 Hz. Can you safely start conventional least-squares FWI at 4 Hz? And at 10 Hz?
> *(4 Hz: half period = 125 ms > 60 ms — safe. 10 Hz: half period = 50 ms < 60 ms — cycle-skipping risk; start lower or change the misfit.)*

### 2.7 Work-arounds for non-linearity

The research community has produced a rich toolbox for making FWI survive its own non-linearity (Métivier & Brossier 2026 give the full taxonomy). What follows is the practical short list.

**(a) Frequency continuation (multiscale inversion).** Invert the lowest usable frequencies first, then add higher-frequency batches in a cascade (Bunks et al. 1995; Pratt 1999). Each stage starts from the previous solution — inside the "trust region" of the next higher frequency. The same idea in the field workflow: refraction FWI at 3–8 Hz first, then extend bandwidth while handing the model to reflection FWI. Figures 10 and 11 show both faces of the strategy: the field data fit improving as the inverted band grows, and the classic scale-model result where successive frequency batches sharpen the model until the small fault appears.

![](figures/term03_lec07/term03_lec07_data_fit_evolution.png){width=95%}

**Figure 10.** *Frequency continuation in practice: observed (red) vs. modelled (blue) shot gathers during a shallow-water OBC inversion (Bohlen, KIT FWI course, Lecture 4; after Habelitz 2017). From left to right: iteration 48 with a 2–6 Hz target band, iteration 90 at 2–10 Hz, iteration 160 at 2–23 Hz. The modelled (blue) traces converge onto the observed (red) ones as the inverted bandwidth grows. This data-fit display is the primary FWI QC: if red and blue wiggles match cycle-for-cycle, the model explains the data.*

![](figures/term03_lec07/term03_lec07_fwi_multiscale_resolution.png){width=95%}

**Figure 11.** *Multiscale FWI on the physical scale model (Pratt 1999, Geophysics; reproduced for teaching). (a) True model (as in Figure 1a). (b) Early inversion stage — the broad structure is recovered but cross-talk artifacts remain (this run used a wrong attenuation: $Q = 100$ where the true value was $Q \approx 10$). (c) Final result with realistic $Q$: the artifacts vanish and the small fault on the dipping interface is resolved — at wavelength scale, well below the Fresnel-zone floor of Figure 1b. Note the $\lambda$ and $\sqrt{\lambda L}$ bars: FWI resolves far below the ray-tomography floor.*

**(b) Time/offset windowing.** Early arrivals (direct and diving waves) are the most linearly related to the shallow model — invert them first, then admit reflections at later times, then the full trace (Shipp & Singh 2002). This is the same "simplify, then relax toward the full problem" logic as frequency continuation.

**(c) Alternative misfit functions.** Replace the raw least-squares residual by something that degrades gracefully under large time shifts (Luo & Schuster 1991 onward):

- **Traveltime / time-shift misfits** — cross-correlate observed and modelled traces in windows; invert the time shifts. Close to tomography; very robust.
- **Adaptive waveform inversion (AWI)** (Warner & Guasch 2016) — design a matching filter from modelled to observed data; iterate until the filter becomes a spike. Convex under time shifts.
- **Instantaneous phase, dynamic time warping, optimal transport** — misfits designed to have wide, well-behaved basins.
- **Lp norms / robust statistics** — for heavy-tailed noise rather than non-linearity.

**(d) Extended formulations.** Add auxiliary degrees of freedom that let an imperfect model fit the data, then penalize them: wavefield reconstruction inversion (WRI; van Leeuwen & Herrmann 2013), extended-source and extended-reflectivity methods. These are the research frontier transitioning to practice.

**(e) Better starting models.** The blunt instrument that never fails: ray tomography, WEMVA (migration-velocity analysis by gather flattening), or interpretation-guided model building before FWI. On land data — where low frequencies are missing and offsets are short — the starting model is often the decisive factor. Figure 11 shows the land case: a gradient starting model cycle-skips the reflection data; a phase-tolerant objective (DFPD; Zhang & Dai 2015) survives it and updates in the correct direction, after which conventional FWI can take over.

![](figures/term03_lec07/term03_lec07_land_cycle_skipping.png){width=70%}

**Figure 12.** *Cycle skipping on land data and a work-around (Zhang & Dai 2015, SPE-177571-MS; reproduced for teaching). (a) True model of the synthetic test; (b) 1D-gradient starting model; (c) input data zoom — the simulated event (from the starting model) arrives a full period away from the observed event: cycle-skipped input for reflection FWI; (d) update from a dynamic-formation-phase-deviation (DFPD) objective: coherent, correct-direction structure; (e) update from a conventional phase-only objective: oscillatory, wrong-direction "ringing" — the signature of cycle skipping.*

**The unifying principle** (Métivier & Brossier 2026): every one of these tricks is a **relaxation** — solve a sequence of simplified FWI problems that converge back to the full-bandwidth, full-physics problem, each stage inside the trust region of the next. Frequency continuation relaxes the data bandwidth; windowing relaxes the event set; misfit modifications relax the metric; extensions relax the model space. Modern workflows combine several at once.

## 3. What FWI buys you

### 3.1 Velocity models at wavelength scale

The headline product: velocity models with detail at the wavelength scale — an order of magnitude finer than ray tomography (recall Figure 1 vs Figure 11). Two examples.

![](figures/term03_lec07/term03_lec07_bp2004_fwi_resolution.png){width=75%}

**Figure 13.** *Resolution demonstration on the BP 2004 benchmark (Zhang & Dai 2015, SPE; reproduced for teaching). (a) True model with the target anomalies circled; (b) smooth FWI starting model — the anomalies removed; (c) true minus starting model: what a perfect inversion should recover; (d) the FWI update after one iteration of reflection-slope inversion: the anomalies (a compact high-velocity body, a cluster of small low-velocity gas pockets) are already imprinted on the gradient. Structures of this size are invisible to ray tomography at these wavelengths.*

![](figures/term03_lec07/term03_lec07_land_fwi_permian.png){width=100%}

**Figure 14.** *Land FWI delivering (Wang et al. 2020, EAGE; reproduced for teaching). Permian Basin field data: velocity model (a) before and (b) after FWI — the smooth initial model gains geologically plausible lateral detail; Kirchhoff depth migration with (c) the initial and (d) the FWI model — reflectors undulate and defocus in (c), flatten and focus in (d). The classic validation pair: the FWI model is trusted because the image built with it improves.*

The gather-level view of the same validation is just as convincing: with the FWI model, image gathers flatten — the residual-moveout signature of an accurate velocity model that students know from Term 1 velocity analysis and Term 3 tomography QC.

![](figures/term03_lec07/term03_lec07_land_fwi_gathers.png){width=95%}

**Figure 15.** *Gather-level QC of land FWI (Wang et al. 2020, EAGE; reproduced for teaching). Kirchhoff stacks (a) before and (b) after the FWI model update, and image gathers (c) before and (d) after: the gathers from the initial model show strong residual moveout below ~8 kft, while the FWI-model gathers are flat and better focused. The same flat-gathers criterion used to accept tomography updates (Term 3 Lecture 02) accepts FWI updates — but at much finer model detail.*

### 3.2 FWI imaging: the reflectivity byproduct

A high-resolution FWI velocity model is nearly a reflectivity model: sharp velocity contrasts at layer boundaries are exactly where reflectivity lives. Take a spatial derivative of the model (1D vertical, 3D along the local dip, or a plane-wave destructor — Kalinicheva et al. 2020; Zhang et al. 2020) and you get an "FWI image" — without running a separate migration.

![](figures/term03_lec07/term03_lec07_fwi_imaging_vs_rtm.png){width=95%}

**Figure 16.** *FWI imaging vs RTM under salt (Baldock et al. 2023, EAGE workshop; reproduced for teaching). Campos Basin towed-streamer data: (a) 3D FWI image (derivative of the FWI velocity model); (b) RTM image with the same FWI model. Green arrows: pre-salt fault blocks and fault planes better resolved in the FWI image, which compensates for the complex overburden wavefield effects.*

![](figures/term03_lec07/term03_lec07_fwi_imaging_clair.png){width=95%}

**Figure 17.** *FWI imaging in the West of Shetlands (Baldock et al. 2023, EAGE; after Wang et al. 2021; reproduced for teaching). (a) RTM with the final FWI model; (b) 3D FWI image from the same model: crisper fine layering in the shallow section and along the flanks of the structure. FWI images are increasingly used as alternatives to — or QC for — Kirchhoff and RTM products. Caveats: the derivative of velocity is not true impedance reflectivity (no density, no AVO), and its bandwidth is limited by the FWI band.*

### 3.3 Multiparameter potential — and its price

Nothing in the formulation restricts FWI to velocity. With an elastic modelling engine, FWI can in principle invert $V_p$, $V_s$ and density simultaneously; with a visco-acoustic engine, velocity and $Q$; with anisotropic engines, $\varepsilon$ and $\delta$. This is Tarantola's original ambition — *direct estimation of physical rock properties* — and elastic FWI is actively researched as a complement to AVO analysis (Operto et al. 2013; Métivier & Brossier 2026).

Two cautions temper the promise:

- **Parameter cross-talk.** The data cannot always tell whether an anomaly is a velocity change, a density change, or a $Q$ change; updates for one parameter leak into another (Keating & Innanen 2016). Careful parameterization, scaling and step-length control are active research.
- **Physics must be modelled.** If the real earth is elastic and the FWI engine is acoustic, the inversion will happily build velocity artifacts that "explain" the unmodelled amplitude behaviour. Figure 18 shows a synthetic test where acoustic FWI fails on data containing elastic effects, while elastic FWI recovers the model — the modelling physics sets the ceiling on what the inversion can deliver.

![](figures/term03_lec07/term03_lec07_acoustic_vs_elastic_fwi.png){width=95%}

**Figure 18.** *Why elastic FWI matters (Bohlen, KIT FWI course, Lecture 4; after Thiel 2018). Synthetic reconstruction test on a marine-style model: P-wave velocity (top) and density (bottom) recovered with an acoustic engine (left) and an elastic engine (right). The acoustic run (with elastic "truth") produces artifacts — note the velocity pull-down around 10 km — and the elastic run recovers both parameters cleanly. The lesson printed on the slide: "Elastic modelling/FWI is necessary" when elastic effects are significant in the data.*

## 4. Modern challenges

FWI is routine — *where its preconditions are met*: marine settings, decent low frequencies, long offsets, good S/N, big computers. The research agenda is exactly the list of preconditions that fail elsewhere.

### 4.1 Cost and its scaling with frequency

FWI needs tens of gradient iterations; each iteration is a forward + adjoint modelling of every shot — the cost of a full RTM imaging project, multiplied by the iteration count and repeated at several frequency stages. And the cost of one modelling scales steeply with maximum frequency:

- Spatial grid spacing must honour ~10 points per minimum wavelength → grid size grows as $f^2$ in 2D, $f^3$ in 3D (per unit volume);
- Time stepping honours the CFL condition → step count grows as $f$;
- Net effect: cost per modelled shot grows roughly as $f^4$ in 3D (Farmer et al. 2006; Jones 2019).

Doubling the frequency makes each iteration ~16× more expensive. This is why "start low" is not only a convergence strategy but a budget strategy, why few discrete frequencies are inverted per stage (the frequency-domain trick of Pratt 1999), why encoded simultaneous sources and plane-wave inversions exist, and why GPU-accelerated solvers matter. FWI drives the hardware market the way RTM did a decade ago.

> **Checkpoint 2 (2 minutes — discuss with a neighbour).**
> You double the maximum inverted frequency from 5 Hz to 10 Hz on a fixed survey. Roughly how does the cost of one iteration change? And what *else* gets harder, beyond cost?
> *(Cost: grid points per wavelength halve in every direction and the time step halves → ~$2^4 = 16×$ more expensive per iteration. Beyond cost: the starting-model requirement tightens fourfold — the half-period tolerance shrinks from 100 ms to 50 ms, so cycle-skipping risk rises.)*

### 4.2 Cycle skipping and the starting model

The half-period criterion (§2.6) links starting-model quality to available low frequencies: **the lower the frequencies you can invert, the worse the starting model you tolerate.** Subsalt updates need ~2 Hz data to start from tomography-grade models (Shen et al. 2017). This is the deep reason the industry pushed broadband, low-frequency sources (Term 3 Lecture 05): a towed-streamer band starting at 2 Hz instead of 8 Hz relaxes the starting-model requirement fourfold. Where low frequencies are unrecorded, the work-arounds of §2.7 (misfit design, WEMVA starting models) carry the load — at a price in effort and risk.

### 4.3 Land data: the hard case

Land FWI lags marine FWI by more than a decade (Plessix et al. 2010; Zhang & Dai 2015; Wang et al. 2020). The obstacles:

- **No simple water layer.** Marine FWI exploits a homogeneous, well-known 1500 m/s layer over the whole survey. Land has a heterogeneous, unconsolidated, strongly variable near surface — the upper part of the section of our statics lectures — with topography.
- **Topography** must be honoured in the modelling (curvilinear grids; Wang et al. 2020), or phase errors appear that the inversion misattributes to the subsurface.
- **Strong near-surface wavefield.** Guided waves and shallow reverberants dominate synthetic gathers while being absent (or incoherent) in field data — they must be attenuated *in both* field and synthetic domains (Figure 17).
- **Noise and S/N.** Ground roll, cultural noise, wind — land records are noisier, and FWI fits *everything*, including noise, unless it is controlled (but heavy processing is also dangerous: FWI wants data as close to "physics" as possible).
- **Elasticity everywhere.** Strong $S$-wave generation and mode conversions in the near surface make the acoustic approximation untenable (recall Figure 16).
- **Source signature and coupling.** Every vibrator/dynamite shot has its own signature, ground coupling varies shot-by-shot, and the source wavelet enters the forward modelling directly (§4.5).
- **Acquisition geometry.** Short offsets and irregular sampling limit diving-wave illumination; missing low frequencies complete the trap that makes reflection FWI cycle-skip (Figure 11).

![](figures/term03_lec07/term03_lec07_land_noise_conditioning.png){width=100%}

**Figure 19.** *Land data conditioning for FWI (Wang et al. 2020, EAGE; reproduced for teaching). (a) Field shot gather before noise attenuation — ground roll dominates; (b) after surface-wave noise attenuation — weaker diving-wave/reflection signal emerges; (c) synthetic gather from the initial model — strong shallow guided-wave energy with no counterpart in the field data; (d) synthetic after the same shallow-wavefield attenuation. Matching field and synthetic domains is the land equivalent of the marine "simple water layer" luxury.*

Two published land workflows show the payoff when these obstacles are met head-on.

**Inner Mongolia (BGP; Zhang & Dai 2015).** Short offsets and missing low frequencies ruled out diving-wave FWI, so the workflow attacked reflections directly: start from a 1-D gradient model, run cycle-skip-tolerant **DFPD FWI** in a 3–8 Hz band (Figure 12 showed its gradient behaviour), refine with **WEMVA** gather flattening, then image. The field result (Figure 20): the FWI model gains coherent lateral structure and the RTM image improves accordingly — on data that would defeat conventional FWI at step one.

![](figures/term03_lec07/term03_lec07_land_fwi_inner_mongolia.png){width=62%}

**Figure 20.** *Land FWI workflow result, Inner Mongolia (Zhang & Dai 2015, SPE-177571-MS; reproduced for teaching; panels as in the source). (a) Starting point: 1-D gradient velocity model and the RTM image migrated with it — events imaged poorly. (b) After cycle-skip-tolerant FWI (DFPD, 3–8 Hz): the velocity model acquires geologically coherent lateral structure and the RTM image focuses. A later WEMVA flattening stage refined the model further before final imaging.*

**Onshore Mexico (Pemex/TGS; Sheng et al. 2022).** A different route to the same goal: **dynamic-matching FWI (DMFWI)** — an objective built on multi-dimensional local cross-correlations that plays down amplitudes and stays robust in strong noise — run from a tomography-derived starting model. Kirchhoff gathers flatten after the update, and both Kirchhoff and RTM images sharpen over the faulted target (Figure 21). Note how this case combines the whole toolbox: tomography starting model, noise-robust misfit design (§2.7), gather-flatness QC — FWI as the sharp tip of the model-building ladder, not a replacement for it.

![](figures/term03_lec07/term03_lec07_land_fwi_pemex_kirchhoff.png){width=100%}

**Figure 21.** *Land FWI imaging, onshore Mexico (Sheng et al. 2022, TGS/Pemex; reproduced for teaching). Kirchhoff PSDM (a) before and (b) after the DMFWI velocity update: red arrows mark imaging improvements over the faulted target — reflectors sharpen and continuity improves. The corresponding RTM comparison shows the same pattern (shown on the slides).*

### 4.4 Physics gaps: elasticity, anisotropy, absorption

Every unmodelled physical effect becomes a systematic data mismatch, which FWI absorbs as model error:

- **Elasticity** — mode conversions, surface waves; solved in principle by elastic FWI (Figure 16) at 10–100× the acoustic cost, with the cross-talk problem of §3.3.
- **Anisotropy** — modern imaging is TTI/anisotropic; FWI must invert $\varepsilon$, $\delta$ (and $V_p$) jointly or inherit biased velocities. Usually anisotropy parameters are constrained externally (wells, tomography) and FWI updates $V_p$ only.
- **Absorption** — real rocks attenuate; the forward engine must include $Q$ with its physically required **dispersion** (Term 2 Lecture 01), otherwise velocity and attenuation are ambiguous (Hak & Mulder 2011; Keating & Innanen 2016). Pratt's scale model (Figure 11b) is the cautionary display: a wrong $Q$ in the engine produced the cross-talk artifacts that the correct $Q$ removed. Visco-acoustic FWI inverts for $Q$ itself — promising, but couples strongly to amplitudes and source signature.

### 4.5 Source signature, coupling, and amplitudes

The forward modelling needs the source wavelet — its phase and amplitude — for every shot. Errors here enter every residual directly:

- Marine: airgun signatures are measurable and stable; de-signatured input is standard (Term 3 Lecture 05).
- Land: the effective source varies shot-to-shot with coupling; source-independent and source-inversion FWI schemes estimate the wavelet inside the loop (Bohlen, FWI Lecture 5).
- Amplitude fidelity matters because FWI fits amplitudes, not just times: geometric spreading, receiver coupling, directivity all bias the update if uncorrected. The gradient is often amplitude-balanced (geometrical-spreading correction) to focus the update on kinematics.

### 4.6 Data quality and the role of preprocessing

FWI is sometimes advertised as "no processing needed — feed the raw shots." The truth is more nuanced (Jones 2019):

- Light denoising and amplitude recovery are applied; **multiples and ghosts can stay** in the data when two-way full-physics modelling reproduces them — they are signal;
- For Born-approximation (single-scattering) reflection FWI, multiples *must* be removed — the engine cannot make them;
- Geometry errors, dead channels, polarity flips, and acquisition footprints all leak into the gradient — data conditioning (Term 3 Lecture 04; Cova et al. 2017) is part of the workflow;
- The final QC is always the same pair: **data fit** (red vs. blue wiggles, Figure 9) and **image quality** with the updated model (Figure 13) — a velocity model is only as good as the data it explains and the image it enables.

## 5. Summary

### Key takeaways

1. **Rays have a resolution floor** ($\approx\sqrt{\lambda L}$, the Fresnel zone); FWI replaces traveltime fitting with full-waveform fitting through a wave-equation engine and resolves down to $\approx\lambda$.
2. **FWI is an iterative loop**: forward modelling → least-squares residual → gradient → line search → update. The gradient is computed by back-propagating the residual and correlating with the source wavefield — the RTM imaging condition applied to the residual: "migrate the residual."
3. **The problem is non-linear because wavelets oscillate**: if the starting model errs by more than half a period, $|\Delta t| < T/2 = 1/2f$, the inversion matches the wrong cycle — **cycle skipping** — and converges to a local minimum.
4. **All work-arounds are relaxations**: frequency continuation, time windowing, alternative misfits (traveltime, AWI, OT), extended formulations (WRI), better starting models. Low frequencies are forgiving — they widen the trust region.
5. **What FWI delivers**: wavelength-scale velocity models, FWI imaging (derivative of the model $\approx$ reflectivity), and a multiparameter path ($V_s$, $\rho$, $Q$, anisotropy) guarded by parameter cross-talk.
6. **Cost scales steeply with frequency** ($\sim f^4$ per shot modelling in 3D): start low for physics *and* budget.
7. **Land is the hard case**: no water layer, topography, a complex attenuative elastic near surface, noisy records, variable source coupling, short offsets, missing low frequencies.
8. **Physics gaps become model errors**: elastic effects, anisotropy, absorption must live in the forward engine — with dispersion if $Q$ is modelled.
9. **QC is two displays**: observed vs. modelled data (cycle-for-cycle fit) and the migrated image / gathers with the updated model.

### The big picture

| | Stacking analysis | Ray tomography | FWI |
|---|---|---|---|
| Data used | reflection moveout | picked traveltimes | full waveforms |
| Physics | hyperbolic NMO | rays, Snell | two-way wave equation |
| Resolution | very smooth | $\sim\sqrt{\lambda L}$ | $\sim\lambda$ |
| Non-linearity | mild | mild | severe (cycle skipping) |
| Cost | low | low | high ($\propto f^4$ per modelling) |
| Preconditions | none special | picks exist | low frequencies, starting model, S/N, physics |

FWI does not replace the earlier ladder — it stands on it. Tomography and WEMVA build the starting model; statics and near-surface models fix what land FWI cannot; broadband acquisition widens the frequencies that make the whole edifice stable. The processing stream and the inversion are converging — toward Symes' "rational replacement for the entire processing stream" — but for now, FWI is the top rung of a ladder the whole course has been climbing.

## Comprehension questions

1. Explain, with the boulder analogy, why ray-based tomography cannot resolve structures comparable to the wavelength. What length scale sets the ray resolution floor, and how does it compare with what FWI resolves?
2. Walk through one FWI iteration in your own words. Why do we say the gradient is "the migration of the residual," and why does the single-shot gradient look like a migration impulse response?
3. Why can FWI not simply "solve" for the best model the way semblance analysis scans stacking velocities? What does the dimension of the model space have to do with the choice of local, iterative optimization?
4. State the half-period criterion for cycle skipping. A starting model predicts arrival times with an rms error of 60 ms. Up to which dominant frequency can you safely start inverting?
5. Explain the multiscale (frequency-continuation) strategy. Why does it reduce cycle-skipping risk, and why is it also a cost strategy?
6. Which misfit-function modifications for cycle skipping can you name? What do they have in common?
7. FWI migrates the residual; RTM migrates the data. Both use cross-correlation imaging conditions. Explain the difference in what the two "images" mean, and why RTM cross-talk ("rabbit ears") is noise in imaging but signal in FWI.
8. List at least four reasons land FWI is harder than marine FWI. Which of them would you address in acquisition, which in preprocessing, and which inside the FWI engine?
9. Why must a forward engine that includes attenuation also include velocity dispersion? What happens to FWI if it does not?
10. An FWI run on your data has converged — the misfit stopped decreasing. Give two QC displays you would check before trusting the model, and what each tells you.

## Suggested reading and sources

- Jones, I. F. (2019). Tutorial: the mechanics of waveform inversion. *First Break*, 37, 31–43. — The backbone of this lecture: gradient, RTM link, cycle skipping, workflow. `wiki/sources/jones2019_fwi_mechanics_tutorial.md`.
- Pratt, R. G. (1999). Seismic waveform inversion in the frequency domain, Part 1. *Geophysics*, 64(3), 888–901. — Scale-model verification; resolution; starting-model criterion; Q effects. `wiki/sources/pratt1999_frequency_domain_fwi.md`.
- Tarantola, A. (1984). Inversion of seismic reflection data in the acoustic approximation. *Geophysics*, 49(8), 1259–1266. — The founding paper. `wiki/sources/tarantola1984_inversion_acoustic.md`.
- Métivier, L., & Brossier, R. (2026). A comprehensive review of strategies to mitigate non-convexity in full waveform inversion. *Geophys. J. Int.*, 247, 1–38. (CC-BY.) — The taxonomy of non-linearity work-arounds. `wiki/sources/metivier2026_fwi_nonconvexity_review.md`.
- Bohlen, T. — *Full Waveform Inversion* lecture series, KIT, WS 2021/22 (`papers/fwi/FWI_Lecture_*.pdf`). — Deeper math (adjoint state, Born) plus the application galleries used here. `wiki/sources/bohlen_fwi_lecture_series.md`.
- Zhang, W., & Dai, N. (2015). Land Data FWI: Methods and Strategies. *SPE-177571-MS*. — Land cycle-skipping work-arounds, BP 2004 resolution test. `wiki/sources/zhang2015_land_data_fwi.md`.
- Wang, D., et al. (2020). Land FWI: challenges and possibilities. *82nd EAGE*. — Topography, near-surface mitigation, Permian Basin example. `wiki/sources/wang2020_land_fwi_challenges.md`.
- Sheng, J., Reta-Tang, C., Liu, F., Vázquez Cantú, A., & Cabrales Vargas, A. (2022). Full-waveform inversion and FWI imaging for land data. *TGS/Pemex abstract*. — Dynamic-matching FWI on land; land FWI imaging. `wiki/sources/sheng2022_land_fwi_imaging.md`.
- Baldock, S., et al. (2023). FWI Imaging: the future or merely derivative? *84th EAGE Workshop*. — FWI imaging examples. `wiki/sources/baldock2023_fwi_imaging.md`.
- Keating, S., & Innanen, K. (2016). Anacoustic FWI: implementation and challenges. *CREWES Research Report*, 28. — Q-in-FWI hazards. `wiki/sources/keating2016_anacoustic_fwi.md`.
- Cova, R., Law, B., & Innanen, K. (2017). Toward robust multicomponent FWI on land data. *CREWES Research Report*, 29. — Land conditioning. `wiki/sources/cova2017_land_multicomponent_conditioning.md`.
