# Slide outline — Term 1 Lecture 02
## Amplitude Corrections and Quality Control of Input Data

---

# Title

**Amplitude Corrections and Quality Control of Input Data**

Term 1, Lecture 02

---

# Learning objectives

By the end of this lecture you should be able to:

- List the physical effects that reduce seismic amplitude during propagation.
- Explain the difference between relative amplitude preservation (RAP) and amplitude equalization.
- Apply spherical divergence correction and understand the $t$ vs $t^2$ convention.
- Describe how AGC works and how window length controls the trade-off.
- Explain the four-factor surface-consistent amplitude model and how it is solved.
- Verify input data quality through geometry checks and attribute analysis.

---

# Why this lecture matters

- A seismic trace is not just a picture of the subsurface.
- Amplitudes are distorted by source, propagation, receiver, and acquisition effects.
- Modern processing goals: AVO, reservoir characterization, time-lapse monitoring.
- These need amplitudes that mean something physically.
- RAP (relative amplitude preservation) is the modern default.

---

# Physical amplitude effects

**Reflection and transmission:**
$$R = \frac{Z_2 - Z_1}{Z_2 + Z_1}, \quad Z = \rho v$$

**Mode conversion** — P-to-S energy loss at non-normal incidence.

**Spherical divergence** — wavefront expands, amplitude $\propto 1/r$.

**Absorption (Q)** — frequency-dependent, high frequencies attenuate faster.

**Scattering** — energy redirected by small-scale heterogeneities.

**Near-surface effects** — source/receiver coupling variations.

---

# Spherical divergence

- Most predictable amplitude effect.
- In a homogeneous medium: amplitude $\propto 1/t$.
- Correction: multiply by a time-dependent gain $t^n$.
  - $n = 1$ if thinking about amplitude.
  - $n = 2$ if thinking about energy.
- Know your software's convention.
- Real velocities increase with depth → rays bend → more spreading.

**Figure:** `term01_lec02_spherical_divergence_correction.png`

---

# Two philosophies of amplitude processing

**RAP — Relative amplitude preservation (modern default)**
- Keep amplitudes proportional to earth reflectivity.
- Required for AVO, inversion, reservoir monitoring.

**Amplitude equalization (intermediate tool only)**
- Make data visible for picking, statics, velocity analysis.
- AGC, normalization — useful but **not** for quantitative work.

**Key rule:** do not apply aggressive equalization before amplitude-sensitive analysis.

---

# Amplitude normalization

Each trace scaled by a constant derived from its own amplitudes:

$$A_{\text{rms}} = \sqrt{\frac{1}{N}\sum_{n=1}^N a_n^2}$$

- **Within-trace** relative amplitudes preserved.
- **Between-trace** relationships changed.
- Harmful for AVO. Useful for display and kinematic processing.

---

# Automatic Gain Control (AGC)

- Sliding window of length $W$.
- Gain = reciprocal of local RMS amplitude.
- **Short window** — flattens envelope, erases amplitude differences.
- **Long window** — preserves trace shape, acts like a scalar gain.

**Figure:** `term01_lec02_agc_example.png`

---

# AGC window length trade-off

| Window length | Effect | Use case |
|:---|:---|:---|
| 1 sample | Constant absolute amplitude | Extreme equalization |
| ~3 periods (~100 ms) | Partially flattened envelope | Balanced |
| ~500 ms | Covers 2 reflections | Moderate equalization |
| Whole trace | Shape preserved, scaled | Like scalar normalization |

**Short windows:** good for display, bad for AVO.
**Long windows:** preserve relative amplitudes.

---

# Surface-consistent amplitude correction

Four-factor model:

$$A_{ij} = S_i \, R_j \, G_k \, M_l$$

- $S_i$ — source term (coupling, weathering, gun performance).
- $R_j$ — receiver term (coupling, planting, sensitivity).
- $G_k$ — geology / CMP term (reflectivity).
- $M_l$ — offset term (AVO trend).

**Figure:** `term01_lec02_surface_consistent_amplitude.png`

---

# Solving the SCAC model

Take logarithms to make the product additive:

$$\log A_{ij} = \log S_i + \log R_j + \log G_k + \log M_l$$

Gauss–Seidel iteration:

1. Estimate sources (assume receivers, geology, offset fixed).
2. Estimate receivers using current source estimates.
3. Update geology and offset terms.
4. Repeat until convergence.

The CMP term $G_k$ contains geology — often not applied to preserve structure.

---

# Quality control — geometry

Geometry errors are the most dangerous:

- Wrong CMP assignment → mis-stacking, wrong velocities, artefacts.
- **Overlay expected offset curves** on shot gathers.
- **LMO stacks** — stack with linear moveout to check alignment.
- **First-break residuals** — systematic differences reveal timing or geometry problems.

**Figure:** `term01_lec02_qc_geometry_first_breaks.png`

---

# Quality control — attribute analysis

**Amplitude attributes:**
- Mean / RMS amplitude in analysis window.
- Signal-to-microseism ratio.

**Spectral attributes:**
- Central frequency, dominant frequency, bandwidth.

**Statistical and map-based QC:**
- Histograms of amplitudes and frequencies.
- Attribute maps by source, receiver, offset, CMP.
- Vertical stripes → source problems.
- Horizontal stripes → receiver problems.
- Diagonal stripes → geology.

**Figure:** `term01_lec02_qc_amplitude_map.png`

---

# Summary

- Six physical effects reduce seismic amplitude (reflection/transmission, mode conversion, spherical divergence, absorption, scattering, near-surface).
- **RAP** is the modern default; equalization is only for intermediate steps.
- **Spherical divergence** correction uses a deterministic $t^n$ gain.
- **AGC** equalizes via a sliding window — short window erases, long window preserves.
- **Surface-consistent amplitude correction** separates source, receiver, geology, and offset effects using a multiplicative model solved by Gauss–Seidel.
- **Geometry QC** is the first step before any processing.
- **Attribute maps** identify acquisition-related vs geological patterns.

---

# Comprehension questions

1. Why does AGC make a section easier to see but less suitable for AVO analysis?
2. List three physical effects that reduce seismic amplitude.
3. What is the difference between a $t$-gain and a $t^2$-gain for spherical divergence?
4. How does surface-consistent amplitude correction separate source and receiver effects?
5. Why is geometry verification the first QC step?
6. A shot/channel amplitude map shows a vertical stripe — what kind of feature might cause this?
