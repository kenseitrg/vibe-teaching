---
title: "Hennenfent, Cole & Kustowski (2011) — Interpretative Noise Attenuation in the Curvelet Domain"
status: draft
type: paper
source_file: papers/noise_attenuation/curvelets/hennenfent2011.txt
language: en
concepts:
  - seismic_data_processing
  - seismic_noise
  - frequency_filtering
tags: [noise-attenuation, curvelet, coherent-noise, random-noise, interpretive-processing]
---

# Hennenfent, Cole & Kustowski (2011) — Interpretative Noise Attenuation in the Curvelet Domain

SEG San Antonio 2011 Annual Meeting, Expanded Abstracts, 3566--3570.

## Overview

This paper presents two real-data examples of curvelet-domain noise attenuation where an interpreter's geological knowledge guides the weighting process. Unlike automated curvelet thresholding, the approach uses interpreter-defined weights in the curvelet domain to selectively remove noise based on its characteristics in different processing domains (common-shot, azimuth, inline, crossline, midpoint gathers). The authors demonstrate that the curvelet transform's ability to localize energy by scale, angle, and position enables more targeted noise attenuation than conventional F-X deconvolution, F-K, or median filtering.

## Key takeaways

- The curvelet noise attenuation algorithm: (1) forward curvelet transform of input data, (2) weight each coefficient by a scalar in [0,1] based on noise characteristics, (3) inverse curvelet transform to obtain signal estimate.
- Unlike F-K modes (global in space), curvelets are localized: altering one coefficient has only local impact, reducing the risk of signal damage.
- Each curvelet is parameterized by dominant period, dominant dip/velocity, and two location coordinates -- providing more degrees of freedom than F-K decomposition.
- Pre-stack land example (on-shore California): multi-pass processing on different gather types successfully attenuated cultural noise and surface waves; surface-consistent amplitude correction after curvelet noise attenuation confirmed that signal amplitudes were preserved.
- Post-stack marine example (Gulf of Mexico): processing on inline, crossline, and depth slices attenuated migration artifacts and random noise without smoothing the signal; steeply dipping migration swings were identified and mitigated.
- The key insight is that interpreter involvement in defining the weighting scheme makes the process more effective and geologically meaningful than fully automated approaches.

## Relation to lecture notes

This paper illustrates practical curvelet noise attenuation workflows discussed in Term 3 Lecture 04 -- Noise Attenuation. It demonstrates the flexibility of curvelet-domain processing across different data domains and noise types, emphasizing the advantage of multi-dimensional, multi-domain processing strategies.

## Related sources

- [Hennenfent & Herrmann (2006)](hennenfent2006_curvelet_intro.md) -- Foundational NFDCT denoising framework
- [Kustowski et al. (2013)](kustowski2013_curvelet_model_guided.md) -- Guided curvelet noise attenuation with signal/noise models
- [Herrmann et al. (2007)](herrmann2007_curvelet_multiple_separation.md) -- Curvelet primary-multiple separation
