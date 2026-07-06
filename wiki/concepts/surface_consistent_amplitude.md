---
title: Surface-consistent amplitude correction
status: draft
sources:
  - brown_2002_surface_consistent_amplitude_correction
  - yilmaz_practical_seismic_data_analysis_amplitude
  - hill_introduction_to_seismic_processing_ch21
tags: [surface-consistent, amplitude-correction, SCAC, source-coupling, receiver-coupling, AVO, Gauss-Seidel]
---

# Surface-consistent amplitude correction

Surface-consistent amplitude correction (SCAC) separates trace-to-trace amplitude variations into source, receiver, offset, and structural (CMP) components. It is used to remove source/receiver coupling and near-surface amplitude effects while preserving geologically meaningful amplitude variations such as AVO.

## Motivation

- Amplitude variations on recorded traces are multiplicative combinations of many effects.
- Some variations are not geology:
  - Land shot coupling changes with weathering and surface hardness.
  - Marine air-gun arrays can have gun drop-outs or varying output.
  - Receiver coupling varies with ground conditions.
- These effects must be removed before AVO/AVA or amplitude-driven interpretation.

## The four-factor model

The amplitude of a trace window is modeled as the product of four factors:

$$
A_{ij} = S_i \, R_j \, G_k \, M_l
$$

where

- $S_i$ = source term for source $i$,
- $R_j$ = receiver term for receiver $j$,
- $G_k$ = geology/CMP term for CMP $k$,
- $M_l$ = offset term for offset class $l$.

Optional extra terms (trace number, user-defined literal) can be added.

Taking logarithms converts the product into a linear system:

$$
\log A_{ij} = \log S_i + \log R_j + \log G_k + \log M_l
$$

## Measuring trace amplitudes

- An analysis window is chosen over the zone of interest.
- The window should contain good-quality signal and, ideally, the same sequence of events across the survey.
- For shallow data with large moveout, the window may need to vary with offset.
- Amplitude statistic options:
  - **RMS amplitude**: robust measure of total window energy, but sensitive to noise bursts.
  - **Mean absolute amplitude**: less dominated by large bursts, but can be more sensitive to other variations.
- Data should be pre-conditioned before picking: noise attenuated, spikes removed, deterministic spreading/attenuation applied, and no adaptive scaling.

## Solving the model

- The log-linear system is usually solved by **Gauss–Seidel iteration**.
- Default order: source → receiver → offset.
- First iteration:
  1. Assume receiver and offset terms are zero; solve for source.
  2. Using the source term, solve for receiver.
  3. Using source and receiver terms, solve for offset.
- Subsequent iterations update each term using the current estimates of the others:

$$
\log S_i = \frac{1}{N_i}\sum\left(\log A_{ij} - \log R_j - \log M_l\right)
$$

and similarly for $R_j$ and $M_l$.
- Iterations stop when the RMS residual between predicted and measured amplitudes becomes small or stops decreasing.

## Two-factor vs. four-factor models

| Model | Terms | Pros | Cons |
|---|---|---|---|
| 2-factor | Source + receiver only | Stable, fewer unknowns | Cannot separate offset/structural variations; may leak geology into source/receiver terms, distorting AVO |
| 4-factor | Source + receiver + offset + CMP | More physically complete | More unknowns; risk of instability, especially with low fold; leakage between terms |

- Leakage between terms is common; the order of solution matters.
- The 2-factor model is simpler but can remove true AVO signal.
- The 4-factor model is more correct but may not fully separate long-wavelength geological variations.

## The CMP / geology term

- The CMP term is a mixture of reflectivity and spatially varying AVO effects.
- Applying it can remove the geological amplitude variations one wants to preserve.
- One strategy is to estimate and subtract an AVO trend from the picks before decomposition (sometimes called LONGWAVELENGTH_REMOVE in Omega), so SCAC only sees residual surface-consistent effects.

## QC

- **Model fit**: mean and RMS of residuals should be small; standard deviation of residuals should also be small.
- **Fold**: low fold at a source/receiver/CMP/offset gives poor statistics and unreliable terms.
- **Visual QC**: compare pre- and post-SCAC gathers and stacks; look for removed shot/receiver streaks and preserved geological trends.
- **Difference maps**: show what each model term removes.

## Related concepts
- [Amplitude effects](amplitude_effects.md)
- [Spherical divergence](spherical_divergence.md)
- [Automatic gain control](automatic_gain_control.md)
- [Seismic data QC](seismic_data_qc.md)
- [Lecture-ready page: Term 1 Lecture 02 — Amplitude Corrections and QC](../lecture_ready/term01_lec02_amplitude_correction_and_qc.md)
- [Residual statics](residual_statics.md) (for the Gauss–Seidel method used in surface-consistent statics)
