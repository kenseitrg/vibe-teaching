---
title: Hill & Rüger (2020) — Illustrated Seismic Processing, Volume 2: Preimaging
status: draft
type: textbook
source_file: papers/textbooks/Steve J Hill - Introduction to Seismic Processing.pdf
language: en
pages: 327
concepts:
  - seismic_data_processing
  - seismic_acquisition
  - common_midpoint
  - seismic_data_sorts
  - seismic_noise
  - seismic_multiples
  - spatial_aliasing
  - seismic_data_formats
tags: [seismic-processing, acquisition, cmp, geometry, noise, multiples, formats, textbook]
---

# Hill & Rüger (2020) — Illustrated Seismic Processing, Volume 2: Preimaging

SEG Course Notes Series No. 16. Aimed at novice processors, interpreters, and acquisition specialists. Emphasizes visual understanding and the consequences of processing decisions.

## Relevant chapters / sections for Term 1 Lecture 1

| Section | Book pages | Topic |
|---------|-----------|-------|
| Appendix A | 253–275 | Seismic acquisition: basic experiment, 2D/3D geometry, arrays, bins, source types, survey design |
| Appendix B | 277–298 | Signal-to-noise improvements: noise types, stack gain, refractions, ground roll, airwave, shot interference |
| Chapter 31 | 239–243 | Sample marine and land processing sequences |
| Chapter 32 | 245–247 | Visual processing summary exercise |

## Key takeaways

### Seismic processing as a sequence of problem-solving steps
- A processed image is the accumulation of many decisions; processing is both art and science.
- Each step has input requirements determined by the steps that follow it.
- The interpreter is a partner in many of these decisions.

### Acquisition essentials
- A seismic experiment sends elastic energy into the earth and records the returning wavefield.
- 2D geometry uses shot and receiver lines; the common-midpoint (CMP) location is halfway between source and receiver.
- 3D geometry bins midpoints into a regular grid of inline/crossline bins; fold varies because of cable feather, boat direction, and overlap.
- Arrays of sources/receivers attenuate unwanted energy by directivity.
- Source types differ between marine (airguns, etc.) and land (dynamite, vibroseis).

### CMP and fold
- The CMP gather groups traces with the same midpoint; for a horizontal reflector this is also the common depth point (CDP).
- Dip causes reflection points to move up-dip; the term CMP is more accurate than CDP in general.
- Stacking CMP traces improves signal-to-noise ratio and is still one of the most important imaging/denoising tools.

### Noise and multiples
- Noise can be random or coherent; coherent noise includes refractions, ground roll, airwaves, shot interference, and multiples.
- A multiple is energy with at least one downward reflection in its path.
- Noise removal often exploits a change of domain (e.g., shot to receiver, time to tau-p) to separate signal and noise.

### Sample processing sequences
- Marine and land sequences both include: geometry loading, noise attenuation, deconvolution, statics/NMO/velocity analysis, demultiple, migration, and post-migration conditioning.
- Order and emphasis differ because of acquisition environment and noise types.

## Figures useful for teaching
- Appendix A: 2D geometry schematic, CMP stacking diagrams, 3D bin geometry, array directivity, source-type comparisons.
- Appendix B: shot gathers showing ground roll, refractions, airwave, random noise, and stack-gain examples.
- Chapter 31: side-by-side marine and land processing flowcharts.

## Relation to lecture notes
- Provides the acquisition geometry and fold intuition for Term 1 Lecture 1.
- Gives concrete processing-flow examples that can be simplified for an undergraduate audience.
- Supports the signal/noise discussion and the idea that processing decisions affect the final image.
