# Slide outline — Term 3, Lecture 1: Quality control of processing and introduction to 3D seismic data

## Slide 1 — Title
- Quality control of seismic processing and introduction to 3D seismic data
- Term 3, Lecture 1
- Figure: none

## Slide 2 — Learning objectives
- Distinguish input-data QC from processing-stage QC.
- List the main QC tools for each processing step (kinematics, noise attenuation, deconvolution/Q, demultiple).
- Explain how well ties and AVO checks anchor processing to geology.
- Describe the main 3D land geometries: template, salvo, swath.
- Compute fold in 3D and explain the role of binning and the unit cell.
- Define cross-spread gathers and OVT/COV panels.

## Slide 3 — Why this lecture matters
- After Term 1 the data are loaded, gained, and deconvolved; Term 2 covers imaging and noise removal.
- Each processing step can fail silently: the section may look fine while velocities, amplitudes, or wavelets are wrong.
- 3D acquisition is the default in modern exploration; 3D geometry decisions affect everything downstream.
- The interpreter and processor must work together — this is ИСО / WDS.

## Slide 4 — Two kinds of QC
- **Input QC** (Term 1, Lecture 2): geometry, first breaks, amplitude attributes, spectral attributes.
- **Processing QC**: verifying the output of each processing step.
- Rule: never trust a metric without looking at the data, and never trust the data without a metric.
- Figure: `term03_lec01_input_vs_processing_qc.png`

## Slide 5 — Geometry QC recap
- Overlay expected offset curves on shot gathers.
- LMO stacks: align direct arrivals / refractions to a chosen velocity.
- First-break-based QC: pick and compare with near-surface model predictions.
- Catches: wrong source/receiver positions, timing errors, near-surface anomalies.

## Slide 6 — Attribute analysis recap
- Amplitude attributes: RMS amplitude, amplitude in frequency bands, signal-to-microseism ratio.
- Correlation attributes: dominant frequency, bandwidth, signal-to-noise ratio.
- Spectral attributes: spectral energy, central frequency, peak frequency, bandwidth.
- Display as maps and histograms; look for stripes and outliers.
- Figure: `term03_lec01_attribute_maps.png`

## Slide 7 — Multi-attribute assessment
- A single attribute can be misleading (any attribute can lie).
- Combine attributes into an overall data-quality metric.
- Useful for ranking gathers, identifying bad traces, or monitoring a survey.
- Keep geology and acquisition effects separate.

## Slide 8 — QC of kinematic processing
- Stacking quality: horizon continuity, coherency, signal-to-noise ratio on stacks.
- Structural QC: time and depth horizon maps, cross-plots with well data.
- Residual NMO: check that gathers are flat after NMO correction.
- Bad moveout → wrong velocity, anisotropy, or residual statics.
- Figure: `term03_lec01_residual_nmo_qc.png`

## Slide 9 — Noise attenuation QC
- Amplitude attribute maps before and after denoising.
- Difference section: should contain noise, not signal.
- **Signal leakage check**: migrate the difference to see if lateral resolution is preserved.
- If signal leaked into the noise panel, the process is too aggressive.
- Figure: `term03_lec01_noise_attenuation_difference.png`

## Slide 10 — Q-compensation and deconvolution QC
- Vertical resolution: autocorrelation attributes, well-tie phase and wavelet shape.
- Lateral stability: maps of dominant frequency and bandwidth; FX slices.
- Compare extracted wavelets in different time windows and across the survey.
- Goal: consistent wavelet, improved resolution, no instability.
- Figure: `term03_lec01_wavelet_stability_map.png`

## Slide 11 — Demultiple QC
- Vertical velocity spectra before and after demultiple: residual multiple energy?
- Residual-moveout maps of suspected multiple arrivals.
- Model multiple traveltimes from well data and compare with the subtracted panel.
- Well-tie: do multiples still corrupt the synthetic-to-seismic match?

## Slide 12 — Interpretation-supervised processing (ИСО / WDS)
- Quantitative metrics help, but the interpreter must validate the result.
- Uses prior information: wells, geology, synthetic traces, AVO response.
- Modern trend: bring wells into processing as early as possible to set parameters and build velocity models (WDS).
- Figure: `term03_lec01_iso_workflow.png`

## Slide 13 — Seismic well tie
- Convert depth to two-way time with the sonic log; calibrate with checkshots.
- Build reflectivity from density and calibrated sonic logs; convolve with an estimated wavelet to make a synthetic seismogram.
- Extract a wavelet and compare synthetic to seismic at the well location.
- Metrics: correlation coefficient, phase rotation, wavelet shape, and bandwidth.
- Deterministic wavelet: from source signature, ghosts, bubble, and instrument response.
- Statistical wavelet: Roy-White frequency-domain method (noisy input-output, multiple coherence, error bars on the spectrum).
- Accuracy metrics from White (1997): PEP measures goodness-of-fit; NMSE measures true accuracy. Keep analysis bandwidth < ~0.5 of data bandwidth.
- Phase-error tolerances: <30° for correlation, <20° for AVO, <15° for zero-phasing/relative impedance, <10° for absolute-impedance inversion.
- For time-migrated data, the best match point is often slightly up-dip from the well. Repeat the tie after seismic conditioning.
- Figure: `term03_lec01_seismic_well_tie.png`

## Slide 14 — AVO analysis as QC
- Compare measured seismic amplitudes with theoretical AVO response.
- Shuey equation: $R(\theta) = R_0 + G \sin^2\theta + F \sin^2\theta \tan^2\theta$; two-term form $R(\theta) \approx R_0 + G \sin^2\theta$.
- Intercept $R_0$ vs gradient $G$ crossplot is a standard interpretation tool.
- Rüger (1996) HTI equation: $G(\phi) = G_\text{iso} + G_\text{aniso} \cos^2\phi$; extended to orthorhombic media.
- AVO check validates amplitude preservation, velocity model, and wavelet.
- Figure: `term03_lec01_avo_qc.png`

## Slide 15 — Part 1 summary
- Input QC: geometry, attributes, first breaks.
- Processing QC: kinematics, noise, Q/deconvolution, demultiple.
- ИСО / WDS ties processing to wells and interpretation through well ties and AVO.

## Slide 16 — Part 2: from 2D to 3D acquisition
- 2D: one source line, one receiver line, one midpoint line.
- 3D: source and receiver are distributed over an area → 5D prestack wavefield.
- Cannot densely sample all four spatial coordinates; 3D symmetric sampling: sample the two varying coordinates of each natural subset (minimal data set) well, sample the other two coarsely.
- Goal: dense, uniform illumination of the subsurface.
- Modern trends: full-azimuth, broadband, dense sampling, nodes, single-source/single-receiver.

## Slide 17 — Basic 3D geometry elements
- Source lines and receiver lines (or streamers).
- Line spacing, station spacing, maximum inline and crossline offsets.
- A **template**: a repeating source–receiver pattern.
- A **salvo**: a group of shots fired into a fixed receiver spread.
- A **swath**: a continuous strip of acquisition, often several templates side by side.
- Figure: `term03_lec01_3d_geometry_elements.png`

## Slide 18 — Unit cell
- The **unit cell** is the smallest repeating area of the geometry.
- It is determined by the two coarsest sampling intervals.
- Controls the spatial density of midpoints and offsets.
- Smaller unit cell → better spatial continuity, fewer migration artifacts.
- Figure: `term03_lec01_unit_cell.png`

## Slide 19 — Acquisition parameters and their influence
- Source/receiver interval: lateral sampling, alias-free wavenumber bandwidth.
- Line spacing: crossline fold and sampling.
- Maximum offset: depth of velocity control, NMO stretch, multiple discrimination.
- Minimum offset: shallow coverage, near-surface QC.
- Record length, sampling rate, source strength, receiver arrays.

## Slide 20 — Fold in 3D
- **Fold** = number of traces per CMP/bin.
- In 3D: fold varies in inline and crossline directions.
- Inline and crossline fold for a regular orthogonal geometry:

$$
M_i = \frac{\text{receiver spread length}}{2 \times \text{shot-line interval}}, \qquad M_c = \frac{\text{shot spread length}}{2 \times \text{receiver-line interval}}
$$

- Total fold $M = M_i \times M_c$ = midpoint area of one cross-spread / area of one unit cell.
- Alternative form:

$$
\text{fold} \approx \frac{N_x \, N_y}{2 \times \text{moveup}_x \times \text{moveup}_y}
$$

- Fold maps reveal holes, overlaps, and edge effects.
- Figure: `term03_lec01_3d_fold_map.png`

## Slide 21 — Cross-spread gathers
- **Cross-spread**: all traces from one source line and one receiver line.
- Natural 3D gather for many processing procedures (statics, interpolation, noise attenuation).
- Preserves the 2D shot/receiver character in the inline and crossline directions.
- Figure: `term03_lec01_cross_spread_gather.png`

## Slide 22 — OVT / COV panels
- **OVT (offset-vector tile)** = unit-cell-sized subarea of a cross-spread; all OVTs in a cross-spread have the same area as the unit cell.
- **COV (common-offset-vector) panel**: pseudo-COV gather made by tiling the same OVT from many cross-spreads.
- Preserves azimuth and offset distribution; each panel is approximately single-fold.
- Used for 3D regularization, migration, and AVO/azimuthal analysis.
- Figure: `term03_lec01_ovt_panel.png`

## Slide 23 — OVT construction in practice
- From input geometry, compute inline half-offset $h_x$ and crossline half-offset $h_y$ for every trace.
- Assign each trace to a midpoint bin and an offset-vector bin (bin size typically one unit cell).
- Each OVT panel is a single-fold 3D volume with a narrow range of offsets and azimuths.
- Reciprocal OVTs (opposite quadrants) are combined to honor reciprocity and reduce cross-spread edge effects.
- Figure: `term03_lec01_ovt_offset_distribution.png`

## Slide 24 — Grid binning
- Midpoints are assigned to a regular (inline, crossline) grid.
- **Bin size**: the lateral dimensions of the CMP cell.
- Trade-off: smaller bins → better resolution, but lower fold and more empty bins.
- Binning QC:
  - Fold uniformity across the survey.
  - Deviation of midpoints from bin center.
- Figure: `term03_lec01_binning_midpoint_distribution.png`

## Slide 25 — Summary
- Processing QC is a step-by-step validation: geometry, kinematics, noise, Q/deconvolution, demultiple.
- Interpretation-supervised processing (ИСО / WDS) uses well ties and AVO to anchor processing to geology.
- 3D acquisition samples a 5D prestack wavefield; geometry choices control illumination, fold, and sampling.
- Template / salvo / swath are building blocks; the unit cell fixes the basic repetition.
- Cross-spread and OVT/COV are key 3D sort orders; grid binning turns midpoints into processable bins.

## Slide 26 — Comprehension questions
- Why is a difference section the main QC tool for noise attenuation?
- What residual-NMO signature tells you that the stacking velocity is too low?
- Name two well-tie metrics and explain what each reveals. What is the difference between PEP and NMSE?
- How does the unit cell affect the spatial continuity of a 3D survey?
- What is the advantage of an OVT panel over a simple CMP gather?
- Why does fold vary in both inline and crossline directions in 3D?
- Explain how a mismatch between measured and theoretical AVO response can point to a processing problem.
- Why are reciprocal OVTs combined, and what does 3D symmetric sampling mean?
