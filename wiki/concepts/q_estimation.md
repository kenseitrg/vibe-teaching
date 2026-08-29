---
title: Q estimation
status: draft
sources:
  - cheng_margrave_2012_2013_q_estimation
  - paradigm_qapp_qest
tags: [q-estimation, spectral-ratio, centroid-frequency-shift, spectrum-modeling, match-filter, vsq, effective-q]
---

# Q estimation

Estimating the quality factor Q from seismic data. Required input to any [inverse Q filtering](inverse_q_filtering.md) or Q-compensating imaging.

## Data sources

- **VSP**: direct transmission between receiver levels — the cleanest geometry (source and path identical between levels); the classic domain for Q estimation (Hauge 1981; Tonn 1991)
- **Sonic/crosswell**: high-frequency, shallow-focused
- **Surface reflection data**: always available but noisier — estimates an **effective Q** averaged over the path; thin-bed tuning contaminates local spectra (Dasgupta & Clark 1998 QVO; Hackert & Parra 2004)
- **Data preparation**: minimal processing — noise attenuation and deghosting only. **Never AGC** (gain destroys the amplitude decay that carries Q). Inspect the time-frequency spectrogram first: it must show smooth exponential decay along time and frequency.

## Methods

### Spectral ratio (classic)
Window two events/levels at $t_1, t_2$; the ratio cancels the unknown source spectrum:

$$\ln\frac{A(\omega,t_2)}{A(\omega,t_1)} = -\frac{\omega(t_2-t_1)}{2Q} + b$$

Slope $k$ of the log-ratio vs $\omega$ gives $Q = -\pi\tau/k$ (equivalently $-\omega$-conventions aside, $Q$ from the linear fit). Optimal on noise-free data (Tonn 1991); deteriorates rapidly with noise; sensitive to windowing, tuning and spectral-division artifacts.

### Centroid (central) frequency shift (Quan & Harris 1997)
Absorption shifts the spectrum's centroid downward. For a near-Gaussian source spectrum with variance $\sigma_f^2$:

$$f_{c,1} - f_{c,2} = \frac{\pi (t_2-t_1)}{Q}\,\sigma_f^2 \quad\Rightarrow\quad Q = \frac{\pi\tau\,\sigma_{f,12}^2}{f_{c,1}-f_{c,2}}$$

Robust to noise (whole-spectrum attribute); but requires a sensible analysis band — whole-band application on non-Gaussian spectra biases the result (Cheng & Margrave 2013: true Q=80 recovered as 76–82 with band-limited, 115–198 whole-band).

### Least-squares spectrum modelling (Janssen 1985, Tonn 1991, Blias 2011)
Avoid spectral division: forward-model the measured amplitude spectrum $|A(f,t)| = G(t)\,|S(f)|\exp(-\pi f t/Q)$ jointly over $Q$ and amplitude factor(s) $G$; solve by least squares (possibly time-varying, in the time-frequency/Gabor domain). Handles spherical divergence explicitly ("variable amplitude" variants); the production-style realization of this idea.

### Wavelet optimization / match-filter (Raikes & White 1984; Cheng & Margrave 2012)
Model the absorbed wavelet for trial Q (constant-Q impulse response including dispersion), compare with the measured wavelet, and minimize the misfit — in the time domain (match-filter: $\min_Q \|w_1 * I(Q,t) - \mu w_2\|^2$, multitaper spectra, minimum-phase equivalents, direct Q search) or frequency domain (complex spectral ratio using amplitude **and** phase; sensitive to reference frequency). Most robust method on noisy reflection data (Cheng & Margrave 2012/2013 comparisons).

## Effective vs interval Q

Estimates over overlapping windows give **effective Q** (path-averaged); layer-stripping inverts for **interval Q** per layer, analogous to interval velocities. QC both; cross-validate with two methods (e.g., variable- vs constant-amplitude LS variants should agree when no amplitude drift is present).

## Relation to lecture notes

Term 2 Lecture 01, Section 7 (estimation of Q), with the spectral-ratio and centroid-shift derivations inline in the notes.

## Related concepts

- [Inverse Q filtering](inverse_q_filtering.md)
- [Seismic absorption](seismic_absorption.md)
- [Spectral analysis](spectral_analysis.md)
- [Seismic well tie](seismic_well_tie.md) (VSP domain)
