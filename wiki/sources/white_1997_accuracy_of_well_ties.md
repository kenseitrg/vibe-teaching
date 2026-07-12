---
title: White (1997) — The accuracy of well ties: practical procedures and examples
status: draft
type: paper
source_file: papers/qc/white1997.pdf
language: en
concepts:
  - seismic_well_tie
  - statistical_deconvolution
  - seismic_wavelet
tags: [well-tie, wavelet, accuracy, phase, predictability, NMSE, time-depth, QC]
---

# White (1997) — The accuracy of well ties: practical procedures and examples

White, R. E. (1997). "The accuracy of well ties: practical procedures and examples." *SEG Annual Meeting Expanded Abstracts / Geophysical Prospecting* (pages 816–819 in the local PDF).

## Contribution

Presents practical methods for assessing the accuracy of seismic-to-well ties. Distinguishes between goodness-of-fit (e.g., peak correlation) and true accuracy (e.g., normalized mean square error, NMSE). Gives phase-error tolerances for different applications and shows how to locate the best match point for time-migrated data.

## Key points for teaching

- Well tie accuracy should be measured, not just fitted.
- Phase-error tolerances vary by application: < 30° for simple correlation, < 20° for AVO modelling, < 15° for zero-phasing or relative impedance, < 10° for absolute-impedance inversion.
- Peak correlation can be misleading; the square root of the normalized mean square error is a better accuracy measure.
- For time-migrated data, the best match location is often displaced up-dip from the well because velocity increases with depth.
- Wavelets from different wells in the same survey can be compared and combined using error bars on amplitude and phase spectra.
- The wavelet can be time-variant; methods are given to track time variance.
- The Roy-White frequency-domain matching algorithm (White, 1980; Walden & White, 1984) automates alignment and minimizes truncation effects.

## Relation to lecture notes

- Supports the seismic well tie section of Term 3 Lecture 1.
- Provides the practical accuracy framework and QC metrics for well ties.

## Source

White, R. E. (1997). "The accuracy of well ties: practical procedures and examples." *SEG Annual Meeting Expanded Abstracts / Geophysical Prospecting* (pages 816–819 in the local PDF).

## Related local sources

- [Walden & White (1998) — Seismic wavelet estimation](walden_white_1998_seismic_wavelet_estimation.md)
- [Carvajal et al. (2023) — Well tie tutorial](carvajal_2023_well_tie_tutorial.md)
