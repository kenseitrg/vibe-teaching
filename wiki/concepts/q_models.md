---
title: Models of Q (attenuation laws)
status: draft
sources:
  - kjartansson_1979_constant_q
  - futterman_1962_dispersive_body_waves
tags: [q-models, constant-q, futterman, kjartansson, ricker, born, white, creep, attenuation-theories]
---

# Models of Q (attenuation laws)

A **model of Q** is a complete, causally consistent pair: an attenuation law $\alpha(\omega)$ **and** the dispersion law $v(\omega)$ implied by it. Compensation and forward modeling both need the pair — amplitude alone or phase alone is not a physical propagation law. Kjartansson (1979, Table 1) organizes the classical families:

## The four classical families

| Family | Linearity | $Q(f)$ | $v(f)$ | Creep $\psi(t)$ | Pulse broadening | Verdict |
|---|---|---|---|---|---|---|
| **Frictional** (Born 1941, White 1966, Knopoff 1964) | nonlinear (Q and velocity depend on amplitude) | independent of f | independent of f | none | distorted or acausal | matches loss-per-cycle observation but **nonlinear and acausal** — unusable for linear processing |
| **Voigt–Ricker** (viscous; Voigt 1892, Ricker 1953) | linear | $1/Q \propto \omega$ | independent at low f | $\propto e^{-at}$ | $\propto \sqrt{T}$ | linear and causal, gives the Ricker wavelet, but Q ∝ f **contradicts measurements** |
| **Kolsky–Futterman NCQ** (Kolsky 1956, Lomnitz 1957, Futterman 1962, Strick 1967) | linear | nearly constant in a band | $\propto 1 + \frac{1}{\pi Q}\ln(\omega/\omega_0)$ (logarithmic) | $\propto \ln(1+at)$ | $\propto T$ | causal, practical; needs low-frequency cutoff $\omega_0$; standard in processing software |
| **Kjartansson CQ** (1979) | linear | **exactly constant** | $= (\omega/\omega_r)^{\gamma}$, $\gamma = \frac{1}{\pi}\arctan\frac{1}{Q}$ | $\propto t^{\gamma}$ | $\propto T$ exactly (self-similar pulse) | two-parameter $(Q, v_r)$ completeness; no cutoff; basis of Wang's inverse Q filter |

## Why the constant-Q ideal matters

- Loss per cycle independent of frequency is the robust experimental observation in rocks
- Constant Q ⇒ attenuation and dispersion follow from just $(Q, v_r)$; pulse shape is self-similar and pulse width grows *exactly* linearly with traveltime (Kjartansson's scaling relations)
- For Q ≥ 30 over seismic bands, NCQ (logarithmic) and CQ (power) laws differ negligibly — model choice is less important than using a **causally consistent pair**

## Practical notes

- Processing software typically offers a Futterman-type dispersion operator and/or a Kjartansson/Wang power-law operator
- Physics and FWI use constant-Q via memory-variable (fractional Laplacian / rheology) formulations
- Forward "modeling mode" of Q filters uses the same laws to *add* absorption (e.g., for feasibility studies or matching)

## Relation to lecture notes

Term 2 Lecture 01, Section 4 (models of Q and their properties).

## Related concepts

- [Seismic absorption](seismic_absorption.md)
- [Velocity dispersion](velocity_dispersion.md)
- [Inverse Q filtering](inverse_q_filtering.md)
- [Seismic wavelet](seismic_wavelet.md) (Ricker wavelet origin)
