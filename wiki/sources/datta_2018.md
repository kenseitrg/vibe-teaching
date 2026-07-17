---
title: "On the application of the f-k-MUSIC method to measurement of multimode surface wave phase velocity dispersion from receiver arrays"
status: draft
source_type: paper
authors: "Arjun Datta"
year: 2018
url: "https://doi.org/10.1007/s10950-018-9803-4"
lectures:
  - term03_lec03
related_concepts:
  - surface_wave_dispersion
  - surface_wave_multimodality
  - fk_music_surface_waves
tags: [surface-waves, dispersion, fk-music, beamforming, array-processing, multimode]
---

# On the application of the f-k-MUSIC method to measurement of multimode surface wave phase velocity dispersion from receiver arrays

Datta, A. (2018). *On the application of the f-k-MUSIC method to measurement of multimode surface wave phase velocity dispersion from receiver arrays*. Journal of Seismology, 22, 1993–2008. https://doi.org/10.1007/s10950-018-9803-4

## Main message

Array-based methods can recover multimode surface-wave dispersion. The paper reviews frequency-domain slant-stack, UC-diagram, and f-k-MUSIC methods, and concludes that f-k-MUSIC gives high-resolution spectra but is less effective than the UC-diagram technique for recovering higher modes.

## Frequency-domain slant-stack

- Stack the wavefield over receivers after applying a frequency-dependent phase shift for a trial wavenumber.
- Peaks in the stacked amplitude correspond to modal wavenumbers; sweeping over frequencies gives an f–c spectrum.
- Simple and fast, but resolution depends on array length.

## UC-diagram technique

- Narrow-band filter the data around a central frequency and approximate the wavenumber linearly using a trial group velocity.
- The diagram is plotted in group-velocity vs. phase-velocity space.
- It can simultaneously extract group and phase velocity and is the most robust of the three for higher modes.

## f-k-MUSIC

- MUSIC is an array signal-processing method that separates signal and noise subspaces.
- It produces a high-resolution f–k spectrum with fewer receivers than conventional 2D FFTs.
- The spectrum is interpolated from f–k to f–c for dispersion picking.
- Implementation here fixes the signal-subspace dimension rather than estimating it from eigenvalues.

## Synthetic tests

- Three different earthquake sources illuminate different parts of the multimode dispersion tree.
- Fundamental mode dominates at low frequencies; higher modes appear at higher frequencies.
- Windowing in the time domain can suppress the fundamental mode and enhance overtone extraction.
- Array length should be 3–4 times the longest wavelength; shorter arrays degrade all methods.
- Station spacing controls aliasing; large spacing can create artefacts that look like modes.
- Noise and lateral heterogeneity affect measured dispersion; scattering simply illuminates different parts of the dispersion tree.

## Real data example

- USArray Transportable Array data for teleseismic events.
- A 2–8 km/s group-velocity window recovers the fundamental mode; a 4–8 km/s window suppresses it to reveal overtones.
- Attributing the correct overtone number to each branch remains challenging.

## Relation to lecture notes

Datta is the source for the FK-MUSIC concept: it explains how high-resolution beamforming improves modal separation, why array geometry matters, and why multimode picking is still ambiguous.

## Related concepts

- [Surface wave dispersion](../concepts/surface_wave_dispersion.md)
- [Surface wave multimodality](../concepts/surface_wave_multimodality.md)
- [FK-MUSIC / array analysis](../concepts/fk_music_surface_waves.md)
