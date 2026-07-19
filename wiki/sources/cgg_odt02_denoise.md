---
title: "CGG ODT02 De-noise — Marine Noise Attenuation Course"
status: draft
source_type: training slides
authors: "CGG UK Training (R. Jupp et al.)"
year: 2016
source_file: papers/noise_attenuation/ODT02_DENOISE_*.pptx (6 parts)
lectures:
  - term03_lec04
related_concepts:
  - seismic_noise
  - frequency_filtering
  - spectral_analysis
  - automatic_gain_control
  - adaptive_subtraction
  - radon_transform
tags: [noise-attenuation, marine-seismic, swell-noise, fk-filter, tau-p, median-filter, fx-deconvolution, linear-noise]
---

# CGG ODT02 De-noise — Marine Noise Attenuation Course

CGG UK Training (2016). *ODT02 De-noise*, Parts 1–4. Internal training slides.

**Note:** Internal CGG training document; images do not have show rights.

## Main message

A four-part internal training course covering the full marine noise-attenuation workflow: noise classification, identification and editing, swell-noise removal (f-x domain), FK (wavenumber) filtering, linear noise removal (Tau-P domain), and supporting theory (mean/median filters, plane-wave decomposition). The course builds from basic noise identification through progressively more sophisticated transform-domain techniques.

## Part 1 — Introduction and Noise Identification (Slides 1–46)

### Key points

1. **Noise classification:** Random (swell noise, background noise, spiking) vs. coherent (industrial noise, cable vibrations, reflected noise from rigs, seismic interference). Also unwanted signal: multiples, refractions, guided waves.
2. **The noise cone concept:** External and reflected noise emanates from a point source as a 3D cone. The shot record is a cross-section through this cone; linear or parabolic shape depends on where the cable intersects the cone.
3. **Marine noise types:** Hydrostatic pressure (0–2 Hz), swell/cable buckling (0–15 Hz), cable tugging/strumming (2–15 Hz), vessel/prop noise (broadband), seismic interference, reflected noise, spikes, extraction errors, background random noise.
4. **De-noise in the processing sequence:** Low-cut filter → edits/despiking → swell noise removal → trace interpolation → K-filter → linear noise removal (LNA) → industrial noise removal → Tau-P mute.
5. **QC amplitude maps:** Global maps (shot-point X,Y) and shot-channel maps identify noisy data. Deep-window RMS amplitude is most sensitive to noise because the window is not dominated by signal. Amplitude scaling should follow de-noise, not precede it.

## Part 2 — Swell Noise Removal (Slides 1–47)

### Key points

6. **Swell noise mechanism:** Caused by cable drag, turbulence, hydrostatic pressure fluctuations, and cable bending. Appears as vertical stripes of high-amplitude, low-frequency noise with variable thickness.
7. **F-X domain swell removal:** Transform to f-x → within frequency bands, compare each trace's median amplitude to the group median → if ratio > threshold, mark as bad → create FX decon prediction filter from surrounding traces → reconstruct bad data → inverse transform.
8. **Key parameters:** Spatial window (2.5–3× swell noise width), temporal window (~1 s), frequency range (typically 0–15 Hz for low-cut target), threshold, start/end time to exclude shallow high-amplitude energy.
9. **Multiple passes:** First pass in shot domain; subsequent passes in receiver or channel domain if coherent component remains. Up to 6 passes can be applied with different parameters.
10. **Signal leakage:** Near-trace amplitudes may be flagged as anomalous. Mitigation: back-to-back/butterfly gathers, reversible scalar scaling of near traces, narrower frequency bands.
11. **F-X random noise attenuation (FX-RNA):** Predict trace from surrounding traces in f-x; difference = unpredictable (random) noise. Only linear events are predictable; filters must be short enough for curved events.
12. **FXY deconvolution:** 3D extension — data predictable as a plane in x-y. Better preservation of curved events and better attenuation of noise coherent in only one direction.
13. **SINAT:** 2D/2D FX-FY sequential process for irregular geometry; extracts energy incoherent in channel domain, then coherent in shot domain to model seismic interference.

## Appendix 1.2 — Mean and Median Filters (Slides 1–25)

### Key points

14. **Median vs. mean:** Median is robust to outliers (spikes); mean smears them. Median filter is the simplest edge-preserving filter — preserves step functions that mean filters smooth out.
15. **Applications in seismic:** 1D median across offsets in CIGs (mild 3-point) for RMO picking/AVO; 2D/3D median for velocity cube smoothing; dip-dependent (structural) median filtering along event dip.
16. **Hybrid filters:** Alpha-trim mean (discard extremes before averaging), Gaussian filter (weighted mean), edited mean (exclude outliers by range), EMM (edge-preserving multi-stage mean using median-of-medians).

## Part 3 — FK (Wavenumber) Filtering (Slides 1–end)

### Key points

17. **F-K domain:** 2D Fourier transform (time→frequency, space→wavenumber). A constant dip maps to a straight line through the origin in f-k. Events of different dip are separated in f-k space.
18. **Spatial aliasing:** Wavenumber beyond ±0.5 cycles/trace is aliased. Aliasing condition: f_alias = V_apparent / (2 × dx). Higher frequencies, steeper dips, and coarser trace spacing all increase aliasing.
19. **FK filter design:** Pass zone (keep signal), reject zone (remove noise), taper zone (smooth transition). FK filtering removes ground roll, airwave, multiples (after NMO), and cable jerk.
20. **Anti-alias filtering:** Before any spatial decimation or transform, apply a temporal low-cut or spatial anti-alias filter to prevent aliasing artefacts.
21. **Practical FK workflow:** Regularise data (interpolation) → design FK operator → apply → QC on gathers and stacks. Always check for signal leakage at near offsets and steep dips.

## Part 4 — Linear Noise Removal / Tau-P (Slides 1–end)

### Key points

22. **Linear noise types in marine:** Post-critical energy (refractions, guided waves, post-critical reflections), cable vibrations (tug/strum from front/rear/mid cable), external noise cones, vessel/prop noise, seismic interference.
23. **Tau-P transform (slant stack):** Decomposes the wavefield into plane waves characterised by ray parameter p = dt/dx (slowness) and intercept time τ. A straight line in T-X maps to a point in Tau-P; a hyperbola maps to an ellipse.
24. **Tau-P vs. FK:** In FK, a constant dip occupies a line through origin across multiple f-k values. In Tau-P, the same dip is localised to a single p-value. Tau-P is preferred for dip filtering because it better separates events by dip.
25. **Linear noise removal workflows:** (a) Forward Tau-P → mute unwanted p-ranges → inverse Tau-P; (b) Forward Tau-P → keep only wanted p-ranges → inverse Tau-P (scenario 1). High-resolution Tau-P uses iterative/sparseness-constrained inversion.
26. **Plane-wave decomposition:** A curved wavefront is the superposition of plane waves at different incidence angles. p₀ sin(θ) = P (ray parameter), conserved through layers by Snell's law. Tau-P of a receiver gather gives energy vs. emergence angle — useful for directional de-signature.
27. **Edge effects:** Data edges (near/far offset, bottom) act like spikes in Tau-P, smearing energy across all p-values. Mitigation: apply tapers/mutes before transform; work in the middle of the aperture.
28. **Post-critical energy as "linear noise":** Refractions, guided waves, and multiples thereof form a high-amplitude cone that masks primaries. LNA in shot/receiver domain removes this before CMP processing. Removing multiple tails can aid de-multiple.

## Relation to lecture notes

This comprehensive course directly supports Term 3 Lecture 04 — Noise Attenuation. Parts 1–2 cover noise classification and the f-x based swell/noise removal (impulsive and random). Part 3 provides the FK-domain theory and practice essential for understanding velocity filtering. Part 4 introduces the Tau-P domain and linear noise removal — key topics for understanding how different processing domains separate signal from noise.

## Related concepts

- [Seismic noise](../concepts/seismic_noise.md)
- [Frequency filtering](../concepts/frequency_filtering.md)
- [Spectral analysis](../concepts/spectral_analysis.md)
- [Automatic gain control](../concepts/automatic_gain_control.md)
- [Adaptive subtraction](../concepts/adaptive_subtraction.md)
- [Radon transform](../concepts/radon_transform.md)

## Related sources

- [NUCNS Technical Documentation](nucns.md)
- [NUCNS Best Practice](nucns_best_practice.md)
- [Cadzow Best Practice](cadzow_best_practice.md)
- [Kneppers — Basic Geophysics](kneppers_basic_geophysics.md)
- [Bormann & Wielandt — Seismic Signals and Noise](bormann_wielandt_seismic_signals_noise.md)
