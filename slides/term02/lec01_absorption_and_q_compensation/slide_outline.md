# Slide outline — Term 2, Lecture 1: Absorption and Q-Compensation

---


## Slide 1 — Title
- Absorption and Q-Compensation
- Term 2, Lecture 1
- Figure: none

---

## Slide 2 — Learning objectives
- Recognize absorption on real data: frequency panels, systematic spectral decay with traveltime.
- Define the quality factor $Q$ from energy loss and from amplitude decay; know typical rock values.
- Explain why causality forces velocity dispersion (Kramers–Kronig relations).
- Distinguish the four classical Q-model families and say why only two survive in processing.
- Describe inverse Q filtering: stable phase correction, stabilized amplitude correction.
- Choose practical parameters: reference frequency, gain limit, compensation mode.
- Estimate Q from VSP and reflection data: spectral ratio, centroid shift, least-squares modelling, wavelet matching.

---

## Slide 3 — Why this lecture matters
- In Term 1 absorption was one line on the amplitude-effects list: "corrected by Q-compensation, covered later."
- This lecture is that "later."
- Absorption removes high frequencies selectively — a 3-second section is blurrier than a 1-second one.
- It also delays the surviving low frequencies — the wavelet stretches.
- Both effects grow with traveltime: the wavelet is nonstationary, and ordinary (stationary) deconvolution cannot handle that.

---

## Slide 4 — Two sections, one difference
- The same data imaged with and without Q-compensation; acquisition unchanged.
- With compensation: deep events sharper, weak reflectors become visible.
- The deep section stops losing "character" with traveltime.
- Figure: `term02_lec01_realdata_with_without_q.png`

---

## Slide 5 — Frequency panels: the direct evidence
- Filter the data into narrow frequency bands; compare the same section at low and high frequency.
- 10–20 Hz: energy survives to the bottom of the record — deep events are there, just blurry.
- 50–60 Hz: fades gradually with traveltime — where it dies, resolution is gone.
- Absorption signature: smooth, systematic loss with time. Not a notch (ghost / anti-alias), not random (noise).
- Figure: `term02_lec01_realdata_freq_panel_high.png`

---

## Slide 6 — Three consequences we must undo
- **Amplitude decay** depending on frequency and traveltime: deep spectra are tilted toward low frequencies.
- **Wavelet stretching and delay**: low frequencies travel slower (dispersion, next section).
- **Nonstationarity**: the wavelet at 0.5 s and at 3.0 s are different.
- Every stationary step — including Term-1 predictive deconvolution — silently assumes they are the same.

---

## Slide 7 — Where Q-compensation sits in the flow
- **Time-domain processing**: a nonstationary inverse Q filter on traces (prestack or poststack), after spherical-spreading correction, before or together with deconvolution.
- **Inside imaging**: modern migration compensates absorption along the path, using a 3D interval-Q model from Q-tomography.
- Either way, two inputs are always needed:
  - a Q value or model (where does it come from? — Section 7 of the notes)
  - a compensation operator (what does it do, which knobs?)

---

## Slide 8 — Intrinsic versus apparent attenuation
- **Intrinsic (anelastic) absorption**: elastic energy converted to heat — friction at grain contacts, squirt flow, frame relaxation.
- **Scattering**: energy redirected by small-scale heterogeneities (layering, faults, porosity patches); lost from the stack but not converted to heat.
- From surface data the two are nearly indistinguishable — both attenuate and both tilt the spectrum low.
- Processing treats them together as apparent attenuation with an effective $Q$.

---

## Slide 9 — The key experimental fact
- Laboratory and field data on consolidated rocks agree:
- **the fractional energy loss per cycle is nearly independent of frequency** over the seismic band.
- Not per second — per cycle.
- A 50 Hz wave completes 5 times more cycles per second than a 10 Hz wave: it loses energy 5 times faster per second.
- High frequencies die first **because they cycle more, not because each cycle is lossier.**

---

## Slide 10 — Defining Q
- From energy: $Q = 2\pi\, E / \Delta E$ — energy stored over energy lost in one cycle; $Q^{-1}$ is the specific dissipation.
- From amplitude: $A(\omega, t) = A_0 \exp(-\omega t / 2Q)$.
- Worked example, $Q = 50$: each cycle costs $2\pi/Q \approx 12.6\%$ of the remaining energy.
- Ten cycles take 71% of the energy — and a deep reflection has completed thousands of cycles.
- Figure: `term02_lec01_q_definition.png`

---

## Slide 11 — Typical Q values
- Weathered layer, unconsolidated sediments: 10–30.
- Consolidated clastics (sand/shale): 50–150.
- Carbonates, evaporites: 150–300+.
- Deep, tight crystalline rocks: 300–1000.
- Rules of thumb: shallower rocks lose more; $Q$ roughly scales with velocity.

---

## Slide 12 — The amplitude law in numbers
- Take $Q = 50$, reflector at two-way time $t_0 = 2$ s: $A/A_0 = \exp(-\pi f t_0 / Q)$.
- At 10 Hz: keeps ~29% of its amplitude. At 40 Hz: keeps 0.65%.
- One and a half octaves — a factor of 45 in amplitude. This tilt is what we must undo.
- As the wavelet travels: amplitude drops, spectrum centroid shifts low, wavelet lengthens — with the low-frequency tail lagging behind.
- Figure: `term02_lec01_pulse_broadening.png`

---

## Slide 13 — Absorption without dispersion is impossible
- Thought experiment: a medium that absorbs high frequencies with no dispersion — all frequencies same speed.
- Its propagation filter would have zero phase at every frequency.
- Zero phase means a symmetric impulse response — ringing before the input arrives.
- That is acausal: the Earth cannot respond before the source triggers.
- Conclusion: attenuation and phase are two halves of one causal response.

---

## Slide 14 — Kramers–Kronig relations
- For any causal linear system, Re H and Im H are Hilbert-transform duals (Kramers 1927, Kronig 1926).
- Applied to propagation: **choose any attenuation law — the dispersion law is then determined.**
- Futterman (near-constant Q, low-frequency cutoff $\omega_0$): $v(f)/v(f_r) \approx 1 + \ln(f/f_r)/(\pi Q)$
- Kjartansson (exactly constant Q, no cutoff): $v(f)/v(f_r) = (f/f_r)^{\gamma}$, $\gamma = \arctan(1/Q)/\pi$
- For small $1/Q$ these are the same law — do not fear the choice in software.

---

## Slide 15 — How large is dispersion?
- Everything scales as $\ln(\text{frequency ratio})/(\pi Q)$.
- $Q = 50$: velocity changes ~1.5% per frequency decade.
- 10 Hz lags 100 Hz by ~29 ms over $t_0 = 2$ s of travel.
- Small compared with geology — but systematic, frequency-dependent, cumulative with traveltime.
- Figure: `term02_lec01_velocity_dispersion.png`

---

## Slide 16 — Why practitioners should care
- **Well ties**: check-shot data (high f) and surface seismic (low f) sample different points of the dispersion curve — a few-ms mismatch that is physics, not error.
- **Velocity analysis**: picked velocities correspond to the dominant frequency of the data.
- **4D**: different spectra accumulate different dispersion delays; reference frequency is a lever that keeps surveys comparable.
- **Processing**: dispersion correction is a pure phase operation — unconditionally stable, the "safe half" of Q-compensation.

---

## Slide 17 — What a "model of Q" must contain
- Not just a number: a complete **causally consistent pair** — attenuation law $\alpha(\omega)$ plus dispersion law $v(\omega)$.
- Consistent with the Kramers–Kronig relations.
- Amplitude alone, or phase alone, is not a propagation model.
- Never mix an attenuation law from one model with a dispersion law from another — that violates causality.

---

## Slide 18 — The four classical families
- **Frictional** (Born, White, Knopoff): loss per cycle constant — but nonlinear and acausal. Dead end for processing.
- **Voigt–Ricker** (viscous solid): linear, causal — gave us the Ricker wavelet; but $Q \propto f$ contradicts measurements.
- **Kolsky–Futterman** (near-constant Q, NCQ): constant Q over a band with cutoff; logarithmic dispersion. The workhorse of processing software.
- **Kjartansson constant Q** (CQ): exactly constant Q at all frequencies; power-law dispersion. The workhorse of wave-equation methods and Wang's inverse Q filter.
- Figure: `term02_lec01_q_models.png`

---

## Slide 19 — Reading the table like a processor
- The frictional family died of nonlinearity — all seismic processing (superposition, convolution, deconvolution) assumes linearity.
- The Voigt–Ricker family died of wrong $Q(f)$ — but the Ricker wavelet outlived its physics.
- Everything modern is NCQ or CQ; for $Q \ge 30$ they agree to well under a percent — the choice is bookkeeping.
- What matters physically: amplitude and phase come from the same causal pair.

---

## Slide 20 — The Earth Q filter: nonstationary convolution
- Propagation for traveltime $t$ multiplies each frequency component by
- $U(t, \omega) = U(0, \omega)\; \exp(-\omega t / 2Q)\; \exp(i\phi(\omega, t))$
- amplitude decay times dispersion phase — each deeper reflection filtered more.
- A different filter at each record time: nonstationary convolution.
- Why ordinary deconvolution is not enough: a stationary spiking filter finds one wavelet for the whole trace — it can only compromise.
- Q-compensation removes the systematic time-varying part first; deconvolution then works as designed.

---

## Slide 21 — Futterman's phase correction: unconditionally stable
- Correcting dispersion is deterministic: apply the exact opposite phase per frequency — a pure, frequency-dependent time shift.
- The phase operator has unit amplitude at every frequency: it rearranges the spectrum, amplifies nothing.
- Cannot blow up, barely touches noise.
- Fixes: wavelet stretching, systematic delay of low frequencies — better timing, better well ties.
- Does not fix: lost high-frequency amplitudes.

---

## Slide 22 — Wang's amplitude correction: needs stabilization
- Recovering amplitudes requires $\exp(+\omega t / 2Q)$ — exponential growth in both frequency and traveltime.
- $Q = 50$, $t = 2$ s: boost ×150 at 40 Hz, ×3000+ at 60 Hz.
- Beyond the noise floor this amplifies noise — Wang (2002) showed wild oscillations on noise-free synthetics (amplified machine precision).
- Two classical stabilizations:
  - gain-limited filter: clip the boost at a maximum gain (Wang 2002)
  - damped least-squares operator: exact where signal lives, graceful taper where it died (Wang 2006)
- Users specify a gain limit in dB; the factor $\sigma^2$ is computed from it.
- Figure: `term02_lec01_inverse_q_operator.png`

---

## Slide 23 — What each mode fixes: synthetic experiment
- Three reflectors after propagation through $Q = 60$: raw, phase-only, amplitude + phase (20 dB limit).
- Phase-only: sharpens and re-centres the wavelet without touching amplitudes.
- Amplitude + phase: additionally restores relative strength across frequency.
- The price: noise is boosted in the depleted band too.
- Figure: `term02_lec01_compensation_modes.png`

---

## Slide 24 — The classic three-panel experiment
- Model data (left), amplitude correction (middle), amplitude + phase (right).
- Amplitude-only restores the spectral tilt — but the wavelet stays stretched.
- Adding phase correction restores symmetry and sharpness.
- Figure: `term02_lec01_realdata_compensation_result.png`

---

## Slide 25 — Handling variable Q
- Real Q varies with depth and laterally. Two implementations:
- **Layered constant Q** (Wang 2002): extrapolate the wavefield layer by layer (downward continuation), constant-Q inverse filter inside each layer.
- **Continuous Q(t)** (Wang 2006): integrate operators through a smoothly varying Q; efficient in the Gabor (windowed Fourier) domain.
- Prestack data in complex areas: compensate inside migration — next slides.

---

## Slide 26 — Practical: the reference frequency
- Every causal dispersion law gives velocity relative to $f_\text{ref}$: that component keeps its traveltime unchanged.
- Frequencies above $f_\text{ref}$ are pulled earlier, below — pushed later. The wavelet is anchored at $f_\text{ref}$.
- The choice is a processing decision, not physics:
  - dominant frequency (common default): event times stay close to picks
  - anchored high: all usable frequencies shift earlier by up to tens of ms; check-shot ties move
  - 4D: baseline and monitor must use the same convention
- "My Q-compensation moved events by 15 ms" → suspect the reference frequency first, not Q.

---

## Slide 27 — Practical: the gain limit
- The main quality knob: how much boost you allow.
- Too low (10 dB): cosmetic; spectra barely change at depth.
- Appropriate (typically 20–40 dB): deep bandwidth recovers to where signal still exceeds noise.
- Too high (60+ dB on noisy data): spiky "resolution illusion," ringing — frequencies that never reached the receivers cannot be restored.
- QC: average spectra in time windows before/after; the boosted band must end at the noise floor; the difference section must contain noise, not events.

---

## Slide 28 — Practical: choosing the compensation mode
- **Phase only**: fixes stretching and delays. Use when amplitudes must be preserved (AVO), data are noisy, or Q is uncertain — the phase part is robust to moderate Q errors.
- **Amplitude only**: fixes the spectral tilt; rare alone — the wavelet stays stretched, resolution barely improves.
- **Amplitude + phase**: fixes everything recoverable; the default for resolution-oriented processing.

---

## Slide 29 — Q-compensation in imaging: Q-tomography
- Deep-water and structurally complex plays: rays sample different Q along different paths — time-domain poststack compensation is not enough.
- Prestack attenuation analysis (estimation methods of Section 7, in tomographic form) inverts amplitude behaviour into interval-Q cubes.
- Figure: `term02_lec01_realdata_q_cubes.png`

---

## Slide 30 — Q-compensating migration: field example
- The same data migrated without (left) and with (right) Q-compensation.
- Vertical resolution and fault definition improve at target level.
- This is the deep-processing route: the Q model and the imaging operator work together.
- Figure: `term02_lec01_realdata_migration_qcomp.jpg`

---

## Slide 31 — Estimating Q: where estimates come from
- **VSP**: receivers in the well record the direct downgoing wave; between two levels everything else is identical — the classical, cleanest domain.
- **Sonic logs / crosswell**: very high frequency, shallow focus, dispersion correction of their own.
- **Surface reflection data**: always available, noisier; windows around two reflectors replace the two VSP levels; gives an effective Q over the path.
- Data preparation rule number one: **no AGC** — the Q information IS the amplitude decay across frequency and time.
- QC the time-frequency spectrogram first: smooth systematic decay before any fitting.
- Figure: `term02_lec01_realdata_well_q.png`

---

## Slide 32 — Spectral-ratio method
- Compare spectra of two windows at $t_1$ and $t_2$; the ratio cancels source, geometry, and frequency-independent gains.
- The log spectral ratio is a straight line in frequency:
- $\ln\,|A_2(f)|/|A_1(f)| = -\pi (t_2 - t_1) f / Q + b$
- Fit the slope $k$ by least squares: $Q = -\pi (t_2 - t_1) / k$.
- Most accurate on clean data (Tonn 1991 VSP tests) — but a ratio of noisy spectra does not cancel noise, it divides it.
- Figure: `term02_lec01_spectral_ratio.png`

---

## Slide 33 — Central-frequency shift method
- Track one robust attribute: the centroid of the spectrum $f_c$ (Quan & Harris 1997).
- Absorption multiplies a Gaussian spectrum by $e^{-\pi f \tau / Q}$ — a linear-in-f exponent: the Gaussian slides down, width unchanged.
- $f_{c,1} - f_{c,2} = \pi \tau \sigma_f^2 / Q$, so $Q = \pi \tau \sigma_f^2 / (f_{c,1} - f_{c,2})$.
- Whole-spectrum attribute → robust to noise; survives in production.
- Weakness: Gaussian assumption and analysis-band choice — whole-band fits can err 40–150%, band-limited fits by a few percent (Cheng & Margrave).
- Figure: `term02_lec01_centroid_shift.png`

---

## Slide 34 — Least-squares modelling and wavelet matching
- **LS spectrum modelling**: fit the measured (t, f) surface directly with the physical model — no spectral division; handles $G(t)$ and time-varying Q. The production default in modern software.
- **Wavelet optimization** (Cheng & Margrave 2012): compare minimum-phase wavelets of two windows in the time domain; search the Q whose forward operator (amplitude + dispersion) maps one into the other.
- Uses the complete propagation model, including phase — not just amplitudes.
- In CREWES comparisons on noisy reflection data: the most accurate and most robust family.

---

## Slide 35 — Method comparison and practical guidance
- Spectral ratio: exact but noise-fragile — best on clean VSP.
- Central-frequency shift: robust, fast — sensitive to the analysis band.
- LS modelling: no division, handles gains and time-varying Q — production default.
- Wavelet matching: most robust on noisy data; uses phase too.
- Surface-data estimates are effective Q; interval Q comes from layer-stripping — the same algebra as interval velocities.
- QC everything: spectrograms first, two methods compared, difference sections after compensation.
- Figure: `term02_lec01_realdata_estimation_panels.png`

---

## Slide 36 — Summary
- Absorption (intrinsic + scattering = apparent): loss is constant per cycle → high frequencies die first; spectra tilt and shift low with traveltime.
- $Q = 2\pi E/\Delta E$; typical rocks 10–30 (weathered) to 300+ (carbonates, crystalline).
- Causality (Kramers–Kronig) forbids absorption without dispersion; Futterman's and Kjartansson's laws coincide over seismic bands.
- A Q model is a causal amplitude/phase pair; NCQ and CQ are the working models.
- The Earth Q filter is nonstationary: phase correction is unconditionally stable; amplitude correction must be gain-limited (dB).
- Practical knobs: reference frequency, gain limit, mode; imaging uses interval-Q from tomography.
- Estimation: spectral ratio, centroid shift, LS modelling, wavelet matching — and never AGC before estimation.

---

## Slide 37 — Comprehension questions
- Why do high frequencies attenuate faster — and why does this follow from the per-cycle nature of the loss?
- $Q = 40$, $t_0 = 2.5$ s: compute $A/A_0$ at 15 Hz and 60 Hz. What does their ratio say about the spectral tilt?
- A colleague builds a "pure absorber" (real attenuation, zero dispersion). What principle does it violate, and what would its impulse response look like?
- Why is the phase-only inverse Q filter unconditionally stable, while the amplitude operator must be stabilized?
- A noisy land stack shows wonderful sharp "resolution" at 4 s after 60 dB of boost. Two reasons to be suspicious?
- After Q-compensation a well-tie event arrives 18 ms earlier. Which parameter was likely set unconventionally?
- Derive $Q = -\pi \Delta t / k$ from the two-window spectral model. Which assumption fails first on a noisy gather?
- Why does AGC before Q-estimation destroy the estimate, while noise attenuation does not?
