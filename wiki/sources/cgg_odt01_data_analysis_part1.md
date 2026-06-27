---
title: CGG ODT01 — Data Analysis Part 1
status: draft
type: training slides
source_file: papers/general/ODT01A_DATA_ANALYSIS_PART1_v8.2.pptx
language: en
pages: ~80
concepts:
  - seismic_data_processing
  - seismic_acquisition
  - common_midpoint
  - seismic_data_sorts
  - seismic_noise
  - seismic_multiples
tags: [cgg, data-analysis, recorded-wavefield, shot-gather, cmp, qc]
---

# CGG ODT01 — Data Analysis Part 1

Internal CGG training slides on seismic data analysis: understanding what is recorded, basic geophysics, shot gathers, and the CMP domain.

## Covered topics

| Section | Content |
|---------|---------|
| §1 Introduction | What data analysis is; the role of QC and asking “what am I seeing?” |
| §2 What do we record? | Seismic records = primaries + noise + multiples + sampling/kinematic/dynamic/acquisition effects |
| §3 Basic geophysics | Diffractions, superposition, Huygens-Fresnel, reflection/transmission, Snell’s law, refractions, diving waves, attenuation |
| §4 Recorded wavefield | Forward-modelled wavefield snapshots; direct arrival, primaries, multiples, refractions, ghosts, guided waves |
| §5 Shot point domain | Shot gathers, normal moveout, post-critical energy, phase/polarity QC, direct arrival as velocity QC |
| §6 CMP domain/gather | CDP vs CMP, fold build-up, stacking, NMO, diffractions in CMP gathers, muting |

## Key takeaways

### What we record
- A shot gather is not a clean image: it contains primaries, multiples, diffractions, refractions, coherent noise, and random noise.
- The same event can be signal in one context and noise in another (e.g., refractions used for statics but removed before stacking).

### Kinematics and dynamics
- **Kinematic effects** change arrival times: statics, NMO, DMO, migration.
- **Dynamic effects** change amplitudes: attenuation, absorption, scattering, geometric spreading.
- **Acquisition effects** include instrument response, positioning, timing, and spatial sampling.

### Shot gathers
- The direct arrival has an apparent velocity equal to the near-surface/water velocity and should project to zero time at zero offset.
- NMO appears because receivers are at different offsets; off-end geometry biases the moveout dip.
- Post-critical energy, guided waves, and swell noise often dominate far offsets.

### CMP gathers
- CMP sorting groups traces with the same midpoint; for dipping reflectors the reflection point moves up-dip, so CDP ≠ CMP in general.
- The stack remains the most important tool for denoising and demultiple.
- NMO correction, muting, and velocity errors strongly influence what appears in the stack.

## Figures useful for teaching
- Slide sequence of modelled wavefield snapshots (direct arrival, first primary, multiple, refraction).
- Shot gather examples before/after NMO, with post-critical noise cone annotated.
- CMP gather examples showing multiples, diffractions, and anellipticity.

## Relation to lecture notes
- Provides the “what do we record?” motivation for Term 1 Lecture 1.
- Gives concrete visual examples of shot gathers, CMP gathers, and wave propagation.
