---
title: Surface-related multiple elimination (SRME)
status: draft
sources:
  - verschuur_2006_eet05_principles_srme
  - verschuur_2006_eet06_practical_srme
  - tang2017_5d_mpfi_srme
tags: [multiples, srme, surface-related, prediction, convolution, feedback]
---

# Surface-related multiple elimination (SRME)

**SRME** predicts surface-related multiples from the data themselves — no subsurface model, no velocity model — by multidimensional convolution of the measured reflection response with itself. It is the canonical *data-driven, wave-equation-based* prediction method: multiples are not filtered out by discrimination, they are *modelled* and subtracted.

## Core idea (1D, normal incidence)

Every surface-related multiple is two (or more) primaries connected at the surface reflection point. Combining two primaries means:

- **travel times add**, and
- **amplitudes multiply** (times the surface reflection coefficient $r_0 = -1$),

which is a **convolution in time**:

$$
m_1(t) = -x_0(t) * x_0(t), \qquad
m_2(t) = +x_0 * x_0 * x_0, \;\ldots
$$

The total measured response is a **feedback system**: each loop through the free surface adds one order of multiples:

$$
x(t) = x_0(t) - x_0(t) * x(t)
$$

From which the multiple-free response follows:

- **Implicit form:** $x_0(t) = x(t) + x_0(t) * x(t)$
- **Explicit series (removal):** $x_0(t) = x(t) + x(t)*x(t) + x(t)*x(t)*x(t) + \dots$ — multiple removal by auto-convolution and summation of the input (Neumann series).
- **Iterative form:** $p_0^{(i+1)} = p - a * p_0^{(i)} * p$, start $p_0^{(0)} = p$; each iteration strips one more multiple order.

## The wavelet problem

With a source signature $s(t)$ instead of an impulse, each convolution multiplies the spectrum by $S(f)$ once more, so a **surface operator** $a(t) = -[s(t)]^{-1}$ must pre-scale each convolution:

$$
p_0(t) = p(t) - a*p*p + a*a*p*p*p - \dots
$$

In practice $s(t)$ is imperfectly known and 2D directivity is neglected → predicted multiples are kinematically right but dynamically wrong → **adaptive subtraction** is mandatory.

## 2D formulation

A multiple from source $x_s$ to receiver $x_r$ with surface (downward) reflection point $x_k$ is predicted by convolving two traces: the shot-gather trace $P(x_k, x_s)$ and the receiver-gather trace $P(x_r, x_k)$. All possible reflection points contribute — integrate over the surface:

$$
M(x_r, x_s; f) = A(f) \int P(x_r, x_k; f)\, P(x_k, x_s; f)\, dx_k
$$

Per frequency this is a matrix multiplication $\mathbf{M} = \mathbf{P}\mathbf{P}$ (operator = data). The integrand as a function of $x_k$ is the **multiple contribution gather**; its apex marks the actual surface reflection point of each multiple event.

## Practical requirements and limitations

- **Needs all shots and all near offsets**: prediction integrates over the whole surface; missing near offsets or coarse/irregular shooting create prediction artifacts (limited-aperture effects grow for later reverberations). Fixes: reciprocity, shot interpolation, near-offset reconstruction (Radon extrapolation), 5D regularization.
- **Data regularity & spatial sampling**: spatial aliasing in the operator smears the prediction.
- **Wavelet/directivity**: convolution adds wavelets; needs deconvolved/deghosted input and adaptive subtraction.
- **Land data**: ground roll, statics, amplitude imbalance and sparse shooting make the raw data unusable as operator; SRME needs a dedicated preprocessed copy of the data *for prediction only* (statics, ground-roll filtering, amplitude balancing, α-trimmed medians). Dilemma: multiples are generated at the true surface (no statics) while data require statics correction.
- **Shallow water**: the water-bottom primary lives in the near-offset gap; SRME is combined with FK filtering of post-critical water-bottom events, predictive deconvolution for water-layer reverberations, and Radon for residuals.
- **Internal multiples**: SRME removes surface-related multiples only; internal multiples need other methods (e.g. IME / Marchenko, beyond the course scope).

## Position in the method landscape

| | Discrimination methods (Radon/FK) | Prediction methods (decon, SRME) |
|---|---|---|
| Physics exploited | moveout/dip difference | periodicity / primary composition |
| Needs velocity model | yes (NMO) | no (SRME) / partially |
| Near offsets | weak (no moveout diff.) | essential input |
| Output | filtered data | multiple model + adaptive subtraction |

Related: [Multiples](multiples.md), [Adaptive subtraction](adaptive_subtraction.md), [Seismic data regularization](seismic_data_regularization.md), [Radon interpolation](radon_interpolation.md), [Predictive deconvolution](predictive_deconvolution.md).
