# Slide outline: Term 1 Lecture 5 — Spectral Analysis and Frequency Filtering

## Slide 1 — Title
- Title: Spectral analysis and frequency filtering
- Subtitle: Term 1, Lecture 5

## Slide 2 — Learning objectives
- List 9 learning objectives from the lecture notes.

## Slide 3 — Seismic trace model: from analog to digital
- A seismic trace starts as a continuous analog signal.
- At the recording station it is anti-alias filtered, sampled, and stored as a finite list of numbers.
- Two fundamental limitations:
  - **Discrete sampling**: only values at $t = n\Delta t$ are kept.
  - **Finite length**: only a window of length $T = N\Delta t$ is kept.
- Typical values: $\Delta t = 1$, $2$, or $4$ ms; $T = 2$–$8$ s; $N = 1000$–$16000$.
- Sampling makes the spectrum periodic; finite length smears the spectrum.

## Slide 4 — From analog to digital (figure)
- Figure: `term01_lec05_trace_model.png`

## Slide 5 — Three forms of Fourier analysis
- **Continuous periodic signal** → Fourier series: discrete frequencies, continuous time.
- **Continuous non-periodic signal** → Fourier transform: continuous frequencies, continuous time.
- **Discrete finite signal** → DFT: discrete frequencies, discrete time.
- Seismic data are finite and sampled, so we use the DFT.

## Slide 6 — The DFT definition
- For a digital trace $x[n]$ with $N$ samples:
  - $X[k] = \sum_{n=0}^{N-1} x[n] \, e^{-i 2\pi k n / N}$
- Frequency of bin $k$: $f_k = k / (N\Delta t) = k / T$.
- Frequency spacing: $\Delta f = 1/T = 1/(N\Delta t)$.
- Longer record → finer frequency resolution.

## Slide 7 — DFT properties
- **Periodicity**: $X[k+N] = X[k]$. Spectrum repeats every $N$ bins.
- **Real-signal symmetry**: for a real trace, $X[-k] = X^*[k]$. Only bins $0$ to $N/2$ are independent.
- **DC and Nyquist**: bin $0$ is DC; bin $N/2$ is Nyquist $f_N = 1/(2\Delta t)$.
- **FFT**: not a different transform; just a fast algorithm for computing the DFT.

## Slide 8 — Fourier pairs and DFT sampling (figure)
- The continuous Fourier transform is a smooth function; the DFT samples it at discrete frequencies $f_k = k/T$.
- Figure: `term01_lec05_fourier_pairs.png`

## Slide 9 — DFT periodicity and symmetry (figure)
- Figure: `term01_lec05_dft_periodicity.png`

## Slide 10 — The convolutional spectrum model
- A single seismic trace: $x(t) = w(t) * r(t) + n(t)$.
- In frequency domain: $X(f) = W(f) \, R(f) + N(f)$.
- Each component contributes its own multiplicative factor to the spectrum.
- Source signature, ghosts, instrument response, absorption, and reflectivity all leave separate fingerprints.

## Slide 11 — Effects of discretization and finite length
- **Sampling** makes the spectrum periodic with period $f_s = 1/\Delta t$. If copies overlap → aliasing.
- **Finite length** = multiplying by a rectangular window → convolution with sinc in frequency domain → **spectral leakage**.
- Frequency resolution: $\Delta f = 1/T$. Two frequencies closer than $1/T$ cannot be separated.

## Slide 12 — Spectral leakage (figure)
- Figure: `term01_lec05_spectral_leakage.png`

## Slide 13 — Amplitude and phase spectra
- $X[k]$ is complex.
- Magnitude $|X[k]|$ = amplitude spectrum.
- Angle $\arg X[k]$ = phase spectrum.
- Two wavelets can have the same amplitude spectrum but very different shapes because their phase spectra differ.
- Power spectrum: $|X(f)|^2$ = Fourier transform of autocorrelation (Wiener–Khinchin theorem).

## Slide 14 — Aliasing: the Nyquist criterion
- Nyquist frequency: $f_N = 1/(2\Delta t)$.
- A sinusoid must be sampled at least twice per cycle.
- For $\Delta t = 4$ ms, $f_N = 125$ Hz.

## Slide 15 — What happens above Nyquist
- Any frequency $f > f_N$ folds back: $f_{\text{apparent}} = |f - k f_s|$.
- Example: 150 Hz sampled at 4 ms → apparent frequency $|150 - 250| = 100$ Hz.
- Once aliased, the true frequency cannot be recovered.

## Slide 16 — Anti-alias protection
- Field systems apply an analog anti-alias filter before digitization.
- Every processing step that changes $\Delta t$ must re-apply anti-alias protection:
  - Decimation must be preceded by a low-pass filter.
  - Interpolation must not create frequencies above the new Nyquist.
  - Resampling in modelling or migration must respect the new Nyquist.

## Slide 17 — Aliasing (figure)
- Figure: `term01_lec05_aliasing.png`

## Slide 18 — Frequency filtering: what it is
- Filtering = multiplying trace spectrum by filter spectrum (frequency domain).
- Equivalent to convolving trace with filter impulse response (time domain).
- Seismic filtering is usually multiplicative in frequency.
- Phase is either left unchanged (zero-phase) or adjusted to keep the filter causal.

## Slide 19 — Common filter types
| Type | What it keeps | Typical seismic use |
|------|---------------|---------------------|
| Low-pass | Frequencies below cutoff | Smoothing, anti-alias pre-filtering |
| High-pass | Frequencies above cutoff | Removing ground roll or low-frequency drift |
| Band-pass | Frequencies between two cutoffs | Isolating the reflection signal band |
| Notch / reject | Everything except a narrow band | Suppressing 50/60 Hz power-line interference |
- Cutoffs specified at the $-3$ dB point (half the passband power).

## Slide 20 — Filter types (figure)
- Figure: `term01_lec05_filter_types.png`

## Slide 21 — The Gibbs phenomenon
- An ideal sharp filter has an infinitely long impulse response (sinc).
- Truncation causes:
  - **Gibbs ringing**: oscillations near sharp transitions.
  - **Sidelobes**: unwanted pass-through of stopband frequencies.
- Trade-off: longer filters → steeper slopes but more computation and noise amplification.

## Slide 22 — Gibbs phenomenon (figure)
- Figure: `term01_lec05_gibbs.png`

## Slide 23 — Filtering a CMP gather
- Band-pass filtering removes low-frequency ground roll while preserving reflections.
- Example: synthetic CMP gather before and after a 15–60 Hz band-pass filter.
- Low-frequency noise dominates shallow, far-offset traces before filtering.
- After filtering, reflection events are clearer.

## Slide 24 — CMP gather filtering (figure)
- Figure: `term01_lec05_filter_gather.png`

## Slide 25 — FIR and IIR filters
- **FIR (finite impulse response)**: non-recursive, finite length, linear phase. Common in seismic processing.
- **IIR (infinite impulse response)**: recursive, causal, compact but introduces phase distortion.
- **Butterworth** is the classic IIR example: maximally flat in passband, smooth roll-off.

## Slide 26 — Butterworth filter: the formula
- Squared amplitude response: $|H(f)|^2 = 1 / (1 + (f/f_c)^{2n})$.
- At cutoff: $|H(f_c)| = 1/\sqrt{2}$ → $-3$ dB.
- Higher order → steeper slope but longer impulse response.

## Slide 27 — Butterworth example
- $f_c = 60$ Hz, $\Delta t = 4$ ms ($f_N = 125$ Hz).

| Frequency | $n = 2$ | $n = 4$ | $n = 8$ |
|-----------|---------|---------|---------|
| 60 Hz (cutoff) | $-3.0$ dB | $-3.0$ dB | $-3.0$ dB |
| 90 Hz | $-8.5$ dB | $-16.0$ dB | $-31.0$ dB |
| 120 Hz | $-12.3$ dB | $-24.1$ dB | $-48.1$ dB |

## Slide 28 — Butterworth responses (figure)
- Figure: `term01_lec05_butterworth.png`

## Slide 29 — Time-variant filters
- High frequencies are attenuated more rapidly with travel distance.
- Useful signal band shifts toward lower frequencies with record time.
- Time-variant filter: different passbands in different time windows.
  - Wider band at shallow times, narrower band at deeper times.
- Detailed design is usually handled by processing software.

## Slide 30 — Summary
- Digital seismic trace is finite and sampled; DFT spectrum is periodic (sampling) and smeared (finite length).
- Frequency resolution: $\Delta f = 1/T$.
- Nyquist frequency $f_N = 1/(2\Delta t)$: highest representable frequency without aliasing.
- Field recording uses anti-alias filters; every processing step that changes $\Delta t$ must re-apply protection.
- Spectral analysis uses the convolutional spectrum model.
- Frequency filters shape the amplitude spectrum; common types: low-pass, high-pass, band-pass, notch.
- Truncating an ideal filter causes Gibbs ringing; trade-off between steepness and length.
- Butterworth filters: smooth, causal IIR; higher order → steeper slope, longer response.
- Time-variant filters adapt passband to changing frequency content with record time.

## Slide 31 — Comprehension questions
1. A seismic trace is recorded with a 4 ms sample interval. What is the Nyquist frequency? What happens to a 150 Hz component?
2. Why does a finite-length window cause a pure frequency to appear spread out in the frequency domain?
3. In the convolutional spectrum model, how does the source signature affect the amplitude spectrum?
4. Why must a low-pass filter be applied before decimating seismic data?
5. Name one processing situation where a high-pass filter is useful and one where a notch filter is useful.
6. What is the Gibbs phenomenon, and why does it force a trade-off between filter steepness and filter length?
7. Using the Butterworth example with $f_c = 60$ Hz, how much more attenuation does an 8th-order filter give at 120 Hz compared with a 2nd-order filter?
8. Why might a time-variant band-pass filter be used on a deep seismic section?

## Slide 32 — References
- Yilmaz (2001), Margrave (2006), Hill & Rüger (2020), Verschuur (2006), CGG ODT01.
