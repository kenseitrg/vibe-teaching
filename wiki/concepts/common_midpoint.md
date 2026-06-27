---
title: Common midpoint (CMP) gather and fold
status: draft
sources:
  - hill_ruger_2020_illustrated_seismic_processing_preimaging
  - cgg_odt01_data_analysis_part1
  - cgg_odt01_data_analysis_part2
  - vermeer_2012_3d_seismic_survey_design
tags: [cmp, cdp, fold, gather, stack, nmo]
---

# Common midpoint (CMP) gather and fold

A **CMP gather** is a collection of traces that share the same midpoint between source and receiver. It is the central organizing unit of 2D reflection processing.

## CMP vs CDP

- **CMP** (common midpoint): traces with the same source–receiver midpoint. This is always true by construction.
- **CDP** (common depth point): traces that reflect from the same subsurface point. This is only true for a horizontal reflector.
- With dip, the reflection point moves up-dip, so the traces share a midpoint but not a depth point. Use **CMP** as the general term.

## How a CMP gather is built

As the source moves along the line, each new shot illuminates a new strip of subsurface. Traces from different shots whose midpoints fall in the same CMP bin are collected together. The number of traces in a bin is the **fold** at that location.

## Why the CMP gather matters

1. **Structure is minimized**: all traces in a CMP gather reflect from nearly the same subsurface location, so structural effects are smaller than in a shot gather.
2. **Velocity information**: the change of arrival time with offset (normal moveout) is a function of velocity.
3. **Stacking**: after NMO correction, traces are summed to create one stacked trace. This improves signal-to-noise ratio by approximately $\sqrt{N}$ for $N$ uncorrelated random-noise traces.
4. **Multiple identification**: primaries and multiples have different NMO, so they separate in the CMP gather.

## Fold

**Fold** is the number of traces contributing to a CMP stack. It varies along the line:

- Maximum fold in the middle of the line.
- Decreasing fold at the start (**run-in**) and end (**run-out**) of the line.
- Irregular fold in 3D because of cable feather, line overlap, and skipped traces.

For a regular 2D marine geometry:

$$
\text{nominal fold} = \frac{\text{number of channels per streamer}}{\text{moveup}}
$$

where moveup is the number of new CMPs added per shot.

## CMP gather in the presence of dip

A dipping event appears on a CMP gather with extra moveout called **dip moveout (DMO)**. After NMO only, a dipping event is not flat; DMO or migration is needed to position it correctly.

Diffractions also appear in CMP gathers with a distinctive upward-curving shape.

## Sources

- Hill & Rüger (2020), *Illustrated Seismic Processing, Vol. 2*, Appendix A and Appendix B.
- CGG ODT01 Data Analysis Part 1, §6.
- CGG ODT01 Data Analysis Part 2, §§7–8.
