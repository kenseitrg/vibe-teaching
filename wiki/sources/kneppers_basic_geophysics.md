---
title: Kneppers — Basic Geophysics: Noise Attenuation
status: draft
source_type: training slides
authors: "Angeline Kneppers"
year: null
source_file: papers/noise_attenuation/Angeline_Kneppers_Basic_Geophysics.pptx
lectures:
  - term03_lec04
related_concepts:
  - seismic_noise
  - frequency_filtering
  - spectral_analysis
  - deconvolution
  - radon_transform
tags: [noise-attenuation, signal-processing, fk-filter, muting, coherent-noise, random-noise]
---

# Kneppers — Basic Geophysics: Noise Attenuation

Kneppers, A. *Basic Geophysics — Noise Attenuation*. Training slides.

## Main message

An introductory training module defining signal, noise, and signal-to-noise ratio, classifying noise into coherent and random categories, and surveying the main noise-attenuation techniques used in seismic processing: frequency filtering, amplitude-based editing (despike, deband, RNA), velocity/dip filtering (FK), muting, stacking, and deconvolution. Includes worked exercises on FK-domain representation of dipping events and spatial aliasing.

## Key points

1. **Signal vs. noise:** Signal carries desired information; noise contains unwanted energy. S/N ratio = energy(signal) / energy(noise) or energy(signal) / total energy.
2. **Random noise:** Uncorrelated from trace to trace; not source-generated (swell, wind, traffic, instrument noise). Removed by stacking, bandpass filtering, despike, f-x filtering.
3. **Coherent noise:** Predictable trace-to-trace; often source-generated (multiples, ground roll, airwave, refractions, cable jerk). Removed by velocity/dip filtering (FK), deconvolution, muting.
4. **Noise removal attributes:** Frequency, amplitude, velocity/dip, two-way travel time. Each attribute motivates a class of processing tools.
5. **FK filter:** Transforms data to frequency-wavenumber domain where events of different dip map to different regions. Pass zone, reject zone, and taper zone are defined. The relationship k = f × dip / trace-spacing links temporal frequency, dip, and wavenumber.
6. **Spatial aliasing:** Occurs when the phase shift between traces exceeds 180°. Aliasing frequency f_alias = V_apparent / (2 × dx). Steeper dips and coarser trace spacing increase aliasing.
7. **Muting types:** First-break mute, inner-trace mute (multiples), tail mute (autofires), surgical mute (spikes), NMO stretch mute. All zero amplitude values in selected regions.
8. **Stacking as noise attenuation:** If noise appears on only one trace in an N-fold CMP, stacking reduces its contribution by factor N.

## Relation to lecture notes

This source provides the foundational vocabulary and classification scheme used throughout Term 3 Lecture 04. The FK-domain exercises (mapping dipping events, understanding wavenumber units, recognising aliasing) directly support the lecture's treatment of velocity filtering and spatial sampling requirements.

## Related concepts

- [Seismic noise](../concepts/seismic_noise.md)
- [Frequency filtering](../concepts/frequency_filtering.md)
- [Spectral analysis](../concepts/spectral_analysis.md)
- [Deconvolution](../concepts/deconvolution.md)
- [Radon transform](../concepts/radon_transform.md)
