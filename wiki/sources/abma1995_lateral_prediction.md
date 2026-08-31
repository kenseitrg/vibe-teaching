---
title: "Abma & Claerbout (1995) — Lateral Prediction for Noise Attenuation by t-x and f-x Techniques"
status: draft
type: paper
source_file: papers/noise_attenuation/fx_deconvolution/abma1995.txt
language: en
concepts:
  - seismic_data_processing
  - seismic_noise
  - wiener_filter
  - frequency_filtering
tags: [noise-attenuation, fx-deconvolution, tx-prediction, lateral-prediction, 3d-processing, random-noise]
---

# Abma & Claerbout (1995) — Lateral Prediction for Noise Attenuation by t-x and f-x Techniques

*Geophysics*, 60(6), 1887--1896.

## Overview

This paper provides a rigorous comparison of time-space (t-x) and frequency-space (f-x) lateral prediction methods for random noise attenuation. While both methods produce similar results in low-noise conditions, t-x prediction has important advantages in the presence of moderate-to-high amplitude noise: it passes less random noise and does not generate spurious events. The key insight is that f-x prediction produces an effective t-x filter that is as long as the input data in time, whereas t-x prediction allows explicit control of the filter length in time.

## Key takeaways

- f-x prediction (Gulunay 1986) computes a separate least-squares prediction filter at each frequency; the collection of these frequency-specific filters forms an effective t-x filter that is as long as the data in time.
- t-x prediction computes a single 2-D filter in the time-space domain using conjugate gradients, with explicit control over the filter's temporal length (typically 3--5 samples).
- The long effective temporal filter of f-x prediction is the root cause of two problems: (1) passing more random noise (many degrees of freedom allow random correlations to be predicted), and (2) generating spurious events parallel to real events when parallel events exist in noise.
- Gulunay's formulation biases filter coefficients toward the nearest traces, allowing slightly more noise to pass; this can be corrected by modifying the system of equations (equation 8 in the paper), but the improvement is minor compared to the benefit of short t-x filter length.
- 3-D extensions of both methods produce better results than two 2-D passes because: (1) more samples are available for prediction, and (2) the linearity assumption is relaxed in 3-D (events nonlinear in one direction but linear in another are predicted exactly).
- One-pass 3-D prediction preserves significantly more detail than two-pass 2-D processing, avoiding smearing across faults and structural discontinuities.

## Relation to lecture notes

This paper is essential for understanding the theoretical basis and practical limitations of f-x deconvolution, covered in Term 3 Lecture 04 -- Noise Attenuation. It explains why f-x deconvolution works despite its simplified theoretical model and provides the comparative framework for choosing between f-x and t-x approaches.

## Related sources

- [Canales (1984)](canales1984_fx_decon.md) -- Original f-x noise reduction concept
- [Gulunay (1986)](gulunay1986_fxdecon.md) -- FXDECON implementation
- [Treitel (1974)](treitel1974_complex_wiener.md) -- Complex Wiener filter theory
- [Denisov & Finikov (2010)](denisov_finikov_2010.md) -- Detailed analysis of f-x deconvolution algorithm features (Russian)
