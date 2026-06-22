---
title: Verschuur (2006) — EAGE EET 03, Predictive Deconvolution
type: course slides
year: 2006
author: Eric Verschuur
source_file: papers/deconvolution/EAGE EET 03 - Predictive Deconvolution.pdf
status: reviewed
tags: [deconvolution, predictive, wiener-filter, radon, multiples]
---

# Verschuur (2006) — EAGE EET 03, Predictive Deconvolution

## Source

- **Author:** Eric Verschuur (Delft University of Technology)
- **Title:** Seismic Multiple Removal Techniques: Past, Present and Future — Chapter 3: Predictive Deconvolution
- **Year:** 2006
- **Type:** EAGE Education Course slides
- **File:** `papers/deconvolution/EAGE EET 03 - Predictive Deconvolution.pdf`

## Main message

Predictive deconvolution removes repetitive energy from seismic data by designing a short filter that predicts the predictable part of the trace and subtracting it. It can be applied in the time domain or in the linear Radon domain for better handling of angle-dependent multiple periods.

## Key points

1. **Adaptive filter design:** Given `x(t)` and desired `y(t)`, find short filter `f(t)` such that `y(t) ≈ f(t) * x(t)`. This leads to the Wiener normal equations.
2. **Predictive deconvolution target:** remove the repetitive character of the seismic measurements, not the source wavelet itself.
3. **Typical applications:**
   - Airgun bubble effects.
   - Shallow-water-layer reverberations.
4. **Filter form:** ideally `f_pred(t) = δ(t) + (-r1)·δ(t - Δt)`, where `Δt = 2·Dz/v`.
5. **Limitation in `x-t`:** for non-vertical rays the multiple period varies with offset, so the constant-period assumption breaks down.
6. **Solution in τ-p domain:** data are organized by ray parameter `p`, where the period is constant per trace. Apply predictive deconvolution per `p`, mute large `p`, then transform back.

## Mathematical summary

Wiener filter objective:

```text
ε = Σ ( y[n] - Σ_{k=0}^{N} f[k]·x[n-k] )² → min
```

Normal equations:

```text
Σ_{k=0}^{N} f[k]·φ_xx[i-k] = φ_yx[i],   i = 0,...,N
```

The autocorrelation matrix is Toeplitz, so the system is solved efficiently by the Wiener-Levinson algorithm.

## Implications for teaching

- Provides a clean derivation of Wiener filter normal equations suitable for students with basic signal-processing background.
- Explains why predictive deconvolution works for short-period multiples but needs angle-domain treatment for long offsets.
- Good source for the link between deconvolution and the linear Radon transform.

## Concepts informed

- [Predictive deconvolution](../concepts/predictive_deconvolution.md)
- [Wiener filter](../concepts/wiener_filter.md)
- [Deconvolution](../concepts/deconvolution.md)

## Quotes / memorable lines

> "Predictive deconvolution aims at removing a repetitive character from the seismic measurements, not the source signal itself."

> "The multiple period is not constant for non-vertical propagation."
