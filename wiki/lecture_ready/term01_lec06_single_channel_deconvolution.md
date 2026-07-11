---
title: Term 1 Lecture 6 — Single-channel deconvolution
status: lecture-ready
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
tags: [term01, deconvolution, single-channel]
---

# Term 1 Lecture 6 — Single-channel deconvolution

> 90-minute lecture. Student-facing notes: `lecture_notes/en/term01_lec06_single_channel_deconvolution.en.md`.

## One-line summary

Build the convolutional model of a seismic trace, understand why phase matters, and derive deterministic and statistical (Wiener) deconvolution from single-channel data.

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

## Key concepts covered

- Convolutional model of a seismic trace: $x = w * r + n$ and the embedded wavelet components (source signature, ghosts, bubble, instrument, absorption).
- Band-limited reflectivity as the realistic target of deconvolution.
- Minimum-, maximum-, zero-, and mixed-phase wavelets; the dipole proof and the partial-energy theorem.
- Causal vs. non-causal inverse filters; polynomial division in the $z$-domain.
- Deterministic deconvolution by spectral division with prewhitening.
- Wiener-Hopf equations from least-squares minimization and the Toeplitz autocorrelation matrix.
- Spiking deconvolution and predictive deconvolution; role of prediction gap.

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

For a dipole $(a, b)$ with sample interval $\Delta t$:

$$
W(z) = a + b\,z^{-1}
$$

Minimum phase if $|a| > |b|$; the zero lies inside the unit circle and the causal inverse is stable.

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

## Generated figures

| Figure | Path |
|--------|------|
| Convolutional model | `figures/term01_lec06/term01_lec06_convolutional_model.png` |
| Dipoles | `figures/term01_lec06/term01_lec06_dipoles.png` |
| Phase wavelets | `figures/term01_lec06/term01_lec06_phase_wavelets.png` |
| Deterministic deconvolution | `figures/term01_lec06/term01_lec06_deterministic_decon.png` |
| Prewhitening | `figures/term01_lec06/term01_lec06_prewhitening.png` |
| Spiking deconvolution | `figures/term01_lec06/term01_lec06_spiking_decon.png` |
| Predictive deconvolution | `figures/term01_lec06/term01_lec06_predictive_decon.png` |

## Lecture materials

- English notes: `lecture_notes/en/term01_lec06_single_channel_deconvolution.en.md`
- Rendered PDF: `lecture_notes/en/term01_lec06_single_channel_deconvolution.en.pdf`
- Russian notes: `lecture_notes/ru/term01_lec06_single_channel_deconvolution.ru.md`
- Rendered PDF (RU): `lecture_notes/ru/term01_lec06_single_channel_deconvolution.ru.pdf`
- Derivation (Wiener): `lecture_notes/derivations/wiener_deconvolution_derivation.en.md`
- Derivation (PEF Z-transform): `lecture_notes/derivations/pef_ztransform_derivation.en.md`
- Exercises: `exercises/term01_lec06_single_channel_deconvolution.md`
- Slide outline: `slides/term01/lec06_single_channel_deconvolution/slide_outline.md`
- Starter deck: `slides/term01/lec06_single_channel_deconvolution/lec06_single_channel_deconvolution.pptx`
- Figure scripts: `scripts/figures/term01_lec06/`

## Related concept pages

- [Deconvolution](../concepts/deconvolution.md)
- [Seismic wavelet](../concepts/seismic_wavelet.md)
- [Minimum phase](../concepts/minimum_phase.md)
- [Deterministic deconvolution](../concepts/deterministic_deconvolution.md)
- [Statistical deconvolution](../concepts/statistical_deconvolution.md)
- [Wiener filter](../concepts/wiener_filter.md)
- [Predictive deconvolution](../concepts/predictive_deconvolution.md)

## Concept-check questions

1. Why can deconvolution not recover frequencies that were never recorded?
2. A dipole is $(4, 1)$. Is it minimum phase? Where is the zero of its Z-transform?
3. Why does a mixed-phase wavelet need a two-sided inverse filter?
4. What assumption lets us design a deconvolution operator from the trace autocorrelation alone?
5. How does the prediction gap control what predictive deconvolution removes?

## Sources

- Hatton et al. (1986), Ch. 2.6–2.8, 3.4.1.5–3.4.1.6.
- Margrave (2006), Ch. 3–4.
- Yilmaz (2001), Vol. 1, deconvolution chapter.
- Verschuur (2006), EAGE EET 03.

## Notes for instructor

- This is the first lecture on deconvolution. Keep the focus on physical intuition: minimum-phase wavelets are front-loaded, so their energy is concentrated early and a stable causal inverse exists.
- The dipole proof is the most technical part; use the dipole figure to show that minimum- and maximum-phase dipoles share the same amplitude spectrum but differ in phase.
- The deterministic examples (designature, instrument response, vibroseis-to-minimum-phase) help students see when prior knowledge removes the need for statistical assumptions.
- Introduce the Wiener-Hopf equations as least-squares linear regression in the time domain; the Toeplitz matrix is a direct consequence of stationarity.
- Emphasize that spiking deconvolution is simply predictive deconvolution with a one-sample gap.
- The Python figure scripts are self-contained; consider running the spiking and predictive deconvolution demos live or assigning them as practical exercises.
- The slide outline still contains the old dipole formula $W(z) = a + bz$; align it with the notes ($a + bz^{-1}$, zero inside unit circle) before presenting.
