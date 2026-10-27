---
title: "Wang, Chen, Zhuang, Mei & Wang (2020) — Land FWI: challenges and possibilities"
status: draft
type: paper
source_file: wiki/sources/_raw_text/Land_FWI_Challenges_and_possibilities_Final_Published.txt
language: en
concepts:
  - full_waveform_inversion
tags: [fwi, land, topography, near-surface, noise, curvilinear-grid, permian-basin, alaska]
---

# Wang et al. (2020) — Land FWI: challenges and possibilities

82ND EAGE ANNUAL CONFERENCE & EXHIBITION. CGG.

## Overview

A field-data-driven summary of why land FWI is harder than marine FWI, and three practical strategies: (1) **curvilinear-grid topography modelling**, (2) **near-surface noise mitigation on both input and synthetic data**, (3) **stable cost functions** for cycle-skipping and amplitude issues. Demonstrated on two land surveys (Permian Basin; Tabasco, Alaska).

## Key takeaways

- **Why land is harder:** irregular topography (staircase-scattering artifacts on Cartesian grids), a highly complex near-surface (strong guided/shallow wavefield energy in synthetics that has no counterpart in field data), and the universal cycle-skipping + amplitude problems — land data typically lack the very low frequencies and long offsets that made marine FWI routine.
- **Topography:** curvilinear-coordinate acoustic wave equation (Shragge 2014) conforms the grid to topography, removing staircase artifacts; extends to VTI/TTI.
- **Near-surface effects:** attenuate the shallow guided wavefield **in the synthetic data too** (empirical scaling during modelling), so that field and modelled data are comparable and the gradient is not dominated by non-reproducible shallow energy. Noise attenuation (e.g. Le Meur et al. 2008 surface-wave method) is applied to field data.
- **Results:** FWI-updated models flatten image gathers (residual moveout removed), improve Kirchhoff focusing and continuity (Permian Basin), and reveal coherent near-surface structure in depth slices (Tabasco).

## Relation to lecture notes

Term 3 Lecture 07 §4 (land challenges; Figures 2 and 3 of the paper reused: noise conditioning and Permian Basin before/after).

## Related sources

- [Zhang & Dai (2015)](zhang2015_land_data_fwi.md) — BGP land FWI strategy (SPE).
- [Cova, Law & Innanen (2017)](cova2017_land_multicomponent_conditioning.md) — land data conditioning for multicomponent FWI.
