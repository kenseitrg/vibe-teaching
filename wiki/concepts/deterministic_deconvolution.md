---
title: Deterministic deconvolution
status: draft
course_term: 1
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - yilmaz_2001_seismic_data_analysis_deconvolution
tags: [deconvolution, deterministic, wavelet, inverse-filter, designature, ghost]
---

# Deterministic deconvolution

**Deterministic deconvolution** removes a wavelet whose shape is known or measured, rather than inferring it statistically from the data. The operator depends only on the known wavelet and the desired output.

## When it applies

| Situation | Known input | Typical desired output |
|-----------|-------------|------------------------|
| Marine airgun data | Measured or modeled far-field source signature | Spike or minimum-phase wavelet |
| Vibroseis data | Known sweep | Minimum-phase equivalent |
| Instrument response | Recorder impulse response | Flat response |
| Ghost removal | Source/receiver geometry and water velocity | Ghost-free wavelet |

## Fourier-domain formulation

If the recorded trace is

$$
x(t) = w(t) * r(t) + n(t) ,
$$

then in the frequency domain

$$
X(f) = W(f)\,R(f) + N(f) .
$$

An inverse filter is

$$
F(f) = \frac{1}{W(f)} \approx \frac{W^*(f)}{|W(f)|^2 + \varepsilon^2} ,
$$

where $\varepsilon^2$ is a prewhitening constant that stabilizes the division where $|W(f)|$ is small.

The deconvolved spectrum is

$$
\hat{R}(f) = F(f)\,X(f) .
$$

## Z-domain formulation

For a finite-length wavelet $w = (w_0, w_1, \dots, w_{N-1})$, deconvolution is polynomial division:

$$
F(z) = \frac{1}{W(z)} = \frac{1}{w_0 + w_1 z + \dots + w_{N-1} z^{N-1}} .
$$

- If $W(z)$ is minimum phase, $F(z)$ can be expanded in **positive** powers of $z$: a causal filter.
- If $W(z)$ is mixed phase, a convergent expansion needs both positive and negative powers: a two-sided (non-causal) filter.
- In practice the infinite expansion is truncated and the result is least-squares optimized.

## Prewhitening

Prewhitening adds a small fraction of white noise to the wavelet spectrum:

$$
F(f) = \frac{W^*(f)}{|W(f)|^2 + \varepsilon^2} .
$$

Effects:
- Stabilizes the operator where the signal spectrum has notches or weak amplitudes.
- Limits amplification of noise outside the signal band.
- Typical values: 0.1–5% of the zero-lag autocorrelation.

## Practical examples

### Designature
- The marine source signature includes the primary pulse and residual bubble oscillations.
- A deterministic inverse filter removes the bubble train if the signature is accurately known.
- Ghosts are harder because the notch frequency depends on source depth and sea state.

### Instrument response removal
- A land geophone plus recording system has a known frequency response (natural frequency, damping, anti-alias filters, recording filters).
- Given the measured or specified instrument response, a deterministic inverse operator can be computed and applied to recover ground motion with a flat, broadband response.

### Vibroseis to minimum phase
- Vibroseis data are correlated with the sweep, giving a zero-phase Klauder wavelet.
- To make the data compatible with minimum-phase processing, apply an amplitude-only correction and compute the minimum-phase equivalent.

## Limitations

- Requires an accurate wavelet estimate.
- Does not adapt to trace-to-trace wavelet variations.
- Ghost notches and missing frequencies cannot be fully recovered.
- Any error in the assumed wavelet propagates into the reflectivity estimate.

## Related concepts

- [Deconvolution](deconvolution.md)
- [Minimum phase](minimum_phase.md)
- [Statistical deconvolution](statistical_deconvolution.md)
- [Seismic wavelet](seismic_wavelet.md)

## Sources

- [Hatton, Worthington & Makin (1986)](../sources/hatton_worthington_makin_1986_seismic_data_processing.md)
- [Yilmaz (2001)](../sources/yilmaz_2001_seismic_data_analysis_deconvolution.md)
