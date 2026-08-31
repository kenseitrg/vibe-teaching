---
title: OVT / COV panels
status: draft
sources:
  - vermeer_2012_3d_seismic_survey_design
  - cgg_odt01_data_analysis_part2
  - hill_ruger_2020_illustrated_seismic_processing_preimaging
tags: [3D, OVT, COV, offset-vector, gather, sort, azimuth, migration, AVO, pseudo-COV, spatial-continuity]
---

# OVT / COV panels

An **OVT (offset-vector tile)** or **COV (common-offset-vector)** panel is a group of traces with similar inline and crossline offset components. OVT panels are pseudo-COV gathers constructed from real 3D geometries; they are one of the most important sort orders for modern 3D processing and imaging.

## The ideal COV gather

In the ideal parallel geometry, a **common-offset-vector (COV) gather** contains all traces with the same offset vector $(h_x, h_y)$ and varying midpoint $(x_m, y_m)$. It is a singlefold data set that extends across the whole survey area. In practice, ideal COV gathers are almost never acquired, so we construct **pseudo-COV gathers** from available data.

## Construction from cross-spreads

For a regular orthogonal geometry, the cross-spread can be divided into **unit-cell-sized** subareas. Each subarea is an **offset-vector tile (OVT)** and is characterized by a limited range of offset vectors. OVTs are extracted from many cross-spreads and combined to form singlefold OVT panels that cover the survey area.

For each trace, the inline and crossline half-offsets are

$$
h_x = \frac{x_r - x_s}{2}, \qquad h_y = \frac{y_r - y_s}{2}
$$

where $(x_s, y_s)$ and $(x_r, y_r)$ are the source and receiver coordinates. Then:

1. Assign each trace to a midpoint bin.
2. Assign each trace to an offset-vector bin in $(h_x, h_y)$ space. The bin size is typically one unit cell.
3. Collect all traces with the same offset-vector bin into one panel.

Each panel is approximately a singlefold 3D volume with a narrow range of offsets and azimuths.

## OVT parameters

An OVT can be described by four parameters (Vermeer, 2012, §2.5.2):

- $h_x$ and $h_y$: the half-offset coordinates of the center of the tile.
- $\Delta h_x$ and $\Delta h_y$: the range of half-offsets inside the tile.

In a symmetric, center-spread cross-spread, each OVT has counterparts in the other three quadrants. OVTs in opposite quadrants have the same absolute offsets and similar shot-receiver azimuths (modulo 180°); these pairs are called **reciprocal OVTs**.

## Why OVT/COV panels matter

- **Azimuth and offset preservation.** They preserve offset and azimuth information, which is needed for AVO and AVAz analysis.
- **Singlefold imaging volumes.** They provide singlefold volumes for 3D migration without mixing offsets and azimuths.
- **Regularization and interpolation.** They are used for 3D regularization and interpolation algorithms.
- **QC.** They make offset and azimuth distribution easy to QC (spiderweb or trace-vector diagrams).
- **Reduced spatial discontinuity.** Compared with tiling whole cross-spreads, OVT tiling spreads spatial discontinuities more thinly across the survey area.

## Reciprocal OVTs

Reciprocal OVTs are pairs of tiles in opposite quadrants of the cross-spread that have the same range of absolute offsets and the same range of shot-receiver azimuths (modulo 180°). Because of source-receiver reciprocity, they contain equivalent information. Combining reciprocal OVTs into twofold gathers reduces edge effects and improves spatial continuity.

## Coverage and fold

The number of different OVT panels equals the fold of coverage in the fullfold area. In a 64-fold geometry, 64 different OVT panels can be extracted. Short-offset panels are larger than long-offset panels because short offsets are acquired across the whole survey area, whereas long offsets only appear near the fullfold area.

When merging two 3D surveys with the same geometry parameters, the merge can be seamless only if the fullfold areas are adjacent (gapless), so that all OVT panels are continuous from one survey into the other.

## Related concepts

- [3D seismic acquisition](3d_seismic_acquisition.md)
- [Cross-spread gather](cross_spread_gather.md)
- [Seismic data sorts](seismic_data_sorts.md)
- [Common midpoint (CMP) and fold](common_midpoint.md)
- [Grid binning](grid_binning.md)
- [AVO analysis](avo_analysis.md)
