---
title: Discrete Fourier transform (DFT)
status: draft
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - margrave_2006_methods_of_seismic_data_processing
  - yilmaz_practical_seismic_data_analysis_amplitude
tags: [dft, fourier-transform, spectral-analysis, sampling, signal-processing]
---

# Discrete Fourier transform (DFT)

The DFT turns a finite digital time series into a finite set of frequency samples. It is the workhorse of digital spectral analysis and of frequency-domain filtering.

## What it does

Given a real or complex time series with $N$ samples spaced by $\Delta t$, the DFT produces $N$ complex frequency samples $X[k]$:

- $k = 0$ is the DC (zero-frequency) component.
- $k = 1, \dots, N/2-1$ are positive frequencies.
- $k = N/2$ is the Nyquist frequency.
- Samples above the Nyquist are redundant for a real input because of symmetry.

The frequency spacing is

$$\Delta f = \frac{1}{N\Delta t} = \frac{1}{T},$$

where $T$ is the total record length. A longer record gives finer frequency resolution.

## Important properties

- **Periodicity**: $X[k+N] = X[k]$. The DFT treats both the time series and its spectrum as periodic.
- **Real-signal symmetry**: for a real-valued time series, $X[-k] = X^*[k]$. Only the first $N/2 + 1$ values are independent.
- **Exact reconstruction**: the inverse DFT recovers the original $N$ samples exactly.
- **Approximation**: the DFT approximates the continuous Fourier transform; the approximation improves as $N$ increases and $\Delta t$ decreases.

## Why it matters for seismic data

A seismic trace is a finite, sampled time series. The DFT lets us:
- inspect its amplitude and phase spectra,
- design and apply frequency filters,
- convert convolution into multiplication for fast filtering,
- analyze noise bands and frequency content for QC.

## Related concepts

- [Aliasing](aliasing.md)
- [Spectral analysis](spectral_analysis.md)
- [Frequency filtering](frequency_filtering.md)

## Sources

- Hatton, Worthington & Makin (1986), Ch. 2.3 — DFT definition, periodicity, symmetry, Nyquist frequency.
- Margrave (2006), Ch. 2 — DFT, sampling, and the convolution theorem.
- Yilmaz, *Practical Seismic Data Analysis*, §1.2–1.3 — sampled time series, z-transform, and Fourier spectrum.
