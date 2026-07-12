---
title: Cross-spread gather
status: draft
sources:
  - vermeer_2012_3d_seismic_survey_design
  - cgg_odt01_data_analysis_part2
  - hill_ruger_2020_illustrated_seismic_processing_preimaging
tags: [3D, gather, cross-spread, sort, source-line, receiver-line, minimal-data-set, orthogonal-geometry, spatial-continuity]
---

# Cross-spread gather

A **cross-spread gather** is the set of all traces recorded from one source line into one receiver line. It is the natural basic subset of **orthogonal geometry** and a key building block of 3D land seismic processing.

## Definition

For an orthogonal land geometry, a cross-spread contains every source station on a chosen source line and every receiver station on a chosen receiver line. The source line and receiver line are perpendicular; their intersection is the center of the cross-spread. The traces form a 2D grid in source-receiver space, and every midpoint in the cross-spread corresponds to a unique shot-receiver pair.

## Properties

- **Midpoint area.** The midpoint area of a cross-spread is centered on the midpoint of the source and receiver lines and extends over the same region as the midpoint area of the corresponding template.
- **Offset and azimuth.** At any midpoint $M$ in a cross-spread, the offset vector links a point on the source line to a point on the receiver line. Because source and receiver lines are perpendicular, the distance of a midpoint from the center equals the corresponding half-offset. As a consequence, traces with the same absolute offset lie on a circle centered on the cross-spread origin.
- **Common-azimuth gathers.** Traces with the same shot-receiver azimuth lie on straight lines through the origin of the cross-spread.
- **Time-slice behavior.** In horizontal geology, reflection events on a time slice through an uncorrected cross-spread appear as circles (because traveltime depends only on absolute offset). With dipping geology, the circles become elliptical.

## Extraction from orthogonal geometry

Cross-spreads can be extracted from an orthogonal 3D survey by collecting all traces that share a source line and a receiver line. The number of cross-spreads equals the number of intersections between source lines and receiver lines.

The maximum inline offset of a cross-spread equals the receiver spread length divided by two, and the maximum crossline offset equals the source spread length divided by two. The **aspect ratio** of the cross-spread (maximum crossline offset / maximum inline offset) is the same as the aspect ratio of the acquisition template.

## Cross-spread vs template

The template is the repeating unit acquired in the field. Its midpoint area consists of small strips, each corresponding to a shot salvo into one receiver line. The cross-spread has the same midpoint area but is spatially continuous: there are no internal jumps between receiver lines. This makes the cross-spread preferable for many processing steps.

In brick-wall geometry (staggered source lines), the cross-spread is split into strips and spatial continuity is degraded.

## Why cross-spreads are useful

- They are a **minimal data set (MDS)**: a singlefold, continuous subset of the 5D prestack wavefield that can be used for imaging.
- They provide natural domains for 3D statics, residual statics, and surface-consistent processing.
- They are used for 3D interpolation, regularization, and noise attenuation.
- They make source/receiver coupling and geometry QC visible in two spatial dimensions.
- They are the source from which **OVT/COV panels** are constructed.

## Limitations

The cross-spread has limited spatial extent because useful offset increases toward the edges. Beyond the maximum useful offset, the subset is not usable. The edges of the cross-spread create spatial discontinuities in the survey, which can cause migration artifacts. Wide geometries (cross-spread aspect ratio near one) reduce the number of edges per unit area and therefore improve spatial continuity.

## Relationship to other 3D sorts

- **Shot gather:** all receivers for one source point (a small part of a cross-spread).
- **Receiver gather:** all sources for one receiver point (a small part of a cross-spread).
- **Cross-spread:** all sources on one line into all receivers on one perpendicular line.
- **OVT / COV panel:** all traces with a similar offset vector, extracted from many cross-spreads.
- **3D midpoint gather:** all traces with the same midpoint (fixed $x_m$, $y_m$, varying offset vector).

## Related concepts

- [3D seismic acquisition](3d_seismic_acquisition.md)
- [OVT / COV panels](ovt_cov_panels.md)
- [Seismic data sorts](seismic_data_sorts.md)
- [Common midpoint (CMP) and fold](common_midpoint.md)
- [Seismic data QC](seismic_data_qc.md)
- [Grid binning](grid_binning.md)
