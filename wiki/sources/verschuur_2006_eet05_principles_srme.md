---
title: Verschuur (2006) — EAGE EET 05, Principles of Surface-Related Multiple Elimination
type: course slides
year: 2006
author: Eric Verschuur
source_file: papers/multiples/EAGE EET 05 - Principles of SRME.pdf
status: reviewed
tags: [multiples, srme, surface-related, feedback-loop, convolution, prediction]
---

# Verschuur (2006) — EAGE EET 05, Principles of SRME

## Source

- **Author:** Eric Verschuur (Delft University of Technology)
- **Title:** Seismic Multiple Removal Techniques: Past, Present and Future — Chapter 5: Principles of surface-related multiple elimination
- **Year:** 2006
- **Type:** EAGE Education Course slides
- **File:** `papers/multiples/EAGE EET 05 - Principles of SRME.pdf`

## Main message

Every surface-related multiple can be seen as primaries connected at their surface reflection point. Therefore the data themselves can act as the multiple-prediction operator: surface multiples are predicted by multidimensional convolution of the measured data with the multiple-free impulse response (approximated iteratively by the data). SRME needs no subsurface model — it is fully data-driven.

## Key points

1. **1D (normal incidence) building block:** a multiple from two primaries has *travel times that add* and *amplitudes that multiply* (× the surface reflection coefficient r0 = −1) — a time-domain convolution: `m1(t) = −x0(t) * x0(t)`, `m2(t) = +x0*x0*x0`, …
2. **Feedback diagram:** the total response is a feedback system: `x(t) = x0(t) − x0(t) * x(t)`. Each loop through the surface adds one order of surface multiples.
3. **Implicit formulation:** `x0(t) = x(t) + x0(t) * x(t)` — primaries are the data minus their own surface-multiple prediction.
4. **Explicit (series) formulation for removal:** `x0 = x + x*x + x*x*x + …` (Neumann series; like 1/(1−a) = 1 + a + a² + …): multiple removal by auto-convolution and summation of the input.
5. **Including the source signature:** with wavelet s(t), the surface operator `a(t) = −[s(t)]⁻¹` appears: `p0 = p − a*p*p + a*a*p*p*p − …`. Each convolution adds one wavelet, so predicted multiples carry extra wavelets — the reason an adaptive subtraction / matching filter is needed in practice.
6. **Iterative implementation:** `p0^(i+1) = p − a*p0^(i)*p`, starting `p0^(0) = p`. Converges to the multiple-free response; each iteration removes one more order of multiples.
7. **2D formulation:** a multiple with source s, surface reflection point k, receiver r is predicted by convolving a shot-gather trace P(x_k, x_s) with a receiver-gather trace X0(x_r, x_k) and integrating over all k: `M(x_r, x_s; f) = ∫ X0(x_r, x_k; f) P(x_k, x_s; f) dx_k`. Per frequency this is a matrix multiplication `M = X0 P`; all possible downward-reflection points contribute (multiple contribution gathers).
8. **Field/synthetic examples:** Nordkapp stacks before/after SRME; iterative SRME on synthetic shot gathers converging to true primaries in ~3 iterations.
9. **Hybrid extensions:** model-driven water-bottom prediction (MWD/SWD: model water bottom, forward model its primary response G, predict bottom multiples M = G*D) and image-driven prediction (migrate, then forward model multiples from the image) — compared against full data-driven SRME on Vøring data.

## Mathematical summary

1D implicit: `x(t) = x0(t) − x0(t)*x(t)` → `x0(t) = x(t) + x0(t)*x(t)`
Series removal: `x0(t) = x(t) + x(t)*x(t) + x(t)*x(t)*x(t) + …`
With wavelet: `p0(t) = p(t) − a(t)*p(t)*p(t) + a(t)*a(t)*p(t)*p(t)*p(t) − …`, `a(t) = −[s(t)]⁻¹`
2D per frequency: `M(x_r, x_s, f) = A(f) ∫ P(x_r, x_k, f) P(x_k, x_s, f) dx_k`

## Implications for teaching

- The 1D "add times, multiply amplitudes" picture is the key intuition step before any equation.
- The feedback diagram makes the implicit form obvious and justifies both the series expansion and the iteration.
- The wavelet bookkeeping (each convolution multiplies spectra by S(f), hence the a(t) = −1/s(t) operator) explains *why* SRME is always paired with adaptive subtraction — a direct bridge to EET 07.

## Concepts informed

- [SRME](../concepts/srme.md)
- [Multiples](../concepts/multiples.md)
- [Seismic wavelet](../concepts/seismic_wavelet.md)
- [Adaptive subtraction](../concepts/adaptive_subtraction.md)

## Quotes / memorable lines

> "Each surface-related multiple consists of separate primaries that are connected at the surface reflection point."

> "Multiple removal by auto-convolution and summation of input."
