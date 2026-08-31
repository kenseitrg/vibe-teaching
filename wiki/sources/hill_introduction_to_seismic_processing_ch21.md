---
title: Hill — Introduction to Seismic Processing, Chapter 21 (Amplitude Correction)
status: draft
type: textbook
source_file: papers/textbooks/Steve J Hill - Introduction to Seismic Processing.pdf
language: en
pages: 88-100
concepts:
  - amplitude_effects
  - spherical_divergence
  - automatic_gain_control
  - amplitude_preservation
tags: [seismic-processing, amplitude-correction, deterministic-gain, statistical-gain, AGC, spherical-divergence]
---

# Hill — *Introduction to Seismic Processing*, Chapter 21 (Amplitude Correction)

SEG course notes (Chapter 21) devoted to the goals, strategies, and pitfalls of seismic amplitude correction.

## Relevant sections

| Section | Book pages | Topic |
|---------|------------|-------|
| What determines amplitudes? | 88–91 | Geometric dilution, absorption, scattering, intervening interfaces, rugosity, velocity lenses, AVO, source/receiver coupling, ghosts, arrays |
| Goals of amplitude correction | 91 | Keep data visible; make amplitudes representative of reflection coefficients |
| Deterministic correction | 91–93 | Geometric-spreading correction; 1/r and 1/(t·V²rms) models |
| Statistical correction | 93–97 | Trace-by-trace gain; windowed AGC; shadow-zone effect; misleading amplitudes near salt |
| Other processes altering amplitudes | 99 | Acquisition, deconvolution, filtering, NMO, statics, demultiple, stack, migration |

## Key takeaways

### Goals
- The ideal goal—amplitudes equal to reflection coefficients—is usually unachievable.
- A more practical goal is twofold:
  1. Keep the data visible throughout the section.
  2. At the end of processing, nearby amplitudes should be representative of the relative strengths of reflection coefficients.
- Evidence of failure: amplitude streaks or dim/bright regions.

### Deterministic vs. statistical amplitude correction
- **Deterministic**: inverts a known or assumed dominant amplitude-decay mechanism (e.g., geometric spreading).
  - Data-independent, preserves amplitude contrast, reversible with few parameters, smooth in time, but does not account for noise or source/receiver variability.
- **Statistical**: derives a gain function from the data’s own amplitude statistics.
  - Data-adaptive, can reduce streaks, but not reversible, can create shadow zones and misleading amplitude discontinuities (e.g., brightening near salt).

### Spherical-divergence correction
- For constant velocity: amplitude ∝ 1/r = 1/(V·t).
- With vertical velocity gradient (curved-ray): amplitude ∝ 1/[t·V²rms(t)].
- Curved rays in a velocity-gradient medium spread faster than straight rays, so amplitude decay is more severe.

### Windowed AGC
- Most common statistical gain.
- Steps: window the trace, compute a window amplitude statistic (e.g., sum of absolute amplitudes), take the reciprocal, interpolate to a continuous gain function, multiply the trace.
- AGC does not distinguish signal from noise; it boosts low-amplitude noise (e.g., pre-first-arrival noise) and can create shadow zones adjacent to very strong amplitudes.
- Shorter window → more amplitude homogenization; longer window → less.

### Amplitude display
- Be aware of clipping, trace normalization, and color-bar scaling when viewing data.
- Default display settings can hide processing problems (e.g., trace-to-trace amplitude variations that cause migration artifacts).

## Figures useful for teaching
- Figure 21-1: Factors that alter seismic amplitudes.
- Figure 21-5: Raw land shot profile with no time-dependent gain.
- Figure 21-7/21-8: Shot profiles before and after spherical-divergence correction.
- Figure 21-10: Windowed AGC operation schematic.
- Figure 21-11: Land shot profile after AGC.
- Figure 21-13/21-14: Misleading amplitudes created by statistical gain near salt and high-amplitude events.

## Relation to lecture notes
- Core reference for the deterministic/statistical gain distinction in Term 1 Lecture 2.
- Supports the spherical-divergence correction and AGC subsections.
- Provides interpreter-oriented warnings about amplitude display and processing artifacts.
