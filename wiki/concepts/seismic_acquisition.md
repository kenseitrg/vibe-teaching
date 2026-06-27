---
title: Seismic acquisition — 2D essentials
status: draft
sources:
  - hill_ruger_2020_illustrated_seismic_processing_preimaging
  - cgg_odt01_data_analysis_part2
  - vermeer_2012_3d_seismic_survey_design
  - seg_sps_format_rev21
tags: [acquisition, 2d, cmp, fold, geometry, source, receiver]
---

# Seismic acquisition — 2D essentials

Seismic acquisition is the field experiment that provides the raw data for processing. In the first two terms of this course we focus on 2D acquisition.

## Basic idea

A source generates elastic waves at the surface. Waves propagate downward, reflect or diffract at impedance contrasts, and return to receivers at the surface. Each receiver records one **trace**. A group of traces from one shot is a **shot gather** (or shot record, ОПВ).

## Data types

| Criterion | Categories |
|-----------|------------|
| Environment | land, marine, transition zone (TZ) |
| Source | impulsive (dynamite, airgun) or vibratory (vibroseis) |
| Receiver deployment | stationary geophones/hydrophones, or cable/streamer moved with the vessel |

## CMP method

The **common-midpoint (CMP) method** deliberately records the same subsurface region many times from different source–receiver pairs.

- For a horizontal reflector, the reflection point lies directly below the midpoint between source and receiver.
- Repeating the measurement with different offsets gives a **CMP gather** (ОСТ gather).
- If the reflector dips, the reflection point moves up-dip; the traces still share a midpoint, so **CMP** is the safer term than **CDP** (common depth point).

## Why repeated observations help

1. **Velocity estimation**: the change of arrival time with offset (normal moveout, NMO) depends on velocity.
2. **Signal-to-noise improvement**: stacking the aligned traces of a CMP gather reinforces signal and suppresses random noise.
3. **Multiple discrimination**: primaries and multiples have different moveout, which is easier to see in a CMP gather.

## Key acquisition parameters

| Parameter | Symbol / name | Effect on processing |
|-----------|---------------|----------------------|
| Source interval | distance between shots | Lateral sampling along the line |
| Receiver interval | group spacing | Lateral sampling and maximum recoverable dip |
| Sampling rate | Δt | Temporal resolution and alias-free bandwidth |
| Record length | T | Maximum imaging depth |
| Minimum offset | near offset | Shallowest coverage, statics QC |
| Maximum offset | far offset | Depth of velocity control, NMO stretch |
| Receiver spread / cable length | aperture | Subsurface illumination range |
| Fold | number of traces per CMP | Noise attenuation and stack quality |

## Fold in 2D

For a simple split-spread or end-on 2D geometry:

$$
\text{fold} \approx \frac{\text{number of active receiver groups}}{2 \times \text{moveup}}
$$

where **moveup** is the number of new CMP locations added per shot. For marine 2D:

$$
\text{moveup} = \frac{\text{shot spacing}}{2 \times \text{CMP spacing}}
, \qquad
\text{CMP spacing} = \frac{\text{receiver group spacing}}{2}
$$

## From acquisition to processing

Acquisition produces:
- Field seismic records (often SEG-D).
- Geometry files describing source and receiver positions (SPS for land, UKOOA P1/90 for marine).
- Observer reports and instrument logs.

Processing starts by merging the seismic traces with their geometry and converting everything into the processing system’s internal format.

## Sources

- Hill & Rüger (2020), *Illustrated Seismic Processing, Vol. 2*, Appendix A.
- CGG ODT01 Data Analysis Part 2, §7.
- SEG SPS Format rev 2.1.
