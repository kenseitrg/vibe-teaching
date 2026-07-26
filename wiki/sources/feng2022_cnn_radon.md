---
title: "Feng et al. (2022) — De-aliased high-resolution Radon transform based on sparse prior information from a CNN"
status: draft
type: paper
source_file: wiki/sources/_raw_text/gxac041.txt
language: en
concepts:
  - radon_interpolation
tags: [radon, interpolation, deep-learning, anti-alias, sparse-inversion, regularization]
---

# Feng et al. (2022) — CNN-prior de-aliased high-resolution Radon

Journal of Geophysics and Engineering (2022) 19, 663–680. DOI: 10.1093/jge/gxac041. China University of Petroleum-Beijing.

## Overview

Combines a high-resolution Radon transform with a **convolutional neural network (CNN)** that supplies sparse prior information, enabling de-aliased interpolation when high-frequency components are aliased by insufficient sampling.

## Key takeaways

- Radon-transform resolution is crucial for seismic interpolation; high frequencies usually suffer serious aliasing under insufficient sampling.
- Constraining high frequencies with un-aliased low frequencies is an effective resolution-improvement strategy — but obtaining high-resolution **low-frequency** Radon coefficients analytically is hard because the basis functions are strongly correlated.
- The authors use a CNN to extract **sparse prior information** that guides a de-aliased high-resolution Radon inversion, improving the reconstruction of aliased data.
- Represents the modern, data-driven extension of classical high-resolution Radon interpolation (cf. Trad et al. 2002).

## Relation to lecture notes

The modern-extension reference for Term 3 Lecture 06 §5.1 (Radon-domain reconstruction), illustrating the low→high frequency prior idea with a learned (CNN) prior. Cross-links to the anti-alias weighting theme in §4.5.

## Related sources

- [Trad et al. (2002)](trad2002_radon_interpolation.md) — the classical high-resolution time-variant Radon interpolation foundation.
- [Schonewille et al. (2009)](schonewille2009_aa_alft.md) — the analogous low→high prior idea in the Fourier (ALFT) domain.
