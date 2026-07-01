# Slide outline — Term 1 Lecture 02
## Kinematics, Velocities and Field Statics

---

# Title

**Kinematics, Velocities and Field Statics**

Term 1, Lecture 02

---

# Learning objectives

By the end of this lecture you should be able to:

- Define interval, average, RMS, NMO and stacking velocity.
- Explain why kinematic processing removes offset-dependent traveltime before stack.
- Apply the NMO equation and identify under/over-correction and stretch.
- Describe how a velocity spectrum is computed and why semblance is used.
- Explain static corrections, datums and replacement velocity.
- Sketch how refraction data constrain the near-surface model.

---

# Why velocities matter

- Every traveltime correction needs a velocity.
- Same layered medium can be described by several velocities.
- Each velocity assumes a different ray path.

**Figure:** `figures/term01_lec02/term01_lec02_velocity_definitions.png`

---

# Velocity definitions

**Interval velocity** $v_i = 2 \Delta z_i / \Delta t_i$

**Average velocity** (vertical ray):
$$V_\text{avg} = \frac{\sum v_i \Delta t_i}{\sum \Delta t_i}$$

**RMS velocity** (straight ray):
$$V_\text{rms}^2 = \frac{\sum v_i^2 \Delta t_i}{\sum \Delta t_i}$$

**NMO velocity** (hyperbolic moveout):
$$t^2(x) = t_0^2 + \frac{x^2}{V_\text{nmo}^2}$$

**Stacking velocity** — best flattens the gather for stack.

---

# Goal of kinematic processing

- Ideal imaging model: vertical ray to each reflector.
- Real data contain offset and near-surface delays.
- Kinematic processing corrects offset-dependent traveltime.
- Statics correct near-surface delays.
- Result: a zero-offset stack section, improved later by migration.

**Figure:** `figures/term01_lec02/term01_lec02_processing_flow.png`

---

# NMO correction

For a flat layered medium:
$$t(x) = \sqrt{t_0^2 + \frac{x^2}{V_\text{nmo}^2}}$$

NMO correction:
$$\Delta t_\text{nmo} = \sqrt{t_0^2 + \frac{x^2}{V_\text{nmo}^2}} - t_0$$

**Figure:** `figures/term01_lec02/term01_lec02_nmo_correction.png`

---

# Under- and over-correction

- Velocity too high → event still curves down (**under-correction**).
- Velocity too low → event curves up (**over-correction**).
- Correct velocity → flat event ready to stack.

**Figure:** `figures/term01_lec02/term01_lec02_nmo_under_over.png`

---

# NMO stretch and muting

- NMO maps far-offset samples to earlier times.
- Wavelet is stretched and frequency is lowered.
- Stretch worst for: far offsets, shallow events, low velocities.
- Stretched samples are muted before stack.

**Figure:** `figures/term01_lec02/term01_lec02_wavelet_stretch.png`

---

# Velocity analysis

- Try many $(t_0, V)$ pairs.
- Measure coherence along each hyperbola.
- Display result as a velocity spectrum.
- Bright peaks mark coherent reflections.

**Figure:** `figures/term01_lec02/term01_lec02_velocity_spectrum.png`

---

# Semblance

Semblance measures coherence, not just amplitude:

$$S(t_0, V) = \frac{1}{M} \frac{\sum_\tau \left( \sum_i u_i(\tau - \Delta t_i) \right)^2}{\sum_\tau \sum_i u_i^2(\tau - \Delta t_i)}$$

Advantages over simple normalized stack:

- Robust to amplitude variations.
- Highlights coherent alignment.
- Range 0 to 1.

---

# Static corrections: origin

Sources of static shifts:

- Elevation changes.
- Weathering-layer thickness and velocity variations.
- Water-column and tidal variations (marine).
- Cultural features.

Key assumption: one constant time shift per trace.

---

# Short- vs long-wavelength statics

- **Short-wavelength** statics: rapid trace-to-trace variations; destroy stack coherence.
- **Long-wavelength** statics: slow variations; distort structural picture.
- Rule of thumb: half the spread length separates the two.

---

# Datums and replacement velocity

- **Intermediate datum**: near base of weathering.
- **Final datum**: flat reference for stack/migration.
- **Replacement velocity** $V_\text{r}$: velocity used below the intermediate datum.
- Choice of $V_\text{r}$ affects computed statics and can distort far offsets.

**Figure:** `figures/term01_lec02/term01_lec02_statics_datums.png`

**Figure:** `figures/term01_lec02/term01_lec02_replacement_velocity.png`

---

# Near-surface model building

Information sources:

- Uphole surveys.
- Refraction shots.
- Well logs, geological maps.
- Microgravity and surface-wave methods.

Refraction statics:

- Low-velocity layer over higher-velocity half-space.
- First arrivals: direct wave near source, head wave beyond crossover distance.
- Delay time isolates near-surface effect.

**Figure:** `figures/term01_lec02/term01_lec02_delay_time_scheme.png`

---

# Delay-time methods

Classical methods for refraction statics:

- **Hagedoorn plus–minus (ABC)** method.
- **Generalized Reciprocal Method (GRM)**.
- **Generalized Linear Inversion (GLI)**.

Modern extension: diving-wave tomography and FWI/SWI (Term 3).

---

# Summary

- Kinematic processing + statics → zero-offset stack section.
- Several velocities: interval, average, RMS, NMO, stacking.
- NMO correction flattens gathers; wrong velocity causes under/over-correction.
- Stretch requires muting at far offsets.
- Velocity spectra use semblance to pick velocities.
- Field statics move data to a datum using replacement velocity.
- Refraction data build near-surface models via delay-time methods.

---

# Comprehension questions

1. Why is RMS velocity $\ge$ average velocity?
2. What happens if NMO velocity is too low?
3. Why mute far offsets after NMO?
4. What do bright peaks in a semblance spectrum mean?
5. Why does a near-surface anomaly shift all reflections by the same time?
