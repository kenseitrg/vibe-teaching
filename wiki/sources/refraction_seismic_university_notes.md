---
title: Refraction Seismic Method (university course notes)
status: reviewed
type: course notes
source_file: papers/statics/Refraction_Seismic.pdf
language: en
pages: 18
concepts:
  - static_corrections
  - seismic_velocities
tags: [refraction, statics, delay-time, plus-minus, grm, head-wave]
---

# Refraction Seismic Method (university course notes)

Course notes for GEOL 335.3 — Refraction Seismic Method.

## Main message

Refraction methods use first-arrival traveltimes to estimate refractor velocity, depth, and dip. They are the classical basis for near-surface model building and static corrections.

## Key concepts

### Two-layer problem

A low-velocity layer ($V_1$) over a higher-velocity half-space ($V_2 > V_1$). At post-critical offsets the first arrival is a head wave travelling along the interface.

### Travel-time relations

For a head wave from a horizontal interface:

$$
t(x) = t_0 + \frac{x}{V_2},
$$

where $t_0$ is the intercept time.

The delay time at source or receiver is:

$$
t_{\text{Delay}} = \frac{h}{V_1 \cos i_c},
$$

with $i_c = \sin^{-1}(V_1/V_2)$ and $h$ the layer thickness.

### Critical and crossover distances

- Critical distance: $x_c = 2h \tan i_c$.
- Crossover distance: offset where the head wave overtakes the direct wave.

### Dipping refractor

Reversed shooting is required. Down-dip apparent velocity is slower than the true refractor velocity; up-dip apparent velocity is faster.

### Interpretation methods

- **Plus–minus method (Hagedoorn)**: uses reciprocal shot pairs.
- **Generalized Reciprocal Method (GRM)**: generalizes plus–minus by allowing arbitrary receiver pairs; produces a velocity-analysis function and a time-depth function.
- **Head-wave migration / travel-time continuation**: maps travel-time curves into a depth image of the refractor.
- **Phantoming**: extends head-wave arrivals using time-shifted picks from other shots.

### Hidden-layer problem

Some velocity contrasts are invisible in first arrivals:
- Low-velocity layers never appear.
- Thin layers on top of a strong contrast may be missed.
- Sparse geophone coverage can miss short travel-time branches.

## Relation to lecture notes

Supports Term 1 Lecture 02 (refraction statics, delay-time methods) and provides context for Term 1 Lecture 03 (tomography as the modern extension).
