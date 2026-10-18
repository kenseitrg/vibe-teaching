---
title: Rho filter
status: draft
sources:
  - margrave_2006_methods_of_seismic_data_processing
  - yilmaz_2001_seismic_data_analysis_taup
  - zhou_greenhalgh_1994_linear_parabolic_taup
tags: [radon, tau-p, rho-filter, inverse-transform, ramp-filter]
---

# Rho filter

The amplitude-restoring **ramp filter |f|** required in the inverse linear Radon (slant-stack) transform. Without it the adjoint inverse is a smeared, low-frequency-biased copy of the data.

## Where it comes from

Changing variables $k_x = p f$ in the inverse 2-D Fourier integral makes $dk_x = f\, dp$ appear — an extra factor of f multiplying the integrand (Margrave 2006, §§2-71–2-73):

$$\Psi(x,t) = \iint f\, \phi(p, f)\, e^{-2\pi i f p x} e^{2\pi i f t}\, dp\, df = \alpha(t) \cdot \int \varphi(p,\, t - px)\, dp$$

i.e. the **adjoint (inverse) slant stack followed by a convolution** whose spectrum is $|f|$ — filtered back projection. The same ramp appears in tomography (the λ-filter) and in the Kirchhoff migration integral (equivalent to differentiating the wavefield before summation).

## Practice

- Applied per trace: multiply the amplitude spectrum of each τ-p trace by |f| before the inverse transform.
- Fixes amplitude/waveform distortion; does **not** fix p-resolution limits from finite aperture and coarse Δp — for that, p-direction deconvolution (Zhou & Greenhalgh 1994) or least-squares / high-resolution Radon inversion is needed.
- Related: the |f| factor is the amplitude price of the non-area-preserving coordinate change between the FK and f–p domains (projection-slice theorem).
