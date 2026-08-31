---
title: Vermeer (2012) — 3D Seismic Survey Design, Second Edition
status: draft
type: textbook
source_file: papers/general/Gijs J. O. Vermeer - 3D Seismic Survey Design, Second Edition.pdf
language: en
pages: 333
concepts:
  - seismic_acquisition
  - 3d_seismic_acquisition
  - common_midpoint
  - seismic_data_sorts
  - cross_spread_gather
  - ovt_cov_panels
  - grid_binning
  - seismic_data_processing
tags: [acquisition, survey-design, geometry, symmetric-sampling, 2d, 3d, fold, offset, textbook]
---

# Vermeer (2012) — 3D Seismic Survey Design

SEG Geophysical References Series No. 12, second edition. A definitive reference on seismic acquisition geometry, connecting survey design to imaging and processing.

## Relevant chapters / sections for Term 1 Lecture 1

| Section | Book pages | Topic |
|---------|-----------|-------|
| Introduction | xxi–xxv | Historical context; 2D vs 3D; continuous wavefield; minimal data sets; overview of chapters |
| Chapter 1 | 1–13 | 2D symmetric sampling: shot/receiver and midpoint/offset coordinates, fold, stack response |
| Chapter 2 (start) | 15–40 | 3D geometries, continuous wavefield, 3D subsets, fold in 3D, binning, unit cell, aspect ratios |
| Chapter 3 (start) | 59–76 | Noise suppression: direct/scattered waves, arrays, stack responses |

## Key takeaways

### 2D symmetric sampling
- A 2D seismic line samples a **3D wavefield**: time $t$, shot coordinate $x_s$, receiver coordinate $x_r$.
- Equivalently, it can be described by **midpoint** $x_m$ and **offset** $h$: offset is a third dimension that must be sampled.
- **Symmetric sampling**: shot and receiver sampling requirements are identical (a corollary of reciprocity).
- Proper sampling of the desired wavefield determines station intervals; arrays may be added to suppress aliased low-velocity noise.

### Coordinate systems
- Shot–receiver coordinates: natural acquisition description.
- Midpoint–offset coordinates: natural for CMP stacking and velocity analysis.
- Both descriptions are equivalent, but each highlights different processing steps.

### Fold and stack response
- Fold is the number of traces per CMP bin; it can also be understood as the number of overlapping basic subsets (minimal data sets).
- The **stack response** describes how effectively stacking suppresses noise and multiples as a function of dip/velocity.
- Wide geometries generally have better stack response than narrow geometries with the same nominal fold.

### From 2D to 3D
- 3D acquisition samples a **5D prestack wavefield** (two shot coordinates, two receiver coordinates, time).
- Not all four spatial coordinates can be densely sampled; geometry design chooses which coordinates to sample well and which to leave coarse.
- Common 3D geometries: **orthogonal**, **parallel**, **areal**.
- The **cross-spread** (orthogonal geometry) and **common-receiver gather** (areal geometry) are examples of minimal data sets.

### Spatial sampling concepts
- **Binning**: grouping midpoints into regular cells.
- **Unit cell**: the area determined by the two coarsest sampling intervals; controls geometry sparsity.
- **Aspect ratios**: for bin size, unit cell, and maximum offset; symmetric sampling aims for aspect ratios near one.
- **Spatial continuity**: smoother acquisition lines and smaller unit cells reduce migration artifacts.

## Figures useful for teaching
- Figure 1.1–1.3: 2D symmetric sampling, coordinate systems, fold build-up.
- Figure 1.4–1.5: symmetric vs asymmetric sampling and stack response.
- Figure 2.1–2.6: 3D geometry classes and their basic subsets.
- Figure 2.7–2.10: midpoint/offset coordinate systems and 3D subsets of the 5D wavefield.
- Figure 2.11–2.14: binning, unit cell, aspect ratios.
- Figure 3.1–3.3: direct waves, scattered waves, and array responses.
## Relation to lecture notes

- Provides the geometric foundation for Term 1 Lecture 1: why offset is a dimension, how fold arises, and what acquisition parameters matter.
- Chapter 2 (sections 2.2–2.5) is the main reference for Term 3 Lecture 1, covering 3D geometry classes, the continuous wavefield, 3D subsets, fold, the unit cell, binning, aspect ratios, and OVT/COV panels.
- The 2D symmetric sampling chapter is especially suitable for an undergraduate introduction before moving to 3D in Term 3.
- The figures in this book are excellent for slide and note illustrations.

## Source

Vermeer, G. J. O. (2012). *3D Seismic Survey Design*, 2nd ed. SEG Geophysical References Series No. 12.
