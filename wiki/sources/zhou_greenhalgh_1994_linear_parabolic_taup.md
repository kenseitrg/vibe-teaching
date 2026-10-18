---
title: "Zhou & Greenhalgh (1994) — Linear and parabolic τ-p transforms revisited"
status: draft
source_type: paper
authors: "Binzhong Zhou, Stewart A. Greenhalgh"
year: 1994
source_file: papers/radon_taup/Binzhong Zhou and Stewart A. Greenhalgh - Linear and parabolic τ-p transforms revisited.pdf
lectures:
  - term02_lec02
related_concepts:
  - radon_transform
  - rho_filter
  - fk_transform
tags: [radon, tau-p, slant-stack, p-deconvolution, aperture, resolution, demultiple]
---

# Zhou & Greenhalgh (1994) — Linear and parabolic τ-p transforms revisited

GEOPHYSICS, VOL. 59, NO. 7 (JULY 1994); P. 1133–1149.

## Main message

For **filtering** applications (e.g. multiple suppression, noise attenuation), the τ-p transform should be derived by defining the **inverse transform first**, then computing the forward transform as its adjoint. With finite-aperture field data the plain forward stack smears events in the p direction; a **p-direction deconvolution** (applied per frequency) compensates for the finite array length, sharpens event focusing, and restores wavelet shape. The deconvolution is required for both linear and parabolic transforms on aperture-limited data — and for the parabolic transform even with infinite aperture.

## Structure and key results

### Historical framing
- Radon (1917) mathematical origin; Hough (1962) transform in image analysis.
- Slant stacking for geophysics originates with **Rieber (1936)**: delayed-and-added recordings forming steered traces with controlled directional sensitivity. Extensively developed in Russia as the **CDR (controlled directional reception)** method (Gardner & Lu, 1991). Useful historical hook for Russian-speaking students.

### Inverse-first philosophy
- The forward transform is usually written as a sum along trajectories (slant stack). For filtering, the data must be **reconstructed** after τ-p processing, so the inverse/adjoint operator is the one that must be well-behaved. Zhou & Greenhalgh derive the continuous pair and then discretize.
- Forward linear τ-p: `u(p,τ) = Σ_x d(x, τ+px)`; inverse (adjoint) distributes energy back along the same trajectories. For sampled data both become matrix operators at each frequency; the pair is not an exact inverse unless deconvolved.

### p-direction deconvolution
- Finite aperture truncates the spatial sum → the τ-p event becomes a smeared, side-lobed wavelet in p rather than a point.
- The smearing is a convolution along p whose length is set by the array length; per-frequency deconvolution in the p direction (with a small white-noise factor) restores focusing and recovers the original wavelet phase/amplitude.
- For the **parabolic** τ-p transform the required deconvolution is present even for infinite aperture (a property of the curvature mismatch), for the **linear** transform it appears with finite aperture.

### Numerical examples
- Linear event, small aperture (70 traces × 10 m, 25 Hz Ricker): without p-decon the expected point is smeared with linear artifacts; with p-decon it focuses and the inverse transform restores the event waveform (no phase distortion).
- Five-layer marine CSP gather with primaries, water-layer multiples and peg-legs: parabolic τ-p (after r²-stretch à la Yilmaz) with p-decon separates the event family cleanly.
- Flow chart (their Fig. 1): FFT over t → per-frequency p-direction deconvolution → inverse FFT over τ — i.e. the "high-resolution" transform is the conventional transform plus deconvolution, per frequency.

## Relation to lecture notes

- Term 2 Lecture 02 (linear noise attenuation): supports Section 8 (inverse Radon challenges) — the adjoint-with-deconvolution idea complements the rho filter (which corrects the time/τ direction, while p-decon corrects the p direction). Also supports the least-squares/high-resolution teaser.
- Term 2 Lecture 03 (multiples): parabolic τ-p with p-decon is a classical demultiple route.

## Related concepts

- [Radon transform](../concepts/radon_transform.md)
- [Rho filter](../concepts/rho_filter.md)

## Related sources

- [Margrave (2006)](margrave_2006_methods_of_seismic_data_processing.md) — least-squares τ-p formulation.
- [Bickel (2000)](bickel_2000_hyperbolic_radon_focusing.md) and [Maeland (1998)](maeland_1998_parabolic_radon.md) — focusing geometry of the transform family.
- [Trad, Ulrych & Sacchi (2002)](trad2002_radon_interpolation.md) — sparse high-resolution Radon.
