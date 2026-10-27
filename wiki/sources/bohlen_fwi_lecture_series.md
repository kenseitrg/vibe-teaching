---
title: "Bohlen (WS 2021/22) — Full Waveform Inversion lecture series, KIT"
status: draft
type: course
source_file: wiki/sources/_raw_text/FWI_Lecture_2.txt
language: en
concepts:
  - full_waveform_inversion
tags: [fwi, course, adjoint-state, born-approximation, elastic, source-inversion, applications]
---

# Bohlen — Full Waveform Inversion lecture series (KIT)

Thomas Bohlen, GEOPHYSICAL INSTITUTE, KARLSRUHE INSTITUTE OF TECHNOLOGY. WS 2021/22 course, ~10 lectures (PDFs in `papers/fwi/FWI_Lecture_*.pdf`).

## Overview

A complete university course on FWI, from theory (perturbation approach, Born approximation, adjoint-state gradients) to applications (body waves, surface waves, GPR). Mathematically deeper than our Term 3 Lecture 07, but its application lectures provide the conceptual figures and examples reused in our course.

## Key takeaways (per lecture, as used by us)

- **Lecture 2 — Gradient calculation:** perturbation/born-series derivation; the FWI procedure loop diagram (forward modelling → residual → adjoint back-propagation → gradient → update) reused as our workflow figure.
- **Lecture 4 — Applications of body waves:** FWI spans **9 orders of magnitude** in scale (medical imaging, NDT, near-surface, exploration, seismology) — reused as the "scales" figure; marine streamer top-salt case (Thiel 2018); OBC shallow-water case (Kunert 2015, Habelitz 2017) with data-fit panels at successive iterations/frequency bands (2–6, 2–10, 2–23 Hz) — reused for frequency continuation; synthetic acoustic-vs-elastic reconstruction test showing acoustic FWI fails where elastic physics dominate ("Elastic Modelling/FWI is necessary") — reused for the elastic-effects challenge.
- **Lecture 5 — Source time function & geometrical spreading:** source signature estimated by deconvolution/correlation with the modelled Green's function (source wavelet correction filter); geometrical-spreading correction of the gradient.
- **Lecture 6 — Multiparameter elastic FWI:** elastic gradients via adjoint method; parameter classes (Vp, Vs, density); **parameter cross-talk** as a key multiparameter difficulty; Marmousi-II examples.
- **Lecture 7–9:** surface-wave FWI, 3D 9C shallow FWI, GPR FWI (not used).

## Relation to lecture notes

Term 3 Lecture 07: workflow figure (Lec 2, slide 4), scales figure (Lec 4, slide 4), data-fit evolution (Lec 4, slide 28, after Habelitz 2017), acoustic-vs-elastic comparison (Lec 4, slide 10, after Thiel 2018).

## Related sources

- [Tarantola (1984)](tarantola1984_inversion_acoustic.md) — theoretical foundation of the adjoint gradient.
- [Keating & Innanen (2016)](keating2016_anacoustic_fwi.md) — anacoustic (attenuation) FWI hazards.
