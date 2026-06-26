---
title: Surface-consistent deconvolution
status: draft
course_term: 1
sources:
  - hutchinson_link_1984_surface_consistency
  - yilmaz_2001_seismic_data_analysis_deconvolution
tags: [deconvolution, surface-consistent, source, receiver, noise, wavelet]
---

# Surface-consistent deconvolution

**Surface-consistent deconvolution** designs separate deconvolution operators for the source and receiver surface locations, then combines them to form the trace operator. The idea is that wavelet variations at the surface are controlled by source coupling, receiver coupling, and the near-surface layer, all of which are surface-location dependent.

## Why trace-by-trace deconvolution can fail

In conventional trace-by-trace Wiener deconvolution:

- Each operator is designed from only a short window of one trace.
- Noise (especially ground roll) has a different spectrum than reflections and biases the operator.
- Short design windows and strong multiples produce unstable, trace-to-trace varying operators.
- Variable ground coupling and near-surface filtering are not compensated.

A trace-by-trace operator may therefore introduce phase and amplitude distortions that change with offset and location.

## Surface-consistent model

Each trace is written as a convolution of four surface-consistent factors and the subsurface reflectivity:

```text
trace_{s,r,h,c}(t) = source_s(t) * receiver_r(t) * offset_h(t) * cdp_c(t) * reflectivity_{s,r,h,c}(t)
```

The deconvolution operator for that trace is then:

```text
operator_{s,r,h,c}(t) = source_operator_s(t) * receiver_operator_r(t) * offset_operator_h(t) * cdp_operator_c(t)
```

In this split, source and receiver factors mainly represent near-surface coupling and shallow-layer filtering that should be compensated. Offset and CDP factors carry the geological response (moveout, AVO, stratigraphy) that should be preserved. Once the near-surface source/receiver effects are removed, a single stable spiking operator can be applied across the survey instead of a separate noisy operator for each trace.

## Advantages

- **More statistics**: many traces share the same source or receiver location, so each operator is estimated from more data.
- **Noise robustness**: noisy offsets can be excluded from the design; a median or robust criterion reduces the influence of outliers.
- **Uniformity**: the final stack has more consistent wavelet character across the section.
- **Compensation for near-surface effects**: source and receiver coupling variations are explicitly separated.
- **Stable spiking operator**: the corrected data allow a single, survey-wide operator rather than trace-by-trace estimates.

## Practical notes

- The method derives amplitude spectra in a surface-consistent way and can use minimum-phase spiking operators.
- It is the preferred deconvolution approach for land and OBC data, where source/receiver coupling and the near surface vary across the survey.
- It is also useful in multiple-prone areas where conventional deconvolution is unstable.
- It does not remove all noise; after correcting the embedded wavelet, zero-phase spectral balancing can be applied.

## Synthetic example (Hutchinson & Link, 1984)

A wedge model with surface-consistent minimum-phase wavelets showed that trace-by-trace deconvolution partially collapsed the lower event near the cusp and altered the upper event, while surface-consistent deconvolution preserved the hyperbolic reflector character.

## Teaching intuition

- Instead of asking "what is the wavelet on this trace?", ask "what wavelet effects are associated with this shot location and this receiver location?".
- Because the same surface location appears in many traces, the answer is more stable.

## Related concepts

- [Deconvolution](deconvolution.md)
- [Statistical deconvolution](statistical_deconvolution.md)
- [Wiener filter](wiener_filter.md)
- [Predictive deconvolution](predictive_deconvolution.md)

## Sources

- [Hutchinson & Link (1984)](../sources/hutchinson_link_1984_surface_consistency.md)
- [Yilmaz (2001)](../sources/yilmaz_2001_seismic_data_analysis_deconvolution.md)
