---
title: Deconvolution
status: draft
course_term: 1
sources:
  - cgg_odt04_deconvolution_part1_wavelet
  - verschuur_2006_predictive_deconvolution
  - hutchinson_link_1984_surface_consistency
tags: [deconvolution, inverse-filter, wavelet, resolution]
---

# Deconvolution

**Deconvolution** is the process of undoing the effects of a convolution. In seismic processing it is used to remove or reshape the seismic wavelet and to suppress repetitive signals such as short-period multiples, reverberations, and ghosts.

## Core idea

The recorded seismic trace can be modeled as a convolution of the earth's reflectivity series with the seismic wavelet (plus noise):

```text
trace(t) = reflectivity(t) * wavelet(t) + noise(t)
```

Deconvolution designs an **inverse filter** that, when convolved with the trace, compresses the wavelet toward a spike or a desired shape and removes predictable repetitive energy.

## What deconvolution can address

| Effect | Description | Common method |
|--------|-------------|---------------|
| Source signature / bubble | Oscillating airgun bubble energy following every event | Signature deconvolution, debubbling |
| Source and receiver ghosts | Free-surface reflections close to the source/receiver | Ghost deconvolution, designature |
| Short-period multiples / reverberations | Energy bouncing in a shallow layer | Predictive deconvolution |
| Band-limited wavelet | Loss of resolution from ghosts and acquisition bandwidth | Spiking / Wiener deconvolution |
| Near-surface source/receiver effects | Variable coupling and filtering at the surface | Surface-consistent deconvolution |

## Main families

1. **Deterministic deconvolution** — uses a known or measured wavelet (source signature, far-field signature).
2. **Statistical deconvolution** — estimates the wavelet from the data itself, typically assuming the reflectivity is white and the wavelet is minimum phase.
3. **Predictive deconvolution** — removes repetitive energy by predicting and subtracting the predictable part of the trace.
4. **Surface-consistent deconvolution** — decomposes the trace-by-trace wavelet into source, receiver, offset, and CDP components to stabilize operators across noisy data.

## Key assumptions and pitfalls

- Reflectivity is approximately white (random amplitudes and arrival times).
- The wavelet is minimum phase for Wiener/spiking deconvolution; phase errors occur if this is wrong.
- Additive noise with a different spectrum than the signal distorts the derived operator.
- Short design windows and strong multiples can make operators unreliable.

## Related concepts

- [Seismic wavelet](seismic_wavelet.md)
- [Predictive deconvolution](predictive_deconvolution.md)
- [Surface-consistent deconvolution](surface_consistent_deconvolution.md)
- [Wiener filter](wiener_filter.md)
- [Comparison of deconvolution methods](../comparisons/deconvolution_methods.md)

## Sources

- [Hutchinson & Link (1984)](../sources/hutchinson_link_1984_surface_consistency.md)
- [Verschuur (2006)](../sources/verschuur_2006_predictive_deconvolution.md)
- [CGG ODT04 Part 1](../sources/cgg_odt04_deconvolution_part1_wavelet.md)
