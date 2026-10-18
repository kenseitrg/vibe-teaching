---
title: FK filtering
status: draft
sources:
  - cgg_odt02_denoise
  - margrave_2006_methods_of_seismic_data_processing
  - gower_2003_intouch_taup
tags: [fk, filtering, dip-filter, fan-filter, noise-attenuation, anti-alias]
---

# FK filtering

Filtering by multiplication with a designed 2-D amplitude mask in the FK domain: forward 2-D FFT → multiply mask → inverse FFT. The 2-D extension of 1-D [frequency filtering](frequency_filtering.md).

## Standard mask types

1. **K-filter (anti-alias cut)** — zero |k| beyond a fraction of $k_N = 1/(2\Delta x)$; spatial analog of a temporal low-pass. Used before trace decimation and to cut already-aliased noise.
2. **Dip / velocity filter** — pass or reject a **fan** of slopes |p| < p_max through the origin; separates steep linear noise (ground roll, air blast) from the reflection fan.
3. **Dip-reject, narrow slope band** — surgical removal of one noise cone at a known apparent velocity.
4. **Polygonal filter** — arbitrary polygon combining dip and frequency limits; the practical general form (e.g. reject the ground-roll cone only below 30 Hz).

Design rules: soft **tapers** on all zone edges (2-D Gibbs ringing wraps around the gather frame); protect low frequencies (a naive fan through the origin removes the low-f energy inside the cone — a broadband-processing concern); QC with before/after/**difference** panels and their FK spectra — the difference must look like the noise model. Amplitude-preserving workflows prefer transform-and-subtract over zero-out.

## Relation to tau-p

A fan reject in FK ≡ a p-band reject in f–p ≡ a p-mute in [tau-p](radon_transform.md) — one transform in two coordinate systems (k = p·f). See [Radon transform](radon_transform.md) and [Rho filter](rho_filter.md).
