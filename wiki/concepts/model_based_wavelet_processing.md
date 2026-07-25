---
title: "Model-Based Wavelet Processing (MBWP)"
status: draft
sources:
  - brown_et_al_mbwp_update_2008
  - hootman_abitbol_mbwp_model_equations
  - mbwp_step1_initial_operator
  - mbwp_step2_estimating_parameters
  - mbwp_step3_final_operator
  - brown_dp3_mbwp_module
tags: [deconvolution, wavelet-processing, Q, signal-to-noise, surface-consistent, mixed-source]
---

# Model-Based Wavelet Processing (MBWP)

## Overview

Model-Based Wavelet Processing (MBWP) is a deterministic deconvolution technique that models the seismic wavelet from its physical components rather than deriving it statistically from the data autocorrelation. MBWP addresses key limitations of surface-consistent deconvolution (SCD) by explicitly accounting for non-minimum-phase wavelet components and noise effects.

## The Convolutional Model

The seismic trace is modeled as:

$$\text{Trace} = [\text{Source} * Q * \text{Reflectivity} + \text{Noise}] * \text{Detector} * \text{Instrument}$$

The **wavelet** is:

$$W(t) = \text{Source}(t) * Q(t) * \text{Detector}(t) * \text{Instrument}(t)$$

### Key Distinction from Statistical Deconvolution

Unlike predictive deconvolution, MBWP does **not** assume:
1. ~~Wavelet is minimum phase~~
2. ~~White reflectivity~~
3. ~~No noise~~

Instead, it models each component deterministically.

## Wavelet Components

### 1. Source Signature

**Vibroseis:**
- Sweep is proportional to applied force (displacement)
- After correlation: Klauder wavelet (autocorrelation of filtered sweep)
- Requires sweep recording from field instruments

**Dynamite:**
- Buried source: first derivative of step function
- Surface source: different radiation pattern
- Requires charge depth and configuration

**Airgun (marine):**
- Far-field signature with ghost
- Measured or modeled

### 2. Absorption (Q)

- Exponential amplitude loss with frequency: $A(f) \propto e^{-\pi f t / Q}$
- Characterized by effective Q parameter
- Typical land values: Q = 15–50

### 3. Detector Response

**Geophone:**
- Resonance frequency (~10 Hz typical)
- Damping factor
- Records particle velocity
- Can be modeled from specifications or measured via tap test

**Hydrophone:**
- Records pressure
- Broader frequency response

### 4. Instrument Response

- Recording system filters
- Measured from pulse tests
- Includes anti-alias filters, low-cut filters

## Why SCD Falls Short

Surface-consistent deconvolution decomposes:
$$W(t) = S(t) * R(t) * O(t) * M(t)$$

**Limitations:**
- Assumes minimum-phase wavelet → cannot correct non-minimum-phase components
- Partially addresses noise through spectral averaging
- Does not model Q absorption explicitly
- Does not account for detector/instrument responses

**MBWP advantage:**
- Models non-minimum-phase components (detector response, Q, instrument filters)
- Explicitly models noise effects on deconvolution
- Provides physically meaningful wavelet estimate

## The MBWP Workflow

### Step 1: Create Initial Operator

**Inputs:**
- Instrument response (pulse test)
- Geophone/detector response (tap test or model)
- Source signature (sweep recording for vibroseis)

**Process:**
1. Prepare input wavelets (instrument response, detector response, source signature)
2. Construct model wavelet with initial Q and S/N estimates (e.g., Q=30, S/N=20 dB)
3. Output: suite of model wavelets including signal and noise autocorrelations

**Key outputs:**
- Signal autocorrelation
- Noise autocorrelation
- Initial MBWP operator

### Step 2: Estimate Parameters

**Goal:** Determine effective Q and S/N from field data

**Process:**
1. Run parameter estimation on field spectral analysis
2. Fit model log spectra to observed log spectra
3. Estimate Q and S/N per trace
4. Surface-consistent decomposition → average values
5. QC: scatter plots, model fits, histograms

**Typical results:**
- Q = 15–50 (land data)
- S/N = 0–20 dB

### Step 3: Create Final Operator

**Process:**
1. Reconstruct model wavelet with estimated Q and S/N
2. QC the MBWP operator:
   - Amplitude spectrum should be flat in data band
   - Phase spectrum shows smooth correction
   - No instabilities or artifacts
3. Condition operator:
   - Apply 100 ms Hanning taper to both ends
   - Remove high-frequency artifacts if present
4. Export as filter operator

**Production application:**
$$\text{SC Decon} \rightarrow \textbf{MBWP filter} \rightarrow \text{NMO/DMO}$$

## Noise Effects on Deconvolution

### The Problem

The autocorrelation that predictive deconvolution "sees":
$$\phi_{xx} = \phi_{ss} + \phi_{nn}$$

This is **not** the wavelet spectrum — it's distorted by noise.

As S/N decreases:
- Autocorrelation becomes noise-dominated
- Minimum-phase wavelet derived from autocorrelation is distorted
- Phase errors increase

### The MBWP Solution

1. Build model wavelet from physical components
2. Compute deconvolution operator from model
3. Compute residual filter:
   $$\text{Residual} = \text{MBWP Op} - \text{Decon Result}$$
4. Apply residual to correct deconvolution output

**Result:** Corrects for noise-induced phase errors.

## MBWP Parameters

Only **two** free parameters:

| Parameter | Role | How to Estimate |
|-----------|------|----------------|
| **Q** | Absorption strength | Fit model to field spectra |
| **S/N** | Noise level | Fit model to field spectra |

Both are estimated from data via parameter estimation.

## Validation Methods

1. **VSP measurements:** Compare model wavelet with downhole recordings
2. **Synthetic seismogram ties:** Well-to-seismic correlation
3. **Mixed-source surveys:** Phase consistency between different source types

### Mixed-Source Example

**Before MBWP:**
- Crosscorrelation phase between dynamite and vibroseis shows significant rotation

**After MBWP:**
- Phase flattens to near zero
- Consistent phase across sources without requiring overlapping data

## Applications

### Land Data
- Corrects receiver coupling effects
- Accounts for near-surface absorption
- Handles mixed vibroseis/dynamite surveys

### Broadband Processing
- Extends usable bandwidth by correcting non-minimum-phase effects
- Improves low-frequency content (receiver response correction)
- Enables consistent phase for inversion

### Mixed-Source Surveys
- Merges vibroseis and dynamite data with consistent phase
- No requirement for overlapping source recordings
- Enables stratigraphic interpretation across source boundaries

## Advantages Over SCD

| Feature | SCD | MBWP |
|---------|-----|------|
| Non-minimum-phase correction | ✗ | ✓ |
| Explicit Q modeling | ✗ | ✓ |
| Noise modeling | Partial (averaging) | ✓ |
| Detector response | ✗ | ✓ |
| Instrument response | ✗ | ✓ |
| Mixed-source consistency | Limited | ✓ |
| Parameters | 4 (S, R, O, M) | 2 (Q, S/N) |

## Limitations

1. **Requires measurements:**
   - Instrument pulse tests
   - Geophone tap tests or specifications
   - Source recordings (vibroseis sweep)

2. **Assumes spatially constant Q:**
   - Effective Q is average value
   - Does not model Q variation with depth
   - Surface-consistent Q decomposition possible but not standard

3. **Only spiking deconvolution:**
   - Gapped operators not directly supported
   - Can be constructed separately but not recommended

4. **Assumes white reflectivity for decon operator:**
   - MBWP operator is residual after decon
   - Coloured deconvolution can be combined

## Practical Considerations

### When to Use MBWP

**Recommended for:**
- Mixed-source surveys (vibroseis + dynamite)
- Land data with strong receiver effects
- Broadband processing requiring phase consistency
- Surveys with good instrument/detector measurements

**May not be needed for:**
- Marine data (use designature + deghosting instead)
- Simple land surveys with minimum-phase wavelets
- Data without instrument/detector measurements

### Integration with Other Processes

**Typical flow:**
1. Surface-consistent deconvolution (addresses S, R, O, M components)
2. **MBWP** (addresses non-minimum-phase residuals)
3. NMO/DMO
4. Stack
5. Post-stack deconvolution (optional)

**Can be combined with:**
- Coloured deconvolution (non-white reflectivity)
- Q-compensation (time-varying Q)
- Surface-consistent amplitude correction

## Summary

MBWP is a **deterministic** approach to wavelet processing that:
- Models the wavelet from physical components (source, Q, detector, instrument)
- Corrects non-minimum-phase effects that SCD cannot address
- Explicitly accounts for noise effects on deconvolution
- Requires only two parameters (Q and S/N)
- Enables consistent phase across mixed-source surveys
- Validates against VSP and well-tie measurements

## Related Concepts

- [Statistical deconvolution](statistical_deconvolution.md)
- [Surface-consistent deconvolution](surface_consistent_deconvolution.md)
- [Predictive deconvolution](predictive_deconvolution.md)
- [Broadband seismic](broadband_seismic.md)
- [Minimum phase](minimum_phase.md)

## References

- Hart, D., & Hootman, B. (2008). Achieving Consistent and Stable Phase with Mixed-Source Surveys. WesternGeco internal document.
- Hootman, B., & Abitbol, M. (2008). MBWP Model Equations. WesternGeco.
- Hootman, B., & Abitbol, M. (2009). MBWP Workflow Steps 1-3. WesternGeco.
- Brown, D. DP3 MBWP Module. WesternGeco training materials.
