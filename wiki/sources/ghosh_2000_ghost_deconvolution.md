---
title: Ghosh (2000) — Deconvolving the ghost effect of the water surface
type: paper
year: 2000
authors: Santi Kumar Ghosh
source_file: papers/marine/ghosh2000.pdf
status: reviewed
tags: [deghosting, ghost-filter, marine, frequency-domain, spectral-zeros, two-depth-recording]
---

# Ghosh (2000) — Deconvolving the ghost effect of the water surface

## Source

- **Author:** Santi Kumar Ghosh (National Geophysical Research Institute, India)
- **Title:** Deconvolving the ghost effect of the water surface in marine seismics
- **Journal:** Geophysics, 65(6), 1831–1836
- **Year:** 2000
- **DOI:** 10.1190/1.1444862
- **File:** `papers/marine/ghosh2000.pdf`

## Main message

The ghost filter $h(t) = \delta(t) - \delta(t - t_0)$ has spectral zeros that make time-domain least-squares inverse filtering unstable and inaccurate. A frequency-domain approach is superior: either explicitly choose a recording band that excludes the zeros, or record at two depths whose ghost filters have no common zeros.

## Key points

1. **Ghost filter in time domain:**
   $$h(t) = \delta(t) - \delta(t - t_0)$$
   where $t_0 = 2D/v_w$, $D$ is sensor depth, $v_w \approx 1500$ m/s.

2. **Ghost filter in frequency domain:**
   $$H(\omega) = 1 - \exp(i\omega t_0) = 2\sin(\omega t_0 / 2) \exp\left[i\left(\frac{\pi}{2} - \frac{\omega t_0}{2}\right)\right]$$
   
   Amplitude spectrum: $|H(\omega)| = 2|\sin(\omega t_0 / 2)|$
   
   **Spectral zeros** at $\omega_n = \frac{2\pi n}{t_0}$ for $n = 0, 1, 2, ...$, i.e., frequencies $f_n = \frac{n}{t_0} = \frac{n v_w}{2D}$.

3. **Problem with time-domain deconvolution:**
   - The ghost filter is **not minimum phase** (has zeros on the unit circle).
   - Least-squares inverse is inexact and unacceptable near spectral zeros.
   - **Disproves Ziolkowski's conjecture** that spectral zeros make the autocorrelation matrix singular. Actually, the matrix is well-conditioned, but the inverse is inexact.

4. **Frequency-domain solution #1: band exclusion**
   - Choose recording band that excludes spectral zeros.
   - For depth $D = 10$ m, $t_0 = 13.3$ ms, first non-zero notch at $f_1 = 75$ Hz.
   - Record only below 75 Hz (or above 150 Hz, etc.).
   - **Limitation:** loses useful frequency content.

5. **Frequency-domain solution #2: two-depth recording**
   - Record at two depths $D_1$ and $D_2$ such that their ghost filters have **no common zeros**.
   - Criterion: $\gcd(D_1, D_2)$ should be small enough that no common zero falls within the recording band.
   - Example: $D_1 = 10$ m (notches at 75, 150, 225 Hz), $D_2 = 15$ m (notches at 50, 100, 150 Hz). Common zero at 150 Hz — not acceptable if band extends to 150 Hz.
   - Better: $D_1 = 10$ m, $D_2 = 12$ m. Notches at 75, 150 Hz and 62.5, 125 Hz. No common zeros below 150 Hz.

6. **Source-side ghost:**
   - Same filter form: $h_s(t) = \delta(t) - \delta(t - t_{0s})$.
   - Criterion for source depths is identical to receiver depths.
   - Multiple sources at different depths can eliminate spectral zeros in the source signature.

7. **Practical implications:**
   - **Conventional streamer:** single depth, spectral zeros unavoidable. Must use processing methods (e.g., Amundsen 2013, Li 2020) that avoid spectral division at zeros.
   - **Dual-depth streamer:** two depths, can combine to fill notches (early version of variable-depth streamer concept).
   - **Dual-sensor (PZ):** hydrophone + geophone have different ghost responses, can combine to eliminate zeros.

8. **Historical context:**
   - Lindsey (1960): feedback filter approach (assumes $|R| < 1$, not applicable to sea surface where $R \approx -1$).
   - Ziolkowski (1971): proposed multiple sources at different depths to eliminate zeros.
   - Ghosh (2000): extended to receivers, provided rigorous criterion for depth selection.

## Key equations

**Ghost filter (time domain):**
$$h(t) = \delta(t) - \delta(t - t_0), \quad t_0 = \frac{2D}{v_w}$$

**Ghost filter (frequency domain):**
$$H(\omega) = 1 - \exp(i\omega t_0) = 2\sin\left(\frac{\omega t_0}{2}\right) \exp\left[i\left(\frac{\pi}{2} - \frac{\omega t_0}{2}\right)\right]$$

**Notch frequencies:**
$$f_n = \frac{n v_w}{2D}, \quad n = 0, 1, 2, ...$$

**Two-depth criterion:**
Choose $D_1, D_2$ such that $\frac{D_1}{D_2}$ is irrational, or $\gcd(D_1, D_2)$ is small enough that no common zero falls within the recording band.

## Practical implications

- **Spectral zeros are fundamental:** cannot be removed by time-domain deconvolution.
- **Frequency-domain approach is superior:** explicit handling of zeros.
- **Two-depth recording:** early concept behind modern variable-depth streamer (BroadSeis).
- **QC:** check amplitude spectra for notches; if present, deghosting is needed.

## Implications for teaching

- Clear mathematical treatment of the ghost filter and its spectral properties.
- Explains why time-domain deconvolution fails for ghosts (non-minimum phase).
- Introduces the concept of using multiple sensors/depths to eliminate zeros (foundation for modern broadband methods).
- Good historical perspective (Lindsey → Ziolkowski → Ghosh).

## Concepts informed

- [Marine deghosting](../concepts/marine_deghosting.md)
- [Broadband seismic](../concepts/broadband_seismic.md)
- [Minimum phase wavelet](../concepts/minimum_phase.md)

## Related sources

- [Lindsey (1960)](lindsey_1960_ghost_elimination.md) — early feedback filter approach
- [Amundsen & Zhou (2013)](amundsen_zhou_2013_deghosting.md) — low-frequency trace-by-trace deghosting
- [Li et al. (2020)](li_et_al_2020_sparse_deghosting.md) — sparse deghosting

## Quotes / memorable lines

> "The ghost filters, both at the source and at the receiver, are evidently not minimum phase filters. This is because a minimum phase filter must have a stable one-sided frequency inverse, and the ghost filters do not possess a frequency inverse owing to having notches in the spectrum at many frequencies (including the d.c. frequency)."

> "A conjecture by Ziolkowski (1971) that zeroes in the spectrum of a wavelet make its autocorrelation matrix singular turns out to be false. Nevertheless, the inexactness of the least-squares inverse of a wavelet is shown to have its origin in the zeroes in the spectrum of the wavelet."

> "The remedy consists of recording at two depths chosen according to the criterion that the respective ghost filters do not have common zeroes in their spectra."
