---
title: "Seismic Signals and Noise — Bormann & Wielandt (NMSOP Ch. 4)"
status: draft
source_type: textbook chapter
authors: "Peter Bormann, Erhard Wielandt"
year: 2013
url: "https://doi.org/10.2312/GFZ.NMSOP-2_ch4"
source_file: papers/noise_attenuation/Egon_Bormann_Wielandt_Ch4_Seismic_Signals_and_Noise.pdf
lectures:
  - term03_lec04
related_concepts:
  - seismic_noise
  - spectral_analysis
  - frequency_filtering
  - seismic_data_qc
tags: [noise-attenuation, spectral-analysis, power-spectral-density, seismic-noise, fourier-transform, detection-thresholds]
---

# Seismic Signals and Noise — Bormann & Wielandt (NMSOP Ch. 4)

Bormann, P. & Wielandt, E. (2013). Seismic Signals and Noise. Chapter 4 in *New Manual of Seismological Observatory Practice 2* (NMSOP-2), GFZ German Research Centre for Geosciences. DOI: 10.2312/GFZ.NMSOP-2_ch4.

## Main message

A comprehensive reference chapter on the nature, mathematical representation, and spectral characterisation of seismic signals and noise. It covers Fourier analysis of transient and stationary signals, power spectral densities, the global seismic noise model (petroseismological noise spectrum), instrumental self-noise, and methods for improving signal-to-noise ratio by frequency filtering, velocity filtering/beamforming, and prediction-error filtering.

## Key points

1. **Signal vs. noise is context-dependent:** What is noise in one study (e.g., ocean microseisms for earthquake detection) may be signal in another (e.g., ambient-noise tomography). Noise sources include ocean microseisms, man-made vibrations, scattering, instrument self-noise, and processing artefacts.
2. **Fourier analysis:** Transient signals use the Fourier integral (continuous) or DFT (sampled). Stationary signals (ambient noise) require power spectral density (PSD) analysis; a strict Fourier transform does not exist for infinite stationary signals.
3. **PSD and the seismic noise model:** The global noise model (Fig. 4.30) shows two noise peaks — the primary microseism peak (~0.05–0.1 Hz from ocean-wave interaction with the seafloor) and the secondary microseism peak (~0.1–0.3 Hz from nonlinear wave–wave interaction). Noise levels vary by ~60 dB depending on location, season, and time of day.
4. **Instrumental self-noise:** Modern broadband seismometers have self-noise levels below the New Low Noise Model (NLNM) in their passband. The self-noise PSD is compared to the earth noise PSD to determine the effective dynamic range.
5. **SNR improvement methods:**
   - **Frequency filtering:** Exploits bandwidth differences between signal and noise.
   - **Velocity filtering / beamforming:** Exploits spatial coherence of signal vs. noise.
   - **Prediction-error filtering:** Removes repetitive noise (multiples, reverberations).
   - **Polarisation filtering:** Exploits particle-motion differences.
6. **Detection thresholds:** Depend on signal bandwidth, duration, and ambient noise level. Short-period body waves (~1 Hz) have higher detection thresholds than long-period surface waves (~0.05 Hz).
7. **Dynamic range:** Modern 24-bit digitisers provide ~140 dB; the useful dynamic range is limited by the noise environment (60 dB variation in ambient noise corresponds to ~3 magnitude units in detection threshold).

## Relation to lecture notes

This chapter provides the theoretical foundation for understanding seismic noise classification and spectral analysis used in Term 3 Lecture 04. The global noise model and PSD framework underpin the lecture's treatment of noise characterisation, while the SNR improvement methods map directly onto the processing techniques (frequency filtering, FK filtering, deconvolution) covered in the course.

## Related concepts

- [Seismic noise](../concepts/seismic_noise.md)
- [Spectral analysis](../concepts/spectral_analysis.md)
- [Frequency filtering](../concepts/frequency_filtering.md)
- [Seismic data QC](../concepts/seismic_data_qc.md)
