---
title: SEG Technical Standards Committee (2017) — SEG-Y rev 2.0 Data Exchange format
status: draft
type: technical standard
source_file: papers/formats/SEG-Yrev2Release.pdf
language: en
pages: 44
concepts:
  - seismic_data_formats
tags: [segy, data-format, technical-standard, trace-header, file-header]
---

# SEG-Y rev 2.0 Data Exchange format

SEG Technical Standards Committee, January 2017. The current SEG standard for exchange of seismic trace data.

## File structure

A SEG-Y file consists of:

1. **Textual file header** (3200 bytes): EBCDIC or ASCII, 40 lines of 80 characters. Describes the dataset, acquisition parameters, and processing history.
2. **Binary file header** (400 bytes): fixed binary fields defining sample rate, number of samples per trace, data format code, coordinate system, etc.
3. **Extended textual file header(s)** (optional): additional metadata in stanza format.
4. **Data traces**: each trace has a **240-byte trace header** followed by the **trace data samples**.

## Key trace header information

| Header content | Purpose |
|----------------|---------|
| Trace sequence number | Position within the file or line |
| Shot / receiver line and point numbers | Link to geometry |
| Source/receiver X, Y, Z coordinates | Spatial positioning |
| CDP / CMP / ensemble number | Common midpoint bin |
| Offset | Source–receiver distance |
| Number of samples, sample interval | Time/depth sampling |
| Trace identification code | Type of trace (seismic, dead, etc.) |

## Data sample formats

Common formats include:
- IBM 32-bit floating point (historical)
- IEEE 32-bit floating point (most common today)
- 32-bit and 16-bit integer
- 8-bit integer (compressed)

## Relevance for teaching

- SEG-Y is the de facto exchange format between contractors, processing centres, and interpretation workstations.
- Raw field data often arrive in SEG-D; final products and intermediate QCs are typically SEG-Y.
- Loading SEG-Y into a processing system requires mapping trace headers correctly (the “dictionary”); mistakes in header mapping produce geometry errors.
- Rev 2.0 added better support for coordinate reference systems and extended headers, but many legacy files still use rev 0 or rev 1 conventions.

## Relation to lecture notes
- Supports the “data formats” section of Term 1 Lecture 1.
- Explains why geometry (SPS/UKOOA) must be merged with trace data for processing.
