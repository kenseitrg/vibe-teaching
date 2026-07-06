---
title: Normal moveout (NMO)
status: draft
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - cgg_odt01_data_analysis_part1
  - noble_2020_whats_the_datum
  - margrave_2006_methods_of_seismic_data_processing
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

## Geometric origin

Margrave (Chapter 7) derives the hyperbola by considering a spherical wavefront expanding from a reflector. If the arrival time at $x=0$ is $t_0$, the time at offset $x$ follows from the extra path length the wavefront must travel, giving the familiar hyperbolic form. The family of NMO curves for a fixed velocity and different $t_0$ all share the asymptotes $t = \pm x / V$.

## NMO correction

**NMO correction** maps each sample to its zero-offset time:

$$
\Delta t_\text{nmo}(x) = \sqrt{t_0^2 + \frac{x^2}{V_\text{nmo}^2}} - t_0.
$$

After correction, reflection events should be flat and ready for stacking.

## Effect of reflector dip

For a reflector dipping at angle $\delta$ beneath a constant-velocity overburden, the image-source construction gives (Margrave):

$$
t^2(x) = t_0^2 + \frac{x^2 \cos^2(\delta)}{V^2},
$$

so the stacking velocity becomes

$$
V_\text{stack} = \frac{V}{\cos(\delta)}.
$$

In 3-D, the apparent dip along the seismic line matters:

$$
V_\text{stack} = \frac{V}{\sqrt{1 - \sin^2(\delta) \cos^2(\omega)}},
$$

where $\omega$ is the azimuth of the line relative to the dip direction. This dip dependence is why a single stacking velocity can fail for steeply dipping events.

## NMO in a v(z) medium

In a vertically varying velocity medium, the traveltime can be expanded as a power series in offset:

$$
t^2(x) = c_1 + c_2 x^2 + c_3 x^4 + \ldots,
$$

with

$$
c_1 = t_0^2,
\qquad
 c_2 = \frac{1}{V_\text{avg} V_m} = \frac{1}{V_\text{rms}^2}.
$$

This is the theoretical link between stacking velocities and RMS velocities (Dix, Al-Chalabi, Taner \& Koehler). The $c_3$ term is the fourth-order moveout coefficient and becomes important when the offset-to-depth ratio $H / z_0$ is large or for converted/shear waves. To the extent higher-order terms are negligible, stacking velocities approximate RMS velocities.

## Key effects

- Under-correction: velocity too high, event still curves downward.
- Over-correction: velocity too low, event curves upward.
- NMO stretch: far-offset samples are stretched in time, lowering frequency; stretched samples are muted before stack.

## Relation to lecture notes

Core topic in [Term 1 Lecture 03 — Kinematics, Velocities and Field Statics](../lecture_ready/term01_lec03_kinematics_and_field_statics.md).
