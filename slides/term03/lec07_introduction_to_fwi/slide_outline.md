# Slide outline — Term 3, Lecture 7: Introduction to Full-Waveform Inversion

---

## Slide 1 — Title
- Introduction to Full-Waveform Inversion (FWI)
- Term 3, Lecture 7
- Conceptual introduction · reused literature figures · light math

---

## Slide 2 — Learning objectives
- Explain the resolution floor of ray-based model building and how FWI passes it.
- Walk through one FWI iteration: modelling → residual → gradient → update.
- Explain cycle skipping with the half-period criterion.
- List the standard non-linearity work-arounds (multiscale, misfits, extensions).
- State the advantages: wavelength-scale models, FWI imaging, multiparameter potential.
- Describe the challenge list: cost vs frequency, starting models, land, physics gaps.

---

## Slide 3 — Why this lecture matters
- Everything so far (statics, velocities, decon, noise, regularization) serves two products: a velocity model and an image.
- Our model-building tools see the earth through the smooth lens of traveltimes.
- Thin reservoirs, small faults, gas pockets, salt interiors — exactly where smooth models give up.
- FWI: use the entire recorded waveform as data for the velocity model.
- From academic dream (1984) to routine marine model building (2010s).

---

# 1. From rays to full wavefields

---

## Slide 4 — The model-building ladder so far
- Semblance / stacking analysis: smooth V_rms from reflection moveout (Term 1).
- Refraction / reflection tomography: picked traveltimes, cell-based rays (Term 3 Lec 02).
- Both are ray methods — the high-frequency approximation.
- Valid when velocity varies gently over a wavelength; breaks when it doesn't.

---

## Slide 5 — When rays break down
- Jones (2019) thought experiment: low-frequency sound meets a boulder-sized anomaly.
- The whole boulder vibrates and re-radiates — a secondary source (diffraction/scattering).
- Applying Snell's law at every point of the corrugated surface is meaningless.
- Anomaly >> wavelength: rays work. Anomaly ≲ wavelength: only wavefield physics describes it — and only wavefield methods can invert it.
- Figure: none

---

## Slide 6 — The resolution floor of ray tomography
- Traveltime tomography resolves ≳ first Fresnel zone width: √(λL) (Williamson 1991).
- Waveform inversion resolves ≈ λ — and below it with reflections/multiples.
- Scale example: λ = 50 m, L = 5 km → ray floor ~500 m; FWI targets 50 m.
- Pratt (1999): controlled crosswell experiment on an epoxy-resin physical scale model — the truth is known exactly.
- Figure: `term03_lec07_ray_vs_waveform_resolution.png`

---

## Slide 7 — The scale-model verdict
- True model: layered block, low-velocity channel, dipping interface, small fault.
- Curved-ray tomography: broad layering only — channel a smudge, fault invisible.
- Bars on the figure: dominant wavelength λ and Fresnel zone √(λL) — the ray floor made visible.
- FWI will resolve the same targets at wavelength scale (shown in §2).
- Figure: `term03_lec07_ray_vs_waveform_resolution.png`

---

## Slide 8 — The FWI idea
- Lailly (1983), Tarantola (1984): model building as full-physics data fitting.
- Start from an initial model → solve the wave equation → synthetic shot gathers.
- Compare wiggle-for-wiggle with field data → compute the model change that reduces mismatch → update → repeat.
- Nothing picked: diving waves, reflections, diffractions, even multiples participate.
- 1980s verdict: "a failure" as velocity estimation (Symes & Carazzone 1991) — waiting for computers, low frequencies, long offsets.

---

## Slide 9 — FWI across nine orders of magnitude
- Same idea from mm to 1000 km: medical imaging, NDT, near-surface, exploration, seismology.
- Different data, frequencies, geometries — same loop.
- This lecture: exploration-scale reflection/refraction FWI.
- Figure: `term03_lec07_fwi_applications_scales.png`

---

# 2. Problem formulation and taming non-linearity

---

## Slide 10 — The FWI loop
- Forward modelling in model m → synthetics d_cal[m].
- Misfit vs field data: classic least squares C(m) = Σ [d_obs − d_cal[m]]².
- Gradient ∂C/∂m via adjoint (back-propagation) modelling.
- Line search → step length → update m.
- Header choices per stage: shots, frequencies, time windows.
- Figure: `term03_lec07_fwi_workflow.png`

---

## Slide 11 — The size of the problem
- 3D model 1000 km² to 10 km: 10⁷ cells at 100 m; 10⁹ at 25 m.
- Each cell may carry Vp, Vs, ρ, ε, δ, Q.
- Cannot scan model space like semblance scans stacking velocity.
- Only local, iterative optimization: gradient descent, conjugate gradients, L-BFGS.
- d_cal[m] depends on m non-linearly — the wavefield changes wholesale when velocity changes.

---

## Slide 12 — The gradient: back-propagating the residual
- Forward-model the source wavefield.
- Back-propagate the residual (observed − modelled) from receivers — exactly what RTM does.
- Correlate the two in time at every point → ∂C/∂m (Tarantola 1984).
- Mental model: FWI = migrate the residual, interpret it as a velocity update.
- Figure: `term03_lec07_gradient_formation.png`

---

## Slide 13 — The gradient looks like a migration
- Single wavelet in the residual → RTM-like impulse response (source-to-receiver arc).
- Full residual shot → superposition of arcs; only the sum over all shots focuses.
- Same constructive/destructive interference logic as migration imaging.
- Figure: `term03_lec07_gradient_impulse_response.png`

---

## Slide 14 — Anatomy of the gradient
- Diving-wave "banana": tomographic sensitivity along the refracted path (shallow).
- Reflection arc: migration-like update (intermediate).
- Cross-talk "rabbit ears": non-physical but useful — reach below diving-wave depth.
- Production sequence: refraction FWI (to ~⅓ max offset), then reflection FWI.
- Figure: `term03_lec07_gradient_components.png`

---

## Slide 15 — Which wavenumbers does FWI update?
- At a scattering point the update carries k = p_r − p_s, with |k| = (2f/v)·cos(θ/2).
- Reflection: θ → 0 → maximum |k| → short wavelengths (reflectivity scale).
- Diving wave: θ → 180° → |k| → 0 → long wavelengths (tomographic scale).
- Explains the gradient anatomy, refraction-then-reflection practice, and why LONG OFFSETS matter for deep updates.
- Figure: `term03_lec07_wavenumber_illumination.png`

---

## Slide 16 — Local descent on the misfit surface
- Gradient direction + line search; repeat (steepest descent → CG → L-BFGS in practice).
- Toy two-parameter picture: contours, start, line minimum, orthogonal next step.
- Real problem: same walk in 10⁷ dimensions.
- Caveat: the surface is not one smooth bowl — next slide.
- Figure: `term03_lec07_cost_function_descent.png`

---

## Slide 17 — Non-linearity: cycle skipping
- Wavelets oscillate → L2 misfit vs time shift is oscillatory: local minima at ±1 period.
- Starting-model error > T/2 → inversion matches the WRONG cycle → converges to a local minimum.
- Half-period criterion (Pratt 1999): predict data within T/2 = 1/2f.
- 20 Hz → 25 ms tolerance; 5 Hz → 100 ms; 2 Hz → 250 ms.
- Low frequencies are forgiving; high frequencies are strict.
- Figure: `term03_lec07_cycle_skipping.png`

---

## Slide 18 — CHECKPOINT: can you start FWI?
- Your starting model has 60 ms rms time error; lowest usable frequency is 4 Hz.
- Safe to start L2 FWI at 4 Hz? At 10 Hz?
- 2 minutes, discuss with a neighbour.
- (Answer: 4 Hz → T/2 = 125 ms > 60 ms — safe. 10 Hz → T/2 = 50 ms < 60 ms — cycle-skipping risk.)
- Figure: none

---

## Slide 19 — Work-around 1: frequency continuation
- Invert the lowest usable band first; add higher batches in a cascade (Bunks 1995, Pratt 1999).
- Each stage starts inside the trust region of the next.
- Field workflow: refraction FWI 3–8 Hz → widen band → reflection FWI.
- The data fit improves band by band — the primary FWI QC.
- Figure: `term03_lec07_data_fit_evolution.png`

---

## Slide 20 — Multiscale in the scale model
- Pratt (1999): successive frequency batches sharpen the model.
- (b) Early stage with wrong Q (=100 vs true ~10): cross-talk artifacts.
- (c) Final stage with realistic Q: artifacts gone, small fault resolved at λ scale.
- Well below the Fresnel-zone floor of ray tomography (bars on figure).
- Figure: `term03_lec07_fwi_multiscale_resolution.png`

---

## Slide 21 — Work-around 2: windowing
- Early arrivals (direct + diving waves) relate most linearly to the shallow model.
- Invert early arrivals first → admit reflections → full trace (Shipp & Singh 2002).
- Same relaxation logic as frequency continuation, applied to the event set.
- Figure: none

---

## Slide 22 — Work-around 3: alternative misfits
- Traveltime / time-shift (cross-correlation) misfits — near-tomography, very robust.
- Adaptive waveform inversion (AWI): matching filter should become a spike (Warner & Guasch).
- Instantaneous phase, dynamic time warping, optimal transport (OT).
- Robust norms (Lp) for heavy-tailed noise.
- Common idea: misfits with wide, well-behaved basins under large time shifts.

---

## Slide 23 — Work-arounds 4–5: extensions and starting models
- Extended formulations: WRI (van Leeuwen & Herrmann 2013), extended source/reflectivity — fit data with an imperfect model, penalize the extension. Research → practice.
- Better starting models: ray tomography, WEMVA (gather flattening), interpretation.
- On land the starting model is often THE decisive factor.
- Figure: `term03_lec07_land_cycle_skipping.png`

---

## Slide 24 — The land cycle-skip story
- Gradient starting model → modelled reflections a full period off — cycle-skipped input.
- Conventional phase-only objective: oscillatory wrong-direction update ("ringing").
- Phase-tolerant objective (DFPD, Zhang & Dai 2015): coherent correct-direction update.
- Then conventional FWI can take over.
- Figure: `term03_lec07_land_cycle_skipping.png`

---

## Slide 25 — The unifying principle
- Every work-around is a RELAXATION: a cascade of simplified FWI problems converging back to the full problem (Métivier & Brossier 2026).
- Frequency continuation relaxes bandwidth; windowing relaxes the event set; misfit design relaxes the metric; extensions relax the model space.
- Modern workflows combine several at once.
- Figure: none

---

# 3. What FWI buys you

---

## Slide 26 — Velocity models at wavelength scale
- An order of magnitude finer detail than ray tomography.
- BP 2004 benchmark: compact high-velocity body + cluster of small gas pockets.
- One reflection-slope FWI iteration already imprints them on the gradient.
- Invisible to ray tomography at these wavelengths.
- Figure: `term03_lec07_bp2004_fwi_resolution.png`

---

## Slide 27 — Land FWI delivering
- Permian Basin field data (Wang et al. 2020).
- Velocity model: smooth initial → detailed FWI model.
- Kirchhoff migration: undulating, defocused reflectors → flat, focused events.
- The classic validation pair: trust the model because the image improves.
- Figure: `term03_lec07_land_fwi_permian.png`

---

## Slide 28 — Land FWI delivering — gather-level QC
- Same validation at the gather level (Wang et al. 2020, Permian Basin).
- Stacks (a/b) and image gathers (c/d) before/after the FWI model.
- Initial-model gathers: strong residual moveout below ~8 kft.
- FWI-model gathers: flat, focused — the same criterion as tomography QC (Term 3 Lec 02).
- Figure: `term03_lec07_land_fwi_gathers.png`

---

## Slide 29 — FWI imaging: the reflectivity byproduct
- High-resolution FWI model ≈ reflectivity model: sharp velocity contrasts = reflectors.
- Take a spatial derivative (1D, 3D dip, plane-wave destructor) → "FWI image".
- No separate migration step; increasingly used alongside / instead of RTM products.
- Caveats: not true impedance reflectivity (no density/AVO); bandwidth = FWI band.
- Figure: `term03_lec07_fwi_imaging_vs_rtm.png`

---

## Slide 30 — FWI imaging vs RTM — salt example
- Campos Basin: FWI image vs RTM with the same FWI model.
- Green arrows: pre-salt fault blocks and fault planes better resolved by FWI imaging.
- FWI image compensates complex overburden wavefield effects.
- Figure: `term03_lec07_fwi_imaging_vs_rtm.png`

---

## Slide 31 — FWI imaging vs RTM — West of Shetlands
- Clair-type section: RTM (final FWI model) vs 3D FWI image.
- Crisper fine layering in the shallow section and along structural flanks.
- FWI imaging as QC for — and increasingly alternative to — conventional imaging.
- Figure: `term03_lec07_fwi_imaging_clair.png`

---

## Slide 32 — Multiparameter potential
- In principle: Vp, Vs, ρ (elastic), Q (visco-acoustic), ε, δ (anisotropic) — Tarantola's original ambition.
- Elastic FWI as a complement to AVO (active research).
- Price 1: parameter cross-talk — updates leak between parameters (Keating & Innanen 2016).
- Price 2: the physics must live in the forward engine.
- Figure: `term03_lec07_acoustic_vs_elastic_fwi.png`

---

## Slide 33 — Physics sets the ceiling
- Synthetic test: acoustic FWI on elastic data → artifacts (velocity pull-down ~10 km).
- Elastic FWI: both Vp and density recovered cleanly.
- Unmodelled physics becomes model error — the inversion absorbs what the engine cannot explain.
- "Elastic modelling/FWI is necessary."
- Figure: `term03_lec07_acoustic_vs_elastic_fwi.png`

---

# 4. Modern challenges

---

## Slide 34 — Cost and its scaling with frequency
- Iterations × shots × (forward + adjoint modelling) — an RTM project per iteration.
- Grid: ~10 points per wavelength → cells grow as f² (2D) / f³ (3D per volume).
- Time step: CFL → steps grow as f. Net: modelling cost ~ f⁴ in 3D.
- Doubling frequency ≈ 16× cost per iteration.
- Start low: convergence strategy AND budget strategy.
- Mitigations: few frequencies per stage (Pratt's frequency domain), simultaneous sources, GPUs.

---

## Slide 35 — CHECKPOINT: the price of frequency
- You double the maximum inverted frequency from 5 to 10 Hz on a fixed survey.
- How does the cost of one iteration change? What ELSE gets harder besides cost?
- 2 minutes, discuss with a neighbour.
- (Answer: ~16x cost per iteration; and the starting-model tolerance tightens fourfold — T/2 shrinks from 100 ms to 50 ms.)
- Figure: none

---

## Slide 36 — Starting models and low frequencies
- Half-period criterion ties starting-model quality to invertible frequencies.
- Subsalt: need ~2 Hz to start from tomography models (Shen et al. 2017).
- Why broadband low-frequency sources matter (Term 3 Lec 05): 2 Hz instead of 8 Hz start = 4× more time tolerance.
- No low frequencies → misfit design + WEMVA starting models carry the load.

---

## Slide 37 — Land: the hard case
- No simple water layer: heterogeneous, attenuative near surface + topography.
- Topography must be modelled (curvilinear grids) or phase errors appear.
- Strong guided/shallow wavefield in synthetics absent in field data — attenuate in BOTH domains.
- Noise (ground roll, cultural), short offsets, irregular geometry.
- Elasticity everywhere; shot-varying source coupling.
- Figure: `term03_lec07_land_noise_conditioning.png`

---

## Slide 38 — Land case study 1: Inner Mongolia
- Short offsets, no low frequencies → reflection FWI from a 1-D gradient start (Zhang & Dai 2015).
- Cycle-skip-tolerant DFPD FWI in 3–8 Hz → WEMVA flattening → RTM.
- Velocity model gains coherent lateral structure; RTM image focuses.
- Land FWI works when the workflow respects its preconditions.
- Figure: `term03_lec07_land_fwi_inner_mongolia.png`

---

## Slide 39 — Land case study 2: onshore Mexico (DMFWI)
- Dynamic-matching FWI: cross-correlation objective, amplitude-insensitive, noise-robust (Sheng et al. 2022).
- Tomography-derived starting model; gather-flatness QC.
- Kirchhoff PSDM before/after: fault-plane imaging improves (red arrows).
- FWI as the sharp tip of the model-building ladder, not its replacement.
- Figure: `term03_lec07_land_fwi_pemex_kirchhoff.png`

---

## Slide 40 — Land case study 2: RTM comparison
- Same DMFWI update, RTM before/after with the velocity model overlaid.
- Reflectors sharpen and continuity improves over the faulted target.
- The same pattern as Kirchhoff — update validated in two imaging engines.
- Figure: `term03_lec07_land_fwi_pemex_rtm.png`

---

## Slide 41 — Physics gaps: elasticity, anisotropy, absorption
- Elasticity: conversions, surface waves → elastic FWI (10–100× cost, cross-talk).
- Anisotropy: TTI imaging world — FWI updates Vp with ε, δ fixed externally, or inverts jointly.
- Absorption: engine must include Q WITH dispersion (Term 2 Lec 01), else velocity/Q ambiguous (Hak & Mulder 2011).
- Pratt's wrong-Q run: the cautionary display (the multiscale scale-model slide).
- Visco-acoustic FWI for Q itself — couples to amplitudes and source.

---

## Slide 42 — Source signature, coupling, amplitudes
- Forward modelling needs every shot's wavelet — phase and amplitude.
- Marine: measured, stable airgun signatures; de-signatured input standard.
- Land: coupling varies shot-to-shot; source-inversion / source-independent FWI.
- Amplitude fidelity: spreading, receiver coupling, directivity bias the update.
- Gradient often amplitude-balanced to focus on kinematics.

---

## Slide 43 — Data quality and preprocessing
- "No processing needed" is a half-truth.
- Light denoise + amplitude recovery; multiples/ghosts CAN stay (two-way engine reproduces them).
- Born-type reflection FWI: multiples must go.
- Geometry errors, dead channels, polarity flips leak into the gradient.
- Final QC pair: data fit (red vs blue wiggles) + image/gathers with the updated model.

---

# 5. Summary

---

## Slide 44 — Key takeaways
- Rays: Fresnel-zone floor √(λL). FWI: full waveforms through a wave-equation engine, resolves ~λ.
- FWI loop: modelling → residual → gradient (RTM of the residual) → line search → update.
- Non-linearity = oscillatory wavelets: |Δt| < T/2 or cycle skipping.
- Work-arounds = relaxations: multiscale, windowing, misfit design, extensions, starting models.
- Advantages: wavelength models, FWI imaging, multiparameter (with cross-talk).
- Challenges: f⁴ cost, low frequencies/starting model, land, physics gaps, source, data quality.

---

## Slide 45 — The big picture
- Table: stacking analysis vs ray tomography vs FWI (data, physics, resolution, non-linearity, cost, preconditions).
- FWI does not replace the ladder — it stands on it: tomography/WEMVA starting models, statics for land near surface, broadband acquisition.
- Processing stream and inversion are converging (Symes' "rational replacement" vision).

---

## Slide 46 — Comprehension questions
- Why can ray tomography not resolve wavelength-scale structures? State the floor.
- Walk through one FWI iteration; why is the gradient "migration of the residual"?
- Starting model 60 ms rms error: up to which frequency can you safely start?
- Why is frequency continuation also a cost strategy?
- Four reasons land FWI is harder than marine — and where you address each.
- Two QC displays before trusting an FWI model.

---

## Slide 47 — Sources and credits
- Jones (2019) First Break — mechanics tutorial (Figs. 3–7, 9).
- Pratt (1999) Geophysics — scale model (Figs. 3, 7).
- Bohlen KIT FWI course — workflow, scales, data fit, elastic test.
- Zhang & Dai (2015) SPE; Wang et al. (2020) EAGE — land FWI.
- Baldock et al. (2023) EAGE — FWI imaging.
- Métivier & Brossier (2026) GJI — non-convexity review.
- Figures reproduced for teaching with attribution; full credits in the lecture notes.
