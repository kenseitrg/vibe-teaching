# Slide outline — Term 1, Lecture 7: Surface-consistent deconvolution and practical implementation

## Slide 1 — Title
- **Title:** Surface-consistent deconvolution and practical implementation
- **Subtitle:** Stable operators from surface geometry
- Figure: none

## Slide 2 — Recap and limitations
- Single-channel deconvolution assumes stationarity and high S/N.
- Noise, short windows, variable coupling, near-surface effects break this.
- Need a method that uses redundancy of surface geometry.

## Slide 3 — Surface-consistent idea
- Trace wavelet = source * receiver * offset * CDP factors.
- Each surface location appears in many traces.
- More statistics → more stable operators.
- Figure: `term01_lec07_surface_consistent_model.png`

## Slide 4 — The four-factor model
- Equation: $w_{s,r,h,c} = s_s * r_r * h_h * c_c$.
- In frequency domain: multiplication.
- In log domain: addition → linear system.

## Slide 5 — Linear system $d = Gm$
- $d$: observed log-spectra/autocorrelations.
- $m$: unknown source/receiver/offset/CDP terms.
- $G$: sparse design matrix.
- Least-squares solution; robust variants.

## Slide 6 — Example
- Trace-by-trace vs. surface-consistent on noisy synthetic gather.
- Figure: `term01_lec07_surface_consistent_example.png`

## Slide 7 — Parallels
- Surface-consistent deconvolution ↔ residual statics.
- Surface-consistent deconvolution ↔ surface-consistent amplitude corrections.
- Same geometry, same design-matrix structure.

## Slide 8 — Parameter choices
- Prediction gap: 1 sample (spiking) vs. reverberation period.
- Operator length: wavelet length, not too long.
- Prewhitening: 0.1–5%.
- Analysis window: signal, no ground roll/multiples, gain balanced.
- Figure: `term01_lec07_parameter_scan.png`

## Slide 9 — Practical implementation: deterministic deconvolution
- Python function using prewhitened spectral division.
- Show code snippet.
- Figure: `term01_lec07_demo_deterministic_decon.png`

## Slide 10 — Practical implementation: Wiener normal equations
- Build autocorrelation matrix $\mathbf{R}$.
- Solve $\mathbf{R} \mathbf{f} = \mathbf{d}$.
- Show code snippet.
- Figure: `term01_lec07_demo_wiener_matrix.png`

## Slide 11 — Tiny surface-consistent system
- 3 shots, 3 receivers, 4 traces.
- Design matrix $G$ and least-squares solution.
- Emphasize scalability.

## Slide 12 — Choosing a deconvolution flow
- Deterministic: measured signature available.
- Predictive: reverberations/multiples.
- Statistical: general compression, no signature.
- Surface-consistent: noisy/variable land data.
- Typical marine and land flows.

## Slide 13 — Summary
- Trace-by-trace methods are local and noisy.
- Surface-consistent methods exploit geometry.
- Parameters balance compression, multiple suppression, and noise.
- Implementation is matrix/spectral operations in Python.

## Slide 14 — Concept check
- Why does surface consistency need trace redundancy?
- When prefer deterministic over statistical?
- Effect of prewhitening at weak frequencies?
