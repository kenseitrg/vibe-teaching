---
title: Derivation of Surface-Wave Dispersion and Multimodality
status: draft
---

# Derivation of Surface-Wave Dispersion and Multimodality

This document derives the dispersion relation for Rayleigh waves on a homogeneous elastic half-space and explains how layering produces dispersion and multiple modes. It is a companion to Term 3 Lecture 03 (Surface Waves) and expands the geometric discussion of the lecture with the equations behind the dispersion curve.

> **Why this matters.** A surface-wave dispersion curve is the main observable in surface-wave inversion. To understand why the curve has the shape it does, why it changes with frequency, and why it can have several branches, we need to derive the relation between frequency and phase velocity from the elastic wave equation and the boundary conditions at the free surface.

> **Prerequisites.** Comfort with partial derivatives, complex exponentials, and the wave equation. A first course in elasticity is helpful but not required; the definitions we need are stated below.

> **What this document does not do.** It does not derive the full Thomson-Haskell propagator matrix for an arbitrary stack of layers; that algebra is lengthy and gives little additional intuition. Instead, the layered case is described conceptually, and the Rayleigh-wave equation is derived for the simplest setting in which it can be obtained exactly.

---

## 1. Elastic-wave preliminaries

We model the Earth as an isotropic, linear elastic material. In the absence of body forces, the displacement vector $\mathbf{u} = (u, v, w)$ satisfies Navier's equation of motion:

$$
(\lambda + 2\mu)\,\nabla(\nabla\cdot\mathbf{u}) - \mu\,\nabla\times(\nabla\times\mathbf{u}) = \rho\,\frac{\partial^2 \mathbf{u}}{\partial t^2},
$$
where $\lambda$ and $\mu$ are the Lamé parameters, $\rho$ is density, and $t$ is time. By taking the divergence and the curl of this equation separately, one finds two uncoupled wave equations:

- **P (compressional) waves**: velocity $V_p = \sqrt{(\lambda + 2\mu)/\rho}$.
- **S (shear) waves**: velocity $V_s = \sqrt{\mu/\rho}$.

For the problems we consider, it is convenient to introduce scalar potentials $\phi$ and $\psi$ such that the displacement is a sum of a P part and an S part:

$$
\mathbf{u} = \nabla\phi + \nabla\times\boldsymbol{\psi}.
$$
In two-dimensional plane strain (all motion in the $x$-$z$ plane, no variation in $y$), the P-SV part is described by a single scalar $\phi$ for P waves and a single scalar $\psi$ for SH waves (the $y$-component of the vector potential). The SH part corresponds to Love waves, which we mention only briefly; our focus is on Rayleigh waves, which are P-SV motion coupled at the free surface.

At the free surface $z=0$, the traction vector must vanish. For a plane surface this means

$$
\sigma_{zz}(x,0,t) = 0, \qquad \sigma_{xz}(x,0,t) = 0.
$$
These two boundary conditions are the source of the Rayleigh wave equation.

---

## 2. Rayleigh waves on a homogeneous half-space

Consider a homogeneous, isotropic elastic half-space occupying $z \ge 0$. We look for a wave that propagates along the surface in the $x$-direction and decays with depth:

$$
\phi(x,z,t) = A\,e^{-i k x}\,e^{-q z}\,e^{i\omega t}, \qquad
\psi(x,z,t) = B\,e^{-i k x}\,e^{-s z}\,e^{i\omega t},
$$
where $k$ is the horizontal wavenumber, $\omega$ is the angular frequency, and $A$ and $B$ are amplitudes. The real parameters $q$ and $s$ must be positive so that the motion vanishes as $z \to \infty$.

Because $\phi$ and $\psi$ must satisfy their respective wave equations, substitution gives

$$
q^2 = k^2\left(1 - \frac{c^2}{V_p^2}\right), \qquad
s^2 = k^2\left(1 - \frac{c^2}{V_s^2}\right),
$$
where

$$
c = \frac{\omega}{k}
$$
is the **phase velocity** of the surface wave. For $q$ and $s$ to be real, we need $c < V_s < V_p$. This is the first important result: a Rayleigh wave on a homogeneous half-space is slower than both body waves.

The displacement components are obtained from the potentials:

$$
\begin{aligned}
u_x &= \frac{\partial\phi}{\partial x} + \frac{\partial\psi}{\partial z}, \\
u_z &= \frac{\partial\phi}{\partial z} - \frac{\partial\psi}{\partial x}.
\end{aligned}
$$
(The sign of the $\psi$ term is a convention; it does not affect the final dispersion relation.)

### 2.1 Applying the boundary conditions

Using Hooke's law for an isotropic medium, the traction-free conditions at $z=0$ become two linear equations in the amplitudes $A$ and $B$:

$$
\begin{aligned}
\left(2 - \frac{c^2}{V_s^2}\right) A + 2i\sqrt{1 - \frac{c^2}{V_s^2}}\,B &= 0, \\
2i\sqrt{1 - \frac{c^2}{V_p^2}}\,A + \left(2 - \frac{c^2}{V_s^2}\right) B &= 0.
\end{aligned}
$$
The exact signs of the off-diagonal terms depend on the sign convention for $\psi$, but the determinant is independent of that convention. For a non-trivial solution $(A,B) \ne (0,0)$, the determinant must vanish:

$$
\left(2 - \frac{c^2}{V_s^2}\right)^2
- 4\sqrt{1 - \frac{c^2}{V_p^2}}\;\sqrt{1 - \frac{c^2}{V_s^2}} = 0.
$$
This is the **Rayleigh equation**.

### 2.2 Solving the Rayleigh equation

The Rayleigh equation depends on the two body-wave velocities $V_p$ and $V_s$. Once those are fixed, it has one real root satisfying $c < V_s$. For typical Poisson's ratios ($0.25$–$0.35$), the solution is approximately

$$
V_R \approx 0.87\,V_s \quad \text{to} \quad 0.92\,V_s.
$$
For a Poisson's ratio of $0.25$ ($V_p = \sqrt{3}\,V_s$), the exact value is

$$
V_R \approx 0.9194\,V_s.
$$
**Key point:** on a homogeneous half-space, the Rayleigh velocity is a fixed fraction of the shear velocity. It does **not** depend on frequency, so the Rayleigh wave on a homogeneous half-space is **non-dispersive**.

> **Teaching note.** The Rayleigh equation is a compatibility condition. It says that the P and S evanescent waves that make up a Rayleigh wave can be matched at the free surface only for one particular phase velocity. This velocity is determined by the material, not by the frequency.

---

## 3. Phase velocity and group velocity from superposition

A wave of a single frequency and single wavenumber fills all space and carries no localized information. In practice, we observe wave packets, which are localized superpositions of many nearby frequencies. The speed of the packet is the **group velocity**; the speed of the individual crests inside the packet is the **phase velocity**.

### 3.1 Phase velocity

For a monochromatic wave

$$
u(x,t) = A\,e^{i(kx - \omega t)},
$$
the argument $(kx - \omega t)$ is constant for an observer moving at speed

$$
c = \frac{\omega}{k}.
$$
This is the **phase velocity**: the speed at which a single crest or trough moves.

### 3.2 Group velocity from two close frequencies

Consider the superposition of two waves with nearly equal frequencies $\omega_1$ and $\omega_2$ and wavenumbers $k_1$ and $k_2$:

$$
u(x,t) = \cos(k_1 x - \omega_1 t) + \cos(k_2 x - \omega_2 t).
$$
Using the identity $\cos a + \cos b = 2\cos\frac{a+b}{2}\cos\frac{a-b}{2}$, this becomes

$$
u(x,t) = 2\cos\left(\frac{k_1 + k_2}{2}x - \frac{\omega_1 + \omega_2}{2}t\right)
\cos\left(\frac{k_1 - k_2}{2}x - \frac{\omega_1 - \omega_2}{2}t\right).
$$
The first cosine is a "carrier" wave with average wavenumber and frequency; it moves at the average phase velocity. The second cosine is a slowly varying "envelope" or "beat" pattern. It moves at speed

$$
U = \frac{\omega_1 - \omega_2}{k_1 - k_2} = \frac{\Delta\omega}{\Delta k}.
$$
In the limit of an infinitesimal frequency band, this becomes

$$
U = \frac{d\omega}{dk}.
$$
This is the **group velocity**: the speed at which the envelope, and hence the energy, propagates.

For a general dispersion relation $\omega(k)$, we can also write

$$
U = \frac{d\omega}{dk} = c + k\frac{dc}{dk} = c - \lambda\frac{dc}{d\lambda},
$$
where $\lambda = 2\pi/k$ is the wavelength. This last form is useful: if $dc/d\lambda > 0$ (velocity increases with wavelength), then $U < c$.

> **Physical picture.** On a dispersive surface-wave record, the individual wiggles in a wave packet travel at the phase velocity, but the bump of energy you actually see travel across the gather moves at the group velocity. When the two differ, the wiggles appear to move through the envelope.

### 3.3 Group velocity for a non-dispersive Rayleigh wave

On a homogeneous half-space, $c = V_R$ is independent of $k$. Therefore

$$
U = \frac{d\omega}{dk} = \frac{d}{dk}(V_R k) = V_R = c.
$$
Phase and group velocities are equal. Dispersion, and therefore a distinction between $c$ and $U$, appears only when the medium is layered.

---

## 4. Rayleigh waves in a layered medium: dispersion

A real near-surface model is not homogeneous. It usually consists of a low-velocity weathering layer over firmer material, with velocity increasing with depth. Rayleigh waves in such a layered medium are **dispersive**: their phase velocity depends on frequency.

### 4.1 Why dispersion arises

The decay rate of a Rayleigh wave with depth is controlled by $q$ and $s$, which are proportional to the wavenumber $k$. A low-frequency wave has a small $k$ and therefore decays slowly; it samples material deep below the surface. A high-frequency wave has a large $k$ and decays rapidly; it is confined to the shallow layers.

Consequently:

- **Low-frequency (long-wavelength) Rayleigh waves** feel the average elastic properties of the deep, usually faster material. Their phase velocity is close to the Rayleigh velocity of the deeper layers.
- **High-frequency (short-wavelength) Rayleigh waves** stay in the shallow, usually slower material. Their phase velocity is close to the Rayleigh velocity of the shallow layers.

As frequency increases, the phase velocity decreases from the deep value toward the shallow value. This produces the characteristic **dispersion curve** $c(f)$ used in MASW/SWI.

### 4.2 The layered eigenvalue problem

In each homogeneous layer, the potentials have the same form as in §2, but with material-dependent decay constants. At every interface, the displacement and traction must be continuous. Applying these conditions across all interfaces and the free surface leads to a system of homogeneous linear equations.

For a non-trivial solution to exist, the determinant of the system must vanish. This condition is the **dispersion relation** for the layered medium. It is usually written as

$$
D(\omega, k) = 0,
$$
where $D$ is a function whose roots are the allowed $(\omega, k)$ pairs. For each frequency $\omega$, solving this equation gives the wavenumber $k$ (and hence the phase velocity $c = \omega/k$) of each propagating mode.

The practical computation uses the **Thomson-Haskell propagator matrix** (or a finite-element equivalent). In this method:

1. Each layer is represented by a matrix that propagates the displacement-traction vector across the layer.
2. The matrices for all layers are multiplied together.
3. The free-surface condition is applied at the top and the radiation condition (no upgoing waves from infinity) at the bottom.
4. The resulting determinant is the dispersion function $D(\omega, k)$; its zeros are the modes.

The matrix algebra is routine for a computer but tedious by hand. The important conceptual point is that the dispersion relation is an **eigenvalue problem** at each frequency: the medium admits only a discrete set of phase velocities.

---

## 5. Multimodality

For a homogeneous half-space, the Rayleigh equation has exactly one root: one Rayleigh mode. For a layered medium, the dispersion relation can have **multiple roots** at a given frequency. Each root corresponds to a different **mode** of propagation.

### 5.1 Fundamental and higher modes

- The **fundamental mode** has the lowest phase velocity at a given frequency. Its motion penetrates deepest and is usually the easiest to observe.
- **Higher modes** (first, second, ...) have higher phase velocities and more complex depth dependence. Their displacement eigenfunctions have more zero crossings with depth.
- Higher modes are not always excited strongly; which modes dominate depends on source depth, frequency content, and the velocity structure.

### 5.2 Why modes matter

Each mode samples the subsurface differently. The fundamental mode is sensitive to the average velocity over its penetration depth. Higher modes add information about shallow structure that the fundamental mode may not resolve well. In practice:

- If only the fundamental mode is picked, the inversion for $V_s$ is less constrained.
- If several modes are picked, the depth resolution improves and it becomes possible to estimate the ratio $V_p/V_s$ (or Poisson's ratio), which is otherwise poorly resolved by dispersion alone.

> **Mode misidentification.** A picked branch on a dispersion spectrum must be assigned the correct mode number. If a higher mode is misidentified as the fundamental, the inverted $V_s$ profile will be wrong.

---

## 6. Worked example: two-layer near-surface model

Consider the simple model:

| Layer | Thickness (m) | $V_s$ (m/s) | $V_p$ (m/s) | $\rho$ (kg/m³) |
|-------|---------------|-------------|-------------|---------------|
| 1     | 10            | 200         | 400         | 1800          |
| 2 (half-space) | $\infty$ | 500         | 1000        | 2000          |

For a homogeneous half-space with $V_s = 200$ m/s and $V_p = 400$ m/s, the Rayleigh velocity would be approximately

$$
V_{R,1} \approx 0.92 \times 200 = 184\ \text{m/s}.
$$
For the deep half-space with $V_s = 500$ m/s and $V_p = 1000$ m/s,

$$
V_{R,2} \approx 0.92 \times 500 = 460\ \text{m/s}.
$$
Because the material is layered, the Rayleigh wave is dispersive:

- At very **high frequency**, the wavelength is much shorter than the layer thickness (10 m). The wave does not feel the deep half-space, so $c(f)$ approaches $V_{R,1} \approx 184$ m/s.
- At very **low frequency**, the wavelength is much longer than the layer thickness. The wave averages over the layer and the half-space, and $c(f)$ approaches $V_{R,2} \approx 460$ m/s.
- At intermediate frequencies, the phase velocity transitions smoothly between these two limits. The exact shape of the transition requires a numerical solution of the layered dispersion relation, but the asymptotic values and the monotonic trend are enough for undergraduate intuition.

This is why a measured dispersion curve can be inverted for the shallow shear-velocity structure: the high-frequency end tells us about the top few meters, and the low-frequency end tells us about the deeper material.

---

## 7. Love waves: a brief note

Love waves are pure SH motion and require a low-shear-velocity layer over a higher-velocity half-space. Their derivation is mathematically simpler than that of Rayleigh waves because the displacement has only one component and the boundary conditions are fewer. The result is a dispersion relation with the same qualitative behavior: phase velocity bounded between the shear velocity of the layer and the half-space, and multiple modes possible in a multilayered model. The physical principles—decay into the half-space, constructive interference in the layer, and frequency-dependent penetration depth—are identical to those described here for Rayleigh waves.

---

## 8. Link to the lecture notes

The lecture notes will use the following results from this derivation without reproducing the full algebra:

- The **Rayleigh equation** for a homogeneous half-space, and the approximate value $V_R \approx 0.92\,V_s$.
- The definitions of **phase velocity** $c = \omega/k$ and **group velocity** $U = d\omega/dk$, with the wave-packet interpretation.
- The physical reason for dispersion in a layered medium: different frequencies sample different depths.
- The concept of **modes** as discrete roots of the layered dispersion relation.
- The two-layer numerical example with $V_{s1}=200$ m/s and $V_{s2}=500$ m/s.

The full derivation of the Rayleigh equation, the boundary-condition setup, and the layered eigenvalue problem are left here for students who want to see the details.

---

## Key equations

- Rayleigh equation (homogeneous half-space):
  $$
  \left(2 - \frac{V_R^2}{V_s^2}\right)^2
  - 4\sqrt{1 - \frac{V_R^2}{V_p^2}}\;\sqrt{1 - \frac{V_R^2}{V_s^2}} = 0.
  $$

- Phase velocity:
  $$
  c = \frac{\omega}{k} = f\lambda.
  $$

- Group velocity:
  $$
  U = \frac{d\omega}{dk} = c - \lambda\frac{dc}{d\lambda}.
  $$

- Layered dispersion relation (conceptual):
  $$
  D(\omega, k) = 0,
  $$
  whose discrete roots are the phase velocities of the fundamental and higher modes.

- Two-layer asymptotes:
  $$
  c(f) \to V_{R,1}\ \text{as}\ f \to \infty, \qquad
  c(f) \to V_{R,2}\ \text{as}\ f \to 0,
  $$
  where $V_{R,1}$ and $V_{R,2}$ are the Rayleigh velocities of the shallow layer and the deep half-space, respectively.
