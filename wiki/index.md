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
| [Predictive deconvolution](concepts/predictive_deconvolution.md) | Removing repetitive signals by prediction error filtering | draft |
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

## Comparisons

| Page | Summary | Status |
|------|---------|--------|
| [Deconvolution methods](comparisons/deconvolution_methods.md) | Side-by-side comparison of deconvolution techniques | draft |

## Lecture-ready pages

| Page | Lecture | Status |
|------|---------|--------|
| *(none yet)* | | |

---

## Maintenance notes

- Status values: `stub`, `draft`, `reviewed`, `lecture-ready`.
- Source summary pages should link to every concept they inform.
- Concept pages should list sources in their frontmatter.
- Update this index whenever a new page is added or a status changes.
