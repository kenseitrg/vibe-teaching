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

### 1.1 Starting point: the acoustic wave equation

In earlier lectures we described wave propagation with the **acoustic wave equation** for the pressure $p(x,z,t)$ in a fluid:

$$
\nabla^2 p = \frac{1}{V_p^2}\,\frac{\partial^2 p}{\partial t^2}.
$$

It is worth recalling what this equation says, because the elastic equation has exactly the same logical structure:

- **Right-hand side** — *inertia*. The second time derivative of $p$ plays the role of an acceleration. This is the "$ma$" side of Newton's second law.
- **Left-hand side** — *restoring force*. The Laplacian $\nabla^2 p$ measures how much the pressure at a point differs from the average of its surroundings. If a small fluid element is compressed more than its neighbours, the pressure imbalance pushes it back. This is the "$F$" side of Newton's second law.
- **The link between them** — the factor $1/V_p^2$ converts "how much the medium is squeezed" into "how fast it responds". Its square root, $V_p$, is the speed at which the disturbance propagates.

So the acoustic wave equation is nothing but **$F = ma$ for a compressible fluid**: the restoring force comes from compression, and only from compression, because a fluid has no resistance to being sheared.

### 1.2 From fluids to solids: one more way to push back

A solid can be deformed in two fundamentally different ways:

1. **Change of volume** (compression/dilatation) — the material is squeezed or stretched uniformly, like a fluid.
2. **Change of shape at constant volume** (shear) — the material is distorted sideways, like a deck of cards sliding over itself.

A fluid resists only the first. A solid resists **both**, and this is the whole difference between the acoustic and elastic wave equations. The two kinds of resistance are measured by two elastic constants, the **Lamé parameters**:

- $\mu$ — the **shear modulus**: stiffness against shape change. For any fluid, $\mu = 0$.
- $\lambda$ — together with $\mu$, controls the stiffness against volume change.

### 1.3 Navier's equation term by term

In a solid, displacement is a vector $\mathbf{u} = (u, v, w)$: every point of the material can move in any direction. The equation of motion — **Navier's equation** — is, once again, just $F = ma$ written per unit volume:

$$
\underbrace{(\lambda + 2\mu)\,\nabla(\nabla\cdot\mathbf{u})}_{\text{compressional restoring force}}
\;\underbrace{-\;\mu\,\nabla\times(\nabla\times\mathbf{u})}_{\text{shear restoring force}}
\;=\;
\underbrace{\rho\,\frac{\partial^2 \mathbf{u}}{\partial t^2}}_{\text{inertia}},
$$

where $\rho$ is density and $t$ is time. Each piece has a direct physical meaning:

| Term | Meaning | Analogy |
|------|---------|---------|
| $\rho\,\partial^2\mathbf{u}/\partial t^2$ | Mass per volume ($\rho$) times acceleration: the inertia of a small material element. | "$ma$" in $F = ma$. |
| $\nabla\cdot\mathbf{u}$ | **Dilatation**: the fractional change of volume of a small element. Positive = expansion, negative = compression. | The analogue of pressure in the acoustic equation. |
| $(\lambda+2\mu)\,\nabla(\nabla\cdot\mathbf{u})$ | Force arising because the compression varies from point to point. If one element is squeezed more than its neighbours, it is pushed back. | The $\nabla^2 p$ term of the acoustic equation. |
| $\nabla\times\mathbf{u}$ | **Rotation**: how much a small element is twisted (sheared) relative to its neighbours, without change of volume. | No acoustic analogue — fluids do not resist twisting. |
| $-\mu\,\nabla\times(\nabla\times\mathbf{u})$ | Force arising because the shear distortion varies from point to point. | The genuinely *solid* part of the equation. |

> **Teaching note.** Do not read Navier's equation as three symbols to memorize. Read it as a sentence: *"the unbalanced elastic force on a small element (left) equals its mass times acceleration (right)"*. The left side has two terms simply because a solid has two independent ways to be deformed.

### 1.4 The acoustic equation as a special case

The parallel becomes exact if we set $\mu = 0$ (a fluid). The shear term disappears, and taking the divergence of what remains gives a scalar wave equation for the dilatation $\nabla\cdot\mathbf{u}$ with propagation speed $\sqrt{\lambda/\rho}$ — precisely the acoustic wave equation, with pressure replaced by (minus) the dilatation. In other words:

> **Elasticity = acoustics + shear.** Everything the acoustic equation does, the elastic equation also does — plus one extra restoring mechanism. That extra mechanism is what allows a second, slower type of wave, and ultimately what makes Rayleigh waves possible at all.

### 1.5 Two uncoupled wave types

Because the compressional and shear restoring forces involve different spatial derivatives, they can be separated. Taking the **divergence** of Navier's equation eliminates the curl term (the divergence of a curl is zero) and gives a scalar wave equation for the dilatation — the **P (compressional) wave**, with velocity

$$
V_p = \sqrt{\frac{\lambda + 2\mu}{\rho}}.
$$

Taking the **curl** eliminates the divergence term and gives a vector wave equation for the rotation — the **S (shear) wave**, with velocity

$$
V_s = \sqrt{\frac{\mu}{\rho}}.
$$

Since $\lambda > 0$ and $\mu > 0$ in a solid, $V_p > V_s$: compressional waves always travel faster than shear waves. (In a fluid, $\mu = 0$ and the S wave disappears entirely.)

For the problems we consider, it is convenient to introduce scalar potentials $\phi$ and $\psi$ such that the displacement is a sum of a P part and an S part:

$$
\mathbf{u} = \nabla\phi + \nabla\times\boldsymbol{\psi}.
$$

This split (the **Helmholtz decomposition**) mirrors the two restoring forces above: $\phi$ carries the volume change (P motion is curl-free, like potential flow), and $\boldsymbol{\psi}$ carries the rotation (S motion is volume-preserving).

### 1.6 Why single scalars are enough in 2D

In full 3D, the vector potential has three components, $\boldsymbol{\psi} = (\psi_x, \psi_y, \psi_z)$, so the decomposition involves four unknown fields ($\phi$ plus three $\psi$'s). This looks worse than just working with $\mathbf{u}$ directly. The payoff comes in **two-dimensional plane strain**: the wave propagates along $x$, the medium is uniform along $y$, so *nothing varies with* $y$, i.e. $\partial(\cdot)/\partial y = 0$. Writing out the components of $\mathbf{u} = \nabla\phi + \nabla\times\boldsymbol{\psi}$ under this assumption:

$$
u_x = \frac{\partial\phi}{\partial x} + \frac{\partial\psi_y}{\partial z}, \qquad
u_y = \frac{\partial\psi_x}{\partial z} - \frac{\partial\psi_z}{\partial x}, \qquad
u_z = \frac{\partial\phi}{\partial z} - \frac{\partial\psi_y}{\partial x}.
$$

Now the magic is visible by inspection:

- **$u_x$ and $u_z$ involve only $\phi$ and $\psi_y$.** The in-plane motion is described by exactly **two scalars**: $\phi$ (the P part) and the single component $\psi_y$ (the in-plane shear part). Shear motion in the $x$-$z$ plane is called **SV** ("vertically polarized" shear: particles move in the vertical plane containing the propagation direction).
- **$u_y$ involves only $\psi_x$ and $\psi_z$**, which never appear in $u_x$ or $u_z$. The out-of-plane motion is completely decoupled. It is called **SH** ("horizontally polarized" shear). Moreover, we do not need to carry two potentials for it: substituting the expression for $u_y$ into Navier's equation collapses to a single scalar wave equation for $u_y$ itself, $\mu\,\nabla^2 u_y = \rho\,\partial^2 u_y/\partial t^2$. So SH motion is also described by one scalar — simply $u_y$, no potential needed.

> **Teaching note.** "2D" does not mean "motion has only two components". It means "nothing *varies* along $y$". The $y$-component of motion survives — it is precisely the SH wave — but it lives its own life, mathematically separate from the in-plane P-SV problem.

The correspondence with surface waves is then direct:

| Motion | Displacement | Field(s) | Wave type | Surface wave |
|--------|--------------|----------|-----------|--------------|
| In-plane ($x$-$z$) | $u_x, u_z$ | $\phi$ and $\psi_y$ | P-SV | **Rayleigh** |
| Out-of-plane ($y$) | $u_y$ | $u_y$ itself | SH | **Love** |

From here on we write $\psi$ for the single component $\psi_y$. Our focus is on Rayleigh waves — P-SV motion coupled at the free surface; Love (SH) waves are mentioned only briefly in §7.

At the free surface $z=0$, the traction vector must vanish. Physically, this says that the air above can neither pull nor drag on the ground: the surface is free to move. For the P-SV problem, two traction components are relevant:

$$
\sigma_{zz}(x,0,t) = 0, \qquad \sigma_{xz}(x,0,t) = 0.
$$

These two boundary conditions are the source of the Rayleigh wave equation. (The third condition, $\sigma_{yz} = 0$, involves only $u_y$ and belongs to the decoupled SH/Love problem.)

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

### 2.1 From the boundary conditions to the Rayleigh equation

So far we have only written down a trial solution. The physics that turns it into the Rayleigh equation lives entirely in the two traction-free conditions — and getting from one to the other is a four-step mechanical exercise with no new ideas. We spell out each step.

**Step 1: Hooke's law — stress from displacement.** The boundary conditions involve stresses, but our trial solution is written in displacements (through the potentials). The bridge between them is Hooke's law for an isotropic elastic solid. This is the same "force = stiffness × deformation" statement as for a spring, except that a solid has two stiffnesses ($\lambda$ and $\mu$, §1.2) because it resists two kinds of deformation:

$$
\sigma_{ij} = \lambda\,(\nabla\cdot\mathbf{u})\,\delta_{ij} + \mu\left(\frac{\partial u_i}{\partial x_j} + \frac{\partial u_j}{\partial x_i}\right),
$$

where $\delta_{ij}$ is 1 when $i=j$ and 0 otherwise. We need only the two components that appear in the boundary conditions:

$$
\sigma_{zz} = \lambda\left(\frac{\partial u_x}{\partial x} + \frac{\partial u_z}{\partial z}\right) + 2\mu\,\frac{\partial u_z}{\partial z}, \qquad
\sigma_{xz} = \mu\left(\frac{\partial u_x}{\partial z} + \frac{\partial u_z}{\partial x}\right).
$$

Read them physically: the normal traction $\sigma_{zz}$ responds to the dilatation (stiffness $\lambda$) plus the vertical stretch (stiffness $2\mu$); the shear traction $\sigma_{xz}$ is simply $\mu$ times the shear strain — the closest analogue of the one-dimensional $\sigma = E\varepsilon$.

**Step 2: Differentiate the trial solution.** From the potentials of §2 and the displacement formulas $u_x = \partial_x\phi + \partial_z\psi$, $u_z = \partial_z\phi - \partial_x\psi$:

$$
u_x = \left(-ikA\,e^{-qz} - sB\,e^{-sz}\right)E, \qquad
u_z = \left(-qA\,e^{-qz} + ikB\,e^{-sz}\right)E,
$$

where $E = e^{i(\omega t - kx)}$ is the common phase factor. It multiplies every stress component as well, and since the boundary conditions are homogeneous it cancels — we omit it from here on. Substituting into Hooke's law and setting $z=0$ (so $e^{-qz} = e^{-sz} = 1$):

$$
\sigma_{xz} = \mu\left[2ikq\,A + (k^2 + s^2)\,B\right], \qquad
\sigma_{zz} = \left[\lambda(q^2 - k^2) + 2\mu q^2\right]A - 2\mu iks\,B.
$$

> **Consistency check.** Along the way one finds $\nabla\cdot\mathbf{u} = (q^2 - k^2)\,A\,e^{-qz}E$: the dilatation contains only the P amplitude $A$. The $B$ terms cancel — the shear part is divergence-free, exactly as the Helmholtz split of §1.5 promised. If your algebra does not show this cancellation, there is a sign error somewhere.

**Step 3: Set the tractions to zero and tidy up.** The conditions $\sigma_{zz} = 0$ and $\sigma_{xz} = 0$ are two homogeneous linear equations for $A$ and $B$. They look much friendlier after dividing through by $k^2$ and using the definitions $q^2 = k^2(1 - c^2/V_p^2)$, $s^2 = k^2(1 - c^2/V_s^2)$, together with $\mu = \rho V_s^2$ and $\lambda = \rho(V_p^2 - 2V_s^2)$ (from the velocity formulas of §1.5). The $\sigma_{zz}$ coefficient collapses beautifully:

$$
\lambda(q^2 - k^2) + 2\mu q^2 = \rho V_s^2 k^2\left(2 - \frac{c^2}{V_s^2}\right),
$$

and the system becomes

$$
\begin{aligned}
\left(2 - \frac{c^2}{V_s^2}\right) A - 2i\sqrt{1 - \frac{c^2}{V_s^2}}\,B &= 0 \qquad (\sigma_{zz} = 0), \\
2i\sqrt{1 - \frac{c^2}{V_p^2}}\,A + \left(2 - \frac{c^2}{V_s^2}\right) B &= 0 \qquad (\sigma_{xz} = 0).
\end{aligned}
$$

> **Where does the $i$ come from?** The factors of $i$ mean that the P and S contributions oscillate $90^\circ$ out of phase with each other. This phase shift is precisely why Rayleigh particle motion is *elliptical* rather than linear — the horizontal and vertical components never peak at the same instant. (Flipping the sign convention for $\psi$ flips the sign of $B$ and hence of one off-diagonal entry; nothing physical changes.)

**Step 4: Demand a non-trivial solution.** Two homogeneous equations for the two unknowns $(A, B)$ have a non-zero solution only when the determinant vanishes:

$$
\left(2 - \frac{c^2}{V_s^2}\right)^2
- 4\sqrt{1 - \frac{c^2}{V_p^2}}\;\sqrt{1 - \frac{c^2}{V_s^2}} = 0.
$$

This is the **Rayleigh equation**. Step back and see what happened: no new physics was added beyond Navier's equation in the interior (built into $q$ and $s$) and Hooke's law at the surface. The Rayleigh equation is purely a *matching condition* — it asks: "for which velocity $c$ can an evanescent P wave and an evanescent S wave conspire to leave the free surface completely unstressed?"

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

### 4.2 The matching problem for a layered medium

The recipe is the same one we followed in §2.1 — it just has more unknowns.

**What changes.** In the half-space there were two unknown amplitudes ($A$ and $B$) and two boundary conditions ($\sigma_{zz}=0$, $\sigma_{xz}=0$). A layered model replaces the homogeneous half-space with a stack of layers, each with its own $\lambda$, $\mu$, and $\rho$. Inside each layer the same trial solution of §2 applies, but each layer now admits two amplitudes per wave type (one in each vertical direction). So a single homogeneous layer has **four** unknown amplitudes (two P, two S), and the bottom half-space has **two** (only the amplitudes that decay with depth — no energy arrives from $z=\infty$).

**Interface conditions.** At each interface between two layers, four conditions must hold:

| Condition | Physical meaning |
|-----------|-----------------|
| $u_x$ continuous | The layers are **welded** together — no gap or slip at the contact. |
| $u_z$ continuous | Same — material cannot jump vertically at the interface. |
| $\sigma_{zz}$ continuous | The normal force per area is balanced — Newton's third law across the interface. |
| $\sigma_{xz}$ continuous | Same — the shear force per area is balanced. |

> **Teaching note.** These are the same kinds of conditions we used in §2.1: two displacement conditions (they ensure the layers are stuck together) and two stress conditions (they ensure forces balance across the interface, action = reaction). There is nothing more to the physics. The rest is bookkeeping.

**A concrete counting exercise.** Consider the simplest layered model — one layer of thickness $H$ over a half-space:

| Unknown | Source |
|---------|--------|
| Two P amplitudes + two S amplitudes in the layer | 4 (one per wave type per vertical direction) |
| P + S amplitudes in the half-space | 2 (decaying only — radiation condition) |
| **Total unknowns** | **6** |

| Condition | Location |
|-----------|----------|
| $\sigma_{zz}=0$, $\sigma_{xz}=0$ | Free surface (top of layer) |
| $u_x$, $u_z$, $\sigma_{zz}$, $\sigma_{xz}$ continuous | Interface (bottom of layer) |
| **Total equations** | **6** |

Six unknowns, six homogeneous equations → a non-trivial solution exists only if the determinant of the system vanishes. This gives a condition

$$
D(\omega, k) = 0,
$$

exactly analogous to the single determinant $(2 - c^2/V_s^2)^2 - 4\sqrt{\ldots} = 0$ of §2.1. For a model with $N$ layers the pattern continues unchanged: more unknowns, more equations, same recipe, one determinant.

**Why this produces dispersion.** Here is the key point. The half-space determinant depended only on the ratio $c = \omega/k$ — it contained no length scale, so the answer $c$ could not depend on frequency, and the wave was non-dispersive (§2.2). A layer of thickness $H$ introduces a length scale. The determinant now depends on the dimensionless product $kH$ (equivalently $\omega H / c$): a high-frequency wave completes many oscillations within the layer, while a low-frequency wave completes only a fraction of one. Because the root $c$ must adjust as $kH$ changes, $c$ becomes a function of $\omega$. This is the mathematical translation of the physical picture of §4.1 — different frequencies sample different depths.

**Discrete roots and modes.** At a fixed frequency $\omega$, $D(\omega, k) = 0$ is one equation in one unknown. Like a vibrating string that supports only discrete standing wavelengths, the layered medium at each frequency supports only a discrete set of wavenumbers $k_0 < k_1 < k_2 < \cdots$, each with its own phase velocity $c_n = \omega/k_n$. Each root is one **mode** of propagation. (In linear algebra this is called an *eigenvalue* problem; the only thing we need from that theory is the idea that solutions exist only for special, discrete values — the modes discussed in §5.)

**Practical computation.** Expanding the full determinant by hand is tedious but unnecessary. The **Thomson-Haskell propagator matrix** (or a finite-element equivalent) does the bookkeeping:

1. Each layer is represented by a small matrix that propagates the displacement-traction vector across the layer.
2. The matrices for all layers are multiplied together.
3. The free-surface condition is applied at the top and the radiation condition (no upgoing waves from infinity) at the bottom.
4. The resulting determinant is $D(\omega, k)$; its zeros are the modes.

The algebra is routine for a computer. What it gives us — a set of discrete dispersion curves $c_n(f)$, one per mode — is exactly what MASW and surface-wave inversion work with.

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

The full derivation of the Rayleigh equation, the boundary-condition setup, and the layered dispersion problem are left here for students who want to see the details.

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
