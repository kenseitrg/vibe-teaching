# Term 3 Lecture 03 — Surface Waves

## Scope

Surface waves are the dominant coherent noise on land seismic records. They travel along the free surface, contaminate near-offset traces, and are dispersive and multimodal. This lecture explains their physics, why they are difficult to remove with conventional filters, how to analyze them (FK-MUSIC), how to invert dispersion curves for near-surface shear velocity, and how to model and subtract them adaptively.

The lecture focuses strictly on surface waves: their physical nature, dispersion, multimodality, analysis, inversion, and adaptive subtraction. It does not cover general coherent-noise attenuation methods such as FK or Radon filtering for other noise types.

## Learning objectives

By the end of this lecture students should be able to:

- Describe Rayleigh and Love surface waves and their particle motion.
- Explain why surface waves are noise for reflection processing but signal for near-surface characterization.
- Define phase velocity and group velocity and explain how dispersion arises in a layered medium.
- Sketch how a layered medium produces multiple surface-wave modes and why each mode samples depth differently.
- Explain why conventional filters fail to remove surface waves without damaging reflections.
- Describe the FK-MUSIC dispersion-spectrum workflow and how to pick dispersion curves.
- Explain how a dispersion curve is inverted for a near-surface $V_s$ profile and how multiple modes can constrain $V_p/V_s$.
- Build a simple frequency-dependent linear-moveout model of surface waves and explain why adaptive subtraction is needed after modeling.
- Recall the conceptual role of auto- and cross-correlation in adaptive filtering.

## Prerequisites

- Term 1 Lecture 06 (single-channel deconvolution): convolution, cross-correlation, Wiener filter basics.
- Basic elasticity: stress, strain, Hooke's law, P-wave and S-wave velocities.
- Term 3 Lecture 02: near-surface velocity model, first-break traveltimes, vertical-ray approximation.

## Timing (90 minutes)

| Section | Time | Notes |
|---------|------|-------|
| 1. What surface waves are | 10 min | Rayleigh and Love waves; particle motion; energy trapped near the free surface |
| 2. Surface waves as noise and as signal | 10 min | Contamination of near offsets; near-surface information; inversion vs. attenuation |
| 3. Dispersion | 15 min | Phase velocity, group velocity, physical origin in depth-dependent velocity |
| 4. Multimodality | 15 min | Layered media, fundamental and higher modes, depth sensitivity |
| 5. Why conventional attenuation fails | 10 min | Overlap with reflections; why velocity/dispersion separation is better |
| 6. Surface-wave analysis: FK-MUSIC | 15 min | Dispersion spectrum, phase-velocity scanning, eigenvector decomposition |
| 7. Inversion for near-surface $V_s$ | 10 min | From dispersion curve to $V_s$ profile; multi-mode $V_p/V_s$ constraint |
| 8. Modeling and adaptive subtraction | 10 min | Frequency-dependent linear moveout; spatial smoothing; adaptive subtraction recap |
| 9. Summary and questions | 5 min | Recap and comprehension questions |
| **Total** | **90 min** | Tight; keep derivations conceptual in the main notes |

## Section 1 — What surface waves are

- Surface waves travel along the free surface of the Earth, not through the deep interior.
- **Rayleigh waves** are the most common on land seismic records. They are P-SV motion coupled at the free surface and produce elliptical retrograde particle motion in the vertical plane.
- **Love waves** require a shallow low-shear-velocity layer over a higher-velocity half-space. They are pure SH motion and produce horizontal transverse particle motion.
- Surface waves decay exponentially with depth; their energy is trapped near the surface.
- In a homogeneous half-space only Rayleigh waves exist (no Love waves); in a layered medium both Rayleigh and Love waves can propagate, and they become dispersive.
- Typical land ground roll is dominated by Rayleigh waves, often mixed with direct arrivals and air waves.
- Figure idea: particle-motion diagrams for Rayleigh and Love waves; schematic of a shot gather with low-velocity surface-wave train.

## Section 2 — Surface waves as noise and as signal

- For reflection processing, surface waves are coherent noise: they overlap with reflections in time and frequency and have high amplitude, masking primary reflections on near-offset traces.
- For near-surface geotechnical or statics work, surface waves are signal: their dispersion curve constrains the shear-velocity structure of the upper tens of meters.
- The same wavefield is processed differently depending on the objective.
- **Surface-wave inversion (SWI)** / **MASW** uses the dispersion curve to estimate $V_s$; this is a standard geotechnical tool and increasingly useful for building near-surface velocity models.
- **Surface-wave attenuation** in reflection processing needs a model of the surface waves; simply filtering in frequency or offset often removes signal too.
- Figure idea: shot gather with surface waves labeled; same gather after surface-wave removal showing reflections; or a flowchart showing the two contexts (noise vs. signal).

## Section 3 — Dispersion

- In a homogeneous half-space the Rayleigh-wave velocity is constant and independent of frequency.
- In a layered medium the phase velocity $c(f)$ depends on frequency because different frequencies sense different depths.
- **Phase velocity**: $c(f) = \omega / k = f \lambda$, where $\omega$ is angular frequency, $k$ is wavenumber, and $\lambda$ is wavelength.
- **Group velocity**: $U = d\omega / dk$; it is the velocity of a wave packet and the energy propagation speed. It can differ from phase velocity, especially near strong dispersion.
- Physical intuition: long-wavelength (low-frequency) surface waves penetrate deeper and are therefore faster when velocity increases with depth; short-wavelength (high-frequency) waves stay shallow and slower.
- A simple two-layer model: shallow layer $V_{s1}$, deep half-space $V_{s2} > V_{s1}$; $c(f)$ increases from near $V_{R1}$ at high frequency to near $V_{R2}$ at low frequency.
- **Dispersion curve**: a plot of $c(f)$ or $V_R(f)$ versus frequency.
- Figure idea: dispersion curve for a two-layer model; wavelength-depth sensitivity diagram; phase vs. group velocity example.
- Key equations to include: definitions of phase and group velocity; qualitative trend of $c(f)$ for an increasing-velocity profile.
- Derivation reference: formal Rayleigh-wave dispersion derivation in `lecture_notes/derivations/surface_wave_dispersion_derivation.en.md`.

## Section 4 — Multimodality

- A single homogeneous layer over a half-space supports one surface-wave mode: the **fundamental mode**.
- A stack of many layers supports an infinite (in theory) sequence of modes: fundamental, first higher, second higher, etc.
- Higher modes are dispersive and have different depth sensitivity than the fundamental mode; they can be observed when the source excites them and the receiver array can resolve them.
- Multimodality is important because combining several modes improves the resolution and depth range of $V_s$ inversion and can help estimate $V_p/V_s$.
- Figure idea: mode shapes (eigenfunctions) for fundamental and first higher mode; dispersion-curve plot showing several modes.
- Derivation reference: layered-medium multimodal derivation in `lecture_notes/derivations/surface_wave_multimodality_derivation.en.md`.

## Section 5 — Why conventional attenuation fails

- Surface waves and reflections overlap in time and frequency, so simple frequency filtering removes reflections too.
- They are spatially coherent and dispersive, so linear-moveout or velocity filters are approximate at best.
- Source and receiver coupling, topography, and near-surface heterogeneity make surface-wave amplitude and phase vary spatially, so a single model does not fit everywhere.
- A better approach is to **model** the surface waves from a measured dispersion curve and then subtract them adaptively.
- Figure idea: spectrum/amplitude comparison showing overlap of surface-wave band and reflection signal; residual after a naive band-reject filter.

## Section 6 — Surface-wave analysis: FK-MUSIC

- **Slant stack / tau-p transform** maps a shot gather to intercept time vs. ray parameter, but for dispersive surface waves we need a frequency-dependent phase-velocity transform.
- **FK analysis** transforms offset-space to wavenumber-frequency; the dispersion curve appears as energy concentration along a line $k = \omega / c(f)$.
- **FK-MUSIC** (Multiple Signal Classification) improves resolution by using the eigenstructure of the cross-spectral matrix across receivers.
  - Build the data matrix in a frequency slice.
  - Compute the cross-spectral matrix and decompose it into signal and noise subspaces.
  - Scan a test phase-velocity vector; the pseudo-spectrum peaks where the steering vector is orthogonal to the noise subspace.
- The result is a high-resolution dispersion spectrum $G(f, c)$ or $P(f, c)$ from which modes can be picked.
- Figure idea: synthetic shot gather of surface waves; conventional FK spectrum; FK-MUSIC pseudo-spectrum with picked peaks; picked dispersion curves.
- Key equation: FK-MUSIC pseudo-spectrum, e.g. $P(f, c) = \left[ \mathbf{e}^H(f, c) \mathbf{E}_n \mathbf{E}_n^H \mathbf{e}(f, c) \right]^{-1}$ or a normalized equivalent.

## Section 7 — Inversion for near-surface $V_s$

- The dispersion curve is a set of observed phase velocities at discrete frequencies.
- Forward problem: given a layered $V_s$, $V_p$, $\rho$ model, compute the theoretical dispersion curve (eigenvalue problem for each frequency).
- Inverse problem: adjust the layered model to minimize the misfit between observed and predicted dispersion curves.
- Regularization is needed because the problem is non-unique and shallow layers are better resolved than deep ones.
- If several modes are picked, the inversion can constrain $V_p/V_s$ and Poisson's ratio in addition to $V_s$.
- Output: a near-surface $V_s$ profile that can be used for geotechnical or statics/migration work.
- Figure idea: observed vs. predicted dispersion curve; inverted $V_s$ profile with depth resolution shaded.
- Key equation: misfit functional, e.g. $\Phi(V_s) = \sum_f \left[ c_\text{obs}(f) - c_\text{pred}(f; V_s) \right]^2 + \lambda \| D V_s \|^2$.

## Section 8 — Modeling and adaptive subtraction

- Once a dispersion curve is picked, surface waves can be modeled on each shot gather by applying a frequency-dependent linear moveout: $t(x, f) = x / c(f)$.
- Spatial smoothing (e.g., median filter along the spatial axis) helps stabilize the model where noise or near-surface variations disrupt the local phase.
- The modeled surface wave has the right kinematics but not necessarily the correct amplitude and phase. Direct subtraction would leave residual energy or remove reflection signal.
- **Adaptive subtraction** uses a short filter that convolves the model with filter coefficients estimated by minimizing the energy of the residual (or maximizing the match to the observed noise). This is conceptually the same Wiener idea as in Term 1 Lecture 06.
- Filter length matters: too short cannot correct amplitude/phase mismatch; too long can adapt to reflections and remove signal.
- Figure idea: input gather, modeled surface-wave gather, residual after adaptive subtraction; panel showing short vs. long filter effect.
- Keep the adaptive-filter math conceptual; reference the Wiener derivation from Term 1 Lecture 06.

## Section 9 — Summary and comprehension questions

- Surface waves are trapped near the free surface; Rayleigh waves dominate land records, Love waves need a low-velocity layer.
- They are noise for reflection processing but contain near-surface $V_s$ information.
- Dispersion: low-frequency waves sense deeper, faster material; the dispersion curve $c(f)$ characterizes the medium.
- Multimodality: layered media support fundamental and higher modes, each with different depth sensitivity.
- Conventional filters fail because of overlap; model-based adaptive subtraction is preferred.
- FK-MUSIC gives high-resolution dispersion spectra from which modes are picked.
- Inversion yields a $V_s$ profile; multiple modes can constrain $V_p/V_s$.
- The modeled surface wave is subtracted adaptively because amplitude and phase are not perfectly known.

## Figures to generate

| Figure | Script | Output | Concept |
|--------|--------|--------|---------|
| Rayleigh and Love particle motion | `plot_particle_motion.py` | `term03_lec03_particle_motion.png` | What surface waves are |
| Surface-wave contamination on a shot gather | `plot_surface_wave_gather.py` | `term03_lec03_surface_wave_gather.png` | Noise vs. signal |
| Dispersion in a two-layer model | `plot_dispersion_two_layer.py` | `term03_lec03_dispersion_two_layer.png` | Dispersion |
| Phase vs. group velocity | `plot_phase_group_velocity.py` | `term03_lec03_phase_group_velocity.png` | Dispersion |
| Fundamental and higher modes | `plot_multimodality.py` | `term03_lec03_multimodality.png` | Multimodality |
| FK-MUSIC dispersion spectrum | `plot_fk_music_spectrum.py` | `term03_lec03_fk_music_spectrum.png` | Surface-wave analysis |
| Inversion result: dispersion curve fit and $V_s$ profile | `plot_inversion_result.py` | `term03_lec03_inversion_result.png` | Inversion |
| Frequency-dependent linear moveout model | `plot_linear_moveout_model.py` | `term03_lec03_linear_moveout_model.png` | Modeling |
| Adaptive subtraction workflow | `plot_adaptive_subtraction.py` | `term03_lec03_adaptive_subtraction.png` | Adaptive subtraction |
| Short vs. long adaptive filter effect | `plot_filter_length.py` | `term03_lec03_filter_length.png` | Adaptive subtraction |

## Key equations to include

- Rayleigh equation for a homogeneous half-space: $(2 - V_R^2/V_s^2)^2 - 4\sqrt{1 - V_R^2/V_p^2}\,\sqrt{1 - V_R^2/V_s^2} = 0$.
- Phase velocity: $c(f) = \omega / k = f \lambda$.
- Group velocity: $U = d\omega / dk$.
- Wavelength-depth rule of thumb: $\lambda \approx V_R / f$; penetration depth scales with $\lambda$.
- FK-MUSIC pseudo-spectrum (normalized): $P(f, c) = \left[ \mathbf{e}^H(f, c) \mathbf{E}_n \mathbf{E}_n^H \mathbf{e}(f, c) \right]^{-1}$.
- Frequency-dependent linear moveout: $t(x, f) = x / c(f)$.
- Dispersion-curve misfit: $\Phi(V_s) = \sum_f \left[ c_\text{obs}(f) - c_\text{pred}(f; V_s) \right]^2 + \lambda \| D V_s \|^2$.

## Comprehension questions

1. Why do surface waves dominate the near offsets of a land shot gather?
2. How does particle motion differ between Rayleigh and Love waves? What elastic structure is needed for a Love wave to exist?
3. Explain dispersion with the "long wavelengths see deeper" intuition for a medium where velocity increases with depth.
4. What is the difference between phase velocity and group velocity? In which part of the dispersion curve is the difference largest?
5. Why does a layered medium support multiple surface-wave modes, while a homogeneous half-space supports only one Rayleigh mode?
6. Why do simple frequency filters or band-reject filters often fail to remove surface waves without damaging reflections?
7. What does FK-MUSIC improve compared with a simple frequency-wavenumber spectrum, and why is it useful for multimodal data?
8. A dispersion curve gives phase velocity versus frequency. How is that information turned into a $V_s$ depth profile?
9. Why is the modeled surface wave subtracted adaptively instead of being subtracted directly?
10. What is the practical risk of using an adaptive filter that is too long?

## Links to wiki concepts

- `wiki/concepts/surface_waves.md` — Rayleigh and Love waves, particle motion, energy trapping.
- `wiki/concepts/surface_wave_dispersion.md` — phase velocity, group velocity, dispersion curves.
- `wiki/concepts/surface_wave_multimodality.md` — modes in layered media, depth sensitivity.
- `wiki/concepts/surface_wave_inversion.md` — from dispersion curve to $V_s$ profile.
- `wiki/concepts/fk_music_surface_waves.md` (or `surface_wave_analysis.md`) — dispersion spectra and FK-MUSIC.
- `wiki/concepts/adaptive_subtraction.md` — conceptual adaptive filtering for modeled noise.
- `wiki/concepts/wiener_filter.md` — link to the Wiener filter from Term 1 Lecture 06.

## Sources to ingest

Ingest all PDFs from `papers/surface_waves/`:

- `Foti - Surface Wave Methods.pdf` — practical and theoretical overview, MASW, inversion.
- `Novotny-SeismicSurfaceWaves-ocr.pdf` — Rayleigh-wave theory, half-space, layered media.
- `SEDI Surface Waves.pdf` — Rayleigh and Love waves, dispersion, global seismology perspective.
- `seismology_lectures.pdf` (Rawlinson) — surface waves and dispersion lecture notes.
- `datta2018.pdf` — short communication on a focused surface-wave topic.
- `surface_waves_practical.pdf` (Priestley) — practical workflow and examples.
- `Julian Ivanov - Benefits of using the high-resolution linear Radon transform with the multichannel analysis of....pdf` — HRLRT for MASW and dispersion analysis.

Optional (if scope allows): the two surface-wave-related papers in `papers/noise_attenuation/`:
- `Sebastiano Foti - Guidelines for the good practice of surface wave analysis - a product of the InterPACIFIC project.pdf` — good-practice guidelines.
- `surface_waves_dispersion_energy_analysis.pdf` — finite-difference modeling of dispersion energy.

## Derivation documents needed

1. `lecture_notes/derivations/surface_wave_dispersion_and_multimodality_derivation.en.md`
   - Rayleigh wave in a homogeneous elastic half-space: elastic wave equation, boundary conditions at the free surface, derivation of the Rayleigh equation, relation $V_R < V_s < V_p$ and $V_R \approx 0.92\,V_s$.
   - Phase velocity and group velocity: derivation from superposition of two close-frequency waves, group velocity as envelope velocity.
   - Layered-medium dispersion: physical origin (depth-dependent sampling), dispersion relation as eigenvalue problem, conceptual Thomson-Haskell propagator matrix.
   - Multimodality: fundamental and higher modes, depth sensitivity, mode misidentification.
   - Brief note on Love waves (same principles, simpler SH derivation).

## Notation to add

Add to the notation glossary in `AGENTS.md`:

| Symbol | Meaning | Russian term |
|--------|---------|--------------|
| $V_R$ | Rayleigh-wave phase velocity | фазовая скорость поверхностной волны |
| $c(f)$ | Frequency-dependent phase velocity | фазовая скорость (зависит от частоты) |
| $U(f)$ | Group velocity | групповая скорость |
| $V_s$ | Shear-wave velocity | скорость поперечной волны |
| $V_p$ | Compressional-wave velocity | скорость продольной волны |
| $\mu$, $\lambda$ | Lamé parameters | параметры Ламе |
| $\rho$ | Density | плотность |
| $k$ | Wavenumber | волновое число |
| $\omega$ | Angular frequency | круговая частота |
| $D(f)$ | Dispersion curve | дисперсионная кривая |
| $n$ | Mode number | номер моды |
| $G(f, c)$ or $P(f, c)$ | Dispersion spectrum / FK-MUSIC pseudo-spectrum | спектр дисперсии |
| $\hat{h}[n]$ | Adaptive filter coefficients | коэффициенты адаптивного фильтра |

## Open questions

- Should the optional noise-attenuation papers (`Sebastiano Foti - Guidelines...` and `surface_waves_dispersion_energy_analysis.pdf`) also be ingested? They are relevant but located in `papers/noise_attenuation/`.
- Should the two formal derivations (dispersion and multimodality) be kept as separate files or merged into one `surface_wave_theory_derivation.en.md`?
- For the FK-MUSIC pseudo-spectrum equation, confirm the preferred normalization (the inverse noise-subspace projection shown above, or a normalized form such as $P = 1 / \| \mathbf{E}_n^H \mathbf{e} \|^2$).