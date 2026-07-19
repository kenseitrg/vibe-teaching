---
title: CADZOW SFM Best Practice — Rank-Reduction Noise Suppression
status: draft
source_type: best practice guide
authors: "Schlumberger"
year: 2017
source_file: papers/noise_attenuation/CADZOW_SFM_Best_Practice_v2.pdf
lectures:
  - term03_lec04
related_concepts:
  - seismic_noise
  - frequency_filtering
  - spectral_analysis
tags: [noise-attenuation, random-noise, rank-reduction, svd, cadzow, f-x-domain]
---

# CADZOW SFM Best Practice — Rank-Reduction Noise Suppression

Schlumberger (2017). *CADZOW SFM Best Practice — Cadzow filtering*. Schlumberger Private – Customer Use.

## Main message

The Cadzow SFM suppresses random noise by exploiting the low-rank structure of the data in the f-x domain. For each frequency slice, a Hankel matrix is formed from the spatial data, decomposed by SVD, and reconstructed using only the largest singular values. The result is a rank-reduced approximation that preserves coherent signal while removing incoherent noise. The method works on any regularly sampled gather type (shot, receiver, CMP, cross-spread, post-stack cube) in 2D or 3D mode.

## Key points

1. **Algorithm:** Transform gather from (x,t) to (x,f). For each frequency slice: form Hankel matrix → SVD → keep N largest singular values → reconstruct filtered frequency slice → inverse transform to (x,t).
2. **Key parameter — Percentage of Singular Values to Keep:** This controls the rank of the reconstructed data. Lower values suppress more noise but risk signal damage. Start at 75% and reduce iteratively.
3. **Window dimensions:** Temporal window (default 600 ms, 30% overlap) and spatial windows on Axis A (and Axis B in 3D mode) with overlap. Larger windows improve stability but increase run time exponentially.
4. **Automatic rank determination:** Two options — Trickett's (2015) variance-estimate method and the Pre-First-Break Window Analysis method, which estimates the noise floor from a pre-signal window and uses it to threshold singular values.
5. **Assumptions:** Input data must be on a regular grid with one trace per location. Anomalous amplitudes should be removed first (e.g., AAA/SWELL). Coherent noise should be removed before applying Cadzow to avoid it being treated as signal.
6. **3D mode:** Processes cross-spread gathers with Axis A = source line direction, Axis B = receiver line direction. Events planar in x-y are better preserved than in sequential 2D passes.
7. **Output types:** 'SIGNAL' (input minus band-limited noise model) or 'NOISE' (the band-limited noise model itself). QC is always recommended at stack level.

## Relation to lecture notes

Cadzow filtering is a core random-noise attenuation technique discussed in Term 3 Lecture 04. The rank-reduction concept in f-x directly illustrates how signal predictability across traces (linear events are perfectly predicted in f-x) enables noise/signal separation.

## Related concepts

- [Seismic noise](../concepts/seismic_noise.md)
- [Frequency filtering](../concepts/frequency_filtering.md)
- [Spectral analysis](../concepts/spectral_analysis.md)

## Related sources

- [NUCNS Technical Documentation](nucns.md)
