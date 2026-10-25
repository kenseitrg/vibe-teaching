---
title: Verschuur (2006) — EAGE EET 02, Multiple Removal Based on Move-out Discrimination
type: course slides
year: 2006
author: Eric Verschuur
source_file: papers/multiples/EAGE EET 02 - Move-out Discrimination.pdf
status: reviewed
tags: [multiples, radon, parabolic-radon, high-resolution-radon, nmo, moveout, fk]
---

# Verschuur (2006) — EAGE EET 02, Move-out Discrimination

## Source

- **Author:** Eric Verschuur (Delft University of Technology)
- **Title:** Seismic Multiple Removal Techniques: Past, Present and Future — Chapter 2: Multiple removal based on move-out discrimination
- **Year:** 2006
- **Type:** EAGE Education Course slides
- **File:** `papers/multiples/EAGE EET 02 - Move-out Discrimination.pdf`

## Main message

Because velocity generally increases with depth (compaction), a multiple generated shallow travels more of its path in low-velocity layers than a primary arriving at the same time — so it has more moveout. Move-out discrimination transforms data (after approximate NMO) to a domain where curvature is an axis (parabolic Radon), mutes the large-curvature region, and transforms back. The least-squares formulation makes the transform reversible; the high-resolution (sparse) formulation removes the residual smearing that limits the least-squares version.

## Key points

1. **Physical basis:** shallow multiple vs. deep primary at the same time → different propagation velocities → different moveout/apparent velocity at the receiver.
2. **Two requirements for any separation domain:** primaries and multiples must actually separate; the transform must be reversible.
3. **Radon family:** linear (τ-p, stacking along straight lines, related to FK by k = f·p), parabolic (curvature q, t + q x²), hyperbolic (velocity, t² + x²/v²).
4. **Parabolic trick:** after approximate NMO correction, residual moveout of both primaries and multiples is well approximated by parabolas; parabolic Radon is efficiently computed per frequency because the shift q x² is time-independent. Hyperbolic Radon has no such frequency-domain implementation.
5. **Adjoint ≠ inverse:** naive forward/adjoint parabolic Radon smears energy in the Radon panel and does not reconstruct the input. Redefine the forward transform as the least-squares inverse of the adjoint: `m = (L^H L + λ² I)^(-1) L^H d` (stabilized). Reconstruction then matches the input and focusing improves.
6. **Hampson (1986) workflow:** NMO with a velocity between primary and multiple → parabolic Radon → mute large curvatures → inverse transform.
7. **High-resolution Radon:** LS minimizes `J = ||d − Lm||² + λ²||m||²`; high-res replaces the L2 model norm by a sparseness norm (L1 or Cauchy), solved iteratively (re-weighted/IRLS-style update of parameters per iteration). Same data reconstruction, far fewer non-zero model parameters. Also suppresses aliasing-related artifacts (Herrmann et al. 2000 comparison).
8. **Limitations:**
   - requires a *recognizable* moveout difference (fails at near offsets, where moveout difference vanishes);
   - assumes parabolic/hyperbolic moveout (fails for complex overburden: non-hyperbolic, apex-shifted events; diffractions);
   - velocity inversion zones: internal multiples of shallow fast layers can move out like primaries;
   - AVO on events smears energy across curvatures (constant-amplitude parabola → perfect spike; AVO → smearing → overlap risk).
9. **Verdict:** velocity discrimination is common, works in 3D, is efficient and works well at far offsets — but is assumption-bound, user-driven (which curvatures to keep), and distorts primary AVO.

## Mathematical summary

Parabolic Radon forward (adjoint): `M(q,f) = Σ_x D(x,f) e^{j2πf q x²}`
LS inverse: `m = (L^H L + λ² I)^(-1) L^H d`, `d̂ = L m`
High-res objective: `J = ||d − L m||² + λ Σ_{τ,q} ln(1 + m²/σ²)` (Cauchy) — non-linear, solved iteratively.

## Implications for teaching

- The bridge from term02_lec02 (FK/tau-p as transforms) to demultiple: same transforms, new discrimination axis (curvature instead of dip).
- Clean place to teach "adjoint is not inverse" and least-squares inversion with a stabilization term — concrete matrix example per frequency slice.
- The limitations list motivates the whole second half of the demultiple lecture (prediction-based methods).

## Concepts informed

- [Multiples](../concepts/multiples.md)
- [Radon transform](../concepts/radon_transform.md)
- [Radon interpolation](../concepts/radon_interpolation.md)
- [Normal moveout](../concepts/normal_moveout.md)

## Quotes / memorable lines

> "A multiple generated shallow has encountered lower velocities than a primary from a deeper reflector arriving at the same time."

> "Requirements: 1) primaries and multiples should separate; 2) the transform should be reversible."
