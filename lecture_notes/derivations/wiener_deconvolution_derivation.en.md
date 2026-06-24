# Derivation of the Wiener Deconvolution Filter

This document gives a step-by-step derivation of the Wiener filter normal
equations, starting from the convolutional model of a seismic trace. A small
worked numerical example is included. It is intended as supplementary reading
for students who want to see where the equations in the lecture notes come
from.

> **Prerequisites.** Comfort with discrete convolution, basic summation
> notation, and partial derivatives. If you have seen linear least squares
> before, the structure here is the same — we just work with sequences instead
> of independent variables.

---

## 1. The convolutional model (discrete)

A recorded seismic trace $x[n]$ is the convolution of the reflectivity $r[n]$
with the seismic wavelet $w[n]$, plus additive noise $n$:

$$
x[n] = \sum_{k} w[k] \, r[n-k] + n[n].
$$

The goal of deconvolution is to find a filter $f$ that, when applied to $x$,
recovers the reflectivity (or some other desired output).

---

## 2. What a finite-length filter looks like

We restrict the filter to a finite number $N+1$ of coefficients:

$$
f[0],\; f[1],\; \dots,\; f[N].
$$

The filter output $y[n]$ at time $n$ is a weighted sum of $N+1$ consecutive
input samples, ending at the current time:

$$
y[n] = \sum_{k=0}^{N} f[k] \; x[n-k].
$$

This is a **causal** filter: the output at time $n$ depends only on $x[n]$,
$x[n-1]$, ..., $x[n-N]$.

> **Naming convention.** In the lecture notes the coefficients are written as
> $f_0, f_1, \dots, f_N$ (subscripts). Here we use square brackets
> $f[0], f[1], \dots$ — they mean the same thing.

---

## 3. Desired output and error

We pick a **desired output** $d[n]$. Two common choices are:

| Desired output $d[n]$ | Name | Effect |
|---|---|---|
| $\delta[n]$ (a unit spike at lag 0) | **Spiking deconvolution** | Compresses the wavelet to a spike |
| $x[n-\alpha]$ (input delayed by $\alpha$) | **Predictive deconvolution** | Removes energy predictable $\alpha$ samples ahead |

The error at each time sample is

$$
e[n] = d[n] - y[n] = d[n] - \sum_{k=0}^{N} f[k] \; x[n-k].
$$

---

## 4. What $n$ range do we sum over?

The filter $f$ has $N+1$ coefficients. The full convolution $y[n]$ is defined
for $n = 0, 1, \dots, L_x + N$ (where $L_x$ is the trace length), but the
first $N$ samples have fewer terms because $x$ is defined to be zero for
negative indices.

In the derivation it is standard to sum over all $n$ where the filter is
**fully immersed** in the data (the "valid" region), or simply over the entire
trace and accept boundary transients. Both choices lead to the same normal
equations in the limit of long data. We write

$$
\varepsilon = \sum_{n} e[n]^2
$$

and let the context clarify that the sum covers the relevant range.

---

## 5. Least-squares minimization

The total squared error is

$$
\varepsilon = \sum_{n} \bigl( d[n] - \sum_{k=0}^{N} f[k] \, x[n-k] \bigr)^2.
$$

This is a quadratic function of $f[0], \dots, f[N]$. To minimize it we take
the partial derivative with respect to each coefficient and set it to zero.

For coefficient $f[j]$:

$$
\frac{\partial \varepsilon}{\partial f[j]}
 = -2 \sum_{n} \bigl( d[n] - \sum_{k=0}^{N} f[k] \, x[n-k] \bigr) \, x[n-j]
 = 0.
$$

Rearranging — moving the term with $f[k]$ to one side — gives

$$
\sum_{n} d[n] \, x[n-j]
 = \sum_{k=0}^{N} f[k] \sum_{n} x[n-k] \, x[n-j], \qquad
 j = 0, \dots, N.
$$

---

## 6. From sums to correlations

Define two functions that depend only on the **lag** $m$:

$$
\boxed{\;
\phi_{xx}[m] = \sum_{n} x[n] \, x[n-m]
\;}
\qquad\text{(autocorrelation of the input)}
$$

$$
\boxed{\;
\phi_{dx}[m] = \sum_{n} d[n] \, x[n-m]
\;}
\qquad\text{(cross-correlation of desired output with input)}.
$$

Notice that $\phi_{xx}[-m] = \phi_{xx}[m]$ — the autocorrelation is even.

With these definitions the derivative condition becomes

$$
\boxed{\;
\sum_{k=0}^{N} f[k] \; \phi_{xx}[j-k] = \phi_{dx}[j],
\qquad j = 0, \dots, N.
\;}
$$

These are the **Wiener-Hopf equations** (also called the **normal equations**).
They are a system of $N+1$ linear equations in $N+1$ unknowns.

---

## 7. Matrix form

Write out the equations for $j=0, 1, \dots, N$ explicitly:

$$
\begin{aligned}
\phi_{xx}[0] f[0] + \phi_{xx}[1] f[1] + \dots + \phi_{xx}[N] f[N]
 &= \phi_{dx}[0] \\
\phi_{xx}[1] f[0] + \phi_{xx}[0] f[1] + \dots + \phi_{xx}[N-1] f[N]
 &= \phi_{dx}[1] \\
&\ \ \vdots \\
\phi_{xx}[N] f[0] + \phi_{xx}[N-1] f[1] + \dots + \phi_{xx}[0] f[N]
 &= \phi_{dx}[N].
\end{aligned}
$$

In matrix-vector form:

$$
\begin{pmatrix}
\phi_{xx}[0] & \phi_{xx}[1] & \cdots & \phi_{xx}[N] \\
\phi_{xx}[1] & \phi_{xx}[0] & \cdots & \phi_{xx}[N-1] \\
\vdots & \vdots & \ddots & \vdots \\
\phi_{xx}[N] & \phi_{xx}[N-1] & \cdots & \phi_{xx}[0]
\end{pmatrix}
\begin{pmatrix}
f[0] \\ f[1] \\ \vdots \\ f[N]
\end{pmatrix}
=
\begin{pmatrix}
\phi_{dx}[0] \\ \phi_{dx}[1] \\ \vdots \\ \phi_{dx}[N]
\end{pmatrix}.
$$

The matrix is:
- **Symmetric** — $\phi_{xx}[m] = \phi_{xx}[-m]$.
- **Toeplitz** — constant along each diagonal (every row is a shifted copy of
  the row above).
- **Positive definite** (for a non-trivial signal), so a unique solution exists.

---

## 8. Stabilization (prewhitening)

The autocorrelation matrix can be nearly singular when the data have a
narrow-band spectrum (e.g., a monochromatic sinusoid, or a seismic wavelet
with a strong notch). The eigenvalues of a Toeplitz autocorrelation matrix
equal the power spectrum of $x$. If the spectrum has near-zero values, the
corresponding eigenvalues are near zero, and the matrix is ill-conditioned.

The standard fix is to add a small positive constant $\varepsilon^2$ to the
main diagonal:

$$
\phi_{xx}[0] \;\rightarrow\; \phi_{xx}[0] + \varepsilon^2.
$$

This is called **prewhitening** (or **Tikhonov regularization**). It:
- shifts all eigenvalues up by $\varepsilon^2$, away from zero,
- improves the condition number of the matrix,
- is equivalent to adding a small amount of white noise to the data before
  designing the filter.

The lecture notes use $\varepsilon^2 \approx 0.01 \cdot \phi_{xx}[0]$ as a
typical starting value.

---

## 9. Solving the system

Because the matrix is Toeplitz, the system can be solved efficiently with the
**Levinson-Durbin recursion** (also called the **Wiener-Levinson algorithm**).
The cost is $O(N^2)$ operations instead of $O(N^3)$ for a general $N \times N$
system. This matters because production deconvolution operators can be
hundreds of samples long.

In Python, for small operators, a direct solve with `numpy.linalg.solve` is
sufficient. The demo script `demo_wiener_matrix.py` builds the Toeplitz
matrix explicitly and solves it — visually, the matrix looks like this:

![Toeplitz autocorrelation matrix and the resulting Wiener operator.]
 (../../figures/term01_lec07/term01_lec07_demo_wiener_matrix.png)

**Figure 1.** *Left:* trace before (blue) and after (green) spiking
deconvolution. *Centre:* the Toeplitz autocorrelation matrix $\mathbf{R}$.
*Right:* the Wiener spiking operator coefficients.

---

## 10. Worked numerical example

To build intuition, here is a tiny example with a 3-coefficient filter
($N=2$) and a 5-sample trace.

### Data

$$
x = \bigl[4,\; 2,\; 1,\; -1,\; -2\bigr].
$$

We design a **spiking** deconvolution filter: $d[n] = \delta[n]$ (a unit spike
at $n=0$).

### Step 1 — autocorrelation

First, compute the autocorrelation at lags $0, 1, 2$:

$$
\begin{aligned}
\phi_{xx}[0] &= 4^2 + 2^2 + 1^2 + (-1)^2 + (-2)^2
            = 16 + 4 + 1 + 1 + 4 = 26, \\[4pt]
\phi_{xx}[1] &= 4\cdot 2 + 2\cdot 1 + 1\cdot(-1) + (-1)\cdot(-2)
            = 8 + 2 - 1 + 2 = 11, \\[4pt]
\phi_{xx}[2] &= 4\cdot 1 + 2\cdot(-1) + 1\cdot(-2)
            = 4 - 2 - 2 = 0.
\end{aligned}
$$

### Step 2 — cross-correlation with the desired output

For spiking deconvolution $d[n] = \delta[n]$, so $\phi_{dx}[j] = x[-j]$.
Since $x$ is causal (zero for $n<0$), we get:

$$
\phi_{dx}[0] = x[0] = 4, \qquad
\phi_{dx}[1] = x[-1] = 0, \qquad
\phi_{dx}[2] = x[-2] = 0.
$$

(For a longer trace, $\phi_{dx}[j]$ for spiking deconvolution is very small
except at $j=0$, which is why we often approximate it as
$[\phi_{xx}[0], 0, \dots, 0]^\mathsf{T}$.)

### Step 3 — assemble and solve

The normal equations are:

$$
\begin{pmatrix}
26 & 11 & 0 \\
11 & 26 & 11 \\
0  & 11 & 26
\end{pmatrix}
\begin{pmatrix}
f[0] \\ f[1] \\ f[2]
\end{pmatrix}
=
\begin{pmatrix}
4 \\ 0 \\ 0
\end{pmatrix}.
$$

Solving (e.g., with Gaussian elimination or `numpy.linalg.solve`):

$$
f[0] \approx 0.170,\quad
f[1] \approx -0.071,\quad
f[2] \approx 0.030.
$$

### Step 4 — apply the filter

Convolve $x$ with $f$ (using `mode = "full"` and taking the first 5 samples):

$$
\begin{aligned}
y[0] &= 4 \cdot 0.170 = 0.680, \\
y[1] &= 2 \cdot 0.170 + 4 \cdot (-0.071) = 0.057, \\
y[2] &= 1 \cdot 0.170 + 2 \cdot (-0.071) + 4 \cdot 0.030 = 0.148, \\
y[3] &= (-1) \cdot 0.170 + 1 \cdot (-0.071) + 2 \cdot 0.030 = -0.181, \\
y[4] &= (-2) \cdot 0.170 + (-1) \cdot (-0.071) + 1 \cdot 0.030 = -0.239.
\end{aligned}
$$

The output has a clear peak at $n=0$ (the desired spike location), with
residual energy elsewhere due to the filter's short length.

---

## 11. Filter length — what happens when $N$ changes?

The choice of $N$ (the number of filter coefficients minus one) involves a
trade-off:

| Short filter ($N$ small) | Long filter ($N$ large) |
|---|---|
| Fewer equations, fast to solve | Computationally more expensive |
| Captures only the dominant wavelet structure | Can model complex wavelets |
| Less sensitive to noise | May overfit the noise |
| Leaves more residual energy in the output | Produces sharper compression |

For seismic deconvolution, $N$ is typically chosen to be 1.5–2 times the
expected wavelet length. A filter that is too short cannot fully compress the
wavelet; a filter that is too long may amplify noise.

---

## 12. Right-hand side for spiking and predictive deconvolution

The same Wiener machinery is used for both cases — only the right-hand side
changes.

### Spiking deconvolution

The desired output is a spike: $d[n] = \delta[n]$ (1 at $n=0$, 0 elsewhere).

$$
\phi_{dx}[j] = \sum_n \delta[n] \, x[n-j] = x[-j].
$$

For a causal $x$, $\phi_{dx}[j] \approx 0$ for $j > 0$. The standard
spiking-deconvolution right-hand side is therefore

$$
\phi_{dx} \approx \bigl[ \phi_{xx}[0],\; 0,\; 0,\; \dots,\; 0 \bigr]^{\mathsf{T}}.
$$

The lecture notes use this form.

### Predictive deconvolution

The desired output is a time-shifted version of the input:
$d[n] = x[n-\alpha]$, where $\alpha$ is the prediction lag (often the
water-layer multiple period).

$$
\phi_{dx}[j] = \sum_n x[n-\alpha] \, x[n-j]
            = \sum_m x[m] \, x[m - (j-\alpha)]
            = \phi_{xx}[j - \alpha].
$$

The right-hand side is therefore the autocorrelation shifted by $\alpha$:

$$
\phi_{dx}[j] = \phi_{xx}[j - \alpha].
$$

This is the only change — the matrix and the solution algorithm remain the
same.

---

## 13. Relation to the lesson code

The script `plot_spiking_decon.py` implements these equations in about 10
lines of Python:

```python
acorr = np.correlate(x, x, mode="full")[n-1:]  # lags 0..n-1
R = toeplitz(acorr[:n_op])                       # build matrix
R += eps * np.eye(n_op) * acorr[0]               # prewhiten
d = np.zeros(n_op)
d[0] = acorr[0]                                   # spike RHS
f = np.linalg.solve(R, d)                         # solve
y = np.convolve(x, f, mode="full")[:len(x)]       # apply
```

Mapping to the derivation:
- Line 1: computes $\phi_{xx}[m]$ for all needed lags.
- Line 2: builds the Toeplitz matrix from the equations in §7.
- Lines 3--5: the right-hand side $\phi_{dx}$ for spiking deconvolution (§12)
  with prewhitening (§8).
- Line 6: solves the $N+1$ normal equations.
- Line 7: applies the filter via convolution.

---

## 14. Summary

Starting from the convolutional model and a least-squares error criterion, the
optimal filter coefficients satisfy the **Wiener-Hopf equations**:

$$
\sum_{k=0}^{N} f[k] \; \phi_{xx}[j-k] = \phi_{dx}[j],
\qquad j = 0, \dots, N,
$$

or, in compact matrix form:

$$
\mathbf{R} \, \mathbf{f} = \boldsymbol{\phi}_{dx}.
$$

- $\mathbf{R}$ is the Toeplitz autocorrelation matrix of the input.
- $\boldsymbol{\phi}_{dx}$ is the cross-correlation of the desired output with
  the input.
- Prewhitening ($+\varepsilon^2$ on the diagonal) stabilizes the solution.
- The Levinson-Durbin recursion solves the system in $O(N^2)$ time.
- The right-hand side changes depending on whether the goal is spiking or
  predictive deconvolution; the matrix and the solver stay the same.

---

## Further reading

- Section 5 of the lecture notes (`term01_lec06`) shows the equations in the
  context of the full deconvolution workflow.
- The wiki page on the [Wiener filter](../../wiki/concepts/wiener_filter.md)
  summarises the practical aspects.
- The script `scripts/figures/term01_lec07/demo_wiener_matrix.py` builds and
  visualises the Toeplitz matrix.
