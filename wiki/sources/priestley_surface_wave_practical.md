---
title: "Surface Wave Practical"
status: draft
source_type: course notes
authors: "Keith Priestley"
year: 2024
url:
lectures:
  - term03_lec03
related_concepts:
  - surface_waves
  - surface_wave_dispersion
  - surface_wave_inversion
tags: [surface-waves, rayleigh-waves, dispersion, group-velocity, phase-velocity, inversion]
---

# Surface Wave Practical

Priestley, K. (2024). *Surface Wave Practical*. ICTP Lithosphere System Workshop.

## Main message

Surface waves are the largest amplitude arrivals on seismograms for shallow earthquakes. Their velocities depend on frequency, and the dispersion curve can be inverted to estimate the S-wave velocity structure of the Earth.

## Phase and group velocity

- The carrier wave of a narrow-band signal propagates at the phase velocity c = ω/k.
- The envelope (energy packet) propagates at the group velocity u = dω/dk.
- The two are related by u = c + k dc/dk or u = c / [1 − (T/c) dc/dT].

## Measuring dispersion

- Determine arrival times of peaks and troughs on the seismogram; the slope of a phase-number vs. arrival-time curve gives the period.
- Group velocity is obtained from the travel time of energy at each period.
- Phase velocity can be estimated from two stations on the same great-circle path by eliminating the unknown source phase term.

## Determining structure

- Compare observed group-velocity curves with theoretical curves for a liquid layer over a half-space (oceanic structure) or a layered elastic model (continental structure).
- The fit gives average properties along the propagation path.
- For example, a water-layer thickness can be estimated from the step in the oceanic group-velocity curve.

## Surface wave tomography

- The practical includes a tomography exercise inverting ambient-noise travel times over Australia.
- A subspace inversion method is used iteratively to solve the non-linear problem.
- Damping and smoothing factors must be balanced to control data fit and model roughness.

## Relation to lecture notes

Priestley provides the hands-on connection between phase/group velocity measurements and S-wave structure. It is useful for showing students how to read a dispersion curve and why inversion needs regularization.

## Related concepts

- [Surface waves](../concepts/surface_waves.md)
- [Surface wave dispersion](../concepts/surface_wave_dispersion.md)
- [Surface wave inversion](../concepts/surface_wave_inversion.md)
