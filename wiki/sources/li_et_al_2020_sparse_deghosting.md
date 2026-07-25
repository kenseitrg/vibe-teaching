---
title: Li et al. (2020) — Simultaneous receiver-side deghosting and denoising
type: paper
year: 2020
authors: Hong-Jian Li, Qin-Yong Yang, Jie-Xiong Cai
source_file: papers/marine/li2020.pdf
status: reviewed
tags: [deghosting, denoising, sparse-inversion, fista, frequency-slowness, marine]
---

# Li et al. (2020) — Simultaneous receiver-side deghosting and denoising

## Source

- **Authors:** Li Hong-Jian, Yang Qin-Yong, Cai Jie-Xiong (Sinopec Geophysical Research Institute)
- **Title:** Simultaneous receiver-side deghosting and denoising method based on the sparsity constraint
- **Journal:** Applied Geophysics, 17(3), 411–418
- **Year:** 2020
- **DOI:** 10.1007/s11770-020-0829-3
- **File:** `papers/marine/li2020.pdf`

## Main message

A frequency-slowness domain deghosting method using sparse constraint (FISTA algorithm) simultaneously removes ghost energy and noise, achieving fast convergence and improved S/N. The method accurately calculates ghost time delay and amplitude coefficient for each slowness, then solves for ghost-free data using L1-norm regularization.

## Key points

1. **Problem statement:** marine seismic data contains primary signal, ghost energy, and noise:
   $$d(x, t) = u(x, t) + R \cdot u_c(x, t) + \text{noise}$$
   where $u$ is upgoing primary, $u_c$ is downgoing ghost, $R$ is sea-surface reflection coefficient.

2. **Frequency-slowness domain formulation:**
   $$D(x, \omega) = \sum_p U(p, \omega) \exp(-i\omega(p \cdot x + \Delta t - \Delta u)) + R \sum_p U(p, \omega) \exp(-i\omega(p \cdot x - \Delta t + \Delta u)) + \text{Noise}$$
   where $p$ is slowness, $\Delta t$ and $\Delta u$ are time and updown delays.

3. **Ghost operator:**
   $$G = \exp(-i\omega(\Delta t - \Delta u)) + R \exp(-i\omega(-\Delta t + \Delta u))$$
   where:
   - $\Delta u = \frac{z}{\cos\theta \cdot v}$ (vertical delay)
   - $\Delta t = \frac{z \cdot \tan\theta \cdot \sin\theta}{v}$ (horizontal delay)
   - $R = -R_0 \exp\left(-\frac{2f^2}{v^2 \cos^2\theta}\right)$ (frequency-dependent reflection, $R_0 \approx 1$)

4. **Linear inverse problem:**
   $$d = G V u + \text{noise}$$
   where $V$ is the inverse frequency-slowness transform operator.

5. **Sparse constraint formulation:**
   $$\min_u \|d - GVu\|_2^2 + \lambda \|u\|_1$$
   where $\lambda$ controls the trade-off between data fidelity and sparsity.

6. **FISTA (Fast Iterative Shrinkage-Thresholding Algorithm):**
   - Soft thresholding operator: $\text{soft}(x, T) = \text{sign}(x) \cdot \max(|x| - T, 0)$
   - Iterative update: $s_k = \text{soft}\left(t_{k-1} - \alpha D^T A (t_{k-1} - x), \frac{\alpha\lambda}{2}\right)$
   - Acceleration: $t_k = s_k + \beta_k (s_k - s_{k-1})$ where $\beta_k = \frac{E_{k-1} - 1}{E_k}$, $E_k = \frac{1 + \sqrt{1 + 4E_{k-1}^2}}{2}$

7. **Advantages:**
   - Simultaneous deghosting and denoising (no separate noise attenuation step needed).
   - Accurate ghost operator calculation for each slowness (angle-dependent).
   - Fast convergence with few iterations (FISTA).
   - Robust to noise (L1-norm regularization).

8. **Limitations:**
   - Assumes 1D wave propagation (vertical ghosts).
   - Requires accurate streamer depth and velocity.
   - Sparsity assumption may not hold for all data (e.g., highly complex geology).

9. **Synthetic example:**
   - Model: 40 Hz Ricker wavelet, streamer at 20 m, source at 10 m, water velocity 1500 m/s.
   - Added white Gaussian noise (SNR = 2.06).
   - Result: ghost notches filled, noise suppressed, resolution improved.

10. **Field data example:**
    - Actual streamer data from offshore China.
    - Result: clearer events, improved S/N, broader bandwidth.

## Key equations

**Ghost time delays:**
$$\Delta u = \frac{z}{v \cos\theta}, \quad \Delta t = \frac{z \tan\theta \sin\theta}{v}$$

**Ghost operator:**
$$G(\omega, p) = \exp(-i\omega(\Delta t - \Delta u)) + R(\omega, \theta) \exp(-i\omega(-\Delta t + \Delta u))$$

**Sparse inversion objective:**
$$\min_u \|d - GVu\|_2^2 + \lambda \|u\|_1$$

**FISTA update:**
$$s_k = \text{soft}\left(t_{k-1} - \alpha D^T A (t_{k-1} - x), \frac{\alpha\lambda}{2}\right)$$
$$t_k = s_k + \beta_k (s_k - s_{k-1})$$

## Practical implications

- **Integrated workflow:** deghosting and denoising in one step (simplifies processing flow).
- **Parameter selection:** $\lambda$ controls noise suppression vs. signal preservation; typical values 0.01–0.1.
- **Iteration count:** FISTA converges in 10–30 iterations (fast).
- **QC:** check amplitude spectra (notches should be filled), compare before/after gathers, verify S/N improvement.
- **Works with conventional streamer data:** no dual-sensor or variable-depth acquisition required.

## Implications for teaching

- Good example of modern sparse-inversion approaches to seismic processing.
- Shows how frequency-slowness domain provides accurate angle-dependent ghost modeling.
- Demonstrates FISTA algorithm (widely used in seismic inversion).
- Bridges classical deghosting (Lindsey, Ghosh) and modern methods (Amundsen, Wang).

## Concepts informed

- [Marine deghosting](../concepts/marine_deghosting.md)
- [Broadband seismic](../concepts/broadband_seismic.md)

## Related sources

- [Amundsen & Zhou (2013)](amundsen_zhou_2013_deghosting.md) — low-frequency trace-by-trace deghosting
- [Ghosh (2000)](ghosh_2000_ghost_deconvolution.md) — frequency-domain deghosting
- [CGG ODT04 Part 2](cgg_odt04_deconvolution_part2_signature.md) — bootstrap deghosting

## Quotes / memorable lines

> "The ghost and noise were suppressed robustly using the fast iterative shrinkage–thresholding algorithm (FISTA)."

> "Ghost-free data with high SNR can be solved simultaneously."

> "The effectiveness of the proposed method was proven using synthetic and field data testing results."
