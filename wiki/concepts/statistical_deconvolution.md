---
title: Statistical deconvolution
status: draft
course_term: 1
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - margrave_2006_methods_of_seismic_data_processing
  - yilmaz_2001_seismic_data_analysis_deconvolution
  - verschuur_2006_predictive_deconvolution
tags: [deconvolution, statistical, wiener-filter, spiking, autocorrelation, assumptions]
---

# Statistical deconvolution

**Statistical deconvolution** estimates the inverse wavelet filter from the seismic trace itself, using assumptions about the reflectivity and noise, rather than from a measured source signature.

## Core idea

If the trace follows the convolutional model

$$
x(t) = w(t) * r(t) + n(t) ,
$$

and the reflection coefficients $r(t)$ are a white random sequence, then the autocorrelation of the trace is dominated by the autocorrelation of the wavelet:

$$
\phi_{xx}(\tau) \approx \phi_{ww}(\tau) + \phi_{nn}(\tau) .
$$

A least-squares inverse filter is designed from $\phi_{xx}$ to compress $w(t)$ toward a spike.

## Assumptions

| Assumption | Why it matters | What happens if it fails |
|------------|----------------|--------------------------|
| Wavelet is minimum phase | Phase of the inverse is derived from the amplitude spectrum | Phase errors; incorrect timing of events |
| Reflectivity is white (random) | Autocorrelation of reflectivity is a spike, so trace autocorrelation ≈ wavelet autocorrelation | Multiples or cyclic geology create spurious correlation; operator is biased |
| Wavelet is stationary | Same wavelet across the design window | Time-variant wavelets (Q, ghosts, arrays) cause non-stationary distortions |
| Noise is additive and white | Does not correlate with signal and has flat spectrum | Correlated or colored noise distorts the autocorrelation |

## Wiener-Hopf equations

For a filter $f = (f_0, f_1, \dots, f_N)$, the normal equations are

$$
\sum_{k=0}^{N} f_k \, \phi_{xx}[i-k] = \phi_{dx}[i], \qquad i = 0, \dots, N .
$$

- For **spiking deconvolution**, the desired output $d$ is a unit spike at zero lag, so the right-hand side is $\phi_{dx}[i] = \delta[i]$.
- For **shaping deconvolution**, the desired output is a chosen wavelet (often zero phase).
- The autocorrelation matrix is Toeplitz and symmetric, so it can be solved efficiently with the Levinson-Durbin / Wiener-Levinson recursion.

With prewhitening:

$$
\sum_{k=0}^{N} f_k \, \bigl(\phi_{xx}[i-k] + \varepsilon^2 \delta[i-k]\bigr) = \phi_{dx}[i] .
$$

## Special cases

| Desired output | Name | Effect |
|----------------|------|--------|
| Spike $\delta[n]$ | Spiking deconvolution | Compress wavelet to a spike |
| $x[n-\alpha]$ | Predictive deconvolution | Remove predictable repetitive energy |
| Known wavelet | Shaping / wavelet processing | Convert wavelet to desired shape |

## Parameters

- **Operator length** (maximum lag): too short → incomplete compression; too long → noise and model violations.
- **Prewhitening / white-noise level**: stabilizes and limits noise amplification.
- **Analysis window**: should contain strong reflections, avoid multiples and ground roll, be gain-balanced.

## Limitations

- Cannot recover frequencies absent from the recorded wavelet.
- Minimum-phase assumption is often only approximate.
- Reflectivity is rarely perfectly white; short-period multiples and cyclic sequences violate it.
- Trace-to-trace noise and non-stationarity make operators unstable.

## Related concepts

- [Deconvolution](deconvolution.md)
- [Wiener filter](wiener_filter.md)
- [Predictive deconvolution](predictive_deconvolution.md)
- [Minimum phase](minimum_phase.md)
- [Deterministic deconvolution](deterministic_deconvolution.md)
- [Surface-consistent deconvolution](surface_consistent_deconvolution.md)

## Sources

- [Hatton, Worthington & Makin (1986)](../sources/hatton_worthington_makin_1986_seismic_data_processing.md)
- [Margrave (2006)](../sources/margrave_2006_methods_of_seismic_data_processing.md)
- [Yilmaz (2001)](../sources/yilmaz_2001_seismic_data_analysis_deconvolution.md)
- [Verschuur (2006)](../sources/verschuur_2006_predictive_deconvolution.md)
