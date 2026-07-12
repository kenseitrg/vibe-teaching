---
title: Seismic processing quality control (QC)
status: draft
sources:
  - cgg_odt01_data_analysis_part1
  - cgg_odt01_data_analysis_part2
  - hill_ruger_2020_illustrated_seismic_processing_preimaging
  - vermeer_2012_3d_seismic_survey_design
tags: [QC, quality-control, processing, kinematics, noise, deconvolution, demultiple, well-tie, AVO, multi-attribute]
---

# Seismic processing quality control (QC)

Processing-stage quality control is the set of checks applied after each major processing step to verify that the step has improved the data without introducing unwanted side effects. It is distinct from input-data QC, which checks the raw records and geometry before processing begins.

## Why processing QC is needed

A processing step can fail in two ways:

- **Insufficient correction:** the target problem remains (e.g., residual multiples after demultiple, residual NMO after velocity analysis).
- **Over-correction:** the step removes wanted signal or creates artifacts (e.g., signal leakage into a noise panel, an unstable high-frequency boost from deconvolution).

The best defense is to check the output in several independent ways: sections, maps, gathers, spectra, and quantitative metrics.

## Input-data QC recap

Before processing, the data must be checked for geometry, timing, and amplitude integrity. Key tools include:

- **Offset-curve overlays:** expected direct-wave or first-break arrival times plotted on shot gathers.
- **LMO stacks:** stacks with a linear moveout to align direct arrivals and refractions.
- **First-break residuals:** comparison of predicted and picked first-break times.
- **Amplitude attributes:** RMS amplitude, amplitude in frequency bands, signal-to-microseism ratio.
- **Spectral/correlation attributes:** dominant frequency, bandwidth, central frequency, signal-to-noise ratio.
- **Attribute maps:** maps by source, receiver, offset, CMP, and midpoint to spot acquisition footprints.

These checks are revisited throughout processing because residual statics or geometry errors can reappear at later stages.

## Multi-attribute assessment

No single attribute reliably measures data quality. A trace may have normal amplitude but anomalous frequency; a gather may have good signal-to-noise ratio but poor flatness. Modern QC therefore combines attributes into an overall quality metric.

Common approaches:

- **Weighted sums of normalized attributes.** Each attribute is scaled to a common range and combined with weights that reflect its importance.
- **Percentile ranks.** Traces are ranked within each attribute and the ranks are combined.
- **Outlier detection.** Statistical thresholds flag traces that are extreme in one or more attributes.
- **Classification.** Machine-learning models trained on examples of good and bad traces can automate quality ranking.

A multi-attribute assessment is useful for ranking gathers, flagging bad traces, monitoring survey-wide quality, and deciding whether a processing step has improved or degraded the data. The key is to keep the metric transparent: the processor must know which attributes drove the result and whether they measure acquisition noise, geology, or processing artifacts.

## QC of kinematic processing

Kinematic processing includes velocity analysis, NMO, DMO, and stack. Its QC centers on alignment and structural plausibility:

- **Flat gathers.** After NMO, events in a CMP gather should be flat. Residual curvature means the velocity is wrong, anisotropy is unmodeled, or residual statics remain. A consistent upward or downward curve indicates a too-low or too-high stacking velocity, respectively.
- **Stack quality.** The stacked section should show continuous, geologically reasonable reflectors with improved signal-to-noise ratio.
- **Structural maps.** Horizon maps in time and depth should match geological expectations and well data. Cross-plots of horizon time or depth against well data reveal systematic shifts.
- **Residual moveout maps.** These reveal spatial variations in velocity error and guide velocity updates.
- **Semblance and velocity spectra.** Semblance peaks should align with the picked stacking velocities. Misaligned peaks may indicate anisotropy, multiples, or statics problems.

## QC of noise attenuation

- **Amplitude and spectral attributes.** Compare amplitude, frequency, and signal-to-noise attributes before and after the process. The average amplitude should drop where noise was removed, but geological amplitude trends should remain.
- **Difference section.** Inspect the **difference section** (input minus output). It should contain noise, not coherent signal. If reflectors are visible in the difference, signal has leaked into the noise panel.
- **Lateral resolution.** Check that lateral resolution is preserved by migrating the difference section or by comparing time/depth slices before and after the process. Focused energy in the migrated difference means signal leakage.
- **Geology preservation.** Horizons should remain continuous and amplitude trends should not be altered where no noise was present.

## QC of deconvolution and Q-compensation

- **Vertical resolution.** Autocorrelation width, well-tie correlation, and the ability to separate closely spaced reflectors show whether the wavelet has been compressed.
- **Lateral stability.** Maps of dominant frequency and bandwidth should be smooth except where geology changes. FX slices show how the spectrum varies with inline and crossline position.
- **Wavelet shape.** Extracted wavelets should be similar across time windows and across the survey. Large trace-to-trace variations indicate an unstable operator.
- **Phase and well tie.** The seismic wavelet should match the synthetic seismogram in phase and timing. After Q-compensation and deconvolution, the wavelet should be compact and near zero phase.
- **Signal-to-noise ratio.** High-frequency boost should improve resolution without amplifying noise.

## QC of demultiple

- **Velocity spectra.** Vertical velocity spectra before and after demultiple show whether residual multiple energy remains. Multiples usually have lower velocities than primaries and appear as separate trends.
- **Residual moveout.** Residual-moveout maps on multiple models indicate incomplete removal.
- **Multiple modeling.** Multiple traveltimes modeled from well data can be compared with the subtracted panel to confirm that the right energy was removed.
- **Well tie.** Multiples that are still present in the seismic data reduce the correlation between synthetic and seismic traces.
- **Difference section.** The subtracted multiple model should not contain primary energy.

## Interpretation-supervised processing (ИСО / WDS)

In Russian practice this is called **ИСО** (интерпретационное сопровождение обработки); related international terms include **WDS** (well-driven seismic) or interpreter-guided QC. The interpreter provides geological and well constraints at each stage:

- checkshots and sonic logs validate velocities,
- synthetic seismograms tie the wavelet to log reflectivity,
- AVO response checks amplitude preservation,
- geological maps and cross-sections constrain structural QC.

The two main instruments are the **seismic well tie** and **AVO analysis**.

## Best practices

- QC after every major step, not just at the beginning and end.
- Use multiple independent views (sections, maps, gathers, spectra, metrics).
- Document decisions and parameter choices in a processing log.
- Involve the interpreter early, especially for amplitude-sensitive work.
- Never trust a single metric without looking at the data, and never trust a visual impression without a metric.

## Related concepts

- [Seismic data QC](seismic_data_qc.md)
- [Seismic well tie](seismic_well_tie.md)
- [AVO analysis](avo_analysis.md)
- [Seismic velocities](seismic_velocities.md)
- [Velocity analysis](velocity_analysis.md)
- [Normal moveout](normal_moveout.md)
- [Deconvolution](deconvolution.md)
- [Predictive deconvolution](predictive_deconvolution.md)
- [Surface-consistent deconvolution](surface_consistent_deconvolution.md)
- [Frequency filtering](frequency_filtering.md)
- [Radon transform](radon_transform.md)
- [3D seismic acquisition](3d_seismic_acquisition.md)
- [Grid binning](grid_binning.md)

## Related lectures

- [Term 3 Lecture 1 — Quality Control of Seismic Processing and Introduction to 3D Seismic Data](../lecture_ready/term03_lec01_processing_qc_and_3d_introduction.md)
