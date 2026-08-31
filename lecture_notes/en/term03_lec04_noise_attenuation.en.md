---
title: Term 3 Lecture 04 — Noise Attenuation Algorithms
status: draft
term: 03
lecture: 04
---

# Noise Attenuation Algorithms

## Learning objectives

By the end of this lecture you should be able to:

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
- Term 2: FK transform, tau-P transform, dip filtering.
- Term 3 Lecture 03: adaptive subtraction concept.

## 0. Why this lecture matters

In Term 2 we learned how to use FK and tau-P transforms to separate signal from noise. A seismic gather gather goes in, a transform is applied, and in the new domain the signal and noise occupy different regions — in principle. In practice, the separation is never perfect. Coherent noise leaks through fan filters, curved events do not map to clean lines in tau-P, and random noise fills the entire transform domain, invisible to any dip-based method.

Modern processing uses specialized algorithms designed for these limitations. This lecture covers five widely used examples: **NUCNS** for coherent noise on irregular 3D land data, **curvelet-domain thresholding** for both coherent and random noise, **frequency-dependent median filtering (AAA)** for anomalous amplitude bursts, **FX-deconvolution** for random noise via spatial prediction, and **SVD/Cadzow filtering** for random and stationary noise via rank reduction. Each exploits a different mathematical property of signal vs. noise. Understanding when each works — and when it fails — is essential for choosing the right tool.

## 1. Noise types: coherent vs random

Noise is any recorded energy that is not the signal of interest for the current processing objective. Whether something counts as noise depends on the goal: a surface wave is signal for near-surface imaging (MASW, SWI) but noise for deep reflection processing.

### 1.1 Coherent noise

Coherent noise has a consistent phase relationship across traces. It follows predictable moveout curves and can be modeled or transformed. Examples:

- **Ground roll**: low-velocity, low-frequency, dispersive surface waves on land data. Dominates near offsets. Covered in detail in Term 3 Lecture 03.
- **Refracted arrivals / head waves**: first breaks and later refracted energy, often high-amplitude.
- **Air waves**: sound propagating through the atmosphere at ~330 m/s. Weak but noticeable on quiet records.
- **Multiples**: energy that reflects more than once in the subsurface. Often coherent and periodic.
- **Cultural noise with a repeating pattern**: power-line hum, machinery vibration, pump noise.

Because coherent noise is predictable, it can often be attacked by transforms (FK, tau-P, curvelet) that map it to a localized region of a new domain.

### 1.2 Random noise

Random noise has no consistent phase relationship across traces. It cannot be predicted trace-to-trace. Examples:

- **Ambient noise**: wind, microtremors, rain, distant ocean waves.
- **Instrument noise**: thermal noise in geophones, ADC quantization error, cable noise.
- **Spikes and bit noise**: single-sample amplitude bursts from transmission errors.
- **Swell noise** (marine): low-frequency, high-amplitude noise from wave action on the streamer.

Random noise is spread across the entire FK spectrum, so no dip-based transform can isolate it. Statistical methods are needed.

### 1.3 Signal-to-noise ratio

The signal-to-noise ratio is:

$$ \text{SNR} = \frac{\text{signal power}}{\text{noise power}} $$

Stacking $N$ traces improves SNR by $\sqrt{N}$ for uncorrelated noise. This is why high-fold 3D acquisition is so effective at suppressing random noise — but stacking also mixes amplitudes and can affect the true amplitude relationships needed for AVO and inversion.

### 1.4 No free lunch

There is no algorithm that removes all noise without affecting the signal:

- Aggressive denoising creates processing artefacts that can look like geology but are not.
- Subtle noise that survives processing degrades velocity analysis, AVO, and inversion.
- Every method has a parameter (threshold, filter length, rank) that trades noise removal against signal preservation.

Before applying noise attenuation, correct for acquisition-related variations: statics, velocities, and surface-consistent amplitudes (SCAC). If these are not removed first, the noise attenuation algorithm will try to model them as noise and fail.

![Shot gathers from different surveys showing common noise types](figures/term03_lec04/term03_lec04_noise_types.png){width=90%}

**Figure 1.** *Five shot gathers from different survey environments illustrating common noise types seen in field records.*

## 2. Why transforms are not enough

### 2.1 FK and tau-P: a quick recap

From Term 2, recall that the FK transform maps a shot gather $x(t, h)$ to frequency-wavenumber space $X(f, k)$. Linear events with apparent velocity $v_\text{app}$ map to lines through the origin with slope $k = f / v_\text{app}$. The tau-P transform maps to intercept time vs. ray parameter, where each linear event maps to a point.

In both domains, signal and noise occupy different regions — in principle. A fan filter in FK or a mute in tau-P should separate them.

### 2.2 Why separation fails in practice

Several factors make transform-based separation imperfect:

- **Overlap**: signal and noise share regions of FK space. Steep-dip reflections and ground roll have overlapping wavenumbers at low frequencies. A fan filter that removes all ground roll also removes some reflection energy.
- **Transition zones**: real filters are not ideal step functions. The transition between pass and reject bands either leaves residual noise or cuts into signal.
- **Spatial aliasing**: on irregular 3D geometries, non-uniform trace spacing causes energy to map to wrong wavenumbers, smearing the FK spectrum.
- **Curved events**: real reflections are hyperbolic, not linear. In tau-P, a hyperbola maps to a curve, not a point — the separation is only approximate.
- **Random noise**: fills the entire FK plane uniformly. No dip filter can isolate it.

![Schematic FK plane showing signal/noise overlap](figures/term03_lec04/term03_lec04_fk_overlap.png){width=90%}

**Figure 2.** *Schematic FK plane. Reflection energy forms a fan around the f-axis that opens toward low apparent velocities, because steeply dipping events and far-offset flanks have small moveout slopes. Ground roll occupies a broad cone at low velocities, widened by dispersion. Where the two overlap (red), no dip filter can separate them: the fan filter shown either loses signal (hatched) or lets noise leak through. Random noise (grey speckle) fills the entire plane and cannot be isolated by dip.*

### 2.3 Two strategies for modern algorithms

Given these limitations, modern noise attenuation algorithms follow one of two strategies:

1. **Model the noise** and subtract it. Examples: NUCNS, SWAMI with adaptive subtraction. The idea is to build a model of the noise wavefield, then subtract it adaptively.
2. **Model the signal** as sparse or predictable, and keep it. Examples: curvelet thresholding, FX-deconvolution, SVD filtering. The idea is to find a domain where the signal is simple and the noise is not.

 **LIFT** (Signal protection techniques): this approach models the signal (or the noise) and subtracts it from the data, treating the residual as the sum of leftover signal and noise. Signal is removed from the residual with some kind of filtering or thresholding. Remaining part of residual is then subtracted from the input data, which allows to preserve more signal with a cost of attenuating less noise.

## 3. NUCNS: coherent noise on non-uniform data

### 3.1 The problem with 2D FK on 3D land data

2D FK filtering works well when traces are uniformly spaced along a receiver line. But 3D land surveys use cross-spread geometry: irregular offsets, varying azimuths, and non-uniform trace spacing. Applying a 2D FK filter to such data causes:

- **Spatial aliasing**: non-uniform spacing smears energy across the FK plane.
- **Leakage**: noise energy maps to wavenumbers where signal also lives.
- **Geometry mismatch**: the filter assumes a regular grid that does not exist.

### 3.2 The NUCNS noise-band model

NUCNS (Non-Uniform Coherent Noise Suppression) avoids these problems by working with the actual acquisition geometry. The key idea is to model coherent noise as a sum of **noise bands**, each with approximately linear moveout:

$$ \text{noise}_i(x, y, t) = A_i \cdot w_i(t - p_x x - p_y y) $$

where $p_x$ and $p_y$ are slownesses in the $x$ and $y$ directions, $A_i$ is an amplitude factor, and $w_i$ is a noise wavelet. For linear kinematics, a single term per band is sufficient. If the moveout is curved, multiple terms or a curved kinematic operator can be used.

### 3.3 NUCNS workflow

1. **Decompose** the data into overlapping spatial windows (cross-spreads or common-shot/receiver gathers).
2. **Fan-filter** in 3D FK space: apply band-pass fan filters defined by velocity ranges to isolate noise bands.
3. **Estimate** the noise model trace-by-trace using least-squares fitting within each band. Because the actual $(x, y)$ coordinates of each trace are used, non-uniform geometry is handled naturally.
4. **Subtract** the estimated noise adaptively (a local Wiener-like filter corrects amplitude and phase mismatch).

![NUCNS fan-filter concept](figures/term03_lec04/term03_lec04_nucns_concept.png){width=90%}

**Figure 3.** *NUCNS concept. A cross-spread gather with ground roll.  3D FK spectrum showing fan-filter bands (each band isolates a velocity range). Estimated noise model doesn't have to be spatially uniform.*

### 3.4 Limitations

- **Linear moveout assumption**: each noise band must have approximately constant dip within the analysis window. Strongly curved or dispersive noise needs smaller windows or multiple terms.
- **Window size trade-off**: too large windows violate the linear-moveout assumption; too small windows do not contain enough data for reliable estimation.
- **Signal leakage**: if a reflection has the same dip as a noise band, some signal may be removed.

## 4. Curvelet-domain noise attenuation

### 4.1 What are curvelets?

Curvelets are a multiscale, multidirectional extension of wavelets. A wavelet is a small, roughly isotropic function — it captures scale and position but not orientation. A curvelet is elongated: it captures scale, position, and direction simultaneously. At fine scales, curvelets are long and thin, making them ideal for representing linear and curved seismic events.

### 4.2 Tiling the FK plane

Curvelets tile the frequency-wavenumber plane in a natural way:

- **Radial division** (scales): concentric rings divide the plane by frequency band. Each ring is an octave (factor of 2 in frequency).
- **Angular division** (directions): each ring is split into wedges, with finer angular sampling at higher frequencies.

This follows the **parabolic scaling law**: at scale $j$, a curvelet has length $\approx 2^{-j/2}$ and width $\approx 2^{-j}$. At fine scales ($j$ large), curvelets are long and thin — matching the shape of a local segment of a dipping event.

![Curvelet tiling of the FK plane](figures/term03_lec04/term03_lec04_curvelet_tiling.png){width=90%}

**Figure 4.** *Curvelet tiling of the 2D FK plane. Concentric rings represent frequency scales; angular wedges represent directions. Each tile corresponds to one curvelet basis function. At high frequency, the tiles are long and thin, aligned with dipping events.*

### 4.3 Why curvelets work for seismic data

The key property is **sparsity**. A clean seismic reflection panel has a sparse curvelet representation: a few large coefficients capture most of the energy, and the rest are near zero. Random noise, on the other hand, spreads its energy roughly equally across all curvelet coefficients. This means:

- **Signal** → few large coefficients.
- **Random noise** → many small coefficients.

Thresholding the small coefficients removes noise while preserving signal. This is analogous to how a JPEG image compressor works: keep the large coefficients, discard the small ones.

### 4.4 Noise attenuation workflow

1. Transform the data to the curvelet domain.
2. Estimate the noise level per scale-direction panel (e.g., from a quiet zone or a noise-only window).
3. Threshold or weight the coefficients: coefficients below the noise level are set to zero or scaled down; coefficients above are preserved.
4. Inverse-transform to recover the denoised data.

For coherent noise, a model-guided variant (Kustowski et al., 2013) uses a signal or noise model to design per-panel weights, rather than applying a blind threshold. An interpreter can guide the process with geological knowledge — for example, "suppress everything with this dip range at this scale."

### 4.5 Advantages and limitations

Advantages:

- Handles curved events, not just linear dips.
- Preserves amplitude and phase better than boxcar FK filters.
- Works better than conventional transforms with irregular sampling (curvelets are frame elements, not tied to grid points).

Limitations:

- Computationally expensive compared to FK or FX methods.
- Many parameters to choose: number of scales, angular divisions, threshold levels.
- If signal and noise overlap in the curvelet domain, separation is imperfect.

![Curvelet denoising before/after](figures/term03_lec04/term03_lec04_curvelet_denoising.png){width=90%}

**Figure 5.** *CMP gathers before (top) and after (bottom) curvelet-domain noise attenuation. Random noise is suppressed while reflection continuity is preserved.*

## 5. Frequency-dependent median filtering (AAA)

### 5.1 The core idea

AAA (Anomalous Amplitude Attenuation) is a statistical method that detects and suppresses noise bursts, spikes, and other "anomalous" amplitude events. It belongs to a broader family of **multichannel spectral editing** methods — any technique that edits individual traces in the frequency domain based on statistics computed across traces.

The core idea is simple: for each frequency, the "normal" amplitude is well represented by the median across traces. A trace whose amplitude is much larger (or much smaller) than the median is likely contaminated by noise.

### 5.2 How it works

For each frequency component in a spatial analysis window:

1. Compute the amplitude spectrum of every trace in the window.
2. For a given frequency $f$, collect the amplitudes $A_1, A_2, \dots, A_N$ across $N$ traces.
3. Compute the median amplitude $\tilde{A}(f)$.
4. Any trace whose amplitude $A_i(f)$ deviates too far from $\tilde{A}(f)$ is penalized — its amplitude is replaced by the median or scaled toward it.

### 5.3 Two operating modes

- **Punish deviations from median**: any trace with $|A_i(f) - \tilde{A}(f)| > \text{threshold}$ is scaled toward the median. This catches both loud bursts and suspiciously quiet traces.
- **Punish amplitudes above a level**: any trace with $A_i(f) > \tilde{A}(f) \times \text{factor}$ is attenuated. This only catches positive anomalies (loud bursts).

### 5.4 Key assumption: most traces are normal

AAA relies on the statistical assumption that at most a few traces in any analysis window contain anomalous noise. If every trace in the window is anomalous, the median itself is biased and no anomaly is detected. The window must be large enough that the "good" traces dominate the median.

The window must also follow the data kinematics — flatten the data first so that the reflection amplitudes are comparable across traces.

### 5.5 The sorting trick: making coherent noise anomalous

AAA is designed for random, trace-localized noise. But it can also target coherent noise if the data are sorted so that the noise appears isolated. For example:

- Ground roll in **shot sort** is coherent: every trace has it, so no trace is anomalous.
- The same ground roll in **random sort** appears as scattered large amplitudes on isolated traces — perfect for median-based detection.

The choice of sort determines what looks "anomalous." This is a powerful idea: by re-sorting, you can turn a coherent-noise problem into a random-noise problem.

### 5.6 AVO risk

Over-aggressive AAA can destroy legitimate **amplitude-variation-with-offset (AVO)** trends. A real AVO gradient causes amplitudes to vary systematically with offset — AAA may mistake this for anomalous noise. The solution is to use a wide enough threshold that the AVO trend is preserved.

### 5.7 Related methods

- **AMPSCAL** (amplitude scaling): similar principle but applied as a global trace scaling, not per-frequency.
- **TFCLEAN** (time-frequency cleaning): removes isolated noise bursts in a time-frequency plane.

The hierarchy is roughly AMPSCAL < TFCLEAN < AAA in sophistication and frequency selectivity.

![AAA median filter concept](figures/term03_lec04/term03_lec04_aaa_median.png){width=90%}

**Figure 6.** *Frequency-dependent median filter (AAA) concept. Top: traces within a frequency band — the anomalous trace (red) has abnormally high energy relative to the rest of the traces. Bottom: energy levels per trace with the median threshold; the outlier trace is scaled down while normal traces are preserved.*

## 6. FX-deconvolution

### 6.1 The core idea: linear events are predictable in F-X

FX-deconvolution (also called F-X prediction filtering, FXDECON, or Random Noise Attenuation — RNA) is one of the most widely used random-noise attenuation methods. The key insight is elegant: **a linear dipping event has the same waveform on every trace, just shifted in time**. In the frequency domain, this time shift becomes a simple phase factor.

Consider a single linear event with apparent velocity $v_\text{app}$:

$$ x_n(t) = w\left(t - \frac{n \Delta x}{v_\text{app}}\right) $$

where $w(t)$ is the wavelet, $n$ is the trace index, and $\Delta x$ is the trace spacing. Fourier-transforming in time:

$$ X_n(f) = W(f) \cdot e^{-j 2\pi f n \Delta x / v_\text{app}} $$

At a fixed frequency $f$, the complex amplitude $X_n(f)$ across traces is a **complex exponential** in the spatial index $n$. A complex exponential is perfectly predictable by a linear prediction filter — the same Wiener filter we studied in Term 1 Lecture 06, but now applied to complex-valued spatial data.

### 6.2 The prediction filter

For each frequency $f$, form the spatial sequence $X_0(f), X_1(f), \dots, X_{M-1}(f)$. Design a prediction-error filter (PEF) along the spatial axis:

$$ \varepsilon^2 = \sum_n \left| X_n(f) + \sum_{k=1}^K h_k X_{n-k}(f) \right|^2 \rightarrow \min $$

This is the Wiener-Levinson problem with complex-valued data (Treitel, 1974). The solution gives the prediction filter coefficients $h_k$ that best predict the next trace from the previous $K$ traces.

- **Predictable part** (signal): the linear event, captured by the PEF.
- **Unpredictable part** (residual): random noise, which cannot be predicted from neighboring traces.

Subtracting the residual from the original data gives the denoised signal. Alternatively, the predicted component itself is the clean signal estimate.

### 6.3 Why it works

- **Signal**: linear or gently curved events with consistent moveout are highly predictable in space. The PEF captures them.
- **Random noise**: uncorrelated from trace to trace. The PEF cannot predict it, so it appears in the residual.

The method is elegant because it requires no explicit model of the noise — it only assumes that the signal is spatially predictable and the noise is not.

### 6.4 Key limitation: constant dip

The prediction filter works well only when the dip (moveout) is roughly constant within the analysis window. If the window contains events with different dips, the PEF cannot predict all of them simultaneously, and signal leaks into the residual — the output looks "synthetic" or over-smoothed.

Practical solutions:

- **Short spatial windows**: use a few traces at a time, so that the constant-dip approximation is locally valid.
- **Flatten the data**: apply NMO before FX-deconvolution so that reflections are approximately horizontal (zero dip). This minimizes the dip variation within any window.
- **Time-varying windows**: split the trace into overlapping time gates and design a separate PEF for each gate.

![FX-decon principle schematic](figures/term03_lec04/term03_lec04_fx_decon_schematic.png){width=90%}

**Figure 7.** *FX-deconvolution principle. Left: several traces with a linear dipping event (blue) and random noise. At each frequency, the complex amplitude of the dipping event rotates by a constant phase increment from trace to trace — a complex exponential (right, top). Random noise has no predictable phase pattern (right, bottom). The PEF captures the exponential and leaves the noise.*

### 6.5 Extensions

- **F-X interpolation**: fill gaps in irregularly sampled data by predicting missing traces from the PEF.
- **F-X regularization**: transform irregular data onto a regular grid using the same prediction principle.
- **Multi-window adaptive**: design multiple PEFs for overlapping windows and blend the results.

![FX-decon before/after](figures/term03_lec04/term03_lec04_fx_decon_result.png){width=90%}

**Figure 8.** *Stacked section before (left) and after (right) FX-deconvolution. Random noise is suppressed, reflection continuity and structural detail are improved, and the amplitude character of the reflections is preserved.*

> **Derivation reference.** The full derivation from the linear event model through the complex Wiener filter to the prediction-error filter is in `lecture_notes/derivations/fx_deconvolution_derivation.en.md`.

## 7. SVD and Cadzow filtering

### 7.1 SVD: the basic idea

Singular Value Decomposition (SVD) is a matrix factorization method from linear algebra. Organize $M$ traces (each of length $N$) as columns of a data matrix $\mathbf{D}$:

$$ \mathbf{D} = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^T $$

- $\mathbf{U}$: left singular vectors (trace-shaped basis functions).
- $\mathbf{V}$: right singular vectors (spatial patterns across traces).
- $\boldsymbol{\Sigma}$: diagonal matrix of singular values $\sigma_1 \geq \sigma_2 \geq \dots \geq \sigma_r > 0$.

The key insight is that **seismic signal lives in a low-dimensional subspace**. A single dipping event can be described by one singular value and its pair of singular vectors (rank 1). Multiple events with different dips need a few more. Random noise, on the other hand, fills the full space — it contributes to all singular values, especially the small ones.

### 7.2 Two SVD filtering strategies

**Strategy 1 — remove random noise (keep the largest singular values).** If the signal is low-rank and the noise is random, the singular-value spectrum shows a "knee": a few large values for signal, many small values for noise. Truncate to the $K$ largest:

$$ \mathbf{D}_\text{denoised} = \sum_{i=1}^{K} \sigma_i \mathbf{u}_i \mathbf{v}_i^T $$

**Strategy 2 — remove strong stationary noise (discard the largest singular values).** When the record contains strong, spatially coherent noise (ground roll, power-line hum), that noise dominates the first few singular values. The signal occupies the smaller ones. Discard the top $K$ components and keep the rest.

The choice of strategy depends on the noise type and the relative energy of signal vs. noise.

### 7.3 Cadzow filtering: SVD with Hankel structure

Raw SVD on the trace matrix is simple but does not exploit the prediction structure of the data. **Cadzow filtering** applies SVD in the F-X domain with a Hankel matrix constraint.

The workflow:

1. Select a spatial window of $M$ adjacent traces.
2. Fourier-transform each trace in time to get complex amplitudes $X_n(f)$.
3. For each frequency $f$, form a **Hankel matrix** from the spatial sequence:

$$ \mathbf{H}(f) = \begin{bmatrix} X_0 & X_1 & X_2 \\ X_1 & X_2 & X_3 \\ X_2 & X_3 & X_4 \end{bmatrix} $$

A Hankel matrix has constant anti-diagonals — each skew-diagonal contains the same value. This structure enforces the prediction property: a single plane wave produces a rank-1 Hankel matrix.

4. Compute SVD of $\mathbf{H}(f)$ and truncate to rank $K$.
5. Flatten the rank-truncated Hankel matrix back to a 1D sequence by averaging along the anti-diagonals.
6. Inverse-Fourier-transform back to the time domain.

**Why the Hankel structure helps**: a single plane wave at frequency $f$ is a rank-1 Hankel matrix. Multiple plane waves give rank $p$. By forcing low rank per frequency, Cadzow keeps only the plane-wave structure and discards noise. It is the algebraic counterpart of FX-deconvolution — under certain conditions, Cadzow and FX-decon are equivalent.

### 7.4 KL transform

The Karhunen-Loève (KL) transform decomposes the data into uncorrelated random vectors. For a zero-mean data matrix, KL is mathematically equivalent to SVD of the covariance matrix $\mathbf{D}^T \mathbf{D}$. The KL components are the right singular vectors, ranked by eigenvalue. Truncating KL components is the same as SVD rank truncation.

### 7.5 Practical notes

- Apply Cadzow to **flattened gathers** (after NMO or dip scan) so that events are approximately horizontal. This minimizes the rank of the signal subspace.
- The spatial window length creates a trade-off: longer windows capture more of the wavelet character but increase the signal rank and may span varying dips.
- Over-aggressive rank truncation damages AVO and removes weak events.

![SVD rank truncation](figures/term03_lec04/term03_lec04_svd_rank_truncation.png){width=90%}

**Figure 9.** *SVD rank truncation. (a) Noisy synthetic gather with three flat reflection events. (b) Singular-value spectrum on a log scale, showing a clear knee: three large signal singular values followed by a noise floor. (c) Denoised gather after keeping only the top 3 singular values — the signal is recovered while random noise is suppressed.*

![Cadzow / Hankel-SVD filtering scheme](figures/term03_lec04/term03_lec04_cadzow_hankel.png){width=90%}

**Figure 10.** *Cadzow filtering step-by-step scheme. (1) Input spatial sequence of complex amplitudes from the F-X domain. (2) Form a Hankel matrix with constant anti-diagonals enforcing the linear-prediction property. (3) Compute the SVD: signal energy concentrates in the first singular values, noise spreads across all. (4) Truncate to rank K (keep signal subspace). (5) Reconstruct by anti-diagonal averaging. (6) Output denoised sequence.*

## 8. Summary

- **Noise is relative**: coherent noise is predictable (ground roll, refractions, multiples); random noise is not (ambient, instrument, spikes).
- **Transforms are not enough**: FK and tau-P help but have overlap, aliasing, and transition-zone problems. Random noise is inseparable by dip alone.
- **Five algorithms, five principles**:

| Method | Noise type | Principle | Key assumption | Main failure mode |
|--------|-----------|-----------|----------------|-------------------|
| NUCNS | Coherent | Model noise bands in 3D FK | Linear moveout per band | Curved noise, signal leakage |
| Curvelet | Both | Sparse representation | Signal is sparse in curvelet domain | Signal/noise overlap in curvelet space |
| AAA | Random (bursts) | Median per frequency | Most traces are normal | All traces anomalous; AVO damage |
| FX-decon | Random | Spatial prediction of complex exponentials | Constant dip in window | Variable dip → signal in residual |
| SVD/Cadzow | Random / stationary | Rank reduction | Signal is low-rank | Over-truncation damages AVO |

- **No free lunch**: every method has a parameter (threshold, filter length, rank) that trades noise removal against signal preservation. The art of processing is choosing the right method and the right parameter for each situation.

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

## Suggested reading and sources

- Canales (1984) — original F-X noise reduction concept; `wiki/sources/canales1984_fx_decon.md`.
- Gulunay (1986) — FXDECON practical implementation; `wiki/sources/gulunay1986_fxdecon.md`.
- Abma & Claerbout (1995) — comparison of t-x and f-x prediction; `wiki/sources/abma1995_lateral_prediction.md`.
- Treitel (1974) — complex Wiener filter theory; `wiki/sources/treitel1974_complex_wiener.md`.
- Денисов & Фиников (2010) — practical aspects of F-X deconvolution (in Russian); `wiki/sources/denisov_finikov_2010.md`.
- Hennenfent & Herrmann (2006) — curvelet introduction for seismic denoising; `wiki/sources/hennenfent2006_curvelet_intro.md`.
- Hennenfent et al. (2011) — interpretative noise attenuation in the curvelet domain; `wiki/sources/hennenfent2011_interpretative_noise.md`.
- Kustowski et al. (2013) — model-guided curvelet denoising; `wiki/sources/kustowski2013_curvelet_model_guided.md`.
- Herrmann et al. (2007) — curvelet primary-multiple separation; `wiki/sources/herrmann2007_curvelet_multiple_separation.md`.
- NUCNS technical documentation; `wiki/sources/nucns.md`.
- NUCNS best practice; `wiki/sources/nucns_best_practice.md`.
- Cadzow best practice; `wiki/sources/cadzow_best_practice.md`.
- CGG ODT02 — denoising course (intro, median, swell noise, K-filter, linear noise, tau-P); `wiki/sources/cgg_odt02_denoise.md`.
- Bormann & Wielandt (2013) — seismic signals and noise (NMSOP Ch. 4); `wiki/sources/bormann_wielandt_seismic_signals_noise.md`.
- Kneppers — basic geophysics noise attenuation training; `wiki/sources/kneppers_basic_geophysics.md`.
- Derivation: `lecture_notes/derivations/fx_deconvolution_derivation.en.md`.
