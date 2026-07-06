# Term 1 Lecture 03 — Kinematics, Velocities and Field Statics

## Scope

This is the first half of the original "kinematics and statics" lecture. It covers:

1. Seismic velocity models and their ray assumptions.
2. The goal of kinematic processing.
3. Normal-moveout (NMO) correction.
4. Velocity analysis.
5. Static correction fundamentals.
6. Near-surface model building from first arrivals.

## Learning objectives

By the end of this lecture students should be able to:

- Define interval, average, RMS, NMO and stacking velocity and state the ray assumption behind each.
- Explain why kinematic processing removes offset-dependent traveltime before stack.
- Apply the NMO equation and identify under-correction, over-correction and stretch.
- Describe how a velocity spectrum is computed and why semblance is preferred over simple normalization.
- Explain the origin of static corrections, the vertical-ray assumption, and the role of datums and replacement velocity.
- Sketch how refraction data constrain the near-surface model and name the main delay-time methods.

## Prerequisites

- Common-midpoint (CMP) geometry and fold (Term 1 Lecture 1).
- Basic wave propagation: traveltime, ray path, reflection, refraction.
- The convolutional seismic trace model.

## Timing (90 minutes)

| Section | Time | Notes |
|---------|------|-------|
| 1. Velocity models | 15 min | Definitions + ray diagrams |
| 2. Goal of kinematic processing | 10 min | Motivation, zero-offset stack |
| 3. NMO correction | 25 min | Formula, stretch, muting, residual moveout |
| 4. Velocity analysis | 20 min | Vertical/horizontal spectra, semblance |
| 5. Static correction fundamentals | 10 min | Origin, datums, replacement velocity |
| 6. Near-surface model building | 10 min | Refraction, delay-time methods |
| Total | 90 min | Tight; examples must be short |

## Section 1 — Velocity models

- Why velocities matter in processing: every traveltime correction needs a velocity.
- Layered model with horizontal layers.
- Interval velocity $v_i$ of one layer.
- Average velocity (vertical ray assumption):
  $$ V_\text{avg}(T) = \frac{\sum_i v_i \Delta t_i}{\sum_i \Delta t_i} = \frac{z}{T} $$
- RMS velocity (straight ray / small-spread assumption):
  $$ V_\text{rms}^2(T) = \frac{\sum_i v_i^2 \Delta t_i}{\sum_i \Delta t_i} $$
- NMO velocity for a single layer and for layered media:
  $$ t^2(x) = t_0^2 + \frac{x^2}{V_\text{nmo}^2} $$
- Stacking velocity: the velocity that best flattens a gather for stack.
- Optimal NMO velocity over an offset range.
- Figure needed: ray diagrams for vertical, straight and hyperbolic rays; velocity curves plotted versus time.

## Section 2 — Goal of kinematic processing

- Idealised imaging model: reflectors are mapped from zero-offset traveltime.
- Real data contain:
  - source–receiver offset,
  - near-surface time delays (statics),
  - structural dips (handled later by migration).
- Kinematic processing removes the offset-dependent traveltime.
- Statics removes near-surface delays.
- Result: a zero-offset stack section that approximates the geology, to be improved at the imaging stage.
- We want traveltimes to show geological structures, not acquisition geometry.

## Section 3 — NMO correction

- CMP gather reflection time for a flat layered medium:
  $$ t^2(x) = t_0^2 + \frac{x^2}{V_\text{nmo}^2} $$
- NMO correction:
  $$ \Delta t_\text{nmo}(x) = t(x) - t_0 = \sqrt{t_0^2 + \frac{x^2}{V_\text{nmo}^2}} - t_0 $$
- How correction changes with velocity, depth, offset and dip (qualitative rules).
- Under-correction: velocity too high → event still curved down.
- Over-correction: velocity too low → event curved up.
- Stretch effect: far-offset samples are mapped to earlier times, low frequencies appear.
- Quantitative stretch measure, e.g.:
  $$ \frac{\partial t}{\partial t_0} = \frac{t_0}{\sqrt{t_0^2 + x^2/V^2}} $$
  or fractional stretch threshold used for muting.
- Why muting is necessary before stack.
- Residual moveout: small curvature left after first NMO, handled by residual statics / velocity updates.
- Figures needed:
  - CMP gather before and after NMO.
  - Under/over-corrected gathers.
  - Stretch demonstration: a wavelet before and after NMO at near and far offset.
  - Mute zone illustration.

## Section 4 — Velocity analysis

- Principle: try many velocities and measure how well each flattens the gather.
- Vertical velocity spectrum at one CMP:
  - For each $(t_0, V)$ pair sum amplitudes along the corresponding hyperbola.
  - Simple normalized sum (stacked amplitude).
  - Semblance:
    $$ S(t_0, V) = \frac{1}{M} \frac{\sum_t \left( \sum_{i=1}^{M} u_i(t - \Delta t_i) \right)^2}{\sum_t \sum_{i=1}^{M} u_i^2(t - \Delta t_i)} $$
  - Advantages of semblance: robust to amplitude variations, highlights coherent events.
- Horizontal (spatial) velocity spectra: continuous picks along a line.
- Practical picking of velocity trends.
- Figures needed:
  - CMP gather with several trial hyperbolae.
  - Vertical semblance panel with picks.
  - Horizon-consistent or spatial velocity spectra concept.

## Section 5 — Static correction fundamentals

- Origin of statics: elevation changes, weathering-layer thickness/velocity, water-column and tidal variations.
- Short-wavelength vs long-wavelength statics.
- Common rule of thumb: half the spread length separates the two.
- Vertical-ray assumption: rays through the near surface are nearly vertical.
- Field statics: measure elevation and near-surface velocity, compute time shift.
- Datums:
  - Intermediate datum (close to base of weathering).
  - Final datum (reference level for stack/migration).
  - How to choose them.
- Replacement velocity: velocity used to replace the weathering layer.
- Effect of replacement-velocity choice on computed statics.
- Figure needed: ray diagram showing elevation, weathering layer, intermediate datum, final datum, replacement velocity.

## Section 6 — Near-surface model building

- Sources of information: uphole surveys, microgravity, refraction shots, well logs.
- Refraction statics: common problem statement.
- Evolution: delay-time methods → tomography.
- Delay-time methods:
  - Hagedoorn's plus-minus method.
  - Generalized Reciprocal Method (GRM).
  - Generalized Linear Inversion (GLI).
- Mention diving-wave tomography as modern approach; details in Term 3.
- Figures needed:
  - Simple two-layer refraction model.
  - Delay-time geometry.

## Figures to generate

| Figure | Script | Output |
|--------|--------|--------|
| Velocity definitions | `plot_velocity_definitions.py` | `term01_lec03_velocity_definitions.png` |
| NMO geometry and corrected gather | `plot_nmo_correction.py` | `term01_lec03_nmo_correction.png` |
| Under/over-correction | `plot_nmo_velocity_sensitivity.py` | `term01_lec03_nmo_under_over.png` |
| NMO stretch and mute | `plot_nmo_stretch_mute.py` | `term01_lec03_nmo_stretch_mute.png` |
| Velocity spectrum / semblance | `plot_velocity_spectrum.py` | `term01_lec03_velocity_spectrum.png` |
| Statics datums and replacement velocity | `plot_statics_datums.py` | `term01_lec03_statics_datums.png` |
| Refraction delay-time geometry | `plot_refraction_geometry.py` | `term01_lec03_refraction_geometry.png` |

## Key equations to include

- Average, RMS, NMO velocities.
- Hyperbolic traveltime and NMO correction.
- Stretch measure.
- Semblance.

## Comprehension questions

1. Why is the RMS velocity always greater than or equal to the average velocity for the same layered medium?
2. What happens to a reflection event in a CMP gather if the NMO velocity used is too low?
3. Why do we mute the far offsets of an NMO-corrected gather before stacking?
4. What does a semblance velocity spectrum display on its axes, and what does a bright peak mean?
5. Explain why a near-surface anomaly produces the same time shift on all reflections of a single trace.

## Sources to cite

- Hatton, Worthington & Makin (1986), *Seismic Data Processing: Theory and Practice* — NMO, velocity analysis, statics.
- CGG ODT01A Data Analysis Part 1 & Part 2 — gathers, NMO, velocity spectra.
- CGG ODT6 Imaging Part 2 — velocity model building.
- Existing slide deck `slides/raw/term01_lecture02_kinematics.pptx`.
- Existing lecture plan `slides/raw/plan_term01_lecture02_kinematics.docx`.

## Open questions for instructor

- Should the split be named `lec02a`/`lec02b` or renumbered to `lec02` and `lec03`?
- Do you want the Russian outline alongside the English one, or only after notes are approved?
