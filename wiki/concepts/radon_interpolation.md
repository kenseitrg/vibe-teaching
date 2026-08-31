---
title: Radon interpolation
status: draft
sources:
  - trad2002_radon_interpolation
  - feng2022_cnn_radon
  - zwartjes2006_fourier_reconstruction
tags: [regularization, interpolation, radon, tau-p, sparse-recovery]
---

# Radon interpolation

Radon interpolation reconstructs missing or irregularly sampled traces by exploiting the fact that reflections in a CMP gather are **sparse in the Radon (τ–p) domain**. It is the "replace Fourier with Radon" branch of [regularization](seismic_data_regularization.md): the same sparse-reconstruction philosophy as the [ALFT](anti_leakage_fourier_transform.md), but using Radon basis functions instead of Fourier ones.

## Why Radon

In a CMP gather, primary reflections follow hyperbolic (or, after NMO, nearly parabolic) moveout curves. A [Radon transform](radon_transform.md) maps each such curve to a **compact, focused peak** in the τ–p domain, while gaps, noise, and sampling artifacts spread out. The model is therefore sparse: a few Radon coefficients capture the primaries. Filling gaps then amounts to estimating a sparse Radon model and transforming it back.

The quality depends on how well the events match the basis functions, so a **true hyperbolic** Radon transform generally outperforms the parabolic one for large moveout (large offsets, common in marine data). The parabolic transform on NMO-corrected gathers is the cheaper alternative.

## High-resolution time-variant Radon (Trad, Ulrych & Sacchi 2002)

A high-resolution Radon transform sharpens the τ–p model so interpolation is accurate. Key implementation points:

- **Sparse inversion.** Solve for a Radon model with a sparseness constraint (Thorson & Claerbout 1985), using weighted conjugate-gradient / LSQR iteration.
- **Time-variant kernel.** The hyperbolic transform's kernel varies with time, so fast solvers like Levinson recursion cannot be used; iterative solvers are required, and each can be stopped early to limit cost.
- **Irregular velocity model space.** Define the model on an *irregularly sampled velocity space* — a central trace carrying a velocity trend from semblance, plus neighbouring perturbation traces (variable spacing works best). This minimizes the number of unknowns and keeps the problem tractable with sparse matrices.
- **Aliasing relaxation.** An irregularly sampled Radon space relaxes the minimum-sampling condition needed to avoid aliasing (Trad & Ulrych 1999) — a useful property for sparse acquisition.

The hyperbolic RT gives accurate interpolation in CMP gathers; an elliptical RT attenuates sampling artifacts in slant-stack sections.

## De-aliased Radon with learned priors (Feng et al. 2022)

High-frequency components are usually aliased under insufficient sampling. A standard fix constrains high frequencies with the un-aliased low frequencies — but obtaining high-resolution low-frequency Radon coefficients analytically is hard because the basis functions are strongly correlated. Feng et al. (2022) use a **convolutional neural network** to extract sparse prior information that guides a de-aliased high-resolution Radon inversion. This is the same low→high frequency prior idea as [AA-ALFT](anti_leakage_fourier_transform.md#anti-alias-alft), with the prior learned from data.

## Strengths and limits

- **Local operators.** Radon-based interpolation can be defined locally without the explicit windowing that Fourier methods need (Naghizadeh & Sacchi 2009).
- **Assumes hyperbolic/parabolic moveout** — best for primaries in CMP gathers; less natural for arbitrary 3D/5D azimuthal regularization, where Fourier (ALFT/MPFI) methods dominate.

## Related concepts

- [Radon transform](radon_transform.md)
- [Seismic data regularization](seismic_data_regularization.md)
- [Anti-leakage Fourier transform](anti_leakage_fourier_transform.md)
- [Matching pursuit](matching_pursuit.md)
- [Normal moveout](normal_moveout.md)

## Sources

- Trad, Ulrych & Sacchi (2002) — accurate interpolation with high-resolution time-variant hyperbolic/elliptical Radon transforms.
- Feng et al. (2022) — de-aliased high-resolution Radon transform using CNN-derived sparse priors.
- Zwartjes & Sacchi (2007) — context: sparse reconstruction and the local-operator contrast with Fourier methods.
