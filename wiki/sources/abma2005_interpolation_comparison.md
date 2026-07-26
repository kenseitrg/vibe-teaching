---
title: "Abma & Kabir (2005) — Comparisons of interpolation methods"
status: draft
type: paper
source_file: wiki/sources/_raw_text/abma2005.txt
language: en
concepts:
  - seismic_data_regularization
tags: [interpolation, comparison, regularization, assumptions, review]
---

# Abma & Kabir (2005) — Comparisons of interpolation methods

The Leading Edge, Acquisition/Processing column. BP, Houston.

## Overview

A practical comparison of seismic interpolation methods, emphasizing that every method rests on assumptions about the character of the data — most commonly that seismic events are **linear**. Because real data are not perfectly linear, the methods differ in where and how they break down.

## Key takeaways

- Data need interpolation whenever the acquired spatial sampling is coarser than a downstream multichannel process requires (from simple stacking to prestack depth migration).
- Interpolation always requires assumptions about the data; the methods compared assume linear events, and the paper shows the consequences when data violate that assumption.
- Provides a practitioner's eye view of the trade-offs among the main interpolation families — useful for choosing a method.

## Relation to lecture notes

The anchor for the unifying "sparsity/simplicity in a transform domain" spine in Term 3 Lecture 06 §2, and for the method-selection guide in §6. Frames *why* different methods (T–X, F–X, F–K, Fourier, Radon) make different assumptions and suit different data.

## Related sources

- [Trad (2009)](trad2009_5d_interpolation.md) — the 5D regularization motivation.
- [Zwartjes & Sacchi (2007)](zwartjes2006_fourier_reconstruction.md) — survey of filter-based interpolation families.
