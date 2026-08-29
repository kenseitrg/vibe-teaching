---
title: "Kjartansson (1979) — Constant Q-Wave Propagation and Attenuation"
status: draft
type: paper
source_file: wiki/sources/_raw_text/Einar Kjartansson - Constant Qwave propagation and attenuation.txt
language: en
concepts:
  - q_models
  - seismic_absorption
  - velocity_dispersion
tags: [constant-q, creep, power-law, velocity-dispersion, attenuation-theories, pulse-broadening]
---

# Kjartansson (1979) — Constant Q-Wave Propagation and Attenuation

*Journal of Geophysical Research*, 84(B9), 4737–4748.

## Overview

Presents the **constant Q (CQ) model**: a linear, causal attenuation theory in which Q is *exactly* independent of frequency. Wave propagation is completely specified by two parameters — Q and a reference phase velocity $c_0$. The paper also organizes the classical attenuation theories into families (its Table 1 is a standard reference) and validates the constant-Q description against the Pierre shale field data of Ricker (1953) and McDonal et al. (1958).

## The Table 1 taxonomy of attenuation theories

| Property | Friction (Born, White) | Voigt–Ricker | NCQ (Kolsky, Futterman, Lomnitz, Strick) | CQ (this paper) |
|---|---|---|---|---|
| Linearity | Nonlinear (velocity and Q depend on amplitude) | Linear | Linear | Linear |
| Q(f) | Independent | $1/Q \propto \omega$ | Nearly independent in a band | Exactly independent |
| Phase velocity(f) | Independent | Independent at low f | $c/c_0 \approx 1 + (1/\pi Q)\ln(\omega/\omega_0)$ | $c/c_0 = (\omega/\omega_0)^{\gamma}$ |
| Transient creep | None | $\psi(t) \propto e^{-at}$ | $\psi(t) \propto 1 + (2/\pi Q)\ln(1+at)$ | $\psi(t) \propto t^{\gamma}$ |
| Pulse broadening | Distorted or acausal | $r \propto T^{1/2}$ | $r \propto T$ | $r \propto T$ |

- **Friction theories** (Born 1941; White 1966; Knopoff 1964): rate-independent friction matches the observed frequency-independent loss but is nonlinear and produces acausal/distorted responses.
- **Voigt–Ricker** (viscous damping): linear and causal, gives the Ricker wavelet, but Q grows linearly with frequency — contradicting measurements.
- **NCQ** (near-constant Q over a finite band; Kolsky 1956, Lomnitz 1957, Futterman 1962, Strick 1967): causal, logarithmic creep and dispersion — the practical basis of most processing implementations.
- **CQ**: exact, self-consistent for all frequencies.

## Constant Q construction

- Linear viscoelasticity via Boltzmann superposition: stress–strain related by convolution with causal relaxation/creep kernels; in the frequency domain a complex, frequency-dependent modulus $M(\omega)$ (correspondence principle).
- Q defined via the loss angle: $Q^{-1} = \tan\phi$ (phase between stress and strain); with mean-stored-energy definition $Q = 4\pi W / \Delta W$ (O'Connell & Budiansky).
- Power-law creep function $\psi(t) \propto t^{2\gamma}$ leads to a modulus with frequency-independent argument, hence **exactly constant Q**:

$$\frac{1}{Q} = \tan(\pi\gamma), \qquad \gamma = \frac{1}{\pi}\arctan\frac{1}{Q} \approx \frac{1}{\pi Q}$$

- Phase velocity: $c(\omega) = c_0\,|\omega/\omega_0|^{\gamma}$, where $c_0$ is the phase velocity at the arbitrary reference frequency $\omega_0$.
- Attenuation: $\alpha(\omega) = \tan(\pi\gamma/2)\,\omega/c(\omega)$ — nearly proportional to frequency (constant Q is *not exactly* α ∝ ω because c varies slightly).
- Complex-velocity notation $c_e = c_0 (i\omega/\omega_0)^{-\gamma}$ simplifies reflection coefficients and multi-dimensional modeling.

## Scaling relations (the elegant part)

- The impulse response is **self-similar**: $b(t, x) = t_x^{-1} b_0(t/t_x)$ — pulse shape is preserved while its width grows.
- Pulse width is *exactly* proportional to traveltime: $r = C(Q)\,T$, with $C(Q)$ nearly constant for $Q > 20$.
- Traveltime of a delta-source pulse grows as $x^{1/(1-\gamma)}$; amplitude decays as $t_x^{-1}$.
- Consequence: dispersion from anelasticity may be observed in the *time domain* (delay vs distance) more readily than in the frequency domain; the field data of Ricker and McDonal et al. in Pierre shale are fitted by constant Q (Q ≈ 30), overturning Ricker's own Voigt-solid interpretation (which requires Q ∝ f).

## Relation to lecture notes

Foundation for Term 2 Lecture 01, Section 4 (models of Q). The CQ power law $v(\omega)/v(\omega_r) = (\omega/\omega_r)^{\gamma}$ is the "Wang" velocity ratio used in inverse Q filtering; Table 1 structures the whole four-family comparison.

## Related sources

- [Futterman (1962)](futterman_1962_dispersive_body_waves.md) — NCQ dispersion from causality with low-frequency cutoff
- [Wang (2002)](wang_2002_stable_inverse_q.md), [Wang (2006)](wang_2006_inverse_q_resolution.md) — inverse Q filtering built on the CQ velocity law
