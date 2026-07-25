---
title: Source signature and designature
status: draft
tags: [source-signature, designature, airgun, bubble, de-bubble, zero-phase, marine]
related_sources:
  - cgg_odt04_deconvolution_part1_wavelet
  - cgg_odt04_deconvolution_part2_signature
  - monk_2020_broadband_seismic
---

# Source Signature and Designature

## Definition

The **source signature** is the time-domain waveform emitted by the seismic source. In marine seismic acquisition, the airgun array signature is a major component of the recorded wavelet. **Designature** is the process of removing or reshaping the source signature to improve resolution and remove undesirable features (bubble oscillation, source ghost).

Designature is a type of **deterministic deconvolution**: we know (or can model) the source signature, so we can design an inverse filter to remove its effect.

## Airgun Source Signature

### Bubble Oscillation

When an airgun fires, it releases a high-pressure air bubble into the water. The bubble expands, overshoots equilibrium, and oscillates. This creates a signature with:
- A sharp initial peak (the "pulse")
- Oscillatory "bubble energy" that decays over time

**Bubble period** depends on gun volume and firing pressure:

$$T_{\text{bubble}} \propto \frac{V^{1/3}}{P^{1/2}}$$

where:
- $V$ = gun volume (typically 10–200 in³)
- $P$ = firing pressure (typically 2000–3000 psi)

Larger guns and lower pressures produce longer bubble periods.

### Array Design

Modern airgun arrays use multiple guns of different sizes fired at different times so that:
- The initial peaks **sum constructively** (all guns fire within ~1 ms)
- The bubble oscillations **destructively interfere** (guns are tuned to cancel each other's bubble energy)

This is called a **tuned array**. The result is a **vertical source signature** (equivalent point-source for vertical rays) with reduced but non-zero residual bubble energy.

### Vertical Source Signature

The vertical source signature is the combined output of the airgun array, modeled as a point source for vertically traveling energy. It includes:
- The initial pulse
- Residual bubble oscillation (not fully canceled)
- Recording system response (hydrophone, filters, etc.)

### Far-Field Signature

The **far-field signature** is the source signature convolved with the **source ghost**:

$$\text{Far-field} = \text{Source signature} * \text{Source ghost}$$

The source ghost is a delayed, polarity-reversed copy from the sea-surface reflection. For a source at depth $d_s$:

$$g_s(t) = \delta(t) - \delta(t - \Delta t_s)$$

where $\Delta t_s = 2d_s / v_w$ is the source ghost delay.

The far-field signature is typically delivered with the seismic data (measured or modeled by the acquisition contractor).

## Designature

### Goals

1. **Compress the source signature** to improve temporal resolution
2. **Remove bubble oscillation** to eliminate false events and improve wavelet shape
3. **Remove source ghost** (if possible) to recover low frequencies
4. **Convert to zero-phase** for easier interpretation

### Designature Toolbox

| Method | Goal | Approach | Typical Use |
|--------|------|----------|-------------|
| **Spiking deconvolution** | Compress to a spike | Deterministic inverse filter | Rarely used alone (noise boosting) |
| **Zero-phase conversion** | Convert to zero-phase | Wiener shaping filter | Standard processing |
| **Shaping** | Match to target wavelet | Amplitude and/or phase shaping | 4D wavelet matching |
| **De-bubble** | Remove bubble oscillation | Deterministic inverse of bubble model | Before zero-phasing |
| **De-ghost** | Remove source/receiver ghosts | Inverse of ghost operator | Broadband processing |

### De-Bubble

**Goal:** Remove the bubble oscillation from the wavelet.

**Why?** Bubble energy creates oscillatory tails in the wavelet, which:
- Reduce temporal resolution
- Create false "events" that can be confused with multiples
- Contaminate the zero-phasing operator if not removed first

**Method:**
1. Model the bubble signature (from gun parameters or measured data)
2. Design a deterministic inverse filter to remove the bubble
3. Apply the filter to the data

**Flow:**
```
Raw wavelet → De-bubble operator → De-bubbled wavelet
```

**Key insight:** If bubble energy is present, a zero-phasing operator designed on the raw wavelet will try to zero-phase the bubble, creating artifacts. Better to **de-bubble first, then zero-phase**.

**Practical note:** De-bubble must be applied **before amplitude recovery** (Q-compensation, divergence correction).

### Zero-Phase Conversion

**Goal:** Convert the wavelet to zero-phase (symmetric, centered on the reflection event).

**Method:**
1. Compute the Fourier transform of the input wavelet
2. Zero the phase spectrum (keep amplitude spectrum)
3. Design a Wiener filter to match input → zero-phase target
4. Apply the filter

**Result:** Zero-phase wavelet with the same amplitude spectrum as the input (but no bubble or ghost artifacts if de-bubbled first).

**Why zero-phase?**
- Easier to interpret (event time = wavelet center)
- Better for well ties and inversion
- Symmetric wavelet has minimal side lobes (if bandwidth is sufficient)

### Spiking Deconvolution (Deterministic)

**Goal:** Compress the wavelet to a spike (maximum resolution).

**Method:**
1. Take the Fourier transform of the wavelet $W(f)$
2. Compute the inverse spectrum: $1/W(f)$
3. Apply pre-whitening to avoid noise amplification at notches:
   $$H(f) = \frac{W^*(f)}{|W(f)|^2 + \varepsilon^2}$$
   where $\varepsilon^2$ is the pre-whitening constant
4. Inverse Fourier transform to get the spiking operator
5. Apply to the data

**Problem:** Spiking deconvolution amplifies frequencies at **ghost notches**, massively boosting noise. The ghost notches move with offset (angle-dependent), so a 1D operator designed on the vertical far-field signature will not work at all offsets.

**Status:** Rarely used for marine data. Zero-phase conversion is preferred.

### Shaping (Wavelet Matching)

**Goal:** Match the input wavelet to a desired target wavelet.

**Applications:**
- **4D wavelet matching** — make two surveys have the same wavelet for time-lapse analysis
- **Amplitude-only shaping** — whitening, blueing, reddening (change spectrum, keep phase)
- **Phase-only conversion** — minimum → zero phase (change phase, keep spectrum)

**Method:**
1. Specify input wavelet $W_{\text{in}}(f)$ and target wavelet $W_{\text{target}}(f)$
2. Design Wiener filter to match input → target:
   $$H(f) = \frac{W_{\text{in}}^*(f) W_{\text{target}}(f)}{|W_{\text{in}}(f)|^2 + \varepsilon^2}$$
3. Apply the filter

**Trade-off:** Shaping to a broader wavelet gives higher resolution but may amplify noise. Shaping to a narrower wavelet is more stable but lower resolution.

## Practical Workflow (Marine)

### Typical Designature Flow

1. **Input:** Raw recorded wavelet (or far-field signature)
2. **QC:** Check source signature, bubble energy, ghost notches
3. **De-bubble:** Remove bubble oscillation (if significant)
4. **Zero-phase conversion:** Convert to zero-phase equivalent
5. **Output:** Zero-phase, de-bubbled wavelet

### For Deghosting

If full deghosting is needed (to recover low frequencies), see [Marine deghosting](marine_deghosting.md). Methods include:
- **Bootstrap deghosting** (tau-p domain inverse problem)
- **Dual-sensor (PZ) deghosting** (hydrophone + geophone)
- **Variable-depth streamer** (BroadSeis)
- **Sparse deghosting** (sparsity-constrained inversion)

### Order of Operations

1. **De-bubble** — before amplitude recovery
2. **Designature** (zero-phase) — after de-bubble
3. **Deghost** — after designature (if needed)
4. **Q-compensation** — after deghost
5. **Predictive deconvolution** — after Q-compensation

## Practical Considerations

### Filter Length

- Longer operators allow more freedom to match input → output
- But longer operators may overfit noise
- Typical designature operators: 100–400 ms, depending on wavelet complexity

### Pre-Whitening

- Dampens extreme boosting at notches
- Reduces bandwidth (trade-off between resolution and stability)
- Typical values: 0.1–1% of maximum amplitude

### Polarity and Phase QC

After designature, check:
- **Polarity:** Does a positive impedance contrast correspond to a positive (or negative) peak?
- **Phase:** Is the wavelet zero-phase? (symmetric, no time shift)
- **Bubble:** Is the bubble oscillation removed? (no oscillatory tails)

### SOD (Start of Data) and Gun/Cable Statics

Before designature, apply:
- **SOD correction** — align time-zero with source firing time
- **Gun/cable statics** — correct to sea surface (required before SRME and depth migration)

After zero-phasing, the main peak/trough should align with the water-bottom reflection.

## Teaching Intuition

- The source signature is **not a spike**: it has bubble energy and is convolved with the source ghost
- Designature removes or reshapes these features to improve resolution
- **De-bubble before zero-phasing** to avoid zero-phasing the bubble
- Spiking deconvolution is rarely used alone: noise boosting at ghost notches is too severe
- Zero-phase conversion is the standard approach for marine data

## Related Concepts

- [Seismic wavelet](seismic_wavelet.md) — wavelet components and properties
- [Broadband seismic](broadband_seismic.md) — bandwidth, resolution, and octaves
- [Marine deghosting](marine_deghosting.md) — removing source and receiver ghosts
- [Deterministic deconvolution](deterministic_deconvolution.md) — inverse filtering with known wavelet
- [Minimum phase wavelet](minimum_phase.md) — phase properties and conversion

## Sources

- [CGG ODT04 Part 1](../sources/cgg_odt04_deconvolution_part1_wavelet.md) — source signature and ghost physics
- [CGG ODT04 Part 2](../sources/cgg_odt04_deconvolution_part2_signature.md) — designature workflows and toolbox
- [Monk (2020)](../sources/monk_2020_broadband_seismic.md) — broadband acquisition and processing overview
