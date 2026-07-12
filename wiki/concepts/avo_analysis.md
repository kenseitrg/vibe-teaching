---
title: AVO analysis
status: draft
sources:
  - hill_ruger_2020_illustrated_seismic_processing_preimaging
  - yilmaz_2001_seismic_data_analysis_deconvolution
  - shuey_1985_simplification_of_zoeppritz_equations
  - ruger_1996_p_wave_reflectivity_offset_azimuth
tags: [AVO, amplitude, offset, Shuey, Ruger, anisotropy, rock-physics, AVAz, intercept, gradient, QC]
---

# AVO analysis

AVO (amplitude versus offset) analysis studies how reflection amplitude changes with source-receiver offset. It is used for lithology and fluid prediction, but it is also a powerful QC tool because the measured amplitude trend can be compared with a theoretical trend computed from well logs or rock-physics models.

## Why AVO matters

At normal incidence, the reflection coefficient depends only on the impedance contrast. At non-normal incidence, the amplitude also depends on the contrast in Poisson's ratio and, in anisotropic media, on the azimuthal elastic properties. AVO therefore carries information beyond the stacked section about:

- lithology,
- fluid content (gas, oil, water),
- porosity,
- anisotropy and fractures.

## Shuey equation

The most common approximation is the **Shuey equation** (Shuey, 1985):

$$
R(\theta) = R_0 + G \sin^2\theta + F \sin^2\theta \tan^2\theta
$$

where:

- $R_0$ is the normal-incidence reflection coefficient (the **intercept**),
- $G$ is the AVO gradient,
- $F$ is the higher-order term,
- $\theta$ is the incidence angle.

For many practical purposes, the higher-order term is dropped and a two-term approximation is used:

$$
R(\theta) \approx R_0 + G \sin^2\theta
$$

In this form, a crossplot of intercept $R_0$ versus gradient $G$ is a standard AVO analysis tool. Different lithology and fluid combinations occupy different regions of the crossplot.

## AVO classes

Based on the intercept and gradient, AVO responses are often classified into classes (Rutherford and Williams, 1989):

| Class | $R_0$ | $G$ | Typical setting |
|-------|-------|-----|-----------------|
| Class 1 | High positive | Negative | Hard kick, e.g., tight sand over shale |
| Class 2 | Near zero | Variable | Weak response, often difficult to detect |
| Class 3 | Negative | Negative | Soft kick, classic gas sand response |
| Class 4 | Negative | Positive | Soft kick with increasing amplitude, e.g., low-impedance gas sands |

## Ruger equation for anisotropic media

For anisotropic media, the **Rüger equation** (Rüger, 1996) adds azimuthal terms. For a horizontally transverse isotropic (HTI) medium with a symmetry axis aligned with a fracture direction, the reflection coefficient depends on the azimuth $\phi$ relative to the symmetry axis:

$$
R(\theta, \phi) = R_0 + \left(G_\text{iso} + G_\text{aniso} \cos^2\phi\right) \sin^2\theta
$$

where $G_\text{iso}$ is the isotropic AVO gradient and $G_\text{aniso}$ is the anisotropic contribution. This forms the basis of **AVAz (amplitude versus azimuth)** analysis, used to detect fracture orientation and intensity. Rüger (1996) also extends the results to orthorhombic media, which are more realistic models for fractured reservoirs.

## Sources

- [Shuey (1985) — A simplification of the Zoeppritz equations](../sources/shuey_1985_simplification_of_zoeppritz_equations.md)
- [Rüger (1996) — Variation of P-wave reflectivity with offset and azimuth](../sources/ruger_1996_p_wave_reflectivity_offset_azimuth.md)

## AVO as a QC tool

AVO is a sensitive probe of amplitude fidelity. A mismatch between measured and theoretical AVO response can indicate:

- incorrect amplitude processing (e.g., AGC, residual source/receiver coupling),
- an incorrect or unstable wavelet,
- residual moveout or an incorrect velocity model,
- unresolved multiples,
- an inadequate rock-physics model.

Because AVO is sensitive to amplitude preservation, it must be performed on data that have been processed with relative amplitude preservation in mind. Any amplitude-scaling operation that is not physically motivated should be avoided before AVO analysis.

## AVO QC workflow

1. **Data preparation.** Ensure the data are NMO-corrected, properly gained, and have a known wavelet phase.
2. **Angle gather generation.** Convert offsets to incidence angles using a velocity model.
3. **Amplitude picking.** Pick amplitudes in a stable window around the target event.
4. **Trend fitting.** Fit the Shuey or Ruger equation to the picked amplitudes.
5. **Comparison.** Compare the measured intercept and gradient with theoretical values from well logs or rock-physics models.
6. **Diagnosis.** If the measured trend differs from theory, investigate amplitude processing, velocity, wavelet, and multiples before interpreting the anomaly geologically.

## Related concepts

- [Surface-consistent amplitude correction](surface_consistent_amplitude.md)
- [Amplitude effects](amplitude_effects.md)
- [Spherical divergence](spherical_divergence.md)
- [Automatic gain control](automatic_gain_control.md)
- [Seismic processing QC](seismic_processing_qc.md)
- [Seismic well tie](seismic_well_tie.md)
- [Seismic wavelet](seismic_wavelet.md)
- [Seismic velocities](seismic_velocities.md)
- [Velocity analysis](velocity_analysis.md)
