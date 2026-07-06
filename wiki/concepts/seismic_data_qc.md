---
title: Seismic data quality control (QC)
status: draft
sources:
  - cgg_odt01_data_analysis_part1
  - cgg_odt01_data_analysis_part2
  - brown_2002_surface_consistent_amplitude_correction
  - hill_introduction_to_seismic_processing_ch21
tags: [QC, quality-control, geometry, first-breaks, attribute-maps, LMO, statistics]
---

# Seismic data quality control (QC)

Quality control of input seismic data is the set of checks performed before and during processing to ensure that geometry, timing, amplitudes, and noise are understood and acceptable. Geometry verification is usually the first and most critical step.

## Geometry verification

### Why it is critical
- Every trace must be assigned the correct source, receiver, and midpoint positions.
- Geometry errors cause:
  - mis-stacking in CMP gathers,
  - wrong stacking velocities,
  - artifacts in time and depth sections,
  - incorrect fold and amplitude maps.
- Geometry should be verified before any process that sorts, stacks, or mixes traces.

### Visual geometry QC
- **Overlay expected offset curves**: on a shot or receiver gather, plot the expected arrival time of the direct wave or first breaks using an approximate near-surface velocity. Mis-positioned traces will not fall on the predicted curve.
- **Linear-moveout (LMO) stacks**: apply a linear moveout with a chosen apparent velocity and stack the data. If the chosen velocity matches the direct arrival or refraction, the event aligns horizontally; geometry or timing errors show up as misalignment.
- **Shot/receiver and midpoint maps**: plot source and receiver positions, fold, and midpoint coverage to spot gaps, overlaps, or misplaced points.

### First-break-based QC
- Predict first-break traveltimes from a near-surface model or a direct-wave velocity.
- Pick actual first breaks on the data.
- Compare predicted and observed picks; systematic differences reveal:
  - geometry errors (wrong source/receiver positions),
  - timing problems (start-of-data delays, clock errors),
  - near-surface velocity anomalies (weathering thickness or velocity variations).

## Attribute analysis

### Amplitude attributes
- Mean or RMS amplitude in an analysis window.
- Amplitude in frequency sub-bands.
- Signal-to-microseism ratio.
- RMS is usually preferred over mean amplitude because it is less sensitive to a single extreme sample.

### Correlation attributes
- Dominant frequency.
- Spectral width or bandwidth.
- Signal-to-noise ratio estimated from autocorrelation or cross-correlation.

### Spectral attributes
- Spectral energy.
- Central (mean) frequency.
- Peak frequency.
- Spectral bandwidth.
- These attributes help detect time-varying amplitude and frequency decay, absorption, and source/receiver coupling problems.

## Statistical and map-based QC

- **Histograms**: amplitude, frequency, and noise distributions reveal outliers and non-stationarity.
- **Sorts by source, receiver, offset, CMP**: looking at attributes in different domains can separate acquisition-related patterns from geology.
- **Attribute maps**: plot attributes against source, receiver, or midpoint coordinates. Common patterns include:
  - Vertical stripes: shallow or source-related feature affecting all traces on a cable while the source passes over it.
  - Horizontal stripes: receiver-related feature (stationary surface anomaly).
  - Diagonal stripes: buried feature affecting a moving offset range as the source moves.
- **Fold maps**: identify holes, overlaps, and low-fold areas that may explain noise or amplitude variations.

## Amplitude-specific QC

- Before amplitude correction, check that deterministic spreading correction has been applied consistently.
- Inspect shot/receiver amplitude maps to identify coupling anomalies.
- After surface-consistent amplitude correction, check that source/receiver streaks are reduced while geological trends are preserved.
- Use difference maps to verify what each correction has removed.

## Best practices
- QC after every major processing step, not just at the start.
- Always understand what an attribute represents before deciding whether a value is good or bad.
- Use multiple domains (shot, receiver, CMP, offset) to isolate the cause of an anomaly.
- Keep a processing log of QC decisions and parameter choices.

## Related concepts
- [Amplitude effects](amplitude_effects.md)
- [Spherical divergence](spherical_divergence.md)
- [Automatic gain control](automatic_gain_control.md)
- [Surface-consistent amplitude correction](surface_consistent_amplitude.md)
- [Seismic data sorts](seismic_data_sorts.md)
- [Seismic data formats](seismic_data_formats.md)
- [Static corrections](static_corrections.md)
- [Lecture-ready page: Term 1 Lecture 02 — Amplitude Corrections and QC](../lecture_ready/term01_lec02_amplitude_correction_and_qc.md)
