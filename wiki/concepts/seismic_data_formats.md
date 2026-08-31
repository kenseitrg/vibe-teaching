---
title: Seismic data formats
status: draft
sources:
  - seg_y_rev2_format
  - seg_sps_format_rev21
  - cgg_odt01_data_analysis_part1
  - cgg_odt01_data_analysis_part2
tags: [segy, segd, sps, ukooa, format, geometry]
---

# Seismic data formats

Field seismic data arrive in specialized formats. Before processing can begin, traces and geometry must be loaded and merged in the processing system.

## Trace data formats

### SEG-D

- **SEG-D** is a field tape format designed for raw, high-resolution seismic records.
- It supports many sample formats, multiple channels, and extensive header information.
- It is common for land acquisition and some marine data.

### SEG-Y

- **SEG-Y** is the standard exchange format for processed or partially processed seismic traces.
- File structure:
  1. **Textual file header** (3200 bytes, EBCDIC or ASCII).
  2. **Binary file header** (400 bytes).
  3. **Optional extended textual headers**.
  4. **Data traces**: each has a 240-byte trace header followed by sample values.
- Key trace headers: shot/receiver line and point, X/Y/Z coordinates, CMP/ensemble number, offset, number of samples, sample interval.
- SEG-Y rev 2.0 (2017) improves coordinate reference system support and extended headers.

## Geometry formats

### SPS (Shell Processing Support)

- Used mainly for **land** 3D surveys.
- Four ASCII file types: **R** (receiver points), **S** (source points), **X** (source–receiver relation), **C** (comments).
- The relation file ties each trace to its source and receiver coordinates.

### UKOOA P1/90

- Marine and transition-zone geometry format.
- Similar purpose to SPS: describe source and receiver positions and how they relate to recorded traces.

## Loading data into a processing system

1. Read the field traces (SEG-D or SEG-Y).
2. Read the geometry files (SPS, UKOOA, or header information embedded in SEG-Y).
3. Assign geometry to each trace, populating trace headers with coordinates, offsets, CMP numbers, etc.
4. Convert to the processing system’s internal format.
5. Perform quality control: check fold, offsets, first breaks, amplitude consistency, and geometry maps.

## Why formats matter

- A mis-mapped byte in a SEG-Y header can shift every shot or receiver position.
- Missing or wrong geometry makes velocity analysis, stacking, and migration meaningless.
- Understanding the formats helps processors diagnose loading problems and communicate with acquisition crews.

## Sources

- SEG-Y rev 2.0 technical standard.
- SPS Format rev 2.1 technical standard.
- CGG ODT01 Data Analysis Part 1, §§7–8 (2D/3D geometry).
