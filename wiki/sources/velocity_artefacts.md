---
title: Velocity Artifacts from Near-Surface Errors
status: draft
source_type: paper
authors: Aleksey V. Novokreschin, Dmitry S. Rakivnenko, Yana A. Ignatieva, Ilya V. Musatov, Ilfat I. Karimov
year: 2021
url: https://doi.org/10.31660/0445-0108-2021-5-69-84
lectures:
  - term03_lec02
related_concepts:
  - static_corrections
  - velocity_analysis
  - migration_datum
  - near_surface_velocity_model
tags: [velocity, floating-datum, statics, artifacts, near-surface]
---

# Velocity Artifacts from Near-Surface Errors

Novokreschin, A. V., Rakivnenko, D. S., Ignatieva, Y. A., Musatov, I. V., and Karimov, I. I., 2021, "Effective velocities artifacts caused by floating datum and compensation methods," *Neft i Gaz*, 5, 69–84.

## Main message

Processing from a floating datum is standard practice, but the curvature of the floating surface itself biases effective-velocity estimates. The paper quantifies the bias and proposes a simple, flow-compatible remedy.

## Key points

- When data are redatumed to a floating surface, the CMP reflection traveltime contains extra terms from the source and receiver elevations relative to the local datum.
- A Taylor expansion of the floating surface around the CMP shows that the **quadratic curvature term** (second derivative) is the dominant source of velocity error; the linear gradient term has no effect on velocity estimation.
- A 1D model with only 6 m of elevation variation across a 2000 m aperture produces a 6.8% error (≈160 m/s) in effective velocity.
- The bias is larger for deeper horizons (larger velocities) and can produce false structural anomalies.
- In 3D, the elevation difference between source and receiver azimuths can create an apparent **HTI anisotropy** in kinematic analysis (snail-gather wobbling) even when the medium is isotropic.

## Proposed remedy

- Bring all sources and receivers within one CMP to a **locally constant level** (equal to the floating-datum value at the CMP) by applying a small static correction before velocity analysis.
- This keeps the moveout hyperbolic and makes the effective velocity correspond to the average velocity to the reflector.
- Alternatively, compute velocities directly from the topographic surface using a double-square-root (DSR)-like traveltime formula; this avoids datum-related statics altogether but requires software support.

## Tests

- 1D, 2D, and 3D synthetic models confirm the theory.
- Real-data tests show that the locally constant level reduces structural distortion and the apparent HTI effect.
- Depth maps built from corrected velocities match the model far better than those built from raw floating-datum velocities.

## Relation to lecture notes

Supports Term 3 Lecture 2: how inaccurate near-surface / datum handling creates velocity and structural artifacts, and why floating-datum processing must be done carefully before imaging.

## Related concepts

- [Static corrections](../concepts/static_corrections.md)
- [Velocity analysis](../concepts/velocity_analysis.md)
- [Migration datum](../concepts/migration_datum.md)
- [Near-surface velocity model](../concepts/near_surface_velocity_model.md)
