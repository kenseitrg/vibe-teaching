# Term 1 Lecture 03 — Exercises: Advanced Statics and the Link to Velocity Analysis

## Concept-check questions

1. **Layer replacement.**  Why is layer replacement used even after refraction statics have been applied?

2. **Cross-correlation statics.**  A residual static is estimated by cross-correlating a trace with a reference trace. The true shift is 35 ms but the dominant period of the wavelet is 50 ms. Why might the estimated shift be −15 ms instead?

3. **4-component model.**  In the surface-consistent model $\Delta t_{ijkl} = s_i + r_j + h_k + c_l$, which term represents geology rather than a static shift? Why must it be removed before solving for the statics?

4. **Gauss–Seidel.**  Why is Gauss–Seidel iteration preferred over directly inverting the normal-equation matrix $G^\top G$ for residual statics?

5. **Statics and velocity.**  A long-wavelength static shifts every trace in a CMP gather by the same time. Why does this bias the velocity picked from a semblance spectrum even though the gather still looks hyperbolic?

6. **Floating datum.**  Explain in words how a floating datum is computed from total statics and why it preserves hyperbolic moveout for velocity analysis.

7. **Correlation domains.**  In which data domain can receiver statics be isolated most directly?  Why do common-midpoint gathers require surface-consistent decomposition to separate source and receiver statics?

8. **Overdetermined and under-constrained.**  A surface-consistent residual-statics problem has far more traces than unknown source/receiver statics, yet the least-squares solution is not unique.  Explain why both statements can be true, and why residual statics are usually forced to zero mean.

## Short problems

### Problem 1 — Apparent velocity from a static shift

A reflection has true zero-offset time $t_0 = 0.6$ s and true velocity $V_\text{true} = 2200$ m/s. A long-wavelength static shifts the entire CMP gather by $\Delta t = +0.08$ s.

For small offsets, the squared shifted traveltime can be approximated as

$$
t^2(x) \approx (t_0 + \Delta t)^2 + \frac{x^2}{V_\text{true}^2}\left(1 + \frac{\Delta t}{t_0}\right).
$$

Estimate the apparent velocity $V_\text{app}$ that a velocity analysis would pick.

### Problem 2 — Delay time and weathering thickness

A refraction survey gives a weathering velocity $V_1 = 800$ m/s and a sub-weathering velocity $V_2 = 2000$ m/s. The measured source delay time is $\delta t = 0.050$ s. Compute the weathering thickness $h$ under the source.

Use

$$
\delta t = \frac{h}{V_1 \cos i_c}, \qquad i_c = \sin^{-1}\frac{V_1}{V_2}.
$$

### Problem 3 — Gauss–Seidel update

In a 4-component residual-statics problem the current estimates are:

| Source $i$ | $s_i$ (ms) | Receiver $j$ | $r_j$ (ms) | Offset $k$ | $h_k$ (ms) | CMP $l$ | $c_l$ (ms) |
|------------|------------|--------------|------------|------------|------------|---------|------------|
| 1          | 5          | 1            | −3         | 1          | 1          | 1       | 10         |
| 2          | ?          | 2            | 4          | 2          | −2         | 2       | 12         |

For source 2 there are three measured time shifts: $d_{2111}=14$ ms, $d_{2122}=10$ ms, $d_{2212}=15$ ms. Update $s_2$ by holding all other components fixed and averaging the residuals.

## Optional mini-project

Open `scripts/figures/term01_lec03/plot_statics_velocity_bias.py`. Change the static shift from 0.1 s to 0.05 s and re-run. How much does the apparent velocity bias change? Write two sentences explaining what your experiment implies about the importance of removing long-wavelength statics before velocity analysis.

## Answers

<details>
<summary>Click to expand answers</summary>

1. Refraction statics only resolve the near surface that is illuminated by first arrivals. Deeper or more complex anomalies may remain unresolved; layer replacement uses reflection data and a reference horizon to estimate the remaining long-wavelength distortion.

2. The shift (35 ms) is more than half the period (25 ms). Cross-correlation may lock onto the next cycle of the wavelet, giving an estimate of 35 − 50 = −15 ms. This is cycle skipping.

3. $c_l$ is the CMP structural term. It represents true geology (two-way time to the reflector at that CMP). If it is not removed, the static solution will absorb structure and distort the image.

4. $G^\top G$ is enormous and nearly singular for a realistic seismic line. Direct inversion is impractical. Gauss–Seidel updates one component class at a time by simple averaging, converging in a few sweeps.

5. A constant shift changes the zero-offset time $t_0$ of the hyperbola but does not change its shape. Velocity analysis fits $t^2 = t_0^2 + x^2/V^2$; the wrong $t_0$ forces a wrong $V$ to minimize the misfit.

6. Total statics are split into a long-wavelength (smoothed) part and a short-wavelength (residual) part. The floating-datum correction applies only the short-wavelength part, so events in each CMP stay hyperbolic and near their true $t_0$. The long-wavelength part is applied later as a final static.

7. Receiver statics can be isolated most directly in a **common-source gather**, because the source static is the same for both traces and cancels out. In a common-midpoint gather, both the source and receiver statics differ from trace to trace, so their contributions are mixed together and must be separated by surface-consistent decomposition.

8. The system is **overdetermined** because there are many more traces (equations) than source/receiver/CMP unknowns, so the least-squares fit is statistically robust. It is **under-constrained** because adding a constant to every source static and subtracting the same constant from every receiver static leaves every trace equation $s_i + r_j$ unchanged; long-wavelength trends can therefore be traded between sources and receivers. Forcing the statics to zero mean removes this ambiguity and keeps the long-wavelength component in the field-statics / floating-datum part of the workflow.

**Problem 1:**
$$
V_\text{app} \approx \frac{V_\text{true}}{\sqrt{1 + \Delta t/t_0}} = \frac{2200}{\sqrt{1 + 0.08/0.6}} = \frac{2200}{\sqrt{1.1333}} \approx 2067 \text{ m/s}.
$$

**Problem 2:**
$$
i_c = \sin^{-1}(800/2000) = 0.4115 \text{ rad}, \qquad \cos i_c = 0.9165.
$$
$$
h = \delta t \, V_1 \cos i_c = 0.050 \times 800 \times 0.9165 \approx 36.7 \text{ m}.
$$

**Problem 3:**
For each trace, the residual for source 2 is $d - r_j - h_k - c_l$:
- $d_{2111}$: $14 - 4 - 1 - 10 = -1$ ms
- $d_{2122}$: $10 - (-3) - (-2) - 12 = 3$ ms
- $d_{2212}$: $15 - 4 - (-2) - 12 = 1$ ms

Average residual: $(-1 + 3 + 1)/3 = 1$ ms. Therefore $s_2^{\text{new}} = 1$ ms.
</details>
