# Slide outline — Term 3, Lecture 4: Noise Attenuation Algorithms

---

## Slide 1 — Title
- Noise Attenuation Algorithms
- Term 3, Lecture 4
- Figure: none

---

## Slide 2 — Learning objectives
- Classify seismic noise as coherent or random and give examples of each.
- Explain why FK and tau-P transforms alone cannot perfectly separate signal from noise.
- Describe the NUCNS noise-band model and why it works on non-uniform 3D geometries.
- Explain the curvelet transform's tiling of the FK plane and why it gives a sparse representation of seismic data.
- Describe the frequency-dependent median filter (AAA) and its "most traces are normal" assumption.
- Explain the FX-deconvolution principle: linear events are predictable as complex exponentials in the F-X domain.
- Describe SVD rank truncation and Cadzow (Hankel-SVD) filtering.
- For each method, state the key assumption and the main failure mode.
- Figure: none

---

## Slide 3 — Why this lecture matters
- In Term 2 we learned FK and tau-P transforms for signal/noise separation.
- In practice, the separation is never perfect: overlap, aliasing, curved events, random noise.
- Modern processing uses specialized algorithms designed for these limitations.
- This lecture: five widely used methods, each exploiting a different property of signal vs. noise.
- Figure: none

---

## Slide 4 — Noise types: coherent vs random
- Coherent noise: consistent phase relationship across traces, follows predictable moveout.
  - Ground roll, refracted arrivals, air waves, multiples, cultural noise.
- Random noise: no consistent phase, cannot be predicted trace-to-trace.
  - Ambient noise, instrument noise, spikes, swell noise.
- Noise is relative to the processing goal: surface waves are signal for MASW, noise for reflection imaging.
- Figure: `term03_lec04_noise_types.png`

---

## Slide 5 — No free lunch
- Every denoising method trades noise removal against signal preservation.
- Aggressive denoising creates processing artefacts that mimic geology.
- Subtle surviving noise degrades velocity analysis, AVO, and inversion.
- Correct acquisition-related variations (statics, velocities, SCAC) before denoising.
- Figure: none

---

## Slide 6 — Why transforms are not enough
- FK: linear events map to lines through origin with slope k = f/v_app.
- tau-P: linear events map to points.
- In both domains, signal and noise should occupy different regions — in principle.
- In practice: overlap, transition zones, spatial aliasing, curved events, random noise.
- Figure: `term03_lec04_fk_overlap.png`

---

## Slide 7 — Two strategies for modern algorithms
- Strategy 1: Model the noise and subtract it (NUCNS, adaptive subtraction).
- Strategy 2: Model the signal as sparse or predictable, and keep it (curvelet, FX-decon, SVD).
- LIFT approach: model signal, subtract from data, treat residual as leftover signal + noise.
- Figure: none

---

## Slide 8 — NUCNS: the problem with 2D FK on 3D land data
- 2D FK filter assumes regular trace spacing along a line.
- 3D land surveys use cross-spread geometry: irregular offsets, varying azimuths.
- Non-uniform spacing causes spatial aliasing and energy leakage in FK.
- Geometry mismatch: filter assumes a regular grid that does not exist.
- Figure: none

---

## Slide 9 — NUCNS noise-band model
- Model coherent noise as a sum of noise bands, each with approximately linear moveout.
- noise_i(x, y, t) = A_i * w_i(t - p_x * x - p_y * y).
- Work with the actual acquisition geometry — non-uniform spacing handled naturally.
- Band-by-band estimation, then adaptive subtraction.
- Figure: `term03_lec04_nucns_concept.png`

---

## Slide 10 — Curvelet transform: tiling the FK plane
- Curvelets partition the 2D FK plane into tiles: concentric rings (frequency scales) and angular wedges (directions).
- At high frequency, tiles are long and thin, aligned with dipping events.
- A dipping event concentrates energy in a few curvelet coefficients.
- Random noise spreads across all coefficients — sparse representation exploits this contrast.
- Figure: `term03_lec04_curvelet_tiling.png`

---

## Slide 11 — Curvelet denoising
- Forward curvelet transform → threshold coefficients (keep large, zero small).
- Inverse curvelet transform → denoised data.
- Large coefficients capture coherent signal; small coefficients capture noise.
- Threshold level controls the noise/signal trade-off.
- Figure: `term03_lec04_curvelet_denoising.png`

---

## Slide 12 — AAA: frequency-dependent median filter
- Assumption: most traces are normal; anomalous traces have abnormally high energy.
- For each frequency band, compute energy per trace.
- Apply median threshold: traces above the median are scaled down.
- Robust against burst noise and spikes without smoothing the whole section.
- Figure: `term03_lec04_aaa_median.png`

---

## Slide 13 — FX-deconvolution: the core idea
- A linear dipping event has the same waveform on every trace, just shifted in time.
- In the frequency domain, the shift becomes a phase factor: X_n(f) = W(f) * e^{-j 2πf n Δx / v_app}.
- At fixed f, the complex amplitude across traces is a complex exponential — perfectly predictable.
- Random noise is unpredictable trace-to-trace.
- Figure: `term03_lec04_fx_decon_schematic.png`

---

## Slide 14 — FX-deconvolution: the prediction filter
- For each frequency f, form the spatial sequence X_0(f), X_1(f), ..., X_{M-1}(f).
- Design a PEF along the spatial axis: minimize residual energy.
- Predictable part (signal) → captured by the PEF.
- Unpredictable part (noise) → appears in the residual.
- Key limitation: constant dip within the analysis window.
- Figure: none

---

## Slide 15 — FX-deconvolution: practical considerations
- Short spatial windows: constant-dip approximation locally valid.
- Flatten the data (NMO) before FX-decon to minimize dip variation.
- Time-varying windows: separate PEF for each time gate.
- Extensions: FX-interpolation for missing traces, FX-regularization for irregular geometry.
- Figure: `term03_lec04_fx_decon_result.png`

---

## Slide 16 — SVD rank truncation
- SVD decomposes the data matrix D = U Σ V^T.
- Signal is low-rank (a few large singular values); noise is full-rank (small singular values across all).
- Truncate to rank K: keep only the top K singular values and vectors.
- The knee in the singular-value spectrum separates signal subspace from noise subspace.
- Works best when events are flat (or nearly flat after NMO).
- Figure: `term03_lec04_svd_rank_truncation.png`

---

## Slide 17 — Cadzow: Hankel-SVD filtering
- Raw SVD on the trace matrix does not exploit prediction structure.
- Cadzow works in the F-X domain: for each frequency, form a Hankel matrix from the spatial sequence.
- A single plane wave produces a rank-1 Hankel matrix.
- SVD + rank truncation on the Hankel matrix enforces the prediction property.
- Flatten by anti-diagonal averaging → denoised spatial sequence.
- Equivalent to FX-deconvolution under certain conditions.
- Figure: `term03_lec04_cadzow_hankel.png`

---

## Slide 18 — Summary: five methods, five principles
- NUCNS: model noise bands in 3D FK → subtract. Assumption: linear moveout per band.
- Curvelet: sparse representation → threshold. Assumption: signal is sparse in curvelet domain.
- AAA: median per frequency → scale outliers. Assumption: most traces are normal.
- FX-decon: spatial prediction of complex exponentials → PEF. Assumption: constant dip in window.
- SVD/Cadzow: rank reduction → truncate. Assumption: signal is low-rank.
- No free lunch: every method has a parameter that trades noise removal against signal damage.
- Figure: none

---

## Slide 19 — Comprehension questions
- Give two examples of coherent noise and two of random noise.
- Why can't an FK fan filter perfectly separate ground roll from reflections?
- What is the key difference between NUCNS and a conventional 2D FK filter?
- In the curvelet domain, why does random noise spread across many coefficients while a reflection concentrates in a few?
- What is the "most traces are normal" assumption in AAA?
- A colleague applies AAA and the AVO gradient on a target horizon is destroyed. What went wrong?
- In FX-deconvolution, what physical property makes a linear event predictable in F-X?
- Why does FX-deconvolution fail when the window contains events with different dips?
- What is the difference between raw SVD on a trace matrix and Cadzow filtering?
- In SVD filtering, when would you discard the largest singular values instead of keeping them?
- Figure: none
