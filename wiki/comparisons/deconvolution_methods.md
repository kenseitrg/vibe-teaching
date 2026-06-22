---
title: Comparison of deconvolution methods
status: draft
sources:
  - verschuur_2006_predictive_deconvolution
  - hutchinson_link_1984_surface_consistency
  - cgg_odt04_deconvolution_part1_wavelet
tags: [deconvolution, comparison, predictive, surface-consistent, spiking]
---

# Comparison of deconvolution methods

## Overview

Different deconvolution methods target different parts of the recorded wavelet and make different assumptions. Choosing the right method depends on what distorts the data and what prior information is available.

## Side-by-side

| Method | Target | Input required | Key assumption | Best for | Main risk |
|--------|--------|----------------|----------------|----------|-----------|
| **Spiking / Wiener deconvolution** | Compress wavelet toward a spike | Seismic traces | Reflectivity is white; wavelet is minimum phase | General wavelet compression, resolution boost | Phase errors if wavelet is not minimum phase; noise biases operator |
| **Predictive deconvolution** | Remove repetitive energy | Seismic traces + prediction lag | Multiple/reverberation period is constant in design window | Bubble energy, shallow-water reverberations, short-period multiples | Breaks down at far offsets where period varies |
| **Surface-consistent deconvolution** | Separate source/receiver/near-surface effects | Traces sorted by source/receiver location | Wavelet factors multiply into source and receiver components | Noisy land data, variable coupling, multiple-prone areas | More complex; needs adequate surface-location redundancy |
| **Signature / deterministic deconvolution** | Remove known source signature | Measured or modeled source signature | Signature is accurately known | Marine data with calibrated far-field signature | Signature errors propagate; ignores receiver ghost and earth filtering |
| **FX deconvolution** | Attenuate random noise / interpolate | Common-offset or common-shot gathers | Signal is predictable spatially, noise is random | Random noise attenuation, spatial interpolation | Can smear coherent signal if misapplied |

## Choosing a method

1. **Start with the wavelet model:** what components are present? Source signature? Ghosts? Bubble? Reverberations?
2. **Check data quality:** is the data noisy? Is ground roll present? Are there variable coupling conditions?
3. **Check acquisition geometry:** are offsets long enough that multiple periods vary significantly?
4. **Check available information:** do you have a measured signature or must you estimate statistically?

## How methods combine

A typical marine processing flow might use several methods in sequence:

```text
raw data
   → designature / debubbling (deterministic or statistical)
   → predictive deconvolution (remove short-period multiples / reverberations)
   → surface-consistent deconvolution (stabilize wavelet across noisy/varied data)
   → final zero-phase shaping
```

## Related concepts

- [Deconvolution](../concepts/deconvolution.md)
- [Predictive deconvolution](../concepts/predictive_deconvolution.md)
- [Surface-consistent deconvolution](../concepts/surface_consistent_deconvolution.md)
- [Wiener filter](../concepts/wiener_filter.md)
- [Seismic wavelet](../concepts/seismic_wavelet.md)

## Sources

- [Verschuur (2006)](../sources/verschuur_2006_predictive_deconvolution.md)
- [Hutchinson & Link (1984)](../sources/hutchinson_link_1984_surface_consistency.md)
- [CGG ODT04 Part 1](../sources/cgg_odt04_deconvolution_part1_wavelet.md)
