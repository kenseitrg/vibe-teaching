---
title: CGG ODT01 — Data Analysis Part 2
status: draft
type: training slides
source_file: papers/general/ODT01A_DATA_ANALYSIS_PART2_v8.3.pptx
language: en
pages: ~70
concepts:
  - seismic_acquisition
  - common_midpoint
  - seismic_data_sorts
  - spatial_aliasing
  - seismic_noise
  - seismic_multiples
  - seismic_data_qc
tags: [cgg, data-analysis, 2d-geometry, 3d-geometry, sorting-domains, spatial-aliasing, qc, attribute-maps]
---

# CGG ODT01 — Data Analysis Part 2

Internal CGG training slides on 2D/3D geometry, sorting domains, spatial aliasing, and noise/multiple identification.

## Covered topics

| Section | Content |
|---------|---------|
| §7 2D and 3D geometry | CMP binning, moveup, nominal fold, 2D CMP numbering vs 3D binned CMP vs pseudo-2D |
| §8 Other sorting domains | Shot, receiver, CMP, common channel, offset plane gathers |
| §9 Spatial aliasing | Causes, dependence on frequency/dip/trace spacing, aliasing in different domains |
| §10 QC domains | Attribute maps, SP_X/SP_Y maps, shot/channel maps |
| §11 Noise introduction | Random and coherent noise types; domain-change removal strategies |
| §12 Multiple introduction | Definition, classification, identification on stacks and gathers |
| §13 Tools | Toggling, differencing, stacking, moveout scans, dip/apparent velocity, frequency spectra |

## Key takeaways

### 2D geometry
- CMP spacing = channel spacing / 2 for a simple 2D marine geometry.
- Moveup = shot spacing on subline / (2 × CMP spacing) = number of new CMPs per shot.
- Nominal fold = number of channels per streamer / moveup.
- 2D CMP numbering gives perfectly regular gathers and nominal fold.

### 3D geometry
- Midpoints are assigned to the 3D bin they fall into; bin centre coordinates depend on the chosen geometry.
- Fold is no longer perfectly regular because of cable feather, variable boat speed/direction, and line overlap.
- True 3D binned CMPs are positioned correctly but have irregular fold/trace spacing; pseudo-2D preserves line identity but not exact subsurface location.

### Sorting domains
- **Shot gather**: traces from the same shot; good for noise attenuation and interpolation, but contains structure.
- **Receiver gather**: traces recorded at the same surface location; natural trace spacing is shot spacing, often aliased.
- **CMP gather**: same midpoint; minimizes structural effects, used for stacking and velocity-based demultiple.
- **Common channel / offset plane**: single offset or narrow offset range; useful for interpolation and common-offset migration.

### Spatial aliasing
- Aliasing occurs when trace spacing is too coarse for the frequency and dip present.
- Relevant dip can be geological dip or apparent dip from moveout.
- Aliasing appears differently in shot, CMP, and offset-plane domains.

### QC attribute maps (§10)
- Attribute maps are an important QC domain; understanding what the attribute represents is essential before deciding what is good or bad.
- **SP_X/SP_Y amplitude maps**: average or RMS amplitudes plotted in shot coordinates. A subsurface feature appears shifted by half the source–receiver offset in the shooting direction, so coherent geology can look like shot-related stripes.
- **Shot/channel maps**: RMS amplitude per channel. Stripes can reveal acquisition problems, source drop-outs, or shallow/buried features.
- Mechanisms causing amplitude map patterns:
  - Very shallow feature: affects all traces on the cable while the source passes over it → vertical stripe on a shot/channel map.
  - Stationary surface feature (e.g., receiver coupling): appears as a common-receiver pattern.
  - Buried feature: affects only certain offsets at a given time → diagonal stripe on shot/channel maps.
- RMS is generally preferred over simple average amplitude because it is less dominated by a single extreme sample.

### Noise and multiples
- Noise-removal strategies: separate signal/noise by domain change (e.g., tau-p) or randomize coherent noise by re-sorting.
- Multiples have at least one downward reflection; classification by shallowest reflector, order, and free-surface involvement.
- Combining stack, near/far stacks, shot gathers, and CMP gathers helps distinguish primaries from multiples.

## Figures useful for teaching
- 2D geometry: shot spacing, channel spacing, moveup, fold build-up.
- 3D geometry: bin grid, midpoint drift, fold variation.
- Domain comparison: shot, receiver, CMP, offset plane.
- Spatial aliasing examples in CMP and offset-plane domains.
- Shot/channel RMS amplitude maps showing acquisition artifacts.

## Relation to lecture notes
- Provides the acquisition-parameter and data-sort material for Term 1 Lecture 1.
- Supports the discussion of fold, CMP, and why different processing domains are used.
- **Supports the input-data QC section of Term 1 Lecture 2: geometry verification, attribute maps, and interpreting amplitude-map patterns.**
