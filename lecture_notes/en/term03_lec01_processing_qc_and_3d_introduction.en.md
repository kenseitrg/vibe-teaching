---
title: Term 3 Lecture 01 — Quality Control of Seismic Processing and Introduction to 3D Seismic Data
author: Seismic Data Processing Course
---

# Quality Control of Seismic Processing and Introduction to 3D Seismic Data

## Why this lecture matters

By the end of Term 2 a seismic processing project has usually passed through geometry loading, amplitude recovery, deconvolution, noise attenuation, velocity analysis, NMO and stack, demultiple, and migration. Every one of those steps can produce a plausible-looking section while quietly degrading the very information the interpreter needs. Velocity analysis may leave residual moveout; noise attenuation may remove signal; deconvolution may over-boost high frequencies; demultiple may leave multiple energy at depth. The only way to catch these problems is systematic quality control at each stage.

At the same time, modern exploration relies on 3D seismic data. The jump from 2D to 3D is not just "more lines"; it changes the way sources, receivers, and bins are arranged, the sort orders that are natural for processing, and the way fold and illumination are computed. A processor who understands 3D geometry can diagnose acquisition problems, design better binning, and choose appropriate gathers for velocity analysis, interpolation, and imaging.

This lecture has two parts:

1. **Quality control of seismic processing** — the step-by-step checks that keep a processing project honest, and the modern interpretation-supervised framework (ИСО / WDS) that ties processing to wells and geology.
2. **Introduction to 3D seismic data** — the basic building blocks of 3D acquisition geometry, the unit cell, fold, cross-spreads, OVT/COV panels, and binning.

## Part 1 — Quality control of seismic processing

### 1.1 Two kinds of QC

It is useful to split quality control into two families.

- **Input-data QC** (the subject of Term 1, Lecture 2) verifies the raw material before any processing begins. It includes geometry checks, first-break analysis, amplitude and spectral attribute analysis, and the statistical separation of acquisition-related patterns from geological ones.
- **Processing-stage QC** verifies the output of each processing step. It asks: did the step do what we wanted, and did it avoid unwanted side effects?

Both kinds of QC share a rule: **never trust a single metric without looking at the data, and never trust a visual impression without a metric.** A beautiful section can hide a bad velocity field; a low correlation coefficient can be caused by a single polarity flip. The best practice is to use several independent views.

![Figure: `figures/term03_lec01/term03_lec01_input_vs_processing_qc.png` — A schematic processing flow with input QC at the start and processing-stage QC after each major step.](./figures/term03_lec01/term03_lec01_input_vs_processing_qc.png)

*Figure 1: Input QC checks the raw data; processing QC checks the result of each step. The two overlap because some attributes are recomputed after each stage.*

### 1.2 Geometry QC recap

Geometry errors are the most dangerous problems because they corrupt everything downstream. A trace assigned to the wrong source or receiver position will land in the wrong CMP gather, so its NMO correction will be wrong, its stack will be misaligned, and its amplitude will be out of place. The main tools are:

- **Offset-curve overlays.** On a shot gather, plot the expected arrival time of the direct wave or first refraction as a function of offset using an approximate near-surface velocity. Mis-positioned traces will not lie on the predicted curve.
- **Linear-moveout (LMO) stacks.** Apply a linear moveout with a chosen velocity and stack the data. If the chosen velocity matches the direct arrival or refraction, the event aligns horizontally; geometry or timing errors show up as misalignment.
- **First-break-based QC.** Predict first-break traveltimes from a near-surface model or a direct-wave velocity, pick the actual first breaks, and compare predicted and observed picks. Systematic residuals reveal geometry errors, timing problems, or near-surface anomalies.

These methods are usually revisited after statics correction, because residual statics can also produce first-break misalignment.

### 1.3 Attribute analysis recap

Attributes turn a volume of traces into scalars that can be mapped, histogrammed, and compared. They are essential for spotting non-stationarity, near-surface and acquisition anomalies.

**Amplitude attributes**

- Mean or RMS amplitude in an analysis window. RMS is usually preferred because it is less sensitive to a single extreme sample.
- Amplitude in frequency sub-bands.
- Signal-to-microseism ratio.

**Correlation attributes**

- Dominant frequency.
- Spectral width or bandwidth.
- Signal-to-noise ratio estimated from autocorrelation or cross-correlation.

**Spectral attributes**

- Spectral energy.
- Central (mean) frequency.
- Peak frequency.
- Spectral bandwidth.

These attributes are computed in windows, sorted by source, receiver, offset, CMP, and midpoint coordinates, and displayed as maps and histograms. Common patterns include vertical stripes (source-related), horizontal stripes (receiver-related), and diagonal stripes (geology or offset-dependent effects). Fold maps are another attribute: they show holes, overlaps, and low-fold areas that explain noise or amplitude variations.

### 1.4 Multi-attribute assessment

No single attribute is reliable enough to judge data quality by itself. A trace can have normal amplitude but anomalous frequency; a gather can have good signal-to-noise ratio but poor flatness. Modern QC therefore combines several attributes into an overall quality metric.

The simplest combination is a weighted average of normalized attributes. More robust methods use percentile ranks or machine-learning classifiers trained on examples of good and bad traces. The key is to keep the decision transparent: the processor must know which attributes drove the metric and whether they are measuring acquisition noise, geology, or processing artifacts.

A multi-attribute assessment is especially useful for:

- ranking gathers by quality,
- identifying bad traces to flag,
- monitoring data quality across a survey,
- deciding where a processing step has improved or degraded the data.

### 1.5 QC of kinematic processing

Kinematic processing includes velocity analysis, NMO correction, stacking and imaging. Its goal is to align reflections in time so that stacking reinforces signal. The main QC tools are:

- **Stacking quality.** Inspect the stacked section for horizon continuity, coherency, and signal-to-noise ratio. A good stack should make continuous reflectors easier to follow, not introduce artificial discontinuities.
- **Structural QC.** Horizon maps in time and depth should be geologically plausible. Cross-plots of horizon time or depth against well data reveal systematic shifts that point to velocity errors or residual statics.
- **Residual NMO.** After NMO correction, gathers should be flat. Residual curvature means the stacking velocity is wrong, anisotropy is ignored, or residual statics remain. A small residual moveout can be tolerated before stack, but it must be understood before AVO or prestack migration.

### 1.6 QC of noise attenuation

Noise attenuation removes unwanted energy. The danger is that it also removes signal. The standard QC procedure is:

- Compare amplitude attribute maps before and after denoising. The average amplitude should drop where noise was removed, but geological amplitude trends should remain.
- Inspect the **difference section** (input minus output). It should contain noise, not coherent signal. If reflectors are visible in the difference, signal has leaked into the noise panel.
- Check **lateral resolution** by migrating the difference section. Lateral resolution is preserved only if the difference has no focused energy after migration.
- Compare vertical and horizontal slices in the same time/depth windows before and after the process.

### 1.7 QC of Q-compensation and deconvolution

Q-compensation and deconvolution reshape the wavelet and restore high frequencies. Their QC focuses on resolution and stability:

- **Vertical resolution.** Autocorrelation attributes, well-tie correlation, and visual inspection of close reflectors show whether the wavelet has been compressed.
- **Lateral stability.** Maps of dominant frequency and bandwidth should be smooth except where geology changes. FX slices show how the spectrum varies with inline and crossline position.
- **Wavelet shape.** Extract wavelets in different time windows and across the survey. A stable process gives similar wavelets everywhere; an unstable process gives wavelets that vary from trace to trace.
- **Phase and well tie.** A successful Q-compensation and deconvolution should leave the seismic data with a wavelet that matches the synthetic seismogram in phase and timing.

### 1.8 QC of demultiple

Multiples are reflected energy that has bounced more than once in the subsurface. They are not removed by ordinary NMO and stack. Demultiple QC includes:

- **Vertical velocity spectra before and after demultiple.** Look for residual multiple energy that has a different moveout from primaries.
- **Residual-moveout maps.** A residual moveout on a multiple model indicates incomplete removal.
- **Multiple modeling from well data.** Given acoustic logs, compute the traveltimes of possible multiple-generating interfaces and compare them with the subtracted panel. If the predicted multiple arrival time matches the energy removed by the process, the demultiple is plausible.
- **Well tie.** Multiples that are still present in the seismic data will reduce the correlation between synthetic and seismic traces.

### 1.9 Interpretation-supervised processing (ИСО / WDS)

All the QC steps above become more powerful when the interpreter is involved from the beginning. In Russian practice this is called **ИСО** (интерпретационное сопровождение обработки, interpretation-supervised processing); internationally the related concept is often called **WDS** (well-driven seismic) or simply interpreter-guided QC.

The idea is not to replace the processor with the interpreter, but to add geological and well constraints at every stage:

- Wells provide checkshots and sonic logs that validate the velocity model.
- Synthetic seismograms tie the seismic wavelet to log reflectivity.
- AVO response checks whether the amplitude-versus-offset behavior matches rock-physics predictions.
- Geological maps and cross-sections constrain structural QC.

The main instruments of this framework are the seismic well tie and AVO analysis, which are described next.

### 1.10 Seismic well tie

A seismic well tie links the depth domain of well logs to the time domain of seismic data. The sonic log converts depth to two-way time by integrating slowness:

$$
t(z) = 2 \int_0^z \frac{d\zeta}{v(\zeta)}
$$

A checkshot survey provides independent time-depth pairs and is used to correct the sonic log for drift, cycle skipping, or borehole-trajectory errors. The steps are:

1. **Compute reflectivity from logs.** Use the calibrated sonic log to convert depth to two-way time and the density log to compute acoustic impedance. The normal-incidence reflection coefficient is

$$
R(t) = \frac{Z(t+\Delta t) - Z(t)}{Z(t+\Delta t) + Z(t)}
$$

2. **Build a wavelet.** The wavelet can be deterministic (derived from the known source signature, ghost, bubble, and instrument response) or statistical (estimated from the seismic data itself). The Roy-White method estimates the wavelet in the frequency domain by treating the problem as a noisy input-output system: both the log-derived reflectivity and the seismic trace contain noise, so ordinary least-squares estimates are biased. Walden and White (1998) use multiple coherence analysis to estimate the output signal-to-noise ratio at each frequency and then estimate an unbiased frequency-response function, producing error bars on the wavelet spectrum.
3. **Convolve reflectivity with wavelet** to produce a synthetic seismogram.
4. **Compare synthetic and seismic** at the well location and estimate the time shift, phase rotation, and correlation coefficient. 

**Metrics of a good tie**

- **Correlation coefficient.** High correlation (typically above 0.7) means the synthetic and seismic match, but it is a measure of goodness-of-fit, not necessarily accuracy.
- **Phase rotation.** After deconvolution the wavelet should be near zero phase; a large residual phase rotation suggests the wavelet is wrong or the process is unbalanced. White (1997) gives typical phase-error tolerances: less than 30° for simple correlation, less than 20° for AVO modelling, less than 15° for zero-phasing or relative impedance, and less than 10° for absolute-impedance inversion.
- **Wavelet shape and bandwidth.** A stable, compact wavelet is better than a long, noisy one. The Roy-White method trades wavelet length against bandwidth: a short wavelet is smooth but may not capture the phase; a wide bandwidth gives a better phase estimate but requires a longer wavelet and can become unstable in noise. The analysis bandwidth should be kept well below the data bandwidth (the ratio of wavelet length to data segment duration should be less than about 0.5).
- **Accuracy measures.** Predictability (PEP = 1 − relative energy of residuals) measures fit; the normalized mean square error (NMSE = error energy in the wavelet / wavelet energy) measures accuracy. Error bars on the amplitude and phase spectra allow wavelets from different wells or time windows to be compared and combined.
- **Quality of the extracted wavelet.** A well tie is not just about maximizing correlation; it is about extracting a wavelet that is geologically reasonable and can be used across the survey. Well-tie should be repeated after each processing step.

### 1.11 AVO analysis as a QC tool

Amplitude-versus-offset (AVO) analysis checks that the seismic amplitudes behave as rock physics predicts. It is therefore a powerful QC tool after amplitude processing, wavelet estimation, and velocity analysis.

The simplest description is the **Shuey equation**, which gives the reflection amplitude as a function of angle:

$$
R(\theta) = R_0 + G \sin^2\theta + F \sin^2\theta \tan^2\theta
$$

where $R_0$ is the normal-incidence reflection coefficient, $G$ is the AVO gradient, $F$ is the higher-order term, and $\theta$ is the incidence angle. In practice the angle is often replaced by offset squared; the two-term approximation $R(\theta) \approx R_0 + G \sin^2\theta$ is the basis of the intercept-versus-gradient crossplot used in AVO interpretation.

For anisotropic media, the **Rüger equation** adds azimuthal dependence. In a horizontally transverse isotropic (HTI) medium — a simple model for a set of parallel vertical fractures — the AVO gradient depends on the azimuth $\phi$ relative to the fracture direction:

$$
G(\phi) = G_\text{iso} + G_\text{aniso} \cos^2\phi
$$

so the reflection coefficient becomes

$$
R(\theta, \phi) = R_0 + \left(G_\text{iso} + G_\text{aniso} \cos^2\phi\right) \sin^2\theta
$$

The azimuthal variation can be inverted for the symmetry-plane directions and for a combination of fracture parameters. Rüger (1996) also extends the result to orthorhombic media, which are more realistic for fractured reservoirs. The key QC idea is the same: the measured amplitude trend with offset and azimuth should match the theoretical trend computed from well logs or a rock-physics model.

If the measured AVO response is wrong, the cause may be:

- incorrect amplitude processing (e.g., AGC, residual source/receiver coupling),
- incorrect wavelet or phase,
- incorrect velocity model or residual moveout,
- unresolved multiples,
- wrong rock-physics model.

## Part 2 — Introduction to 3D seismic data

### 2.1 From 2D to 3D acquisition

In 2D acquisition the sources and receivers lie along a single line, and the data are organized by one midpoint coordinate and one offset. A 2D line therefore samples a 3D wavefield: time $t$, source coordinate $x_s$, and receiver coordinate $x_r$.

In 3D acquisition the sources and receivers are distributed over a surface area. The prestack wavefield is now 5D: time $t$, two source coordinates $(x_s, y_s)$, and two receiver coordinates $(x_r, y_r)$. It is impossible to sample all four spatial coordinates densely; 3D geometry design is the art of choosing which coordinates to sample well and which to leave coarse, consistent with the survey objectives and budget. This is the idea of **3D symmetric sampling**: sample the two spatial coordinates that vary within each natural 3D subset (the minimal data set) adequately, while the other two coordinates may be sampled more coarsely.

3D data are superior to 2D data for several reasons:

- **True 3D illumination.** The subsurface is sampled from many azimuths and offsets, not just one line.
- **Better noise attenuation.** Random noise is suppressed by stacking in two spatial dimensions.
- **Better imaging.** Migration can position diffractors and dipping events correctly in 3D space.
- **AVO and azimuthal analysis.** The full range of offsets and azimuths enables AVO and fracture characterization.

Modern trends push toward denser, wider, and more uniform sampling: full-azimuth surveys, broadband sources, single-source and single-receiver acquisition, and ocean-bottom nodes (OBN).

### 2.2 Basic 3D geometry elements

A 3D land or transition-zone survey is built from source lines and receiver lines. A marine survey is built from source sail lines and streamers. The key terms are:

- **Source line:** the line along which sources are placed or fired.
- **Receiver line:** the line along which receivers are deployed.
- **Inline direction:** the direction parallel to the source or receiver lines, depending on convention; usually the long axis of the survey.
- **Crossline direction:** the direction perpendicular to the inline direction.
- **Template:** a repeating source–receiver pattern that is moved across the survey.
- **Salvo:** a group of shots fired into a fixed receiver spread, common in some marine or node surveys.
- **Swath:** a continuous strip of acquisition, often several templates side by side, acquired before moving to the next strip.

![Figure: `figures/term03_lec01/term03_lec01_3d_geometry_elements.png` — Source lines, receiver lines, template, salvo, and swath in a land 3D survey.](./figures/term03_lec01/term03_lec01_3d_geometry_elements.png)

*Figure 2: A 3D land survey is built from source and receiver lines. Templates, salvos, and swaths are the repeating units used to cover the area.*

### 2.3 The unit cell

The **unit cell** is the smallest repeating area of the geometry. It is determined by the two coarsest sampling intervals, usually the source-line spacing and the receiver-line spacing. All midpoints and offsets in the unit cell repeat in the neighboring cells.

The unit cell controls the spatial density of the geometry:

- A small unit cell gives dense, continuous midpoint coverage and fewer migration artifacts.
- A large unit cell gives sparse coverage and may produce aliasing or acquisition footprints in the final image.
- The shape of the unit cell (its aspect ratio) matters: a square unit cell is usually preferred for symmetric sampling.

For an orthogonal geometry with source line spacing $S$ and receiver line spacing $R$, the unit cell area is approximately $S \times R$. The midpoint sampling inside the cell depends on the source and receiver station intervals.

![Figure: `figures/term03_lec01/term03_lec01_unit_cell.png` — Source and receiver positions and the repeating unit cell of an orthogonal 3D geometry.](./figures/term03_lec01/term03_lec01_unit_cell.png)

*Figure 3: The unit cell is the smallest repeating area of the geometry. Its size and shape control the sampling of the 5D wavefield.*

### 2.4 Acquisition parameters and their influence

The parameters of a 3D survey interact with each other. A change in one parameter usually forces a change in another. The most important parameters are:

| Parameter | Effect |
|-----------|--------|
| Source interval | Inline midpoint sampling; alias-free wavenumber bandwidth. |
| Receiver interval | Inline midpoint sampling; aliasing of steep dips and noise. |
| Source-line spacing | Crossline midpoint sampling and fold. |
| Receiver-line spacing | Crossline midpoint sampling and fold. |
| Maximum inline offset | Depth of velocity control, NMO stretch, multiple discrimination. |
| Maximum crossline offset | Crossline illumination and AVO/azimuth coverage. |
| Minimum offset | Shallowest coverage and near-surface QC. |
| Record length | Maximum imaging depth. |
| Sampling rate | Temporal resolution and alias-free frequency. |
| Source strength / receiver arrays | Signal-to-noise ratio and noise attenuation. |

A good survey design balances these parameters against the geological targets. For example, deep targets need large offsets for velocity control; shallow targets need small minimum offsets and dense sampling.

### 2.5 Fold in 3D

**Fold** is the number of traces that fall into a CMP bin. In 2D, fold varies mainly along the line. In 3D, fold varies in both inline and crossline directions, and it is sensitive to feathering, skipped lines, and edge effects.

For a regular orthogonal land geometry, the total fold $M$ can be estimated as the product of inline fold $M_i$ and crossline fold $M_c$:

$$
M_i = \frac{\text{receiver spread length}}{2 \times \text{shot-line interval}}, \qquad M_c = \frac{\text{shot spread length}}{2 \times \text{receiver-line interval}}
$$

so that

$$
M = M_i \times M_c = \frac{\text{midpoint area of one cross-spread}}{\text{area of one unit cell}}
$$

Equivalently, if $N_x$ and $N_y$ are the number of active receiver groups in the inline and crossline directions and $\text{moveup}_x$ and $\text{moveup}_y$ are the number of new bin rows/columns added per shot,

$$
\text{fold} \approx \frac{N_x \, N_y}{2 \times \text{moveup}_x \times \text{moveup}_y}
$$

The factor of 2 appears because each shot contributes offsets on both sides of the source in the ideal case. In traditional marine streamer acquisition, crossline fold is usually one, so total fold equals inline fold.

Fold maps are a basic QC tool. A uniform fold is desirable, but it is rarely perfect in practice because of:

- run-in and run-out at the edges of the survey,
- cable feather in marine data,
- skipped shots or receivers,
- irregular terrain or obstructions.

### 2.6 Cross-spread gathers

A **cross-spread gather** is the set of all traces recorded from one source line into one receiver line. It is a natural 3D gather because it preserves the 2D shot/receiver character in both the inline and crossline directions.

Cross-spreads are useful for:

- 3D noise attenuation,
- 3D interpolation and regularization,

The cross-spread is one example of a **minimal data set** — a subset of the 5D wavefield that is continuous and can be processed independently.

![Figure: `figures/term03_lec01/term03_lec01_cross_spread_gather.png` — A cross-spread gather: one source line and one receiver line. The traces form a 2D grid of source and receiver positions.](./figures/term03_lec01/term03_lec01_cross_spread_gather.png)

*Figure 4: A cross-spread gather contains all traces from one source line into one receiver line. It is a natural 3D processing unit.*

### 2.7 OVT / COV panels

An **offset-vector tile (OVT)**, also called a **common-offset-vector (COV) panel**, is a group of traces with similar inline and crossline offset components. In orthogonal geometry, an OVT is a unit-cell-sized subarea of a cross-spread. A pseudo-COV gather is built by tiling the same OVT from many adjacent cross-spreads; the result is an approximately single-fold 3D volume that covers the whole survey area.

The construction is:

1. For each trace, compute the inline half-offset $h_x$ and the crossline half-offset $h_y$ from the source and receiver coordinates.
2. Assign each trace to a midpoint bin and an offset-vector bin. The bin size is typically one unit cell.
3. Collect all traces with the same offset-vector bin into a single panel.

Each OVT panel is approximately a single-fold 3D volume with a narrow range of offsets and azimuths. The panels are useful for:

- 3D regularization and interpolation,
- prestack migration without mixing offsets and azimuths,
- AVO and azimuthal (AVAz) analysis,
- quality control of offset and azimuth distribution.

Because reciprocity requires that source and receiver offsets be treated symmetrically, **reciprocal OVTs** (positive and negative offset vectors in opposite quadrants) can be combined and processed in pairs. Combining reciprocal OVTs reduces the edge effects of individual panels and improves spatial continuity, but limits azimuth distribution.

![Figure: `figures/term03_lec01/term03_lec01_ovt_panel.png` — An OVT/COV panel: traces with a narrow range of inline and crossline offsets.](./figures/term03_lec01/term03_lec01_ovt_panel.png)

*Figure 5: An OVT panel is a single-fold 3D volume with a narrow range of offset vectors. It preserves azimuthal information.*

### 2.8 Offset and midpoint coverage for OVTs

The offset coverage of an OVT panel depends on how the offset-vector bins are chosen. A common choice is to divide the full offset range into rectangular bins in $(h_x, h_y)$ space. The midpoint coverage is the set of midpoint bins that contain at least one trace in the chosen offset-vector bin.

For a regular orthogonal geometry, the inline offset $h_x$ and crossline offset $h_y$ of a trace are

$$
h_x = \frac{x_r - x_s}{2}, \qquad h_y = \frac{y_r - y_s}{2}
$$

where $(x_s, y_s)$ and $(x_r, y_r)$ are the source and receiver coordinates. The midpoint coordinates are

$$
x_m = \frac{x_s + x_r}{2}, \qquad y_m = \frac{y_s + y_r}{2}
$$

The offset-vector bin limits and the midpoint bin size determine how many traces fall into each OVT panel. Panels with small offset-vector bins have fewer traces but better azimuth preservation; panels with large bins have more traces but mix azimuths.

### 2.9 Grid binning

Grid binning is the step that assigns each trace to a regular (inline, crossline) CMP bin. The bin size is a design choice:

- A small bin size gives better lateral resolution but lower fold and more empty bins.
- A large bin size gives higher fold and more uniform statistics but worse resolution.

Binning QC checks:

- **Fold uniformity.** The fold map should be as uniform as possible, with no holes or spikes.
- **Midpoint deviation from bin center.** The distance between the trace midpoint and the bin center should be small. Large deviations mean the bin is not representative of the trace positions.
- **Offset and azimuth distribution.** Each bin should contain a representative range of offsets and azimuths for AVO and stack response.

![Figure: `figures/term03_lec01/term03_lec01_binning_midpoint_distribution.png` — Midpoints scattered within CMP bins; the bin center is marked. Fold and midpoint deviation are the main binning QC metrics.](./figures/term03_lec01/term03_lec01_binning_midpoint_distribution.png)

*Figure 6: Binning assigns midpoints to regular cells. QC checks fold uniformity and how far midpoints are from the bin centers.*

## Summary

- Seismic processing is a chain of steps, and each step needs its own QC.
- Geometry QC, attribute analysis, and multi-attribute assessment are the foundation.
- Kinematic QC checks flat gathers, stack quality, and structural maps.
- Noise-attenuation QC relies on difference sections and preservation of lateral resolution.
- Q-compensation and deconvolution QC checks vertical resolution, lateral wavelet stability, and well ties.
- Demultiple QC uses velocity spectra, residual moveout, and multiple modeling from wells.
- Interpretation-supervised processing (ИСО / WDS) brings wells, AVO, and geology into the loop.
- 3D acquisition samples a 5D prestack wavefield. Geometry choices control illumination, fold, and sampling.
- Template, salvo, and swath are the repeating building blocks; the unit cell controls the basic spatial repetition.
- Cross-spread gathers and OVT/COV panels are the natural 3D sort orders for processing and imaging.
- Grid binning turns scattered midpoints into regular CMP bins; fold uniformity and midpoint deviation are the main QC metrics.

## Suggested reading

- Vermeer, G. J. O. (2012). *3D Seismic Survey Design*, 2nd ed. SEG Geophysical References Series No. 12, Chapter 2.
- Hill & Rüger (2020). *Illustrated Seismic Processing, Vol. 2*, Appendix A — geometry and gather definitions.
- CGG ODT01 Data Analysis Part 2 — 2D/3D geometry, sorts, and fold.
- White, R. E. (1997). "The accuracy of well ties: practical procedures and examples." SEG Annual Meeting Expanded Abstracts / Geophysical Prospecting — accuracy metrics and practical well-tie QC.
- Walden, A. T., & White, R. E. (1998). "Seismic wavelet estimation: a frequency domain solution to a geophysical noisy input-output problem." IEEE Transactions on Geoscience and Remote Sensing — the Roy-White frequency-domain wavelet estimation method.
- Carvajal, C., Fernandez, J., & Aristimuno, J. (2023). "Well tie tutorial and its importance in seismic interpretation and inversion." GeoConvention 2023 — practical quantitative well-tie workflow.
- Shuey, R. T. (1985). "A simplification of the Zoeppritz equations." *Geophysics* — AVO approximation.
- Rüger, A. (1996). "Variation of P-wave reflectivity with offset and azimuth in anisotropic media." SEG Technical Program Expanded Abstracts — anisotropic AVO and AVAz.

## Comprehension questions

1. Why do we need to compare migrated data to QC noise attenuation?
2. What residual-NMO signature tells you that the stacking velocity is too low?
3. Name two well-tie metrics and explain what each reveals.
4. How does the unit cell size affect the spatial continuity of a 3D survey?
5. What is the advantage of an OVT panel over a simple CMP gather?
6. Explain how a mismatch between measured and theoretical AVO response can point to a processing problem.
7. Why is binning QC important before stacking or migration?