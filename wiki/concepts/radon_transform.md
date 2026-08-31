---
title: Radon transform
status: draft
sources:
  - trad2002_radon_interpolation
tags: [radon, tau-p, multiples, noise-attenuation, transform, interpolation]
---

# Radon transform

The Radon transform (τ–p transform) maps seismic data from the time–offset (or time–space) domain into a domain of intercept time τ and ray parameter / moveout parameter p. Coherent events that follow a known moveout curve collapse to focused points, which makes the transform a powerful tool for separation, filtering, and reconstruction.

## Variants by moveout assumption

The basis functions differ in the traveltime curve they assume:

- **Linear τ–p** — sums along straight lines; suits planar events / far-field arrivals.
- **Parabolic** — sums along parabolas; applied to **NMO-corrected** CMP gathers where primaries are nearly flat-with-residual-curvature. Computationally efficient (Zhou & Greenhalgh 1994).
- **Hyperbolic** — sums along true hyperbolas; best approximation of primaries at **large offsets**, but time-variant so it needs iterative solvers (Trad et al. 2002). See [Radon interpolation](radon_interpolation.md).

The transform can be implemented as a forward stacking operator plus an inverse, or as a least-squares inversion that produces a **high-resolution** (sparse, focused) model.

## Uses in the course

- **Multiple attenuation** — primaries and multiples separate in the τ–p domain because their moveout (curvature) differs; multiples can be muted and the data transformed back. Covered in Term 3 Lecture 04 (noise attenuation).
- **Noise attenuation** — coherent noise with a different apparent velocity/dip maps to a different region of the Radon domain.
- **Interpolation / regularization** — a sparse Radon model of a gappy CMP gather predicts the missing traces. See [Radon interpolation](radon_interpolation.md).

## Resolution and focusing

The Radon model is only useful if events focus tightly. Resolution depends on the aperture, the moveout assumption, and whether a sparseness constraint is applied. Maeland (1998) and Bickel (2000) analyse the focusing/impulse-response of the parabolic and hyperbolic transforms geometrically.

## Related concepts

- [Radon interpolation](radon_interpolation.md)
- [Predictive deconvolution](predictive_deconvolution.md)
- [Normal moveout](normal_moveout.md)
- [Seismic data regularization](seismic_data_regularization.md)

## Sources

- Trad, Ulrych & Sacchi (2002) — high-resolution time-variant hyperbolic/elliptical Radon transforms for interpolation.
- Zhou & Greenhalgh (1994), Maeland (1998), Bickel (2000) — Radon transform theory and focusing (in `papers/radon_taup/`).
