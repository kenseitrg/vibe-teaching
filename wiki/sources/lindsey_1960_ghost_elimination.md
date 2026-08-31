---
title: Lindsey (1960) — Elimination of seismic ghost reflections by means of a linear filter
type: paper
year: 1960
authors: J. P. Lindsey
source_file: papers/marine/lindsey1960.pdf
status: reviewed
tags: [deghosting, ghost-filter, marine, feedback-filter, historical]
---

# Lindsey (1960) — Elimination of seismic ghost reflections by means of a linear filter

## Source

- **Author:** J. P. Lindsey (Phillips Petroleum Company)
- **Title:** Elimination of seismic ghost reflections by means of a linear filter
- **Journal:** Geophysics, 25(1), 130–140
- **Year:** 1960
- **File:** `papers/marine/lindsey1960.pdf`

## Main message

A feedback filter can eliminate ghost reflections from seismic data. The filter is designed to convert the total response (primary + ghost) to the primary reflection alone. The filter has a transfer function $F(s) = \frac{1}{1 - \alpha H(s) e^{-s\tau}}$, which can be realized as a feedback system.

## Key points

1. **Ghost model:**
   - Downgoing wavefront from shot: $b(t)$ (incident) + $\alpha H(s) b(t) e^{-s\tau}$ (ghost).
   - $\alpha$ is reflection coefficient at overlying boundary.
   - $H(s)$ is tuning effect of two passes through overlying strata.
   - $\tau$ is two-way traveltime from shot to ghosting boundary.

2. **Surface response:**
   $$R(s) = r(t) * [b(t) - \alpha H(s) b(t) e^{-s\tau}]$$
   where $r(t)$ is primary reflection series.

3. **Desired response:**
   $$R_{\text{desired}}(s) = r(t) * b(t)$$

4. **Filter design:**
   $$F(s) R(s) = R_{\text{desired}}(s)$$
   $$F(s) = \frac{R(s) b(s)}{R(s) [b(s) - \alpha H(s) b(s) e^{-s\tau}]} = \frac{1}{1 - \alpha H(s) e^{-s\tau}}$$

5. **Feedback realization:**
   - Forward loop transfer function: 1.
   - Loop transfer function: $\alpha H(s) e^{-s\tau}$.
   - **Positive feedback** (not negative, because ghost has opposite polarity for $R \approx -1$ at sea surface).

6. **Filter behavior:**
   - Expanding $F(s)$ as infinite series:
     $$F(s) = 1 + \alpha H(s) e^{-s\tau} + \alpha^2 H^2(s) e^{-2s\tau} + ...$$
   - For negligible earth filter $H(s) \approx 1$:
     $$F(s) = 1 + \alpha e^{-s\tau} + \alpha^2 e^{-2s\tau} + ...$$
   - Impulse response: infinite series of impulses at intervals $\tau$, decaying by factor $\alpha$.

7. **Problem with sea-surface ghosts:**
   - For sea surface, $\alpha \approx -1$ (reflection coefficient for upgoing wave at water-air interface).
   - Filter becomes unstable (positive feedback with $\alpha = -1$ leads to growing oscillations).
   - **Lindsey's method assumes $|\alpha| < 1$**, which is not valid for sea-surface ghosts.
   - Later work (Ghosh 2000) addressed this limitation.

8. **Practical considerations:**
   - Filter should only be applied to portions of record subject to ghosting.
   - Early arrivals (first breaks, direct waves) have no ghost and should be muted before filtering.
   - If earth filter $H(s)$ is negligible (simple geology above shot), a simple low-pass filter with ~6 dB/octave attenuation suffices.

9. **Historical significance:**
   - First published method for ghost elimination by linear filtering.
   - Introduced feedback filter concept for seismic processing.
   - Paved way for later work (Ziolkowski 1971, Ghosh 2000, Amundsen 2013).

10. **Limitations:**
    - Assumes ghost reflection coefficient $|\alpha| < 1$ (not valid for sea surface).
    - Assumes ghost is time-invariant (stationary).
    - Infinite impulse response can create artifacts if not properly windowed.

## Key equations

**Ghost filter (Laplace domain):**
$$F(s) = \frac{1}{1 - \alpha H(s) e^{-s\tau}}$$

**Impulse response (for $H(s) \approx 1$):**
$$f(t) = \delta(t) + \alpha \delta(t - \tau) + \alpha^2 \delta(t - 2\tau) + ...$$

**Feedback system:**
- Forward path: 1
- Feedback path: $\alpha H(s) e^{-s\tau}$
- **Positive feedback** (because ghost has opposite polarity)

## Practical implications

- **Historical method:** not directly applicable to sea-surface ghosts ($\alpha \approx -1$).
- **Concept:** feedback filter idea influenced later deghosting methods.
- **QC:** check for ghost arrivals on data; if present, modern deghosting methods are needed.

## Implications for teaching

- **Historical perspective:** shows evolution of deghosting ideas.
- **Feedback filter concept:** useful for understanding modern inverse methods.
- **Limitation:** illustrates why sea-surface ghosts require special treatment (Ghosh 2000, Amundsen 2013).

## Concepts informed

- [Marine deghosting](../concepts/marine_deghosting.md)
- [Minimum phase wavelet](../concepts/minimum_phase.md)

## Related sources

- [Ghosh (2000)](ghosh_2000_ghost_deconvolution.md) — addressed Lindsey's limitation for sea-surface ghosts
- [Amundsen & Zhou (2013)](amundsen_zhou_2013_deghosting.md) — modern trace-by-trace deghosting
- [CGG ODT04 Part 1](cgg_odt04_deconvolution_part1_wavelet.md) — ghost physics

## Quotes / memorable lines

> "The existence of a large velocity discontinuity above a seismic shot has long been recognized as the source of 'ghost' reflections appearing on the seismogram."

> "The filter required to eliminate ghost reflections may be defined as one that converts the total response at the surface to the primary reflections alone."

> "This filter converts a primary reflection plus ghost reflection at the input into a primary reflection only at the output."
