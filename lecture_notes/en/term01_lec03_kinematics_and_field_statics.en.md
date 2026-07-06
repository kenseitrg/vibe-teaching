---
title: Term 1 Lecture 03 — Kinematics, Velocities and Field Statics
status: draft
term: 01
lecture: 03
---

# Kinematics, Velocities and Field Statics

## Learning objectives

By the end of this lecture you should be able to:

- Define interval, average, RMS, NMO and stacking velocity and state the ray assumption behind each.
- Explain why kinematic processing removes offset-dependent traveltime before stack.
- Apply the NMO equation and identify under-correction, over-correction and stretch.
- Describe how a velocity spectrum is computed and why semblance is preferred over simple normalization.
- Explain the origin of static corrections, the vertical-ray assumption, and the role of datums and replacement velocity.
- Sketch how refraction data constrain the near-surface model and name the main delay-time methods.

## Prerequisites

- Common-midpoint (CMP) geometry and fold.
- Basic wave propagation: traveltime, ray path, reflection, refraction.
- The convolutional seismic trace model.


\newpage{}

## 1. Velocity models in seismic processing

Every traveltime correction in seismic processing needs a velocity. The same stack of layers can be described by several different velocities, each tied to a different simplifying assumption about the ray path (Figure 1).

![Velocity definitions](figures/term01_lec03/term01_lec03_velocity_definitions.png){width=90%}

**Figure 1.** *Left:* a three-layer earth model with the true refracted ray (bent at each interface by Snell's law), the vertical-ray approximation used for average velocity, and the straight-ray approximation used for RMS velocity. *Right:* interval, average and RMS velocity curves as functions of two-way time for the same model.

Consider a horizontally layered medium with layer interval velocities $v_i$ and two-way interval times $\Delta t_i$.

It is convenient to define **vertical traveltime** $\tau$ as the natural time coordinate for a vertically varying medium:

$$
\tau(z) = \int_0^z \frac{dz'}{v(z')}, \qquad z(\tau) = \int_0^\tau v(\tau') \, d\tau'.
$$

For a simple linear gradient $v(z) = v_0 + k z$, the vertical traveltime is $t = (1/k)\,\ln(v/v_0)$; equivalently, depth grows exponentially with traveltime. A step-by-step derivation is given in `lecture_notes/derivations/linear_gradient_traveltime.en.md`.

Using $\tau$, the velocity averages become continuous integrals rather than layer sums.

**Interval velocity** is the velocity of one layer:

$$
v_i = \frac{2 \Delta z_i}{\Delta t_i}.
$$

**Average velocity** is the total depth divided by total one-way time. It assumes a vertical ray. In layer form:

$$
V_\text{avg}(T) = \frac{\sum_i v_i \Delta t_i}{\sum_i \Delta t_i} = \frac{z}{T/2}.
$$

As a function of vertical traveltime:

$$
V_\text{avg}(\tau) = \frac{1}{\tau} \int_0^\tau v(\tau') \, d\tau'.
$$

**RMS velocity** is the root-mean-square of interval velocities weighted by interval time. In layer form:

$$
V_\text{rms}^2(T) = \frac{\sum_i v_i^2 \Delta t_i}{\sum_i \Delta t_i}.
$$

As a function of vertical traveltime:

$$
V_\text{rms}^2(\tau) = \frac{1}{\tau} \int_0^\tau v^2(\tau') \, d\tau'.
$$

The **Dix formula** inverts the RMS average: it recovers the interval velocity of a layer from the RMS velocities measured at the top and bottom of that layer. In layer form, if $t_i$ is the two-way vertical time at the base of layer $i$ and $V_{\text{rms},i}$ is the RMS velocity to that depth, then

$$
v_i = \sqrt{\frac{V_{\text{rms},i}^2 \, t_i - V_{\text{rms},i-1}^2 \, t_{i-1}}{t_i - t_{i-1}}}.
$$

In the continuous limit this becomes

$$
v^2(\tau) = \frac{\mathrm{d}}{\mathrm{d}\tau} \Bigl[ \tau \, V_\text{rms}^2(\tau) \Bigr].
$$

> **Key point.** Velocity analysis gives us stacking/NMO velocities, which approximate RMS velocities. The Dix formula converts those RMS velocities into interval velocities — the velocities of individual geological layers.

> **Warning: Dix instability.** The Dix formula is a **difference** of squared RMS velocities, so small errors or wiggles in the picked RMS velocity are amplified when they are divided by the thin-layer time interval. A 2 % uncertainty in RMS velocity can produce a much larger uncertainty in interval velocity, especially when the layer is thin. This is why interval-velocity profiles from raw stacking velocities are usually heavily smoothed or constrained with additional information (well logs, geological bounds, tomography).

Because velocities are squared before averaging, the RMS velocity is always greater than or equal to the average velocity for the same layered medium. The two are equal only when all interval velocities are identical. A useful exact relation is

$$
V_\text{rms}^2 = V_\text{avg} \, V_\text{m},
$$

where $V_\text{m}$ is the mean velocity over depth.

> **Sanity check.** For a linear increase with depth $v(z) = v_0 + c z$, the instantaneous velocity as a function of vertical traveltime is exponential: $v(\tau) = v_0 e^{c \tau}$. A small velocity gradient with depth produces a large exponential variation with time, which is why velocity analysis is done in fine time gates.

For a single horizontal layer the reflection traveltime as a function of source–receiver offset $x$ is exactly hyperbolic:

$$
t^2(x) = t_0^2 + \frac{x^2}{v^2}.
$$

In layered media the exact expression is more complicated, but for small offsets it is common to use the same hyperbolic form with an **NMO velocity** $V_\text{nmo}$:

$$
t^2(x) \approx t_0^2 + \frac{x^2}{V_\text{nmo}^2}.
$$

**Stacking velocity** is the velocity that best flattens the events in a CMP gather so that stacking produces a clean zero-offset trace. For flat horizontal layers it is close to the NMO velocity.

> **Key point.** Average, RMS and NMO velocities are not the same. Average velocity is needed for depth conversion; RMS velocity is a small-offset approximation; NMO/stacking velocity is what we pick from data to flatten gathers. RMS velocity $\ge$ average velocity for the same medium.


\newpage{}

## 2. Goal of kinematic processing

The idealised imaging model assumes that every trace represents a vertical raypath from the surface to a reflector and back. Real data do not satisfy this assumption because:

- shots and receivers are separated by an offset,
- the near surface introduces irregular time delays,
- reflectors may be dipping.

**Kinematic processing** corrects for the offset-dependent part of the traveltime. **Static corrections** remove the near-surface delays. After both corrections, the CMP gather should contain a set of approximately zero-offset traces that can be stacked to form a zero-offset section (Figure 2).

![Processing flow](figures/term01_lec03/term01_lec03_processing_flow.png){width=40%}

**Figure 2.** *Simplified processing flow around the kinematic stage. Mute removes stretched far-offset samples before stack. The zero-offset stack is only an approximation of the geology; it is improved later by migration.*

The result is not the final image. It is a useful approximation: a zero-offset stack section in which traveltimes primarily reflect geological structure rather than acquisition geometry. The imaging stage (migration) will later correct for dip and focusing effects.


\newpage{}

## 3. NMO correction

### 3.1 The NMO equation

For a flat layered medium the reflection time on a CMP gather is approximately

$$
t(x) = \sqrt{t_0^2 + \frac{x^2}{V_\text{nmo}^2}}.
$$

The **normal-moveout (NMO) correction** is the time shift that maps every offset sample to its zero-offset time $t_0$:

$$
\Delta t_\text{nmo}(x) = t(x) - t_0 = \sqrt{t_0^2 + \frac{x^2}{V_\text{nmo}^2}} - t_0.
$$

Figure 3 shows a synthetic CMP gather before and after applying the correct NMO correction.

![NMO correction](figures/term01_lec03/term01_lec03_nmo_correction.png){width=90%}

**Figure 3.** *(a) Synthetic CMP gather with three reflection hyperbolae. Dashed lines show the true hyperbolic moveout. (b) The same gather after NMO correction; the reflections are flattened. The wavelets are stretched at far offsets, especially for the shallowest event, because the NMO mapping is nonlinear.*

### 3.2 Qualitative behaviour

From the equation you can see that the NMO correction:

- decreases as velocity increases (higher velocity → flatter hyperbola),
- decreases with depth (larger $t_0$),
- increases with offset $x$,
- decreases with dip (dipping events have less curvature in a CMP gather).

These rules help interpreters spot velocity problems by eye. They also explain why picking velocities on far-offset data is harder than on near-offset data: the relative moveout is smaller and more sensitive to errors.

For a dipping reflector beneath a constant-velocity overburden, the image-source construction gives the exact relation:

$$
t^2(x) = t_0^2 + \frac{x^2 \cos^2(\delta)}{V^2},
$$

so the stacking velocity becomes

$$
V_\text{stack} = \frac{V}{\cos(\delta)}.
$$

In 3-D the line azimuth $\omega$ relative to the dip direction matters:

$$
V_\text{stack} = \frac{V}{\sqrt{1 - \sin^2(\delta) \cos^2(\omega)}}.
$$

This is why a single stacking velocity can fail for steeply dipping events.

![Dipping reflector geometry](figures/term01_lec03/term01_lec03_dip_moveout_cosine.png){width=90%}

**Figure 7.** *Geometry of a dipping reflector. The source $S$ and receiver $R$ are separated by the surface offset $x$ with midpoint $M$. The mirror image $S'$ makes the reflected path $S \to I \to R$ equivalent to the straight line $S'R$. Decomposing $S'R$ into the zero-offset normal path $Vt_0 = 2z$ and the effective offset $x \cos\theta$ gives the hyperbola $t^2 = t_0^2 + x^2 \cos^2\theta / V^2$, so the stacking velocity is $V / \cos\theta$.*

The construction works because the reflector is a mirror. Reflecting the source $S$ across the dipping reflector gives the image point $S'$. The distance from $S'$ to any point $I$ on the reflector is exactly the same as the distance from $S$ to that same point, so the two legs $S \to I$ and $S' \to I$ are equal. Therefore the total reflected path $S \to I \to R$ has the same length as the straight line $S' \to R$.

In the zero-offset case the receiver is at the midpoint $M$, so $S' \to M$ is the normal-incidence ray (perpendicular to the reflector). Its length is $V t_0 = 2z$, where $z$ is the normal distance from $M$ to the reflector. When the receiver moves to $R$ by a horizontal offset $x$, the straight line $S'R$ is no longer along the normal. Decomposing it into a part parallel to the reflector and a part perpendicular to the reflector gives the right triangle shown in the figure: the perpendicular leg is still the zero-offset path $V t_0$, and the parallel leg is the projection of the surface offset onto the reflector direction, $x \cos\theta$.

Because the hypotenuse is the total equivalent path $Vt$, Pythagoras gives

$$
(Vt)^2 = (Vt_0)^2 + (x\cos\theta)^2.
$$

Dividing by $V^2$ and comparing with the standard hyperbolic moveout $t^2 = t_0^2 + x^2/V_\text{stack}^2$ shows immediately that

$$
V_\text{stack} = \frac{V}{\cos\theta}.
$$

In other words, the dipping reflector has less curvature in a CMP gather than a flat reflector at the same depth because only the $x\cos\theta$ part of the offset contributes to the hyperbolic moveout.

\newpage{}

### 3.3 Under-correction and over-correction

If the wrong NMO velocity is used, the gather is not flattened:

- **Velocity too high** → the hyperbola is not curved enough to be removed; the event still smiles downward. This is **under-correction**.
- **Velocity too low** → the correction is too large; the event curves upward. This is **over-correction**.

![NMO velocity sensitivity](figures/term01_lec03/term01_lec03_nmo_under_over.png){width=90%}

**Figure 4.** *Effect of using the wrong NMO velocity. Left: velocity too high (under-correction, event still curves down). Centre: correct velocity. Right: velocity too low (over-correction, event curves up).*


\newpage{}

### 3.4 NMO stretch and muting

A reflection wavelet is not a mathematical impulse; it occupies a finite time window. In that window the NMO velocity is not constant: it usually increases with depth, and therefore with time. The top of the wavelet corresponds to a slightly shallower time than the bottom, so it is associated with a lower NMO velocity. Because a lower NMO velocity produces a larger NMO correction, the top of the wavelet must be shifted upward more than the bottom. The wavelet is therefore stretched in time, and its dominant frequency is lowered.

![Wavelet stretch during NMO](figures/term01_lec03/term01_lec03_wavelet_stretch.png){width=90%}

**Figure 5.** *NMO stretch and reversal. (a) Two reflection hyperbolae on a CMP gather; the numbers mark the samples of the wavelet at different offsets. (b) After NMO correction the same samples no longer line up. At near offsets the wavelet is preserved; at larger offsets it is stretched, and eventually the sample order reverses.*

For small NMO corrections the fractional frequency drop is approximately the same as the fractional NMO shift:

$$
\frac{\Delta f}{f} \approx -\frac{\Delta t_\text{nmo}}{t_0}.
$$

A 10 % NMO correction ($\Delta t_\text{nmo}/t_0 = 0.1$) therefore lowers the dominant frequency by about 10 %. Stretch is worst for:

- large offsets,
- shallow events (small $t_0$),
- low velocities.

Before stacking, the stretched far-offset samples are usually **muted** (set to zero). A common threshold is 20 % stretch. Muting prevents low-frequency noise from contaminating the stack and protects amplitude information.

### 3.5 Residual moveout

Even after a careful NMO correction, small residual curvatures may remain. These can be caused by:

- velocity errors,
- anisotropy,
- residual statics,
- structural dip.

Residual moveout is one reason velocity analysis is iterated and why residual statics are applied later. Residual statics and the link to velocity analysis are covered in detail in Term 1 Lecture 04.

### 3.6 NMO in a vertically varying medium

In a medium where velocity changes with depth, the exact traveltime is not a simple hyperbola. For small offsets it can be expanded as a power series:

$$
t^2(x) = c_1 + c_2 x^2 + c_3 x^4 + \ldots,
$$

with

$$
c_1 = t_0^2, \qquad c_2 = \frac{1}{V_\text{rms}^2}.
$$

This is the theoretical link between the stacking velocity we pick from data and the RMS velocity of the medium. The higher-order coefficient $c_3$ is the **fourth-order moveout**. It becomes important when the offset-to-depth ratio $H/z_0$ is large or for converted/shear waves. To the extent that the higher-order terms are negligible, stacking velocities approximate RMS velocities, and interval velocities can be estimated with the Dix formula.


\newpage{}

## 4. Velocity analysis

### 4.1 Principle

Velocity analysis tries many candidate $(t_0, V)$ pairs and measures how well each pair flattens the gather. A good velocity produces a coherent, high-amplitude stack along the corresponding hyperbola; a poor velocity does not.

> **Definition.** The **stacking velocity** is the velocity parameter that produces the best-fit hyperbola to the actual traveltime curve on a CMP gather. The precise meaning of “best fit” depends on the software, and the stacking velocity is a function of the maximum offset used in the analysis. Changing the maximum offset can change the stacking velocity even for the same reflector.

### 4.2 Computing a velocity spectrum

For each $t_0$ and each trial velocity $V$:

1. Compute the NMO shift $\Delta t_\text{nmo}(x)$ for every offset $x$.
2. Align samples along the hyperbola.
3. Measure coherence, for example by summing amplitudes or computing semblance.

The result is a 2-D panel with zero-offset time on the vertical axis and velocity on the horizontal axis. Peaks in the panel indicate coherent reflections (Figure 6).

![Velocity spectrum](figures/term01_lec03/term01_lec03_velocity_spectrum.png){width=90%}

**Figure 6.** *(a) Synthetic CMP gather. Dashed lines show the true reflection hyperbolae. (b) Semblance velocity spectrum. Bright peaks mark velocities that flatten the gather; cyan dots show the picked trend.*

### 4.3 Semblance

A simple measure is the stacked amplitude along each hyperbola, normalized by the number of traces. This is fast but sensitive to amplitude variations and noise.

A more robust measure is **semblance**:

$$
S(t_0, V) = \frac{1}{M} \frac{\sum_\tau \left[ \sum_{i=1}^{M} u_i\bigl(\tau - \Delta t_i(t_0, V)\bigr) \right]^2}{\sum_\tau \sum_{i=1}^{M} u_i^2\bigl(\tau - \Delta t_i(t_0, V)\bigr)}.
$$

Each part of this expression has a simple meaning:

- **$M$** — the number of traces in the CMP gather.
- **$u_i$** — the $i$-th trace, i.e. the recorded seismic trace at offset $i$.
- **$\tau$** — output time; the outer sum runs over a short window around the trial zero-offset time $t_0$.
- **$\Delta t_i(t_0, V)$** — the NMO shift predicted for trace $i$ with the trial $(t_0, V)$ pair. It is subtracted from $\tau$ so that samples along the trial hyperbola are aligned before stacking.
- **Inner sum $\sum_{i=1}^{M} u_i(\tau - \Delta t_i)$** — the shifted traces are simply added together. This is a stack along the trial moveout curve.
- **Square $[\cdots]^2$** — the instantaneous energy of the stacked trace. It is large only when the shifted traces line up constructively.
- **Numerator $\sum_\tau [\cdots]^2$** — the total coherent energy of the stacked trace inside the analysis window.
- **Denominator $\sum_\tau \sum_i u_i^2$** — the total energy of all individual traces in the same window. It normalizes the numerator so that strong amplitudes do not artificially dominate the result.
- **$1/M$** — a normalization that makes semblance bounded between 0 and 1, regardless of fold.

Semblance is therefore the ratio of coherent energy to total energy. It ranges from 0 to 1 and is high only when the aligned traces are coherent.

### 4.4 Vertical and horizontal spectra

A **vertical velocity spectrum** is computed at a single CMP location and shows velocity as a function of time. **Horizontal spectra** or horizon-consistent spectra display velocity variations along a line or around a picked horizon. They are used to build a smoothly varying velocity field for NMO and, later, for time imaging.


\newpage{}

## 5. Static correction fundamentals

### 5.1 Where statics come from

Static corrections are time shifts applied to whole traces to compensate for traveltime differences in the near surface. Sources include:

- elevation changes along the survey line,
- thickness and velocity variations in the weathering layer,
- water-column variations and tides in marine surveys,
- cultural features (roads, buildings).

The key assumption is that the near-surface delay is the same for every reflection on a given trace, so it can be removed by a single time shift. This is called the **vertical-ray assumption**: the rays travel almost vertically through the near surface.

### 5.2 Short-wavelength versus long-wavelength statics

- **Short-wavelength statics** vary rapidly from trace to trace, often within one spread length. They destroy stacking coherence and must be removed before stack.
- **Long-wavelength statics** vary slowly and can distort the structural picture if not corrected.

A common rule of thumb is that anomalies longer than about half the spread length are treated as long-wavelength statics. Long-wavelength statics shift the whole CMP gather up or down by a constant time; the events stay hyperbolic but are placed at the wrong $t_0$. This biases velocity analysis and is the main reason for using a floating datum (Lecture 04).


\newpage{}

### 5.3 Datums and replacement velocity

Field statics move the data from the physical surface to a reference level called a **datum**. A datum is simply an elevation used as a reference surface for the data (Noble, 2020). Several datums appear during processing:

- **Client datum** or **final datum**: the flat elevation datum used for delivery and final imaging.
- **Intermediate datum**: usually chosen near the base of the weathering layer. It removes the most irregular part of the static and lets the final datum and replacement velocity be changed later.
- **Floating datum** (Lecture 04): a smoothed surface that follows the long-wavelength statics trend; used during NMO and velocity analysis so that events stay hyperbolic.

The statics model can be written as follows. Let $e_\text{bns}$ be the elevation of the base of the near surface (BNS), $e_\text{dat}$ the datum elevation, and $V_\text{rep}$ the replacement velocity. We adopt the convention that **a positive static shift is added to the trace and moves it down to later times**. We assume the source is located exactly at the BNS, so the source-side static is just the replacement-velocity shift from the BNS down to the datum:

$$
\delta t_s = \frac{e_\text{bns} - e_\text{dat}}{V_\text{rep}}.
$$

For the receiver side, the measured uphole time $t_\text{uh}(r)$ is the time actually spent travelling from the BNS up to the surface. This time must be removed and replaced by the replacement-velocity shift from the BNS down to the datum, so the receiver static is

$$
\delta t_r = \frac{e_\text{bns} - e_\text{dat}}{V_\text{rep}} - t_\text{uh}(r).
$$

The total static applied to a trace is $\delta t_s + \delta t_r$ and is **added** to the measured arrival times; a positive value shifts the trace down to later times.

Between the surface and the datum we replace the real low-velocity weathering layer with a **replacement velocity** $V_\text{r}$. This velocity should be a best estimate of the vertical velocity in the consolidated material just below the weathering. Because the static shift is $T = D/V$, a low replacement velocity gives a large static and a high replacement velocity gives a small static. The wrong choice does not just shift the section; it can introduce long-wavelength structural distortions (Figure 9).

![Replacement velocity choice](figures/term01_lec03/term01_lec03_replacement_velocity.png){width=90%}

**Figure 9.** *Effect of replacement velocity choice. (a) Flat-surface model with a variable-thickness weathering layer and two flat sub-weathering reflectors with different velocities. (b) Traveltimes before static correction; the weathering anomaly is imprinted on both near- and far-offset events. (c) After correction with the correct replacement velocity the shallow and deep reflectors are flat for both offsets (solid and dashed lines); the semi-transparent dotted curves show where the same reflectors would land if a wrong replacement velocity were used. (d) Residual structural distortion when the replacement velocity is too low or too high; the error is much larger at far offsets because the wrong replacement velocity also changes the RMS velocity and therefore the NMO moveout.*

The statics process is an approximate form of downward continuation that is only correct for vertical raypaths. For energy that travels slantingly through the near surface, the correction is approximate. To keep later processing (NMO, migration) from being distorted, the **bulk (mean) static shift should be kept small**. A common practice is to remove the mean from the statics solution and save it to be applied as the final shift to the interpretation datum.

![Statics datums](figures/term01_lec03/term01_lec03_statics_datums.png){width=90%}

**Figure 8.** *Field-statics geometry. The weathering layer (low velocity) is replaced by a replacement velocity down to an intermediate datum; the data are then shifted up to the final datum, which is placed above the highest surface elevation to avoid negative total static shifts. Vertical rays are assumed.*

### 5.4 Computing field statics

With the vertical-ray assumption the total static shift for one side of a trace is the sum of an elevation contribution and a weathering contribution. For one side it is approximately

$$
\Delta t = \frac{h_\text{elev} + h_w}{V_\text{r}} - \frac{h_\text{elev}}{V_\text{r}} - \frac{h_w}{V_w} = h_w \left( \frac{1}{V_\text{r}} - \frac{1}{V_w} \right),
$$

where $h_\text{elev}$ is elevation above datum, $h_w$ is weathering-layer thickness, $V_w$ is weathering velocity, and $V_\text{r}$ is the replacement velocity. The first term is the time from the surface to the datum if the entire column were replaced by $V_\text{r}$; the second and third terms subtract the actual time spent in the elevation column and in the weathering layer. The result is the replacement time minus the actual time for the near-surface column. In practice the expression is written per source and receiver location, the two sides are summed, and the total static is **added** to the trace; a positive value shifts the trace down to later times.


\newpage{}

## 6. Near-surface model building

### 6.1 Sources of information

A reliable near-surface model is needed for accurate field statics. Information comes from:

- uphole surveys (direct measurement of weathering thickness and velocity),
- refraction shots,
- well logs and geological maps,
- microgravity and surface-wave methods.

Uphole surveys are attractive because they measure the vertical traveltime directly, but in practice shots sometimes lie inside the weathered layer, uphole picks are noisy, and shot spacing can be too sparse for reliable interpolation.


\newpage{}

### 6.2 Refraction problem statement

Refraction statics use first arrivals to estimate the weathering-layer thickness and velocity. The classic model is a low-velocity layer over a higher-velocity half-space. At offsets larger than the **crossover distance** the first arrival is a critically refracted head wave rather than the direct wave.

![Refraction geometry and delay time](figures/term01_lec03/term01_lec03_delay_time_scheme.png){width=90%}

**Figure 10.** *Two-layer refraction model. Top: traveltime versus source–receiver offset; the direct arrival follows velocity $v_1$, the refracted head wave follows the higher velocity $v_2$, and the crossover distance $x_c$ marks where the refracted wave becomes the first arrival. The intercept time $T_i$ measures the delay introduced by the near-surface layer. Bottom: ray geometry with the critically refracted ray ($\\theta_c$) and the delay-time path that isolates the near-surface contribution.*

### 6.3 Delay-time methods

The **delay time** is the difference between the observed refracted traveltime and the time that would be spent travelling the same horizontal distance at the sub-weathering velocity. For a source or receiver above a weathering layer of thickness $h$, the delay time is

$$
\delta t = \frac{h}{V_1 \cos i_c},
$$

where $i_c = \sin^{-1}(V_1/V_2)$ is the critical angle. This isolates the near-surface contribution and is the basis for refraction statics.

The refraction traveltime for a flat two-layer model is

$$
t_\text{refraction} = \frac{X}{V_2} + t_i, \qquad t_i = \frac{2 Z_1}{V_1} \cos(i_c),
$$

where $t_i$ is the **intercept time** and $Z_1$ is the weathering-layer thickness. The critical distance is $X_c = Z_1 \tan(i_c)$. When $V_1 \ll V_2$, the delay time becomes a good approximation to the vertical traveltime through the weathering layer.

A full derivation of the delay-time formula from the refracted ray geometry, together with the linear system solved by delay-time methods, is given in `lecture_notes/derivations/refraction_delay_time_linear_system.en.md`.

Important classical methods include:

- **Hagedoorn's plus–minus method** (also called the ABC method): uses reciprocal shot pairs, forms plus and minus traveltimes, and solves for delay times and refractor velocity.
- **Generalized Reciprocal Method (GRM)**: generalizes Hagedoorn by allowing arbitrary receiver pairs (offsets $XY$); produces both a velocity-analysis function and a time-depth function.
- **Generalized Linear Inversion (GLI)**: solves for weathering thickness and velocity by least-squares inversion of many refracted arrival times.

These methods remain useful, but modern processing often replaces or supplements them with diving-wave tomography and full-waveform inversion. Those advanced topics are covered in Term 3.

## Summary

- Kinematic processing removes offset-dependent traveltime; static corrections remove near-surface delays. Together they prepare a zero-offset stack section.
- Interval, average, RMS, NMO and stacking velocities are related but not identical. NMO/stacking velocity is what we estimate from CMP gathers.
- NMO correction flattens hyperbolae using the equation $t^2(x) = t_0^2 + x^2/V_\text{nmo}^2$. Wrong velocities produce under-correction or over-correction.
- NMO stretch at far offsets requires muting before stack.
- Velocity analysis scans $(t_0, V)$ space and measures coherence with semblance.
- Field statics move traces from the surface to a datum using the vertical-ray assumption and a replacement velocity. Wrong replacement velocity can distort structure.
- Refraction data constrain the near-surface model through delay-time methods; tomography is the modern extension.
- Long-wavelength statics shift whole CMP gathers and bias velocity analysis; the floating-datum solution is covered in Lecture 04.

## Comprehension questions

1. Why is the RMS velocity always greater than or equal to the average velocity for the same layered medium?
2. What happens to a reflection event in a CMP gather if the NMO velocity used is too low?
3. Why do we mute the far offsets of an NMO-corrected gather before stacking?
4. What does a semblance velocity spectrum display on its axes, and what does a bright peak mean?
5. Explain why a near-surface anomaly produces the same time shift on all reflections of a single trace.

## Further reading

- Hatton, Worthington & Makin (1986), *Seismic Data Processing: Theory and Practice* — NMO, velocity analysis and statics (Sections 3.7.1, 5.10).
- Noble (2020), *What's the Datum?* — datums and replacement velocity.
- Jones (2012), *Incorporating near-surface velocity anomalies in pre-stack depth migration models* — statics components and floating datum.
- CGG ODT01A Data Analysis Part 1 & Part 2 — CMP gathers, NMO and velocity spectra.
- Refraction Seismic course notes — delay-time methods and GRM.
- Existing slide deck `slides/raw/term01_lecture02_kinematics.pptx`.
