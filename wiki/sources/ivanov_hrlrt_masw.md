---
title: "Benefits of using the high-resolution linear Radon transform (HRLRT) with the multi-channel analysis of surface waves (MASW) method"
status: draft
source_type: conference abstract
authors: "Julian Ivanov, Richard D. Miller, Daniel Z. Feigenbaum, J. Tyler Schwenk"
year: 2017
url:
lectures:
  - term03_lec03
related_concepts:
  - surface_waves
  - surface_wave_dispersion
  - surface_wave_multimodality
  - surface_wave_inversion
  - fk_music_surface_waves
tags: [surface-waves, masw, radon-transform, hrlrt, multimodal-inversion]
---

# Benefits of using the HRLRT with the MASW method

Ivanov, J., Miller, R. D., Feigenbaum, D. Z., & Schwenk, J. T. (2017). *Benefits of using the high-resolution linear Radon transform (HRLRT) with the multi-channel analysis of surface waves (MASW) method*. SEG International Exposition and 87th Annual Meeting, Expanded Abstracts, 2647–2651.

## Main message

The conventional phase-shift method for imaging surface-wave dispersion can blur modes and truncate the usable frequency range. The high-resolution linear Radon transform (HRLRT) produces sharper dispersion images, which improves mode separation, passive-data processing, and the resolution of inverted S-wave models.

## The MASW workflow

- Record a single shot gather or passive record.
- Transform the shot gather into a dispersion image.
- Pick the dispersion curve(s) and invert to a 1D VS profile.
- Multiple 1D profiles can be assembled into 2D or 3D models.

## HRLRT vs. conventional phase-shift

- Synthetic 2-layer data: HRLRT shows sharper fundamental- and higher-mode trends and a better low-frequency fit.
- Garland, Michigan data: fundamental and higher modes were blended in the phase-shift image but clearly separated with HRLRT.
- Yuma, Arizona data: HRLRT extended the fundamental-mode frequency range from ~35 Hz to ~55 Hz, improving shallow resolution.

## Real-data examples

- Love-wave analysis at a Texas levee: HRLRT extended the fundamental mode from ~32 Hz to >50 Hz and allowed shorter receiver spreads while still separating the first higher mode.
- Multi-mode inversion with 20 layers gave a greater maximum depth (~10 m vs. ~8 m) and finer vertical detail than a 10-layer fundamental-mode inversion.
- Passive data: HRLRT revealed a clear 20–70 Hz fundamental-mode trend where the phase-shift method showed almost no coherent trend, even after stacking 64 records.

## Spectral leakage

- Conventional methods can produce fake trends (spectral leakage) that resemble real modes.
- HRLRT suppresses these artefacts, reducing the risk of misinterpreting aliasing as surface-wave energy.

## Relation to lecture notes

This source supports the discussion of how dispersion curves are measured and why high-resolution transforms are useful: they help separate modes and recover a wider frequency band, which is essential for reliable multi-mode inversion.

## Related concepts

- [Surface waves](../concepts/surface_waves.md)
- [Surface wave dispersion](../concepts/surface_wave_dispersion.md)
- [Surface wave multimodality](../concepts/surface_wave_multimodality.md)
- [Surface wave inversion](../concepts/surface_wave_inversion.md)
- [FK-MUSIC / array analysis](../concepts/fk_music_surface_waves.md)
