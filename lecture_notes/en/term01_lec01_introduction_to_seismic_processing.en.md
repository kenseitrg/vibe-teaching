---
title: Term 1 Lecture 1 — Introduction to seismic data processing
author: Seismic Data Processing Course
lang: en
---

# Term 1 Lecture 1 — Introduction to seismic data processing

## Learning objectives

By the end of this lecture you should be able to:

1. Explain where seismic data processing fits into geological exploration and how it relates to interpretation.
2. State the main goal of seismic processing: recover geological information from raw records and prepare data for interpretation.
3. Distinguish between kinematic and dynamic processing problems.
4. List the four main processing phases and give examples of each.
5. Describe the CMP method and the meaning of fold, offset, and moveup.
6. Name the main seismic data sorts and explain why each is useful.
7. Identify the main field data formats and explain why geometry assignment is a separate preprocessing step.

---

## 1. Course structure and the role of processing

Seismic data processing is a set of procedures that turn raw field recordings into images and measurements that geoscientists can interpret. In this course we will follow the main stages of a 2D land or marine processing flow, understand the physics behind each step, and learn how to choose parameters in production software.

The broader context is **geological exploration**. Seismic is only one source of information; it must be integrated with well data, geological maps, and prior knowledge. Figure 1 shows a simplified lifecycle.

![Geological exploration lifecycle](figures/term01_lec01/term01_lec01_exploration_workflow.png)

**Figure 1 — Seismic processing in the exploration workflow.** (a) Geological maps and prior knowledge. (b) Seismic acquisition in the field. (c) Processed seismic sections and velocity models. (d) Geological model of the subsurface. (e) Well drilling and production. Seismic processing connects the field data to the interpretable image.

The course is organized in three terms:

- **Term 1 — Foundations:** data formats, geometry, statics, velocities, single-channel filtering, deconvolution, surface-consistent processing.
- **Term 2 — Intermediate methods:** absorption, FK/Radon filtering, multiples, imaging fundamentals.
- **Term 3 — 3D and modern techniques:** 3D geometry, advanced denoise, regularization, QC, well-driven processing.

At the practical sessions we will use an industry processing package to see how the theoretical steps are implemented and how parameter choices affect the result.

---

## 2. What we want to recover: the geological signal

The ideal seismic experiment would measure the earth's **reflectivity** directly: a spike at every impedance contrast, with amplitude proportional to the reflection coefficient. In practice we never record this ideal signal.

What we record is a band-limited, noisy, distorted version. Figure 2 shows the progression from the ideal reflectivity series to the recorded trace.

![Idealized vs recorded trace](figures/term01_lec01/term01_lec01_idealized_vs_recorded_trace.png)

**Figure 2 — From geology to the recorded trace.** (a) Ideal reflectivity series. (b) Convolution with a band-limited wavelet gives the ideal seismic response. (c) The recorded trace adds noise, multiples, and acquisition effects.

The **goal of seismic processing** is therefore:

> Remove or compensate for everything that is not geology, and prepare the data so that an interpreter can identify structures, stratigraphy, and rock properties.

This is usually split into two connected tasks:

- **Kinematic task:** place reflected energy at the correct position in space and time.
- **Dynamic task:** recover true relative amplitudes and wavelet character.

---

## 3. What contaminates the seismic record

The recorded wavefield is a superposition of useful signal and unwanted energy. Some contaminating factors come from the acquisition system, others from wave propagation.

![Distortions added to the geological signal](figures/term01_lec01/term01_lec01_distortions_overview.png)

**Figure 3 — Distortions added to the geological signal.** The clean primary reflections are accompanied by ghosts, array responses, geometric spreading, absorption, multiples, refractions, surface waves, and random noise.

### Acquisition factors

| Factor | Effect |
|--------|--------|
| Source/receiver positions | Geometry must be known accurately; otherwise events are mispositioned. |
| Source signature | Every source emits a finite wavelet, not an ideal spike. |
| Receiver arrays / groups | Arrays attenuate noise but also filter the signal. |
| Instrument response | Recording system has its own amplitude and phase response. |
| Sampling | Finite time and spatial sampling limit resolution and can alias events. |

### Wave-propagation factors

| Factor | Effect |
|--------|--------|
| Geometric spreading | Amplitude decreases with distance from the source. |
| Absorption (Q) | High frequencies are lost, changing the wavelet with travel time. |
| Transmission losses | Energy is lost at every interface. |
| Multiples | Energy bounces more than once before reaching the receiver. |
| Refractions and surface waves | Coherent energy that is usually noise for reflection imaging. |
| Mode conversion | P-waves may convert to S-waves at interfaces. |
| Anisotropy | Velocity depends on propagation direction. |

The same physical event can be signal in one context and noise in another. For example, refractions are removed before stacking, but their first arrivals are used to build near-surface velocity models for statics corrections.

---

## 4. Kinematic vs dynamic problems

Processing algorithms can be grouped by which aspect of the data they address.

### Kinematic problem

> **Where in space and time does the recorded energy belong?**

Examples:
- **Static corrections** compensate for near-surface time delays.
- **Normal moveout (NMO) correction** flattens reflection hyperbolas in a CMP gather.
- **Migration** moves dipping reflections and diffractions to their correct subsurface positions.

### Dynamic problem

> **What are the true relative amplitudes and wavelet shape?**

Examples:
- **Gain corrections** compensate for geometric spreading and absorption.
- **Deconvolution** compresses the wavelet and improves temporal resolution.
- **Q-compensation** restores high-frequency attenuation.
- **Demultiple** attenuates multiples that distort amplitudes.

In modern processing these two problems are solved iteratively. A better velocity model improves migration; a cleaner image helps amplitude interpretation; amplitude analysis can feed back into velocity model building.

---

## 5. Main processing flow

A typical 2D processing sequence has four phases.

![Processing flow](figures/term01_lec01/term01_lec01_processing_flow.png)

**Figure 4 — Processing workflow (simplified).** Modern seismic processing begins with data input and geometry assignment, iterates between kinematic (positioning) and dynamic (amplitude) corrections, and ends with imaging and model building.

### Phase 1 — Preprocessing

The inputs are field records (SEG-D or SEG-Y) and geometry files (SPS, UKOOA). Preprocessing:

- converts data to the processing system's internal format;
- assigns geometry to every trace (source and receiver coordinates, offset, CMP);
- performs quality control: fold, offsets, first breaks, amplitude consistency;
- computes field statics and produces a **brute stack** — a first rough image.

### Phase 2 — Kinematic processing

This phase improves the positioning of events:

- refraction and residual statics corrections;
- velocity analysis and NMO correction;
- building a velocity model for imaging.

### Phase 3 — Dynamic processing

This phase recovers amplitudes and removes unwanted energy:

- noise attenuation (random and coherent);
- multiple attenuation;
- deconvolution and wavelet processing;
- amplitude correction and Q-compensation;
- regularization and interpolation.

### Phase 4 — Imaging and post-imaging

The final phase places energy at its correct subsurface position:

- time or depth migration;
- post-migration conditioning for the interpreter (filtering, scaling, angle gathers).

---

## 6. Limitations and challenges

Several fundamental limits constrain what processing can achieve.

| Limitation | Consequence |
|------------|-------------|
| Seismic wavelength | Resolution is on the order of the wavelength; thin layers cannot be separated. |
| Acquisition geometry | Finite aperture, fold, and spatial sampling limit illumination and can alias dips. |
| Non-uniqueness | Different earth models can produce similar data; external information is needed. |
| Data volume | Modern surveys can be terabytes; algorithms must be computationally efficient. |
| Signal-to-noise ratio | Random noise can only be suppressed by stacking or averaging; coherent noise must be separated. |

The processor's job is to make the best use of the available data while being honest about what cannot be recovered.

---

## 7. 2D acquisition and the CMP method

In the first two terms we focus on 2D seismic lines. A source generates elastic waves, receivers record the returning wavefield, and each receiver produces one **trace**.

![2D acquisition geometry](figures/term01_lec01/term01_lec01_2d_acquisition_geometry.png)

**Figure 5 — 2D end-on acquisition geometry.** Sources move along the line; the receiver spread records each shot. Midpoints between source and receiver pairs build up the CMP coverage. The lower panel shows how fold increases from the line start to the full-fold plateau.

### Acquisition environments and sources

| Environment | Common sources | Receivers |
|-------------|----------------|-----------|
| Land | Dynamite, vibroseis | Geophone groups / arrays |
| Marine | Air-gun arrays | Hydrophone streamers or ocean-bottom cables |
| Transition zone | Various | Geophones and hydrophones |

### Key parameters

| Parameter | Symbol | Meaning |
|-----------|--------|---------|
| Source interval | $\Delta x_\text{shot}$ | Distance between consecutive shots |
| Receiver interval | $\Delta x_\text{rec}$ | Distance between receiver groups |
| Minimum offset | $x_\text{min}$ | Offset of the nearest receiver to the source |
| Maximum offset | $x_\text{max}$ | Offset of the farthest receiver |
| Record length | $T$ | Total recording time |
| Sampling interval | $\Delta t$ | Time between samples |
| Fold | $F$ | Number of traces contributing to one CMP stack |

### CMP spacing and moveup

For a simple 2D marine geometry the CMP spacing is half the receiver interval:

$$
\Delta x_\text{CMP} = \frac{\Delta x_\text{rec}}{2}.
$$

The **moveup** is the number of new CMP locations added per shot:

$$
\text{moveup} = \frac{\Delta x_\text{shot}}{2 \Delta x_\text{CMP}} = \frac{\Delta x_\text{shot}}{\Delta x_\text{rec}}.
$$

The nominal fold is approximately

$$
F \approx \frac{N_\text{channels}}{2 \times \text{moveup}} = \frac{N_\text{channels} \times \Delta x_\text{rec}}{2 \Delta x_\text{shot}}.
$$

**Worked example.** A marine survey has 240 channels, receiver interval 12.5 m, and shot interval 25 m.

- CMP spacing: $12.5 / 2 = 6.25$ m.
- Moveup: $25 / 12.5 = 2$.
- Nominal fold: $240 / (2 \times 2) = 60$.

### Why repeated observations help

The **common-midpoint (CMP) method** records the same subsurface region many times with different source–receiver offsets. This gives us:

1. **Velocity information** from the change of arrival time with offset (normal moveout).
2. **Signal-to-noise improvement** from stacking aligned traces.
3. **Multiple discrimination** because primaries and multiples have different moveout.

![CMP gather and stack](figures/term01_lec01/term01_lec01_cmp_gather_stack.png)

**Figure 6 — CMP gather and stack.** Left: raw CMP gather with a primary and a multiple. Right: after NMO correction the primary is flat and stacks constructively; the multiple is undercorrected and partially stacks out.

---

## 8. Data sorts and formats

### Common sorting domains

A **gather** is a group of traces sharing a common attribute. Changing the sort order changes what we see and what processing is convenient.

![Data sorts](figures/term01_lec01/term01_lec01_data_sorts.png)

**Figure 7 — Seismic data sorts on the source-receiver plane.** Each trace is a point $(x_s, x_r)$ in the source-receiver plane. A fixed source coordinate gives a shot gather, a fixed receiver coordinate gives a receiver gather, a fixed midpoint ($x_s+x_r=\text{const}$) gives a CMP gather, and a fixed offset ($x_s-x_r=\text{const}$) gives a common-offset gather.

| Gather | Sort key | Typical use |
|--------|----------|-------------|
| Shot gather | Source position | Noise attenuation, first-break analysis |
| Receiver gather | Receiver position | Shot interpolation, noise randomization |
| CMP gather | Midpoint | Velocity analysis, stacking, demultiple |
| Common-offset / offset plane | Offset | Common-offset migration, regularization |

### Field data formats

Seismic data arrive in specialized formats that must be loaded before processing.

| Format | Content | Typical role |
|--------|---------|--------------|
| SEG-D | Raw field records | Archive and initial loading |
| SEG-Y | Exchange format for traces | Intermediate products and final deliveries |
| SPS | Land geometry: source/receiver/relation files | Geometry assignment |
| UKOOA P1/90 | Marine/transition-zone geometry | Geometry assignment |

![SEG-Y structure](figures/term01_lec01/term01_lec01_segy_structure.png)

**Figure 8 — SEG-Y file organization.** SEG-Y rev 2.0 starts with an optional 128-byte tape label, a 3200-byte textual file header, and a 400-byte binary file header. Optional extended textual headers may follow. The bulk of the file is a sequence of data traces; each trace has a 240-byte trace header followed by sample values.

\pagebreak

\includegraphics[width=0.75\linewidth]{figures/term01_lec01/term01_lec01_segd_structure.png}

**Figure 9 — SEG-D file organization (raw field records).** SEG-D stores raw field data with a general header, multiple scan-type headers, channel-set headers, and trace headers preceding the data. It is used for archival and initial loading; traces are later converted to SEG-Y or a processing system's internal format.

Key trace header information in SEG-Y includes:

- shot and receiver line/point numbers;
- source and receiver X, Y, Z coordinates;
- offset;
- CMP or ensemble number;
- number of samples and sample interval.

Geometry files (SPS or UKOOA) describe where each source and receiver was located and how they are related to the recorded traces. **Geometry assignment** is the step that merges this spatial information with the seismic samples. A single mis-mapped byte in a SEG-Y header can misposition every trace, so this step is critical.

---

## 9. Summary

- Seismic processing turns raw recordings into interpretable images.
- Its goal is to recover geological information by compensating for acquisition effects and wave-propagation phenomena.
- Kinematic processing places energy correctly; dynamic processing recovers amplitudes.
- The CMP method uses repeated observations from different offsets to measure velocities, improve signal-to-noise ratio, and separate multiples.
- Field data come in specialized formats (SEG-D, SEG-Y, SPS, UKOOA); geometry must be carefully assigned before any processing.

---

## Comprehension questions

1. Why is seismic data processing necessary? Name two acquisition factors and two wave-propagation factors that complicate the raw record.
2. What is the difference between a kinematic and a dynamic processing task? Give one example of each.
3. Explain why the CMP method improves the signal-to-noise ratio.
4. A 2D marine survey has 240 channels with 12.5 m group spacing and 25 m shot spacing. What are the CMP spacing, moveup, and nominal fold?
5. Why must geometry information from SPS or UKOOA files be merged with SEG-Y trace data before processing?

---

## References and further reading

- Hill, S. J. & Rüger, A. (2020). *Illustrated Seismic Processing, Volume 2: Preimaging*. SEG. Appendix A, Appendix B, Chapter 31.
- CGG. ODT01 — Data Analysis Part 1 & Part 2 (training slides).
- Margrave, G. F. (2006). *Methods of Seismic Data Processing*. University of Calgary course notes, Chapter 1.
- Vermeer, G. J. O. (2012). *3D Seismic Survey Design*, 2nd ed. SEG, Chapter 1.
- SEG Technical Standards Committee (2017). SEG-Y rev 2.0 Data Exchange format.
- SEG Technical Standards Committee. SPS Format rev 2.1.
