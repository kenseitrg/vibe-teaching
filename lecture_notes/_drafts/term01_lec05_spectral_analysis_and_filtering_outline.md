# Term 1 Lecture 05 — Spectral Analysis and Frequency Filtering

## Scope

This lecture builds the signal-processing foundation used in every later processing step. It moves from the recorded seismic trace as a finite digital time series to the frequency-domain ideas needed to understand and design filters.

The lecture covers:

1. The seismic trace model: from continuous analog signal to finite, sampled digital data.
2. A brief Fourier-theory recap: continuous, discrete, and finite-length signals; the DFT and its properties.
3. Spectral analysis: the convolutional spectrum model, spectral leakage, and periodicity of the discrete spectrum.
4. Aliasing: the Nyquist criterion and why it matters in acquisition and in processing resampling.
5. Frequency filtering: filter types, the Gibbs phenomenon, the slope-vs-length trade-off, and IIR filters (Butterworth example).

Prerequisites are Term 1 Lecture 01 (the recorded trace as a convolutional signal) and basic undergraduate signal-processing ideas: sinusoids, amplitude, phase, and the idea of a spectrum.

## Learning objectives

By the end of this lecture students should be able to:

- Describe a seismic trace as a finite, sampled version of a continuous signal and list the consequences of sampling and finite length.
- State the forward and inverse DFT in words, and explain periodicity, frequency resolution, and real-signal symmetry.
- Use the convolutional spectrum model: trace spectrum = product of wavelet, reflectivity, and noise spectra plus the effects of windowing and sampling.
- Define the Nyquist frequency and predict aliased frequencies for a given sample interval.
- Explain why anti-alias filtering is needed before digitization and before downsampling in processing.
- Distinguish low-pass, high-pass, band-pass, and notch filters and give a typical seismic use case for each.
- Describe the Gibbs phenomenon and the trade-off between filter transition steepness and filter length.
- Sketch the amplitude response of a Butterworth filter and explain why it is smooth and causal.
- Recognize that time-variant filters are sometimes used because the useful signal band changes with record time.

## Prerequisites

- Term 1 Lecture 01: the recorded trace, convolutional model, source/receiver geometry.
- Basic sinusoids, amplitude, phase, and complex exponentials from a companion signal-processing course.
- Comfort with summation notation and simple complex numbers.

## Timing (90 minutes)

| Section | Time | Notes |
|---------|------|-------|
| 1. Seismic trace model | 10 min | Analog → sampled → finite; sample interval and record length |
| 2. Fourier theory recap | 20 min | Continuous vs. discrete; DFT definition and properties |
| 3. Spectral analysis | 20 min | Convolutional spectrum model; leakage and periodicity |
| 4. Aliasing | 15 min | Nyquist criterion; field anti-alias; processing resampling |
| 5. Frequency filtering | 25 min | Filter types, Gibbs, slope vs. length, Butterworth |
| Total | 90 min | Tight; keep the Fourier review focused on the discrete case |

## Section 1 — Seismic trace model: from analog to finite digital data

- A recorded seismic trace is originally a continuous analog signal in time.
- Field digitization: anti-alias analog filter → sample-and-hold → analog-to-digital converter.
- Sample interval $\Delta t$: typically 1, 2, or 4 ms; high-resolution surveys may use 0.5 or 0.25 ms.
- Record length $T$ and number of samples $N$: $T = N\Delta t$.
- Consequences of the digital representation:
  - Finite length $\Rightarrow$ limited frequency resolution and spectral leakage.
  - Discrete sampling $\Rightarrow$ periodic spectrum and possible aliasing.
- Figure needed: continuous analog signal, sampling instants, finite window, and the resulting discrete sequence.

## Section 2 — Brief Fourier theory recap and the DFT

- Fourier idea: decompose a signal into sinusoids with amplitude and phase.
- Three situations:
  - Continuous periodic $\to$ Fourier series (discrete frequencies, continuous time).
  - Continuous non-periodic $\to$ Fourier transform (continuous frequencies).
  - Discrete finite $\to$ DFT (discrete frequencies, discrete time).
- Seismic data use the DFT, so focus on that case.
- DFT definition (in words): each frequency sample is the sum of the time samples weighted by a complex exponential.
- Inverse DFT recovers the original $N$ samples exactly.
- Frequency resolution: $\Delta f = 1/(N\Delta t) = 1/T$.
- DFT periodicity: $X[k+N] = X[k]$; spectrum repeats every $f_s = 1/\Delta t$.
- Real-signal symmetry: for a real trace, negative frequencies are conjugates; only $0$ to $N/2$ are independent.
- $k=0$ is DC; $k=N/2$ is the Nyquist frequency.
- Figure needed: time-domain pulse and its amplitude/phase spectrum; illustrate periodic repetition of the spectrum.

## Section 3 — Spectral analysis: the convolutional spectrum model

- The convolutional model in frequency domain:

  $$X(f) = W(f)\,R(f) + N(f)$$

  (plus source ghost, receiver ghost, instrument response, absorption effects).
- Each convolutional component becomes a multiplicative factor in the spectrum.
- Effects of finite length:
  - Multiplying by a rectangular window in time is convolution with a sinc function in frequency.
  - Spectral leakage: a pure frequency spreads into neighboring bins.
  - Frequency resolution $\Delta f = 1/T$ limits how close two frequencies can be separated.
- Effects of sampling:
  - The spectrum becomes periodic with period $f_s = 1/\Delta t$.
  - Frequencies above Nyquist fold back into the principal band (aliasing — covered in §4).
- Amplitude and phase spectra:
  - Amplitude spectrum: energy distribution vs. frequency.
  - Phase spectrum: timing of each frequency component.
- Power spectrum: $|X(f)|^2$ or Fourier transform of autocorrelation.
- Practical uses: filter design, QC, comparing wavelet spectra, identifying noise bands.
- Figure needed: a single-frequency sinusoid in a finite window and its leaked sinc-shaped spectrum; also the convolutional spectrum model diagram.

## Section 4 — Aliasing and the Nyquist criterion

- Nyquist frequency: $f_N = 1/(2\Delta t)$.
- A sinusoid must be sampled at least twice per cycle to be uniquely determined.
- If $f > f_N$, the apparent frequency is $f_{\text{apparent}} = |f - k f_s|$ for the integer $k$ that brings it into the principal band.
- Example: at 4 ms sampling, $f_N = 125$ Hz; a 150 Hz signal aliases to 100 Hz.
- Anti-alias protection in the field:
  - Analog anti-alias filter before the ADC removes energy above the Nyquist.
  - This is why properly recorded data are usually not aliased in time.
- Aliasing risks in processing:
  - Decimation (downsampling) must be preceded by a low-pass filter.
  - Interpolation and resampling must respect the new Nyquist frequency.
  - Modelling or migration can introduce implicit resampling; keep the frequency band inside the Nyquist.
- Figure needed: a high-frequency sinusoid sampled too coarsely and the apparent low-frequency alias; also a spectrum showing fold-back.

## Section 5 — Frequency filtering

- Filtering = modifying one time series by another (convolution in time, multiplication in frequency).
- In seismic processing, filters are usually designed in the frequency domain and applied by convolution or FFT multiplication.
- Common filter types:
  - **Low-pass**: keep frequencies below cutoff; used for smoothing or anti-alias pre-filtering.
  - **High-pass**: keep frequencies above cutoff; used to remove ground roll or low-frequency drift.
  - **Band-pass**: keep frequencies between two cutoffs; the most common reflection-signal filter.
  - **Notch / reject**: remove a narrow frequency band; e.g., 50/60 Hz power-line interference.
- Filter parameters:
  - Cutoff frequency (often at -3 dB / half-power point).
  - Passband and stopband.
  - Transition band and slope (dB per octave).
- Ideal filter vs. real filter:
  - Ideal brick-wall filter has infinite length in time (sinc function).
  - Truncating to finite length creates the Gibbs phenomenon: ringing (sidelobes) near sharp transitions.
- Trade-off:
  - Longer filter $\to$ steeper slope, lower sidelobes, but more computation and more noise amplification.
  - Shorter filter $\to$ gentler slope, less ringing, but poorer frequency selectivity.
- Windowing (e.g., Hamming, Blackman) reduces ringing at the cost of a slightly wider transition band.
- FIR vs. IIR:
  - FIR: finite impulse response, non-recursive, can have linear phase, stable.
  - IIR: infinite impulse response, recursive, causal, compact, but phase distortion.
- Butterworth filter example:
  - Maximally flat amplitude response in the passband.
  - Smooth monotonic roll-off; no ripple.
  - Squared amplitude response: $|H(f)|^2 = 1 / (1 + (f/f_c)^{2n})$, where $n$ is the order.
  - Higher order = steeper slope but longer effective impulse response.
  - Numerical example: $f_c = 60$ Hz, $\Delta t = 4$ ms, orders $n = 2, 4, 8$; show dB attenuation at 60, 90, 120 Hz.
- Filtering a CMP gather: band-pass filter removes low-frequency ground roll while preserving reflections.
- Time-variant filters: brief mention that the useful signal band shifts toward lower frequencies with record time; filters can adapt accordingly.
- Figures needed: amplitude spectra of the four filter types; Gibbs ringing for different filter lengths; Butterworth responses of several orders; CMP gather before and after filtering.

## Figures to generate

| Figure | Script | Output |
|--------|--------|--------|
| Trace model: analog → sampled → finite | `plot_trace_model.py` | `term01_lec05_trace_model.png` |
| Fourier transform pairs (time pulse and spectrum) | `plot_fourier_pairs.py` | `term01_lec05_fourier_pairs.png` |
| DFT periodicity and real-signal symmetry | `plot_dft_periodicity.py` | `term01_lec05_dft_periodicity.png` |
| Spectral leakage from finite window | `plot_spectral_leakage.py` | `term01_lec05_spectral_leakage.png` |
| Aliasing example | `plot_aliasing.py` | `term01_lec05_aliasing.png` |
| Filter types (low-pass, high-pass, band-pass, notch) | `plot_filter_types.py` | `term01_lec05_filter_types.png` |
| Gibbs phenomenon and filter length | `plot_gibbs.py` | `term01_lec05_gibbs.png` |
| Band-pass filtering of a CMP gather | `plot_filter_gather.py` | `term01_lec05_filter_gather.png` |
| Butterworth filter example (orders 2,4,8) | `plot_butterworth.py` | `term01_lec05_butterworth.png` |

## Key equations to include

- DFT forward and inverse (summation form).
- Frequency resolution: $\Delta f = 1/(N\Delta t) = 1/T$.
- Convolution theorem: $x(t) * w(t) \;\leftrightarrow\; X(f)\,W(f)$.
- Nyquist frequency: $f_N = 1/(2\Delta t)$.
- Aliased apparent frequency: $f_{\text{apparent}} = |f - k f_s|$ (with $k$ chosen so the result lies in $[0, f_N]$).
- Butterworth squared amplitude response: $|H(f)|^2 = 1 / (1 + (f/f_c)^{2n})$.

## Comprehension questions

1. A seismic trace is recorded with a 4 ms sample interval. What is the Nyquist frequency? What happens to a 150 Hz component in the recorded data?
2. Why does a finite-length window cause a pure frequency to appear spread out in the frequency domain?
3. In the convolutional spectrum model, how does the source signature affect the amplitude spectrum of the recorded trace?
4. Why must a low-pass filter be applied before decimating (downsampling) seismic data?
5. Name one processing situation where a high-pass filter is useful and one where a notch filter is useful.
6. What is the Gibbs phenomenon, and why does it force a trade-off between filter steepness and filter length?
7. How does a higher-order Butterworth filter change the amplitude response and the time-domain impulse response?
8. Why might a time-variant band-pass filter be used on a deep seismic section?

## Links to wiki concepts

- `wiki/concepts/spectral_analysis.md` — frequency content of traces and wavelets.
- `wiki/concepts/frequency_filtering.md` — filter types, Gibbs, slope vs. length, Butterworth.
- `wiki/concepts/discrete_fourier_transform.md` — DFT and its properties.
- `wiki/concepts/aliasing.md` — Nyquist sampling and alias folding.
- `wiki/concepts/seismic_wavelet.md` — components of the recorded wavelet that shape the spectrum.

## Sources to ingest / reference

- `papers/general/geokniga-xatton-l-uerdington-m-mejkin-dzh-obrabotka-sejsmicheskix-dannyx-teoriya-i-p.djv` (Hatton, Worthington & Makin, Ch. 2.2–2.5, 2.9) — Fourier theory, DFT, aliasing, filtering, spectral analysis.
- `papers/textbooks/Methods of Seismic Data Processing.pdf` (Margrave, Chapter 2) — convolution, Fourier transforms, DFT, sampling, filtering, spectral estimation.
- `papers/textbooks/Yilmaz - Seismic Data Analysis_1.pdf` (Ch. 1.2–1.3.1) — sampled time series, aliasing, Fourier amplitude spectrum.
- `slides/raw/term01_lecture05_spectral_analysis_filters.docx` and `.pptx` — existing lecture plan and slides.

## Derivation documents needed

- A short derivation covering DFT periodicity, real-signal symmetry, and why finite windowing causes spectral leakage (convolution with a sinc function). Suggested file: `lecture_notes/derivations/dft_and_spectral_leakage_derivation.en.md`.

## Resolved questions

- One-slide overview of continuous Fourier theory is sufficient; focus on DFT.
- Butterworth filter includes a worked numerical example with dB values.
- Filtering demonstrated on a synthetic CMP gather (low-frequency noise vs. reflections).
- Time-variant filters mentioned briefly as a concept only.
