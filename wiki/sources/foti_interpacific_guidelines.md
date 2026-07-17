---
title: "Guidelines for the good practice of surface wave analysis: a product of the InterPACIFIC project"
status: draft
source_type: paper
authors: "Sebastiano Foti, Fabrice Hollender, Flora Garofalo, Dario Albarello, Michael Asten, Pierre-Yves Bard, Cesare Comina, Cécile Cornou, Brady Cox, Giuseppe Di Giulio, Thomas Forbriger, Koichi Hayashi, Enrico Lunedei, Antony Martin, Diego Mercerat, Matthias Ohrnberger, Valerio Poggi, Florence Renalier, Deborah Sicilia, Valentina Socco"
year: 2018
url: "https://doi.org/10.1007/s10518-017-0206-7"
lectures:
  - term03_lec03
related_concepts:
  - surface_waves
  - surface_wave_dispersion
  - surface_wave_multimodality
  - surface_wave_inversion
  - fk_music_surface_waves
tags: [surface-waves, masw, ambient-vibration, guidelines, vs30, inversion]
---

# Guidelines for the good practice of surface wave analysis: a product of the InterPACIFIC project

Foti, S., Hollender, F., Garofalo, F., Albarello, D., Asten, M., Bard, P.-Y., ... & Socco, V. (2018). *Guidelines for the good practice of surface wave analysis: a product of the InterPACIFIC project*. Bulletin of Earthquake Engineering, 16, 2367–2420. https://doi.org/10.1007/s10518-017-0206-7

## Main message

The InterPACIFIC guidelines give practical, step-by-step advice for acquiring, processing, and inverting surface-wave data. They emphasize that the interpretation is nonlinear and non-unique, and they target non-expert users while remaining useful as a general reference.

## Basic principles

- Surface waves are generated at a free boundary; Rayleigh waves have elliptical particle motion, Love waves are transverse.
- In vertically heterogeneous media, phase velocity depends on frequency (geometric dispersion).
- Higher modes exist above cut-off frequencies; energy distribution among modes depends on source, site, and frequency.
- Near-field effects bias phase velocities when receivers are too close to the source.
- Sharp lateral heterogeneity invalidates the 1D layered model; smooth 2D/3D variations can be approximated as locally 1D.

## Acquisition

- Active surveys typically use MASW (linear array) or SASW (two-station).
- Passive surveys should use 2D arrays when possible; linear arrays cannot determine wave propagation direction.
- For targets deeper than 20–25 m, combine active high-frequency data with passive low-frequency data.
- Common active source: 8 kg sledgehammer (high frequencies, limited depth); weight-drop or vibrator for lower frequencies.
- Geophone choice and sensor coupling matter; 4.5 Hz geophones are usually adequate for ~30 m targets.

## Processing

- Active data: transform from time-offset to f–k, f–p, or f–phase-velocity and pick maxima.
- Passive data: f–k beamforming or SPAC/ESAC/MSPAC.
- High-resolution methods (MUSIC, Capon, etc.) improve separation but can be unstable.
- Array aperture controls maximum wavelength and resolution; inter-receiver spacing controls minimum wavelength and aliasing.

## Inversion

- Parameterize the subsurface as homogeneous isotropic layers; thickness and VS are the most influential parameters.
- Fix or bound VP and density using a priori information (water table matters).
- Use the minimum number of layers that reproduces the data; test multiple parameterizations to assess epistemic uncertainty.
- Quantify uncertainty by reporting sets of equivalent solutions rather than a single best fit.

## Applications

- **VS,30** is the time-average S-wave velocity in the top 30 m, used for seismic site classification.
- Surface-wave profiles can be used in 1D ground-response analysis, but profiles should be checked against the measured dispersion curve and site resonance frequency.

## Relation to lecture notes

This guideline is the source for the practical workflow section of the lecture: it explains how to design a survey, what processing alternatives exist, and how to report uncertainty in the inverted S-wave profile.

## Related concepts

- [Surface waves](../concepts/surface_waves.md)
- [Surface wave dispersion](../concepts/surface_wave_dispersion.md)
- [Surface wave multimodality](../concepts/surface_wave_multimodality.md)
- [Surface wave inversion](../concepts/surface_wave_inversion.md)
- [FK-MUSIC / array analysis](../concepts/fk_music_surface_waves.md)
