---
title: Wiener filter
status: draft
course_term: 1
sources:
  - verschuur_2006_predictive_deconvolution
  - hutchinson_link_1984_surface_consistency
  - hatton_worthington_makin_1986_seismic_data_processing
  - margrave_2006_methods_of_seismic_data_processing
  - yilmaz_2001_seismic_data_analysis_deconvolution
tags: [deconvolution, wiener-filter, least-squares, autocorrelation]
---

# Wiener filter

The **Wiener filter** is the optimal linear filter that transforms one signal into another in the least-squares sense. It is the workhorse behind many deconvolution algorithms, including spiking and predictive deconvolution.

## Problem statement

Given an input signal `x(t)` and a desired output `y(t)`, find a finite-length filter `f[n]` of length `N+1` such that:

```text
ε = Σ ( y[n] - Σ f[k] · x[n-k] )²  is minimized
```

## Normal equations

Minimizing the error leads to the Wiener-Hopf equations (normal equations):

```text
Σ_{k=0}^{N} f[k] · φ_xx[i-k] = φ_yx[i]    for i = 0, ..., N
```

where:

- `φ_xx[i] = Σ x[n] · x[n+i]` is the autocorrelation of the input.
- `φ_yx[i] = Σ y[n] · x[n+i]` is the cross-correlation of the desired output with the input.

In matrix form:

```text
| φ_xx[0]+ε²  φ_xx[1]   ...  φ_xx[N]   |   | f[0] |   | φ_yx[0] |
| φ_xx[1]    φ_xx[0]+ε² ...  φ_xx[N-1] | · | f[1] | = | φ_yx[1] |
|   ...         ...     ...     ...     |   | ...  |   |   ...   |
| φ_xx[N]    φ_xx[N-1] ...  φ_xx[0]+ε² |   | f[N] |   | φ_yx[N] |
```

The small positive constant `ε²` (prewhitening) stabilizes the inversion.

## Efficient solution

The autocorrelation matrix is Toeplitz and symmetric, so the system can be solved efficiently with the **Wiener-Levinson algorithm** (also called Levinson-Durbin recursion).

## Special cases

| Desired output | Name | Effect |
|----------------|------|--------|
| Spike (`δ[n]`) | Spiking deconvolution | Compresses the wavelet to a spike |
| Time-shifted input `x[n-α]` | Predictive deconvolution | Removes predictable repetitive energy |
| Known wavelet `w[n]` | Shaping filter | Shapes input wavelet to desired wavelet |

## Practical considerations

- The filter length and the prewhitening factor are user parameters.
- Longer filters can match the data better but are more sensitive to noise and window length.
- Minimum-phase assumption is implicit in classical spiking deconvolution: the phase of the operator is derived from the amplitude spectrum.

## Teaching intuition

- The Wiener filter asks: "What weighted sum of past input samples best predicts the desired output?"
- The autocorrelation tells us how predictable the signal is; the cross-correlation tells us how the input relates to the desired output.

## Related concepts

- [Deconvolution](deconvolution.md)
- [Statistical deconvolution](statistical_deconvolution.md)
- [Predictive deconvolution](predictive_deconvolution.md)
- [Surface-consistent deconvolution](surface_consistent_deconvolution.md)
- [Minimum phase](minimum_phase.md)

## Sources

- [Verschuur (2006)](../sources/verschuur_2006_predictive_deconvolution.md)
- [Hutchinson & Link (1984)](../sources/hutchinson_link_1984_surface_consistency.md)
- [Hatton, Worthington & Makin (1986)](../sources/hatton_worthington_makin_1986_seismic_data_processing.md)
- [Margrave (2006)](../sources/margrave_2006_methods_of_seismic_data_processing.md)
- [Yilmaz (2001)](../sources/yilmaz_2001_seismic_data_analysis_deconvolution.md)
