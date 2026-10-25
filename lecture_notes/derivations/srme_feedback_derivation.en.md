# Derivation: SRME from the Feedback Diagram

This document derives the surface-related multiple elimination (SRME)
relations step by step: the feedback model, the implicit equation, the
series (explicit) solution, the iterative scheme, the surface operator,
and the 2D matrix formulation. It is the mathematical companion to Term 2
Lecture 04 (Sections 3.1–3.4).

> **Prerequisites.** Convolution, the convolution theorem, geometric
> series, and — for the 2D part — matrix multiplication. No wave
> equation is needed; the whole derivation is signal bookkeeping on one
> honest physical assumption.

---

## 1. The physical starting point

Write the earth's **primary impulse response** as $x_0(t)$: the
reflection response we would record if the free surface did not reflect
(no mirror at $z=0$). The free surface has reflection coefficient
$r_0 \approx -1$ (a pressure-release boundary: nearly perfect mirror).

**One honest assumption**: a wave that reaches the surface reflects
back down with coefficient $r_0$; whatever happens below the surface
is described by the same linear response $x_0$ every time. The earth
is a linear, time-invariant system; the surface is its feedback loop.

### 1.1 Building the multiple family order by order

- **Primaries** (order 0): the recorded response without any surface
  bounce: $x_0(t)$.
- **Order 1**: a primary comes up, reflects down ($\times r_0$),
  propagates through the subsurface *again* — that second round trip is
  exactly $x_0(t)$ as the operator. In the time domain, "propagate the
  response again" = convolve with $x_0$:

$$
m_1(t) \;=\; r_0\, x_0(t) * x_0(t) \;=\; -\,x_0 * x_0 .
$$

- **Order 2**: another loop — convolve once more:

$$
m_2(t) \;=\; r_0^2\, x_0 * x_0 * x_0 \;=\; +\,x_0 * x_0 * x_0 ,
$$

and in general $m_n = r_0^{\,n}\, x_0^{*(n+1)}$ ($n$-fold convolution of
$x_0$ with itself, $n+1$ factors). The **total recorded response** is

$$
x(t) \;=\; \sum_{n=0}^{\infty} m_n(t)
\;=\; x_0 \;-\; x_0*x_0 \;+\; x_0*x_0*x_0 \;-\;\dots
$$

Check the signs: each surface bounce contributes one factor
$r_0 = -1$, so the orders alternate $+,-,+,\dots$

---

## 2. The feedback (implicit) equation

The infinite sum has a closed form. Factor the series:

$$
x \;=\; x_0 \;-\; x_0 * \underbrace{(x_0 - x_0*x_0 + \dots)}_{=\;x}
\;=\; x_0 \;-\; x_0 * x .
$$

$$
\boxed{\; x(t) \;=\; x_0(t) \;-\; x_0(t)*x(t) \;}
$$

This is the **feedback diagram** of the lecture read as an equation:
the output $x$ is fed back through the loop ($r_0$ + subsurface $x_0$)
and added to the input $x_0$. (In the frequency domain it is simply
$X = X_0 - X_0 X = X_0(1 - X)$.)

### 2.1 Solving for the primaries — three equivalent ways

**(a) Implicit form.** Rearranging:

$$
x_0(t) \;=\; x(t) + x_0(t)*x(t) .
$$

The primaries are the data minus their *own* multiple prediction —
still implicit ($x_0$ on both sides).

**(b) Explicit series.** Solve the algebra in the frequency domain:
$X_0 = X/(1-X)$, and expand with the geometric series
$\frac{1}{1-a} = 1 + a + a^2 + \dots$ (converges for $|X(f)| < 1$,
i.e. reflectivity weak enough — see §4):

$$
\boxed{\;
x_0(t) \;=\; x(t) \;+\; x(t)*x(t) \;+\; x(t)*x(t)*x(t) \;+\;\dots
\;}
$$

**Multiple removal by auto-convolution and summation of the input.**
Each term is one more order of multiples, expressed through the data
themselves. Substituting the feedback relation shows the series
reorganizes the multiple orders: the $k$-th term predicts (part of)
every order $\ge k$.

**(c) Iterative (fixed-point) scheme.** Use the implicit form as an
update rule — start with the data as the first guess:

$$
\boxed{\;
p_0^{(0)} = p, \qquad
p_0^{(i+1)} \;=\; p \;-\; a * p_0^{(i)} * p
\;}
$$

($a$ is the surface operator, §3; with $a = 1$ this is the pure
impulse-response version.) Each iteration removes one more multiple
order to leading accuracy:

- iteration 1 subtracts $p*p$, the first-order prediction;
- iteration 2 subtracts the prediction computed from the *cleaned*
  estimate, effectively the second order;
- ... converging geometrically to $x_0$ (lecture figure: residual
  $33\% \to 15\% \to 9\% \to 5\% \to \dots$).

Why the iteration is preferred in practice: it never forms the higher
auto-convolutions explicitly (which grow long and expensive), and it
pairs naturally with adaptive subtraction at each pass.

---

## 3. The wavelet and the surface operator

Real sources are not impulses: the primary response is convolved with
the source signature $s(t)$ (and the receiver response; absorb
everything into one wavelet). Then

$$
p_0(t) = x_0(t)*s(t), \qquad p(t) = x(t)*s(t),
$$

and the naive feedback would read $p \overset{?}{=} p_0 - p_0*p$ —
which is dimensionally wrong: $p_0*p$ carries *two* wavelets
(spectrum $\propto S^2$), while a multiple in $p$ carries one
($\propto S$). The correct loop must divide one wavelet out at each
convolution. Define the **surface operator**

$$
\boxed{\; a(t) \;=\; -\,[s(t)]^{-1} \;}
\qquad\text{(an inverse-source filter, } A(f) = -1/S(f) \text{)}
$$

and the feedback becomes

$$
p(t) \;=\; p_0(t) \;+\; a(t) * p_0(t) * p(t) ,
$$

giving the practical iterative scheme (the one implemented in the
lecture figures):

$$
p_0^{(i+1)} \;=\; p \;-\; a * p_0^{(i)} * p .
$$

**Practical notes.**

1. $1/S(f)$ must be stabilized (the wavelet spectrum vanishes at low
   and high frequencies): use $A(f) = -\overline{S(f)} /
   (|S(f)|^2 + \varepsilon)$ with $\varepsilon$ a small fraction of
   $\max|S|^2$, plus a band taper — outside the usable band the
   operator must vanish or the iteration amplifies noise and diverges.
2. $s(t)$ is never perfectly known, and directivity/3D effects are not
   in $a$ at all — hence adaptive subtraction as the final step.
3. Sign bookkeeping: $a$ already contains the surface reflection
   coefficient ($r_0 = -1$); do not multiply it in twice.

---

## 4. When does the series converge?

In the frequency domain the series solution is geometric:
$x_0 = x(1 + x + x^2 + \dots)$ converges iff $|X(f)| < 1$ for all $f$.
Since $X = X_0/(1+X_0)$, this means $|X_0(f)| > -\tfrac12$-bounded;
roughly: the **sum of reflection coefficients along any resonant path
must not approach $-1$**. Physical reading: a water column whose
reverberation gain ($R_\text{bot} \cdot |r_0|$) approaches 1 traps the
energy — the series (and the iteration) then diverges. Real data sit
well inside the convergence region ($\sum |R_k| \lesssim 0.5$), which
is why 2–3 iterations suffice in production.

---

## 5. The 2D formulation

### 5.1 From scalar to matrix

In 2D, the recorded data are a function of source and receiver:
$P(x_r, x_s, t)$ — and "convolve the response with itself" becomes
"convolve a shot-gather trace with a receiver-gather trace, integrated
over the surface". Justification by ray bookkeeping (the lecture's
Figure 7):

- take a surface multiple recorded at $(x_s \to x_r)$ with downward
  reflection point $x_k$;
- **leg 1**: $x_s \to$ subsurface $\to x_k$ — this is a trace of the
  *shot gather* of $x_s$: $P(x_k, x_s)$;
- **leg 2**: $x_k \to$ subsurface $\to x_r$ — a trace of the
  *receiver gather* of $x_r$, i.e. a "shot" at $x_k$: $P(x_r, x_k)$;
- the multiple's travel time is the sum of the legs' times; its
  amplitude the product of the legs' amplitudes (and $r_0$) — time
  convolution again, this time trace-to-trace.

We do not know $x_k$, so we sum over all surface points:

$$
\boxed{\;
M(x_r, x_s; f) \;=\; A(f) \int P(x_r, x_k; f)\, P(x_k, x_s; f)\;dx_k
\;}
$$

Discretizing the surface ($N$ points, spacing $\Delta x$) and
collecting the data per frequency slice into the **data matrix**
$\mathbf{P}(f) = [P(x_r, x_s; f)]$ (receivers as rows, shots as
columns):

$$
\mathbf{M}(f) \;=\; A(f)\,\Delta x\; \mathbf{P}(f)\,\mathbf{P}(f) ,
$$

a matrix product per frequency — this *is* the multidimensional
convolution. The feedback relation becomes a matrix equation,

$$
\mathbf{P} \;=\; \mathbf{P}_0 \;+\; A\,\mathbf{P}_0\,\mathbf{P}
\qquad\Longrightarrow\qquad
\mathbf{P}_0 \;=\; \mathbf{P} - A\,\mathbf{P}_0\,\mathbf{P} ,
$$

solved by the same iteration $\mathbf{P}_0^{(i+1)} =
\mathbf{P} - A\,\mathbf{P}_0^{(i)}\mathbf{P}$.

### 5.2 The multiple contribution gather

For one target trace, the integrand $A\,P(x_r, x_k) P(x_k, x_s)$ as a
function of $x_k$ is the **MCG**. Each multiple event in it has its
apex (stationary point of the sum) exactly at the true surface
reflection point of that path — the diagnostic panel used to QC
aperture problems (missing near offsets truncate the MCG's flat legs;
missing shots decimate its columns).

### 5.3 What the discretization hides

The integral $\int dx_k$ assumes the surface is densely and
completely sampled: **missing data are missing prediction**. The
dimensional prefactor $\Delta x$ (and, in rigorous treatments, the
geometrical-spreading/obliquity weights of the representation theorem)
is absorbed in practice into the surface operator $A$ and the adaptive
subtraction — which is why the teaching engine of the lecture figures
calibrates the coupling constant and still recovers the multiples.

### 5.4 3D and beyond

In 3D the integral runs over the 2D surface: $M(x_r, x_s) =
A \iint P(x_r, x_k) P(x_k, x_s)\, dx_k dy_k$ — the data become a
matrix per inline/crossline pair, and the requirements (dense shots
*and* crossline sampling) multiply. This is why 3D SRME drove the
industry to wide-azimuth acquisition, shot interpolation and 5D
regularization. Internal multiples require removing the "surface"
assumption entirely — extension methods (IME, Marchenko) exist but are
beyond this course.

---

## 6. Worked example (the lecture figure, quantified)

The figure `term02_lec04_srme_iterations.png` implements §3 exactly:
four reflectors ($R = 0.20, 0.10, 0.08, 0.05$; $\sum|R| = 0.43 <
\tfrac12$), 26 Hz wavelet, $A(f)$ stabilized at $\varepsilon =
10^{-3}\max|S|^2$ with a band taper at $10\%\,|S|_{\max}$.

Numbers to remember: relative primary residual per iteration
$33\% \to 15\% \to 9\% \to 5\% \to 4\% \to 3\%$ — geometric
convergence, one order of multiples per iteration, all of it computed
from the data themselves.

---

## References

- Verschuur, D. J. (2006). *Seismic Multiple Removal Techniques: Past,
  Present and Future*, EET Chapter 5. `wiki/sources/verschuur_2006_eet05_principles_srme.md`
- Berkhout, A. J. & Verschuur, D. J. (1997). Estimation of multiple
  scattering by iterative inversion, Part I. *Geophysics* 62(5).
- Verschuur, D. J., Berkhout, A. J. & Wapenaar, C. P. A. (1992).
  Adaptive surface-related multiple elimination. *Geophysics* 57(9).
- Companion lecture notes: Term 2 Lecture 04, Sections 3.1–3.4.
