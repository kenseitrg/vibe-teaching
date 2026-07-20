# FX-Deconvolution: Derivation of the F-X Prediction Operator

This document derives the FX-deconvolution operator step by step, following
the ideas of Canales (1984), Treitel (1974), and Abma & Claerbout (1995). It
is supplementary reading for Term 3 Lecture 04 and assumes familiarity with
the Wiener filter and the prediction-error filter (PEF) from Term 1
Lecture 06.

> **Prerequisites.** Discrete convolution, the Fourier transform, and the
> real-valued Wiener filter normal equations (see
> [Wiener filter derivation](wiener_deconvolution_derivation.en.md) and
> [PEF Z-transform derivation](pef_ztransform_derivation.en.md)). The only new
> ingredient here is that the data are **complex-valued**, which changes the
> normal equations slightly (Section 4).

---

## 1. Signal model: linear events in the $t$-$x$ domain

Consider an ensemble of $M$ seismic traces (a stacked section or a common offset gather).
Following Canales (1984), model the data as a sum of $P$ events, each a
wavelet $w_j(t)$ delayed by a moveout function $\tau_j(x)$:

$$
u(t, x) = \sum_{j=1}^{P} A_j \, w_j\bigl(t - \tau_j(x)\bigr),
$$

where $A_j$ is the amplitude of event $j$ and $x$ is the spatial coordinate
(trace position).

**Linearity assumption.** Within a small spatial window, each event is
approximately linear in $x$:

$$
\tau_j(x) = \tau_j^{0} + p_j \, x,
$$

where $p_j = \Delta t / \Delta x = 1 / v_{\text{app},j}$ is the slope (dip) of
event $j$ — the reciprocal of its apparent velocity. Real reflections can have a complex shape, but any smooth curve is locally linear if the window
is small enough. This is why FX-deconvolution is always applied in windows.

---

## 2. From $t$-$x$ to $f$-$x$: complex exponentials

Fourier-transform each trace in time. A time shift becomes a phase factor:

$$
w_j(t - \tau_j) \;\xrightarrow{\;\mathcal{F}\;}\; W_j(f)\, e^{-i 2\pi f \tau_j}.
$$

Applying this to the model and inserting the linear moveout:

$$
U(f, x) = \sum_{j=1}^{P} A_j \, W_j(f)\, e^{-i 2\pi f (\tau_j^0 + p_j x)}
        = \sum_{j=1}^{P} C_j(f)\, e^{-i 2\pi f p_j x},
$$

where $C_j(f) = A_j W_j(f) e^{-i 2\pi f \tau_j^0}$ collects everything that
does not depend on $x$.

Now sample the spatial axis at the trace positions $x_n = n\,\Delta x$,
$n = 0, 1, \dots, M-1$:

$$
\boxed{\;
U_n(f) = \sum_{j=1}^{P} C_j(f)\, z_j^{\,n},
\qquad z_j = e^{-i 2\pi f p_j \Delta x}.
\;}
$$

> **Key result.** At each fixed frequency $f$, the signal along the spatial
> axis is a **sum of complex exponentials** in the trace index $n$. Each
> dipping event contributes one exponential; the dip $p_j$ controls the
> phase rotation $\theta_j = 2\pi f p_j \Delta x$ per trace.

Random noise, in contrast, has no such structure: it is uncorrelated from
trace to trace at every frequency. This difference — predictable exponentials
vs. unpredictable noise — is the entire basis of the method.

---

## 3. Predictability of complex exponentials

### 3.1 A single event is perfectly predictable with one coefficient

For a single event ($P = 1$), the spatial sequence is $U_n = C z^n$. The next
value follows from the current one by a single multiplication:

$$
U_{n} = z \cdot U_{n-1}, \qquad z = e^{-i 2\pi f p \Delta x}.
$$

So a **one-coefficient prediction filter** $h_1 = z$ predicts the event with
zero error. The filter coefficient is simply the phase rotation per trace.

### 3.2 $P$ events are perfectly predictable with $P$ coefficients

A sum of $P$ complex exponentials satisfies a linear recurrence of order $P$.
Define the polynomial whose roots are the $z_j$:

$$
A(z) = \prod_{j=1}^{P} \bigl(1 - z_j\, z^{-1}\bigr)
     = 1 + a_1 z^{-1} + \dots + a_P z^{-P}.
$$

Because each $z_j$ is a root, the sequence $U_n = \sum_j C_j z_j^n$ is
annihilated by the corresponding filter:

$$
U_n + a_1 U_{n-1} + \dots + a_P U_{n-P} = 0
\quad\Longrightarrow\quad
U_n = -\sum_{k=1}^{P} a_k\, U_{n-k}.
$$

So a $P$-coefficient prediction filter $h_k = -a_k$ predicts the signal
**exactly**, and the prediction error is identically zero. This is Canales'
Appendix A argument: all roots $z_j$ lie **on** the unit circle
($|z_j| = 1$), the PEF's last reflection coefficient has unit magnitude, and
the prediction error vanishes (Claerbout, 1976).

> **Intuition.** The number of filter coefficients needed equals the number
> of distinct dips in the window. One dipping event → one coefficient. Two
> events with different dips → two coefficients. This is why short spatial
> windows (few dips) allow short filters, and why windows with many
> conflicting dips defeat the method.

---

## 4. Estimating the prediction filter: the complex Wiener filter

In practice we do not know the dips or the number of events, and the data
contain noise. We therefore **estimate** the prediction filter from the data
by least squares, using Treitel's (1974) complex Wiener filter theory.

### 4.1 Least-squares setup

At a fixed frequency $f$, let the observed spatial sequence be

$$
X_n = S_n + N_n, \qquad n = 0, \dots, M-1,
$$

where $S_n$ is the signal (sum of complex exponentials) and $N_n$ is random
noise. (We drop the explicit $f$ dependence for readability.)

We seek a one-step-ahead prediction filter $h_1, \dots, h_K$ that minimizes
the prediction-error energy

$$
\varepsilon^2 = \sum_n \left| X_n - \sum_{k=1}^{K} h_k\, X_{n-k} \right|^2.
$$

Everything is complex-valued: the data $X_n$, the filter $h_k$, and the
error. Note the modulus squared $|\cdot|^2$ in place of the ordinary square.

### 4.2 Complex normal equations

Define the complex autocorrelation of the spatial sequence:

$$
\phi[k] = \sum_n X_n\, X_{n-k}^{*},
\qquad \phi[-k] = \phi[k]^{*},
$$

where ${}^{*}$ denotes complex conjugation. The autocorrelation is
**Hermitian**: its value at negative lag is the conjugate of its value at
positive lag.

Minimizing $\varepsilon^2$ with respect to each $h_m^{*}$ (the standard
complex least-squares trick: treat $h_m$ and $h_m^{*}$ as independent
variables and differentiate with respect to the conjugate) gives

$$
\sum_{k=1}^{K} h_k\, \phi[m-k] = \phi[m],
\qquad m = 1, 2, \dots, K.
$$

In matrix form:

$$
\boxed{\;
\mathbf{R}\, \mathbf{h} = \mathbf{g},
\;}
$$

with

$$
\mathbf{R} =
\begin{bmatrix}
\phi[0] & \phi[-1] & \cdots & \phi[-(K-1)] \\
\phi[1] & \phi[0] & \cdots & \phi[-(K-2)] \\
\vdots & \vdots & \ddots & \vdots \\
\phi[K-1] & \phi[K-2] & \cdots & \phi[0]
\end{bmatrix},
\qquad
\mathbf{g} =
\begin{bmatrix}
\phi[1] \\ \phi[2] \\ \vdots \\ \phi[K]
\end{bmatrix}.
$$

### 4.3 Properties of the system

- $\mathbf{R}$ is **Hermitian** ($\mathbf{R}^H = \mathbf{R}$) and
  **Toeplitz** (constant along each diagonal). This is the complex
  counterpart of the symmetric Toeplitz autocorrelation matrix from the
  real-valued Wiener filter.
- The right-hand side $\mathbf{g}$ contains the autocorrelation at lags
  $1, \dots, K$ — exactly as in unit-gap ($\alpha = 1$) predictive
  deconvolution, but with complex values.
- The system can be solved efficiently with the **block-Toeplitz Levinson
  recursion** (Robinson, 1967), which — as Treitel showed — can be organized
  so that no complex arithmetic is needed on the computer: writing
  $\mathbf{R} = \mathbf{P} + i\mathbf{Q}$ with $\mathbf{P}$ real symmetric
  and $\mathbf{Q}$ real skew-symmetric, the complex system becomes a real
  block-Toeplitz system of twice the size.

### 4.4 Minimum prediction error

Substituting the normal equations into the error energy gives the minimum
error:

$$
\varepsilon^2_{\min} = \phi[0] - \sum_{k=1}^{K} h_k\, \phi[k]^{*}
                     = \phi[0] - \mathbf{g}^{H} \mathbf{h}.
$$

- If the data are a pure sum of $P \le K$ complex exponentials (no noise),
  the filter predicts the signal exactly and $\varepsilon^2_{\min} = 0$
  (Section 3.2).
- With random noise added, the signal part is still predicted, but the noise
  is not: $\varepsilon^2_{\min}$ equals (approximately) the noise energy.

---

## 5. The FX-deconvolution algorithm

The prediction machinery above is applied independently at each frequency.
The complete workflow (Canales 1984; Gulunay's FXDECON, 1986) is:

1. **Window** the data in space (and optionally in time) so that events are
   approximately linear within each window. Typical spatial windows are
   10–30 traces.
2. **Fourier-transform** each trace in time.
3. **For each frequency** $f$ in the signal band:
   1. Form the spatial sequence $X_0(f), \dots, X_{M-1}(f)$.
   2. Estimate the autocorrelations $\phi[0], \dots, \phi[K]$.
   3. Solve the complex normal equations
      $\mathbf{R}\mathbf{h} = \mathbf{g}$ for the prediction filter
      $h_1, \dots, h_K$ (filter length $K$ typically 2–6).
   4. Compute the **predicted (signal) component**:
      $$
      \hat{S}_n(f) = \sum_{k=1}^{K} h_k\, X_{n-k}(f).
      $$
4. **Inverse Fourier-transform** $\hat{S}_n(f)$ back to the time domain.

The output $\hat{S}_n$ is the least-squares estimate of the predictable —
laterally coherent — part of the data. The removed noise is the residual
$X_n - \hat{S}_n$.

> **Naming.** Gulunay called the process FXDECON ("f-x deconvolution"). As
> Abma & Claerbout point out, the name is a misnomer: deconvolution removes
> the predictable part, whereas here the predictable part **is** the desired
> output. "F-X prediction filtering" or "random noise attenuation (RNA)" are
> more accurate names.

---

## 6. Worked example: a single dipping event

Take a single linear event with dip $p$ on traces spaced $\Delta x$ apart, at
a single frequency $f$. The spatial sequence (noiseless) is

$$
X_n = C\, z^n, \qquad z = e^{i\theta}, \qquad \theta = -2\pi f p \Delta x.
$$

**Autocorrelations** (over $N$ samples in the sum):

$$
\phi[k] = \sum_n C z^n \bigl(C z^{n-k}\bigr)^{*}
        = |C|^2 z^{k} \sum_n 1
        = N |C|^2 z^{k}.
$$

**Normal equation for $K = 1$:**

$$
h_1\, \phi[0] = \phi[1]
\quad\Longrightarrow\quad
h_1 = \frac{N|C|^2 z}{N|C|^2} = z = e^{i\theta}.
$$

The optimal filter is exactly the phase rotation per trace, as Section 3.1
predicted. The predicted signal is

$$
\hat{S}_n = h_1 X_{n-1} = z \cdot C z^{n-1} = C z^n = X_n,
$$

so the prediction error is identically zero.

**Numerical check.** Let $f = 30$ Hz, $p = 0.5$ ms/trace (a dip of half a
millisecond per trace), so $\theta = -2\pi \cdot 30 \cdot 0.0005 \approx
-0.0942$ rad. The filter coefficient is $h_1 = e^{-0.0942\,i} \approx
0.996 - 0.094\,i$: nearly unity, with a small negative imaginary part that
rotates the phase by about $5.4°$ per trace — exactly the dip-induced phase
shift.

**With noise.** If $X_n = C z^n + N_n$ with white complex noise of variance
$\sigma^2$, the autocorrelation becomes $\phi[0] = N|C|^2 + \sigma^2$ and
$\phi[1] = N|C|^2 z$, so

$$
h_1 = \frac{N|C|^2}{N|C|^2 + \sigma^2}\, z.
$$

The filter still has the correct phase $z$, but its magnitude is shrunk by
the factor $\text{SNR}/(1 + \text{SNR})$ — a classic Wiener-filter result:
noisy data are predicted conservatively, and the shrinkage is largest where
the noise is strongest.

---

## 7. Why the constant-dip assumption matters

Suppose the window contains **two** events with different dips
$p_1 \neq p_2$. The signal is $S_n = C_1 z_1^n + C_2 z_2^n$ and, by
Section 3.2, a $K = 2$ filter predicts it exactly. But with only $K = 1$,
the normal equation gives

$$
h_1 = \frac{\phi[1]}{\phi[0]}
     = \frac{|C_1|^2 z_1 + |C_2|^2 z_2}{|C_1|^2 + |C_2|^2},
$$

an energy-weighted average of the two phase rotations. The filter predicts
**neither** event correctly; both leak partially into the residual and are
partially subtracted as "noise."

This is the central failure mode of FX-deconvolution:

- **Too few coefficients for the number of dips** → coherent signal appears
  in the noise panel; the output looks over-smoothed or "synthetic."
- **Too many coefficients** → the filter starts fitting the noise itself,
  and random noise leaks into the output.

Practical consequences (Abma & Claerbout, 1995):

- Use **short spatial windows** so that at most a few dips are present.
- **Flatten** the data first (e.g., apply NMO): flat events all have dip
  $p \approx 0$, so even a short filter predicts all of them, and residual
  dip variation is minimized.
- Use **time-variant windows**, because dip generally varies with time on a
  gather.

---

## 8. The $t$-$x$ view: what the operator really looks like

Each frequency is filtered independently, with $K$ spatial coefficients per
frequency. Abma & Claerbout (1995) observed that when the collection of
per-frequency filters is transformed back to the $t$-$x$ domain, they combine
into a **single 2-D prediction operator whose time length equals the full
window length**:

- The operator has as many free coefficients in time as the data have
  samples.
- This enormous number of degrees of freedom lets the operator fit — and
  therefore pass — more random noise than a compact $t$-$x$ filter would.
- It can also **generate spurious events**, particularly in the presence of
  parallel events.

A compact $t$-$x$ prediction filter (a few coefficients in time, a few in
space) avoids this because its time length is explicitly controlled. The
trade-off is that the $t$-$x$ design problem is a single large least-squares
problem (solved, e.g., by conjugate gradients) instead of many small
per-frequency systems.

Gulunay's FXDECON also biases predictions toward traces nearest the output
trace, which passes somewhat more noise; the bias can be removed by
modifying the system of equations. In practice, FX-deconvolution remains
popular because it is fast, robust at moderate noise levels, and trivially
parallel over frequencies.

---

## 9. Practical notes

- **Prewhitening.** Adding a small constant $\varepsilon^2$ to $\phi[0]$
  stabilizes the normal equations and makes the filter more conservative —
  the same trick as in time-domain deconvolution.
- **Forward-backward prediction.** The spatial sequence can be predicted in
  both directions (the reversed sequence has the conjugate phase structure).
  Averaging the two normal-equation systems doubles the effective data and
  improves the filter estimate on short windows.
- **Difference QC.** Always inspect the removed noise (input minus output).
  If coherent events are visible in the difference, the window is too large
  or the filter too short for the dip content (Section 7).
- **Two passes.** Canales applied the process twice, with amplitude
  rebalancing between passes, for extra improvement on very noisy data.

---

## 10. Summary

| Step | Real-valued Wiener/PEF (time domain) | FX-deconvolution (f-x domain) |
|---|---|---|
| Data | Real time series $x[n]$ | Complex spatial sequence $X_n(f)$ at each $f$ |
| Signal structure | Repetition every $\alpha$ samples | Sum of complex exponentials $C_j z_j^n$ |
| Predictability | Wavelet/multiples predictable in time | Linear events predictable in space |
| Normal equations | $\mathbf{R}\mathbf{h} = \mathbf{g}$, symmetric Toeplitz | $\mathbf{R}\mathbf{h} = \mathbf{g}$, **Hermitian** Toeplitz |
| Desired output | Prediction error (deconvolution) | **Prediction itself** (signal estimate) |
| Key assumption | Stationary wavelet | Constant dip within the window |
| Filter length | $N+1$ coefficients | $K \approx$ number of dips (2–6) |
| Failure mode | Non-minimum-phase wavelet | Conflicting dips; noise fitting |

---

## 11. Relationship to other derivations

- The normal equations in Section 4 have exactly the same structure as the
  real-valued case derived in the
  [Wiener filter derivation](wiener_deconvolution_derivation.en.md); the only
  differences are the Hermitian transpose in place of the transpose and
  complex autocorrelations.
- The prediction-filter/PEF relationship ($F(z) = 1 - z^{-1}H(z)$, zeros on
  the unit circle annihilate predictable components) is developed in the
  [PEF Z-transform derivation](pef_ztransform_derivation.en.md). Section 3.2
  here is the spatial, complex-valued analogue.
- Cadzow (Hankel-structured SVD) filtering, covered in Section 7 of the
  lecture, enforces the same "sum of exponentials" model algebraically: a
  rank-$P$ Hankel matrix represents exactly $P$ complex exponentials. Rank
  truncation and prediction filtering are two faces of the same signal
  model.

---

## References

- Canales, L. L. (1984). Random noise reduction. *54th SEG Annual Meeting,
  Expanded Abstracts*, 525–527. `wiki/sources/canales1984_fx_decon.md`
- Treitel, S. (1974). The complex Wiener filter. *Geophysics*, 39(2),
  169–173. `wiki/sources/treitel1974_complex_wiener.md`
- Gulunay, N. (1986). FXDECON and complex Wiener prediction filter.
  *56th SEG Annual Meeting, Expanded Abstracts*, 279–281.
  `wiki/sources/gulunay1986_fxdecon.md`
- Abma, R. & Claerbout, J. (1995). Lateral prediction for noise attenuation
  by t-x and f-x techniques. *Geophysics*, 60(6), 1887–1896.
  `wiki/sources/abma1995_lateral_prediction.md`
- Claerbout, J. F. (1976). *Fundamentals of Geophysical Data Processing.*
  McGraw-Hill.
