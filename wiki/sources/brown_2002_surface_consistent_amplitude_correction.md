---
title: Brown (2002) — Surface Consistent Amplitude Correction (SCAC)
status: draft
type: training slides
source_file: papers/signal_processing/metcas - SCAC.ppt.pdf
language: en
pages: 1-112
concepts:
  - surface_consistent_amplitude
  - amplitude_preservation
  - seismic_data_qc
tags: [surface-consistent, amplitude-correction, SCAC, Omega, AVO, QC]
---

# Brown (2002) — Surface Consistent Amplitude Correction (SCAC)

Internal CGG training slides compiled by David Brown (January 2002, updated July 2002) on the surface-consistent amplitude-correction method implemented in the Omega processing system.

## Covered topics

| Section | Slides | Topic |
|---------|--------|-------|
| Introduction | 1–11 | Why amplitude preservation matters; 2D land and 3D marine examples |
| Methodology | 12–20 | Expected and actual data models; log-linear equations; Gauss–Seidel iteration |
| Omega workflow | 21–57 | SCAC_PICK, SCAC_DECOMPOSITION, SCAC_APPLY, WINDOW_DESIGN, LONGWAVELENGTH_REMOVE |
| The CMP term | 58–75 | Geology vs. reflectivity; AVO leakage; spatial smoothing |
| Pseudo surface-consistent effect | 76–87 | Array directivity; why SCAC can help even when assumptions are violated |
| QC products | 88–103 | Model QC, residual QC, maps, pre/post stack comparisons |
| Conclusion | 104–112 | Best practices and caveats |

## Key takeaways

### Why SCAC is needed
- Amplitude variations caused by source strength and receiver coupling are multiplicative and are not geology.
- Examples: land shots that penetrate (or fail to penetrate) the subweathering layer can produce ~20 dB shot-to-shot amplitude variations; marine source arrays can have gun drop-outs.
- Amplitude preservation is essential for AVO, AVAz, and stratigraphic interpretation.

### The 4-factor model
- The amplitude of a measured trace window is modeled as the product of four factors:

$$
A_{ij} = S_i \, R_j \, G_k \, M_l
$$

where $S_i$ = source, $R_j$ = receiver, $G_k$ = geology/CMP, and $M_l$ = offset.
- Optional extra terms: trace-number term and a user-defined literal term.
- Taking logs converts the product into a sum, solved as a large linear system.

### Gauss–Seidel iteration
- The default order is source → receiver → offset.
- First iteration: assume receiver and offset terms are zero, solve for source; then source-corrected receiver; then source- and receiver-corrected offset.
- Subsequent iterations use the previous estimates:

$$
\log S_i = \frac{1}{N_i}\sum\left(\log A_{ij} - \log R_j - \log M_l\right)
$$

and similarly for $R_j$ and $M_l$.
- Iterations stop when the RMS residual between predicted and measured amplitudes becomes small or stops decreasing.

### Practical workflow
- **Input pre-conditioning**: valid start times, bad traces removed, noise attenuated, spikes removed, deterministic spreading/attenuation applied, no adaptive scaling before picking.
- **Window design**: one window only; should contain good-quality signal and preferably the same sequence of events across the survey. For shallow data with large moveout, offset-dependent windows may be needed.
- **SCAC_PICK**: measures RMS or mean-absolute amplitude in the window. RMS is common but sensitive to noise bursts.
- **SCAC_DECOMPOSITION**: builds the source/receiver/offset/CMP model. Order of terms matters; leakage between terms occurs.
- **SCAC_APPLY**: reads the model and applies the multiplicative compensation factors to the traces.

### The CMP / geology term
- The CMP term is a mixture of geology (reflectivity) and spatially varying AVO effects.
- Applying it can remove the very signal one wants to preserve; not applying it can leave long-wavelength amplitude anomalies in the data.
- One strategy is to estimate and subtract an AVO trend from the picks before decomposition (LONGWAVELENGTH_REMOVE), so that SCAC only sees residual surface-consistent effects.

### Noise and QC
- Noise in the picking window biases the model, causing over-attenuation of individual sources or receivers.
- QC diagnostics:
  - **Fold**: low fold means poor statistics.
  - **Mean residual**: should be small.
  - **RMS residual**: small indicates good model fit.
  - **Standard deviation of residuals**: small and clustered around the mean is desirable.
- Visual QC: pre- and post-stack gathers, marker-horizon amplitude maps on a single offset, and difference maps.

### Limitations
- Array directivity is strictly not surface-consistent (it depends on emergence angle), yet SCAC can partially reduce its appearance in stacked data.
- Leakage between terms means omitting a term from application can leave compensating errors in the remaining terms.
- 3D surveys require consistent model handling across the whole area; super-gridding may help.

## Figures useful for teaching
- Slide 5: multiplicative source/receiver coupling table.
- Slide 8: shot amplitude estimates from Indonesia dynamite land data.
- Slide 9–10: pre- and post-SCAC CMPs from a 3D marine data set.
- Slide 12–14: 4-factor model equations.
- Slide 18–20: Gauss–Seidel iteration steps.
- Slide 85–86: array directivity as a pseudo-surface-consistent effect.
- Slide 103–110: pre/post SCAC source/receiver/offset term application.

## Relation to lecture notes
- Primary source for the surface-consistent amplitude-correction section of Term 1 Lecture 2.
- Provides the four-factor model, the log-linear Gauss–Seidel solution, and practical QC workflow.
- Supports the discussion of why amplitude preservation matters for AVO.
