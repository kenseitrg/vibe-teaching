# A Short Primer on the Singular Value Decomposition

This note reviews the **singular value decomposition** (SVD) of a matrix. It is
intended as a refresher for students who have already seen eigenvalues and
eigenvectors, and who now need the SVD for seismic noise attenuation by
rank-reduction. 

> **Prerequisites.** Basic matrix multiplication, transposes, orthogonality, and
eigenvalues/eigenvectors of symmetric matrices. No prior knowledge of the SVD is
assumed.

---

## 1. The basic idea: write a matrix as a sum of rank-one pieces

A matrix $A$ of size $m \times n$ has $mn$ entries. The simplest kind of matrix
is **rank one**: every row is a multiple of the same row, and every column is a
multiple of the same column. Such a matrix can always be written as an outer
product

$$
\mathbf{u} \mathbf{v}^{\mathsf{T}} = \begin{bmatrix} u_1 \\ u_2 \\ \vdots \\ u_m \end{bmatrix}
\begin{bmatrix} v_1 & v_2 & \cdots & v_n \end{bmatrix}.
$$

The SVD says that **any** matrix $A$ can be decomposed into a sum of rank-one
pieces, chosen so that the pieces are mutually orthogonal and ordered by
importance:

$$
A = \sigma_1 \mathbf{u}_1 \mathbf{v}_1^{\mathsf{T}} + \sigma_2 \mathbf{u}_2 \mathbf{v}_2^{\mathsf{T}} + \cdots + \sigma_r \mathbf{u}_r \mathbf{v}_r^{\mathsf{T}}.
$$

The number of non-zero terms, $r$, is the **rank** of $A$. The positive scalars
$\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_r > 0$ are the **singular
values**; the vectors $\mathbf{u}_i$ and $\mathbf{v}_i$ are the **left** and **right singular
vectors**.

> **Why this is useful.** If the signal we care about is simple (low-rank) and
the noise is complicated, the signal tends to sit in the first few pieces while
the noise is pushed into the later pieces. Keeping only the leading pieces is
the idea behind SVD-based noise attenuation.

---

## 2. The full SVD theorem

Collect the singular vectors into matrices:

- $\mathbf{U} = [\mathbf{u}_1 \; \mathbf{u}_2 \; \cdots \; \mathbf{u}_m]$ is an $m \times m$ **orthogonal** matrix
  ($\mathbf{U}^{\mathsf{T}} \mathbf{U} = \mathbf{I}$). Its columns are eigenvectors of $A A^{\mathsf{T}}$.
- $\mathbf{V} = [\mathbf{v}_1 \; \mathbf{v}_2 \; \cdots \; \mathbf{v}_n]$ is an $n \times n$ **orthogonal** matrix
  ($\mathbf{V}^{\mathsf{T}} \mathbf{V} = \mathbf{I}$). Its columns are eigenvectors of $A^{\mathsf{T}} A$.
- $\boldsymbol{\Sigma}$ is an $m \times n$ diagonal matrix with the singular values
  $\sigma_1, \sigma_2, \ldots, \sigma_r$ on the diagonal and zeros elsewhere.

Then the SVD is written compactly as

$$
\boxed{ \; A = \mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^{\mathsf{T}}. \; }
$$

For computations with a rank-$r$ matrix, the **reduced (economy) SVD** is
usually enough:

$$
A = \mathbf{U}_r \boldsymbol{\Sigma}_r \mathbf{V}_r^{\mathsf{T}},
$$

where $\mathbf{U}_r$ is $m \times r$, $\boldsymbol{\Sigma}_r$ is $r \times r$, and $\mathbf{V}_r$ is $n \times r$.

---

## 3. Where the pieces come from

The connection back to ordinary eigenvalue problems is:

- The eigenvalues of $A^{\mathsf{T}} A$ and of $A A^{\mathsf{T}}$ are the same
  non-negative numbers $\lambda_1, \lambda_2, \ldots, \lambda_r$.
- The singular values are their square roots:

  $$
  \sigma_i = \sqrt{\lambda_i}.
  $$

- The right singular vectors $\mathbf{v}_i$ are the unit eigenvectors of
  $A^{\mathsf{T}} A$.
- The left singular vectors $\mathbf{u}_i$ are obtained from

  $$
  \mathbf{u}_i = \frac{1}{\sigma_i} A \mathbf{v}_i,
  $$

  and they are unit eigenvectors of $A A^{\mathsf{T}}$.

This is why the SVD always exists, even for rectangular or non-symmetric
matrices: $A^{\mathsf{T}} A$ and $A A^{\mathsf{T}}$ are symmetric and positive
semidefinite, so their eigenvectors are orthogonal and their eigenvalues are
real and non-negative.

---

## 4. Low-rank approximation

Writing $A$ as a sum of rank-one pieces makes the best approximation of a given
rank obvious: just keep the leading terms. If we keep only the first $k$ pieces
($k < r$), we obtain the rank-$k$ approximation

$$
A_k = \sigma_1 \mathbf{u}_1 \mathbf{v}_1^{\mathsf{T}} + \sigma_2 \mathbf{u}_2 \mathbf{v}_2^{\mathsf{T}} + \cdots + \sigma_k \mathbf{u}_k \mathbf{v}_k^{\mathsf{T}}.
$$

This is the closest rank-$k$ matrix to $A$ in the Frobenius norm (the
Eckart–Young–Mirsky theorem). The error is the sum of squares of the discarded
singular values:

$$
\| A - A_k \|_{F}^{2} = \sigma_{k+1}^{2} + \sigma_{k+2}^{2} + \cdots + \sigma_r^{2}.
$$

So the singular values tell us both the importance of each piece and the
approximation error we incur by discarding it.

---

## 5. Worked example: $A = \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix}$

This is Strang's Example 3 in Section 7.2. The matrix has full rank $r = 2$.

**Step 1. Compute $A^{\mathsf{T}} A$ and $A A^{\mathsf{T}}$.**

$$
A^{\mathsf{T}} A = \begin{bmatrix} 3 & 4 \\ 0 & 5 \end{bmatrix}
\begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix}
= \begin{bmatrix} 25 & 20 \\ 20 & 25 \end{bmatrix},
\qquad
A A^{\mathsf{T}} = \begin{bmatrix} 9 & 12 \\ 12 & 41 \end{bmatrix}.
$$

Both have trace $50$. Their determinants agree because $A^{\mathsf{T}} A$ and
$A A^{\mathsf{T}}$ share the same non-zero eigenvalues:

$$
\det(A^{\mathsf{T}} A) = 25 \cdot 25 - 20^{2} = 225, \qquad
\det(A A^{\mathsf{T}}) = 9 \cdot 41 - 12^{2} = 225.
$$

**Step 2. Eigenvalues and singular values.**

The eigenvalues of $A^{\mathsf{T}} A$ satisfy

$$
\det(A^{\mathsf{T}} A - \lambda I) = (25 - \lambda)^{2} - 20^{2} = 0,
$$

so $\lambda_1 = 45$ and $\lambda_2 = 5$. Thus

$$
\sigma_1 = \sqrt{45} = 3\sqrt{5}, \qquad \sigma_2 = \sqrt{5}.
$$

Notice that $\sigma_1 \sigma_2 = \sqrt{45 \cdot 5} = 15 = |\det A|$, which is a
general fact for square matrices.

**Step 3. Right singular vectors $\mathbf{v}_i$ (eigenvectors of $A^{\mathsf{T}} A$).**

For $\lambda_1 = 45$:

$$
(A^{\mathsf{T}} A - 45I)\mathbf{v} = \begin{bmatrix} -20 & 20 \\ 20 & -20 \end{bmatrix} \mathbf{v} = 0
\quad \Rightarrow \quad \mathbf{v}_1 = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 \\ 1 \end{bmatrix}.
$$

For $\lambda_2 = 5$:

$$
(A^{\mathsf{T}} A - 5I)\mathbf{v} = \begin{bmatrix} 20 & 20 \\ 20 & 20 \end{bmatrix} \mathbf{v} = 0
\quad \Rightarrow \quad \mathbf{v}_2 = \frac{1}{\sqrt{2}} \begin{bmatrix} -1 \\ 1 \end{bmatrix}.
$$

**Step 4. Left singular vectors $\mathbf{u}_i = A \mathbf{v}_i / \sigma_i$.**

$$
\mathbf{u}_1 = \frac{1}{\sqrt{45}} A \mathbf{v}_1
     = \frac{1}{3\sqrt{5}} \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix}
       \frac{1}{\sqrt{2}} \begin{bmatrix} 1 \\ 1 \end{bmatrix}
     = \frac{1}{\sqrt{10}} \begin{bmatrix} 1 \\ 3 \end{bmatrix},
$$

$$
\mathbf{u}_2 = \frac{1}{\sqrt{5}} A \mathbf{v}_2
     = \frac{1}{\sqrt{5}} \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix}
       \frac{1}{\sqrt{2}} \begin{bmatrix} -1 \\ 1 \end{bmatrix}
     = \frac{1}{\sqrt{10}} \begin{bmatrix} -3 \\ 1 \end{bmatrix}.
$$

**Step 5. Assemble the SVD.**

$$
\mathbf{U} = \frac{1}{\sqrt{10}} \begin{bmatrix} 1 & -3 \\ 3 & 1 \end{bmatrix},
\qquad
\boldsymbol{\Sigma} = \begin{bmatrix} \sqrt{45} & 0 \\ 0 & \sqrt{5} \end{bmatrix},
\qquad
\mathbf{V}^{\mathsf{T}} = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ -1 & 1 \end{bmatrix}.
$$

You can verify directly that $\mathbf{U} \boldsymbol{\Sigma} \mathbf{V}^{\mathsf{T}} = A$.

The rank-one expansion is

$$
A = \sqrt{45} \, \mathbf{u}_1 \mathbf{v}_1^{\mathsf{T}} + \sqrt{5} \, \mathbf{u}_2 \mathbf{v}_2^{\mathsf{T}}.
$$

Because $\sigma_1 = 3\sqrt{5} \approx 6.71$ is much larger than
$\sigma_2 = \sqrt{5} \approx 2.24$, the first piece captures most of the
"energy" of $A$. The rank-one approximation $A_1 = \sigma_1 \mathbf{u}_1 \mathbf{v}_1^{\mathsf{T}}$
has error squared $\sigma_2^{2} = 5$.

---

## 6. Geometric interpretation

For a square matrix $A$, the SVD decomposes the action of $A$ on a vector into
three simple steps:

1. $\mathbf{V}^{\mathsf{T}}$ rotates the input vector in $\mathbb{R}^{n}$.
2. $\boldsymbol{\Sigma}$ stretches or shrinks each coordinate axis by $\sigma_i$.
3. $\mathbf{U}$ rotates the result in $\mathbb{R}^{m}$.

Applied to the unit circle in $\mathbb{R}^{2}$, this produces an ellipse whose
semi-axis lengths are the singular values of $A$. The directions of the axes
are the left singular vectors $\mathbf{u}_i$; the pre-image directions are the right
singular vectors $\mathbf{v}_i$.

---

## 7. Application to seismic noise attenuation

Consider a **CMP gather** arranged as a matrix $\mathbf{D}$ whose rows are time samples
and whose columns are traces. After a good NMO correction, the primary
reflections are nearly flat and therefore highly correlated from trace to trace.
Random noise, by contrast, is uncorrelated.

This difference shows up in the singular values of $\mathbf{D}$:

- The structured signal lives in a low-dimensional subspace, so it contributes
  to the **large singular values**.
- The random noise contributes to **small singular values**.

We can therefore approximate the signal by keeping only the leading $k$ singular
values:

$$
\mathbf{D}_{\text{signal}} \approx \sum_{i=1}^{k} \sigma_i \mathbf{u}_i \mathbf{v}_i^{\mathsf{T}}
= \mathbf{U}_k \boldsymbol{\Sigma}_k \mathbf{V}_k^{\mathsf{T}}.
$$

The discarded tail,

$$
\mathbf{D}_{\text{noise}} \approx \sum_{i=k+1}^{r} \sigma_i \mathbf{u}_i \mathbf{v}_i^{\mathsf{T}},
$$

contains the less coherent, noise-like energy. Choosing $k$ is a trade-off:
smaller $k$ removes more noise but may also remove weak signal.

> **In practice.** This is the same rank-reduction idea used in methods such as
Cadzow filtering and f-x SVD denoising. The data are first transformed into a
domain where the desired signal is low-rank; then the SVD is truncated and the
result is transformed back.

---

## 8. Summary

| Symbol | Meaning | How it is obtained |
|--------|---------|--------------------|
| $A$ | Data matrix ($m \times n$) | Given |
| $r$ | Rank of $A$ | Number of non-zero singular values |
| $\sigma_i$ | $i$-th singular value | $\sigma_i = \sqrt{\lambda_i(A^{\mathsf{T}} A)}$ |
| $\mathbf{v}_i$ | Right singular vector | Eigenvector of $A^{\mathsf{T}} A$ |
| $\mathbf{u}_i$ | Left singular vector | Eigenvector of $A A^{\mathsf{T}}$, or $\mathbf{u}_i = A \mathbf{v}_i / \sigma_i$ |
| $\mathbf{U}, \mathbf{V}$ | Orthogonal matrices of singular vectors | $\mathbf{U}^{\mathsf{T}} \mathbf{U} = \mathbf{I}$, $\mathbf{V}^{\mathsf{T}} \mathbf{V} = \mathbf{I}$ |
| $\boldsymbol{\Sigma}$ | Diagonal matrix of singular values | $\Sigma_{ii} = \sigma_i$, zeros elsewhere |

The key facts to remember are:

1. The SVD always exists, even for rectangular and non-symmetric matrices.
2. It provides orthonormal bases for the four fundamental subspaces of $A$.
3. The singular values are non-negative and ordered: $\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_r > 0$.
4. The best rank-$k$ approximation keeps the $k$ largest singular values and
   discards the rest.
5. In seismic processing, rank-reduction via the SVD separates structured signal
   from unstructured noise.
