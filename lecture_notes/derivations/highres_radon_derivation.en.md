# Derivation: From Least-Squares to High-Resolution Radon

This document derives the least-squares parabolic Radon transform used for
multiple attenuation, and then the high-resolution (sparse) version. It is the
mathematical companion to Term 2 Lecture 03 (Sections 4.3–4.4); the lecture
keeps the intuition, this document keeps the algebra.

> **Prerequisites.** Complex exponentials, matrix multiplication, and the
> normal equations of least squares (Term 1 Lecture 06 derived the same
> structure for the Wiener filter). No calculus beyond partial derivatives.

---

## 1. Why parabolas, and why frequency by frequency

After an NMO correction with any reasonable velocity, the residual moveout of
an event in a CMP gather is approximately parabolic:

$$
t(x) \;\approx\; t_0 + q\,x^2 ,
$$

with $q$ in s/m$^2$ (practical units: residual moveout at maximum offset). The
claim is empirical: a difference of two hyperbolas with similar velocities is
well approximated by $q x^2$ over typical offset ranges (Hampson, 1986).

Write the gather in the temporal frequency domain, trace by trace:
$d(x, f)$. A parabolic event with amplitude $a$ and intercept $t_0$ has the
spectrum

$$
d(x, f) \;=\; a\, e^{-i 2\pi f (t_0 + q x^2)} .
$$

**Key observation:** at a *fixed frequency* $f$, the offset dependence
$e^{-i 2\pi f q x^2}$ does not involve $t_0$ or time in any way. So for each
frequency we can treat the gather as a vector over offset
($\mathbf{d} \in \mathbb{C}^{N_x}$) and the Radon panel slice as a vector over
curvature ($\mathbf{m} \in \mathbb{C}^{N_q}$), linked by a matrix that depends
only on $f$ and the geometry. The 2-D transform factorizes into $N_f$
independent small matrix problems — this is the entire computational
attraction of the parabolic form. (For the *hyperbolic* Radon transform the
shift $x^2/v^2$ sits inside a square root together with $t_0^2$; no such
factorization exists.)

---

## 2. Adjoint and inverse

Define the forward modeling matrix at frequency $f$ (curvature $q_i$, offset
$x_j$):

$$
L_{ij}(f) \;=\; e^{\,i 2\pi f q_i x_j^2}, \qquad
\hat{\mathbf{d}} \;=\; \mathbf{L}^{\mathsf T} \mathbf{m}.
$$

$\mathbf{L}^{\mathsf T}$ maps a Radon slice to a data slice (model → data);
its conjugate transpose $\mathbf{L}^{\mathsf H}$ maps data to model
(data → model). The **adjoint Radon transform** ("stack along parabolas") is

$$
\mathbf{m}_\text{adj} \;=\; \mathbf{L}^{\mathsf H}\, \mathbf{d}.
$$

### 2.1 Why the adjoint is not an inverse

The adjoint inverts $\mathbf{L}^{\mathsf T}$ exactly only if
$\mathbf{L}^{\mathsf H}\mathbf{L}^{\mathsf T} = \mathbf{I}$. In reality:

- different curvatures $q_i, q_j$ produce nearly parallel phase functions
  over a finite aperture, so columns of $\mathbf{L}^{\mathsf T}$ are far from
  orthogonal — the Gram matrix $\mathbf{G} = \mathbf{L}^{\mathsf H}
  \mathbf{L}^{\mathsf T}$ has strong off-diagonal entries;
- the number of curvatures is typically larger than the number of offsets
  ($N_q > N_x$), so $\mathbf{G}$ is rank-deficient.

Consequences: energy smears along the $q$ axis in the panel, and the round
trip $\mathbf{L}^{\mathsf T} \mathbf{L}^{\mathsf H}$ does not reproduce the
input.

### 2.2 The least-squares inverse

Redefine the forward transform as the *best model that reconstructs the data*:

$$
\mathbf{m}_\text{ls} \;=\; \arg\min_{\mathbf{m}} \left\| \mathbf{d} -
\mathbf{L}^{\mathsf T}\mathbf{m} \right\|_2^2 .
$$

Setting the gradient to zero (identical algebra to the Wiener normal
equations, with $\mathbf{L}^{\mathsf T}$ playing the role of the wavelet
matrix):

$$
\boxed{\;
\left(\mathbf{L}^{\mathsf H}\mathbf{L}^{\mathsf T} + \lambda^2 \mathbf{I}\right)
\mathbf{m}_\text{ls} \;=\; \mathbf{L}^{\mathsf H}\,\mathbf{d}
\;}
$$

The stabilization $\lambda^2 \mathbf{I}$ (or, equivalently, truncating the
small eigenvalues of $\mathbf{G}$) handles the rank deficiency: near-null
directions — pairs of curvatures the aperture cannot distinguish — are damped
instead of being inverted with huge amplification.

**Sanity checks.**

1. If $\mathbf{G}$ were exactly $\mathbf{I}$ (perfectly orthogonal
   parabolas), the LS solution would equal the adjoint — stabilization or
   not. The adjoint is what the LS solution *degenerates to* in the ideal
   case.
2. Reconstruction: $\hat{\mathbf{d}} = \mathbf{L}^{\mathsf T}
   \mathbf{m}_\text{ls}$ fits $\mathbf{d}$ up to the damped modes — in
   practice a few percent residual, versus hundreds of percent for the
   adjoint round trip.
3. The price: $\lambda^2$ damps *all* directions equally, including those
   carrying real (but weak) energy near the null space. The LS panel is
   focused but not sparse — residual smearing tails remain. This is what the
   high-resolution transform removes.

---

## 3. High-resolution Radon: changing the prior

The LS objective says: "among all models that fit, choose the one with the
smallest total energy." Total energy is the wrong prior for a Radon panel — a
panel is a collection of a *few compact events*, not a diffuse fog. The
mathematical expression of "a few big coefficients rather than many small
ones" is a **sparseness norm**. The standard choice (Sacchi & Ulrych, 1995;
Trad et al., 2003) is the Cauchy norm:

$$
J(\mathbf{m}) \;=\; \left\| \mathbf{d} - \mathbf{L}^{\mathsf T}\mathbf{m}
\right\|_2^2 \;+\; \lambda \sum_{i} \ln\!\left(1 + \frac{|m_i|^2}{\sigma^2}\right).
$$

### 3.1 Why Cauchy

Compare penalties per coefficient:

- **L2** ($\lambda |m_i|^2$): doubling a coefficient quadruples its penalty —
  big coefficients are expensive. The optimizer prefers many small ones.
- **L1** ($\lambda |m_i|$): penalty grows linearly — many small coefficients
  cost exactly as much as one big one; indifferent to *how* the energy is
  distributed among coefficients, but still favors zeros over non-zeros.
- **Cauchy** ($\lambda \ln(1 + |m_i|^2/\sigma^2)$): grows like L2 for
  $|m_i| \ll \sigma$ (small coefficients are strongly discouraged) but like
  $\ln|m_i|$ for $|m_i| \gg \sigma$ (big coefficients are almost free). This
  is a *differentiable* approximation to L1 with better conditioning — the
  standard practical choice. $\sigma$ sets the crossover: coefficients
  below $\sigma$ are treated as noise to be suppressed; above it, as events
  to be kept.

### 3.2 The normal equations become iterative

$J$ is non-quadratic in $\mathbf{m}$, so we cannot solve it in one linear
step. Set the gradient to zero:

$$
\mathbf{L}^{\mathsf H}\left(\mathbf{d} - \mathbf{L}^{\mathsf T}\mathbf{m}\right)
- \lambda\, \mathbf{Q}(\mathbf{m})\, \mathbf{m} \;=\; 0,
\qquad
Q_{ii}(\mathbf{m}) \;=\; \frac{1/\sigma^2}{1 + |m_i|^2/\sigma^2}
\;=\; \frac{1}{\sigma^2 + |m_i|^2},
$$

where $\mathbf{Q}$ is a *diagonal* matrix of weights that depend on the
current model. Rearranged:

$$
\boxed{\;
\left(\mathbf{L}^{\mathsf H}\mathbf{L}^{\mathsf T} +
\lambda\,\mathbf{Q}(\mathbf{m}^{(k)})\right) \mathbf{m}^{(k+1)}
\;=\; \mathbf{L}^{\mathsf H}\,\mathbf{d}
\;}
$$

This is **iteratively re-weighted least squares (IRLS)**: at iteration $k$,
solve a *linear* stabilized system whose damping is diagonal and
model-dependent:

- coefficients that are currently **large** get $Q_{ii} \rightarrow 0$: almost
  no additional damping — they survive and grow;
- coefficients that are currently **small** get $Q_{ii} \rightarrow
  1/\sigma^2$: strong damping — they are crushed toward zero.

Each iteration is the same cost as one LS solve. Start from
$\mathbf{m}^{(0)} = \mathbf{m}_\text{ls}$; 10–40 iterations suffice. In
practice $\lambda$ may be *decreased* across iterations (continuation):
start well-damped (behave like LS), end nearly un-damped (behave like pure
sparse inversion). Beware, though: as $\lambda \to 0$ the redundant
curvature grid re-opens near-null directions of $\mathbf{G}$ and the solve
can blow up. The lecture figure keeps $\lambda$ fixed for exactly this
reason and lets the weights do all the focusing. Typical parameters:
one $\sigma \approx 0.3$–0.6\,max$_q\|m_q\|$ shared by all frequencies
(so the sparse support stays consistent from slice to slice), and
$\lambda = 10^{-2}\,\|\mathbf{G}\|_2^2$, fixed. A final *support polish* —
a least-squares re-fit restricted to the curvatures the IRLS selected,
with damping inversely proportional to their energy — removes the
bin-to-bin solver jitter and gives clean, wavelet-shaped events.

### 3.3 What is gained, what is paid

- **Gained:** the panel becomes sparse — each event occupies a compact
  blob at its true curvature. Mute leakage (multiples bleeding through the
  keep-zone) drops sharply; aliased events focus too, making the transform
  more forgiving of coarse sampling.
- **Paid:** the data fit degrades by a few percent (the sparse model refuses
  to explain the smearing that the data does not actually need), the
  computation is an order of magnitude heavier, and two new parameters
  ($\sigma$, the $\lambda$ schedule) must be chosen. Too aggressive sparsity
  (small $\sigma$, fast $\lambda$ decay) can split one event into several
  spikes or create patchy, non-reproducible panels — always QC the
  reconstruction residual.

### 3.4 Connection forward

The same sparse-inversion pattern — *quadratic data term + sparseness prior,
solved by iterative re-weighting* — reappears throughout the course: sparse
Radon interpolation (Term 3), matching-pursuit Fourier interpolation
(Term 3 Lecture 06), and robust (L1) adaptive subtraction (Term 2 Lecture 04,
adaptive subtraction section). Learn it once here; reuse it everywhere.

---

## 4. Worked numerical example (the lecture figure, quantified)

The figure `term02_lec03_highres_radon.png` is generated with exactly this
algorithm:

- $N_x = 101$ offsets (0–2000 m, $\Delta x = 20$ m), $N_q = 21$ curvatures
  spanning $-40$–$+120$ ms, 5 events with residuals $(-8, -4, 0, +15, +40)$
  ms (three primaries, two multiples), Ricker 20 Hz wavelet;
- band 10–60 Hz; damped LS start
  ($\lambda = 10^{-2}\,\|\mathbf{G}\|_2^2$, fixed through all iterations);
- IRLS: one Cauchy weight per curvature shared by all frequencies,
  $\sigma = 0.5\,\max_q \|m_q\|$, 12 iterations.

Numbers to remember: LS reconstruction residual $\approx$ 4%; HR
reconstruction residual $\approx$ 7% — the sparse model pays a few percent
of fit for a panel made of compact, well-separated blobs. After the same
mute ($|q| \le 12$ ms) the HR-based demultiple removes the close multiple
($+15$ ms) far more completely than the LS-based one: near that multiple
the two outputs differ by $\sim 13\%$ of its amplitude, and the difference
panel of the figure shows exactly this leaked residue.

---

## References

- Hampson, D. (1986). Inverse velocity stacking for multiple elimination.
  *SEG Expanded Abstracts*.
- Sacchi, M. D. & Ulrych, T. J. (1995). High-resolution velocity gathers
  (off-line and on-line) via hyperbolic Radon transform. *SEG Expanded
  Abstracts*.
- Trad, D., Ulrych, T. & Sacchi, M. (2003). Latest views of the sparse Radon
  transform. *Geophysics*, 68(1), 386–399.
- Verschuur, D. J. (2006). *Seismic Multiple Removal Techniques*, EET
  Chapter 2. `wiki/sources/verschuur_2006_eet02_moveout_discrimination.md`
