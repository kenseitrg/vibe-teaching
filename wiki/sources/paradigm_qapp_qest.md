---
title: "Paradigm Echos QAPP / QEST — Q Compensation and Q Estimation Reference Guide"
status: draft
type: software-doc
source_file: wiki/sources/_raw_text/Q Application Reference.txt
language: en
concepts:
  - inverse_q_filtering
  - q_estimation
tags: [q-compensation, q-estimation, stabilization, gain-limit, reference-frequency, processing-software]
---

# Paradigm Echos QAPP / QEST — Reference Guide Summary

Paradigm™19 Reference Guide: *QAPP: Q Application* and *QEST: Q Compensation Analysis and Estimation*. Production-software documentation that shows how the theory of inverse Q filtering and Q estimation appears as concrete processing parameters.

> Note: in lecture materials, refer to these capabilities generically ("modern processing software"), not by product/module names.

## QAPP — Q application (compensation and modeling)

- Applies anelastic attenuation correction using either a constant Q or a time-varying (effective or interval) Q function supplied as a vertical function file.
- Two modes: **compensation** (time-varying inverse filter) and **modeling** (time-varying forward filter — no stabilization needed since no inversion is performed).
- Implementation: **non-stationary convolution** (time-varying filter per trace).
- **Stabilization is mandatory for compensation**: the inverse filter's exponential exceeds numerical limits when amplitudes become very small. User parameter **MAXDB** specifies the maximum amplitude increase (dB) of the filter; the program caps it if the requested value is unsafe for the given Q, frequency band, and record length. Higher MAXDB compensates higher frequencies at later times.
- Phase options include a **Futterman operator switch** (FUTTOPT) — the choice of causal dispersion law.
- Practical message: reference frequency and gain limit are the two knobs that control *where the wavelet is anchored* and *how much boost is allowed*.

## QEST — Q estimation

- Robust estimation of constant or time-varying **effective Q** from prestack gathers or poststack sections; output is a vertical (time, Q) function.
- Implementation: Gabor time-frequency decomposition; amplitude model $A(t,\omega) = A_0(t)\exp(-\frac{\omega}{2} Q_\text{eff}^{-1}(t)\, t)$ (Wang 2004); joint least-squares minimization over Q and the amplitude factor over the 2-D (t, ω) surface.
- Two variants:
  - **VARAMP** (variable amplitude in time) — assumes an amplitude factor varying with time (spherical divergence, transmission loss); preferred default.
  - **CNSTAMP** (constant amplitude) — assumes time-constant amplitude; more robust to noise.
  - Running both is a QC: if the two time-varying Q functions agree, a variable amplitude factor is likely absent and results are validated; if they diverge, CNSTAMP results are invalid.
- **Data preparation**: minimal prior processing (deghosting and noise attenuation only — never AGC); visual spectrogram QC to confirm smooth exponential decay along both time and frequency axes before estimation.
- Analysis parameters: frequency band (FMIN/FMAX), window length (WLEN) and increment (WINC) — windows should exceed ~1 s for robust estimation.
- Recommendations: near-offset NMO-corrected sub-gathers for prestack; super-gathers / stacks for S/N.

## Key takeaways for teaching

- The concepts from Wang (2002/2006) appear in production as: time-varying effective Q functions, non-stationary convolution, mandatory amplitude stabilization via a dB gain limit, choice of Futterman vs alternative dispersion operator.
- The concepts from Cheng & Margrave / Quan & Harris appear as: joint LS fitting of amplitude and Q in the time-frequency domain, explicit band selection, spectrogram QC.
- "No AGC before Q-estimation" is a hard practical rule — gain destroys the amplitude decay that carries the Q information.

## Relation to lecture notes

Term 2 Lecture 01, Sections 5–7: stabilization (MAXDB ↔ σ² gain limit of Wang 2006), reference frequency, compensation vs modeling modes, effective vs interval Q, estimation workflows and QC.

## Related sources

- [Wang (2002)](wang_2002_stable_inverse_q.md), [Wang (2006)](wang_2006_inverse_q_resolution.md) — theory behind QAPP-type compensation
- [Cheng & Margrave (2012, 2013)](cheng_margrave_2012_2013_q_estimation.md) — theory behind LS spectrum-fitting estimation
