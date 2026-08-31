# Slide outline — Term 3, Lecture 6: Regularization and Interpolation

---

## Slide 1 — Title
- Regularization and Interpolation of Seismic Data
- Term 3, Lecture 6
- Migration artifacts · Sparsity domains · Legacy filters · ALFT sparse reconstruction

---

## Slide 2 — Learning objectives
- Explain why migration and SRME need regularly sampled input, and how irregular sampling makes migration artifacts.
- Distinguish regularization from interpolation, and state why "regular" depends on the migration domain.
- Explain the dimensionality ladder — 3D, 4D, 5D — and what each preserves or loses.
- State the unifying principle: every method assumes the data are sparse or simple in some transform domain.
- Describe the legacy T–X, F–X, and F–K methods, their assumptions, and why they break down.
- Explain spectral leakage on an irregular grid and why a plain DFT fails there.
- Describe the ALFT as matching pursuit with a Fourier dictionary, plus its weighting, windowing, and anti-alias extensions.
- Choose a regularization method for a given problem and validate it by predicting the input.

---

## Slide 3 — Why this lecture matters
- Almost every advanced step assumes the data live on a regular grid.
- Migration sums energy along operator surfaces; 3D SRME convolves data across offsets and azimuths; AVO/AVAz needs an even offset range.
- Real surveys are never on a perfect grid: obstacles, permits, roads, rivers, economics leave gaps.
- Wide-azimuth, long-offset surveys — the ones we want — are the most irregularly sampled.
- Before imaging or demultiple we must regularize: map irregular traces onto the regular grid.
- One thread ties it together: methods succeed where data are sparse/simple in some domain, and fail where that breaks.

---

# 1. Why regularization is necessary

---

## Slide 4 — Migration artifacts from irregular input
- Kirchhoff migration sums the wavefield along traveltime surfaces.
- Image at point m: I(m) = Σ wᵢ x(tᵢ(m), xᵢ) — an approximation to an aperture integral.
- Dense, regular input → a clean, focused impulse response (the image of a point diffractor).
- Missing or irregular traces → an incomplete sum → tails and smearing along the operator.
- These artifacts are false dips, arcs, and "smiles" with no geological meaning.
- Figure: `term03_lec06_migration_artifacts.png`

---

## Slide 5 — Irregular vs regular aperture
- Same number of traces in every panel; only the placement differs.
- Point diffractor: irregular aperture gives a smeared response with tails; regular aperture focuses the energy.
- Flat horizon: irregular aperture scatters artifacts; regular aperture gives a clean, continuous event.
- The artifacts are not noise — they are the signature of an incomplete aperture sum.
- Regularization (reconstructing onto a regular grid) removes them.
- Figure: `term03_lec06_migration_artifacts.png`

---

## Slide 6 — "Regular" depends on the migration domain
- There is no single regular grid; the target is set by the migration domain.
- Offset migration: data regular in midpoint and offset; each offset class imaged separately.
- OVT / COV migration: data regular in offset-vector tiles (midpoint × offset-x × offset-y).
- OVT preserves azimuth — essential for TTI/HTI imaging and amplitude-versus-azimuth.
- The algorithm must be told which geometry to regularize into, and its dimensionality must match.
- Figure: `term03_lec06_regular_vs_irregular.png`

---

## Slide 7 — Irregular fold vs regular target
- Shown as a fold map (traces per CMP–offset bin) for one inline of an orthogonal land geometry.
- Recorded fold (a) is irregular, banded, and gappy — perpendicular lines sample the plane unevenly.
- Regularized target (b) is a uniform grid, every bin filled to the designed fold.
- Average fold per offset: recorded (c) varies strongly with offset; regularized (d) is flat.
- Figure: `term03_lec06_regular_vs_irregular.png`

---

# 2. Terminology and the unifying principle

---

## Slide 8 — Regularization vs interpolation
- The words are often used interchangeably, but the emphasis differs.
- Regularization is the primary goal: produce a regularly sampled dataset; output locations fixed by the target grid.
- Interpolation is filling in missing traces at specific locations.
- Interpolation is sometimes a beneficial side effect, sometimes the explicit goal.
- Example explicit goal: increase density so a noise-attenuation step can handle aliased coherent noise.
- Figure: none

---

## Slide 9 — The unifying principle: sparsity in a domain
- No method can invent information that is not there.
- Every method assumes the data have a compact representation in some transform domain, then reconstructs from it.
- T–X, F–X: events locally linear and stationary.
- F–K: events globally linear.
- ALFT / MPFI: the spatial spectrum is sparse.
- Radon: events sparse in moveout / curvature.
- Find the domain where data are simplest, model them there, transform back.
- Figure: `term03_lec06_sparsity_domains.png`

---

## Slide 10 — The same data in three domains
- Three linear events of different dip, shown in three domains.
- Time–space (a): events overlap and cross — the data look complex.
- F–K (b): each linear event maps to a single dip (a line through the origin) — few dominant components.
- Linear Radon (c): each event focuses to a single point at its intercept and slowness.
- What looks complex in (a) is sparse in (b) and (c).
- Interpolation = keep the few large coefficients, discard the rest, transform back onto a regular grid.
- Figure: `term03_lec06_sparsity_domains.png`

---

# 3. Legacy methods and their shortcomings

---

## Slide 11 — T–X interpolation
- Predict a missing trace from its neighbours: a locally linear event continues smoothly across traces.
- Find the dominant local dip p (slowness, s/m), shift neighbours by p Δx, form a weighted sum.
- x̂(t, x₀) = Σ aᵢ x(t − p(xᵢ − x₀), xᵢ).
- A principled version uses prediction-error filtering in T–X (Claerbout & Nichols 1991).
- Assumption: events locally linear and stationary within the window.
- Limit: smears curved events; fails for complex dip fields or large gaps.
- Figure: none

---

## Slide 12 — F–X interpolation (Spitz 1991)
- At one temporal frequency, linear events are a sum of complex exponentials in space.
- X(f, x) = Σ Aₘ exp(i 2π kₘ x).
- A sum of exponentials is predictable: X(f, xₙ₊₁) = Σ Pⱼ(f) X(f, xₙ₊₁₋ⱼ).
- Pⱼ(f) is a spatial prediction filter estimated from the data at frequency f.
- Figure: none

---

## Slide 13 — F–X: the anti-alias trick
- Interpolating at frequency f needs a filter derivable from data at f/2 — where data are not aliased.
- Estimate the filter at non-aliased low frequencies, transfer it to the aliased high frequencies.
- A low-frequency prior for high-frequency aliasing — a trick that recurs all lecture.
- Assumption: a finite number of linear, non-dispersive, stationary events in the window.
- Fast and robust for moderately aliased linear events; struggles with curved events, noise, gappy data.
- Naghizadeh & Sacchi (2009) made the filters adaptive (RLS with a forgetting factor).
- Figure: none

---

## Slide 14 — F–K interpolation (Gülünay 2003)
- Interpolate directly in the Fourier transform domain (f–k, or f–kx–ky for 3D).
- The operator is designed from the non-aliased low frequencies.
- Using FFT cyclic properties, it is the same operator that fills periodically zeroed traces.
- Again the low→high frequency prior, with an elegant wavenumber representation.
- Assumption: globally linear events (one f–k spectrum describes the whole window).
- Limit: global linearity is restrictive; degrades for complex, non-linear wavefields.
- Figure: none

---

## Slide 15 — Why we need sparse reconstruction
- All three legacy methods are filter-based and rest on linearity / stationarity.
- They break down exactly where modern surveys are hardest.
- Curved or conflicting events violate the linear-event model.
- Large, irregular gaps leave too little local information for a prediction filter.
- Strong aliasing beyond what the low-frequency prior can resolve.
- Higher dimensions: extending a 2D filter to 4D/5D is awkward and expensive.
- New philosophy: estimate a sparse transform model of the whole wavefield and invert onto the target grid.
- Figure: `term03_lec06_interpolation_methods.png`

---

## Slide 16 — Regular vs irregular decimation
- The three legacy methods applied under two decimations, each keeping half the traces.
- Regular decimation: the mask is a periodic comb → the spectrum is merely replicated → structured, invertible aliasing.
- Irregular decimation: the mask is an aperiodic comb → sidelobes at every wavenumber → spectral leakage.
- Every method degrades on irregular sampling; F–K most of all.
- T–X carries a larger error throughout — the signature of its single-dip assumption on multi-dip data.
- This is fundamental, and motivates the sparse-reconstruction approach.
- Figure: `term03_lec06_interpolation_methods.png`

---

# 4. Modern regularization: sparse reconstruction

---

## Slide 17 — The dimensionality of the transform
- Modern regularization operates on multi-dimensional data at once.
- 3D (inline, crossline, time): preserves structural dip; cannot fill missing offsets.
- 4D (+ offset): fills offset gaps; but mixes all azimuths at a given offset.
- 5D (+ azimuth, or offset-x/offset-y): preserves azimuth and AVO/AVAz; best gap filling; most expensive.
- Dimensionality is chosen to match the migration domain: OVT calls for 5D.
- 5D is the state of the art (Trad 2009).
- Figure: none

---

## Slide 18 — Spatial spectral leakage
- Fourier regularization estimates a spatial spectrum and inverts it onto the target grid.
- Obstacle: a plain DFT does not work on an irregular grid.
- Sampling = multiplying by a sampling function L(x): f_s(x) = f(x) L(x).
- In the Fourier domain this is convolution: f̂_s(k) = f̂(k) * L̂(k).
- Regular grid: L̂(k) is a clean comb → ordinary aliasing (replication).
- Irregular grid: L̂(k) has sidelobes at all wavenumbers → energy crosstalk = spectral leakage.
- Figure: `term03_lec06_spectral_leakage.png`

---

## Slide 19 — Why the DFT fails on an irregular grid
- DFT basis functions exp(i 2π k·x) are orthogonal only on a regular grid.
- On an irregular grid they are not orthogonal → projecting onto one basis contaminates it with all the others.
- A direct forward DFT gives biased coefficients → reconstruction artifacts.
- Least-squares Fourier estimation (Duijndam 1999; Zwartjes & Sacchi 2007) removes leakage when band-limited and well sampled.
- But it becomes poorly determined for sparse, gappy data.
- The ALFT solves this with an iterative scheme that stays stable exactly where least squares fails.
- Figure: `term03_lec06_spectral_leakage.png`

---

## Slide 20 — Spectral leakage visualized
- Left: 1D spectra, regular vs irregular, for two signals (a sine sum and a Ricker wavelet).
- Regular sampling reproduces the true spectrum; irregular sampling smears it via f̂_s = f̂ * L̂.
- Energy leaks into frequencies that contain none.
- Right: the same contrast in 2D.
- Regular traces (a) → clean F–K dips (b); identical traces irregularly sampled (c) → energy scattered into sidelobes (d).
- Figure: `term03_lec06_spectral_leakage.png`

---

## Slide 21 — The non-uniform DFT as enabler
- ALFT works in time–frequency: a temporal FFT first (time is regular, so cheap), leaving spatial axes irregular.
- At each frequency it needs a non-uniform DFT — Fourier coefficients from irregular locations.
- f̂(k) = [1 / Σ w(xₚ)] Σ w(xₚ) f(xₚ) exp(−i 2π k·xₚ), with an integral weight w(x).
- Direct evaluation costs O(N Nₚ) per wavenumber and cannot use the FFT.
- Accelerated by gridding: spread samples onto an oversampled regular grid, FFT, correct for the kernel.
- This brings the cost near an FFT and makes 4D/5D feasible.
- Figure: none

---

## Slide 22 — ALFT: matching pursuit with a Fourier dictionary
- The ALFT (Xu & Pham 2004; Xu et al. 2010) estimates the spectrum by matching pursuit.
- Peel off the strongest component at a time, removing leakage from already-explained energy.
- At each temporal frequency:
- 1. Initialize all components to zero; residual = input data.
- 2. Forward non-uniform DFT of the residual.
- 3. Pick the strongest coefficient; add it to the accumulated spectrum.
- 4. Subtract that component: f_u(x) = f(x) − f̂_max(k) exp(i 2π k·x).
- 5. Iterate 2–4 until the residual is small enough.
- Figure: `term03_lec06_alft_iteration.png`

---

## Slide 23 — ALFT convergence, visualized
- Data: a sum of three complex harmonics, sampled irregularly — the true spectrum is three spikes.
- Top row (iteration 0): the input and its non-uniform DFT, already smeared with leakage sidelobes.
- Rows below advance through iterations 1, 3, 8.
- (a) the spatial residual shrinks toward zero (RMS annotated).
- (b) the residual's DFT loses its strongest peak each iteration (red marker = next pick).
- (c) the accumulated stems land on the true spikes; later iterations mop up small leakage.
- Figure: `term03_lec06_alft_iteration.png`

---

## Slide 24 — ALFT: cost, windowing, weighting
- A full high-dimensional ALFT costs roughly O(N² Nₚ) per iteration.
- Local spatial windows cut the cost, but a small window undersamples wavenumber → Gibbs artifacts.
- Fix (Xu et al. 2010): wavenumber-domain oversampling inversion — a small least-squares fit per iteration.
- The integral weight w(x) controls each sample's contribution.
- Choices: sample spacing (1D), Voronoi-cell areas (2D), hit-count (higher dim), or a smooth Gaussian density with w = 1/ρ.
- ALFT is fairly insensitive to the exact weight, but a good one speeds convergence.
- Figure: none

---

## Slide 25 — Anti-alias ALFT
- Standard ALFT handles steep dips on irregular grids well.
- Surprise weakness: for nearly regular data, aliased copies have the same amplitude as the true component (Schonewille 2009).
- Matching pursuit can then lock onto an alias and reconstruct at the wrong dip.
- AA-ALFT fixes this with the low→high prior: un-aliased low frequencies derive weights that guide high-frequency selection.
- Same philosophy as Spitz's F–X and the Radon methods: trust the low frequencies.
- Figure: `term03_lec06_antialias_weighting.png`

---

## Slide 26 — Anti-alias ALFT, step by step
- (1) Input f–k: true wavenumber and aliases carry equal amplitude — selection is ambiguous.
- (2) Reduced-bandwidth ALFT on low frequencies only: the true component is inside Nyquist, aliases outside → un-aliased prior.
- (3) Extrapolate the spectral weights from the clean low-frequency estimate up to high frequency.
- (4) Apply the weights to the full aliased spectrum: pass the true component, suppress the aliases.
- (5) Result: aliasing removed, event restored to its correct dip.
- Figure: `term03_lec06_antialias_weighting.png`

---

## Slide 27 — Parameters and QC
- Window size: trades cost against wavenumber resolution (hence the oversampling fix).
- Number of coefficients / iterations: how sparse the model is and when to stop.
- Frequency range, and the low→high weighting bandwidth for anti-aliasing.
- Essential QC: prediction of the input.
- Sample the reconstructed model back at the irregular input locations and compare with what was recorded.
- A good regularization reproduces the measured traces; a large mismatch signals over- or under-fitting.
- Figure: none

---

# 5. Modern extensions

---

## Slide 28 — Radon-domain reconstruction
- The same sparse-reconstruction idea works with a Radon dictionary.
- For CMP gathers it is often a better match: primaries follow hyperbolic moveout → focused peaks in τ–p.
- Gaps and noise spread out; filling gaps = estimate a sparse Radon model and transform back.
- True hyperbolic Radon beats parabolic at large offsets, but its kernel is time-variant.
- Trad, Ulrych & Sacchi (2002): sparse inversion (weighted CG / LSQR) on an irregular velocity space.
- Irregularly sampled Radon space relaxes the aliasing condition (Trad & Ulrych 1999).
- Figure: none

---

## Slide 29 — Radon: strengths, limits, a CNN twist
- A modern twist (Feng et al. 2022): a CNN extracts sparse priors to guide a de-aliased high-resolution Radon inversion.
- The low→high prior idea again — but the prior is learned from data, not taken from the same gather's low frequencies.
- Practical advantage: Radon operators can be defined locally without explicit windowing.
- Limitation: the moveout assumption suits primaries in CMP gathers.
- Less well suited to full 3D/5D azimuthal regularization, where Fourier (ALFT/MPFI) methods dominate.
- Figure: none

---

## Slide 30 — Priors from a separate dataset
- AA-ALFT and MPFI usually derive the anti-alias prior from the data's own low frequencies.
- Schonewille et al. (2013): a significant uplift when the prior comes from a separate, denser dataset.
- Dense-over / sparse-under acquisitions: a dense shallow survey over a sparse deep one.
- Time-lapse data: the baseline survey provides the prior for interpolating the monitor survey.
- Figure: none

---

## Slide 31 — Orthogonal matching pursuit
- Basic matching pursuit can be slow and may re-select atoms.
- OMP improves it: after each atom, re-solve a least-squares fit over all atoms chosen so far.
- This keeps the residual orthogonal to the selected subspace.
- Tropp & Gilbert (2007): OMP recovers m non-zero coefficients from O(m ln d) random measurements.
- Comparable to ℓ1 (basis pursuit) guarantees, but faster and simpler to implement.
- OMP underpins the orthogonal matching pursuit extensions in modern regularization.
- Figure: none

---

# 6. Summary

---

## Slide 32 — Key takeaways (1)
- Regularization maps irregular, sparse data onto a regular grid so migration, SRME, and amplitude analysis work.
- Irregular input produces migration artifacts — impulse-response tails from an incomplete aperture sum.
- "Regular" depends on the migration domain: offset for offset migration, OVT tiles for OVT/COV.
- Dimensionality is the defining modern feature: 3D preserves structure; 4D fills offsets but mixes azimuths; 5D preserves offset and azimuth.
- (Not time-lapse!)
- Figure: none

---

## Slide 33 — Key takeaways (2)
- Every method assumes sparsity / simplicity in some domain; methods fail where the assumption breaks.
- Spectral leakage makes a plain DFT useless on an irregular grid; a non-uniform DFT plus iterative inversion is required.
- ALFT is matching pursuit with a Fourier dictionary: estimate, pick the strongest, subtract, repeat.
- Weighting, windowing with wavenumber oversampling, and low→high anti-alias weighting make it robust.
- Extensions — Radon, external priors, OMP, 5D MPFI — broaden the basic sparse-reconstruction idea.
- Always QC by predicting the input.
- Figure: none

---

## Slide 34 — The big picture
- T–X: space domain, 2D, weak on aliasing, locally linear events only.
- F–X (Spitz): f–x, 2D, handles aliasing via low→high prior, linear/stationary, needs windowing.
- F–K (Gülünay): f–k, 2D/3D, handles aliasing, globally linear.
- ALFT / AA-ALFT: spatial Fourier, 3D–5D, AA weights handle aliasing, cost grows with dimension.
- MPFI (+priors): spatial Fourier, up to 5D, handles aliasing beyond Nyquist, needs a good prior.
- Figure: none
