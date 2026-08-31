---
title: Seismic data processing — overview
status: draft
sources:
  - hill_ruger_2020_illustrated_seismic_processing_preimaging
  - cgg_odt01_data_analysis_part1
  - cgg_odt01_data_analysis_part2
  - margrave_2006_methods_of_seismic_data_processing
tags: [seismic-processing, workflow, kinematics, dynamics, inversion]
---

# Seismic data processing — overview

Seismic data processing turns raw recorded wavefields into images and measurements that interpreters can use to understand the subsurface.

## Why processing is needed

A seismic trace records a complicated superposition of:

- **Useful signal**: primary reflections and diffractions from geological boundaries.
- **Noise**: random background noise, coherent noise (ground roll, airwave, shot interference), and unwanted but organized energy (refractions, multiples).
- **Acquisition effects**: source and receiver positions, instrument responses, spatial sampling, and timing.
- **Wave propagation effects**: geometric spreading, absorption, transmission losses, multiples, mode conversions, anisotropy.

The processor must remove or compensate for the unwanted effects while preserving the geology.

## Two linked problems

| Problem | Question | Typical tools |
|---------|----------|---------------|
| **Kinematic** | Where in space and time does the energy belong? | Statics, NMO, DMO, velocity analysis, migration |
| **Dynamic** | What are the true relative amplitudes and wavelet character? | Gain recovery, deconvolution, Q-compensation, noise attenuation, demultiple |

In modern processing these two problems are often solved iteratively: a better velocity model improves imaging, and a better image improves amplitude interpretation.

## A typical processing flow

The exact sequence varies with acquisition (land vs. marine) and geology, but a broad outline is:

1. **Preprocessing**
   - Load SEG-Y/SEG-D traces.
   - Assign geometry from SPS/UKOOA and perform QC.
   - Apply field statics and a first rough velocity to produce a **brute stack**.

2. **Kinematic processing**
   - Refine statics corrections.
   - Build stacking (RMS) velocities.
   - Eventually build a velocity model for imaging.

3. **Dynamic processing**
   - Noise attenuation and demultiple.
   - Amplitude and wavelet processing (deconvolution, Q-compensation).
   - Regularization and interpolation.

4. **Imaging and post-imaging**
   - Migration places energy at its correct subsurface position.
   - Post-migration conditioning tailors the result for interpretation.

## Fundamental limitations

- **Wavelength limits resolution**: the smallest separable feature is on the order of the seismic wavelength.
- **Acquisition limits sampling**: finite receiver spacing, aperture, and fold restrict what can be recovered.
- **Inverse-problem ambiguity**: different earth models can produce similar data; additional information (wells, geology, prior models) is required.
- **Cost and volume**: modern surveys produce terabytes of data and require large computational resources.

## Relation to the rest of the course

- Term 1 builds the foundations: geometry, statics, velocities, deconvolution.
- Term 2 covers intermediate methods: absorption, FK/Radon filtering, multiples, imaging fundamentals.
- Term 3 moves to 3D geometry and modern techniques.

## Sources

- Hill & Rüger (2020), *Illustrated Seismic Processing, Vol. 2*, Appendix A–B and Chapter 31.
- CGG ODT01 Data Analysis Part 1, §§1–6.
- CGG ODT01 Data Analysis Part 2, §§7–13.
- Margrave (2006), *Methods of Seismic Data Processing*, Chapter 1.

## Related lecture

- [Term 1 Lecture 1 — Introduction to seismic data processing](../lecture_ready/term01_lec01_introduction_to_seismic_processing.md)
