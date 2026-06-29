---
title: Normal moveout (NMO)
status: draft
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - cgg_odt01_data_analysis_part1
  - noble_2020_whats_the_datum
tags:
  - nmo
  - velocity
  - cmp-gather
---

# Normal moveout (NMO)

**Normal moveout (NMO)** is the offset-dependent increase in reflection traveltime observed on a common-midpoint (CMP) gather. For a flat, horizontally layered medium the reflection arrival time is approximately hyperbolic:

$$
t^2(x) = t_0^2 + \frac{x^2}{V_\text{nmo}^2},
$$

where $x$ is source–receiver offset, $t_0$ is the zero-offset two-way time, and $V_\text{nmo}$ is the NMO velocity.

## NMO correction

**NMO correction** maps each sample to its zero-offset time:

$$
\Delta t_\text{nmo}(x) = \sqrt{t_0^2 + \frac{x^2}{V_\text{nmo}^2}} - t_0.
$$

After correction, reflection events should be flat and ready for stacking.

## Key effects

- Under-correction: velocity too high, event still curves downward.
- Over-correction: velocity too low, event curves upward.
- NMO stretch: far-offset samples are stretched in time, lowering frequency; stretched samples are muted before stack.

## Relation to lecture notes

Core topic in [Term 1 Lecture 02 — Kinematics, Velocities and Field Statics](../lecture_ready/term01_lec02_kinematics_and_field_statics.md).
