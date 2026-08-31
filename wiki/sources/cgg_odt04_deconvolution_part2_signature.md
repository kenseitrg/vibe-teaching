---
title: CGG ODT04 Part 2 — Signature Deconvolution
type: training slides
year: 2015
author: CGG (internal training)
source_file: papers/deconvolution/ODT04_DECONVOLUTION_PART2_v7.0_signature_decon.pptx
status: reviewed
tags: [designature, de-bubble, deghosting, zero-phase, signature-deconvolution, marine]
---

# CGG ODT04 Part 2 — Signature Deconvolution

## Source

- **Author:** CGG UK Training
- **Title:** ODT04 Deconvolution Part 2: Signature Deconvolution
- **Version:** 7.0, June 2015
- **Type:** Internal training slides
- **File:** `papers/deconvolution/ODT04_DECONVOLUTION_PART2_v7.0_signature_decon.pptx`

**Note:** Internal CGG training document; images do not have show rights. Use for understanding and structure; cite external papers for published materials.

## Main message

Signature deconvolution encompasses a family of deterministic wavelet-shaping operations — de-bubble, designature, zero-phasing, and deghosting — that transform the raw recorded wavelet into a desired target wavelet. The designature toolbox uses least-squares Wiener filtering to convert any known input wavelet into any desired output, but the practical challenge is balancing resolution, signal-to-noise ratio, and wavelet shape.

## Key points

### 1. Spiking signature deconvolution

- Given a known wavelet (e.g., far-field signature), design a least-squares operator to convert it to a spike.
- Operator design in frequency domain: take reciprocal of amplitude spectrum, negate phase spectrum.
- **Problem:** spiking deconvolution amplifies frequencies at ghost notches, massively boosting noise.
- Ghost notches move with angle, so a 1D operator designed on the vertical far-field signature will misalign with real data notches.
- Pre-whitening dampens extreme boosting but reduces bandwidth, compromising the spike target.

### 2. Zero-phase conversion

- Design an operator that preserves amplitude spectrum but zeros the phase spectrum.
- Two approaches: (1) create zero-phase equivalent wavelet, then design Wiener shaping filter; (2) design operator directly in Fourier domain.
- **De-bubble before zero-phasing:** if bubble energy is present in the input wavelet, the zero-phase operator will try to zero-phase the bubble. Better to remove bubble first, then zero-phase.
- Flow: input wavelet → de-bubble operator → zero-phase operator → final zero-phase, bubble-free wavelet.

### 3. De-bubble workflow

- De-bubble operator removes bubble oscillation from the wavelet.
- Design: model the bubble component, create inverse filter.
- After de-bubble: wavelet has no bubble, associated spectral ripple disappears.
- **Key insight:** de-bubble must be applied before amplitude recovery (Q-compensation, divergence correction).

### 4. Designature toolbox

The designature toolbox includes:
- **Spiking deconvolution:** compress wavelet to spike (rarely used alone due to noise).
- **Shaping/matching:** convert input wavelet to arbitrary target (amplitude-only, phase-only, or both).
- **Phase conversion:** zero-phase, minimum-phase equivalents.
- **Whitening/blueing/reddening:** amplitude shaping with same phase.
- **4D wavelet matching:** match one survey's wavelet to another.

### 5. Pre-migration deghosting (bootstrap method)

- **Problem:** receiver ghost is variable with offset/angle; 1D designature cannot remove it.
- **Bootstrap approach:** use tau-p domain inverse problem.
  1. Transform data to tau-p space.
  2. Model: data = upgoing primary + downgoing ghost (mirror image at negative datum).
  3. Solve inverse problem: given data and forward model, estimate ghost-free data in tau-p.
  4. Inverse transform to t-x to get deghosted data.
- Can extend to include demultiple (water-layer reverberations) in the same inversion.
- **Advantage:** with correct a priori information (cable geometry, water depth), can modify forward model to account for variable-depth streamer, 3D effects.

### 6. Filter length effects

- Longer filters allow more freedom to match input to output wavelet.
- But longer filters may overfit noise or create artifacts.
- Typical designature operators: 100-400 ms, depending on wavelet complexity.

### 7. Practical QC: SOD, gun/cable statics, polarity

- **Start of Data (SOD) delay:** static shift to align time-zero with source firing time.
- **Gun/cable statics:** correct to sea surface (required before SRME and depth migration).
- **Polarity statement:** after zero-phasing, clearly state whether positive impedance increase corresponds to positive or negative sample values.
- **QC:** after SOD + zero-phasing + NMO, water bottom should match autocorrelation trough.

## Key equations

**Ghost notch frequency:**
```
f_notch = n · v_water / (2 · depth)     for n = 0, 1, 2, ...
```

**Least-squares operator design:**
Minimize L = Σ(actual_output - desired_output)²

**Wiener filter in frequency domain:**
```
H(f) = W*(f) / (|W(f)|² + ε²)
```
where W(f) is input wavelet spectrum, ε² is pre-whitening constant.

## Practical implications

- **Marine processing flow:** typical designature sequence is: raw wavelet → de-bubble → zero-phase (or spiking decon with caution).
- **Deghosting:** for conventional fixed-depth streamer, use bootstrap (tau-p inverse) or similar methods; for variable-depth streamer (BroadSeis), deghosting is built into acquisition.
- **Trade-offs:** spiking decon gives highest resolution but amplifies noise; shaping to a broader wavelet is more stable but lower resolution.
- **QC is essential:** always check SOD, polarity, and water-bottom alignment before proceeding.

## Implications for teaching

- Excellent source for understanding the designature toolbox and the trade-offs involved.
- Explains why spiking decon is rarely used alone: noise boosting at ghost notches.
- Provides concrete workflow diagrams (slide 73) showing the complete designature flow.
- Bootstrap deghosting (slides 59-70) gives a clear inverse-problem formulation suitable for advanced students.

## Concepts informed

- [Marine deghosting](../concepts/marine_deghosting.md)
- [Broadband seismic](../concepts/broadband_seismic.md)
- [Source signature and designature](../concepts/source_signature_designature.md)
- [Deterministic deconvolution](../concepts/deterministic_deconvolution.md)
- [Seismic wavelet](../concepts/seismic_wavelet.md)

## Quotes / memorable lines

> "Deconvolution undoes the effects of a convolution, hence the name. It is an inverse filter."

> "Spiking deconvolution designed on a fixed 1D wavelet will also try and fill the ghost notches, massively boosting the noise in these frequency ranges. The notches in the real data will move with angle and will thus misalign with the notch in the 1D operator."

> "So on real data spiking deconvolution is rarely used to compress the whole wavelet, because it is hard to get the right balance of S/N, resolution and wavelet shape, so we effectively end up compromising all three."

> "We have a raw wavelet which: is not zero phase; has large side lobes mainly due to the band limitation of the gun and cable notches; has undesirable features such as the bubble energy; is different for different propagation angles."

> "We want a wavelet which: is zero phase; has as high resolution as possible; does not have any undesirable features such as the bubble energy; is the same for all propagation effects."

## Summary workflow (slide 73)

```
Raw seismic wavelet
  ↓
De-bubble (remove bubble oscillation)
  ↓
Zero-phase conversion (or spiking decon with caution)
  ↓
Deghosting (bootstrap / tau-p inverse / dual-sensor / variable-depth)
  ↓
Final: zero-phase, broadband, ghost-free wavelet
```

**Designature options:**
- Input wavelet → target wavelet (shape A-B, amplitude only, amplitude+phase, phase only)
- White noise addition (pre-whitening)
- Bootstrap deghosting, PZ sum, redatuming, joint deconvolution
