---
title: Term 1 Lecture 03 — Advanced Statics and the Link to Velocity Analysis
status: lecture-ready
lecture: term01_lec03
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - noble_2020_whats_the_datum
  - jones_2012_incorporating_near_surface_velocity_anomalies
tags:
  - layer-replacement
  - residual-statics
  - surface-consistent
  - gauss-seidel
  - floating-datum
  - velocity-analysis
---

# Term 1 Lecture 03 — Advanced Statics and the Link to Velocity Analysis

## One-line summary

The second half of the kinematics/statics lecture: layer replacement, residual statics (cross-correlation and surface-consistent Gauss–Seidel), and the floating-datum solution to the statics–velocity-analysis coupling.

## Key concepts covered

- Layer replacement method for long-wavelength statics.
- Residual statics: cross-correlation with a reference trace, cycle skipping.
- Surface-consistent 4-component model: source, receiver, offset, CMP.
- Least-squares formulation and Gauss–Seidel iteration.
- Why long-wavelength statics bias velocity analysis even though CMP gathers remain hyperbolic.
- Floating datum: split total statics into short-wavelength (for processing) and long-wavelength (for final datum) parts.

## Key equations

- 4-component residual statics: $\Delta t_{ijkl} = s_i + r_j + h_k + c_l + \text{noise}$
- Least-squares objective: $\Phi(\mathbf{m}) = \| \mathbf{d} - G \mathbf{m} \|^2$
- Gauss–Seidel source update: $s_i^{(n+1)} = \frac{1}{N_i} \sum (d_{ijkl} - r_j^{(n)} - h_k^{(n)} - c_l^{(n)})$
- Shifted hyperbola: $t^2(x) = (t_0 + \Delta t)^2 + x^2/V^2$
- Floating datum: $\Delta t_\text{floating} = \Delta t_\text{total} - \Delta t_\text{smoothed}$

## Generated figures

| Figure | Path |
|--------|------|
| Layer replacement workflow | `figures/term01_lec03/term01_lec03_layer_replacement.png` |
| Cross-correlation statics | `figures/term01_lec03/term01_lec03_crosscorrelation_statics.png` |
| 4-component model | `figures/term01_lec03/term01_lec03_four_component_model.png` |
| Gauss–Seidel iteration | `figures/term01_lec03/term01_lec03_gauss_seidel.png` |
| Statics bias velocity analysis | `figures/term01_lec03/term01_lec03_statics_velocity_bias.png` |
| Floating datum | `figures/term01_lec03/term01_lec03_floating_datum.png` |

## Lecture materials

- English notes: `lecture_notes/en/term01_lec03_advanced_statics_and_velocity_link.en.md`
- Rendered PDF: `lecture_notes/en/term01_lec03_advanced_statics_and_velocity_link.en.pdf`
- Exercises: `exercises/term01_lec03_advanced_statics_and_velocity_link.md`
- Slide outline: `slides/term01/lec03_advanced_statics_and_velocity_link/slide_outline.md`
- Starter deck: `slides/term01/lec03_advanced_statics_and_velocity_link/lec03_advanced_statics_and_velocity_link.pptx`

## Related concept pages

- [Layer replacement](../concepts/layer_replacement.md)
- [Residual statics](../concepts/residual_statics.md)
- [Floating datum](../concepts/floating_datum.md)
- [Static corrections](../concepts/static_corrections.md)
- [Velocity analysis](../concepts/velocity_analysis.md)
- [Normal moveout](../concepts/normal_moveout.md)

## Notes for instructor

- This lecture is the second half of the original kinematics/statics lecture. Lecture 02 must be covered first.
- The Gauss–Seidel section is the most mathematical part. Keep the update formula simple and emphasize that each sweep is just averaging residuals.
- The velocity-bias figure is important: students often expect statics to destroy hyperbolicity; the point is that hyperbolicity is preserved but $t_0$ is wrong.
- Floating datum is easiest to explain after the velocity-bias argument.
