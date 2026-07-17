---
title: Surface wave dispersion
status: draft
sources:
  - foti_surface_wave_methods
  - foti_interpacific_guidelines
  - novotny_seismic_surface_waves
  - sedi_surface_waves
  - rawlinson_surface_waves_dispersion
  - priestley_surface_wave_practical
  - datta_2018
  - ivanov_hrlrt_masw
tags: [surface-waves, dispersion, phase-velocity, group-velocity, layered-media]
---

# Surface wave dispersion

In a homogeneous half-space, a Rayleigh wave has a single fixed velocity. In real, layered media, the velocity of a surface wave depends on its frequency. This frequency dependence is called **dispersion**.

## Phase velocity and group velocity

- **Phase velocity** c(f) = ω / k: the speed at which a single frequency component (the carrier) travels.
- **Group velocity** U(f) = dω / dk: the speed at which the energy packet (the envelope) travels.
- For dispersive waves, c and U are generally different. A long, dispersed wavetrain is the result of different frequencies arriving at different times.

## Physical origin of dispersion

A surface wave of a given wavelength samples a depth range of roughly one wavelength below the surface. If the subsurface velocity increases with depth:

- Long wavelengths (low frequencies) feel deeper, faster material, so they travel faster.
- Short wavelengths (high frequencies) stay in the shallow, slower material, so they travel slower.

This produces a dispersion curve where phase velocity decreases as frequency increases, called **normal dispersion**.

## Two-layer model intuition

Consider a soft layer with VS ≈ 200 m/s over a stiff half-space with VS ≈ 800 m/s:

- At very low frequencies (long wavelengths), the wave is mostly in the half-space, so c ≈ 0.92 × 800 ≈ 740 m/s.
- At very high frequencies (short wavelengths), the wave is trapped in the layer, so c ≈ 0.92 × 200 ≈ 180 m/s.
- Between these limits, the phase velocity transitions smoothly with frequency.

Real profiles have many layers and velocity gradients, so the curve is more complex, but the same principle holds.

## The dispersion curve

The **dispersion curve** is a plot of phase velocity vs. frequency (or period, or wavelength). It is the primary observable used in surface-wave methods because each curve shape is characteristic of a particular S-wave velocity profile.

## Why it matters

- Dispersion is the reason surface waves can be used to map near-surface S-wave velocity.
- In reflection seismology, dispersion means that a ground-roll wavelet is stretched and chirped across offsets, making simple filtering difficult.
- In global seismology, the dispersion of long-period surface waves is used to constrain crustal and upper-mantle structure.

## Related concepts

- [Surface waves](surface_waves.md)
- [Surface wave multimodality](surface_wave_multimodality.md)
- [Surface wave inversion](surface_wave_inversion.md)
- [FK-MUSIC / array analysis](fk_music_surface_waves.md)

## Sources

- [Foti et al. (2011) — Surface wave methods](../sources/foti_surface_wave_methods.md)
- [Foti et al. (2018) — InterPACIFIC guidelines](../sources/foti_interpacific_guidelines.md)
- [Novotny (1999) — Seismic surface waves](../sources/novotny_seismic_surface_waves.md)
- [Igel (2007) — Surface waves and free oscillations](../sources/sedi_surface_waves.md)
- [Rawlinson (2007) — Surface waves and dispersion](../sources/rawlinson_surface_waves_dispersion.md)
- [Priestley (2024) — Surface wave practical](../sources/priestley_surface_wave_practical.md)
- [Datta (2018) — f-k-MUSIC method](../sources/datta_2018.md)
- [Ivanov et al. (2017) — HRLRT with MASW](../sources/ivanov_hrlrt_masw.md)
