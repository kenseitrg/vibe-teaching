---
title: Term 1 Lecture 02 — Kinematics, Velocities and Field Statics
status: draft
term: 01
lecture: 02
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

## 1. Velocity models in seismic processing

Every traveltime correction in seismic processing needs a velocity. The same stack of layers can be described by several different velocities, each tied to a different simplifying assumption about the ray path (Figure 1).

![Velocity definitions](figures/term01_lec02/term01_lec02_velocity_definitions.png){width=90%}

**Figure 1.** *Left:* schematic ray assumptions for average (vertical), RMS (straight) and NMO (hyperbolic) velocities. *Right:* interval, average, RMS and NMO velocity curves for a simple three-layer model.

Consider a horizontally layered medium with layer interval velocities $v_i$ and two-way interval times $\Delta t_i$.

It is convenient to define **vertical traveltime** $\tau$ as the natural time coordinate for a vertically varying medium:

$$
\tau(z) = \int_0^z \frac{dz'}{v(z')}, \qquad z(\tau) = \int_0^\tau v(\tau') \, d\tau'.
$$

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

## 2. Goal of kinematic processing

The idealised imaging model assumes that every trace represents a vertical raypath from the surface to a reflector and back. Real data do not satisfy this assumption because:

- shots and receivers are separated by an offset,
- the near surface introduces irregular time delays,
- reflectors may be dipping.

**Kinematic processing** corrects for the offset-dependent part of the traveltime. **Static corrections** remove the near-surface delays. After both corrections, the CMP gather should contain a set of approximately zero-offset traces that can be stacked to form a zero-offset section (Figure 2).

```text
Raw shot records
      ↓
  Sort to CMP gathers
      ↓
  Static corrections
      ↓
  NMO correction (needs velocity)
      ↓
  Stack → zero-offset section
      ↓
  Migration (Term 2/3)
```

**Figure 2.** *Simplified processing flow around the kinematic stage. The zero-offset stack is only an approximation of the geology; it is improved later by migration.*

The result is not the final image. It is a useful approximation: a zero-offset stack section in which traveltimes primarily reflect geological structure rather than acquisition geometry. The imaging stage (migration) will later correct for dip and focusing effects.

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

![NMO correction](figures/term01_lec02/term01_lec02_nmo_correction.png){width=90%}

**Figure 3.** *(a) Synthetic CMP gather with three reflection hyperbolae. Dashed lines show the true hyperbolic moveout. (b) The same gather after NMO correction; the reflections are flattened and ready for stacking.*

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

### 3.3 Under-correction and over-correction

If the wrong NMO velocity is used, the gather is not flattened:

- **Velocity too high** → the hyperbola is not curved enough to be removed; the event still smiles downward. This is **under-correction**.
- **Velocity too low** → the correction is too large; the event curves upward. This is **over-correction**.

![NMO velocity sensitivity](figures/term01_lec02/term01_lec02_nmo_under_over.png){width=90%}

**Figure 4.** *Effect of using the wrong NMO velocity. Left: velocity too high (under-correction, event still curves down). Centre: correct velocity. Right: velocity too low (over-correction, event curves up).*

### 3.4 NMO stretch and muting

During NMO correction each output time sample $t_0$ is taken from an input time $t = t_0 + \Delta t_\text{nmo}$. The local time derivative is

$$
\frac{\mathrm{d}t}{\mathrm{d}t_0} = \frac{t_0}{t} = \frac{t_0}{\sqrt{t_0^2 + x^2/V_\text{nmo}^2}} \le 1.
$$

Because the input time interval is compressed into a shorter output interval, the wavelet is **stretched** in time and its dominant frequency is lowered. Stretch is worst for:

- large offsets,
- shallow events (small $t_0$),
- low velocities.

![NMO stretch and mute](figures/term01_lec02/term01_lec02_nmo_stretch_mute.png){width=90%}

**Figure 5.** *Top left: a wavelet before NMO and after NMO at near and far offsets. Top right: fractional stretch versus offset for $t_0 = 1.0$ s. Bottom: stretch factor as a function of offset and zero-offset time; the white dashed line marks a typical 20 % mute threshold.*

Before stacking, the stretched far-offset samples are usually **muted** (set to zero). A common threshold is 20 % stretch. Muting prevents low-frequency noise from contaminating the stack and protects amplitude information.

### 3.5 Residual moveout

Even after a careful NMO correction, small residual curvatures may remain. These can be caused by:

- velocity errors,
- anisotropy,
- residual statics,
- structural dip.

Residual moveout is one reason velocity analysis is iterated and why residual statics are applied later. Residual statics and the link to velocity analysis are covered in detail in Term 1 Lecture 03.

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

![Velocity spectrum](figures/term01_lec02/term01_lec02_velocity_spectrum.png){width=90%}

**Figure 6.** *(a) Synthetic CMP gather. Dashed lines show the true reflection hyperbolae. (b) Semblance velocity spectrum. Bright peaks mark velocities that flatten the gather; cyan dots show the picked trend.*

### 4.3 Semblance

A simple measure is the stacked amplitude along each hyperbola, normalized by the number of traces. This is fast but sensitive to amplitude variations and noise.

A more robust measure is **semblance**:

$$
S(t_0, V) = \frac{1}{M} \frac{\sum_\tau \left[ \sum_{i=1}^{M} u_i\bigl(\tau - \Delta t_i(t_0, V)\bigr) \right]^2}{\sum_\tau \sum_{i=1}^{M} u_i^2\bigl(\tau - \Delta t_i(t_0, V)\bigr)},
$$

where $M$ is the number of offsets and $u_i$ is trace $i$. Semblance is the ratio of the energy of the stacked trace to the total trace energy. It ranges from 0 to 1 and is high only when the aligned traces are coherent.

### 4.4 Vertical and horizontal spectra

A **vertical velocity spectrum** is computed at a single CMP location and shows velocity as a function of time. **Horizontal spectra** or horizon-consistent spectra display velocity variations along a line or around a picked horizon. They are used to build a smoothly varying velocity field for NMO and, later, for time imaging.

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

A common rule of thumb is that anomalies longer than about half the spread length are treated as long-wavelength statics. Long-wavelength statics shift the whole CMP gather up or down by a constant time; the events stay hyperbolic but are placed at the wrong $t_0$. This biases velocity analysis and is the main reason for using a floating datum (Lecture 03).

### 5.3 Datums and replacement velocity

Field statics move the data from the physical surface to a reference level called a **datum**. A datum is simply an elevation used as a reference surface for the data (Noble, 2020). Several datums appear during processing:

- **Client datum** or **final datum**: the flat elevation datum used for delivery and final imaging.
- **Intermediate datum**: usually chosen near the base of the weathering layer. It removes the most irregular part of the static and lets the final datum and replacement velocity be changed later.
- **Floating datum** (Lecture 03): a smoothed surface that follows the long-wavelength statics trend; used during NMO and velocity analysis so that events stay hyperbolic.

The statics model can be written as follows. Let $e_\text{bns}$ be the elevation of the base of the near surface (BNS), $e_\text{dat}$ the datum elevation, and $V_\text{rep}$ the replacement velocity. The source-side and receiver-side statics are the vertical traveltimes from the source/receiver to the BNS plus the replacement-velocity shift from the BNS to the datum:

$$
\delta t_s = \text{traveltime from source to BNS} + \frac{e_\text{bns} - e_\text{dat}}{V_\text{rep}}.
$$

For the receiver side, if the source is below the BNS and the uphole time $t_\text{uh}$ has been measured, the receiver static is

$$
\delta t_r = t_\text{uh}(r) + \frac{e_\text{bns} - e_\text{dat}}{V_\text{rep}}.
$$

The total static applied to a trace is $\delta t_s + \delta t_r$ and must be subtracted from the measured arrival times.

Between the surface and the datum we replace the real low-velocity weathering layer with a **replacement velocity** $V_\text{r}$. This velocity should be a best estimate of the vertical velocity in the consolidated material just below the weathering. Because the static shift is $T = D/V$, a low replacement velocity gives a large static and a high replacement velocity gives a small static. The wrong choice does not just shift the section; it can introduce long-wavelength structural distortions (a figure demonstrating this distortion is still needed).

The statics process is an approximate form of downward continuation that is only correct for vertical raypaths. For energy that travels slantingly through the near surface, the correction is approximate. To keep later processing (NMO, migration) from being distorted, the **bulk (mean) static shift should be kept small**. A common practice is to remove the mean from the statics solution and save it to be applied as the final shift to the interpretation datum.

![Statics datums](figures/term01_lec02/term01_lec02_statics_datums.png){width=90%}

**Figure 7.** *Field-statics geometry. The weathering layer (low velocity) is replaced by a replacement velocity down to an intermediate datum; data are then moved to the final datum. Vertical rays are assumed.*

### 5.4 Computing field statics

With the vertical-ray assumption the total static shift for a trace is the sum of a source-side contribution and a receiver-side contribution. For one side it is approximately

$$
\Delta t = \frac{h_\text{elev} + h_w}{V_\text{r}} - \frac{h_\text{elev}}{V_\text{r}} - \frac{h_w}{V_w},
$$

where $h_\text{elev}$ is elevation above datum, $h_w$ is weathering-layer thickness, and $V_w$ is weathering velocity. The first term is the time from the surface to the datum if the entire column were replaced by $V_\text{r}$; the second and third terms subtract the actual time spent in the elevation column and in the weathering layer. In practice the expression is written per source and receiver location and summed to give the total static for each trace.

## 6. Near-surface model building

### 6.1 Sources of information

A reliable near-surface model is needed for accurate field statics. Information comes from:

- uphole surveys (direct measurement of weathering thickness and velocity),
- refraction shots,
- well logs and geological maps,
- microgravity and surface-wave methods.

Uphole surveys are attractive because they measure the vertical traveltime directly, but in practice shots sometimes lie inside the weathered layer, uphole picks are noisy, and shot spacing can be too sparse for reliable interpolation.

### 6.2 Refraction problem statement

Refraction statics use first arrivals to estimate the weathering-layer thickness and velocity. The classic model is a low-velocity layer over a higher-velocity half-space. At offsets larger than the **crossover distance** the first arrival is a critically refracted head wave rather than the direct wave.

![Refraction geometry](figures/term01_lec02/term01_lec02_refraction_geometry.png){width=90%}

**Figure 8.** *Two-layer refraction model. The direct ray travels at $v_1$ along the surface; the refracted ray dives to the interface, travels horizontally at $v_2$, and returns to the surface. The delay time at the receiver measures the near-surface effect.*

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
- Long-wavelength statics shift whole CMP gathers and bias velocity analysis; the floating-datum solution is covered in Lecture 03.

## Comprehension questions

1. Why is the RMS velocity always greater than or equal to the average velocity for the same layered medium?
2. What happens to a reflection event in a CMP gather if the NMO velocity used is too low?
3. Why do we mute the far offsets of an NMO-corrected gather before stacking?
4. What does a semblance velocity spectrum display on its axes, and what does a bright peak mean?
5. Explain why a near-surface anomaly produces the same time shift on all reflections of a single trace.

## Figures still needed

- A figure showing structural distortion caused by choosing a wrong replacement velocity (low vs. correct vs. high) on a stacked section.

## Further reading

- Hatton, Worthington & Makin (1986), *Seismic Data Processing: Theory and Practice* — NMO, velocity analysis and statics (Sections 3.7.1, 5.10).
- Noble (2020), *What's the Datum?* — datums and replacement velocity.
- Jones (2012), *Incorporating near-surface velocity anomalies in pre-stack depth migration models* — statics components and floating datum.
- CGG ODT01A Data Analysis Part 1 & Part 2 — CMP gathers, NMO and velocity spectra.
- Refraction Seismic course notes — delay-time methods and GRM.
- Existing slide deck `slides/raw/term01_lecture02_kinematics.pptx`.
