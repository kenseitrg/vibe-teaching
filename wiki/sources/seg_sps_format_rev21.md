---
title: SEG Technical Standards Committee — SPS Format rev 2.1 (Shell Processing Support)
status: draft
type: technical standard
source_file: papers/formats/SEG SPS Format rev 2.1.pdf
language: en
pages: ~25
concepts:
  - seismic_data_formats
  - seismic_acquisition
tags: [sps, geometry-format, data-format, technical-standard, survey]
---

# SPS Format rev 2.1 — Shell Processing Support Format for 3D Surveys

Adopted by the SEG in 1993; revised to conform with SEG-D rev 2.1 (2006). Defines how land 3D (and 2D) survey geometry is delivered to the processing centre.

## File types

An SPS delivery normally contains four ASCII files:

| File | Prefix | Content |
|------|--------|---------|
| Receiver point file | R | Receiver line, point, X/Y/Z coordinates, elevation, geophone details |
| Source point file | S | Source line, point, X/Y/Z coordinates, elevation, source details |
| Cross-reference / relation file | X | Links source–receiver pairs to recorded trace ensembles |
| Comment file | C | Free-text comments and quality-control notes |

## Record types

- **Header records**: describe the survey, units, projection, datum, etc.
- **Point records**: list each physical source or receiver point with its surface coordinates.
- **Relation records**: define which source and receiver points combine to form each trace; the relation file is what ties geometry to the seismic traces.

## Key concepts

- SPS is a **relational** format: trace geometry is reconstructed from the relation file by looking up source and receiver point coordinates.
- Point numbers and line numbers are usually integer; coordinates can be in a local grid or a global CRS.
- SPS is designed for **land** surveys; marine geometry is often delivered in related P1/90 (UKOOA) or internal contractor formats.

## Relevance for teaching

- Before any processing can begin, SEG-Y trace headers must be populated with geometry from SPS (or UKOOA).
- Errors in SPS point numbers or relation files are a common cause of geometry problems in land processing.
- Understanding SPS helps explain why “geometry assignment” is a separate preprocessing step.

## Relation to lecture notes
- Supports the “data formats” section of Term 1 Lecture 1, especially land acquisition geometry.
- Complements the SEG-Y source page: traces carry the samples, SPS carries the spatial metadata.
