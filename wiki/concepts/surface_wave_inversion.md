---
title: Surface wave inversion
status: draft
sources:
  - foti_surface_wave_methods
  - foti_interpacific_guidelines
  - priestley_surface_wave_practical
  - mi_surface_waves_dispersion_energy
  - novotny_seismic_surface_waves
  - sedi_surface_waves
  - ivanov_hrlrt_masw
tags: [surface-waves, inversion, masw, swi, regularization, vs-profile]
---

# Surface wave inversion

Surface wave inversion turns an observed dispersion curve into a shear-wave velocity (VS) profile of the subsurface. The workflow is usually called **MASW** (Multichannel Analysis of Surface Waves) or **SWI** (Surface Wave Inversion) in near-surface geophysics.

## From dispersion curve to VS profile

1. Acquire surface-wave data (active source, passive noise, or both).
2. Extract the experimental dispersion curve (phase velocity vs. frequency) for one or more modes.
3. Build a layered earth model with thickness, VS, VP, and density for each layer.
4. Compute the theoretical dispersion curve for the model (forward problem).
5. Adjust the model to minimize the misfit between observed and predicted curves (inverse problem).

## Forward problem

Given a stack of homogeneous, isotropic layers, the modal phase velocities are found by solving the eigenvalue problem for the layered medium. This involves matching boundary conditions at each interface and the free surface. The result is a set of theoretical dispersion curves, one for each mode.

## Inverse problem

The inverse problem is **non-linear** and **non-unique**:

- Different VS profiles can produce nearly the same dispersion curve.
- The data constrain the average velocity over a wavelength range, but fine layer boundaries may be poorly resolved.
- Layer thickness and VS are the most influential parameters; VP and density have a smaller effect and are usually fixed or bounded.

## Regularization and constraints

- Use the **minimum number of layers** needed to explain the data.
- Apply **smoothness** or **damping** so that the model does not oscillate wildly.
- Include **a priori** information (geology, borehole logs, water table) to fix VP and density.
- Invert multiple modes together to tighten the solution.
- Report a **set of equivalent solutions** rather than a single best model, because the data do not uniquely determine the profile.

## Multi-mode constraint for VP/VS

Including higher modes in the inversion reduces the trade-off between layer thickness and velocity. It also helps constrain the ratio VP/VS (Poisson's ratio), which is important for distinguishing saturated from unsaturated soils.

## Common pitfalls

- Misidentifying a higher mode or LVL-guided energy as the fundamental mode.
- Over-parameterizing the model with too many layers.
- Ignoring lateral heterogeneity when the site is not 1D.
- Trusting a single best-fit model without uncertainty bounds.

## Related concepts

- [Surface waves](surface_waves.md)
- [Surface wave dispersion](surface_wave_dispersion.md)
- [Surface wave multimodality](surface_wave_multimodality.md)
- [FK-MUSIC / array analysis](fk_music_surface_waves.md)
- [Adaptive subtraction](adaptive_subtraction.md)

## Sources

- [Foti et al. (2011) — Surface wave methods](../sources/foti_surface_wave_methods.md)
- [Foti et al. (2018) — InterPACIFIC guidelines](../sources/foti_interpacific_guidelines.md)
- [Priestley (2024) — Surface wave practical](../sources/priestley_surface_wave_practical.md)
- [Mi et al. (2016) — Dispersion energy analysis](../sources/mi_surface_waves_dispersion_energy.md)
- [Novotny (1999) — Seismic surface waves](../sources/novotny_seismic_surface_waves.md)
- [Igel (2007) — Surface waves and free oscillations](../sources/sedi_surface_waves.md)
- [Ivanov et al. (2017) — HRLRT with MASW](../sources/ivanov_hrlrt_masw.md)
