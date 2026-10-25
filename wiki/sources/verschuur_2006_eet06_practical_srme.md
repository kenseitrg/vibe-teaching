---
title: Verschuur (2006) — EAGE EET 06, Practical Aspects of SRME
type: course slides
year: 2006
author: Eric Verschuur
source_file: papers/multiples/EAGE EET 06 - Practical Aspects of SRME.pdf
status: reviewed
tags: [multiples, srme, near-offsets, interpolation, shallow-water, land-data, regularization]
---

# Verschuur (2006) — EAGE EET 06, Practical Aspects of SRME

## Source

- **Author:** Eric Verschuur (Delft University of Technology)
- **Title:** Seismic Multiple Removal Techniques: Past, Present and Future — Chapter 6: Practical aspects of surface-related multiple elimination
- **Year:** 2006
- **Type:** EAGE Education Course slides
- **File:** `papers/multiples/EAGE EET 06 - Practical Aspects of SRME.pdf`

## Main message

SRME in theory needs complete, regularly sampled, broadband data with near offsets included. Real surveys violate every one of these assumptions, and "non-ideal data give non-ideal prediction results". The practical recipe is a preprocessing chain: deconvolution/deghosting, near-offset reconstruction, shot interpolation, then SRME, then Radon for residual multiples. On land, SRME additionally fights statics, ground roll and amplitude balancing problems.

## Key points

1. **Prediction involves all shots:** each predicted multiple trace is an integral over all surface points → any missing/coarse/irregular data create artifacts in the prediction ("multiple contribution gathers" show the apex at the surface reflection point).
2. **Coarse source spacing** → spatial aliasing artifacts in prediction; poor-man's fix: repeat available sources.
3. **Missing near offsets** → limited-aperture artifacts; effect grows for later reverberations (they need flatter, longer path contributions).
4. **Near-offset interpolation recipe:** NMO-corrected CMP → parabolic Radon → extrapolate beyond aperture → inverse Radon → re-insert interpolated traces. Error grows sharply in shallow water (50–100 m), where the water-bottom primary itself lives in the gap.
5. **Data-regularization sequence:** reciprocity to split spread → select desired area → interpolate sources → near-offset reconstruction.
6. **Shallow-water strategy (staged):** remove water-layer multiples (FK filter for post-critical events / water-bottom mute) → remove water-layer reverberations (predictive deconvolution, possibly τ-p) → remove the remaining surface multiples (SRME) → wavelet deconvolution. Gulf of Suez example walks through FK → pred.decon → SRME stages.
7. **Standard SRME-based marine sequence:** swell-noise removal, bad-trace editing, FK filtering of post-critical events, direct-wave removal, wavelet decon + deghosting, predictive decon (shallow water), shot interpolation, near-offset reconstruction, SRME, Radon demultiple for residuals.
8. **Land data:** marine shots are clean operators; land shots carry ground roll, statics, amplitude imbalance → SRME needs dedicated preprocessing of the *operator* data (residual statics, ground-roll filter, amplitude balancing, lateral filtering, α-trimmed median in common-offset domain); the preprocessed version is only used for prediction, subtraction is applied to the raw input. Strong surface multiples on land require a consolidated near surface (Middle East example).
9. **Statics discussion:** multiples are generated at the *true* surface (no statics should be applied before SRME), whereas a multiple generated at a reflector below the surface needs statics — a practical dilemma for land SRME.
10. **OBS/ocean-bottom data:** up/down wavefield decomposition (P and Vz) suppresses receiver-side reverberations but not source-side; elastic decomposition needs Vx too.

## Implications for teaching

- This chapter is the "SRME limitations" lecture material: near offsets, regularity/aliasing, wavelet, land-data difficulties.
- Connects forward to regularization/interpolation (term03_lec06) and back to τ-p and Radon tools already taught.
- The staged shallow-water recipe shows how all demultiple tools of the lecture are *combined* in a real flow — a great summary slide.

## Concepts informed

- [SRME](../concepts/srme.md)
- [Multiples](../concepts/multiples.md)
- [Seismic data regularization](../concepts/seismic_data_regularization.md)
- [Radon interpolation](../concepts/radon_interpolation.md)

## Quotes / memorable lines

> "Non-ideal data give non-ideal prediction results."

> "Land data need careful preprocessing before using them as [a prediction] operator."
