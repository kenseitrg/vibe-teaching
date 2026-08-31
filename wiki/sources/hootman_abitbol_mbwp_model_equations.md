---
title: "Hootman & Abitbol - MBWP Model Equations"
status: reviewed
sources:
  - papers/deconvolution/MBWP Model Equations.pptx
tags: [MBWP, wavelet-model, Q, signal-to-noise, deconvolution, operator-design]
authors: [Bruce Hootman, Michael Abitbol]
date: 2008-05-30
type: technical-reference
---

# Hootman & Abitbol — MBWP Model Equations

## Overview

Technical reference documenting the mathematical model behind MBWP operator construction and parameter estimation. Defines the signal-to-noise equation and the model wavelet equations for each source type.

## Signal-to-Noise Equation

The S/N model used in parameter estimation:

$$k = k_s - k_n + k_p + \frac{Q_p - Q_{ave}}{f_0}$$

where:
- $k$ — signal-to-noise ratio (dB)
- $k_s$ — signal scalar (dB)
- $k_n$ — noise scalar (dB)
- $k_p$ — starting S/N ratio (dB)
- $f_0$ — frequency (Hz) at which S/N is measured
- $Q_p$ — starting Q value (s⁻¹)
- $Q_{ave}$ — average Q value after iterations (s⁻¹)

## Model Wavelet Equations by Source Type

### Buried Dynamite with Detector

$$M = S \cdot d \cdot Q \cdot g \cdot I$$

Signal model: source wavelet $S$ differentiated ($d$ = first derivative), filtered by absorption ($Q$), detector ($g$), and instrument ($I$).

### Surface Dynamite with Detector

Same structure as buried dynamite but the source radiation pattern differs (surface source has different near-field coupling).

### Airgun with Detector

$$M = F \cdot Q \cdot g \cdot I$$

where $F$ = far-field airgun signature (with ghost). No derivative operator for marine sources.

### Force Phase-Lock Vibroseis with Detector

$$M = S_w \cdot Q \cdot g \cdot I$$

where $S_w$ = sweep response. After correlation:

$$A = \text{Autocorrelation of filtered sweep}$$

### Base Plate Velocity-Lock Vibroseis with Detector

Same structure as force phase-lock but uses base plate velocity measurement instead.

### Vibroseis Sweep and Autocorrelation Relation

- If $A$ is input: converts to zero-phase → frequency domain → square root of amplitude → back to time domain
- If $(S_w * I)$ is input: simply computes autocorrelation
- Phase information is lost in the A path, but this is acceptable since it is only used as an autocorrelation later

## MBWP Operator Definition

Given:
- $X(t) = M(t) + k \cdot N(t)$ — resultant wavelet (model + scaled noise)
- $O(t)$ — spiking decon operator (inverse of model)
- $W(t) = O(t) * X(t)$ — MBWP operator (residual wavelet)
- $Z(t)$ — zero-phase wavelet embedded in data after MBWP application

The MBWP operator is defined as the residual between a spiking deconvolution operator and the model wavelet:

$$W(t) = O(t) * X(t)$$

where $O(t)$ is the inverse of the model wavelet $M(t)$.

## Time-Shifting

The resultant wavelet $X(t)$ is time-shifted to eliminate bulk delay:
1. Compute the amplitude envelope of $X(t)$
2. Find the time of peak amplitude
3. Apply time shift to place peak at zero time
4. Create $W(t)$ from the shifted wavelet

## Polarity Conventions

- **Geophone polarity:** Reversed from standard — so that MBWP application does not change the recording polarity
- **SEG convention:** A negative peak corresponds to an increase in acoustic impedance
- **Vibroseis:** Typically requires an additional −90° phase rotation to reach zero phase

## Output Wavelet Suite

The MBWP operator construction outputs the following wavelet suite:

| Trace | Name | Description |
|-------|------|-------------|
| 1 | INSTRUMENT_RESPONSE | Instrument impulse response |
| 2 | SWEEP_AUTOCORRELATION | (Vibroseis only) Sweep autocorrelation |
| 3 | GEOPHONE_RESPONSE | Detector impulse response |
| 4 | SIGNAL_AUTOCORRELATION | Signal model autocorrelation |
| 5 | ABSORPTION_RESPONSE | Q absorption wavelet |
| 6 | SIGNAL_MODEL | Signal model wavelet |
| 7 | SIGNAL_Q_AUTOCORRELATION | Signal Q autocorrelation |
| 8 | NOISE_MODEL | Noise model wavelet |
| 9 | NOISE_AUTOCORRELATION | Noise model autocorrelation |
| 10 | SIGNAL_PLUS_NOISE | Signal + noise resultant |
| 11 | DECON_OPERATOR | Spiking decon operator |
| 12 | DECON_SIGNAL_MODEL | Deconvolved signal model |
| 13 | MBWP operator | **MBWP operator** (residual wavelet) |
| 14 | MBWP_SIGNAL_MODEL | Signal model after MBWP |

**Key outputs for parameter estimation:** Traces 4 (signal autocorrelation) and 9 (noise autocorrelation).

**Key output for production:** Trace 13 (MBWP operator).

## Relevance to Course

- Provides the mathematical foundation for MBWP
- Shows how Q and S/N interact in the wavelet model
- Demonstrates why MBWP can correct non-minimum-phase effects
- Explains the operator design chain from model → decon → residual

## Related Wiki Pages

- [Brown et al. MBWP Update 2008](brown_et_al_mbwp_update_2008.md)
- [MBWP Step 1 — Initial Operator](mbwp_step1_initial_operator.md)
- [MBWP Step 2 — Estimating Parameters](mbwp_step2_estimating_parameters.md)
- [MBWP Step 3 — Final Operator](mbwp_step3_final_operator.md)
