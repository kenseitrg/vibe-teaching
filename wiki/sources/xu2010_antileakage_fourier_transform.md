---
title: "Xu, Zhang & Lambaré (2010) — Antileakage Fourier transform for seismic data regularization in higher dimensions"
status: draft
type: paper
source_file: wiki/sources/_raw_text/xu2010.txt
language: en
concepts:
  - seismic_data_regularization
  - anti_leakage_fourier_transform
  - spatial_spectral_leakage
  - nonuniform_fourier_transform
tags: [regularization, alft, fourier, 5d, matching-pursuit, anti-leakage]
---

# Xu, Zhang & Lambaré (2010) — Antileakage Fourier transform in higher dimensions

GEOPHYSICS, VOL. 75, NO. 6 (NOVEMBER-DECEMBER 2010); P. WB113–WB120. DOI: 10.1190/1.3507248. CGGVeritas.

## Overview

This paper generalizes the anti-leakage Fourier transform (ALFT) — originally proposed by Xu & Pham (2004) for 2D/3D common-offset/common-azimuth data — to **higher dimensions** (4D/5D), targeting sparse wide-azimuth acquisition (e.g. WATS in the Gulf of Mexico). The Fourier-regularization philosophy is to estimate Fourier coefficients on an irregular input grid and reconstruct onto any desired grid. The paper names three core difficulties and solves each.

## Key takeaways

- **Three difficulties** of Fourier regularization: (1) spectral leakage, (2) accurate estimation of Fourier components on an irregular grid, (3) an effective anti-aliasing scheme.
- **ALFT iteration** (matching pursuit with a Fourier dictionary): initialize spectrum to zero; compute all Fourier coefficients of the residual via an irregular-grid DFT; pick the maximum-energy coefficient and accumulate it; subtract that component from the residual; iterate until the residual is small. Because the DFT basis is non-orthogonal on an irregular grid, the same component may be re-selected and contributions accumulate over iterations.
- **Irregular-grid DFT** with an integral weight $w(x)$: $\hat f(k)=\frac{1}{\sum w}\sum_p w(x_p) f(x_p)e^{-2\pi i k\cdot x_p}$.
- **Weighting in high dimensions:** 1D uses sample spacing; 2D uses Voronoi polygons (Canning & Gardner 1998) or Pipe-Menon (Zwartjes & Gisolf 2002); higher dimensions often use a discontinuous "hit-count" weight. The authors instead build a smooth **sampling density** by convolving sample locations with a Gaussian and set $w(x)=1/\rho(x)$ — a sampling-density-function weighting. ALFT is fairly insensitive to the weight, but a good one speeds convergence.
- **Cost and windowing:** a full high-dimensional ALFT is $\sim O(N^2 N_p)$ per iteration. Windowing cuts cost but undersamples the wavenumber domain and causes Gibbs artifacts; the fix is a **wavenumber-domain oversampling** least-squares inversion per iteration, enabling small windows.
- **Cascaded 5D via two 3D passes:** common-shot + common-receiver 3D regularizations can recover 5D data with lower-dimensional schemes, though this is weaker for large irregular acquisition holes — motivating true high-dimensional interpolation (cf. Trad 2009).
- Validated on Marmousi synthetic and a real WATS dataset.

## Relation to lecture notes

The central modern reference for Term 3 Lecture 06 §4 (ALFT): the leakage concept (§4.2), the matching-pursuit reconstruction (§4.3), the multi-dimensional/NUFFT implementation (§4.2), and the weighting/anti-aliasing parameters (§4.5–4.6) all draw directly on this paper.

## Related sources

- [Schonewille et al. (2009)](schonewille2009_aa_alft.md) — anti-alias ALFT extension.
- [Schonewille et al. (2013)](schonewille2013_mpfi_priors.md) — matching-pursuit Fourier interpolation with priors.
- [Trad (2009)](trad2009_5d_interpolation.md) — 5D interpolation context.
- [Zwartjes & Sacchi (2007)](zwartjes2006_fourier_reconstruction.md) — least-squares Fourier reconstruction.
