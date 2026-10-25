---
title: Term 2 Lecture 03 — Multiple Attenuation I (Kinematic Methods)
status: lecture-ready
lecture: term02_lec03
sources:
  - verschuur_2006_eet01_multiples_problem
  - verschuur_2006_eet02_moveout_discrimination
  - maeland_1998_parabolic_radon
  - trad2002_radon_interpolation
tags: [multiples, radon, parabolic-radon, high-resolution-radon, demultiple, moveout]
---

# Term 2 Lecture 03 — Multiple Attenuation I (Kinematic Methods)

First of the two demultiple sessions. Notes: `lecture_notes/en/term02_lec03_multiple_attenuation_kinematics.en.md`; deck: `slides/term02/lec03_multiple_attenuation_kinematics/`.

## Coverage

1. **What a multiple is**: ≥1 extra downward reflection; same wavelet as a primary → false reflectors/structure (real Nordkapp + synthetic false-anticline demos).
2. **Two fingerprints**: periodicity (Δt_w = 2h_w/v_w; times add, amplitudes multiply) and excess moveout (multiples live in slow shallow layers; grows per order). Secondary: conflicting dips, focusing/defocusing.
3. **Classification**: surface-related vs. internal (definition test: "disappear if the surface were removed"); long- vs. short-period vs. wavelet length; treatment by cell.
4. **Kinematic recipe** (transform → separate → mute → back) with its two requirements (separability, reversibility); legacy end-members: NMO+stack, FK.
5. **Parabolic Radon**: adjoint vs. LS inverse m=(LᴴL+λ²I)⁻¹Lᴴd per frequency; Hampson (1986) workflow; high-resolution Radon (Cauchy sparsity, IRLS) — derivation doc `highres_radon_derivation`.
6. **Four limitations**: near offsets (differential moveout → 0), velocity inversions (internal multiples move like primaries), non-hyperbolicity, AVO smear/damage → motivation for prediction methods (lec04).

## Figures (9 synthetic + 5 real-data carries)

`multiple_raypaths`, `false_structure`, `periodicity`, `multiple_moveout`, `multiple_taxonomy`, `parabolic_radon_ls`, `radon_demultiple`, `highres_radon`, `kinematic_limits`; real: stack with multiples (Nordkapp), migration with/without demultiple, Radon demultiple input/output (North Sea).

## Teaching notes

- The "adjoint ≠ inverse" moment (parabolic Radon) intentionally mirrors the rho-filter lesson of term02_lec02.
- The false-structure figure pre-computes multiples with the 1D feedback relation — an explicit SRME preview planted in Session 1.
- Numeric anchors: LS reconstruction residual ~3–4%; HR sacrifices ~2% fit for sparse panels; near-offset discrimination collapse below ~500 m.

## Status

- EN notes + PDF rendered; deck built (29 slides). Exercises: deferred by instructor. RU translation: pending.
