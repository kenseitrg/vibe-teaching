---
title: "Gower (2003) — Optimising tau-p for noise & multiple suppression: a North Sea example"
status: draft
source_type: internal article / training slides
authors: "Rick Gower (WesternGeco)"
year: 2003
source_file: papers/radon_taup/JGoto - intouch_taup_200103.ppt.pdf
lectures:
  - term02_lec02
  - term02_lec03
related_concepts:
  - radon_transform
  - seismic_noise
  - fk_filtering
tags: [tau-p, linear-noise, model-subtract, demultiple, north-sea, production]
---

# Gower (2003) — Optimising tau-p for noise & multiple suppression

WesternGeco inTouch presentation, January 2003. Identical copy in `papers/duplicates/Optimising_taup.pdf`.

## Main message

A production case study showing two tau-p workflows on North Sea streamer data: (1) **direct-arrival (linear) noise suppression** by transforming only the noise dips to tau-p and **subtracting the noise model** from the input, and (2) **demultiple** via targeted tau-p deconvolution plus muting. The philosophy throughout is *model the noise, subtract it, keep the signal* — not zero-out — so far offsets survive for PSTM/AVO.

## Data

8 streamers × 2 sources, 6 km cable, 480 groups at **12.5 m spacing**, 25 m flip-flop, 8 s record, flat waterbottom at 90 ms.

## Part 1 — direct-arrival noise suppression (linear noise attenuation)

Processing steps (slide 5, with the rationale):

1. Isolate the contaminated part of the shot gather (avoid processing clean data).
2. Time-shift down 1000 ms, then **LMO with a constant velocity (1550 m/s)** — this turns the direct-arrival cone into a small family of dips separable from the underlying signal.
3. **Linear tau-p transform of the noise-related dips only** (choose the p range to model noise, not signal).
4. Optionally mute in tau-p with a taper (the authors found it made little difference — done largely for client confidence).
5. Inverse transform, remove LMO and time shift → **noise model**.
6. Gentle inner mute on the noise model, then **subtract** from the input.
7. Regional NMO + mild stretch mute + **0.5K anti-alias filter** (wraparound-aware).

Lesson: transform → keep only noise → inverse → subtract. The subtraction (not the mute) protects signal amplitudes.

## Part 2 — demultiple with tau-p (for Term 2 Lecture 03)

- Multiples are periodic in the tau-p domain → **targeted tau-p deconvolution** (prediction-gap style) applied to selected p traces.
- Mute design discipline: **200 ms time tapers on all edges, no sharp corners** (sharp corners ring when transformed back), sloping limbs → time-variant mute pattern; symmetry is arbitrary.
- QC panels: raw shots → tau-p → decon → mute → back to x-t; raw vs post CMPs (NMO'd) and QC stacks; "difference" stack shows what was removed.

## Practical outcomes

- Significant increase in usable far-offset data for PSTM and AVO.
- Avoided direct-arrival muting, shot f-k filtering, DENOISE and SWATT passes — a one-pass tau-p route replaced several legacy steps.
- Mute-edge tapering rules and the LMO-before-tau-p trick are directly transferable to any tau-p noise-attenuation implementation.

## Relation to lecture notes

- Term 2 Lecture 02: Sections 4.3 and 6.2 (model-and-subtract vs zero-out QC; mute design with tapers; LMO conditioning before the transform).
- Term 2 Lecture 03 (multiples): periodicity of multiples in tau-p and targeted tau-p deconvolution.

## Related concepts

- [Radon transform](../concepts/radon_transform.md)
- [Seismic noise](../concepts/seismic_noise.md)
- [FK filtering](../concepts/fk_filtering.md)

## Related sources

- [CGG ODT02 De-noise](cgg_odt02_denoise.md) — Part 4 covers the same tau-p LNA workflow from CGG's perspective.
- [Yilmaz (2001) §6.3](yilmaz_2001_seismic_data_analysis_taup.md) — tau-p deconvolution of multiples.
