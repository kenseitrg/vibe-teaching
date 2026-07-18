---
title: Term 3 Lecture 03 — Surface Waves
status: draft
term: 03
lecture: 03
---

# Surface Waves

## Learning objectives

By the end of this lecture you should be able to:

- Describe Rayleigh and Love surface waves and their particle motion.
- Explain why surface waves are noise for reflection processing but signal for near-surface characterization.
- Define phase velocity and group velocity and explain how dispersion arises in a layered medium.
- Sketch how a layered medium produces multiple surface-wave modes and why each mode samples depth differently.
- Explain why conventional filters fail to remove surface waves without damaging reflections.
- Describe the FK-MUSIC dispersion-spectrum workflow and how to pick dispersion curves.
- Explain how a dispersion curve is inverted for a near-surface $V_s$ profile and how multiple modes can constrain $V_p/V_s$.
- Build a simple frequency-dependent linear-moveout model of surface waves and explain why adaptive subtraction is needed after modeling.
- Recall the conceptual role of auto- and cross-correlation in adaptive filtering.

## Prerequisites

- Term 1 Lecture 06 (single-channel deconvolution): convolution, cross-correlation, Wiener filter basics.
- Basic elasticity: stress, strain, Hooke's law, P-wave and S-wave velocities.
- Term 3 Lecture 02: near-surface velocity model, first-break traveltimes, vertical-ray approximation.

## 0. Why this lecture matters

In Term 1 we learned how to correct amplitudes, estimate velocities, and apply statics. Almost all of that work assumed that the reflections we wanted were the dominant events on the record. On land, they usually are not. The largest-amplitude, most spatially coherent energy on a land shot gather is **ground roll** — a train of surface waves that travels along the free surface, masks near-offset reflections, and resists simple filtering because it overlaps with reflections in both time and frequency.

This lecture is about those surface waves. We will cover what they are (Rayleigh and Love waves), why they are dispersive and multimodal, how to measure their dispersion curves with array-processing methods (FK-MUSIC), how to turn those curves into near-surface shear-velocity profiles (MASW/SWI), and how to model and subtract them adaptively so that the reflections underneath become visible. The key message is: **surface waves are noise for reflection processing, but they carry near-surface $V_s$ information that is valuable in its own right.**

## 1. What surface waves are

### 1.1 Rayleigh waves

Surface waves travel along or near the free surface of the Earth rather than through its interior. **Rayleigh waves** are the most common type on land seismic records. They arise when P and SV motion couple at the free surface: the stress-free boundary condition forces a specific combination of compressional and shear displacements that decays exponentially with depth.

In a **homogeneous half-space** (uniform material to infinite depth), the Rayleigh wave has several distinctive properties:

- **Phase velocity** $V_R$ is fixed at about $0.92\,V_s$ for a typical Poisson's ratio of 0.25. It is slower than both the P-wave and the S-wave.
- **Particle motion** is **retrograde elliptical** in the vertical plane: as the wave propagates forward, a surface particle traces an ellipse that rotates backward at the top of its orbit. Think of a rolling wheel — the top of the wheel moves opposite to the direction of travel.
- **Amplitude decays exponentially with depth**, becoming negligible within about one wavelength below the surface.

Because the velocity is a fixed fraction of $V_s$ and does not depend on frequency, the Rayleigh wave on a homogeneous half-space is **non-dispersive**: all frequency components travel at the same speed.

> **Note.** The elliptical particle motion is a direct consequence of the P-SV coupling at the free surface. The 90° phase shift between the horizontal and vertical components (visible in the derivation as the factor of $i$ connecting P and S amplitudes) is what makes the motion elliptical rather than linear. See `lecture_notes/derivations/surface_wave_dispersion_and_multimodality_derivation.en.md` for the full derivation.

### 1.2 Love waves

**Love waves** are pure SH motion — horizontal displacement perpendicular to the direction of propagation. Unlike Rayleigh waves, Love waves **cannot exist on a homogeneous half-space**. They require a shallow low-shear-velocity layer over a higher-velocity half-space. Multiple reflections within the low-velocity layer interfere constructively and trap energy near the surface, creating a guided wave that is always dispersive in layered media.

### 1.3 Energy trapping and the 1/r decay

Body waves (P and S) spread outward in three dimensions, so their energy decays roughly as $1/r^2$. Surface waves are confined to the near-surface and spread in two dimensions, so their energy decays roughly as $1/r$. Because the decay is slower, surface waves can dominate the late part of a seismogram and have much higher amplitude than reflections at near offsets.

On a typical land shot gather, ground roll appears as a high-amplitude, low-velocity, low-frequency train of energy that fans out from the source. It is often mixed with direct arrivals and air waves. Typical ground-roll velocities range from 100 to 1000 m/s — much slower than P-wave reflections (1500–5000 m/s).

> **Figure idea:** Particle-motion diagrams for Rayleigh (retrograde ellipse in x-z) and Love (horizontal transverse in y); schematic of a shot gather with low-velocity surface-wave train.

## 2. Surface waves as noise and as signal

### 2.1 Noise for reflection processing

For reflection processing, surface waves are **coherent noise**. They overlap with reflections in time and frequency and have high amplitude, masking primary reflections on near-offset traces. The lower frequencies (typically 5–30 Hz) and lower velocities (100–1000 m/s) mean that ground roll occupies a distinctive region of the frequency-wavenumber domain, but this region partially overlaps with the reflection band.

### 2.2 Signal for near-surface characterization

For near-surface geotechnical or statics work, the same surface waves are **signal**. Their dispersion curve — the relationship between phase velocity and frequency — constrains the shear-velocity structure of the upper tens of meters. This is the basis of:

- **MASW** (Multichannel Analysis of Surface Waves): an active-source method that uses a linear receiver array to record surface waves from a hammer or weight drop, extracts the dispersion curve, and inverts it for a $V_s$ profile.
- **SWI** (Surface Wave Inversion): a broader term that includes passive ambient-noise methods.

### 2.3 Two processing contexts

The same wavefield is processed differently depending on the objective:

| Objective | Surface waves are... | Method |
|-----------|---------------------|--------|
| Reflection imaging | Noise | Model and subtract adaptively |
| Near-surface $V_s$ estimation | Signal | Extract dispersion curve, invert |


> **Figure idea:** Shot gather with surface waves labeled; same gather after surface-wave removal showing reflections.

## 3. Dispersion

### 3.1 The physical origin

In a homogeneous half-space the Rayleigh-wave velocity is constant and independent of frequency — there is no dispersion. In a layered medium, however, the phase velocity $c(f)$ depends on frequency. The reason is geometric: **different frequencies sample different depths**.

A surface wave of a given wavelength $\lambda$ has significant energy down to a depth of roughly one wavelength. If the subsurface velocity increases with depth:

- **Long wavelengths (low frequencies)** penetrate deeper and sense the faster material below. Their phase velocity is close to the Rayleigh velocity of the deeper layers.
- **Short wavelengths (high frequencies)** stay in the shallow, slower material. Their phase velocity is close to the Rayleigh velocity of the shallow layers.

As frequency increases, the phase velocity decreases from the deep value toward the shallow value. This produces a **normal dispersion curve** where $c(f)$ decreases with increasing frequency.

### 3.2 Phase velocity and group velocity

**Phase velocity** is the speed at which a single frequency component (the carrier wave) travels:

$$
c(f) = \frac{\omega}{k} = f \lambda,
$$

where $\omega$ is angular frequency, $k$ is wavenumber, and $\lambda$ is wavelength. On a dispersion curve, $c(f)$ is the quantity plotted on the vertical axis.

**Group velocity** is the speed at which the energy packet (the envelope) travels:

$$
U = \frac{d\omega}{dk} = c - \lambda \frac{dc}{d\lambda}.
$$

For a non-dispersive wave ($dc/d\lambda = 0$), the two are equal. For dispersive waves, they generally differ. The group velocity can be understood as the velocity of a wave packet formed by superposing two close frequencies: the envelope moves at $U$ while the carrier crests inside move at $c$.

> **Physical picture.** On a dispersive surface-wave record, the individual wiggles in a wave packet travel at the phase velocity, but the bump of energy you actually see travel across the gather moves at the group velocity. When the two differ, the wiggles appear to move through the envelope. See derivation §3 for the formal superposition argument.

### 3.3 Two-layer model intuition

Consider a simple two-layer model:

| Layer | Thickness | $V_s$ | $V_p$ | $\rho$ |
|-------|-----------|-------|-------|--------|
| 1 (shallow) | 10 m | 200 m/s | 400 m/s | 1800 kg/m³ |
| 2 (half-space) | $\infty$ | 500 m/s | 1000 m/s | 2000 kg/m³ |

The Rayleigh velocity of the shallow layer is $V_{R,1} \approx 0.92 \times 200 \approx 184$ m/s, and of the half-space $V_{R,2} \approx 0.92 \times 500 \approx 460$ m/s.

Because the medium is layered, the Rayleigh wave is dispersive:

- At very **high frequency** (wavelength $\ll$ 10 m), the wave is trapped in the shallow layer: $c(f) \to V_{R,1} \approx 184$ m/s.
- At very **low frequency** (wavelength $\gg$ 10 m), the wave averages over both layers: $c(f) \to V_{R,2} \approx 460$ m/s.
- At intermediate frequencies, $c(f)$ transitions smoothly between these limits.

This is the key result: **the dispersion curve encodes the velocity structure**. The high-frequency end tells us about the top few meters; the low-frequency end tells us about deeper material.

### 3.4 The dispersion curve

The **dispersion curve** is a plot of phase velocity $c(f)$ versus frequency (or period, or wavelength). It is the primary observable in surface-wave methods. The shape of the curve is characteristic of a particular $V_s$ profile, which is why it can be inverted.

The wavelength-depth rule of thumb is:

$$
\lambda \approx \frac{c}{f} \approx \frac{V_R}{f},
$$

with penetration depth scaling roughly with $\lambda$. For a 10 Hz Rayleigh wave at 300 m/s, $\lambda \approx 30$ m, so the wave samples the upper ~30 m.

> **Figure idea:** Dispersion curve for the two-layer model above, showing asymptotes at $V_{R,1}$ and $V_{R,2}$.

> **Derivation reference.** The formal derivation of the Rayleigh equation, the dispersion relation for a layered medium, and the two-layer numerical example are given in `lecture_notes/derivations/surface_wave_dispersion_and_multimodality_derivation.en.md` §§2–4.

## 4. Multimodality

### 4.1 Fundamental and higher modes

A single homogeneous layer over a half-space supports one surface-wave mode: the **fundamental mode** — the lowest-velocity mode at each frequency, with the simplest depth dependence (no node in the uppermost part of the wavefield).

A stack of many layers supports an infinite (in theory) sequence of modes: the fundamental, the first higher mode (or first overtone), the second higher mode, and so on. Each mode has its own phase velocity at each frequency, producing a **family of dispersion curves** — one per mode.

Higher modes exist only above a **cut-off frequency**: as frequency increases, more modes become possible. Which modes are actually observed depends on the source depth, the frequency content, and the velocity structure.

### 4.2 Depth sensitivity of modes

Each mode samples the subsurface differently:

- The **fundamental mode** is sensitive to the average velocity over its penetration depth and is usually the most energetic at low frequencies.
- **Higher modes** have more complex depth dependence (more zero crossings or "nodes" in their eigenfunctions) and can sample different depth ranges. They add independent information about the $V_s$ profile.

In normally dispersive profiles (velocity increasing monotonically with depth), the fundamental mode is often dominant. In profiles with strong contrasts or embedded low-velocity layers, higher modes can dominate certain frequency bands.

### 4.3 Why multimodality matters

Combining several modes in the inversion improves both the depth resolution and the vertical resolution of the $V_s$ profile. It also makes it possible to estimate the ratio $V_p/V_s$ (or Poisson's ratio), which is otherwise poorly resolved by the fundamental mode alone (Foti et al., 2011; InterPACIFIC guidelines, Foti et al., 2018).

### 4.4 Mode misidentification and low-velocity layer effects

A common pitfall is **mode misidentification**: an energy branch on the dispersion image that looks like the fundamental mode may actually be a higher mode or a guided wave from a low-velocity layer (LVL). Mi et al. (2016) showed with finite-difference modeling that:

- In a normally dispersive model, Rayleigh and Love dispersion energy is continuous and each mode is distinct.
- When an LVL is present, LVL-guided waves trap energy in the low-velocity channel. On the dispersion image the energy appears to **"jump"** from the fundamental mode to higher modes.
- If the LVL shear velocity is lower than the surface layer, the LVL-guided energy can interlace with the true fundamental mode and be mistaken for it.

Misidentified curves can produce large errors in the inverted $V_s$ profile. Analysts should check whether high-frequency energy is continuous along the surface-wave branch; a lack of high-frequency energy may indicate a guided wave rather than a true surface wave.

> **Figure idea:** Two panels: (left) eigenfunctions / depth sensitivity for fundamental and first higher mode; (right) dispersion curves showing two modes with the fundamental and first overtone.

> **Derivation reference.** The mathematical origin of modes as discrete roots of the layered dispersion relation is derived in `lecture_notes/derivations/surface_wave_dispersion_and_multimodality_derivation.en.md` §§4–5.

## 5. Why conventional attenuation fails

Surface waves and reflections overlap in both time and frequency. A simple band-reject filter centered on the ground-roll frequency band (say, 5–25 Hz) would remove reflections in the same band. Velocity filters (e.g., narrow FK fan or linear moveout filters) can separate events with different apparent velocities, but surface waves are dispersive — their apparent velocity changes with frequency — so a single velocity gate cannot capture the whole ground-roll train without also removing some reflection energy.

The problem is compounded by:

- **Source and receiver coupling variations**, which change the surface-wave amplitude and phase from trace to trace.
- **Topography and near-surface heterogeneity**, which scatter surface waves and make their wavefield spatially variable.
- **Near-field effects**: when receivers are close to the source, the surface-wave phase velocity is biased and the wavefield is not yet planar (Foti et al., 2018).

A better approach is to **model** the surface waves from a measured dispersion curve and then **subtract them adaptively**. This preserves the reflection signal because only the predicted surface-wave energy is removed.

> **Figure idea:** Spectrum / amplitude comparison showing overlap of surface-wave band and reflection signal; residual after a naive band-reject filter.

## 6. Surface-wave analysis

### 6.1 The beamforming idea

The goal of surface-wave analysis is to transform a multichannel shot gather into a **dispersion image** — a plot of energy as a function of phase velocity and frequency — from which the modal dispersion curves can be picked.

All array-based methods for building dispersion images share one idea (Datta, 2018): **cancel the phase accumulated by plane-wave propagation across the array, using trial phase velocities.** At each frequency, shift every trace by the phase shift it would have if a plane wave were propagating at a trial velocity $c$, then stack. When $c$ matches the true phase velocity of a mode, the traces add constructively and the stacked amplitude is large. When $c$ does not match, the traces interfere destructively and the amplitude is small.

Sweeping over frequencies and trial velocities produces a dispersion image. The methods below differ in *how* they implement this stacking idea.

### 6.2 Frequency-domain slant-stack

The simplest implementation (Park et al., 1998): at each frequency $\omega$, apply a position-dependent phase shift $e^{-ik x_i}$ to each receiver $i$ and sum:

$$
S(\omega, k) = \sum_{i=1}^{N} U(x_i, \omega)\, e^{-ik x_i},
$$

where $U(x_i, \omega)$ is the frequency-domain wavefield at receiver $i$ and $N$ is the number of receivers. Peaks in $|S|$ correspond to modal wavenumbers; converting $k$ to phase velocity $c = \omega/k$ gives the dispersion image.

This method is fast and easy to implement, but its resolution is limited by the array aperture — closely spaced modes may not be separated.

### 6.3 Conventional beamforming and the correlation matrix

A more general framework starts from the **spatial correlation matrix** $\mathbf{R} = \mathbf{Y}\mathbf{Y}^\dagger$, where $\mathbf{Y}$ is the vector of frequency-domain records across the array and $\dagger$ denotes conjugate transpose. Each element $R_{ij}$ encodes how receivers $i$ and $j$ correlate — it contains information about the relative phase between every receiver pair.

If $\mathbf{e}$ is the **steering vector** — the expected phase shifts across the array for a plane wave at trial velocity $c$ — then the conventional beamformer's output power is:

$$
P(c) = \mathbf{e}^\dagger \mathbf{R}\, \mathbf{e}.
$$

This is the mathematical form of the stacking idea: $\mathbf{e}$ compensates the propagation phase, and $\mathbf{R}$ provides the data. The output peaks at the true modal velocities. The slant-stack of §6.2 is a special case of this.

### 6.4 FK-MUSIC: using the noise subspace

**MUSIC** (Multiple Signal Classification; Schmidt, 1986) is an adaptive beamforming technique that produces much sharper spectra than conventional stacking. The key insight is: **instead of measuring how well the data stack, MUSIC measures how well the steering vector aligns with the noise.**

Here is the idea. The correlation matrix $\mathbf{R}$ is Hermitian, so it can be decomposed into eigenvectors $\mathbf{u}_1, \mathbf{u}_2, \ldots, \mathbf{u}_M$ with corresponding eigenvalues $\lambda_1 \ge \lambda_2 \ge \cdots \ge \lambda_M$, where $M$ is the number of receivers. The eigenvectors split into two groups:

- **Signal subspace**: the first $N_s$ eigenvectors (those with large eigenvalues) span the directions in which the actual wavefield has energy — the modes.
- **Noise subspace**: the remaining $M - N_s$ eigenvectors (those with small, nearly equal eigenvalues) span directions that contain only noise.

The number of signal eigenvectors $N_s$ equals the number of modes present in the data at that frequency.

MUSIC exploits the fact that these two subspaces are **orthogonal complements**: any steering vector that matches a true mode lies entirely in the signal subspace and is therefore orthogonal to every noise eigenvector. The MUSIC pseudo-spectrum is defined as:

$$
P_\text{MUSIC}(f, c) = \frac{1}{\displaystyle\sum_{i=N_s+1}^{M} \left| \mathbf{e}^\dagger(f, c)\, \mathbf{u}_i \right|^2}.
$$

When the trial velocity $c$ matches a true modal velocity, the numerator of each term in the sum is near zero (the steering vector is orthogonal to the noise), so the pseudo-spectrum peaks sharply. Between modes, the steering vector has a component in the noise subspace, and the pseudo-spectrum is small.

The result is a high-resolution dispersion image where each mode appears as a narrow ridge, even when modes are closely spaced.

> **Why is this sharper than conventional stacking?** Conventional stacking (§6.2–6.3) measures how much energy the steering vector captures. MUSIC measures how much energy it *does not* capture — specifically, how much it leaks into the noise subspace. Because the noise subspace is typically well separated from the signal subspace, this "leakage test" is a much more sensitive discriminator than direct stacking.

> **Full derivation.** The mathematical chain — from conventional beamforming output, through the minimum-variance beamformer, to the eigenanalysis that yields the signal/noise split and the MUSIC formula — is given in `lecture_notes/derivations/fk_music_beamforming_derivation.en.md`.

### 6.5 Picking dispersion curves

The FK-MUSIC pseudo-spectrum is a plot of $P_\text{MUSIC}(f, c)$ on a logarithmic scale. Picking follows these steps:

1. Identify continuous, high-amplitude branches on the image.
2. Use the expected velocity range and curve shape to distinguish the fundamental mode from higher modes.
3. **Window in the group-velocity domain** (Datta, 2018): apply a time-domain window corresponding to a chosen group-velocity range to suppress unwanted modes. For example, a window of 4–8 km/s can suppress the fundamental mode and reveal overtones that were masked beneath it.
4. Be cautious: attributing the correct overtone number to each branch remains a challenge. artefacts from aliasing, noise, or lateral heterogeneity can resemble real modes.

### 6.6 Practical requirements

From the InterPACIFIC guidelines (Foti et al., 2018) and Datta (2018):

- **Array aperture** should be 3–4 times the longest wavelength of interest. For near-surface MASW targets (top 30 m), an aperture of 50–100 m is typical. For regional studies, arrays of 2000+ km are needed (Datta, 2018).
- **Station spacing** must be small enough to avoid spatial aliasing: the Nyquist wavenumber $k_N = \pi / \Delta x$ must exceed the maximum wavenumber of interest. Aliasing artefacts can mimic dispersion branches and lead to mode misidentification.
- **Time windowing** in the group-velocity domain is essential for extracting higher modes. Different events (earthquakes, shots) illuminate different parts of the multimode dispersion tree; combining results from multiple sources improves coverage (Datta, 2018).
- **High-resolution methods** (MUSIC, Capon) improve mode separation but can be sensitive to noise and model errors. They should be validated against simpler methods (slant-stack) and used with appropriate array geometry.

> **Figure idea:** Two panels: (left) conventional FK dispersion spectrum (blurry); (right) FK-MUSIC pseudo-spectrum (sharp peaks) with picked dispersion curves overlaid.

## 7. Inversion for near-surface $V_s$

### 7.1 The MASW/SWI workflow

The dispersion curve is a set of observed phase velocities at discrete frequencies. The goal of inversion is to find a layered $V_s$ model whose theoretical dispersion curve matches the observed one. The standard workflow (Foti et al., 2011; InterPACIFIC guidelines) is:

1. **Acquire** surface-wave data (active source, passive noise, or both).
2. **Extract** the experimental dispersion curve for one or more modes.
3. **Build** a starting layered model with thickness, $V_s$, $V_p$, and density for each layer.
4. **Compute** the theoretical dispersion curve (forward problem).
5. **Adjust** the model to minimize the misfit between observed and predicted curves (inverse problem).

### 7.2 Forward problem

Given a stack of homogeneous, isotropic layers, the modal phase velocities are found by solving an eigenvalue problem for each frequency. This involves matching boundary conditions (displacement and stress continuity) at each interface and the free surface. The result is a set of theoretical dispersion curves, one per mode. The algebra is handled by the Thomson-Haskell propagator matrix or finite-element equivalents; the conceptual framework is derived in `lecture_notes/derivations/surface_wave_dispersion_and_multimodality_derivation.en.md` §4.

### 7.3 Inverse problem and regularization

The inverse problem is **non-linear** and **non-unique**: different $V_s$ profiles can produce nearly the same dispersion curve. The data constrain the average velocity over a wavelength range, but fine layer boundaries may be poorly resolved.

The misfit functional is:

$$
\Phi(V_s) = \sum_f \left[ c_\text{obs}(f) - c_\text{pred}(f;\, V_s) \right]^2 + \lambda \, \| D \, V_s \|^2,
$$

where the first term measures the data misfit and the second term is a regularization penalty (smoothness or damping operator $D$) that prevents oscillatory models. The trade-off parameter $\lambda$ controls model complexity.

**Practical guidelines** from the InterPACIFIC project (Foti et al., 2018):

- Use the **minimum number of layers** needed to explain the data.
- Fix or bound $V_p$ and density using a priori information (borehole logs, water table depth).
- **Invert multiple modes together** to reduce non-uniqueness and improve depth resolution.
- Report a **set of equivalent solutions** rather than a single best-fit model.

### 7.4 Multi-mode constraint for $V_p/V_s$

Including higher modes in the inversion reduces the trade-off between layer thickness and velocity. It also helps constrain $V_p/V_s$ (Poisson's ratio), which is important for distinguishing saturated from unsaturated soils. The fundamental mode alone is primarily sensitive to $V_s$; higher modes add sensitivity to $V_p$ through the P-SV coupling at layer boundaries.

### 7.5 Output

The output is a near-surface $V_s$ profile that can be used for:

- **Geotechnical engineering**: site classification ($V_{s,30}$), ground-response analysis.
- **Static corrections**: the $V_s$ model supplements or replaces the refraction-based near-surface model from Term 3 Lecture 02.
- **Migration**: a more accurate near-surface velocity model improves prestack depth migration.

> **Figure idea:** Two panels: (left) observed vs. predicted dispersion curve showing the fit; (right) inverted $V_s$ profile with depth.

## 8. Modeling and adaptive subtraction

### 8.1 Frequency-dependent linear moveout

Once a dispersion curve $c(f)$ is picked, surface waves can be modeled on each shot gather by applying a **frequency-dependent linear moveout**: for each frequency component, shift each trace by

$$
t(x, f) = \frac{x}{c(f)}.
$$

This reconstructs the predicted surface-wave wavefield with the correct kinematics: long wavelengths (low frequencies) arrive with a steep moveout because $c$ is large; short wavelengths (high frequencies) arrive with a gentler moveout because $c$ is small.

### 8.2 Spatial smoothing

After the frequency-dependent linear moveout is applied, the surface-wave components are approximately aligned across offsets — each frequency arrives at the same corrected time on every trace. Reflections, however, have hyperbolic moveout and remain misaligned after the surface-wave moveout correction.

This difference is exploited by **spatial smoothing**: applying a median filter (or a simple spatial average) along the offset axis after moveout alignment. The aligned surface waves pass through largely unchanged, while the misaligned reflections and other non-surface-wave energy are attenuated. The result is a cleaner surface-wave model that contains mostly the coherent noise to be subtracted, with less contamination from the reflections we want to preserve.

Spatial smoothing also helps stabilize the model against lateral variations in the surface wavefield caused by near-surface heterogeneity, source coupling, and topography.

### 8.3 Why adaptive subtraction is needed

Direct subtraction of the raw model usually leaves residual noise because:

- The predicted amplitudes and phases do not match the real data exactly.
- Source coupling, near-surface scattering, and 3D effects introduce amplitude and phase variations that the simple moveout model cannot capture.

The modeled surface wave has the right **kinematics** (moveout) but not necessarily the right **amplitudes and phases**. Direct subtraction would either leave residual energy or remove reflection signal.

### 8.4 Adaptive filter: the Wiener connection

**Adaptive subtraction** uses a short filter that convolves the model with filter coefficients estimated by minimizing the energy of the residual. This is conceptually the same Wiener-filter idea from Term 1 Lecture 06.

Let $m[n]$ be the modeled surface wave and $d[n]$ be the recorded data (which contains both surface waves and reflections). We seek filter coefficients $\hat{h}[n]$ such that the filtered model $\hat{h} * m$ best matches the surface-wave component of $d$. The Wiener–Hopf normal equations for this problem are:

$$
\underbrace{\mathbf{R}_{mm} \, \hat{\mathbf{h}}}_{\text{model autocorrelation} \times \text{filter}} = \underbrace{\mathbf{r}_{dm}}_{\text{data--model cross-correlation}},
$$

where $\mathbf{R}_{mm}$ is the autocorrelation matrix of the model and $\mathbf{r}_{dm}$ is the cross-correlation vector between the data and the model.

- **Left-hand side** ($\mathbf{R}_{mm} \hat{\mathbf{h}}$): the autocorrelation of the model captures its spectral character — how the modeled surface wave correlates with itself at different lags.
- **Right-hand side** ($\mathbf{r}_{dm}$): the cross-correlation between data and model captures how well the model, at each possible time shift, matches what was actually recorded.

The filter $\hat{\mathbf{h}}$ adjusts the model's amplitude and phase to best fit the surface-wave component of the data. After filtering, the adapted model is subtracted from the data:

$$
\text{residual} = d[n] - (\hat{h} * m)[n].
$$

If the filter is well designed, the residual contains mostly reflection energy with the surface waves removed.

### 8.5 Filter-length trade-off

- A **short filter** (2–5 coefficients) adapts quickly to local amplitude and phase variations but may not capture the full wavelet shape. Some residual noise may remain.
- A **long filter** (10+ coefficients) can match the wavelet better but may also start to fit the reflection signal that is not in the model, effectively removing reflections along with the noise.

The filter length is a regularization choice: it controls how aggressively the algorithm subtracts coherent noise. In practice, the shortest filter that gives acceptable noise removal is preferred.

> **Figure idea:** Three panels: (top) input gather with surface waves; (middle) modeled surface wave; (bottom) residual after adaptive subtraction. Second figure: two panels comparing short vs. long filter effects.

## 9. Summary

- **Surface waves** are trapped near the free surface; Rayleigh waves dominate land records (retrograde elliptical motion, $V_R \approx 0.92\,V_s$), Love waves require a low-velocity layer.
- **Dual role**: noise for reflection processing, signal for near-surface $V_s$ characterization.
- **Dispersion**: in a layered medium, low-frequency waves sense deeper, faster material; the dispersion curve $c(f)$ characterizes the medium.
- **Multimodality**: layered media support fundamental and higher modes, each with different depth sensitivity. Mode misidentification (especially from LVL-guided waves) is a common pitfall (Mi et al., 2016).
- **Conventional filters fail** because of time-frequency overlap with reflections; model-based adaptive subtraction is preferred.
- **FK-MUSIC** gives high-resolution dispersion spectra from which modes are picked, using the eigenstructure of the cross-spectral matrix.
- **Inversion** yields a $V_s$ profile; multiple modes constrain $V_p/V_s$ and reduce non-uniqueness. The InterPACIFIC guidelines emphasize reporting equivalent solutions (Foti et al., 2018).
- The modeled surface wave is **subtracted adaptively** with a Wiener-like filter because amplitude and phase are not perfectly known. Filter length controls the trade-off between noise removal and signal preservation.

## Comprehension questions

1. Why do surface waves dominate the near offsets of a land shot gather?
2. How does particle motion differ between Rayleigh and Love waves? What elastic structure is needed for a Love wave to exist?
3. Explain dispersion with the "long wavelengths see deeper" intuition for a medium where velocity increases with depth.
4. What is the difference between phase velocity and group velocity? In which part of the dispersion curve is the difference largest?
5. Why does a layered medium support multiple surface-wave modes, while a homogeneous half-space supports only one Rayleigh mode?
6. Why do simple frequency filters or band-reject filters often fail to remove surface waves without damaging reflections?
7. What does FK-MUSIC improve compared with a simple frequency-wavenumber spectrum, and why is it useful for multimodal data?
8. A dispersion curve gives phase velocity versus frequency. How is that information turned into a $V_s$ depth profile?
9. Why is the modeled surface wave subtracted adaptively instead of being subtracted directly? Write the Wiener–Hopf equation and identify the left-hand and right-hand sides.
10. What is the practical risk of using an adaptive filter that is too long?

## Suggested reading and sources

- Foti et al. (2011) — surface wave methods (MASW, inversion); `wiki/sources/foti_surface_wave_methods.md`.
- Foti et al. (2018) — InterPACIFIC guidelines for good practice in surface wave analysis; `wiki/sources/foti_interpacific_guidelines.md`.
- Novotny (1999) — Rayleigh-wave theory, half-space, layered media; `wiki/sources/novotny_seismic_surface_waves.md`.
- Igel (2007) — surface waves and free oscillations; `wiki/sources/sedi_surface_waves.md`.
- Rawlinson (2007) — surface waves and dispersion lecture notes; `wiki/sources/rawlinson_surface_waves_dispersion.md`.
- Priestley (2024) — practical surface wave workflow; `wiki/sources/priestley_surface_wave_practical.md`.
- Mi et al. (2016) — dispersion energy analysis with finite-difference modeling, LVL effects; `wiki/sources/mi_surface_waves_dispersion_energy.md`.
- Datta (2018) — f-k-MUSIC method, comparison with slant-stack and UC-diagram; `wiki/sources/datta_2018.md`.
- Ivanov et al. (2017) — HRLRT with MASW; `wiki/sources/ivanov_hrlrt_masw.md`.
- Derivation: `lecture_notes/derivations/surface_wave_dispersion_and_multimodality_derivation.en.md`.
- Derivation: `lecture_notes/derivations/fk_music_beamforming_derivation.en.md`.
