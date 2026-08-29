---
title: "Wang (2002) — A Stable and Efficient Approach of Inverse Q Filtering"
status: draft
type: paper
source_file: wiki/sources/_raw_text/Yanghua Wang - A stable and efficient approach of inverse Q filtering.txt
language: en
concepts:
  - inverse_q_filtering
  - velocity_dispersion
tags: [inverse-q, downward-continuation, stabilization, layered-q, gain-limit, nonstationary-filtering]
---

# Wang (2002) — A Stable and Efficient Approach of Inverse Q Filtering

*Geophysics*, 67(2), 657–663.

## Overview

Addresses the two chronic problems of inverse Q filtering — **numerical instability** and **computational efficiency** — by recasting it as wavefield *downward continuation* through a layered constant-Q earth model. Each layer is treated by extrapolating the recorded wavefield to the top of the layer (stabilized), then applying a fast constant-Q inverse filter within the layer.

## Inverse Q filter and instability

- One-way wave propagation with complex wavenumber containing the Q effect; inverse Q filter = the inverse operator, containing an amplitude-compensation exponential $\exp(+|\omega|T/2Q)$ (two-way traveltime) and a dispersion-phase exponential.
- Uses the Kjartansson phase-velocity model $v(\omega) = v(\omega_0)(\omega/\omega_0)^{\gamma}$ with $\gamma = 1/\pi Q$.
- Demonstration: synthetic Ricker wavelets (dominant 50 Hz) at 1.0–1.9 s with Q = 400…25. Full inverse Q filtering restores wavelets for Q ≥ 200 but develops strong artifacts for low Q / late times **even on noise-free data** — the amplitude operator amplifies machine-precision "noise" once the true signal has decayed below it.
- Phase-only inverse Q filtering (amplitude operator ≡ 1) is **unconditionally stable**.

## Stabilization (gain-limited filter)

- Empirical stability condition: the accumulated exponent of the amplitude factor should not exceed ≈ 1, giving a time-varying frequency limit $\omega_q$.
- Three tested schemes: (1) truncate both phase and amplitude at $\omega_q$ with cosine² taper; (2) full-band phase, band-limited amplitude; (3) full-band phase with modified amplitude operator — a **gain-limited inverse Q filter** that clips the exponential boost beyond $\omega_q$. Scheme 3 performs best.

## Layered implementation

- Earth Q model divided into N constant-Q layers at two-way traveltimes $T_n$.
- Recursive downward continuation to the top of layer n using the exact layered operators; the top of each layer is treated as a new recording surface.
- Within a constant-Q layer, the change of variable $\omega' = \omega^{1-\gamma}$ makes the phase term linear in $\omega'$ → the filter reduces to resampling + rescaling + inverse FFT (Stolt-like; same trick as Hargreaves & Calvert 1991 phase-only method).
- The 2-D amplitude operator $A(t, \omega') = \exp(\frac{|\omega'|}{2}\int t/Q \ldots)$ is approximated three ways: $A_1(\omega')$ (averaged over the time window — a band-pass on the phase-corrected trace), $A_2(t)$ (averaged over frequency — a time gain, usable together with spherical-divergence correction instead of AGC before energy-preserving deconvolution), and the optimal separable product $A_3(t,\omega') = A_{31}(t)A_{32}(\omega')$.

## Stabilized downward continuation across overburden

- Instead of applying the (unstable) inverse extrapolation directly, a **reversed upward-continuation system** (the forward earth Q filter) is solved as a damped least-squares problem with stabilization constant $\sigma^2$: $U \approx B^*(BU_0)/(B^*B + \sigma^2)$.

## Key takeaways

- Inverse Q filtering = reverse of forward propagation; instability is intrinsic to the amplitude operator, not an implementation artifact.
- Phase correction is exact and stable; amplitude correction must be bounded.
- Layered, FFT-based implementation makes prestack application practical.
- Real-data example (stacked section, layered effective Q from 400 to 70) shows improved resolution and event continuity.

## Relation to lecture notes

Foundation for Term 2 Lecture 01, Section 5 (Futterman's and Wang's approaches to Q-compensation). The gain-limit idea connects directly to the amplitude damping factor / MAXDB-style parameter of modern processing software.

## Related sources

- [Wang (2006)](wang_2006_inverse_q_resolution.md) — continuous-variable Q extension and σ² ↔ gain-limit formula
- [Kjartansson (1979)](kjartansson_1979_constant_q.md) — velocity law used by Wang's filter
- [Futterman (1962)](futterman_1962_dispersive_body_waves.md) — causal dispersion requirement
