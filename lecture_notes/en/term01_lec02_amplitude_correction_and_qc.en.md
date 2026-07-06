---
title: Term 1 Lecture 02 — Amplitude Corrections and Quality Control of Input Data
author: Seismic Data Processing Course
---

# Amplitude Corrections and Quality Control of Input Data

## Why this lecture matters

A seismic trace is not just a picture of the subsurface. It is a record of elastic energy that has been changed by every step of its journey: source radiation, propagation through the earth, reflection, transmission, absorption, scattering, and the conditions at the receiver. By the time we see it on screen, the amplitudes have usually decayed by orders of magnitude and have been further distorted by the acquisition system.

If all we care about is structure, we could stop after stacking and migration. But modern seismology uses amplitudes for much more: AVO (amplitude versus offset), reservoir characterization, stratigraphic interpretation, and time-lapse monitoring. Those applications need amplitudes that mean something physically. This lecture is about making amplitudes usable.

We will look at:

1. The physical effects that change amplitudes during propagation.
2. The difference between preserving true amplitudes and merely equalizing them for display or intermediate processing.
3. Spherical divergence correction — the first deterministic amplitude correction.
4. Deterministic equalization methods such as amplitude normalization and AGC.
5. Surface-consistent amplitude correction — separating source, receiver, offset, and structural effects.
6. Quality control of input data, especially geometry verification.

## 1. Physical amplitude effects during wave propagation

When a seismic wave travels from the source to the receiver, its amplitude decreases. Several mechanisms contribute. Some are deterministic; others are statistical; some are hard to separate from each other.

### Reflection and transmission at boundaries

At every elastic interface, the wave is split into a reflected part and a transmitted part. The amount of reflected energy depends on the impedance contrast between the two layers. For a P-wave at normal incidence,

$$
R = \frac{Z_2 - Z_1}{Z_2 + Z_1}, \qquad Z = \rho v
$$

where $Z$ is the acoustic impedance, $\rho$ is density, and $v$ is P-wave velocity. A stack of many thin layers therefore reduces the transmitted energy cumulatively. This is one reason deep reflections are weaker than shallow ones, even before spreading and absorption are considered.

### Mode conversion

At non-normal incidence, P-wave energy is not simply reflected or transmitted as P-wave energy. Some of it converts to S-wave energy, and vice versa. The amount of conversion increases with incidence angle. This means that the reflected P-wave amplitude is further reduced because some of its energy has been diverted into S-waves. Mode conversion is important for AVO analysis, but for our present purpose it is simply another amplitude-loss mechanism.

### Spherical divergence (geometric spreading)

This is the most predictable amplitude effect. As the wavefront expands, the same total energy is spread over a larger area. In a homogeneous 3D medium with a point source, the wavefront is a sphere. The area of the sphere grows as $r^2$, so the energy density falls as $1/r^2$. Because amplitude is proportional to the square root of energy density, the amplitude falls as $1/r$.

In a constant-velocity medium, the distance $r$ is proportional to the two-way traveltime $t$, so the amplitude decay can be written as

$$
A \propto \frac{1}{t}
$$

This is the origin of the $t$-gain correction. In practice, processing packages sometimes use $t^2$ instead of $t$; we will return to this convention in Section 3.

### Absorption and scattering

**Absorption** (or intrinsic attenuation) converts elastic energy into heat. It is controlled by the quality factor $Q$ of the rock. Absorption is frequency dependent: higher frequencies are attenuated more than lower ones. As a result, the recorded spectrum shifts toward lower frequencies with increasing traveltime.

**Scattering** redirects energy by small-scale inhomogeneities in velocity and density. It is like fog scattering light: some of the original wavefront energy is lost to the coherent reflected signal.

In practice, absorption and scattering are often treated together because they are difficult to separate from recorded data alone. They are corrected together by **Q-compensation** or broader **amplitude recovery** methods, which are covered in later terms.

### Near-surface source and receiver effects

On land, the coupling between the source and the ground, and between the geophone and the ground, varies from location to location. A shot in loose soil sends less energy into the earth than a shot in compacted soil. A geophone on rock responds differently from one on mud. Marine sources can have gun drop-outs or array directivity effects. These variations are multiplicative: they scale the entire trace by a location-dependent factor.

### Summary of amplitude effects

Figure [fig:amplitude_effects] is a schematic of the main effects.

![Planned figure: `figures/term01_lec02/term01_lec02_amplitude_effects_ray_diagram.png` — Ray diagram showing reflection/transmission, mode conversion, spherical divergence, absorption/scattering, and near-surface source/receiver effects.](./figures/term01_lec02/term01_lec02_amplitude_effects_ray_diagram.png)

*Figure 1: Physical effects that reduce seismic amplitude as the wave travels from source to receiver. Not all of these can be separated in practice.*

## 2. Two philosophies of amplitude processing

Before applying any amplitude correction, we must decide what we are trying to achieve. There are two broad philosophies.

### True amplitude / relative amplitude preservation

The goal is to recover amplitudes that are proportional to the earth’s reflection coefficients, or at least to preserve the relative amplitudes between traces and offsets. This is essential for AVO, AVAz, amplitude-based interpretation, and reservoir monitoring. Every step in the processing flow must be chosen with this goal in mind.

### Amplitude equalization for intermediate steps

The goal is to make the data visible and easy to process. The absolute amplitudes may be changed intentionally. For example, we may apply AGC so that weak deep reflections can be seen on the screen, or normalize traces so that all have the same maximum amplitude. These operations are not reversible and do not preserve physical amplitudes, but they are useful for visualization, structural interpretation, and kinematic processing (picking velocities, statics, etc.).

The key rule is: **do not apply AGC or aggressive equalization before any amplitude-sensitive analysis**. If you do, you destroy the very signal you are trying to interpret.

## 3. Spherical divergence correction

Spherical divergence correction is the simplest deterministic amplitude correction. Because the physics is well understood, we can apply it directly.

### Constant-velocity model

In a constant-velocity medium, the amplitude of a primary reflection falls as $1/t$ because the wavefront is a sphere. To compensate, we multiply the trace by a gain that grows as $t$:

$$
G(t) = t
$$

or, more generally,

$$
G(t) = t^n
$$

where $n$ depends on the convention and the assumed wavefront geometry.

### Why $t^2$?

The $t^2$ convention comes from thinking about energy rather than amplitude. If the amplitude falls as $1/t$, then the energy falls as $1/t^2$. Some packages define the gain as the inverse of the energy loss, so they apply a $t^2$ gain. Other packages keep the gain as the inverse of amplitude and use $t$. The important thing is to know which convention your software uses. In this course, when we write $t^n$, we mean the user must choose the appropriate exponent for their package; the physics is the same.

### Curved-ray and layered-earth corrections

Real velocities usually increase with depth, so rays bend and the wavefront expands faster than in a constant-velocity sphere. A common approximation for a layered medium is

$$
A \propto \frac{1}{t \, V_{\text{rms}}^2(t)}
$$

where $V_{\text{rms}}(t)$ is the RMS velocity. This requires knowing the velocity, which is not always available at the early stages of processing. Therefore, a simple $t$-gain is often used as a first approximation, and the exact correction is deferred to migration, which accounts for the full 3D wavefront geometry.

### Worked example

Suppose a reflection arrives at two-way time $t = 2.0$ s. Using a constant-velocity $t$-gain:

$$
G(2.0\,\text{s}) = 2.0
$$

A sample with amplitude $0.05$ at that time would be scaled to $0.10$. If the package uses a $t^2$ gain instead:

$$
G(2.0\,\text{s}) = (2.0)^2 = 4.0
$$

and the same sample would be scaled to $0.20$. Both conventions are correct in their own context; the difference is whether the output is intended to be amplitude-like or energy-like.

Figure [fig:spherical_divergence] shows a synthetic gather before and after divergence correction.

![Planned figure: `figures/term01_lec02/term01_lec02_spherical_divergence_correction.png` — Uncorrected and corrected shot gathers, with amplitude-versus-time curves.](./figures/term01_lec02/term01_lec02_spherical_divergence_correction.png)

*Figure 2: Spherical divergence correction. (Left) Raw gather with amplitude decaying with time. (Right) After applying a time-dependent $t$-gain. The lower panels show the mean amplitude decay before and after correction.*

## 4. Deterministic amplitude equalization

Even after divergence correction, amplitudes may still vary from trace to trace or from time to time. For intermediate visualization and processing, we can apply deterministic equalization methods. These are not true amplitude corrections, but they are useful when used knowingly.

### Amplitude normalization

Each trace is scaled by a constant derived from its own amplitude statistics. Common choices are the maximum absolute amplitude, the mean absolute amplitude, or the RMS amplitude:

$$
A_{\text{rms}} = \sqrt{\frac{1}{N} \sum_{n=1}^{N} a_n^2}
$$

After normalization, every trace has the same overall amplitude level. The relative amplitudes **within** each trace are preserved, but the relative amplitudes **between** traces are intentionally changed. This is useful for display but harmful for AVO.

### Automatic gain control (AGC)

AGC applies a time-varying gain on each trace. A sliding window of length $W$ is moved down the trace, and the gain at the center of the window is set to the reciprocal of the local amplitude statistic (usually the sum of absolute amplitudes or the RMS amplitude). The gains are interpolated between window centers to give a smooth function.

Mathematically, for a window centered at time $t$:

$$
G(t) = \frac{1}{\sum_{n \in \text{window}} |a_n|}
$$

or, using RMS:

$$
G(t) = \frac{1}{A_{\text{rms}}(\text{window})}
$$

#### Effect of window length

A **short window** makes every window have the same amplitude, nearly erasing all amplitude variation. A **long window** preserves more of the original amplitude variation. The choice depends on the goal: short windows for visualization, longer windows for processing that still needs some amplitude information.

#### Appropriate use cases

AGC and normalization are appropriate for:

- **Visualization**: making weak deep events visible.
- **Structural analysis**: mapping reflector continuity and terminations.
- **Kinematic processing**: helping to pick velocities, first breaks, and residual statics, where the main goal is to identify arrival times, not to preserve amplitudes.

#### Risks

AGC is not reversible, destroys true amplitude relationships, boosts noise, and can create misleading amplitudes. It should never be used before AVO or any quantitative amplitude study.

Figure [fig:agc] shows a trace before and after AGC.

![Planned figure: `figures/term01_lec02/term01_lec02_agc_example.png` — Trace and amplitude envelope before and after AGC.](./figures/term01_lec02/term01_lec02_agc_example.png)

*Figure 3: Effect of AGC. (Top) Original trace and its envelope. (Bottom) After AGC, the envelope is flattened, but the relative amplitudes of different reflections are lost.*

## 5. Surface-consistent amplitude correction

After divergence correction, amplitudes may still vary because of source and receiver coupling, near-surface conditions, and offset-dependent effects. These are not geology. Surface-consistent amplitude correction (SCAC) separates these factors from the geological signal.

### The four-factor model

The amplitude measured in a trace window is modeled as a product of four terms:

$$
A_{ij} = S_i \, R_j \, G_k \, M_l
$$

where

- $S_i$ is the source term for source $i$,
- $R_j$ is the receiver term for receiver $j$,
- $G_k$ is the geology/CMP term for common midpoint $k$,
- $M_l$ is the offset term for offset class $l$.

This model is multiplicative because coupling and near-surface effects scale the recorded amplitude. By taking logarithms, the product becomes a sum, and the problem becomes a large linear system:

$$
\log A_{ij} = \log S_i + \log R_j + \log G_k + \log M_l
$$

### Measuring trace amplitudes

The first step is to measure an amplitude in a chosen time window on each trace. The window should contain good-quality reflections and should be the same sequence of events across the survey. The amplitude statistic is usually RMS amplitude or mean absolute amplitude.

Window selection is critical. If the window is too noisy, the measured amplitude is biased. If the window includes large moveout, events may fall outside the window at far offsets. For shallow data, offset-dependent windows may be needed.

### Solving the model: Gauss–Seidel iteration

The linear system is usually solved iteratively. A common order is source → receiver → offset. In the first iteration, the receiver and offset terms are assumed zero, and the source terms are estimated. Then, using the source terms, the receiver terms are estimated, and so on. In subsequent iterations, each term is updated using the current estimates of the others:

$$
\log S_i = \frac{1}{N_i} \sum \left( \log A_{ij} - \log R_j - \log M_l \right)
$$

and similarly for $R_j$ and $M_l$. Iterations stop when the residual between the predicted and measured amplitudes becomes small.

This is the same Gauss–Seidel idea that is used for surface-consistent residual statics, which will be covered in the next lecture.

### Two-factor vs. four-factor models

A **two-factor model** (source + receiver only) is more stable because it has fewer unknowns. However, it cannot separate offset and structural variations, so it may leak geology into the source/receiver terms and distort AVO.

A **four-factor model** is more physically complete but has more unknowns. It can be unstable if the fold is low. There is also leakage between terms: an error in one term can be partly compensated by an opposite error in another term. The order in which terms are solved matters.

### The CMP/geology term

The CMP term $G_k$ contains both reflectivity and spatially varying AVO effects. Applying it would remove the very geological amplitude variations we want to preserve. Therefore, in practice, the CMP term is often handled carefully: sometimes it is not applied, or an AVO trend is subtracted from the picks before decomposition so that SCAC only sees the residual surface-consistent effects.

### Practical example

Consider a land survey where some shots are fired in the weathering layer and others penetrate below it. The shots in the weathering layer may have amplitudes 10–20 dB lower. SCAC would estimate a low source term for those shots and apply a compensating gain. After correction, the amplitude variations across the section are more consistent, and the remaining variations are more likely to be geology.

Figure [fig:scac] shows a synthetic CMP gather before and after surface-consistent amplitude correction.

![Planned figure: `figures/term01_lec02/term01_lec02_surface_consistent_amplitude.png` — Synthetic gather with source/receiver amplitude anomalies before and after correction.](./figures/term01_lec02/term01_lec02_surface_consistent_amplitude.png)

*Figure 4: Surface-consistent amplitude correction. (Left) Synthetic gather with source and receiver amplitude anomalies. (Right) After correction, the amplitudes are balanced and the geological AVO trend is preserved.*

## 6. Quality control of input data

Before any amplitude correction or processing step, we must verify that the input data are correct. Geometry errors are particularly dangerous because they affect every subsequent process.

### Geometry verification

Every trace must be assigned the correct source, receiver, and midpoint positions. If a trace is assigned to the wrong CMP, it will stack with traces that do not share the same subsurface reflection point. This leads to:

- mis-stacking and loss of signal,
- wrong stacking velocities,
- artifacts in the stacked section,
- incorrect amplitude and fold maps.

Geometry verification should be done before sorting, stacking, or any multi-trace process.

### Visual geometry QC

#### Overlay expected offset curves

On a shot gather, the direct arrival or first break should follow an approximately linear trajectory in the time–offset plane. If the near-surface velocity is known, the expected arrival time for each offset is

$$
t(x) = \frac{x}{v_{\text{near}}}
$$

where $x$ is the source–receiver offset. Overlaying this curve on the gather is a quick check. If many traces do not fall near the curve, the geometry or timing is likely wrong.

#### Linear-moveout (LMO) stacks

An LMO stack applies a linear time shift proportional to offset and then stacks the data. If the chosen moveout velocity matches the direct arrival or refraction, the event aligns horizontally. Misalignment indicates geometry or timing errors.

### First-break-based QC

First-break picking is the most common geometry and statics QC tool. The idea is:

1. Predict first-break traveltimes from a near-surface velocity model or a known direct-wave velocity.
2. Pick the actual first breaks on the data.
3. Compare predicted and observed picks.

Systematic differences reveal problems:

- A constant time shift suggests a timing error or incorrect start-of-data delay.
- A spatially varying shift suggests a geometry error or near-surface velocity anomaly.
- A sinusoidal or cable-shaped pattern may indicate feathering or positioning errors.

### Attribute analysis for field-data QC

After geometry is verified, we examine the data for amplitude, frequency, and noise attributes. Common attributes include:

#### Amplitude attributes
- Mean or RMS amplitude in an analysis window.
- Amplitude in selected frequency bands.
- Signal-to-microseism ratio.

#### Correlation attributes
- Dominant frequency.
- Spectral width or bandwidth.
- Signal-to-noise ratio from autocorrelation or cross-correlation.

#### Spectral attributes
- Spectral energy.
- Central frequency.
- Peak frequency.
- Bandwidth.

RMS amplitude is usually preferred over simple mean amplitude because it is less affected by a single extreme sample.

### Statistical and map-based QC

- **Histograms** show the distribution of amplitudes, frequencies, and noise levels. Outliers may indicate bad traces, acquisition problems, or unusual geology.
- **Sorts by source, receiver, offset, and CMP** help separate acquisition-related patterns from geology. For example, a stripe that follows the source line is probably a source problem, not a subsurface feature.
- **Attribute maps** plot attributes against spatial coordinates. Shallow features produce vertical stripes on shot/channel maps; stationary receiver coupling problems produce horizontal stripes; buried features produce diagonal stripes.

Figure [fig:qc_geometry] shows the planned geometry QC figure.

![Planned figure: `figures/term01_lec02/term01_lec02_qc_geometry_first_breaks.png` — Shot gather with predicted offset curves, LMO panel, and first-break residual plot.](./figures/term01_lec02/term01_lec02_qc_geometry_first_breaks.png)

*Figure 5: Geometry QC using first breaks and LMO. (Left) Shot gather with predicted direct-arrival curve. (Middle) LMO stack at the near-surface velocity. (Right) Residuals between predicted and picked first-break times.*

Figure [fig:qc_amplitude_map] shows a receiver-index amplitude map.

![Planned figure: `figures/term01_lec02/term01_lec02_qc_amplitude_map.png` — Receiver-index amplitude map with an outlier group highlighted.](./figures/term01_lec02/term01_lec02_qc_amplitude_map.png)

*Figure 6: Receiver-index amplitude map. A group of high-amplitude receivers (red) may indicate coupling problems or a localized near-surface anomaly.*

## Summary

- Seismic amplitudes are reduced by reflection/transmission, mode conversion, geometric spreading, absorption, scattering, and near-surface effects.
- **True amplitude preservation** aims to keep amplitudes proportional to reflection coefficients; **amplitude equalization** only makes data visible and processable.
- **Spherical divergence correction** is a deterministic $t^n$ gain that compensates for wavefront spreading. The choice of $n$ depends on package convention.
- **Amplitude normalization** and **AGC** are statistical methods useful for visualization and kinematic processing, but they destroy true amplitude relationships and should not be used before AVO.
- **Surface-consistent amplitude correction** separates source, receiver, offset, and CMP terms using a multiplicative model solved by Gauss–Seidel iteration.
- **Geometry verification** is the first QC step. Methods include offset-curve overlays, LMO stacks, and first-break residuals. Attribute maps and statistical summaries help identify acquisition problems.

## Comprehension questions

1. Why does AGC make a section easier to see but less suitable for AVO analysis?
2. List three physical effects that reduce seismic amplitude as the wave travels from source to receiver.
3. If a trace is scaled by its own RMS amplitude, what happens to the relative amplitudes of two reflections on that trace? What happens to the relative amplitudes between two different traces?
4. Why is geometry verification the first QC step before any processing step?
5. In a surface-consistent amplitude model, which factor would you expect to capture a wet patch near a receiver station? Which factor would you expect to capture a zone where the source coupling is poor?
6. Explain the difference between a $t$-gain and a $t^2$-gain for spherical divergence correction. In what sense are both physically reasonable?
7. A shot/channel amplitude map shows a vertical stripe. What kind of feature might cause this? What if it shows a horizontal stripe?

## References and further reading

- `wiki/concepts/amplitude_effects.md`
- `wiki/concepts/spherical_divergence.md`
- `wiki/concepts/automatic_gain_control.md`
- `wiki/concepts/surface_consistent_amplitude.md`
- `wiki/concepts/seismic_data_qc.md`
- `wiki/sources/yilmaz_practical_seismic_data_analysis_amplitude.md`
- `wiki/sources/hill_introduction_to_seismic_processing_ch21.md`
- `wiki/sources/brown_2002_surface_consistent_amplitude_correction.md`
- `wiki/sources/cgg_odt01_data_analysis_part1.md`
- `wiki/sources/cgg_odt01_data_analysis_part2.md`
