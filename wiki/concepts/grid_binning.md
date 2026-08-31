---
title: Grid binning
status: draft
sources:
  - vermeer_2012_3d_seismic_survey_design
  - cgg_odt01_data_analysis_part2
  - seg_sps_format_rev21
tags: [3D, binning, CMP, fold, midpoint, spatial-sampling, geometry, QC, natural-bin, offset-distribution]
---

# Grid binning

Grid binning is the step that assigns each trace midpoint to a regular (inline, crossline) CMP bin. It is the bridge between the continuous acquisition geometry and the discrete cells used for stacking, velocity analysis, and imaging.

## Why binning is needed

Midpoints computed from source and receiver coordinates are scattered. To form a processable volume, traces are grouped into regular bins. The bin becomes the basic lateral sample of the stacked image and the organizing unit for fold, velocity analysis, and AVO.

## Natural bin size

For a regular orthogonal geometry, the **natural bin size** is set by the source and receiver station intervals (Vermeer, 2012, §2.4.1):

- Inline bin size = receiver-station interval / 2
- Crossline bin size = source-station interval / 2

This convention comes from the fact that moving a source or receiver by one station interval shifts the midpoint by half that interval. In parallel marine geometry, the crossline bin size equals the midpoint-line interval.

In a perfectly regular geometry, one trace lands at the center of each bin. In practice, source and receiver positions are not always perfectly regular, so midpoints may be spread within bins.

## Bin size trade-off

The bin size is a design choice:

- **Smaller bins:** better lateral resolution, but lower fold and more empty bins.
- **Larger bins:** higher fold and more uniform statistics, but worse resolution and more mixing of dips and azimuths.

The bin size is usually chosen based on the target depth, the desired lateral resolution, and the available fold.

## Offset distribution in a bin

The offset distribution inside a bin depends on the position of the bin within the unit cell. In a cross-spread, the offset vector of a trace points from the source line to the receiver line. Because of the periodicity of the geometry, each unit cell contains as many different offset distributions as there are bins in the cell. The corner bins of the unit cell have the smallest minimum offsets, while the center bins have the largest minimum offsets (LMOS).

For even inline and crossline folds, the shortest and longest offsets occur in the same bins; for odd folds, they are shifted. The absolute-offset distribution is symmetric across the four quadrants of the unit cell.

## Midpoint smear and modern processing

Historically, it was important to keep midpoints close to bin centers to avoid **midpoint smear** during stack. With modern prestack processing (DMO, prestack migration, and regularization), the data are re-sampled and re-positioned anyway, so the exact midpoint-to-bin-center distance is less critical than it once was. However, large deviations can still bias fold, offset, and azimuth statistics.

## Binning QC

- **Fold uniformity:** the fold map should be smooth, with no unexpected holes or spikes.
- **Midpoint deviation:** the distance from each trace midpoint to the center of its bin should be small. Large deviations mean the bin is not representative of the trace positions.
- **Offset and azimuth distribution:** each bin should contain a representative range of offsets and azimuths for stacking and AVO.
- **Acquisition footprint:** periodic variations in fold or offset distribution can indicate an acquisition footprint related to the unit cell.

## From binning to processing

After binning, the data are usually organized as:

- CMP gathers for stacking and velocity analysis,
- OVT/COV panels for prestack imaging and AVO,
- cross-spread gathers for 3D interpolation and noise attenuation.

## Related concepts

- [3D seismic acquisition](3d_seismic_acquisition.md)
- [Common midpoint (CMP) and fold](common_midpoint.md)
- [OVT / COV panels](ovt_cov_panels.md)
- [Cross-spread gather](cross_spread_gather.md)
- [Seismic data sorts](seismic_data_sorts.md)
- [Seismic data QC](seismic_data_qc.md)
- [Seismic data formats](seismic_data_formats.md)
