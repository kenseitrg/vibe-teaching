---
title: Hutchinson & Link (1984) — Surface consistency for noisy seismic data
type: paper
year: 1984
authors: Dave Hutchinson, Brian Link
source_file: papers/deconvolution/Dave Hutchinson, Brian Link - Surface consistency - A solution to the problem of deconvolving noisy seismic data.pdf
status: summarized
tags: [deconvolution, surface-consistent, noise, wavelet]
---

# Hutchinson & Link (1984) — Surface consistency for noisy seismic data

## Source

- **Authors:** Dave Hutchinson (Techco Geophysical Services), Brian Link (Seiscom Delta United)
- **Title:** Surface consistency: A solution to the problem of deconvolving noisy seismic data
- **Year:** 1984
- **Type:** SEG conference paper
- **File:** `papers/deconvolution/Dave Hutchinson, Brian Link - Surface consistency - A solution to the problem of deconvolving noisy seismic data.pdf`

## Main message

Trace-by-trace statistical deconvolution is unreliable on noisy data because each operator is estimated from too little data and is biased by noise (especially ground roll). A **surface-consistent** formulation derives separate source and receiver operators from many traces, yielding more stable and uniform deconvolution.

## Key points

1. **Conventional deconvolution assumptions break down** in the presence of non-white additive noise and short design windows.
2. **Ground roll** is concentrated at low frequencies and changes with offset, so a single pre-filter cannot be optimal for all traces.
3. **Surface-consistent model:** the unit impulse response for each trace is the convolution of a source-location response and a receiver-location response, each associated with near-surface coupling and filtering.
4. **Statistical advantage:** many traces share the same source or receiver location, so operators are estimated from more data.
5. **Noise robustness:** because the system is overdetermined, noisy offset ranges can be omitted; a median-type criterion reduces outlier influence.
6. **Result:** more uniform wavelet character across the section and better preservation of structural character in stack.

## Synthetic example

A wedge model with surface-consistent minimum-phase wavelets was processed with:

- 80 ms spiking deconvolution, trace-by-trace.
- 80 ms surface-consistent spiking deconvolution.

The surface-consistent result better preserved the lower event near the wedge cusp and maintained the hyperbolic reflector shape.

## Implications for teaching

- Good example of how increasing the statistical population improves operator stability.
- Explains why pre-filtering for ground roll is a hit-and-miss approach.
- Shows a practical bridge between deterministic signature methods and trace-by-trace statistical deconvolution.

## Concepts informed

- [Surface-consistent deconvolution](../concepts/surface_consistent_deconvolution.md)
- [Deconvolution](../concepts/deconvolution.md)
- [Wiener filter](../concepts/wiener_filter.md)

## Quotes / memorable lines

> "We believe that a surface-consistent solution to the deconvolution problem will result in the computation of more reliable inverse operators."

> "Surface-consistent deconvolution obviates this problem since there is normally a high degree of redundancy in the solution."
