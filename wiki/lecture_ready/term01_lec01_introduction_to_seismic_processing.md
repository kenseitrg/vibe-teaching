---
title: Term 1 Lecture 1 — Introduction to seismic data processing
status: lecture-ready
lecture: term01_lec01
concepts:
  - seismic_data_processing
  - seismic_acquisition
  - common_midpoint
  - seismic_data_sorts
  - seismic_data_formats
tags: [term01, lec01, introduction, workflow, acquisition, formats]
---

# Term 1 Lecture 1 — Introduction to seismic data processing

## Lecture goal

Give students a high-level map of seismic data processing: why we process, what the main stages are, how 2D data are acquired, and how raw field data are organized.

## Learning objectives

By the end of the lecture students should be able to:

1. Explain the place of seismic processing within geological exploration (ГРР) and its relation to interpretation.
2. Distinguish the kinematic and dynamic problems of seismic processing.
3. List the four main processing phases (preprocessing, kinematics, dynamics, imaging) and give examples of each.
4. Describe the CMP method and the meaning of fold, offset, and moveup.
5. Name the main seismic data sorts (shot, receiver, CMP, offset) and why each is useful.
6. Identify the main field data formats (SEG-Y, SEG-D, SPS, UKOOA) and explain why geometry assignment is a separate step.

## Prerequisites

- Basic physics of waves (propagation, reflection, refraction).
- Familiarity with the idea of sampling and signal-to-noise ratio.

## Key concepts (link to wiki)

- [Seismic data processing overview](../concepts/seismic_data_processing.md)
- [Seismic acquisition — 2D essentials](../concepts/seismic_acquisition.md)
- [Common midpoint (CMP) gather and fold](../concepts/common_midpoint.md)
- [Seismic data sorting domains / gathers](../concepts/seismic_data_sorts.md)
- [Seismic data formats](../concepts/seismic_data_formats.md)

## Suggested 90-minute outline

| Section | Time | Content |
|---------|------|---------|
| 1. Course structure and role of processing | 10 min | Goals of the course; processing as part of ГРР; processing vs interpretation |
| 2. What contaminates the seismic record | 15 min | Acquisition factors and wave-propagation phenomena; signal vs noise; kinematic vs dynamic problems |
| 3. Main processing flow | 20 min | Preprocessing → kinematics → dynamics → imaging; iterative nature of modern flows |
| 4. Limitations and challenges | 10 min | Wavelength, acquisition geometry, data volume, non-uniqueness |
| 5. 2D acquisition and CMP method | 20 min | Land/marine sources and receivers; CMP/CDP; fold; acquisition parameters; fold formula |
| 6. Data sorts and formats | 10 min | Shot, receiver, CMP, offset gathers; SEG-Y/SEG-D/SPS/UKOOA; loading and geometry QC |
| 7. Comprehension questions and discussion | 5 min | 3–5 short questions |

## Figures needed

1. Seismic in the exploration workflow (lifecycle of geological study).
2. Kinematic vs dynamic distortions on a simple gather.
3. Four-phase processing flow diagram.
4. 2D acquisition geometry with source, receivers, midpoints, fold build-up.
5. CMP gather cartoon showing NMO and stack.
6. Shot/receiver/CMP/offset sort cartoons.
7. SEG-Y file structure and trace header essentials.

## Key equations (introductory)

- Approximate 2D fold: $F \approx N / (2 \cdot \text{moveup})$.
- CMP spacing from receiver spacing: $\Delta x_{\text{CMP}} = \Delta x_{\text{receiver}} / 2$.
- Moveup for marine 2D: $\text{moveup} = \Delta x_{\text{shot}} / (2 \Delta x_{\text{CMP}})$.

## Source material

- Hill & Rüger (2020), *Illustrated Seismic Processing, Vol. 2*, Appendix A–B and Chapter 31.
- CGG ODT01 Data Analysis Part 1 & Part 2.
- Margrave (2006), *Methods of Seismic Data Processing*, Chapter 1.
- Vermeer (2012), *3D Seismic Survey Design*, Chapter 1 (2D symmetric sampling).
- SEG-Y rev 2.0 and SEG SPS rev 2.1 format standards.

## Next steps

- Draft detailed lecture notes in `lecture_notes/en/term01_lec01_introduction_to_seismic_processing.en.md`.
- Generate figures with self-contained Python scripts.
- Translate to Russian.
- Build slide outline and update PowerPoint.
