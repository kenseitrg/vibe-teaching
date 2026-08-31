---
title: FX-deconvolution (F-X prediction filtering)
status: draft
sources:
  - canales1984_fx_decon
  - gulunay1986_fxdecon
  - abma1995_lateral_prediction
  - treitel1974_complex_wiener
  - denisov_finikov_2009
  - denisov_finikov_2010
tags: [fx-deconvolution, random-noise, prediction-filter, spatial-prediction, wiener-filter]
---

# FX-deconvolution (F-X prediction filtering)

FX-deconvolution (also called F-X prediction filtering, FXDECON, or Random Noise Attenuation — RNA) attenuates random noise by exploiting the spatial predictability of linear events in the frequency domain.

## Core idea

A single linear dipping event has the same waveform on every trace, just shifted in time. In the frequency domain, this time shift becomes a complex phase factor:

$$ X_n(f) = A(f) \cdot e^{-j 2\pi f n \Delta x / v_\text{app}} $$

At a fixed frequency $f$, the complex amplitudes $X_0, X_1, \dots, X_{N-1}$ form a complex sinusoid across the spatial dimension $n$. A sinusoid is perfectly predictable by a linear prediction filter.

## How it works

1. Fourier-transform each trace to the frequency domain.
2. For each frequency $f$ (or a decimated set), form a spatial sequence of complex values: $X_n(f)$ for $n = 0, 1, \dots, N-1$.
3. Design a prediction-error filter (PEF) along the spatial axis that minimizes the prediction error:

$$ \varepsilon^2 = \sum_n \left| X_n(f) + \sum_{k=1}^K h_k X_{n-k}(f) \right|^2 $$

This is the same Wiener-Levinson problem as in [Wiener filter](wiener_filter.md), but applied to **complex-valued** spatial data.
4. The predictable part is the signal; the prediction error (residual) contains the random noise.
5. Subtract the residual or reconstruct the signal from the predicted component.

## Why it works

- **Signal**: linear or gently curved events with consistent moveout → highly predictable in space → captured by the PEF.
- **Random noise**: uncorrelated trace-to-trace → unpredictable → appears in the residual.

## Key limitation: constant dip

The prediction filter works well only when the dip (moveout) is roughly **constant within the analysis window**. If dips vary, the PEF cannot predict all events simultaneously, and signal may leak into the residual. Solutions:

- Use short spatial windows (a few traces) to approximate constant dip.
- Flatten the data (apply NMO) before F-X deconvolution.
- Use adaptive or multi-window approaches.

## Extensions

- **F-X interpolation**: fill gaps in irregularly sampled data by predicting missing traces from the PEF.
- **F-X regularization**: similar idea for transforming irregular data onto a regular grid.
- **Time-varying F-X decon**: split the trace into overlapping time windows, handle variable dips over time.

## Connection to Wiener filtering

The mathematics is identical to time-domain Wiener prediction filtering, but applied per-frequency to complex spatial sequences. The autocorrelation matrix is now complex-valued and Hermitian (conjugate-symmetric).

## Related concepts

- [Wiener filter](wiener_filter.md)
- [Predictive deconvolution](predictive_deconvolution.md)
- [Seismic noise](seismic_noise.md)
- [SVD / Cadzow filtering](cadzow_svd_filtering.md)
- [Curvelet transform](curvelet_transform.md)
- [Frequency filtering](frequency_filtering.md)

## Sources

- [Canales (1984) — F-X deconvolution.](../sources/canales1984_fx_decon.md)
- [Gulunay (1986) — FXDECON.](../sources/gulunay1986_fxdecon.md)
- [Abma & Claerbout (1995) — Lateral prediction.](../sources/abma1995_lateral_prediction.md)
- [Treitel (1974) — The complex Wiener filter.](../sources/treitel1974_complex_wiener.md)
- [Денисов & Фиников (2009) — Парадоксы f-x деконволюции.](../sources/denisov_finikov_2009.md)
- [Денисов & Фиников (2010) — Особенности алгоритма f-x деконволюции.](../sources/denisov_finikov_2010.md)
