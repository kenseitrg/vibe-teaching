---
title: Inverse Q filtering (absorption compensation)
status: draft
sources:
  - wang_2002_stable_inverse_q
  - wang_2006_inverse_q_resolution
  - futterman_1962_dispersive_body_waves
  - paradigm_qapp_qest
tags: [inverse-q, q-compensation, nonstationary-filtering, stabilization, gain-limit, reference-frequency, downward-continuation]
---

# Inverse Q filtering (absorption compensation)

**Inverse Q filtering** removes (part of) the earth's absorption filter from seismic data: it boosts the attenuated high frequencies and undoes the dispersion phase, restoring bandwidth and wavelet compactness at depth. Because absorption is time-varying, the operator is a **nonstationary filter** — effectively a different filter at each record time.

## Forward model (earth Q filter)

One-way propagation for traveltime $t$ in a constant-Q medium:

$$U(t,\omega) = U(0,\omega)\,\exp\Big(-\frac{\omega t}{2Q}\Big)\,\exp\big(i\phi(\omega,t)\big)$$

with the dispersion phase $\phi$ fixed by the causal model ([Futterman](velocity_dispersion.md) or Kjartansson power law). The recorded trace is reflectivity filtered by a *time-varying* version of this operator — deeper reflections are weaker, lower-frequency and more stretched.

## Two classical routes

- **Futterman's approach**: dispersion is the Hilbert-transform dual of attenuation; correct the phase exactly. Phase-only correction (Hargreaves & Calvert 1991 made it a fast Stolt-style operation) is **unconditionally stable** — it fixes timing and stretching but not the lost amplitudes.
- **Wang's approach (2002, 2006)**: inverse Q filtering as **wavefield downward continuation** (reverse propagation); compensates amplitude **and** phase. The amplitude operator $\exp(+\omega t/2Q)$ grows exponentially in frequency and time → **numerically unstable** even on noise-free data (boosts whatever noise floor exists once signal has decayed below it) → requires **stabilization**.

## Stabilization and the gain limit

- Stabilized amplitude operator (Wang 2006): $\Lambda = (\Lambda_a + \sigma^2)/(\Lambda_a^2 + \sigma^2)$ — equals the exact inverse where the signal survives, tapers gracefully where it has died
- User-facing form: **maximum amplitude boost in dB** (gain limit, e.g. MAXDB-style parameters); empirical link $\sigma^2 = \exp(-(0.23\,G_\lim + 1.63))$ (10–100 dB)
- Trade-off: higher gain limit → more resolution but more amplified noise; QC with spectra and difference panels
- Phase operator needs no stabilization

## Practical parameters

- **Reference frequency**: dispersion laws give velocity *relative to* $f_\text{ref}$; the operator anchors the wavelet there. Choice affects event timing — important for well ties and 4D. A high reference moves events earlier; the dominant-frequency anchor keeps picks stable.
- **Q model**: constant, effective time-varying, or interval Q; variable Q(τ) handled by continuation through layers or continuous integration (Gabor-domain implementation)
- **Compensation modes**: phase-only (safe, stable — when amplitudes must be preserved for AVO or data are noisy), amplitude-only (rare), amplitude+phase (full inverse Q — resolution enhancement)
- Typical position: after geometric-spreading correction, before/with deconvolution (Q-compensation makes the wavelet more stationary, helping decon); modern imaging compensates Q inside migration using Q from tomography

## Relation to lecture notes

Term 2 Lecture 01, Sections 5–6.

## Related concepts

- [Seismic absorption](seismic_absorption.md)
- [Velocity dispersion](velocity_dispersion.md)
- [Models of Q](q_models.md)
- [Q estimation](q_estimation.md)
- [Spherical divergence](spherical_divergence.md)
- [Deconvolution](deconvolution.md)
