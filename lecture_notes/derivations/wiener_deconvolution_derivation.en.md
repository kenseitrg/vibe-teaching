# Derivation of the Wiener Deconvolution Filter

This document gives a step-by-step derivation of the Wiener filter normal equations starting from the convolutional model of a seismic trace. It is intended as supplementary reading for students who want to see where the equations come from.

---

## 1. The convolutional model

A recorded seismic trace $x(t)$ can be written as the convolution of the earth's reflectivity series $r(t)$ with the seismic wavelet $w(t)$, plus additive noise $n(t)$:

$$
x(t) = w(t) * r(t) + n(t)
$$

In discrete time, using $*$ for convolution:

$$
x[n] = \sum_k w[k]\, r[n-k] + n[n]
$$

The goal of deconvolution is to find a filter $f[n]$ that, when convolved with $x[n]$, gives an output $y[n]$ that is as close as possible to the reflectivity $r[n]$ (or to some desired output $d[n]$).

---

## 2. What the filter should do

We seek a finite-length filter with coefficients

$$
f[0], f[1], \dots, f[N]
$$

such that

$$
y[n] = \sum_{k=0}^{N} f[k]\, x[n-k]
$$

is close to a desired output $d[n]$. For **spiking deconvolution**, $d[n]$ is a spike $\delta[n]$. For **predictive deconvolution**, $d[n]$ is a time-shifted version of the input.

---

## 3. The least-squares error

Define the error at each sample as

$$
e[n] = d[n] - y[n] = d[n] - \sum_{k=0}^{N} f[k]\, x[n-k]
$$

We want to minimize the total squared error over all samples where the filter is defined:

$$
\varepsilon = \sum_n e[n]^2 = \sum_n \left( d[n] - \sum_{k=0}^{N} f[k]\, x[n-k] \right)^2
$$

This is a quadratic function of the unknown filter coefficients $f[0], \dots, f[N]$.

---

## 4. Take derivatives with respect to each coefficient

To minimize $\varepsilon$, take the partial derivative with respect to each coefficient $f[j]$ and set it to zero:

$$
\frac{\partial \varepsilon}{\partial f[j]} = -2 \sum_n \left( d[n] - \sum_{k=0}^{N} f[k]\, x[n-k] \right) x[n-j] = 0
$$

Rearranging:

$$
\sum_n d[n]\, x[n-j] = \sum_{k=0}^{N} f[k] \sum_n x[n-k]\, x[n-j]
$$

---

## 5. Identify the correlation functions

Define the **autocorrelation** of the input $x$:

$$
\varphi_{xx}[m] = \sum_n x[n]\, x[n-m]
$$

and the **cross-correlation** of the desired output $d$ with the input $x$:

$$
\varphi_{dx}[m] = \sum_n d[n]\, x[n-m]
$$

Using these definitions, the derivative condition becomes:

$$
\varphi_{dx}[j] = \sum_{k=0}^{N} f[k]\, \varphi_{xx}[j-k], \quad j = 0, \dots, N
$$

These are the **Wiener-Hopf equations** (or normal equations) for the optimal filter.

---

## 6. Matrix form

Write the equations for $j = 0, 1, \dots, N$ explicitly:

$$
\begin{aligned}
\varphi_{xx}[0] f[0] + \varphi_{xx}[1] f[1] + \dots + \varphi_{xx}[N] f[N] &= \varphi_{dx}[0] \\
\varphi_{xx}[1] f[0] + \varphi_{xx}[0] f[1] + \dots + \varphi_{xx}[N-1] f[N] &= \varphi_{dx}[1] \\
&\vdots \\
\varphi_{xx}[N] f[0] + \varphi_{xx}[N-1] f[1] + \dots + \varphi_{xx}[0] f[N] &= \varphi_{dx}[N]
\end{aligned}
$$

In matrix-vector form:

$$
\begin{pmatrix}
\varphi_{xx}[0] & \varphi_{xx}[1] & \cdots & \varphi_{xx}[N] \\
\varphi_{xx}[1] & \varphi_{xx}[0] & \cdots & \varphi_{xx}[N-1] \\
\vdots & \vdots & \ddots & \vdots \\
\varphi_{xx}[N] & \varphi_{xx}[N-1] & \cdots & \varphi_{xx}[0]
\end{pmatrix}
\begin{pmatrix}
f[0] \\ f[1] \\ \vdots \\ f[N]
\end{pmatrix}
=
\begin{pmatrix}
\varphi_{dx}[0] \\ \varphi_{dx}[1] \\ \vdots \\ \varphi_{dx}[N]
\end{pmatrix}
$$

The matrix is symmetric and Toeplitz (constant along diagonals) because the autocorrelation is even: $\varphi_{xx}[m] = \varphi_{xx}[-m]$.

---

## 7. Stabilization (prewhitening)

In practice, the autocorrelation matrix can be poorly conditioned when the input spectrum has notches or when the data are noisy. A common fix is to add a small positive constant $\varepsilon^2$ to the diagonal:

$$
(\varphi_{xx}[0] + \varepsilon^2)\, f[0] + \varphi_{xx}[1]\, f[1] + \dots + \varphi_{xx}[N]\, f[N] = \varphi_{dx}[0]
$$

This is equivalent to adding a small amount of white noise to the input before designing the filter. The constant $\varepsilon^2$ is called the **prewhitening factor**.

---

## 8. Solving the system

Because the matrix is Toeplitz, the system can be solved efficiently with the **Levinson-Durbin recursion** (or, more generally, the **Wiener-Levinson algorithm**) in $O(N^2)$ operations instead of $O(N^3)$ for a general linear system.

---

## 9. Summary

Starting from the convolutional model, the Wiener deconvolution filter is the filter that minimizes the squared difference between the actual output and the desired output. The optimal coefficients satisfy the Wiener-Hopf equations:

$$
\sum_{k=0}^{N} f[k]\, \varphi_{xx}[j-k] = \varphi_{dx}[j], \quad j = 0, \dots, N
$$

or, in compact form:

$$
\boldsymbol{\Phi}_{xx}\, \mathbf{f} = \boldsymbol{\varphi}_{dx}
$$

where $\boldsymbol{\Phi}_{xx}$ is the autocorrelation matrix, $\mathbf{f}$ is the filter vector, and $\boldsymbol{\varphi}_{dx}$ is the cross-correlation vector.

---

## 10. Link back to deconvolution

For **spiking deconvolution**, the desired output is a spike:

$$
d[n] = \delta[n] \;\longrightarrow\; \varphi_{dx}[j] = x[-j]
$$

For **predictive deconvolution**, the desired output is a time-shifted copy of the input:

$$
d[n] = x[n-\alpha] \;\longrightarrow\; \varphi_{dx}[j] = \varphi_{xx}[j-\alpha]
$$

where $\alpha$ is the prediction lag (often the multiple period).

In both cases, the same Wiener machinery applies; only the right-hand side of the normal equations changes.
