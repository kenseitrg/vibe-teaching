---
title: Spatial spectral leakage
status: draft
sources:
  - xu2010_antileakage_fourier_transform
  - schonewille2009_aa_alft
  - zwartjes2006_fourier_reconstruction
tags: [regularization, fourier-transform, leakage, sampling, aliasing]
---

# Spatial spectral leakage

Spectral leakage is the smearing of energy from one spatial Fourier component into others. It is the central obstacle to Fourier-based [regularization](seismic_data_regularization.md) of *irregularly* sampled data.

## Where it comes from

Sampling a continuous signal $f(x)$ at discrete locations is equivalent to multiplying it by a **sampling function** — a train of impulses at the sample positions:

$$f_s(x) = f(x)\,L(x).$$

Multiplication in space becomes **convolution in the Fourier domain**:

$$\hat{f}_s(k) = \hat{f}(k) * \hat{L}(k).$$

- For a **regular** grid, $\hat{L}(k)$ is itself a comb of impulses. Convolution just replicates the spectrum cleanly (this is ordinary aliasing).
- For an **irregular** grid, $\hat{L}(k)$ has a strong peak at $k=0$ but also *non-zero sidelobes at all wavenumbers*. Convolving with these sidelobes spreads each true component's energy across many other wavenumbers. That crosstalk is **spectral leakage**.

A direct DFT of irregularly sampled data therefore does not give clean Fourier coefficients: a large true component shows up partly as many small false ones, and vice versa.

## Why it breaks the standard DFT

The DFT basis functions $e^{2\pi i k \cdot x}$ are **orthogonal only on a regular grid**. On an irregular grid they are no longer orthogonal, so projecting the data onto one basis function picks up contributions from all the others. The estimated spectrum is biased, and reconstructing onto a new grid from that spectrum produces artifacts.

## How to deal with it

A plain forward DFT is not adequate. Options, in increasing sophistication:

1. **Least-squares Fourier estimation** (Duijndam et al. 1999; [Zwartjes & Sacchi 2007](../sources/zwartjes2006_fourier_reconstruction.md)) — solve for the coefficients that best fit the data. Eliminates leakage when the data are band-limited and well sampled, but becomes poorly determined for sparse data with large gaps.
2. **Minimum-weighted-norm / high-resolution inversion** (Liu & Sacchi 2004; Zwartjes & Sacchi 2007) — add a sparsity constraint to stabilize the underdetermined problem.
3. **Anti-leakage Fourier transform (ALFT)** — an iterative [matching-pursuit](matching_pursuit.md) scheme that peels off the strongest component at a time, so leakage from already-explained energy is removed at every step. See [ALFT](anti_leakage_fourier_transform.md).

ALFT is the workhorse because it stays stable even when the data are sparse and gappy — exactly the regime where least squares fails.

## Related concepts

- [Anti-leakage Fourier transform](anti_leakage_fourier_transform.md)
- [Matching pursuit](matching_pursuit.md)
- [Non-uniform Fourier transform](nonuniform_fourier_transform.md)
- [Aliasing](aliasing.md)
- [Discrete Fourier transform](discrete_fourier_transform.md)

## Sources

- Xu, Zhang & Lambaré (2010) — defines spectral leakage as one of three core difficulties of Fourier regularization and motivates ALFT.
- Schonewille, Klaedtke & Vigner (2009) — leakage explained via the sampling pulse-train convolution picture.
- Zwartjes & Sacchi (2007) — least-squares / minimum-weighted-norm Fourier reconstruction of aliased data.
