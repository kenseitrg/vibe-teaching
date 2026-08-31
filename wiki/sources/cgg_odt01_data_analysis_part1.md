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
  - normal_moveout
  - seismic_noise
  - seismic_multiples
  - amplitude_effects
  - spherical_divergence
  - automatic_gain_control
tags: [cgg, data-analysis, recorded-wavefield, shot-gather, cmp, qc, amplitude, attenuation, AGC, geometric-spreading]
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

### Attenuation (slide 47)
- Attenuation is a reduction in amplitude or energy caused by the transmitting medium or system.
- It includes geometric spreading (wavefront expansion), absorption (conversion of elastic energy to heat), transmissivity losses, and mode conversion.
- Absorption is frequency dependent; high frequencies are attenuated more than low frequencies.
- Difference between **amplitude recovery** (broader correction for all amplitude loss) and **spherical divergence correction** (correction for geometric spreading only).

### Shot gathers and the direct arrival
- The direct arrival has an apparent velocity equal to the near-surface/water velocity and should project to zero time at zero offset (a rough QC of start-of-data timing).
- Wavefront divergence is the amplitude decay purely from spreading; this is why divergence correction is applied (slide 65).
- As the wavefield enters deeper layers it is refracted and further attenuated by absorption and scattering (slide 66).

## Figures useful for teaching
- Slide sequence of modelled wavefield snapshots (direct arrival, first primary, multiple, refraction).
- Shot gather examples before/after NMO, with post-critical noise cone annotated.
- CMP gather examples showing multiples, diffractions, and anellipticity.
- Slide 47: attenuation definition (geometric spreading, absorption, transmissivity, mode conversion).
- Slides 65–66: direct arrival as a velocity QC and the physical origin of divergence correction.

## Relation to lecture notes
- Provides the “what do we record?” motivation for Term 1 Lecture 1.
- Gives concrete visual examples of shot gathers, CMP gathers, and wave propagation.
- Supports the NMO introduction in Term 1 Lecture 3.
- **Supports the physical amplitude-effects and spherical-divergence sections of Term 1 Lecture 2.**
