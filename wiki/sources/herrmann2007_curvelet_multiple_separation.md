---
title: "Herrmann, Böninger & Verschuur (2007) — Non-linear Primary-Multiple Separation with Directional Curvelet Frames"
status: draft
type: paper
source_file: papers/noise_attenuation/curvelets/herrmann2007.txt
language: en
concepts:
  - seismic_data_processing
  - adaptive_subtraction
  - wiener_filter
tags: [noise-attenuation, curvelet, multiple-attenuation, primary-multiple-separation, sparsity, l1-norm]
---

# Herrmann, Böninger & Verschuur (2007) — Non-linear Primary-Multiple Separation with Directional Curvelet Frames

*Geophysical Journal International*, 170, 781--799.

## Overview

This paper proposes a transformed-domain method for separating primaries from multiples that exploits differences in the multiscale and multidirectional characteristics of these signal components in the curvelet domain. Unlike conventional adaptive subtraction (matched filtering), the method seeks a sparse representation of both components using weighted l1-norm optimization, formulated as a Bayesian estimation problem. The algorithm does not compute a matched filter; instead, it recovers primaries and multiples simultaneously from imperfect predictions via an iterative block-relaxation method with cooling.

## Key takeaways

- The signal model is y = s1 + s2 + n (primaries + multiples + noise), with a prediction s2_hat for the multiples.
- Primary-multiple separation is cast as: minimize ||x||_{w,1} subject to ||y - A*x||_2 <= epsilon, where A = [A1, A2] is the augmented synthesis matrix (one transform per component).
- Weights w1 = max(sigma*sqrt(2*log N), C1*|x2_hat|) and w2 = max(sigma*sqrt(2*log N), C2*|x1_hat|) drive the components apart: where predicted multiples are large, primary coefficients are suppressed and vice versa.
- The curvelet transform achieves the best sparsity for both primaries and multiples among compared transforms (Dirac, Fourier, wavelet, curvelet), with cross-correlation R = 0.004 (vs. 0.97 for Dirac).
- The cooling method starts with a large Lagrange multiplier (emphasizing the sparsity prior) and gradually relaxes it; a stopping criterion based on cross-correlation between residues prevents overfitting.
- Synthetic and field data examples show cleaner separation compared to conventional adaptive matched filtering, with improved stack quality.

## Relation to lecture notes

This paper generalizes the curvelet shrinkage framework from Hennenfent & Herrmann (2006) to the two-component separation problem, relevant to Term 3 Lecture 04 -- Noise Attenuation. It provides the theoretical foundation for non-adaptive subtraction in the curvelet domain and connects sparsity-promoting optimization (basis-pursuit denoising) to practical multiple attenuation.

## Related sources

- [Hennenfent & Herrmann (2006)](hennenfent2006_curvelet_intro.md) -- Foundational curvelet denoising with NFDCT
- [Kustowski et al. (2013)](kustowski2013_curvelet_model_guided.md) -- Guided curvelet noise attenuation
- [Treitel (1974)](treitel1974_complex_wiener.md) -- Complex Wiener filter theory underlying f-x prediction
