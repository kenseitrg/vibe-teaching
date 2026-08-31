# Derivation of the Gauss–Seidel solution for the surface-consistent residual-statics system

This document gives a step-by-step derivation of the Gauss–Seidel iteration used to solve the surface-consistent residual-statics problem. It is intended as supplementary reading for students who want to see how the design matrix is built and why the iterative update formulas are just averaging over the appropriate traces.

> **Prerequisites.** Basic linear algebra: systems of equations, matrix-vector notation, and least-squares minimisation. The derivations use only summations and averages; no advanced optimisation theory is needed.

---

## 1. The 4-component residual-statics model

For a single trace with source $i$, receiver $j$, offset class $k$, and CMP $l$, the measured residual time shift $d_{ijkl}$ is modelled as the sum of four components plus noise:

$$
d_{ijkl} = s_i + r_j + h_k + c_l + \epsilon_{ijkl},
$$

where

- $s_i$ = source static for source $i$,
- $r_j$ = receiver static for receiver $j$,
- $h_k$ = offset-class residual moveout for offset class $k$,
- $c_l$ = CMP structural (geological) term for CMP $l$,
- $\epsilon_{ijkl}$ = residual error.

The $c_l$ term is **not** a static shift; it represents the true two-way time of the reflector at CMP $l$. It must be estimated and removed so that the static solution does not absorb geology.

---

## 2. Collecting all traces into a linear system

Suppose we have $N_s$ sources, $N_r$ receivers, $N_h$ offset classes, and $N_c$ CMPs. Each recorded trace gives one equation. Collecting all traces, we can write the system in matrix form as

$$
\mathbf{d} = G \mathbf{m} + \boldsymbol{\epsilon},
$$

where

- $\mathbf{d}$ is a vector of length $N_{\text{tr}}$ containing every measured shift $d_{ijkl}$,
- $\mathbf{m}$ is a vector of length $N_s + N_r + N_h + N_c$ containing all unknown components,
- $G$ is the $N_{\text{tr}} \times (N_s + N_r + N_h + N_c)$ **design matrix**,
- $\boldsymbol{\epsilon}$ is the noise vector.

### 2.1 Structure of the design matrix

Each row of $G$ corresponds to one trace and has exactly four ones: in the columns for the source, receiver, offset class, and CMP of that trace. All other entries are zero.

For example, consider the four-trace survey used in the worked example in §6. The design matrix has one row per trace and one column per source, receiver, offset class, and CMP. Because there is only one offset class, the offset-class block is a single column of ones. With the trace order from §6, the matrix is

$$
G = \begin{bmatrix}
1 & 0 & 1 & 0 & 1 & 1 & 0 \\
1 & 0 & 0 & 1 & 1 & 0 & 1 \\
0 & 1 & 1 & 0 & 1 & 0 & 1 \\
0 & 1 & 0 & 1 & 1 & 1 & 0
\end{bmatrix},
$$

with the column order $(s_1, s_2, r_1, r_2, h_1, c_1, c_2)$. Each row therefore has exactly four ones: one in the source block, one in the receiver block, one in the offset-class block, and one in the CMP block.

For a realistic 2-D seismic line, $N_{\text{tr}}$ can be hundreds of thousands while the number of unknowns is only a few thousand. The matrix is therefore **very tall and sparse**.

---

## 3. Least-squares objective

We want the unknown vector $\mathbf{m}$ that best predicts the measured shifts. The least-squares objective is

$$
\Phi(\mathbf{m}) = \| \mathbf{d} - G \mathbf{m} \|^2
                = \sum_{\text{all traces}} \left( d_{ijkl} - s_i - r_j - h_k - c_l \right)^2.
$$

Minimising $\Phi$ with respect to each unknown would require solving the normal equations

$$
G^\top G \, \mathbf{m} = G^\top \mathbf{d}.
$$

The matrix $G^\top G$ has size $(N_s + N_r + N_h + N_c) \times (N_s + N_r + N_h + N_c)$. Although it is much smaller than $G$, it is still enormous for a real survey, and it is **close to singular** because the columns of $G$ are not independent. Direct inversion is therefore impractical.

> **Why $G^\top G$ is singular.** If we add a constant $a$ to every source static $s_i$ and subtract the same constant $a$ from every receiver static $r_j$, every trace equation $s_i + r_j$ is unchanged. The same kind of ambiguity exists for smooth long-wavelength trends. This is why the system is **under-constrained** and must be supplied with constraints such as zero mean before solving.

---

## 4. Gauss–Seidel iteration

Gauss–Seidel is a natural way to solve this large, sparse, block-structured system. The idea is to update one class of components at a time while holding the others fixed. Because the update for each class is just an average over the relevant traces, the algorithm is easy to implement and converges quickly.

### 4.1 General update rule

Suppose we hold all components except the source statics fixed. The objective becomes a sum of terms each depending on only one source static $s_i$:

$$
\Phi(s_i) = \sum_{\text{traces with source } i} \left( d_{ijkl} - s_i - r_j - h_k - c_l \right)^2.
$$

Differentiating with respect to $s_i$ and setting the result to zero gives

$$
\sum_{\text{traces with source } i} \left( d_{ijkl} - s_i - r_j - h_k - c_l \right) = 0.
$$

Solving for $s_i$:

$$
s_i = \frac{1}{N_i} \sum_{\text{traces with source } i} \left( d_{ijkl} - r_j - h_k - c_l \right),
$$

where $N_i$ is the number of traces with source $i$. In words: **the updated source static is the average of the residuals left after removing the current receiver, offset, and CMP estimates.**

Exactly the same argument gives the updates for the other three classes:

$$
r_j = \frac{1}{N_j} \sum_{\text{traces with receiver } j} \left( d_{ijkl} - s_i - h_k - c_l \right),
$$

$$
h_k = \frac{1}{N_k} \sum_{\text{traces with offset class } k} \left( d_{ijkl} - s_i - r_j - c_l \right),
$$

$$
c_l = \frac{1}{N_l} \sum_{\text{traces with CMP } l} \left( d_{ijkl} - s_i - r_j - h_k \right).
$$

### 4.2 Iteration with source and receiver set to zero first

One convenient starting point is to set all source and receiver components to zero and estimate the CMP terms first. The CMP update with $s_i = 0$ and $r_j = 0$ is simply

$$
c_l^{(0)} = \frac{1}{N_l} \sum_{\text{traces with CMP } l} d_{ijkl}.
$$

This is the **average measured shift in each CMP gather**. It captures the local structure and any near-surface trend that is shared within the gather.

With these CMP estimates fixed, we then update the source and receiver statics:

$$
s_i^{(1)} = \frac{1}{N_i} \sum_{\text{traces with source } i} \left( d_{ijkl} - r_j^{(0)} - h_k^{(0)} - c_l^{(0)} \right),
$$

$$
r_j^{(1)} = \frac{1}{N_j} \sum_{\text{traces with receiver } j} \left( d_{ijkl} - s_i^{(1)} - h_k^{(0)} - c_l^{(0)} \right).
$$

Note that $s_i^{(1)}$ is used immediately in the receiver update; this is the Gauss–Seidel property (use the latest available estimate).

For the offset term, if it is included, the update is

$$
h_k^{(1)} = \frac{1}{N_k} \sum_{\text{traces with offset class } k} \left( d_{ijkl} - s_i^{(1)} - r_j^{(1)} - c_l^{(0)} \right).
$$

### 4.3 Next iteration: feed the updated statics back into the CMP estimate

At the start of the next iteration, we re-estimate the CMP terms using the newly updated source and receiver statics:

$$
c_l^{(1)} = \frac{1}{N_l} \sum_{\text{traces with CMP } l} \left( d_{ijkl} - s_i^{(1)} - r_j^{(1)} - h_k^{(1)} \right).
$$

This is the key feedback step: the CMP estimates are improved because the source and receiver statics have been partially removed. The cycle then repeats:

$$
\text{update } c \rightarrow \text{update } s \rightarrow \text{update } r \rightarrow \text{update } h \rightarrow \text{update } c \rightarrow \cdots
$$

Each sweep lowers the least-squares objective until the estimates stop changing.

> **Order of updates.** The order is not unique. Source updates are often performed before receiver updates because source fold is usually higher than receiver fold, giving more stable early estimates. Whatever order is chosen, Gauss–Seidel converges as long as the latest estimates are used immediately.

---

## 5. Connection to the normal equations

Each Gauss–Seidel update is exactly one step of block-coordinate descent on the least-squares objective. Holding all blocks except one fixed, the update sets the partial derivative of $\Phi$ with respect to that block to zero. Because the objective is quadratic, this zero-gradient condition is the same as the corresponding block of the normal equations. Repeating the block updates is therefore equivalent to solving the normal equations iteratively without ever forming the full matrix $G^\top G$.

---

## 6. Worked numerical example

Consider a tiny survey with 2 sources, 2 receivers, 1 offset class, and 2 CMPs. The acquisition geometry is:

| Trace | Source $i$ | Receiver $j$ | Offset class $k$ | CMP $l$ | Measured shift $d$ (ms) |
|-------|------------|--------------|------------------|---------|---------------------------|
| 1 | 1 | 1 | 1 | 1 | 12 |
| 2 | 1 | 2 | 1 | 2 | 8 |
| 3 | 2 | 1 | 1 | 2 | 5 |
| 4 | 2 | 2 | 1 | 1 | 7 |

There are $2 + 2 + 1 + 2 = 7$ unknowns and 4 equations, so the system is highly overdetermined in a relative sense; here the small size is just for illustration. We will set the offset term to zero and not update it, to keep the example compact. The unknowns are then $s_1, s_2, r_1, r_2, c_1, c_2$.

### 6.1 Initialisation

Set all source and receiver statics to zero:

$$
s_1^{(0)} = s_2^{(0)} = r_1^{(0)} = r_2^{(0)} = 0.
$$

Estimate CMP terms as the average measured shift in each CMP:

$$
c_1^{(0)} = \frac{d_1 + d_4}{2} = \frac{12 + 7}{2} = 9.5 \text{ ms},
$$

$$
c_2^{(0)} = \frac{d_2 + d_3}{2} = \frac{8 + 5}{2} = 6.5 \text{ ms}.
$$

### 6.2 First source update

Source 1 appears in traces 1 and 2:

$$
s_1^{(1)} = \frac{1}{2} \big[ (d_1 - r_1^{(0)} - c_1^{(0)}) + (d_2 - r_2^{(0)} - c_2^{(0)}) \big]
        = \frac{1}{2} \big[ (12 - 0 - 9.5) + (8 - 0 - 6.5) \big]
        = \frac{1}{2}(2.5 + 1.5) = 2.0 \text{ ms}.
$$

Source 2 appears in traces 3 and 4:

$$
s_2^{(1)} = \frac{1}{2} \big[ (d_3 - r_1^{(0)} - c_2^{(0)}) + (d_4 - r_2^{(0)} - c_1^{(0)}) \big]
        = \frac{1}{2} \big[ (5 - 0 - 6.5) + (7 - 0 - 9.5) \big]
        = \frac{1}{2}(-1.5 - 2.5) = -2.0 \text{ ms}.
$$

### 6.3 First receiver update (using the updated source statics)

Receiver 1 appears in traces 1 and 3:

$$
r_1^{(1)} = \frac{1}{2} \big[ (d_1 - s_1^{(1)} - c_1^{(0)}) + (d_3 - s_2^{(1)} - c_2^{(0)}) \big]
        = \frac{1}{2} \big[ (12 - 2.0 - 9.5) + (5 - (-2.0) - 6.5) \big]
        = \frac{1}{2}(0.5 + 0.5) = 0.5 \text{ ms}.
$$

Receiver 2 appears in traces 2 and 4:

$$
r_2^{(1)} = \frac{1}{2} \big[ (d_2 - s_1^{(1)} - c_2^{(0)}) + (d_4 - s_2^{(1)} - c_1^{(0)}) \big]
        = \frac{1}{2} \big[ (8 - 2.0 - 6.5) + (7 - (-2.0) - 9.5) \big]
        = \frac{1}{2}(-0.5 - 0.5) = -0.5 \text{ ms}.
$$

### 6.4 Second CMP estimate (feedback step)

Now re-estimate the CMP terms using the updated source and receiver statics:

$$
c_1^{(1)} = \frac{1}{2} \big[ (d_1 - s_1^{(1)} - r_1^{(1)}) + (d_4 - s_2^{(1)} - r_2^{(1)}) \big]
        = \frac{1}{2} \big[ (12 - 2.0 - 0.5) + (7 - (-2.0) - (-0.5)) \big]
        = \frac{1}{2}(9.5 + 9.5) = 9.5 \text{ ms}.
$$

$$
c_2^{(1)} = \frac{1}{2} \big[ (d_2 - s_1^{(1)} - r_2^{(1)}) + (d_3 - s_2^{(1)} - r_1^{(1)}) \big]
        = \frac{1}{2} \big[ (8 - 2.0 - (-0.5)) + (5 - (-2.0) - 0.5) \big]
        = \frac{1}{2}(6.5 + 6.5) = 6.5 \text{ ms}.
$$

In this tiny example, the CMP estimates did not change after one sweep because the data are perfectly consistent with the model. In real data, the CMP estimates would continue to adjust until convergence.

### 6.5 Final residual

Using the estimates after one sweep, the predicted shift for each trace is:

| Trace | $s_i^{(1)} + r_j^{(1)} + c_l^{(1)}$ | Predicted (ms) | Measured (ms) | Residual (ms) |
|-------|--------------------------------------|----------------|---------------|---------------|
| 1 | $2.0 + 0.5 + 9.5$ | 12.0 | 12 | 0.0 |
| 2 | $2.0 - 0.5 + 6.5$ | 8.0 | 8 | 0.0 |
| 3 | $-2.0 + 0.5 + 6.5$ | 5.0 | 5 | 0.0 |
| 4 | $-2.0 - 0.5 + 9.5$ | 7.0 | 7 | 0.0 |

The model exactly fits the four measured shifts with six unknowns, but the solution is not unique: we could add $1$ ms to both source statics and subtract $1$ ms from both receiver statics without changing any predicted shift. This illustrates the under-constrained nature of the system.

---

## 7. The zero-mean constraint

Because the solution is under-constrained, a constraint is applied before iteration begins. The most common choice is to force the source and receiver statics to have zero mean:

$$
\sum_i s_i = 0, \qquad \sum_j r_j = 0.
$$

This removes the ambiguity of adding a constant to sources and subtracting it from receivers. In the worked example, the source statics $(2.0, -2.0)$ and receiver statics $(0.5, -0.5)$ already have zero mean, so no additional adjustment is needed.

If the initial unconstrained estimates do not have zero mean, subtract the mean from each class before the next iteration:

$$
s_i \leftarrow s_i - \frac{1}{N_s} \sum_i s_i, \qquad
r_j \leftarrow r_j - \frac{1}{N_r} \sum_j r_j.
$$

The mean that is removed represents the long-wavelength static component. It is not discarded: it is handled separately by field statics, layer replacement, or a floating datum.

---

## 8. Summary

- The residual-statics problem is a large, sparse, overdetermined linear system $\mathbf{d} = G \mathbf{m} + \boldsymbol{\epsilon}$.
- Directly inverting $G^\top G$ is impractical because the matrix is huge and close to singular.
- Gauss–Seidel solves the system by updating one component class at a time while holding the others fixed.
- Each update is an **average** of the residuals after removing the current estimates of the other classes.
- A typical sweep starts with source and receiver statics set to zero, estimates the CMP terms as averages, then updates source and receiver statics, and feeds the updated values back into the next CMP estimate.
- The zero-mean constraint removes the under-constrained ambiguity and keeps the long-wavelength component separate from the residual statics.

## References

- Hatton, Worthington & Makin (1986), *Seismic Data Processing: Theory and Practice*, Section 5.10.
- Li (1999), *Residual statics analysis using prestack equivalent offset migration*, University of Calgary, Chapter 2.
- Taner, Koehler & Alhilali (1974), "Estimation and correction of near-surface time anomalies", *Geophysics*.
- Wiggins, Larner & Wisecup (1976), "Residual statics analysis as a general linear inverse problem", *Geophysics*.
