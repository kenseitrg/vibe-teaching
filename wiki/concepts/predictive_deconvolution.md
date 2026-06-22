---
title: Predictive deconvolution
status: draft
course_term: 1
sources:
  - verschuur_2006_predictive_deconvolution
tags: [deconvolution, predictive, multiples, reverberations, radon]
---

# Predictive deconvolution

**Predictive deconvolution** removes repetitive (predictable) energy from seismic data by subtracting a prediction of the trace from the trace itself. It does **not** try to remove the source wavelet itself; it targets the repetitive character in the measurements.

## When it applies

- The source signal has a repetitive character (e.g., airgun bubble).
- A shallow layer creates strong reverberations (e.g., shallow water layer).
- Short-period multiples overlap the primary arrival.

## Basic idea

For a shallow water layer, the recorded pressure can be written as:

```text
p(t) = p_primary(t) + r1 · p_primary(t - Δt) + higher-order terms
```

where `Δt = 2 · Dz / v` is the two-way traveltime in the water layer and `r1` is the reflection coefficient at the water bottom.

The goal is to find a filter `f_pred(t)` such that a time-shifted and scaled version of the input predicts the repetitive part, which is then subtracted.

## Predictive filter

Ideal one-step predictive filter:

```text
f_pred(t) = δ(t) + (-r1) · δ(t - Δt)
```

In practice, a short Wiener shaping filter is designed from the autocorrelation of the data at lag `Δt`.

The prediction error (residual) becomes the deconvolved output:

```text
e(t) = y(t) - f_pred(t) * y(t - Δt)
```

## Limitation in the space-time domain

For non-vertical ray paths, the multiple period varies with offset because the ray angle changes. Predictive deconvolution assumes a **constant period**, so it works best on near-zero-offset or angle-sorted data.

## Extension: linear Radon domain

Transform the data to the **linear Radon (τ-p) domain**, where data are organized by ray parameter `p`. In this domain, the multiple period is approximately constant for each `p` trace, so predictive deconvolution can be applied trace-by-trace after muting large `p` values.

## Workflow summary

1. Transform shot gather to linear Radon domain.
2. Apply double-gate predictive deconvolution per `p` trace.
3. Mute large `p` (steep angles) where assumptions break down.
4. Transform back to space-time.

## Teaching intuition

- Predictive deconvolution says: "If I see a wavelet at time `t`, I expect to see a scaled copy at time `t + Δt`. Let me subtract that expected copy."
- It works well for periodic energy but needs the period to be roughly constant across the design window.

## Related concepts

- [Deconvolution](deconvolution.md)
- [Seismic wavelet](seismic_wavelet.md)
- [Wiener filter](wiener_filter.md)
- [Radon transform](radon_transform.md) (stub)

## Sources

- [Verschuur (2006)](../sources/verschuur_2006_predictive_deconvolution.md)
