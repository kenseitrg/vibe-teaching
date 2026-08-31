---
title: Seismic velocities
status: draft
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - margrave_2006_methods_of_seismic_data_processing
  - noble_2020_whats_the_datum
tags:
  - velocity
  - nmo
  - rms
  - interval-velocity
---

# Seismic velocities

Seismic processing uses several velocity definitions. Each is tied to a different assumption about the ray path through the subsurface. Margrave (Chapter 6) derives these systematically from the instantaneous velocity $v(z)$ and the vertical traveltime $\tau$.

## Definitions

For a horizontally layered medium with layer interval velocities $v_i$ and two-way interval times $\Delta t_i$:

**Interval velocity** — velocity of one layer:

$$
v_i = \frac{2 \Delta z_i}{\Delta t_i}.
$$

**Average velocity** — total depth over total one-way time; assumes a vertical ray:

$$
V_\text{avg} = \frac{\sum_i v_i \Delta t_i}{\sum_i \Delta t_i}.
$$

Equivalently, as a function of vertical traveltime:

$$
V_\text{avg}(\tau) = \frac{1}{\tau} \int_0^\tau v(\tau') \, d\tau'.
$$

**RMS velocity** — root-mean-square of interval velocities; assumes a straight ray / small offset:

$$
V_\text{rms}^2 = \frac{\sum_i v_i^2 \Delta t_i}{\sum_i \Delta t_i}.
$$

As a function of vertical traveltime:

$$
V_\text{rms}^2(\tau) = \frac{1}{\tau} \int_0^\tau v^2(\tau') \, d\tau'.
$$

**NMO velocity** — velocity that makes the reflection traveltime hyperbolic:

$$
t^2(x) = t_0^2 + \frac{x^2}{V_\text{nmo}^2}.
$$

**Stacking velocity** — velocity that best flattens the gather for stack. For flat horizontal layers it is close to the NMO velocity.

## Relations

For the same layered medium, $V_\text{rms} \ge V_\text{avg}$ (Schwartz inequality). Interval velocity can be estimated from RMS velocities with the Dix formula:

$$
v_\text{int}^2 = \frac{V_\text{rms,2}^2 t_2 - V_\text{rms,1}^2 t_1}{t_2 - t_1}.
$$

Margrave stresses that the Dix result must be physically plausible: the interval-velocity squared must be positive, which constrains how fast $V_\text{rms}$ can decrease with time. Noisy or invalid $V_\text{rms}$ estimates can produce imaginary or otherwise unphysical interval velocities.

## Vertical traveltime and instantaneous velocity

Margrave defines vertical traveltime as

$$
\tau(z) = \int_0^z \frac{dz'}{v(z')},
\qquad
z(\tau) = \int_0^\tau v(\tau') \, d\tau'.
$$

For a linear $v(z) = v_0 + c z$ medium, the instantaneous velocity as a function of vertical traveltime is exponential:

$$
v(\tau) = v_0 e^{c \tau}.
$$

This is a useful sanity check: a small velocity gradient with depth produces a large exponential variation with time, so velocity analysis must be performed in fine time gates.

## Relation to lecture notes

Core topic in [Term 1 Lecture 03 — Kinematics, Velocities and Field Statics](../lecture_ready/term01_lec03_kinematics_and_field_statics.md).
