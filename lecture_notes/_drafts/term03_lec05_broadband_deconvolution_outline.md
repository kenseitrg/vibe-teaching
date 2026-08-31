# Term 3 Lecture 05 — Broadband Deconvolution: Lecture Outline

## Overview

**Duration:** 90 minutes  
**Topic:** Broadband seismic data processing — extending usable frequency bandwidth through advanced deconvolution techniques  
**Prerequisites:** Term 1 Lectures 06-07 (deconvolution), Term 2 (Q-compensation)

---

## Section 1: Introduction to Broadband Seismic (15 min)

### 1.1 What is Broadband Seismic? (5 min)
- Definition: 6+ octaves of usable bandwidth (e.g., 1–64 Hz)
- Contrast with conventional data (2–3 octaves, e.g., 10–60 Hz)
- **Figure 1:** Broadband wavelet comparison (2, 3, 6 octaves) with amplitude spectra
  - Show how more octaves → sharper wavelet, lower side lobes
  - Key equation: $L_w \propto 2/(f_{\max} - f_{\min})$

### 1.2 Benefits of Broadband Data (5 min)
- **Resolution:** Sharper wavelets, better event resolution
- **Interpretation:** Low-frequency texture, subtle impedance variations, fault tracking
- **Inversion:** Extended low frequencies → reduced dependence on initial model
- **AVO:** More consistent amplitude vs. offset behavior
- **Deep imaging:** Low frequencies penetrate better through absorptive layers
- **Figure 2:** Benefits diagram (wavelet → interpretation → inversion → AVO)

### 1.3 The Bandwidth Problem (5 min)
- Ghost notches: $f_n = n \cdot v_w / (2d)$
- For 6 m streamer: first notch at 125 Hz → all frequencies below 125 Hz are degraded
- **Figure 3:** Ghost notch diagram showing source and receiver ghosts
  - Show amplitude spectrum with notches
  - Explain angle dependence (notch frequency increases with offset)

---

## Section 2: Recap — Wave Propagation Effects (10 min)

### 2.1 What Limits Bandwidth? (5 min)
- **Source effects:** Airgun bubble oscillation, source ghost
- **Receiver effects:** Receiver ghost, geophone resonance (land)
- **Propagation effects:** Absorption (Q-effects), scattering
- **Near-surface effects:** Coupling, weathering layer
- **Figure 4:** Wave propagation effects diagram (source → propagation → receiver)

### 2.2 Why Conventional Processing Falls Short (5 min)
- Statistical deconvolution assumes white reflectivity → fails for colored reflectivity
- Trace-by-trace deconvolution → unstable in noisy areas
- 1D designature → fails at non-zero offset (ghost delay varies with angle)
- **Key insight:** Need advanced methods to recover full bandwidth

---

## Section 3: Marine Data Processing (30 min)

### 3.1 De-Bubble (5 min)
- **Goal:** Remove bubble oscillation from source signature
- **Why?** Bubble creates oscillatory tails → false events, reduced resolution
- **Method:** Deterministic inverse filter from bubble model
- **Flow:** Raw wavelet → De-bubble operator → De-bubbled wavelet
- **Key point:** De-bubble BEFORE zero-phasing (avoid zero-phasing the bubble)
- **Figure 5:** De-bubble workflow diagram
  - Show wavelet before/after de-bubble
  - Show amplitude spectrum (bubble ripple removed)

### 3.2 Designature (10 min)
- **Goal:** Compress or reshape source signature
- **Designature toolbox:**
  1. **Spiking deconvolution:** Compress to spike (rarely used — noise boosting)
  2. **Zero-phase conversion:** Convert to zero-phase equivalent (standard)
  3. **Shaping:** Match to target wavelet (4D matching)
- **Zero-phase conversion workflow:**
  1. Compute Fourier transform of input wavelet
  2. Zero the phase spectrum
  3. Design Wiener filter to match input → zero-phase target
  4. Apply filter
- **Trade-off:** Resolution vs. stability (pre-whitening)
- **Figure 6:** Designature workflow diagram
  - Show input wavelet → zero-phase wavelet
  - Show amplitude and phase spectra before/after

### 3.3 Deghosting (15 min)
- **Goal:** Remove source and receiver ghosts to fill spectral notches
- **Classical 1D approach:** Deterministic inverse filter (vertical ray assumption)
  - Problem: Fails at non-zero offset (ghost delay varies with angle)
  - Status: Rarely used alone
- **Modern methods:**
  1. **Bootstrap deghosting (tau-p domain):**
     - Transform to tau-p → ghost becomes simple time shift
     - Solve inverse problem → estimate ghost-free data
     - Inverse transform back to t-x
     - **Advantage:** Accounts for angle-dependent delays
  2. **Dual-sensor (PZ) deghosting:**
     - Record pressure (hydrophone) + particle velocity (geophone)
     - Ghosts have opposite polarity → sum cancels ghost
     - **Advantage:** Simple, robust, no inverse problem
  3. **Variable-depth streamer (BroadSeis):**
     - Tow cable at varying depths → notch diversity
     - Combine data from all depths → fill notches
     - **Advantage:** Achieves true broadband (6+ octaves)
  4. **Sparse deghosting (Li et al. 2020):**
     - Sparsity constraint in frequency-slowness domain
     - Simultaneous deghosting and denoising
  5. **Low-frequency deghosting (Amundsen & Zhou 2013):**
     - Trace-by-trace operator using integrated/differentiated pressure
     - Recovers low frequencies below first notch
- **Figure 7:** Deghosting methods comparison
  - Before/after amplitude spectra for different methods
  - Show notch filling
- **Figure 8:** Dual-sensor deghosting diagram
  - Show hydrophone and geophone responses
  - Show ghost polarity difference → summation cancels ghost

---

## Section 4: Land Data Processing — Model-Based Wavelet Processing (25 min)

### 4.1 Why Land Data Is Harder (3 min)
- **Four challenges specific to land:**
  1. Receiver coupling effects (geophone resonance, near-surface)
  2. Absorption (Q) — high-frequency loss with depth
  3. Non-white reflectivity (blueness or redness)
  4. Random noise distorting deconvolution operators
- Marine data has ghosts and bubble — but the wavelet is more consistent
- Land data has non-minimum-phase components that statistical deconvolution cannot fix
- **Figure 9:** Land vs. marine wavelet comparison
  - Show marine wavelet (airgun + ghost) vs. land wavelet (source + Q + geophone + instrument)

### 4.2 Receiver Effects and Absorption Recap (3 min)
- **Receiver effects:**
  - Geophones have resonance frequency (~10 Hz) → distorts low frequencies
  - Poor coupling in dry/loose soil → additional attenuation
  - Need to characterize and compensate for detector response
- **Absorption (Q):**
  - Exponential high-frequency loss: $A(f) \propto e^{-\pi f t / Q}$
  - Q-compensation corrects for this (covered in Term 2)
  - Typical land Q values: 15–50
- **Figure 10:** Receiver and Q effects on wavelet spectrum
  - Show geophone response curve
  - Show Q absorption curve
  - Show combined effect on wavelet spectrum

### 4.3 Coloured Reflectivity and Noise (5 min)
- **Non-white reflectivity:**
  - Statistical deconvolution assumes white reflectivity spectrum
  - Well logs show real reflectivity is "blue" (high-frequency dominated): $\text{Amplitude} \propto f^{C_{LR}}$
  - Solution: coloured deconvolution — adjust operator to match reflectivity color
  - Estimate $C_{LR}$ from well data or spectral slope analysis
- **Noise effects on deconvolution:**
  - The autocorrelation that deconvolution "sees": $\phi_{xx} = \phi_{ss} + \phi_{nn}$
  - This is **not** the wavelet spectrum — it is distorted by noise
  - As S/N decreases → minimum-phase wavelet from autocorrelation becomes distorted → phase errors
  - **Figure 11:** Noise distortion of deconvolution operator
    - Show signal spectrum, noise spectrum, and their sum
    - Show how derived minimum-phase wavelet changes with S/N

### 4.4 Why Surface-Consistent Deconvolution Is Not Enough (4 min)
- **SCD model:** $W(t) = S(t) * R(t) * O(t) * M(t)$
- SCD solves for surface-consistent components → partially addresses noise through spectral averaging
- **Three fundamental limitations:**
  1. Assumes minimum-phase wavelet → cannot correct non-minimum-phase components
  2. Does not model Q absorption explicitly
  3. Does not account for detector and instrument responses
- **Key insight:** After SCD, non-minimum-phase residuals remain in the wavelet
- **Figure 12:** SCD limitations diagram
  - Show wavelet components: source, Q, detector, instrument
  - Highlight which components SCD can and cannot address

### 4.5 Model-Based Wavelet Processing — Theory (5 min)
- **The MBWP model:**
  $$\text{Trace} = [\text{Source} * Q * \text{Reflectivity} + \text{Noise}] * \text{Detector} * \text{Instrument}$$
- **Wavelet decomposed into physical components:**
  $$W(t) = \underbrace{S(t)}_{\text{source}} * \underbrace{Q(t)}_{\text{absorption}} * \underbrace{D(t)}_{\text{detector}} * \underbrace{I(t)}_{\text{instrument}}$$
- **Key distinction:** MBWP does NOT assume minimum phase, white reflectivity, or no noise
- **Only two free parameters:** effective Q and signal-to-noise ratio
- **Source models by type:**
  - Vibroseis: Klauder wavelet (autocorrelation of filtered sweep)
  - Dynamite: first derivative of step function (buried) or surface radiation pattern
  - Airgun: far-field signature with ghost
- **Validation:** Compare model wavelets with VSP downhole recordings
- **Figure 13:** MBWP model diagram
  - Show convolutional model with all components
  - Show how model wavelet is assembled from physical components

### 4.6 MBWP Workflow and Comparison with SCD (5 min)
- **Three-step workflow:**
  1. **Construct initial model** — from instrument response, detector response, source signature (default Q=30, S/N=20 dB)
  2. **Estimate parameters** — fit model spectra to field data spectra, decompose Q and S/N surface-consistently
  3. **Build final operator** — reconstruct model with estimated Q and S/N, condition and export as filter
- **Production application:**
  $$\text{SC Decon} \rightarrow \textbf{MBWP filter} \rightarrow \text{NMO/DMO}$$
- **Advantages over SCD:**

| Feature | SCD | MBWP |
|---------|-----|------|
| Non-minimum-phase correction | ✗ | ✓ |
| Explicit Q modeling | ✗ | ✓ |
| Noise modeling | Partial (averaging) | ✓ |
| Detector/instrument response | ✗ | ✓ |
| Mixed-source consistency | Limited | ✓ |
| Free parameters | 4 (S, R, O, M) | 2 (Q, S/N) |

- **Mixed-source application:**
  - Before MBWP: crosscorrelation phase between vibroseis and dynamite shows significant rotation
  - After MBWP: phase flattens to near zero → consistent phase without overlapping recordings
- **Figure 14:** MBWP workflow diagram
  - Show 3-step process: initial model → parameter estimation → final operator
  - Show before/after spectra and phase
- **Figure 15:** Mixed-source phase consistency
  - Show crosscorrelation phase before/after MBWP correction

---

## Section 5: Robust Surface-Consistent Deconvolution (10 min)

### 5.1 Why Traditional SC Deconvolution Fails (3 min)
- Traditional SC decon uses L2 norm (least squares)
- Assumes Gaussian noise distribution
- **Problem:** Foothill areas have inconsistent noise (ground roll, bursts)
  - Non-Gaussian error distribution
  - Can affect up to 20% of traces
  - Result: Unstable operators, poor deconvolution
- **Figure 16:** Traditional vs. robust SC deconvolution comparison
  - Show operators for noisy data

### 5.2 Robust SC Deconvolution Approach (5 min)
- **Key innovation:** Hybrid L1/L2 norm optimization
  - L2 norm for signal
  - L1 norm for noise outliers
- **Result:** Unbiased results even with strong inconsistent noise
- **Three-step procedure:**
  1. Spectral analysis: Compute logarithmic spectrum for all traces
  2. Spectral decomposition: Extract source, receiver, CMP, offset components (L1/L2)
  3. Spectral application: Apply deconvolution operators
- **Advantages:**
  - Effective noise suppression at both high and low frequencies
  - Resolution improvement without noise amplification
  - Works for challenging foothill data
- **Figure 17:** Robust SC deconvolution flow diagram
  - Show three-step procedure
  - Show L1/L2 optimization

### 5.3 Field Data Example (2 min)
- **Example:** South China foothill data (Zhang & Yuan 2019)
  - Original: 8–55 Hz
  - After traditional SC decon: 6–65 Hz (modest improvement)
  - After robust SC decon: 4–90 Hz (25 Hz broadening at both ends)
- **Figure 18:** Field data example
  - Show shot gathers before/after
  - Show amplitude spectra
  - Show stack sections

---

## Summary and Q&A (5 min)

### Key Takeaways
1. **Broadband seismic** = 6+ octaves of bandwidth → better resolution, interpretation, inversion
2. **Marine processing flow:** De-bubble → Designature → Deghosting
3. **Modern deghosting methods:** Bootstrap, dual-sensor, variable-depth, sparse, low-frequency
4. **Land data challenges:** Receiver effects, absorption, coloured reflectivity, and noise all distort deconvolution
5. **MBWP:** Models the wavelet from physical components (source × Q × detector × instrument) — corrects non-minimum-phase residuals that SCD cannot address, using only two parameters (Q and S/N)
6. **Robust SC deconvolution:** L1/L2 optimization for challenging environments

### Questions for Students
1. Why is bandwidth measured in octaves, and why are 6+ octaves desirable?
2. What is the ghost notch frequency for a receiver at 8 m depth? How does this change at 30° offset?
3. Why do we de-bubble before zero-phasing? What happens if we reverse the order?
4. Compare bootstrap deghosting and dual-sensor (PZ) deghosting. What are the advantages and limitations of each?
5. What is the "blueness" of reflectivity, and how does it affect deconvolution?
6. Why does surface-consistent deconvolution fail to correct non-minimum-phase wavelet components? How does MBWP address this?
7. What are the two free parameters in MBWP, and how are they estimated from field data?
8. Why does traditional surface-consistent deconvolution fail in foothill areas? How does robust SC deconvolution solve this problem?

---

## Figures Summary

**Total figures:** 18

1. Broadband wavelet comparison (2, 3, 6 octaves)
2. Benefits diagram (wavelet → interpretation → inversion → AVO)
3. Ghost notch diagram (source and receiver ghosts)
4. Wave propagation effects diagram (source → propagation → receiver)
5. De-bubble workflow diagram
6. Designature workflow diagram
7. Deghosting methods comparison (before/after spectra)
8. Dual-sensor deghosting diagram
9. Land vs. marine wavelet comparison
10. Receiver and Q effects on wavelet spectrum
11. Noise distortion of deconvolution operator (signal + noise spectra, minimum-phase wavelet vs. S/N)
12. SCD limitations diagram (which wavelet components SCD can/cannot address)
13. MBWP model diagram (convolutional model with all physical components)
14. MBWP workflow diagram (3-step process: initial model → parameter estimation → final operator)
15. Mixed-source phase consistency (crosscorrelation phase before/after MBWP)
16. Traditional vs. robust SC deconvolution comparison
17. Robust SC deconvolution flow diagram
18. Field data example (south China foothill)

---

## References

### Textbooks
- Monk, D. J. (2020). *Survey Design and Seismic Acquisition*. SEG Distinguished Instructor Short Course No. 23. Chapter 2.

### Journal Papers
- Amundsen, L., & Zhou, H. (2013). Low-frequency seismic deghosting. *Geophysics*, 78(2), WA15–WA20.
- Li, H.-J., Yang, Q.-Y., & Cai, J.-X. (2020). Simultaneous receiver-side deghosting and denoising. *Applied Geophysics*, 17(3), 411–418.
- Ghosh, S. K. (2000). Deconvolving the ghost effect. *Geophysics*, 65(6), 1831–1836.
- Lindsey, J. P. (1960). Elimination of seismic ghost reflections. *Geophysics*, 25(1), 130–140.
- Zhang, Y., & Mo, Y. (2019). Robust Deconvolution for foothill seismic data. *SEG Workshop*.

### Training Materials
- CGG ODT04 Deconvolution (2015). Parts 1–3.
- Hart, D., & Hootman, B. (2008). Achieving Consistent and Stable Phase with Mixed-Source Surveys (MBWP Update 2008). WesternGeco.
- Hootman, B., & Abitbol, M. (2008–2009). MBWP Model Equations and Workflow Steps 1–3. WesternGeco.
- Brown, D. DP3 MBWP Module. WesternGeco training materials.
