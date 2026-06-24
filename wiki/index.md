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
| [Seismic wavelet](concepts/seismic_wavelet.md) | Components of the recorded wavelet: signature, ghosts, bubble | draft |
| [Minimum phase wavelet](concepts/minimum_phase.md) | Causal front-loaded wavelet and the dipole proof | draft |
| [Deterministic deconvolution](concepts/deterministic_deconvolution.md) | Deconvolution with a known or measured wavelet | draft |
| [Statistical deconvolution](concepts/statistical_deconvolution.md) | Estimating the inverse filter from the data itself | draft |
| [Predictive deconvolution](concepts/predictive_deconvolution.md) | Removing repetitive signals by prediction error filtering | draft |
| [Radon transform](concepts/radon_transform.md) | Transform data to ray-parameter domain for filtering and deconvolution | draft |
| [Surface-consistent deconvolution](concepts/surface_consistent_deconvolution.md) | Separating source/receiver coupling and near-surface effects | draft |
| [Wiener filter](concepts/wiener_filter.md) | Optimal least-squares shaping filter and normal equations | draft |

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

## Comparisons

| Page | Summary | Status |
|------|---------|--------|
| [Deconvolution methods](comparisons/deconvolution_methods.md) | Side-by-side comparison of deconvolution techniques | draft |

## Lecture-ready pages

| Page | Lecture | Status |
|------|---------|--------|
| [Term 1 Lecture 6 — Single-channel deconvolution](lecture_ready/term01_lec06_single_channel_deconvolution.md) | term01_lec06 | draft |
| [Term 1 Lecture 7 — Surface-consistent deconvolution](lecture_ready/term01_lec07_surface_consistent_deconvolution.md) | term01_lec07 | draft |

---

## Maintenance notes

- Status values: `stub`, `draft`, `reviewed`, `lecture-ready`.
- Source summary pages should link to every concept they inform.
- Concept pages should list sources in their frontmatter.
- Update this index whenever a new page is added or a status changes.
