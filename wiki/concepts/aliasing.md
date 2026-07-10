---
title: Aliasing and the Nyquist sampling theorem
status: draft
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - margrave_2006_methods_of_seismic_data_processing
  - yilmaz_practical_seismic_data_analysis_amplitude
tags: [aliasing, nyquist, sampling, anti-alias, signal-processing]
---

# Aliasing and the Nyquist sampling theorem

Aliasing is the misidentification of a high-frequency signal as a lower frequency after discretization.

## Nyquist criterion

If a time series is sampled at interval $\Delta t$, the highest frequency that can be uniquely represented is the **Nyquist frequency**:

$$f_N = \frac{1}{2\Delta t}.$$

A sinusoid must be sampled at least twice per cycle to avoid ambiguity. For example, with $\Delta t = 4$ ms, $f_N = 125$ Hz.

## What happens when the criterion is violated

Sampling makes the spectrum periodic with period $f_s = 1/\Delta t$. Any frequency $f$ outside the Nyquist band is therefore indistinguishable from a frequency inside the band. To find the **apparent** frequency:

1. Take the remainder of $f$ after division by $f_s$:
   $$f_{\text{rem}} = f \bmod f_s \quad \text{(in the range $[0, f_s)$)}.$$
2. If $f_{\text{rem}} \le f_N$, the apparent frequency is $f_{\text{rem}}$.
3. Otherwise it folds back from $f_s$:
   $$f_{\text{apparent}} = f_s - f_{\text{rem}}.$$

A useful special case: a frequency just above Nyquist, $f_N < f < f_s$, aliases to

$$f_{\text{apparent}} = f_s - f.$$

For example, with $\Delta t = 4$ ms we have $f_s = 250$ Hz and $f_N = 125$ Hz. A 150 Hz component aliases to $250 - 150 = 100$ Hz.

## Anti-alias protection in acquisition

Field recording systems apply an analog **anti-alias filter** before digitization to remove energy above the Nyquist. This is why properly recorded seismic data are usually not aliased in time.

## Aliasing risks in processing

Aliasing can reappear whenever we change the sampling rate:
- **Decimation** (downsampling): must low-pass filter first.
- **Interpolation**: the output must not contain frequencies above the new Nyquist.
- **Resampling** for modelling or migration: keep the desired frequency band inside the new Nyquist.

## Related concepts

- [Discrete Fourier transform](discrete_fourier_transform.md)
- [Frequency filtering](frequency_filtering.md)
- [Spectral analysis](spectral_analysis.md)

## Sources

- Hatton, Worthington & Makin (1986), Ch. 2.3.3 — sampling and the Nyquist criterion.
- Margrave (2006), Ch. 2 — sampling, spectrum replication, and anti-alias filtering.
- Yilmaz, *Practical Seismic Data Analysis*, §1.2.3–1.2.4 — aliasing and spatial aliasing.
