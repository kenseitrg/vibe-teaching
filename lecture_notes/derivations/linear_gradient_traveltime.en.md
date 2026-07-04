# Traveltime in a linear velocity gradient

## Problem statement

Consider a 1-D medium where velocity increases linearly with depth:

$$v(z) = v_0 + k z, \qquad k > 0.$$

A seismic ray starts at the surface $(z = 0)$ with take-off angle $\theta_0$ measured from the vertical. We want an expression for the traveltime $t$ to a point on the ray where the velocity is $v$ and the ray angle is $\theta$.

## 1. Ray parameter

Snell’s law for a vertically varying medium says that the ray parameter

$$p = \frac{\sin\theta}{v(z)}$$

is constant along a ray. At the surface $z = 0$:

$$p = \frac{\sin\theta_0}{v_0}.$$

## 2. Traveltime integral

An element of arc length along the ray is $ds$, so the traveltime is

$$t = \int \frac{ds}{v}.$$

Because the ray makes angle $\theta$ with the vertical,

$$dz = ds \cos\theta \quad \Longrightarrow \quad ds = \frac{dz}{\cos\theta}.$$

Using Snell’s law, $\sin\theta = p v$, so

$$\cos\theta = \sqrt{1 - p^2 v^2},$$

and therefore

$$t = \int \frac{dz}{v \sqrt{1 - p^2 v^2}}.$$

## 3. Substitute the linear gradient

With $v = v_0 + k z$, we have $dv = k\, dz$. The integral becomes

$$t = \frac{1}{k} \int \frac{dv}{v\sqrt{1 - p^2 v^2}}.$$

Let $u = p v$; then $dv = du / p$ and

$$t = \frac{1}{k} \int \frac{du}{u\sqrt{1 - u^2}}.$$

The antiderivative is

$$\int \frac{du}{u\sqrt{1 - u^2}} = \ln\!\left(\frac{u}{1 + \sqrt{1 - u^2}}\right) + C.$$

Recalling that $\sin\theta = p v = u$ and

$$\tan\frac{\theta}{2} = \frac{\sin\theta}{1 + \cos\theta} = \frac{p v}{1 + \sqrt{1 - p^2 v^2}},$$

we can write the antiderivative more compactly as

$$t = \frac{1}{k} \ln\!\left(\tan\frac{\theta}{2}\right) + C.$$

## 4. Evaluate between the surface and a point on the ray

At the surface, $\theta = \theta_0$; at the target point, $\theta = \theta$. Thus

$$t = \frac{1}{k} \ln\!\left(\frac{\tan\frac{\theta}{2}}{\tan\frac{\theta_0}{2}}\right).$$

This is the **exponential traveltime law** for a linear velocity gradient: the traveltime is a logarithm of the ratio of the half-angles. Equivalently, the angle (and hence the velocity) grows exponentially with traveltime along the ray.

## 5. Vertical ray special case

For a vertical ray, $\theta_0 = 0$ and $\theta = 0$ everywhere, so the formula above is indeterminate. Going back to the traveltime integral with $p = 0$ gives

$$t = \frac{1}{k} \int_{v_0}^{v} \frac{dv}{v} = \frac{1}{k} \ln\!\left(\frac{v}{v_0}\right) = \frac{1}{k} \ln\!\left(1 + \frac{k z}{v_0}\right).$$

Solving for depth:

$$z = \frac{v_0}{k}\left(e^{k t} - 1\right).$$

So for a vertical ray, depth grows exponentially with one-way traveltime.

## 6. Numerical example

Suppose $v_0 = 1500\ \text{m/s}$ and $k = 0.6\ \text{s}^{-1}$. The vertical traveltime to $z = 1000\ \text{m}$ is

$$t = \frac{1}{0.6} \ln\!\left(1 + \frac{0.6 \times 1000}{1500}\right) = \frac{1}{0.6} \ln(1.4) \approx 0.56\ \text{s}.$$

For a constant-velocity medium at $v_0$, the same depth would take $1000 / 1500 \approx 0.67\ \text{s}$; the gradient speeds up the arrival.

## 7. Summary

- A linear velocity gradient $v(z) = v_0 + k z$ makes ray paths circular arcs.
- Traveltime along a ray is logarithmic in the ray angle:
  $$t = \frac{1}{k} \ln\!\left(\frac{\tan\frac{\theta}{2}}{\tan\frac{\theta_0}{2}}\right).$$
- For a vertical ray this reduces to $t = \frac{1}{k} \ln(v/v_0)$, so depth grows exponentially with traveltime.
- This model is useful for understanding first arrivals, diving waves, and tomographic velocity updates.
