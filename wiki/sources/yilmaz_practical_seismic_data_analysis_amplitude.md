---
title: Yilmaz — Practical Seismic Data Analysis, Chapter 1.2–1.3 (Sampling, Aliasing, Fourier, Amplitude and Gain Control)
status: draft
type: textbook
source_file: papers/textbooks/Yilmaz - Seismic Data Analysis_1.pdf
language: en
pages: 20-31
concepts:
  - amplitude_effects
  - spherical_divergence
  - automatic_gain_control
  - seismic_wavelet
  - spectral_analysis
  - frequency_filtering
  - discrete_fourier_transform
  - aliasing
tags: [seismic-processing, amplitude, gain-control, geometric-spreading, AGC, AVO, spectral-analysis, frequency-filtering, dft, aliasing]
---

# Yilmaz — *Practical Seismic Data Analysis*, Chapter 1.2–1.3 (Sampling, Aliasing, Fourier, Amplitude and Gain Control)

Textbook chapter that introduces sampled time series, the z-transform, sampling and aliasing, Fourier analysis, seismic amplitude, the physical factors that affect it, and the basic gain-control tools used in processing.

## Relevant sections

| Section | Book pages | Topic |
|---------|------------|-------|
| 1.2.1 | 22 | Sampled time series |
| 1.2.2 | 23 | The z-transform |
| 1.2.3 | 23–25 | Sampling theorem and temporal aliasing |
| 1.2.4 | 25–26 | Spatial aliasing |
| 1.3.1 | 25–26 | Seismic amplitude; gain controls; Fourier/amplitude spectrum |
| 1.3.2 | 26–30 | Source radiation pattern; intrinsic attenuation; geometric spreading; structural properties |
| 1.3.3 | 30–31 | Gain control: AGC, RMS AGC, surface-consistent gain |
| 1.3.4 | 31 | Amplitude-versus-offset (AVO) and why AGC harms it |

## Key takeaways

### Sampled time series
- A seismic trace is a sampled time series: amplitudes recorded at regular time intervals (e.g., 2 ms or 4 ms).
- The z-transform represents a discrete time series as a polynomial in the unit-delay operator `z`.

### Aliasing and the Nyquist condition
- A time series must be sampled at least twice per cycle for the highest frequency present.
- The Nyquist frequency is `f_N = 1/(2Δt)`; energy above it folds back into the principal band.
- Practical sampling rates are often 5–10 points per cycle to allow for noise and unexpected frequencies.
- Spatial aliasing occurs when dipping events are undersampled in space.

### Fourier decomposition
- The Fourier transform decomposes a trace into sinusoidal components.
- The amplitude spectrum shows how much energy is present at each frequency.
- Figure 1.13 gives a clear visual decomposition of a trace and its amplitude spectrum.

### Seismic amplitude
- Amplitude is the magnitude of the seismic wiggles; it quantifies the energy level of the wavefield as a function of time, space, and frequency.
- Any process that alters amplitudes is called a **gain control**.

### Physical factors affecting amplitude
- **Source radiation pattern**: real sources are not isotropic; radiation varies with frequency, angle, and source type.
- **Receiver response**: usually known/measurable and compensated.
- **Media effects**:
  - **Intrinsic attenuation (absorption)**: anelastic loss quantified by the quality factor *Q*; higher frequencies are attenuated more strongly, so the spectrum shifts toward lower frequencies with time/distance.
  - **Geometric spreading**: systematic amplitude decay as the wavefront expands. In a homogeneous medium, a point source spreads spherically (amplitude ∝ 1/r), while a line source spreads cylindrically (amplitude ∝ 1/√r).
  - **Structural properties**: elastic-impedance contrasts and anisotropy create reflection/transmission partitioning.

### Gain control
- Gain control balances time-variant amplitude variations.
- **RMS amplitude AGC**: computes the RMS amplitude in a sliding gate and applies the reciprocal as a time-varying gain. The gate length can be constant or increase with time.
- **Instantaneous AGC**: the gain is assigned sample-by-sample as the gate slides one sample at a time.
- **Surface-consistent gain controls**: associate attenuation factors with each source and geophone location, accounting for near-surface effects.
- AGC is useful for display but is **harmful to any study that depends on amplitude integrity**, such as AVO.

## Figures useful for teaching
- Figure 1.10: a signal and its echo.
- Figure 1.12: spatial aliasing examples.
- Figure 1.13: Fourier decomposition of a trace and its amplitude spectrum.
- Figure 1.14: Airgun array radiation pattern at different frequencies.
- Figure 1.15: Typical amplitude decay curve, between cylindrical and spherical spreading.
- Figure 1.16: Shot gather before AGC, after trace AGC, and after trace balancing.
- Figure 1.17: AVO example (migrated CMP gather, well logs, synthetic).

## Relation to lecture notes
- Provides the physical amplitude-effects section for Term 1 Lecture 2 (amplitude corrections and QC).
- Supports the sampling, aliasing, and Fourier-decomposition sections of Term 1 Lecture 5 (spectral analysis and frequency filtering).
- Supports the AGC discussion and the warning about AVO-sensitive processing.
- Explains the energy-conservation argument behind geometric-spreading correction.
