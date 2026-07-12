---
title: Walden & White (1998) — Seismic wavelet estimation: a frequency domain solution to a geophysical noisy input-output problem
status: draft
type: paper
source_file: papers/qc/walden1998.pdf
language: en
concepts:
  - seismic_well_tie
  - seismic_wavelet
  - statistical_deconvolution
tags: [wavelet, well-tie, frequency-domain, coherence, noisy-input-output, SNR, spectral-estimation]
---

# Walden & White (1998) — Seismic wavelet estimation: a frequency domain solution to a geophysical noisy input-output problem

Walden, A. T., & White, R. E. (1998). "Seismic wavelet estimation: a frequency domain solution to a geophysical noisy input-output problem." *IEEE Transactions on Geoscience and Remote Sensing*, 36(1), 287–297.

## Contribution

Formulates seismic wavelet estimation as a noisy input-output problem in the frequency domain. Uses multiple coherence analysis to estimate the output signal-to-noise ratio at each frequency and then estimates the frequency response function (wavelet spectrum) from the ordinary coherence, input spectrum, and input-output cross-spectrum.

## Key points for teaching

- The observed seismic trace is a noisy output of a linear system driven by the (also noisy) log-derived reflectivity.
- Standard least-squares wavelet estimation is biased when the input reflectivity is noisy.
- Multiple coherence analysis estimates the output SNR at each frequency by exploiting repeated measurements (e.g., multiple traces around the well).
- Combining the output SNR with ordinary coherence and the input-output cross-spectrum gives an unbiased estimate of the wavelet's frequency response.
- The method works well on real and synthetic data and produces error bars on the wavelet spectrum.
- Error bars are essential for deciding whether wavelets from different wells or time windows differ significantly.

## Relation to lecture notes

- Supports the seismic well tie section of Term 3 Lecture 1.
- Provides the theoretical basis for the Roy-White statistical wavelet estimation method.

## Source

Walden, A. T., & White, R. E. (1998). "Seismic wavelet estimation: a frequency domain solution to a geophysical noisy input-output problem." *IEEE Transactions on Geoscience and Remote Sensing*, 36(1), 287–297.

## Related local sources

- [White (1997) — The accuracy of well ties](white_1997_accuracy_of_well_ties.md)
- [Carvajal et al. (2023) — Well tie tutorial](carvajal_2023_well_tie_tutorial.md)
- [Longbottom et al. (1988) — Maximum kurtosis phase estimation](longbottom_1988_maximum_kurtosis_phase_estimation.md)
