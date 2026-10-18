---
title: "Maeland (1998) — Focusing aspects of the parabolic Radon transform"
status: draft
source_type: paper
authors: "Einar Maeland"
year: 1998
source_file: papers/radon_taup/PINNACLE - Maeland.tex.pdf
lectures:
  - term02_lec02
  - term02_lec03
related_concepts:
  - radon_transform
tags: [radon, parabolic-radon, focusing, peg-leg-multiples, demultiple]
---

# Maeland (1998) — Focusing aspects of the parabolic Radon transform

GEOPHYSICS, VOL. 63, NO. 5 (SEPTEMBER-OCTOBER 1998); P. 1708–1715, 8 FIGS.

## Main message

From a geometric point of view the parabolic Radon transform of a common-shot (or CMP) gather is a **focusing technique** whose "focal length" is determined by the velocity field. Where the traveltime curves are approximately hyperbolic at small offset, the reciprocal of the curvature of an "image" in the transform domain relates to the square of the curvature at zero offset of the original traveltime curve. Each event separates in the transform, and — usefully — **the positions of the foci associated with peg-leg multiples can be predicted**, which underpins parabolic-Radon demultiple design.

## Context provided by the introduction

- The standard slant stack / linear Radon transform converts hyperbolas in (x, t) into **ellipses** in (p, τ).
- A **hyperbolic** Radon transform would convert hyperbolas into points, but is time-variant and computationally unsuitable; the **parabolic** transform (applied after NMO or an r²-stretch) is the practical compromise.
- Canonical applications with references: multiple suppression (Hampson 1986; Foster & Mosher 1992; Verschuur & Kabir 1992), velocity filtering (Mitchell & Kelamis 1990), and least-squares implementations (Beylkin 1987; Kostov 1990; Zhou & Greenhalgh 1994; Sacchi & Ulrych 1995).

## Relation to lecture notes

- Term 2 Lecture 02: one-sentence contrast in §5 — hyperbolas → points only under a matching (hyperbolic/parabolic) transform; the linear transform keeps them as ellipses but localizes linear noise to points, which is what linear-noise attenuation needs.
- Term 2 Lecture 03 (multiples): parabolic Radon focusing and peg-leg foci prediction are the classical demultiple geometry.

## Related concepts

- [Radon transform](../concepts/radon_transform.md)

## Related sources

- [Bickel (2000)](bickel_2000_hyperbolic_radon_focusing.md) — extends this analysis to the hyperbolic transform.
- [Zhou & Greenhalgh (1994)](zhou_greenhalgh_1994_linear_parabolic_taup.md).
