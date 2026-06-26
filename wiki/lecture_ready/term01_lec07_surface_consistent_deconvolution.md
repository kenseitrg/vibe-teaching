---
title: Term 1 Lecture 7 — Surface-consistent deconvolution and practical implementation
status: draft
course_term: 1
lecture: term01_lec07
sources:
  - hutchinson_link_1984_surface_consistency
  - yilmaz_2001_seismic_data_analysis_deconvolution
  - hatton_worthington_makin_1986_seismic_data_processing
concepts:
  - surface_consistent_deconvolution
  - statistical_deconvolution
  - predictive_deconvolution
  - deconvolution
tags: [lecture-ready, term01, deconvolution, surface-consistent, practical]
---

# Term 1 Lecture 7 — Surface-consistent deconvolution and practical implementation

> 90-minute lecture. Student-facing notes: `lecture_notes/en/term01_lec07_surface_consistent_deconvolution.en.md`.

## Learning objectives

After this lecture students should be able to:
1. Explain how surface-consistent deconvolution reduces the near-surface influence on source and receiver wavelets.
2. Write the surface-consistent convolutional model and the linear system $d = Gm$.
3. List the four surface-consistent factors and describe how they enter the trace operator.
4. Choose deconvolution parameters (prediction gap, operator length, prewhitening, analysis window) for a given goal.
5. Implement a simple deterministic deconvolution and a Wiener normal-equation solution in Python/NumPy.
6. Compare deterministic, statistical, predictive, and surface-consistent methods and choose an appropriate flow.

## Prerequisites

- Single-channel deconvolution (Lecture 6).
- Basic least-squares / linear algebra.
- Python/NumPy at the level used in earlier lectures.

## Lecture outline (90 min)

| Section | Time | Key idea |
|---------|------|----------|
| 1. Recap and limitations of trace-by-trace deconvolution | 5 min | Four-factor model; near-surface source/receiver effects vs. geological offset/CDP effects |
| 2. Surface-consistent deconvolution | 25 min | Four-factor model, linear system, robust solutions |
| 3. Deconvolution parameters in practice | 15 min | Gap (first/second zero crossing), length, prewhitening, window selection (exclude first breaks/guided waves) |
| 4. Python practical: deterministic and Wiener deconvolution | 30 min | Spectral division, normal equations, apply to synthetic data |
| 5. Choosing a deconvolution flow | 10 min | Land/OBC: surface-consistent preferred; marine: designature → deghosting → predictive → zero-phase; land: min-phase conversion → instrument inverse filter → surface-consistent → zero-phase |
| 6. Comprehension questions and discussion | 5 min | |

## Key equations

### Surface-consistent trace model

$$
trace_{s,r}(t) = source_s(t) * receiver_r(t) * offset_{s,r}(t) * cdp_{s,r}(t) * reflectivity_{s,r}(t)
$$

Source and receiver factors encode near-surface filtering to be compensated; offset and CDP factors encode the geological response to be preserved.

### Linear system

$$
d = Gm
$$

where $d$ contains trace spectra or autocorrelations, $m$ contains source/receiver/offset/CDP log-spectra or wavelets, and $G$ is a sparse design matrix encoding surface geometry.

## Figures to generate

1. Schematic of source, receiver, offset, CDP factors.
2. Synthetic example: trace-by-trace vs. surface-consistent result.
3. Parameter scan: prediction gap and operator length.
4. Python demo screenshots / code snippets.

## Practical exercises

1. Write a function that performs deterministic deconvolution by spectral division with prewhitening.
2. Build the Wiener normal-equation matrix from a trace autocorrelation and solve for a spiking operator.
3. Apply the operator to a synthetic trace and compare input/output autocorrelations.
4. Optional: set up a tiny surface-consistent linear system and solve it.

## Concept-check questions

1. Why does surface-consistent deconvolution need more than one trace per source/receiver location?
2. What happens if the analysis window contains strong ground roll, first breaks, or guided waves?
3. When would you prefer deterministic deconvolution over statistical deconvolution?
4. How does prewhitening affect the deconvolved spectrum at frequencies with weak signal?
5. What is the parallel between surface-consistent deconvolution and residual statics?

## Sources

- Hutchinson & Link (1984), surface-consistent deconvolution paper.
- Yilmaz (2001), Vol. 1, surface-consistent deconvolution section.
- Hatton et al. (1986), practical deconvolution parameters.
