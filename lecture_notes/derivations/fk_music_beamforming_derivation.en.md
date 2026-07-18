---
title: "Derivation of the FK-MUSIC Beamforming Method"
status: draft
---

# Derivation of the FK-MUSIC Beamforming Method

This document derives the FK-MUSIC method for measuring surface-wave phase velocity dispersion from array seismic data. It follows the pedagogical development of Datta (2018) and expands the conceptual discussion of Term 3 Lecture 03 (§6) with the full mathematical chain.

> **Why this matters.** The dispersion image is the primary tool for extracting modal phase velocities from a multichannel shot gather. Understanding how FK-MUSIC produces sharper spectra than conventional stacking — and where the improvement comes from — requires tracing the method from the beamforming idea through eigenanalysis to the final pseudo-spectrum.

> **Prerequisites.** Complex exponentials, matrix eigenvalues and eigenvectors, Hermitian matrices, basic linear algebra (inner products, orthogonality).

> **What this document does not do.** It does not derive the slant-stack or UC-diagram methods in full; those are covered in Datta (2018) and Socco et al. (2010). It focuses on the mathematical chain that leads from conventional beamforming to MUSIC.

---

## 1. The beamforming idea

We record surface waves on an array of $M$ receivers at positions $x_1, x_2, \ldots, x_M$. At angular frequency $\omega$, the record at receiver $i$ is a complex number $U(x_i, \omega)$ — the Fourier transform of the time series.

In the plane-wave approximation, the wavefield at receiver $i$ is a sum of $N_s$ modes:

$$
U(x_i, \omega) = \sum_{m=1}^{N_s} F_m(x_i, \omega)\, e^{i k_m x_i},
$$

where $k_m$ is the wavenumber of mode $m$ and $F_m$ is its amplitude (which may depend on receiver position through site effects, radiation pattern, etc.).

The problem is: given the vector of records $\mathbf{Y} = [U(x_1, \omega),\, U(x_2, \omega),\, \ldots,\, U(x_M, \omega)]^T$, estimate the wavenumbers $k_m$ — equivalently, the phase velocities $c_m = \omega / k_m$.

All array-based methods attack this by **steering**: apply a trial phase shift to each receiver and stack. When the trial phase shift compensates the true propagation phase of a mode, the traces add constructively.

---

## 2. The spatial correlation matrix

Define the **spatial correlation matrix** (also called the cross-spectral matrix):

$$
\mathbf{R} = \mathbf{Y}\,\mathbf{Y}^\dagger,
$$

where $\dagger$ denotes conjugate transpose. Element $(i, j)$ of $\mathbf{R}$ is:

$$
R_{ij} = U(x_i, \omega)\, U^*(x_j, \omega).
$$

This is the product of the frequency-domain record at receiver $i$ with the complex conjugate of the record at receiver $j$. It encodes the relative phase between every receiver pair.

The matrix $\mathbf{R}$ is **Hermitian** ($\mathbf{R} = \mathbf{R}^\dagger$) and **positive semi-definite** (since $\mathbf{R} = \mathbf{Y}\mathbf{Y}^\dagger$). These two properties guarantee that its eigenvalues are real and non-negative, and its eigenvectors are mutually orthogonal — facts we will exploit shortly.

In practice, $\mathbf{R}$ is estimated by averaging over time windows or frequency samples. The derivation below uses the sample estimate; the algebra is the same for the population matrix.

---

## 3. Conventional beamforming

### 3.1 Steering vector

Define the **steering vector** for a trial wavenumber $k$:

$$
\mathbf{e}(k) = \begin{bmatrix} e^{ikx_1} \\ e^{ikx_2} \\ \vdots \\ e^{ikx_M} \end{bmatrix}.
$$

Its $i$-th element is the phase shift that a plane wave with wavenumber $k$ would accumulate at receiver $i$ relative to the origin. The steering vector depends on the array geometry and the trial wavenumber, but not on the data.

### 3.2 Output power

The beamformer's output is the inner product of the steering vector with the data:

$$
Z(k) = \mathbf{e}^\dagger(k)\, \mathbf{Y}.
$$

This is a scalar: it stacks all receivers after compensating for the trial propagation phase. The **output power** is:

$$
P(k) = |Z|^2 = \mathbf{e}^\dagger \mathbf{Y}\, \mathbf{Y}^\dagger \mathbf{e} = \mathbf{e}^\dagger \mathbf{R}\, \mathbf{e}.
$$

This is the fundamental beamforming equation. The output power is a quadratic form in the steering vector, with the correlation matrix as the kernel.

### 3.3 Why it works

Expand $\mathbf{R}$ using the plane-wave model:

$$
\mathbf{R} = \sum_{m=1}^{N_s} \mathbf{f}_m \mathbf{f}_m^\dagger,
$$

where $\mathbf{f}_m$ is the vector of mode-$m$ amplitudes across the array (absorbing the phase factor into $\mathbf{f}_m$). Then:

$$
P(k) = \sum_{m=1}^{N_s} \left| \mathbf{e}^\dagger(k)\, \mathbf{f}_m \right|^2.
$$

When $k = k_m$ (the trial wavenumber matches a true mode), the inner product $\mathbf{e}^\dagger \mathbf{f}_m$ is large because the steering vector and the mode have the same phase pattern. When $k$ does not match any mode, the inner products are small due to destructive interference.

The output power $P(k)$ therefore peaks at the true modal wavenumbers. Sweeping $k$ (or equivalently $c = \omega/k$) at each frequency produces the conventional dispersion image.

### 3.4 Limitation

The resolution of conventional beamforming is limited by the array aperture: two modes with closely spaced wavenumbers produce overlapping peaks in $P(k)$. The width of each peak is approximately $\Delta k \sim 2\pi / L$, where $L$ is the array length. To resolve two modes, their wavenumber separation must exceed this limit.

---

## 4. The minimum variance beamformer

### 4.1 Adaptive weighting

The conventional beamformer (§3) uses fixed weights: every receiver contributes equally after the phase correction. This means the beamformer has a fixed **beam pattern** — it responds not only to the trial direction but also to nearby directions through sidelobes. Any interfering mode whose wavenumber falls within the main lobe or a strong sidelobe leaks into the output and broadens the peak.

An **adaptive** beamformer adjusts the weights to suppress this interference. The idea is: find weights $\mathbf{w}$ that minimize the total output power $\mathbf{w}^\dagger \mathbf{R}\, \mathbf{w}$ while keeping the response at the trial wavenumber undistorted, i.e., subject to the constraint $\mathbf{w}^\dagger \mathbf{e} = 1$.

Why this works. The total output power $\mathbf{w}^\dagger \mathbf{R}\, \mathbf{w}$ is the sum of contributions from all sources in the wavefield — the desired signal at the trial wavenumber, interfering modes at other wavenumbers, and noise. By minimizing this total power while forcing the beamformer to pass the trial direction with unit gain ($\mathbf{w}^\dagger \mathbf{e} = 1$), the optimization is forced to do the only thing left: **suppress everything that is not in the trial direction**. The resulting weights place deep nulls in the directions of interfering modes while maintaining a distortionless response at the trial wavenumber.

The constrained optimization is solved with Lagrange multipliers. Define the Lagrangian:

$$
\mathcal{L}(\mathbf{w}, \lambda) = \mathbf{w}^\dagger \mathbf{R}\, \mathbf{w} - \lambda\, (\mathbf{w}^\dagger \mathbf{e} - 1) - \lambda^*\, (\mathbf{e}^\dagger \mathbf{w} - 1).
$$

Setting $\partial \mathcal{L} / \partial \mathbf{w}^* = 0$ gives $\mathbf{R}\, \mathbf{w} = \lambda\, \mathbf{e}$, so $\mathbf{w} = \lambda\, \mathbf{R}^{-1}\, \mathbf{e}$. The constraint $\mathbf{w}^\dagger \mathbf{e} = 1$ fixes $\lambda = 1 / (\mathbf{e}^\dagger \mathbf{R}^{-1}\, \mathbf{e})$, yielding:

$$
\mathbf{w} = \frac{\mathbf{R}^{-1}\, \mathbf{e}}{\mathbf{e}^\dagger \mathbf{R}^{-1}\, \mathbf{e}}.
$$

The output power of the **minimum variance beamformer** (also called the Capon beamformer) is:

$$
P_\text{MV}(k) = \mathbf{w}^\dagger \mathbf{R}\, \mathbf{w} = \frac{1}{\mathbf{e}^\dagger(k)\, \mathbf{R}^{-1}\, \mathbf{e}(k)}.
$$

### 4.2 Why MV is sharper

The MV beamformer is more selective than conventional beamforming because it actively nulls interferers rather than simply averaging over them. Two modes with closely spaced wavenumbers, which would produce overlapping peaks in conventional beamforming, now produce narrower and better-separated peaks because the beamformer designed for one mode places a null in the direction of the other.

However, $P_\text{MV}$ still depends on the full inverse $\mathbf{R}^{-1}$, which mixes signal and noise information. MUSIC separates these two contributions.

---

## 5. Eigenanalysis of $\mathbf{R}$

### 5.1 Eigendecomposition

Since $\mathbf{R}$ is Hermitian and positive semi-definite, it has an eigendecomposition:

$$
\mathbf{R} = \sum_{i=1}^{M} \lambda_i\, \mathbf{u}_i\, \mathbf{u}_i^\dagger,
$$

where $\lambda_1 \ge \lambda_2 \ge \cdots \ge \lambda_M \ge 0$ are the eigenvalues and $\mathbf{u}_1, \mathbf{u}_2, \ldots, \mathbf{u}_M$ are the corresponding orthonormal eigenvectors ($\mathbf{u}_i^\dagger \mathbf{u}_j = \delta_{ij}$).

The eigenvectors form a complete orthonormal basis for $\mathbb{C}^M$. Any vector $\mathbf{x} \in \mathbb{C}^M$ can be written as $\mathbf{x} = \sum_i (\mathbf{x}^\dagger \mathbf{u}_i)\, \mathbf{u}_i$.

### 5.2 Quadratic forms in the eigenbasis

For any vector $\mathbf{x}$, the quadratic form $\mathbf{x}^\dagger \mathbf{R}\, \mathbf{x}$ can be rewritten using the eigendecomposition:

$$
\mathbf{x}^\dagger \mathbf{R}\, \mathbf{x} = \sum_{i=1}^{M} \lambda_i\, |\mathbf{x}^\dagger \mathbf{u}_i|^2.
$$

Similarly, for $\mathbf{R}^{-1}$ (assuming all eigenvalues are positive):

$$
\mathbf{x}^\dagger \mathbf{R}^{-1}\, \mathbf{x} = \sum_{i=1}^{M} \lambda_i^{-1}\, |\mathbf{x}^\dagger \mathbf{u}_i|^2.
$$

These expansions are the key to understanding how MUSIC separates signal from noise.

---

## 6. Signal and noise subspaces

### 6.1 The split

In the plane-wave model with $N_s$ modes and additive noise, the correlation matrix takes the form:

$$
\mathbf{R} = \mathbf{R}_\text{signal} + \sigma^2 \mathbf{I},
$$

where $\mathbf{R}_\text{signal}$ has rank $N_s$ (it is the sum of $N_s$ outer products) and $\sigma^2 \mathbf{I}$ represents uncorrelated noise with variance $\sigma^2$.

The eigenvalues of $\mathbf{R}$ are:

- **Signal eigenvalues**: $\lambda_1, \ldots, \lambda_{N_s}$, which are large (signal + noise).
- **Noise eigenvalues**: $\lambda_{N_s+1} = \cdots = \lambda_M = \sigma^2$, which are all equal to the noise variance.

The corresponding eigenvectors split into two orthogonal subspaces:

- **Signal subspace** $\mathcal{S}$: spanned by $\mathbf{u}_1, \ldots, \mathbf{u}_{N_s}$. This subspace contains the directions in which the wavefield has energy — it is spanned by the mode propagation vectors.
- **Noise subspace** $\mathcal{N}$: spanned by $\mathbf{u}_{N_s+1}, \ldots, \mathbf{u}_M$. This subspace contains only noise directions.

These two subspaces are **orthogonal complements**: $\mathcal{S} \perp \mathcal{N}$, and $\mathcal{S} \oplus \mathcal{N} = \mathbb{C}^M$.

### 6.2 Determining $N_s$

The number of signal eigenvectors $N_s$ equals the number of modes present at the analysis frequency. In practice, $N_s$ is estimated by counting eigenvalues that are significantly larger than the noise floor. Alternatively, as Datta (2018) does, $N_s$ can be fixed as an input parameter: build $\mathbf{R}$ from a narrow band of frequency samples (rather than a single frequency) so that its rank is at most $N_s$.

---

## 7. From minimum variance to MUSIC

### 7.1 Rewriting $P_\text{MV}$

Substitute the eigenbasis expansion of $\mathbf{R}^{-1}$ into the MV output power:

$$
P_\text{MV}(k) = \frac{1}{\mathbf{e}^\dagger \mathbf{R}^{-1} \mathbf{e}} = \frac{1}{\displaystyle\sum_{i=1}^{M} \lambda_i^{-1}\, |\mathbf{e}^\dagger \mathbf{u}_i|^2}.
$$

Split the sum into signal and noise contributions:

$$
P_\text{MV}(k) = \frac{1}{\displaystyle\underbrace{\sum_{i=1}^{N_s} \lambda_i^{-1}\, |\mathbf{e}^\dagger \mathbf{u}_i|^2}_{\text{signal subspace}} + \underbrace{\sum_{i=N_s+1}^{M} \lambda_{\min}^{-1}\, |\mathbf{e}^\dagger \mathbf{u}_i|^2}_{\text{noise subspace}}},
$$

where $\lambda_{\min} = \sigma^2$ is the common noise eigenvalue.

### 7.2 The MUSIC idea

The two subspaces are orthogonal complements. When the steering vector $\mathbf{e}(k)$ matches a true modal wavenumber $k_m$, it lies entirely in the signal subspace $\mathcal{S}$, so:

$$
\mathbf{e}^\dagger \mathbf{u}_i = 0 \quad \text{for all } i = N_s+1, \ldots, M.
$$

That is, $\mathbf{e}$ is orthogonal to every noise eigenvector. The noise subspace sum vanishes, and the reciprocal of the MV output power is dominated by the signal contribution — it is small, so $P_\text{MV}$ is large.

When $\mathbf{e}(k)$ does not match any mode, it has a component in the noise subspace. The noise sum is non-zero, and $P_\text{MV}$ is smaller.

**MUSIC** (Schmidt, 1986) observes that the signal subspace contribution in the denominator is unnecessary for locating the peaks. Since we only care about *where* $P_\text{MV}$ is large (i.e., where $\mathbf{e}$ is orthogonal to the noise), we can drop the signal subspace sum and set all noise eigenvalues to unity (whitening). This gives the **MUSIC pseudo-spectrum**:

$$
P_\text{MUSIC}(k) = \frac{1}{\displaystyle\sum_{i=N_s+1}^{M} |\mathbf{e}^\dagger(k)\, \mathbf{u}_i|^2}.
$$

### 7.3 Why this is sharper

The key difference from $P_\text{MV}$:

- $P_\text{MV}$ uses $\lambda_i^{-1}$ weighting: large signal eigenvalues contribute small terms, and the noise eigenvalue $\lambda_{\min}$ contributes a constant. The peaks are modulated by the signal eigenvalue structure.
- $P_\text{MUSIC}$ uses uniform weighting (all noise eigenvalues set to 1): the peaks are determined purely by the geometric alignment between the steering vector and the noise subspace.

Because the noise eigenvectors are orthogonal to the signal subspace, the sum $\sum |\mathbf{e}^\dagger \mathbf{u}_i|^2$ vanishes exactly when $\mathbf{e}$ is a signal direction. The transition from "large" (off-mode) to "zero" (on-mode) is sharper than the transition in $P_\text{MV}$, where the signal eigenvalues blur the picture.

In physical terms: **conventional stacking measures how much energy the steering vector captures. MUSIC measures how much energy it leaks into the noise subspace.** The noise subspace is a well-defined, low-dimensional complement to the signal, so the leakage test is a much more sensitive discriminator.

### 7.4 Equivalent matrix form

Define the **noise projection matrix**:

$$
\mathbf{R}^{-1}_\text{MUSIC} = \sum_{i=N_s+1}^{M} \mathbf{u}_i\, \mathbf{u}_i^\dagger = \mathbf{V}_n\, \mathbf{V}_n^\dagger,
$$

where $\mathbf{V}_n = [\mathbf{u}_{N_s+1}, \ldots, \mathbf{u}_M]$ is the matrix whose columns are the noise eigenvectors. Then:

$$
P_\text{MUSIC}(k) = \frac{1}{\mathbf{e}^\dagger(k)\, \mathbf{R}^{-1}_\text{MUSIC}\, \mathbf{e}(k)}.
$$

This is the form used in computation: $\mathbf{R}^{-1}_\text{MUSIC}$ is a low-rank matrix (rank $M - N_s$) that projects any vector onto the noise subspace.

---

## 8. Practical implementation via SVD

### 8.1 Singular value decomposition

In practice, $\mathbf{R}$ is estimated from a data matrix $\mathbf{Y}$ of size $M \times N_f$, where $N_f$ is the number of frequency samples in a narrow band. The singular value decomposition (SVD) of $\mathbf{Y}$ is:

$$
\mathbf{Y} = \mathbf{U}\, \mathbf{S}\, \mathbf{V}^\dagger,
$$

where $\mathbf{U}$ is $M \times M$ unitary, $\mathbf{S}$ is $M \times N_f$ diagonal with singular values, and $\mathbf{V}$ is $N_f \times N_f$ unitary. The eigenvalues of $\mathbf{R} = \mathbf{Y}\mathbf{Y}^\dagger$ are the squares of the singular values of $\mathbf{Y}$, and the eigenvectors of $\mathbf{R}$ are the columns of $\mathbf{U}$.

### 8.2 Extracting the noise subspace

Datta (2018) fixes $N_s$ as an input parameter rather than estimating it from the eigenvalue spectrum. The algorithm:

1. Choose $N_s$ (the number of modes expected at the analysis frequency).
2. Compute the SVD of $\mathbf{Y}$: $\mathbf{Y} = \mathbf{U}\mathbf{S}\mathbf{V}^\dagger$.
3. Form the noise subspace matrix $\mathbf{V}_n$ by taking columns $N_s + 1$ through $M$ of $\mathbf{U}$.
4. Compute $\mathbf{R}^{-1}_\text{MUSIC} = \mathbf{V}_n \mathbf{V}_n^\dagger$.
5. For each trial wavenumber $k$, compute $P_\text{MUSIC}(k) = 1 / (\mathbf{e}^\dagger \mathbf{R}^{-1}_\text{MUSIC}\, \mathbf{e})$.

The result is an f–k spectrum. Convert wavenumber to phase velocity ($c = \omega/k$) by linear interpolation to obtain the f–c dispersion image.

---

## 9. Relation to slant-stack

The frequency-domain slant-stack (§6.2 of the lecture notes) is the simplest case of conventional beamforming. Its stacked amplitude is:

$$
S(\omega, k) = \sum_{i=1}^{M} U(x_i, \omega)\, e^{-ikx_i} = \mathbf{e}^\dagger(k)\, \mathbf{Y}.
$$

The output power is $|S|^2 = \mathbf{e}^\dagger \mathbf{R}\, \mathbf{e}$, which is exactly the conventional beamformer of §3. Slant-stack and conventional beamforming are mathematically equivalent; the difference is only in notation and normalization.

FK-MUSIC replaces $\mathbf{e}^\dagger \mathbf{R}\, \mathbf{e}$ with $\mathbf{e}^\dagger \mathbf{R}^{-1}_\text{MUSIC}\, \mathbf{e}$ — substituting the full correlation matrix with the noise-subspace projector. This single substitution is what transforms a conventional dispersion image into a high-resolution MUSIC spectrum.

---

## 10. Link to the lecture notes

The lecture notes (Term 3 Lecture 03, §6) use the following results from this derivation without reproducing the full algebra:

- The **beamforming idea**: cancel propagation phase, stack, sweep over trial velocities (§1).
- The **correlation matrix** $\mathbf{R}$ and the conventional beamformer output $P = \mathbf{e}^\dagger \mathbf{R}\, \mathbf{e}$ (§2–3).
- The **signal and noise subspaces** from eigenanalysis of $\mathbf{R}$ (§5–6).
- The **MUSIC pseudo-spectrum** as the inverse noise-subspace projection (§7).
- The insight that MUSIC measures **leakage into the noise** rather than energy captured (§7.3).

The full chain — from conventional beamforming through the minimum-variance beamformer to the eigenanalysis that yields the MUSIC formula — is left here for students who want to see where the pseudo-spectrum comes from.

---

## Key equations

- Conventional beamformer output power:
  $$
  P(k) = \mathbf{e}^\dagger(k)\, \mathbf{R}\, \mathbf{e}(k).
  $$

- Minimum variance (Capon) beamformer:
  $$
  P_\text{MV}(k) = \frac{1}{\mathbf{e}^\dagger(k)\, \mathbf{R}^{-1}\, \mathbf{e}(k)}.
  $$

- Eigendecomposition of $\mathbf{R}$:
  $$
  \mathbf{R} = \sum_{i=1}^{M} \lambda_i\, \mathbf{u}_i\, \mathbf{u}_i^\dagger.
  $$

- MV output in the eigenbasis:
  $$
  P_\text{MV}(k) = \frac{1}{\displaystyle\sum_{i=1}^{M} \lambda_i^{-1}\, |\mathbf{e}^\dagger \mathbf{u}_i|^2}.
  $$

- MUSIC pseudo-spectrum:
  $$
  P_\text{MUSIC}(k) = \frac{1}{\displaystyle\sum_{i=N_s+1}^{M} |\mathbf{e}^\dagger(k)\, \mathbf{u}_i|^2}.
  $$

- Noise projection matrix:
  $$
  \mathbf{R}^{-1}_\text{MUSIC} = \sum_{i=N_s+1}^{M} \mathbf{u}_i\, \mathbf{u}_i^\dagger.
  $$
