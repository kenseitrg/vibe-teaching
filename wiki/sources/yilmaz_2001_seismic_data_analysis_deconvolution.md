---
title: Yilmaz (2001) — Seismic Data Analysis. Deconvolution chapter (Vol. 1)
status: reviewed
type: textbook
source_file: papers/textbooks/Yilmaz - Seismic Data Analysis_1.pdf
pages: ~145–215 of Vol. 1
concepts:
  - deconvolution
  - seismic_wavelet
  - wiener_filter
  - predictive_deconvolution
  - minimum_phase
  - z_transform
  - surface_consistent_deconvolution
tags: [deconvolution, seismic-data-analysis, wiener-filter, predictive-decon, minimum-phase, z-transform, surface-consistent]
---

# Yilmaz (2001) — Seismic Data Analysis. Deconvolution

Extracted from pages 145–215 of Volume 1 of *Seismic Data Analysis: Processing, Inversion, and Interpretation of Seismic Data*.

## Relevant sections

| Section | Pages | Topic |
|---------|-------|-------|
| 2.2 / 2.3 | ~149– | The convolutional model, source wavelet, ghosts, deconvolution assumptions |
| 2.4 | ~ | Inverse filtering, spiking deconvolution |
| 2.5 | ~ | Predictive deconvolution |
| 2.6 | ~ | Surface-consistent deconvolution |
| Appendix | ~507–509 | Minimum phase, Z-transform, mathematical foundation |

## Key takeaways

### Wavelet model
- The seismic trace is modeled as the convolution of the earth's reflectivity series with the source wavelet plus noise.
- The recorded wavelet includes the source signature, source ghost, receiver ghost, and instrument response.
- Ghosts create notches in the amplitude spectrum; their frequencies depend on source/receiver depth.

### Deconvolution assumptions
1. The earth's reflectivity is a white random sequence.
2. The wavelet is minimum phase.
3. The wavelet is stationary in the analysis window.
4. Noise is additive and white.

When these hold, the autocorrelation of the trace is proportional to the autocorrelation of the wavelet, and a least-squares inverse filter can be designed from the trace alone.

### Inverse and Wiener filtering
- Spiking deconvolution compresses the wavelet to a zero-lag spike.
- It can be implemented by spectral division in the frequency domain or by solving the Wiener normal equations in the time domain.
- Prewhitening stabilizes the inversion.

### Predictive deconvolution
- A prediction filter estimates the trace at a future time from past values.
- The prediction-error filter removes predictable components such as short-period multiples and reverberations.
- The prediction lag controls what is removed:
  - One sample → spiking deconvolution.
  - Water-layer two-way time → reverberation suppression.
- Predictive deconvolution assumes a constant multiple period; it works best on near-offset or angle-sorted data.

### Surface-consistent deconvolution
- Decomposes the trace operator into source, receiver, offset, and CDP components.
- Each trace operator is the convolution of a source-location operator and a receiver-location operator (and possibly offset/CDP terms).
- More statistics per surface location → more stable operators in noisy data.

## Relation to lecture notes
- Standard reference for the convolutional model and deconvolution assumptions.
- Provides mathematical foundation for minimum phase and the Wiener filter.
- Covers surface-consistent deconvolution needed for Term 1 Lecture 7.
