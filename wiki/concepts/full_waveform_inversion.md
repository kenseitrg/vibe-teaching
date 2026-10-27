---
title: Full-waveform inversion (FWI)
status: draft
sources:
  - jones2019_fwi_mechanics_tutorial
  - metivier2026_fwi_nonconvexity_review
  - pratt1999_frequency_domain_fwi
  - tarantola1984_inversion_acoustic
  - bohlen_fwi_lecture_series
tags: [fwi, inversion, velocity-model-building, wavefield, gradient]
---

# Full-waveform inversion (FWI)

**Full-waveform inversion** is a model-building method that iteratively updates a subsurface model (primarily P-wave velocity) so that **synthetic seismograms**, computed by numerically solving the wave equation, match **recorded field data** — using the full waveform (arrival times, phase, amplitudes), not just picked traveltimes.

## The one-sentence idea

> Migrate the residual, and call the result a velocity update. (After Tarantola 1984; Jones 2019)

## Position among model-building methods

| Method | Data used | Physics | Resolves | Cost |
|--------|-----------|---------|----------|------|
| Stacking / semblance velocity analysis | NMO curves of reflections | hyperbolic moveout | long-wavelength $V_\text{rms}$ | low |
| Refraction (ray) tomography | picked first-arrival times | rays (Snell) | features ≳ Fresnel zone $\sqrt{\lambda L}$ | low |
| Reflection (ray) tomography | picked residual moveout | rays + migration | long-wavelength updates | low |
| **FWI** | **full waveforms** | **wave equation (two-way)** | **≈ wavelength λ and below** | high (∝ $f_{\max}^4$ per shot) |

Rays are a high-frequency approximation: valid when velocity varies smoothly on the scale of a wavelength. When anomalies are comparable to or smaller than λ, scattering/diffraction dominates and ray-based descriptions break down — FWI is the tool for that regime.

## Formulation (conceptual)

Minimize over model $m$ (gridded velocity):

$$ C(m) = \| d_\text{obs} - d_\text{cal}[m] \|^2, \qquad d_\text{cal}[m] = \text{solve wave equation in } m \text{ at receiver positions}. $$

- $d_\text{cal}$ depends **nonlinearly** on $m$ → iterative **local** optimization (gradient descent / conjugate gradients), not a one-shot solve.
- **Gradient** $\partial C/\partial m$: obtained without explicit derivatives by an **adjoint-state (back-propagation)** construction — forward-model the source wavefield, back-propagate the data residual from the receivers ("adjoint source"), correlate the two; conceptually the RTM imaging condition applied to the residual.
- **Step length / line search** fixes how far to move along the gradient; the Hessian (second derivatives) would be ideal but is impractical for $10^7$–$10^8$ cells.
- One iteration = a few full 3D modelling jobs (forward + adjoint) over all shots — hence the cost.

## Workflow

1. Preprocessing: geometry, denoise (lightly), amplitude recovery; wavelet estimate.
2. Starting model (smooth, kinematically correct): ray tomography / WEMVA / interpretation.
3. Cycle-skip-avoiding update (traveltime/adaptive misfits), then low-frequency FWI.
4. Frequency continuation: invert progressively higher frequency batches (multiscale).
5. Refraction (diving-wave) FWI for shallow (~⅓ max offset), reflection FWI for deeper.
6. QC: data fit (observed vs modelled shot gathers / frequency panels), flat image gathers, migrated image quality; FWI imaging (derivative of the final model) as a byproduct.

## What the gradient looks like

Summed over shots, the gradient resembles a migration image of the residual: contributions focus along wave paths — the diving-wave "banana" kernel (tomographic, long-wavelength), reflection arcs, and the "rabbit-ear" cross-talk kernels that reach below the diving-wave depth.

## Strengths

- Resolution down to ≈ λ (sub-wavelength with reflections/multiples).
- Uses all physics the modelling contains (turning waves, multiples if two-way modelling).
- Extensible in principle to multi-parameter (density, $V_s$, anisotropy ε/δ, $Q$, attenuation) — elastic FWI, visco-acoustic FWI.
- FWI imaging: spatial derivative of the final model ≈ reflectivity image.

## See also

- [Cycle skipping](fwi_cycle_skipping.md) — the non-linearity problem and its mitigations.
- [Seismic velocities](seismic_velocities.md), [Velocity analysis](velocity_analysis.md) — the classical route FWI complements.
