---
title: "Pratt (1999) — Seismic waveform inversion in the frequency domain, Part 1"
status: draft
type: paper
source_file: wiki/sources/_raw_text/pratt1999.txt
language: en
concepts:
  - full_waveform_inversion
  - fwi_cycle_skipping
tags: [fwi, frequency-domain, crosswell, resolution, starting-model, fresnel-zone]
---

# Pratt (1999) — Seismic waveform inversion in the frequency domain, Part 1

GEOPHYSICS, VOL. 64, NO. 3 (MAY–JUNE 1999); P. 888–901. With co-authors on Part 2 (Shin & Hicks).

## Overview

Classic verification of frequency-domain waveform inversion on a **physical scale model** (epoxy-resin crosswell experiment, 55×120 m at 1:1000 scale). Demonstrates on controlled data: (1) the resolution gap between ray tomography and FWI, (2) the frequency-continuation strategy, (3) the starting-model requirement, (4) the role of attenuation (Q) in matching amplitudes.

## Key takeaways

- **Frequency-domain formulation:** invert a few discrete frequencies at a time; each frequency is a complex-valued data set (amplitude + phase). Successive low→high frequency batches behave like a multiscale continuation; a handful of frequencies (4–5 per batch) suffices — the results of a few frequencies compare well with time-domain inversion.
- **Starting model:** waveform inversion is a local, descent method — the starting model must predict waveforms to **within half a wavelength (half a period)** of the observations, otherwise the inversion matches the wrong cycle. Traveltime (ray) tomography provides robust but low-resolution starting models.
- **Resolution comparison (Fig. 3 vs Figs. 7/9):** curved-ray traveltime tomography resolves only features larger than about the **first Fresnel zone width** $\sqrt{\lambda L}$ (~15 m in the experiment) — the small fault and semi-circular channel are invisible; waveform inversion resolves details at the **wavelength scale** (~5 m) and below — the fault and channel are recovered.
- **Attenuation matters:** inverting with wrong Q (100 vs true ~10) produced artifacts (X-shaped crosstalk); amplitude behaviour constrains Q, and realistic Q must be included in forward modelling to match amplitudes.
- **Data fit QC:** frequency-domain complex data panels (observed vs modelled vs residual, per source–receiver pair) directly show where the model explains the data.

## Relation to lecture notes

Term 3 Lecture 07 §1 (ray resolution limit, Fig. 3 and Fig. 7 of the paper reused) and §2 (frequency continuation, starting-model criterion), §4 (absorption challenge).

## Related sources

- [Tarantola (1984)](tarantola1984_inversion_acoustic.md) — time-domain origin of the method.
- [Jones (2019)](jones2019_fwi_mechanics_tutorial.md) — modern industrial view of the same workflow.
