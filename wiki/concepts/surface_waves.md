---
title: Surface waves
status: draft
sources:
  - foti_surface_wave_methods
  - foti_interpacific_guidelines
  - novotny_seismic_surface_waves
  - sedi_surface_waves
  - rawlinson_surface_waves_dispersion
  - priestley_surface_wave_practical
  - mi_surface_waves_dispersion_energy
  - ivanov_hrlrt_masw
tags: [surface-waves, rayleigh-waves, love-waves, ground-roll, near-surface]
---

# Surface waves

Surface waves are elastic waves that travel along or near the free surface of the Earth rather than through its interior. They are usually the largest-amplitude events on land seismograms, especially at longer offsets and lower frequencies.

## Why they are different from body waves

- **Body waves** (P and S) spread outward in three dimensions, so their energy decays roughly as 1/r².
- **Surface waves** are confined to the near-surface and spread in two dimensions, so their energy decays roughly as 1/r.
- Because the decay is slower, surface waves can dominate the late part of a seismogram and even circle the Earth after a large earthquake.

## Rayleigh waves

Rayleigh waves are coupled P-SV motion that satisfies the stress-free condition at the Earth's surface. In a homogeneous half-space:

- The phase velocity is fixed at about 0.92 times the shear-wave velocity.
- Particle motion is **retrograde elliptical** at the surface: as the wave moves forward, a surface particle moves backward at the top of its orbit.
- Amplitude decays exponentially with depth, becoming small within about one wavelength.

In layered media, Rayleigh waves become dispersive: different frequencies travel at different velocities because they sample different depth ranges.

## Love waves

Love waves are pure SH motion. They do **not** exist on a homogeneous half-space; they need a low-velocity layer over a higher-velocity half-space. Multiple reflections within the low-velocity layer interfere constructively and trap energy near the surface. Love waves are always dispersive in layered media.

## Surface waves in exploration seismology

- For **reflection processing**, surface waves are usually treated as **noise** (ground roll). They are low-velocity, low-frequency, and high-amplitude, and they can obscure deeper reflections.
- For **near-surface characterization**, surface waves are the **signal**. Their dispersion curve is used to estimate S-wave velocity profiles (MASW/SWI).

## Teaching intuition

- Think of a Rayleigh wave as a ripple trapped at the surface: the motion is elliptical, like a rolling wheel, and dies away with depth.
- Think of a Love wave as a trapped SH echo in a soft surface layer: it can only exist if the layer is slower than what is underneath.
- A typical land shot gather may show ground roll with velocities of 100–1000 m/s, much slower than P-wave reflections (1500–5000 m/s).

## Related concepts

- [Surface wave dispersion](surface_wave_dispersion.md)
- [Surface wave multimodality](surface_wave_multimodality.md)
- [Surface wave inversion](surface_wave_inversion.md)
- [FK-MUSIC / array analysis](fk_music_surface_waves.md)
- [Adaptive subtraction](adaptive_subtraction.md)
- [Term 3 Lecture 3 — Surface Waves](../lecture_ready/term03_lec03_surface_waves.md)

## Sources

- [Foti et al. (2011) — Surface wave methods](../sources/foti_surface_wave_methods.md)
- [Foti et al. (2018) — InterPACIFIC guidelines](../sources/foti_interpacific_guidelines.md)
- [Novotny (1999) — Seismic surface waves](../sources/novotny_seismic_surface_waves.md)
- [Igel (2007) — Surface waves and free oscillations](../sources/sedi_surface_waves.md)
- [Rawlinson (2007) — Surface waves and dispersion](../sources/rawlinson_surface_waves_dispersion.md)
- [Priestley (2024) — Surface wave practical](../sources/priestley_surface_wave_practical.md)
- [Mi et al. (2016) — Dispersion energy analysis](../sources/mi_surface_waves_dispersion_energy.md)
- [Ivanov et al. (2017) — HRLRT with MASW](../sources/ivanov_hrlrt_masw.md)
