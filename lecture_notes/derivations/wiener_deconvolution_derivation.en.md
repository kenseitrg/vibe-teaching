# Derivation of the Wiener Deconvolution Filter

This document gives a step-by-step derivation of the Wiener filter normal equations starting from the convolutional model of a seismic trace. It is intended as supplementary reading for students who want to see where the equations come from.

---

## 1. The convolutional model

A recorded seismic trace `x(t)` can be written as the convolution of the earth's reflectivity series `r(t)` with the seismic wavelet `w(t)`, plus additive noise `n(t)`:

```text
x(t) = w(t) * r(t) + n(t)
```

In discrete time, using `*` for convolution:

```text
x[n] = Σ_k w[k] r[n-k] + n[n]
```

The goal of deconvolution is to find a filter `f[n]` that, when convolved with `x[n]`, gives an output `y[n]` that is as close as possible to the reflectivity `r[n]` (or to some desired output `d[n]`).

---

## 2. What the filter should do

We seek a finite-length filter with coefficients

```text
f[0], f[1], ..., f[N]
```

such that

```text
y[n] = Σ_{k=0}^{N} f[k] x[n-k]
```

is close to a desired output `d[n]`. For **spiking deconvolution**, `d[n]` is a spike `δ[n]`. For **predictive deconvolution**, `d[n]` is a time-shifted version of the input.

---

## 3. The least-squares error

Define the error at each sample as

```text
e[n] = d[n] - y[n] = d[n] - Σ_{k=0}^{N} f[k] x[n-k]
```

We want to minimize the total squared error over all samples where the filter is defined:

```text
E = Σ_n e[n]^2 = Σ_n ( d[n] - Σ_{k=0}^{N} f[k] x[n-k] )²
```

This is a quadratic function of the unknown filter coefficients `f[0], ..., f[N]`.

---

## 4. Take derivatives with respect to each coefficient

To minimize `E`, take the partial derivative with respect to each coefficient `f[j]` and set it to zero:

```text
∂E / ∂f[j] = -2 Σ_n ( d[n] - Σ_{k=0}^{N} f[k] x[n-k] ) x[n-j] = 0
```

Rearranging:

```text
Σ_n d[n] x[n-j] = Σ_{k=0}^{N} f[k] Σ_n x[n-k] x[n-j]
```

---

## 5. Identify the correlation functions

Define the **autocorrelation** of the input `x`:

```text
φ_xx[m] = Σ_n x[n] x[n-m]
```

and the **cross-correlation** of the desired output `d` with the input `x`:

```text
φ_dx[m] = Σ_n d[n] x[n-m]
```

Using these definitions, the derivative condition becomes:

```text
φ_dx[j] = Σ_{k=0}^{N} f[k] φ_xx[j-k]    for j = 0, ..., N
```

These are the **Wiener-Hopf equations** (or normal equations) for the optimal filter.

---

## 6. Matrix form

Write the equations for `j = 0, 1, ..., N` explicitly:

```text
φ_xx[0] f[0] + φ_xx[1] f[1] + ... + φ_xx[N] f[N] = φ_dx[0]
φ_xx[1] f[0] + φ_xx[0] f[1] + ... + φ_xx[N-1] f[N] = φ_dx[1]
...
φ_xx[N] f[0] + φ_xx[N-1] f[1] + ... + φ_xx[0] f[N] = φ_dx[N]
```

In matrix-vector form:

```text
| φ_xx[0]  φ_xx[1]  ...  φ_xx[N]   |   | f[0] |   | φ_dx[0] |
| φ_xx[1]  φ_xx[0]  ...  φ_xx[N-1] |   | f[1] |   | φ_dx[1] |
|   ...       ...    ...     ...    | · |  ... | = |   ...   |
| φ_xx[N]  φ_xx[N-1] ...  φ_xx[0]  |   | f[N] |   | φ_dx[N] |
```

The matrix is symmetric and Toeplitz (constant along diagonals) because the autocorrelation is even: `φ_xx[m] = φ_xx[-m]`.

---

## 7. Stabilization (prewhitening)

In practice, the autocorrelation matrix can be poorly conditioned when the input spectrum has notches or when the data are noisy. A common fix is to add a small positive constant `ε²` to the diagonal:

```text
(φ_xx[0] + ε²) f[0] + φ_xx[1] f[1] + ... = φ_dx[0]
```

This is equivalent to adding a small amount of white noise to the input before designing the filter. The constant `ε²` is called the **prewhitening factor**.

---

## 8. Solving the system

Because the matrix is Toeplitz, the system can be solved efficiently with the **Levinson-Durbin recursion** (or, more generally, the **Wiener-Levinson algorithm**) in `O(N²)` operations instead of `O(N³)` for a general linear system.

---

## 9. Summary

Starting from the convolutional model, the Wiener deconvolution filter is the filter that minimizes the squared difference between the actual output and the desired output. The optimal coefficients satisfy the Wiener-Hopf equations:

```text
Σ_{k=0}^{N} f[k] φ_xx[j-k] = φ_dx[j]    for j = 0, ..., N
```

or, in compact form:

```text
Φ_xx  f = φ_dx
```

where `Φ_xx` is the autocorrelation matrix, `f` is the filter vector, and `φ_dx` is the cross-correlation vector.

---

## 10. Link back to deconvolution

For **spiking deconvolution**, the desired output is a spike:

```text
d[n] = δ[n]  →  φ_dx[j] = x[-j]
```

For **predictive deconvolution**, the desired output is a time-shifted copy of the input:

```text
d[n] = x[n-α]  →  φ_dx[j] = φ_xx[j-α]
```

where `α` is the prediction lag (often the multiple period).

In both cases, the same Wiener machinery applies; only the right-hand side of the normal equations changes.
