---
title: Term 3 Lecture 05 — Broadband Processing
status: draft
term: 03
lecture: 05
---

# Broadband Processing

## Learning objectives

By the end of this lecture you should be able to:

- Define broadband seismic data in terms of octave count and explain why 6+ octaves are desirable.
- Calculate ghost notch frequencies for a given source or receiver depth and explain how they limit bandwidth.
- Describe the marine processing chain: de-bubble → deghosting → designature, and explain why the order matters.
- Compare at least three modern deghosting methods (bootstrap, dual-sensor, variable-depth streamer, sparse, low-frequency) and state the key advantage of each.
- Explain why land data is harder to deconvolve than marine data and identify the four main challenges.
- Describe the MBWP wavelet model, its two free parameters (Q and S/N), and how it corrects non-minimum-phase residuals that surface-consistent deconvolution cannot address.
- Explain why conventional surface-consistent deconvolution fails when the near-surface is complex and the signal-to-noise ratio is relatively low, and how robust L1/L2 optimization solves the problem.

## Prerequisites

- Term 1 Lecture 06: convolutional model, Wiener filter, minimum-phase wavelets, prediction-error filter.
- Term 1 Lecture 07: surface-consistent deconvolution model and decomposition.
- Term 2: Q-compensation (absorption), FK and tau-P transforms.
- Term 3 Lecture 04: adaptive noise attenuation concepts.

## 0. Why this lecture matters

In Term 1 we learned that deconvolution reshapes the embedded wavelet to sharpen reflections. But conventional deconvolution — whether statistical (spiking, predictive) or surface-consistent — operates on a wavelet that is already band-limited by ghosts, bubble energy, absorption, and instrument effects. It can compress what is there, but it cannot create what is missing.

Modern seismic exploration demands more. Subtle stratigraphic traps, thin reservoirs, and complex lithologies require seismic images with 6+ octaves of usable bandwidth — roughly 2-128 Hz, compared to the 2–3 octaves (e.g., 10–60 Hz) typical of conventional data. Achieving this requires **advanced deconvolution techniques** that explicitly model and remove each wavelet component: the source bubble, the ghost notches, the absorption, the detector response.

This lecture covers two complementary domains. For **marine data**, we follow the processing chain de-bubble → deghosting → designature, which attacks the source and receiver wavelet components in sequence. For **land data**, where the wavelet is more complex and less consistent, we introduce **Model-Based Wavelet Processing (MBWP)** — a method that assembles the wavelet from physical components (source, Q, detector, instrument) and corrects non-minimum-phase residuals that no statistical method can reach. We close with **robust surface-consistent deconvolution**, which extends the classical decomposition to handle the inconsistent noise that appears whenever the near-surface is complex and the signal-to-noise ratio is relatively low — a situation typical of foothill and mountain surveys, but not limited to them.

## 1. Introduction to broadband seismic

### 1.1 What is broadband seismic?

Broadband seismic data is defined by the number of **octaves** of usable bandwidth:

$$ N_\text{octaves} = \log_2\left(\frac{f_{\max}}{f_{\min}}\right) $$

An octave is a factor of two in frequency. Conventional marine data typically spans 10–60 Hz — about 2.6 octaves. Broadband data targets 2-128 Hz — about 6 octaves. The difference is dramatic:

| Data type | Bandwidth | Octaves | Wavelet character |
|-----------|-----------|---------|-------------------|
| Conventional | 10–60 Hz | ~2.6 | Oscillatory, strong side lobes |
| Broadband | 2-128 Hz | 6 | Sharp, impulsive, minimal side lobes |

Why octaves? Because the wavelet's **side lobe amplitude** is controlled by relative bandwidth (octave count), not absolute bandwidth. High frequencies control the central lobe width (resolution); low frequencies control the side lobe amplitude (isolation). A 6-octave wavelet has dramatically lower side lobes than a 3-octave wavelet, even if both have the same highest frequency.

The wavelet lobe width follows:

$$ L_w \propto \frac{2}{f_{\max} - f_{\min}} $$

So extending the low end from 10 Hz to 1 Hz — while keeping $f_{\max} = 60$ Hz — narrows the lobe from $2/50 = 0.04$ s to $2/59 \approx 0.034$ s. More importantly, it suppresses the ringing side lobes that mask thin beds and subtle impedance contrasts.

![](figures/term03_lec05/term03_lec05_wavelet_octave_comparison.png){width=90%}

**Figure 1.** *Wavelet comparison across octave counts. Three zero-phase Ormsby wavelets (2, 3, and 6 octaves) that share the same 64-80 Hz high end, shown in the time domain with their amplitude spectra. Because the high frequencies are identical, the central-lobe width (vertical resolution) barely changes; adding low octaves instead collapses the side lobes, improving event isolation. This is the visual signature of broadband data.*

### 1.2 Benefits of broadband data

Broader bandwidth improves every downstream task:

- **Resolution.** Sharper wavelets resolve thinner beds. The minimum resolvable thickness (tuning thickness) decreases as bandwidth increases.
- **Interpretation.** Low-frequency content reveals impedance layering, subtle fluid contacts, and fault planes that are invisible in conventional data. The seismic image looks more "geological."
- **Inversion.** Seismic inversion requires low frequencies to constrain the background impedance trend. With 6+ octaves extending to ~1–2 Hz, the gap that must be filled by the initial model shrinks to 0–1 Hz — reducing model dependence.
- **AVO.** Ghost removal produces more consistent amplitude-versus-offset behavior, because the ghost modulation varies with angle and contaminates the true AVO response.
- **Deep imaging.** Low frequencies are less affected by absorption ($A \propto e^{-\pi f t / Q}$), so they penetrate deeper through attenuative layers (salt, basalt, chalk).

![](figures/term03_lec05/term03_lec05_bandwidth_resolution.png){width=90%}

**Figure 2.** *Resolution benefit of bandwidth extension. Acoustic (P-)impedance $Z = \rho v$ derived by seismic inversion: **extended bandwidth (left)** versus the **original, conventional bandwidth (right)**. Broadening the usable band — at the high-frequency end in this example — sharpens the impedance contrasts and resolves thinner layers that merge together in the original. This is the resolution side of the bandwidth story: as Figure 1 showed, high frequencies sharpen the central lobe (vertical resolution) while low frequencies suppress the side lobes (event isolation).

## 2. What limits bandwidth: the wavelet components

### 2.1 The convolutional chain

The raw recorded seismic trace is built from a chain of convolutions:

$$ x(t) = s_s(t) * r_r(t) * h_h(t) * c_c(t) * r(t) + n(t) $$

where each component shapes the wavelet:

| Component | Effect | Domain |
|-----------|--------|--------|
| Source signature $s_s(t)$ | Airgun bubble, source ghost | Marine |
| Propagation / Q | High-frequency absorption | All |
| Receiver ghost | Spectral notches | Marine |
| Detector response | Geophone resonance, coupling | Land |
| Instrument filter | Anti-alias, recording filters | All |
| Near-surface | Weathering, coupling | Land |

For marine data, the dominant limitations are the source bubble and the ghost notches. For land data, the wavelet is a more complex mixture of source type, absorption, geophone response, and coupling — and it varies from trace to trace.

### 2.2 Why conventional deconvolution falls short

Recall from Term 1 Lecture 06 that statistical deconvolution (spiking, predictive) makes strong assumptions:

1. **White reflectivity** — the reflectivity spectrum is flat.
2. **Minimum-phase wavelet** — all energy is front-loaded.
3. **White noise** — the autocorrelation of the trace equals the autocorrelation of the wavelet.
4. **Stationarity** — the wavelet does not change within the design window.

These assumptions are violated in practice:

- Real reflectivity can be **colored** (typically "blue" — enriched in high frequencies).
- The wavelet contains **non-minimum-phase components** (ghosts, geophone response, instrument filters).
- **Noise** distorts the autocorrelation, leading to phase errors in the derived operator.
- The wavelet is **non-stationary** due to absorption (Q) — high frequencies are lost with depth.

Surface-consistent deconvolution (Term 1 Lecture 07) partially addresses noise through spectral averaging across traces, but it still assumes minimum phase and cannot correct non-minimum-phase residuals. We need methods that explicitly model each physical component.

![](figures/term03_lec05/term03_lec05_wavelet_components.png){width=60%}

**Figure 3.** *Factors that shape the recorded wavelet. This cartoon depicts the physical effects that act on the seismic wave as it travels from source to receiver — the source signature (bubble energy and the source ghost), propagation through the earth (absorption/$Q$ and scattering), the receiver ghost, and the detector, instrument, and near-surface responses. In the convolutional model above, each of these is one link in the chain: in the frequency domain they multiply the spectrum, so every factor leaves its own imprint on the wavelet's amplitude and phase.*

## 3. Marine broadband processing

Marine data has a well-characterized wavelet: the source signature is measured or modeled, the ghost geometry is known (source depth, cable depth, water velocity). This makes **deterministic** processing possible. The standard chain is:

$$ \text{Raw wavelet} \xrightarrow{\text{De-bubble}} \xrightarrow{\text{Deghosting}} \xrightarrow{\text{Designature}} \text{Broadband, minimum-phase wavelet} $$

This ordering — de-bubble, then deghosting, then de-signature as the final wavelet-shaping step — is the standard modern marine broadband workflow (Bekara et al., 2025).

### 3.1 De-bubble

**Goal:** Remove bubble oscillation from the source signature.

When an airgun fires, the compressed air forms a bubble that oscillates before dissipating. This oscillation creates a long, ringing tail on the source wavelet — false events that degrade resolution and can be confused with short-period multiples.

The de-bubble operator is a **deterministic inverse filter** designed from a physical model of the bubble. The workflow is:

1. Model or measure the bubble component of the source signature.
2. Design an inverse filter that compresses the bubble tail.
3. Apply the filter to the source signature (or directly to the data if the source wavelet is embedded).

After de-bubble, the wavelet has no oscillatory tail and the associated spectral ripple disappears from the amplitude spectrum.

**Critical ordering rule:** De-bubble is the **first** wavelet-processing step — it must be applied **before** deghosting and designature. If you designature first, the shaping operator matches the bubble oscillation along with the primary, embedding the bubble artifacts into the output instead of removing them.

Similarly, de-bubble must precede amplitude recovery (Q-compensation, spherical divergence correction), because those processes amplify the bubble tail along with the signal.

![](figures/term03_lec05/term03_lec05_debubble.png){width=90%}

**Figure 4.** *De-bubble, modeled with a Berlage source wavelet $p(t) = t^n e^{-\alpha t}\sin(2\pi f_0 t)$ — a causal source pulse. The raw airgun signature (top row) is this pulse convolved with a decaying bubble pulse train $g(t) = \sum_k r^k\,\delta(t - kT_b)$. In the time domain (a) the re-radiated echoes form a ringy tail; in the frequency domain (b) the bubble train acts as a comb filter, producing ripples spaced by $1/T_b$. De-bubble applies the inverse of $g(t)$ and recovers the clean Berlage pulse: the tail disappears (c) and the spectrum is flattened (d).*

### 3.2 Deghosting

**Goal:** Remove source and receiver ghosts to fill the spectral notches and recover the full bandwidth.

Deghosting is the key step that distinguishes broadband processing from conventional processing. Without deghosting, the ghost notches permanently remove bands of frequencies from the data — no amount of statistical deconvolution can recover them. To understand what deghosting must undo, we first look at where these notches come from.

#### 3.2.1 Where the notches come from

What limits the bandwidth of conventional marine data? The primary culprit is the **ghost** — a reflection from the sea surface that arrives shortly after the primary signal with opposite polarity.

Consider a source at depth $d_s$ below the sea surface. The direct downgoing wave is accompanied by an upgoing reflection from the sea surface (reflection coefficient $R \approx -1$). This creates a ghost arrival delayed by:

$$ \Delta t_s = \frac{2 d_s \cos\theta}{v_w} $$

where $\theta$ is the propagation angle and $v_w \approx 1500$ m/s is the water velocity. The same effect occurs at the receiver (streamer at depth $d_r$):

$$ \Delta t_r = \frac{2 d_r \cos\theta}{v_w} $$

In the frequency domain, the ghost acts as a **comb filter**. For vertical incidence ($\theta = 0$), the ghost transfer function is:

$$ G(f) = 1 - e^{-i 2\pi f \Delta t} $$

with amplitude spectrum:

$$ |G(f)| = 2\left|\sin\left(\frac{\pi f \Delta t}{1}\right)\right| = 2|\sin(\pi f \Delta t)| $$

This produces **spectral notches** (zeros) at frequencies:

$$ f_n = \frac{n \cdot v_w}{2d}, \quad n = 0, 1, 2, \ldots $$

For a streamer at 6 m depth: the first non-zero notch is at $f_1 = 1500/(2 \times 6) = 125$ Hz. But the source at 6 m depth also creates notches at 125 Hz. The combined source + receiver ghost system creates deep notches throughout the spectrum, with the most damaging effect at low frequencies where the first notch of the combined system suppresses everything below ~60–80 Hz.

Crucially, the notch frequency **increases with offset** (because $\cos\theta$ decreases): the notches are not fixed in frequency but migrate upward as the propagation angle grows (Figure 5b). The entire notch pattern is therefore set by the acquisition geometry — source depth, cable depth, and offset. This raises the obvious question: can we simply invert the ghost filter and divide the notches out?

![](figures/term03_lec05/term03_lec05_ghost_notch.png){width=90%}

**Figure 5.** *Ghost notch diagram. Both source and receiver ghosts act as the same two-path interference filter $G(f) = 1 - e^{-i2\pi f \Delta t}$ with $\Delta t = 2d\cos\theta/v_w$, so the analysis below applies to either one. (a) **Depth sets the notch frequency** (vertical incidence, $\theta = 0$): the first notch is at $f_1 = v_w/(2d)$, so doubling the depth from 6 m to 12 m halves it from 125 Hz to 62.5 Hz. (b) **Offset shifts the notches higher**: at non-zero propagation angle the delay shrinks by $\cos\theta$, so the first notch migrates upward (62.5 Hz at $\theta = 0^\circ$ → 125 Hz at $\theta = 60^\circ$ for $d = 12$ m). This angle dependence is why a 1-D deghosting operator designed for vertical incidence misaligns with the real notches at far offsets.*


#### 3.2.2 Why 1-D deghosting fails

The simplest approach is to design a deterministic inverse of the ghost filter:

$$ H_\text{deghost}(f) = \frac{1}{G(f)} = \frac{1}{1 - e^{-i2\pi f \Delta t}} $$

For vertical incidence, this works — but at the notch frequencies, $|G(f)| = 0$ and the inverse is infinite. Pre-whitening prevents division by zero, but leaves deep residual notches. Worse, because the notch frequencies shift with offset (Figure 5b), a single operator designed for vertical incidence **misaligns** with the actual notches at far offsets — no fixed 1-D filter can match the whole gather.

This is why modern deghosting methods work in domains where the angle dependence is handled explicitly.

#### 3.2.3 Bootstrap deghosting (tau-P domain)

The bootstrap method transforms the problem to the tau-P domain, where each plane-wave component has a well-defined slowness $p = \sin\theta/v_w$ and therefore a well-defined ghost delay:

$$ \Delta t(p) = \frac{2d}{v_w}\sqrt{1 - (p \cdot v_w)^2} $$

The workflow:

1. Transform data to tau-P domain.
2. For each slowness $p$, the ghost is a simple time shift with known delay $\Delta t(p)$ and reflection coefficient $R \approx -1$.
3. Solve the inverse problem: estimate the ghost-free upgoing wavefield.
4. Inverse transform back to t-x.

**Advantage:** Handles angle-dependent ghost delays exactly. Can be extended to variable-depth streamers and combined with demultiple in the same inversion.

**Limitation:** Requires accurate water depth and cable geometry. Tau-P transform introduces edge effects and requires regularization.

#### 3.2.4 Dual-sensor (PZ) deghosting

Dual-sensor streamers record both **pressure** (hydrophone) and **vertical particle velocity** (geophone or accelerometer). The key physics: for the upgoing primary wavefield, pressure and velocity have the **same sign**; for the downgoing ghost, they have **opposite signs**.

Summing the two sensor outputs with appropriate scaling cancels the ghost:

$$ P + \rho v_w V_z = 2 \cdot P_\text{upgoing} $$

**Advantage:** Simple, robust, no inverse problem. Works trace-by-trace.

**Limitation:** The geophone signal-to-noise ratio is poor at low frequencies (below ~10 Hz), so the summation is typically only effective above 10 Hz. Does not recover the very low frequencies that modern broadband targets.

#### 3.2.5 Sparse deghosting (Li et al., 2020)

This method formulates deghosting as a **sparse inversion** in the frequency-slowness domain. The recorded data is modeled as:

$$ d = G \cdot V \cdot u + \text{noise} $$

where $G$ is the ghost operator (angle-dependent), $V$ is the inverse slowness transform, and $u$ is the ghost-free wavefield. The solution minimizes:

$$ \min_u \|d - GVu\|_2^2 + \lambda \|u\|_1 $$

The L1-norm promotes sparsity, which simultaneously suppresses noise and stabilizes the inversion near notch frequencies. The FISTA algorithm provides fast convergence (10–30 iterations).

**Advantage:** Simultaneous deghosting and denoising in one step. Angle-dependent ghost operator computed exactly for each slowness.

**Limitation:** Assumes the wavefield is sparse in the frequency-slowness domain. Requires accurate streamer depth and water velocity.

#### 3.2.6 Low-frequency deghosting (Amundsen & Zhou, 2013)

This trace-by-trace method targets the low-frequency band below the first notch, where conventional methods struggle with S/N. The deghosted pressure field is approximated as:

$$ U^\text{DG}(t) \approx U(t) + \frac{c}{2z}\int_0^t U(t')\,dt' + \frac{z}{6c}\frac{\partial U(t)}{\partial t} $$

That is: the deghosted field equals the pressure plus a scaled time integral plus a scaled time derivative. This simple formula is effective up to approximately half the second notch frequency (e.g., ~75 Hz for a 10 m depth).

**Advantage:** Trace-by-trace — no spatial sampling requirements. Works with conventional streamer data and legacy recordings.

**Limitation:** The trace-by-trace approximation neglects angle-dependent effects. Effective bandwidth is limited to below the second notch.

#### 3.2.8 Choosing a deghosting method

| Method | Bandwidth recovery | Complexity | Data requirement |
|--------|-------------------|------------|-----------------|
| 1D inverse | Poor (notch residuals) | Low | Conventional |
| Bootstrap (tau-P) | Good | Medium | Conventional |
| Dual-sensor (PZ) | Good (>10 Hz) | Low | Dual-sensor cable |
| Sparse (FISTA) | Good | Medium | Conventional |
| Low-frequency (Amundsen) | Low-freq only | Low | Conventional |

In practice, methods are often combined: e.g., PZ deghosting for the mid-band plus low-frequency deghosting for the very low end.

![](figures/term03_lec05/term03_lec05_deghosting_data.png){width=90%}

**Figure 6.** *Seismic data and its amplitude spectrum before and after deghosting. The data are modeled with a broadband minimum-phase source wavelet (Ormsby, 10/30/160/200 Hz corners) convolved with a sparse reflectivity, then contaminated with a source ghost (6 m) and a receiver ghost (12 m). Before deghosting (a, b) the ghosts carve deep spectral notches at 62.5 and 125 Hz and make the trace ringy; after deghosting (c, d) the notches are filled — the spectrum becomes smooth and broadband — and the ghost echoes are removed from the trace. Left column: time domain; right column: amplitude spectrum.*

![](figures/term03_lec05/term03_lec05_pz_deghosting.png){width=90%}

**Figure 7.** *Dual-sensor (PZ) deghosting principle, illustrated with a primary at 50 ms and its receiver ghost delayed by 40 ms. (a) Hydrophone pressure $P$: the primary and the ghost appear with the same (positive) sign. (b) Geophone vertical velocity $V_z$ (scaled by the water impedance): the ghost appears with the opposite sign to the primary. (c) The sum $P + V_z$: the primary is reinforced ($\times 2$, same sign on both sensors) while the ghost cancels (opposite sign on the two sensors), yielding the deghosted primary. The upgoing primary and the downgoing ghost are thus separated by polarity rather than by an inverse filter — so, unlike 1-D deghosting, there is no spectral-notch problem.*

### 3.3 Designature (minimum-phase conversion)

**Goal:** Convert the source wavelet to a minimum-phase equivalent, or reshape it to a desired target.

The designature toolbox includes several options:

| Method | Target | Use case |
|--------|--------|----------|
| Spiking deconvolution | Spike ($\delta(t)$) | Maximum resolution (rarely used alone) |
| Minimum-phase conversion | minimum-phase equivalent | Standard production |
| Wavelet shaping | Arbitrary target wavelet | 4D matching, well tie |

**Why not spiking deconvolution?** Spiking decon designs an operator that is the inverse of the wavelet's amplitude spectrum. At frequencies where the amplitude is near zero (spectral notches or minima), the inverse amplifies those frequencies enormously — boosting noise by 20–40 dB. On real data with noise, the result is unstable. Pre-whitening tames the noise boost but at the cost of bandwidth, defeating the purpose.

**Minimum-phase conversion workflow:**

1. Take the Fourier transform of the (de-bubbled and deghosted) input wavelet: $W(f) = |W(f)| e^{i\phi(f)}$.
2. Construct the minimum-phase target: $W_\text{min}(f) = |W(f)|$ (same amplitude, minimum phase).
3. Design a Wiener shaping filter that converts the input wavelet to the minimum-phase target:

$$ H(f) = \frac{W^*(f) \cdot W_\text{min}(f)}{|W(f)|^2 + \varepsilon^2} $$

4. Apply the filter to the data.

The result is a wavelet with the same bandwidth as the input but more front-loaded (minimum-phase) — maximum energy concentrated at the start of the wavelet, no phase distortion.

**Pre-whitening** ($\varepsilon^2$) controls the trade-off between resolution and stability. Typical values: 0.1–1.0% of the zero-lag autocorrelation.

![](figures/term03_lec05/term03_lec05_designature.png){width=75%}

**Figure 8.** *The designature workflow. Left column — time domain; right column — amplitude spectrum. **Top row:** the input source signature and its spectrum, which carries distortions (here concentrated at low frequencies). **Middle row:** the designature filter and its spectrum. **Bottom row:** the designature output — a shorter, more compact signature with a smooth amplitude spectrum. The filter reshapes the signature toward the target wavelet.*

## 4. Land data: why it is harder

### 4.1 Four challenges specific to land

Marine data has ghosts and bubble — but the wavelet is relatively consistent from trace to trace. The source signature is measured, the ghost geometry is known, and the water layer is well characterized. Land data presents four additional challenges that make the wavelet harder to model:

1. **Receiver coupling effects.** Geophones have a resonance frequency (typically ~10 Hz) that distorts the low-frequency response. Poor coupling in dry or loose soil adds further attenuation and phase distortion. The coupling varies from station to station.

2. **Absorption (Q).** The near-surface weathering layer strongly attenuates high frequencies. Typical land Q values are 15–50 (compared to 100+ in consolidated rock). The absorption follows:

$$ A(f, t) \propto e^{-\pi f t / Q} $$

This makes the wavelet **non-stationary** — it changes with two-way time as high frequencies are progressively lost.

3. **Non-white reflectivity.** Statistical deconvolution assumes a flat reflectivity spectrum. Well logs show that real reflectivity is typically "blue" (enriched in high frequencies):

$$ \text{Amplitude}(f) \propto f^{C_{LR}} $$

where $C_{LR}$ is estimated from well data or spectral slope analysis. If uncorrected, the deconvolution operator misinterprets the reflectivity color as part of the wavelet.

4. **Random noise.** The autocorrelation that deconvolution "sees" is:

$$ \phi_{xx}[k] = \phi_{ss}[k] + \phi_{nn}[k] $$

This is **not** the wavelet autocorrelation — it is distorted by noise. As S/N decreases, the minimum-phase wavelet derived from this autocorrelation becomes increasingly distorted, introducing **phase errors** that no amount of pre-whitening can fix.

The combined effect: land wavelets contain significant **non-minimum-phase components** (geophone response, instrument filters, absorption) that violate the fundamental assumption of statistical deconvolution.

### 4.2 Receiver effects and absorption

**Geophone response.** A moving-coil geophone is a damped harmonic oscillator with natural frequency $f_0$ (typically 10 Hz) and damping factor $h$ (typically 0.7). Below $f_0$, the response rolls off at 12 dB/octave. Above $f_0$, it is approximately flat. This means the geophone **suppresses low frequencies** — exactly the frequencies that broadband processing aims to recover.

Accelerometers, by contrast, have a flat response down to DC (0 Hz). This is one reason why modern land broadband surveys increasingly use accelerometers or MEMS sensors.

**Coupling.** A geophone planted in dry, loose, or rocky soil does not faithfully record the ground motion. The coupling acts as an additional low-pass filter with variable cutoff frequency. It is difficult to measure and varies from station to station.

**Absorption.** The quality factor $Q$ describes how rapidly high frequencies are absorbed:

$$ A(f, t) = A_0(f) \cdot e^{-\pi f t / Q} $$

For $Q = 30$ and two-way time $t = 1$ s, the attenuation at 60 Hz relative to 10 Hz is:

$$ 20\log_{10}\left(\frac{e^{-\pi \cdot 60 / 30}}{e^{-\pi \cdot 10 / 30}}\right) = 20\log_{10}\left(e^{-\pi \cdot 50/30}\right) \approx -45 \text{ dB} $$

This is an enormous dynamic range. Q-compensation (Term 2) corrects for this, but it also amplifies noise at high frequencies — creating a trade-off between resolution and S/N.

![](figures/term03_lec05/term03_lec05_receiver_q_spectrum.png){width=90%}

**Figure 9.** *Receiver and Q effects on the wavelet spectrum (geophone $f_0 = 10$ Hz, damping $h = 0.7$; $Q = 30$, two-way time $t = 1$ s). (a) The two effects as transfer functions: the geophone response is flat above $f_0$ but rolls off at 12 dB/octave below it, suppressing the low frequencies that broadband processing aims to recover; Q absorption is a progressive high-frequency loss that steepens with travel time. (b) Their combined effect on a broadband source wavelet spectrum (dashed): the geophone carves off the low end and Q carves off the high end, leaving the narrow, low-frequency-peaked recorded spectrum (solid).*

### 4.3 Colored reflectivity and noise

**Non-white reflectivity.** The assumption of white reflectivity is central to statistical deconvolution: if the reflectivity spectrum is flat, then the trace autocorrelation reveals the wavelet. But well logs consistently show that reflectivity is **blue** — its power spectrum increases with frequency:

$$ |R(f)|^2 \propto f^{2 C_{LR}} $$

where $C_{LR}$ (the "color" of reflectivity) is typically 0.2–0.5. If this is not corrected, the deconvolution operator will fail to correctly restore high-frequency content.

**Colored deconvolution** addresses this by:
1. Estimating $C_{LR}$ from well logs or from the spectral slope of stacked data.
2. Applying a correction filter to flatten the reflectivity spectrum before designing the deconvolution operator.
3. Alternatively, incorporating the reflectivity color into the operator design directly.

**Noise and phase distortion.** The effect of noise on deconvolution is subtle and important. When noise is present, the trace autocorrelation becomes:

$$ \phi_{xx}[k] = \phi_{ww}[k] * \phi_{rr}[k] + \phi_{nn}[k] $$

If reflectivity is white ($\phi_{rr}[k] \approx \delta[k]$), this simplifies to:

$$ \phi_{xx}[k] \approx \phi_{ww}[k] + \phi_{nn}[k] $$

The noise term adds a spike at zero lag (for white noise), which is equivalent to pre-whitening. But for **colored noise** or **low S/N**, the noise autocorrelation distorts the shape of $\phi_{xx}$, and the minimum-phase wavelet derived from it has **incorrect phase**. The lower the S/N, the larger the phase error.

This is a fundamental limitation of statistical deconvolution: it cannot separate wavelet phase from noise effects without an independent model of the wavelet.

![](figures/term03_lec05/term03_lec05_noise_influence_on_decon.png){width=90%}

**Figure 10.** *Influence of noise on statistical deconvolution, shown at increasing noise levels. The three panels show: the power spectra, where the noise floor rises with the noise level; the deconvolved wavelet, which becomes progressively broader (less compact) as noise increases; and the phase spectrum, which departs further from the minimum phase as the signal-to-noise ratio falls. This illustrates why statistical deconvolution struggles at low S/N — noise contaminates the trace autocorrelation ($\phi_{xx} \approx \phi_{ww} + \phi_{nn}$), so the minimum-phase wavelet derived from it has increasingly incorrect phase.*

### 4.4 Why surface-consistent deconvolution is not enough

Surface-consistent deconvolution (SCD, Term 1 Lecture 07) decomposes the wavelet into source, receiver, CMP, and offset components:

$$ W_{ij}(t) = S_i(t) * R_j(t) * M_{(i+j)/2}(t) * O_{(i-j)/2}(t) $$

SCD solves for these components by spectral decomposition across many traces, which provides **averaging** that suppresses random noise effects. This is an improvement over trace-by-trace deconvolution.

However, SCD has three fundamental limitations:

1. **Assumes minimum-phase wavelet.** The spectral decomposition recovers amplitude spectra, and the phase is reconstructed via the minimum-phase assumption (Hilbert transform of the log amplitude). Any non-minimum-phase component — geophone response, instrument filter, absorption — is incorrectly assigned a minimum-phase equivalent. The resulting operator has the right amplitude but the **wrong phase**.

2. **Does not model Q explicitly.** Absorption is buried in the CMP component, mixed with genuine reflectivity effects. SCD cannot separate the absorption trend from the geological signal.

3. **Does not account for detector and instrument responses.** These are deterministic, known quantities — but SCD treats them as unknown statistical components, adding unnecessary uncertainty.

The result: after SCD, the data still contains **non-minimum-phase residuals** in the wavelet. The amplitude spectrum may look good, but the phase is wrong — and phase errors are particularly damaging for interpretation and inversion.

## 5. Model-Based Wavelet Processing (MBWP)

### 5.1 The MBWP model

Model-Based Wavelet Processing (Hart & Hootman, 2001; Hootman & Abitbol, 2008–2009) takes a fundamentally different approach: instead of estimating the wavelet statistically from the data, it **constructs** the wavelet from known physical components.

The trace model is:

$$ x(t) = [\underbrace{S(t) * Q(t) * D(t) * I(t)}_{\text{Wavelet } W(t)} * r(t)] + [\underbrace{D(t) * I(t) * n(t)}_{\text{Filtered noise}}] $$

where:
- $S(t)$ — source signature (vibroseis Klauder wavelet, dynamite derivative, or airgun far-field signature)
- $Q(t)$ — absorption wavelet (parameterized by effective Q)
- $D(t)$ — detector response (geophone or accelerometer)
- $I(t)$ — instrument response (recording filters)
- $r(t)$ — reflectivity
- $n(t)$ — random noise

The crucial distinction from SCD: **MBWP does not assume minimum phase, white reflectivity, or zero noise.** Instead, it builds the wavelet from measured or modeled components, each of which may be non-minimum-phase.

### 5.2 Only two free parameters

Despite the apparent complexity, the model has only **two free parameters** that must be estimated from the data:

| Parameter | Meaning | Typical range (land) |
|-----------|---------|---------------------|
| $Q_\text{eff}$ | Effective absorption | 15–50 |
| S/N | Signal-to-noise ratio (dB) | 0–20 dB |

All other components are **known** or **measured**:
- Source signature: from sweep recording (vibroseis) or charge configuration (dynamite).
- Detector response: from geophone specifications (natural frequency, damping) or tap test.
- Instrument response: from pulse test of the recording system.

### 5.3 Source models by type

The source component $S(t)$ depends on the source type:

**Vibroseis.** The source applies a frequency sweep to the ground. After crosscorrelation with the sweep (standard field processing), the effective source wavelet is the **Klauder wavelet** — the autocorrelation of the filtered sweep:

$$ K(t) = \int S_w(f) \cdot S_w^*(f) \cdot e^{i2\pi f t}\,df $$

The Klauder wavelet is zero-phase by construction. An additional −90° phase rotation is typically needed to account for the fact that geophones record particle velocity while the vibrator applies force (proportional to displacement).

**Dynamite (buried).** The applied force is approximately the first derivative of a step function. The source wavelet is therefore a differentiated impulse, modified by the near-surface coupling.

**Airgun (marine).** The source is the measured far-field signature, including the source ghost. No derivative is needed because the hydrophone records pressure directly.

### 5.4 Why MBWP corrects what SCD cannot

The key insight is the **noise model**. When SCD (or any statistical method) estimates the wavelet from the trace autocorrelation, it "sees":

$$ \phi_{xx}[k] = \phi_{ww}[k] + \phi_{nn}[k] $$

The minimum-phase wavelet derived from this distorted autocorrelation has incorrect phase. MBWP avoids this by:

1. Building the model wavelet $M(t)$ from physical components — no statistical estimation needed.
2. Adding a noise model with the estimated S/N to form the "resultant wavelet" $X(t) = M(t) + k \cdot N(t)$.
3. Computing a spiking deconvolution operator $O(t)$ from $X(t)$ — this is what SCD would produce.
4. Computing the **residual** between the spiking decon result and the true model:

$$ W_\text{MBWP}(t) = O(t) * X(t) $$

This residual operator captures exactly the phase and amplitude errors that SCD introduces. Applying it after SCD corrects the non-minimum-phase residuals.

### 5.5 The three-step workflow

**Step 1: Construct the initial model.**

- Load instrument response (from pulse test), detector response (from tap test or specifications), and source signature (from sweep recording or default model).
- Set initial Q = 30 and S/N = 20 dB (typical land starting values).
- Build the model wavelet by convolving all components.
- Output: signal and noise autocorrelations for parameter estimation.

**Step 2: Estimate Q and S/N from field data.**

- Compute logarithmic power spectra of field traces (same setup as SCD spectral analysis).
- Fit the model log spectrum to the observed log spectrum across a fitting range (typically 15–80 Hz, excluding unreliable low frequencies).
- From the spectral slope, estimate Q:

$$ Q/t = 55 / \text{slope} $$

- From the level difference between signal and noise model spectra at a reference frequency (e.g., 35 Hz), estimate S/N.
- Decompose Q and S/N surface-consistently together with other components.
- Compute average effective Q and S/N from histograms.

**Step 3: Build the final operator.**

- Reconstruct the model wavelet with the estimated Q and S/N.
- Compute the MBWP operator (residual filter).
- QC: amplitude spectrum should be flat in the data band; phase spectrum shows the correction.
- Condition: apply 100 ms Hanning taper to both ends; remove high-frequency artifacts if present.
- Export as a filter for production application.

### 5.6 Production application

The MBWP operator is applied **after** surface-consistent deconvolution and **before** moveout correction:

$$ \text{SC Decon} \longrightarrow \boxed{\text{MBWP filter}} \longrightarrow \text{NMO/DMO} \longrightarrow \cdots $$

SCD handles the bulk of the wavelet shaping (surface-consistent effects correction). The MBWP filter corrects the residual phase and amplitude errors — the non-minimum-phase components that SCD could not address.

### 5.7 Advantages over SCD

| Feature | SCD | MBWP |
|---------|-----|------|
| Non-minimum-phase correction | $\times$ | $\checkmark$ |
| Explicit Q modeling | $\times$ | $\checkmark$ |
| Noise modeling | Partial (averaging) | $\checkmark$ |
| Detector/instrument response | $\times$ | $\checkmark$ |
| Mixed-source consistency | Limited | $\checkmark$ |
| Free parameters | 4 (S, R, M, O components) | 2 (Q, S/N) |

### 5.8 Validation

MBWP can be validated by three independent methods:

1. **VSP measurements.** Downhole geophones record the actual propagating wavelet. Model wavelets from MBWP closely match VSP first arrivals for both dynamite and vibroseis sources.

2. **Synthetic seismogram ties.** Well-to-seismic ties improve after MBWP, confirming that the wavelet phase is correct.

3. **Mixed-source phase consistency.** In surveys using both vibroseis and dynamite, the crosscorrelation phase spectrum between the two source types shows significant rotation before MBWP. After the MBWP residual filter, the phase flattens to near zero — consistent phase across sources without requiring overlapping recordings.

**Figure 11.** *MBWP model diagram. The convolutional model showing source, Q, detector, and instrument components assembled into the model wavelet. The noise path through detector and instrument is shown separately.*

**Figure 12.** *MBWP workflow. Three-step process: initial model (default Q, S/N) → parameter estimation (fit to field spectra) → final operator (residual filter). Before/after amplitude and phase spectra shown.*

**Figure 13.** *Mixed-source phase consistency. Crosscorrelation phase spectrum between vibroseis and dynamite data before MBWP (significant rotation) and after MBWP (phase near zero).*

## 6. Robust surface-consistent deconvolution

### 6.1 The problem: complex near-surface and low signal-to-noise ratio

Conventional SCD decomposes the wavelet spectrum using least-squares (L2 norm) optimization. This assumes that the residuals (model misfit) follow a **Gaussian distribution**. The assumption holds reasonably well for clean data acquired over a simple, well-behaved near-surface with high signal-to-noise ratio. But it breaks down whenever the near-surface is complex and the signal-to-noise ratio is relatively low — a condition typical of  many land environments (loose or rocky soils, karst, permafrost, urban areas with cultural noise):

- **Ground roll** contaminates near-offset traces with strong, coherent low-frequency energy.
- **Noise bursts** from cultural sources, wind, or coupling problems affect individual traces.
- Up to **20% of traces** may contain inconsistent noise at any given time.

The result: the error distribution has heavy tails (non-Gaussian), and the L2 solution is pulled toward the outliers. The estimated source and receiver spectra become unstable, producing erratic deconvolution operators that amplify noise instead of removing it.

### 6.2 The robust solution: hybrid L1/L2 optimization

Robust surface-consistent deconvolution (Zhang & Yuan, 2019) replaces the pure L2 criterion with a **hybrid L1/L2 norm**:

$$ \min \sum_\text{signal} |E_i|^2 + \lambda \sum_\text{noise} |E_i| $$

The key insight:
- **L2 norm** (least squares) is optimal for Gaussian-distributed signal residuals — it gives the minimum-variance estimate.
- **L1 norm** (least absolute deviations) is robust to outliers — large errors contribute linearly rather than quadratically, so they have less influence on the solution.

By assigning L2 to the signal component and L1 to the noise outliers, the decomposition produces **unbiased** estimates of the source, receiver, CMP, and offset spectra even when 20% of traces are contaminated.

### 6.3 Three-step procedure

The robust SCD follows the same surface-consistent framework as conventional SCD, but with a robust solver:

**Step 1: Spectral analysis.**
Compute the logarithmic amplitude spectrum $\ln A_{ij}(f)$ for all traces in the analysis window. Under the minimum-phase assumption:

$$ \ln A_{ij} = \ln A_{s_i} + \ln A_{g_j} + \ln A_{m_k} + \ln A_{o_l} $$

**Step 2: Spectral decomposition (robust).**
Solve for the four component spectra using the hybrid L1/L2 optimization. The solver (JOR — Jacobi with Overrelaxation) iteratively updates each component:

$$ \ln A_s^{(k+1)} = (1 - \omega)\ln A_s^{(k)} + \omega \cdot f\!\left(\ln A_g^{(k)}, \ln A_m^{(k)}, \ln A_o^{(k)}\right) $$

Operators are computed per frequency band, with the amount of deconvolution adapted to the local S/N. In noise-dominated bands, the operator is automatically weakened.

**Step 3: Spectral application.**
Apply the deconvolution operators to all traces. Because the operators are derived from robust estimates, they are stable and can be applied with the sampling rate as the operator step (very short operators are feasible).

### 6.4 Field data results

Zhang & Yuan (2019) demonstrate the method on foothill data from southern China — a representative example of the complex-near-surface, low-S/N regime described above:

| Stage | Effective bandwidth |
|-------|-------------------|
| Original data | 8–55 Hz |
| After conventional SCD | 6–65 Hz |
| After robust SCD | **4–90 Hz** |

Robust SCD broadens the effective bandwidth by ~25 Hz at **both** the low and high frequency ends compared to conventional SCD. The stack section shows improved S/N and spatial energy consistency — the operators do not introduce the erratic amplitude variations seen with conventional SCD on the same data.

**Figure 14.** *Traditional vs. robust SC deconvolution. Operators derived from noisy, complex-near-surface data — conventional SCD produces erratic operators; robust SCD produces smooth, stable operators.*

**Figure 15.** *Robust SC deconvolution flow. Three-step procedure: spectral analysis → robust L1/L2 decomposition → spectral application.*

**Figure 16.** *Field data example (southern China foothill, after Zhang & Yuan 2019). Shot gathers and amplitude spectra before, after conventional SCD, and after robust SCD. The robust result shows broader bandwidth and better S/N.*

## 7. Summary

### Key takeaways

1. **Broadband seismic** means 6+ octaves of usable bandwidth (e.g., 2-128 Hz). More octaves produce sharper wavelets with lower side lobes — improving resolution, interpretation, and inversion.

2. **Ghost notches** are the primary bandwidth limitation in marine data: $f_n = n v_w / (2d)$. They vary with offset angle, making 1D removal inadequate.

3. **Marine processing chain:** De-bubble (remove bubble oscillation) → Deghosting (fill spectral notches) → Designature (minimum-phase conversion), the final wavelet-shaping step. The order matters: de-bubble first; deghosting before designature; de-bubble before amplitude recovery.

4. **Modern deghosting methods** handle the angle-dependent ghost problem: bootstrap (tau-P inverse), dual-sensor (PZ summation), sparse inversion (FISTA), and low-frequency trace-by-trace methods.

5. **Land data is harder** because of receiver coupling, absorption (Q), colored reflectivity, and noise — all of which introduce non-minimum-phase components that statistical deconvolution cannot correct.

6. **MBWP** builds the wavelet from physical components with only two free parameters (Q and S/N). It corrects the non-minimum-phase residuals that SCD leaves behind.

7. **Robust SCD** uses hybrid L1/L2 optimization to handle the non-Gaussian noise that arises over a complex near-surface at relatively low S/N, producing stable operators and broader bandwidth than conventional L2-based SCD.

### The big picture

| Domain | Method | What it corrects | Key limitation |
|--------|--------|-----------------|----------------|
| Marine | De-bubble + Designature | Source bubble, phase | Requires known source signature |
| Marine | Deghosting (bootstrap, PZ, variable-depth, sparse) | Ghost notches | Requires accurate geometry or special sensors |
| Land | SCD | Surface-consistent wavelet variations | Assumes minimum phase; no Q or detector modeling |
| Land | MBWP | Non-minimum-phase residuals (Q, detector, instrument, noise) | Requires measured instrument/detector/source responses |
| Land (complex near-surface, low S/N) | Robust SCD | Unstable operators from inconsistent noise | Still assumes minimum phase for phase reconstruction |

## Comprehension questions

1. Why is bandwidth measured in octaves rather than Hz? What is the practical difference between a 3-octave wavelet (10–80 Hz) and a 6-octave wavelet (2-128 Hz) in terms of interpretation?
2. Calculate the ghost notch frequencies for a source at 5 m depth and a receiver at 8 m depth (water velocity 1500 m/s). At what frequency do the source and receiver notches coincide?
3. Why must de-bubble be applied before designature? What would happen if the order were reversed?
4. A colleague designs a 1D deghosting operator for vertical incidence and applies it to a full-offset gather. Why will the result be poor at far offsets? What is the physical reason?
5. Compare bootstrap deghosting and dual-sensor (PZ) deghosting. What are the advantages and limitations of each? When would you choose one over the other?
6. Why does statistical deconvolution produce phase errors on low-S/N land data? Explain using the autocorrelation equation $\phi_{xx} = \phi_{ww} + \phi_{nn}$.
7. What are the two free parameters in MBWP? Why are they sufficient to describe the entire wavelet?
8. A survey uses both vibroseis and dynamite sources. After conventional SCD, the crosscorrelation phase between the two source types shows 30° rotation. How does MBWP fix this without requiring overlapping recordings?
9. Why does conventional SCD fail when the near-surface is complex and the signal-to-noise ratio is relatively low? What property of the noise violates the L2 assumption, and how does the L1 norm fix it?
10. The robust SCD result shows bandwidth extension from 8–55 Hz to 4–90 Hz. Is this "creating" new frequencies? Explain what is actually happening physically.

## Suggested reading and sources

- Monk, D. J. (2020). *Survey Design and Seismic Acquisition*. SEG DISC No. 23, Chapter 2. — Broadband concept, benefits, ghost physics, commercial techniques. `wiki/sources/monk_2020_broadband_seismic.md`.
- Lindsey, J. P. (1960). Elimination of seismic ghost reflections. *Geophysics*, 25(1), 130–140. — Historical first method (feedback filter). `wiki/sources/lindsey_1960_ghost_elimination.md`.
- Ghosh, S. K. (2000). Deconvolving the ghost effect. *Geophysics*, 65(6), 1831–1836. — Spectral zeros, two-depth recording criterion. `wiki/sources/ghosh_2000_ghost_deconvolution.md`.
- Amundsen, L., & Zhou, H. (2013). Low-frequency seismic deghosting. *Geophysics*, 78(2), WA15–WA20. — Trace-by-trace low-frequency method. `wiki/sources/amundsen_zhou_2013_deghosting.md`.
- Li, H.-J., Yang, Q.-Y., & Cai, J.-X. (2020). Simultaneous deghosting and denoising. *Applied Geophysics*, 17(3), 411–418. — Sparse FISTA method. `wiki/sources/li_et_al_2020_sparse_deghosting.md`.
- Bekara, M., Eid, M., Shabaan, H., & Gamal, N. (2025). Mixed-phase wavelet estimation for designature in marine seismic data processing. *Fifth EAGE Eastern Mediterranean Workshop*, Cairo. — Standard marine wavelet-processing sequence (system-delay correction, low-frequency noise attenuation, source/receiver deghosting, then de-signature as the final step); deterministic (far-field modeled) vs. data-driven (higher-order statistics) designature. `papers/marine/0011.pdf`.
- Hart, D., & Hootman, B. (2008). Achieving Consistent and Stable Phase with Mixed-Source Surveys. WesternGeco. — MBWP theory and validation. `wiki/sources/brown_et_al_mbwp_update_2008.md`.
- Zhang, Y., & Mo, Y. (2019). Robust Deconvolution for foothill seismic data. SEG Foothill Workshop. — L1/L2 hybrid method and field example. `wiki/sources/zhang_yuan_2019_robust_deconvolution.md`.
