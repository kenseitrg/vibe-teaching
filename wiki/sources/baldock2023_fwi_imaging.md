---
title: "Baldock et al. (2023) — FWI Imaging: the future or merely derivative?"
status: draft
type: paper
source_file: wiki/sources/_raw_text/1278.txt
language: en
concepts:
  - full_waveform_inversion
tags: [fwi-imaging, reflectivity, derivative, rtm, campos-basin, clair]
---

# Baldock et al. (2023) — FWI Imaging: the future or merely derivative?

84TH EAGE ANNUAL CONFERENCE & EXHIBITION — WORKSHOP PROGRAMME. TGS.

## Overview

"FWI imaging" = producing reflectivity images directly from high-resolution FWI velocity models by taking a form of the **spatial derivative of velocity** (1D derivative, 3D derivative along dominant dip, or plane-wave destructor), instead of migrating the data again. The paper shows marine examples (Campos Basin narrow-azimuth towed streamer; West of Shetlands/Clair) where FWI images compete with — or replace — Kirchhoff/RTM products, and discusses remaining challenges.

## Key takeaways

- FWI imaging is a **byproduct** of the velocity model: the workflow collapses (FWI → derivative image), skipping separate model building + migration QC loops.
- Why it works: a high-resolution FWI model already contains reflectivity-band information; the derivative turns sharp velocity contrasts (wavelength-scale and below) into apparent reflectivity.
- Examples: better pre-salt fault-block imaging under salt (Campos), crisper shallow layering and fault planes vs RTM (Clair), RTM migrated with FWI model improves where the FWI image complements it.
- Challenges noted: velocity-derived "reflectivity" is not true impedance reflectivity (no density/AVO), dependence on FWI bandwidth and preprocessing, quantitative use still maturing.

## Relation to lecture notes

Term 3 Lecture 07 §3 (FWI imaging as a byproduct; Figs. 3 and 5 reused: FWI image vs RTM comparisons).

## Related sources

- Kalinicheva et al. (2020), Zhang et al. (2020), McLeman et al. (2021) — method origins cited within.
- [Jones (2019)](jones2019_fwi_mechanics_tutorial.md) — FWI models as constraints for impedance inversion.
