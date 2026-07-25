---
title: "Hart & Hootman - MBWP Update 2008: Achieving Consistent and Stable Phase with Mixed-Source Surveys"
status: reviewed
sources:
  - papers/deconvolution/MBWP Update 2008.pptx
tags: [MBWP, mixed-source, wavelet-model, Q, signal-to-noise, VSP-validation, surface-consistent]
authors: [Douglas Hart, Bruce Hootman]
date: 2008-06-16
type: technical-paper
---

# Hart & Hootman — MBWP Update 2008

## Overview

Comprehensive presentation explaining the theoretical foundation of Model-Based Wavelet Processing (MBWP), its advantages over surface-consistent deconvolution (SCD), parameter estimation methodology, and validation with VSP data. Originally presented March 2001, edited June 2008. ©WesternGeco 2001.

## The Problem: Mixed-Source Surveys

**Challenges:**
- Vibroseis and dynamite sources in same survey
- Transition zone surveys
- Merging interpretations from multiple surveys
- Stratigraphic interpretation requires consistent phase

## The Convolutional Model

$$\text{Seismic Trace} = \text{Wavelet} * \text{Reflectivity} + \text{Noise}$$

**Goal:** Determine reflectivity from the seismic trace.

**Challenge:** One equation with two unknowns (wavelet and reflectivity), plus noise.

### Methods for Determining the Wavelet

1. Statistical techniques (phase unwrapping, decomposition)
2. Inversion approaches
3. Deterministic approaches (well-tie wavelet extraction)
4. Wavelet modeling
5. Surface-consistent deconvolution (SCD)
6. **Model-Based Wavelet Processing (MBWP)**

## Limitations of SCD

The surface-consistent deconvolution model:
$$\text{Wavelet} = \text{Source} * \text{Detector} * \text{Offset} * \text{Midpoint}$$

**Issues:**
- SCD partially addresses random noise by averaging spectra
- SCD does **not** address non-minimum-phase components of the wavelet
- SCD assumes minimum-phase wavelet — often violated

**MBWP addresses these limitations directly.**

## The MBWP Model

### Trace Model

$$\text{Seismic Trace} = [\text{Source} * Q * \text{Reflectivity} + \text{Noise}] * \text{Detector} * \text{Instrument}$$

Expanded:
$$= [\underbrace{\text{Source} * Q * \text{Detector} * \text{Instrument}}_{\text{Wavelet}} * \text{Reflectivity}] + [\underbrace{\text{Detector} * \text{Instrument} * \text{Noise}}_{\text{Noise term}}]$$

### Key Distinction: Assumptions NOT Made

Unlike conventional deconvolution, MBWP does **not** assume:
1. ~~Wavelet is minimum phase~~
2. ~~White reflectivity~~
3. ~~No noise~~

### Components of the Model Wavelet

$$\text{Wavelet} = \text{Source} * Q * \text{Detector} * \text{Instrument}$$

#### Source Models

**Vibroseis:**
- Sweep is proportional to applied force
- After crosscorrelation: Klauder wavelet (autocorrelation of sweep)
- Force is proportional to displacement

**Dynamite:**
- Buried source: applied force → derivative of step function
- Surface source: different radiation pattern

#### Absorption (Q)

- Exponential loss with frequency
- Characterized by effective Q parameter

#### Detectors and Instruments

- **Geophone response:** computed from natural frequency and damping, or measured from tap test
- **Hydrophone:** records pressure
- **Instrument response:** measured from pulse tests
- Geophones record particle velocity; sources apply displacement → first derivative needed

## Validating the Model

### VSP Experiment

- Geophone at depth (e.g., 1006 m)
- Sources: 0.22 kg explosive charge at 6.1 m depth + Vibroseis
- Compare model wavelets with VSP first-arrival data

**Result:** Model wavelets closely match VSP measurements for both dynamite and vibroseis sources.

## Modeling Predictive Deconvolution with MBWP

### Assumptions for the Model

- Reflectivity is white
- Noise is white

### Signal and Noise Autocorrelations

The autocorrelation that predictive deconvolution "sees" in the data is:

$$\phi_{xx} = \phi_{ss} + \phi_{nn}$$

This is **not** the spectrum of the wavelet — it's the spectrum of the autocorrelation, distorted by noise.

### Effect of S/N on the Minimum-Phase Wavelet

As S/N decreases:
- The autocorrelation becomes more noise-dominated
- The minimum-phase wavelet derived from the autocorrelation becomes distorted
- Phase errors increase

### The MBWP Solution

1. Build model wavelet from physical components:
   $$\text{Decon Op} * \text{Wavelet} = \text{Decon Op} * \text{Source} * Q * \text{Detector} * \text{Instrument}$$

2. Compute residual filter:
   $$\text{Residual} = \text{MBWP Operator} - \text{Decon Result}$$

3. Apply residual filter to correct deconvolution output:
   $$\text{Corrected} = \text{Decon Result} * \text{Residual Filter}$$

**Result:** Both dynamite and vibroseis data are brought to consistent zero-phase.

## MBWP Parameters

MBWP contains only **two** parameters:

| Parameter | Role | Typical Range |
|-----------|------|--------------|
| Q (effective) | Amount of absorption | 15–50 (land) |
| S/N ratio | Noise level relative to signal | 0–20 dB |

### Finding Q and S/N from Power Spectra

From the model power spectra:
$$Q/t = 55/\text{slope}$$

The S/N is visible as the level difference between signal and noise spectra at a reference frequency (e.g., 35 Hz).

### Parameter Estimation

1. Run parameter estimation on field data
2. Fit model log spectra to observed log spectra
3. Estimate Q and S/N per trace
4. Surface-consistent decomposition → average values
5. Use averages to create final operator

## Assessing Reliability

Three validation methods:
1. **VSP measurements** of the propagating wavelet
2. **Synthetic seismogram ties** (well-to-seismic)
3. **Mixed-source survey ties** (crosscorrelation phase consistency)

### Mixed-Source Example

- **Before MBWP:** Crosscorrelation phase spectrum shows significant phase rotation between dynamite and vibroseis data
- **After MBWP residual filter:** Crosscorrelation phase flattens to near zero → consistent phase across sources

## Extensions to the MBWP Model

Potential improvements:
- Non-white reflectivity effects
- Non-white noise modeling
- Source and receiver ghost modeling
- Processing filter effects:
  - Minimum-phase conversion
  - Bandpass filtering
  - Coherent-noise suppression
  - Spectral amortization

## Requirements for Application

| Component | How to Obtain |
|-----------|--------------|
| Instrument filters | Pulse the instruments |
| Polarity conventions | Document 90° phase shifts in vibroseis |
| Detector responses | Modeled or tap tests |
| Source parameters | Vibroseis sweep recording; dynamite charge configuration |

## Key Conclusions

1. MBWP models the seismic wavelet from physical components
2. Accounts for non-minimum-phase components that SCD cannot address
3. Explicitly models noise effects on deconvolution
4. Only two parameters (Q and S/N) — both estimable from data
5. Validated by VSP measurements and mixed-source ties
6. Enables consistent phase across different source types without requiring overlapping data

## Relevance to Course

This is the **primary theoretical reference** for MBWP. It explains:
- Why SCD is insufficient for non-minimum-phase wavelets
- How the MBWP model decomposes the wavelet into physical components
- How noise distorts the deconvolution operator
- How Q and S/N are the only free parameters
- How to validate MBWP results

## Related Wiki Pages

- [MBWP Step 1 — Initial Operator](mbwp_step1_initial_operator.md)
- [MBWP Step 2 — Estimating Parameters](mbwp_step2_estimating_parameters.md)
- [MBWP Step 3 — Final Operator](mbwp_step3_final_operator.md)
- [Hootman & Abitbol — MBWP Model Equations](hootman_abitbol_mbwp_model_equations.md)
- [David Brown — DP3 MBWP Module](brown_dp3_mbwp_module.md)
- [Surface-consistent deconvolution](../concepts/surface_consistent_deconvolution.md)
- [Statistical deconvolution](../concepts/statistical_deconvolution.md)
- [Broadband seismic](../concepts/broadband_seismic.md)
