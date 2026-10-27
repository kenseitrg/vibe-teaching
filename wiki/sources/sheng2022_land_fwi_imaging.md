---
title: "Sheng, Reta-Tang, Liu, Vázquez Cantú & Cabrales Vargas (2022) — Full-waveform inversion and FWI imaging for land data"
status: draft
type: paper
source_file: wiki/sources/_raw_text/FWI_FWI_Imaging_Land_FINAL.submitted.txt
language: en
concepts:
  - full_waveform_inversion
  - fwi_cycle_skipping
tags: [fwi, land, dm fwi, dynamic-matching, cross-correlation, fwi-imaging, mexico]
---

# Sheng et al. (2022) — Full-waveform inversion and FWI imaging for land data

TGS / PEMEX SUBMITTED ABSTRACT (PDF dated September 2022; venue not printed on the manuscript).

## Overview

A land model-building and imaging workflow built around **dynamic-matching full-waveform inversion (DMFWI)** — an objective function based on multi-dimensional local cross-correlations that suppresses the influence of amplitudes and remains reliable in strong noise — applied to onshore surveys in Mexico, followed by **FWI imaging** (reflectivity estimated from the high-resolution FWI velocity model) as an alternative image for poor-S/N land data.

## Key takeaways

- **Land obstacles** (their framing): topography/datum differences, heterogeneous weathering layer producing complex elastic waves, ground roll on vertical geophones; near-surface model building traditionally by refraction tomography + statics. Even elastic FWI can mis-estimate near-surface P-velocity (citing Yilmaz et al. 2022).
- **DMFWI misfit**: multi-dimensional local cross-correlation objective — a member of the cross-correlation/time-shift misfit family that tolerates amplitude errors and cycle-skipping better than raw L2 (cf. our §2.7 "misfit modifications").
- **Workflow**: tomography-derived starting model → DMFWI updates; QC by gather flatness (Kirchhoff CIGs flatten after the update) and image quality.
- **Results**: Kirchhoff PSDM and RTM images sharpen over the faulted target; FWI images from the derivative of the FWI model provide a noise-robust alternative reflectivity product on poor-S/N land data.

## Relation to lecture notes

Term 3 Lecture 07 §4.3 (land challenges — case study; Fig. 2 Kirchhoff before/after reused, Fig. 3 RTM before/after on the slides) and §3.2 (FWI imaging on land).

## Related sources

- [Baldock et al. (2023)](baldock2023_fwi_imaging.md) — marine FWI imaging counterpart.
- [Wang et al. (2020)](wang2020_land_fwi_challenges.md), [Zhang & Dai (2015)](zhang2015_land_data_fwi.md) — other land FWI strategies.
