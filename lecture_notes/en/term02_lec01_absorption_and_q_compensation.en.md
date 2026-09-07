---
title: Term 2 Lecture 01 — Absorption and Q-Compensation
author: Seismic Data Processing Course
---

# Absorption and Q-Compensation

## Why this lecture matters

In Term 1 we treated absorption as one item on a list of amplitude effects: "high frequencies are attenuated more than low ones, controlled by the quality factor $Q$ — corrected by Q-compensation, covered later." This lecture is that "later."

Absorption is not just another gain problem. It is the reason a 3-second seismic section looks blurrier than a 1-second one. It removes high frequencies *selectively*, so it lowers resolution with depth. And — less obviously but just as important — it delays the low frequencies that survive, stretching the wavelet. Both effects grow with traveltime, so the effective wavelet on your data is **not stationary**: it changes from top to bottom of every trace. Ordinary deconvolution cannot handle that; Q-compensation can.

We will look at:

1. What absorption does to real seismic data, and how to recognize it.
2. The physical mechanism and the definition of the quality factor $Q$.
3. Why absorption *forces* velocity dispersion (Kramers–Kronig relations) — a consequence of causality.
4. Four classical models of Q and which of them processing actually uses.
5. Q-compensation operators: Futterman's phase correction and Wang's stabilized amplitude + phase correction.
6. Practical decisions: reference frequency, amplitude damping limit, compensation modes.
7. Estimating $Q$ from seismic data: spectral ratios, central frequency shift, least-squares modelling, wavelet optimization.

---

## 1. What absorption does to seismic data

### Two sections, one difference

Figure 1 shows the same section imaged with and without Q-compensation. Nothing about the acquisition or the geometry changed — only the treatment of absorption. With compensation, deep events are sharper, weaker reflectors become visible, and the overall "character" of the deep section stops degrading with time.

![Figure: `figures/term02_lec01/term02_lec01_realdata_with_without_q.png` — Section imaged with and without Q-compensation (from the instructor's slide deck).](./figures/term02_lec01/term02_lec01_realdata_with_without_q.png)

*Figure 1: The same data with and without absorption compensation. Notice how resolution degrades with traveltime in the uncompensated image.*

### Frequency panels: the direct evidence

The cleanest way to *see* absorption is to filter the data into narrow frequency bands and compare the same section at low and high frequencies (Figures 2 and 3).

![Figure: `figures/term02_lec01/term02_lec01_realdata_freq_panel_low.png` — 10–20 Hz frequency panel.](./figures/term02_lec01/term02_lec01_realdata_freq_panel_low.png)

*Figure 2: 10–20 Hz panel. Low frequencies suffer a noticeable delay.*

![Figure: `figures/term02_lec01/term02_lec01_realdata_freq_panel_high.png` — 50–60 Hz frequency panel.](./figures/term02_lec01/term02_lec01_realdata_freq_panel_high.png)

*Figure 3: 50–60 Hz panel of the same data. High frequencies are delayed less, but without gain we would see them with much lower amplitudes.*

Notice what the two panels tell us:

- The **10–20 Hz** energy survives to the bottom of the record. Deep events are there, but the wavelet stretches.
- The **50–60 Hz** energy dies out gradually with time. Where it dies, resolution is gone: we would have to apply a special gain to bring back that information.

This is the signature of absorption: a smooth, systematic loss of high frequencies with traveltime, not a sudden change at a "bad frequency" (that would be a ghost notch or an anti-alias filter) and not a random loss (that would be noise).

### The three consequences we must undo

1. **Amplitude decay that depends on frequency and traveltime.** Deeper reflectors are not just weaker — their spectrum is tilted toward low frequencies.
2. **Wavelet stretching and delay.** As we will prove in Section 3, absorption necessarily travels with velocity dispersion: lower frequencies move slightly slower. The wavelet that reaches a deep reflector and returns is longer and its peak arrives late relative to its high-frequency onset.
3. **Nonstationarity.** Effects 1 and 2 accumulate with traveltime. The wavelet at 0.5 s and the wavelet at 3.0 s are different. Every stationary processing step (including predictive deconvolution, designed in Term 1) silently assumes they are the same.

### Where Q-compensation sits in the flow

Absorption correction is applied in one of two places:

- **Time-domain processing:** a nonstationary inverse Q filter applied to traces (prestack or poststack), typically after geometric-spreading correction and before or together with deconvolution. This is the classical route and the subject of Sections 5–6.
- **Inside imaging:** modern migration algorithms compensate absorption along the propagation path, using a 3D interval-$Q$ model built by Q-tomography. This is the deep-processing route; we will look at examples but not derive it.

Either way, two inputs are always needed: **a Q value or model** (Section 7: where does it come from?) and **a compensation operator** (Sections 5–6: what does it do, and which knobs does it have?).

---

## 2. The absorption mechanism and the quality factor Q

### Intrinsic versus apparent attenuation

Two families of processes remove energy from the propagating wavefront:

- **Intrinsic (anelastic) absorption:** elastic energy is converted to heat. Mechanisms include friction at grain contacts, viscous flow of pore fluid between cracks and pores of different stiffness ("squirt flow"), and frame relaxation. This is *true* absorption.
- **Scattering:** energy is redirected by small-scale velocity and density heterogeneities — layering above and below the wavelength, faults, porosity patches. The energy is not converted to heat; it is converted to incoherent or delayed wavefield that our stack does not recover.

From surface data the two are nearly indistinguishable: both attenuate amplitudes and both bias toward low frequencies. Processing treats them together as **apparent attenuation** quantified by an effective $Q$. In these notes "absorption" means the combined effect, unless we say otherwise.

### The key experimental fact

Laboratory and field measurements on consolidated rocks agree on one point that drives the whole theory:

> **The fractional energy loss per oscillation cycle is nearly independent of frequency** over the seismic band.

Not per second — per *cycle*. So per second, a 50 Hz wave loses energy 5 times faster than a 10 Hz wave, simply because it oscillates 5 times more often. **High frequencies die first because they cycle more, not because any individual cycle is more lossy.** 

### Defining Q from energy

The **quality factor** $Q$ measures the loss per cycle:

$$
\boxed{\; Q = 2\pi\,\frac{E}{\Delta E} \;}
$$

where $E$ is the energy stored (peak, or for large losses, the mean) and $\Delta E$ the energy lost during one cycle. The inverse, $Q^{-1}$, is called the **specific dissipation** or loss factor — "how lossy" the rock is. A perfect elastic medium has $Q = \infty$.

**Worked example.** $Q = 50$ means each cycle costs a fraction $\Delta E/E = 2\pi/Q \approx 12.6\%$ of the remaining energy. After $N$ cycles the energy is $E_N = E_0\, e^{-2\pi N/Q}$. Ten cycles take 71% of the energy — but a deep reflection has completed *thousands* of cycles. This is why absorption that looks mild per cycle is devastating over a seismic travel path.

### Defining Q from amplitude decay

For a wave of frequency $f$ (angular frequency $\omega = 2\pi f$) travelling for time $t$ in a medium with constant $Q$, the amplitude decays as

$$
\boxed{\; A(\omega, t) = A_0(\omega)\, \exp\!\Big( -\frac{\omega\, t}{2Q} \Big) \;}
$$

The connection to the per-cycle definition: $N$ cycles take a time $t = N\,2\pi/\omega$, and inserting this recovers $e^{-\pi N/Q}$ per amplitude — energy $e^{-2\pi N/Q}$, exactly the per-cycle law above.

Equivalently, over distance $x$ the amplitude decays as $e^{-\alpha x}$ with the **absorption coefficient**

$$
\alpha(\omega) = \frac{\omega}{2Q\,v} \qquad \text{(nearly proportional to frequency)} .
$$

Figure 4 shows both views of the definition side by side.

![Figure: `figures/term02_lec01/term02_lec01_q_definition.png` — Energy loss per cycle and exponential amplitude decay for two Q values.](./figures/term02_lec01/term02_lec01_q_definition.png)

*Figure 4: Two equivalent definitions of $Q$. Left: the fraction of energy lost per cycle ($Q = 50$ loses 12.6% per cycle, $Q = 200$ loses 3.1%). Right: the resulting exponential amplitude decay with the number of cycles.*

### Typical Q values

| Material | $Q$ |
|---|---|
| Weathered layer, unconsolidated sediments | 10–30 |
| Consolidated clastics (sand/shale) | 50–150 |
| Carbonates, evaporites | 150–300+ |
| "Deep, tight" crystalline rocks | 300–1000 |

Two rules of thumb: shallower rocks lose more (less consolidation, more fluid mobility), and $Q$ roughly scales with velocity — fast rocks are usually also high-$Q$ rocks.

### The amplitude law in numbers

$$
\frac{A}{A_0} = \exp\!\Big( -\frac{\pi f t}{Q} \Big)
$$

Take $Q = 50$, a reflector at two-way time $t = 2$ s:

- At $f = 10$ Hz: $\;e^{-\pi \cdot 10 \cdot 2 / 50} = e^{-1.26} \approx 0.29$. The 10 Hz component keeps ~29% of its amplitude.
- At $f = 40$ Hz: $\;e^{-\pi \cdot 40 \cdot 2 / 50} = e^{-5.03} \approx 0.0065$. The 40 Hz component keeps 0.65%.

One octave and a half of frequency, a factor of 45 in amplitude. *This* is the tilt we must undo — and the reason undoing it fully is hopeless beyond the point where signal has dropped below noise (Section 5.4).

### What the wavelet looks like as it travels

Figure 5 shows a wavelet propagated through a constant-$Q$ medium to increasing traveltimes, with the corresponding amplitude spectra.

![Figure: `figures/term02_lec01/term02_lec01_pulse_broadening.png` — Pulse propagation in a constant-Q medium.](./figures/term02_lec01/term02_lec01_pulse_broadening.png)

*Figure 5: A wavelet at increasing traveltimes in a medium with $Q = 60$ (synthetic, Kjartansson model). Each wavelet is centred on the arrival of the reference frequency (dashed line). Notice three things: the amplitude drops, the spectrum's centre of mass shifts to lower frequencies, and the wavelet gets longer with its low-frequency tail lagging behind the dashed line — dispersion, Section 3.*

Three observations to carry through the rest of the lecture:

1. The **spectrum tilts and shifts** — centroid moving down as $t$ grows.
2. The **wavelet broadens** — resolution at 3 s is intrinsically worse than at 1 s.
3. The broadening is not symmetric stretching: the *late* side of the wavelet (low frequencies) is dragged out. That asymmetry is dispersion, and it is not optional — it is required by physics.

---

## 3. Absorption without dispersion is impossible

### The causality argument

Here is a thought experiment. Suppose a medium absorbed high frequencies but had **no** velocity dispersion: all frequencies travel at exactly the same speed. Propagation through it would be a filter that attenuates the spectrum and adds **zero phase at every frequency**.

Now recall Term 1 Lecture 05: a zero-phase frequency response belongs to a **symmetric** impulse response — a wavelet centred on $t = 0$ that starts ringing *before* the input arrives. A filter that responds before it is excited is **acausal**. Physical wave propagation cannot do this: the earth's response at a receiver cannot precede the source trigger.

So for a linear earth, "absorption without dispersion" is not merely unusual — it is *forbidden*. Attenuation and phase are two halves of one causal response.

### The Kramers–Kronig relations

The rigorous statement is a pair of integral relations (Kramers 1927, Kronig 1926), familiar from optics and circuit theory. For any causal linear system with frequency response $H(\omega)$, the real and imaginary parts are Hilbert-transform duals:

$$
\operatorname{Re}H(\omega) = -\frac{1}{\pi}\, P\!\!\int_{-\infty}^{\infty} \frac{\operatorname{Im}H(u)}{u - \omega}\, du,
\qquad
\operatorname{Im}H(\omega) = \frac{1}{\pi}\, P\!\!\int_{-\infty}^{\infty} \frac{\operatorname{Re}H(u)}{u - \omega}\, du
$$

($P$ denotes the Cauchy principal value.) Applied to wave propagation — where the attenuation law and the phase (velocity) law are the real and imaginary parts of one propagation constant — the relations say:

> **Choose any attenuation law you like. The dispersion law is then determined — you have no further freedom.**

The derivation (causality $\to$ step function $\to$ one Fourier integral $\to$ KK) takes about two pages and needs only Term 1 Fourier analysis: see the companion derivation document. Two of its results matter for the rest of this lecture:

1. **Futterman's logarithmic law.** For a nearly constant-$Q$ medium (loss per cycle constant) above a low cutoff frequency $\omega_0$:

$$
\frac{1}{v(\omega)} = \frac{1}{v_0}\Big[ 1 - \frac{1}{\pi Q}\, \ln\frac{\omega}{\omega_0} \Big],
\qquad
\frac{v(\omega)}{v(\omega_r)} \approx 1 + \frac{1}{\pi Q}\ln\frac{\omega}{\omega_r}
$$

2. **Kjartansson's power law** (exactly constant $Q$ at all frequencies, no cutoff):

$$
\frac{v(\omega)}{v(\omega_r)} = \Big( \frac{\omega}{\omega_r} \Big)^{\gamma},
\qquad \gamma = \frac{1}{\pi}\arctan\frac{1}{Q} \approx \frac{1}{\pi Q}
$$

Since $x^{\gamma} \approx 1 + \gamma\ln x$ for small $\gamma$, the two laws are the same law to first order in $1/Q$.

### How large is dispersion, in numbers?

Everything scales as $\frac{1}{\pi Q}\ln(\text{frequency ratio})$. For $Q = 50$:

| Quantity | Value |
|---|---|
| Velocity change per decade of frequency | $\frac{\ln 10}{\pi Q} \approx 1.5\%$ |
| Delay of 10 Hz relative to 100 Hz at $t_0 = 2$ s | $t_0 \cdot \frac{\ln 10}{\pi Q} \approx 29$ ms |

A few percent of velocity, tens of milliseconds of wavelet stretch. Small compared with geological velocity contrasts — but *systematic*, *frequency-dependent*, and *cumulative with traveltime*. Figure 6 plots the two dispersion laws for exactly this case.

![Figure: `figures/term02_lec01/term02_lec01_velocity_dispersion.png` — Velocity dispersion curves for Q = 50.](./figures/term02_lec01/term02_lec01_velocity_dispersion.png)

*Figure 6: Velocity ratio $v(f)/v(f_\text{ref})$ for $Q = 50$, $f_\text{ref} = 100$ Hz. Futterman's logarithmic law and Kjartansson/Wang's power law are nearly identical over the seismic band. High frequencies travel up to 2–3% faster than low frequencies — which is why the low-frequency tail of every deep wavelet lags behind.*

### Why practitioners should care

- **Well ties.** Check-shot (sonic) data carry high-frequency content; surface seismic is band-limited lower. They sample *different points of the dispersion curve* — a systematic few-ms mismatch that is physics, not error.
- **Velocity analysis.** Picked stacking velocities correspond to the dominant frequency of the data being picked. Two surveys with different bandwidths will give measurably different "apparent velocity" over the same geology.
- **4D.** Baseline and monitor with different spectra (different source depths, different water velocities) accumulate different dispersion delays. Reference-frequency choice in Q-compensation (Section 6.1) is one of the levers that keeps them comparable.
- **Processing.** Dispersion correction is a pure *phase* operation — per-frequency time shifts. It is unconditionally stable (Section 5.2), the "safe half" of Q-compensation.

---

## 4. Models of Q and their properties

### What a "model of Q" must contain

A model of Q is not just a number $Q$. It is a complete **causally consistent pair**:

$$
\big( \text{attenuation law } \alpha(\omega),\ \text{dispersion law } v(\omega) \big)
$$

consistent with the Kramers–Kronig relations. Amplitude alone, or phase alone, is not a propagation model — you cannot compensate one without implicitly assuming the other. When software asks you to choose a "Q model" or an attenuation/dispersion operator, it is asking: *which causal pair do I use?*

Kjartansson's famous 1979 paper contains a one-table summary of the classical theories — worth reading in the original. The four families:

### The four classical families

| Family | Linear? | $Q(f)$ | $v(f)$ | Verdict |
|---|---|---|---|---|
| **Frictional** (Born 1941; White 1966; Knopoff) | no — response depends on amplitude | constant | constant | Matches "loss per cycle constant" — but **nonlinear** (rules out superposition, the basis of all our processing) and produces **acausal/distorted** responses. Dead end for processing. |
| **Voigt–Ricker** (viscous solid) | yes | $1/Q \propto f$ — Q grows with frequency | constant at low $f$ | Linear and causal, gives the **Ricker wavelet** (its lasting contribution). But $Q \propto f$ **contradicts measurements**. Ricker wavelets remain our favourite *shape*, detached from the physics that produced them. |
| **Kolsky–Futterman** (near-constant Q, "NCQ") | yes | nearly constant over a finite band | logarithmic law | Linear, causal, matches data over the seismic band. Requires a low-frequency cutoff $\omega_0 \neq 0$ (Section 3). **The workhorse of processing software.** |
| **Kjartansson constant Q** ("CQ") | yes | **exactly constant**, all frequencies | power law $v \propto \omega^{\gamma}$ | Linear, causal, no cutoff, fully specified by $(Q, v_0)$. Self-similar: pulse width grows *exactly* linearly with traveltime. **The workhorse of wave-equation methods and Wang's inverse Q filter.** |

![Figure: `figures/term02_lec01/term02_lec01_q_models.png` — Q(f) and v(f) for the four model families.](./figures/term02_lec01/term02_lec01_q_models.png)

*Figure 7: The four model families in Kjartansson's taxonomy. Top: $Q(f)$ — only NCQ and CQ stay near-constant over the seismic band (shaded). Bottom: corresponding dispersion. For $Q \ge 30$ the NCQ and CQ curves differ by fractions of a percent — model choice is convenience, causal consistency is the physics.*

### Reading the table like a processor

- The frictional family died because it is **nonlinear** — all of seismic processing (superposition, convolutional model, deconvolution) assumes linearity at seismic strains.
- The Voigt–Ricker family died because its $Q(f)$ is wrong, but it left us the Ricker wavelet — a reminder that a useful mathematical shape can outlive its physical model.
- Everything modern is NCQ or CQ. They differ in whether Q is constant over a *band* (with cutoff) or at *all* frequencies. Over any seismic band with $Q \ge 30$, their predictions agree to well under a percent: the choice between "Futterman" and "Kjartansson/Wang" operators in software is a matter of bookkeeping, not physics.
- What matters physically is that the amplitude and phase parts of the operator come **from the same causal pair**. Mixing an attenuation law from one model with a dispersion law from another violates causality — the resulting filter would respond before it is excited.

---

## 5. Q-compensation: inverting the earth Q filter

### The forward problem: a time-varying filter

Combine Sections 2 and 3: propagation for traveltime $t$ through a constant-$Q$ medium multiplies each frequency component by

$$
\boxed{\;
U(t, \omega) = U(0, \omega)\;
\underbrace{\exp\!\Big(-\frac{\omega t}{2Q}\Big)}_{\text{amplitude decay}}
\;\underbrace{\exp\big( i\,\phi(\omega, t) \big)}_{\text{dispersion phase}}
\;}
$$

where the phase $\phi$ is fixed by the chosen causal model (Futterman or Kjartansson). A recorded trace is therefore the reflectivity series convolved with a filter whose strength **grows with traveltime**: each deeper reflection has been filtered more. This is a **nonstationary convolution** — effectively a different filter at each record time, not one wavelet for the whole trace.

> **Why ordinary deconvolution is not enough.** A stationary spiking filter finds one wavelet for the whole trace. With absorption, shallow reflections carry a sharp wavelet and deep ones a long, tilted wavelet; a single inverse filter can only compromise. Q-compensation removes the *systematic time-varying* part first, leaving a wavelet that is nearly stationary again — after which deconvolution works as designed. This is why Q-compensation belongs *before* deconvolution in the flow.

The inverse operation — undoing both factors — is **inverse Q filtering**. The two factors have completely different temperaments.

### Futterman's approach: the phase is stable

Since the KK relations tie dispersion to attenuation, correcting dispersion is deterministic once $Q$ is known: compute the causal dispersion law, and apply the exact opposite phase per frequency — a pure, frequency-dependent time shift. This idea (Futterman 1962; made practical as a fast Fourier-domain operation by Hargreaves & Calvert 1991) is the **phase-only inverse Q filter**.

Key property: the phase operator has unit amplitude at every frequency. It *rearranges* the spectrum in time — it does not amplify anything. It is **unconditionally stable**: it cannot blow up, and it barely touches the noise level. What it fixes:

- wavelet stretching (sharper wavelets),
- the systematic delay of low frequencies (better event timing, better well ties).

What it does *not* fix: the lost high-frequency amplitudes. After phase-only correction, deep events are better positioned but still lack bandwidth.

### Wang's approach: amplitude needs stabilization

To recover amplitudes we must apply the inverse of the decay: the **amplitude compensation operator**

$$
\exp\!\Big( +\frac{\omega t}{2Q} \Big)
$$

Look at it closely: it grows *exponentially in both frequency and traveltime*. At $Q = 50$, $t = 2$ s, $f = 40$ Hz it must boost by $1/0.0065 \approx 150$. At 60 Hz, by more than 3000. Beyond the frequency where the signal has decayed below the noise floor, this operator amplifies **noise** — and eventually overflows any numerical format. Wang (2002) demonstrated the resulting wild oscillations on *noise-free* synthetic data: the "noise" being amplified there was machine precision.

Two classical stabilizations:

1. **Gain-limited filter** (Wang 2002): cap the boost at a maximum gain, beyond which the operator is clipped. Simple, but it happily boosts pure noise up to the cap.
2. **Stabilized operator** (Wang 2006): solve the amplitude inversion as a damped least-squares problem, giving

$$
\Lambda(\tau, \omega) = \frac{\Lambda_a + \sigma^2}{\Lambda_a^2 + \sigma^2},
\qquad \Lambda_a = \exp\!\Big( -\frac{\omega \tau}{2Q} \Big)
$$

The stabilization factor $\sigma^2$ (small) makes the operator behave like the exact inverse wherever the signal survived, and *taper gracefully* to near-zero where the signal has died. Unlike a hard clip, it does not drag ambient noise up with the signal.

The stabilization factor is not chosen directly. Users specify a **maximum gain limit in dB** — "how much boost am I willing to allow" — and the factor is computed from it. Wang's empirical relation (fitted for gain limits of 10–100 dB, independent of $Q$):

$$
\sigma^2 = \exp\big( -0.23\, G_\text{lim} - 1.63 \big)
$$

Modern processing software exposes exactly this: a compensation mode (phase only / amplitude only / amplitude + phase), a gain limit in dB, and a Q model (constant or time-varying). Different packages, same physics.

Figure 8 shows the geometry of the stabilized operator.

![Figure: `figures/term02_lec01/term02_lec01_inverse_q_operator.png` — The amplitude compensation operator with and without stabilization.](./figures/term02_lec01/term02_lec01_inverse_q_operator.png)

*Figure 8: The inverse-Q amplitude operator in the $(t, f)$ plane. Left: the raw operator $\exp(\pi f t / Q)$ — an exponential wall at late time / high frequency (note the colour scale: values grow to $10^3$–$10^6$ and beyond — this is the instability). Right: the same operator with a gain-limit stabilization — full boost where signal lives, graceful taper beyond. The phase operator (not shown) has magnitude 1 everywhere — nothing to stabilize.*

### What each mode fixes: a synthetic experiment

Figure 9 and Figure 10 show the classic three-panel experiment: model data, amplitude correction only, amplitude + phase correction.

![Figure: `figures/term02_lec01/term02_lec01_realdata_compensation_result.png` — Model data: amplitude correction vs amplitude+phase correction.](./figures/term02_lec01/term02_lec01_realdata_compensation_result.png)

*Figure 9: model data (left), amplitude correction (middle), amplitude + phase correction (right). Amplitude-only restores the spectrum's tilt but leaves the wavelet stretched; adding phase correction restores symmetry and sharpness.*

![Figure: `figures/term02_lec01/term02_lec01_compensation_modes.png` — Synthetic comparison of compensation modes.](./figures/term02_lec01/term02_lec01_compensation_modes.png)

*Figure 10: Three reflectors after propagation through $Q = 60$: raw (black), phase-only correction (blue), amplitude+phase with a 20 dB gain limit (red). Phase-only sharpens and re-centres without touching amplitudes; amplitude+phase additionally restores relative strength across frequency — at the price of also boosting noise in the depleted band.*

### Handling variable Q

Real Q varies with depth (and laterally). Two implementations:

- **Layered constant-Q** (Wang 2002): divide the earth into constant-$Q$ layers; extrapolate the wavefield down layer by layer (downward continuation, as in migration), applying a fast constant-Q inverse filter within each layer.
- **Continuous $Q(t)$** (Wang 2006): integrate the operators through a continuously varying $Q(\tau)$; implement efficiently in the Gabor (windowed Fourier) domain.

For prestack data in complex areas, the state of the art compensates Q **inside migration** using interval-Q from tomography — shown in Section 6.4.

---

## 6. Practical Q-compensation

### The reference frequency

Every causal dispersion law gives velocity *relative to* something. Concretely, in the Futterman ratio

$$
\frac{v(f)}{v(f_\text{ref})} \approx 1 + \frac{1}{\pi Q}\,\ln\frac{f}{f_\text{ref}}
$$

the operator is normalized so that **the component at $f_\text{ref}$ keeps its traveltime unchanged**. Frequencies below $f_\text{ref}$ are pulled earlier (they were travelling "too slow" relative to it), frequencies above are pushed later. The wavelet is *anchored* at $f_\text{ref}$.

The choice is a **processing decision, not physics**:

- Anchor at the **dominant frequency** of the data (common default): event times stay close to what velocity analysis and interpretation expect.
- Anchor **high** (e.g., 100+ Hz): all usable frequencies get pulled earlier by up to a few tens of ms — image times shift systematically; check-shot ties move.
- **4D**: baseline and monitor must use the *same* reference convention, or a systematic time shift is manufactured between surveys.

### The amplitude damping factor (gain limit)

The gain limit $G_\text{lim}$ (Section 5.3) is the main quality knob. Reading it is straightforward:

- **Too low** (e.g., 10 dB): correction is cosmetic; spectra barely change at depth.
- **Appropriate** (typically 20–40 dB): deep bandwidth recovers up to where signal still exceeds noise; difference sections show no coherent leftovers.
- **Too high** (60+ dB on noisy data): the operator boosts noise in the depleted band — spiky "resolution illusion", ringing, and damage. Remember: frequencies that never reached the receivers cannot be restored; boosting them manufactures noise, not information.

QC recipe: compare average amplitude spectra in time windows before/after; the boosted band should end where the pre-stack spectrum sinks into the noise floor. Watch the difference section — it should contain noise, not events.

### Choosing the compensation mode

| Mode | Fixes | Use when |
|---|---|---|
| **Phase only** | stretching, delays | amplitudes must be preserved for AVO; data are noisy; or $Q$ is uncertain (phase part is robust to moderate Q errors) |
| **Amplitude only** | spectral tilt | rare alone — leaves the wavelet stretched, so resolution barely improves |
| **Amplitude + phase** | everything recoverable | default for resolution-oriented processing; the "full inverse Q" |

### Q-compensation in imaging

For deep-water and structurally complex plays, time-domain post-stack compensation is not enough: rays sample different $Q$ along different paths. The modern workflow builds **interval-Q cubes by Q-tomography** (from prestack attenuation analysis — essentially the estimation methods of Section 7 applied in tomographic form) and compensates inside the migration kernel. Figures 11–12 show a production example: the amplitude behaviour (left) is inverted into a Q model (right), and the migrated image with Q-compensation shows improved fault and reservoir definition.

![Figure: `figures/term02_lec01/term02_lec01_realdata_amplitude_cube.png` — Amplitude behaviour used as input to Q-tomography.](./figures/term02_lec01/term02_lec01_realdata_amplitude_cube.png)

*Figure 11: Input to Q-estimation in an imaging workflow: amplitude behaviour over the survey.*

![Figure: `figures/term02_lec01/term02_lec01_realdata_q_cubes.png` — Q model from tomography.](./figures/term02_lec01/term02_lec01_realdata_q_cubes.png)

*Figure 12: The resulting interval-Q model used by Q-compensating migration.*

![Figure: `figures/term02_lec01/term02_lec01_realdata_migration_qcomp.jpg` — Migration without and with Q-compensation.](./figures/term02_lec01/term02_lec01_realdata_migration_qcomp.jpg)

*Figure 13: Migration without (left) and with (right) Q-compensation on the same data. Vertical resolution and fault definition improve at target level.*

---

## 7. Estimating Q from seismic data

Compensation needs $Q$ — where does it come from? This section covers the four estimation approaches you will meet in practice, in rough historical order, ending with the ones inside modern software.

### Where Q estimates come from

- **VSP** (vertical seismic profile): receivers in the well record the *direct* downgoing wave. Between two receiver levels, source, path geometry and near-surface are identical — the cleanest possible comparison. The classical domain for Q estimation.
- **Sonic logs / crosswell**: very high frequency; shallow focus; needs dispersion correction of its own.
- **Surface reflection data**: always available but noisier; windows around two reflectors play the role of the two VSP levels; thin-bed tuning contaminates the local spectrum. What is estimated is an **effective Q** along the total path.

**Data preparation rule number one: no AGC.** The Q information lives precisely in the amplitude decay across frequency and time; any data-driven gain destroys it. Minimal processing before estimation: noise attenuation, (deghosting if marine), and that is nearly all. Modern estimation software will ask you to QC the time-frequency spectrogram first: it must show a smooth, systematic decay along both axes — the visual signature of Figure 5 — before any fitting is meaningful.

### The spectral-ratio method

The idea: compare the spectra of two windows at times $t_1$ and $t_2$, and let the ratio cancel everything that is *not* absorption.

**Derivation.** Model the amplitude spectrum of a window around reflection time $t_i$:

$$
|A_i(f)| = g_i\, |S(f)|\, |R_i(f)|\, \exp\!\Big( -\frac{\pi f t_i}{Q} \Big)
$$

where $S$ is the source spectrum (same for both windows), $R_i$ the local reflectivity spectrum, and $g_i$ collects frequency-*independent* amplitude factors: spherical divergence, transmission losses, tuning-independent gain. Take the ratio and the logarithm:

$$
\ln \frac{|A_2(f)|}{|A_1(f)|}
= \underbrace{\ln\frac{g_2 |R_2(f)|}{g_1 |R_1(f)|}}_{\text{slowly varying in } f}
\; - \frac{\pi f\, (t_2 - t_1)}{Q}
$$

Over a moderate analysis band, the first term is approximately a constant $b$ (and any residual curvature averages out). The log-ratio is then a **straight line in frequency**:

$$
\boxed{\; \ln \frac{|A_2(f)|}{|A_1(f)|} = -\frac{\pi (t_2 - t_1)}{Q}\, f + b \;}
$$

Fit a straight line by least squares; if its slope is $k$, then

$$
Q = -\frac{\pi\,(t_2 - t_1)}{k}.
$$

Steeper slope — faster spectral decay — means lower Q. Figure 14 shows the workflow on synthetic data.

![Figure: `figures/term02_lec01/term02_lec01_spectral_ratio.png` — Spectral-ratio method.](./figures/term02_lec01/term02_lec01_spectral_ratio.png)

*Figure 14: Spectral-ratio method. Left: amplitude spectra of two windows ($t_1 = 1.0$ s, $t_2 = 2.5$ s) — the later window is tilted toward low frequencies. Right: log spectral ratio vs frequency with the least-squares line; its slope gives $Q$. Here the ratio of two noisy spectra is itself noisy — the method's Achilles heel.*

**Assessment.** In Tonn's (1991) extensive VSP comparison, the spectral-ratio method was the *most accurate* method on noise-free data — the derivation is exact, after all. But taking the ratio of two noisy spectra is statistically fragile: the noise does not cancel, it divides. Estimates degrade quickly as noise grows, and the method is sensitive to window choice, tuning effects and any residual gain.

### The central frequency shift method

The idea: instead of comparing spectra point-by-point, track one robust attribute — the **centroid** (centre of mass) of the spectrum:

$$
f_c = \frac{\int f\, |A(f)|\, df}{\int |A(f)|\, df}, \qquad
\sigma_f^2 = \frac{\int (f - f_c)^2\, |A(f)|\, df}{\int |A(f)|\, df}
$$

**Derivation** (Quan & Harris 1997). Let the first window's spectrum be Gaussian, $|A_1(f)| \propto \exp\big( -(f - f_{c,1})^2 / (2\sigma_f^2) \big)$, and let the second window be the same spectrum after absorption over interval $\tau = t_2 - t_1$:

$$
|A_2(f)| = |A_1(f)|\, \exp\!\Big( -\frac{\pi f \tau}{Q} \Big)
$$

The absorption factor is *linear* in $f$ in the exponent. Multiplying a Gaussian by the exponential of a linear function gives... another Gaussian: collect the $f$-terms in the exponent,

$$
-\frac{(f - f_{c,1})^2}{2\sigma_f^2} - \frac{\pi \tau}{Q}\, f
= -\frac{\big( f - (f_{c,1} - \pi\tau\sigma_f^2/Q) \big)^2}{2\sigma_f^2} + \text{const}
$$

— same variance, shifted centre. So the centroid moves down by exactly

$$
f_{c,1} - f_{c,2} = \frac{\pi \tau \sigma_f^2}{Q}
\qquad\Longrightarrow\qquad
\boxed{\; Q = \frac{\pi \tau\, \sigma_f^2}{f_{c,1} - f_{c,2}} \;}
$$

Absorption does not change the width of a Gaussian spectrum — it slides it down in frequency. Measure the slide, get Q.

![Figure: `figures/term02_lec01/term02_lec01_centroid_shift.png` — Central frequency shift method.](./figures/term02_lec01/term02_lec01_centroid_shift.png)

*Figure 15: Centroid-frequency shift. Left: spectra at two traveltimes with their centroids marked — the Gaussian shape slides down without changing width. Right: centroid vs traveltime on a longer series of windows; the slope of the decline gives $Q$ (steeper decline — lower Q).*

**Assessment.** The centroid is a whole-spectrum attribute: noise perturbs it gently, not catastrophically — the method is **robust to noise**, which is why it survives in production. Its weakness is the Gaussian assumption: real seismic spectra are not Gaussian, and the variance $\sigma_f^2$ must itself be estimated from data. Cheng & Margrave's tests showed the estimated Q can be badly biased if the analysis band is chosen carelessly (whole-band: errors of 40–150%; band-limited where the spectrum *is* roughly Gaussian: errors of a few percent). The practical lesson: **the analysis band is part of the method**, and QC of the Gaussian approximation is mandatory.

### Least-squares spectrum modelling

The spectral ratio divides two spectra; modelling avoids the division. Fit the *measured* amplitude spectrum directly with the physical model,

$$
|A(f, t)| = G(t)\, |S(f)|\, \exp\!\Big( -\frac{\pi f t}{Q} \Big)
$$

with unknowns $Q$, the amplitude factor $G(t)$ (spherical divergence etc.) and possibly a parametrized source spectrum $S$. Working in the time-frequency domain (Gabor transform), one fits the whole $(t, f)$ surface at once, obtaining either a constant $Q$ or a time-varying **effective Q** function. Two variants matter in practice: assuming $G$ constant in time (more robust to noise) or variable (more realistic — most datasets have geometric spreading and transmission loss). Running both is a QC: if they agree, no significant amplitude drift is present.

This family — robust, whole-surface, no spectral division — is what modern estimation software implements.

### Wavelet optimization / match filtering

The most robust modern variant works in the **time domain** (Cheng & Margrave 2012). Sketch:

1. Estimate smoothed spectra of two windowed events; construct their minimum-phase equivalent wavelets $w_1$, $w_2$.
2. For a trial $Q$, compute the constant-Q propagation operator $I(Q, t)$ over the interval between the events (amplitude decay *plus* causal dispersion phase — the full forward model of Section 5).
3. Choose $Q$ (and a scaling factor $\mu$) minimizing the mismatch:

$$
Q_\text{est} = \arg\min_Q \big\| w_1 * I(Q, \cdot) - \mu\, w_2 \big\|^2
$$

Because the comparison happens between *wavelets in the time domain* (not between pointwise spectral ratios), noise perturbs the estimate gently. In the CREWES comparisons on noisy reflection data, the match-filter method was the most accurate and most robust — and it uses the *complete* propagation model including dispersion, not just amplitudes.

### Comparison and practical guidance

| Method | Domain | Strengths | Weaknesses | Best data |
|---|---|---|---|---|
| Spectral ratio | frequency | exact on clean data; simple | fragile with noise; window/tuning sensitive | clean VSP |
| Central frequency shift | frequency | robust; fast; good QC | Gaussian assumption; band-sensitive | VSP, good reflection data |
| LS spectrum modelling | time-frequency | no division; handles $G(t)$; time-varying Q | model assumptions; needs band choice | production default |
| Wavelet matching | time | most robust; uses phase too | nonlinear search; needs wavelet estimates | noisy reflection data |

Final practicalities:

- Estimates from surface data are **effective Q** over the path; interval Q comes from layer-stripping (inverting a chain of effective values — algebraically the same step you know from interval velocities).
- QC everything: spectrograms first, two methods compared, effective-vs-interval consistency, and — always — the compensation difference sections (Section 6.2).

![Figure: `figures/term02_lec01/term02_lec01_realdata_well_q.png` — Q estimation from well data.](./figures/term02_lec01/term02_lec01_realdata_well_q.png)

*Figure 16: Q analysis on well data (from the instructor's deck): VSP-based estimation comparing spectra between receiver levels.*

![Figure: `figures/term02_lec01/term02_lec01_realdata_estimation_panels.png` — Estimation QC panels.](./figures/term02_lec01/term02_lec01_realdata_estimation_panels.png)

*Figure 17: QC panels for Q estimation from seismic data (from the instructor's deck): spectral ratios and central-frequency tracking over analysis windows.*

---

## Summary

- **Absorption** (intrinsic + scattering = apparent attenuation) converts wave energy to heat and redirection; loss is roughly constant **per cycle**, so **high frequencies die first** — spectra tilt and shift low with traveltime.
- **Q** quantifies the loss: $Q = 2\pi E / \Delta E$ per cycle, equivalently $A(\omega,t) = A_0\,e^{-\omega t/2Q}$; typical rocks: 10–30 (shallow/weathered) to 150–300+ (carbonates).
- **Causality forbids absorption without dispersion** (Kramers–Kronig): the attenuation law uniquely determines the dispersion law; over seismic bands, Futterman's logarithmic law and Kjartansson's power law coincide. A few percent velocity change; tens of ms of wavelet stretch at depth.
- **Models of Q** = causal amplitude/phase pairs. Frictional (nonlinear, acausal) and Voigt–Ricker ($Q \propto f$) are historical; Kolsky–Futterman (near-constant Q, cutoff) and Kjartansson (exact constant Q) are the working models — and agree for $Q \ge 30$.
- **The earth Q filter is nonstationary** — a different filter at each traveltime — so it needs a nonstationary inverse: **inverse Q filtering**. Phase correction (Futterman/Hargreaves) is exact and unconditionally stable; amplitude correction (Wang) grows exponentially in $(f, t)$ and **must be stabilized** by a gain limit (dB), which is the main quality knob.
- **Practical knobs**: reference frequency (anchors event times; critical for ties and 4D), gain limit (resolution vs noise), mode (phase-only / amplitude+phase). In imaging, Q-tomography supplies interval-Q cubes to Q-compensating migration.
- **Q estimation**: spectral ratio (exact but noise-fragile), central frequency shift (robust, Gaussian-band-sensitive), LS spectrum modelling (production default), wavelet matching (most robust on noisy reflection data). No AGC before estimation — ever.

## Comprehension questions

1. Explain in one or two sentences, without equations, why high frequencies are attenuated faster than low frequencies — and why this follows from the *per-cycle* nature of the loss, not from any preference of rocks for low frequencies.
2. A reflector lies at two-way time $t_0 = 2.5$ s in a medium with $Q = 40$. Compute the amplitude ratio $A/A_0$ for 15 Hz and for 60 Hz. What does the ratio of the two numbers tell you about the tilt of the spectrum?
3. Your colleague claims to have built a "pure absorber" model: real attenuation, zero dispersion. What principle does this violate, what would its impulse response look like, and what would you observe at the first break of a trace filtered by it?
4. Why is the phase-only inverse Q filter unconditionally stable, while the amplitude operator must be stabilized? What geometrical feature of the amplitude operator $\exp(\pi f t / Q)$ in the $(t, f)$ plane is the instability?
5. You run inverse Q filtering on a noisy land stack with a 60 dB gain limit and see wonderful sharp "resolution" at 4 s. Give two independent reasons to be suspicious.
6. The same reflector is tied in a well tie before and after Q-compensation; after compensation the seismic event arrives 18 ms earlier. Which parameter was likely set unconventionally, and what should you check?
7. Derive the spectral-ratio estimator $Q = -\pi\Delta t / k$ from the windowed-spectrum model, listing every assumption you make. Which assumption fails first on a noisy CMP gather?
8. Why does applying AGC before Q-estimation destroy the estimate, while noise attenuation does not?
9. Two estimation methods on the same data give effective $Q = 45$ and $Q = 120$. Following Section 7, what are the likely causes of the discrepancy, and which method-family checks would you run?

## References and further reading

- Futterman, W. I. (1962). Dispersive body waves. *Journal of Geophysical Research*, 67, 5279–5291. `wiki/sources/futterman_1962_dispersive_body_waves.md`
- Kjartansson, E. (1979). Constant Q-wave propagation and attenuation. *Journal of Geophysical Research*, 84, 4737–4748. `wiki/sources/kjartansson_1979_constant_q.md`
- Wang, Y. (2002). A stable and efficient approach of inverse Q filtering. *Geophysics*, 67(2), 657–663. `wiki/sources/wang_2002_stable_inverse_q.md`
- Wang, Y. (2006). Inverse Q-filter for seismic resolution enhancement. *Geophysics*, 71(2), V51–V60. `wiki/sources/wang_2006_inverse_q_resolution.md`
- Schönleber, M. (2014). A simple derivation of the Kramers–Kronig relations from the perspective of system theory. *American Journal of Physics*. `wiki/sources/schonleber_2014_kk_system_theory.md`
- Quan, Y. & Harris, J. M. (1997). Seismic attenuation tomography using the frequency shift method. *Geophysics*, 62(3), 895–905.
- Cheng, P. & Margrave, G. F. (2012, 2013). Estimation of Q / Comparison of Q-estimation methods: an update. CREWES Research Reports. `wiki/sources/cheng_margrave_2012_2013_q_estimation.md`
- Hargreaves, N. D. & Calvert, A. J. (1991). Inverse Q filtering by Fourier transform. *Geophysics*, 56(4), 519–527.
- Companion derivation: [Kramers–Kronig relations and velocity dispersion](../derivations/kramers_kronig_dispersion_derivation.en.md)
