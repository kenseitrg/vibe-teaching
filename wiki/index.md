# Seismic Data Processing Wiki — Index

This wiki is a persistent, compounding knowledge base for the undergraduate seismic data processing course. It sits between the raw paper/PPT library (`papers/`) and the lecture materials (`lecture_notes/`, `slides/`, `figures/`).

## Quick navigation

- [Concepts](#concepts)
- [Techniques](#techniques)
- [Sources](#sources)
- [Comparisons](#comparisons)
- [Lecture-ready pages](#lecture-ready-pages)
- [Log](log.md)

---

## Concepts

| Page | Summary | Status |
|------|---------|--------|
| [Deconvolution](concepts/deconvolution.md) | Inverse filtering to remove wavelet/reverberation effects | draft |
| [Seismic velocities](concepts/seismic_velocities.md) | Interval, average, RMS, NMO and stacking velocity definitions | draft |
| [Normal moveout](concepts/normal_moveout.md) | Offset-dependent reflection traveltime and NMO correction | draft |
| [Velocity analysis](concepts/velocity_analysis.md) | Estimating stacking/NMO velocity from CMP gathers | draft |
| [Static corrections](concepts/static_corrections.md) | Near-surface time shifts and datum corrections | draft |
| [Residual statics](concepts/residual_statics.md) | Surface-consistent residual statics and Gauss–Seidel solution | draft |
| [Floating datum](concepts/floating_datum.md) | Smoothed datum for NMO and velocity analysis | draft |
| [Layer replacement](concepts/layer_replacement.md) | Long-wavelength statics from overburden replacement | draft |
| [Seismic wavelet](concepts/seismic_wavelet.md) | Components of the recorded wavelet: signature, ghosts, bubble | draft |
| [Minimum phase wavelet](concepts/minimum_phase.md) | Causal front-loaded wavelet and the dipole proof | draft |
| [Deterministic deconvolution](concepts/deterministic_deconvolution.md) | Deconvolution with a known or measured wavelet | draft |
| [Statistical deconvolution](concepts/statistical_deconvolution.md) | Estimating the inverse filter from the data itself | draft |
| [Predictive deconvolution](concepts/predictive_deconvolution.md) | Removing repetitive signals by prediction error filtering | draft |
| [Radon transform](concepts/radon_transform.md) | Transform data to ray-parameter domain for filtering and deconvolution | draft |
| [Surface-consistent deconvolution](concepts/surface_consistent_deconvolution.md) | Separating source/receiver coupling and near-surface effects | draft |
| [Wiener filter](concepts/wiener_filter.md) | Optimal least-squares shaping filter and normal equations | draft |
| [Seismic data processing](concepts/seismic_data_processing.md) | Overview, goals, and typical processing flow | draft |
| [Seismic acquisition](concepts/seismic_acquisition.md) | 2D acquisition essentials, CMP method, parameters | draft |
| [Common midpoint (CMP)](concepts/common_midpoint.md) | CMP/CDP gather, fold, stacking | draft |
| [Seismic data sorts](concepts/seismic_data_sorts.md) | Shot, receiver, CMP, offset gathers and their uses | draft |
| [Seismic data formats](concepts/seismic_data_formats.md) | SEGY, SEGD, SPS, UKOOA and data loading | draft |

## Techniques

| Page | Summary | Status |
|------|---------|--------|
| *(none yet)* | | |

## Sources

| Page | Document | Type | Status |
|------|----------|------|--------|
| [Hutchinson & Link (1984)](sources/hutchinson_link_1984_surface_consistency.md) | Surface consistency: A solution to the problem of deconvolving noisy seismic data | paper | summarized |
| [Verschuur (2006)](sources/verschuur_2006_predictive_deconvolution.md) | EAGE EET 03 — Predictive Deconvolution | course slides | summarized |
| [CGG ODT04 Part 1](sources/cgg_odt04_deconvolution_part1_wavelet.md) | ODT04 Deconvolution Part 1: The Seismic Wavelet | training slides | summarized |
| [Hatton, Worthington & Makin (1986)](sources/hatton_worthington_makin_1986_seismic_data_processing.md) | Seismic Data Processing: Theory and Practice | textbook | reviewed |
| [Margrave (2006)](sources/margrave_2006_methods_of_seismic_data_processing.md) | Methods of Seismic Data Processing — lecture notes | lecture notes | reviewed |
| [Yilmaz (2001) Vol. 1](sources/yilmaz_2001_seismic_data_analysis_deconvolution.md) | Seismic Data Analysis — deconvolution chapter | textbook | reviewed |
| [Hill & Rüger (2020)](sources/hill_ruger_2020_illustrated_seismic_processing_preimaging.md) | Illustrated Seismic Processing, Vol. 2: Preimaging | textbook | summarized |
| [CGG ODT01 Part 1](sources/cgg_odt01_data_analysis_part1.md) | Data Analysis Part 1: recorded wavefield, shot and CMP gathers | training slides | summarized |
| [CGG ODT01 Part 2](sources/cgg_odt01_data_analysis_part2.md) | Data Analysis Part 2: 2D/3D geometry, sorts, aliasing, noise/multiples | training slides | summarized |
| [Noble (2020)](sources/noble_2020_whats_the_datum.md) | What's the Datum? — datums and replacement velocity | conference presentation | reviewed |
| [Jones (2012)](sources/jones_2012_incorporating_near_surface_velocity_anomalies.md) | Near-surface velocity anomalies in pre-stack depth migration | journal article | reviewed |
| [Refraction Seismic notes](sources/refraction_seismic_university_notes.md) | Refraction Seismic Method — delay-time methods | course notes | reviewed |
| [SEG-Y rev 2.0](sources/seg_y_rev2_format.md) | SEG-Y rev 2.0 Data Exchange format | technical standard | draft |
| [SEG SPS rev 2.1](sources/seg_sps_format_rev21.md) | Shell Processing Support format for 3D surveys | technical standard | draft |
| [Vermeer (2012)](sources/vermeer_2012_3d_seismic_survey_design.md) | 3D Seismic Survey Design, 2nd ed. | textbook | draft |

## Comparisons

| Page | Summary | Status |
|------|---------|--------|
| [Deconvolution methods](comparisons/deconvolution_methods.md) | Side-by-side comparison of deconvolution techniques | draft |

## Lecture-ready pages

| Page | Lecture | Status |
|------|---------|--------|
| [Term 1 Lecture 1 — Introduction to seismic data processing](lecture_ready/term01_lec01_introduction_to_seismic_processing.md) | term01_lec01 | lecture-ready |
| [Term 1 Lecture 2 — Kinematics, Velocities and Field Statics](lecture_ready/term01_lec02_kinematics_and_field_statics.md) | term01_lec02 | lecture-ready |
| [Term 1 Lecture 3 — Advanced Statics and the Link to Velocity Analysis](lecture_ready/term01_lec03_advanced_statics_and_velocity_link.md) | term01_lec03 | lecture-ready |
| [Term 1 Lecture 6 — Single-channel deconvolution](lecture_ready/term01_lec06_single_channel_deconvolution.md) | term01_lec06 | draft |
| [Term 1 Lecture 7 — Surface-consistent deconvolution](lecture_ready/term01_lec07_surface_consistent_deconvolution.md) | term01_lec07 | draft |

---

## Maintenance notes

- Status values: `stub`, `draft`, `reviewed`, `lecture-ready`.
- Source summary pages should link to every concept they inform.
- Concept pages should list sources in their frontmatter.
- Update this index whenever a new page is added or a status changes.
