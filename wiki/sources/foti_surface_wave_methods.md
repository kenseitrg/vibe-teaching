---
title: "Application of Surface-Wave Methods for Seismic Site Characterization"
status: draft
source_type: paper
authors: "Sebastiano Foti, Stefano Parolai, Dario Albarello, Matteo Picozzi"
year: 2011
url: "https://doi.org/10.1007/s10712-011-9134-2"
lectures:
  - term03_lec03
related_concepts:
  - surface_waves
  - surface_wave_dispersion
  - surface_wave_multimodality
  - surface_wave_inversion
  - fk_music_surface_waves
tags: [surface-waves, masw, passive-seismic, inversion, site-characterization]
---

# Application of Surface-Wave Methods for Seismic Site Characterization

Foti, S., Parolai, S., Albarello, D., & Picozzi, M. (2011). *Application of Surface-Wave Methods for Seismic Site Characterization*. Surveys in Geophysics, 32, 777–825. https://doi.org/10.1007/s10712-011-9134-2

## Main message

Surface-wave methods use the frequency-dependent phase velocity of Rayleigh waves (geometric dispersion) in vertically heterogeneous media to infer shear-wave velocity profiles. The paper reviews acquisition, processing, and inversion strategies, with recommendations for both active and passive surveys.

## Surface wave dispersion

- Rayleigh-wave velocity is mainly controlled by the local S-wave velocity structure.
- High-frequency (short-wavelength) components sample shallow layers; low-frequency (long-wavelength) components sample deeper layers.
- The phase velocity vs. frequency curve is the **dispersion curve**.
- In real media several modes can propagate; the fundamental mode is not always dominant, especially in the presence of low-velocity layers or strong velocity contrasts.

## Active-source methods

- **SASW**: two-station method using cross-power spectrum phase; requires several geometries and phase unwrapping.
- **MASW**: multi-station linear array; transforms shot gathers into f–k, f–p, or phase-velocity images to pick dispersion curves.
- Acquisition design (source type, array length, spacing) must match the frequency band needed for the target depth.

## Passive-source methods

- **ReMi**: slant-stack analysis of ambient noise on linear arrays.
- **2D arrays**: f–k beamforming (BFM) and maximum likelihood (MLM) methods.
- **SPAC/ESAC**: azimuthal averaging of spatial autocorrelation.
- Passive surveys are rich in low frequencies and useful for deep characterization; single-station H/V spectral ratio can complement dispersion data.

## Inversion

- Forward modelling solves the modal eigenvalue problem for a layered, elastic medium.
- Higher modes and apparent dispersion must be accounted for, otherwise artifacts can appear.
- Local-search methods can get stuck; global search or combined strategies are preferable for complex sites.
- Joint inversion of dispersion and H/V curves reduces non-uniqueness.

## Recommendations and new perspectives

- Prefer multi-station methods over two-station SASW in noisy or complex settings.
- Avoid linear-array passive methods as the only source; use 2D arrays and combine active and passive data.
- Be aware of resolution limits and near-field effects.
- Seismic interferometry and surface-wave tomography are emerging tools for 2D/3D characterization.

## Relation to lecture notes

This paper provides the physics-to-practice bridge for the surface-wave lecture: it explains why surface waves are used as signal for near-surface characterization, how dispersion curves are measured, and how they are inverted to S-wave profiles.

## Related concepts

- [Surface waves](../concepts/surface_waves.md)
- [Surface wave dispersion](../concepts/surface_wave_dispersion.md)
- [Surface wave multimodality](../concepts/surface_wave_multimodality.md)
- [Surface wave inversion](../concepts/surface_wave_inversion.md)
- [FK-MUSIC / array analysis](../concepts/fk_music_surface_waves.md)
