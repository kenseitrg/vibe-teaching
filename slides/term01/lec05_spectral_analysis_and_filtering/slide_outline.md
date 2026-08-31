# Slide outline — Term 1, Lecture 5: Spectral analysis and frequency filtering

---

## Slide 1 — Spectral analysis and frequency filtering
- Term 1, Lecture 5
- Figure: none

---

## Slide 2 — Learning objectives
- Describe a seismic trace as a finite, sampled version of a continuous signal.
- State the DFT and explain periodicity, frequency resolution, and real-signal symmetry.
- Use the convolutional spectrum model: trace spectrum = product of wavelet, reflectivity, and noise spectra.
- Define the Nyquist frequency and predict aliased frequencies.
- Explain why anti-alias filtering is needed before digitization and downsampling.
- Distinguish low-pass, high-pass, band-pass, and notch filters.
- Describe the Gibbs phenomenon and the trade-off between filter steepness and length.
- Sketch a Butterworth amplitude response.
- Recognize that time-variant filters adapt to changing signal bandwidth.

---

## Slide 3 — Seismic trace model: from analog to digital
- A seismic trace starts as a continuous analog signal in time.
- At the recording station it is anti-alias filtered, sampled, and stored as a finite list of numbers.
- Two fundamental limitations:
  - **Discrete sampling**: only values at $t = n\Delta t$ are kept.
  - **Finite length**: only a window of length $T = N\Delta t$ is kept.
- Typical values: $\Delta t = 1$, $2$, or $4$ ms; $T = 2$–$8$ s; $N = 1000$–$16000$.
- Sampling makes the spectrum periodic; finite length smears the spectrum.
- Figure: `term01_lec05_trace_model.png`

---

## Slide 4 — Three forms of Fourier analysis
- **Continuous periodic signal** → Fourier series: discrete frequencies, continuous time.
- **Continuous non-periodic signal** → Fourier transform: continuous frequencies, continuous time.
- **Discrete finite signal** → DFT: discrete frequencies, discrete time.
- Seismic data are finite and sampled, so we use the DFT.

---

## Slide 5 — The DFT definition
- For a digital trace $x[n]$ with $N$ samples:
  - $X[k] = \sum_{n=0}^{N-1} x[n] \, e^{-i 2\pi k n / N}$
- Frequency of bin $k$: $f_k = k / (N\Delta t) = k / T$.
- Frequency spacing: $\Delta f = 1/T = 1/(N\Delta t)$.
- Longer record → finer frequency resolution.

---

## Slide 6 — DFT properties
- **Periodicity**: $X[k+N] = X[k]$. Spectrum repeats every $N$ bins.
- **Real-signal symmetry**: for a real trace, $X[-k] = X^*[k]$. Only bins $0$ to $N/2$ are independent.
- **DC and Nyquist**: bin $0$ is DC; bin $N/2$ is Nyquist $f_N = 1/(2\Delta t)$.
- **FFT**: not a different transform; just a fast algorithm for computing the DFT.
- Figure: `term01_lec05_fourier_pairs.png`

---

## Slide 7 — DFT periodicity and symmetry (figure)
- Figure: `term01_lec05_dft_periodicity.png`

---

## Slide 8 — The convolutional spectrum model
- A single seismic trace: $x(t) = w(t) * r(t) + n(t)$.
- In frequency domain: $X(f) = W(f) \, R(f) + N(f)$.
- Each component contributes its own multiplicative factor to the spectrum.
- Source signature, ghosts, instrument response, absorption, and reflectivity all leave separate fingerprints.

---

## Slide 9 — Effects of discretization and finite length
- **Sampling** makes the spectrum periodic with period $f_s = 1/\Delta t$. If copies overlap → aliasing.
- **Finite length** = multiplying by a rectangular window → convolution with sinc in frequency domain → **spectral leakage**.
- Frequency resolution: $\Delta f = 1/T$. Two frequencies closer than $1/T$ cannot be separated.

---

## Slide 10 — Spectral leakage (figure)
- Figure: `term01_lec05_spectral_leakage.png`

---

## Slide 11 — Amplitude and phase spectra
- $X[k]$ is complex.
- Magnitude $|X[k]|$ = amplitude spectrum.
- Angle $\arg X[k]$ = phase spectrum.
- Two wavelets can have the same amplitude spectrum but very different shapes because their phase spectra differ.
- Power spectrum: $|X(f)|^2$ = Fourier transform of autocorrelation (Wiener–Khinchin theorem).

---

## Slide 12 — Aliasing: the Nyquist criterion
- Nyquist frequency: $f_N = 1/(2\Delta t)$.
- A sinusoid must be sampled at least twice per cycle.
- For $\Delta t = 4$ ms, $f_N = 125$ Hz.

---

## Slide 13 — What happens above Nyquist
- Any frequency $f > f_N$ folds back: $f_{\text{apparent}} = |f - k f_s|$.
- Example: 150 Hz sampled at 4 ms → apparent frequency $|150 - 250| = 100$ Hz.
- Once aliased, the true frequency cannot be recovered.

---

## Slide 14 — Anti-alias protection
- Field systems apply an analog anti-alias filter before digitization.
- Every processing step that changes $\Delta t$ must re-apply anti-alias protection:
  - Decimation must be preceded by a low-pass filter.
  - Interpolation must not create frequencies above the new Nyquist.
  - Resampling in modelling or migration must respect the new Nyquist.

---

## Slide 15 — Aliasing (figure)
- Figure: `term01_lec05_aliasing.png`

---

## Slide 16 — Frequency filtering: what it is
- Filtering = multiplying trace spectrum by filter spectrum (frequency domain).
- Equivalent to convolving trace with filter impulse response (time domain).
- Seismic filtering is usually multiplicative in frequency.
- Phase is either left unchanged (zero-phase) or adjusted to keep the filter causal.

---

## Slide 17 — Common filter types
- **Low-pass**: keep frequencies below cutoff; smoothing, anti-alias pre-filtering.
- **High-pass**: keep frequencies above cutoff; removing ground roll or low-frequency drift.
- **Band-pass**: keep frequencies between two cutoffs; isolating the reflection signal band.
- **Notch / reject**: remove a narrow frequency band; e.g., 50/60 Hz power-line interference.
- Cutoffs specified at the $-3$ dB point (half the passband power).
- Figure: `term01_lec05_filter_types.png`

---

## Slide 18 — The Gibbs phenomenon
- An ideal sharp filter has an infinitely long impulse response (sinc).
- Truncation causes:
  - **Gibbs ringing**: oscillations near sharp transitions.
  - **Sidelobes**: unwanted pass-through of stopband frequencies.
- Trade-off: longer filters → steeper slopes but more computation and noise amplification.
- Windowing (Hamming, Blackman) reduces ringing at cost of wider transition band.
- Figure: `term01_lec05_gibbs.png`

---

## Slide 19 — Filtering a CMP gather
- Band-pass filtering removes low-frequency ground roll while preserving reflections.
- Example: synthetic CMP gather before and after a 15–60 Hz band-pass filter.
- Low-frequency noise dominates shallow, far-offset traces before filtering.
- After filtering, reflection events are clearer.
- Figure: `term01_lec05_filter_gather.png`

---

## Slide 20 — FIR and IIR filters
- **FIR (finite impulse response)**: non-recursive, finite length, linear phase. Common in seismic processing.
- **IIR (infinite impulse response)**: recursive, causal, compact but introduces phase distortion.
- **Butterworth** is the classic IIR example: maximally flat in passband, smooth roll-off.

---

## Slide 21 — Butterworth filter: the formula
- Squared amplitude response: $|H(f)|^2 = 1 / (1 + (f/f_c)^{2n})$.
- At cutoff: $|H(f_c)| = 1/\sqrt{2}$ → $-3$ dB.
- Higher order → steeper slope but longer impulse response.

---

## Slide 22 — Butterworth example
- $f_c = 60$ Hz, $\Delta t = 4$ ms ($f_N = 125$ Hz).
- 2nd-order: $-3.0$ dB at 60 Hz, $-8.5$ dB at 90 Hz, $-12.3$ dB at 120 Hz.
- 4th-order: $-3.0$ dB at 60 Hz, $-16.0$ dB at 90 Hz, $-24.1$ dB at 120 Hz.
- 8th-order: $-3.0$ dB at 60 Hz, $-31.0$ dB at 90 Hz, $-48.1$ dB at 120 Hz.
- Figure: `term01_lec05_butterworth.png`

---

## Slide 23 — Time-variant filters
- High frequencies are attenuated more rapidly with travel distance.
- Useful signal band shifts toward lower frequencies with record time.
- Time-variant filter: different passbands in different time windows.
  - Wider band at shallow times, narrower band at deeper times.
- Detailed design is usually handled by processing software.

---

## Slide 24 — Summary
- Digital seismic trace is finite and sampled; DFT spectrum is periodic (sampling) and smeared (finite length).
- Frequency resolution: $\Delta f = 1/T$.
- Nyquist frequency $f_N = 1/(2\Delta t)$: highest representable frequency without aliasing.
- Field recording uses anti-alias filters; every processing step that changes $\Delta t$ must re-apply protection.
- Spectral analysis uses the convolutional spectrum model.
- Frequency filters shape the amplitude spectrum; common types: low-pass, high-pass, band-pass, notch.
- Truncating an ideal filter causes Gibbs ringing; trade-off between steepness and length.
- Butterworth filters: smooth, causal IIR; higher order → steeper slope, longer response.
- Time-variant filters adapt passband to changing frequency content with record time.

---

## Slide 25 — Comprehension questions
- What is the Nyquist frequency for a 4 ms sample interval? What happens to a 150 Hz component?
- Why does a finite-length window cause a pure frequency to appear spread out in the frequency domain?
- In the convolutional spectrum model, how does the source signature affect the amplitude spectrum?
- Why must a low-pass filter be applied before decimating seismic data?
- Name one situation where a high-pass filter is useful and one where a notch filter is useful.
- What is the Gibbs phenomenon, and why does it force a trade-off between filter steepness and length?
- How much more attenuation does an 8th-order Butterworth give at 120 Hz compared with a 2nd-order?
- Why might a time-variant band-pass filter be used on a deep seismic section?

---

## Slide 26 — References
- Hatton, Worthington & Makin (1986), Ch. 2.2–2.5, 2.9.
- Margrave (2006), *Methods of Seismic Data Processing*, Ch. 2.
- Yilmaz, *Practical Seismic Data Analysis*, Ch. 1.2–1.3.1.
