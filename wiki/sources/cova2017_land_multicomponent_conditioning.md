---
title: "Cova, Law & Innanen (2017) — Toward robust multicomponent FWI on land data: handling topography and data conditioning"
status: draft
type: report
source_file: wiki/sources/_raw_text/CRR201711.txt
language: en
concepts:
  - full_waveform_inversion
tags: [fwi, land, multicomponent, topography, data-conditioning]
---

# Cova, Law & Innanen (2017) — Land multicomponent FWI: topography and data conditioning

CREWES RESEARCH REPORT — VOLUME 29 (2017). University of Calgary.

## Overview

Examines what must be fixed in land multicomponent data before elastic FWI can converge: **topography handling** in forward modelling and systematic **data conditioning**. Motivated by the observation that successful multicomponent FWI case studies are overwhelmingly marine (OBC), while land remains difficult.

## Key takeaways

- Marine FWI benefits (high S/N, low frequencies, long offsets, simple water near-surface) are precisely what land data lack; multicomponent land adds free-surface/topography and mode-conversion complexity.
- Topography must be honoured in the modelling (boundary conditions on irregular surfaces) — mismatches map directly into phase errors that the inversion attributes wrongly to the subsurface.
- Data conditioning (geometry consistency, noise, receiver coupling consistency, component rotation) is a prerequisite: FWI compares full waveforms, so any non-reproducible data defect becomes a model error.

## Relation to lecture notes

Term 3 Lecture 07 §4 (land challenges: topography, coupling, data quality).

## Related sources

- [Wang et al. (2020)](wang2020_land_fwi_challenges.md) — industrial land FWI strategies.
- [Zhang & Dai (2015)](zhang2015_land_data_fwi.md) — BGP land FWI strategies.
