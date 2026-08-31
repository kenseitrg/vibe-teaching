---
title: Term 1 Lecture 7 — Surface-consistent deconvolution and practical implementation
status: lecture-ready
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
tags: [term01, deconvolution, surface-consistent, practical]
---

# Term 1 Lecture 7 — Surface-consistent deconvolution and practical implementation

> 90-minute lecture. Student-facing notes: `lecture_notes/en/term01_lec07_surface_consistent_deconvolution.en.md`.

## One-line summary

Extend single-channel deconvolution to a surface-consistent four-factor model, then connect parameter choices and Python implementation to real marine and land processing flows.

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

## Key concepts covered

- Limitations of trace-by-trace deconvolution: noise, non-stationarity, and variable coupling.
- Surface-consistent four-factor model: source, receiver, offset, CDP.
- Log-spectrum linearization and the sparse design matrix $G$.
- Least-squares solution, robust norms, and scalability to large surveys.
- Parallels with residual statics and surface-consistent amplitude corrections.
- Practical parameter choice: prediction gap, operator length, prewhitening, analysis window.
- Deterministic deconvolution and Wiener normal equations in Python/NumPy.
- Choosing a deconvolution flow for marine and land data.

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
w_{s,r,h,c}(t) = s_s(t) * r_r(t) * h_h(t) * c_c(t)
$$

Full trace model:

$$
x_{s,r,h,c}(t) = w_{s,r,h,c}(t) * r_{s,r,h,c}(t) + n_{s,r,h,c}(t)
$$

Source and receiver factors encode near-surface filtering to be compensated; offset and CDP factors encode the geological response to be preserved.

### Log-spectrum linear system

Taking logarithms turns the multiplicative frequency-domain model into a linear system. For one frequency:

$$
d = Gm
$$

where $d$ contains trace log-spectra or autocorrelations, $m$ contains source/receiver/offset/CDP log-spectra or wavelets, and $G$ is a sparse design matrix encoding surface geometry.

### Least-squares solution

$$
m = (G^T G)^{-1} G^T d
$$

## Generated figures

| Figure | Path |
|--------|------|
| Surface-consistent model | `figures/term01_lec07/term01_lec07_surface_consistent_model.png` |
| Trace-by-trace vs. surface-consistent example | `figures/term01_lec07/term01_lec07_surface_consistent_example.png` |
| Parameter scan | `figures/term01_lec07/term01_lec07_parameter_scan.png` |
| Deterministic deconvolution demo | `figures/term01_lec07/term01_lec07_demo_deterministic_decon.png` |
| Wiener matrix demo | `figures/term01_lec07/term01_lec07_demo_wiener_matrix.png` |

## Lecture materials

- English notes: `lecture_notes/en/term01_lec07_surface_consistent_deconvolution.en.md`
- Rendered PDF: `lecture_notes/en/term01_lec07_surface_consistent_deconvolution.en.pdf`
- Russian notes: `lecture_notes/ru/term01_lec07_surface_consistent_deconvolution.ru.md`
- Rendered PDF (RU): `lecture_notes/ru/term01_lec07_surface_consistent_deconvolution.ru.pdf`
- Derivation: `lecture_notes/derivations/surface_consistent_deconvolution_derivation.en.md`
- Exercises: `exercises/term01_lec07_surface_consistent_deconvolution.md`
- Slide outline: `slides/term01/lec07_surface_consistent_deconvolution/slide_outline.md`
- Starter deck: `slides/term01/lec07_surface_consistent_deconvolution/lec07_surface_consistent_deconvolution.pptx`
- Figure scripts: `scripts/figures/term01_lec07/`

## Related concept pages

- [Surface-consistent deconvolution](../concepts/surface_consistent_deconvolution.md)
- [Deconvolution](../concepts/deconvolution.md)
- [Predictive deconvolution](../concepts/predictive_deconvolution.md)
- [Statistical deconvolution](../concepts/statistical_deconvolution.md)
- [Wiener filter](../concepts/wiener_filter.md)
- [Residual statics](../concepts/residual_statics.md)
- [Surface-consistent amplitude correction](../concepts/surface_consistent_amplitude.md)

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

## Notes for instructor

- This lecture builds directly on Lecture 6; students must be comfortable with the Wiener-Hopf equations before the four-factor extension.
- The parallel with residual statics is the key pedagogical bridge; the design matrix has the same sparse geometry (one row per trace, one column per source/receiver/offset/CDP factor).
- Use the tiny surface-consistent Python example to show that the method is a large least-squares problem, not a black box; this also motivates robust norms and iterative solvers.
- The Python practical section is central; allocate enough time for students to run the deterministic and Wiener demos and to inspect the operator spectra.
- When discussing parameter choices, stress that the analysis window must exclude first breaks, ground roll, and multiples; otherwise the operator is tuned to noise rather than the embedded wavelet.
- The marine vs. land flow discussion is the capstone; it shows students how to assemble a real processing sequence from the building blocks covered in the two lectures.
