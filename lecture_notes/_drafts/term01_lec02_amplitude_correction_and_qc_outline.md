# Term 1 Lecture 02 — Amplitude Corrections and Quality Control of Input Data

## Outline

### Learning objectives

After this lecture, students should be able to:

1. List the main physical effects that attenuate seismic amplitudes during wave propagation.
2. Distinguish between true/relative amplitude preservation and amplitude equalization for intermediate processing.
3. Explain the cause of spherical divergence and apply a simple time-dependent correction.
4. Describe deterministic amplitude equalization methods (normalization, AGC) and their appropriate use.
5. State the surface-consistent amplitude model and identify the four factors it separates.
6. Explain why input-data QC—especially geometry verification—is critical before any processing step.
7. Name common amplitude, correlation, and spectral attributes used in field-data QC.

### Prerequisites

- Seismic wave types and basic reflection ray paths (Term 1 Lecture 1).
- Source–receiver geometry and the CMP concept (Term 1 Lecture 1).
- Basic signal-processing ideas: trace, amplitude, RMS, Fourier spectrum (assumed from companion courses).

### 1. Introduction (5 min)

- What seismic processing is trying to recover: traveltimes *and* amplitudes.
- Why amplitude integrity matters: structural imaging, AVO/AVA, reservoir characterization, stratigraphic interpretation.
- Preview: this lecture is about making recorded amplitudes usable, not about final interpretation.

### 2. Physical amplitude effects during wave propagation (15–20 min)

- Wavefront spreading and energy conservation.
- Reflection and transmission at elastic boundaries (partitioning of energy).
- Mode conversion at elastic boundaries (P-to-S and S-to-P energy partitioning).
- Spherical divergence (geometric spreading).
- Absorption (anelastic attenuation) and scattering.
- Near-surface source and receiver effects: coupling, weathering, source strength variations.
- Practical note: absorption and scattering are often treated together because they are hard to separate with recorded data alone.
- Figure: ray diagram showing the main amplitude-loss mechanisms from source to receiver.

### 3. Two philosophies of amplitude processing (10 min)

- True amplitude / relative amplitude preserving processing: recover physically meaningful amplitudes for later AVO/interpretation.
- Amplitude equalization for intermediate steps: make data visible and processable; may distort true amplitudes intentionally.
- When each is appropriate.
- Key rule: never apply AGC or aggressive equalization before amplitude-sensitive analysis.

### 4. Spherical divergence correction (15–20 min)

- Energy spreads over a wavefront; energy ∝ 1/r², amplitude ∝ 1/r.
- General form of a divergence correction: multiply by t^n where n depends on the assumed wavefront geometry and dimensionality (commonly n = 1 or n = 2).
- Physics behind t²: in a constant-velocity medium the wavefront radius grows linearly with traveltime, so the wavefront area grows as t² and the energy density falls as 1/t²; amplitude therefore falls as 1/t in the absence of absorption, and the compensating gain grows as t.
- More realistic correction uses an approximate velocity function; exact correction is usually deferred to migration.
- Worked example: compute the divergence factor for a reflection at a given two-way time.
- Figure: uncorrected vs. corrected shot gather showing amplitude decay with time/offset.

### 5. Deterministic amplitude equalization (10–15 min)

- Amplitude normalization: scale each trace by its mean/RMS or maximum amplitude, mainly for display.
- Automatic gain control (AGC): apply a time-varying scale in a short sliding window.
- How AGC changes the waveform and why it destroys true amplitude relationships.
- Practical use cases: visualization, structural analysis, and kinematic processing (e.g., velocity picking and residual-statics estimation).
- Figure: same trace with and without AGC; comparison of amplitude envelopes.

### 6. Surface-consistent amplitude correction (15–20 min)

- Motivation: source and receiver coupling, near-surface conditions, and offset-dependent effects create amplitude variations that are not geology.
- Four-factor model: source component, receiver component, offset component, and structural (CMP) component.
- How trace amplitudes are measured: analysis window selection, frequency band, noise considerations.
- Effect of noise on amplitude estimates and how it can over-attenuate individual sources or receivers.
- Two-factor vs. four-factor models: stability vs. geological fidelity, AVO preservation.
- Mention that the Gauss–Seidel solution method will be covered in the next lecture (Lecture 3).
- Figure: synthetic CMP gather with source/receiver amplitude anomalies before and after surface-consistent correction.

### 7. Quality control of input data (10–15 min)

- Geometry checking: every trace must have the correct source, receiver, and midpoint positions; why this is critical before any processing step.
- Consequences of geometry errors: mis-stacking, wrong velocities, artifacts in time sections.
- Visual geometry QC:
  - Overlay expected offset curves on shot/receiver gathers using an approximation of the direct-wave arrival.
  - Linear-moveout (LMO) stacks to verify that arrivals align at the correct apparent velocity.
  - Figure: shot gather with predicted offset curves, LMO panel, and first-break residual plot.
- First-break-based geometry QC:
  - Predict first-break traveltimes from a near-surface model or direct-wave velocity.
  - Compare predicted and observed picks; systematic differences reveal geometry errors, timing problems, or near-surface anomalies.
- Attribute analysis for field-data QC:
  - amplitude attributes: mean/RMS amplitudes in analysis windows, frequency-band amplitudes, signal-to-microseism ratio;
  - correlation attributes: dominant frequency, spectral width, signal-to-noise ratio from autocorrelation/cross-correlation;
  - spectral attributes: spectral energy, central frequency, peak frequency, bandwidth.
- Statistical methods: histograms, maps, sorting by shot/receiver/offset/CMP to spot outliers.
- Figure: QC map of trace amplitudes by receiver index, with an outlier group highlighted.

### 8. Comprehension questions and discussion (10 min)

1. Why does AGC make a section easier to see but less suitable for AVO analysis?
2. List three physical effects that reduce seismic amplitude as the wave travels.
3. If a trace is scaled by its own RMS amplitude, what happens to the relative amplitudes of two reflections on that trace?
4. Why is geometry verification the first QC step before any processing step?
5. In a surface-consistent amplitude model, which factor would you expect to capture a wet patch near a receiver station?

### Figures to generate

1. `term01_lec02_amplitude_effects_ray_diagram.png` — ray diagram showing reflection/transmission, spreading, absorption, and near-surface effects.
2. `term01_lec02_spherical_divergence_correction.png` — uncorrected vs. corrected gather and amplitude-vs-time curves.
3. `term01_lec02_agc_example.png` — trace and envelope before/after AGC.
4. `term01_lec02_surface_consistent_amplitude.png` — synthetic gather with source/receiver anomalies before and after correction.
5. `term01_lec02_qc_geometry_first_breaks.png` — shot gather with predicted offset curves, LMO panel, and first-break residual plot.
6. `term01_lec02_qc_amplitude_map.png` — receiver-index amplitude map with outliers.

### Key equations to include

- Divergence relationship: amplitude ∝ 1/r, or energy ∝ 1/r².
- General form of a spherical-divergence correction: $G(t) = t^n$, where $n$ depends on wavefront geometry and convention (commonly $n = 1$ or $n = 2$).
- RMS amplitude definition used for normalization and for surface-consistent amplitude estimation.
- Surface-consistent amplitude model: $A_{ij} = s_i \, r_j \, h_k \, c_l$ (source, receiver, offset class, CMP).

### Derivation documents needed

- None required for the main equations; all can be explained conceptually in the lecture notes.

### Links to wiki concepts

- `wiki/concepts/amplitude_effects.md` — physical causes of amplitude attenuation.
- `wiki/concepts/spherical_divergence.md` — geometric spreading correction.
- `wiki/concepts/automatic_gain_control.md` — AGC and deterministic equalization.
- `wiki/concepts/surface_consistent_amplitude.md` — four-factor surface-consistent amplitude model.
- `wiki/concepts/seismic_data_qc.md` — input-data quality control attributes and methods.

### Sources to ingest / reference

- `papers/textbooks/Yilmaz - Seismic Data Analysis.pdf` — amplitude recovery and QC sections.
- `papers/textbooks/Steve J Hill - Introduction to Seismic Processing.pdf` — amplitude processing overview.
- `papers/general/ODT01A_DATA_ANALYSIS_PART1_v8.2.pptx` — geometry and data QC.
- `papers/signal_processing/metcas - SCAC.ppt.pdf` — surface-consistent amplitude correction.

### Timing estimate

| Section | Time |
|---|---|
| Introduction | 5 min |
| Physical amplitude effects | 15–20 min |
| Two philosophies | 10 min |
| Spherical divergence correction | 15–20 min |
| Deterministic equalization | 10–15 min |
| Surface-consistent amplitude correction | 15–20 min |
| Input-data QC | 10–15 min |
| Questions / discussion | 10 min |
| **Total** | **90–105 min** |

Buffer: drop one worked example or shorten the equalization section if the class needs more time on divergence.
