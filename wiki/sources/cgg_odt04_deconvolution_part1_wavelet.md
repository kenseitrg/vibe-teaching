---
title: CGG ODT04 Part 1 — The Seismic Wavelet
type: training slides
year: 2015
author: CGG (internal training)
source_file: papers/deconvolution/ODT04_DECONVOLUTION_PART1_v7.0_sesimic_wavelet.pptx
status: summarized
tags: [wavelet, source-signature, ghost, bubble, bandwidth, resolution]
---

# CGG ODT04 Part 1 — The Seismic Wavelet

## Source

- **Author:** CGG UK Training
- **Title:** ODT04 Deconvolution Part 1: The Seismic Wavelet
- **Version:** 7.0, June 2015
- **Type:** Internal training slides
- **File:** `papers/deconvolution/ODT04_DECONVOLUTION_PART1_v7.0_sesimic_wavelet.pptx`

**Note:** Internal CGG training document; images do not have show rights.

## Main message

Before applying deconvolution, one must understand the components of the recorded seismic wavelet and how they vary. The raw marine streamer wavelet is built from the source signature convolved with source and receiver ghosts; it is not zero phase, it has side lobes and notches, and it varies with angle and depth.

## Key points

1. **Deconvolution is an inverse filter.** Many processing steps (signature decon, predictive decon, FX decon, debubbling, shaping, matching) use the same mathematical tool.
2. **The wavelet is a chain of convolutions:** source command → source signature → recording system response → source ghost → receiver ghost → pre-processing filters.
3. **Source signature:** combined output of an airgun array; not a point source. Arrays are tuned so vertical peaks sum constructively and bubble energy cancels.
4. **Vertical source signature** is the equivalent point-source output for vertical rays.
5. **Far-field signature** = vertical source signature convolved with the source ghost.
6. **Ghosts** are time-delayed, polarity-reversed copies from the free surface. They create notches in the amplitude spectrum:
   ```text
   f_notch ≈ n · v / (2 · depth)
   ```
7. **Raw recorded wavelet** = far-field signature × receiver ghost × pre-processing filters.
8. **Source directivity:** signature and ghosts vary with propagation angle and azimuth.
9. **Desired wavelet:** zero phase, broad bandwidth, no bubble/ghost artifacts, angle-independent.
10. **Resolution:** broader bandwidth (low + high frequencies) gives sharper wavelets.

## Ghost notch example

Source depth = 6 m, cable depth = 8 m ± 1 m, water velocity = 1500 m/s:

- Source ghost first non-zero notch: 125 Hz.
- Receiver ghost first notch range: 83–107 Hz.

## Practical implications

- The delivered far-field signature usually includes the source ghost but not the receiver ghost.
- Receiver ghost modeling is typically the processing team's responsibility.
- Variable-depth cables (BroadSeis) exploit receiver-notch diversity to remove receiver ghosts.
- Bubble energy is part of the source signature, not a multiple, but it can be confused with short-period multiples.

## Implications for teaching

- Excellent source for physical/geometric intuition about the seismic wavelet.
- Explains why raw wavelets are mixed-phase and band-limited before any processing.
- Provides concrete numbers and exercises for ghost-notch calculations.

## Concepts informed

- [Seismic wavelet](../concepts/seismic_wavelet.md)
- [Deconvolution](../concepts/deconvolution.md)

## Quotes / memorable lines

> "Deconvolution undoes the effects of a convolution, hence the name. It is an inverse filter."

> "Most of what we consider the seismic wavelet could be said to be made up of multiples."

> "Broad bandwidth is required for high resolution wavelets. Not just high frequencies, but the low frequencies as well."
