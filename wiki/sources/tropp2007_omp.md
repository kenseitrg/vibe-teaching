---
title: "Tropp & Gilbert (2007) — Signal recovery from random measurements via orthogonal matching pursuit"
status: draft
type: paper
source_file: wiki/sources/_raw_text/tropp2007.txt
language: en
concepts:
  - matching_pursuit
tags: [sparse-recovery, omp, matching-pursuit, theory, compressed-sensing]
---

# Tropp & Gilbert (2007) — Signal recovery via OMP

IEEE TRANSACTIONS ON INFORMATION THEORY, VOL. 53, NO. 12 (DECEMBER 2007); P. 4655–4666.

## Overview

A theoretical and empirical study showing that **orthogonal matching pursuit (OMP)** reliably recovers a signal with $m$ non-zero entries in dimension $d$ from $O(m\ln d)$ random linear measurements — a major improvement over earlier bounds that required $O(m^2)$ measurements.

## Key takeaways

- OMP is a greedy sparse-recovery algorithm: iteratively select the dictionary atom most correlated with the residual, then re-fit by least squares over all selected atoms (keeping the residual orthogonal to the chosen subspace).
- The new recovery guarantee ($O(m\ln d)$ measurements) is comparable to Basis Pursuit (ℓ1 minimization) results, but OMP is often faster and simpler to implement.
- Provides the theoretical underpinning for using greedy matching pursuit in sparse reconstruction problems such as seismic regularization.

## Relation to lecture notes

The theory reference for Term 3 Lecture 06 §4.3 (matching-pursuit reconstruction) and §5.3 (orthogonal matching pursuit extensions). Explains *why* greedy sparse recovery works and when it can be trusted.

## Related sources

- [Xu et al. (2010)](xu2010_antileakage_fourier_transform.md) — matching pursuit applied with a Fourier dictionary (ALFT).
