---
title: "Hootman & Abitbol - MBWP Step 3: Final Operator"
status: reviewed
sources:
  - papers/deconvolution/MBWP Step 3 - Final Operator.pptx
tags: [MBWP, operator-design, wavelet-processing]
authors: [Michael Abitbol, Bruce Hootman]
date: 2009-02-06
type: workflow-guide
---

# MBWP Step 3: Creating and Exporting the Final Operator

## Overview

Final step in the MBWP workflow: reconstruct the model wavelet with estimated Q and S/N from Step 2, QC the output operator, condition it, and export as a filter for production use.

## Workflow

### 1. Reconstruct Model with Estimated Parameters

Starting from the Step 1 setup:

- Set **effective Q** = value from [Step 2](mbwp_step2_estimating_parameters.md) parameter estimation
- Set **S/N ratio** = value from Step 2 parameter estimation
- Set **deconvolution parameters** to match production SCD setup:
  - Length to Trim Internal Models: **2000**
  - MBWP Operator length: **500**
  - Only **spiking deconvolution** is used
  - (Gapped operators can be constructed separately, but generally not recommended)

### 2. QC the Output

Load the output wavelet suite and examine the components:

#### MBWP Operator (Trace 13)
- **Amplitude spectrum:** should be flat across the data frequency band
- **Phase spectrum:** represents the correction applied to data
- **Check for:** instabilities or artifacts

#### Decon Operator (Trace 11)
- **Amplitude spectrum:** should be inverse of model trace
- **Phase:** should be minimum-phase

### 3. Load MBWP Operator for Conditioning

Load the MBWP operator (residual wavelet) into a wavelet visualization/editing tool.

### 4. Condition the Operator

#### Tapering (Required)
- Apply **Hanning cosine taper** to both ends
- Taper length: **100 ms** on each end

#### High-Cut Filter (If Needed)
- Inspect amplitude spectrum for high-frequency artifacts
- If artifacts present: apply zero-phase high-cut filter
- Example: 140 Hz high-cut removes typical artifacts
- This step is **optional** — only if artifacts are visible

### 5. Export as Filter Operator

- Export the conditioned MBWP operator as a **bandpass filter**
- **Normalization:** ON
- **High and low cut frequencies:** set to reasonable values
- **Documentation:** include enough information to trace back to:
  - Wavelet suite used
  - Model construction parameters
  - Q and S/N values used
  - What the operator does

### 6. Final Verification

- Verify filter coefficients match the MBWP operator
- This is the last check before production use

## Production Application

The filter containing the MBWP operator goes into the processing flow:

- **After:** Surface-consistent deconvolution
- **Before:** Any moveout correction (NMO, DMO)
- **Best practice:** Apply as the **next step after SC decon**

$$\text{SC Decon} \longrightarrow \textbf{MBWP filter} \longrightarrow \text{NMO/DMO} \longrightarrow \cdots$$

## QC Checklist

- [ ] Q and S/N set to estimated values from Step 2
- [ ] Decon parameters match production SCD
- [ ] MBWP operator amplitude spectrum is flat in data band
- [ ] MBWP operator phase spectrum shows smooth correction
- [ ] No instabilities or artifacts in operator
- [ ] Decon operator is minimum-phase
- [ ] Operator tapered with 100 ms Hanning cosine
- [ ] High-frequency artifacts removed (if present)
- [ ] Filter operator has normalization ON
- [ ] Documentation records provenance
- [ ] Coefficients verified against MBWP operator

## Summary of Complete MBWP Workflow

| Step | Action | Output |
|------|--------|--------|
| 1 | Create initial operator (default Q=30, S/N=20) | Initial wavelet suite |
| 2 | Estimate Q and S/N via parameter estimation | Effective Q and S/N values |
| 3 | Reconstruct with estimated parameters | Final MBWP operator (filter) |

## Related Wiki Pages

- [MBWP Step 1 — Initial Operator](mbwp_step1_initial_operator.md)
- [MBWP Step 2 — Estimating Parameters](mbwp_step2_estimating_parameters.md)
- [Hootman & Abitbol — MBWP Model Equations](hootman_abitbol_mbwp_model_equations.md)
- [Brown et al. — MBWP Update 2008](brown_et_al_mbwp_update_2008.md)
