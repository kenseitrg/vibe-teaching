---
title: "Term 3 Lecture 05 — Broadband Deconvolution"
status: draft
lecture: term03_lec05
tags: [broadband, deconvolution, marine, land, deghosting, designature, MBWP, robust]
sources:
  - cgg_odt04_deconvolution_part1_wavelet
  - cgg_odt04_deconvolution_part2_signature
  - cgg_odt04_deconvolution_part3_demultiple
  - monk_2020_broadband_seismic
  - amundsen_zhou_2013_deghosting
  - li_et_al_2020_sparse_deghosting
  - ghosh_2000_ghost_deconvolution
  - lindsey_1960_ghost_elimination
  - zhang_yuan_2019_robust_deconvolution
  - brown_et_al_mbwp_update_2008
  - hootman_abitbol_mbwp_model_equations
  - mbwp_step1_initial_operator
  - mbwp_step2_estimating_parameters
  - mbwp_step3_final_operator
  - brown_dp3_mbwp_module
---

# Term 3 Lecture 05 — Broadband Deconvolution

## Summary

This lecture covers broadband seismic data processing, focusing on extending the usable frequency bandwidth of seismic data through advanced deconvolution techniques. The lecture is divided into two parts: marine processing (de-bubble, designature, deghosting) and land processing (Model-Based Wavelet Processing). The lecture also introduces robust surface-consistent deconvolution for challenging environments.

## Key Concepts

1. **Broadband Seismic** — Extended bandwidth (6+ octaves) for improved resolution and interpretation
2. **Ghost Physics** — Source and receiver ghosts create spectral notches that limit bandwidth
3. **Marine Processing Flow** — De-bubble → Designature → Deghosting → Q-compensation → Deconvolution
4. **Source Signature** — Airgun array output with bubble oscillation and ghost effects
5. **Designature** — Removing or reshaping the source signature (zero-phase conversion, de-bubble)
6. **Deghosting** — Removing source and receiver ghosts to recover lost bandwidth
7. **Land MBWP** — Model-Based Wavelet Processing for land data (receiver effects, absorption, blueness, noise)
8. **Robust SC Deconvolution** — L1/L2 optimization for foothill and challenging environments

## Lecture Outline

### 1. Introduction to Broadband Seismic (15 min)

**Key points:**
- Definition: 6+ octaves of usable bandwidth (e.g., 1–64 Hz)
- Benefits: sharper wavelets, better resolution, improved interpretation, AVO, and inversion
- Bandwidth and resolution: lobe width $L_w \propto 2/(f_{\max} - f_{\min})$
- Octaves: each octave doubles the frequency range
- Low frequencies control wavelet isolation (side lobes)
- High frequencies control resolution (central lobe width)
- Ghost notches: $f_n = n \cdot v_w / (2d)$ — all frequencies below first notch are lost

**Concepts:** [Broadband seismic](../concepts/broadband_seismic.md)

**Sources:** Monk (2020) Chapter 2

### 2. Recap: Wave Propagation Effects (10 min)

**Key points:**
- Seismic wave propagation is affected by:
  - Source signature (airgun bubble oscillation)
  - Ghosts (source and receiver)
  - Absorption (Q-effects, covered in Term 2)
  - Receiver coupling (land data)
  - Near-surface effects (covered in Term 1)
- These effects limit the effective bandwidth of seismic data
- Broadband processing aims to remove or compensate for these effects

**Concepts:** [Seismic wavelet](../concepts/seismic_wavelet.md), [Broadband seismic](../concepts/broadband_seismic.md)

**Sources:** [CGG ODT04 Part 1](../sources/cgg_odt04_deconvolution_part1_wavelet.md)

### 3. Marine Data Processing (30 min)

#### 3.1 De-Bubble (5 min)

**Key points:**
- Bubble oscillation creates oscillatory tails in the wavelet
- Reduces resolution and creates false events
- De-bubble before zero-phasing to avoid zero-phasing the bubble
- Flow: Raw wavelet → De-bubble operator → De-bubbled wavelet

**Concepts:** [Source signature and designature](../concepts/source_signature_designature.md)

**Sources:** [CGG ODT04 Part 2](../sources/cgg_odt04_deconvolution_part2_signature.md)

#### 3.2 Designature (10 min)

**Key points:**
- Designature toolbox: spiking decon, zero-phase conversion, shaping
- Zero-phase conversion: convert wavelet to zero-phase (symmetric, centered)
- Spiking decon: compress to spike (rarely used — noise boosting at notches)
- Shaping: match to target wavelet (4D matching, amplitude/phase shaping)
- Trade-off: resolution vs. stability (pre-whitening)

**Concepts:** [Source signature and designature](../concepts/source_signature_designature.md)

**Sources:** [CGG ODT04 Part 2](../sources/cgg_odt04_deconvolution_part2_signature.md)

#### 3.3 Deghosting (15 min)

**Key points:**
- Ghost physics: source and receiver ghosts create spectral notches
- Ghost notch frequency: $f_n = n \cdot v_w / (2d)$
- Angle dependence: ghost delay varies with offset (1D designature fails)
- Deghosting methods:
  - Classical 1D designature (vertical ray assumption — rarely used)
  - Bootstrap deghosting (tau-p domain inverse problem)
  - Dual-sensor (PZ) deghosting (hydrophone + geophone)
  - Variable-depth streamer (BroadSeis — notch diversity)
  - Sparse deghosting (sparsity-constrained inversion)
  - Low-frequency deghosting (trace-by-trace operator)

**Concepts:** [Marine deghosting](../concepts/marine_deghosting.md), [Broadband seismic](../concepts/broadband_seismic.md)

**Sources:** 
- [CGG ODT04 Part 2](../sources/cgg_odt04_deconvolution_part2_signature.md)
- [Amundsen & Zhou (2013)](../sources/amundsen_zhou_2013_deghosting.md)
- [Li et al. (2020)](../sources/li_et_al_2020_sparse_deghosting.md)
- [Ghosh (2000)](../sources/ghosh_2000_ghost_deconvolution.md)

### 4. Land Data Processing — MBWP (25 min)

#### 4.1 Effect of Receivers and Station (5 min)

**Key points:**
- Land receivers (geophones) have resonance frequency (~10 Hz)
- Poor coupling in dry/loose near-surface attenuates low frequencies
- Receiver response limits low-frequency content
- Need to characterize and compensate for receiver effects

**Concepts:** [Broadband seismic](../concepts/broadband_seismic.md), [Model-Based Wavelet Processing](../concepts/model_based_wavelet_processing.md)

**Sources:** Monk (2020) Chapter 2, [CGG ODT04 Part 2](../sources/cgg_odt04_deconvolution_part2_signature.md), [MBWP Update 2008](../sources/brown_et_al_mbwp_update_2008.md)

#### 4.2 Absorption and Q-Compensation Recap (5 min)

**Key points:**
- Absorption (Q-effects) attenuates high frequencies with depth
- Q-compensation corrects for absorption losses (covered in Term 2)
- Q-compensation is part of the broadband processing flow
- Non-stationary convolution: Q-filter varies with time/depth
- MBWP models Q as part of the wavelet: $W(t) = S(t) * Q(t) * D(t) * I(t)$

**Concepts:** [Broadband seismic](../concepts/broadband_seismic.md), [Model-Based Wavelet Processing](../concepts/model_based_wavelet_processing.md)

**Sources:** Term 2 Lecture materials (Q-compensation), [MBWP Model Equations](../sources/hootman_abitbol_mbwp_model_equations.md)

#### 4.3 Non-White Reflectivity — Blueness Correction (10 min)

**Key points:**
- Statistical deconvolution assumes white reflectivity
- Real reflectivity is often "blue" (high-frequency dominated) or "red" (low-frequency dominated)
- Blueness correction: adjust deconvolution operator to account for non-white reflectivity
- Color deconvolution: match wavelet to desired spectrum (whitening, blueing, reddening)
- Practical approach: estimate reflectivity color from well data or statistical analysis
- Coloured deconvolution model: $\text{Amplitude} \propto (\text{Frequency})^{C_{LR}}$ where $C_{LR} = m/2$

**Concepts:** [Statistical deconvolution](../concepts/statistical_deconvolution.md), [Broadband seismic](../concepts/broadband_seismic.md)

**Sources:** [CGG ODT04 Part 2](../sources/cgg_odt04_deconvolution_part2_signature.md), [David Brown DP3 Module](../sources/brown_dp3_mbwp_module.md) (slides 47-66)

#### 4.4 Effect of Random Noise (5 min)

**Key points:**
- Random noise affects deconvolution operator stability
- High noise levels → unstable operators → poor results
- The autocorrelation that predictive deconvolution "sees" is: $\phi_{xx} = \phi_{ss} + \phi_{nn}$
- This is **not** the wavelet spectrum — it's distorted by noise
- As S/N decreases, minimum-phase wavelet derived from autocorrelation becomes distorted
- Solutions:
  - Surface-consistent deconvolution (use multiple traces to estimate operator)
  - **Model-Based Wavelet Processing** (explicitly models noise effects)
  - Robust deconvolution (L1/L2 optimization — see Section 5)
  - Pre-whitening (dampen noise amplification)
- Trade-off: more aggressive deconvolution → more noise amplification

**Concepts:** [Surface-consistent deconvolution](../concepts/surface_consistent_deconvolution.md), [Statistical deconvolution](../concepts/statistical_deconvolution.md), [Model-Based Wavelet Processing](../concepts/model_based_wavelet_processing.md)

**Sources:** [CGG ODT04 Part 2](../sources/cgg_odt04_deconvolution_part2_signature.md), [MBWP Update 2008](../sources/brown_et_al_mbwp_update_2008.md) (slides 29-38), [David Brown DP3 Module](../sources/brown_dp3_mbwp_module.md) (slides 30-38)

#### 4.5 Model-Based Wavelet Processing — Theory (15 min)

**Key points:**

**The Problem with SCD:**
- Surface-consistent deconvolution decomposes: $W(t) = S(t) * R(t) * O(t) * M(t)$
- Assumes minimum-phase wavelet → cannot correct non-minimum-phase components
- Partially addresses noise through spectral averaging
- Does not model Q absorption explicitly
- Does not account for detector/instrument responses

**The MBWP Solution:**
- Models the wavelet from physical components: $W(t) = S(t) * Q(t) * D(t) * I(t)$
- Does **not** assume minimum phase, white reflectivity, or no noise
- Explicitly models each component:
  - **Source:** vibroseis sweep, dynamite charge, airgun signature
  - **Q:** absorption (exponential loss with frequency)
  - **Detector:** geophone response (resonance ~10 Hz), hydrophone
  - **Instrument:** recording system filters (measured from pulse tests)

**Why MBWP Works:**
- Corrects non-minimum-phase effects (detector response, Q, instrument filters)
- Accounts for noise distortion of the deconvolution operator
- Only two free parameters: **Q** and **S/N ratio**
- Both parameters estimable from field data

**Validation:**
- VSP measurements: model wavelet matches downhole recordings
- Mixed-source surveys: consistent phase between vibroseis and dynamite
- Well ties: improved synthetic seismogram correlation

**Applications:**
- Mixed-source surveys (vibroseis + dynamite) without requiring overlap
- Land data with strong receiver effects
- Broadband processing requiring phase consistency

**Concepts:** [Model-Based Wavelet Processing](../concepts/model_based_wavelet_processing.md), [Surface-consistent deconvolution](../concepts/surface_consistent_deconvolution.md)

**Sources:** [MBWP Update 2008](../sources/brown_et_al_mbwp_update_2008.md), [MBWP Model Equations](../sources/hootman_abitbol_mbwp_model_equations.md)

#### 4.6 MBWP Workflow (10 min)

**Key points:**

**Step 1: Create Initial Operator**
- **Inputs needed:**
  - Instrument response (pulse test)
  - Geophone/detector response (tap test or model)
  - Source signature (sweep recording for vibroseis)
- Prepare input wavelets (instrument response, detector response, source signature)
- Construct model wavelet with initial estimates: Q=30, S/N=20 dB
- Output: suite of model wavelets

**Step 2: Estimate Parameters**
- Run parameter estimation on field spectral analysis
- Fit model log spectra to observed log spectra
- Estimate Q and S/N per trace
- Surface-consistent decomposition → average values
- QC: scatter plots, model fits, histograms
- Typical results: Q = 15–50, S/N = 0–20 dB

**Step 3: Create Final Operator**
- Reconstruct model wavelet with estimated Q and S/N
- QC the MBWP operator:
  - Amplitude spectrum should be flat in data band
  - Phase spectrum shows smooth correction
  - No instabilities or artifacts
- Condition operator: apply 100 ms Hanning taper
- Export as filter operator

**Production Application:**
$$\text{SC Decon} \rightarrow \textbf{MBWP filter} \rightarrow \text{NMO/DMO}$$

**Advantages Over SCD:**

| Feature | SCD | MBWP |
|---------|-----|------|
| Non-minimum-phase correction | ✗ | ✓ |
| Explicit Q modeling | ✗ | ✓ |
| Noise modeling | Partial | ✓ |
| Detector response | ✗ | ✓ |
| Instrument response | ✗ | ✓ |
| Mixed-source consistency | Limited | ✓ |
| Parameters | 4 (S, R, O, M) | 2 (Q, S/N) |

**Concepts:** [Model-Based Wavelet Processing](../concepts/model_based_wavelet_processing.md)

**Sources:** [MBWP Step 1](../sources/mbwp_step1_initial_operator.md), [MBWP Step 2](../sources/mbwp_step2_estimating_parameters.md), [MBWP Step 3](../sources/mbwp_step3_final_operator.md), [MBWP Model Equations](../sources/hootman_abitbol_mbwp_model_equations.md)

### 5. Robust Surface-Consistent Deconvolution (10 min)

**Key points:**
- Traditional SC deconvolution uses L2 norm (least squares)
- Assumes Gaussian noise distribution
- Fails in foothill areas with inconsistent noise (ground roll, bursts)
- Robust SC deconvolution: hybrid L1/L2 norm optimization
- L2 norm for signal, L1 norm for noise outliers
- Unbiased results even with strong inconsistent noise
- Effective noise suppression at both high and low frequencies
- Field example: south China foothill data — bandwidth extended by 25 Hz at both ends

**Concepts:** [Surface-consistent deconvolution](../concepts/surface_consistent_deconvolution.md), [Robust deconvolution]

**Sources:** [Zhang & Yuan (2019)](../sources/zhang_yuan_2019_robust_deconvolution.md)

## Learning Objectives

After this lecture, students should be able to:

1. **Define broadband seismic** and explain why 6+ octaves of bandwidth are desirable
2. **Describe ghost physics** and calculate ghost notch frequencies for given source/receiver depths
3. **Explain the marine processing flow** (de-bubble → designature → deghosting) and the purpose of each step
4. **Compare deghosting methods** (bootstrap, PZ, variable-depth, sparse, low-frequency) and their advantages/limitations
5. **Describe the MBWP workflow** for land data and explain how it addresses receiver effects, absorption, blueness, and noise
6. **Explain robust SC deconvolution** and why it is needed for foothill and challenging environments
7. **Design a broadband processing flow** for a given dataset (marine or land)

## Figures

To be created:

1. **Broadband wavelet comparison** — Show wavelets with different bandwidths (2, 3, 6 octaves) and their amplitude spectra
2. **Ghost notch diagram** — Illustrate source and receiver ghost physics, show notch frequencies for different depths
3. **Marine processing flow** — Diagram showing de-bubble → designature → deghosting workflow
4. **Deghosting methods comparison** — Before/after amplitude spectra for different deghosting methods
5. **MBWP workflow** — Diagram showing land processing flow (receiver effects → absorption → blueness → noise)
6. **Robust SC deconvolution example** — Before/after comparison for foothill data (from Zhang & Yuan 2019)

## Exercises

To be created:

1. **Ghost notch calculation** — Calculate ghost notch frequencies for different source/receiver depths
2. **Deghosting method selection** — Given a dataset, choose the appropriate deghosting method and justify the choice
3. **Bandwidth analysis** — Analyze amplitude spectra before/after deghosting, calculate octaves of bandwidth
4. **Robust vs. traditional SC deconvolution** — Compare results for a noisy dataset

## Prerequisites

- Term 1 Lecture 06: Single-channel deconvolution (Wiener filter, spiking decon)
- Term 1 Lecture 07: Surface-consistent deconvolution
- Term 2: Q-compensation and absorption effects
- Term 3 Lecture 04: Noise attenuation (optional, but helpful)

## Related Lectures

- Term 1 Lecture 06: Single-channel deconvolution
- Term 1 Lecture 07: Surface-consistent deconvolution
- Term 3 Lecture 04: Noise attenuation

## References

### Textbooks and Books
- Monk, D. J. (2020). *Survey Design and Seismic Acquisition for Land, Marine, and In-between in Light of New Technology and Techniques*. SEG Distinguished Instructor Short Course No. 23. Chapter 2: Broadband Seismic.

### Journal Papers
- Amundsen, L., & Zhou, H. (2013). Low-frequency seismic deghosting. *Geophysics*, 78(2), WA15–WA20.
- Li, H.-J., Yang, Q.-Y., & Cai, J.-X. (2020). Simultaneous receiver-side deghosting and denoising method based on the sparsity constraint. *Applied Geophysics*, 17(3), 411–418.
- Ghosh, S. K. (2000). Deconvolving the ghost effect of the water surface in marine seismics. *Geophysics*, 65(6), 1831–1836.
- Lindsey, J. P. (1960). Elimination of seismic ghost reflections by means of a linear filter. *Geophysics*, 25(1), 130–140.
- Zhang, Y., & Mo, Y. (2019). Robust Deconvolution to improve resolution of foothill seismic data. *SEG 2019 Workshop: 2nd SEG Foothill Exploration Workshop*.

### Training Materials
- CGG ODT04 Deconvolution (2015). Parts 1–3: The Seismic Wavelet, Signature Deconvolution, Deconvolution as De-multiple.

## Comprehension Questions

1. Why is bandwidth measured in octaves, and why are 6+ octaves desirable for seismic data?
2. What is the ghost notch frequency for a receiver at 8 m depth? How does this change at 30° offset?
3. Why do we de-bubble before zero-phasing? What happens if we reverse the order?
4. Compare bootstrap deghosting and dual-sensor (PZ) deghosting. What are the advantages and limitations of each?
5. What is the "blueness" of reflectivity, and how does it affect deconvolution?
6. Why does traditional surface-consistent deconvolution fail in foothill areas? How does robust SC deconvolution solve this problem?
7. Design a broadband processing flow for a marine dataset acquired with a conventional streamer at 8 m depth.
8. Design a broadband processing flow for a land dataset acquired in a foothill area with high noise levels.

## Instructor Notes

- **Timing:** The lecture is designed for 90 minutes. Adjust timing based on class progress and questions.
- **Emphasis:** Focus on the physical intuition behind ghost physics and deghosting methods. The mathematical details are important but secondary to understanding the concepts.
- **Examples:** Use real data examples where possible (if available). The Zhang & Yuan (2019) paper provides a good example of robust SC deconvolution for foothill data.
- **Connections:** Emphasize the connections to Term 1 (deconvolution fundamentals) and Term 2 (Q-compensation). This lecture builds on those foundations.
- **Marine vs. Land:** Make sure to clearly distinguish between marine and land processing challenges. Marine processing focuses on ghosts and bubble; land processing focuses on receiver effects, absorption, and noise.
- **Broadband benefits:** Emphasize that broadband data is not just about resolution — it also improves interpretation, AVO, and inversion. The low frequencies are critical for impedance inversion and reducing dependence on initial models.

## Status

- [x] Source materials ingested into wiki
- [x] Concept pages created
- [ ] Lecture outline finalized
- [ ] Figures created
- [ ] Exercises created
- [ ] English lecture notes drafted
- [ ] Russian translation
- [ ] Slide deck created
