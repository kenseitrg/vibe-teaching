---
title: Seismic data sorting domains / gathers
status: draft
sources:
  - cgg_odt01_data_analysis_part1
  - cgg_odt01_data_analysis_part2
  - hill_ruger_2020_illustrated_seismic_processing_preimaging
tags: [gather, sort, shot, receiver, cmp, offset, domain]
---

# Seismic data sorting domains / gathers

A **gather** is a group of traces that share one or more common attributes. Changing the sort order puts the same data into different domains, which is a powerful processing and QC tool.

## Common 2D gathers

| Gather | Definition | Typical use |
|--------|------------|-------------|
| **Shot gather** (ОПВ) | Traces from the same shot | Noise attenuation, interpolation, QC of direct arrival and first breaks |
| **Receiver gather** (ОПП) | Traces recorded at the same surface receiver location | Noise attenuation, shot interpolation; note trace spacing equals shot spacing |
| **CMP gather** (ОСТ) | Traces with the same midpoint | Stacking, velocity analysis, NMO/demultiple |
| **Common offset / offset plane** | Traces with the same or similar offset | Common-offset migration, regularization, denoising |
| **Common channel** | Traces with the same channel number on one subsurface line | Single-offset processing, shot interpolation |

## Choosing a domain

- Use **shot gathers** when all traces were recorded at the same time and therefore share noise character.
- Use **receiver gathers** when noise is coherent in the shot domain but can be randomized by re-sorting.
- Use **CMP gathers** when you want to minimize structure and exploit moveout.
- Use **offset planes** when you need a single-fold volume for migration or interpolation.

## Spatial sampling in each domain

The natural trace spacing is different in each domain:

- **Shot gather**: receiver spacing.
- **Receiver gather**: shot spacing.
- **CMP gather**: moveup distance (often much smaller than shot spacing).
- **Common channel / offset plane**: shot spacing along the line.

This affects whether a given event is spatially aliased in that domain.

## 3D considerations

In 3D, sorting also includes inline and crossline:

- **Inline/crossline sort**: the natural 3D volume organization.
- **Offset vector tile (OVT)**: groups traces with similar inline and crossline offset components.
- **Cross-spread gather**: a 3D gather of traces from one source line and one receiver line.

These 3D sorts are covered in Term 3.

## Sources

- CGG ODT01 Data Analysis Part 1, §§5–6.
- CGG ODT01 Data Analysis Part 2, §§7–8.
- Hill & Rüger (2020), *Illustrated Seismic Processing, Vol. 2*, Appendix A.
