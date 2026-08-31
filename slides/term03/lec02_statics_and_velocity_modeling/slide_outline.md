# Slide outline — Term 3, Lecture 2: Statics and velocity modeling

---

## Slide 1 — Title
- Statics and velocity modeling
- Term 3, Lecture 2
- Figure: none

---

## Slide 2 — Learning objectives
- Describe first-break picking as the input to refraction-based near-surface model building.
- Compare single-trace pickers with multichannel methods and explain why the latter are more robust.
- Sketch the diving-wave tomography workflow: picks, rays, slowness model, residuals, QC.
- Distinguish short-period statics from long-period statics and explain their effects.
- Define effective velocity and marginal effective velocity and explain how statics change them.
- Explain the trade-off between statics and the velocity model.
- Choose between flat, floating, and smooth-surface datums for imaging.
- Diagnose inaccurate near-surface velocities from residual moveout and structural anomalies.

---

## Slide 3 — Why this lecture matters
- Statics and the velocity model describe the same near-surface time distortions.
- You cannot fully correct the same feature with both.
- A mistake in the near-surface model leaks into velocities, statics, and the final image.
- Figure: none

---

## Slide 4 — Near-surface model building: two families
- Layered refraction methods: delay-time, Hagedoorn, GRM, GLI.
- Diving-wave tomography: continuous slowness grid, rays turn back to the surface.
- Full-waveform inversion: uses the full wavefield, more powerful but demanding.
- All share the same input: first-break picks.
- Figure: none

---

## Slide 5 — Single-trace first-break pickers
- Amplitude threshold: fast but sensitive to noise spikes.
- STA/LTA: ratio of short-term to long-term energy; adapts to local noise.
- Envelope / instantaneous amplitude: smooth onset, less sensitive to phase.
- Figure: `term03_lec02_first_break_picking.png`

---

## Slide 6 — Why single-trace pickers are not enough
- Ignore spatial consistency: a noise spike can be mis-picked as a first break.
- Cannot judge physical plausibility: a pick far from the expected moveout is likely wrong.
- Multichannel picking uses the whole gather and enforces a smooth moveout.
- Figure: `term03_lec02_multichannel_picking.png`

---

## Slide 7 — Diving-wave tomography: the big picture
- Models the near surface as a smooth grid of slowness (1/velocity).
- Rays bend until their ray parameter becomes zero, then return to the surface.
- Traveltime of a diving ray is the integral of slowness along the curved path.
- Figure: `term03_lec02_diving_wave_tomography.png`

---

## Slide 8 — The tomographic system
- Eikonal equation: $(\partial t/\partial x)^2 + (\partial t/\partial z)^2 = s^2(x,z)$.
- Traveltime perturbation: $\delta t \approx \int_\text{ray} \delta s(l)\, dl$.
- Discretize into cells: $\delta t_i = \sum_j L_{ij}\, \delta s_j$.
- Matrix form: $\delta \mathbf{t} = L\, \delta \mathbf{s}$.
- Regularized least squares: $\min \|\delta \mathbf{t} - L\delta \mathbf{s}\|^2 + \lambda \|D\delta \mathbf{s}\|^2$.
- Figure: none

---

## Slide 9 — Iterative workflow and QC
- Start model: smooth 1-D velocity or layered refraction result.
- Trace rays / solve Eikonal; compute residuals; solve for $\delta s$; update model.
- QC: data residual, ray coverage, checkerboard test, geological plausibility, stack response.
- Figure: `term03_lec02_diving_wave_tomography.png`

---

## Slide 10 — Short-period vs long-period statics
- Short-period statics: vary rapidly source-to-source or receiver-to-receiver; destroy hyperbolicity.
- Long-period statics: vary slowly; leave events hyperbolic but shift $t_0$ and bias velocity analysis.
- Figure: none

---

## Slide 11 — Effective velocity
- Effective velocity is the best-fit hyperbola for a chosen offset range.
- Changing $x_\text{max}$ changes the part of the curve that is fit, so $V_\text{eff}$ changes even if geology does not.
- Figure: `term03_lec02_effective_velocity.png`

---

## Slide 12 — Marginal effective velocity
- Marginal effective velocity: limit as offset range shrinks to zero.
- Slope of the $t^2$ vs. $x^2$ curve at the origin.
- For a purely hyperbolic event, equals the NMO velocity.
- Figure: `term03_lec02_marginal_effective_velocity.png`

---

## Slide 13 — How statics change effective velocities
- A constant static shifts $t_0$ but leaves curvature unchanged.
- Velocity analysis implicitly uses the wrong $t_0$, biasing the picked velocity.
- Spatially varying statics create velocity variations that track the near surface, not geology.
- Figure: `term03_lec02_statics_velocity_bias.png`

---

## Slide 14 — Datum choice for imaging
- Flat datum: large replacement statics, may distort velocities.
- Floating datum: keeps moveout hyperbolic but breaks surface consistency.
- Smooth-surface datum: preserves surface-consistent source/receiver statics and gives a smooth reference for migration.
- Figure: `term03_lec02_datum_choice.png`

---

## Slide 15 — The fundamental trade-off
- Statics remove a feature as a trace-constant shift; then the velocity model cannot recover it.
- Short-wavelength, surface-consistent features → handle with statics.
- Long-wavelength, kinematic features → handle with statics or velocity model, but not both.
- Figure: none

---

## Slide 16 — Effects of inaccurate near-surface velocity model
- Offset-dependent errors: residual non-hyperbolic moveout after NMO.
- Structural anomalies: false pull-down or push-up below near-surface errors.
- Migration defocusing: far offsets show residual moveout first.
- Figure: `term03_lec02_near_surface_velocity_error.png`

---

## Slide 17 — Summary
- First-break picking is the input; multichannel methods are more robust than single-trace pickers.
- Diving-wave tomography uses a linearized ray-path system to build a smooth near-surface model.
- Short-period statics restore hyperbolicity; long-period statics bias effective velocities.
- Effective velocity depends on offset range; marginal effective velocity is the zero-offset slope.
- Statics and velocity model are two approximations of the same distortion; choose one for each feature.
- Smooth-surface datum with surface-consistent statics is preferred for migration.
- Inaccurate near-surface velocities produce residual moveout, false structure, and defocusing.

---

## Slide 18 — Comprehension questions
- Why is multichannel picking more robust than single-trace picking?
- What is the role of the Eikonal equation in diving-wave tomography?
- Name three QC measures for a tomographic model.
- How does a long-wavelength static bias the velocity picked by velocity analysis?
- What is the difference between effective velocity and marginal effective velocity?
- Why should the same near-surface feature not be corrected by both statics and the velocity model?
- What are the advantages of a smooth-surface datum over a floating datum?
- How can you tell that a near-surface velocity model is wrong on a migrated gather?
