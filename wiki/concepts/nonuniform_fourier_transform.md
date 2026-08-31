---
title: Non-uniform Fourier transform
status: draft
sources:
  - xu2010_antileakage_fourier_transform
  - zwartjes2006_fourier_reconstruction
tags: [fourier-transform, regularization, nufft, sampling, computation]
---

# Non-uniform Fourier transform (NUFFT)

A non-uniform Fourier transform computes Fourier coefficients of data sampled at **irregular** spatial locations — or evaluates a spectrum back onto an irregular grid. It is the computational enabler behind Fourier-based [regularization](seismic_data_regularization.md): without it, every iteration of the [ALFT](anti_leakage_fourier_transform.md) would require an expensive direct DFT.

## The problem with a plain DFT

The DFT assumes equally spaced samples so it can use the fast Fourier transform (FFT, $O(N\log N)$). Irregular acquisition breaks that assumption. A direct irregular-grid DFT,

$$\hat{f}(k) = \sum_p w(x_p)\,f(x_p)\,e^{-2\pi i k\cdot x_p},$$

costs $O(N\,N_p)$ per wavenumber and cannot use the FFT.

## Two directions

- **Non-uniform samples → uniform spectrum (analysis).** Used in the ALFT forward step.
- **Uniform spectrum → non-uniform samples (adjoint).** Used to subtract a chosen component back onto the irregular input grid, and in gridding.

## Making it fast: gridding

The standard trick (Fourmont 2003; the gridding method of O'Sullivan) is:

1. **Spread** the irregular samples onto a nearby regular oversampled grid using a smooth kernel (e.g. Gaussian — the same kernel Xu et al. 2010 use for their sampling-density weight).
2. Apply a regular **FFT** on that grid.
3. **Correct** for the kernel's effect (deconvolution in the Fourier domain).

This brings the cost close to that of an FFT while handling arbitrary sample locations. Least-squares Fourier reconstruction (Zwartjes & Sacchi 2007; Meng et al. 2008) wraps the same non-uniform forward/adjoint operators inside an iterative inversion.

## Role in regularization

In the ALFT, the NUFFT is called repeatedly: once to analyse the residual spectrum, once per selected component to map it back to the input grid for subtraction. A fast NUFFT is therefore what makes high-dimensional (4D/5D) regularization feasible at all. Windowing plus wavenumber-domain oversampling (Xu et al. 2010) further reduces the cost for large 5D problems.

## Related concepts

- [Anti-leakage Fourier transform](anti_leakage_fourier_transform.md)
- [Spatial spectral leakage](spatial_spectral_leakage.md)
- [Discrete Fourier transform](discrete_fourier_transform.md)
- [Seismic data regularization](seismic_data_regularization.md)

## Sources

- Xu, Zhang & Lambaré (2010) — irregular-grid DFT with sampling-density weighting; windowed high-dimensional implementation.
- Zwartjes & Sacchi (2007) — least-squares Fourier reconstruction built on non-uniform Fourier operators.
