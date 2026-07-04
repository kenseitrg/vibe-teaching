---
title: Static corrections
status: draft
sources:
  - hutchinson_link_1984_surface_consistency
  - cgg_odt01_data_analysis_part1
  - noble_2020_whats_the_datum
  - jones_2012_incorporating_near_surface_velocity_anomalies
  - margrave_2006_methods_of_seismic_data_processing
  - li_1999_introduction_to_residual_statics_analysis
tags:
  - statics
  - near-surface
  - datum
---

# Static corrections

**Static corrections** are trace-constant time shifts that compensate for near-surface traveltime variations such as elevation changes and weathering-layer thickness/velocity anomalies.

Static corrections are widely used to reduce traveltime anomalies. The methods to estimate statics are often called statics analysis methods. Li (1999, Chapter 1) stresses that the most serious near-surface effect in processing is the traveltime anomaly, and that decades of practice show near-surface effects can be virtually corrected by estimating these traveltime anomalies. Field statics (elevation, refraction, uphole) correct the long-wavelength part; residual statics correct the short-wavelength remainder.

## Components

For land data, Jones (2012) decomposes near-surface statics into:

- **High spatial frequency (HF)** surface-consistent source and receiver components from rapid topography and rapid near-surface velocity variation.
- **Low spatial frequency (LF)** CMP-consistent component to move all traces in a CMP to a common flat processing datum at the CMP elevation.
- **Very high frequency (VHF)** jitter removed by residual statics.

## Key datums

- **Client datum**: final flat datum for delivery.
- **Intermediate datum**: often near the base of weathering.
- **Floating datum**: smoothed version of topography used during NMO/velocity analysis.
- **Final flat velocity datum**: for migration velocity model, often above the highest topography.

## Replacement velocity

The velocity used to replace the weathered layer when moving data to a datum. A low replacement velocity gives large statics; a high replacement velocity gives small statics. Margrave recommends choosing the datum as a smoothed version of the topography and the replacement velocity as an average near-surface velocity, then removing the mean shift so that the bulk static does not bias later processing.

## Vertical-ray approximation and replacement model

Margrave (Chapter 5) treats statics as an approximate **vertical-ray downward continuation** (or wave-equation datuming simplified to vertical paths). It strips the variable topography/weathering layer and replaces it with a smoother near-surface model defined by:

- $\delta t_s$ — source-side traveltime from shot to the base of the near surface (BNS).
- $\delta t_r$ — receiver-side traveltime from BNS to receiver.
- $e_\text{bns}$ — elevation of the BNS.
- $e_\text{dat}$ — elevation of the chosen datum.
- $V_\text{rep}$ — replacement velocity used to convert elevation differences to time shifts.

Because the correction assumes vertical raypaths through the near surface, it is only approximate for energy that actually travels slantingly. The vertical-ray assumption is physically reasonable because the strong velocity contrast at the base of the weathering layer forces rays to become nearly vertical in the low-velocity near surface. To keep NMO and migration from being distorted, the bulk (mean) static shift should be kept small; the mean is often removed and saved for a final shift to the interpretation datum.

After residual statics are estimated, the source and receiver components should be checked for geophysical consistency: in nearby locations they should usually have the same sign. The main exception is a buried source, where source and receiver statics may legitimately differ.

## Statics from uphole times

When buried impulsive sources are used, a near-surface receiver can measure the **uphole time** $t_\text{uh}$ from the shot depth to the surface. The shot-to-datum static is then:

$$
\delta t_s \approx \frac{e_s - d_s - e_\text{dat}}{V_\text{rep}}
$$

and the receiver static includes the uphole time:

$$
\delta t_r = t_\text{uh}(r) + \frac{e_s(r) - d_s(r) - e_\text{dat}}{V_\text{rep}}.
$$

In practice, shots sometimes lie inside the weathered layer, uphole picks are noisy, and shot spacing can be too sparse for reliable interpolation.

## Related concepts

- [Floating datum](floating_datum.md)
- [Residual statics](residual_statics.md)
- [Layer replacement](layer_replacement.md)

## Lectures

- [Term 1 Lecture 02 — Kinematics, Velocities and Field Statics](../lecture_ready/term01_lec02_kinematics_and_field_statics.md)
- [Term 1 Lecture 03 — Advanced Statics and the Link to Velocity Analysis](../lecture_ready/term01_lec03_advanced_statics_and_velocity_link.md)
