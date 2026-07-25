---
title: Zhang & Yuan (2019) — Robust surface-consistent deconvolution for foothill seismic data
type: paper
year: 2019
authors: Zhang Yuan, Mo Yangang
source_file: papers/deconvolution/Robust Deconvolution 2019 Zhang Yuan.pdf
status: reviewed
tags: [deconvolution, surface-consistent, robust, L1-L2, noise, foothill, resolution]
---

# Zhang & Yuan (2019) — Robust surface-consistent deconvolution

## Source

- **Authors:** Zhang Yuan, Mo Yangang (SINOPEC Geophysical Corporation R&D Center, Beijing)
- **Title:** Robust Deconvolution to improve resolution of foothill seismic data
- **Conference:** SEG 2019 Workshop: 2nd SEG Foothill Exploration Workshop, Chengdu, China
- **Year:** 2019
- **DOI:** 10.1190/FEW2019-18.1
- **File:** `papers/deconvolution/Robust Deconvolution 2019 Zhang Yuan.pdf`

## Main message

Traditional surface-consistent deconvolution (SCD) fails in foothill areas due to inconsistent noise (ground roll, sporadic noise bursts) that violates Gaussian error assumptions. Robust surface-consistent deconvolution (RSCD) uses hybrid L1/L2 norm optimization to obtain stable operators even with strong inconsistent noise, effectively suppressing high- and low-frequency noise while broadening the effective bandwidth.

## Key points

1. **Problem with conventional SCD:**
   - Solved by least-squares method (L2 norm).
   - Assumes Gaussian noise distribution.
   - Inconsistent noise (ground roll, bursts) creates non-Gaussian error distribution with expectation ~2 dB.
   - Can affect up to 20% of traces.
   - Result: unstable operators, poor deconvolution.

2. **Robust SCD approach:**
   - **Hybrid L1/L2 norm:** L2 norm for signal, L1 norm for noise outliers.
   - **Mathematically correct solver:** handles non-Gaussian noise distribution.
   - **Unbiased results:** even with strong inconsistent noise.

3. **Surface-consistent convolution model:**
   $$w_{ij}(t) = s_i(t) * g_j(t) * m_{(i+j)/2}(t) * p_{(i-j)/2}(t) + n(t)$$
   where:
   - $s_i(t)$: source component at shot $i$
   - $g_j(t)$: receiver component at receiver $j$
   - $m_{(i+j)/2}(t)$: CMP component
   - $p_{(i-j)/2}(t)$: offset component
   - $n(t)$: random noise

4. **Frequency-domain decomposition:**
   $$W(\omega) = S(\omega) G(\omega) M(\omega) P(\omega)$$
   
   Amplitude spectrum:
   $$A_{ij} = A_s A_g A_m A_p$$
   
   Phase spectrum:
   $$\Phi_{ij} = \Phi_s + \Phi_g + \Phi_m + \Phi_p$$

5. **Logarithmic spectrum (minimum-phase assumption):**
   $$\ln A_{ij} = \ln A_s + \ln A_g + \ln A_m + \ln A_p$$

6. **Model error:**
   $$E = \|A_{ij} - \hat{A}_{ij}\|$$
   where $\|\cdot\|$ is Euclidean length of difference vector.

7. **Optimization:**
   $$\frac{\partial E}{\partial \ln A_s} = \frac{\partial E}{\partial \ln A_g} = \frac{\partial E}{\partial \ln A_m} = \frac{\partial E}{\partial \ln A_p} = 0$$
   
   Solved by JOR (Jacobi with Overrelaxation) method.

8. **Three-step procedure:**
   1. **Spectral analysis:** compute logarithmic spectrum $\ln A_{ij}$ for all traces in analysis window.
   2. **Spectral decomposition:** extract component terms $\ln A_s, \ln A_g, \ln A_m, \ln A_p$ by statistical L1/L2 optimization. Operators automatically computed based on S/N of different frequency bands.
   3. **Spectral application:** apply deconvolution operators to all data. Operators are more stable, can use sampling rate as step. Frequency spectrum corrected before deconvolution to reduce effect on noise-dominant bands.

9. **Field data example (south China mountain area):**
   - **Original shot:** effective band 8–55 Hz.
   - **After conventional SCD:** effective band 6–65 Hz (modest improvement).
   - **After robust SCD:** effective band 4–90 Hz (25 Hz broadening at both ends).
   - **Stack section:** RSCD shows better S/N and spatial energy consistency than conventional SCD.

10. **Key advantages:**
    - Stable operators even with inconsistent noise.
    - Effective noise suppression at both high and low frequencies.
    - Resolution improvement without noise amplification.
    - Works for challenging foothill data.

## Key equations

**Surface-consistent convolution model:**
$$w_{ij}(t) = s_i(t) * g_j(t) * m_{(i+j)/2}(t) * p_{(i-j)/2}(t) + n(t)$$

**Frequency-domain decomposition:**
$$W(\omega) = S(\omega) G(\omega) M(\omega) P(\omega)$$

**Logarithmic spectrum:**
$$\ln A_{ij} = \ln A_s + \ln A_g + \ln A_m + \ln A_p$$

**Model error (L2 norm):**
$$E = \|A_{ij} - \hat{A}_{ij}\|$$

**Robust optimization (hybrid L1/L2):**
$$\min \sum_{\text{signal}} |E|^2 + \lambda \sum_{\text{noise}} |E|$$

**JOR update:**
$$\ln A_s^{(k+1)} = (1 - \omega) \ln A_s^{(k)} + \omega \cdot f(\ln A_g^{(k)}, \ln A_m^{(k)}, \ln A_p^{(k)})$$
where $\omega$ is overrelaxation parameter.

## Practical implications

- **Foothill data:** conventional SCD fails due to inconsistent noise; RSCD provides stable results.
- **Parameter selection:** analysis window should be representative; operator length controls bandwidth.
- **QC:** compare amplitude spectra before/after; check stack sections for S/N and continuity.
- **Workflow:** RSCD can replace conventional SCD in challenging areas (foothills, thrust belts, complex near-surface).

## Implications for teaching

- Good example of robust estimation in seismic processing.
- Shows how L1/L2 hybrid norm handles non-Gaussian noise.
- Demonstrates practical application to challenging field data.
- Bridges theoretical surface-consistent model and real-world implementation.

## Concepts informed

- [Surface-consistent deconvolution](../concepts/surface_consistent_deconvolution.md)
- [Deconvolution](../concepts/deconvolution.md)
- [Statistical deconvolution](../concepts/statistical_deconvolution.md)

## Related sources

- [Hutchinson & Link (1984)](hutchinson_link_1984_surface_consistency.md) — original surface-consistent deconvolution paper
- [CGG ODT04 Part 2](cgg_odt04_deconvolution_part2_signature.md) — designature and deghosting workflows
- [Yilmaz (2001)](yilmaz_2001_seismic_data_analysis_deconvolution.md) — textbook treatment of SCD

## Quotes / memorable lines

> "The operator of robust surface deconvolution according to the signal to noise ratio of different frequency bands is more stable, and gives unbiased results even in the presence of strong inconsistent noise in foothill area."

> "The conventional surface consistent decomposition is solved by a least square method and this is problematic as the inconsistent noise creates an error distribution that is far from Gaussian center with an expectancy of about 2 dB."

> "At the kernel of robust surface consistent deconvolution is a mathematically correct and efficient solver for hybrid L1/L2 problem."

> "The spectral phase of RSCD has broadened up to 25Hz at both the high and low frequency."
