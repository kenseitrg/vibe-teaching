---
title: FK-MUSIC / array analysis for surface waves
status: draft
sources:
  - datta_2018
  - foti_surface_wave_methods
  - foti_interpacific_guidelines
  - ivanov_hrlrt_masw
  - mi_surface_waves_dispersion_energy
  - priestley_surface_wave_practical
tags: [surface-waves, fk, music, beamforming, array-processing, dispersion]
---

# FK-MUSIC / array analysis for surface waves

Array-based methods measure surface-wave dispersion by exploiting the fact that the wavefront arrives at different receivers with a phase shift that depends on its frequency and apparent velocity. The goal is to turn a set of seismograms into a dispersion image (phase velocity vs. frequency) and then pick the modal branches.

## Frequency–wavenumber (f–k) analysis

- Apply a 2D Fourier transform over time and space.
- Energy peaks in the f–k spectrum correspond to propagating modes.
- Convert wavenumber to phase velocity: c = f / k.
- The resolution depends on array length and station spacing; a longer array gives better separation of nearby modes.

## f–k-MUSIC

- **MUSIC** (Multiple Signal Classification) is an array-processing technique from radar/sonar.
- It separates the recorded wavefield into a **signal subspace** (the modes) and a **noise subspace**.
- Because it uses the noise subspace, it can produce a much sharper spectrum than conventional f–k with fewer receivers.
- The f–k spectrum is interpolated to a phase-velocity (f–c) dispersion image for picking.

## Phase-velocity scanning and slant-stack

- **Slant-stack** (or frequency-domain slant-stack): apply a trial phase shift to each trace and stack; repeat for many trial velocities to build a dispersion image.
- **High-resolution linear Radon transform (HRLRT)**: a near-surface MASW technique that suppresses spectral leakage and improves separation between fundamental and higher modes.
- **UC-diagram**: a method that plots energy in group-velocity vs. phase-velocity space and can recover both quantities simultaneously.

## Picking dispersion curves

- Identify continuous, high-amplitude branches on the dispersion image.
- Use the expected velocity range and the shape of the curve to distinguish the fundamental mode from higher modes.
- Window the data in time (group-velocity window) to suppress the fundamental mode and reveal overtones.
- Be cautious: artefacts from aliasing, noise, or lateral heterogeneity can look like real branches.

## Practical requirements

- Array length should be several times the longest wavelength of interest (Datta suggests 3–4× for upper-mantle studies).
- Station spacing must be small enough to avoid spatial aliasing.
- 2D arrays are preferred for passive ambient-noise data because the wavefield can arrive from any direction.

## Related concepts

- [Surface waves](surface_waves.md)
- [Surface wave dispersion](surface_wave_dispersion.md)
- [Surface wave multimodality](surface_wave_multimodality.md)
- [Surface wave inversion](surface_wave_inversion.md)

## Sources

- [Datta (2018) — f-k-MUSIC method](../sources/datta_2018.md)
- [Foti et al. (2011) — Surface wave methods](../sources/foti_surface_wave_methods.md)
- [Foti et al. (2018) — InterPACIFIC guidelines](../sources/foti_interpacific_guidelines.md)
- [Ivanov et al. (2017) — HRLRT with MASW](../sources/ivanov_hrlrt_masw.md)
- [Mi et al. (2016) — Dispersion energy analysis](../sources/mi_surface_waves_dispersion_energy.md)
- [Priestley (2024) — Surface wave practical](../sources/priestley_surface_wave_practical.md)
