# Draft outline: Deconvolution (two 90-minute sessions)

> Based on the instructor's lecture flow and existing slides/plan in `slides/raw/`.

## Lecture numbering options

- Option A (course structure in `AGENTS.md`): split into
  - `term01_lec06_single_channel_deconvolution`
  - `term01_lec07_surface_consistent_deconvolution`
- Option B (follow existing slide/deck name): `term01_lec05_deconvolution` as a single two-part lecture.

Please confirm which numbering to use.

---

## Session 1 — Single-channel deconvolution (~90 min)

### 1. Introduction: why deconvolution? (10 min)
- Goal of seismic processing: recover band-limited earth reflectivity.
- What deconvolution does: wavelet compression, reverberation suppression, phase control.
- What it cannot do: recover frequencies that were never recorded.

### 2. Convolutional model of a seismic trace (10 min)
- `x(t) = w(t) * r(t) + n(t)`
- Components of the embedded wavelet (signature, ghosts, bubble, instrument response).
- Assumptions: stationarity, white reflectivity, minimum phase, additive noise.

### 3. Phase and the Z-transform (20 min)
- Z-transform as a compact notation for discrete convolution.
- Link to Fourier: `z = e^{-i 2 \pi f \Delta t}`.
- Minimum-phase, maximum-phase, zero-phase, causal wavelets.
- **Dipole proof**: why a causal wavelet with a stable inverse is front-loaded.
- Consequences: convolution of minimum-phase signals is minimum phase.

### 4. Deterministic deconvolution (20 min)
- Wavelet is known or measured.
- Fourier form: spectral division, `F(f) = 1 / W(f)`.
- Z-domain form: polynomial division.
- Why non-minimum-phase / mixed-phase wavelets need non-causal coefficients.
- Regularization (prewhitening): add `\varepsilon^2` to the denominator.
- Examples: designature, instrument response removal, vibroseis-to-minimum-phase conversion.

### 5. Statistical deconvolution — Wiener filter (20 min)
- Wavelet shape unknown; derive filter from data.
- Least-squares derivation of Wiener-Hopf equations.
- Matrix form and prewhitening.
- Why the conditions matter: minimum phase, stationary wavelet, white reflectivity, white noise.
- Wiener-Levinson recursion (mention, do not derive in class).

### 6. Spiking and predictive deconvulation (10 min)
- Spiking deconvolution = prediction distance of one sample.
- Predictive deconvolution: prediction-error operator.
- Parameter effects: prediction gap, operator length, prewhitening.

### Comprehension check / discussion (0–5 min buffer)

---

## Session 2 — Surface-consistent deconvolution and practical implementation (~90 min)

### 1. Recap of single-channel limits (5 min)
- Trace-by-trace operators are noisy and inconsistent.
- Short windows, ground roll, and variable coupling bias the operator.

### 2. Surface-consistent deconvolution (25 min)
- Four-factor model: source, receiver, offset, CDP.
- Trace as convolution of source and receiver wavelets with reflectivity.
- Derivation of the linear system `d = G m`.
- Brief solution methods: least-squares, robust/median approaches.
- Parallels with residual statics and surface-consistent amplitude corrections.

### 3. Deconvolution parameters in practice (15 min)
- Prediction distance: one sample (spiking) vs. water-bottom period (reverberations).
- Operator length: too short → incomplete; too long → noise.
- Prewhitening / additive noise stabilization.
- Analysis window selection: avoid multiples and ground roll.
- QC: autocorrelation before/after, residual wavelet checks.

### 4. Practical implementation demo (30 min)
- Simple deterministic deconvolution in Python (spectral division with prewhitening).
- Wiener normal equations as matrix operations in Python/NumPy.
- Build a spiking operator and apply it to a synthetic trace.
- Show effect of violating assumptions (non-minimum-phase wavelet, colored noise).

### 5. Choosing a deconvolution flow (10 min)
- When to use deterministic vs. statistical vs. predictive vs. surface-consistent.
- Typical marine/land processing sequences.

### 6. Comprehension questions and exercises (5 min)

---

## Figures needed

1. Convolutional model: reflectivity + wavelet = trace.
2. Minimum-, maximum-, zero-phase wavelets with same amplitude spectrum.
3. Dipole illustration: roots inside/outside unit circle.
4. Deterministic deconvolution: known wavelet → inverse filter → spike/desired output.
5. Effect of prewhitening on inverse filter stability.
6. Wiener spiking deconvolution on synthetic trace.
7. Predictive deconvolution: prediction gap and operator length sweep.
8. Surface-consistent model: source/receiver/offset/CDP factors.
9. Practical demo screenshots/code snippets.

## Python demos

- `demo_deterministic_decon.py`
- `demo_wiener_spiking_decon.py`
- `demo_predictive_decon.py`
- `demo_surface_consistent_model.py` (small linear system)

## Sources to ingest / update in wiki

- Margrave (2006) *Methods of Seismic Data Processing* — chapters on convolutional model, phase, deconvolution.
- Yilmaz (2001) *Seismic Data Analysis* — deconvolution chapter.
- Hatton *Seismic Data Processing* — minimum-phase dipole proof (DJVU extraction pending).
