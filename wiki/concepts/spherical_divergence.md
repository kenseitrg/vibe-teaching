---
title: Spherical divergence correction
status: draft
sources:
  - yilmaz_practical_seismic_data_analysis_amplitude
  - hill_introduction_to_seismic_processing_ch21
  - cgg_odt01_data_analysis_part1
tags: [amplitude-correction, geometric-spreading, spherical-divergence, deterministic-gain, energy-conservation]
---

# Spherical divergence correction

Spherical divergence correction (also called **geometric spreading correction**) compensates for the amplitude decay caused by the expansion of the seismic wavefront as it travels away from the source. It is a deterministic amplitude correction because it is based on a physical model rather than on the data’s own amplitude statistics.

## Physical basis

- Conservation of energy requires that the total energy flux through a wavefront remain constant (ignoring absorption and scattering).
- For a point source in a homogeneous medium, the wavefront is a sphere of radius $r$. The surface area grows as $r^2$, so the **energy density** falls as $1/r^2$.
- Because seismic amplitude is proportional to the square root of energy density, the **amplitude** falls as $1/r$.
- In a constant-velocity medium, distance is proportional to two-way traveltime $t$, so a simple compensation gain is proportional to $t$:

$$
G(t) \propto t \quad \text{or} \quad A_{\text{corrected}}(t) = t \, A_{\text{recorded}}(t)
$$

## General $t^n$ form

In practice, processors often write the correction as

$$
G(t) = t^n
$$

where $n$ depends on the assumed wavefront geometry and convention:

| Geometry | Amplitude decay | Compensating gain | Exponent $n$ |
|---|---|---|---|
| 3D point source, homogeneous | $\propto 1/r$ | $\propto t$ | 1 |
| 2D line source, homogeneous | $\propto 1/\sqrt{r}$ | $\propto \sqrt{t}$ | 0.5 |
| Some processing packages | $\propto 1/r^2$ (energy) | $\propto t^2$ | 2 |

- The $t^2$ convention comes from thinking in terms of **energy** rather than amplitude: energy density falls as $1/t^2$, so the energy-compensating gain grows as $t^2$.
- Whatever convention is used, the important thing is to be consistent and to know whether the displayed amplitudes are energy-like or amplitude-like.

## Curved-ray / layered-medium corrections

- Real subsurface velocities usually increase with depth, so rays bend and the wavefront expands faster than in a constant-velocity medium.
- A common approximation (Newman, 1973) for a layered medium is:

$$
A \propto \frac{1}{t \, V_{\text{rms}}^2(t)}
$$

- More accurate corrections require a velocity model and are often deferred to **migration**, which accounts for the true 3D wavefront geometry.

## Properties of deterministic gain

| Property | Behavior |
|---|---|
| Data independence | Uses a model, not trace-by-trace statistics |
| Amplitude contrast | Preserves relative amplitude contrasts |
| Noise | Boosts noise as well as signal at the same time |
| Reversibility | Can be removed if the velocity/model parameters are saved |
| Smoothness | Time dependence is smooth, no artificial discontinuities |
| Streaks | Identical gain for all traces does not remove source/receiver coupling variations |

## When to use
- As a first amplitude correction before stacking or velocity analysis.
- Before surface-consistent amplitude correction, so that the remaining amplitude variations are not dominated by geometric spreading.
- Not suitable as the final correction for AVO/AVA work unless the velocity model is accurate; migration provides a more rigorous correction.

## Related concepts
- [Amplitude effects](amplitude_effects.md)
- [Automatic gain control](automatic_gain_control.md)
- [Surface-consistent amplitude correction](surface_consistent_amplitude.md)
- [Lecture-ready page: Term 1 Lecture 02 — Amplitude Corrections and QC](../lecture_ready/term01_lec02_amplitude_correction_and_qc.md)
