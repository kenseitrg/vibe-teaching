---
title: Minimum phase wavelet
status: draft
course_term: 1
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - margrave_2006_methods_of_seismic_data_processing
  - yilmaz_2001_seismic_data_analysis_deconvolution
tags: [phase, minimum-phase, wavelet, z-transform, dipole, causality]
---

# Minimum phase wavelet

A **minimum-phase wavelet** is the causal wavelet with a given amplitude spectrum that has the fastest build-up of energy in time. It is also the causal wavelet whose inverse filter is causal and stable.

## Why it matters in seismology

- Many deconvolution algorithms (spiking / Wiener deconvolution) assume the embedded wavelet is minimum phase.
- Constant-Q attenuation and many physical propagation processes are minimum phase.
- Once the amplitude spectrum is known, the minimum-phase wavelet is uniquely determined.

## Dipole intuition

The building block is a **dipole** — a two-sample wavelet $(a, b)$ with Z-transform

$$
W(z) = a + bz .
$$

$(a, b)$ and $(b, a)$ have the same amplitude spectrum, but different phase spectra.

| Dipole | Condition | Phase type | Energy placement |
|--------|-----------|------------|------------------|
| $(a, b)$ | $|a| > |b|$ | minimum phase | front-loaded |
| $(b, a)$ | $|b| > |a|$ | maximum phase | back-loaded |

The inverse of a dipole is obtained by polynomial division:

$$
\frac{1}{a + bz} = \frac{1}{a}\left(1 - \frac{b}{a}z + \left(\frac{b}{a}\right)^2 z^2 - \cdots \right) .
$$

If $|a| > |b|$, the series converges in **positive** powers of $z$; the inverse filter is causal. If $|b| > |a|$, a convergent expansion requires **negative** powers of $z$, i.e. a non-causal filter.

## General causal wavelet

Any finite causal wavelet can be factored into dipoles (roots of its Z-transform polynomial). The wavelet is minimum phase **if and only if every dipole factor is minimum phase**. Equivalently, all zeros of $W(z)$ lie **outside** the unit circle.

Because the phase spectra of the dipoles add, the total phase delay is minimized when every dipole is minimum phase.

## Front-loading property

Define the partial energy up to sample $p$:

$$
E_p = \sum_{k=0}^{p} w_k^2 .
$$

For a minimum-phase wavelet, $E_p$ is larger than for any other causal wavelet with the same amplitude spectrum, for every $p$. This is the formal meaning of "front-loaded" or "minimum delay".

## Amplitude–phase relationship

For a causal, stable wavelet with a causal stable inverse, the phase spectrum $\varphi(\omega)$ and the log amplitude spectrum $\ln A(\omega)$ form a Hilbert-transform pair:

$$
\varphi(\omega) = \mathcal{H}\{ \ln A(\omega) \} .
$$

Therefore, knowing the amplitude spectrum is enough to compute the minimum-phase wavelet.

## Important properties

- The convolution of two minimum-phase wavelets is minimum phase.
- The convolution of a minimum-phase wavelet with a zero-phase wavelet is generally **mixed phase**, unless the zero-phase wavelet is much broader band.
- A band-limited wavelet can never be exactly minimum phase over its whole spectrum, because zeros in the amplitude spectrum violate the stable-inverse condition.

## Teaching intuition

- Minimum phase = "as early as causality allows".
- It is not about preserving a particular phase value; it is a relationship between amplitude and phase.
- If you change the amplitude spectrum (e.g. by filtering), you must also change the phase spectrum to keep the wavelet minimum phase.

## Related concepts

- [Seismic wavelet](seismic_wavelet.md)
- [Deterministic deconvolution](deterministic_deconvolution.md)
- [Statistical deconvolution](statistical_deconvolution.md)
- [Wiener filter](wiener_filter.md)
- [Predictive deconvolution](predictive_deconvolution.md)

## Sources

- [Hatton, Worthington & Makin (1986)](../sources/hatton_worthington_makin_1986_seismic_data_processing.md)
- [Margrave (2006)](../sources/margrave_2006_methods_of_seismic_data_processing.md)
- [Yilmaz (2001)](../sources/yilmaz_2001_seismic_data_analysis_deconvolution.md)
