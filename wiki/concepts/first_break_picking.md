---
title: First-break picking
status: draft
sources:
  - fbpicking
  - law_trad_comparison_of_refraction_inversion_methods
  - hill_introduction_to_seismic_processing_ch22
tags: [first-breaks, statics, qc, refraction]
---

# First-break picking

First-break picking is the process of identifying the onset time of the first coherent seismic arrival on each trace. For land data, these arrivals are usually direct waves or head waves from the base of the weathering layer; they are the input to refraction statics and diving-wave tomography.

## Why it matters

- The quality of first-break picks limits the accuracy of refraction-based statics.
- Errors propagate into the near-surface velocity model and therefore into datum/static corrections.
- Manual picking is subjective and time-consuming; automatic picking is essential for large surveys.

## Single-trace methods

Common attributes computed in a sliding window along the trace:

- **Energy ratio / STA-LTA**: short-term average over long-term average; detects abrupt amplitude increase.
- **Entropy**: measures the statistical disorder of the trace; rises when the signal arrives.
- **Fractal dimension / variogram**: quantifies the roughness of the trace; correlated signal has lower dimension than random noise.
- **Amplitude threshold**: simple amplitude-level trigger, often used as a first guess.

## Multichannel quality control

Because first-breaks follow approximately linear moveout across a shot gather, whole-gather constraints can correct mispicks:

1. Make an initial trace-by-trace pick.
2. Fit a refraction line to the picks and reject statistical outliers.
3. Repick inside a tolerance window around the line.
4. Refit and final-pick with a narrower window.
5. Reject traces that still cannot be matched as bad/dead traces.

## Practical challenges

- Vibroseis records may have side-lobes before the true first break.
- Correlated noise and low signal-to-noise ratio can delay the pick.
- Near-surface irregularities and statics change the moveout from shot to shot.
