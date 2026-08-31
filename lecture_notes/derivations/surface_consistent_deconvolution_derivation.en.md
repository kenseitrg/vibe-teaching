# Derivation of the surface-consistent deconvolution system

This document derives the linear system used in surface-consistent
deconvolution, starting from the four-factor convolutional model. It also
shows how the same geometric structure appears in surface-consistent
amplitude corrections, and how to build a usable deconvolution operator from
the estimated log-spectra.

> **Prerequisites.** Discrete convolution, the (real) Fourier transform,
> autocorrelation, basic partial derivatives, and the idea of least-squares.
> Familiarity with the single-channel Wiener derivation in
> `wiener_deconvolution_derivation.en.md` is helpful but not required.

---

## 1. The four-factor convolutional model

In the surface-consistent model the effective wavelet on a trace is the
convolution of four factors associated with the surface geometry of that
trace:

$$
w_{s,r,h,c}(t) = s_s(t) * r_r(t) * h_h(t) * c_c(t),
$$

where

| Symbol | Meaning |
|--------|---------|
| $s_s(t)$ | Source-location wavelet at shot $s$ |
| $r_r(t)$ | Receiver-location wavelet at receiver $r$ |
| $h_h(t)$ | Offset-class wavelet for offset bin $h$ |
| $c_c(t)$ | CDP-location wavelet for CDP $c$ |

The recorded trace is then

$$
x_{s,r,h,c}(t) = w_{s,r,h,c}(t) * \rho_{s,r,h,c}(t) + n_{s,r,h,c}(t),
$$

where $\rho$ is the earth reflectivity along the ray path and $n$ is additive
noise. In what follows we drop the subscripts when the context is clear and
write a single trace as

$$
x(t) = s(t) * r(t) * h(t) * c(t) * \rho(t) + n(t).
$$

The goal is to estimate $s$, $r$, $h$, and $c$ separately, remove their
effects, and leave the geology encoded in $\rho$ as unchanged as possible.

---

## 2. Why work in the frequency domain?

Convolution becomes multiplication after the Fourier transform. Taking the
Fourier transform of the noise-free trace model gives

$$
X(f) = S(f) \, R(f) \, H(f) \, C(f) \, \mathcal{R}(f) + N(f).
$$

The magnitudes multiply and the phases add. Surface-consistent deconvolution
is usually carried out on **amplitude spectra** (or equivalently on
autocorrelations), so we focus on magnitudes first:

$$
|X(f)| = |S(f)| \, |R(f)| \, |H(f)| \, |C(f)| \, |\mathcal{R}(f)| + \text{noise terms}.
$$

Taking logarithms turns the product into a sum:

$$
\ln |X(f)| = \ln |S(f)| + \ln |R(f)| + \ln |H(f)| + \ln |C(f)| + \ln |\mathcal{R}(f)| + \text{noise}.
$$

For a fixed frequency $f$ this is a **linear equation** in the unknown
log-amplitudes of the surface factors. That is the key simplification that
makes surface-consistent deconvolution tractable.

---

## 3. From traces to autocorrelations

In practice we do not know $X(f)$ exactly because we do not know the
reflectivity. What we can estimate reliably from the data is the
**autocorrelation** of the trace:

$$
\phi_{xx}[\tau] = \sum_t x(t) \, x(t+\tau).
$$

The Fourier transform of the autocorrelation is the **power spectrum**
$|X(f)|^2$. Under the usual minimum-phase assumption for the embedded
wavelet, the amplitude spectrum $|X(f)|$ (or, equivalently, the power
spectrum) is sufficient to characterize the wavelet. Therefore

$$
\ln |X(f)|^2 = \ln |S(f)|^2 + \ln |R(f)|^2 + \ln |H(f)|^2 + \ln |C(f)|^2 + \ln |\mathcal{R}(f)|^2 + \text{noise}.
$$

Dividing by 2 gives the same linear system in log-amplitudes:

$$
\ln |X(f)| = \ln |S(f)| + \ln |R(f)| + \ln |H(f)| + \ln |C(f)| + \ln |\mathcal{R}(f)| + \text{noise}.
$$

So each trace contributes one noisy linear equation per frequency. Because
many traces share the same shot, receiver, offset class, or CDP, the system
is highly overdetermined and can be solved by least squares.

---

## 4. The linear system $d = Gm$ for one frequency

Fix a frequency $f$. Collect all traces indexed by $i = 1, \dots, M$. Each
trace has a shot index $s_i$, receiver index $r_i$, offset class $h_i$, and
CDP $c_i$. Define the observed data vector

$$
d_i = \ln |X_i(f)|,
$$

and the unknown parameter vector

$$
m = \begin{pmatrix}
\ln |S_1(f)| \\ \vdots \\ \ln |S_{N_s}(f)| \\
\ln |R_1(f)| \\ \vdots \\ \ln |R_{N_r}(f)| \\
\ln |H_1(f)| \\ \vdots \\ \ln |H_{N_h}(f)| \\
\ln |C_1(f)| \\ \vdots \\ \ln |C_{N_c}(f)|
\end{pmatrix}.
$$

The model for trace $i$ is

$$
d_i = \ln |S_{s_i}(f)| + \ln |R_{r_i}(f)| + \ln |H_{h_i}(f)| + \ln |C_{c_i}(f)| + \ln |\mathcal{R}_i(f)| + n_i.
$$

The reflectivity term $\ln |\mathcal{R}_i(f)|$ is different for every trace
and acts as random noise in this system. We therefore absorb it into the
noise term and solve for the surface factors only.

Stacking all traces gives the matrix equation

$$
\mathbf{d} = \mathbf{G} \, \mathbf{m} + \mathbf{n},
$$

where $\mathbf{d}$ has one entry per trace, $\mathbf{m}$ has one entry per
unknown surface factor, and $\mathbf{G}$ is a sparse design matrix with
exactly four ones in each row (one in the shot block, one in the receiver
block, one in the offset block, and one in the CDP block).

For example, with two shots, two receivers, one offset class, and one CDP,
and four traces, the matrix looks like

$$
\mathbf{G} =
\begin{pmatrix}
1 & 0 & 1 & 0 & 1 & 1 \\
1 & 0 & 0 & 1 & 1 & 1 \\
0 & 1 & 1 & 0 & 1 & 1 \\
0 & 1 & 0 & 1 & 1 & 1
\end{pmatrix},
$$

where the columns are ordered $(S_1, S_2, R_1, R_2, H_1, C_1)$.

---

## 5. Least-squares solution

For a fixed frequency the least-squares estimate minimizes

$$
E(f) = \sum_i \bigl( d_i(f) - (\mathbf{G} \mathbf{m})_i \bigr)^2
      = \bigl( \mathbf{d} - \mathbf{G} \mathbf{m} \bigr)^\mathsf{T}
        \bigl( \mathbf{d} - \mathbf{G} \mathbf{m} \bigr).
$$

Take the gradient with respect to $\mathbf{m}$ and set it to zero:

$$
\frac{\partial E}{\partial \mathbf{m}}
 = -2 \, \mathbf{G}^\mathsf{T} \mathbf{d}
   + 2 \, \mathbf{G}^\mathsf{T} \mathbf{G} \, \mathbf{m}
 = 0.
$$

This gives the normal equations

$$
\mathbf{G}^\mathsf{T} \mathbf{G} \, \mathbf{m} = \mathbf{G}^\mathsf{T} \mathbf{d},
$$

and, when $\mathbf{G}^\mathsf{T} \mathbf{G}$ is invertible,

$$
\boxed{
\hat{\mathbf{m}}(f) = \bigl( \mathbf{G}^\mathsf{T} \mathbf{G} \bigr)^{-1}
                       \mathbf{G}^\mathsf{T} \mathbf{d}(f).
}
$$

The same design matrix $\mathbf{G}$ is used for **every frequency**; only
the right-hand side $\mathbf{d}(f)$ changes. This is why the method is
computationally attractive: factor $\mathbf{G}^\mathsf{T}\mathbf{G}$ once,
then solve a small linear system per frequency.

---

## 6. Rank deficiency and the reference solution

The columns of $\mathbf{G}$ sum to a constant vector (each trace has exactly
one shot, one receiver, one offset, and one CDP). Therefore $\mathbf{G}$ is
rank-deficient by one: adding a constant to all source log-amplitudes and
subtracting it from all receiver log-amplitudes leaves $\mathbf{G}\mathbf{m}$
unchanged.

In practice this is fixed by imposing a reference condition, for example

$$
\sum_s \ln |S_s(f)| = 0,
\qquad
\sum_r \ln |R_r(f)| = 0,
\qquad
\sum_h \ln |H_h(f)| = 0,
\qquad
\sum_c \ln |C_c(f)| = 0,
$$

or simply by dropping one factor from each block and setting it to unity.
The physical meaning is that only the *relative* source/receiver/offset/CDP
spectra are identifiable; the overall spectral shape is absorbed into the
remaining zero-phase or surface-consistent balancing step.

---

## 7. Parallel with surface-consistent amplitude corrections

Surface-consistent amplitude corrections use the identical geometric
structure. The model for trace amplitude is

$$
A_i = S_{s_i} \, R_{r_i} \, H_{h_i} \, C_{c_i} \, G_i,
$$

where $A_i$ is the observed trace amplitude, $S$, $R$, $H$, $C$ are
source/receiver/offset/CDP amplitude scalars, and $G_i$ is the geological
amplitude. Taking logarithms gives

$$
\ln A_i = \ln S_{s_i} + \ln R_{r_i} + \ln H_{h_i} + \ln C_{c_i} + \ln G_i.
$$

This is exactly the same linear system

$$
\mathbf{d} = \mathbf{G} \mathbf{m},
$$

with the same design matrix $\mathbf{G}$. The only differences are:

| | Surface-consistent amplitude | Surface-consistent deconvolution |
|---|---|---|
| Unknowns | One scalar per surface location | One log-amplitude spectrum per surface location |
| Data | One observed amplitude per trace | One observed log-amplitude per trace **per frequency** |
| Number of systems | One least-squares problem | One least-squares problem **per frequency** |
| Output | Gain scalars | Deconvolution operators |

This parallel is useful for teaching: once students understand the
surface-consistent amplitude system, the deconvolution system is the same
idea applied independently at each frequency.

---

## 8. Building the deconvolution operators

After solving for $\hat{\mathbf{m}}(f)$ we have estimates of the log-amplitude
spectra

$$
\ln |\hat{S}_s(f)|, \quad
\ln |\hat{R}_r(f)|, \quad
\ln |\hat{H}_h(f)|, \quad
\ln |\hat{C}_c(f)|.
$$

In principle the effective wavelet on a trace combines all four factors. In
practice, however, most implementations use only the **source and receiver
estimates** to build the deconvolution operator. The offset and CDP terms are
often left aside: the offset term contains moveout and AVO information that
we prefer to preserve, while the CDP term contains the local geological
response. Absorbing these into the operator would distort the very signals
we want to keep. Thus the estimated embedded wavelet for trace $i$ is usually
taken as

$$
|\hat{W}_i(f)| \approx
\exp\!\bigl( \ln |\hat{S}_{s_i}(f)| + \ln |\hat{R}_{r_i}(f)| \bigr).
$$

The practical workflow for building and applying the operator is then:

1. exponentiate the source and receiver log-amplitude spectra,
2. multiply the spectra for the shot and receiver of the trace,
3. add a minimum-phase spectrum (or assume minimum phase),
4. stabilize with prewhitening and invert.

### 8.1 Amplitude spectrum of the combined wavelet

For trace $i$ the practical estimate of the embedded-wavelet amplitude
spectrum is

$$
|\hat{W}_i(f)| =
\exp\!\bigl( \ln |\hat{S}_{s_i}(f)| + \ln |\hat{R}_{r_i}(f)| \bigr).
$$

### 8.2 Prewhitening

Before inversion we add a small constant to the power spectrum for numerical
stability:

$$
|\hat{W}_i(f)|^2 \;\rightarrow\; |\hat{W}_i(f)|^2 + \varepsilon^2 \, P_{\max},
$$

where $P_{\max} = \max_f |\hat{W}_i(f)|^2$. The inverse filter in the
frequency domain is then

$$
\hat{F}_i(f) =
\frac{\hat{W}_i^*(f)}{|\hat{W}_i(f)|^2 + \varepsilon^2 P_{\max}}.
$$

### 8.3 Minimum-phase reconstruction

The log-amplitude estimate contains no phase information. To obtain a causal
stable inverse we assume the embedded wavelet is **minimum phase** and
reconstruct the phase from the log-amplitude spectrum via the Hilbert
transform.

For a minimum-phase signal the log-magnitude and phase are a Hilbert-transform
pair:

$$
\phi(f) = -\mathcal{H}\{ \ln |\hat{W}_i(f)| \},
$$

where $\mathcal{H}$ denotes the Hilbert transform. The complex spectrum of the
estimated wavelet is therefore

$$
\hat{W}_i(f) = |\hat{W}_i(f)| \, e^{j \phi(f)}.
$$

The minimum-phase deconvolution operator is the inverse of this spectrum,
with prewhitening:

$$
\hat{D}_i(f) = \frac{1}{\hat{W}_i(f) + \varepsilon}
              = \frac{\hat{W}_i^*(f)}{|\hat{W}_i(f)|^2 + \varepsilon^2}.
$$

Transforming back to the time domain gives the operator $d_i(t)$, which is
applied to the trace by convolution.

Some implementations build the operator directly from the amplitude spectrum
and the Hilbert-transform phase, while others design a Wiener spiking
operator from the estimated autocorrelation. Both approaches are equivalent
in the minimum-phase case.

---

## 9. Practical summary of the workflow

1. **Compute trace autocorrelations** (or amplitude spectra) for every trace.
2. **Set up $\mathbf{G}$** once from the acquisition geometry.
3. **For each frequency** solve $\hat{\mathbf{m}}(f) = (\mathbf{G}^\mathsf{T}
   \mathbf{G})^{-1} \mathbf{G}^\mathsf{T} \mathbf{d}(f)$.
4. **Exponentiate** the estimated log-spectra to get amplitude spectra per
   shot, receiver, offset class, and CDP.
5. **Combine factors** for each trace and apply prewhitening.
6. **Reconstruct minimum phase** with the Hilbert transform and inverse-FFT to
   obtain the time-domain operator.
7. **Apply** the operator to the trace.

---

## 10. Connection to the lecture notes

The main lecture notes state the four-factor model and the linear system
$d = Gm$ without deriving them. This document supplies the missing steps:

- why the Fourier/log transform gives a linear system,
- why autocorrelations are used instead of raw spectra,
- how the normal equations arise from least squares,
- why the same $\mathbf{G}$ appears in surface-consistent amplitude
corrections,
- how to go from estimated log-spectra to a usable minimum-phase operator.

---

## Further reading

- Hutchinson & Link (1984), *Surface consistency: A solution to the problem
  of deconvolving noisy seismic data* — original surface-consistent
  deconvolution paper.
- Yilmaz (2001), *Seismic Data Analysis*, Vol. 1, surface-consistent
  deconvolution section.
- Hatton, Worthington & Makin (1986), *Seismic Data Processing: Theory and
  Practice*, Ch. 3.4.1 — practical parameter choices.
- Wiki page on
  [surface-consistent deconvolution](../../wiki/concepts/surface_consistent_deconvolution.md).
