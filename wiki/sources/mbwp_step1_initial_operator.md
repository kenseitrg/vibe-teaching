---
title: "Hootman & Abitbol - MBWP Step 1: Initial Operator"
status: reviewed
sources:
  - papers/deconvolution/MBWP Step 1 - Initial Operator.pptx
tags: [MBWP, workflow, operator-design, wavelet-processing]
authors: [Michael Abitbol, Bruce Hootman]
date: 2009-02-06
type: workflow-guide
---

# MBWP Step 1: Creating the Initial Operator

## Overview

Step-by-step workflow for creating the initial MBWP operator. This initial operator uses default Q and S/N values; these are refined in Step 2.

## Prerequisites

Before starting, you need:

1. **Instrument response** — pulse test of the field recording instrument
2. **Geophone or GAC response** — measured tap test or known natural frequency + damping
3. **Source signature** (non-dynamite only) — filtered sweep or airgun signature

## Workflow: Dynamite Case

### 1. Prepare Input Wavelets

#### Instrument Response
- Load instrument response from pulse test data
- Create amplitude and phase spectra for QC
- Verify spectrum matches recording instrument filter settings

#### Geophone Response
- Load geophone/GAC response from tap test or create from specifications
- Create amplitude and phase spectra for QC
- Verify amplitude and phase match expected geophone response

#### Save Wavelet Suite
- Save all wavelets in a wavelet file for model construction

### 2. Construct Initial Model Wavelet

#### Input Setup
- Set **Sampling Interval** to match data sample rate
- Load instrument response and geophone response wavelets

#### Model Construction Parameters
- **Source type:** Dynamite (or Vibroseis, Airgun, etc.)
- **Detector Type:** NOT_USED (since providing measured response)
- **Q:** Set initial estimate (e.g., Q = 30 — typical land value)
- **S/N:** Set initial estimate (e.g., S/N = 20 dB)
- **Deconvolution parameters:** Match production SCD setup
  - Length to Trim Internal Models: **2000** (more stable)
  - MBWP Operator length: **500** (recommended)

#### Output
- Suite of model wavelets (14 components)
- **Signal and noise autocorrelations** → input to parameter estimation (Step 2)

## Workflow: Vibroseis Case

### Additional Step: Source Signature

1. Load sweep from field recording
2. Specify start/end time of sweep
3. Create Klauder wavelet via crosscorrelation of sweep with itself
4. If using minimum-phase conversion filter:
   - Load bandpass filter coefficients
   - Convolve Klauder wavelet with filter
   - Result: instrument-filtered sweep
5. Save wavelet suite

### Model Construction Setup
- Same as dynamite case plus source signature
- **Source type:** Vibroseis
- **Form of Sweep Input:** Autocorrelation
- Load instrument-filtered sweep wavelet
- Output has 15 components (sweep autocorrelation added)

## Important Notes

### Naming Conventions
The following wavelet components must be clearly identified:
- Instrument response
- Geophone/detector response
- Source signature (vibroseis sweep or dynamite model)

Proper labeling ensures correct assembly of the model wavelet.

### Resampling
- If data was recorded at 2 ms but resampled to 4 ms for processing:
  - Resample wavelets to match processing sample rate
  - Set wavelet sampling interval to 4 ms

### Typical Initial Parameters
| Parameter | Typical Value |
|-----------|--------------|
| Q | 30 |
| S/N | 20 dB |
| Trim length | 2000 |
| Operator length | 500 |

These are **initial** values — refined in Step 2.

## Next Step

→ [Step 2: Estimating Parameters](mbwp_step2_estimating_parameters.md)

## Related Wiki Pages

- [Hootman & Abitbol — MBWP Model Equations](hootman_abitbol_mbwp_model_equations.md)
- [MBWP Step 2 — Estimating Parameters](mbwp_step2_estimating_parameters.md)
- [MBWP Step 3 — Final Operator](mbwp_step3_final_operator.md)
- [Brown et al. — MBWP Update 2008](brown_et_al_mbwp_update_2008.md)
