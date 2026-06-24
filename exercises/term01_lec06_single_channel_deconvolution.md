# Exercises — Term 1, Lecture 6: Single-channel deconvolution

## Concept-check questions

1. Why can deconvolution not recover frequencies that were never recorded by the acquisition system?
2. A dipole is $(4, 1)$ with a 4 ms sample interval. Is it minimum phase? Where is the zero of its $z$-transform? What is the first coefficient of its causal inverse filter?
3. Explain, using the dipole example, why a mixed-phase wavelet generally needs a two-sided (non-causal) inverse filter.
4. What happens to the result of spiking deconvolution if the reflectivity series is not white?
5. How does increasing the prediction gap change the behavior of predictive deconvolution?
6. Why is prewhitening important in both deterministic and statistical deconvolution?
7. List the four main assumptions of statistical deconvolution and state what goes wrong if each one is violated.

## Short numerical / analytical problems

### Problem 1 — Dipole phase

Consider the dipole $w = (3, 1)$.

(a) Write its $z$-transform $W(z)$.
(b) Find the zero of $W(z)$ and decide whether the dipole is minimum phase.
(c) Compute the first four coefficients of the causal inverse filter by polynomial division.
(d) If the dipole were $(1, 3)$, where would the convergent inverse series live in time?

### Problem 2 — Fourier inverse filter

A known wavelet has amplitude spectrum

$$
|W(f)| = \begin{cases}
1, & 10 \le |f| \le 60 \text{ Hz}, \\
0, & \text{otherwise}.
\end{cases}
$$

(a) Write the expression for the deterministic inverse filter with prewhitening $\varepsilon^2$.
(b) What happens to the inverse-filter gain at $f = 0$ and $f = 70$ Hz when $\varepsilon^2 = 0$?
(c) How does a small positive $\varepsilon^2$ change the gain at those frequencies?

### Problem 3 — Wiener normal equations

A trace has autocorrelation values

$$
\phi_{xx}[0] = 5, \quad \phi_{xx}[1] = 2, \quad \phi_{xx}[2] = 1.
$$

We want a two-coefficient spiking deconvolution operator $f = (f_0, f_1)$.

(a) Write the $2 \times 2$ Wiener normal equations (ignore prewhitening).
(b) Solve for $f_0$ and $f_1$.
(c) Add prewhitening $\varepsilon^2 = 0.5$ to the diagonal and solve again. How do the coefficients change?

## Practical exercise

Open `scripts/figures/term01_lec06/plot_spiking_decon.py`.

1. Change the wavelet to be mixed phase by adding a small leading coefficient (for example, make $w = (0.2, 0.9, 0.4, 0.1)$ and re-normalize). What happens to the recovered wavelet after spiking deconvolution?
2. Increase the noise level from 0.02 to 0.2. How does the deconvolved trace change? What parameter can you adjust to stabilize the result?
3. Replace the random reflectivity with a cyclic sequence (for example, spikes every 20 ms). Does spiking deconvolution still work well? Why or why not?

## Discussion question

In a typical marine processing flow, would you apply deterministic designature before or after predictive deconvolution? Justify your answer in terms of what each method assumes and what each removes.
