---
title: Margrave (2006) — Methods of Seismic Data Processing. Course Lecture Notes
status: reviewed
type: lecture notes
source_file: papers/textbooks/Methods of Seismic Data Processing.pdf
pages: 410
concepts:
  - deconvolution
  - minimum_phase
  - wiener_filter
  - predictive_deconvolution
  - convolutional_model
  - surface_consistent_deconvolution
tags: [deconvolution, convolutional-model, minimum-phase, wiener-filter, predictive-decon, q-attenuation, lecture-notes]
---

# Margrave (2006) — Methods of Seismic Data Processing

Course lecture notes for Geophysics 557/657, University of Calgary, Winter 2006.
Extracted pages 125–205 cover minimum phase, the convolutional model, and deconvolution.

## Relevant chapters / sections

| Section | Pages | Topic |
|---------|-------|-------|
| 3-14 to 3-18 | 125–129 | Constant-Q attenuation; non-stationary wavelet |
| 3-18 to 3-26 | 129–137 | Minimum phase: intuitive, Hilbert transform, partial energy, dispersion |
| 4-1 to 4-5 | 145–149 | Bandlimited reflectivity; convolutional model and simplifying assumptions |
| 4-? | ~149– | Frequency-domain spiking deconvolution; Wiener spiking deconvolution; gapped predictive deconvolution; Burg deconvolution |

## Key takeaways

### Convolutional model
- Ultimate goal: recover the earth's reflectivity as a function of position.
- Because seismic sources do not generate useful power at all frequencies, the best achievable result is **bandlimited reflectivity** — the true reflectivity convolved with a zero-phase wavelet.
- Sheriff & Geldart decompose the earth impulse response into near-surface effects, propagation effects (multiples, absorption, mode conversions), and target reflectors. Margrave notes this terminology can be self-contradictory if the "impulse response" is supposed to be only the desired signal.
- For deconvolution theory we need stronger simplifying assumptions than pure linearity.

### Minimum phase
- Infinitely many wavelets share the same amplitude spectrum; only a few have practical use.
- A **minimum-phase wavelet** is the most front-loaded of all causal wavelets with the same amplitude spectrum.
- Minimum-phase wavelets arise naturally in the earth from causality and linearity; constant-Q attenuation is a minimum-phase process.
- For a causal, stable function with a causal stable inverse, amplitude and phase are related by the Hilbert transform. The phase is `φ(ω) = H[ln A(ω)]`.
- Partial energies `E_p = Σ_{k=0}^{p} f_k^2` are larger for the minimum-phase wavelet than for any other causal wavelet with the same amplitude spectrum, for all `p`.
- If the amplitude spectrum of a minimum-phase dataset is changed, the phase spectrum must also change to preserve the minimum-phase relationship.

### Deconvolution algorithms
- Frequency-domain spiking deconvolution: divide the trace spectrum by the wavelet spectrum. Prewhitening is essential for stability.
- Wiener spiking deconvolution designs a finite least-squares inverse filter using the autocorrelation of the trace.
- The autocorrelation matrix is Toeplitz and symmetric; use the Wiener-Levinson (Levinson-Durbin) recursion.
- Gapped predictive deconvolution: desired output is the trace shifted by the prediction gap; the residual is the deconvolved trace.
- Burg (maximum entropy) deconvolution explicitly constructs a minimum-phase prediction-error filter.

### Practical notes
- Real data are non-stationary: the wavelet changes with time because of attenuation and with offset because of arrays/ghosts.
- Arrays of sources/receivers create a variable embedded wavelet, violating strict stationarity assumptions.

## Figures useful for teaching

- Constant-Q amplitude spectra at increasing time (pages 125–126).
- Minimum-phase vs. zero-phase bandlimited reflectivity (page 146).
- Matrix representation of convolution (page 146).

## Relation to lecture notes
- Good source for the Hilbert-transform link between amplitude and phase spectrum.
- Explains why bandlimited reflectivity, not the full impulse response, is the realistic processing target.
- Provides matrix view of convolution and Wiener normal equations.
