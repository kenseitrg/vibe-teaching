# Term 3 Lecture 04 — Noise Attenuation Algorithms

## Scope

Modern seismic processing goes beyond simple FK and tau-P transforms to separate signal from noise. This lecture surveys five widely used algorithms for coherent and random noise attenuation: NUCNS for coherent noise on non-uniform 3D land data, curvelet-domain thresholding for both coherent and random noise, frequency-dependent median filtering (AAA) for anomalous amplitude bursts, FX-deconvolution for random noise via spatial prediction, and SVD/Cadzow filtering for random and stationary noise via rank reduction.

The lecture assumes familiarity with FK and tau-P transforms from Term 2. It does not cover surface-wave-specific methods (Term 3 Lecture 03) or demultiple.

## Learning objectives

By the end of this lecture students should be able to:

- Classify seismic noise as coherent or random and give examples of each.
- Explain why FK and tau-P transforms alone cannot perfectly separate signal from noise.
- Describe the NUCNS noise-band model and why it works on non-uniform 3D geometries.
- Explain the curvelet transform's tiling of the FK plane and why it gives a sparse representation of seismic data.
- Describe the frequency-dependent median filter (AAA) and its "most traces are normal" assumption.
- Explain the FX-deconvolution principle: linear events are predictable as complex exponentials in the F-X domain.
- Describe SVD rank truncation and Cadzow (Hankel-SVD) filtering and their two strategies (keep-large vs. discard-large).
- For each method, state the key assumption and the main failure mode.

## Prerequisites

- Term 1 Lecture 06 (single-channel deconvolution): convolution, Wiener filter, prediction-error filter.
- Term 2 (assumed): FK transform, tau-P transform, dip filtering.
- Term 3 Lecture 03: adaptive subtraction concept.

## Timing (90 minutes)

| Section | Time | Notes |
|---------|------|-------|
| 1. Noise types — coherent vs random | 10 min | Classification, examples, SNR concept |
| 2. Why transforms are not enough | 8 min | FK/tau-P recap, imperfect separation, random noise inseparable |
| 3. NUCNS — coherent noise on non-uniform data | 12 min | Noise-band model, 3D FK decomposition, adaptive subtraction |
| 4. Curvelet-domain noise attenuation | 12 min | Curvelet tiling, sparsity, thresholding, model-guided weights |
| 5. Frequency-dependent median filtering (AAA) | 10 min | Median per frequency, anomaly detection, AVO risk |
| 6. FX-deconvolution | 20 min | Complex exponentials, spatial PEF, derivation sketch, constant-dip limitation |
| 7. SVD and Cadzow filtering | 12 min | Rank reduction, eigenvalue spectrum, raw SVD vs Hankel-SVD, two strategies |
| 8. Summary and comprehension questions | 6 min | Recap, comparison table, questions |
| **Total** | **90 min** | FX-decon gets the most time as the mathematically richest method |

## Section 1 — Noise types: coherent vs random

- Noise = any recorded energy not used as signal for the current processing objective. Whether something is noise depends on the goal (surface waves: signal for MASW, noise for reflection imaging).
- **Coherent noise**: consistent phase across traces, predictable moveout. Examples: ground roll, refracted arrivals, air waves, multiples, cultural noise with a repeating pattern.
- **Random noise**: no consistent phase across traces, cannot be predicted trace-to-trace. Examples: ambient noise (wind, microtremors), instrument noise, quantization noise, spikes, swell noise (marine).
- **Signal-to-noise ratio**: SNR = signal power / noise power. Stacking improves SNR by sqrt(N) for uncorrelated noise.
- Key insight: no algorithm removes all noise without affecting signal. Every method trades noise removal against signal preservation via a parameter (threshold, filter length, rank).
- Before applying noise attenuation, correct for acquisition-related variations: statics, velocities, surface-consistent amplitudes (SCAC).
- Figure idea: shot gather with labeled noise types (ground roll cone, refraction, air wave, random background, spike).

## Section 2 — Why transforms are not enough

- Recap from Term 2: FK transform maps a shot gather to frequency-wavenumber; tau-P maps to intercept time vs ray parameter. In both domains, signal and noise occupy different regions — in principle.
- In practice, separation is never perfect:
  - Signal and noise overlap in FK space (e.g., steep-dip reflections and ground roll share wavenumbers at low frequencies).
  - Fan filters and pie-slice filters have transition zones that either leave noise or cut signal.
  - Spatial aliasing on irregular geometries smears energy across the FK plane.
  - Curved events do not map to clean lines in tau-P.
- Random noise is fundamentally inseparable by any dip-based transform: it fills the entire FK plane.
- Modern algorithms use one of two strategies: **model the noise** and subtract it (NUCNS, adaptive subtraction), or **model the signal** as sparse/predictable and keep it (curvelet thresholding, FX-decon, SVD).
- Brief mention of **LIFT** (Linear Filtering): model the signal (or the noise), subtract it from the data, and treat the residual as the complementary part. This is the same idea as adaptive subtraction from Term 3 Lecture 03, applied to general coherent noise.
- Figure idea: FK spectrum of a shot gather showing overlap between signal and ground-roll regions; same data after a fan filter showing residual noise and damaged signal.

## Section 3 — NUCNS: coherent noise on non-uniform data

- NUCNS = Non-Uniform Coherent Noise Suppression. Designed for 3D land data with irregular cross-spread geometry where 2D FK fails.
- **Noise-band model**: coherent noise (ground roll, refractions) arrives with approximately linear moveout over a short spatial window. Each band is:
  $$ \text{noise}_i(x, y, t) = A_i \cdot w_i(t - p_x x - p_y y) $$
  where $p_x, p_y$ are slownesses, $A_i$ is an amplitude factor, and $w_i$ is a noise wavelet. For linear kinematics, one term per band suffices.
- NUCNS workflow:
  1. Decompose data into overlapping spatial windows (cross-spreads or common-shot/receiver gathers).
  2. In each window, apply band-pass fan filters in 3D FK space to isolate noise bands by velocity range.
  3. Estimate noise model trace-by-trace using least-squares fitting within each band.
  4. Adaptively subtract the estimated noise.
- Why not 2D FK: non-uniform sampling causes spatial aliasing and leakage. NUCNS works with the actual acquisition geometry.
- Limitations: assumes linear moveout per band per window; window size trade-off (large = violates linearity, small = insufficient data); signal leakage if reflections share noise dip.
- Figure idea: schematic of fan-filter bands in 3D FK space; NUCNS noise-model estimation workflow.

## Section 4 — Curvelet-domain noise attenuation

- Curvelets are multiscale, multidirectional basis functions. Unlike wavelets (point-like, isotropic), curvelets are elongated — they capture orientation and scale simultaneously.
- **Tiling of the FK plane**: concentric rings (scales/frequency bands) × angular wedges (directions). At scale $j$, a curvelet has length ~$2^{-j/2}$ and width ~$2^{-j}$ (parabolic scaling). At fine scales, curvelets are long and thin — ideal for linear and curved seismic events.
- **Sparsity**: clean seismic reflections have few large curvelet coefficients; random noise spreads energy across all coefficients. Thresholding small coefficients removes noise while preserving signal.
- Workflow:
  1. Transform to curvelet domain.
  2. Estimate noise level per scale-direction panel.
  3. Threshold or weight coefficients (small = noise, large = signal).
  4. Inverse-transform.
- Model-guided variant (Kustowski et al. 2013): use a signal or noise model to design per-panel weights, rather than blind thresholding. Interpreters can guide the process with geological knowledge.
- Advantages: handles curved events, preserves amplitude and phase, works with irregular sampling.
- Limitations: computationally expensive, many parameters (scales, angles, thresholds), imperfect when signal and noise overlap in curvelet space.
- Figure idea: curvelet tiling of the FK plane; before/after denoising example.

## Section 5 — Frequency-dependent median filtering (AAA and multichannel spectral editing)

- AAA = Anomalous Amplitude Attenuation. A frequency-domain statistical method for sporadic noise bursts and spikes. The broader family is **multichannel spectral editing** — any method that edits individual traces in the frequency domain based on statistics across traces.
- Core idea: for each frequency, compute the median amplitude across traces in a spatial window. Traces that deviate strongly from the median are penalized.
- Two modes:
  - Punish deviations from median (both positive and negative anomalies).
  - Punish amplitudes above a threshold (positive anomalies only).
- **Key assumption**: most traces in the window are "normal." If all traces are anomalous, the median is biased and nothing is detected. Window must be large enough for good traces to dominate.
- Window design: must follow data kinematics (flatten first). Overlapping windows for smooth transitions.
- **AVO risk**: aggressive AAA can destroy legitimate amplitude-variation-with-offset trends. Apply before AVO-sensitive steps or use conservative thresholds.
- **Sorting trick**: coherent noise can be made "anomalous" by re-sorting. Ground roll in shot sort is coherent (all traces have it); in CMP sort or random sort it appears as scattered large amplitudes on isolated traces — perfect for median-based detection. The choice of sort determines what looks "anomalous."
- Related methods: AMPSCAL (global trace scaling), TFCLEAN (time-frequency cleaning). Hierarchy: AMPSCAL < TFCLEAN < AAA in sophistication.
- Figure idea: amplitude spectra of several traces at a single frequency, showing median, threshold, and one anomalous trace being penalized.

## Section 6 — FX-deconvolution

- Also called F-X prediction filtering, FXDECON, or Random Noise Attenuation (RNA).
- **Core idea**: a linear dipping event has the same waveform on every trace, shifted in time. In the frequency domain, this time shift becomes a phase factor:
  $$ X_n(f) = A(f) \cdot e^{-j 2\pi f n \Delta x / v_\text{app}} $$
  At fixed frequency $f$, the complex amplitudes across traces form a complex sinusoid — perfectly predictable by a linear prediction filter.
- Workflow:
  1. Fourier-transform each trace to the frequency domain.
  2. For each frequency, form the spatial sequence $X_0(f), X_1(f), \dots, X_{M-1}(f)$.
  3. Design a prediction-error filter (PEF) along the spatial axis:
     $$ \varepsilon^2 = \sum_n \left| X_n(f) + \sum_{k=1}^K h_k X_{n-k}(f) \right|^2 $$
     This is the Wiener-Levinson problem with complex-valued data (Treitel 1974).
  4. The predictable part is the signal; the prediction error is random noise.
  5. Inverse-transform the predicted (signal) component.
- **Why it works**: signal (linear/curved events with consistent moveout) is spatially predictable; random noise is not.
- **Key limitation — constant dip**: the PEF assumes all events in the analysis window have the same dip. If dips vary, the filter cannot predict all events and signal leaks into the residual. Solutions: short spatial windows, flatten data first (NMO), or time-varying windows.
- Extensions: F-X interpolation, F-X regularization, multi-window adaptive approaches.
- Derivation reference: `lecture_notes/derivations/fx_deconvolution_derivation.en.md` — full derivation from the linear event model through the complex Wiener filter to the prediction-error filter.
- Figure idea: schematic showing spatial prediction across traces; before/after shot gather comparison; effect of dip variation on prediction quality.

## Section 7 — SVD and Cadzow filtering

- SVD = Singular Value Decomposition. Organize $M$ traces as columns of a data matrix $\mathbf{D}$, decompose:
  $$ \mathbf{D} = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^T $$
  Signal occupies a low-rank subspace (few large singular values); random noise fills a high-rank subspace (many small singular values).
- **Strategy 1 — remove random noise**: keep the $K$ largest singular values, discard the rest. The singular-value spectrum shows a "knee" separating signal from noise.
- **Strategy 2 — remove strong stationary noise**: discard the largest singular values (they capture the high-energy stationary noise), keep the rest.
- **Cadzow filtering** (Hankel-SVD): apply SVD in the F-X domain. For each frequency:
  1. Form a Hankel matrix from the spatial sequence $X_0(f), \dots, X_{M-1}(f)$ (constant anti-diagonals).
  2. SVD-truncate to rank $K$.
  3. Flatten back by averaging anti-diagonals.
  A single plane wave at frequency $f$ produces a rank-1 Hankel matrix. Rank truncation keeps only the plane-wave structure.
- **Why Hankel**: the Hankel structure enforces the prediction property — it is the algebraic counterpart of F-X deconvolution. Cadzow = SVD + Hankel structure constraint.
- KL transform: equivalent to SVD of the covariance matrix $\mathbf{D}^T \mathbf{D}$.
- Practical notes: apply to flattened gathers; window length trades wavelet capture against rank increase; over-truncation damages AVO.
- Figure idea: singular-value spectrum showing the knee; rank-truncation effect on a synthetic gather; Hankel matrix structure schematic.

## Section 8 — Summary and comprehension questions

- Noise is relative to the processing goal. Coherent noise is predictable; random noise is not.
- FK/tau-P transforms help but are never perfect; random noise is inseparable by dip alone.
- Five modern algorithms, five different principles:
  | Method | Noise type | Principle | Key assumption |
  |--------|-----------|-----------|----------------|
  | NUCNS | Coherent | Model noise bands in 3D FK | Linear moveout per band |
  | Curvelet | Both | Sparse representation | Signal is sparse in curvelet domain |
  | AAA | Random (bursts) | Median per frequency | Most traces are normal |
  | FX-decon | Random | Spatial prediction of complex exponentials | Constant dip in window |
  | SVD/Cadzow | Random / stationary | Rank reduction | Signal is low-rank |
- No free lunch: every method has a parameter that trades noise removal against signal damage.

## Figures to generate

| Figure | Script | Output | Concept |
|--------|--------|--------|---------|
| Shot gather with labeled noise types | `plot_noise_types.py` | `term03_lec04_noise_types.png` | Coherent vs random noise |
| FK spectrum showing signal/noise overlap | `plot_fk_overlap.py` | `term03_lec04_fk_overlap.png` | Why transforms fail |
| NUCNS fan-filter bands and noise model | `plot_nucns_concept.py` | `term03_lec04_nucns_concept.png` | NUCNS |
| Curvelet tiling of the FK plane | `plot_curvelet_tiling.py` | `term03_lec04_curvelet_tiling.png` | Curvelet transform |
| Curvelet denoising before/after | `plot_curvelet_denoising.py` | `term03_lec04_curvelet_denoising.png` | Curvelet denoising |
| AAA median filter on amplitude spectra | `plot_aaa_median.py` | `term03_lec04_aaa_median.png` | Frequency-dependent median |
| FX-decon spatial prediction schematic | `plot_fx_decon_schematic.py` | `term03_lec04_fx_decon_schematic.png` | FX-deconvolution principle |
| FX-decon before/after comparison | `plot_fx_decon_result.py` | `term03_lec04_fx_decon_result.png` | FX-deconvolution result |
| SVD singular-value spectrum and rank truncation | `plot_svd_rank_truncation.py` | `term03_lec04_svd_rank_truncation.png` | SVD filtering |
| Cadzow Hankel matrix structure | `plot_cadzow_hankel.py` | `term03_lec04_cadzow_hankel.png` | Cadzow filtering |

## Key equations to include

- NUCNS noise band: $\text{noise}_i(x, y, t) = A_i \cdot w_i(t - p_x x - p_y y)$
- FX-decon complex exponential model: $X_n(f) = A(f) \cdot e^{-j 2\pi f n \Delta x / v_\text{app}}$
- FX-decon prediction error: $\varepsilon^2 = \sum_n |X_n(f) + \sum_{k=1}^K h_k X_{n-k}(f)|^2$
- SVD decomposition: $\mathbf{D} = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^T$
- SVD rank truncation: $\mathbf{D}_K = \sum_{i=1}^K \sigma_i \mathbf{u}_i \mathbf{v}_i^T$
- Curvelet parabolic scaling: length $\sim 2^{-j/2}$, width $\sim 2^{-j}$ at scale $j$

## Comprehension questions

1. Give two examples of coherent noise and two of random noise. For each, explain why it is classified that way.
2. Why can't an FK fan filter perfectly separate ground roll from reflections? What are the two failure modes?
3. What is the key difference between NUCNS and a conventional 2D FK filter? When would you choose NUCNS?
4. In the curvelet domain, why does random noise spread across many coefficients while a reflection concentrates in a few?
5. What is the "most traces are normal" assumption in AAA? What happens if it is violated?
6. A colleague applies AAA and finds that the AVO gradient on a target horizon is destroyed. What went wrong and how would you fix it?
7. In FX-deconvolution, what physical property of a linear event makes it predictable in the F-X domain?
8. Why does FX-deconvolution fail when the analysis window contains events with different dips? What are two practical solutions?
9. What is the difference between raw SVD on a trace matrix and Cadzow (Hankel-SVD) filtering? Why does the Hankel structure help?
10. In SVD filtering, when would you discard the largest singular values instead of keeping them?

## Links to wiki concepts

- `wiki/concepts/seismic_noise.md` — coherent vs random noise classification, SNR
- `wiki/concepts/nucns.md` — NUCNS noise-band model and workflow
- `wiki/concepts/curvelet_transform.md` — curvelet tiling, sparsity, thresholding
- `wiki/concepts/median_filtering_frequency_domain.md` — AAA median filter
- `wiki/concepts/fx_deconvolution.md` — FX-deconvolution principle and derivation
- `wiki/concepts/cadzow_svd_filtering.md` — SVD rank reduction and Cadzow filtering
- `wiki/concepts/adaptive_subtraction.md` — adaptive subtraction concept (links to Term 3 Lecture 03)
- `wiki/concepts/wiener_filter.md` — Wiener filter foundation (links to Term 1 Lecture 06)
- `wiki/concepts/frequency_filtering.md` — FK filtering basics (links to Term 2)
- `wiki/concepts/radon_transform.md` — tau-P transform (links to Term 2)

## Derivation documents needed

1. `lecture_notes/derivations/fx_deconvolution_derivation.en.md` (and `.ru.md`)
   - Start from the linear event model in the time domain.
   - Fourier-transform to the frequency domain: time shift → phase factor.
   - Show that the complex amplitude at each frequency is a complex exponential in space.
   - Derive the prediction filter as a complex Wiener-Hopf problem (reference Treitel 1974).
   - Show that the prediction error is the random noise.
   - Discuss the constant-dip assumption and its violation.
   - Connect to the existing `pef_ztransform_derivation.en.md` from Term 1.

## Notation to add

Add to the notation glossary in `AGENTS.md`:

| Symbol | Meaning | Russian term |
|--------|---------|--------------|
| $X_n(f)$ | Complex amplitude at frequency $f$, trace $n$ | комплексная амплитуда |
| $v_\text{app}$ | Apparent velocity of a dipping event | кажущаяся скорость |
| $p_x$, $p_y$ | Slowness components in $x$ and $y$ | компоненты медленности |
| $\sigma_i$ | $i$-th singular value | $i$-е сингулярное число |
| $\mathbf{U}$, $\mathbf{V}$ | Left and right singular vector matrices | матрицы левых и правых сингулярных векторов |
| $\mathbf{H}(f)$ | Hankel matrix at frequency $f$ | матрица Ганкеля |
| $K$ | Rank truncation parameter (number of kept singular values) | параметр усечения ранга |

## Open questions

- None — decisions made: LIFT brief mention in Section 2, multichannel spectral editing integrated into Section 5 (AAA), sorting trick integrated into Section 5 (AAA).
