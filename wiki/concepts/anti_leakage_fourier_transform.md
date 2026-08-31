---
title: Anti-leakage Fourier transform (ALFT)
status: draft
sources:
  - xu2010_antileakage_fourier_transform
  - schonewille2009_aa_alft
  - schonewille2013_mpfi_priors
tags: [regularization, fourier-transform, matching-pursuit, anti-leakage, 5d]
---

# Anti-leakage Fourier transform (ALFT)

The anti-leakage Fourier transform (ALFT) is the workhorse algorithm for modern Fourier-based [regularization](seismic_data_regularization.md). It estimates a sparse spatial Fourier spectrum from irregularly sampled data using iterative [matching pursuit](matching_pursuit.md), sidestepping [spectral leakage](spatial_spectral_leakage.md). It was introduced by Xu & Pham (2004) and generalized to higher dimensions by Xu, Zhang & Lambaré (2010).

## The algorithm

Work in the time-frequency domain (a temporal FFT first, so only the spatial axes are irregular). At each temporal frequency:

1. **Initialize** all Fourier components to zero; the residual equals the input data.
2. **Forward DFT on the irregular grid** — compute every spatial Fourier coefficient of the residual:

   $$\hat{f}(k) = \frac{1}{\sum w(x)}\sum_{p} w(x_p)\,f(x_p)\,e^{-2\pi i k\cdot x_p},$$

   where $w(x)$ is an integral weight (see below).
3. **Pick the strongest** coefficient $\hat{f}_\text{max}(k)$ and add it to the accumulated spectrum.
4. **Subtract** that single component from the residual:

   $$f_u(x) = f(x) - \hat{f}_\text{max}(k)\,e^{2\pi i k\cdot x}.$$
5. **Iterate** steps 2–4 until the residual is small enough.

Because the same component can be re-selected in later iterations (the basis is not orthogonal on an irregular grid), contributions to a given $k$ accumulate gradually and the leakage from already-explained energy is removed at every step. The final spectrum is then inverted onto any desired output grid with a standard inverse DFT/FFT.

## Three difficulties, three solutions

Xu et al. (2010) identify the three core challenges and the ALFT answers:

| Difficulty | ALFT solution |
|------------|---------------|
| Spectral leakage | iterative matching pursuit (peel off the strongest component) |
| Accurate coefficient estimation on an irregular grid | a smooth **area/sampling-density weighting** scheme |
| Effective anti-aliasing | low-frequency spectral weights applied at high frequencies (see [AA-ALFT](#anti-alias-alft)) |

### Weighting function

The integral weight $w(x)$ controls how each irregular sample contributes to the DFT sum. Choices by dimension:

- **1D:** distance to neighbouring samples.
- **2D:** Voronoi-cell areas (Canning & Gardner 1998) or the Pipe-Menon scheme (Zwartjes & Gisolf 2002).
- **Higher dimensions:** a "hit-count" (samples per bin) estimate — but this is discontinuous and biases the coefficients.

Xu et al. (2010) instead build a smooth **sampling density** by convolving the sampling locations with a Gaussian, then set $w(x) = 1/\rho(x)$. ALFT is fairly insensitive to the exact weight, but a good one speeds convergence and improves the result.

### Windowing and wavenumber oversampling

A full high-dimensional ALFT is expensive ($\sim O(N^2 N_p)$ per iteration). Running it in **local spatial windows** cuts the cost, but a small window undersamples the wavenumber domain and introduces Gibbs artifacts. The fix is a **wavenumber-domain oversampling inversion**: solve a small least-squares problem per iteration for the best-fit coefficient, which lets ALFT run in small windows cleanly.

## Anti-alias ALFT

Standard ALFT handles steep dips on *irregular* grids, but for data that are *nearly regular* the aliased copies of an event have the **same amplitude** as the true component. The algorithm can then lock onto an alias and reconstruct the event wrongly (Schonewille et al. 2009).

**Anti-alias ALFT (AA-ALFT)** fixes this by using the *un-aliased low frequencies* to derive spectral weights that guide the selection at *high frequencies*, so the true component is preferred over its aliases. This is the same "low-frequency prior" philosophy used in F–X interpolation (Spitz 1991) and in [Radon interpolation](radon_interpolation.md).

## Extensions

- **Matching-pursuit Fourier interpolation (MPFI)** uses priors to push beyond aliasing. Schonewille et al. (2013) derive the prior from a *separate, more densely sampled dataset* (e.g. dense-over/sparse-under, or time-lapse data) for a significant uplift.
- **5D MPFI** (Tang et al. 2017) applies the full 5D scheme to large-offset dual-coil data feeding SRME.

## Practical parameters

- **Window size** — trades cost against wavenumber resolution.
- **Number of coefficients / iterations** — controls how sparse the model is.
- **Frequency range** — and the low→high frequency weighting for anti-aliasing.
- **QC** — validate by predicting the *input* data: the reconstructed spectrum, sampled back at the irregular input locations, should match what was actually recorded.

## Related concepts

- [Spatial spectral leakage](spatial_spectral_leakage.md)
- [Matching pursuit](matching_pursuit.md)
- [Non-uniform Fourier transform](nonuniform_fourier_transform.md)
- [Seismic data regularization](seismic_data_regularization.md)
- [Radon interpolation](radon_interpolation.md)

## Sources

- Xu, Zhang & Lambaré (2010) — ALFT generalized to higher dimensions: weighting, windowing, wavenumber oversampling.
- Schonewille, Klaedtke & Vigner (2009) — anti-alias ALFT using low-frequency spectral weights.
- Schonewille et al. (2013) — matching-pursuit Fourier interpolation with priors from a second dataset.
