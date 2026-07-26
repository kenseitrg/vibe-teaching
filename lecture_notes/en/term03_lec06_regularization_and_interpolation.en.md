---
title: Term 3 Lecture 06 — Regularization and Interpolation of Seismic Data
status: draft
term: 03
lecture: 06
---

# Regularization and Interpolation of Seismic Data

## Learning objectives

By the end of this lecture you should be able to:

- Explain why migration and SRME require regularly sampled input, and describe how irregular sampling produces migration artifacts (impulse-response tails).
- Distinguish **regularization** from **interpolation**, and state why the meaning of "regular" depends on the migration domain (offset, OVT, COV).
- Explain the dimensionality ladder — 3D, 4D, 5D — and what each level preserves or loses (structure, offset, azimuth, AVO).
- State the unifying principle behind every interpolation method: the data are assumed sparse or simple in some transform domain.
- Describe the legacy T–X, F–X, and F–K interpolation methods, the assumptions each makes, and why those assumptions break down.
- Explain spectral leakage on an irregular grid and why a plain DFT fails there.
- Describe the anti-leakage Fourier transform (ALFT) as matching pursuit with a Fourier dictionary, including its weighting, windowing, and anti-alias extensions.
- Describe how Radon-domain reconstruction and modern extensions (priors from a second dataset, OMP, 5D MPFI) extend the basic ALFT idea.
- Choose an appropriate regularization method for a given data problem and validate the result by predicting the input.

## Prerequisites

- Term 1 Lecture 05: the discrete Fourier transform, sampling, aliasing, and the convolution theorem.
- Term 1 Lecture 06: prediction-error filters and the predictability of coherent events.
- Term 2: the Radon (τ–p) transform and its use for separation.
- Term 3 Lecture 01: 3D acquisition geometry, bins, fold, and the unit cell.
- Term 3 Lecture 04: noise attenuation and the idea of sparsity in a transform domain (FK, Radon, curvelet).

## 0. Why this lecture matters

Almost every advanced processing step assumes the data live on a **regular grid**. Migration sums energy along operator surfaces; 3D SRME predicts multiples by convolving the data with itself across offsets and azimuths; AVO/AVAz analysis measures amplitude trends across a complete, evenly spaced offset range. None of these tolerates missing or irregularly placed traces gracefully.

But real surveys are never acquired on a perfect grid. Obstacles, permit boundaries, roads, rivers, and economics leave gaps and irregular spacing. Wide-azimuth and long-offset surveys — exactly the ones we want for complex imaging — are typically the *most* sparsely and irregularly sampled. So before we can image or demultiple, we must **regularize**: map the recorded traces from their irregular acquisition grid onto the regular grid that the downstream algorithm expects.

This lecture traces the evolution of that idea. We start from *why* it matters (migration artifacts), clarify the terminology, then move through the legacy prediction-filter methods (T–X, F–X, F–K) and their limits, to the modern workhorse — sparse Fourier reconstruction via the **anti-leakage Fourier transform** — and its Radon-domain and machine-learning extensions. Throughout, one principle ties everything together: **every method succeeds by assuming the data are sparse or simple in some domain, and fails where that assumption breaks.**

## 1. Why regularization is necessary

### 1.1 Migration artifacts from irregular input

Kirchhoff migration builds an image by summing the recorded wavefield along traveltime surfaces. Conceptually, the image at a point $\mathbf{m}$ is a weighted sum over input traces:

$$ I(\mathbf{m}) = \sum_i w_i \; x\!\left(t_i(\mathbf{m}),\, \mathbf{x}_i\right), $$

where $t_i(\mathbf{m})$ is the traveltime from trace location $\mathbf{x}_i$ to image point $\mathbf{m}$, and $w_i$ is an aperture weight. This sum approximates an integral over a continuous aperture. When the input traces are dense and regular, the approximation is good and the migration **impulse response** — the image of a single point diffractor — is a clean, focused arc.

When traces are missing or irregularly spaced, the sum is incomplete. The impulse response develops **tails and smearing**: energy that should focus at one point leaks along the operator surface. These are the migration artifacts that degrade the image — false dips, arcs, and "smiles" that have no geological meaning.

![](figures/term03_lec06/term03_lec06_migration_artifacts.png){width=90%}

**Figure 1.** *Migration impulse response with and without regularization. A single point diffractor is migrated from (left) a sparsely/irregularly sampled input and (right) the same data after regularization. The irregular input produces a smeared impulse response with prominent tails; regularization restores a focused response. The artifacts are not noise — they are the signature of an incomplete aperture summation.*

The same logic applies to wave-equation migration and to any multi-channel process. 3D SRME, for instance, requires data on a regular offset–azimuth grid; gaps produce incomplete multiple predictions that leave residual multiples after subtraction.

### 1.2 What "regular" means depends on the migration domain

There is no single "regular grid." The target grid is defined by the **migration domain**:

- **Offset migration** — data should be regular in midpoint and offset. Each offset class is imaged separately.
- **OVT / COV migration** (Term 3 Lecture 01) — data should be regular in **offset-vector tiles**: midpoint $\times$ offset-x $\times$ offset-y. This preserves azimuth, which is essential for azimuthally anisotropic (TTI/HTI) imaging and for amplitude-versus-azimuth analysis.

The regularization algorithm must therefore be told which domain to regularize into, and its dimensionality (Section 4.1) must match that domain.

![](figures/term03_lec06/term03_lec06_regular_vs_irregular.png){width=80%}

**Figure 2.** *Irregular acquisition versus a regular target grid. Recorded midpoint–offset locations (dots, left) are scattered and gappy. Regularization (right) reconstructs the wavefield onto a fixed, evenly spaced grid of bins and offsets defined by the chosen migration domain. The output grid is fixed by the algorithm's requirements — not by where data happen to be missing.*

## 2. Terminology and the unifying principle

### 2.1 Regularization vs interpolation

The two words are often used interchangeably, but their emphasis differs:

- **Regularization** is the primary goal: produce a *regularly sampled* dataset so that downstream algorithms behave correctly. The output locations are fixed by the target grid.
- **Interpolation** is filling in *missing* traces at specific locations. It is sometimes a beneficial side effect of regularization, and occasionally the explicit goal — for example, densifying data so that a noise-attenuation step can handle aliased coherent noise.

Most algorithms marketed as "interpolation" are, in practice, regularization engines. We will use both terms but keep the distinction in mind.

### 2.2 The unifying principle: sparsity in a domain

No method can invent information that is not there. Every interpolation method works by assuming the data have a **compact representation in some transform domain**, then reconstructing from that compact model. The methods differ only in which domain they choose:

| Method family | Domain | Assumption about the data |
|---------------|--------|---------------------------|
| T–X, F–X | space / frequency–space | events are **locally linear** and stationary |
| F–K | frequency–wavenumber | events are **globally linear** |
| ALFT / MPFI | spatial Fourier | the spatial spectrum is **sparse** |
| Radon | intercept–curvature (τ–p) | events are **sparse in moveout/curvature** |

This single idea — *find the domain in which the data are simplest, model them there, transform back* — is the spine of the whole lecture. It also tells us why methods fail: when the data violate the assumption (curved events, complex structure, gaps larger than the model can span), the reconstruction degrades.

![](figures/term03_lec06/term03_lec06_sparsity_domains.png){width=90%}

**Figure 3.** *The same CMP gather represented in four domains. In the time–offset domain the data look complex, but each transform concentrates the energy differently: a few dominant dips in F–K, focused peaks in the Radon domain, a sparse set of components in the spatial Fourier domain. Interpolation = keep the few large coefficients, discard the rest, transform back onto the regular grid.*

## 3. Legacy methods and their shortcomings

### 3.1 T–X interpolation

The time–space approach predicts a missing trace from its neighbours, exploiting the fact that a **locally linear event** continues smoothly across traces. The simplest form finds the dominant local dip $p$ (slowness, in s/m), shifts neighbouring traces by the dip moveout $p\,\Delta x$, and forms a weighted sum:

$$ \hat{x}(t, x_0) = \sum_i a_i \; x\!\left(t - p\,(x_i - x_0),\, x_i\right). $$

A more principled version uses **prediction-error filtering** in the T–X domain (Claerbout & Nichols 1991): estimate a 2D prediction filter from the data, then use it to predict traces at the finer spacing.

**Assumption and limit.** The method assumes events are locally linear and stationary within the estimation window. It handles gently dipping, continuous events well, but smears curved events and fails where the dip field is complex or the gaps are large.

### 3.2 F–X interpolation

Spitz (1991) moved the prediction idea into the frequency–space domain, where it becomes especially clean. At a single temporal frequency $f$, a set of linear events is a sum of complex exponentials in space:

$$ X(f, x) = \sum_m A_m \, e^{\,i 2\pi k_m x}. $$

A sum of complex exponentials is **predictable**: the value at the next spatial sample is a linear combination of the previous ones,

$$ X(f, x_{n+1}) = \sum_j P_j(f)\, X(f, x_{n+1-j}), $$

where $P_j(f)$ is a spatial **prediction filter** estimated from the data at frequency $f$.

The elegant part is how Spitz handles **aliasing**. Interpolating (doubling the spatial sampling) at frequency $f$ requires a prediction filter that can be derived from the data at frequency $f/2$ — where the data are *not* aliased. So the filter is estimated at the non-aliased low frequencies and transferred to the aliased high frequencies. This "low-frequency prior for high-frequency aliasing" trick recurs throughout the lecture.

**Assumption and limit.** F–X interpolation assumes a finite number of linear, non-dispersive, stationary events within the analysis window. It is fast and robust for moderately aliased linear events, but the windowing is essential (the events must be locally stationary), and it struggles with curved events, strong noise, and very sparse or gappy sampling. Naghizadeh & Sacchi (2009) made the filters **adaptive** (recursive least squares with a forgetting factor) so the local filter is updated from window to window rather than re-estimated from scratch.

### 3.3 F–K interpolation

Gülünay (2003) interpolates directly in the **Fourier transform domain** (f–k, or f–kx–ky for 3D). The interpolation operator is designed from the non-aliased low frequencies and, exploiting the cyclic properties of the FFT, is the same operator that fills periodically zeroed traces. This again uses the low→high frequency prior idea, but with an elegant wavenumber-domain representation that is closely related to F–X prediction filtering.

**Assumption and limit.** F–K methods assume globally linear events (a single f–k spectrum describes the whole window). They handle aliasing better than a naive f–k filter, but the global linearity assumption is restrictive, and like F–X they degrade for complex, non-linear wavefields.

### 3.4 Bridge: why we need sparse reconstruction

All three legacy methods are **filter-based** and rest on linearity/stationarity. They break down precisely where modern surveys are hardest:

- **Curved or conflicting events** violate the linear-event model.
- **Large, irregular gaps** leave too little local information for a prediction filter.
- **Strong aliasing** beyond what the low-frequency prior can resolve.
- **Higher dimensions** — extending a 2D prediction filter to 4D/5D is awkward and expensive.

These limitations motivated a different philosophy: rather than predicting trace-to-trace, **estimate a sparse transform model of the whole wavefield and invert it onto the target grid**. This is the sparse-reconstruction approach, and its Fourier version is the subject of Section 4.

## 4. Modern regularization: multi-dimensional sparse reconstruction

### 4.1 The dimensionality of the transform

The defining feature of modern regularization is that it operates on **multi-dimensional** data at once. The number of spatial axes used determines what the reconstruction can preserve and what it can fill:

| Dim. | Axes used | Preserves | Cannot / mixes |
|------|-----------|-----------|----------------|
| **3D** | inline, crossline, time | structural dip | cannot fill missing offsets |
| **4D** | + offset | fills offset gaps | mixes all azimuths at a given offset |
| **5D** | + azimuth (or offset-x, offset-y) | azimuth **and** AVO/AVAz | best gap filling; most expensive |

A 3D regularization works within a single offset class: it can repair the spatial (midpoint) sampling but says nothing about missing offsets. Adding the offset axis (4D) fills offset gaps, but because azimuth is not a separate axis, all azimuths at a given offset are averaged together — smearing the azimuthal signal we need for TTI imaging and AVAz analysis. Only a **5D** transform, which uses every spatial axis (inline, crossline, offset, azimuth, time), has enough information to preserve azimuth and AVO while filling gaps. 5D is the state of the art (Trad 2009).

> **Naming pitfall.** "4D" and "5D" here count the **axes of the data cube** (spatial dimensions plus time). They have nothing to do with *4D time-lapse* seismic. This confusion is common — flag it explicitly.

The dimensionality is chosen to match the migration domain of Section 1.2: an OVT migration calls for 5D regularization so that offset and azimuth are both made regular.

![](figures/term03_lec06/term03_lec06_dimensionality_ladder.png){width=90%}

**Figure 4.** *The dimensionality ladder. The same irregular wide-azimuth dataset reconstructed at 3D, 4D, and 5D. 3D repairs structure but leaves offset gaps; 4D fills offsets but smears azimuth; 5D preserves both offset and azimuth and fills the most gaps. The improvement comes from giving the inversion more of the data's spatial structure to constrain the solution.*

### 4.2 Spatial spectral leakage

Fourier-based regularization estimates a spatial Fourier spectrum from the input and inverts it onto the target grid. The obstacle is that a plain DFT does not work on an **irregular** grid.

Sampling a continuous wavefield $f(x)$ at discrete locations is multiplication by a sampling function $L(x)$ — a train of impulses at the sample positions:

$$ f_s(x) = f(x)\,L(x). $$

Multiplication in space becomes **convolution in the Fourier domain**:

$$ \hat{f}_s(k) = \hat{f}(k) * \hat{L}(k). $$

For a regular grid, $\hat{L}(k)$ is itself a clean comb of impulses, and the convolution merely replicates the spectrum (ordinary aliasing). For an **irregular** grid, $\hat{L}(k)$ has a strong peak at $k=0$ but also non-zero sidelobes at all wavenumbers. Convolving with those sidelobes spreads each true component's energy across many others. This crosstalk is **spectral leakage**.

Equivalently: the DFT basis functions $e^{i2\pi k\cdot x}$ are orthogonal only on a regular grid. On an irregular grid they are not orthogonal, so projecting the data onto one basis function contaminates it with all the others. A direct DFT gives biased coefficients, and reconstructing from them produces artifacts.

A plain forward DFT is therefore inadequate. Least-squares Fourier estimation (Duijndam et al. 1999; Zwartjes & Sacchi 2007) solves for the coefficients that best fit the data and removes leakage when the data are band-limited and well sampled — but becomes poorly determined for sparse, gappy data. The anti-leakage Fourier transform solves this with an iterative scheme that stays stable exactly where least squares fails.

![](figures/term03_lec06/term03_lec06_spectral_leakage.png){width=85%}

**Figure 5.** *Spectral leakage from irregular sampling. Top: a clean spatial spectrum (a few sharp peaks) sampled on a regular grid reconstructs faithfully. Bottom: the same wavefield sampled irregularly — the sampling function's sidelobes convolve with the spectrum, smearing each peak into many false ones. A direct DFT of the irregular data returns this smeared spectrum, not the true one.*

### 4.3 The non-uniform DFT as computational enabler

The ALFT works in the time–frequency domain: a temporal FFT first (time is regularly sampled, so this is cheap), leaving only the spatial axes irregular. At each temporal frequency it needs a **non-uniform DFT** — Fourier coefficients from irregular spatial locations:

$$ \hat{f}(k) = \frac{1}{\sum_p w(x_p)} \sum_p w(x_p)\, f(x_p)\, e^{-i 2\pi k\cdot x_p}, $$

with an integral weight $w(x)$ discussed below. A direct evaluation costs $O(N\,N_p)$ per wavenumber and cannot use the FFT. In practice this is accelerated by **gridding**: spread the irregular samples onto a nearby regular oversampled grid with a smooth kernel, apply a regular FFT, then correct for the kernel (deconvolution). This brings the cost close to an FFT and is what makes high-dimensional (4D/5D) regularization feasible at all.

### 4.4 Matching-pursuit reconstruction: the ALFT algorithm

The anti-leakage Fourier transform (Xu & Pham 2004; Xu et al. 2010) estimates the spatial spectrum by **matching pursuit** with a Fourier dictionary — peeling off the strongest component at a time so that the leakage from already-explained energy is removed at every step.

At each temporal frequency:

1. **Initialize** all Fourier components to zero; set the residual equal to the input data.
2. **Forward non-uniform DFT** — compute every spatial Fourier coefficient of the residual (equation above).
3. **Pick the strongest** coefficient $\hat{f}_\text{max}(k)$ and add it to the accumulated spectrum.
4. **Subtract** that single component from the residual:

   $$ f_u(x) = f(x) - \hat{f}_\text{max}(k)\, e^{\,i 2\pi k\cdot x}. $$
5. **Iterate** steps 2–4 until the residual is small enough.

Because the basis is non-orthogonal on the irregular grid, the same component may be re-selected in later iterations, and a given $k$ accumulates its contribution gradually. The final spectrum is then inverted onto any desired output grid with a standard inverse DFT (or FFT, for a regular output grid).

**Cost and windowing.** A full high-dimensional ALFT costs roughly $O(N^2 N_p)$ per iteration. Running it in **local spatial windows** cuts the cost dramatically, but a small window undersamples the wavenumber domain and introduces Gibbs artifacts. The fix (Xu et al. 2010) is a **wavenumber-domain oversampling inversion**: a small least-squares fit per iteration for the best coefficient, which lets ALFT run cleanly in small windows.

**The weighting function.** The integral weight $w(x)$ controls how each irregular sample contributes. Choices depend on dimension: sample spacing in 1D; Voronoi-cell areas in 2D (Canning & Gardner 1998); a discontinuous "hit-count" (samples per bin) in higher dimensions. Xu et al. (2010) instead build a smooth **sampling density** by convolving the sample locations with a Gaussian and set $w(x)=1/\rho(x)$. ALFT is fairly insensitive to the exact weight, but a good one speeds convergence and improves the result.

![](figures/term03_lec06/term03_lec06_alft_iteration.png){width=90%}

**Figure 6.** *One ALFT iteration, visualized. Left: the residual's spatial spectrum (non-uniform DFT). Centre: the single strongest component selected. Right: the residual after that component is subtracted. Repeating this peeling concentrates the model on the few dominant components; the accumulated selected components form the final sparse spectrum used for reconstruction.*

### 4.5 Anti-alias ALFT: interpolation beyond aliasing

Standard ALFT handles steep dips well on *irregular* grids, but has a surprising weakness: for data that are *nearly regular*, the **aliased copies** of an event have the **same amplitude** as the true component (Schonewille et al. 2009). Matching pursuit can then lock onto an alias and reconstruct the event at the wrong dip.

**Anti-alias ALFT (AA-ALFT)** fixes this with the now-familiar low→high prior idea: use the **un-aliased low frequencies** to derive spectral weights that guide component selection at the **high frequencies**, biasing the algorithm toward the true (non-aliased) component. This is the same philosophy as Spitz's F–X interpolation and as the Radon methods of Section 5 — a recurring theme: *trust the low frequencies, let them constrain the aliased high frequencies.*

![](figures/term03_lec06/term03_lec06_antialias_weighting.png){width=80%}

**Figure 7.** *Anti-alias weighting. In near-regular sampling, an event's true wavenumber and its aliases have equal amplitude (left), so selection is ambiguous. The low-frequency spectrum is un-aliased and identifies the true component; its weights (centre) are extrapolated to high frequency to suppress the aliases (right), steering the reconstruction to the correct dip.*

### 4.6 Parameters and QC

The main practical parameters of an ALFT regularization are:

- **Window size** — trades computational cost against wavenumber resolution; too small a window undersamples wavenumber (hence the oversampling fix).
- **Number of coefficients / iterations** — controls how sparse the model is and when to stop.
- **Frequency range** — and the low→high weighting bandwidth for anti-aliasing.

The essential QC is **prediction of the input**: sample the reconstructed model back at the *irregular input locations* and compare with what was actually recorded. A good regularization reproduces the measured traces; a large mismatch signals over- or under-fitting. This closes the loop — the model is only trustworthy if it explains the data we already have.

## 5. Modern extensions

### 5.1 Radon-domain reconstruction

The ALFT uses a Fourier dictionary. The same sparse-reconstruction idea works with a **Radon dictionary** — and for CMP gathers it is often a better match, because primary reflections follow hyperbolic moveout and so collapse to **focused peaks** in the τ–p domain, while gaps and noise spread out (Term 2). Filling gaps then means estimating a sparse Radon model and transforming back.

The quality depends on how well events match the basis. A **true hyperbolic** Radon transform approximates reflections better than the parabolic one at large offsets (common in marine data), but its kernel is time-variant, so fast solvers cannot be used. Trad, Ulrych & Sacchi (2002) make it practical:

- solve a **sparse inversion** (weighted conjugate gradient / LSQR) with a sparseness constraint;
- define the model on an **irregularly sampled velocity space** — a central trace carrying a semblance-derived velocity trend, plus neighbouring perturbation traces with variable spacing — to keep the number of unknowns small;
- exploit the fact that an **irregularly sampled Radon space relaxes the aliasing condition** (Trad & Ulrych 1999).

The hyperbolic transform gives accurate interpolation in CMP gathers; an elliptical variant cleans up slant-stack sections.

A modern twist (Feng et al. 2022) uses a **convolutional neural network** to extract sparse prior information that guides a de-aliased high-resolution Radon inversion — the low→high frequency prior idea again, but with the prior *learned from data* rather than taken from the low frequencies of the same gather.

A practical advantage of Radon-based methods is that their operators can be defined **locally without the explicit windowing** that Fourier methods require (Naghizadeh & Sacchi 2009). Their limitation is the moveout assumption: they are natural for primaries in CMP gathers but less well suited to full 3D/5D azimuthal regularization, where Fourier (ALFT/MPFI) methods dominate.

![](figures/term03_lec06/term03_lec06_radon_interpolation.png){width=90%}

**Figure 8.** *Radon interpolation of a gappy CMP gather. Left: input gather with missing offsets (zeroed traces). Centre: the sparse high-resolution τ–p model — primaries focus to a few peaks; the gaps contribute spread-out, low-amplitude energy that the sparsity constraint suppresses. Right: the reconstructed gather with the missing offsets filled by inverse Radon transform.*

### 5.2 Priors from a separate dataset

AA-ALFT and MPFI normally derive their anti-alias prior from the data's own low frequencies. Schonewille et al. (2013) show a significant uplift when the prior comes from a **separate, more densely sampled dataset**. Practical cases include **dense-over/sparse-under** acquisitions (a dense shallow survey over a sparse deep one) and **time-lapse** data, where the baseline survey provides the prior for interpolating the monitor survey.

### 5.3 Orthogonal matching pursuit

Basic matching pursuit can be slow and may re-select atoms. **Orthogonal matching pursuit (OMP)** improves on it: after each atom is selected, re-solve a least-squares fit over *all* atoms chosen so far, keeping the residual orthogonal to the selected subspace. Tropp & Gilbert (2007) showed that OMP reliably recovers a signal with $m$ non-zero coefficients from $O(m \ln d)$ random measurements — comparable to ℓ1 (basis pursuit) guarantees, but faster and simpler to implement. OMP underpins the "orthogonal matching pursuit" extensions used in modern regularization.

### 5.4 5D MPFI for SRME

Tang et al. (2017) apply full **5D matching-pursuit Fourier interpolation** to multivessel "dual-coil" wide-azimuth, long-offset acquisition, specifically to feed SRME. Dual-coil data give richer azimuth and longer offsets for subsalt imaging, but large-offset coverage is less uniform than the dominant azimuths — exactly the irregularity that degrades SRME. 5D MPFI regularizes across all spatial axes, producing the regular offset–azimuth grid that SRME requires. This closes the loop back to Section 1: we regularize so that SRME and migration can work.

## 6. Method selection and a real-data example

### 6.1 Choosing a method

| Situation | Recommended method | Why |
|-----------|-------------------|-----|
| Gentle, continuous events; mild aliasing; 2D | F–X (Spitz) or T–X | Fast, robust for linear events |
| Aliased linear events, moderate gaps | F–K (Gülünay) or F–X | Low→high prior handles aliasing |
| Sparse, irregular 3D; steep dips | 3D ALFT | Stable where least squares fails |
| Wide-azimuth; preserve offset + azimuth; AVO/AVAz | 5D ALFT / MPFI | Uses all spatial axes |
| Beyond-aliasing, near-regular sampling | AA-ALFT | Low-freq weights suppress aliases |
| Denser companion dataset available | MPFI with external prior | Stronger anti-alias constraint |
| Gappy CMP gathers; primary interpolation | High-res Radon | Sparse in τ–p; local operators |
| Feeding SRME on irregular long-offset data | 5D MPFI | Regular offset–azimuth grid |

### 6.2 A real-data example

The accompanying slides show an OVT migration of a wide-azimuth dataset processed three ways: with no regularization, with OVT-domain regularization, and with offset-class regularization. The un-regularized migration shows the impulse-response tails of Section 1.1; the properly regularized (OVT) migration suppresses them and preserves azimuth. A second example runs ALFT+AA on the data and shows the interpolation windows and the effect of the coefficient count — using too few coefficients (1) under-fits and leaves gaps, while a moderate count (4–64) reconstructs the events cleanly without inventing artifacts. The QC in every case is prediction of the input: the reconstructed model, sampled back at the recorded locations, must match the measured traces.

![](figures/term03_lec06/term03_lec06_method_comparison.png){width=90%}

**Figure 9.** *Effect of the number of Fourier coefficients in ALFT. With 1 coefficient the model under-fits and leaves gaps; with 4 and 64 coefficients the dominant events are reconstructed progressively more completely. The right choice balances fidelity to the input (QC) against sparsity — enough coefficients to explain the data, no more.*

## 7. Summary

### Key takeaways

1. **Regularization maps irregular, sparse data onto a regular grid** so that migration, SRME, and amplitude analysis work correctly. Irregular input produces migration artifacts — impulse-response tails from an incomplete aperture sum.
2. **"Regular" depends on the migration domain** — offset for offset migration, offset-vector tiles for OVT/COV migration.
3. **Dimensionality is the defining modern feature**: 3D preserves structure but cannot fill offsets; 4D fills offsets but mixes azimuths; 5D preserves offset and azimuth (AVO/AVAz) and fills the most gaps. (Not time-lapse!)
4. **Every method assumes sparsity/simplicity in some domain** — T–X/F–X (local linearity), F–K (global linearity), ALFT (sparse Fourier), Radon (sparse curvature). Methods fail where the assumption breaks.
5. **Spectral leakage** — energy crosstalk from irregular sampling — makes a plain DFT useless on an irregular grid; a non-uniform DFT plus iterative inversion is required.
6. **ALFT is matching pursuit with a Fourier dictionary**: estimate the spectrum, pick the strongest component, subtract, repeat. Weighting, windowing with wavenumber oversampling, and low→high anti-alias weighting make it robust and accurate.
7. **Extensions** — Radon-domain reconstruction, priors from a second dataset, OMP, and 5D MPFI — broaden the reach of the basic sparse-reconstruction idea.
8. **Always QC by predicting the input**: the reconstructed model must reproduce the measured traces at the irregular input locations.

### The big picture

| Method | Domain | Dimensionality | Handles aliasing | Key limitation |
|--------|--------|---------------|------------------|----------------|
| T–X | space | 2D | weak | locally linear events only |
| F–X (Spitz) | f–x | 2D | yes (low→high prior) | linear, stationary; needs windowing |
| F–K (Gülünay) | f–k | 2D/3D | yes | globally linear |
| ALFT / AA-ALFT | spatial Fourier | 3D–5D | yes (AA weights) | cost grows with dimension |
| MPFI (+priors) | spatial Fourier | up to 5D | yes, beyond aliasing | needs good prior |
| High-res Radon | τ–p | 2D (CMP) | partial | moveout assumption; primaries |

## Comprehension questions

1. Why does irregular input cause migration artifacts? Explain in terms of the aperture summation $I(\mathbf{m})=\sum_i w_i x(t_i,\mathbf{x}_i)$.
2. What is the difference between regularization and interpolation? Give a case where interpolation is the explicit goal rather than a side effect.
3. Why can a 3D regularization not fill missing offsets, and why does a 4D regularization smear azimuth? What does 5D add?
4. Explain spectral leakage using the relation $\hat f_s(k)=\hat f(k)*\hat L(k)$. Why is the leakage worse for irregular than for regular sampling?
5. Why is the DFT basis non-orthogonal on an irregular grid, and what consequence does this have for a direct forward DFT?
6. Describe the five steps of one ALFT iteration. Why might the same Fourier component be selected more than once?
7. Why does windowing the ALFT reduce cost but introduce Gibbs artifacts, and how does wavenumber-domain oversampling fix this?
8. In AA-ALFT, why do aliased components cause trouble for near-regular data, and how do low-frequency weights solve the problem? How is this the same idea as Spitz's F–X interpolation?
9. A CMP gather has missing near offsets. Why is a sparse high-resolution Radon transform a good choice here, and why is the hyperbolic transform preferred over the parabolic one at large offsets?
10. You regularize a dataset and want to check the result. What QC do you perform, and what does a large mismatch tell you?
11. A colleague says "we need 4D regularization for this time-lapse survey." What ambiguity should you clarify?
12. Compare F–X interpolation and ALFT for a sparse, gappy wide-azimuth dataset with steep dips and strong aliasing. Which would you choose and why?

## Suggested reading and sources

- Xu, S., Zhang, Y., & Lambaré, G. (2010). Antileakage Fourier transform for seismic data regularization in higher dimensions. *Geophysics*, 75(6), WB113–WB120. — The core ALFT reference: leakage, weighting, windowing, wavenumber oversampling. `wiki/sources/xu2010_antileakage_fourier_transform.md`.
- Schonewille, M., Klaedtke, A., & Vigner, A. (2009). Anti-alias anti-leakage Fourier transform. *SEG Expanded Abstracts*, 3249. — AA-ALFT and the low→high weighting idea. `wiki/sources/schonewille2009_aa_alft.md`.
- Schonewille, M., Yan, Z., Bayly, M., & Bisley, R. (2013). Matching pursuit Fourier interpolation using priors derived from a second data set. *SEG Expanded Abstracts*. — MPFI with external priors. `wiki/sources/schonewille2013_mpfi_priors.md`.
- Trad, D. (2009). Five-dimensional interpolation: Recovering from acquisition constraints. *Geophysics*, 74(6), V123–V132. — The 5D dimensionality rationale. `wiki/sources/trad2009_5d_interpolation.md`.
- Trad, D. O., Ulrych, T. J., & Sacchi, M. D. (2002). Accurate interpolation with high-resolution time-variant Radon transforms. *Geophysics*, 67(2), R61–R65. — High-resolution Radon interpolation. `wiki/sources/trad2002_radon_interpolation.md`.
- Feng, L., Xue, Y., Chen, C., Guo, M., & Shen, H. (2022). De-aliased high-resolution Radon transform based on the sparse prior information from the convolutional neural network. *J. Geophys. Eng.*, 19(4), 663–680. — CNN-prior Radon interpolation. `wiki/sources/feng2022_cnn_radon.md`.
- Zwartjes, P. M., & Sacchi, M. D. (2007). Fourier reconstruction of nonuniformly sampled, aliased seismic data. *Geophysics*, 72(1), V21–V32. — Least-squares Fourier reconstruction; survey of filter-based methods. `wiki/sources/zwartjes2006_fourier_reconstruction.md`.
- Tropp, J. A., & Gilbert, A. C. (2007). Signal recovery from random measurements via orthogonal matching pursuit. *IEEE Trans. Inf. Theory*, 53(12), 4655–4666. — OMP theory. `wiki/sources/tropp2007_omp.md`.
- Spitz, S. (1991). Seismic trace interpolation in the F-X domain. *Geophysics*, 56(6), 785–794. — The classic F–X interpolation method. `wiki/sources/spitz1991_fx_interpolation.md`.
- Naghizadeh, M., & Sacchi, M. D. (2009). f-x adaptive seismic-trace interpolation. *Geophysics*, 74(1), V9–V16. — Adaptive (RLS) F–X interpolation. `wiki/sources/naghizadeh2009_fx_adaptive.md`.
- Gülünay, N. (2003). Seismic trace interpolation in the Fourier transform domain. *Geophysics*, 68(1), 355–369. — F–K domain interpolation. `wiki/sources/gulunay2003_ft_interpolation.md`.
- Abma, R., & Kabir, N. (2005). Comparisons of interpolation methods. *The Leading Edge*. — The assumptions behind each method family. `wiki/sources/abma2005_interpolation_comparison.md`.
- Tang, J., et al. (2017). 5D MPFI and its application in surface-related multiple elimination for large offset coil data. *SEG Expanded Abstracts*. — 5D MPFI for SRME on dual-coil data. `wiki/sources/tang2017_5d_mpfi_srme.md`.
