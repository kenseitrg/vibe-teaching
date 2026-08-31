---
title: Automatic gain control (AGC) and deterministic amplitude equalization
status: draft
sources:
  - yilmaz_practical_seismic_data_analysis_amplitude
  - hill_introduction_to_seismic_processing_ch21
  - cgg_odt01_data_analysis_part1
tags: [AGC, automatic-gain-control, amplitude-normalization, statistical-gain, amplitude-equalization, visualization]
---

# Automatic gain control (AGC) and deterministic amplitude equalization

Amplitude equalization methods make seismic data visible and processable, but they do not necessarily preserve the physical amplitudes needed for AVO or quantitative interpretation. They are best treated as **intermediate visualization and processing aids**.

## Amplitude normalization

- Each trace is scaled by a single constant derived from its own amplitude statistics.
- Common scalars:
  - Maximum absolute amplitude: trace max is set to a fixed value.
  - Mean absolute amplitude: average absolute value is set to a fixed value.
  - RMS amplitude: $A_{\text{rms}} = \sqrt{\frac{1}{N}\sum_n a_n^2}$ is set to a fixed value.
- After normalization, the relative amplitudes **within** a trace are preserved, but the relative amplitudes **between** traces are deliberately changed.
- Main use case: display and qualitative comparison.

## Automatic gain control (AGC)

- A time-varying gain function is applied trace by trace so that the local amplitude level is balanced within a sliding window.
- Typical implementation:
  1. Define a time window (gate) of length $W$.
  2. Compute a statistic in the window, e.g., sum of absolute amplitudes or RMS amplitude.
  3. Take the reciprocal of the statistic and assign it as the gain at the center of the window.
  4. Interpolate between window centers to get a smooth gain function.
  5. Multiply the trace by the gain function.
  6. Slide the window and repeat.

### Effect of window length
- **Short window**: strong homogenization; reflections and noise are forced to the same amplitude level.
- **Long window**: weaker homogenization; more of the original amplitude variation is retained.

### AGC use cases in processing
- **Visualization**: making weak deep reflections visible on screen or in plots.
- **Structural analysis**: helping an interpreter see reflector continuity and terminations.
- **Kinematic processing**: aiding steps such as velocity picking and residual-statics estimation, where the goal is to identify event times rather than preserve amplitudes.

### Risks and artifacts
- **True amplitude destruction**: AGC removes the relative amplitude relationships that AVO, AVAz, and reservoir characterization require. Do not use AGC before amplitude-sensitive work.
- **Noise boost**: AGC cannot distinguish signal from noise; low-amplitude noise windows receive large gains.
- **Shadow-zone effect**: a very strong amplitude (e.g., salt edge, water bottom) lowers the gain in adjacent windows, making neighboring events appear weak.
- **Misleading amplitudes**: AGC can create artificial brightening or dimming that looks like geology.
- **Non-reversibility**: the applied gain is usually discarded, so the correction cannot be undone later.

## Deterministic vs. statistical equalization

| Feature | Deterministic (e.g., spherical divergence) | Statistical (e.g., AGC) |
|---|---|---|
| Basis | Physical model of amplitude decay | Data’s own amplitude statistics |
| Reversibility | Usually reversible | Not reversible |
| Preserves amplitude contrast | Yes | No (intentionally homogenizes) |
| Adapts to local anomalies | No | Yes |
| Use case | First-order amplitude correction | Visualization, kinematic processing |

## Related concepts
- [Amplitude effects](amplitude_effects.md)
- [Spherical divergence](spherical_divergence.md)
- [Surface-consistent amplitude correction](surface_consistent_amplitude.md)
- [Seismic data QC](seismic_data_qc.md)
- [Lecture-ready page: Term 1 Lecture 02 — Amplitude Corrections and QC](../lecture_ready/term01_lec02_amplitude_correction_and_qc.md)
