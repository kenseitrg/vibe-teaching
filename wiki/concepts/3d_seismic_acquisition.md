---
title: 3D seismic acquisition
status: draft
sources:
  - vermeer_2012_3d_seismic_survey_design
  - hill_ruger_2020_illustrated_seismic_processing_preimaging
  - cgg_odt01_data_analysis_part2
  - seg_sps_format_rev21
tags: [3D, acquisition, geometry, template, salvo, swath, unit-cell, fold, offset, azimuth, symmetric-sampling, spatial-continuity]
---

# 3D seismic acquisition

3D seismic acquisition records sources and receivers over a surface area rather than along a single line. It samples a **5D prestack wavefield**: time $t$, two source coordinates $(x_s, y_s)$, and two receiver coordinates $(x_r, y_r)$. Because it is impossible to sample all four spatial coordinates densely, 3D geometry design is the art of choosing which coordinates to sample well and which to leave coarse, consistent with the survey objectives and budget.

## From 2D to 3D

A 2D line samples a 3D wavefield: time $t$, source coordinate $x_s$, and receiver coordinate $x_r$. A 3D survey samples a 5D wavefield: time $t$, source coordinates $(x_s, y_s)$, and receiver coordinates $(x_r, y_r)$. The two extra spatial dimensions make 3D acquisition both more powerful and more difficult to design.

The 5D wavefield can also be described in midpoint/offset coordinates $(x_m, y_m, h_x, h_y)$. The **offset vector** $(h_x, h_y)$ describes the magnitude and azimuth of the source-receiver offset; it is a key variable in 3D sorting and analysis.

## Advantages of 3D data

- **True 3D illumination.** The subsurface is sampled from many azimuths and offsets, not just one line.
- **Better noise attenuation.** Random noise is suppressed by stacking in two spatial dimensions.
- **Better imaging.** Migration can position diffractors and dipping events correctly in 3D space.
- **AVO and azimuthal analysis.** The full range of offsets and azimuths enables AVO and AVAz (amplitude versus azimuth) studies for lithology and fracture characterization.

## Classes of 3D geometry

Vermeer's framework divides 3D geometries into two main classes (Vermeer, 2012, §2.2):

### Areal geometries

In **areal geometry**, the receivers listening to each shot occupy a dense areal grid, while the shots are sampled on a coarse grid (or vice versa). The basic subsets are 3D common-shot gathers or 3D common-receiver gathers. Full areal sampling is expensive and is rarely used on land; it is more practical in deep-water ocean-bottom settings where receivers can be stationary.

### Line geometries

In **line geometry**, shots and receivers are densely sampled along parallel lines. The line geometries are subdivided by the orientation of the shot and receiver lines:

- **Parallel geometry.** Shot lines and receiver lines are parallel. It is the basis of marine streamer acquisition (multisource, multistreamer) and some land surveys. The basic subset is the **midpoint line** or, in the ideal case, the **COV gather**.
- **Crossed-array / orthogonal geometry.** Shot lines and receiver lines cross at 90°. This is the most common land 3D geometry. The basic subset is the **cross-spread**. Variations include brick-wall geometry (staggered shot lines) and continuous shot-line geometry.
- **Slanted geometry.** Shot and receiver lines cross at an angle other than 90° (often with $\tan \alpha = 1$ or $2$).
- **Zigzag geometry.** Two families of parallel shot lines at ±45° to the receiver lines. It is efficient in desert environments with vibrators. The basic subsets are **zig-spreads** and **zag-spreads**.

Other specialized geometries include hybrid (combining OBC with dense shots), random, circular (coil shooting), and spiderweb geometries.

## Common 3D geometry elements

- **Source line:** line along which sources are placed or fired.
- **Receiver line:** line along which receivers are deployed.
- **Inline direction:** usually the long axis of the survey; the direction of the receiver lines in many land conventions.
- **Crossline direction:** perpendicular to the inline direction.
- **Template:** a repeating source–receiver pattern used in field acquisition. In orthogonal geometry, a template may consist of a shot salvo shooting into a fixed set of receiver lines.
- **Shot salvo:** a group of shots fired into a fixed receiver spread.
- **Swath:** a continuous strip of acquisition, often several templates side by side, or a group of receiver lines listening to each shot in zigzag geometry.

## 3D subsets and minimal data sets

A **3D subset** (or basic subset) is a 3D cross-section of the 5D prestack wavefield in which two spatial coordinates are fixed and two vary. Important examples include:

- 3D common-shot gather (fixed shot, varying receivers)
- 3D common-receiver gather (fixed receiver, varying shots)
- Cross-spread (one source line, one receiver line)
- COV gather (fixed offset vector, varying midpoint)
- 3D midpoint gather (fixed midpoint, varying offset vector)

A **minimal data set (MDS)** is a singlefold subset that can be used for imaging. Cross-spreads and 3D shot gathers are MDSs with limited spatial extent; the COV gather is the only MDS that can extend across the whole survey area, but it is rarely acquired in practice.

## Unit cell

The **unit cell** is the smallest repeating area of the geometry. It represents the periodicity of the acquisition parameters (Vermeer, 2012, §2.3.4.1). In orthogonal geometry, the unit cell is the area between two adjacent shot lines and two adjacent receiver lines.

The unit cell controls:

- **Spatial continuity.** A smaller unit cell means denser sampling of the basic subsets and fewer spatial discontinuities, which reduces migration artifacts.
- **Acquisition footprint.** At shallow levels, the periodicity of the geometry can appear as an acquisition footprint with the same periodicity as the unit cell.
- **Offset distribution.** The offset vectors in each bin of the unit cell are replicated across the fullfold area of the survey.
- **LMOS (largest minimum offset).** The diagonal of the unit cell sets the largest minimum offset, an important parameter for shallow coverage.

## Fold in 3D

**Fold** (or fold of coverage) is the number of traces per CMP bin. It can also be understood as the number of overlapping singlefold basic subsets at a point. For a regular orthogonal geometry, the total fold $M$ can be computed as

$$
M = M_i \times M_c
$$

where $M_i$ is the inline fold and $M_c$ is the crossline fold. Equivalently,

$$
M = \frac{\text{midpoint area of one cross-spread}}{\text{area of one unit cell}}
$$

In terms of acquisition parameters:

$$
M_i = \frac{\text{receiver spread length}}{2 \times \text{shot-line interval}}, \qquad M_c = \frac{\text{shot spread length}}{2 \times \text{receiver-line interval}}
$$

Fold varies in both directions because of:

- run-in and run-out at the edges of the survey,
- cable feather in marine data,
- skipped shots or receivers,
- irregular terrain or obstructions.

In marine streamer acquisition, crossline fold is usually one, so total fold equals inline fold.

## Aspect ratios

Three aspect ratios characterize orthogonal geometry (Vermeer, 2012, §2.4.3):

- **Aspect ratio of the bin:** shot-station interval / receiver-station interval.
- **Aspect ratio of the unit cell:** receiver-line interval / shot-line interval.
- **Aspect ratio of the cross-spread:** maximum crossline offset / maximum inline offset.

For symmetric sampling, all three aspect ratios should be close to one. This makes the inline and crossline sampling equivalent, which improves imaging, noise attenuation, and AVO/azimuth analysis.

## Spatial continuity

**Spatial continuity** is the absence of spatial discontinuities in the sampled wavefield. It is essential for good prestack imaging because discontinuities cause migration artifacts. The main factors affecting spatial continuity are:

- The line intervals (or grid intervals in areal geometry), which determine the spacing between basic subsets.
- Regularity of the geometry.
- Center-spread acquisition, which ensures reciprocal OVTs and better continuity.
- Missing shots, skipped lines, or irregular geometry, which create gaps.

Wide geometries (cross-spread aspect ratio near one) have fewer edges per unit area for a given fold and therefore better spatial continuity than narrow geometries.

## Acquisition parameters and their influence

| Parameter | Influence |
|-----------|-----------|
| Source/receiver station interval | Inline midpoint sampling; alias-free wavenumber bandwidth along the lines. |
| Source-line / receiver-line spacing | Crossline sampling, fold, and unit-cell size. |
| Maximum inline offset | Depth of velocity control, NMO stretch, multiple discrimination. |
| Maximum crossline offset | Crossline illumination, AVO/azimuth coverage. |
| Minimum offset | Shallowest coverage, near-surface QC, LMOS. |
| Record length | Maximum imaging depth. |
| Sampling rate | Temporal resolution and alias-free frequency. |
| Source/receiver arrays | Signal-to-noise ratio, anti-alias filtering, ground-roll suppression. |

## Symmetric sampling

**3D symmetric sampling** (Vermeer, 2012, §2.4.5) aims to sample the two varying spatial coordinates of each basic subset adequately. This is more affordable than dense sampling of all four spatial coordinates. The prescription is:

- Sample shots and receivers along their lines at the same interval (or intervals that satisfy the anti-alias requirements).
- Use source and receiver arrays with lengths equal to the station intervals when needed for noise suppression.
- Maximize the useful spatial extent of the basic subsets.
- Keep aspect ratios close to one for orthogonal geometry.

## Related concepts

- [Seismic acquisition — 2D essentials](seismic_acquisition.md)
- [Common midpoint (CMP) and fold](common_midpoint.md)
- [Seismic data sorts](seismic_data_sorts.md)
- [Cross-spread gather](cross_spread_gather.md)
- [OVT / COV panels](ovt_cov_panels.md)
- [Grid binning](grid_binning.md)
- [Seismic data formats](seismic_data_formats.md)
- [Seismic data QC](seismic_data_qc.md)
- [Seismic processing QC](seismic_processing_qc.md)
