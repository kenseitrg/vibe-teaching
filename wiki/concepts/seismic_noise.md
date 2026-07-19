---
title: Seismic noise
status: draft
sources:
  - cgg_odt02_denoise
  - hill_ruger_2020_illustrated_seismic_processing_preimaging
tags: [noise, coherent-noise, random-noise, signal-to-noise]
---

# Seismic noise

Seismic noise is any recorded energy that is not the signal of interest. Whether something is "noise" depends on the target: a surface wave is signal for near-surface imaging (MASW, SWI) but coherent noise for reflection processing aimed at deeper targets.

## Coherent noise

Coherent noise has a consistent phase relationship across traces. It follows predictable moveout curves and can be modeled or transformed. Examples:

- **Ground roll**: low-velocity, low-frequency, dispersive surface waves on land data. Energy in the Rayleigh-wave cone.
- **Refracted arrivals / head waves**: first breaks and later refracted energy, often high-amplitude.
- **Air waves**: sound propagating through the atmosphere at ~330 m/s. Weak but noticeable on quiet records.
- **Multiples**: energy that reflects more than once in the subsurface. Often coherent and predictable in period.


Coherent noise can often be suppressed by transforms (FK, $\tau$-$p$, curvelet) because it maps to localized regions of transform space.

## Random noise

Random noise has no consistent phase relationship across traces. It cannot be modeled or predicted trace-to-trace. Examples:

- **Ambient noise**: wind, microtremors, rain, distant ocean waves — uncorrelated background vibrations.
- **Instrument noise**: thermal noise in geophones, analog-to-digital converter (ADC) quantization error, cable noise.
- **Bit noise / spikes**: single-sample amplitude bursts caused by transmission errors.
- **Cultural noise**: power-line hum (49/60 Hz), traffic, pumps, drilling activity — any human-generated energy.

Random noise is spread across the entire FK spectrum, so it cannot be removed by simple dip filtering. Statistical methods (median filtering, FX-deconvolution, SVD/Cadzow) are needed.

## Signal-to-noise ratio

The signal-to-noise ratio (SNR) is defined as:

$$ \text{SNR} = \frac{\text{signal power}}{\text{noise power}} $$

In practice, SNR is measured over a window where the signal is known (e.g., the first-arrival window for first-break quality). Stacking improves SNR by a factor of $\sqrt{N}$ for uncorrelated noise, where $N$ is the fold.

## No free lunch

There is no algorithm that removes all noise without affecting the signal:

- Aggressive denoising creates "processing artefacts" that look like geology but are not.
- Subtle noise that survives processing degrades subsequent steps (velocity analysis, AVO, inversion).
- Every denoising method has a parameter (threshold, filter length, rank) that trades noise removal against signal preservation.

## Two approaches

There are two complementary strategies:

- **Model the noise** (e.g., predict the ground roll from dispersion, estimate coherent noise bands), then subtract it.
- **Model the signal** (e.g., FX-deconvolution, curvelet thresholding — assume the signal is sparse or predictable), then keep it.

Most modern workflows combine both: model what they can predict, then attenuate the residual with a statistical method.

## Related concepts

- [Frequency filtering](frequency_filtering.md)
- [Radon transform](radon_transform.md)
- [Adaptive subtraction](adaptive_subtraction.md)
- [FK-MUSIC / array analysis](fk_music_surface_waves.md)
- [NUCNS / coherent noise suppression](nucns.md)
- [Curvelet transform](curvelet_transform.md)
- [Median filtering / AAA](median_filtering_frequency_domain.md)
- [FX-deconvolution](fx_deconvolution.md)
- [SVD / Cadzow filtering](cadzow_svd_filtering.md)

## Sources

- CGG (ODT-02) — Denoise processing guide.
- Hill & Rüger (2020) — *Illustrated Seismic Processing*, ch. "Pre-imaging".
