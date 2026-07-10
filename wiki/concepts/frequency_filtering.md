---
title: Frequency filtering
status: draft
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - margrave_2006_methods_of_seismic_data_processing
  - yilmaz_practical_seismic_data_analysis_amplitude
tags: [frequency-filtering, band-pass, low-pass, high-pass, notch, gibbs, iir, fir]
---

# Frequency filtering

Frequency filtering modifies a seismic trace by shaping its amplitude spectrum. In the time domain the same operation is a convolution with a filter operator.

## Time domain vs. frequency domain

- **Multiplication in frequency domain**: multiply the trace spectrum by the filter spectrum.
- **Convolution in time domain**: convolve the trace with the filter impulse response.

The two views are equivalent because of the convolution theorem.

## Common filter types

| Type | What it keeps | Typical use |
|------|---------------|-------------|
| **Low-pass** | frequencies below cutoff | remove high-frequency noise, smooth data |
| **High-pass** | frequencies above cutoff | remove low-frequency ground roll or drift |
| **Band-pass** | frequencies between two cutoffs | isolate the reflection signal band |
| **Notch/reject** | everything except a narrow band | suppress 50/60 Hz power-line interference |

## Filter parameters

- **Cutoff frequency**: often defined at the -3 dB (half-power) point.
- **Passband**: the range of frequencies kept with little attenuation.
- **Stopband**: the range strongly attenuated.
- **Transition band**: the range between passband and stopband.
- **Slope**: attenuation rate, usually expressed in dB per octave.

## The Gibbs phenomenon and filter length

An ideal filter with a perfectly sharp cutoff has an infinitely long impulse response (a sinc function). Truncating it to a finite length produces:

- **Gibbs ringing**: oscillations in the time domain near sharp amplitude transitions.
- **Sidelobes**: unwanted pass-through of stopband frequencies.

A longer filter gives a steeper cutoff and lower sidelobes, but costs more computation and can amplify noise. Applying a tapered window (e.g., Hamming, Blackman) reduces ringing.

## FIR and IIR filters

- **FIR (finite impulse response)**: non-recursive, finite length, can be designed with linear phase. Common in seismic processing.
- **IIR (infinite impulse response)**: recursive, causal, compact but with non-linear phase. A **Butterworth** filter is a common IIR example with a maximally flat passband and smooth roll-off.

## Practical examples

- A low-cut filter removes ground roll from land data.
- A band-pass filter (e.g., 10–70 Hz) isolates the reflection signal band.
- A notch filter removes 50 Hz industrial interference.
- Anti-alias low-pass filters protect data before decimation.

## Trade-offs

| Want | Cost |
|------|------|
| Steep slope | Longer filter, more ringing |
| Short filter | Shallow slope, less frequency selectivity |
| Linear phase | FIR design, longer operator |
| Smooth response | IIR (Butterworth), but phase distortion |

## Related concepts

- [Discrete Fourier transform](discrete_fourier_transform.md)
- [Aliasing](aliasing.md)
- [Spectral analysis](spectral_analysis.md)
- [Seismic wavelet](seismic_wavelet.md)
- [Deconvolution](deconvolution.md)

## Sources

- Hatton, Worthington & Makin (1986), Ch. 2.5 — filter types, slopes, decibels, ringing.
- Margrave (2006), Ch. 2 — filtering, generic wavelets, and Z-transform.
- Yilmaz, *Practical Seismic Data Analysis*, §1.1.5 — processing-flow examples using band-pass filtering.
