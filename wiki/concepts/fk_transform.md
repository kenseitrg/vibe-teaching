---
title: FK transform
status: draft
sources:
  - margrave_2006_methods_of_seismic_data_processing
  - yilmaz_2001_seismic_data_analysis_taup
  - cgg_odt02_denoise
tags: [fk, fourier, wavenumber, apparent-velocity, aliasing, transform]
---

# FK transform

The 2-D Fourier (frequency–wavenumber) transform decomposes a seismic gather into plane waves:

$$D(f, k) = \iint d(t, x)\, e^{-i 2\pi (f t + k x)}\, dt\, dx$$

Each point (f, k) is a plane-wave component: temporal frequency f and spatial frequency (wavenumber) k.

## Slope relation

A linear event $d(t,x) = s(t - p x)$ has all its energy on the **radial line** $k = p f$ through the origin:

$$p = \frac{dt}{dx} = \frac{k}{f}, \qquad V_\text{app} = \frac{1}{p} = \frac{f}{k}$$

- Horizontal events in (x, t) are vertical lines in (k, f) and vice versa.
- All events with the same apparent velocity collect onto one radial line (distinguished by phase).
- A hyperbola is locally linear: its tangent segments sweep a fan of slopes → **fan-shaped (triangular) region** in FK between the near-offset slope and p = 1/V.
- Discrete forward/backward DFT are exact inverses of each other.

## Spatial aliasing

Spatial sampling at trace spacing Δx permits wavenumbers only up to the spatial Nyquist $k_N = 1/(2\Delta x)$ (0.5 cycles/trace). An event with apparent velocity $V_\text{app}$ aliases above

$$f_\text{alias} = \frac{V_\text{app}}{2 \Delta x}$$

Aliased energy wraps around ±k_N and appears at reflection-like dips. Unlike temporal aliasing (removed by analog filters before digitization), spatial aliasing is essentially always present to some degree.

## Uses

- Dip/velocity filtering (see [FK filtering](fk_filtering.md)), noise attenuation, migration (f-k methods), interpolation.
- The [Radon transform](radon_transform.md) is the same information in polar coordinates of the FK plane (projection-slice theorem).
