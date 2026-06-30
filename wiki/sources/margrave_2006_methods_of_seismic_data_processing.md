---
title: Margrave (2006) — Methods of Seismic Data Processing. Course Lecture Notes
status: reviewed
type: lecture notes
source_file: papers/textbooks/Methods of Seismic Data Processing.pdf
pages: 410
concepts:
  - seismic_data_processing
  - deconvolution
  - minimum_phase
  - wiener_filter
  - predictive_deconvolution
  - convolutional_model
  - surface_consistent_deconvolution
  - static_corrections
  - residual_statics
  - floating_datum
  - layer_replacement
  - seismic_velocities
  - normal_moveout
  - velocity_analysis
tags: [seismic-processing, deconvolution, convolutional-model, minimum-phase, wiener-filter, predictive-decon, q-attenuation, lecture-notes, statics, residual-statics, floating-datum, layer-replacement, velocities, nmo, velocity-analysis]
---

# Margrave (2006) — Methods of Seismic Data Processing

Course lecture notes for Geophysics 557/657, University of Calgary, Winter 2006.
Extracted pages 125–205 cover minimum phase, the convolutional model, and deconvolution.
**OCR-extracted pages 206–298 cover surface-consistent methods, velocity definitions, and normal moveout/stack.**
Chapter 1 (pages 1-2 of the notes) provides a high-level “big picture” useful for an introductory lecture.

## Relevant chapters / sections

| Section | Pages | Topic |
|---------|-------|-------|
| 1-1 to 1-2 | 6–9 | The big picture: imaging vs deconvolution, inverse problems, bandlimited reflectivity |
| 3-14 to 3-18 | 125–129 | Constant-Q attenuation; non-stationary wavelet |
| 3-18 to 3-26 | 129–137 | Minimum phase: intuitive, Hilbert transform, partial energy, dispersion |
| 4-1 to 4-5 | 145–149 | Bandlimited reflectivity; convolutional model and simplifying assumptions |
| 4-? | ~149– | Frequency-domain spiking deconvolution; Wiener spiking deconvolution; gapped predictive deconvolution; Burg deconvolution |
| 5-1 to 5-9 | 206–215 | Seismic line coordinates; surface-consistent convolutional model; surface-consistent methods |
| 5-10 to 5-16 | 216–222 | Statics and datums; statics with uphole times |
| 5-17 to 5-24 | 223–230 | Surface-consistent residual statics; Wiggins model; Gauss–Seidel solution |
| 5-25 to 5-29 | 231–234 | Refraction statics; delay-time geometry |
| 6-1 to 6-7 | 235–241 | Velocity definitions: instantaneous, vertical traveltime, average, RMS |
| 6-8 to 6-17 | 242–251 | Interval velocity, Dix formula, constraints on physically plausible RMS decreases |
| 6-18 to 6-25 | 252–260 | Snell's law; ray parameter; raytracing in v(z); linear v(z) rays are circular arcs |
| 7-1 to 7-5 | 261–265 | Normal moveout; stacking velocity as best-fit hyperbola |
| 7-6 to 7-9 | 266–269 | Dipping reflector NMO: stacking velocity = V / cos(δ) |
| 7-10 to 7-14 | 270–275 | NMO in v(z) medium; Dix link between stacking and RMS velocities |
| 7-15 to 7-29 | 276–298 | NMO removal, multiples, CMP stacking, ZOS model, Fresnel zones |

## Key takeaways

### The big picture (introductory view)
- Seismic data processing does **not** undo all physical effects exactly; we are limited by ignorance of the subsurface.
- The problem is an **inverse problem**: to undo wave propagation we need to know the very subsurface properties we hope to discover.
- We therefore subdivide, approximate, and compartmentalize the problem into solvable pieces.
- Two broad families of processes:
  - **Imaging processes** place energy at the correct spatial position (NMO, CMP stack, migration).
  - **Deconvolution processes** remove the illuminating wavelet and improve resolution (gain recovery, statistical deconvolution, inverse-Q filtering, wavelet processing).
- The simplest usable model is the **convolutional model**: trace ≈ wavelet convolved with reflectivity.

### Convolutional model
- Ultimate goal: recover the earth's reflectivity as a function of position.
- Because seismic sources do not generate useful power at all frequencies, the best achievable result is **bandlimited reflectivity** — the true reflectivity convolved with a zero-phase wavelet.
- Sheriff & Geldart decompose the earth impulse response into near-surface effects, propagation effects (multiples, absorption, mode conversions), and target reflectors. Margrave notes this terminology can be self-contradictory if the "impulse response" is supposed to be only the desired signal.
- For deconvolution theory we need stronger simplifying assumptions than pure linearity.

### Minimum phase
- Infinitely many wavelets share the same amplitude spectrum; only a few have practical use.
- A **minimum-phase wavelet** is the most front-loaded of all causal wavelets with the same amplitude spectrum.
- Minimum-phase wavelets arise naturally in the earth from causality and linearity; constant-Q attenuation is a minimum-phase process.
- For a causal, stable function with a causal stable inverse, amplitude and phase are related by the Hilbert transform. The phase is `φ(ω) = H[ln A(ω)]`.
- Partial energies `E_p = Σ_{k=0}^{p} f_k^2` are larger for the minimum-phase wavelet than for any other causal wavelet with the same amplitude spectrum, for all `p`.
- If the amplitude spectrum of a minimum-phase dataset is changed, the phase spectrum must also change to preserve the minimum-phase relationship.

### Deconvolution algorithms
- Frequency-domain spiking deconvolution: divide the trace spectrum by the wavelet spectrum. Prewhitening is essential for stability.
- Wiener spiking deconvolution designs a finite least-squares inverse filter using the autocorrelation of the trace.
- The autocorrelation matrix is Toeplitz and symmetric; use the Wiener-Levinson (Levinson-Durbin) recursion.
- Gapped predictive deconvolution: desired output is the trace shifted by the prediction gap; the residual is the deconvolved trace.
- Burg (maximum entropy) deconvolution explicitly constructs a minimum-phase prediction-error filter.

### Surface-consistent methods (Chapter 5)
- Seismic data are recorded in shot gathers but can be re-sorted into receiver, CMP, or offset gathers. The coordinate pairs `(s, r)` (acquisition) and `(x, h)` (processing) are linked by `x = (s + r)/2` and `h = (r - s)/2`.
- The surface-consistency assumption splits effects into those that vary with source/receiver coordinates (near surface) and those that vary with midpoint/offset (subsurface).
- A surface-consistent trace model in frequency domain is `H(s,r,x,h,ω) = A(s,ω) B(r,ω) C(x,ω) D(h,ω)`. Taking logs turns it into a linear least-squares problem.
- Near-surface terms (attenuation, ghosts, peg-leg multiples, instrument response) are more stationary and more minimum-phase than subsurface terms, making them good deconvolution targets.
- **Statics and datums**: a static correction is an approximate vertical-ray downward continuation that replaces the variable near surface with a smooth replacement layer. The datum should be a smoothed version of topography; the replacement velocity should be an average near-surface velocity. Large bulk shifts degrade NMO and migration, so mean statics are often removed and saved for final datum shift.
- **Uphole statics**: measured uphole times give a direct estimate of the weathering-layer traveltime, but shots in the weathered layer, inaccurate picks, and sparse coverage cause problems.
- **Residual statics**: Wiggins et al. (1976) model total traveltime as `T_ij = S_i + R_j + G_k + M_k X_ij^2` plus a pilot trace. The shifts are measured by cross-correlation and solved as a sparse least-squares system, often by Gauss–Seidel iteration. Long-wavelength trends (greater than a spread length) are not reliably resolved and should be constrained to zero mean.
- **Refraction statics**: first-break refraction methods give the delay time `t_i = 2Z_1 cos(θ_crit)/V_1`, which approximates the vertical traveltime through the weathering layer when `V_1 << V_2`.

### Velocity definitions (Chapter 6)
- **Instantaneous velocity** `v_ins(z)` is the local P-wave speed; in a `v(z) = v_0 + c z` medium it becomes `v(τ) = v_0 e^{cτ}` as a function of vertical traveltime.
- **Average velocity** `V_avg = z / τ = (1/τ) ∫ v(τ) dτ` is an average over vertical traveltime, not depth.
- **RMS velocity** `V_rms^2 = (1/τ) ∫ v^2(τ) dτ` is always ≥ average velocity (Schwartz inequality).
- **Interval velocity** can be computed from RMS velocities via the Dix formula: `V_int^2(τ_1, τ_2) = (V_rms,2^2 τ_2 - V_rms,1^2 τ_1) / (τ_2 - τ_1)`. The result must be positive and physically plausible; rapid RMS decreases can produce imaginary interval velocities.
- **Snell's law and ray parameter**: for a horizontally layered or `v(z)` medium, `p = sin(θ(z))/v(z)` is conserved along a ray. Rays in a linear `v(z)` medium are circular arcs.

### Normal moveout and stack (Chapter 7)
- For a constant-velocity medium, reflection traveltime is a hyperbola: `t_x^2 = t_0^2 + x^2 / V^2`.
- **Stacking velocity** is the velocity parameter that gives the best-fit hyperbola to a CMP gather; it depends on the maximum offset used.
- For a dipping reflector: `V_stack = V / cos(δ)` (2-D) or `V_stack = V / sqrt(1 - sin^2(δ) cos^2(ω))` (3-D, where ω is the azimuth of the line relative to dip).
- In a `v(z)` medium, the traveltime series has `t^2(x) = c_1 + c_2 x^2 + c_3 x^4 + ...` with `c_1 = t_0^2` and `c_2 = 1 / (V_avg V_m) = 1 / V_rms^2`. This is the theoretical link between stacking velocities and RMS velocities (Dix, Al-Chalabi, Taner & Koehler).
- Higher-order moveout (`c_3`) becomes important when `H / z_0` is large or for converted/shear waves.
- Multiples have lower stacking velocities than primaries and are not flattened by the primary velocity, which helps attenuate them in CMP stacking.
- The CMP stack can be viewed as a zero-offset section (ZOS) model; it collapses Fresnel zones and improves S/N.

### Practical notes
- Real data are non-stationary: the wavelet changes with time because of attenuation and with offset because of arrays/ghosts.
- Arrays of sources/receivers create a variable embedded wavelet, violating strict stationarity assumptions.
- Residual statics and velocity analysis form a chicken-and-egg problem: velocity analysis needs statics, residual statics need good NMO. Iteration and floating datums are the practical solutions.

## Figures useful for teaching

- Constant-Q amplitude spectra at increasing time (pages 125–126).
- Minimum-phase vs. zero-phase bandlimited reflectivity (page 146).
- Matrix representation of convolution (page 146).
- Surface-consistent coordinate systems (pages 207–208).
- Statics datum replacement model (pages 218–220).
- Residual statics linear system structure (page 226).
- Linear `v(z)` circular raypaths (page 259).
- NMO hyperbola family and dip-dependent NMO (pages 263–269).

## Relation to lecture notes
- Good source for the Hilbert-transform link between amplitude and phase spectrum.
- Explains why bandlimited reflectivity, not the full impulse response, is the realistic processing target.
- Provides matrix view of convolution and Wiener normal equations.
- **Chapters 5–7 directly support Term 1 Lecture 02 (kinematics, velocities, field statics) and Lecture 03 (advanced statics, residual statics, floating datum, velocity-analysis link).**
