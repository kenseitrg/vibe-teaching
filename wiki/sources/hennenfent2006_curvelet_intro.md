---
title: "Hennenfent & Herrmann (2006) — Seismic Denoising with Nonuniformly Sampled Curvelets"
status: draft
type: paper
source_file: papers/noise_attenuation/curvelets/hennenfent2006.txt
language: en
concepts:
  - seismic_data_processing
  - seismic_noise
  - adaptive_subtraction
tags: [noise-attenuation, curvelet, denoising, nonuniform-sampling, binning]
---

# Hennenfent & Herrmann (2006) — Seismic Denoising with Nonuniformly Sampled Curvelets

Published in *Computing in Science & Engineering*, 8(3), 16--25, 2006.

## Overview

This paper extends the fast discrete curvelet transform (FDCT) to handle nonuniformly sampled data via the nonequally sampled fast Fourier transform (NFFT). Seismic data volumes are typically acquired irregularly due to obstacles (buildings, lakes) or uncontrolled source positions (passive seismology). Treating irregularly sampled data as uniformly sampled destroys wavefront continuity and degrades curvelet performance. The proposed nonuniformly sampled FDCT (NFDCT) simultaneously performs denoising and binning (mapping irregular data to a regular grid).

## Key takeaways

- Curvelets are multiscale, multidirectional frames with parabolic scaling (width ~ length^2), well adapted to representing wavefronts in seismic data.
- For 2-D data with piecewise C^2 singularities, curvelets achieve near-optimal nonlinear approximation rates O(L^{-2}), outperforming Fourier O(L^{-1/2}) and wavelets O(L^{-1}).
- The NFDCT factors the regular FDCT as C = T*F, then replaces the standard FFT with the NFFT pseudo-inverse, producing curvelet coefficients on a regular Fourier grid from irregular spatial data.
- Denoising is performed by soft thresholding of curvelet coefficients: m_hat = C^T * Sw(C * d), where Sw is element-wise soft thresholding with threshold w = 3*sigma.
- Coherent signal separation (e.g., primary-multiple separation) uses a weighted threshold w = max(3*sigma*delta, |C*s2_hat|) where s2_hat is the predicted noise component.
- On synthetic nonuniformly sampled data at 0 dB SNR, the combined NFFT binning and denoising achieved 8 dB SNR, losing only 1 dB compared to denoising alone on noise-free binned data.

## Relation to lecture notes

This paper provides the theoretical foundation for curvelet-domain noise attenuation, covered in Term 3 Lecture 04 -- Noise Attenuation. It introduces the shrinkage/denoising framework that is generalized in later papers (Herrmann et al. 2007, Hennenfent et al. 2011, Kustowski et al. 2013).

## Related sources

- [Herrmann et al. (2007)](herrmann2007_curvelet_multiple_separation.md) -- Non-linear primary-multiple separation using curvelets
- [Hennenfent et al. (2011)](hennenfent2011_interpretative_noise.md) -- Interpretative curvelet noise attenuation on real data
- [Demanet & Ying (2007)](demanet_ying_mirror_extended.md) -- ME-curvelets for boundary handling
