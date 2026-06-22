---
title: Surface-consistent deconvolution
status: draft
course_term: 1
sources:
  - hutchinson_link_1984_surface_consistency
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

Each trace can be written as a convolution of a source-location wavelet, a receiver-location wavelet, and the subsurface reflectivity:

```text
trace_{s,r}(t) = source_s(t) * receiver_r(t) * reflectivity_{s,r}(t)
```

The deconvolution operator for that trace is then:

```text
operator_{s,r}(t) = source_operator_s(t) * receiver_operator_r(t)
```

## Advantages

- **More statistics**: many traces share the same source or receiver location, so each operator is estimated from more data.
- **Noise robustness**: noisy offsets can be excluded from the design; a median or robust criterion reduces the influence of outliers.
- **Uniformity**: the final stack has more consistent wavelet character across the section.
- **Compensation for near-surface effects**: source and receiver coupling variations are explicitly separated.

## Practical notes

- The method derives amplitude spectra in a surface-consistent way and can use minimum-phase spiking operators.
- It is especially useful in noisy land data and in multiple-prone areas where conventional deconvolution is unstable.
- It does not remove all noise; after correcting the embedded wavelet, zero-phase spectral balancing can be applied.

## Synthetic example (Hutchinson & Link, 1984)

A wedge model with surface-consistent minimum-phase wavelets showed that trace-by-trace deconvolution partially collapsed the lower event near the cusp and altered the upper event, while surface-consistent deconvolution preserved the hyperbolic reflector character.

## Teaching intuition

- Instead of asking "what is the wavelet on this trace?", ask "what wavelet effects are associated with this shot location and this receiver location?".
- Because the same surface location appears in many traces, the answer is more stable.

## Related concepts

- [Deconvolution](deconvolution.md)
- [Wiener filter](wiener_filter.md)

## Sources

- [Hutchinson & Link (1984)](../sources/hutchinson_link_1984_surface_consistency.md)
