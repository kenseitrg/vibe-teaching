---
title: First-Break Picking Algorithms
status: draft
source_type: paper
authors: Juan I. Sabbione, Danilo Velis
year: 2010
url: https://doi.org/10.1190/1.3463703
lectures:
  - term03_lec02
related_concepts:
  - first_break_picking
  - seismic_data_qc
  - static_corrections
tags: [first-breaks, picking, qc, statics, automation]
---

# First-Break Picking Algorithms

Sabbione, J. I., and Velis, D., 2010, "Automatic first-breaks picking: New strategies and algorithms," *Geophysics*, 75, V67–V76.

## Main message

Accurate first-break picks are the foundation of refraction statics and tomostatics. The paper proposes three automatic single-trace pickers and a robust multi-channel mispick-correction stage that uses the whole shot gather.

## Single-trace pickers

All three methods compute a trace attribute in a sliding window and detect the transition from noise to signal plus noise:

- **Modified Coppens’s method (MCM)**: energy ratio of a short leading window to a longer window. Edge-preserving smoothing (EPS) is applied to the energy-ratio attribute, and the pick is placed at the maximum derivative of the smoothed attribute. Works well for impulsive sources (dynamite, marine).
- **Entropy method (EM)**: uses the entropy of the trace as a measure of variability/correlation structure. The entropy rises sharply at the first break; EPS and derivative detection follow the same logic as MCM.
- **Fractal-dimension method (FDM)**: based on the variogram/fractal dimension of the trace. Random noise has a higher fractal dimension than a correlated signal. A small amount of white noise is deliberately added to decorrelate precursor noise (especially useful for vibroseis records). The pick is placed at the minimum derivative of the smoothed fractal-dimension attribute.

## Multichannel mispick correction

A five-step procedure enforces spatial consistency across the shot gather:

1. Trace-by-trace initial picks using one of the three methods.
2. Fit two straight lines per gather flank (direct/refracted arrivals) by least-squares; reject outliers beyond 3σ.
3. Repick within a tolerance window around the preliminary refraction model.
4. Refit the final refraction model using the updated picks.
5. Final picks within a narrower window; traces with no acceptable local extremum are rejected as bad/dead traces.

This shot-consistent correction improves results under correlated noise, bad traces, pulse changes, and indistinct vibroseis first breaks.

## Relation to lecture notes

Supports Term 3 Lecture 2: first-break picking quality is the first link in any refraction/tomo statics workflow; multichannel QC is essential for reliable statics.

## Related concepts

- [First-break picking](../concepts/first_break_picking.md)
- [Seismic data QC](../concepts/seismic_data_qc.md)
- [Static corrections](../concepts/static_corrections.md)
