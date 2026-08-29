# Kramers–Kronig Relations and Velocity Dispersion: A Step-by-Step Derivation

This document derives, step by step, why absorption of seismic waves **must**
be accompanied by velocity dispersion, and where the two classical dispersion
laws — Futterman's logarithmic law and Kjartansson's power law — come from.
It is supplementary reading for Term 2 Lecture 01 (Absorption and
Q-compensation).

> **Prerequisites.** The Fourier transform, convolution, and the concept of an
> impulse response (Term 1 Lecture 05). No complex analysis is required for
> the main line of the proof — only one Fourier integral evaluated by hand.

---

## 1. The claim: absorption without dispersion is physically impossible

Suppose a magic medium absorbed high frequencies but treated all frequencies
as equally fast. Its propagation filter would have an amplitude response like
$e^{-\alpha(\omega) x}$ with $\alpha$ growing in frequency — and a phase
response of exactly zero at every frequency.

A zero phase at all frequencies means an impulse response that is **symmetric
about $t = 0$**: it starts ringing *before* the input impulse arrives. Such a
system responds before it is excited. It is **acausal** — and physical wave
propagation cannot work that way.

The rigorous statement of this intuition is the **Kramers–Kronig (KK)
relations**: for any linear, time-invariant, *causal* system, the real and
imaginary parts of the frequency response are not independent — each is the
Hilbert transform of the other. Applied to wave propagation, this means:

> **The attenuation law $\alpha(\omega)$ uniquely determines the dispersion
> law $v(\omega)$.** You may choose the attenuation, but then the dispersion
> is no longer yours to choose.

We prove this in Sections 2–5 (following Schönleber, 2014), then apply it to
rocks (Sections 6–9, following Futterman, 1962, and Kjartansson, 1979).

---

## 2. Linear time-invariant systems in one page

A linear time-invariant (LTI) system is fully described by its **impulse
response** $h(t)$: the output produced by a unit impulse $\delta(t)$ at the
input. Any input $x(t)$ is decomposed into shifted impulses, and by linearity
the output is the **convolution**

$$
y(t) = (x * h)(t) = \int_{-\infty}^{\infty} x(\tau)\, h(t - \tau)\, d\tau .
$$

Throughout this document we use the Fourier transform pair

$$
H(\omega) = \int_{-\infty}^{\infty} h(t)\, e^{-i\omega t}\, dt,
\qquad
h(t) = \frac{1}{2\pi} \int_{-\infty}^{\infty} H(\omega)\, e^{+i\omega t}\, d\omega .
$$

With this convention, two facts we will need:

1. **Convolution theorem (time):** $y = x * h$ transforms into a product:
   $Y(\omega) = X(\omega)\,H(\omega)$. This is why $H(\omega)$ is called the
   *frequency response*.
2. **Convolution theorem (frequency):** a *product* in the time domain
   transforms into a convolution in the frequency domain (divided by
   $2\pi$):

$$
\mathcal{F}\{f(t)\,g(t)\}(\omega) = \frac{1}{2\pi}\int_{-\infty}^{\infty} F(\omega')\, G(\omega - \omega')\, d\omega' .
\tag{2.1}
$$

Fact 2 is the standard dual of the convolution theorem; it follows by
expanding $f$ and $g$ in inverse transforms and integrating over $t$.

---

## 3. Causality in the time domain

The system is **causal** if the output never precedes the input:

$$
h(t) = 0 \qquad \text{for all } t < 0 .
$$

Introduce the Heaviside step function

$$
\sigma(t) = \begin{cases} 0, & t < 0 \\ 1, & t > 0 \end{cases}
$$

Then causality is exactly the statement that $h$ may be written as a product:

$$
h(t) = \sigma(t)\, h(t) \qquad \text{(causality)} .
\tag{3.1}
$$

This trivial-looking rewrite is the whole trick: we now have a *product in
the time domain*, and the frequency-domain convolution theorem (2.1) applies.

---

## 4. The Fourier transform of the step function

To use (2.1) we need $\Sigma(\omega) = \mathcal{F}\{\sigma(t)\}$. The step
function is not absolutely integrable, so we regularize it as
$\sigma(t) = \lim_{\varepsilon \to 0} e^{-\varepsilon t}\,\sigma(t)$ and
compute:

$$
\int_0^{\infty} e^{-\varepsilon t} e^{-i\omega t}\, dt
= \frac{1}{\varepsilon + i\omega}
= \frac{\varepsilon}{\varepsilon^2 + \omega^2} \;-\; i\,\frac{\omega}{\varepsilon^2 + \omega^2}.
$$

Now let $\varepsilon \to 0$ term by term:

- The first term is a **nascent delta function**: it is sharply peaked at
  $\omega = 0$ with total integral $\pi$ (check: substitute $\omega = \varepsilon u$).
  So $\dfrac{\varepsilon}{\varepsilon^2+\omega^2} \to \pi\,\delta(\omega)$.
- The second term simply loses $\varepsilon$:
  $\dfrac{\omega}{\varepsilon^2 + \omega^2} \to \dfrac{1}{\omega}$, to be
  understood as a **principal value** $P$ (the integral through the pole at
  $\omega = 0$ is taken symmetrically).

The result:

$$
\boxed{\;\Sigma(\omega) = \pi\,\delta(\omega) \;+\; P\,\frac{1}{i\omega}\;}
\tag{4.1}
$$

The step function is "half a constant plus a switch", and its spectrum
shows exactly that: a delta (the DC half) plus a slowly decaying $1/\omega$
tail (the infinitely sharp switch).

---

## 5. Deriving the Kramers–Kronig relations

Transform both sides of the causality statement (3.1) and apply the
product-convolution theorem (2.1):

$$
H(\omega) = \frac{1}{2\pi} \int_{-\infty}^{\infty} \Sigma(\omega')\, H(\omega - \omega')\, d\omega' .
$$

Insert (4.1). The delta term collapses trivially:

$$
H(\omega) = \frac{1}{2} H(\omega) \;+\; \frac{1}{2\pi i}\, P\!\!\int_{-\infty}^{\infty} \frac{H(\omega - \omega')}{\omega'}\, d\omega' .
$$

Substitute $u = \omega - \omega'$ in the integral (so $\omega' = \omega - u$,
and the limits swap and cancel the minus sign of $d\omega' = -du$):

$$
H(\omega) = \frac{1}{2} H(\omega) \;+\; \frac{1}{2\pi i}\, P\!\!\int_{-\infty}^{\infty} \frac{H(u)}{\omega - u}\, du ,
$$

hence

$$
H(\omega) = \frac{1}{\pi i}\, P\!\!\int_{-\infty}^{\infty} \frac{H(u)}{\omega - u}\, du .
\tag{5.1}
$$

Equation (5.1) already says it all: **$H$ is reconstructed from itself** —
its values cannot be arbitrary. To see the usual form, write
$H = R + iI$ with $R = \operatorname{Re}H$, $I = \operatorname{Im}H$, multiply
(5.1) by $i$, and equate real and imaginary parts. The result is the pair of
**Kramers–Kronig relations**:

$$
\boxed{\;
R(\omega) = -\frac{1}{\pi}\, P\!\!\int_{-\infty}^{\infty} \frac{I(u)}{u - \omega}\, du,
\qquad
I(\omega) = \frac{1}{\pi}\, P\!\!\int_{-\infty}^{\infty} \frac{R(u)}{u - \omega}\, du .
\;}
\tag{5.2}
$$

The two operations on the right are called the **Hilbert transform**. In
words: *the attenuation (real part, for a propagation filter) and the phase
(imaginary part) are Hilbert-transform duals — two views of a single causal
response.*

> **Sanity check (recommended).** Test (5.2) on the causal exponential
> $h(t) = e^{-t}\sigma(t)$, for which
> $H(\omega) = \frac{1}{1+i\omega} = \frac{1}{1+\omega^2} - i\,\frac{\omega}{1+\omega^2}$.
> Splitting $\int \frac{-u}{(1+u^2)(u-\omega)} du$ into partial fractions and
> using $P\!\int \frac{du}{u - \omega} = 0$, $\int \frac{du}{1+u^2} = \pi$
> reproduces exactly $R(\omega) = \frac{1}{1+\omega^2}$ from $I$, and
> $I(\omega)$ from $R$. Doing this once by hand removes all mystery from the
> relations.

> **For the curious (no exam material).** The same result has an elegant
> complex-analysis proof: causality makes $H(z)$ an *analytic* function of
> complex frequency $z$ in the upper half-plane $\operatorname{Im} z > 0$
> (the inverse transform then only ever uses $e^{+izt}$, which decays
> there). Closing the contour around the pole at $z = \omega$ in Cauchy's
> integral formula yields (5.2). This is the route of classical optics
> texts; the system-theory route above needs no contour integration.

---

## 6. From the theorem to rocks: the propagation filter

A plane wave travelling in the $+x$ direction through an absorbing medium is
written (Futterman, 1962)

$$
u(x, t) = u_0\, e^{i K(\omega) x}\, e^{-i\omega t},
\qquad
K(\omega) = k(\omega) + i\,\alpha(\omega),
$$

so that the amplitude decays as $e^{-\alpha x}$ with the **absorption
coefficient** $\alpha > 0$, and the phase advances as $e^{ikx}$ with
wavenumber $k = \omega / v(\omega)$. Propagation over distance $x$ is an LTI
filter with frequency response

$$
H_x(\omega) = e^{i K(\omega) x} = \underbrace{e^{-\alpha(\omega) x}}_{\text{attenuation}} \cdot \underbrace{e^{i k(\omega) x}}_{\text{phase}} .
$$

Seismic propagation is linear and causal to an excellent approximation, so
the KK relations (5.2) apply to $H_x$ — with one technical refinement.
Following Futterman, it is cleaner to work with the **(complex) index of
refraction**

$$
n(\omega) = \frac{K(\omega)}{\omega / v_0} = \frac{v_0}{v(\omega)} + i\,\frac{v_0\, \alpha(\omega)}{\omega},
\tag{6.1}
$$

where $v_0$ is a fixed reference velocity (the nondispersive low-frequency
limit in Futterman's construction). The imaginary part of $n$ is proportional
to $\alpha/\omega$ — the loss *per radian of phase* — and its real part is
the reciprocal phase velocity. KK then links the two halves of $n$.

> **A note on sign conventions.** Whether the absorptive part of a response
> enters the imaginary part with a plus or a minus depends on whether one
> synthesizes signals with $e^{+i\omega t}$ or $e^{-i\omega t}$; both
> conventions appear in the literature. The physics does not depend on it.
> Below we follow Futterman's bookkeeping (absorption in
> $\operatorname{Im} n > 0$), and the consistency check in Section 7.1
> verifies that the resulting dispersion has the physically required sign.

Two facts make the seismic application concrete:

- **Small-loss definition of Q.** The energy lost per cycle defines
  $Q^{-1} = \Delta E / (2\pi E)$. Working through the energy of a damped
  standing wave or a propagating train (Futterman's Section on Q) gives

$$
\frac{1}{Q(\omega)} \approx \frac{2\, \alpha(\omega)\, v(\omega)}{\omega},
\qquad \text{hence} \qquad
\alpha(\omega) \approx \frac{\omega}{2 Q\, v(\omega)} .
\tag{6.2}
$$

  For weak absorption $Q \approx k/(2\alpha)$, and the reduced quality
  factor $Q_0 = \omega / (2\alpha v_0)$ obeys
  $\operatorname{Im} n = 1/(2Q_0)$ exactly. (Equation (6.2) is the
  approximate relation valid for small $1/Q$; the exact bookkeeping is a
  remark at the end of Section 8.)

- **Near-constant Q.** Laboratory and field data show the loss per cycle is
  roughly frequency-independent: $Q \approx \text{const}$, so from (6.2)
  $\alpha(\omega) \propto \omega$ — absorption linear in frequency. This is
  assumption (a) of Futterman's paper, and it makes
  $\operatorname{Im} n = 1/(2Q_0)$ a constant over the seismic band.

---

## 7. Futterman's dispersion equation

### 7.1 Doing the KK integral

Take the simplest causal absorption model that respects the data:
**no absorption below a cutoff frequency $\omega_0$, constant
$\operatorname{Im} n = 1/(2Q_0)$ above it**. In the dimensionless variable
$x = \omega / \omega_0$:

$$
\operatorname{Im} n(x) = \begin{cases} 0, & x < 1 \\ \dfrac{1}{2Q_0}, & x > 1 \end{cases}
$$

For a real-valued response, $n$ obeys the crossing symmetry
$n(-x) = n^*(x)$; reducing the KK relations (5.2) to positive frequencies
for the index, and subtracting the no-dispersion reference (the careful
derivation is in Futterman's Appendix), gives his **dispersion equation**:

$$
\operatorname{Re} n(x) - 1 = \frac{2}{\pi}\, P\!\!\int_0^{\infty} \frac{u\, \operatorname{Im} n(u)}{u^2 - x^2}\, du .
\tag{7.1}
$$

Because our $\operatorname{Im} n$ never dies out, this integral diverges at
its upper end unless we also cap the absorption at some very high frequency
$x_c$ (physically: at molecular scales materials stop absorbing; the exact
form of that cap is irrelevant — watch what happens). With the cap:

$$
\operatorname{Re} n(x) - 1 = \frac{1}{\pi Q_0} P\!\!\int_{1}^{x_c} \frac{u}{u^2 - x^2}\, du
= \frac{1}{2\pi Q_0}\, \ln \left| \frac{x_c^2 - x^2}{1 - x^2} \right| .
\tag{7.2}
$$

In the seismic band — far above the low cutoff and far below the high one,
$1 \ll x \ll x_c$ — this simplifies beautifully:

$$
\operatorname{Re} n(x) - 1 \approx \frac{1}{\pi Q_0}\, \ln \frac{x_c}{x}
\;\;\Longrightarrow\;\;
\frac{v_0}{v(\omega)} \approx \text{const} - \frac{1}{\pi Q_0}\, \ln \frac{\omega}{\omega_0} .
$$

Absorbing the constant (it only redefines the velocity scale) gives
**Futterman's logarithmic dispersion law**:

$$
\boxed{\;
\frac{1}{v(\omega)} = \frac{1}{v_0}\left[ 1 - \frac{1}{\pi Q}\, \ln\frac{\omega}{\omega_0} \right]
\qquad (\omega \gg \omega_0)
\;}
\tag{7.3}
$$

Read it carefully: $1/v$ is *linear in $\ln\omega$*. Higher frequencies have
smaller slowness — **higher frequencies travel faster**, by an amount
proportional to $1/Q$ and to the logarithm of the frequency ratio.

> **Consistency check (the sign of dispersion).** Physically, absorption is
> present at *every* frequency above the cutoff — the seismic band sits
> inside the absorption band, not below it. Media whose absorption lies
> entirely *above* the band of interest show normal dispersion (velocity
> decreasing with frequency, like glass for visible light). Inside an
> absorption band the KK machinery forces the opposite, *anomalous*
> behaviour — and that is exactly what (7.3) delivers: higher frequencies
> faster. The sign of the law is not an arbitrary choice; it is the only
> causal possibility.

### 7.2 Why a cutoff is mandatory

Look at the denominator in (7.2). If we had let the constant-loss band extend
all the way down to $\omega = 0$ (replacing the lower limit 1 by 0), the
denominator $|1 - x^2|$ would become $x^2$, and

$$
\operatorname{Re} n(x) \sim \ln \frac{1}{x} \to \infty
\qquad \text{as } \omega \to 0 :
$$

the slowness would diverge at low frequency — the medium would be
infinitely slow at DC, and no finite nondispersive limit $v_0$ would exist.
Futterman's conclusion: a **finite low-frequency cutoff $\omega_0 \neq 0$ is
required** by causality itself (it may be arbitrarily small — Futterman
suggests values like $10^{-8}\,\mathrm{s}^{-1}$, far below any measurement).
Because dispersion depends on $\omega$ only *logarithmically*, the answer in
the measured band is insensitive to where exactly the cutoffs sit. This is a
gift: the law (7.3) is robust even though the cutoff is phenomenological.

### 7.3 The velocity ratio (the form used in processing)

Absolute velocities require knowing $v_0$ and $\omega_0$; practice always
uses **ratios anchored at a reference frequency** $\omega_r$. From (7.3):

$$
\boxed{\;
\frac{v(\omega)}{v(\omega_r)} = \frac{1 - \frac{1}{\pi Q}\ln\frac{\omega_r}{\omega_0}}{1 - \frac{1}{\pi Q}\ln\frac{\omega}{\omega_0}}
\;\;\approx\;\;
1 + \frac{1}{\pi Q}\, \ln\frac{\omega}{\omega_r}
\;}
\tag{7.4}
$$

where the approximation holds for $\frac{1}{\pi Q}\ln(\cdot) \ll 1$
(excellent for $Q \gtrsim 20$). Equation (7.4) is the "Futterman velocity
ratio" offered by Q-compensation software. Note what the reference frequency
does: it is the **anchor** — frequencies above $\omega_r$ arrive earlier
than a nondispersive medium would deliver them, frequencies below arrive
later. Choosing $\omega_r$ means choosing *which frequency keeps its
traveltime* — the practical knob behind well-tie and 4D consistency.

---

## 8. Kjartansson's exact constant-Q law

Futterman's law is "nearly constant Q" above a cutoff. Kjartansson (1979)
asked: can a medium have *exactly* constant Q at **all** frequencies,
causally, with no cutoff? Yes — at the price of a power law instead of a
logarithm.

### 8.1 The power-law construction

Loss per cycle independent of frequency means the material has **no
characteristic time scale**: its response to a step load (the creep
function) must be a pure power of time, $\psi(t) \propto t^{2\gamma}$ — a
straight line on log-log paper at every scale. (Exponential creep
$e^{-at}$ of the Voigt solid, by contrast, has the time scale $1/a$, and
delivers $Q \propto \omega$ — wrong for rocks; this is the Ricker family of
models.) Fourier-transforming the creep gives a complex modulus

$$
M(\omega) = M_0 \left( \frac{i\omega}{\omega_0} \right)^{2\gamma},
\qquad 0 < \gamma < \tfrac{1}{2},
$$

whose **argument** $\gamma\pi$ is the same at every frequency: stress lags
strain by a constant angle, and since the loss tangent *is* that angle's
tangent, Q is exactly frequency-independent:

$$
\frac{1}{Q} = \tan(\pi\gamma)
\qquad\Longleftrightarrow\qquad
\gamma = \frac{1}{\pi} \arctan \frac{1}{Q} \approx \frac{1}{\pi Q}.
\tag{8.1}
$$

Inserting $M(\omega)$ into the 1-D wave equation, the wavenumber takes the
power-law form

$$
K(\omega) = \frac{\omega}{\tilde v(\omega)}\, e^{i\pi\gamma/2},
\qquad
\tilde v(\omega) = \sqrt{\frac{M_0}{\rho}}\left( \frac{\omega}{\omega_0} \right)^{\gamma},
$$

with $\rho$ the density (the sign of the constant phase is set by the
propagation convention so that amplitudes decay). The essential feature is
the **constant phase angle** $\pi\gamma/2$: real and imaginary parts of $K$
are in a fixed ratio at every frequency. Reading them off,
$k = (\omega/\tilde v)\cos(\pi\gamma/2)$ and
$\alpha = (\omega/\tilde v)\sin(\pi\gamma/2)$. The cosine is
frequency-*independent*, so we absorb it into the velocity scale and define the
phase velocity $v(\omega) = \tilde v(\omega)/\cos(\pi\gamma/2)$, with
$v_0 = \sqrt{M_0/\rho}/\cos(\pi\gamma/2)$ — Kjartansson's normalization.
Then $k = \omega/v(\omega)$ exactly, and the complete causal pair becomes

$$
\boxed{\;
v(\omega) = v_0 \left( \frac{\omega}{\omega_0} \right)^{\gamma},
\qquad
\alpha(\omega) = \tan\!\left( \frac{\pi\gamma}{2} \right) \frac{\omega}{v(\omega)} \approx \frac{\omega}{2Q\,v(\omega)} .
\;}
\tag{8.2}
$$

**Exactly constant Q, attenuation nearly proportional to frequency, and
dispersion as a power law** — the whole propagation specified by two
parameters $(Q, v_0)$. The approximation
$\tan(\pi\gamma/2) \approx \pi\gamma/2 \approx 1/(2Q)$ (valid to better than
0.5% for $Q \ge 10$) recovers the familiar amplitude law used in Sections 6
and 7; use the identity
$\tan(\theta/2) = \sin\theta/(1+\cos\theta)$ with $\theta = \arctan(1/Q)$ to
check it.

> **Remark (definitions of Q, honestly).** The loss-angle definition
> $Q^{-1} = \tan(\pi\gamma)$ and the spatial-decay definition
> $2\alpha v/\omega = 2\tan(\pi\gamma/2)$ differ slightly; they agree to
> first order in $1/Q$ (and Futterman states his $Q \approx k/2\alpha$ is
> "strictly approximate"). For $Q \ge 20$ the difference is far below
> measurement error — which is why textbooks (and processing software)
> freely mix them. Just don't be surprised when two papers' "exact"
> constant-Q formulas differ by terms of order $1/Q^3$.

### 8.2 Why no cutoff is needed here

The power law is self-similar: no frequency is special, so nothing diverges
and no band edge must be declared. The price is that the medium has
*infinite* memory (creep at all time scales) — acceptable as a
phenomenological description over any finite band, and exactly why
Kjartansson's law has become the standard in theoretical work and in
wave-equation Q-compensation.

### 8.3 The two laws are the same law (to first order)

Expand the power law for small $\gamma$:

$$
\left( \frac{\omega}{\omega_r} \right)^{\gamma} = e^{\gamma \ln(\omega/\omega_r)} \approx 1 + \gamma \ln\frac{\omega}{\omega_r} + O(\gamma^2).
$$

With $\gamma \approx 1/(\pi Q)$ this is *exactly* the approximate Futterman
ratio (7.4). For $Q \gtrsim 30$ the two dispersion laws differ by fractions
of a percent across the seismic band — the choice between them in software
is a matter of convenience, **not** of physics. What matters physically is
that both are *causally consistent pairs*: amplitude and phase linked, as
the KK relations demand.

---

## 9. How big is dispersion in real numbers?

Everything above is proportional to $\frac{1}{\pi Q}\ln(\cdot)$, so one
worked example fixes the intuition. Take $Q = 50$ (a consolidated sediment),
so $1/(\pi Q) = 6.37 \times 10^{-3}$:

| Quantity | Value |
|---|---|
| Velocity change per frequency decade, $\Delta v / v$ | $\frac{1}{\pi Q}\ln 10 \approx 1.5\%$ |
| Velocity change from 10 Hz to 100 Hz ($\omega_r$ = 100 Hz) | $\approx 1.5\%$ (fast at high $f$) |
| Delay of the 10 Hz component relative to 100 Hz at $t_0 = 2$ s | $t_0 \cdot \frac{1}{\pi Q}\ln 10 \approx 29$ ms |
| Same delay for $Q = 200$ | $\approx 7$ ms |

A 10–30 ms frequency-dependent stretch of the wavelet is *exactly* the
"delay of the low frequencies" seen on real data — it is not a static shift
(it varies with frequency) and not a wavelet-shape effect you can absorb
into a time shift: it must be undone frequency by frequency. That is what
the **phase part** of inverse Q filtering does, and why that phase operator
(a pure per-frequency time shift) is unconditionally stable while the
amplitude part (an exponential boost) is not — the subject of the lecture.

Consequences worth remembering:

- **Well ties and 4D.** Check-shot times (high-frequency content) and
  surface-seismic times (lower frequencies) probe different points of the
  dispersion curve; mismatches of a few ms are expected, not mysterious.
- **Velocity analysis.** Picked stacking velocities correspond to the
  dominant-frequency content of the data; absorption shifts them
  systematically (an *apparent* velocity effect on top of the geological
  one).
- **Resolution.** The stretched, delayed low-frequency tail is part of why
  deep wavelets are long: dispersion smears them even where amplitudes
  survive.

---

## 10. Summary

| Step | Result |
|---|---|
| Causality: $h(t) = \sigma(t)h(t)$ | product in time (3.1) |
| $\mathcal{F}\{\sigma\} = \pi\delta(\omega) + P\frac{1}{i\omega}$ | step spectrum (4.1) |
| Product $\to$ convolution in frequency | master relation (5.1) |
| Split into real/imaginary parts | **KK relations** (5.2): attenuation and phase are Hilbert duals |
| Apply to propagation constant, $\operatorname{Im} n = 1/(2Q_0)$ above cutoff $\omega_0$ | logarithmic law: $\frac{1}{v} \propto 1 - \frac{1}{\pi Q}\ln\frac{\omega}{\omega_0}$ (7.3) |
| Cutoff required: else $\operatorname{Re}n \to \infty$ as $\omega \to 0$ | Futterman's $\omega_0 \neq 0$; insensitivity via the log |
| Power-law (scale-free) modulus $M \propto (i\omega)^{2\gamma}$ | Kjartansson: $\frac{v}{v_r} = (\omega/\omega_r)^\gamma$, $\frac{1}{Q} = \tan\pi\gamma$, exactly constant Q, no cutoff (8.1–8.2) |
| Small-$\gamma$ expansion | power law $\equiv$ logarithmic law to $O(1/Q)$ |
| Magnitude | $\sim 1.5\%$ per decade for Q = 50 → 10–30 ms wavelet stretch |

---

## 11. Self-check questions

1. Compute $\Sigma(\omega)$ yourself from
   $\int_0^\infty e^{-(\varepsilon + i\omega)t} dt$ and confirm (4.1),
   including the $\pi$ in front of the delta (hint: nascent delta).
2. Carry out the partial-fractions sanity check of Section 5 on
   $h(t) = e^{-2t}\sigma(t)$ (the numbers change, the structure does not).
3. From (7.3), derive the exact velocity ratio (7.4) and verify that the
   linearized form reproduces Kjartansson's power law to first order in
   $\gamma$.
4. Show $\tan(\pi\gamma/2) \approx 1/(2Q)$ when $\gamma = \arctan(1/Q)/\pi$,
   using the half-angle identity. Up to which $Q$-value is the 1% error
   barrier crossed?
5. A processor claims: "I applied a zero-phase bandpass filter — that's my
   absorption model; it's fine because it only changes amplitudes." What is
   wrong with this as a *propagation* model, and what would the recorded
   data look like near the first break?
6. Why is the choice of reference frequency a *processing decision* rather
   than physics, and which two applications from Section 9 does it most
   directly affect?

---

## References

- Schönleber, M. (2014). A simple derivation of the Kramers–Kronig relations
  from the perspective of system theory. *American Journal of Physics*.
  `wiki/sources/schonleber_2014_kk_system_theory.md`
- Futterman, W. I. (1962). Dispersive body waves. *Journal of Geophysical
  Research*, 67, 5279–5291.
  `wiki/sources/futterman_1962_dispersive_body_waves.md`
- Kjartansson, E. (1979). Constant Q-wave propagation and attenuation.
  *Journal of Geophysical Research*, 84, 4737–4748.
  `wiki/sources/kjartansson_1979_constant_q.md`
- Wang, Y. (2002, 2006). Stable inverse Q filtering; inverse Q-filter for
  seismic resolution enhancement. *Geophysics*.
  `wiki/sources/wang_2002_stable_inverse_q.md`,
  `wiki/sources/wang_2006_inverse_q_resolution.md`
