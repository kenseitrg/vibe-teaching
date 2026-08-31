---
title: Adaptive subtraction of surface waves
status: draft
sources:
  - foti_surface_wave_methods
  - ivanov_hrlrt_masw
  - mi_surface_waves_dispersion_energy
  - priestley_surface_wave_practical
tags: [surface-waves, noise-attenuation, adaptive-subtraction, ground-roll, wiener-filter]
---

# Adaptive subtraction of surface waves

In reflection seismology, surface waves are usually treated as coherent noise (ground roll). One way to remove them is to build a model of the surface-wave wavefield and then subtract it from the recorded data. Because the model is never perfect, an **adaptive subtraction** step is normally used.

## Modeling the surface wave

A surface-wave model can be built from the picked dispersion curve:

- For each frequency, the phase velocity is known, so the moveout across the receiver array is also known.
- The model is a synthetic wavefield that contains only the predicted surface-wave energy.
- Because surface waves are dispersive, the moveout is **frequency-dependent**: long wavelengths arrive earlier relative to short wavelengths than they would for a simple linear moveout.

## Frequency-dependent linear moveout

If the phase velocity c(f) is known, the travel time to offset x is approximately t(f, x) = x / c(f). Applying this frequency-dependent delay and summing over frequencies reconstructs the predicted surface-wave arrival.

## Spatial smoothing

Real surface waves vary laterally along the profile. A modeled wavefield may be smoothed over offset or along the survey line so that it matches the slowly varying coherent noise without following every local amplitude fluctuation.

## Why adaptive subtraction is needed

Direct subtraction of the raw model often leaves residual noise because:

- The predicted amplitudes and phases do not match the real data exactly.
- The wavefield may be affected by source coupling, near-surface scattering, and 3D effects.
- A simple static or deterministic filter cannot account for these variations.

## Adaptive filter concept

An adaptive filter finds a local filter that minimizes the energy remaining after subtraction. The idea is the same as a **Wiener filter**: design a filter that best matches the predicted noise to the actual noise, then subtract the filtered model. The filter coefficients are estimated from the cross-correlation between the model and the data, under the assumption that the residual should be as small as possible.

## Filter-length trade-off

- A **short filter** adapts quickly to local variations but may not capture the full wavelet shape.
- A **long filter** can match the wavelet better but may also start to remove reflected signal that is similar to the noise.
- The filter length is a regularization choice: it controls how aggressively the algorithm subtracts coherent noise.

## Relation to other methods

Adaptive subtraction is conceptually related to MASW/SWI processing, but the goal is different: instead of extracting a dispersion curve for inversion, the goal is to predict and remove the surface wave so that deeper reflections are visible.

## Related concepts

- [Surface waves](surface_waves.md)
- [Surface wave dispersion](surface_wave_dispersion.md)
- [Surface wave inversion](surface_wave_inversion.md)
- [FK-MUSIC / array analysis](fk_music_surface_waves.md)
- [Wiener filter](wiener_filter.md)

## Sources

- [Foti et al. (2011) — Surface wave methods](../sources/foti_surface_wave_methods.md)
- [Ivanov et al. (2017) — HRLRT with MASW](../sources/ivanov_hrlrt_masw.md)
- [Mi et al. (2016) — Dispersion energy analysis](../sources/mi_surface_waves_dispersion_energy.md)
- [Priestley (2024) — Surface wave practical](../sources/priestley_surface_wave_practical.md)
