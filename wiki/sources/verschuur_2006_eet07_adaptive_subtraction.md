---
title: Verschuur (2006) — EAGE EET 07, Adaptive Subtraction of Predicted Multiples
type: course slides
year: 2006
author: Eric Verschuur
source_file: papers/multiples/EAGE EET 07 - Adaptive Subtraction.pdf
status: reviewed
tags: [multiples, srme, adaptive-subtraction, wiener-filter, l1-norm, matching-filter]
---

# Verschuur (2006) — EAGE EET 07, Adaptive Subtraction

## Source

- **Author:** Eric Verschuur (Delft University of Technology)
- **Title:** Seismic Multiple Removal Techniques: Past, Present and Future — Chapter 7: Adaptive subtraction of predicted multiples
- **Year:** 2006
- **Type:** EAGE Education Course slides
- **File:** `papers/multiples/EAGE EET 07 - Adaptive Subtraction.pdf`

## Main message

Predicted multiples are right in kinematics but wrong in dynamics: source/receiver directivity, 2D/3D propagation effects and wavelet uncertainty mean a scaling is not enough. The practical fix is a least-squares **matching filter** estimated in overlapping local windows (Wiener filter of data vs. multiple model), and subtracted. Where primaries and multiples interfere, the L2 assumption "minimum-energy output" fails; L1 subtraction is more robust to outliers (crossing events) at the cost of a non-linear estimation.

## Key points

1. **Why adaptation is needed:** SRME theory uses a surface operator A for directivity; in practice a scalar/`A(f)` is neglected, so a time-domain matching filter `a(t)` absorbs wavelet and directivity errors: `P0 = P − a(t) * M`.
2. **Implementation:** estimate a short matching filter in overlapping space-time windows; the filter length and window sizes trade adaptation accuracy against protection of primaries (long filter + small window can adapt primaries away).
3. **Two-stage strategy:** (1) large windows to find the global inverse-wavelet filter — well done in common-offset gathers (one filter per offset); (2) small windows for local amplitude/directivity corrections — best in shot domain.
4. **L2 assumption:** least-squares subtraction implicitly minimizes output energy — valid only if the output (primaries) has minimum energy. At primary-multiple interference the assumption breaks → **leakage** (residual multiples) and primary damage.
5. **L1 subtraction:** minimize Σ|e(t)| instead of Σe²(t) — puts less emphasis on large residuals (outliers), i.e. on the moments when a primary interferes with the multiple; filter estimation becomes a non-linear (iteratively re-weighted) inversion. 1D and field examples show L1 keeps the primary where L2 damages it.
6. **Curvelet-domain separation** (outlook): curvelets localize in dip and frequency; primaries and predicted multiples map to different curvelet coefficients; a notch/threshold mask separates them without a subtraction — works when the two do not overlap in the curvelet domain (Neelamani et al. 2010).
7. **Method comparison table:**
   - L2: easy, fast, robust — problems with crossing events.
   - L1: better interference handling — slower, non-linear.
   - Curvelet: discriminates on local dip/frequency — assumes no overlap, more expensive.
   - "Processor needs toolbox approach!"

## Mathematical summary

Matching-filter objective per window: given data `d(t)` and multiple model `m(t)`, find filter `a(t)` minimizing
`J_L2 = Σ (d[n] − Σ_k a[k] m[n−k])²` → Wiener normal equations (`R_mm a = r_dm`).
L1 variant: `J_L1 = Σ |d[n] − (a*m)[n]|`, solved by IRLS.

## Implications for teaching

- Direct application of the Wiener filter from term01_lec06 to a real processing problem — reinforces normal equations with a concrete purpose.
- The window/filter-length/parameter discussion maps exactly onto the instructor's "parameters of adaptive filtering" slide; L1-vs-L2 demo (1D example with filter length axis) is reproducible as a course figure.
- Generalizes beyond SRME: adaptive subtraction is the universal "model + subtract" engine for any predictable noise.

## Concepts informed

- [Adaptive subtraction](../concepts/adaptive_subtraction.md)
- [SRME](../concepts/srme.md)
- [Wiener filter](../concepts/wiener_filter.md)
- [Multiples](../concepts/multiples.md)

## Quotes / memorable lines

> "Predicted multiples are accurate in kinematics, but not always in dynamics."

> "The major assumption for least-squares subtraction is: the multiple-free output has minimum energy!"

> "Processor needs toolbox approach!"
