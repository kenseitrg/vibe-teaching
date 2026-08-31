---
title: "Demanet & Ying (2007) — Curvelets and Wave Atoms for Mirror-Extended Images"
status: draft
type: paper
source_file: papers/noise_attenuation/curvelets/mirrorextended.txt
language: en
concepts:
  - seismic_data_processing
  - seismic_noise
  - frequency_filtering
tags: [curvelet, wave-atom, mirror-extension, boundary-conditions, discrete-cosine-transform]
---

# Demanet & Ying (2007) — Curvelets and Wave Atoms for Mirror-Extended Images

Preprint, July 2007. Included in Curvelab and WaveAtom toolboxes.

## Overview

Standard discrete curvelet and wave atom transforms use the FFT, which implicitly periodizes the image at boundaries. This creates wrap-around artifacts where basis functions near one edge connect to the opposite edge -- a problem when the contrast at opposite edges is unphysical. This paper introduces mirror-extended (ME) variants of both transforms that tile the discrete cosine domain (DCT) instead of the discrete Fourier domain, eliminating boundary artifacts without increasing redundancy or computational complexity in the shift-invariant case.

## Key takeaways

- The standard FDCT via wrapping tiles the discrete Fourier domain; basis functions near image edges wrap around periodically, creating artifacts for images where opposite-edge contrasts are unphysical.
- ME-curvelets work by tiling the DCT domain of the original image rather than the DFT domain, combined with adequate reorganization of in-tile data.
- For shift-invariant ME-curvelets and ME-wave atoms, there is no penalty on redundancy or computational complexity compared to the periodized versions.
- For shift-variant wave atoms, the penalty is a factor of 2 (compared to a naive factor of 4 from simply applying the transform to the mirror-extended image).
- The key algorithm modification: replace the 2D FFT with a DCT, then reorganize the frequency-domain data within each scale-angle tile to account for the mirror symmetry.
- Curvelets are good for representing edges and bandlimited wavefronts; wave atoms are good for oscillatory patterns and textures. The ME variants extend both to situations where periodization at boundaries is inappropriate.

## Relation to lecture notes

This paper addresses a practical implementation detail of curvelet transforms relevant to seismic data processing (Term 3 Lecture 04 -- Noise Attenuation). Seismic data often has sharp boundaries at survey edges where periodic boundary conditions are physically meaningless. ME-curvelets provide a cleaner implementation for such data, and are included in the standard Curvelab toolbox used in research.

## Related sources

- [Hennenfent & Herrmann (2006)](hennenfent2006_curvelet_intro.md) -- FDCT for seismic denoising
- [Herrmann et al. (2007)](herrmann2007_curvelet_multiple_separation.md) -- Curvelet-based primary-multiple separation
