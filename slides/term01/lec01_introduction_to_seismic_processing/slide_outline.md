# Slide outline: Term 1 Lecture 1 — Introduction to seismic data processing

## Slide 1 — Title
- Title: Introduction to seismic data processing
- Subtitle: Term 1, Lecture 1

## Slide 2 — Learning objectives
- List 7 learning objectives from the lecture notes.

## Slide 3 — Seismic processing in the exploration workflow
- Geological exploration lifecycle: Study of Geology → Field Acquisition → Seismic Processing → Interpretation → Geological Modeling → Drilling.
- Seismic data is one input among wells, geology, and a priori information.
- Figure: `term01_lec01_exploration_workflow.png`

## Slide 4 — Course structure
- Term 1: Foundations (formats, geometry, statics, velocities, deconvolution).
- Term 2: Intermediate methods (absorption, FK/Radon, multiples, imaging).
- Term 3: 3D and modern techniques (geometry, denoise, regularization, QC, well-driven).
- Practical sessions: industry software + parameter choice.
- Updated Term 1 to 8 lectures: single-channel filtering and deconvolution split into two lectures.

## Slide 5 — What we want to recover: the geological signal
- Ideal reflectivity series → band-limited wavelet → recorded trace.
- Processing goal: remove/compensate non-geological effects; prepare data for interpretation.
- Figure: `term01_lec01_idealized_vs_recorded_trace.png`

## Slide 6 — What contaminates the record: acquisition factors
- Source/receiver positions, source signature, arrays, instrument response, sampling.
- Figure: `term01_lec01_distortions_overview.png` (left + top-right icons)

## Slide 7 — What contaminates the record: wave propagation
- Geometric spreading, absorption, transmission losses, multiples, refractions, surface waves, mode conversion, anisotropy.
- Signal vs noise depends on the task.
- Figure: `term01_lec01_distortions_overview.png` (bottom-right icons)

## Slide 8 — Kinematic vs dynamic problems
- Kinematic: place energy at correct time and position.
- Dynamic: recover true amplitudes and wavelet shape.
- Explain verbally; no figure.

## Slide 9 — Main processing flow: overview
- Four phases: Preprocessing → Kinematic → Dynamic → Imaging.
- Phases 2 and 3 iterate.
- Figure: `term01_lec01_processing_flow.png` (copied from slides/raw/processin_flow_modern.png)

## Slide 10 — Phase 1: Preprocessing
- Data loading and format conversion.
- Geometry assignment and QC.
- Field statics and brute stack.

## Slide 11 — Phase 2: Kinematic processing
- Static corrections.
- Velocity analysis and NMO.
- Velocity model building.

## Slide 12 — Phase 3: Dynamic processing
- Noise attenuation.
- Demultiple.
- Deconvolution, amplitude correction, Q-compensation.
- Regularization/interpolation.

## Slide 13 — Phase 4: Imaging
- Migration.
- Post-migration conditioning.

## Slide 14 — Limitations and challenges
- Wavelength limits resolution.
- Acquisition geometry limits illumination and causes aliasing.
- Non-uniqueness of inverse problems.
- Data volume and computational cost.
- Signal-to-noise ratio constraints.

## Slide 15 — 2D acquisition: geometry
- End-on geometry: source, receivers, midpoints, fold build-up.
- Parameters: source interval, receiver interval, min/max offset, CMP spacing, fold.
- Figure: `term01_lec01_2d_acquisition_geometry.png`

## Slide 16 — 2D acquisition: environments and sources
- Land: dynamite, vibroseis, geophone arrays.
- Marine: air-gun arrays, streamers, OBC.
- Transition zone.

## Slide 17 — CMP method
- Record same subsurface point with many offsets.
- Benefits: velocity estimation, S/N improvement, multiple discrimination.
- Figure: `term01_lec01_cmp_gather_stack.png` (raw gather + NMO-corrected gather with stack)

## Slide 18 — Fold formula (worked example)
- Δx_CMP = Δx_rec / 2.
- moveup = Δx_shot / Δx_rec.
- F ≈ N_channels / (2 × moveup).
- Example: 240 channels, 12.5 m receiver interval, 25 m shot interval → CMP=6.25 m, moveup=2, fold=60.

## Slide 19 — Data sorts
- Shot gather, receiver gather, CMP gather, common-offset gather.
- Figure: `term01_lec01_data_sorts.png` (source-receiver plane schematic from slides/raw/shot-receiver-plane.png)

## Slide 20 — Field data formats
- SEG-D: raw field records.
- SEG-Y: trace exchange format.
- SPS, UKOOA P1/90: geometry files.
- Figures: `term01_lec01_segy_structure.png` (from slides/raw/segy_headers.png), `term01_lec01_segd_structure.png` (from slides/raw/segd_headers.png)

## Slide 21 — Why geometry assignment matters
- Every trace needs source/receiver coordinates, offset, CMP.
- SPS/UKOOA geometry merged with SEG-Y trace data.
- One wrong byte can misposition traces.

## Slide 22 — Summary
- Processing goal: recover geology from raw records.
- Kinematic vs dynamic tasks.
- Four processing phases.
- CMP method and fold.
- Data sorts and formats.

## Slide 23 — Comprehension questions
- List 5 questions from lecture notes.

## Slide 24 — References
- Hill & Rüger (2020), CGG ODT01, Margrave (2006), Vermeer (2012), SEG-Y rev 2.0, SPS rev 2.1.
