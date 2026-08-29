---
title: Seismic absorption (anelastic attenuation)
status: draft
sources:
  - futterman_1962_dispersive_body_waves
  - kjartansson_1979_constant_q
  - paradigm_qapp_qest
tags: [absorption, quality-factor, attenuation, high-frequency-loss, anelastic]
---

# Seismic absorption (anelastic attenuation)

**Absorption** (intrinsic or anelastic attenuation) is the conversion of elastic wave energy into heat as a seismic wave propagates through rock. It is distinct from **scattering attenuation** (energy redistributed by heterogeneities), though the two are difficult to separate in recorded data and are usually treated together as apparent attenuation.

## Physical mechanisms

- Grain-boundary friction and relative motion of rock grains (loss per oscillation cycle)
- Viscous pore-fluid flow ("squirt flow") between cracks and pores of different compliance
- Fluid relaxation and thermal effects

Key experimental observation: for most consolidated rocks, the **fractional energy loss per cycle is nearly frequency-independent** over the seismic band. Since higher frequencies complete more cycles per second (and per metre), they lose energy faster — the physical origin of the "high frequencies die first" rule.

## Definition of Q

The **quality factor** $Q$ quantifies absorption via the energy lost per cycle:

$$Q = 2\pi\,\frac{E}{\Delta E} \qquad \text{or} \qquad Q^{-1} = \frac{1}{2\pi}\frac{\Delta E}{E}$$

where $E$ is the (maximum or mean) stored energy and $\Delta E$ the loss per cycle. For a linear medium $Q^{-1}$ equals $\tan\phi$, the loss tangent between stress and strain.

Amplitude form over traveltime $t$ (constant Q):

$$A(\omega, t) = A_0(\omega)\,\exp\!\Big(-\frac{\omega t}{2Q}\Big), \qquad \alpha(\omega) = \frac{\omega}{2Qv} \;\; (\text{decay} \propto e^{-\alpha x})$$

Typical values: unconsolidated near-surface Q ≈ 10–30; consolidated sediments Q ≈ 50–150; carbonates/evaporites Q > 150. Q ≈ ∞ means lossless.

## Consequences for seismic data

- **Loss of high-frequency content** with traveltime — the amplitude spectrum shifts toward low frequencies; deep events are low-frequency and lower-resolution
- **Wavelet stretching and delay** — dispersion (a necessary companion of absorption for a causal linear earth) makes low frequencies travel slower; see [velocity dispersion](velocity_dispersion.md)
- Nonstationarity: the effective wavelet changes with record time — ordinary stationary deconvolution cannot remove this; it requires nonstationary [inverse Q filtering](inverse_q_filtering.md) or Q-compensating imaging
- Combined with spherical divergence, absorption is the main reason deep amplitudes are many orders of magnitude weaker than shallow ones — but unlike divergence, absorption is **frequency-selective** and only partly recoverable (noise, stabilization limits)

## Apparent vs intrinsic Q

What we estimate from data (VSP, surface seismic) is an **effective/apparent Q** along the propagation path, mixing intrinsic absorption with scattering, intrabed multiples and other losses. Interval Q (layer-stripped) and effective Q relate much like interval and RMS velocities.

## Relation to lecture notes

Term 1 Lecture 02 introduces absorption qualitatively; Term 2 Lecture 01 develops the mechanism, Q definitions and consequences in full.

## Related concepts

- [Velocity dispersion](velocity_dispersion.md)
- [Models of Q](q_models.md)
- [Inverse Q filtering](inverse_q_filtering.md)
- [Spherical divergence](spherical_divergence.md)
