---
title: "Cheng & Margrave (2012, 2013) — Comparison of Q-Estimation Methods"
status: draft
type: paper
source_file: wiki/sources/_raw_text/Comparison of Q-estimation methods - an update.txt
language: en
concepts:
  - q_estimation
tags: [q-estimation, spectral-ratio, centroid-frequency-shift, spectrum-modeling, match-filter, vsq]
---

# Cheng & Margrave (2012, 2013) — Comparison of Q-Estimation Methods

CREWES Research Reports, Volumes 24 (2012) and 25 (2013). Two companion studies comparing Q-estimation methods on synthetic VSP/reflection data and real VSP data.

## Overview

- **2012 paper** compares four methods: the classic spectral-ratio method, a match-technique method, a spectrum-modeling method, and a time-domain match-filter method (new, Cheng & Margrave 2012a).
- **2013 update** compares three: the complex spectral-ratio method (spectral ratio + phase), the centroid frequency-shift method, and the match-filter method.
- Motivating context (with references): spectral ratio is optimal in the noise-free case (Tonn 1991) but deteriorates drastically with noise (Patton 1988; Tonn 1991); reliable estimation from surface reflection data additionally suffers from thin-bed tuning effects (Dasgupta & Clark 1998 QVO; Hackert & Parra 2004 well-log correction).

## Forward model common to all methods

Local reflection wavelet at time $t_1$: $|A_1(f)| \approx g(t_1)|S(f)||R_1(f)|\exp(-\pi f t_1/Q)$ — source spectrum, local reflectivity spectrum, frequency-independent amplitude factor g (spherical divergence + transmission losses), and the constant-Q exponential decay.

## Methods

1. **Classic spectral ratio** (Båth 1974; Spencer et al. 1982): $\ln[A_2/A_1] \approx -\pi f\tau/Q + b$; least-squares line fit with slope k gives $Q = -\pi\tau/k$. Exact on noise-free data; fragile with noise.
2. **Complex spectral ratio** (Cheng & Margrave 2008): include the phase term $\mathrm{Im} \approx (2f\tau/Q)\ln|f/f_0|$ and invert for Q by minimizing complex misfit — improved accuracy, but sensitive to the reference frequency $f_0$ used to model phase; requires minimum-phase equivalent wavelets on real data.
3. **Centroid frequency shift** (Quan & Harris 1997): centroid $f_c = \int f|A|df/\int|A|df$ and variance $\sigma_f^2$ of the (assumed Gaussian) amplitude spectrum; attenuation gives $f_{c,1} - f_{c,2} = (\pi\tau/Q)\sigma_f^2$, so $Q = \pi\tau\sigma_{f,12}^2/(f_{c,1}-f_{c,2})$. Robust to noise, but sensitive to the analysis band: whole-band computation on non-Gaussian spectra gave biased results (true Q = 80 → estimates 115–198); limited bands (e.g., 5–90 Hz) recovered 75–82. Power-spectrum vs amplitude-spectrum variants ("approaches 1–3") trade bias vs stability.
4. **Spectrum modeling** (Janssen et al. 1985; Tonn 1991; Blias 2011): avoid the spectral division — forward-model both amplitude spectra jointly (source, Q, amplitude factors) and fit by least squares.
5. **Time-domain match-filter** (Cheng & Margrave 2012): estimate smoothed spectra of the two local wavelets (multitaper), form minimum-phase equivalent wavelets $w_1, w_2$, then find Q by direct search minimizing $\|w_1 * I(Q,t) - \mu w_2\|^2$, where $I(Q,t)$ is the constant-Q impulse response over the interval (including the Hilbert-transform dispersion phase) and μ a scaling factor.

## Results and conclusions

- All methods are workable on good data; ranking on robustness: **match-filter is the most robust to noise** and works for both VSP and reflection data; complex spectral ratio improves on classic spectral ratio when phase is usable; centroid shift is stable but requires careful band selection.
- Match-filter on reflection data is mainly affected by reflector tuning, not by noise.
- Practical guidance: define signal-dominated frequency bands; use minimum-phase equivalents; validate with multiple methods.

## Relation to lecture notes

Term 2 Lecture 01, Section 7 (estimation of Q): spectral ratio (with inline derivation), centroid frequency shift, least-squares spectrum modelling, and wavelet-optimization/match-filter — this pair of papers is the comparison backbone.

## Related sources

- [Paradigm QEST reference](paradigm_qapp_qest.md) — production LS spectrum-fitting implementation
- [Kjartansson (1979)](kjartansson_1979_constant_q.md) — constant-Q impulse response used in matching
- [Wang (2006)](wang_2006_inverse_q_resolution.md) — compensation that consumes the estimated Q
