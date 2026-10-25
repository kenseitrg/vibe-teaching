---
title: Multiples (multiple reflections)
status: draft
sources:
  - verschuur_2006_eet01_multiples_problem
  - verschuur_2006_eet02_moveout_discrimination
  - verschuur_2006_eet05_principles_srme
  - cgg_odt04_deconvolution_part3_demultiple
tags: [multiples, noise-attenuation, surface-related, internal, periodicity, moveout]
---

# Multiples (multiple reflections)

A **multiple** is a reflection that has undergone at least one *additional downward* reflection (at the free surface or at an intrabed interface) before being recorded. A **primary** has exactly one upward reflection. Multiples carry the same wavelet and the same frequency band as primaries — they are reflections too — which is why they are the most dangerous coherent noise in seismic processing: they image as false reflectors and false structure.

## Classification

### By downward-reflection interface

- **Surface-related multiples** — at least one downward reflection at the earth's free surface (or sea surface, with reflection coefficient ≈ −1). Definition (Verschuur): *the multiples that would disappear if the earth's surface were removed.*
  - water-bottom multiples (source → bottom → surface → bottom → receiver, etc.)
  - peg-legs / reverberations involving the first layer
  - surface multiples from deeper reflectors (source → deep reflector → surface → deep reflector → receiver)
- **Internal (interbed) multiples** — all downward reflections happen below the surface, inside the subsurface. Interface-related multiples are named by their *shallowest* downward reflection.

### By period

- **Long-period multiples** (roughly > 50 ms separation): appear as separate events; "deterministic", individually predictable and removable (Radon demultiple, SRME).
- **Short-period multiples** (separation ≲ wavelet length): interfere with primaries; behave as an effective transmission effect, addressed statistically (deconvolution) rather than event-by-event.

## Characteristics exploited by removal methods

Every demultiple method exploits one of two properties:

1. **Kinematic difference (moveout/dip).** Because velocity generally increases with depth, a shallow multiple and a deep primary arriving at the same zero-offset time have different stacking velocities: the multiple has more moveout (arrives increasingly late at far offset). Higher-order multiples have progressively more moveout. This is the basis of NMO/FK-based and Radon-based demultiple.
2. **Periodicity / predictability.** In 1D (normal incidence), multiples repeat with the two-way period of the generating layer(s): a multiple is a sum of primaries with *times added and amplitudes multiplied*. This is the basis of predictive deconvolution and SRME.

Additional recognizable behaviors: increasing dips for higher orders; conflicting dips with primaries; focusing/defocusing caused by structure in the multiple-generating layer; amplitude magnification for higher orders; interference with primaries.

## Why they matter

- Migration images multiples as if they were primaries → false reflectors, false structure (classic Middle East false-anticline examples).
- Multiples contaminate AVO/AVA analysis, velocity analysis (they stack at too-low velocities and bias picks), and well ties.
- In areas with strong water-bottom reflectivity (shallow water, hard bottom) or with velocity inversions, multiples can dominate the section.

## Removal method families

| Family | Discriminating property | Methods |
|---|---|---|
| Move-out / dip discrimination | different kinematics in CMP domain | NMO-based stack discrimination, FK demultiple, (hyperbolic/parabolic, least-squares, high-resolution) Radon demultiple |
| Periodicity / prediction | 1D periodicity or primary-composition predictability | predictive deconvolution (t-x and τ-p), SRME (data-driven), model-driven and image-driven prediction |
| Subtraction technology | matches a *modelled* noise to the data | adaptive subtraction (L2/L1 matching filters) — the engine that makes prediction methods practical |

Related: [Radon transform](radon_transform.md), [Predictive deconvolution](predictive_deconvolution.md), [SRME](srme.md), [Adaptive subtraction](adaptive_subtraction.md), [FK filtering](fk_filtering.md).
