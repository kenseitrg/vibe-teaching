---
title: "Treitel (1974) — The Complex Wiener Filter"
status: draft
type: paper
source_file: papers/noise_attenuation/fx_deconvolution/treitel1974.txt
language: en
concepts:
  - wiener_filter
  - deconvolution
  - seismic_data_processing
  - seismic_noise
tags: [wiener-filter, complex-arithmetic, hermitian-matrix, least-squares, fx-deconvolution]
---

# Treitel (1974) — The Complex Wiener Filter

*Geophysics*, 39(2), 169--173.

## Overview

This paper derives the Wiener filter formulation for complex-valued inputs and desired outputs, generalizing the standard real-valued Wiener filter theory. The resulting complex normal equations involve a Hermitian autocorrelation matrix R (rather than a symmetric one) and a complex cross-correlation vector g. An efficient solution algorithm exploits the block-Toeplitz structure of the expanded real system, avoiding the need for complex arithmetic in the digital computer. This work provides the mathematical foundation for f-x deconvolution as later developed by Canales (1984) and Gulunay (1986).

## Key takeaways

- For complex-valued input x_t, desired output d_t, and filter f_t, the error energy I = e^H * e is minimized when the normal equations R*f = g are satisfied, where R = X^H * X is Hermitian and g = X^H * d.
- The complex autocorrelation matrix R = P + iQ, where P is real symmetric and Q is real skew-symmetric; the expanded 2(m+1) system has block-Toeplitz structure solvable by Robinson's recursive algorithm.
- The normalized error energy epsilon = 1 - (g^H * f) / delta provides a quality measure analogous to the real-valued case; epsilon must satisfy 0 <= epsilon <= 1.
- The formal solution f = R^{-1} * g parallels the real-valued case, but with Hermitian transpose replacing ordinary transpose throughout.
- An explicit worked example with a 2-length complex input sequence demonstrates the complete computation, including the complex convolution and normalized error energy calculation.
- The primary application motivation was holographic deconvolution of earth holograms recorded as amplitude and phase observations at sensor positions.

## Relation to lecture notes

This paper provides the mathematical foundation for the complex Wiener filter used in f-x deconvolution, discussed in Term 3 Lecture 04 -- Noise Attenuation. The complex normal equations (equation 3) are the same equations solved independently at each frequency in the f-x domain, making this paper essential background for understanding why f-x deconvolution works.

## Related sources

- [Canales (1984)](canales1984_fx_decon.md) -- Applies complex Wiener prediction in f-x domain
- [Gulunay (1986)](gulunay1986_fxdecon.md) -- Practical FXDECON implementation using Treitel's theory
- [Abma & Claerbout (1995)](abma1995_lateral_prediction.md) -- Compares f-x and t-x prediction approaches
