---
title: Longbottom, Walden & White (1988) — Principles and application of maximum kurtosis phase estimation
status: draft
type: paper
source_file: papers/qc/longbottom1988.pdf
language: en
concepts:
  - seismic_wavelet
  - statistical_deconvolution
  - deconvolution
tags: [phase-estimation, kurtosis, minimum-entropy-deconvolution, MED, wavelet-phase, deconvolution]
---

# Longbottom, Walden & White (1988) — Principles and application of maximum kurtosis phase estimation

Longbottom, J., Walden, A. T., & White, R. E. (1988). "Principles and application of maximum kurtosis phase estimation." *Geophysical Prospecting*, 36(2), 115–138.

## Contribution

Analyzes Wiggins' minimum entropy deconvolution (MED) and shows that its varimax norm is actually an estimate of kurtosis. Demonstrates that full MED operators are unstable and can severely band-pass filter the data. Proposes a more practical method: correcting the data by the phase rotation that maximizes kurtosis, leaving whitening and noise control to conventional methods.

## Key points for teaching

- Minimum entropy deconvolution (MED) uses the varimax norm, which is essentially a kurtosis measure.
- Full MED operators are unstable and often band-pass filter rather than whiten the data.
- A more robust alternative is to use the kurtosis-maximizing phase rotation only, then apply conventional whitening and noise suppression.
- The signal-dominated bandwidth must exceed a threshold for the method to work; a considerable amount of data is required for stable phase estimation.
- Kurtosis-based phase estimation can outperform norms that are theoretically efficient only under full-band, noise-free assumptions.

## Relation to lecture notes

- Provides background on statistical wavelet phase estimation and deconvolution.
- Related to the seismic wavelet and deconvolution concepts in the course.

## Source

Longbottom, J., Walden, A. T., & White, R. E. (1988). "Principles and application of maximum kurtosis phase estimation." *Geophysical Prospecting*, 36(2), 115–138.

## Related local sources

- [Walden & White (1998) — Seismic wavelet estimation](walden_white_1998_seismic_wavelet_estimation.md)
- [White (1997) — The accuracy of well ties](white_1997_accuracy_of_well_ties.md)
