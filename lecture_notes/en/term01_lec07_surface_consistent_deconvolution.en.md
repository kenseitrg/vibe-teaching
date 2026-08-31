---
title: "Term 1, Lecture 7 — Surface-consistent deconvolution and practical implementation"
author: "Seismic Data Processing Course"
date: "2026"
---

# Term 1, Lecture 7 — Surface-consistent deconvolution and practical implementation

## Learning objectives

After this lecture you should be able to:

1. Explain how surface-consistent deconvolution reduces the near-surface influence on source and receiver wavelets.
2. Write the surface-consistent convolutional model and the linear system $d = Gm$.
3. List the four surface-consistent factors and describe how they enter the trace operator.
4. Choose deconvolution parameters (prediction gap, operator length, prewhitening, analysis window) for a given goal.
5. Implement a simple deterministic deconvolution and a Wiener normal-equation solution in Python/NumPy.
6. Compare deterministic, statistical, predictive, and surface-consistent methods and choose an appropriate flow.

---

## 1. Why trace-by-trace deconvolution is not always enough

In Lecture 6 we designed a single deconvolution operator from one trace. That works well when the signal-to-noise ratio is high, the wavelet is stationary, the reflectivity is white, and we only need a local answer. Real land and OBC data usually violate these assumptions: coupling, near-surface filtering, and noise change from trace to trace, so a trace-by-trace operator is estimated from too few samples and can amplify noise.

**Surface-consistent deconvolution** attacks this problem with a four-factor model. The effective wavelet on a trace is split into

- a **source factor** $s_s(t)$,
- a **receiver factor** $r_r(t)$,
- an **offset factor** $h_h(t)$,
- a **CDP factor** $c_c(t)$.

The source and receiver factors carry the location-dependent, near-surface filtering that we want to compensate. The offset and CDP factors carry the geological response (moveout, AVO, stratigraphy) that we want to keep unchanged. Because every shot and receiver location appears in many traces, the near-surface factors can be estimated far more stably than a separate operator for each trace. Once those factors are removed, a single spiking operator can be used across the survey, which is more stable than trace-by-trace estimates.

---

## 2. The surface-consistent model

### 2.1 Four factors

In the surface-consistent model, the wavelet on each trace is written as a convolution of factors associated with the surface locations that define the trace:

$$
w_{s,r,h,c}(t) = s_s(t) * r_r(t) * h_h(t) * c_c(t),
$$ {#eq:surface-consistent-wavelet}

where

| Symbol | Meaning |
|--------|---------|
| $s_s(t)$ | Source-location wavelet at shot $s$ |
| $r_r(t)$ | Receiver-location wavelet at receiver $r$ |
| $h_h(t)$ | Offset-class wavelet for offset bin $h$ |
| $c_c(t)$ | CDP-location wavelet for CDP $c$ |

The full trace model is

$$
x_{s,r,h,c}(t) = w_{s,r,h,c}(t) * r_{s,r,h,c}(t) + n_{s,r,h,c}(t).
$$ {#eq:surface-consistent-trace}

In the frequency domain, convolution becomes multiplication, and taking logarithms turns multiplication into addition:

$$
\ln X_{s,r,h,c}(f) = \ln S_s(f) + \ln R_r(f) + \ln H_h(f) + \ln C_c(f) + \ln R_{\text{earth}}(f) + \text{noise}.
$$ {#eq:surface-consistent-log}

For a fixed frequency, this is a linear equation in the unknown log-spectra of the surface factors.

### 2.2 Linear system $d = Gm$

Collect all traces for which we have measurements and all unknown surface factors. For one frequency we can write

$$
d = Gm,
$$ {#eq:surface-consistent-system}

where

- $d$ is a vector of observed log-spectra (or autocorrelations, or wavelet spectra) from all traces,
- $m$ is a vector of unknown source, receiver, offset, and CDP log-spectra,
- $G$ is a sparse design matrix with one row per trace and columns indicating which source, receiver, offset, and CDP contribute to that trace.

Each row of $G$ contains exactly four ones (or a subset if some factors are ignored). The system is usually overdetermined because many traces share the same shot or receiver location.

![](figures/term01_lec07/term01_lec07_surface_consistent_model.png){width=80%}

**Figure 1.** Surface-consistent model. The effective wavelet on a trace is the convolution of source, receiver, offset, and CDP factors. Because each surface location appears in many traces, the factors can be estimated more stably than a trace-by-trace operator.

### 2.3 Solving the system

The classical solution is least squares:

$$
m = (G^T G)^{-1} G^T d.
$$ {#eq:ls-solution}

A step-by-step derivation of this system — from the four-factor model through autocorrelations, logarithms, and least-squares minimization — is given in `lecture_notes/derivations/surface_consistent_deconvolution_derivation.en.md`.

Because $G$ is sparse and structured, the normal matrix $G^T G$ has a block structure that can be exploited for efficiency. In practice:

- The system may be solved iteratively (Gauss-Seidel, conjugate gradients) to avoid forming $G^T G$ explicitly.
- Robust norms ($L_1$, Huber, median) reduce the influence of noisy traces and outliers.
- Some implementations estimate amplitude spectra only and then build minimum-phase operators from those spectra.

### 2.4 Parallels with residual statics and surface-consistent amplitude corrections

Surface-consistent deconvolution shares the same geometric structure as two other common processes:

- **Residual statics.** The traveltime shift on a trace is modeled as a sum of source static, receiver static, and residual moveout. The design matrix has the same sparse form.
- **Surface-consistent amplitude corrections.** The trace amplitude is modeled as a product (or sum in log domain) of source, receiver, offset, and structural factors.

All three methods exploit the fact that the same surface location participates in many traces, so local noise averages out.

![](figures/term01_lec07/term01_lec07_surface_consistent_example.png){width=85%}

**Figure 2.** Real-data example. (Left) Trace-by-trace deconvolution: the section is noisier and events are less continuous because each trace is processed independently. (Right) Surface-consistent deconvolution: source and receiver factors are estimated from many traces, giving a more stable result with better event continuity.

---

## 3. Deconvolution parameters in practice

### 3.1 Prediction gap (minimum lag)

| Gap | Effect |
|-----|--------|
| 1 sample | Spiking deconvolution; full wavelet compression |
| A few samples | Partial compression, less noise amplification |
| Water-layer two-way time | Reverberation suppression |
| Longer | Multiple suppression, little wavelet compression |

A useful rule: pick the gap from the autocorrelation. The first zero crossing or the lag of the first strong repetitive peak guides the choice. Choosing the **second zero crossing** leaves the signal spectrum almost unchanged while suppressing short-period multiples.

### 3.2 Operator length

- Too short: the wavelet is not fully compressed.
- Too long: noise and non-stationarity leak into the operator.
- Rule of thumb: roughly the length of the embedded wavelet, often 80–200 ms for spiking deconvolution.

Hatton et al. describe the ideal operator as a "dinosaur": thick in the middle and thin at both ends.

### 3.3 Prewhitening

Start with a small value (0.1%) for numerical stability. Increase to 1–5% if the data are noisy or if the operator spectrum has large spikes. Always check the operator spectrum for narrow peaks, which indicate amplification of noise.

### 3.4 Analysis window

The window should:

- contain strong signal (reflections, not noise),
- avoid multiples, ground roll, first breaks, and guided-wave zones,
- be short enough to be stationary,
- be long enough to give reliable statistics,
- have amplitudes balanced by a smooth gain function.

![](figures/term01_lec07/term01_lec07_parameter_scan.png){width=85%}

**Figure 3.** Effect of prediction gap and operator length. A small gap compresses the wavelet; a gap matched to the reverberation period suppresses multiples; a very long operator amplifies noise.

---

## 4. Practical implementation in Python

The ideas of deconvolution are just matrix operations. Below are two self-contained examples.

### 4.1 Deterministic deconvolution by spectral division

```python
import numpy as np
import matplotlib.pyplot as plt


def deterministic_decon(trace, wavelet, dt, eps=0.05):
    """
    Deterministic deconvolution by prewhitened spectral division.

    Parameters
    ----------
    trace : 1-D array
        Input seismic trace.
    wavelet : 1-D array
        Known wavelet (same length as trace or shorter).
    dt : float
        Sample interval in seconds.
    eps : float
        Prewhitening fraction (relative to max power).

    Returns
    -------
    decon : 1-D array
        Deconvolved trace.
    """
    n = len(trace)
    W = np.fft.rfft(wavelet, n=n)
    X = np.fft.rfft(trace, n=n)
    power = np.max(np.abs(W) ** 2)
    F = np.conj(W) / (np.abs(W) ** 2 + eps ** 2 * power)
    R = X * F
    decon = np.fft.irfft(R, n=n)
    return decon
```

The key line is

$$
F(f) = \frac{W^*(f)}{|W(f)|^2 + \varepsilon^2 \max |W|^2}.
$$

Without the $\varepsilon^2$ term, any notch in the wavelet spectrum would blow up the inverse filter.

### 4.2 Wiener spiking deconvolution as a matrix operation

```python
import numpy as np
from numpy.linalg import solve


def wiener_spiking_operator(trace, n_op, eps=0.01):
    """
    Design a Wiener spiking-deconvolution operator.

    Parameters
    ----------
    trace : 1-D array
        Input seismic trace.
    n_op : int
        Operator length in samples.
    eps : float
        Prewhitening fraction added to the diagonal.

    Returns
    -------
    f : 1-D array
        Spiking operator.
    """
    n = len(trace)
    acorr = np.correlate(trace, trace, mode="full")
    acorr = acorr[n - 1:]                 # lags 0, 1, ..., n-1

    # Build symmetric Toeplitz autocorrelation matrix
    R = np.zeros((n_op, n_op))
    for i in range(n_op):
        for j in range(n_op):
            R[i, j] = acorr[abs(i - j)]

    # Prewhitening
    R += eps * np.eye(n_op) * acorr[0]

    # Desired output = spike at lag 0
    d = np.zeros(n_op)
    d[0] = acorr[0]

    # Solve normal equations
    f = solve(R, d)
    return f
```

The code implements exactly the matrix equation from Lecture 6:

$$
\mathbf{R} \mathbf{f} = \mathbf{d}.
$$ {#eq:normal-eq-code}

Because $\mathbf{R}$ is Toeplitz, a production implementation would use the Levinson-Durbin recursion instead of a general solver. For teaching, the direct matrix form makes the operation transparent.

### 4.3 Tiny surface-consistent system

```python
import numpy as np
from numpy.linalg import lstsq

# Three shots (S0,S1,S2), three receivers (R0,R1,R2)
# Four traces:
#   T0: S0-R0, T1: S0-R1, T2: S1-R0, T3: S2-R2
G = np.array([
    [1, 0, 0, 1, 0, 0],   # S0, R0
    [1, 0, 0, 0, 1, 0],   # S0, R1
    [0, 1, 0, 1, 0, 0],   # S1, R0
    [0, 0, 1, 0, 0, 1],   # S2, R2
])

# Observed log-amplitude spectra at one frequency (dummy values)
d = np.array([2.0, 1.8, 1.5, 0.9])

m, *_ = lstsq(G, d, rcond=None)
source_terms = m[:3]
receiver_terms = m[3:]
```

The same pattern scales to thousands of shots and receivers.

---

## 5. Choosing a deconvolution flow

The right method depends on what distorts the data and what prior information is available.

| Problem | Recommended method | Why |
|---------|-------------------|-----|
| Known source signature | Deterministic designature | Uses measured information directly |
| Bubble energy / reverberations | Predictive deconvolution | Targets predictable repetitive energy |
| Noisy land data, variable coupling | Surface-consistent deconvolution | Averages over surface locations |
| General wavelet compression | Spiking / Wiener deconvolution | No wavelet measurement needed |
| Vibroseis data | Convert to minimum phase, then spiking | Makes phase assumptions valid |

For **land and OBC data**, surface-consistent deconvolution is generally preferred because source and receiver coupling and the near surface vary strongly across the survey.

A typical **marine** flow is:

```text
raw data
  → deterministic designature
  → deghosting
  → predictive deconvolution (reverberations)
  → final zero-phase shaping
```

A typical **land** flow focuses on deconvolution:

```text
raw data
  → minimum-phase conversion (vibroseis data)
  → inverse filtering for instrument signature
  → surface-consistent deconvolution
  → zero-phasing
```

The order matters: deterministic methods that use measured information usually come first; statistical methods that make strong assumptions come after the data have been conditioned.

---

## 6. Summary

- Trace-by-trace deconvolution is noisy and unstable when data quality or coupling varies.
- Surface-consistent deconvolution uses a four-factor model to separate near-surface source/receiver effects from geological offset/CDP effects, and solves a sparse linear system.
- For land and OBC data it is the preferred deconvolution approach because it compensates variable near-surface filtering.
- Parameter choices (gap, length, prewhitening, window) control the trade-off between wavelet compression, multiple suppression, and noise amplification.
- Deterministic deconvolution and Wiener filtering are straightforward matrix/spectral operations in Python.
- The choice of method should follow the wavelet model and the available prior information: designature and deghosting first for marine data, minimum-phase conversion and instrument correction first for land data.

---

## Comprehension questions

1. Why does surface-consistent deconvolution need more than one trace per source or receiver location?
2. What happens to a spiking-deconvolution operator if the analysis window contains strong ground roll?
3. When would you prefer deterministic deconvolution over statistical deconvolution?
4. How does prewhitening affect the deconvolved spectrum at frequencies where the signal is weak?
5. What is the parallel between surface-consistent deconvolution and residual statics?
6. Why is a long operator not always better than a short operator?

---

## Practical exercises

1. Implement `deterministic_decon(trace, wavelet, dt, eps)` and apply it to a synthetic trace. Vary `eps` and describe the effect on the output.
2. Implement `wiener_spiking_operator(trace, n_op, eps)` and compare the operator designed from a clean trace with one designed from a noisy trace.
3. Build the tiny surface-consistent matrix shown in Section 4.3 and verify that you can recover the source and receiver terms.
4. Add a non-minimum-phase component to the synthetic wavelet in Exercise 1. Does deterministic deconvolution with a causal inverse still give a good result?

---

## Further reading

- Hutchinson \& Link (1984), *Surface consistency: A solution to the problem of deconvolving noisy seismic data*.
- Yilmaz (2001), *Seismic Data Analysis*, Vol. 1, surface-consistent deconvolution section.
- Hatton, Worthington \& Makin (1986), *Seismic Data Processing: Theory and Practice*, Ch. 3.4.1.
