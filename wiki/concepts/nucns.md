---
title: Non-Uniform Coherent Noise Suppression (NUCNS)
status: draft
sources:
  - nucns
  - nucns_best_practice
tags: [nucns, coherent-noise, fk-filter, 3d-noise-attenuation]
---

# Non-Uniform Coherent Noise Suppression (NUCNS)

NUCNS is a method for estimating and subtracting shot-generated coherent noise in 3D land data. It works on non-uniform geometries — cross-spreads, common-shot gathers, and common-receiver gathers — without needing regular spatial sampling.

## What it does

NUCNS estimates a **noise model** for each trace location by decomposing the data into moving windows and identifying energy that follows linear moveout bands. The estimated noise is then adaptively subtracted:

1. Decompose the data into overlapping spatial windows.
2. For each window, estimate the dominant coherent noise bands in 3D FK space.
3. Convert each band into an amplitude factor times a kinematic (moveout) operator.
4. Subtract the modeled noise from the original data.

## Key idea: linear noise bands

Coherent noise (ground roll, refracted energy) often arrives with approximately linear moveout over a short spatial window. Each "noise band" is described by:

$$ \text{noise}_i(x, y, t) = A_i \cdot w_i(t - p_x x - p_y y) $$

where $p_x$ and $p_y$ are slownesses in the $x$ and $y$ directions, $A_i$ is an amplitude scaling factor, and $w_i$ is a noise wavelet. For linear kinematics, a single term per band is sufficient. If the moveout is curved, multiple terms and a curved kinematic operator may be needed.

## Why not just 2D FK?

- 2D FK filtering requires uniformly sampled receiver lines. Real 3D land data uses cross-spreads with irregular offsets and azimuths.
- Non-uniform geometry causes spatial aliasing and leakage in 2D FK — energy maps to wrong wavenumbers.
- NUCNS builds a noise model trace-by-trace using the actual acquisition geometry, so it helps to separate signal and noise regions.

## Adaptive subtraction

The estimated noise model is rarely perfect in amplitude and phase. NUCNS typically follows with an adaptive subtraction step (a local Wiener or matching filter) to fine-tune the match before subtraction.

## Limitations

- **Assumes linear moveout** for each noise band within the analysis window. Strongly curved or dispersive noise may need smaller windows or multiple terms.
- **Window size matters**: too large windows violate the linear-moveout assumption; too small windows do not contain enough data to estimate the noise reliably.
- **Signal leakage**: if the reflection signal has the same dip as a noise band, some signal may be removed.

## Related concepts

- [Seismic noise](seismic_noise.md)
- [Adaptive subtraction](adaptive_subtraction.md)
- [Frequency filtering](frequency_filtering.md)
- [FK-MUSIC / array analysis](fk_music_surface_waves.md)
- [Radon transform](radon_transform.md)

## Sources

- CGG — NUCNS processing description.
- CGG — NUCNS best practice guide.
