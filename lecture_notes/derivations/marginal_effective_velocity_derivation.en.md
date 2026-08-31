---
title: Derivation of the Marginal Effective Velocity Formula
status: draft
---

# Derivation of the Marginal Effective Velocity Formula

This document derives the relationship between the marginal effective velocity and the second derivative of traveltime with respect to offset. It is a companion to Term 3 Lecture 2 and expands the discussion of effective and marginal velocities.

## 1. Definition of marginal effective velocity

In the lecture notes, the **marginal effective velocity** is defined as the limit of the effective velocity as the offset range shrinks to zero:

$$
V_\text{marg}^2 = \left. \frac{d x^2}{d(t^2)} \right|_{x \to 0} .
$$

Equivalently, it is the slope of the $t^2$ versus $x^2$ curve at the origin:

$$
V_\text{marg}^2 = \left. \frac{d(t^2)}{d(x^2)} \right|_{x=0}^{-1} .
$$

## 2. From the $t^2$–$x^2$ slope to the second derivative of $t$

We want to relate this slope to the curvature of the traveltime curve $t(x)$. Apply the chain rule:

$$
\frac{d(t^2)}{d(x^2)} = \frac{d(t^2)/dx}{d(x^2)/dx} = \frac{2t \, dt/dx}{2x} = \frac{t}{x} \frac{dt}{dx} .
$$

At $x = 0$, the moveout is symmetric, so $dt/dx = 0$. Therefore we evaluate the limit:

$$
\left. \frac{d(t^2)}{d(x^2)} \right|_{x=0}
= \lim_{x \to 0} \frac{t}{x} \frac{dt}{dx}
= t_0 \lim_{x \to 0} \frac{dt/dx}{x}
= t_0 \left. \frac{d^2 t}{dx^2} \right|_{x=0} .
$$

The last step uses the fact that $dt/dx = 0$ at $x = 0$, so the limit of the ratio is the second derivative.

Substituting back into the definition of $V_\text{marg}$ gives the alternative formula

$$
\boxed{
V_\text{marg} = \frac{1}{\sqrt{t_0 \left. \frac{d^2 t}{dx^2} \right|_{x=0}}}
}
$$

or, in squared form,

$$
\boxed{
V_\text{marg}^2 = \frac{1}{t_0 \left. \frac{d^2 t}{dx^2} \right|_{x=0}} .
}
$$

## 3. Check with the hyperbolic case

For a pure hyperbola,

$$
t(x) = \sqrt{t_0^2 + \frac{x^2}{v^2}} .
$$

The first derivative is

$$
\frac{dt}{dx} = \frac{x}{v^2 \sqrt{t_0^2 + x^2/v^2}} .
$$

The second derivative is

$$
\frac{d^2 t}{dx^2} = \frac{1}{v^2 \sqrt{t_0^2 + x^2/v^2}} - \frac{x^2}{v^4 (t_0^2 + x^2/v^2)^{3/2}} .
$$

At $x = 0$ this reduces to

$$
\left. \frac{d^2 t}{dx^2} \right|_{x=0} = \frac{1}{v^2 t_0} .
$$

Therefore

$$
V_\text{marg} = \frac{1}{\sqrt{t_0 \cdot \frac{1}{v^2 t_0}}} = v .
$$

So for a purely hyperbolic event the marginal effective velocity is exactly the NMO velocity, as expected.

## 4. Non-hyperbolic moveout used in the lecture

In the lecture notes the traveltime is modeled as

$$
t^2(x) = t_0^2 + \frac{x^2}{v^2} + \varepsilon x^4 .
$$

Write $f(x) = t_0^2 + x^2/v^2 + \varepsilon x^4$ so that $t = \sqrt{f}$. Then

$$
\frac{dt}{dx} = \frac{f'}{2\sqrt{f}}, \qquad
\frac{d^2 t}{dx^2} = \frac{f''}{2\sqrt{f}} - \frac{(f')^2}{4 f^{3/2}} .
$$

At $x = 0$ we have $f = t_0^2$, $f' = 0$, and $f'' = 2/v^2$, so

$$
\left. \frac{d^2 t}{dx^2} \right|_{x=0} = \frac{2/v^2}{2 t_0} = \frac{1}{v^2 t_0} .
$$

Thus the marginal velocity is still $V_\text{marg} = v$; the $\varepsilon x^4$ term does not affect the curvature at zero offset. However, the **effective velocity** over a finite offset range is biased downward because the best-fit straight line in the $t^2$–$x^2$ plane is tilted by the extra term.

## 5. Why the two forms are useful

- The form $V_\text{marg}^2 = dx^2/d(t^2)$ is practical: it is the slope measured in a $t^2$–$x^2$ velocity analysis with very short offsets.
- The form $V_\text{marg}^2 = 1/[t_0 \, t''(0)]$ is useful for theory: it connects the marginal velocity directly to the local curvature of the traveltime curve and is the basis for many moveout expansions (e.g., the Taner-Koehler expansion).

## 6. Summary

Starting from the definition

$$
V_\text{marg}^2 = \left. \frac{d x^2}{d(t^2)} \right|_{x=0} ,
$$

we used the chain rule and the fact that $dt/dx = 0$ at zero offset to obtain the equivalent form

$$
V_\text{marg}^2 = \frac{1}{t_0 \left. \frac{d^2 t}{dx^2} \right|_{x=0}} .
$$

For a hyperbola this reduces to the NMO velocity, and for the small non-hyperbolic perturbation used in the lecture it leaves the marginal velocity unchanged while still biasing the finite-offset effective velocity.

## References

- Taner, M. T., and Koehler, F., 1969, *Velocity spectra — digital computer derivation and applications of velocity functions*, Geophysics, 34, 859–881.
- Term 3 Lecture 2 notes: `lecture_notes/en/term03_lec02_statics_and_velocity_modeling.en.md`.
