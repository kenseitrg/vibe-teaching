---
title: "Gulunay (1986) — FXDECON — Frequency Domain Complex Prediction"
status: draft
type: paper
source_file: papers/noise_attenuation/fx_deconvolution/gulunay1986.txt
language: en
concepts:
  - seismic_data_processing
  - seismic_noise
  - wiener_filter
  - deconvolution
tags: [noise-attenuation, fx-deconvolution, wiener-filter, lateral-prediction, random-noise]
---

# Gulunay (1986) — FXDECON — Frequency Domain Complex Prediction

56th Annual SEG Meeting, Expanded Abstracts, 279--281.

## Overview

This paper provides the first detailed practical implementation of the f-x domain noise attenuation method proposed by Canales (1984), naming it FXDECON (frequency-space domain predictive deconvolution). The implementation combines Canales' f-x prediction idea with Treitel's (1974) complex Wiener filter theory. The method produces two outputs: a "signal" section with noise removed, and a "noise" section showing exactly what was removed (signal + noise = input).

## Key takeaways

- For a given frequency, the f-x response along the spatial coordinate x is a complex-valued sequence; a one-step-ahead prediction filter is computed using complex Wiener filter theory.
- The desired output for prediction is a one-sample-advanced version of the input: if input is (x1, x2, ..., xN), the desired output is (x2, x3, ..., xN+1).
- An extra trace x_{N+1} is kept and used as desired output to ensure that the filter produces output with the same amplitude as input when no noise is present -- a critical quality control criterion.
- The complex Wiener filter is computed from normal equations involving Hermitian autocorrelation matrices and complex cross-correlation vectors; the Hermitian structure is exploited via Robinson's block-Toeplitz algorithm.
- The process is effective in removing spurious data, ground roll, random noise, and even diffractions from stacked data.
- The dual output (signal and noise sections) provides built-in QC: recombination of signal + noise must equal the input exactly.

## Relation to lecture notes

This paper is the standard reference for the FXDECON algorithm, a core tool in post-stack noise attenuation covered in Term 3 Lecture 04 -- Noise Attenuation. It bridges the theoretical insight of Canales (1984) with a production-ready implementation, and is the version most commonly cited in processing software documentation.

## Related sources

- [Canales (1984)](canales1984_fx_decon.md) -- Original f-x noise reduction concept
- [Abma & Claerbout (1995)](abma1995_lateral_prediction.md) -- Comparison with t-x prediction
- [Treitel (1974)](treitel1974_complex_wiener.md) -- Complex Wiener filter theory
- [Denisov & Finikov (2009)](denisov_finikov_2009.md) -- Analysis of f-x deconvolution paradoxes (Russian)
