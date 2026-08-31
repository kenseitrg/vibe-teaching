---
title: "Schonewille, Klaedtke & Vigner (2009) — Anti-alias anti-leakage Fourier transform"
status: draft
type: paper
source_file: wiki/sources/_raw_text/schonewille2009.txt
language: en
concepts:
  - anti_leakage_fourier_transform
  - spatial_spectral_leakage
tags: [regularization, alft, anti-alias, fourier, priors]
---

# Schonewille, Klaedtke & Vigner (2009) — Anti-alias ALFT

SEG Houston 2009 International Exposition and Annual Meeting, Expanded Abstracts, 3249–. PGS.

## Overview

Identifies a weakness of the standard ALFT — it can lock onto **aliased** Fourier components when the data are nearly regular — and proposes **anti-alias ALFT (AA-ALFT)**, which uses un-aliased low frequencies to weight the selection at high frequencies.

## Key takeaways

- **ALFT review** (iterative spectrum estimation): (1) DFT of input; (2) select strongest Fourier component; (3) add to estimated spectrum; (4) inverse DFT of that component to the original grid; (5) subtract from input → next iteration. The same component can be re-selected later because of leakage.
- **Spectral leakage picture:** a sampled signal = continuous signal × pulse train; in the Fourier domain this is convolution with the pulse train's spectrum. Irregular sampling gives that spectrum non-zero sidelobes, so energy "leaks" between frequencies. A plain forward DFT is therefore not optimal — a least-squares estimate (e.g. Duijndam et al. 1999) is better when data are band-limited and well sampled.
- **Aliasing problem for near-regular data:** for regularly (or nearly regularly) sampled data, an event's aliased Fourier components have the **same amplitude** as the true component, so ALFT may select an alias and mis-reconstruct the event.
- **AA-ALFT fix:** use the **un-aliased lower frequencies** to provide spectral weights for the higher frequencies, biasing the selection toward the true (non-aliased) component. Significant improvement shown on 2D synthetic and 3D field data with steep dips.
- Contextualizes ALFT among alternatives: high-resolution transforms (Sacchi & Ulrych 1996; Zwartjes & Sacchi 2007), MWNI (Liu & Sacchi 2004), POCS (Abma & Kabir 2006).

## Relation to lecture notes

The anchor for Term 3 Lecture 06 §4.5 (anti-alias weighting for interpolation beyond aliasing). The low→high frequency prior idea recurs in Spitz F–X interpolation and in Radon interpolation (Feng et al. 2022).

## Related sources

- [Xu et al. (2010)](xu2010_antileakage_fourier_transform.md) — base ALFT algorithm and higher-dimensional generalization.
- [Schonewille et al. (2013)](schonewille2013_mpfi_priors.md) — priors from a second dataset (MPFI).
