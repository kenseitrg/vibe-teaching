---
title: Derivation of the Linearized Tomographic System
status: draft
---

# Derivation of the Linearized Tomographic System

This document derives the linearized system used in diving-wave (turning-ray) tomography. It is a companion to Term 3 Lecture 2 and expands the geometric discussion of the lecture with the matrix formulation.

## 1. Traveltime as a line integral

In a medium with velocity $v(x,z)$, the slowness is $s(x,z)=1/v(x,z)$. A seismic ray that connects a source at $\mathbf{x}_s$ and a receiver at $\mathbf{x}_r$ has traveltime

$$
t = \int_\text{ray} s\bigl(\mathbf{x}(l)\bigr)\, dl ,
$$

where $l$ is the arclength along the ray.

For a homogeneous medium $v(x,z)=v_0$, the ray is a straight line and the traveltime is simply

$$
t = \frac{\text{path length}}{v_0} = \int_0^L \frac{dl}{v_0} .
$$

When velocity varies, the ray bends according to Snell's law and the integral must follow the curved path.

## 2. Perturbation and linearization

Suppose we have a starting model $s_0(x,z)$ and a starting ray path $\text{ray}_0$. The predicted traveltime is

$$
t_0 = \int_{\text{ray}_0} s_0(l)\, dl .
$$

Let the true slowness differ from the starting model by a small perturbation:

$$
s = s_0 + \delta s .
$$

The true ray also shifts slightly, but to first order the traveltime change depends only on the slowness perturbation integrated along the **unperturbed** ray. This is Fermat's principle: the first-order traveltime change is independent of the first-order ray-path shift.

Therefore

$$
\delta t = t - t_0 \approx \int_{\text{ray}_0} \delta s(l)\, dl .
$$

This is the key linearization that makes tomography practical.

## 3. Discretization into cells

Divide the model into $M$ cells, each with a constant slowness perturbation $\delta s_j$, $j=1,\ldots,M$. For a given ray $i$, let $L_{ij}$ be the length of ray $i$ that lies inside cell $j$. Then

$$
\int_{\text{ray}_i} \delta s(l)\, dl = \sum_{j=1}^{M} L_{ij}\, \delta s_j .
$$

For $N$ observed rays, collect the residuals and unknowns into vectors:

$$
\delta \mathbf{t} = \begin{pmatrix} \delta t_1 \\ \delta t_2 \\ \vdots \\ \delta t_N \end{pmatrix},
\qquad
\delta \mathbf{s} = \begin{pmatrix} \delta s_1 \\ \delta s_2 \\ \vdots \\ \delta s_M \end{pmatrix}.
$$

The $N \times M$ matrix $L$ with entries $L_{ij}$ is the **ray-path length matrix**. The linearized tomographic system is

$$
\delta \mathbf{t} = L \, \delta \mathbf{s} .
$$

Each row of $L$ contains the path lengths of one ray through the model cells; each column corresponds to one cell and shows which rays pass through it.

## 4. Least-squares solution

Usually $N \gg M$ (many more rays than cells), so the system is overdetermined. We solve it in the least-squares sense:

$$
\min_{\delta \mathbf{s}} \left\| \delta \mathbf{t} - L\, \delta \mathbf{s} \right\|^2 .
$$

The normal equations are

$$
L^\top L \, \delta \mathbf{s} = L^\top \delta \mathbf{t} .
$$

If $L^\top L$ is invertible, the solution is

$$
\delta \mathbf{s} = (L^\top L)^{-1} L^\top \delta \mathbf{t} .
$$

In practice $L^\top L$ is often ill-conditioned because some cells are poorly illuminated. The standard remedy is **Tikhonov regularization** (also called damping or smoothing):

$$
\min_{\delta \mathbf{s}} \left\| \delta \mathbf{t} - L\, \delta \mathbf{s} \right\|^2 + \lambda \left\| D \, \delta \mathbf{s} \right\|^2 ,
$$

where $D$ is a finite-difference operator that penalizes rough models. The regularized normal equations are

$$
\bigl( L^\top L + \lambda D^\top D \bigr) \delta \mathbf{s} = L^\top \delta \mathbf{t} ,
$$

and the solution is

$$
\delta \mathbf{s} = \bigl( L^\top L + \lambda D^\top D \bigr)^{-1} L^\top \delta \mathbf{t} .
$$

The parameter $\lambda$ balances data fit against model smoothness. A small $\lambda$ fits the data tightly but may produce an unstable, oscillatory model; a large $\lambda$ gives a smooth model but may leave significant residuals.

## 5. Iterative updating

Tomography is nonlinear because the ray paths depend on the velocity model. The standard strategy is to iterate:

1. Start with $s^{(0)}(x,z)$.
2. For iteration $k$:
   - Trace rays through $s^{(k)}$ to compute $L^{(k)}$ and predicted traveltimes $\mathbf{t}^{(k)}$.
   - Compute residuals $\delta \mathbf{t}^{(k)} = \mathbf{t}_\text{obs} - \mathbf{t}^{(k)}$.
   - Solve the regularized system for $\delta \mathbf{s}^{(k)}$.
   - Update $s^{(k+1)} = s^{(k)} + \delta s^{(k)}$.
3. Stop when residuals stop decreasing.

## 6. Worked example: two rays, two cells

Consider the simplest non-trivial model: two cells and two rays.

Cell slownesses (perturbations): $\delta s_1$, $\delta s_2$.

Ray 1 passes through cell 1 only, with length $L_{11}=1.0$ km.
Ray 2 passes through both cells with lengths $L_{21}=0.5$ km, $L_{22}=0.5$ km.

The system is

$$
\begin{pmatrix} \delta t_1 \\ \delta t_2 \end{pmatrix}
=
\begin{pmatrix} 1.0 & 0.0 \\ 0.5 & 0.5 \end{pmatrix}
\begin{pmatrix} \delta s_1 \\ \delta s_2 \end{pmatrix}.
$$

Suppose the observed residuals are $\delta t_1 = 0.02$ s and $\delta t_2 = 0.015$ s. Then

$$
L^\top L = \begin{pmatrix} 1.0 & 0.5 \\ 0.0 & 0.5 \end{pmatrix}
\begin{pmatrix} 1.0 & 0.0 \\ 0.5 & 0.5 \end{pmatrix}
=
\begin{pmatrix} 1.25 & 0.25 \\ 0.25 & 0.25 \end{pmatrix},
$$

$$
L^\top \delta \mathbf{t} = \begin{pmatrix} 1.0 & 0.5 \\ 0.0 & 0.5 \end{pmatrix}
\begin{pmatrix} 0.02 \\ 0.015 \end{pmatrix}
=
\begin{pmatrix} 0.0275 \\ 0.0075 \end{pmatrix}.
$$

Solving the normal equations gives

$$
\delta s_1 = 0.020 \text{ s/km}, \qquad \delta s_2 = -0.005 \text{ s/km}.
$$

Cell 1 is slower than the starting model (positive slowness perturbation), while cell 2 is slightly faster. The predicted residuals are exactly matched:

$$
\delta t_1 = 1.0 \times 0.020 = 0.020 \text{ s},
\qquad
\delta t_2 = 0.5 \times 0.020 + 0.5 \times (-0.005) = 0.015 \text{ s}.
$$

If we add a small amount of smoothing regularization, the slowness perturbations become more similar (e.g., $\delta s_1 \approx 0.017$, $\delta s_2 \approx 0.004$ for a moderate $\lambda$), reflecting the prior information that near-surface velocities should vary smoothly.

## 7. Quality diagnostics from the matrix

The matrix $L^\top L$ tells us about model resolution and uncertainty:

- **Diagonal entries**: roughly the total ray length through each cell. Small diagonal entries mean poor illumination.
- **Off-diagonal entries**: coupling between cells that share rays. Strong coupling means slowness perturbations are not independently resolvable.
- **Condition number**: the ratio of the largest to smallest singular value of $L^\top L$. A large condition number means the system is unstable and needs regularization.
- **Null space**: directions in model space that produce no traveltime change. These cannot be resolved by traveltime tomography alone.

A checkerboard test is essentially a probe of the resolution matrix $R = (L^\top L + \lambda D^\top D)^{-1} L^\top L$. If $R$ is close to the identity, the model is well resolved; if $R$ smears the pattern, the model is poorly resolved.

## 8. From slowness perturbations to statics

Once the near-surface slowness model is estimated, the static correction for source $i$ and receiver $j$ is computed by integrating the slowness from the acquisition surface to the chosen datum along the near-vertical path:

$$
\Delta t_s(i) = \int_{z_\text{source}}^{z_\text{datum}} s_\text{model}(x_i,z)\, dz,
\qquad
\Delta t_r(j) = \int_{z_\text{receiver}}^{z_\text{datum}} s_\text{model}(x_j,z)\, dz .
$$

For a flat datum with replacement velocity $V_\text{rep}$ this reduces to the familiar elevation static. For a smooth-surface datum, the datum depth varies with $x$ and the integrals are computed trace by trace.

## 9. Summary of the key steps

1. Traveltime along a ray is the integral of slowness.
2. A small slowness perturbation changes the traveltime by its integral along the unperturbed ray (Fermat's principle).
3. Discretize the model into cells; the linear system is $\delta \mathbf{t} = L \, \delta \mathbf{s}$.
4. Solve the regularized least-squares problem because $L^\top L$ is ill-conditioned.
5. Iterate because ray paths depend on the model.
6. Use ray coverage, residuals, and checkerboard tests to judge model quality.
7. Convert the final slowness model into source and receiver statics for the chosen datum.

## References

- Law, B., and Trad, D., 2017, *Comparison of refraction inversion methods*, CREWES Research Report, Vol. 29. Source summary: `wiki/sources/law_trad_comparison_of_refraction_inversion_methods.md`.
- Hill, S. J., 2020, *Introduction to Seismic Processing*, Chapter 22: Statics. Source summary: `wiki/sources/hill_introduction_to_seismic_processing_ch22.md`.
