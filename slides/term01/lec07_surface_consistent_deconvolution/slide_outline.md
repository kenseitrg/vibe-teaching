# Slide outline — Term 1, Lecture 7: Surface-consistent deconvolution and practical implementation

## Slide 1 — Surface-consistent deconvolution and practical implementation
- Stable operators from surface geometry
- Figure: none

## Slide 2 — Learning objectives
- Reduce near-surface influence on source and receiver wavelets.
- Write the four-factor model and the linear system $d = Gm$.
- Choose deconvolution parameters (gap, length, prewhitening, window).
- Implement deterministic deconvolution and Wiener normal equations in Python.
- Compare methods and choose an appropriate processing flow.

## Slide 3 — Why trace-by-trace deconvolution is not always enough
- Single-channel deconvolution assumes stationarity and high S/N.
- Land/OBC data: coupling, near-surface filtering, and noise change from trace to trace.
- Trace-by-trace operators are estimated from too few samples and can amplify noise.
- Need a method that uses the redundancy of surface geometry.

## Slide 4 — Surface-consistent idea
- Effective trace wavelet = source * receiver * offset * CDP factors.
- Source and receiver factors encode near-surface effects to compensate.
- Offset and CDP factors encode the geological response to preserve.
- Each surface location appears in many traces → more stable operators.
- After removing near-surface factors, a single spiking operator can be applied across the survey.
- Figure: `term01_lec07_surface_consistent_model.png`

## Slide 5 — The four-factor model
- Equation: $w_{s,r,h,c}(t) = s_s(t) * r_r(t) * h_h(t) * c_c(t)$.
- Full trace model: $x_{s,r,h,c}(t) = w_{s,r,h,c}(t) * r_{s,r,h,c}(t) + n_{s,r,h,c}(t)$.
- Frequency domain: convolution becomes multiplication.
- Log domain: multiplication becomes addition → linear system.

## Slide 6 — Linear system $d = Gm$
- $d$: observed log-spectra/autocorrelations from all traces.
- $m$: unknown source/receiver/offset/CDP log-spectra.
- $G$: sparse design matrix (one row per trace, four ones per row).
- Least-squares solution: $m = (G^T G)^{-1} G^T d$.
- Robust variants (L1, Huber, median) reduce influence of noisy traces.

## Slide 7 — Example
- Trace-by-trace vs. surface-consistent on real data.
- Surface-consistent result has better event continuity and less noise.
- Figure: `term01_lec07_surface_consistent_example.png`

## Slide 8 — Parallels
- Surface-consistent deconvolution ↔ residual statics.
- Surface-consistent deconvolution ↔ surface-consistent amplitude corrections.
- Same geometry, same sparse design-matrix structure.

## Slide 9 — Deconvolution parameters in practice
- Prediction gap:
  - 1 sample → spiking, full wavelet compression.
  - First/second zero crossing of autocorrelation → partial compression / multiple suppression.
  - Reverberation period → reverberation suppression, wavelet preserved.
- Operator length: roughly wavelet length; too long leaks noise.
- Prewhitening: 0.1–5% for stability.
- Analysis window: reflections only; exclude multiples, ground roll, first breaks, guided waves.
- Figure: `term01_lec07_parameter_scan.png`

## Slide 10 — Practical implementation: deterministic deconvolution
- Prewhitened spectral division: $F(f) = W^*(f) / (|W(f)|^2 + \varepsilon^2 \max |W|^2)$.
- Python function `deterministic_decon(trace, wavelet, dt, eps)`.
- Show code snippet.
- Figure: `term01_lec07_demo_deterministic_decon.png`

## Slide 11 — Practical implementation: Wiener normal equations
- Build symmetric Toeplitz autocorrelation matrix $\mathbf{R}$.
- Solve $\mathbf{R} \mathbf{f} = \mathbf{d}$ for the spiking operator.
- Python function `wiener_spiking_operator(trace, n_op, eps)`.
- Show code snippet.
- Figure: `term01_lec07_demo_wiener_matrix.png`

## Slide 12 — Tiny surface-consistent system
- 3 shots, 3 receivers, 4 traces.
- Design matrix $G$ and least-squares solution `lstsq(G, d)`.
- Emphasize scalability to thousands of shots/receivers.

## Slide 13 — Choosing a deconvolution flow
- Deterministic: measured signature available (designature).
- Predictive: reverberations / short-period multiples.
- Statistical: general compression, no signature measurement.
- Surface-consistent: noisy/variable land and OBC data (preferred).
- Typical marine flow: designature → deghosting → predictive deconvolution → zero-phase shaping.
- Typical land flow: min-phase conversion → instrument inverse filter → surface-consistent deconvolution → zero-phasing.

## Slide 14 — Summary
- Trace-by-trace methods are local and noisy when coupling/near surface vary.
- Surface-consistent methods exploit geometry to separate near-surface source/receiver effects from geological offset/CDP effects.
- Parameter choices balance wavelet compression, multiple suppression, and noise amplification.
- Implementation is matrix/spectral operations in Python.

## Slide 15 — Concept check
- Why does surface consistency need trace redundancy?
- When would you prefer deterministic over statistical deconvolution?
- How does prewhitening affect weak-frequency parts of the spectrum?
- What is the parallel between surface-consistent deconvolution and residual statics?
