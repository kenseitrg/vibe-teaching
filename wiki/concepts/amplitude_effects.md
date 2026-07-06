---
title: Amplitude effects in seismic wave propagation
status: draft
sources:
  - yilmaz_practical_seismic_data_analysis_amplitude
  - hill_introduction_to_seismic_processing_ch21
  - cgg_odt01_data_analysis_part1
tags: [amplitude, wave-propagation, attenuation, geometric-spreading, absorption, mode-conversion, near-surface]
---

# Amplitude effects in seismic wave propagation

Recorded seismic amplitudes are affected by many physical processes and acquisition conditions between the source and the receiver. Understanding these effects is the first step toward deciding which amplitudes are geology and which should be corrected.

## Main amplitude-reducing mechanisms

### 1. Reflection and transmission at boundaries
- At an elastic interface, part of the energy is reflected and part is transmitted.
- The partitioning depends on the impedance contrast and the incidence angle (Zoeppritz equations; at normal incidence, reflection coefficient $R = (Z_2 - Z_1)/(Z_2 + Z_1)$ with $Z = \rho v$).
- A stack of many intervening reflectors creates cumulative **transmission losses**.

### 2. Mode conversion
- At non-normal incidence, P-wave energy can convert to S-wave energy and vice versa.
- Mode conversion increases with incidence angle, especially beyond the critical angle.
- This removes energy from the reflected P-wave and is a form of amplitude loss.

### 3. Geometric spreading (spherical divergence)
- As the wavefront expands, the same total energy is distributed over a larger area.
- In a homogeneous medium:
  - Point source: wavefront is a sphere, energy density $\propto 1/r^2$, amplitude $\propto 1/r$.
  - Line source: wavefront is a cylinder, energy density $\propto 1/r$, amplitude $\propto 1/\sqrt{r}$.
- In layered media, ray curvature from velocity gradients modifies the simple $1/r$ law.

### 4. Absorption (anelastic attenuation)
- Elastic energy is converted to heat by pore-fluid movement, grain friction, and other mechanisms.
- Quantified by the quality factor $Q$; higher $Q$ means less attenuation.
- Absorption is frequency dependent: higher frequencies are attenuated more strongly, causing the recorded spectrum to shift toward lower frequencies with time/distance.

### 5. Scattering
- Subsurface inhomogeneities with scale comparable to the wavelength redirect energy in many directions.
- Like fog scattering light, scattering removes energy from the coherent reflected wavefront.
- In practice, scattering and absorption are often treated together because they are hard to separate from recorded data alone.

### 6. Near-surface source and receiver effects
- **Source coupling**: on land, source coupling varies with surface hardness, moisture, and source type.
- **Receiver coupling**: geophones planted in rocky or wet ground respond differently.
- **Source strength**: marine air-gun arrays can have drop-outs or varying output; vibroseis base-plate coupling changes with surface.
- **Weathering layer**: lateral velocity and thickness variations also affect amplitude.

## Why it matters for processing
- Many of these effects are **not geology**, so they must be removed or reduced before amplitude-sensitive interpretation.
- Some effects are **deterministic** (geometric spreading, known source signatures) and can be corrected directly.
- Others are **statistical** or **surface-consistent** (source/receiver coupling) and require data-driven separation.
- Some are **irreversible** in practice (e.g., AGC), so the choice of amplitude correction must match the processing goal.

## Related concepts
- [Spherical divergence](spherical_divergence.md)
- [Automatic gain control](automatic_gain_control.md)
- [Surface-consistent amplitude correction](surface_consistent_amplitude.md)
- [Seismic data QC](seismic_data_qc.md)
- [Lecture-ready page: Term 1 Lecture 02 — Amplitude Corrections and QC](../lecture_ready/term01_lec02_amplitude_correction_and_qc.md)
