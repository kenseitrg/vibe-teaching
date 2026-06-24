---
title: Hatton, Worthington & Makin (1986) — Seismic Data Processing. Theory and Practice
status: reviewed
type: textbook
source_file: papers/general/geokniga-xatton-l-uerdington-m-mejkin-dzh-obrabotka-sejsmicheskix-dannyx-teoriya-i-p.djv
language: ru
pages: 216
concepts:
  - deconvolution
  - seismic_wavelet
  - wiener_filter
  - predictive_deconvolution
  - minimum_phase
  - z_transform
  - deterministic_deconvolution
  - statistical_deconvolution
tags: [deconvolution, wavelet, phase, wiener-filter, predictive-decon, deterministic-decon, textbook]
---

# Hatton, Worthington & Makin (1986) — Seismic Data Processing

Russian translation of *Seismic Data Processing. Theory and Practice* (Blackwell, 1986), published by Mir, 1989.
Text extracted from the DJVU version in `papers/general/`.

## Relevant chapters / sections

| Section | Pages (Russian edition) | Topic |
|---------|------------------------|-------|
| 2.4 | ~35–40 | Convolution and discrete filters |
| 2.6 | ~33–37 | Z-transform, phase, delay, minimum/maximum/zero phase, dipoles |
| 2.7 | ~37–43 | Autocorrelation and cross-correlation |
| 2.8 | ~43–47 | Wiener filter, shaping filter, inverse filter, predictive deconvolution, white-noise parameter |
| 2.9 | ~47– | Spectral analysis, spectrum of autocorrelation |
| 3.4.1.5 | ~96–103 | Deterministic deconvolution: designature, ghosts, instrument response, wavelet estimation |
| 3.4.1.6 | ~103–108 | Statistical deconvolution with Wiener filters: assumptions, parameters, operator length, prediction gap |
| 3.5.1.4 | ~ | Predictive deconvolution in processing flows |

## Key takeaways

### Z-transform and dipoles
- The Z-transform of a discrete sequence is a polynomial in `z` (the unit-delay operator). Multiplication of Z-transforms is convolution.
- Fourier transform is a special case: `z = exp(-iω)`.
- A **dipole** `(a, b)` has Z-transform `a + bz`.
- `(a, b)` and `(b, a)` have the **same amplitude spectrum**.
- If `|a| > |b|`, the dipole `(a, b)` is **minimum-phase**; its phase spectrum is everywhere smaller than that of `(b, a)`.
- The first sample of a minimum-phase dipole is larger than the first sample of the maximum-phase dipole with the same amplitude spectrum.
- Any polynomial can be factored into dipoles. A causal signal is minimum-phase **iff** all of its dipole factors are minimum-phase.
- Therefore, among all causal signals with the same amplitude spectrum, the minimum-phase signal has the fastest energy build-up (minimum delay). Its partial energies `E_p = Σ_{k=0}^{p} f_k^2` are largest for every `p`.

### Causality and inverse filters
- Deconvolution in the Z-domain is polynomial division: find `X(z)` such that `X(z)(a + bz) = 1`.
- If the dipole is minimum-phase (`|a| > |b|`), the inverse series `1/(a+bz)` converges in **positive** powers of `z`, i.e. the inverse filter is causal (pure delay components).
- If the dipole is maximum-phase (`|b| > |a|`), the causal expansion diverges; the convergent expansion uses **negative** powers of `z`, i.e. the inverse filter has non-causal (leading) components.
- For mixed-phase signals one generally needs a two-sided filter.

### Wiener filter
- Discrete convolution can be written as a matrix equation `Y = XH`.
- The Wiener-Hopf equations arise from minimizing the squared error between a desired output `d` and the filter output `Xh`.
- In terms of autocorrelation `φ_xx` and cross-correlation `φ_dx`:
  `Σ_k h_k φ_xx[i-k] = φ_dx[i]`.
- Special cases:
  - **Shaping filter**: desired output is a different wavelet.
  - **Inverse (spiking) filter**: desired output is a unit spike.
  - **Predictive deconvolution**: desired output is the input shifted forward by the prediction gap `q`.
- The prediction-error filter is `(1, 0, ..., 0, -h_q)` and removes predictable repetitive energy.

### White-noise parameter (prewhitening)
- Adding a small constant to the zero-lag autocorrelation (the diagonal of the normal-equation matrix) stabilizes inversion.
- Typical values: 0.0001% for numerical stability, 0.5–5% for noise control.
- It limits amplification at frequencies where the signal spectrum is weak.

### Deterministic deconvolution
- Requires a known or estimated wavelet (source signature, far-field signature, instrument response).
- Can be applied separately to each convolutional component (source signature, source ghost, receiver ghost, instrument response).
- Ghosts are hard to remove completely because their notch frequency varies with source/receiver depth and sea state.
- Vibroseis data are usually converted to minimum-phase via an amplitude-only correction plus minimum-phase spectral factorization.

### Statistical deconvolution
- Assumptions:
  1. Reflection coefficients are random and uncorrelated (white).
  2. Noise is random and stationary.
  3. Wavelet is minimum-phase.
- Operator parameters:
  - **Prediction gap (minimum lag)**: one sample = spiking deconvolution; larger = predictive deconvolution.
  - **Maximum lag / operator length**: controls how much of the autocorrelation is used.
  - **White-noise level / prewhitening**.
  - **Analysis window**: should contain strong signal, avoid ground roll and multiples, use gain correction.
- Practical advice:
  - On noisy traces, deconvolution cannot produce much compression.
  - Correlated noise biases the autocorrelation.
  - Prefiltering high-noise bands improves results.

## Figures useful for teaching

- Fig. 2.21–2.24: minimum-phase vs. zero-phase band-pass filters and their convolution products.
- Fig. 2.35: schematic of predictive deconvolution (prediction gap = multiple period).
- Fig. 3.54: undesirable operator spectrum from a bad desired-output choice.
- Fig. 3.55–3.56: operator length and zero-time position iteration.
- Fig. 3.57–3.58: deterministic designature examples and far-field signatures for different source types.
- Fig. 3.59: smoothing a ghost operator to reduce spectral notch depth.
- Fig. 3.60: choice of prediction gap and maximum lag.

## References cited in the book
- Robinson, E.A. & Treitel, S. (1980). *Geophysical Signal Analysis*. Prentice-Hall.
- Sheriff, R.E. & Geldart, L.P. (1995). *Exploration Seismology*.
- Various Western Geophysical / seismic source papers.

## Relation to lecture notes
- Provides the dipole-based proof of minimum-phase front-loading requested for Term 1 Lecture 6.
- Gives practical parameter guidance for spiking/predictive deconvolution.
- Explains deterministic designature and ghost removal.
