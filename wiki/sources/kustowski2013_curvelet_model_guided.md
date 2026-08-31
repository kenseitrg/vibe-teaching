---
title: "Kustowski et al. (2013) — Curvelet Noise Attenuation Guided by a Signal or Noise Model"
status: draft
type: paper
source_file: papers/noise_attenuation/curvelets/kustowski2013.txt
language: en
concepts:
  - seismic_data_processing
  - seismic_noise
  - adaptive_subtraction
tags: [noise-attenuation, curvelet, guided-filtering, multiple-attenuation, migration-artifacts, ocean-bottom-seismic]
---

# Kustowski et al. (2013) — Curvelet Noise Attenuation Guided by a Signal or Noise Model

SEG Houston 2013 Annual Meeting, Expanded Abstracts, 4267--4270.

## Overview

This paper presents a versatile guided noise suppression method that compares input data with either a noise prediction or a signal prediction in the curvelet domain, then subtracts energy identified as noise. The comparison and subtraction are both performed coefficient-by-coefficient in the curvelet domain. The method is non-adaptive (no matched filtering step) and requires minimal parameter tuning. Three case studies demonstrate its applicability to multiple attenuation, migration swing removal, and Vz noise attenuation on ocean-bottom node data.

## Key takeaways

- The algorithm: (1) transform input data and noise/signal model to curvelet domain, (2) compare absolute values of corresponding coefficients, (3) mute coefficients identified as noise (or retain those identified as signal), (4) inverse transform.
- When used with a noise model (e.g., multiple prediction): coefficients in the input matching the noise model are muted. This is equivalent to the non-adaptive curvelet subtraction of Herrmann et al. (2007).
- When used with a signal model (e.g., full-azimuth stack): coefficients matching the signal are retained, and everything else is removed. This approach is effective for migration swing suppression.
- Multiple attenuation example: curvelet-based subtraction removes more multiple energy while preserving primaries, compared to least-squares adaptive subtraction, because events with different dip/frequency are separated in the curvelet domain even at the same location.
- Migration swing removal: stacking across azimuthal bins creates a signal guide (migration swings cancel in the stack but signal survives); the algorithm removes incoherent noise and steeply dipping artifacts without dip filtering.
- Vz noise attenuation: the hydrophone (P) component serves as a signal guide for cleaning the vertical geophone (Vz) component contaminated by shear-wave energy.

## Relation to lecture notes

This paper demonstrates practical applications of curvelet-domain noise attenuation covered in Term 3 Lecture 04 -- Noise Attenuation. It extends the framework of Herrmann et al. (2007) and Hennenfent et al. (2011) by showing how different types of guides (noise predictions vs. signal predictions) can be used flexibly within the same algorithmic framework.

## Related sources

- [Hennenfent et al. (2011)](hennenfent2011_interpretative_noise.md) -- Interpreter-guided curvelet noise attenuation
- [Herrmann et al. (2007)](herrmann2007_curvelet_multiple_separation.md) -- Theoretical framework for curvelet-based primary-multiple separation
- [Hennenfent & Herrmann (2006)](hennenfent2006_curvelet_intro.md) -- Foundational NFDCT denoising
