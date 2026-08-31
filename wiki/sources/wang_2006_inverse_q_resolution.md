---
title: "Wang (2006) — Inverse Q-Filter for Seismic Resolution Enhancement"
status: draft
type: paper
source_file: wiki/sources/_raw_text/Yanghua Wang - Inverse Q -filter for seismic resolution enhancement.txt
language: en
concepts:
  - inverse_q_filtering
tags: [inverse-q, stabilization, gabor-transform, gain-limit, continuous-q, resolution]
---

# Wang (2006) — Inverse Q-Filter for Seismic Resolution Enhancement

*Geophysics*, 71(2), V51–V60.

## Overview

Refines the stabilized full inverse Q filter of Wang (2002) to handle a **continuously variable Q(τ)** earth model (no layering approximation), analyzes what stabilization does physically, and derives an **empirical link between the stabilization factor σ² and a user-specified gain limit in dB** — the practical "amplitude damping" knob of modern Q-compensation software.

## Algorithm

- Forward propagation with complex wavenumber $k(\omega) = (1 - i/2Q_r)(\omega/v_r)(\omega/\omega_h)^{-\gamma}$, where $Q_r, v_r$ are at an arbitrary reference frequency, $\gamma = \pi^{-1}Q_r^{-1}$ (following Kolsky and Kjartansson), and $\omega_h$ is a tuning parameter tied to the highest usable frequency.
- Inverse Q filter = amplitude operator $\exp(\int (\omega/\omega_h)^{-\gamma}\omega/2Q(\tau')\,d\tau')$ and dispersion phase operator $\exp(i\int(\omega/\omega_h)^{-\gamma}\omega\,d\tau')$ with Q(τ) varying continuously over traveltime.
- Stabilization by solving the amplitude inversion as a damped least-squares problem:

$$\Lambda(\tau,\omega) = \frac{\Lambda_a(\tau,\omega) + \sigma^2}{\Lambda_a^2(\tau,\omega) + \sigma^2}, \qquad \Lambda_a = \exp\Big(-\!\!\int_0^\tau \tfrac{\omega}{2Q(\tau')}d\tau'\Big)$$

- Phase operator applied **exactly** (unconditionally stable); only the amplitude operator is stabilized.

## Physical understanding and design choices

- Inverse Q filtering is a nonstationary (time-variant) weighting of plane waves; beyond the traveltime where a frequency component has decayed below ambient noise, the filter should *not* try to restore it.
- Two stabilization variants: without high-ω suppression (σ² in numerator — operator is invertible/removable, preferred for 4D re-processing) vs. conventional with suppression (Λ/(Λ²+σ²) — acts as a time-variant low-pass tied to the Q model, not invertible).
- **Gain limit relation**: with ε = ωτ and g(ε) = exp(ε/2Q), the explicit gain-limit scheme clips gain at $g_\text{lim} = e^{G_\text{lim}/20}$; matching the accumulated gain of both curves yields the empirical formula

$$\sigma^2 = \exp\!\big(-(0.23\,G_\text{lim} + 1.63)\big)$$

  valid for gain limits 10–100 dB, independent of Q. Example: σ² = 2.66% used in a field example.
- The stabilized scheme beats a plain gain limit + high-cut: it tapers the gain gracefully where signal has died instead of boosting ambient noise to the limit.

## Implementation

- Exact implementation evaluates the filter sample-by-sample (expensive); an efficient approximate implementation works in the **Gabor transform** domain (localized FFTs down the trace): modify the time-frequency spectrum, inverse-transform back.
- Synthetic tests (Q = 88; five-Q series 400…25): stabilization removes instability artifacts; wavelet phase fully recovered in the band where amplitudes exceed ~−80 dB; stabilized scheme compensates more high-frequency energy than gain-limited scheme at equal noise level.
- Field data (both land stack and prestack examples) show visibly improved resolution, stronger S/N than gain-limited alternatives.

## Key takeaways

- Stabilization factor ↔ maximum amplitude boost in dB is the practical parameter students will meet in processing software (e.g., "maximum gain / MAXDB"-style parameters).
- Amplitude + phase compensation with proper stabilization improves resolution **without** proportional noise amplification.
- The Q model may be a continuous function of traveltime — effective Q or interval Q.

## Relation to lecture notes

Term 2 Lecture 01, Section 5 (Wang's approach) and Section 6 (practical aspects: amplitude damping factor, compensation modes). In lecture notes, refer to software parameters generically ("modern processing software"), not by module names.

## Related sources

- [Wang (2002)](wang_2002_stable_inverse_q.md) — layered predecessor with gain-limited filter
- [Kjartansson (1979)](kjartansson_1979_constant_q.md) — velocity power law
- [Paradigm QAPP/QEST references](paradigm_qapp_qest.md) — production implementation of the same ideas
