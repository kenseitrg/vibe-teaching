---
title: Term 3 Lecture 1 — Quality Control of Seismic Processing and Introduction to 3D Seismic Data
status: draft
lecture: term03_lec01_processing_qc_and_3d_introduction
sources:
  - vermeer_2012_3d_seismic_survey_design
  - cgg_odt01_data_analysis_part1
  - cgg_odt01_data_analysis_part2
  - hill_ruger_2020_illustrated_seismic_processing_preimaging
  - white_1997_accuracy_of_well_ties
  - walden_white_1998_seismic_wavelet_estimation
  - carvajal_2023_well_tie_tutorial
  - shuey_1985_simplification_of_zoeppritz_equations
  - ruger_1996_p_wave_reflectivity_offset_azimuth
concepts:
  - seismic_data_qc
  - seismic_processing_qc
  - seismic_well_tie
  - avo_analysis
  - seismic_acquisition
  - 3d_seismic_acquisition
  - common_midpoint
  - cross_spread_gather
  - ovt_cov_panels
  - grid_binning
  - seismic_data_sorts
  - seismic_velocities
  - velocity_analysis
  - normal_moveout
  - deconvolution
  - surface_consistent_deconvolution
  - frequency_filtering
  - radon_transform
tags: [term03, lecture-ready, QC, 3D, acquisition, well-tie, AVO, OVT, binning]
---

# Term 3 Lecture 1 — Quality Control of Seismic Processing and Introduction to 3D Seismic Data

## One-line summary

Verify each processing step with geometry, kinematic, noise, deconvolution, and demultiple QC; anchor the results to wells and AVO; then introduce the geometry, sorts, and binning of 3D seismic acquisition.

## Key concepts covered

- Input-data QC recap: geometry verification, attribute analysis, multi-attribute assessment, first-break QC.
- Processing-stage QC: flat gathers, stack quality, structural maps, residual NMO, difference sections, wavelet stability, lateral resolution, multiple residuals.
- Seismic well tie: synthetic seismogram, deterministic and statistical wavelets, correlation, phase rotation, wavelet shape.
- AVO analysis: Shuey and Ruger equations, comparing measured and theoretical AVO response.
- Interpretation-supervised processing (ИСО / WDS): using wells, geology, and rock physics to guide processing decisions.
- 3D acquisition: 5D prestack wavefield, template, salvo, swath, unit cell, acquisition parameters, 3D fold.
- Cross-spread gathers and OVT/COV panels: construction, offset/azimuth preservation, uses in 3D processing.
- Grid binning: bin size, fold uniformity, midpoint deviation, offset/azimuth distribution.

## Key equations

- Normal-incidence reflection coefficient from logs:

$$
R(t) = \frac{Z(t+\Delta t) - Z(t)}{Z(t+\Delta t) + Z(t)}
$$

- Shuey AVO equation:

$$
R(\theta) = R_0 + G \sin^2\theta + F \sin^2\theta \tan^2\theta
$$

- Inline and crossline offsets and midpoint coordinates:

$$
h_x = \frac{x_r - x_s}{2}, \qquad h_y = \frac{y_r - y_s}{2}
$$

$$
x_m = \frac{x_s + x_r}{2}, \qquad y_m = \frac{y_s + y_r}{2}
$$

- Nominal 3D fold for a regular orthogonal geometry:

$$
\text{fold} \approx \frac{N_x \, N_y}{2 \times \text{moveup}_x \times \text{moveup}_y}
$$

## Generated figures

| Figure | Path |
|--------|------|
| Input vs processing QC flow | `figures/term03_lec01/term03_lec01_input_vs_processing_qc.png` |
| 3D geometry elements | `figures/term03_lec01/term03_lec01_3d_geometry_elements.png` |
| Unit cell | `figures/term03_lec01/term03_lec01_unit_cell.png` |
| Cross-spread gather | `figures/term03_lec01/term03_lec01_cross_spread_gather.png` |
| OVT panel | `figures/term03_lec01/term03_lec01_ovt_panel.png` |
| Binning midpoint distribution | `figures/term03_lec01/term03_lec01_binning_midpoint_distribution.png` |

## Lecture materials

- Lecture notes (English): `lecture_notes/en/term03_lec01_processing_qc_and_3d_introduction.en.md`
- Slide outline: `slides/term03/lec01_processing_qc_and_3d_introduction/slide_outline.md`
- Starter deck: `slides/term03/lec01_processing_qc_and_3d_introduction/lec01_processing_qc_and_3d_introduction.pptx`
- Exercises: *(to be added)* `exercises/term03_lec01_processing_qc_and_3d_introduction.md`
- Russian notes: `lecture_notes/ru/term03_lec01_processing_qc_and_3d_introduction.ru.md`

## Related concept pages

- [Seismic data QC](../concepts/seismic_data_qc.md)
- [Seismic processing QC](../concepts/seismic_processing_qc.md)
- [Seismic well tie](../concepts/seismic_well_tie.md)
- [AVO analysis](../concepts/avo_analysis.md)
- [Seismic acquisition](../concepts/seismic_acquisition.md)
- [3D seismic acquisition](../concepts/3d_seismic_acquisition.md)
- [Common midpoint (CMP) and fold](../concepts/common_midpoint.md)
- [Seismic data sorts](../concepts/seismic_data_sorts.md)
- [Cross-spread gather](../concepts/cross_spread_gather.md)
- [OVT / COV panels](../concepts/ovt_cov_panels.md)
- [Grid binning](../concepts/grid_binning.md)

## Notes for instructor

- This is a survey lecture. The goal is to make students aware of the QC questions that should be asked at each stage, not to derive every equation.
- The term ИСО may be unfamiliar to English-speaking students; relate it to well-driven seismic (WDS) or interpreter-guided QC.
- For the 3D part, emphasize that 3D geometry is a sampling problem: the 5D wavefield cannot be densely sampled everywhere, so design is a trade-off.
- The unit cell is the key abstraction that connects source/receiver line spacing to midpoint coverage and fold.
- Cross-spreads and OVT panels are best explained with a sketch of source and receiver lines.

## Comprehension questions

1. Why is a difference section the main QC tool for noise attenuation?
2. What residual-NMO signature tells you that the stacking velocity is too low?
3. Name two well-tie metrics and explain what each reveals.
4. How does the unit cell affect the spatial continuity of a 3D survey?
5. What is the advantage of an OVT panel over a simple CMP gather?
6. Why does fold vary in both inline and crossline directions in 3D?
7. How can a mismatch between measured and theoretical AVO response point to a processing problem?
8. Why is binning QC important before stacking or migration?
