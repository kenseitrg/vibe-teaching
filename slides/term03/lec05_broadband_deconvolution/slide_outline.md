# Slide outline — Term 3, Lecture 5: Broadband Processing

---

## Slide 1 — Title
- Broadband Processing
- Term 3, Lecture 5
- Marine broadband · Land MBWP · Robust surface-consistent deconvolution

---

## Slide 2 — Learning objectives
- Define broadband seismic data by octave count and explain why 6+ octaves are desirable.
- Calculate ghost notch frequencies for a given source/receiver depth and explain how they limit bandwidth.
- Describe the marine chain de-bubble → deghosting → designature and explain why the order matters.
- Compare modern deghosting methods (bootstrap, dual-sensor, sparse, low-frequency) and state each advantage.
- Explain why land data is harder to deconvolve than marine data (four challenges).
- Describe the MBWP wavelet model, its two free parameters (Q and S/N), and how it fixes non-minimum-phase residuals.
- Explain why conventional SCD fails over a complex near-surface at low S/N, and how robust L1/L2 optimization solves it.

---

## Slide 3 — Why this lecture matters
- Conventional deconvolution compresses the wavelet but cannot create missing bandwidth.
- Modern exploration needs 6+ octaves (~2–128 Hz) vs. the 2–3 octaves (~10–60 Hz) of conventional data.
- Subtle stratigraphic traps, thin reservoirs, and complex lithologies demand broadband images.
- This lecture: explicit modeling and removal of each wavelet component.
- Two domains: marine (de-bubble → deghosting → designature) and land (MBWP + robust SCD).

---

# 1. Introduction to broadband seismic

---

## Slide 4 — What is broadband seismic?
- Bandwidth is measured in octaves: N = log2(f_max / f_min).
- Conventional marine data: 10–60 Hz ≈ 2.6 octaves — oscillatory wavelet, strong side lobes.
- Broadband data: 2–128 Hz ≈ 6 octaves — sharp, impulsive, minimal side lobes.
- Side-lobe amplitude is controlled by relative bandwidth (octaves), not absolute bandwidth.
- Figure: `term03_lec05_wavelet_octave_comparison.png`

---

## Slide 5 — What octaves buy you
- High frequencies sharpen the central lobe (vertical resolution).
- Low frequencies suppress the side lobes (event isolation).
- Adding low octaves barely changes the central lobe but collapses the ringing side lobes.
- Lobe width scales as L_w ∝ 2 / (f_max − f_min).
- Figure: `term03_lec05_wavelet_octave_comparison.png`

---

## Slide 6 — Benefits of broadband data
- Resolution: sharper wavelets resolve thinner beds (smaller tuning thickness).
- Interpretation: low frequencies reveal impedance layering, fluid contacts, fault planes.
- Inversion: low frequencies constrain the background impedance trend, reducing model dependence.
- AVO: ghost removal gives cleaner amplitude-versus-offset behavior.
- Deep imaging: low frequencies survive absorption and penetrate salt, basalt, chalk.
- Figure: `term03_lec05_bandwidth_resolution.png`

---

# 2. What limits bandwidth

---

## Slide 7 — The convolutional chain
- The recorded trace is a chain of convolutions: source, propagation/Q, ghosts, detector, instrument, near-surface.
- In the frequency domain each component multiplies the spectrum.
- Marine: dominant limits are the source bubble and the ghost notches.
- Land: a complex, trace-varying mix of source, absorption, geophone response, and coupling.
- Figure: `term03_lec05_wavelet_components.png`

---

## Slide 8 — Why conventional deconvolution falls short
- Statistical deconvolution assumes: white reflectivity, minimum-phase wavelet, white noise, stationarity.
- Real reflectivity is colored (typically "blue" — high-frequency enriched).
- The wavelet has non-minimum-phase parts: ghosts, geophone response, instrument filters.
- Noise distorts the autocorrelation, causing phase errors in the derived operator.
- Absorption (Q) makes the wavelet non-stationary with depth.
- Figure: none

---

# 3. Marine broadband processing

---

## Slide 9 — Marine processing chain
- Marine wavelet is well characterized: source signature measured, ghost geometry known.
- This makes deterministic processing possible.
- Standard order: de-bubble → deghosting → designature.
- De-bubble first; deghosting before designature; de-bubble before amplitude recovery.
- Figure: none

---

## Slide 10 — De-bubble
- An airgun bubble oscillates before dissipating, leaving a long ringing tail and false events.
- De-bubble is a deterministic inverse filter built from a physical bubble model.
- Model/measure the bubble, design the inverse, apply to the signature (or data).
- After de-bubble: no oscillatory tail; the spectral ripple disappears.
- Figure: `term03_lec05_debubble.png`

---

## Slide 11 — De-bubble ordering rule
- De-bubble must be the FIRST wavelet-processing step.
- If you designature first, the shaping operator matches the bubble and embeds the artifacts.
- De-bubble must also precede amplitude recovery (Q-comp, spherical divergence).
- Otherwise those processes amplify the bubble tail along with the signal.
- Figure: `term03_lec05_debubble.png`

---

## Slide 12 — Deghosting: where the notches come from
- The ghost is a sea-surface reflection arriving after the primary with opposite polarity.
- Ghost delay: Δt = 2 d cos(θ) / v_w, with v_w ≈ 1500 m/s.
- The ghost acts as a comb filter G(f) = 1 − exp(−i 2π f Δt).
- Spectral notches (zeros) occur at f_n = n · v_w / (2 d).
- Figure: `term03_lec05_ghost_notch.png`

---

## Slide 13 — Notch frequency depends on geometry
- Depth sets the notch: a 6 m streamer gives a first notch at 125 Hz; 12 m gives 62.5 Hz.
- Doubling the depth halves the notch frequency.
- Offset shifts notches higher: as cos(θ) decreases, notches migrate upward.
- The whole notch pattern is set by source depth, cable depth, and offset.
- Figure: `term03_lec05_ghost_notch.png`

---

## Slide 14 — Why 1-D deghosting fails
- The naive inverse is H(f) = 1 / G(f).
- At the notch frequencies |G(f)| = 0, so the inverse is infinite.
- Pre-whitening avoids division by zero but leaves deep residual notches.
- Because notches shift with offset, one vertical-incidence operator misaligns at far offsets.
- Modern methods work in domains that handle the angle dependence explicitly.
- Figure: none

---

## Slide 15 — Bootstrap deghosting (tau-P)
- Transform to the tau-P domain: each plane wave has a well-defined slowness p.
- For each p the ghost is a simple time shift with known delay Δt(p) and R ≈ −1.
- Solve the inverse problem for the ghost-free upgoing wavefield; transform back.
- Advantage: handles angle-dependent delays exactly; extends to variable-depth streamers.
- Limitation: needs accurate water depth and geometry; tau-P edge effects need regularization.
- Figure: none

---

## Slide 16 — Dual-sensor (PZ) deghosting
- Dual-sensor streamers record pressure (hydrophone) and vertical velocity (geophone).
- For the upgoing primary, P and V_z have the same sign; for the downgoing ghost, opposite signs.
- Summing P + ρ v_w V_z reinforces the primary (×2) and cancels the ghost.
- Separation is by polarity, not by an inverse filter — no spectral-notch problem.
- Limitation: geophone S/N is poor below ~10 Hz, so the very low end is not recovered.
- Figure: `term03_lec05_pz_deghosting.png`

---

## Slide 17 — Sparse and low-frequency deghosting
- Sparse (Li et al., 2020): L1-regularized inversion in frequency-slowness; deghost + denoise in one step.
- Solved with FISTA (10–30 iterations); angle-dependent ghost operator computed exactly.
- Low-frequency (Amundsen & Zhou, 2013): trace-by-trace, pressure + scaled integral + scaled derivative.
- Effective below the second notch; works on conventional and legacy streamer data.
- Figure: none

---

## Slide 18 — Choosing a deghosting method
- 1-D inverse: poor recovery (notch residuals), low complexity, conventional data.
- Bootstrap (tau-P): good recovery, medium complexity, conventional data.
- Dual-sensor (PZ): good above 10 Hz, low complexity, needs dual-sensor cable.
- Sparse (FISTA): good recovery, medium complexity, conventional data.
- In practice methods are combined (e.g., PZ mid-band + low-frequency for the very low end).
- Figure: none

---

## Slide 19 — Deghosting result
- Before: ghosts carve deep notches (here 62.5 and 125 Hz) and make the trace ringy.
- After: the notches are filled, the spectrum becomes smooth and broadband, ghost echoes gone.
- Left column: time domain; right column: amplitude spectrum.
- Figure: `term03_lec05_deghosting_data.png`

---

## Slide 20 — Designature (minimum-phase conversion)
- Goal: convert the source wavelet to minimum phase, or reshape to a target.
- Toolbox: spiking decon, minimum-phase conversion, wavelet shaping.
- Spiking decon inverts the amplitude spectrum — at spectral minima it boosts noise 20–40 dB.
- Minimum-phase conversion keeps the amplitude, imposes minimum phase via a Wiener shaping filter.
- Pre-whitening (ε², ~0.1–1%) trades resolution for stability.
- Figure: `term03_lec05_designature.png`

---

# 4. Land data: why it is harder

---

## Slide 21 — Four challenges specific to land
- Marine wavelet is consistent and well characterized; land wavelet varies trace to trace.
- Receiver coupling: geophone resonance (~10 Hz) and poor soil coupling distort the low end.
- Absorption (Q ≈ 15–50): strong high-frequency loss, making the wavelet non-stationary.
- Non-white reflectivity: real reflectivity is "blue," violating the white-reflectivity assumption.
- Random noise: distorts the autocorrelation, introducing phase errors no pre-whitening can fix.
- Figure: none

---

## Slide 22 — Receiver response and absorption
- A geophone is a damped oscillator (f_0 ≈ 10 Hz, h ≈ 0.7); below f_0 it rolls off at 12 dB/octave.
- The geophone suppresses exactly the low frequencies broadband aims to recover.
- Accelerometers / MEMS are flat to DC — one reason broadband land surveys adopt them.
- Q absorption: A(f, t) ∝ exp(−π f t / Q); for Q = 30, t = 1 s, 60 Hz loses ~45 dB vs 10 Hz.
- Figure: `term03_lec05_receiver_q_spectrum.png`

---

## Slide 23 — Combined receiver + Q effect on the spectrum
- The geophone carves off the low end; Q carves off the high end.
- Together they leave a narrow, low-frequency-peaked recorded spectrum.
- Q-compensation restores highs but also amplifies noise — a resolution vs S/N trade-off.
- Figure: `term03_lec05_receiver_q_spectrum.png`

---

## Slide 24 — Colored reflectivity and noise
- Reflectivity power rises with frequency: |R(f)|² ∝ f^(2 C_LR), with C_LR ≈ 0.2–0.5.
- Colored deconvolution estimates C_LR (from wells or spectral slope) and corrects it.
- With noise, φ_xx[k] ≈ φ_ww[k] + φ_nn[k] — not the pure wavelet autocorrelation.
- Colored noise or low S/N distorts φ_xx, so the derived minimum-phase wavelet has wrong phase.
- Statistical deconvolution cannot separate wavelet phase from noise without an independent model.
- Figure: `term03_lec05_noise_influence_on_decon.png`

---

## Slide 25 — Why surface-consistent deconvolution is not enough
- SCD decomposes the wavelet into source, receiver, CMP, and offset components.
- Spectral averaging suppresses random noise — better than trace-by-trace.
- But SCD assumes minimum phase: non-minimum-phase parts get the wrong phase.
- SCD does not model Q explicitly, nor the deterministic detector and instrument responses.
- After SCD, non-minimum-phase residuals remain — the phase is wrong even if the amplitude looks good.
- Figure: none

---

# 5. Model-Based Wavelet Processing (MBWP)

---

## Slide 26 — The MBWP idea
- Instead of estimating the wavelet statistically, MBWP constructs it from physical components.
- Trace model: x(t) = [S * Q * D * I * r](t) + [D * I * n](t).
- S = source signature, Q = absorption, D = detector, I = instrument, r = reflectivity, n = noise.
- No assumption of minimum phase, white reflectivity, or zero noise.
- Each component may be non-minimum-phase.
- Figure: `term03_lec05_mbwp_model.png`

---

## Slide 27 — Only two free parameters
- Despite the complexity, only two parameters are estimated from the data.
- Q_eff (effective absorption), typical land range 15–50.
- S/N (signal-to-noise ratio, dB), typical land range 0–20 dB.
- Everything else is known or measured: source (sweep/charge), detector (tap test/specs), instrument (pulse test).
- Figure: `term03_lec05_mbwp_model.png`

---

## Slide 28 — Source models by type
- Vibroseis: Klauder wavelet (autocorrelation of the sweep), zero-phase by construction; ~−90° rotation needed.
- Dynamite (buried): force ≈ derivative of a step; modified by near-surface coupling.
- Airgun (marine): measured far-field signature including the source ghost; no derivative needed.
- Figure: none

---

## Slide 29 — Why MBWP corrects what SCD cannot
- SCD "sees" φ_xx = φ_ww + φ_nn, so its minimum-phase wavelet has incorrect phase.
- MBWP builds the model wavelet M(t) from physical components — no statistical estimation.
- Add a noise model with the estimated S/N to form the resultant wavelet X(t).
- Derive a spiking-decon operator from X(t), then the residual W_MBWP = O * X.
- That residual captures exactly the phase and amplitude errors SCD introduces.
- Figure: none

---

## Slide 30 — MBWP three-step workflow
- Step 1 — Initial model: load responses, start from Q = 30 and S/N = 20 dB, build W(t).
- Step 2 — Estimate Q and S/N: fit the model log-spectrum to field data (slope → Q, level → S/N); decompose surface-consistently.
- Step 3 — Final operator: rebuild W(t), derive the residual filter, QC amplitude and phase, export.
- Figure: `term03_lec05_mbwp_workflow.png`

---

## Slide 31 — Production application
- The MBWP operator is applied AFTER surface-consistent deconvolution and BEFORE NMO/DMO.
- SCD handles the bulk of the wavelet shaping (surface-consistent effects).
- The MBWP filter corrects the residual phase and amplitude errors.
- These are the non-minimum-phase components SCD could not address.
- Figure: none

---

## Slide 32 — MBWP advantages over SCD
- Non-minimum-phase correction: SCD no, MBWP yes.
- Explicit Q modeling: SCD no, MBWP yes.
- Noise modeling: SCD partial (averaging), MBWP yes.
- Detector and instrument response: SCD no, MBWP yes.
- Mixed-source consistency: SCD limited, MBWP yes.
- Figure: none

---

## Slide 33 — MBWP validation: mixed-source phase
- VSP measurements: model wavelets match downhole first arrivals (dynamite and vibroseis).
- Synthetic ties: well-to-seismic ties improve after MBWP (correct phase).
- Mixed-source: crosscorrelation phase between vibroseis and dynamite rotates before MBWP.
- After the MBWP residual filter the phase flattens to near zero — consistent without overlapping recordings.
- Figure: `term03_lec05_mbwp_xcor_correction.png`

---

# 6. Robust surface-consistent deconvolution

---

## Slide 34 — The problem: complex near-surface, low S/N
- Conventional SCD uses least-squares (L2), assuming Gaussian residuals.
- That holds for a simple near-surface at high S/N.
- It breaks down over complex near-surface (loose/rocky soil, karst, permafrost, urban noise).
- Ground roll, noise bursts, and up to 20% contaminated traces give heavy-tailed (non-Gaussian) errors.
- The L2 solution is pulled toward outliers, producing erratic operators that amplify noise.
- Figure: none

---

## Slide 35 — The robust solution: hybrid L1/L2
- Replace pure L2 with a hybrid L1/L2 norm (Zhang & Yuan, 2019).
- L2 on the signal residuals: minimum-variance estimate for Gaussian signal.
- L1 on the noise outliers: large errors contribute linearly, so they have less influence.
- The decomposition stays unbiased even with 20% contaminated traces.
- Figure: none

---

## Slide 36 — Three-step robust procedure
- Step 1 — Spectral analysis: compute log amplitude spectra; ln A = ln A_s + ln A_g + ln A_m + ln A_o.
- Step 2 — Robust decomposition: solve the four spectra with hybrid L1/L2 (JOR iterative solver).
- Operators are computed per frequency band, weakened automatically in noise-dominated bands.
- Step 3 — Spectral application: apply the stable operators to all traces.
- Figure: none

---

## Slide 37 — Field data results
- Foothill data from southern China (Zhang & Yuan, 2019): complex near-surface, low S/N.
- Effective bandwidth: original 8–55 Hz; after conventional SCD 6–65 Hz; after robust SCD 4–90 Hz.
- Robust SCD broadens bandwidth by ~25 Hz at both the low and high ends.
- The stack shows improved S/N and spatial energy consistency, without erratic amplitude variations.
- Figure: `term03_lec05_robust_scd_data.png`

---

# 7. Summary

---

## Slide 38 — Key takeaways (1)
- Broadband = 6+ octaves (e.g., 2–128 Hz): sharper wavelets, lower side lobes.
- Ghost notches (f_n = n v_w / 2d) are the main marine bandwidth limit and vary with offset.
- Marine chain: de-bubble → deghosting → designature; the order matters.
- Modern deghosting handles the angle dependence: bootstrap, PZ, sparse, low-frequency.
- Figure: none

---

## Slide 39 — Key takeaways (2)
- Land is harder: coupling, Q, colored reflectivity, and noise create non-minimum-phase components.
- MBWP builds the wavelet from physical components with two free parameters (Q, S/N).
- MBWP corrects the non-minimum-phase residuals SCD leaves behind.
- Robust SCD uses hybrid L1/L2 for non-Gaussian noise, giving stable operators and broader bandwidth.
- Figure: none

---

## Slide 40 — The big picture
- Marine de-bubble + designature: source bubble and phase; needs a known source signature.
- Marine deghosting: ghost notches; needs accurate geometry or special sensors.
- Land SCD: surface-consistent variations; assumes minimum phase, no Q or detector modeling.
- Land MBWP: non-minimum-phase residuals; needs measured responses.
- Land robust SCD: unstable operators from inconsistent noise; still assumes minimum phase for phase.
- Figure: none
