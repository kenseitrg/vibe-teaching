---
title: Term 1 Lecture 6 — Single-channel deconvolution
status: draft
course_term: 1
lecture: term01_lec06
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - margrave_2006_methods_of_seismic_data_processing
  - yilmaz_2001_seismic_data_analysis_deconvolution
  - verschuur_2006_predictive_deconvolution
concepts:
  - deconvolution
  - minimum_phase
  - deterministic_deconvolution
  - statistical_deconvolution
  - wiener_filter
  - predictive_deconvolution
tags: [lecture-ready, term01, deconvolution, single-channel]
---

# Term 1 Lecture 6 — Single-channel deconvolution

> 90-minute lecture. Student-facing notes: `lecture_notes/en/term01_lec06_single_channel_deconvolution.en.md`.

## Learning objectives

After this lecture students should be able to:
1. State the convolutional model of a seismic trace and list the main components of the embedded wavelet.
2. Explain why deconvolution is needed and what it cannot do.
3. Define minimum-phase, maximum-phase, zero-phase, and causal wavelets using the dipole example.
4. Apply deterministic deconvolution in the Fourier and Z-transform domains, including prewhitening.
5. Derive the Wiener-Hopf equations from the least-squares criterion and explain the role of each assumption.
6. Distinguish spiking and predictive deconvolution by prediction gap and operator length.

## Prerequisites

- Discrete convolution and Fourier transform.
- Autocorrelation and cross-correlation.
- Basic matrix algebra.

## Lecture outline (90 min)

| Section | Time | Key idea |
|---------|------|----------|
| 1. Introduction: goal of deconvolution | 10 min | Recover band-limited reflectivity; wavelet compression and reverberation removal |
| 2. Convolutional model | 10 min | `x = w * r + n`; signature, ghosts, bubble, instrument |
| 3. Phase and Z-transform | 20 min | Dipole proof of minimum phase; causal vs. non-causal inverse |
| 4. Deterministic deconvolution | 20 min | Spectral division, polynomial division, prewhitening, designature/vibroseis examples |
| 5. Statistical deconvolution — Wiener filter | 20 min | Least-squares derivation, normal equations, assumptions |
| 6. Spiking and predictive deconvolution | 10 min | Prediction gap, operator length, parameter effects |

## Key equations

### Convolutional model

$$
x(t) = w(t) * r(t) + n(t)
$$

### Dipole Z-transform

$$
W(z) = a + bz
$$

Minimum phase if $|a| > |b|$; inverse is causal.

### Deterministic inverse filter with prewhitening

$$
F(f) = \frac{W^*(f)}{|W(f)|^2 + \varepsilon^2}
$$

### Wiener-Hopf equations

$$
\sum_{k=0}^{N} f_k \, \phi_{xx}[i-k] = \phi_{dx}[i], \qquad i = 0, \dots, N
$$

### Prediction-error filter

$$
e(t) = x(t) - \hat{x}(t) = x(t) - \sum_{k} h_k \, x(t - \alpha - k)
$$

## Figures to generate

1. Reflectivity + wavelet = trace (convolutional model).
2. Minimum-, maximum-, zero-phase wavelets with same amplitude spectrum.
3. Dipole roots inside/outside unit circle.
4. Deterministic deconvolution: wavelet, inverse filter, output spike.
5. Effect of prewhitening on operator spectrum.
6. Wiener spiking deconvolution on synthetic trace.
7. Predictive deconvolution with varying prediction gap.

## Concept-check questions

1. Why can deconvolution not recover frequencies that were never recorded?
2. A dipole is $(4, 1)$. Is it minimum phase? Where are the zeros of its Z-transform?
3. Why does a mixed-phase wavelet need a two-sided inverse filter?
4. What assumption lets us design a deconvolution operator from the trace autocorrelation alone?
5. How does the prediction gap control what predictive deconvolution removes?

## Sources

- Hatton et al. (1986), Ch. 2.6–2.8, 3.4.1.5–3.4.1.6.
- Margrave (2006), Ch. 3–4.
- Yilmaz (2001), Vol. 1, deconvolution chapter.
- Verschuur (2006), EAGE EET 03.
