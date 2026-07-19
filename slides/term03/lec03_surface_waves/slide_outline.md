# Slide outline — Term 3, Lecture 3: Surface Waves

---

## Slide 1 — Title
- Surface Waves
- Term 3, Lecture 3
- Figure: none

---

## Slide 2 — Learning objectives
- Describe Rayleigh and Love surface waves and their particle motion.
- Explain why surface waves are noise for reflection processing but signal for near-surface characterization.
- Define phase velocity and group velocity and explain how dispersion arises in a layered medium.
- Sketch how a layered medium produces multiple surface-wave modes and why each mode samples depth differently.
- Explain why conventional filters fail to remove surface waves without damaging reflections.
- Describe the FK-MUSIC dispersion-spectrum workflow and how to pick dispersion curves.
- Explain how a dispersion curve is inverted for a near-surface Vs profile and how multiple modes can constrain Vp/Vs.
- Figure: none

---

## Slide 3 — Why this lecture matters
- On land, ground roll — a train of surface waves — is the largest-amplitude event on a shot gather.
- Surface waves overlap reflections in both time and frequency.
- They are noise for reflection imaging, but carry valuable near-surface Vs information.
- Figure: none

---

## Slide 4 — Rayleigh waves
- Travel along the free surface; P and SV motion couple at the stress-free boundary.
- Phase velocity VR ≈ 0.92 Vs (for Poisson's ratio 0.25) — slower than P and S.
- Particle motion: retrograde elliptical in the vertical plane (x–z).
- Amplitude decays exponentially with depth, negligible within ~1 wavelength.
- Non-dispersive on a homogeneous half-space.
- Figure: none

---

## Slide 5 — Particle motion: Rayleigh and Love
- Rayleigh: retrograde ellipse in x–z plane.
- Love: horizontal transverse motion (y); requires a low-velocity layer over a faster half-space.
- Love waves cannot exist on a homogeneous half-space.
- Figure: `term03_lec03_particle_motion.png`

---

## Slide 6 — Surface waves on a shot gather
- Ground roll: high-amplitude, low-velocity (100–1000 m/s), low-frequency (5–30 Hz) train.
- Fans out from the source; mixed with direct arrivals and air waves.
- 2D spreading (1/r decay) vs 3D for body waves (1/r²) — surface waves dominate at late times and near offsets.
- Figure: none

---

## Slide 7 — Noise for reflection processing, signal for near-surface
- Reflection processing: surface waves are coherent noise masking near-offset reflections.
- Near-surface characterization: the same waves are signal — their dispersion curve constrains Vs.
- MASW (active source) and SWI (passive ambient noise) exploit this dual role.
- Figure: `term03_lec03_ground_roll_removal.jpg`

---

## Slide 8 — Dispersion: physical origin
- In a homogeneous half-space, Rayleigh velocity is constant — no dispersion.
- In a layered medium, phase velocity c(f) depends on frequency.
- Different frequencies sample different depths:
  - Low frequency (long λ) → deeper, faster material → higher c.
  - High frequency (short λ) → shallow, slower material → lower c.
- Figure: none

---

## Slide 9 — Phase velocity and group velocity
- Phase velocity c = ω/k = fλ: speed of a single frequency component.
- Group velocity U = dω/dk: speed of the energy packet (envelope).
- Non-dispersive: c = U. Dispersive: crests migrate through the envelope.
- Figure: `term03_lec03_phase_and_group_velocity.png`

---

## Slide 10 — Two-layer model and the dispersion curve
- Two-layer example: Vs = 200 m/s over 500 m/s half-space.
- High f: c → VR,1 ≈ 184 m/s (shallow layer).
- Low f: c → VR,2 ≈ 460 m/s (half-space).
- Dispersion curve encodes the velocity structure — the key observable in surface-wave methods.
- Figure: `term03_lec03_dispersion_curve.png`

---

## Slide 11 — Wavelength–depth rule of thumb
- λ ≈ c/f ≈ VR/f.
- Penetration depth scales roughly with λ.
- Example: 10 Hz Rayleigh wave at 300 m/s → λ ≈ 30 m → samples upper ~30 m.
- Figure: none

---

## Slide 12 — Multimodality: fundamental and higher modes
- A layered medium supports a family of modes: fundamental, first overtone, second overtone, etc.
- Each mode has its own phase velocity at each frequency.
- Higher modes exist above cut-off frequencies; which modes are observed depends on source depth and velocity structure.
- Figure: none

---

## Slide 13 — Depth sensitivity of modes
- Fundamental mode: simplest depth dependence, most energetic at low frequencies.
- Higher modes: more zero crossings, sample different depth ranges.
- In normally dispersive profiles, fundamental mode dominates; in strong contrasts, higher modes can dominate.
- Figure: `term03_lec03_mode_depth_sensitivity.png`

---

## Slide 14 — Why multimodality matters
- Combining modes in inversion improves depth resolution and vertical resolution.
- Higher modes help constrain Vp/Vs (Poisson's ratio), important for saturated vs. unsaturated soils.
- Mode misidentification (especially from LVL-guided waves) is a common pitfall.
- Figure: none

---

## Slide 15 — Why conventional filters fail
- Surface waves and reflections overlap in time and frequency.
- Band-reject filter removes reflections in the same band.
- Velocity filters (FK fan) fail because surface waves are dispersive — velocity changes with frequency.
- Coupling variations, topography, and near-field effects compound the problem.
- Figure: none

---

## Slide 16 — Surface-wave analysis: the beamforming idea
- Goal: transform a multichannel shot gather into a dispersion image (energy vs. phase velocity and frequency).
- Core idea: cancel the phase accumulated by plane-wave propagation using trial velocities.
- At each frequency, shift traces by the expected phase for trial c, then stack.
- Constructive interference at true modal velocities → peaks in the dispersion image.
- Figure: none

---

## Slide 17 — Frequency-domain slant-stack
- At each frequency ω, apply phase shift e^{-ikxi} to each receiver i and sum.
- S(ω, k) = Σ U(xi, ω) e^{-ikxi}.
- Peaks in |S| → modal wavenumbers; convert k to c = ω/k.
- Fast and simple, but resolution limited by array aperture.
- Figure: none

---

## Slide 18 — Conventional beamforming and the correlation matrix
- Spatial correlation matrix R = YY† encodes receiver-pair correlations.
- Steering vector e: expected phase shifts for trial velocity c.
- Beamformer output: P(c) = e† R e.
- Peaks at true modal velocities; slant-stack is a special case.
- Figure: none

---

## Slide 19 — FK-MUSIC: using the noise subspace
- Decompose R into eigenvectors: signal subspace (large eigenvalues) and noise subspace (small eigenvalues).
- Signal subspace spans the modes; noise subspace spans directions with only noise.
- MUSIC pseudo-spectrum: PMUSIC(f, c) = 1 / Σ|e†ui|² over noise eigenvectors.
- When c matches a true mode, steering vector is orthogonal to noise → sharp peak.
- Figure: none

---

## Slide 20 — FK-MUSIC vs conventional methods
- MUSIC measures how well the steering vector aligns with the noise — a more sensitive discriminator than direct stacking.
- Produces sharper dispersion spectra with better mode separation.
- Sensitive to noise and model errors; validate against simpler methods.
- Figure: `term03_lec03_fk_music_comparison.png`

---

## Slide 21 — Picking dispersion curves
- Identify continuous, high-amplitude branches on the FK-MUSIC image.
- Use expected velocity range to distinguish fundamental from higher modes.
- Window in group-velocity domain to suppress unwanted modes and reveal overtones.
- Be cautious: artefacts can resemble real modes.
- Figure: none

---

## Slide 22 — Practical requirements
- Array aperture: 3–4× longest wavelength of interest.
- Station spacing: Nyquist wavenumber kN = π/Δx must exceed maximum wavenumber.
- Time windowing in group-velocity domain essential for extracting higher modes.
- High-resolution methods (MUSIC, Capon) improve mode separation but need careful validation.
- Figure: none

---

## Slide 23 — MASW/SWI workflow
- Acquire surface-wave data (active or passive).
- Extract experimental dispersion curve for one or more modes.
- Build starting layered model (thickness, Vs, Vp, density).
- Compute theoretical dispersion curve (forward problem).
- Adjust model to minimize misfit (inverse problem).
- Figure: none

---

## Slide 24 — Inversion: forward and inverse problems
- Forward: solve eigenvalue problem for each frequency → theoretical dispersion curves.
- Inverse: non-linear and non-unique — different Vs profiles can produce similar dispersion curves.
- Misfit: Σ[ cobs(f) - cpred(f; Vs) ]² + λ‖D Vs‖² (regularization).
- Use minimum number of layers; fix Vp and density with a priori info.
- Figure: `term03_lec03_inversion_result.png`

---

## Slide 25 — Multi-mode constraint for Vp/Vs
- Fundamental mode alone is primarily sensitive to Vs.
- Higher modes add sensitivity to Vp through P-SV coupling at layer boundaries.
- Combining modes reduces trade-off between layer thickness and velocity.
- Figure: none

---

## Slide 26 — Inversion output and applications
- Output: near-surface Vs profile.
- Geotechnical engineering: site classification (Vs,30), ground-response analysis.
- Static corrections: supplements or replaces refraction-based near-surface model.
- Migration: more accurate near-surface velocity improves prestack depth migration.
- Figure: none

---

## Slide 27 — Modeling: frequency-dependent linear moveout
- Once dispersion curve c(f) is picked, model surface waves on each shot gather.
- For each frequency, shift each trace by t(x, f) = x/c(f).
- Reconstructs predicted surface-wave wavefield with correct kinematics.
- Figure: none

---

## Slide 28 — Spatial smoothing
- After moveout alignment, surface waves are approximately aligned across offsets.
- Apply median filter or spatial average along offset axis.
- Aligned surface waves pass through; misaligned reflections are attenuated.
- Stabilizes model against lateral variations from heterogeneity and coupling.
- Figure: none

---

## Slide 29 — Why adaptive subtraction is needed
- Direct subtraction leaves residual noise because predicted amplitudes and phases don't match exactly.
- Source coupling, scattering, and 3D effects introduce variations the simple moveout model cannot capture.
- The model has the right kinematics but not necessarily the right amplitudes and phases.
- Figure: none

---

## Slide 30 — Adaptive filter: the Wiener connection
- Adaptive subtraction uses a short Wiener-like filter.
- Minimize residual energy: Rmm ĥ = rdm (Wiener–Hopf normal equations).
- Left side: model autocorrelation captures spectral character.
- Right side: data–model cross-correlation captures match at each time shift.
- Filter adjusts model's amplitude and phase; then subtract adapted model from data.
- Figure: none

---

## Slide 31 — Filter-length trade-off
- Short filter (2–5 coefficients): adapts quickly, may not capture full wavelet.
- Long filter (10+ coefficients): matches wavelet better, may also remove reflections.
- Preference: shortest filter that gives acceptable noise removal.
- Figure: none

---

## Slide 32 — Summary
- Rayleigh waves: retrograde elliptical motion, VR ≈ 0.92 Vs; Love waves need a low-velocity layer.
- Dual role: noise for reflections, signal for near-surface Vs.
- Dispersion: low frequencies sense deeper, faster material; dispersion curve encodes velocity structure.
- Multimodality: fundamental and higher modes with different depth sensitivity.
- Conventional filters fail due to time-frequency overlap; model-based adaptive subtraction preferred.
- FK-MUSIC gives high-resolution dispersion spectra using eigenstructure of cross-spectral matrix.
- Inversion yields Vs profile; multiple modes constrain Vp/Vs and reduce non-uniqueness.
- Adaptive subtraction with Wiener-like filter handles amplitude and phase mismatches.
- Figure: none

---

## Slide 33 — Comprehension questions
- Why do surface waves dominate the near offsets of a land shot gather?
- How does particle motion differ between Rayleigh and Love waves?
- Explain dispersion with the "long wavelengths see deeper" intuition.
- What is the difference between phase velocity and group velocity?
- Why does a layered medium support multiple surface-wave modes?
- Why do simple frequency filters often fail to remove surface waves?
- What does FK-MUSIC improve compared with a simple FK spectrum?
- How is a dispersion curve turned into a Vs depth profile?
- Why is the modeled surface wave subtracted adaptively instead of directly?
- What is the practical risk of an adaptive filter that is too long?
- Figure: none
