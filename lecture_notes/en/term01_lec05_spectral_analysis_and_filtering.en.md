---
title: Term 1 Lecture 05 — Spectral Analysis and Frequency Filtering
status: draft
term: 01
lecture: 05
---

# Spectral Analysis and Frequency Filtering

## Learning objectives

By the end of this lecture you should be able to:

- Describe a seismic trace as a finite, sampled version of a continuous signal and explain the consequences of sampling and finite length.
- State the DFT in words, explain its periodicity, and use the frequency-resolution formula $\Delta f = 1/(N\Delta t)$.
- Use the convolutional spectrum model: trace spectrum = product of wavelet, reflectivity, and noise spectra, plus the effects of windowing and sampling.
- Define the Nyquist frequency and predict aliased frequencies for a given sample interval.
- Explain why anti-alias filtering is needed before digitization and before downsampling in processing.
- Distinguish low-pass, high-pass, band-pass, and notch filters and give a typical seismic use case for each.
- Describe the Gibbs phenomenon and the trade-off between filter transition steepness and filter length.
- Sketch a Butterworth amplitude response and interpret a simple numerical example.
- Recognize that time-variant filters are sometimes used because the useful signal band changes with record time.

## Prerequisites

- Term 1 Lecture 01: the recorded trace, the convolutional model, source–receiver geometry.
- Basic sinusoids, amplitude, phase, and complex exponentials from a companion signal-processing course.
- Comfort with summation notation and simple complex numbers.

## 1. Seismic trace model: from analog to finite digital data

A seismic trace starts as a continuous analog signal in time. At the recording station it is passed through an anti-alias filter, sampled at regular intervals, and stored as a finite list of numbers. The two fundamental limitations of the stored trace are therefore:

1. **Discrete sampling**: only values at $t = n\Delta t$ are kept.
2. **Finite length**: only a window of length $T = N\Delta t$ is kept.

Typical values are:

- sample interval $\Delta t = 1$, $2$, or $4$ ms (high-resolution surveys may use $0.25$ or $0.5$ ms);
- record length $T$ from a few seconds to several seconds;
- number of samples $N = T / \Delta t$, often $1000$–$20000$.

Both sampling and finite length have direct consequences in the frequency domain. Sampling makes the spectrum periodic, and finite length smears the spectrum. The DFT is the practical tool that computes that spectrum.

![](figures/term01_lec05/term01_lec05_trace_model.png){width=90%}

**Figure 1.** *From a continuous analog signal to a finite digital trace. Sampling selects points at interval $\Delta t$; the finite window selects only the interval of length $T = N\Delta t$.*

## 2. Fourier theory and the discrete Fourier transform

### 2.1 Three forms of Fourier analysis

Fourier analysis comes in three flavours, depending on whether the signal is continuous or discrete and whether it is periodic or not:

- **Continuous periodic signal** $\to$ Fourier series: discrete frequencies, continuous time.
- **Continuous non-periodic signal** $\to$ Fourier transform: continuous frequencies, continuous time.
- **Discrete finite signal** $\to$ discrete Fourier transform (DFT): discrete frequencies, discrete time.

Seismic data are finite and sampled, so the DFT is the form we use in practice. We will keep the continuous forms as a one-slide mental map and focus on the DFT.

### 2.2 The DFT definition

For a digital trace $x[n]$ with $N$ samples, the DFT is

$$
X[k] = \sum_{n=0}^{N-1} x[n] \, e^{-i 2\pi k n / N}, \qquad k = 0, \dots, N-1.
$$

The inverse DFT recovers the original samples exactly:

$$
x[n] = \frac{1}{N} \sum_{k=0}^{N-1} X[k] \, e^{i 2\pi k n / N}, \qquad n = 0, \dots, N-1.
$$

The frequency of bin $k$ is

$$
f_k = \frac{k}{N\Delta t} = \frac{k}{T},
$$

so the frequency spacing is

$$
\Delta f = \frac{1}{T} = \frac{1}{N\Delta t}.
$$

A longer record gives finer frequency resolution.

### 2.3 DFT properties

- **Periodicity**: $X[k+N] = X[k]$. The DFT produces $N$ bins but the spectrum repeats every $N$ bins.
- **Real-signal symmetry**: for a real-valued trace, $X[-k] = X^*[k]$. Only bins $0$ to $N/2$ are independent.
- **DC and Nyquist**: bin $0$ is the zero-frequency (DC) component; bin $N/2$ is the Nyquist frequency $f_N = 1/(2\Delta t)$.
- **FFT**: the fast Fourier transform is not a different transform; it is simply a fast algorithm for computing the DFT.

The step-by-step derivation of DFT periodicity and spectral leakage is given in `lecture_notes/derivations/dft_and_spectral_leakage_derivation.en.md`.

![](figures/term01_lec05/term01_lec05_fourier_pairs.png){width=90%}

**Figure 2.** *A time-domain pulse and its amplitude spectrum. The continuous transform is a smooth function; the DFT samples that function at the discrete frequencies $f_k = k/T$.*

![](figures/term01_lec05/term01_lec05_dft_periodicity.png){width=90%}

**Figure 3.** *DFT periodicity and real-signal symmetry. The spectrum repeats every $N$ bins, and for a real trace the negative-frequency part is the complex conjugate of the positive-frequency part.*

## 3. Spectral analysis

### 3.1 The convolutional spectrum model

A single seismic trace is often approximated by

$$
x(t) = w(t) * r(t) + n(t),
$$

where $w(t)$ is the embedded wavelet, $r(t)$ is the reflectivity, and $n(t)$ is noise. In the frequency domain convolution becomes multiplication:

$$
X(f) = W(f) \, R(f) + N(f).
$$

Each convolutional component therefore contributes its own multiplicative factor to the spectrum. The source signature, ghosts, instrument response, absorption, and the reflectivity all leave separate fingerprints.

### 3.2 Effects of discretization and finite length

A real digital trace is both sampled and finite. The two effects are:

- **Sampling** makes the spectrum periodic with period $f_s = 1/\Delta t$. The spectrum is repeated at multiples of the sampling frequency; if these copies overlap, aliasing occurs.
- **Finite length** is equivalent to multiplying the infinite trace by a rectangular window. In the frequency domain this is a convolution with the window's spectrum, which is a sinc function. The result is **spectral leakage**: a single frequency is no longer a sharp line but a broad sinc-shaped peak, and adjacent frequencies leak into one another.

Frequency resolution is limited by the record length:

$$
\Delta f = \frac{1}{T}.
$$

Two frequencies closer than $1/T$ cannot be separated.

![](figures/term01_lec05/term01_lec05_spectral_leakage.png){width=90%}

**Figure 4.** *Spectral leakage. A single cosine observed through a finite rectangular window has a sinc-shaped spectrum; its energy leaks into neighbouring frequency bins.*

### 3.3 Amplitude and phase spectra

The DFT coefficient $X[k]$ is complex. Its magnitude $|X[k]|$ is the **amplitude spectrum**; its angle $\arg(X[k])$ is the **phase spectrum**. Two wavelets can have the same amplitude spectrum but very different shapes because their phase spectra differ. This is why phase is a central topic in deconvolution.

### 3.4 Power spectrum

The power spectrum is $|X(f)|^2$. It is also the Fourier transform of the autocorrelation of the trace (the Wiener–Khinchin theorem). This older route was once preferred because the autocorrelation is less sensitive to noise; with the FFT, direct computation from the DFT is now more common.

## 4. Aliasing

### 4.1 The Nyquist criterion

If a sinusoid is sampled at interval $\Delta t$, the highest frequency that can be uniquely represented is the **Nyquist frequency**:

$$
f_N = \frac{1}{2\Delta t}.
$$

A sinusoid must be sampled at least twice per cycle. For a 4 ms sample interval, $f_N = 125$ Hz.

### 4.2 What happens above Nyquist

Any frequency $f > f_N$ folds back into the principal band and appears as an **alias frequency**:

$$
f_{\text{apparent}} = |f - k f_s|,
$$

where $k$ is the integer that brings the result into the band $[0, f_N]$. For example, a 150 Hz sinusoid sampled at 4 ms has apparent frequency

$$
f_{\text{apparent}} = |150 - 250| = 100\ \text{Hz}.
$$

Once aliased, the true frequency cannot be recovered from the digital data.

### 4.3 Anti-alias protection in the field

Field recording systems apply an analog **anti-alias filter** before digitization to remove energy above the Nyquist. Properly recorded seismic data are therefore usually not aliased in time. The filter is not perfect, so a small safety margin is left between the desired signal band and the Nyquist frequency.

### 4.4 Aliasing risks in processing

Aliasing can reappear whenever the sampling rate is changed:

- **Decimation** (downsampling) must be preceded by a low-pass filter.
- **Interpolation** must not create frequencies above the new Nyquist.
- **Resampling** in modelling or migration must keep the desired frequency band inside the new Nyquist.

The rule is: the data are already dealiased when they arrive, but every processing step that changes the sample interval must re-apply anti-alias protection.

![](figures/term01_lec05/term01_lec05_aliasing.png){width=90%}

**Figure 5.** *Aliasing. A high-frequency sinusoid sampled too coarsely appears as a lower-frequency alias. The spectrum on the right shows the high-frequency energy folding back into the principal band below the Nyquist frequency.*

## 5. Frequency filtering

### 5.1 What filtering is

Filtering modifies one time series by another. In the frequency domain this means multiplying the trace spectrum by the filter spectrum; in the time domain it means convolving the trace with the filter impulse response. The two views are equivalent because of the convolution theorem.

Seismic filtering is usually multiplicative in frequency: the amplitude spectrum is shaped, and the phase is either left unchanged (zero-phase filter) or adjusted to keep the filter causal.

### 5.2 Common filter types

| Type | What it keeps | Typical seismic use |
|------|---------------|---------------------|
| **Low-pass** | Frequencies below cutoff | Smoothing, anti-alias pre-filtering |
| **High-pass** | Frequencies above cutoff | Removing ground roll or low-frequency drift |
| **Band-pass** | Frequencies between two cutoffs | Isolating the reflection signal band |
| **Notch / reject** | Everything except a narrow band | Suppressing 50/60 Hz power-line interference |

The cutoffs are usually specified at the $-3$ dB point, where the power is half the passband level.

![](figures/term01_lec05/term01_lec05_filter_types.png){width=90%}

**Figure 6.** *Amplitude spectra of low-pass, high-pass, band-pass, and notch filters. The shaded areas are the passbands; the transition regions are the slopes between passband and stopband.*

### 5.3 Filter slope and the Gibbs phenomenon

An ideal filter with a perfectly sharp cutoff has an infinitely long impulse response (a sinc function). In practice we truncate it to a finite length. Truncation causes two problems:

- **Gibbs ringing**: oscillations near sharp transitions in the time domain.
- **Sidelobes**: unwanted pass-through of stopband frequencies.

Longer filters give steeper slopes and lower sidelobes, but they cost more computation and can amplify noise. Applying a tapered window (Hamming, Hanning, Blackman) reduces ringing at the cost of a slightly wider transition band.

![](figures/term01_lec05/term01_lec05_gibbs.png){width=90%}

**Figure 7.** *Gibbs phenomenon. Truncating an ideal sharp filter to a finite length produces ringing in the time domain. Longer filters reduce the ringing but increase the filter length and computational cost.*

### 5.4 Filtering a CMP gather

A practical use of band-pass filtering is to remove low-frequency ground roll while preserving the reflection signal. The figure below shows a synthetic CMP gather before and after a band-pass filter. The low-frequency noise dominates the shallow, far-offset traces before filtering; after filtering the reflection events are clearer.

![](figures/term01_lec05/term01_lec05_filter_gather.png){width=90%}

**Figure 8.** *Band-pass filtering of a synthetic CMP gather. Left: gather with low-frequency noise (ground roll). Right: after filtering, the reflection events are visible while the low-frequency noise is suppressed.*

### 5.5 FIR and IIR filters

- **FIR (finite impulse response)** filters are non-recursive, finite in length, and can be designed with linear phase. They are common in seismic processing because phase distortion is easy to control.
- **IIR (infinite impulse response)** filters are recursive, causal, and compact but introduce phase distortion. They are used when a smooth, steep response is needed with a short operator.

A **Butterworth** filter is the classic IIR example. Its amplitude response is maximally flat in the passband and rolls off smoothly in the stopband.

### 5.6 Butterworth filter: a numerical example

For a Butterworth low-pass filter of order $n$ and cutoff $f_c$, the squared amplitude response is

$$
|H(f)|^2 = \frac{1}{1 + \left(f / f_c\right)^{2n}}.
$$

At the cutoff frequency, $|H(f_c)| = 1/\sqrt{2}$, which is $-3$ dB. Higher order means a steeper slope but a longer effective impulse response.

**Example.** Let the cutoff be $f_c = 60$ Hz and the sample interval be $\Delta t = 4$ ms (Nyquist $f_N = 125$ Hz). The amplitude at several frequencies is:

| Frequency | $n = 2$ | $n = 4$ | $n = 8$ |
|-----------|---------|---------|---------|
| 60 Hz (cutoff) | $-3.0$ dB | $-3.0$ dB | $-3.0$ dB |
| 90 Hz | $-8.5$ dB | $-16.0$ dB | $-31.0$ dB |
| 120 Hz | $-12.3$ dB | $-24.1$ dB | $-48.1$ dB |

A 2nd-order filter attenuates only gently near the Nyquist; an 8th-order filter gives strong attenuation but its impulse response is longer and contains more ringing. In practice one chooses the lowest order that gives the required attenuation at the Nyquist or at the target stopband edge.

![](figures/term01_lec05/term01_lec05_butterworth.png){width=90%}

**Figure 9.** *Butterworth low-pass amplitude responses for orders $n = 2$, $4$, and $8$ with cutoff $f_c = 60$ Hz. Higher order gives a steeper slope but a longer impulse response and more ringing.*

### 5.7 Time-variant filters

Because high frequencies are attenuated more rapidly than low frequencies as the wave travels, the useful signal band often shifts toward lower frequencies with increasing record time. A **time-variant filter** uses different passbands in different time windows (e.g., a wider band at shallow times and a narrower band at deeper times). The concept is common in processing, but the detailed design is usually handled by the processing software.

## Summary

- A digital seismic trace is finite and sampled; its DFT spectrum is periodic because of sampling and smeared because of finite length.
- Frequency resolution is limited by record length: $\Delta f = 1/T$.
- The Nyquist frequency $f_N = 1/(2\Delta t)$ is the highest frequency that can be represented without aliasing; energy above it folds back into the principal band.
- Field recording uses anti-alias filters before digitization; processing steps that change the sample interval must re-apply anti-alias protection.
- Spectral analysis uses the convolutional spectrum model: the trace spectrum is the product of the wavelet, reflectivity, and noise spectra, modified by windowing and sampling effects.
- Frequency filters shape the amplitude spectrum; common types are low-pass, high-pass, band-pass, and notch.
- Truncating an ideal filter causes Gibbs ringing; longer filters give steeper slopes but more ringing and more noise amplification.
- Butterworth filters are smooth, causal IIR filters; higher order gives steeper slope but longer response.
- Time-variant filters adapt the passband to the changing frequency content of the signal with record time.

## Comprehension questions

1. A seismic trace is recorded with a 4 ms sample interval. What is the Nyquist frequency? What happens to a 150 Hz component in the recorded data?
2. Why does a finite-length window cause a pure frequency to appear spread out in the frequency domain?
3. In the convolutional spectrum model, how does the source signature affect the amplitude spectrum of the recorded trace?
4. Why must a low-pass filter be applied before decimating (downsampling) seismic data?
5. Name one processing situation where a high-pass filter is useful and one where a notch filter is useful.
6. What is the Gibbs phenomenon, and why does it force a trade-off between filter steepness and filter length?
7. Using the Butterworth example with $f_c = 60$ Hz, how much more attenuation does an 8th-order filter give at 120 Hz compared with a 2nd-order filter?
8. Why might a time-variant band-pass filter be used on a deep seismic section?

## Further reading

- Hatton, Worthington & Makin (1986), *Seismic Data Processing: Theory and Practice*, Ch. 2.2–2.5, 2.9 — Fourier theory, DFT, aliasing, filtering, and spectral analysis.
- Margrave (2006), *Methods of Seismic Data Processing*, Ch. 2 — convolution, Fourier transforms, DFT, sampling, filtering, and spectral estimation.
- Yilmaz, *Practical Seismic Data Analysis*, Ch. 1.2–1.3.1 — sampled time series, aliasing, and Fourier amplitude spectrum.
- Step-by-step derivation: `lecture_notes/derivations/dft_and_spectral_leakage_derivation.en.md`.
