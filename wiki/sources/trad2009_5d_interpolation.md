---
title: "Trad (2009) — Five-dimensional interpolation: Recovering from acquisition constraints"
status: draft
type: paper
source_file: wiki/sources/_raw_text/trad2009.txt
language: en
concepts:
  - seismic_data_regularization
tags: [regularization, 5d, interpolation, ovt, avo, acquisition]
---

# Trad (2009) — Five-dimensional interpolation

GEOPHYSICS, VOL. 74, NO. 6 (NOVEMBER-DECEMBER 2009); P. V123–V132. DOI: 10.1190/1.3245216.

## Overview

Makes the case for **5D interpolation** (inline, crossline, offset, azimuth, time) as the way to recover from acquisition constraints in wide-azimuth surveys. Argues that lower-dimensional methods cannot simultaneously preserve offset and azimuth information needed for modern imaging and amplitude analysis.

## Key takeaways

- Coarse/irregular sampling degrades interference-sensitive processes and biases amplitude-versus-offset/azimuth (AVO/AVAz) analysis that we want to observe in the migrated domain.
- The only perfect fix is well-sampled acquisition; all processing remedies treat symptoms, with no guarantee of success — but we usually cannot re-acquire.
- 5D interpolation uses all spatial axes at once, giving the most information for filling gaps and preserving both offset and azimuth, unlike cascaded 3D/4D approaches that mix azimuths.
- Provides the dimensionality rationale (3D → 4D → 5D) that motivates high-dimensional regularization.

## Relation to lecture notes

The anchor for Term 3 Lecture 06 §1 (why regularize; what "regular" means) and §4.1 (the 3D→4D→5D dimensionality ladder). Defines the modern target: a regular grid in the migration domain that preserves offset and azimuth.

## Related sources

- [Xu et al. (2010)](xu2010_antileakage_fourier_transform.md) — high-dimensional ALFT implementation.
- [Abma & Kabir (2005)](abma2005_interpolation_comparison.md) — comparison of interpolation methods.
- [Tang et al. (2017)](tang2017_5d_mpfi_srme.md) — 5D MPFI applied to SRME.
