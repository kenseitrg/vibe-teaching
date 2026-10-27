---
title: "Keating & Innanen (2016) — Anacoustic FWI: implementation and challenges"
status: draft
type: report
source_file: wiki/sources/_raw_text/CRR201634.txt
language: en
concepts:
  - full_waveform_inversion
tags: [fwi, attenuation, q, dispersion, multiparameter, cross-talk]
---

# Keating & Innanen (2016) — Anacoustic FWI: Implementation and challenges

CREWES RESEARCH REPORT — VOLUME 28 (2016). University of Calgary.

## Overview

A report on the specific difficulties of including **attenuation** (Q) in FWI — "anacoustic" FWI — as a multiparameter problem. Framed around hazards: naive reuse of single-parameter FWI strategies (optimization, regularization, frequency-band updating) fails when Q is an unknown.

## Key takeaways

- Why go beyond acoustic single-parameter FWI: real data contain elastic, anisotropic and attenuative effects; a model with wrong physics may fit the data better than the true model fits — a genuine concern for a misfit-minimizing method.
- **Attenuation cannot be inverted without dispersion:** Hak & Mulder (2011) — without causal (physically required) dispersion, velocity and attenuation models are ambiguous.
- Multiparameter coupling creates **cross-talk**: updates for $v$ leak into $Q$ and vice versa; parameterization, scaling and step-length strategies must account for it.
- Frequency-band continuation strategies designed for velocity can behave differently when Q is involved (amplitude vs phase roles of the two parameter classes).

## Relation to lecture notes

Term 3 Lecture 07 §4 (absorption challenge, multiparameter cross-talk).

## Related sources

- [Bohlen FWI Lecture 6](bohlen_fwi_lecture_series.md) — parameter cross-talk in elastic FWI.
- [Pratt (1999)](pratt1999_frequency_domain_fwi.md) — wrong-Q artifacts in the scale-model experiment.
