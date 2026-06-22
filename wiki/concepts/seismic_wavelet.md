---
title: Seismic wavelet
status: draft
course_term: 1
sources:
  - cgg_odt04_deconvolution_part1_wavelet
tags: [wavelet, source-signature, ghost, bubble, bandwidth, resolution]
---

# Seismic wavelet

The **seismic wavelet** is the effective impulse response that convolves with the earth's reflectivity to produce the recorded seismic trace. It is not a single fixed shape: it is built from several components and varies with source/receiver depth, propagation angle, and acquisition geometry.

## Components of the recorded wavelet (marine streamer)

For a conventional marine streamer, the raw wavelet is approximately:

```text
raw_wavelet = source_signature * source_ghost * receiver_ghost * recording_system_response
```

| Component | What it is | Effect |
|-----------|------------|--------|
| **Source signature** | Combined output of the airgun array | Main peak plus residual bubble energy |
| **Source ghost** | Free-surface reflection of upward source energy | Delayed, polarity-reversed copy of the signature |
| **Receiver ghost** | Free-surface reflection of upward recorded energy | Additional delayed, polarity-reversed copy |
| **Recording system response** | Hydrophone, filters, ADC | Embedded in the delivered signature |

## Key quantities

- **Vertical source signature**: equivalent point-source output for vertically traveling energy.
- **Far-field signature**: source signature convolved with the source ghost; often delivered with the data.
- **Raw recorded wavelet**: far-field signature convolved with the receiver ghost and pre-processing filters.

## Ghosts and the amplitude spectrum

A ghost is a time-delayed, polarity-reversed copy of the primary signal. It creates **notches** in the amplitude spectrum at frequencies:

```text
f_notch ≈ n · v_water / (2 · depth)     for n = 0, 1, 2, ...
```

- Source depth and cable depth each produce their own notch series.
- The first notch from the source ghost is at 0 Hz (n=0); the first non-zero notch is at `v / (2 · d_source)`.
- Ghost notches limit usable bandwidth and therefore resolution.

### Example

Source depth = 6 m, cable depth = 8 m ± 1 m, water velocity = 1500 m/s:

- Source ghost first non-zero notch: `1500 / (2 · 6) = 125 Hz`.
- Receiver ghost first notch range: `1500 / (2 · 9) ≈ 83 Hz` to `1500 / (2 · 7) ≈ 107 Hz`.

## Directionality

The source signature and ghosts vary with propagation angle:

- Horizontal ray paths experience stronger ghost cancellation.
- Notch frequency increases with angle/offset and decreases with depth.
- For variable-depth cables (BroadSeis), different receiver depths give different notch diversity that can be exploited to remove receiver ghosts.

## Desired wavelet properties

| Property | Why it matters |
|----------|----------------|
| **Zero phase** | Event time is unambiguously at the wavelet center peak |
| **Broad bandwidth** | High resolution (sharp, low side-lobes) |
| **No bubble / ghost artifacts** | Cleaner reflectivity series |
| **Angle-independent** | Consistent amplitudes for AVA analysis |

## Teaching intuition

- The raw wavelet is mostly made of **multiples**: ghost energy dominates the side lobes.
- A spike has a white spectrum; real wavelets are band-limited because of ghosts and finite source bandwidth.
- Both low and high frequencies are needed for resolution.

## Related concepts

- [Deconvolution](deconvolution.md)
- [Predictive deconvolution](predictive_deconvolution.md)

## Sources

- [CGG ODT04 Part 1](../sources/cgg_odt04_deconvolution_part1_wavelet.md)
