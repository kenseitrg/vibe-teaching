# Slide outline — Term 1, Lecture 6: Single-channel deconvolution

## Slide 1 — Title
- **Title:** Single-channel deconvolution
- **Subtitle:** Recovering reflectivity by removing the embedded wavelet
- Figure: none

## Slide 2 — Goal of seismic processing
- We want the earth's reflectivity as a function of position.
- Real data = reflectivity convolved with a long wavelet + noise.
- Deconvolution compresses/reshapes the wavelet.
- Cannot recover missing frequencies.
- Figure: `term01_lec06_convolutional_model.png`

## Slide 3 — Convolutional model
- Equation: $x(t) = w(t) * r(t) + n(t)$.
- Embedded wavelet = source signature * ghosts * bubble * instrument * absorption.
- Assumptions: stationarity, white reflectivity, minimum phase, additive white noise.
- Figure: wavelet components diagram (optional, can be added later).

## Slide 4 — Why phase matters
- Same amplitude spectrum can have many phase spectra.
- Minimum, maximum, zero, and mixed phase.
- Causal vs. non-causal.
- Figure: `term01_lec06_phase_wavelets.png`

## Slide 5 — The dipole
- Dipole $(a,b)$ has $z$-transform $a + bz$.
- $(a,b)$ and $(b,a)$ have the same amplitude spectrum.
- Minimum phase if $|a| > |b|$.
- Figure: `term01_lec06_dipoles.png`

## Slide 6 — Minimum phase = front-loaded
- Factor any wavelet into dipoles.
- Minimum phase iff all zeros are outside the unit circle.
- Inverse filter is causal and stable.
- Partial energies are maximized.
- Key equation: $E_p = \sum_{k=0}^p w_k^2$.

## Slide 7 — Causality and inverse filters
- Minimum-phase dipole: inverse expands in positive powers of $z$.
- Maximum-phase dipole: convergent inverse needs negative powers of $z$.
- Mixed phase: two-sided filter.

## Slide 8 — Deterministic deconvolution
- Wavelet is known or measured.
- Fourier: $F(f) = W^*(f) / (|W(f)|^2 + \varepsilon^2)$.
- $z$-domain: polynomial division.
- Examples: designature, instrument response, vibroseis-to-minimum-phase.
- Figure: `term01_lec06_deterministic_decon.png`

## Slide 9 — Prewhitening
- Stabilizes spectral division.
- Limits noise amplification at weak frequencies.
- Typical values 0.1–5%.
- Figure: `term01_lec06_prewhitening.png`

## Slide 10 — Statistical deconvolution
- Wavelet unknown; estimate from data.
- Least-squares criterion.
- Wiener-Hopf equations.
- Figure: matrix equation (can use `term01_lec07_demo_wiener_matrix.png` or typeset).

## Slide 11 — Assumptions of statistical deconvolution
- White reflectivity.
- Minimum-phase wavelet.
- Stationarity.
- Additive white noise.
- Consequences of violating each.

## Slide 12 — Spiking deconvolution
- Desired output = spike at zero lag.
- Prediction gap = 1 sample.
- Figure: `term01_lec06_spiking_decon.png`

## Slide 13 — Predictive deconvolution
- Predict future samples from past samples.
- Prediction-error filter removes predictable energy.
- Gap controls target: wavelet compression vs. reverberations/multiples.
- Figure: `term01_lec06_predictive_decon.png`

## Slide 14 — Parameters
- Prediction gap.
- Operator length.
- Prewhitening.
- Analysis window.
- Trade-offs.

## Slide 15 — Summary and concept check
- Deconvolution = undo convolution.
- Phase matters; minimum phase gives causal inverse.
- Deterministic vs. statistical.
- Spiking vs. predictive.
- Ask 1–2 concept-check questions.
