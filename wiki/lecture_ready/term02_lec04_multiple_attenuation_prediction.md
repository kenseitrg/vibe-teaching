---
title: Term 2 Lecture 04 — Multiple Attenuation II (Prediction Methods)
status: lecture-ready
lecture: term02_lec04
sources:
  - verschuur_2006_predictive_deconvolution
  - verschuur_2006_eet05_principles_srme
  - verschuur_2006_eet06_practical_srme
  - verschuur_2006_eet07_adaptive_subtraction
  - tang2017_5d_mpfi_srme
tags: [multiples, srme, predictive-deconvolution, tau-p, adaptive-subtraction, wiener-filter, l1-norm]
---

# Term 2 Lecture 04 — Multiple Attenuation II (Prediction Methods)

Second demultiple session. Notes: `lecture_notes/en/term02_lec04_multiple_attenuation_prediction.en.md`; deck: `slides/term02/lec04_multiple_attenuation_prediction/`.

## Coverage

1. **Prediction vs. discrimination**: a multiple is built from primaries → predictable without a velocity model.
2. **Predictive decon**: gap = water period; period varies with angle (Δt(θ)=Δt_0/cosθ) → fails at offset; **tau-p decon** with analytic gap Δτ(p)=Δt_0√(1−p²v_w²) per p-trace + p-mute; remaining limits (locally flat generator, Wiener assumptions, no long-period peg-legs).
3. **SRME**: 1D building block (times add, amplitudes multiply → convolution); feedback relation x = x_0 − x_0*x; series x_0 = x + x*x + x*x*x + …; iteration p_0^(i+1) = p − a·p_0^(i)·p (one order per pass, 33%→3% in demo); wavelet bookkeeping → surface operator a = −1/s; 2D: M(x_r,x_s;f) = A∫P(x_r,x_k)P(x_k,x_s)dx_k — matrix product per frequency, MCG apexes at true reflection points. Derivation doc: `srme_feedback_derivation`.
4. **SRME requirements**: near offsets (MCG flat legs), regular dense sampling (aliasing), wavelet/directivity, land preprocessing (operator copy; statics dilemma), internal multiples out of scope.
5. **Adaptive subtraction**: Wiener matching filter R_mm·a = r_dm in local windows; parameter interactions (length = model trust; window = adaptivity vs. stability; two-stage COG→shot); L2 minimum-energy assumption fails at interference (27% primary damage demo) vs. L1 outliers (1%) via IRLS — same re-weighting as high-res Radon; filter-length trap (bad model + long filter eats primaries); toolbox table (L2/L1/curvelets).
6. **Shallow-water chain**: decon (fog) + SRME (long-period) + Radon (residuals); EET 06 production sequence.

## Figures (10 synthetic + 6 real-data carries)

`period_vs_offset`, `taup_decon`, `srme_1d_series`, `srme_wavelet`, `srme_iterations`, `srme_2d_drp` (2D matrix engine, 8% prediction mismatch), `srme_requirements` (gap/decimation demos), `adaptive_subtraction`, `l1_vs_l2`, `shallow_water_strategy`; real: SRME predicted/subtracted, full/no-near-offset predictions, adaptive subtraction.

## Teaching notes

- The IRLS pattern deliberately recurs (high-res Radon ↔ L1 subtraction) — teach it once, reuse twice.
- The 2D figure calibrates the discrete surface integral (coupling absorbed in the operator — stated honestly in the caption); production handles this via A(f) + adaptive subtraction.
- tau-p decon figure demonstrates the mechanism in-panel (ACF evidence at the analytic gap: 98–105% periodicity suppression) — the inverse transform deliberately references the Session-1 LS machinery rather than re-deriving it.

## Status

- EN notes + PDF rendered; deck built (27 slides). Exercises: deferred by instructor. RU translation: pending.
