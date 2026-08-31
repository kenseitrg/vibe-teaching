---
title: "Schönleber (2014) — A Simple Derivation of the Kramers–Kronig Relations from the Perspective of System Theory"
status: draft
type: paper
source_file: wiki/sources/_raw_text/Michael Schönleber - A simple derivation of the Kramers-Kronig relations from the perspective of system theory.txt
language: en
concepts:
  - velocity_dispersion
tags: [kramers-kronig, causality, hilbert-transform, system-theory, analytic-function]
---

# Schönleber (2014) — A Simple Derivation of the Kramers–Kronig Relations from System Theory

*American Journal of Physics* (short note).

## Overview

A compact, undergraduate-accessible proof that **causality of a linear time-invariant (LTI) system implies the Kramers–Kronig relations** between the real and imaginary parts of its frequency response. This is the cleanest route to the KK relations for teaching purposes — no electromagnetism or scattering theory needed, only Fourier analysis.

## Derivation route (in brief)

1. Let $h(t)$ be the impulse response of an LTI system; frequency response $H(\omega) = \frac{1}{2\pi}\int h(t)e^{-i\omega t}dt$ (impedance in the electrical analogy).
2. Causality: $h(t) = 0$ for all $t < 0$; equivalently $h(t) = h(t)\,\sigma(t)$ with the Heaviside step function.
3. Multiplication in the time domain = convolution in the frequency domain; the transform of $\sigma(t)$ is $\pi\delta(\omega) + \mathrm{P}\frac{1}{i\omega}$, giving:

$$H(\omega) = \frac{1}{2}\Big[H(\omega) + \frac{i}{\pi}\,\mathrm{P}\!\!\int_{-\infty}^{\infty}\frac{H(\omega')}{\omega' - \omega}d\omega'\Big]$$

4. Splitting into real and imaginary parts yields the two KK relations (Hilbert-transform pair between Re H and Im H).

## Key takeaways

- The proof needs only: causality, linearity, time invariance — the same assumptions as seismic wave propagation to first order.
- KK relations state that attenuation and phase are two views of one causal response: fixing one fixes the other.
- Direct pedagogical bridge to Futterman (1962), who applies the same relations to the seismic propagation constant.

## Relation to lecture notes

This note is the backbone of `lecture_notes/derivations/kramers_kronig_dispersion_derivation.en.md` (Term 2 Lecture 01, Section 3): the derivation document reproduces this proof step by step and then specializes it to the seismic absorption–dispersion pair.

## Related sources

- [Futterman (1962)](futterman_1962_dispersive_body_waves.md) — application to dispersive body waves
