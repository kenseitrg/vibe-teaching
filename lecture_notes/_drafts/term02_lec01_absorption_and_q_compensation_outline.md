# Term 2 Lecture 01 — Absorption and Q-Compensation: Lecture Outline

## Overview

**Duration:** 90 minutes  
**Topic:** Seismic absorption — physical mechanisms, the quality factor Q, causality and velocity dispersion, models of Q, inverse Q filtering (theory and practice), and Q estimation  
**Prerequisites:** Term 1 Lecture 02 (amplitude effects, spherical divergence, absorption mentioned qualitatively), Term 1 Lecture 05 (spectral analysis, Fourier transform), Term 1 Lecture 06 (deconvolution, minimum phase)  
**Slide deck base:** `slides/raw/q_compensation.pptx` (RU, image-rich), `slides/raw/Q-Compensation P22.pptx` (Q tomography / imaging)

---

## Section 1: Motivation — what absorption does to seismic data (7 min)

### 1.1 Real-data example (4 min)
- Stack / section imaged with and without Q-compensation (raw deck slide 1)
  - Notice: deeper events are weaker and lower-frequency; Q-compensation restores resolution
- Frequency panels of the same data: 10–20 Hz vs 50–60 Hz (raw deck slides 3–4)
  - Notice: low frequencies survive to great depths, high frequencies die out quickly
- Consequences for processing: resolution decreases with traveltime/depth; wavelet is not stationary — it changes with time; amplitude and phase are both affected

### 1.2 Position in the processing flow (3 min)
- Absorption correction sits between amplitude recovery (geometric spreading) and deconvolution — or is merged into imaging (Q-migration)
- What we need to apply it: a Q value/model (how to estimate — Section 6) and a compensation operator (Sections 4–5)
- **Figure 1:** Real-data with/without absorption compensation + frequency panels (reuse raw deck images)

---

## Section 2: Absorption mechanism and the definition of Q (13 min)

### 2.1 What causes absorption (4 min)
- Intrinsic (anelastic) attenuation vs scattering attenuation — both attenuate, only intrinsic converts energy to heat; in practice they are hard to separate and are treated together
- Physical mechanisms: grain-boundary friction / relative grain motion, viscous pore-fluid flow (squirt flow), fluid relaxation — energy lost per oscillation cycle
- Key experimental fact: for most dry/consolidated rocks the loss **per cycle** is nearly frequency-independent over the seismic band → motivates constant-Q thinking
- Absorption is proportional to the number of cycles experienced: high frequencies complete more cycles per second → die faster

### 2.2 Definition of Q via energy and amplitude (5 min)
- Energy definition: $Q = 2\pi \dfrac{E}{\Delta E}$ — energy stored vs energy lost per cycle
  - Worked example: Q = 50 → about 12.6% of wave energy lost per cycle; after N cycles, $E_N = E_0 e^{-2\pi N/Q}$
- Amplitude form over traveltime $t$: $A(\omega, t) = A_0(\omega)\,\exp\!\big(-\dfrac{\omega t}{2Q}\big)$
  - Equivalence: $t = N\,T = N\,2\pi/\omega$ recovers the per-cycle decay
  - Absorption coefficient: $\alpha(\omega) = \dfrac{\omega}{2Qv}$, amplitude decays as $e^{-\alpha x}$ with distance
- Typical values: shallow unconsolidated Q = 10–30; consolidated sediments Q = 50–150; carbonates Q > 150
- **Figure 2:** Q definition — energy loss per cycle and exponential amplitude decay over many cycles (Q = 50 vs Q = 200)

### 2.3 Consequences to seismic data (4 min)
- Amplitude spectrum: high frequencies attenuated more → spectrum shifts toward low frequencies with traveltime (dispersion of the spectrum, not the ray!)
- Wavelet: broadens, peak moves to later times (lower frequencies travel slower — Section 3)
- Resolution: tuning thickness and wavelet duration worsen with depth
- Contrast with geometric spreading: spherical divergence is frequency-independent and fully reversible; absorption is frequency-dependent and only partly reversible (noise, instability — Sections 4–5)
- **Figure 3:** Synthetic pulse propagation in constant-Q medium — traces at increasing traveltime with their amplitude spectra; notice broadening, delay, and downward centroid shift

---

## Section 3: Causality requires velocity dispersion — Kramers–Kronig relations (13 min)

### 3.1 Why absorption without dispersion is impossible (5 min)
- Thought experiment: a filter that attenuates high frequencies but passes all frequencies at the same speed → its impulse response is a symmetric (zero-phase) wavelet → it starts before t = 0 → acausal
- Principle: any **linear causal** system (response cannot precede input) must have connected amplitude and phase spectra
- Seismic propagation is (to good accuracy) linear and causal → absorption necessarily implies velocity dispersion
- Reference: Futterman (1962) — "absence of accompanying dispersion implies a nonlinear wave equation"

### 3.2 Kramers–Kronig relations (4 min)
- Statement: for a causal transfer function $H(\omega)$, real and imaginary parts are a Hilbert-transform pair:
  $$\operatorname{Re} H(\omega) = \frac{1}{\pi}\, \mathrm{P}\!\!\int_{-\infty}^{\infty} \frac{\operatorname{Im} H(\omega')}{\omega' - \omega}\, d\omega', \qquad \operatorname{Im} H(\omega) = -\frac{1}{\pi}\, \mathrm{P}\!\!\int_{-\infty}^{\infty} \frac{\operatorname{Re} H(\omega')}{\omega' - \omega}\, d\omega'$$
- Application to absorption: attenuation law $\alpha(\omega)$ → phase velocity $v(\omega)$ is determined (not free!) — dispersion is **uniquely determined** by the absorption law
- Full step-by-step derivation (causality → analyticity → KK) in the derivation document `kramers_kronig_dispersion_derivation.en.md`

### 3.3 Magnitude of dispersion in seismic bands (4 min)
- Futterman's result: with a low-frequency cutoff $\omega_0$ (below which attenuation is set to zero to keep the theory physical), for frequencies well above $\omega_0$:
  - attenuation grows linearly with frequency (near-constant Q)
  - phase velocity: $\dfrac{v(\omega_r)}{v(\omega)} \approx 1 + \dfrac{1}{\pi Q} \ln\dfrac{\omega_r}{\omega}$ (logarithmic dispersion)
- Wang's (Kjartansson-type) power law: $\dfrac{v(\omega)}{v(\omega_r)} = \left(\dfrac{\omega}{\omega_r}\right)^{\gamma}$, $\gamma = \dfrac{1}{\pi}\arctan\dfrac{1}{Q} \approx \dfrac{1}{\pi Q}$
- Numbers: Q = 50, 10 → 100 Hz → velocity changes by ~2–4%; traveltime differences of tens of ms at 2–3 s — visible, matters for well ties and 4D
- Higher frequencies travel faster → the low-frequency tail of the wavelet lags → wavelet stretches and its peak is delayed (this is the "delay of lower frequencies" from Section 2.3)
- **Figure 4:** Velocity dispersion curves $v(\omega)/v(\omega_r)$ for Q = 50, $f_\text{ref}$ = 100 Hz — Futterman's logarithmic law vs Wang's power law (replicates raw deck slide 5); annotate Δv/v over the seismic band

---

## Section 4: Models of Q and their properties (12 min)

### 4.1 Why we need models (2 min)
- Q-compensation needs a complete propagation law: amplitude decay **and** dispersion, consistent with each other (causality!) — a "model of Q" is the pair $\alpha(\omega),\, v(\omega)$
- Kjartansson (1979) Table 1 organizes the classical theories by linearity, Q(f), v(f), creep, pulse broadening

### 4.2 Four classical model families (7 min)
1. **Frictional (Born, White):** rate-independent friction between grain contacts
   - Q independent of frequency — matches experiment — BUT nonlinear, amplitude-dependent, and produces acausal/distorted responses → unacceptable for linear processing
2. **Voigt–Ricker (viscous):** adds a velocity-proportional damping term to the stress–strain law
   - Linear, causal, analytic (Ricker wavelet!) — but $1/Q \propto \omega$: Q grows linearly with frequency → contradicts measurements; velocity constant at low frequencies (no dispersion where it matters); pulse broadening $\propto \sqrt{t}$
   - Historical role: Ricker's wavelets are still used everywhere — but as a wavelet shape, not as an earth model
3. **Kolsky–Futterman / near-constant Q (NCQ):** linear creep law, nearly constant Q over any finite band
   - Causal, Q ≈ const in seismic band, logarithmic dispersion; requires a low-frequency cutoff $\omega_0$; the working model behind most processing implementations (including Paradigm QAPP FUTTOPT)
4. **Kjartansson constant Q (CQ):** power-law creep → **exactly** constant Q for all frequencies
   - Fully specified by two parameters $(Q, v_r)$; $v(\omega) = v_r\,(\omega/\omega_r)^{\gamma}$, $\gamma = \tfrac{1}{\pi}\arctan(1/Q)$
   - Self-similar pulse propagation: pulse shape is preserved, width grows strictly linearly with traveltime; no cutoff needed; the model behind Wang's inverse Q filter
- **Figure 5:** Four model families — small multiples of $Q(f)$ and $v(f)$; notice which are linear, which are causal, which match the "loss per cycle ≈ constant" observation

### 4.3 Which models are used in practice (3 min)
- Processing software (e.g., QAPP): Futterman (Kolsky–Futterman) or Kjartansson/Wang operators — user picks via an option switch
- Physics/FWI: constant Q (Kjartansson) — memory-variable formulations
- Takeaway for students: exact model choice matters little for Q ≥ 30 (they differ by fractions of a percent in $v(\omega)$); consistency (causal amplitude–phase pair) matters a lot

---

## Section 5: Q-compensation — Futterman's and Wang's approaches (15 min)

### 5.1 Forward problem: the earth Q filter (4 min)
- One-way propagation through constant-Q medium for traveltime $t$:
  $$U(t, \omega) = U(0,\omega)\; \underbrace{\exp\!\Big(-\frac{\omega t}{2Q}\Big)}_{\text{amplitude decay}}\; \underbrace{\exp\!\big(i\,\phi(\omega, t)\big)}_{\text{dispersion phase}}, \qquad \phi(\omega,t) \text{ from } v(\omega)$$
- The recorded trace = reflectivity convolved with a **time-varying** (nonstationary) Q filter — deeper reflectors see a different wavelet
- Consequence: ordinary (stationary) deconvolution cannot undo absorption; we need a nonstationary inverse

### 5.2 Futterman's approach — phase correction via Hilbert transform (4 min)
- Futterman (1962): the dispersion is the Hilbert transform of the attenuation — given $\alpha(\omega)$, compute $v(\omega)$, then apply the exact phase inverse
- Hargreaves & Calvert (1991) made it practical: phase-only inverse Q as a Stolt-like constant-$Q$ phase correction
- Phase operator is a pure time shift per frequency — **unconditionally stable**: a "one-time-per-frequency" correction, no amplitude blow-up
- What it fixes: wavelet stretching/delay, event timing; what it does not fix: the lost high-frequency amplitudes

### 5.3 Wang's approach — full (amplitude + phase) inverse with stabilization (7 min)
- Wang (2002, 2006): inverse Q filtering = wavefield **downward continuation** (like migration); layered/variable Q handled by continuation through each layer
- Amplitude compensation operator $\exp\!\big(+\frac{\omega t}{2Q}\big)$ grows exponentially in both frequency and traveltime → **numerically unstable** — boosts noise, overflows
- Stabilization: cap the maximum gain (Paradigm QAPP `MAXDB` parameter: maximum amplitude increase in dB; Wang's $\sigma$ factor); the operator becomes a **clipped** exponential — full boost at low f / early t, bounded boost at high f / late t
- Phase operator applied exactly (stable), amplitude operator stabilized — Wang's key insight
- **Figure 6:** Amplitude compensation operator heat-map $\Lambda(t, f)$ without and with stabilization; notice the exponential wall at late t / high f and the clipped plateau
- **Figure 7:** Synthetic example — original, absorbed, amplitude-only correction, phase-only, amplitude + phase (mirrors raw deck slide 9); notice each mode fixes one symptom
- Where applied today: time-domain nonstationary filtering (post-stack or pre-stack), or inside migration — Q tomography builds interval Q cubes, migration compensates per ray path (raw deck slides 6–7, P22 deck)

---

## Section 6: Practical Q-compensation (12 min)

### 6.1 Choosing the reference frequency (4 min)
- Dispersion laws give velocity **relative to a reference** $f_\text{ref}$: the operator does not change amplitudes/arrival times at $f_\text{ref}$ — it re-anchors the wavelet there
- Choices and effects: $f_\text{ref}$ at the dominant frequency (keeps events at their picked times) vs high reference (events move earlier — important for well ties and 4D consistency)
- Tie to velocity analysis: dispersion biases picked velocities (apparent velocity depends on the frequency content used for picking) — mention Simangunsong/velocity-bias discussion
- In QAPP-type software the reference frequency is an explicit user parameter

### 6.2 Amplitude damping factor / stabilization level (4 min)
- The gain limit (MAXDB / $\sigma$) trades resolution for noise: too low → no visible boost; too high → noise and artifacts amplified, ringing
- QC: compare amplitude spectra and difference panels before/after; the boosted band should end where signal dies into noise
- Rule of thumb: start conservative (e.g., 20–30 dB), increase while monitoring S/N in a difference plot

### 6.3 Amplitude-only, phase-only, amplitude–phase (2 min)
- Phase-only: safest, stable, fixes timing/stretching — use when amplitudes are for AVO or noise is heavy
- Amplitude-only: rarely used alone — leaves the wavelet stretched
- Amplitude + phase: full inverse Q — resolution enhancement, default for imaging targets
- Where in the flow: before deconvolution? after? — conventional order and why (decon assumes stationarity; Q-comp makes the wavelet more stationary again)

### 6.4 Q-compensation in imaging (2 min)
- Modern deep-water / complex areas: absorption compensation inside migration using interval-Q models from Q tomography (raw deck slide 6–7; P22 deck)
- Benefits shown on real data: fault imaging, vertical resolution increase at target level

---

## Section 7: Estimation of Q (13 min)

### 7.1 What we estimate from (2 min)
- Wells: VSP (direct transmission between receiver levels — cleanest), sonic logs, cross-dipole
- Surface data: CMP gathers / stacks — effective Q (averaged along the path), noisier but always available
- Data preparation: minimal processing (no AGC! — gain destroys the amplitude decay we need), noise attenuation OK, spectrogram QC first (QEST recommendation)

### 7.2 Spectral-ratio method + derivation (4 min)
- Take two time windows $t_1, t_2$ (VSP levels or reflection windows): amplitude ratio cancels the source term:
  $$\ln\frac{A(\omega, t_2)}{A(\omega, t_1)} = -\frac{\omega\,(t_2 - t_1)}{2Q} + \text{const}$$
  - slope of a straight line in $\omega$ → $Q$; **derivation inline in the notes** (half a page: from the decay law through source-term cancellation to the linear fit)
- Best method in noise-free synthetic tests (Tonn 1991); degrades quickly with noise; sensitive to windowing and tuning effects

### 7.3 Central (centroid) frequency shift method (3 min)
- Quan & Harris (1997): absorption shifts the **centroid** $f_c$ of the spectrum downward; with a Gaussian-shaped source spectrum of variance $\sigma_f^2$:
  $$f_{c,2} - f_{c,1} = -\frac{\sigma_f^2 (t_2 - t_1)}{\pi Q}\ \Rightarrow\ Q \text{ from centroid drift vs time}$$
- Robust to noise (uses the whole spectrum, not a pointwise ratio); needs a bandwidth where centroids are measurable; assumes spectrum shape roughly Gaussian

### 7.4 Least-squares spectrum modelling and wavelet optimization (4 min)
- Spectrum modelling (Janssen, Tonn, Blias; QEST): model the measured amplitude spectrum as $A_0\,t^\beta \exp(-\omega t / 2Q)$ — estimate $Q$ and amplitude factors jointly by least squares (QEST VARAMP/CNSTAMP variants); avoids the spectral division of the ratio method
- Wavelet-optimization / match-filter (Raikes & White; Cheng & Margrave time-domain match-filter): model the absorbed wavelet for trial Q, match to the data in time domain, minimize misfit — most robust on noisy reflection data
- Practical comparison (Cheng & Margrave 2012/2013): spectral ratio best noise-free; centroid shift robust; match-filter best overall on real reflection data
- Output QC: effective Q vs interval Q (layer-stripping inversion, like interval velocities), constant-Q approximation sanity check
- **Figure 8:** Spectral-ratio method — two windowed spectra, log-ratio vs frequency, fitted line, slope → Q
- **Figure 9:** Centroid-frequency shift — spectra with centroids at two traveltimes; centroid vs time; drift → Q

---

## Section 8: Summary and comprehension questions (5 min)

- Absorption = per-cycle energy loss → HF die first → wavelet broadens and delays; Q quantifies it
- Causality ties absorption to dispersion (KK) — the two must be compensated together
- Models: Born-White (acausal), Ricker (wrong Q(f)), Kolsky-Futterman (practical), Kjartansson (elegant, exact CQ)
- Compensation: Futterman phase (stable) + Wang stabilized amplitude (MAXDB); reference frequency anchors the result
- Estimation: spectral ratio (clean data), centroid shift (robust), LS/wavelet modelling (reflection data)

Comprehension questions (in notes + exercises file):
1. Why is absorption without velocity dispersion physically impossible for a linear earth?
2. Compute the amplitude ratio at 40 Hz after 2 s for Q = 60. What is it at 10 Hz?
3. Why does the amplitude operator of inverse Q filtering need stabilization while the phase operator does not?
4. You must estimate Q from a noisy land CMP gather — which method and why?
5. What is the role of the reference frequency, and why can a poorly chosen one hurt a 4D project?
6. Why does AGC before Q-estimation destroy the estimate?

---

## Figures plan

| # | Concept | Script | Reuse from raw deck? |
|---|---------|--------|---------------------|
| 1 | Real-data motivation: with/without Q, frequency panels | — | yes (slides 1, 3, 4) |
| 2 | Q definition: energy per cycle, exponential decay | `plot_q_definition.py` | no |
| 3 | Pulse broadening in constant-Q medium + spectra | `plot_pulse_broadening.py` | no |
| 4 | Velocity dispersion: Futterman vs Wang, Q = 50 | `plot_velocity_dispersion.py` | replicates slide 5 |
| 5 | Four Q-model families: Q(f), v(f) | `plot_q_models.py` | no |
| 6 | Stabilized amplitude operator heat-map | `plot_inverse_q_operator.py` | no |
| 7 | Compensation modes on synthetic | `plot_compensation_modes.py` | mirrors slide 9 |
| 8 | Spectral-ratio method | `plot_spectral_ratio.py` | mirrors slide 11 |
| 9 | Centroid frequency shift | `plot_centroid_shift.py` | mirrors slide 11 |

Real-data images to reuse from raw decks: Q-tomography amplitude/Q cubes (slide 6), migration with/without Q (slide 7), well-based estimation (slide 10), Q tomography in imaging (P22 slides 2–4).

## Derivation documents

1. `kramers_kronig_dispersion_derivation.en.md` — causality → KK relations (Schönleber system-theory route: causal impulse response → analytic transfer function → Hilbert-transform pair), then Futterman's dispersion equation with low-frequency cutoff, near-constant-Q approximation, Kjartansson exact constant-Q law, Wang's velocity ratio. **Requested by instructor.**

The spectral-ratio and centroid-shift derivations stay inline in the lecture notes (instructor decision).

## Wiki updates

New concept pages: `seismic_absorption.md`, `velocity_dispersion.md`, `q_models.md`, `inverse_q_filtering.md`, `q_estimation.md`  
New source pages: `futterman_1962_dispersive_body_waves.md`, `kjartansson_1979_constant_q.md`, `wang_2002_stable_inverse_q.md`, `wang_2006_inverse_q_resolution.md`, `schonleber_2014_kk_system_theory.md`, `cheng_margrave_2012_2013_q_estimation.md`, `paradigm_qapp_qest.md`

## Notation to add to glossary (AGENTS.md)

| Symbol | Meaning | Russian term |
|--------|---------|--------------|
| $\alpha(\omega)$ | Absorption coefficient | коэффициент поглощения |
| $v(\omega)$, $c(\omega)$ | Frequency-dependent phase velocity | фазовая скорость (дисперсионная) |
| $f_\text{ref}$, $\omega_r$ | Reference frequency | опорная частота |
| $\omega_0$ | Low-frequency cutoff (Futterman) | граничная (низкочастотная) частота отсечки |
| $\gamma$ | Constant-Q velocity exponent, $\tfrac{1}{\pi}\arctan(1/Q)$ | показатель степени постоянного Q |
| $f_c$ | Centroid (central) frequency | центральная частота |
| $\sigma_f^2$ | Spectral variance of source spectrum | дисперсия спектра |
| $\Lambda(\tau, \omega)$ | Stabilized amplitude compensation operator | стабилизированный амплитудный оператор |
| MAXDB | Maximum gain limit in dB (stabilization) | предельное усиление (дБ) |
| $Q^{-1}$ | Specific dissipation (loss) factor | фактор потерь |
