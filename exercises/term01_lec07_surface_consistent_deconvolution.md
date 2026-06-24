# Exercises — Term 1, Lecture 7: Surface-consistent deconvolution and practical implementation

## Concept-check questions

1. Why does surface-consistent deconvolution need more than one trace per source or receiver location?
2. What happens to a spiking-deconvolution operator if the analysis window contains strong ground roll?
3. When would you prefer deterministic deconvolution over statistical deconvolution?
4. How does prewhitening affect the deconvolved spectrum at frequencies where the signal is weak?
5. What is the parallel between surface-consistent deconvolution and residual statics?
6. Why is a long operator not always better than a short operator?
7. Explain why taking the logarithm of the amplitude spectrum turns the surface-consistent convolutional model into a linear system.

## Short problems

### Problem 1 — Surface-consistent geometry

A survey has 3 shots and 3 receivers. The observed log-amplitude values at 30 Hz for four traces are:

| Trace | Shot | Receiver | Observed $d$ |
|-------|------|----------|--------------|
| 0     | S0   | R0       | 2.0          |
| 1     | S0   | R1       | 1.8          |
| 2     | S1   | R0       | 1.5          |
| 3     | S2   | R2       | 0.9          |

(a) Write the design matrix $G$ for the unknown source terms $s_0, s_1, s_2$ and receiver terms $r_0, r_1, r_2$.
(b) How many equations and how many unknowns do you have? Is the system overdetermined or underdetermined?
(c) Set up the least-squares normal equations $G^T G m = G^T d$ and solve for the source and receiver terms.

### Problem 2 — Parameter choices

For each processing goal below, choose reasonable values or ranges for prediction gap, operator length, and prewhitening, and justify your choices.

(a) Compress the wavelet on a high-S/N marine line with a stable source signature.
(b) Suppress water-layer reverberations with a two-way time of 80 ms on data sampled at 4 ms.
(c) Stabilize deconvolution on a noisy land line with visible ground roll below 12 Hz.

## Practical exercises

### Exercise 1 — Deterministic deconvolution

Run `scripts/figures/term01_lec07/demo_deterministic_decon.py`.

1. Change the prewhitening parameter `eps` to 0.0, 0.01, 0.05, and 0.5. Plot the output for each case and describe the trade-off.
2. Add a ghost to the wavelet by convolving it with $(1, 0, -0.8)$. Does deterministic deconvolution still recover sharp spikes?

### Exercise 2 — Wiener normal equations

Run `scripts/figures/term01_lec07/demo_wiener_matrix.py`.

1. Print the first row and the main diagonal of the autocorrelation matrix $\mathbf{R}$. Why is the matrix symmetric and Toeplitz?
2. Increase the noise level from 0.03 to 0.3. How do the operator and the output change? What parameter can you tune to recover stability?
3. Replace the spike desired output with a smoothed desired wavelet (for example, a Ricker wavelet) and observe the shaping-filter behavior.

### Exercise 3 — Tiny surface-consistent system

Use the design matrix from Problem 1 and the NumPy function `numpy.linalg.lstsq` to solve for source and receiver terms. Verify that your least-squares prediction reproduces the observed values as closely as possible.

## Discussion question

A colleague argues that surface-consistent deconvolution is unnecessary because modern Wiener deconvolution already uses robust estimators. Under what field conditions would you disagree? Give specific examples of noise or acquisition geometry where the surface-consistent model provides a clear advantage.
