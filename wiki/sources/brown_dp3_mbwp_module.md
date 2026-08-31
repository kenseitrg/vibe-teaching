---
title: "David Brown - DP3 MBWP Module"
status: reviewed
sources:
  - papers/deconvolution/David Brown - DP3 MBWP Module.pptx
tags: [deconvolution, predictive-deconvolution, coloured-deconvolution, surface-consistent, MBWP, wavelet-processing]
author: David Brown
type: training-module
---

# David Brown - DP3 MBWP Module

## Overview

Comprehensive training module on deconvolution within the DP3 (Data Processing 3) workflow. Covers predictive deconvolution, surface-consistent deconvolution, coloured deconvolution, and introduces MBWP (Model-Based Wavelet Processing) as an advanced approach.

## Key Topics

### 1. The Objective of Deconvolution

**In theory:**
- Extract reflectivity by removing wavelet effects, including ghosts and short-period multiples

**In practice:**
- Arrive at a better estimate of reflectivity
- Output trace represents reflectivity in terms of amplitude, polarity, and depth within signal property limits

### 2. Inverse Filters

The convolutional model: $X(t) = \omega(t) * r(t)$

**Ideal solution:**
- Convolve with inverse wavelet: $X(t) * 1/\omega(t) = r(t)$

**Challenge:**
- Requires accurate wavelet estimate $\omega(t)$
- No simple one-step approach for real seismic data
- Solution: combine **deterministic** and **statistical** deconvolution

### 3. Predictive Deconvolution

**Method:**
- Derives wavelet estimate from trace autocorrelation
- Uses early part of trace to predict and deconvolve later part

**Major Assumptions:**
1. Dataset is noise-free
2. Wavelet is minimum phase
3. Wavelet is time-invariant (stationary)
4. Reflection coefficient series is random (white)

**Types:**
- **Spiking deconvolution:** Gap = 1 sample (compresses to spike)
- **Gapped deconvolution:** Gap > 1 sample (predicts multiples, ringing)

### 4. Assumptions in Detail

#### White Reflectivity
- Use long design windows (10% rule)
- Data must be well-balanced within window
- Use geospread correction
- Apply exponential gain if needed (careful with multiples)
- Exclude areas of very strong reflectivity

#### Stationary Wavelet
- Wavelet should not change within design window
- Choose windows carefully
- Use multiple windows if needed
- Consider time-varying approaches

#### Minimum Phase
- Critical for spiking deconvolution
- Less critical for gapped deconvolution
- Long-gap decons don't modify wavelet phase significantly
- Multiples must be minimum phase

### 5. Pre-Whitening

**Purpose:**
- Add white noise to autocorrelation during operator design
- Prevents numerical instability (divisions by zero)
- Lessens filtering effect

**Practical range:** 0.1% - 1.0%

**Trade-offs:**
- Too little: unstable operator, decreased S/N
- Too much: reduced deconvolution effectiveness, narrowed bandwidth

### 6. Effects of Random Noise

- Random noise has similar effect to pre-whitening
- Increasing noise decreases deconvolution effect
- Can cause spurious spikes in data and spectrum
- High noise → minimal pre-whitening needed
- Spiking deconvolution best done after stack (improved S/N)

### 7. Multi-Channel Deconvolution

**Advantages:**
- More randomness due to differential moveout
- Noise changes trace-to-trace
- Better noise cancellation

**Disadvantages:**
- Smearing of extracted wavelet

**Typical procedure:**
- Average autocorrelations for shot
- One filter per shot

### 8. Surface-Consistent Deconvolution (SCD)

**Model:**
$$\text{Wavelet} = \text{Source} * \text{Detector} * \text{Offset} * \text{Midpoint} * \text{?}$$

**Approach:**
- Solve for surface-consistent components
- Reconstruct wavelet from components
- Reconstruction smooths random noise effects

**Limitations:**
- Partially addresses random noise through spectral averaging
- Does not address non-minimum-phase wavelet components
- Does not address reflectivity issues

### 9. Coloured Deconvolution

**Problem with conventional approach:**
- Assumes white reflectivity
- Real reflectivity deviates from white-noise model
- Well logs show: rich in high frequencies, deficient in low frequencies

**Coloured Reflectivity Model:**
$$\text{Amplitude} \propto (\text{Frequency})^{C_{LR}}$$

where $C_{LR} = m/2$ and $m$ is the slope of log power spectrum of reflectivity.

**Procedure:**
1. Estimate coloured reflectivity $r_{CLR}$
2. Compute and apply inverse $r_{CLR}^{-1}$
3. Design deconvolution operator on corrected trace

**Benefits:**
- Extension of conventional deconvolution
- Better approximates actual reflection coefficients
- Improves resolution
- Good for seismic inversion

### 10. Other Deconvolution Types

- **Spectrally constrained:** Extends coloured decon
- **Maximum entropy (BURG_DECON):** Makes data as random as possible
- **HARMONIZER_DECON:** Sample-by-sample deconvolution
- **Spectral broadening**
- **Stochastic deconvolution**
- **Minimum entropy (FMED)**
- **Sparse spike (linear programming)**

## Key Takeaways

1. Inverse filtering requires accurate wavelet estimate
2. Predictive deconvolution relies on strong assumptions (minimum phase, white reflectivity, no noise)
3. Autocorrelation reveals wavelet and multiple characteristics
4. Noise significantly impacts deconvolution effectiveness
5. Coloured deconvolution better models real reflectivity
6. Surface-consistent approach reduces noise effects but doesn't solve all problems

## Relevance to Course

This module provides foundational understanding of:
- Why statistical deconvolution assumptions often fail
- How noise affects deconvolution operators
- The motivation for model-based approaches like MBWP
- Surface-consistent decomposition concepts

## Related Wiki Pages

- [Statistical deconvolution](../concepts/statistical_deconvolution.md)
- [Surface-consistent deconvolution](../concepts/surface_consistent_deconvolution.md)
- [Minimum phase](../concepts/minimum_phase.md)
- [Predictive deconvolution](../concepts/predictive_deconvolution.md)
- [Brown et al. MBWP Update 2008](brown_et_al_mbwp_update_2008.md)
