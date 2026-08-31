---
title: "Term 1, Lecture 6 — Single-channel deconvolution"
author: "Seismic Data Processing Course"
date: "2026"
---

# Term 1, Lecture 6 — Single-channel deconvolution

## Learning objectives

After this lecture you should be able to:

1. State the convolutional model of a seismic trace and identify the main components of the embedded wavelet.
2. Explain why deconvolution is used and what it cannot recover.
3. Define minimum-phase, maximum-phase, zero-phase, and causal wavelets, and prove the front-loading property for a dipole.
4. Design a deterministic deconvolution operator in the Fourier and $z$-domains, including prewhitening.
5. Derive the Wiener-Hopf equations from a least-squares criterion and explain each statistical-deconvolution assumption.
6. Distinguish spiking deconvolution from predictive deconvolution by their parameters.

---

## 1. What is deconvolution trying to do?

The ultimate goal of reflection seismology is to map the earth's reflectivity — the sequence of reflection coefficients at layer boundaries — as a function of position. In practice we can never recover a truly broadband reflectivity series, because seismic sources do not emit useful energy at all frequencies and the earth attenuates high frequencies. The realistic target is **band-limited reflectivity**: the true reflectivity convolved with a short, zero-phase wavelet.

A raw seismic trace, however, is not band-limited reflectivity. It is the reflectivity convolved with a much longer **embedded wavelet** that contains the source signature, ghosts, bubble energy, instrument response, and near-surface filtering. Deconvolution is the family of processes that tries to undo this convolution.

In a single sentence:

> **Deconvolution removes or reshapes the embedded wavelet so that the trace better represents the earth's reflectivity.**

What deconvolution can do:

- Compress the wavelet (improve temporal resolution).
- Remove predictable repetitive energy such as reverberations and short-period multiples.
- Convert data to a desired phase, most commonly minimum phase or zero phase.
- Remove a known source signature or instrument response.

What deconvolution cannot do:

- Recover frequencies that were never recorded.
- Fully separate signal from noise when their spectra overlap.
- Compensate for a non-stationary wavelet without additional assumptions.

![](figures/term01_lec06/term01_lec06_convolutional_model.png){width=80%}

**Figure 1.** Convolutional model. A sparse reflectivity series (left) is convolved with the embedded wavelet (center) to give the seismic trace (right). Deconvolution tries to recover the reflectivity from the trace.

---

## 2. The convolutional model

The classical model for a single seismic trace is

$$
x(t) = w(t) * r(t) + n(t),
$$ {#eq:convolutional-model}

where

- $x(t)$ is the recorded trace,
- $w(t)$ is the embedded wavelet,
- $r(t)$ is the earth's reflectivity series,
- $n(t)$ is additive noise,
- $*$ denotes convolution.

The embedded wavelet is itself a convolution of several effects:

$$
w(t) = s(t) * g_s(t) * g_r(t) * b(t) * i(t) * a(t),
$$ {#eq:embedded-wavelet}

where

| Symbol | Effect | What it does |
|--------|--------|--------------|
| $s(t)$ | Source signature | Airgun pulse, vibrator sweep, explosion |
| $g_s(t)$ | Source ghost | Free-surface reflection near the source |
| $g_r(t)$ | Receiver ghost | Free-surface reflection near the receiver |
| $b(t)$ | Bubble / reverberation | Oscillating airgun bubble, shallow-layer reverberations |
| $i(t)$ | Instrument response | Geophone, hydrophone, recording filters |
| $a(t)$ | Absorption / near surface | Attenuation and filtering in the shallow subsurface |

Not every dataset contains all of these, but at least a few are usually present. Deconvolution methods differ in which of these components they attack and in what prior information they require.

### Assumptions of the classical model

For the simplest deconvolution algorithms we assume:

1. **Stationarity**: the wavelet does not change within the analysis window.
2. **White reflectivity**: reflection coefficients are random and uncorrelated, so their autocorrelation is a spike.
3. **Minimum-phase wavelet**: the phase spectrum of the wavelet is tied to its amplitude spectrum in a specific causal way.
4. **Additive white noise**: noise is uncorrelated with the signal and has a flat spectrum.

When these hold, the autocorrelation of the trace is approximately the autocorrelation of the wavelet, and we can estimate an inverse filter from the trace alone. When they fail, the result degrades in predictable ways.

---

## 3. Phase and the $z$-transform

### 3.1 The $z$-transform as a delay operator

For a discrete sequence $w_0, w_1, w_2, \dots$, the $z$-transform is the polynomial

$$
W(z) = w_0 + w_1 z + w_2 z^2 + \cdots .
$$ {#eq:z-transform}

The variable $z$ is the **unit-delay operator**: multiplying by $z$ delays the sequence by one sample. The $z$-transform turns convolution into polynomial multiplication:

$$
\text{if } x = w * r, \quad \text{then } X(z) = W(z) \, R(z).
$$ {#eq:convolution-z}

Setting $z = e^{-i 2\pi f \Delta t}$ gives the discrete-time Fourier transform, so the Fourier spectrum is a special case of the $z$-transform evaluated on the unit circle.

### 3.2 Dipoles: minimum, maximum, and mixed phase

The simplest non-trivial wavelet is a **dipole** with two samples $(a, b)$:

$$
W(z) = a + b\,z^{-1}.
$$ {#eq:dipole}

The dipole $(a, b)$ and the reversed dipole $(b, a)$ have the **same amplitude spectrum**, because swapping the two samples changes only the phase. The amplitude spectrum is

$$
|W(f)| = \sqrt{a^2 + b^2 + 2ab \cos(2\pi f \Delta t)}.
$$ {#eq:dipole-amplitude}

The phase spectrum is

$$
\phi(f) = \arctan\!\left(\frac{-b \sin(2\pi f \Delta t)}{a + b \cos(2\pi f \Delta t)}\right).
$$ {#eq:dipole-phase}

Compare the two dipoles $(a, b)$ and $(b, a)$ with $a > b > 0$. The phase of $(a, b)$ is smaller at every frequency than the phase of $(b, a)$. Therefore $(a, b)$ is called **minimum-phase**, and $(b, a)$ is called **maximum-phase**.

![](figures/term01_lec06/term01_lec06_dipoles.png){width=80%}

**Figure 2.** A minimum-phase dipole $(a, b)$ and a maximum-phase dipole $(b, a)$ share the same amplitude spectrum. The minimum-phase dipole has its energy concentrated at the front.

### 3.3 Why minimum phase is front-loaded

The inverse of a dipole is obtained by polynomial division:

$$
\frac{1}{a + b\,z^{-1}} = \frac{1}{a}\left(1 - \frac{b}{a}z^{-1} + \left(\frac{b}{a}\right)^2 z^{-2} - \cdots \right).
$$ {#eq:dipole-inverse}

If $|a| > |b|$, the terms $(b/a)^k$ decay, so the series converges in **negative** powers of $z$ (i.e., as $z^{-k}$). That means the inverse filter is **causal**: it has non-zero coefficients only at and after time zero.

If $|b| > |a|$, the same expansion diverges. The convergent expansion must be written in **positive** powers of $z$:

$$
\frac{1}{a + b\,z^{-1}} = \frac{1}{b\,z^{-1}}\left(1 - \frac{a}{b}z + \left(\frac{a}{b}\right)^2 z^{2} - \cdots \right).
$$ {#eq:dipole-inverse-noncausal}

This inverse filter is **non-causal**: it has coefficients before time zero.

The condition $|a| > |b|$ is exactly the condition that the zero of $W(z)$ lies **inside** the unit circle:

$$
a + b\,z^{-1} = 0 \quad \Rightarrow \quad z = -\frac{b}{a}, \quad \left|-\frac{b}{a}\right| < 1.
$$ {#eq:zero-inside}

Any finite causal wavelet can be factored into dipoles. The wavelet is minimum-phase **if and only if every zero of $W(z)$ lies inside the unit circle**, or equivalently, every dipole factor is minimum-phase.  Conversely, a wavelet with one or more zeros outside the unit circle is **mixed-phase** (or maximum-phase, if all zeros are outside).

Because phase spectra add under convolution, the total phase delay is minimized when every dipole factor is minimum-phase. This is the origin of the name *minimum phase* and of the **front-loaded** property: among all causal wavelets with the same amplitude spectrum, the minimum-phase wavelet concentrates its energy earliest in time.

A useful formal statement is the **partial-energy theorem**: for a minimum-phase wavelet $w_n$,

$$
E_p = \sum_{k=0}^{p} w_k^2
$$ {#eq:partial-energy}

is larger than the partial energy of any other causal wavelet with the same amplitude spectrum, for every $p$.

### 3.4 Zero-phase and causal wavelets

A **zero-phase wavelet** is symmetric around time zero. It has the minimum possible duration among *all* wavelets with a given amplitude spectrum, causal or not, but it is non-causal because it extends to negative times.

A **causal wavelet** is zero before time zero. Minimum-phase wavelets are a subset of causal wavelets.

A **mixed-phase wavelet** has some zeros inside and some zeros outside the unit circle. Its inverse filter generally needs both causal and non-causal coefficients.

![](figures/term01_lec06/term01_lec06_phase_wavelets.png){width=90%}

**Figure 3.** Three wavelets with the same amplitude spectrum. The minimum-phase wavelet is front-loaded; the maximum-phase wavelet is back-loaded; the zero-phase wavelet is symmetric and non-causal.

### 3.5 Consequences for filtering

- The convolution of two minimum-phase wavelets is minimum phase.
- The convolution of a minimum-phase wavelet with a zero-phase wavelet is generally **mixed phase**, unless the zero-phase wavelet is much broader band than the minimum-phase wavelet.
- If you change the amplitude spectrum of a minimum-phase wavelet (for example by band-pass filtering), you must also change its phase spectrum to keep it minimum phase.

---

## 4. Deterministic deconvolution

When the wavelet is known or measured, we can design the deconvolution operator directly from the wavelet. This is **deterministic deconvolution**.

### 4.1 Frequency-domain inverse filter

From the convolutional model in the frequency domain,

$$
X(f) = W(f)\,R(f) + N(f).
$$ {#eq:freq-model}

If noise is negligible, the inverse filter is

$$
F(f) = \frac{1}{W(f)}.
$$ {#eq:inverse-filter}

Applying it gives

$$
\hat{R}(f) = F(f)\,X(f) \approx R(f).
$$ {#eq:deconvolved-spectrum}

In practice $W(f)$ has notches and weak amplitudes, so direct division is unstable. We add a prewhitening constant:

$$
F(f) = \frac{W^*(f)}{|W(f)|^2 + \varepsilon^2},
$$ {#eq:prewhitened-inverse}

where $\varepsilon^2$ is a small fraction of the average power. This limits amplification at frequencies where $|W(f)|$ is small.

### 4.2 $z$-domain inverse filter

In the $z$-domain, deconvolution is polynomial division:

$$
F(z) = \frac{1}{W(z)}.
$$ {#eq:z-inverse}

If $W(z)$ is minimum phase, $F(z)$ expands in positive powers of $z$ and the filter is causal. If $W(z)$ is mixed phase, a convergent expansion requires both positive and negative powers, so the filter is two-sided.

![](figures/term01_lec06/term01_lec06_deterministic_decon.png){width=90%}

**Figure 4.** Deterministic deconvolution of a known minimum-phase wavelet. Left: the wavelet. Center: the causal inverse filter obtained by prewhitened spectral division. Right: the convolution of the wavelet with its inverse filter is compressed close to a spike at time zero.

### 4.3 Prewhitening in practice

Prewhitening has two roles:

1. **Numerical stability.** It shifts the eigenvalues of the autocorrelation matrix away from zero.
2. **Noise control.** It limits the amplification of frequencies where the signal-to-noise ratio is low.

A typical value is 0.1–5% of the zero-lag autocorrelation. The effect is to make the deconvolved spectrum a little less white: a small amount of the original wavelet spectrum is retained.

![](figures/term01_lec06/term01_lec06_prewhitening.png){width=80%}

**Figure 5.** Prewhitening stabilizes the inverse filter. Without it, spectral notches produce large spikes in the operator (dashed). With prewhitening, the operator is bounded (solid).

### 4.4 Examples

**Designature.** Marine airgun arrays emit a primary pulse followed by a bubble oscillation. If the far-field signature is measured or modeled, a deterministic inverse filter can remove the bubble train.

**Instrument response removal.** A land geophone plus recording system has a known frequency response (for example, a 10 Hz geophone natural frequency combined with anti-alias and recording filters). Given the measured or specified instrument response, a deterministic inverse operator can be computed and applied to the recorded data to recover ground motion with a flat, broadband response.

**Vibroseis to minimum phase.** Vibroseis data are correlated with the known sweep, producing a zero-phase Klauder wavelet. To process the data with minimum-phase algorithms, an amplitude-only correction followed by minimum-phase spectral factorization converts the wavelet to its minimum-phase equivalent.

---

## 5. Statistical deconvolution — the Wiener filter

Often the wavelet is not known. **Statistical deconvolution** estimates the inverse filter from the trace itself, using the assumptions listed in Section 2.

### 5.1 Least-squares formulation

We seek a finite-length filter $f = (f_0, f_1, \dots, f_N)$ such that when convolved with the trace $x$, the output is as close as possible to a desired output $d$. The error is

$$
E = \sum_t \left| d_t - \sum_{k=0}^{N} f_k \, x_{t-k} \right|^2.
$$ {#eq:ls-error}

Minimizing $E$ with respect to each $f_j$ gives the **Wiener-Hopf equations**:

$$
\sum_{k=0}^{N} f_k \, \phi_{xx}[j-k] = \phi_{dx}[j], \qquad j = 0, \dots, N,
$$ {#eq:wiener-hopf}

where

- $\phi_{xx}[j] = \sum_t x_t \, x_{t+j}$ is the autocorrelation of the input,
- $\phi_{dx}[j] = \sum_t d_t \, x_{t+j}$ is the cross-correlation of the desired output with the input.

In matrix form:

$$
\begin{bmatrix}
\phi_{xx}[0] & \phi_{xx}[1] & \cdots & \phi_{xx}[N] \\
\phi_{xx}[1] & \phi_{xx}[0] & \cdots & \phi_{xx}[N-1] \\
\vdots & \vdots & \ddots & \vdots \\
\phi_{xx}[N] & \phi_{xx}[N-1] & \cdots & \phi_{xx}[0]
\end{bmatrix}
\begin{bmatrix}
f_0 \\
f_1 \\
\vdots \\
f_N
\end{bmatrix}
=
\begin{bmatrix}
\phi_{dx}[0] \\
\phi_{dx}[1] \\
\vdots \\
\phi_{dx}[N]
\end{bmatrix}.
$$ {#eq:wiener-matrix}

The matrix is Toeplitz and symmetric. With prewhitening we add $\varepsilon^2$ to the main diagonal.

### 5.2 Why the assumptions matter

- **White reflectivity.** If the reflectivity autocorrelation is a spike, then $\phi_{xx} \approx \phi_{ww}$ and the operator depends only on the wavelet. Correlated reflectivity (for example from cyclic sequences or short-period multiples) contaminates $\phi_{xx}$.
- **Minimum-phase wavelet.** The phase of the inverse operator is derived from the amplitude spectrum. If the wavelet is mixed phase, the recovered reflectivity has wrong timing.
- **Stationarity.** The operator is designed from a single autocorrelation. If the wavelet changes with time because of attenuation or ghost variation, a single operator cannot be optimal everywhere.
- **White noise.** Correlated or colored noise biases the autocorrelation and distorts the operator.

### 5.3 Efficient solution

The Toeplitz structure allows the system to be solved in $O(N^2)$ operations by the **Wiener-Levinson** or **Levinson-Durbin** recursion, instead of $O(N^3)$ for a general matrix. This is the algorithm used in production processing for long operators.

---

## 6. Spiking and predictive deconvolution

### 6.1 Spiking deconvolution

If the desired output $d$ is a unit spike at zero lag, the cross-correlation on the right-hand side of the Wiener-Hopf equations becomes

$$
\phi_{dx}[j] = \delta[j] = \begin{cases} 1, & j = 0, \\ 0, & j \neq 0. \end{cases}
$$ {#eq:spiking-rhs}

This is **spiking deconvolution**. It tries to compress the wavelet to a single sample. It is the most common form of statistical deconvolution.

In the predictive-deconvolution framework, spiking deconvolution corresponds to a **prediction gap of one sample**.

![](figures/term01_lec06/term01_lec06_spiking_decon.png){width=90%}

**Figure 6.** Spiking deconvolution. Left: input trace (top) and its embedded wavelet (middle), with the input amplitude spectrum (right). Bottom row: the trace after spiking deconvolution, the compressed recovered wavelet, and the broader output amplitude spectrum.

### 6.2 Predictive deconvolution

Many unwanted signals are predictable from past values. A shallow-water layer, for example, produces reverberations with a roughly constant period. Predictive deconvolution estimates the predictable part of the trace and subtracts it.

The desired output is the input trace shifted forward by $\alpha$ samples:

$$
d_t = x_{t+\alpha}.
$$ {#eq:prediction-desired}

The prediction filter $h$ satisfies the Wiener-Hopf equations with the right-hand side $\phi_{dx}[j] = \phi_{xx}[j+\alpha]$. The **prediction-error filter** is

$$
e_t = x_t - \hat{x}_t = x_t - \sum_k h_k \, x_{t-\alpha-k}.
$$ {#eq:prediction-error}

In $z$-form it is

$$
P(z) = 1 - z^{-\alpha} H(z).
$$ {#eq:pef-z}

Because the filter uses only past samples, it is causal. Because it removes predictable energy, it suppresses reverberations and short-period multiples.

### 6.3 Parameter choices

| Parameter | Symbol | Effect |
|-----------|--------|--------|
| Prediction gap | $\alpha$ | One sample → spiking; water-layer period → reverberation suppression |
| Operator length | $N+1$ | Longer operator can model more detail but amplifies noise |
| Prewhitening | $\varepsilon^2$ | Stabilizes and limits noise amplification |
| Analysis window | — | Should contain strong reflections, avoid multiples and ground roll |

A larger prediction gap leaves the wavelet less compressed but removes more multiple energy. A longer operator compresses the wavelet better but is more sensitive to noise and to violations of the stationarity assumption.

![](figures/term01_lec06/term01_lec06_predictive_decon.png){width=90%}

**Figure 7.** Predictive deconvolution with varying prediction gap. Top: input reflectivity. Second row: trace with water-layer reverberations. Third row: gap of one sample (spiking) compresses the wavelet but leaves reverberations. Bottom row: gap matched to the reverberation period suppresses the reverberation train.

### 6.4 Limitations

Predictive deconvolution assumes the multiple period is constant. At far offsets the period of a water-layer multiple changes with ray angle, so the method works best on near-offset data or on data transformed to a domain where the period is constant, such as the linear Radon ($\tau$-$p$) domain.

---

## 7. Summary

- Deconvolution aims to recover band-limited reflectivity by removing or reshaping the embedded wavelet.
- The convolutional model $x = w * r + n$ underlies most single-channel methods.
- Phase matters: minimum-phase wavelets have causal stable inverses and are front-loaded; mixed-phase wavelets need two-sided filters.
- Deterministic deconvolution uses a known wavelet; prewhitening stabilizes spectral division.
- Statistical deconvolution uses the Wiener-Hopf equations derived from least squares; its validity depends on white reflectivity, minimum phase, stationarity, and white noise.
- Spiking deconvolution is a one-sample predictive deconvolution; larger gaps target reverberations and short-period multiples.

---

## Comprehension questions

1. Why can deconvolution not recover frequencies that were never recorded?
2. A dipole is $(4, 1)$ with sample interval 4 ms. Is it minimum phase? Where is the zero of its $z$-transform?
3. Explain why a mixed-phase wavelet generally needs a two-sided inverse filter.
4. What happens to a spiking-deconvolution result if the reflectivity is not white?
5. How does increasing the prediction gap change the behavior of predictive deconvolution?
6. Why is prewhitening important in both deterministic and statistical deconvolution?

---

## Further reading

- Hatton, Worthington & Makin (1986), *Seismic Data Processing: Theory and Practice*, Ch. 2.6–2.8 and 3.4.1.5–3.4.1.6.
- Margrave (2006), *Methods of Seismic Data Processing*, University of Calgary lecture notes, Ch. 3–4.
- Yilmaz (2001), *Seismic Data Analysis*, Vol. 1, deconvolution chapter.
- Verschuur (2006), EAGE EET 03 — Predictive Deconvolution.
