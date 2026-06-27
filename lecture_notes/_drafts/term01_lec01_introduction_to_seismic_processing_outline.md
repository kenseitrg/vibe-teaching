# Draft outline: Term 1 Lecture 1 — Introduction to seismic data processing

## Lecture metadata

- **Lecture**: Term 1, Lecture 1
- **Topic**: Introduction to seismic data processing
- **Duration**: 90 minutes
- **Audience**: Undergraduate geophysics students (Term 1)
- **Prerequisites**: Basic wave physics, reflection/refraction, sampling, signal-to-noise ratio

## Learning objectives

By the end of the lecture students should be able to:

1. Explain the place of seismic processing within geological exploration (ГРР) and its relation to interpretation.
2. Distinguish the kinematic and dynamic problems of seismic processing.
3. List the four main processing phases and give examples of each.
4. Describe the CMP method and the meaning of fold, offset, and moveup.
5. Name the main seismic data sorts and why each is useful.
6. Identify the main field data formats and explain why geometry assignment is a separate step.

## Section breakdown and timing

| Section | Time | Content |
|---------|------|---------|
| 1. Course structure and role of processing | 8 min | Course goals; processing as part of ГРР; processing vs interpretation |
| 2. What we want to recover: the geological signal | 10 min | The idealized earth response; processing goal = recover geological information and prepare data for interpretation; why this is hard |
| 3. What contaminates the seismic record | 12 min | Acquisition factors and wave-propagation phenomena; signal vs noise; kinematic vs dynamic problems |
| 4. Main processing flow | 20 min | Preprocessing → kinematics → dynamics → imaging; iterative nature of modern flows |
| 5. Limitations and challenges | 8 min | Wavelength, acquisition geometry, data volume, non-uniqueness |
| 6. 2D acquisition and CMP method | 20 min | Land/marine sources and receivers; CMP/CDP; fold; acquisition parameters; fold formula |
| 7. Data sorts and formats | 7 min | Shot, receiver, CMP, offset gathers; SEG-Y/SEG-D/SPS/UKOOA; loading and geometry QC |
| 8. Comprehension questions and discussion | 5 min | 3–5 short questions |

## Figures and visualizations needed

1. Seismic in the exploration workflow (lifecycle of geological study).
2. Idealized impulse response of a layered earth vs. the recorded band-limited, noisy trace.
3. Acquisition factors and wave-propagation phenomena: a schematic of what gets added to the ideal signal.
4. Kinematic vs dynamic distortions on a simple gather.
5. Four-phase processing flow diagram.
6. 2D acquisition geometry: source, receivers, midpoints, fold build-up.
7. CMP gather cartoon showing NMO and stack.
8. Shot/receiver/CMP/offset sort cartoons.
9. SEG-Y file structure and trace header essentials.

## Key equations

- Approximate 2D fold: $F \approx N / (2 \cdot \text{moveup})$.
- CMP spacing from receiver spacing: $\Delta x_{\text{CMP}} = \Delta x_{\text{receiver}} / 2$.
- Moveup for marine 2D: $\text{moveup} = \Delta x_{\text{shot}} / (2 \Delta x_{\text{CMP}})$.

## Source material

- Hill & Rüger (2020), *Illustrated Seismic Processing, Vol. 2*, Appendix A–B and Chapter 31.
- CGG ODT01 Data Analysis Part 1 & Part 2.
- Margrave (2006), *Methods of Seismic Data Processing*, Chapter 1.
- Vermeer (2012), *3D Seismic Survey Design*, Chapter 1.
- SEG-Y rev 2.0 and SEG SPS rev 2.1 format standards.

## Wiki links

- [Seismic data processing overview](../../wiki/concepts/seismic_data_processing.md)
- [Seismic acquisition — 2D essentials](../../wiki/concepts/seismic_acquisition.md)
- [Common midpoint (CMP) gather and fold](../../wiki/concepts/common_midpoint.md)
- [Seismic data sorting domains / gathers](../../wiki/concepts/seismic_data_sorts.md)
- [Seismic data formats](../../wiki/concepts/seismic_data_formats.md)

## Comprehension questions (draft)

1. Why is seismic data processing necessary? Name two acquisition factors and two wave-propagation factors that complicate the raw record.
2. What is the difference between a kinematic and a dynamic processing task?
3. Explain why the CMP method improves signal-to-noise ratio.
4. A 2D marine survey has 240 channels with 12.5 m group spacing and 25 m shot spacing. What are the CMP spacing and nominal fold?
5. Why must geometry information from SPS/UKOOA files be merged with SEG-Y trace data before processing?
