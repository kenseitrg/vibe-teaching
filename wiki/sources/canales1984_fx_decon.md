---
title: "Canales (1984) — Random Noise Reduction"
status: draft
type: paper
source_file: papers/noise_attenuation/fx_deconvolution/canales1984.txt
language: en
concepts:
  - seismic_data_processing
  - seismic_noise
  - wiener_filter
  - deconvolution
tags: [noise-attenuation, fx-deconvolution, wiener-filter, lateral-prediction, random-noise]
---

# Canales (1984) — Random Noise Reduction

54th Annual SEG Meeting, Atlanta, Expanded Abstracts, 525--527.

## Overview

This paper introduces the f-x domain random noise reduction method, now commonly known as "f-x deconvolution." The key insight is that for nearly linear seismic events, the signal at each frequency in the f-x domain is a sum of complex exponentials and is therefore predictable as a function of spatial position x. By applying complex Wiener filter theory to estimate the predictable (signal) part of the data at each frequency independently, random noise is effectively attenuated without the lateral mixing artifacts common in mixing schemes.

## Key takeaways

- The seismic trace ensemble U(t,x) is modeled as a sum of delayed impulses; after Fourier transformation in time, the model becomes a sum of complex exponentials in the (omega, x) domain.
- Under a linearity assumption (events nearly linear in x within sub-ensembles), U(omega, x) is strictly sinusoidal in x, making it predictable by a one-step-ahead convolutional prediction filter.
- The complex Wiener prediction filter is applied independently at each frequency to estimate the predictable (signal) component, then transformed back to the (t, x) domain.
- The method does not produce the "synthetic" or mixed appearance common in mixing schemes; removed noise appears random, confirming that coherent events are preserved.
- Two passes of the process can be applied for additional improvement, with balancing between passes to account for amplitude reduction in noisy areas.
- This work established the foundation for all subsequent f-x deconvolution methods, including Gulunay (1986) and Abma & Claerbout (1995).

## Relation to lecture notes

This is the foundational paper for f-x deconvolution, a core noise attenuation technique covered in Term 3 Lecture 04 -- Noise Attenuation. The method bridges Wiener filter theory (Treitel 1974) with practical spatial prediction for seismic data, forming the basis for one of the most widely used post-stack noise attenuation algorithms.

## Related sources

- [Gulunay (1986)](gulunay1986_fxdecon.md) -- Practical implementation as FXDECON
- [Abma & Claerbout (1995)](abma1995_lateral_prediction.md) -- Comparison of f-x and t-x prediction
- [Treitel (1974)](treitel1974_complex_wiener.md) -- Complex Wiener filter theory
