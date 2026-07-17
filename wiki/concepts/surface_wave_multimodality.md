---
title: Surface wave multimodality
status: draft
sources:
  - foti_surface_wave_methods
  - foti_interpacific_guidelines
  - novotny_seismic_surface_waves
  - sedi_surface_waves
  - rawlinson_surface_waves_dispersion
  - datta_2018
  - mi_surface_waves_dispersion_energy
  - ivanov_hrlrt_masw
tags: [surface-waves, modes, higher-modes, fundamental-mode, dispersion]
---

# Surface wave multimodality

In a horizontally layered medium, surface waves can propagate in more than one way at the same frequency. Each distinct propagation pattern is a **mode**. The lowest-velocity mode is the **fundamental mode**; faster modes are **higher modes** or **overtones**.

## Fundamental and higher modes

- The fundamental mode has no node in the uppermost part of the wavefield and is usually the most energetic at low frequencies.
- Higher modes exist only above a **cut-off frequency**. As frequency increases, more modes become possible.
- Each mode has its own phase velocity at each frequency, so a layered medium produces a family of dispersion curves, one per mode.

## Depth sensitivity of modes

- Higher modes have more complex depth dependence (more nodes) than the fundamental mode.
- This means they sample different depth ranges and can add independent information about the S-wave velocity profile.
- In normally dispersive profiles, the fundamental mode is often dominant; in profiles with strong contrasts or embedded low-velocity layers, higher modes can dominate certain frequency bands.

## Practical implications

- **Mode misidentification** is a common pitfall: an energy branch that looks like the fundamental mode may actually be a higher mode or a guided wave from a low-velocity layer.
- Misidentified curves can produce large errors in the inverted S-wave profile.
- **Multi-mode inversion** uses two or more modes together. It reduces non-uniqueness and can improve both maximum investigation depth and vertical resolution.
- High-resolution transforms (HRLRT, f-k-MUSIC) help separate modes on the dispersion image so they can be picked correctly.

## When higher modes matter

- Strong velocity contrast at shallow depth (e.g., soft sediment over bedrock).
- Embedded low-velocity layer (LVL), which can create LVL-guided energy that interlaces with true surface-wave modes.
- Stiff or rock sites where the fundamental mode is weak or only measurable over a narrow band.

## Related concepts

- [Surface waves](surface_waves.md)
- [Surface wave dispersion](surface_wave_dispersion.md)
- [Surface wave inversion](surface_wave_inversion.md)
- [FK-MUSIC / array analysis](fk_music_surface_waves.md)

## Sources

- [Foti et al. (2011) — Surface wave methods](../sources/foti_surface_wave_methods.md)
- [Foti et al. (2018) — InterPACIFIC guidelines](../sources/foti_interpacific_guidelines.md)
- [Novotny (1999) — Seismic surface waves](../sources/novotny_seismic_surface_waves.md)
- [Igel (2007) — Surface waves and free oscillations](../sources/sedi_surface_waves.md)
- [Rawlinson (2007) — Surface waves and dispersion](../sources/rawlinson_surface_waves_dispersion.md)
- [Datta (2018) — f-k-MUSIC method](../sources/datta_2018.md)
- [Mi et al. (2016) — Dispersion energy analysis](../sources/mi_surface_waves_dispersion_energy.md)
- [Ivanov et al. (2017) — HRLRT with MASW](../sources/ivanov_hrlrt_masw.md)
