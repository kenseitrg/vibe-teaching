---
title: Frequency-dependent median filtering (AAA)
status: draft
sources:
  - cgg_odt02_denoise
tags: [median-filter, anomalous-amplitude, frequency-domain, random-noise, aaa]
---

# Frequency-dependent median filtering (AAA)

Anomalous Amplitude Attenuation (AAA) is a frequency-domain statistical method that detects and suppresses sporadic noise bursts, spikes, and other "anomalous" amplitude events. It uses the median as a robust estimator of the typical amplitude level per frequency.

## Core concept

For each frequency component in a spatial analysis window:

1. Compute the amplitude spectrum of every trace in the window.
2. For a given frequency $f$, collect the amplitudes $A_1, A_2, \dots, A_N$ across $N$ traces.
3. Compute the median amplitude $\tilde{A}(f)$.
4. Any trace whose amplitude $A_i(f)$ deviates too far from $\tilde{A}(f)$ is penalized — its amplitude is replaced or scaled down.

## Two operating modes

- **Mode 1 — punish deviations from median**: any trace with $|A_i(f) - \tilde{A}(f)| > \text{threshold}$ is scaled toward the median. This catches both positive and negative anomalies.
- **Mode 2 — punish amplitudes above a level**: any trace with $A_i(f) > \tilde{A}(f) \times \text{factor}$ is attenuated. This only catches positive anomalies (loud bursts).

## Key assumption: most traces are "normal"

AAA relies on the statistical assumption that at most a few traces in any analysis window contain anomalous noise. If every trace in the window is anomalous (e.g., all traces are noisy), the median itself is biased and no anomaly is detected. The window must be large enough that the "good" traces dominate the median.

## Window design

The analysis window must follow the data kinematics:

- Flatten the window so that the target event has approximately constant moveout.
- The window should cover the expected spatial extent of the noise burst (typically a few traces to a few tens of traces).
- Overlapping windows ensure smooth transitions.

## Limitation: AVO damage

Over-aggressive AAA can damage **amplitude-variation-with-offset (AVO)** trends. A legitimate AVO gradient causes amplitudes to vary systematically with offset — AAA may mistake this for anomalous noise. The solution is to apply AAA before AVO-sensitive processing, or to use a wide enough threshold that the AVO trend is preserved.

## Sorting for coherent noise

AAA is designed for random, trace-localized noise. However, it can also target coherent noise if the data are sorted so that the noise appears isolated: for example, a ground-roll cone in a shot gather is not anomalous in shot sort, but in CMP sort it may appear as scattered large amplitudes.

## Related methods

- **AMPSCAL** (amplitude scaling): similar principle but applied as a global trace scaling, not per-frequency.
- **TFCLEAN** (time-frequency cleaning): removes isolated noise bursts in a time-frequency plane, related to the median-filtering idea.

## Related concepts

- [Seismic noise](seismic_noise.md)
- [Frequency filtering](frequency_filtering.md)
- [Automatic gain control](automatic_gain_control.md)
- [Surface-consistent amplitude](surface_consistent_amplitude.md)
- [AVO analysis](avo_analysis.md)

## Sources

- CGG (ODT-02) — Denoise processing guide.
