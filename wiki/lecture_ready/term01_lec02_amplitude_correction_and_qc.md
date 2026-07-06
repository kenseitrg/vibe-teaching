---
title: Term 1 Lecture 02 — Amplitude Corrections and Quality Control of Input Data
status: lecture-ready
lecture: term01_lec02
sources:
  - yilmaz_practical_seismic_data_analysis_amplitude
  - hill_introduction_to_seismic_processing_ch21
  - brown_2002_surface_consistent_amplitude_correction
  - cgg_odt01_data_analysis_part1
  - cgg_odt01_data_analysis_part2
tags:
  - amplitude-correction
  - spherical-divergence
  - AGC
  - surface-consistent-amplitude
  - quality-control
  - geometry-verification
---

# Term 1 Lecture 02 — Amplitude Corrections and Quality Control of Input Data

## One-line summary

Understand why seismic amplitudes decay, distinguish true-amplitude preservation from display equalization, apply the main correction methods, and verify input geometry before any processing step.

## Key concepts covered

- Physical amplitude effects during propagation: reflection/transmission, mode conversion, geometric spreading, absorption, scattering, and near-surface source/receiver effects.
- True amplitude / relative amplitude preservation versus amplitude equalization for intermediate visualization and kinematic processing.
- Spherical divergence correction: energy conservation, $t^n$ gain conventions, physics of $t^2$, curved-ray / layered-earth approximations.
- Deterministic amplitude equalization: trace normalization (max, mean, RMS) and AGC; window-length effects; why AGC destroys AVO information.
- Surface-consistent amplitude correction: four-factor multiplicative model, log-linear system, Gauss–Seidel iteration, 2-factor vs. 4-factor trade-offs, handling the CMP/geology term.
- Input-data QC: geometry verification, offset-curve overlays, LMO stacks, first-break residuals, amplitude/correlation/spectral attributes, statistical and map-based QC.

## Key equations

- Reflection coefficient at normal incidence:

$$
R = \frac{Z_2 - Z_1}{Z_2 + Z_1}, \qquad Z = \rho v
$$

- Spherical divergence gain (general form):

$$
G(t) = t^n
$$

commonly $n = 1$ (amplitude gain) or $n = 2$ (energy gain).

- Layered-earth curved-ray approximation:

$$
A \propto \frac{1}{t \, V_{\text{rms}}^2(t)}
$$

- RMS amplitude:

$$
A_{\text{rms}} = \sqrt{\frac{1}{N} \sum_{n=1}^{N} a_n^2}
$$

- Surface-consistent amplitude model:

$$
A_{ij} = S_i \, R_j \, G_k \, M_l
$$

and its log-linear form:

$$
\log A_{ij} = \log S_i + \log R_j + \log G_k + \log M_l
$$

- Direct-arrival / first-break time for near-surface QC:

$$
t(x) = \frac{x}{v_{\text{near}}}
$$

## Generated figures

| Figure | Path |
|--------|------|
| Amplitude-effects ray diagram | `figures/term01_lec02/term01_lec02_amplitude_effects_ray_diagram.png` |
| Spherical divergence correction | `figures/term01_lec02/term01_lec02_spherical_divergence_correction.png` |
| AGC example | `figures/term01_lec02/term01_lec02_agc_example.png` |
| Surface-consistent amplitude correction | `figures/term01_lec02/term01_lec02_surface_consistent_amplitude.png` |
| Geometry QC: first breaks and LMO | `figures/term01_lec02/term01_lec02_qc_geometry_first_breaks.png` |
| Receiver-index amplitude QC map | `figures/term01_lec02/term01_lec02_qc_amplitude_map.png` |

## Lecture materials

- English notes: `lecture_notes/en/term01_lec02_amplitude_correction_and_qc.en.md`
- Outline: `lecture_notes/_drafts/term01_lec02_amplitude_correction_and_qc_outline.md`
- Exercises: *(to be added)* `exercises/term01_lec02_amplitude_correction_and_qc.md`
- Russian notes: *(to be added)* `lecture_notes/ru/term01_lec02_amplitude_correction_and_qc.ru.md`
- Slide outline: *(to be added)* `slides/term01/lec02_amplitude_correction_and_qc/slide_outline.md`
- Starter deck: *(to be added)* `slides/term01/lec02_amplitude_correction_and_qc/lec02_amplitude_correction_and_qc.pptx`

## Related concept pages

- [Amplitude effects](../concepts/amplitude_effects.md)
- [Spherical divergence](../concepts/spherical_divergence.md)
- [Automatic gain control](../concepts/automatic_gain_control.md)
- [Surface-consistent amplitude correction](../concepts/surface_consistent_amplitude.md)
- [Seismic data QC](../concepts/seismic_data_qc.md)

## Notes for instructor

- This is the new Lecture 2. It replaces the previous placeholder topic (data formats and data loading), which is now assumed to be covered briefly in Lecture 1 or moved to a practical session.
- Emphasize the **two philosophies** early: true-amplitude preservation is not the same as making the data visible. Students often confuse AGC with amplitude correction.
- The $t^n$ discussion is a common source of confusion. Be explicit about whether the software is working with amplitude or energy, and avoid deriving the $t^2$ form purely as a rule of thumb.
- For SCAC, keep the Gauss–Seidel explanation conceptual. The goal is for students to understand what is being separated and why, not to implement the iteration.
- Geometry QC should be stressed as the **first step** before any amplitude correction. A geometry error cannot be fixed by an amplitude correction.
- The planned figures are placeholders; the Python scripts to generate them are deferred.
