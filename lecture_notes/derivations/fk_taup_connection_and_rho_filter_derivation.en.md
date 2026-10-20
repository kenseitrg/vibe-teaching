# The FK–Tau-p Connection and the Rho Filter: A Step-by-Step Derivation

This document derives, step by step, the two results that Term 2 Lecture 02 states without proof: the **Fourier slice theorem**, which says that the tau-p panel is the FK spectrum read in "polar" coordinates, and the **rho filter**, the ramp response $|f|$ that must be applied to each p-trace before the adjoint (sum-back) transform can reconstruct the data. It is supplementary reading for Term 2 Lecture 02, Sections 5–8, and follows the development of Margrave (2006, §§2-63–2-73) and Yilmaz (2001, §6.3).

> **Prerequisites.** The 1-D Fourier transform and convolution theorem (Term 1 Lecture 05), the 2-D Fourier transform and the FK picture of dips (Term 2 Lecture 02, §§2 and 7), the delta function and the identity $\int e^{2\pi i \xi t}\,dt = \delta(\xi)$ (see the [DFT and spectral leakage derivation](dft_and_spectral_leakage_derivation.en.md)), and the matrix transpose as an adjoint. No tomography background is assumed.

---

## 1. Setup: three representations of one gather

A shot gather is a function of time and offset, $d(t, x)$. Throughout this document we use the 2-D Fourier transform pair in the sign convention of the lecture notes,

$$
D(f, k) = \iint d(t, x)\, e^{-2\pi i (f t - k x)}\, dt\, dx,
\qquad
d(t, x) = \iint D(f, k)\, e^{+2\pi i (f t - k x)}\, df\, dk .
$$

Here $f$ is temporal frequency (cycles/s) and $k$ is wavenumber (cycles/m). It will be convenient to give a name to the *per-trace* spectrum — the 1-D Fourier transform of one trace over time,

$$
\psi(x, f) \;=\; \int d(t, x)\, e^{-2\pi i f t}\, dt ,
$$

so that the 2-D transform factorizes into two 1-D transforms:

$$
D(f, k) \;=\; \int \psi(x, f)\, e^{+2\pi i k x}\, dx .
$$

(Do the $t$-integral first and you get $\psi$; then the $x$-integral finishes the job. The $+2\pi i k x$ sign is not a typo: it is how $k$ enters our convention $e^{-2\pi i (ft - kx)}$.)

The **linear Radon transform** (slant stack) of the lecture, written as a continuous integral, is

$$
u(\tau, p) \;=\; \int d(\tau + p x,\; x)\, dx :
$$

shift each trace by the linear moveout $-px$, sum over offsets, and record the result on the trace "belonging" to the slope $p$. Finally, the **f–p spectrum** is the 1-D Fourier transform of the tau-p panel over the intercept-time axis,

$$
U(f, p) \;=\; \int u(\tau, p)\, e^{-2\pi i f \tau}\, d\tau .
$$

The two claims to be proved:

> **Claim 1 (projection-slice theorem, §2).**
> $\displaystyle U(f, p) = D(f,\; pf)$ — the f–p spectrum is the FK spectrum resampled onto the radial line $k = pf$.

> **Claim 2 (filtered back projection, §5).**
> $\displaystyle d(t, x) = \alpha(t) * \int u(t - p x,\; p)\, dp$, where the **rho filter** $\alpha$ has spectrum $\hat\alpha(f) = |f|$ — the exact inverse is the adjoint ("sum back") *followed by* the ramp filter $|f|$.

The plan: §2 proves Claim 1 and works a plane-wave example. §3 derives the adjoint operator properly. §4 composes forward + adjoint and discovers — in three lines — the defect that the rho filter repairs. §5 rederives the inverse honestly, by a change of variables in the inverse 2-D Fourier integral, and shows where the $|f|$ comes from geometrically. §6 studies the rho filter itself, and §7 collects the practical recipe, the matrix view, and the door to least squares.

---

## 2. Forward direction: the projection-slice theorem

### 2.1 Fourier-transform the slant stack over $\tau$

Start from the definition of the f–p spectrum and substitute the slant stack:

$$
U(f, p) = \int \left[\, \int d(\tau + p x,\; x)\, dx \,\right] e^{-2\pi i f \tau}\, d\tau
= \iint d(\tau + p x,\; x)\; e^{-2\pi i f \tau}\; dx\, d\tau .
$$

For each fixed offset $x$, change variables in the $\tau$-integral: let

$$
t = \tau + p x \qquad \Longleftrightarrow \qquad \tau = t - p x, \qquad d\tau = dt .
$$

The exponential picks up the shift: $e^{-2\pi i f \tau} = e^{-2\pi i f (t - px)} = e^{-2\pi i f t}\, e^{+2\pi i f p x}$. Therefore

$$
U(f, p) = \int \underbrace{\left[\, \int d(t, x)\, e^{-2\pi i f t}\, dt \,\right]}_{=\;\psi(x,\,f)} e^{+2\pi i f p x}\, dx .
$$

Compare the bracket with §1: it is exactly the per-trace spectrum $\psi(x, f)$. And the outer integral has precisely the form of the spatial half of the 2-D Fourier transform, $\int \psi\, e^{+2\pi i k x} dx$, evaluated at

$$
k = p f .
$$

Hence the theorem:

$$
\boxed{\; U(f, p) = D(f,\; k = p f) \;}
$$

Read it in words: *the 1-D Fourier transform over $\tau$ of the slant stack at slope $p$ equals the FK spectrum along the radial line through the origin with slope $p$.* All the lecture's dictionary between the domains follows: a linear event (energy on one radial line in FK) becomes a point on one p-trace; a dip-reject fan in FK is a band of rejected $p$-values in f–p; and a point in tau-p spreads into the line $k = pf$ once transformed over $\tau$.

Read backwards, the same chain of equalities gives a legitimate *computational* route for the forward transform: 2-D FFT the gather, resample the spectrum from the rectangular $(f, k)$ grid onto radial lines $k = p_j f$ for each requested $p_j$, then inverse FFT over $f$ to get $\tau$ back. This is how tau=p transform can be computed in the frequency domain.

### 2.2 Worked example: one plane wave on a finite cable

Take a single linear event — a plane wave $d(t,x) = s(t - \tau_0 - p_0 x)$ with wavelet $s$, intercept $\tau_0$ and slope $p_0$. Its per-trace spectrum is a delayed wavelet spectrum:

$$
\psi(x, f) = S(f)\, e^{-2\pi i f (\tau_0 + p_0 x)} .
$$

Now slant-stack it over a symmetric cable of half-length $L/2$, i.e. integrate $x$ from $-L/2$ to $+L/2$. By the calculation of §2.1,

$$
U(f, p) = S(f)\, e^{-2\pi i f \tau_0} \int_{-L/2}^{L/2} e^{2\pi i f (p - p_0) x}\, dx
= S(f)\, e^{-2\pi i f \tau_0}\; L\, \mathrm{sinc}\!\left( f L (p - p_0) \right),
$$

where $\mathrm{sinc}(\xi) = \sin(\pi \xi) / (\pi \xi)$. The event focuses where it should — at $p = p_0$, where the sinc peaks — but on a *finite* cable the focus is not a point: it is a sinc-shaped smear in $p$ whose first null sits at

$$
|p - p_0| \;=\; \frac{1}{f L} \qquad \text{(p-resolution of a finite cable)} .
$$

**Numbers** (the lecture's running example): a symmetric cable of half-length $1475$ m has $L = 2950$ m. At $f = 20$ Hz the first null lies $1/(20 \times 2950) \approx 17\ \mu\text{s/m}$ from the true dip. The two noise trains of the running example — ground roll at $p = 3.33$ ms/m and air blast at $1.67$ ms/m — are separated by $1660\ \mu\text{s/m}$, some 95 resolution widths: they focus as cleanly separated blobs. Even at 5 Hz the null width is only $68\ \mu\text{s/m}$. Resolution in $p$ degrades toward low frequency and short cables — the same trade-off as any aperture-limited measurement.

### 2.3 A first appearance of $1/|f|$

What if the cable were infinitely long? Then the integral $\int e^{2\pi i f (p - p_0) x} dx$ over an infinite line is a delta function of its exponent's argument:

$$
\int_{-\infty}^{\infty} e^{2\pi i f (p - p_0) x}\, dx \;=\; \delta\!\big(f (p - p_0)\big) \;=\; \frac{\delta(p - p_0)}{|f|},
$$

using the scaling rule $\delta(a\,\xi) = \delta(\xi)/|a|$ (here $a = f$, held fixed while the delta acts in $p$). So even the *perfect*, infinite-aperture transform of a plane wave is

$$
U(f, p) = S(f)\, e^{-2\pi i f \tau_0}\; \frac{\delta(p - p_0)}{|f|} :
$$

a perfect point in $p$, but a **$1/|f|$-weighted copy of the wavelet spectrum** along $\tau$.

### 2.4 The discrete caveat

The theorem equates *continuous* objects. On a grid, $D(f, k)$ is known only at rectangular $(f, k)$ samples, while the radial samples $k = p_j f$ fall between them, at positions that depend on $f$. Resampling (interpolation) is required, and there is a structural annoyance: the radial lines crowd toward the origin and spread apart at high $|k|$, so **no set of discrete $p$ values covers the $(f, k)$ grid uniformly**. The discrete tau-p transform always loses something in a round trip — unlike the DFT pair, whose forward and backward matrices are exact inverses of each other.

---

## 3. The adjoint of the slant stack

### 3.1 Adjoints from inner products

The adjoint of an operator is defined through inner products: $R^*$ is the adjoint of $R$ if, for every input $d$ and every test function $m$,

$$
\langle R d,\; m \rangle \;=\; \langle d,\; R^* m \rangle ,
$$

where the inner product on each space is "sum of products" (integral over the domain, or plain dot product for vectors). Physically the identity is an energy-bookkeeping statement: the correlation of the panel with *any* test pattern equals the correlation of the data with the back-projected test pattern. The adjoint is *derived*, not guessed — so let us derive it.

Take $R$ = slant stack, $u = R d$, and compute with a real-valued gather (complex data: conjugate the first factor; nothing else changes):

$$
\langle u,\, m \rangle
= \iint \underbrace{\left[\int d(\tau + p x,\; x)\, dx\right]}_{u(\tau, p)}\; m(\tau, p)\; d\tau\, dp .
$$

Interchange the order of integration (the functions are decent; this is Fubini's theorem), and in the $\tau$-integral for each fixed $x$ substitute $t = \tau + p x$, $d\tau = dt$:

$$
\langle u,\, m \rangle
= \int dx \int dt\; d(t, x) \underbrace{\left[\int m(t - p x,\; p)\, dp\right]}_{=\;(R^* m)(t, x)} .
$$

The bracket multiplies $d$ and is integrated over $t$ and $x$: it is exactly the inner product $\langle d,\, R^* m\rangle$ with

$$
\boxed{\; (R^* m)(t, x) = \int m(t - p x,\; p)\, dp \;}
$$

— the **adjoint slant stack**: distribute each p-trace along the line $t = \tau + px$ (an *inverse* linear moveout) and sum over $p$. This is the operator the lecture called $d_\text{adj}(t,x) = \sum_j u(t - p_j x,\, p_j)\, \Delta p$. In discrete form, with the time shifts implemented as a matrix, the adjoint is simply the matrix transpose — "run the movie backwards". Forward: LMO then sum over $x$. Adjoint: sum over $p$ then un-LMO. Symmetric-looking — but symmetric is not the same as inverse.

---

## 4. The round trip: why the adjoint alone fails

### 4.1 One frequency at a time

The Fourier transform over $t$ turns the whole discussion into algebra, because the slant stack's time shifts become phases. From §2.1 (with the roles of the variables swapped) and §3.1, per frequency $f$:

$$
\text{forward:}\quad U(p) = \int \psi(x)\, e^{+2\pi i f p x}\, dx,
\qquad
\text{adjoint:}\quad \psi_\text{adj}(x) = \int U(p)\, e^{-2\pi i f p x}\, dp ,
$$

where we write $\psi(x)$ for $\psi(x, f)$ and $U(p)$ for $U(f, p)$ — at this one frequency, both are just functions of one variable, and the pair of integrals looks almost like a Fourier transform and its inverse. *Almost* is the operative word.

### 4.2 The composition: three lines and a surprise

Compose them — forward, then adjoint — on arbitrary $\psi$:

$$
\psi_\text{adj}(x)
= \int dp\; e^{-2\pi i f p x} \int dx'\; \psi(x')\, e^{+2\pi i f p x'}
= \int dx'\; \psi(x') \underbrace{\int dp\; e^{2\pi i f p (x' - x)}}_{=\;\delta\left(f (x'-x)\right)} .
$$

The inner integral is our delta-function identity from §2.3, now acting in $x'-x$ at fixed $f$, so $\delta(f(x'-x)) = \delta(x'-x)/|f|$. The delta collapses the outer integral:

$$
\boxed{\; \psi_\text{adj}(x, f) = \frac{1}{|f|}\; \psi(x, f) \;}
$$

— with complete, continuous sampling in both $x$ and $p$, the round trip $\;R^* R\;$ is not the identity but a **$1/|f|$ filter**. Every frequency of every trace comes back attenuated in proportion to $1/|f|$.

This single line explains everything the lecture's Figure 12 shows about the adjoint-only reconstruction:

- the output is a **low-frequency-flavored** copy — a 5 Hz component survives ten times stronger (relatively) than a 50 Hz one, so the reconstructed wavelets are broader and duller than the input's;
- the fix is staring at us: if the round trip multiplies by $1/|f|$, then the correct inverse is the adjoint **combined with a multiplication by $|f|$**. That multiplier is the rho filter. The remaining sections make this rigorous and geometric.

### 4.3 The two truncations of real data

The identity $R^*R = 1/|f|$ assumed integration over $-\infty < x < \infty$ and $-\infty < p < \infty$. Real transforms truncate both, and each truncation adds its own artifact on top of the $1/|f|$ defect:

- **Finite $p$-range** $[p_{\min},\, p_{\max}]$: the inner integral above becomes a windowed integral, $\int_{p_{\min}}^{p_{\max}} e^{2\pi i f p \Delta x} dp$ — a sinc in $\Delta x = x' - x$ with first null at $\Delta x = 1/(f \, p_\text{range})$. The reconstruction at offset $x$ is now a *smeared average* of the true section around $x$: too narrow a $p$-range limits the reconstructable dip bandwidth. Discrete, coarse $\Delta p$ sampling adds periodic replicas of this kernel — the p-aliasing of lecture §6.1, governed by Taner et al.'s rule $\Delta p \le 1/(2\, x_\text{max} f_\text{max})$.
- **Finite aperture** $[-L/2, L/2]$: the *forward* transform is truncated in $x$, and §2.2 showed the consequence — the focused image of an event acquires the sinc side lobes $L\,\mathrm{sinc}(fL(p-p_0))$ smeared along $p$, of width $1/(fL)$, worst at low frequency and at the aperture edges.

| Defect | Symptom (lecture §8.1) | Cure |
|---|---|---|
| missing $\|f\|$ ramp | low-frequency-flavored, broadened wavelets | **rho filter** |
| finite aperture | smearing + side lobes *along $p$* | p-direction deconvolution (Zhou & Greenhalgh 1994) or least-squares / high-resolution Radon (§7.3) |
| coarse $\Delta p$ | replica artifacts, opposite-sign $p$ energy | finer $p$ sampling, low-pass before transform (lecture §6.1) |

The rho filter repairs the first row only. That division of labor is worth remembering: the rho filter works along the *time* axis of each p-trace; the remaining problems live along the *p* axis and need operators that act in $p$.

---

## 5. The exact inverse: filtered back projection

Section 4 guessed the inverse from the round-trip behavior. Here is the honest construction, which does not assume complete sampling: start from the inverse 2-D Fourier transform and simply change variables.

### 5.1 Change of variables in the inverse 2-D integral

Begin with the exact inversion formula of §1:

$$
d(t, x) = \iint D(f, k)\, e^{+2\pi i (f t - k x)}\, df\, dk
= \int df \underbrace{\int dk\; D(f, k)\, e^{-2\pi i k x}}_{\text{inner: over } k \text{ at fixed } f}\, e^{+2\pi i f t} .
$$

We want the $k$-integral expressed through $p$ — using the slice theorem's identification $k = pf$. Substitute $k = f p$ and treat the two signs of $f$ separately, because the substitution behaves differently for each:

**For $f > 0$:** as $p$ runs from $-\infty$ to $+\infty$, $k = fp$ runs from $-\infty$ to $+\infty$ — same direction, and $dk = f\,dp$ with $f > 0$. Straightforwardly,

$$
\int_{-\infty}^{\infty} D(f, k)\, e^{-2\pi i k x}\, dk
= \int_{-\infty}^{\infty} f\, D(f, p f)\, e^{-2\pi i f p x}\, dp .
$$

**For $f < 0$:** now $k = fp$ runs from $+\infty$ to $-\infty$ as $p$ runs from $-\infty$ to $+\infty$ — the substitution *reverses the direction of travel* along the axis. Tracing the limits carefully,

$$
\int_{k=-\infty}^{\infty} D\, e^{-2\pi i k x}\, dk
= \int_{p=+\infty}^{-\infty} D(f, pf)\, e^{-2\pi i f p x}\; (f\, dp)
= -\int_{-\infty}^{\infty} f\, D(f, pf)\, e^{-2\pi i f p x}\, dp
= \int_{-\infty}^{\infty} |f|\, D(f, pf)\, e^{-2\pi i f p x}\, dp ,
$$

because $-f = |f|$ when $f < 0$. Both signs of $f$ give the same expression with the factor $|f|$, so the full integral becomes

$$
\boxed{\; d(t, x) = \iint |f|\; D(f, p f)\; e^{+2\pi i f (t - p x)}\; dp\, df \;}
$$

(The set $f = 0$, where the substitution is undefined, is a line of zero area — it contributes nothing.)

Two equivalent ways to remember the $|f|$:

- **Jacobian.** The coordinate map $(k, f) \to (p, f)$, $p = k/f$, has Jacobian determinant $\partial k / \partial p = f$; a change of measure uses its absolute value. The orientation reversal for $f<0$ is exactly the sign that the absolute value removes.
- **Cell areas.** A small rectangle $df \times dp$ in the f–p plane maps to a patch of FK area $|f|\, df\, dp$ (a strip of width $f\,dp$ at height $f$). The two coordinate systems do not measure area the same way, and the mismatch grows with frequency — the "amplitude price" of lecture §7. High-frequency p-cells carry more FK territory per unit $p$.

### 5.2 Factoring into adjoint $\times$ convolution

Now use Claim 1 to replace $D(f, pf)$ by the f–p spectrum $U(f, p)$ — the Fourier transform over $\tau$ of the panel we already have:

$$
d(t, x) = \iint |f|\; U(f, p)\; e^{+2\pi i f (t - p x)}\, dp\, df
= \int dp \underbrace{\int |f|\, U(f, p)\, e^{+2\pi i f (t - px)}\, df}_{\text{inner: over } f \text{ at fixed } p} .
$$

Focus on the inner integral. If it were not for the leading $|f|$, it would be exactly the inverse Fourier transform of the p-trace $u(\tau, p)$, evaluated at the shifted time $t - px$. Multiplication by $|f|$ in the frequency domain is, by the convolution theorem (Term 1 Lecture 05), convolution in the time domain with the (distributional) function $\alpha$ whose spectrum is $|f|$. Defining $\alpha$ by

$$
\hat\alpha(f) = |f| ,
$$

the inner integral is $(\alpha * u(\cdot, p))(t - px)$ — filter the p-trace, then time-shift it. Pulling the convolution out of the $p$-integral (it acts on $t$ only, not on $p$):

$$
\boxed{\; d(t, x) = \alpha(t) \;*\; \int u(t - p x,\; p)\, dp \;}
$$

The integral on the right is *precisely* the adjoint slant stack of §3. So the exact inverse of the tau-p transform is

$$
\text{inverse} \;=\; \underbrace{\alpha}_{\text{rho filter}} \;*\; \underbrace{R^*}_{\text{adjoint}} \;,
$$

— **filtered back projection**: project each (filtered) p-trace back along its line and sum, then restore the spectrum with the ramp. This is the same formula tomography uses to reconstruct a CT scan from projections; there the ramp is called the $\lambda$-filter. Note how the two derivations meet: §4.2 found that $R^*R$ multiplies spectra by $1/|f|$; §5 finds that the true inverse contains a compensating $|f|$. Two halves of one Jacobian.

### 5.3 Frequency-domain implementation

Taking the Fourier transform over $t$ of the boxed formula gives the practical implementation:

$$
\psi(x, f) = |f| \int U(f, p)\, e^{-2\pi i f p x}\, dp :
$$

per frequency, multiply by the ramp, sum over $p$ with the steering phase $e^{-2\pi i fpx}$, then inverse-FFT over $f$. 

---

## 6. The rho filter itself

### 6.1 Spectrum

The rho filter is the convolution operator

$$
\alpha(t) \quad \text{with} \quad \hat\alpha(f) = |f| :
$$

a **zero-phase ramp** — real, even, non-negative. Zero phase matters: the adjoint round trip *attenuated* amplitudes but rotated no phases, so the repair must be a pure amplitude rescaling, applied equally to positive and negative frequencies. A true time derivative has the same amplitude shape ($2\pi |f|$, up to the constant) but adds a $90^\circ$ phase rotation; using it instead of $\alpha$ would restore the amplitudes and rotate every wavelet into an antisymmetric ringing shape. (The name "$\rho$-filter", with $\hat\rho = |\omega|$ in angular-frequency notation, comes to seismic processing via Claerbout, as presented in Yilmaz §6.3.)

### 6.2 Impulse response

What does $\alpha$ look like in time? Formally,

$$
\alpha(t) = \int_{-\infty}^{\infty} |f|\, e^{+2\pi i f t}\, df
= 2 \int_0^\infty f \cos(2\pi f t)\, df ,
$$

where the sine half dropped out because $|f|$ is even. The integral does not converge as an ordinary integral — $\alpha$ is a *distribution*, like the delta function itself. To see its shape, regularize: multiply the ramp by $e^{-\varepsilon |f|}$, integrate, then let $\varepsilon \to 0^+$. The elementary integral (differentiate $\int_0^\infty e^{-\varepsilon f}\cos(\omega f) df = \varepsilon/(\varepsilon^2 + \omega^2)$ with respect to $\varepsilon$) gives

$$
\int_0^\infty f\, e^{-\varepsilon f} \cos(\omega f)\, df = \frac{\varepsilon^2 - \omega^2}{(\varepsilon^2 + \omega^2)^2}
\;\xrightarrow[\varepsilon \to 0^+]{}\; -\frac{1}{\omega^2},
\qquad \omega = 2\pi t .
$$

Therefore

$$
\boxed{\; \alpha(t) = -\frac{1}{2\pi^2 t^2} \quad (t \neq 0) \;}
$$

— a sharply peaked, symmetric, strongly singular spike at $t=0$ sitting on broad negative tails that decay like $1/t^2$ (plus a compensating delta-like correction at the origin that the pointwise formula hides; the regularized $\alpha_\varepsilon$ has zero net area, its positive spike exactly balanced by the negative tails — as it must, since $\hat\alpha(0) = 0$). In practice one never applies this ideal object: the discrete ramp $|f|$ on the grid $|f| \le f_N$, tapered toward Nyquist, has a well-behaved, symmetric, short impulse response of exactly this character — big central lobe, small negative side lobes.

### 6.3 Relatives

The similar ramp can be met in other applications:

- **Derivative + Hilbert transform.** With $\tfrac{d}{dt} \leftrightarrow 2\pi i f$ and the Hilbert transform $\mathcal{H} \leftrightarrow -i\,\mathrm{sgn}(f)$, their composition obeys $(2\pi i f)\cdot(-i\,\mathrm{sgn} f) = 2\pi |f|$, hence
  $$\alpha = \tfrac{1}{2\pi}\, \mathcal{H}\,\tfrac{d}{dt} = \tfrac{1}{2\pi}\, \tfrac{d}{dt}\, \mathcal{H} :$$
  the rho filter is *a first derivative with the derivative's phase removed* — "differentiate the wavefield, then un-rotate it". This is why the rho filter sharpens wavelets the way differentiation would, without smearing them into antisymmetric doublets.
- **CT tomography.** The $\lambda$-filter of filtered back projection in computerized tomography is the same $|\omega|$ ramp, for the same reason: the Radon transform of a 2-D object samples the object's 2-D spectrum along radial slices, and reassembling polar samples into a Cartesian integral carries the same Jacobian.
- **Kirchhoff migration.** The migration integral is a diffraction stack — an adjoint-type summation over a family of curves — and its amplitude-preserving form contains a time-differentiation of the stacked result (Yilmaz §4.1): the same ramp, meeting us again from the other direction in Term 3.

---

## 7. Practice, and what the rho filter does not fix

### 7.1 The recipe

A production inverse tau-p with rho filtering:

1. Fourier-transform each p-trace over $\tau$: $u(\tau, p_j) \to U(f, p_j)$.
2. Multiply each $U(f, p_j)$ by the ramp $|f|$ — the *complex* spectrum times a *real* ramp, i.e. amplitudes scaled, phases untouched — **tapered gently toward Nyquist**.
3. Inverse-transform back to $\tau$ (or keep the spectra and fold step 3 into step 4 via §5.3).
4. Adjoint slant stack: spread each p-trace along $t = \tau + p_j x$ with sinc interpolation of the time shifts, sum over $j$.

Why taper the ramp? The ideal ramp wants to keep growing past Nyquist; the data cannot follow it there, and the top octave is dominated by interpolation error from the $\tau$-shifts and by whatever noise survived the forward transform. Boosting $|f|$ near $f_N$ multiplies exactly those components. A soft taper trades a little brightness for a lot of noise suppression — the same philosophy as the prewhitening of Term 1 deconvolution.

Why does it not matter whether $\alpha$ is applied to the p-traces *before* the adjoint (step 2–3) or to the reconstructed gather *after* it (as the lecture's formula $\alpha * \sum_j u \Delta p$ writes it)? Because convolution with a fixed filter commutes with time shifts and with sums: $(\alpha * u)(t - px) = \alpha * \big(u(t - px)\big)$ componentwise. 

### 7.2 What is repaired, what is not

After rho filtering, the round trip of §4 satisfies $\;|f| \cdot R^*R \approx I\;$ *to the extent that the sampling was complete*. The defects of the second and third rows of the §4.3 table — smearing and side lobes along $p$ from the finite aperture, replicas from coarse $\Delta p$ — survive the rho filter untouched, because they live in the $p$ direction and $\alpha$ acts along $\tau$ only. The lecture's Figure 12 shows precisely this: with rho, wavelets regain bandwidth and symmetry; the residual error is defocus and side lobes *in p*.

### 7.3 The matrix view and the door to least squares

Discretize, and work per frequency $f$ as in §4.1: samples $\psi_k = \psi(x_k, f)$ of the gather and $U_j = U(f, p_j)$ of the panel. The pair of transforms is a pair of matrices,

$$
U = G\,\psi, \qquad G_{jk} = e^{2\pi i f p_j x_k},
\qquad\qquad
\psi_\text{adj} = G^* U ,
$$

where $G^*$ (conjugate transpose; plain transpose for real data at fixed $f$) implements the adjoint. The two composition results of this document now read, in matrix language:

$$
G^* G \;\approx\; \frac{1}{|f|}\, I_{n_x}
\qquad\text{(complete } p \text{ sampling: §4.2),}
$$

so the rho-corrected adjoint $\;|f|\, G^* U\;$ is an approximate inverse; and

$$
(G G^*)_{j j'} = \sum_k e^{2\pi i f (p_j - p_{j'}) x_k}
\;\approx\; L\, \mathrm{sinc}\!\big(f L (p_j - p_{j'})\big)
\qquad\text{(finite aperture: §2.2),}
$$

so the *forward* transform on real data smears each event with the aperture sinc along $p$ — this is the matrix whose inverse (with a small white-noise term for stability, $\varepsilon^2$, exactly the prewhitening of Wiener deconvolution) constitutes the **p-direction deconvolution** of Zhou & Greenhalgh (1994).

One more step closes the loop with the lecture's §8.3 teaser. Instead of accepting the smeared forward panel $U = G\psi$, solve for the panel that best explains the data through the rho-adjoint — a least-squares problem,

$$
U_\text{LS} = \big(G G^* + \varepsilon^2 I\big)^{-1} G\, \psi ,
$$

(up to the $|f|$ bookkeeping of §5.3). Because the inversion divides out the aperture sinc $G G^*$, the LS panel is focused where the conventional panel smears, and its rho-adjoint reconstruction has fewer artifacts. Add a sparsity constraint on $U$ and you have the **high-resolution Radon transform** — the subject of Term 3 Lecture 06, where the same least-squares machinery returns for Radon interpolation and de-aliasing. The classical warning stands: on poorly sampled data the plain transform pair is a poor approximation to anything, and LS or sparse inversion is not a luxury but a necessity (Marfurt et al. 1996).

---

## References

- Margrave, G. F. (2006). *Methods of Seismic Data Processing* (Geophysics 557 lecture notes), University of Calgary, §§2-63–2-73 (projection-slice theorem; inverse tau-p and filtered back projection). `wiki/sources/margrave_2006_methods_of_seismic_data_processing.md`
- Yilmaz, Ö. (2001). *Seismic Data Analysis*, Vol. 2, §6.3 (slant-stack transformation; rho filter as presented after Claerbout). `wiki/sources/yilmaz_2001_seismic_data_analysis_taup.md`
- Zhou, B. & Greenhalgh, S. A. (1994). Linear and parabolic $\tau$-$p$ transforms revisited. *Geophysics*, 59(7), 1133–1149 (p-direction deconvolution for finite aperture). `wiki/sources/zhou_greenhalgh_1994_linear_parabolic_taup.md`
- Taner, M. T., Koehler, F., Alhilali, K. A. & Sherwood, R. D. (1990). Aliasing in the tau-p transform and the removal of spatially aliased coherent noise. *Geophysics*, 55(9), 1496–1503 (the $\Delta p$ rule).
- Marfurt, K. J., Schneider, R. V. & Mueller, M. C. (1996). Pitfalls of using conventional Radon transforms on poorly sampled data. *Geophysics*, 61(5), 1467–1482.
- Trad, D., Ulrych, T. & Sacchi, M. (2002). Accurate interpolation with high-resolution time-variant Radon transforms (the sparse/LS outlook of §7.3). `wiki/sources/trad2002_radon_interpolation.md`
