# Term 1 Lecture 02 — Exercises: Kinematics, Velocities and Field Statics

## Concept-check questions

1. **Velocity definitions.**  For a layered medium, which velocity is the largest in general: average, RMS, or NMO?  Explain why using the ray assumptions behind each definition.

2. **NMO correction.**  A CMP gather contains a reflection with $t_0 = 1.0$ s.  Using an NMO velocity of $2000$ m/s, compute the reflection time at offsets $x = 0$, $1000$ and $3000$ m.

3. **Under- and over-correction.**  Sketch the shape of a reflection after NMO correction if the applied velocity is (a) too high, (b) too low, and (c) correct.

4. **Stretch and mute.**  Why does NMO correction stretch the wavelet at far offsets?  Why must stretched samples be muted before stack?

5. **Semblance.**  Explain why semblance is preferred over a simple stacked-amplitude measure when picking velocities from noisy data.

6. **Statics.**  A receiver sits on a hill $30$ m above the final datum.  The weathering layer is $20$ m thick with velocity $800$ m/s and is replaced by a velocity of $1800$ m/s.  Assuming vertical rays, compute the total static shift (in milliseconds) relative to the datum.  Is the shift a time advance or a delay?

7. **Refraction statics.**  In a two-layer model, the crossover distance increases if the weathering velocity decreases (other parameters fixed).  Explain why this makes physical sense.

## Short problems

### Problem 1 — Convert RMS to interval velocity with Dix

A vertical velocity spectrum gives the following RMS-velocity picks:

| $t_0$ (s) | $V_\text{rms}$ (m/s) |
|-----------|----------------------|
| 0.5       | 1800                 |
| 1.0       | 2100                 |

Use the Dix formula to estimate the interval velocity of the layer between $t_0 = 0.5$ s and $t_0 = 1.0$ s:

$$
v_\text{int}^2 = \frac{V_\text{rms,2}^2 \, t_2 - V_\text{rms,1}^2 \, t_1}{t_2 - t_1}.
$$

### Problem 2 — NMO stretch threshold

For an event at $t_0 = 0.6$ s and $V_\text{nmo} = 1800$ m/s, find the maximum offset at which the fractional NMO stretch stays below $20$ %.  Use the approximate stretch expression

$$
\text{fractional stretch} \approx \frac{x^2}{2 \, t_0^2 \, V_\text{nmo}^2} \times 100\%.
$$

### Problem 3 — Refraction delay time

A two-layer model has weathering thickness $h = 80$ m, weathering velocity $v_1 = 1000$ m/s, and bedrock velocity $v_2 = 2500$ m/s.  The critical angle is $\theta_c = \sin^{-1}(v_1/v_2)$.  Compute the delay time for a vertical ray that travels down to the bedrock and back up through the weathering layer.

## Optional mini-project

Open `scripts/figures/term01_lec02/plot_velocity_spectrum.py` and modify the reflector parameters (times, velocities, amplitudes).  Re-run the script and observe how the semblance peaks move in the velocity spectrum.  Write two or three sentences explaining what you learned about the trade-off between velocity resolution and time resolution.

## Answers

<details>
<summary>Click to expand answers</summary>

1. RMS $\ge$ average because it squares velocities before averaging.  NMO velocity can be close to RMS for flat layers but may differ in the presence of anisotropy or dip.

2. Using $t(x) = \sqrt{t_0^2 + x^2/V^2}$:
   - $x = 0$: $t = 1.000$ s
   - $x = 1000$ m: $t = \sqrt{1 + (1000/2000)^2} = 1.118$ s
   - $x = 3000$ m: $t = \sqrt{1 + (3000/2000)^2} = 1.803$ s

3. (a) Too high: event still curves downward (under-corrected).  (b) Too low: event curves upward (over-corrected).  (c) Correct: flat event.

4. NMO maps samples from a longer input time to a shorter output time, stretching the wavelet.  Stretched samples have lowered frequency and can contaminate the stack, so they are muted.

5. Semblance normalizes by the total trace energy, so it is robust to amplitude variations and highlights coherent alignment rather than strong amplitudes.

6. Time from surface to datum through real layers:
   - Elevation: $30 / 1800 = 0.01667$ s
   - Weathering: $20 / 800 = 0.025$ s
   - Total real time: $0.04167$ s
   - Time if replaced by $1800$ m/s over $50$ m: $50/1800 = 0.02778$ s
   - Static shift: $0.04167 - 0.02778 = 0.01389$ s $\approx 13.9$ ms delay.  The recorded trace is delayed, so the static correction is a negative shift (advance).

7. Lower weathering velocity makes the direct wave slower relative to the refracted wave, so the refracted wave becomes the first arrival at a larger offset.

**Problem 1:**
$$
v_\text{int}^2 = \frac{2100^2 \times 1.0 - 1800^2 \times 0.5}{1.0 - 0.5}
= \frac{4.41 \times 10^6 - 1.62 \times 10^6}{0.5}
= 5.58 \times 10^6
$$
so $v_\text{int} \approx 2362$ m/s.

**Problem 2:**
$$
0.20 \approx \frac{x^2}{2 \times 0.6^2 \times 1800^2}
\Rightarrow x^2 \approx 0.20 \times 2 \times 0.36 \times 3.24 \times 10^6
\approx 4.67 \times 10^5
$$
so $x \approx 683$ m.

**Problem 3:**
Critical angle: $\theta_c = \sin^{-1}(1000/2500) = 0.4115$ rad.
Vertical travel path through weathering: $2h = 160$ m.
Delay time: $\delta t = 2h\cos\theta_c / v_1 = 160 \times \cos(0.4115) / 1000 \approx 0.147$ s.
</details>
