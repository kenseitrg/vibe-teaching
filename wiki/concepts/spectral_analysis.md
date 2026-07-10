---
title: Spectral analysis
status: draft
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - margrave_2006_methods_of_seismic_data_processing
  - yilmaz_practical_seismic_data_analysis_amplitude
tags: [spectral-analysis, amplitude-spectrum, phase-spectrum, dft, convolution]
---

# Spectral analysis

Spectral analysis looks at the frequency content of a seismic trace or wavelet. It decomposes a time-domain signal into amplitude and phase as a function of frequency.

## The convolutional model in the frequency domain

A single seismic trace is often approximated by

$$x(t) = w(t) * r(t) + n(t).$$

In the frequency domain this becomes multiplication:

$$X(f) = W(f) \, R(f) + N(f),$$

so each convolutional component contributes its own amplitude and phase spectrum. The source signature, ghosts, instrument response, absorption, and reflectivity all leave separate fingerprints in the spectrum.

## What discretization and finite length do

A real seismic trace is:
1. **Sampled** in time. This makes the spectrum periodic; frequencies above Nyquist alias.
2. **Finite in length**. This is equivalent to multiplying by a rectangular window, which convolves the true spectrum with a sinc function.

The practical consequences are:

- **Spectral leakage**: a single frequency sinusoid spreads energy across neighboring frequencies.
- **Limited frequency resolution**: two close frequencies can only be separated if the record is long enough ($\Delta f \approx 1/T$).
- **Periodic replication**: the spectrum repeats at multiples of the sampling frequency.

## Amplitude and phase spectra

- **Amplitude spectrum**: how much of each frequency is present.
- **Phase spectrum**: the timing relationship between frequencies.
- A zero-phase wavelet is symmetric; a minimum-phase wavelet is causal and front-loaded.

## Uses in processing

- Designing band-pass filters.
- Diagnosing source ghosts, instrument notches, and noise bands.
- Comparing spectra before and after deconvolution.
- QC: checking that high-frequency signal decays with time as expected from absorption.

## Related concepts

- [Discrete Fourier transform](discrete_fourier_transform.md)
- [Aliasing](aliasing.md)
- [Frequency filtering](frequency_filtering.md)
- [Minimum phase wavelet](minimum_phase.md)
- [Seismic wavelet](seismic_wavelet.md)

## Sources

- Hatton, Worthington & Makin (1986), Ch. 2.9 — spectral analysis and the convolutional spectrum model.
- Margrave (2006), Ch. 2 — Fourier transforms, convolution theorem, and spectral estimation.
- Yilmaz, *Practical Seismic Data Analysis*, §1.3.1 — Fourier decomposition of a trace and its amplitude spectrum.
