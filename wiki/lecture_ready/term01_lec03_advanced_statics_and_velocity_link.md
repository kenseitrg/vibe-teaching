---
title: Term 1 Lecture 03 — Advanced Statics and the Link to Velocity Analysis
status: lecture-ready
lecture: term01_lec03
sources:
  - hatton_worthington_makin_1986_seismic_data_processing
  - noble_2020_whats_the_datum
  - jones_2012_incorporating_near_surface_velocity_anomalies
  - margrave_2006_methods_of_seismic_data_processing
  - li_1999_introduction_to_residual_statics_analysis
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
- Residual statics: cross-correlation with a reference trace, cycle skipping, and correlation domains (common source, receiver, offset, CMP).
- Surface-consistent 4-component model: source, receiver, offset, CMP; surface consistency arises from vertical-ray propagation through the low-velocity near surface.
- Least-squares formulation and Gauss–Seidel iteration; the system is overdetermined but under-constrained.
- Why long-wavelength statics bias velocity analysis: the gather is shifted in $t_0$ but its curvature is unchanged, so velocity analysis fits the wrong velocity to the same curvature.
- Floating datum: smooth source/receiver fields, interpolate to CMPs, subtract half of the long-wavelength component from each side, and apply residual corrections so that each CMP sits on a locally flat surface near the recording surface.

## Key equations

- 4-component residual statics: $\Delta t_{ijkl} = s_i + r_j + h_k + c_l + \text{noise}$
- Least-squares objective: $\Phi(\mathbf{m}) = \| \mathbf{d} - G \mathbf{m} \|^2$
- Gauss–Seidel source update: $s_i^{(n+1)} = \frac{1}{N_i} \sum (d_{ijkl} - r_j^{(n)} - h_k^{(n)} - c_l^{(n)})$
- Shifted hyperbola: $t^2(x) = (t_0 + \Delta t)^2 + x^2/V^2$
- Floating datum at CMP $l$: $\Delta t_\text{long-wavelength}(l) = S^\text{LW}(x_l) + R^\text{LW}(x_l)$
- Residual source/receiver statics after floating-datum removal:
  $$
  s_i^\text{res}(l) = s_i - \frac{1}{2}\Delta t_\text{long-wavelength}(l), \quad
  r_j^\text{res}(l) = r_j - \frac{1}{2}\Delta t_\text{long-wavelength}(l).
  $$

## Generated figures

| Figure | Path |
|--------|------|
| Layer replacement workflow | `figures/term01_lec03/term01_lec03_layer_replacement.png` |
| Cross-correlation statics | `figures/term01_lec03/term01_lec03_crosscorrelation_statics.png` |
| 4-component model | `figures/term01_lec03/term01_lec03_four_component_model.png` |
| Statics bias velocity analysis | `figures/term01_lec03/term01_lec03_statics_velocity_bias.png` |
| Floating datum | `figures/term01_lec03/term01_lec03_floating_datum.png` |
| Velocity and statics (ray paths and traveltime curves) | `figures/term01_lec03/term01_lec03_velocity_and_statics.png` |

## Lecture materials

- English notes: `lecture_notes/en/term01_lec03_advanced_statics_and_velocity_link.en.md`
- Rendered PDF: `lecture_notes/en/term01_lec03_advanced_statics_and_velocity_link.en.pdf`
- Derivation (Gauss–Seidel): `lecture_notes/derivations/gauss_seidel_residual_statics_derivation.en.md`
- Rendered derivation PDF: `lecture_notes/derivations/gauss_seidel_residual_statics_derivation.en.pdf`
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
- The velocity-bias argument is central: a long-wavelength static shifts the whole gather in $t_0$ but leaves the curvature unchanged. Students often expect statics to destroy hyperbolicity; the point is that the same curvature is now fitted to a hyperbola with the wrong zero-offset time, which biases the velocity pick.
- The new ray-path/traveltime figure (`term01_lec03_velocity_and_statics.png`) is useful for showing the link between topography, datums, and the recorded traveltime curve before introducing the hyperbola equation.
- The correlation-domains table is a powerful way to show why different data sorts are used in statics analysis and which effects cancel out in each domain.
- The design-matrix section introduces two key ideas: the system is **overdetermined** (many more traces than unknowns), which gives statistical robustness, and **under-constrained** (not unique; adding a constant to all sources and subtracting it from all receivers leaves the fit unchanged), which explains why zero-mean constraints are needed and why long wavelengths cannot be resolved.
- Floating datum is easiest to explain after the velocity-bias argument. Emphasize that the long-wavelength component is removed in the CMP domain, so the residual source and receiver statics are no longer strictly surface-consistent.
- When discussing QC, stress that residual source and receiver statics should be geophysically consistent (same sign in nearby locations) except for buried sources, where they may legitimately differ. Also note that correlation windows should avoid first arrivals (too shallow) and multiples (too deep), and avoid NMO-stretched shallow data.
