---
title: NUCNS SFM Best Practice — Coherent Noise Suppression for Land Data
status: draft
source_type: best practice guide
authors: "Schlumberger"
year: 2018
url: null
source_file: papers/noise_attenuation/NUCNS_SFM_Best_Practice_v4.pdf
lectures:
  - term03_lec04
related_concepts:
  - seismic_noise
  - surface_waves
  - adaptive_subtraction
  - automatic_gain_control
  - frequency_filtering
tags: [noise-attenuation, coherent-noise, best-practice, ground-roll, land-seismic]
---

# NUCNS SFM Best Practice — Coherent Noise Suppression for Land Data

Schlumberger (2018, rev. 04). *NUCNS SFM Best Practice — Non-Uniform Coherent Noise Suppression for land data*. Schlumberger Private – Customer Use.

## Main message

This best-practice guide walks through the end-to-end NUCNS workflow for land ground-roll attenuation: data analysis, preconditioning, parameter selection (gather definition, filter AGC, filter definition, signal protection), noise-model subtraction, and testing procedure. It emphasises velocity iteration, AGC strategy, and the use of adaptive subtraction to minimise signal damage.

## Key points

1. **Data analysis first:** Before running NUCNS, analyse the ground-roll characteristics (frequency, apparent velocity, spatial extent) using spectral and FK analysis. Choose representative test gathers that span quiet to noisy conditions.
2. **Preconditioning:** Apply a low-cut filter to remove very low-frequency hydrostatic pressure noise; remove dead/traces and apply basic edits. The data should have no coordinate regularisation applied before NUCNS.
3. **Gather definition:** Cross-spread gathers and common-receiver gathers are the two most common domains. For cross-spreads, set `EOG_LITERAL = SOURCE_LINE_ID`; for common-receiver, `EOG_LITERAL = STATION_NUM_DETECT`.
4. **Filter AGC:** An internal AGC applied before LS weight estimation improves stability. The AGC is removed from the output so the noise model preserves relative amplitudes. The window length should be long enough to capture signal character but short enough to follow amplitude variation.
5. **Filter definition — velocities:** Define velocity bands from the dispersion analysis. Start with conservative (narrow) velocity bands and expand iteratively. Each iteration can have its own velocity and frequency parameters.
6. **Signal protection:** Define a signal velocity band so that the LS estimation accounts for signal, but the signal-related fan filters are excluded from the noise model. This is the primary mechanism to prevent signal leakage.
7. **Adaptive subtraction:** After NUCNS produces the noise model, use `ADAPTIVE_SUBTRACT` to adaptively subtract it from the original data. This step accounts for amplitude and phase mismatches between the model and the actual noise.
8. **Testing procedure:** Run NUC stacks, gather-level QC, and amplitude-map comparisons. Test on both noisy and clean lines. Evaluate likelihood of change (typically low for parameter tweaking, moderate for topology changes).

## Relation to lecture notes

This source provides the practical counterpart to the NUCNS theory in Term 3 Lecture 04. It shows how the theoretical f-x LS framework is parameterised in production, including the critical role of adaptive subtraction and the iterative velocity-refinement strategy.

## Related concepts

- [Seismic noise](../concepts/seismic_noise.md)
- [Surface waves](../concepts/surface_waves.md)
- [Adaptive subtraction](../concepts/adaptive_subtraction.md)
- [Automatic gain control](../concepts/automatic_gain_control.md)
- [Frequency filtering](../concepts/frequency_filtering.md)

## Related sources

- [NUCNS Technical Documentation](nucns.md)
