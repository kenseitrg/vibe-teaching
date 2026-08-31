---
title: "Hootman & Abitbol - MBWP Step 2: Estimating Parameters"
status: reviewed
sources:
  - papers/deconvolution/MBWP Step 2 - Estimating Parameters.pptx
tags: [MBWP, parameter-estimation, Q, signal-to-noise, surface-consistent]
authors: [Bruce Hootman, Michael Abitbol]
date: 2009-02-04
type: workflow-guide
---

# MBWP Step 2: Estimating Q and S/N Parameters

## Overview

Procedure for estimating effective Q and signal-to-noise ratio. These estimated parameters replace the initial guesses from Step 1 and are used to create the final MBWP operator.

## Inputs

1. **Spectral analysis data** — same setup as production SC deconvolution spectral analysis
   - Full dataset or selected subset suitable for surface-consistent decomposition
   - Production SCD spectral analysis can be used directly
2. **Initial MBWP wavelets** — output from Step 1 (traces 4 and 9)

## Parameter Estimation Setup

### Initial Parameter Estimates

| Parameter | Typical Value | Notes |
|-----------|--------------|-------|
| Q | 30 | Initial estimate |
| S/N | 20 dB | Initial estimate |
| Frequency | 35 Hz | Fixed — no need to change |

### Fitting Frequency Range

- Adjust range if the fit is poor for all traces
- Usually best to **eliminate lowest frequencies** (10–15 Hz)
- Don't worry about frequencies outside the fitting range

### Output

1. **Log spectra** — spectral analysis output with average Q and S/N estimates
2. **QC trace pairs** — for each selected trace:
   - Field data log spectrum
   - Model log spectrum
   - (Twice the number of selected traces)

## QC Procedures

### 1. Scatter Plot of Q and S/N

- Plot all estimated Q and S/N values
- Check for reasonable scatter (not clustered or extreme)
- Average values should not be far from initial estimates

**Typical land values:**
- Q = 15–50
- S/N = 0–20 dB

### 2. Model Fit QC

For each trace pair:
- **Good fit:** modeled log spectrum matches field data across fitting range
- **Acceptable:** minor deviations at edges of fitting range
- **Poor fit:** large notches not modeled, systematic misfit
- Don't worry about:
  - Low frequencies outside fitting range (always unreliable)
  - High frequencies outside fitting range

### 3. Surface-Consistent Decomposition

After parameter estimation, decompose Q and S/N into surface-consistent components:

- **Input:** log power spectra from parameter estimation
- **Decomposition:** source and detector terms only (no global term)
- **QC geometry database** output

### 4. Compute Corrected S/N

Supply initial values from parameter estimation:
- Initial Q value
- Initial S/N value  
- Frequency value

The S/N equation is:
$$k = k_s - k_n + k_p + \frac{Q_p - Q_{ave}}{f_0}$$

### 5. Histogram Analysis

Create histograms of source terms:
- **Q histogram:** gives average effective Q
- **S/N histogram:** gives average effective S/N

The source term is decomposed first, so it contains the bulk of Q and S/N information. Detector terms are perturbations only.

### Example Results

| Parameter | Value |
|-----------|-------|
| Average Q | ~34 |
| Average S/N | ~7 dB |

### Spatial Analysis (Optional)

- Map Q variation spatially — may correlate with geology/elevation
- Map S/N variation — identifies noisy areas
- Surface-consistent Q and S/N maps may be useful client deliverables
- Future use: surface-consistent variation in MBWP operator

## Final Step

With estimated parameters:
1. Return to [Step 1 workflow](mbwp_step1_initial_operator.md)
2. Replace initial Q and S/N with estimated values
3. Rerun model construction → proceed to [Step 3](mbwp_step3_final_operator.md)

## QC Checklist

- [ ] Scatter plot shows reasonable distribution
- [ ] Average Q in range 15–50 (typical land)
- [ ] Average S/N in range 0–20 dB
- [ ] Model fits match field data across fitting range
- [ ] No systematic notches or misfits
- [ ] Histograms of source terms are well-behaved

## Related Wiki Pages

- [MBWP Step 1 — Initial Operator](mbwp_step1_initial_operator.md)
- [MBWP Step 3 — Final Operator](mbwp_step3_final_operator.md)
- [Hootman & Abitbol — MBWP Model Equations](hootman_abitbol_mbwp_model_equations.md)
- [Brown et al. — MBWP Update 2008](brown_et_al_mbwp_update_2008.md)
- [Surface-consistent deconvolution](../concepts/surface_consistent_deconvolution.md)
