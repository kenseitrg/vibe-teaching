# Prediction-Error Filter via the Z-Transform

This note shows how the **prediction-error filter** (PEF) arises from the
predictive deconvolution setup, and why the Z-transform gives an intuitive
picture of what the filter does. It assumes familiarity with the Wiener filter
derivation.

---

## 1. Predictive deconvolution setup

We have a trace $x[n]$ that contains a primary reflection followed by
reverberations (e.g., water-layer multiples) with a period of $\alpha$
samples.  The idea of predictive deconvolution is:

> Use the past $N$ samples of $x$ to **predict** the sample $\alpha$ steps
> ahead.  Subtract the prediction from the actual value; what remains is the
> **unpredictable** part — the primary.

Concretely, let $h[k],\ k=0,\dots,N-1$ be the coefficients of a prediction
filter that minimises the squared error

$$
\varepsilon = \sum_n \bigl( x[n+\alpha] - \sum_{k=0}^{N-1} h[k]\, x[n-k] \bigr)^2.
$$

The predicted value $\hat{x}[n+\alpha]$ is

$$
\hat{x}[n+\alpha] = \sum_{k=0}^{N-1} h[k]\, x[n-k].
$$

---

## 2. The prediction-error filter

The **prediction error** at time $n+\alpha$ is

$$
e[n+\alpha] = x[n+\alpha] - \hat{x}[n+\alpha]
            = x[n+\alpha] - \sum_{k=0}^{N-1} h[k]\, x[n-k].
$$

It is more convenient to re-index so that the output is aligned with the input
at the same time index.  Replace $n$ by $n-\alpha$:

$$
e[n] = x[n] - \sum_{k=0}^{N-1} h[k]\, x[n-\alpha-k].
$$

This is a **convolution** of $x[n]$ with the **prediction-error filter**

$$
\boxed{\;
f[n] = \delta[n] - \sum_{k=0}^{N-1} h[k]\, \delta[n-\alpha-k].
\;}
$$

Explicitly, the coefficients are

$$
f = \bigl[\, 1,\; \underbrace{0,\ \dots,\ 0}_{\alpha-1\text{ zeros}},\;
       -h[0],\; -h[1],\; \dots,\; -h[N-1]\, \bigr].
$$

The output $y[n] = (x * f)[n]$ is the deconvolved trace.

---

## 3. Z-transform picture

Take the Z-transform of the PEF:

$$
\begin{aligned}
F(z) &= 1 \;-\; h[0]\, z^{-\alpha} \;-\; h[1]\, z^{-\alpha-1}
      \;-\; \dots \;-\; h[N-1]\, z^{-\alpha-N+1} \\[4pt]
     &= 1 \;-\; z^{-\alpha}
        \bigl( h[0] + h[1]\, z^{-1} + \dots + h[N-1]\, z^{-N+1} \bigr) \\[4pt]
     &= 1 \;-\; z^{-\alpha}\, H(z),
\end{aligned}
$$

where $H(z) = \sum_{k=0}^{N-1} h[k]\, z^{-k}$ is the Z-transform of the
prediction filter.

The deconvolved trace in the Z-domain is therefore

$$
Y(z) = F(z)\, X(z) = \bigl(1 - z^{-\alpha} H(z)\bigr)\, X(z).
$$

---

## 4. What this means intuitively

### 4.1  A predictable component is removed

If the trace $x[n]$ contains a component that repeats every $\alpha$ samples,
that component is **predictable** from the past.  The optimal filter $H(z)$
learns the repetition operator, and $z^{-\alpha} H(z)$ approximates it.
Subtracting it from $X(z)$ removes the predictable energy.

**Example — a single water-layer multiple.**  The trace can be modelled as

$$
x[n] = p[n] + c\, p[n-\alpha] + c^2 p[n-2\alpha] + \cdots,
$$

where $p[n]$ contains the primaries and $c$ is the water-bottom reflection
coefficient.  In the Z-domain:

$$
X(z) = \frac{P(z)}{1 + c\, z^{-\alpha}}.
$$

A single-coefficient prediction filter $H(z) = -c$ gives $F(z) = 1 + c\,z^{-\alpha}$,
which exactly cancels the denominator:

$$
Y(z) = (1 + c\,z^{-\alpha})\, X(z) = P(z).
$$

The reverberations are removed and the primaries are recovered.

---

### 4.2  Gap $\boldsymbol{\alpha = 1}$ — spiking deconvolution

When $\alpha = 1$, the PEF predicts **one sample ahead**.  This is the
spiking deconvolution case.

#### Time-domain coefficients

With $\alpha = 1$, there are no gap zeros — the PEF coefficients are

$$
f = [\, 1,\; -h[0],\; -h[1],\; \dots,\; -h[N-1]\,].
$$

This is exactly the structure of a standard **Wiener spiking operator**
obtained from the normal equations

$$
\sum_{k=0}^{N} f[k]\, \phi_{xx}[j-k] = \delta_{j,0}\,\phi_{xx}[0],
\qquad j = 0, \dots, N.
$$

For $\alpha = 1$, the right-hand side of the prediction-filter normal
equations is $\phi_{xx}[j+1]$, and the resulting PEF satisfies
the same equations as the spiking operator — both produce a filter that
**whitens** the data.

#### Z-transform form

$$
F(z) = 1 - z^{-1} H(z).
$$

where $H(z) = h[0] + h[1] z^{-1} + \dots + h[N-1] z^{-N+1}$.

#### Why it compresses the wavelet

Consider a trace that is a pure minimum-phase wavelet (ignoring reflectivity
and noise for clarity): $x[n] = w[n]$, with $W(z)$ having all zeros inside
the unit circle.  The one-step-ahead prediction filter learns to predict
$w[n+1]$ from $w[n], w[n-1], \dots$, i.e., it learns the wavelet's internal
structure.  Subtracting this prediction leaves only the unpredictable
innovation — a spike at time zero.

Concretely, for a minimum-phase $W(z)$, the wavelet can be written as the
output of a causal, stable **innovation filter** driven by a spike:
$W(z) = 1 / A(z)$, where $A(z) = 1 - z^{-1} \tilde{H}(z)$ is monic and
minimum-phase.  The PEF $F(z) = 1 - z^{-1} H(z)$ learns $A(z)$, giving

$$
Y(z) = F(z) X(z) \approx A(z) \cdot \frac{1}{A(z)} R(z) = R(z),
$$

where $R(z)$ is the reflectivity.  The wavelet is compressed to a spike and
the reflectivity sequence is recovered.

#### Worked example — minimum-phase dipole

Take the simplest minimum-phase wavelet: a dipole $w = (a, b)$ with $a > b > 0$.
Its Z-transform (standard convention) is

$$
W(z) = a + b\,z^{-1}.
$$

The trace is the wavelet itself: $X(z) = W(z)$.  The one-step prediction
filter $H(z)$ solves

$$
\varepsilon = \sum_n \bigl( x[n+1] - h[0]\, x[n] \bigr)^2.
$$

Because the wavelet is deterministic and minimum-phase, $h[0] = b/a$
perfectly predicts the next sample.  The PEF is

$$
F(z) = 1 - z^{-1} \cdot \frac{b}{a} = 1 - \frac{b}{a}\,z^{-1}.
$$

Applying it:

$$
Y(z) = F(z) W(z) = \left(1 - \frac{b}{a}\,z^{-1}\right) (a + b\,z^{-1})
      = a + b\,z^{-1} - b\,z^{-1} - \frac{b^2}{a}\,z^{-2}
      = a - \frac{b^2}{a}\,z^{-2}.
$$

The output is approximately a spike at $n=0$ followed by a small residual
at $n=2$ (amplitude $-b^2/a$, which is small when $b \ll a$).  A longer
filter would drive this residual to zero.

#### Summary for $\alpha = 1$

The PEF with unit gap:
- Has no zero gap, so its coefficients directly form the spiking operator.
- Learns the inverse of a minimum-phase wavelet from the data.
- Compresses the wavelet to a spike, recovering the reflectivity.
- Is equivalent to the standard Wiener spiking deconvolution filter.

---

### 4.3  Gap $\boldsymbol{\alpha > 1}$ — reverberation suppression

When $\alpha$ is larger than the wavelet duration, the filter cannot predict
the wavelet itself (it has already decayed within $\alpha$ samples).  What it
can predict is the reverberation tail that arrives exactly $\alpha$ samples
after the primary.

In the Z-domain, $F(z) = 1 - z^{-\alpha} H(z)$:
- The $1$ passes the primary wavelet unchanged.
- The $-z^{-\alpha} H(z)$ subtracts the predicted reverberation.

The result is a trace that retains the primary wavelet shape but has the
reverberation suppressed.

---

### 4.4  Frequency-domain interpretation

On the unit circle $z = e^{i\omega\Delta t}$, the PEF becomes

$$
F(\omega) = 1 - e^{-i\omega\alpha\Delta t}\, H(\omega).
$$

When $\alpha$ equals the reverberation period, the PEF creates **notches** at
the reverberation frequencies $f_k = k / (\alpha\Delta t),\ k = 0, 1, 2, \dots$
— exactly the frequencies that are amplified by the water-layer resonance.

---

## 5. Summary

| Concept | Z-domain | Time-domain effect |
|---|---|---|
| Prediction filter | $H(z) = \sum_{k} h[k] z^{-k}$ | Predicts $x[n+\alpha]$ from past samples |
| Prediction-error filter | $F(z) = 1 - z^{-\alpha} H(z)$ | Removes predictable component at lag $\alpha$ |
| Gap $\alpha = 1$ | $F(z) \approx 1/W(z)$ | Compresses wavelet to a spike |
| Gap $\alpha >$ wavelet length | $F(z)$ leaves $1$ for primary | Suppresses reverberations; preserves wavelet |
| Single multiple | $F(z) = 1 + c\,z^{-\alpha}$ | Cancels a periodic repetition |

The key insight is that **the same filter structure** — a unit coefficient
at lag 0, a gap of $\alpha$ zeros, and a prediction tail — controls whether
the deconvolution compresses the wavelet or targets the reverberation, simply
by changing $\alpha$.

---

## 6. Relationship to the Wiener filter derivation

The prediction coefficients $h[k]$ are found by solving the Wiener-Hopf
equations with the right-hand side $\phi_{dx}[j] = \phi_{xx}[j+\alpha]$ (see
§12 of the [Wiener filter derivation](wiener_deconvolution_derivation.en.md)).
The PEF is assembled from $h[k]$ as $f = [1, 0_{1\times\alpha-1}, -h]$, and
applied via convolution.
