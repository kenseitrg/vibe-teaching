---
title: Term 1 Lecture 02 — Kinematics, Velocities and Field Statics
status: lecture-ready
lecture: term01_lec02
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - cgg_odt01_data_analysis_part1
  - cgg_odt01_data_analysis_part2
  - noble_2020_whats_the_datum
  - refraction_seismic_university_notes
  - hutchinson_link_1984_surface_consistency
tags:
  - nmo
  - velocity-analysis
  - statics
  - refraction
  - kinematic-processing
---

# Term 1 Lecture 02 — Kinematics, Velocities and Field Statics

## One-line summary

The first half of the kinematics/statics lecture: velocity definitions, NMO correction, velocity analysis, field statics and refraction-based near-surface model building.

## Key concepts covered

- Seismic velocity models and ray assumptions: interval, average, RMS, NMO, stacking.
- Goal of kinematic processing: remove offset-dependent traveltime and near-surface delays to obtain a zero-offset stack section.
- NMO correction: hyperbolic equation, under/over-correction, stretch, muting, residual moveout.
- Velocity analysis: vertical/horizontal spectra, semblance, advantages over simple normalization.
- Static correction fundamentals: origin, short vs long wavelength, vertical-ray assumption, datums, replacement velocity.
- Near-surface model building: sources of information, refraction problem statement, delay-time methods (Hagedoorn, GRM, GLI), mention of tomography.

## Key equations

- Average velocity: $V_\text{avg} = \frac{\sum v_i \Delta t_i}{\sum \Delta t_i}$
- RMS velocity: $V_\text{rms}^2 = \frac{\sum v_i^2 \Delta t_i}{\sum \Delta t_i}$
- Hyperbolic moveout: $t^2(x) = t_0^2 + x^2/V_\text{nmo}^2$
- NMO correction: $\Delta t_\text{nmo} = \sqrt{t_0^2 + x^2/V_\text{nmo}^2} - t_0$
- Semblance: $S(t_0, V) = \frac{1}{M} \frac{\sum_\tau [\sum_i u_i(\tau - \Delta t_i)]^2}{\sum_\tau \sum_i u_i^2(\tau - \Delta t_i)}$

## Generated figures

| Figure | Path |
|--------|------|
| Velocity definitions | `figures/term01_lec02/term01_lec02_velocity_definitions.png` |
| NMO correction | `figures/term01_lec02/term01_lec02_nmo_correction.png` |
| Under/over-correction | `figures/term01_lec02/term01_lec02_nmo_under_over.png` |
| NMO stretch and mute | `figures/term01_lec02/term01_lec02_nmo_stretch_mute.png` |
| Velocity spectrum | `figures/term01_lec02/term01_lec02_velocity_spectrum.png` |
| Statics datums | `figures/term01_lec02/term01_lec02_statics_datums.png` |
| Refraction geometry | `figures/term01_lec02/term01_lec02_refraction_geometry.png` |

## Lecture materials

- English notes: `lecture_notes/en/term01_lec02_kinematics_and_field_statics.en.md`
- Rendered PDF: `lecture_notes/en/term01_lec02_kinematics_and_field_statics.en.pdf`
- Exercises: `exercises/term01_lec02_kinematics_and_field_statics.md`
- Slide outline: `slides/term01/lec02_kinematics_and_field_statics/slide_outline.md`
- Starter deck: `slides/term01/lec02_kinematics_and_field_statics/lec02_kinematics_and_field_statics.pptx`

## Related concept pages

- [NMO / normal moveout](../concepts/normal_moveout.md)
- [Velocity analysis](../concepts/velocity_analysis.md)
- [Static corrections](../concepts/static_corrections.md)
- [Seismic velocities](../concepts/seismic_velocities.md)

## Notes for instructor

- This lecture is the first half of the original "kinematics and statics" lecture.  The second half (Lecture 03) covers layer replacement, residual statics and the floating-datum link.
- Timing is tight; keep worked examples short and let the figures carry the intuition.
- The stretch/mute figure is particularly useful for explaining why mute zones are non-negotiable before stack.
