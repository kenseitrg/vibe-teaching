---
title: Non-Uniform Coherent Noise Suppression (NUCNS) — Technical Documentation
status: draft
source_type: technical documentation
authors: "Schlumberger"
year: 2020
source_file: papers/noise_attenuation/NUCNS_SFM.docx
lectures:
  - term03_lec04
related_concepts:
  - seismic_noise
  - frequency_filtering
  - surface_waves
  - adaptive_subtraction
  - cross_spread_gather
tags: [noise-attenuation, coherent-noise, f-x-filtering, least-squares, surface-waves, ground-roll]
---

# Non-Uniform Coherent Noise Suppression (NUCNS)

Schlumberger (2020). *NUCNS Seismic Function Module — Non-Uniform Coherent Noise Suppression*. Schlumberger Private – Customer Use.

## Main message

NUCNS suppresses shot-generated coherent noise (primarily ground roll and surface waves) on non-uniformly sampled land data by estimating local noise models in the frequency-space (f-x) domain using fan filters and a least-squares weighting scheme. Unlike conventional f-k filters, NUCNS does not require regular trace spacing and works directly in f-x space, making it suitable for point-source/point-receiver geometries with irregular sampling.

## Key points

1. **Noise model in f-x domain:** For each reference trace, NUCNS selects a local macro-gather (cross-spread, common shot, or common receiver), Fourier-transforms to f-x, and applies band-pass fan filters defined by velocity ranges.
2. **Least-squares optimization:** Weighting coefficients for each fan filter are determined by minimising the residual between the model and the data. The normal-equation solution is computed independently at each frequency.
3. **Signal protection:** Signal and noise fan filters are both used in the LS estimation, but only the noise-related fan filters contribute to the output noise model, preserving the signal of interest.
4. **Macro-gather types:** Cross-spread gathers (most common for 3D land), common receiver gathers, and common shot gathers. All traces of one macro-gather must be contiguous in the input.
5. **Multiple iterations:** The process can be applied multiple times with progressively refined parameters, each iteration operating on data with improved signal-to-noise ratio.
6. **AGC option:** An automatic gain control can be applied internally before computing the LS weights and removed afterward, ensuring stable amplitude estimation across large dynamic ranges.
7. **Anti-alias protection:** The fan filters include anti-alias protection to prevent spatial aliasing artefacts from contaminating the noise model.

## Relation to lecture notes

This source directly supports Term 3 Lecture 04 — Noise Attenuation, where the theory of f-x fan filters and LS coherent-noise estimation is presented. NUCNS illustrates how frequency-domain approaches can handle irregular geometries that violate the assumptions of conventional f-k filtering.

## Related concepts

- [Seismic noise](../concepts/seismic_noise.md)
- [Frequency filtering](../concepts/frequency_filtering.md)
- [Surface waves](../concepts/surface_waves.md)
- [Adaptive subtraction](../concepts/adaptive_subtraction.md)
- [Cross-spread gather](../concepts/cross_spread_gather.md)

## Related sources

- [NUCNS Best Practice](nucns_best_practice.md)
