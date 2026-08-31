---
title: Term 3 Lecture 02 — Statics and Velocity Modeling
status: draft
lecture: term03_lec02
sources:
  - law_trad_comparison_of_refraction_inversion_methods
  - davletkhanov_nsm_and_velocity
  - fbpicking
  - jones_2012_incorporating_near_surface_velocity_anomalies
  - noble_2020_whats_the_datum
  - hill_introduction_to_seismic_processing_ch22
  - sysoev_statics
  - velocity_artefacts
  - term03_lecture02_statics_and_kinematics_presentation
tags:
  - statics
  - velocity-analysis
  - first-break-picking
  - diving-wave-tomography
  - effective-velocity
  - migration-datum
  - near-surface-model
---

# Term 3 Lecture 02 — Statics and Velocity Modeling

## One-line summary

A deeper look at the near-surface–velocity link: how first-break picks and diving-wave tomography build a near-surface model, how statics bias stacking velocities, and how the choice of datum couples statics to imaging.

## Key concepts covered

- First-break picking as the input to refraction-based near-surface model building.
- Single-trace pickers (STA/LTA, amplitude threshold, envelope) and why multichannel methods are more robust.
- Diving-wave (turning-ray) tomography: Eikonal equation, linearized tomographic system, iterative solution, and quality metrics (residuals, ray coverage, checkerboard tests).
- Short-period vs. long-period statics: the former restores hyperbolicity, the latter biases velocity estimates.
- Effective velocity: optimal velocity for a given offset range; marginal effective velocity as the zero-offset slope of the moveout curve.
- How large statics and datum choice change effective velocities.
- Statics and imaging: statics assumes vertical rays, migration uses true refraction; compensating a near-surface effect with statics removes it from the velocity model.
- Datum choice: smooth surface vs. CMP floating datum; preserving surface-consistent corrections while migrating from a smooth surface.
- Impact of inaccurate near-surface velocities: offset-dependent traveltime errors, residual non-hyperbolic moveout, false structural anomalies, and migration defocusing.

## Key equations

- First-break traveltime along a diving ray: $t = \int_\text{ray} s(l) \, dl$, where $s(l)=1/v(l)$ is slowness.
- Linearized tomography: $\delta \mathbf{t} = L \, \delta \mathbf{s}$, where $L$ is the ray-path length matrix.
- Hyperbolic moveout with statics: $t^2(x) = (t_0 + \Delta t)^2 + x^2/V^2$.
- Effective velocity: $V_\text{eff}(x_\text{max}) = \arg\min_V \sum_{x} \left[ t(x) - \sqrt{t_0^2 + x^2/V^2} \right]^2$.
- Marginal effective velocity: $V_\text{marg}^2 = \left. \dfrac{dx^2}{d(t^2)} \right|_{x \to 0}$.
- Statics-induced velocity bias from Sysoev: $t_{0,3}=t_0+2c(x)$, $V_3^2 = \left[ (t_0+2c)\left(t_0/V^2 + c''/2\right) \right]^{-1}$.
- Smooth-surface datum statics: keep source/receiver statics surface-consistent while moving sources and receivers to a smooth reference surface.

## Generated figures

| Figure | Path |
|--------|------|
| First-break picking algorithms | `figures/term03_lec02/term03_lec02_first_break_picking.png` |
| Multichannel vs. single-trace picking | `figures/term03_lec02/term03_lec02_multichannel_picking.png` |
| Diving-wave tomography: rays and grid | `figures/term03_lec02/term03_lec02_diving_wave_tomography.png` |
| Effective velocity and best-fit hyperbola | `figures/term03_lec02/term03_lec02_effective_velocity.png` |
| Marginal effective velocity as zero-offset slope | `figures/term03_lec02/term03_lec02_marginal_effective_velocity.png` |
| Statics bias on velocity spectrum | `figures/term03_lec02/term03_lec02_statics_velocity_bias.png` |
| Datum choice: flat, floating, and smooth surface | `figures/term03_lec02/term03_lec02_datum_choice.png` |
| Near-surface velocity error and residual moveout | `figures/term03_lec02/term03_lec02_near_surface_velocity_error.png` |

## Lecture materials

- English notes: `lecture_notes/en/term03_lec02_statics_and_velocity_modeling.en.md`
- Rendered PDF: `lecture_notes/en/term03_lec02_statics_and_velocity_modeling.en.pdf`
- Russian notes: `lecture_notes/ru/term03_lec02_statics_and_velocity_modeling.ru.md`
- Rendered PDF: `lecture_notes/ru/term03_lec02_statics_and_velocity_modeling.ru.pdf`
- Derivation (tomography): `lecture_notes/derivations/tomographic_system_derivation.en.md`
- Russian derivation: `lecture_notes/derivations/tomographic_system_derivation.ru.md`
- Exercises: `exercises/term03_lec02_statics_and_velocity_modeling.md`
- Slide outline: `slides/term03/lec02_statics_and_velocity_modeling/slide_outline.md`
- Starter deck: `slides/term03/lec02_statics_and_velocity_modeling/lec02_statics_and_velocity_modeling.pptx`

## Related concept pages

- [First-break picking](../concepts/first_break_picking.md)
- [Diving-wave tomography](../concepts/diving_wave_tomography.md)
- [Effective velocity](../concepts/effective_velocity.md)
- [Static corrections](../concepts/static_corrections.md)
- [Residual statics](../concepts/residual_statics.md)
- [Velocity analysis](../concepts/velocity_analysis.md)
- [Floating datum](../concepts/floating_datum.md)
- [Migration datum](../concepts/migration_datum.md)
- [Near-surface velocity model](../concepts/near_surface_velocity_model.md)
- [Normal moveout](../concepts/normal_moveout.md)
- [Seismic velocities](../concepts/seismic_velocities.md)

## Notes for instructor

- This lecture assumes students remember Term 1 Lectures 3 and 4 (NMO, velocity analysis, field statics, residual statics, floating datum). Begin with a brief recap rather than re-deriving those topics.
- Diving-wave tomography is the focus. Keep the ray-equation and Eikonal discussion qualitative; the full linearized system is in the derivation document.
- The effective-velocity / marginal-effective-velocity section is the conceptual heart of the lecture. Use the figures to show that the same traveltime curve can be fit by different hyperbolae when offsets change or when statics shift $t_0$.
- Emphasize the trade-off between statics and velocity model: what statics removes is no longer available to the velocity model, and vice versa. This is why accurate near-surface velocities are essential for good imaging.
- When discussing the smooth-surface datum, stress that surface-consistent source and receiver corrections must be preserved; a CMP floating datum breaks surface consistency because each trace has different source and receiver statics.
- The near-surface velocity error section connects to practical QC: look for residual non-hyperbolic moveout and structural anomalies that track near-surface variations, not geology.
- Suggested timing for a 90-minute lecture: recap (5 min), first-break picking (10 min), diving-wave tomography (20 min), statics and velocity estimation (20 min), statics and imaging (15 min), inaccurate near-surface model (15 min), summary and questions (5 min).
