---
title: Adaptive subtraction
status: draft
sources:
  - verschuur_2006_eet07_adaptive_subtraction
  - foti_surface_wave_methods
  - ivanov_hrlrt_masw
tags: [adaptive-subtraction, wiener-filter, matching-filter, noise-attenuation, multiples, srme, l1-norm]
---

# Adaptive subtraction

**Adaptive subtraction** is the practical engine of every "model the noise, then remove it" method. A noise model (predicted multiples, modeled surface waves, anything predictable) is never exactly right in amplitude, phase and wavelet, so instead of subtracting it directly we estimate a short **matching filter** that adapts the model to the data in local windows, and subtract the *filtered* model. The filter estimation is a Wiener least-squares problem — the same machinery as Term 1 deconvolution.

## Why direct subtraction fails

A predicted noise event is usually accurate in **kinematics** (travel times, moveout — the model got the physics of propagation right) but inaccurate in **dynamics**: amplitudes, source/receiver directivity, wavelet phase, and 3D effects are imperfectly known. Subtracting an unadapted model leaves residual noise; scaling by a single constant is not enough when errors vary with offset, time or position.

## Wiener matching-filter formulation

Given data $d(t)$ containing signal plus noise, and a noise model $m(t)$, estimate filter $a(t)$ minimizing the residual after subtraction:

$$
e[n] = d[n] - \sum_{k} a[k]\, m[n-k], \qquad
J_{L2} = \sum_n |e[n]|^2 \;\rightarrow\; \min
$$

This is exactly the Wiener problem: normal equations $\mathbf{R}_{mm} \mathbf{a} = \mathbf{r}_{dm}$, where $\mathbf{R}_{mm}$ is the autocorrelation matrix of the model and $\mathbf{r}_{dm}$ the cross-correlation of data and model (usually with a small prewhitening added for stability). In processing systems the correlations are summed in a local **space-time window**, so the filter adapts laterally and temporally.

## Parameters and their trade-offs

- **Filter length.** Short filters adapt gross amplitude/phase only and are safe for signal; long filters can shape the model to fit *anything* — including the signal where it interferes with the noise, damaging primaries. Rule: the filter should be long enough to absorb wavelet errors, no longer.
- **Window size (space and time).** Small windows → locally accurate adaptation but unstable (little data per filter, risk of adapting signal away). Large windows → stable, well-determined filters but no adaptation to local variations.
- **Interaction of the two.** The filter length must stay small relative to the window, and the window must be large enough that signal and noise are not both "fitted". A two-stage strategy is common: big windows for a global inverse-wavelet filter (e.g. one filter per common-offset gather), then small windows for local amplitude/directivity corrections (shot domain).
- **Mode/iteration**: single-pass vs iterative model-and-subtract loops.

## L2 vs L1 subtraction

L2 assumes the subtraction **output has minimum energy** — true when the output is signal uncorrelated with the model. It fails where signal and noise interfere (crossing events): the least-squares filter compromises between fitting the noise and annihilating the signal, producing both leakage (residual noise) and primary damage.

The L1 norm,

$$
J_{L1} = \sum_n |e[n]| \;\rightarrow\; \min,
$$

penalizes large residuals less, i.e. it tolerates a big misfit exactly at the interfering samples (treated as outliers) instead of forcing them to zero. The price: the problem becomes non-linear and is solved iteratively (iteratively re-weighted least squares). In practice L1 preserves primaries under interference; L2 is faster and more robust when interference is mild.

Beyond norms: **curvelet-domain separation** discriminates predicted noise from signal by local dip and frequency without explicit subtraction — works when the two occupy different curvelet coefficients.

## Applications

1. **SRME / demultiple** (the main industrial use): predicted surface multiples are adaptively matched and subtracted; two-stage L2 or L1 strategies are standard. See [SRME](srme.md).
2. **Surface-wave (ground-roll) removal**: a modeled dispersive surface-wave wavefield (from a picked dispersion curve, with frequency-dependent moveout and lateral smoothing) is adaptively subtracted from reflection data.
3. Any model-driven noise removal: swell noise, modeled diffractions, 4D matching.

## Related concepts

- [Wiener filter](wiener_filter.md)
- [SRME](srme.md)
- [Multiples](multiples.md)
- [Surface waves](surface_waves.md)
- [Predictive deconvolution](predictive_deconvolution.md)

## Sources

- [Verschuur (2006) — EAGE EET 07, Adaptive Subtraction](../sources/verschuur_2006_eet07_adaptive_subtraction.md)
- [Foti et al. (2011) — Surface wave methods](../sources/foti_surface_wave_methods.md)
- [Ivanov et al. (2017) — HRLRT with MASW](../sources/ivanov_hrlrt_masw.md)
- [Mi et al. (2016) — Dispersion energy analysis](../sources/mi_surface_waves_dispersion_energy.md)
- [Priestley (2024) — Surface wave practical](../sources/priestley_surface_wave_practical.md)
