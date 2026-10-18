---
title: "Bickel (2000) — Focusing aspects of the hyperbolic Radon transform"
status: draft
source_type: paper
authors: "Samuel H. Bickel"
year: 2000
source_file: papers/radon_taup/S.H. Bickel - Focusing aspects of the hyperbolic Radon transform.pdf
lectures:
  - term02_lec02
related_concepts:
  - radon_transform
tags: [radon, hyperbolic-radon, parabolic-radon, envelope, ellipse, focusing]
---

# Bickel (2000) — Focusing aspects of the hyperbolic Radon transform

GEOPHYSICS, VOL. 65, NO. 2 (MARCH-APRIL 2000); P. 652–655. Short note extending Maeland (1998).

## Main message

A single envelope construction unifies the whole Radon-transform family. Using the fixed-focus hyperbolic Radon transform of Foster & Mosher (1992) with focusing depth `z`:

$$F(p, \tau; x) = t(x) - \tau - p\big(\sqrt{z^2 + x^2} - z\big)$$

the envelope of a mapped event follows from the simultaneous equations `F = 0`, `∂F/∂x = 0`. The parameter `z` interpolates between the family members:

- **z = 0** → the hyperbolic term reduces to `px` → the **linear Radon (slant-stack) transform**;
- **z → ∞** → the term reduces to `qx²` with `q = p/(2z)` → the **parabolic Radon transform** (Maeland, 1998);
- **z = νT₀** (focusing depth matched to the event's moveout velocity) → the hyperbolic event **focuses to a point** at `(τ, p) = (T₀, 1/ν)`.

For a hyperbolic event `t(x) = √(T₀² + x²/ν²)` the mapped curve is a **rotated ellipse** when `νT₀ > z` and a hyperbolic arc when `νT₀ < z`. In the linear case (z = 0) the result reduces to the familiar ellipse `τ(p) = T₀√(1 − p²ν²)` closing at `p = ±1/ν`.

## Relation to lecture notes

- Term 2 Lecture 02, Section 5.3: the envelope method `F = ∂F/∂x = 0` is exactly the geometric technique used inline in the notes to derive the reflection ellipse for the linear transform. Bickel's eq. (7) with `z = 0` reproduces the lecture formula.
- Also documents *why* the hyperbolic transform is not the everyday tool: it is time-variant and computationally heavy (each focusing depth suits one velocity family), whereas the linear transform is one FFT-like operation — the reason this lecture teaches the linear transform first.

## Related concepts

- [Radon transform](../concepts/radon_transform.md)

## Related sources

- [Maeland (1998)](maeland_1998_parabolic_radon.md) — the parabolic case this note extends.
- [Zhou & Greenhalgh (1994)](zhou_greenhalgh_1994_linear_parabolic_taup.md) — discrete implementation aspects.
