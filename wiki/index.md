# Seismic Data Processing Wiki — Index

This wiki is a persistent, compounding knowledge base for the undergraduate seismic data processing course. It sits between the raw paper/PPT library (`papers/`) and the lecture materials (`lecture_notes/`, `slides/`, `figures/`).

## Quick navigation

- [Concepts](#concepts)
- [Techniques](#techniques)
- [Sources](#sources)
- [Comparisons](#comparisons)
- [Lecture-ready pages](#lecture-ready-pages)
- [Log](log.md)

---

## Concepts

| Page | Summary | Status |
|------|---------|--------|
| [Deconvolution](concepts/deconvolution.md) | Inverse filtering to remove wavelet/reverberation effects | draft |
| [Seismic velocities](concepts/seismic_velocities.md) | Interval, average, RMS, NMO and stacking velocity definitions | draft |
| [Normal moveout](concepts/normal_moveout.md) | Offset-dependent reflection traveltime and NMO correction | draft |
| [Velocity analysis](concepts/velocity_analysis.md) | Estimating stacking/NMO velocity from CMP gathers | draft |
| [Static corrections](concepts/static_corrections.md) | Near-surface time shifts and datum corrections | draft |
| [Residual statics](concepts/residual_statics.md) | Surface-consistent residual statics and Gauss–Seidel solution | draft |
| [Floating datum](concepts/floating_datum.md) | Smoothed datum for NMO and velocity analysis | draft |
| [Layer replacement](concepts/layer_replacement.md) | Long-wavelength statics from overburden replacement | draft |
| [Seismic wavelet](concepts/seismic_wavelet.md) | Components of the recorded wavelet: signature, ghosts, bubble | draft |
| [Minimum phase wavelet](concepts/minimum_phase.md) | Causal front-loaded wavelet and the dipole proof | draft |
| [Deterministic deconvolution](concepts/deterministic_deconvolution.md) | Deconvolution with a known or measured wavelet | draft |
| [Statistical deconvolution](concepts/statistical_deconvolution.md) | Estimating the inverse filter from the data itself | draft |
| [Predictive deconvolution](concepts/predictive_deconvolution.md) | Removing repetitive signals by prediction error filtering | draft |
| [Radon transform](concepts/radon_transform.md) | Transform data to ray-parameter domain for filtering, demultiple and interpolation | draft |
| [Surface-consistent deconvolution](concepts/surface_consistent_deconvolution.md) | Separating source/receiver coupling and near-surface effects | draft |
| [Wiener filter](concepts/wiener_filter.md) | Optimal least-squares shaping filter and normal equations | draft |
| [Seismic data processing](concepts/seismic_data_processing.md) | Overview, goals, and typical processing flow | draft |
| [Seismic acquisition](concepts/seismic_acquisition.md) | 2D acquisition essentials, CMP method, parameters | draft |
| [3D seismic acquisition](concepts/3d_seismic_acquisition.md) | 3D geometry, unit cell, fold, and acquisition parameters | draft |
| [First-break picking](concepts/first_break_picking.md) | Identifying first-arrival times for refraction statics and QC | draft |
| [Diving-wave tomography](concepts/diving_wave_tomography.md) | Turning-ray tomography for near-surface velocity models | draft |
| [Effective velocity](concepts/effective_velocity.md) | Stacking/NMO velocity after static corrections and its biases | draft |
| [Migration datum](concepts/migration_datum.md) | Reference surface for migration and replacement velocity | draft |
| [Near-surface velocity model](concepts/near_surface_velocity_model.md) | Shallow velocity model for statics and migration datums | draft |
| [Common midpoint (CMP)](concepts/common_midpoint.md) | CMP/CDP gather, fold, stacking | draft |
| [Seismic data sorts](concepts/seismic_data_sorts.md) | Shot, receiver, CMP, offset gathers and their uses | draft |
| [Cross-spread gather](concepts/cross_spread_gather.md) | 3D gather from one source line and one receiver line | draft |
| [OVT / COV panels](concepts/ovt_cov_panels.md) | Offset-vector tiles for azimuth-preserved 3D processing | draft |
| [Grid binning](concepts/grid_binning.md) | Assigning midpoints to regular CMP bins | draft |
| [Seismic data formats](concepts/seismic_data_formats.md) | SEGY, SEGD, SPS, UKOOA and data loading | draft |
| [Amplitude effects](concepts/amplitude_effects.md) | Physical causes of amplitude attenuation during propagation | draft |
| [Spherical divergence](concepts/spherical_divergence.md) | Geometric spreading correction | draft |
| [Automatic gain control](concepts/automatic_gain_control.md) | AGC and deterministic amplitude equalization | draft |
| [Surface-consistent amplitude correction](concepts/surface_consistent_amplitude.md) | Four-factor surface-consistent amplitude model | draft |
| [Seismic data QC](concepts/seismic_data_qc.md) | Input-data quality control attributes and methods | draft |
| [Seismic processing QC](concepts/seismic_processing_qc.md) | Processing-stage QC for kinematics, noise, deconvolution, demultiple | draft |
| [Seismic well tie](concepts/seismic_well_tie.md) | Synthetic seismograms, wavelet estimation, phase, and correlation | draft |
| [AVO analysis](concepts/avo_analysis.md) | Amplitude versus offset and its use as a QC tool | draft |
| [Spectral analysis](concepts/spectral_analysis.md) | Frequency content of traces and wavelets | draft |
| [Frequency filtering](concepts/frequency_filtering.md) | Shaping seismic spectra by filter operators | draft |
| [Discrete Fourier transform](concepts/discrete_fourier_transform.md) | DFT and its properties for sampled seismic data | draft |
| [Aliasing](concepts/aliasing.md) | Nyquist sampling and alias folding | draft |
| [Surface waves](concepts/surface_waves.md) | Rayleigh and Love waves, ground roll vs. near-surface signal | draft |
| [Surface wave dispersion](concepts/surface_wave_dispersion.md) | Phase velocity, group velocity, and layered-medium dispersion | draft |
| [Surface wave multimodality](concepts/surface_wave_multimodality.md) | Fundamental and higher modes, mode misidentification | draft |
| [Surface wave inversion](concepts/surface_wave_inversion.md) | MASW/SWI from dispersion curve to S-wave profile | draft |
| [FK-MUSIC / array analysis](concepts/fk_music_surface_waves.md) | Beamforming, f–k-MUSIC, and high-resolution dispersion imaging | draft |
| [Adaptive subtraction](concepts/adaptive_subtraction.md) | Model and adaptively subtract surface waves from reflection data | draft |
| [Broadband seismic](concepts/broadband_seismic.md) | Broadband concept, benefits, ghost notches, resolution and bandwidth | draft |
| [Marine deghosting](concepts/marine_deghosting.md) | Ghost physics, notch frequencies, and deghosting methods (bootstrap, PZ, sparse) | draft |
| [Source signature and designature](concepts/source_signature_designature.md) | Airgun signature, bubble oscillation, de-bubble, designature workflow | draft |
| [Model-Based Wavelet Processing](concepts/model_based_wavelet_processing.md) | Deterministic wavelet modeling from physical components (Q, S/N, detector, instrument) | draft |
| [Seismic data regularization](concepts/seismic_data_regularization.md) | Mapping irregular/sparse data to a regular grid for migration and SRME; 3D/4D/5D | draft |
| [Spatial spectral leakage](concepts/spatial_spectral_leakage.md) | Fourier energy crosstalk from irregular sampling and how to control it | draft |
| [Anti-leakage Fourier transform](concepts/anti_leakage_fourier_transform.md) | Iterative matching-pursuit Fourier regularization (ALFT/AA-ALFT/MPFI) | draft |
| [Matching pursuit](concepts/matching_pursuit.md) | Greedy sparse recovery (MP/OMP) with a transform dictionary | draft |
| [Non-uniform Fourier transform](concepts/nonuniform_fourier_transform.md) | Fourier analysis/synthesis on irregular grids; gridding and the NUFFT | draft |
| [Radon interpolation](concepts/radon_interpolation.md) | Sparse high-resolution Radon reconstruction of missing traces | draft |
| [Seismic absorption](concepts/seismic_absorption.md) | Anelastic attenuation, quality factor Q, energy/amplitude definitions, HF loss | draft |
| [Velocity dispersion](concepts/velocity_dispersion.md) | Causality, Kramers–Kronig relations, Futterman and Kjartansson dispersion laws | draft |
| [Models of Q](concepts/q_models.md) | Four attenuation-theory families: frictional, Voigt–Ricker, Kolsky–Futterman NCQ, Kjartansson CQ | draft |
| [Inverse Q filtering](concepts/inverse_q_filtering.md) | Absorption compensation: phase-only vs stabilized amplitude+phase, gain limit, reference frequency | draft |
| [Q estimation](concepts/q_estimation.md) | Spectral ratio, centroid frequency shift, LS spectrum modelling, match-filter | draft |

## Techniques

| Page | Summary | Status |
|------|---------|--------|
| *(none yet)* | | |

## Sources

| Page | Document | Type | Status |
|------|----------|------|--------|
| [Hutchinson & Link (1984)](sources/hutchinson_link_1984_surface_consistency.md) | Surface consistency: A solution to the problem of deconvolving noisy seismic data | paper | reviewed |
| [Verschuur (2006)](sources/verschuur_2006_predictive_deconvolution.md) | EAGE EET 03 — Predictive Deconvolution | course slides | reviewed |
| [CGG ODT04 Part 1](sources/cgg_odt04_deconvolution_part1_wavelet.md) | ODT04 Deconvolution Part 1: The Seismic Wavelet | training slides | reviewed |
| [Hatton, Worthington & Makin (1986)](sources/hatton_worthington_makin_1986_seismic_data_processing.md) | Seismic Data Processing: Theory and Practice | textbook | reviewed |
| [Margrave (2006)](sources/margrave_2006_methods_of_seismic_data_processing.md) | Methods of Seismic Data Processing — lecture notes | lecture notes | reviewed |
| [Yilmaz (2001) Vol. 1](sources/yilmaz_2001_seismic_data_analysis_deconvolution.md) | Seismic Data Analysis — deconvolution chapter | textbook | reviewed |
| [Yilmaz — Practical Seismic Data Analysis, Ch. 1.2–1.3](sources/yilmaz_practical_seismic_data_analysis_amplitude.md) | Practical Seismic Data Analysis — sampling, aliasing, Fourier, amplitude and gain control | textbook | draft |
| [Hill — Introduction to Seismic Processing, Ch. 21](sources/hill_introduction_to_seismic_processing_ch21.md) | Introduction to Seismic Processing — amplitude correction | textbook | draft |
| [Brown (2002) — SCAC](sources/brown_2002_surface_consistent_amplitude_correction.md) | Surface Consistent Amplitude Correction training slides | training slides | draft |
| [Hill & Rüger (2020)](sources/hill_ruger_2020_illustrated_seismic_processing_preimaging.md) | Illustrated Seismic Processing, Vol. 2: Preimaging | textbook | draft |
| [CGG ODT01 Part 1](sources/cgg_odt01_data_analysis_part1.md) | Data Analysis Part 1: recorded wavefield, shot and CMP gathers | training slides | summarized |
| [CGG ODT01 Part 2](sources/cgg_odt01_data_analysis_part2.md) | Data Analysis Part 2: 2D/3D geometry, sorts, aliasing, noise/multiples | training slides | summarized |
| [Noble (2020)](sources/noble_2020_whats_the_datum.md) | What's the Datum? — datums and replacement velocity | conference presentation | reviewed |
| [Jones (2012)](sources/jones_2012_incorporating_near_surface_velocity_anomalies.md) | Near-surface velocity anomalies in pre-stack depth migration | journal article | reviewed |
| [Law and Trad (2017)](sources/law_trad_comparison_of_refraction_inversion_methods.md) | Comparison of refraction inversion methods | paper | draft |
| [Davletkhanov (2017)](sources/davletkhanov_nsm_and_velocity.md) | Near-surface model and velocity | thesis | draft |
| [Sabbione and Velis (2010)](sources/fbpicking.md) | Automatic first-break picking algorithms | paper | draft |
| [Sysoev (2011)](sources/sysoev_statics.md) | Statics and kinematic corrections | course notes | draft |
| [Novokreschin et al. (2021)](sources/velocity_artefacts.md) | Velocity artifacts from near-surface errors | paper | draft |
| [Term 3 Lecture 2 presentation](sources/term03_lecture02_statics_and_kinematics_presentation.md) | Statics and Kinematics (legacy presentation) | presentation | draft |
| [Refraction Seismic notes](sources/refraction_seismic_university_notes.md) | Refraction Seismic Method — delay-time methods | course notes | reviewed |
| [SEG-Y rev 2.0](sources/seg_y_rev2_format.md) | SEG-Y rev 2.0 Data Exchange format | technical standard | draft |
| [SEG SPS rev 2.1](sources/seg_sps_format_rev21.md) | Shell Processing Support format for 3D surveys | technical standard | draft |
| [Vermeer (2012)](sources/vermeer_2012_3d_seismic_survey_design.md) | 3D Seismic Survey Design, 2nd ed. | textbook | draft |
| [White (1997)](sources/white_1997_accuracy_of_well_ties.md) | The accuracy of well ties: practical procedures and examples | paper | draft |
| [Walden & White (1998)](sources/walden_white_1998_seismic_wavelet_estimation.md) | Seismic wavelet estimation: a frequency domain solution to a noisy input-output problem | paper | draft |
| [Carvajal et al. (2023)](sources/carvajal_2023_well_tie_tutorial.md) | Well tie tutorial and its importance in seismic interpretation and inversion | conference paper | draft |
| [Shuey (1985)](sources/shuey_1985_simplification_of_zoeppritz_equations.md) | A simplification of the Zoeppritz equations | paper | draft |
| [Rüger (1996)](sources/ruger_1996_p_wave_reflectivity_offset_azimuth.md) | Variation of P-wave reflectivity with offset and azimuth in anisotropic media | conference abstract | draft |
| [Longbottom et al. (1988)](sources/longbottom_1988_maximum_kurtosis_phase_estimation.md) | Principles and application of maximum kurtosis phase estimation | paper | draft |
| [Li (1999)](sources/li_1999_introduction_to_residual_statics_analysis.md) | Residual statics analysis using prestack equivalent offset migration (Chapters 1–2) | thesis | summarized |
| [Foti et al. (2011)](sources/foti_surface_wave_methods.md) | Application of Surface-Wave Methods for Seismic Site Characterization | paper | draft |
| [Foti et al. (2018)](sources/foti_interpacific_guidelines.md) | Guidelines for the good practice of surface wave analysis: a product of the InterPACIFIC project | paper | draft |
| [Ivanov et al. (2017)](sources/ivanov_hrlrt_masw.md) | Benefits of using the HRLRT with the MASW method | conference abstract | draft |
| [Novotny (1999)](sources/novotny_seismic_surface_waves.md) | Seismic Surface Waves | lecture notes | draft |
| [Igel (2007)](sources/sedi_surface_waves.md) | Surface Waves and Free Oscillations | course notes | draft |
| [Rawlinson (2007)](sources/rawlinson_surface_waves_dispersion.md) | Surface waves and dispersion | lecture notes | draft |
| [Datta (2018)](sources/datta_2018.md) | On the application of the f-k-MUSIC method to multimode surface wave dispersion | paper | draft |
| [Priestley (2024)](sources/priestley_surface_wave_practical.md) | Surface Wave Practical | course notes | draft |
| [Mi et al. (2016)](sources/mi_surface_waves_dispersion_energy.md) | Dispersion energy analysis of Rayleigh and Love waves using finite-difference modeling | paper | draft |
| [NUCNS (2020)](sources/nucns.md) | Non-Uniform Coherent Noise Suppression — SFM technical documentation | technical documentation | draft |
| [NUCNS Best Practice (2018)](sources/nucns_best_practice.md) | NUCNS SFM Best Practice — coherent noise suppression for land data | best practice guide | draft |
| [Cadzow Best Practice (2017)](sources/cadzow_best_practice.md) | Cadzow SFM Best Practice — rank-reduction noise suppression | best practice guide | draft |
| [Kneppers](sources/kneppers_basic_geophysics.md) | Basic Geophysics — noise attenuation training slides | training slides | draft |
| [Bormann & Wielandt (2013)](sources/bormann_wielandt_seismic_signals_noise.md) | Seismic Signals and Noise — NMSOP Ch. 4 | textbook chapter | draft |
| [CGG ODT02 (2016)](sources/cgg_odt02_denoise.md) | ODT02 De-noise — marine noise attenuation course (6 parts) | training slides | draft |
| [Hennenfent & Herrmann (2006)](sources/hennenfent2006_curvelet_intro.md) | Seismic Denoising with Nonuniformly Sampled Curvelets | paper | draft |
| [Hennenfent et al. (2011)](sources/hennenfent2011_interpretative_noise.md) | Interpretative Noise Attenuation in the Curvelet Domain | paper | draft |
| [Herrmann et al. (2007)](sources/herrmann2007_curvelet_multiple_separation.md) | Non-linear Primary-Multiple Separation with Directional Curvelet Frames | paper | draft |
| [Kustowski et al. (2013)](sources/kustowski2013_curvelet_model_guided.md) | Curvelet Noise Attenuation Guided by a Signal or Noise Model | paper | draft |
| [Demanet & Ying (2007)](sources/demanet_ying_mirror_extended.md) | Curvelets and Wave Atoms for Mirror-Extended Images | preprint | draft |
| [Canales (1984)](sources/canales1984_fx_decon.md) | Random Noise Reduction | paper | draft |
| [Gulunay (1986)](sources/gulunay1986_fxdecon.md) | FXDECON — Frequency Domain Complex Prediction | paper | draft |
| [Abma & Claerbout (1995)](sources/abma1995_lateral_prediction.md) | Lateral Prediction for Noise Attenuation by t-x and f-x Techniques | paper | draft |
| [Treitel (1974)](sources/treitel1974_complex_wiener.md) | The Complex Wiener Filter | paper | draft |
| [Денисов & Фиников (2009)](sources/denisov_finikov_2009.md) | Парадоксы f-x деконволюции | conference paper (ru) | draft |
| [Li et al. (2020)](sources/li_et_al_2020_sparse_deghosting.md) | Simultaneous receiver-side deghosting and denoising based on sparsity constraint | paper | draft |
| [Amundsen & Zhou (2013)](sources/amundsen_zhou_2013_deghosting.md) | Low-frequency seismic deghosting | paper | draft |
| [Ghosh (2000)](sources/ghosh_2000_ghost_deconvolution.md) | Deconvolving the ghost effect of the water surface in marine seismics | paper | draft |
| [Lindsey (1960)](sources/lindsey_1960_ghost_elimination.md) | Elimination of seismic ghost reflections by means of a linear filter | paper | draft |
| [Monk (2020)](sources/monk_2020_broadband_seismic.md) | Survey Design and Seismic Acquisition, Chapter 2: Broadband Seismic | textbook chapter | draft |
| [Zhang & Yuan (2019)](sources/zhang_yuan_2019_robust_deconvolution.md) | Robust surface-consistent deconvolution for foothill seismic data | paper | draft |
| [CGG ODT04 Part 2](sources/cgg_odt04_deconvolution_part2_signature.md) | ODT04 Deconvolution Part 2: Signature Deconvolution | training slides | reviewed |
| [CGG ODT04 Part 3](sources/cgg_odt04_deconvolution_part3_demultiple.md) | ODT04 Deconvolution Part 3: Deconvolution as De-multiple | training slides | reviewed |
| [Денисов & Фиников (2010)](sources/denisov_finikov_2010.md) | Особенности алгоритма f-x деконволюции | journal article (ru) | draft |
| [Hart & Hootman (2008)](sources/brown_et_al_mbwp_update_2008.md) | MBWP Update 2008: Achieving Consistent and Stable Phase with Mixed-Source Surveys | technical presentation | reviewed |
| [Hootman & Abitbol (2008)](sources/hootman_abitbol_mbwp_model_equations.md) | MBWP Model Equations — mathematical foundation | technical reference | reviewed |
| [Abitbol & Hootman (2009)](sources/mbwp_step1_initial_operator.md) | MBWP Step 1: Initial Operator Creation | workflow guide | reviewed |
| [Hootman & Abitbol (2009)](sources/mbwp_step2_estimating_parameters.md) | MBWP Step 2: Estimating Q and S/N Parameters | workflow guide | reviewed |
| [Abitbol & Hootman (2009)](sources/mbwp_step3_final_operator.md) | MBWP Step 3: Final Operator Creation and Export | workflow guide | reviewed |
| [Brown (DP3 Module)](sources/brown_dp3_mbwp_module.md) | DP3 MBWP Module — deconvolution training | training module | reviewed |
| [Xu, Zhang & Lambaré (2010)](sources/xu2010_antileakage_fourier_transform.md) | Antileakage Fourier transform for regularization in higher dimensions | paper | draft |
| [Schonewille et al. (2009)](sources/schonewille2009_aa_alft.md) | Anti-alias anti-leakage Fourier transform | paper | draft |
| [Schonewille et al. (2013)](sources/schonewille2013_mpfi_priors.md) | Matching pursuit Fourier interpolation with priors from a second dataset | paper | draft |
| [Trad (2009)](sources/trad2009_5d_interpolation.md) | Five-dimensional interpolation: recovering from acquisition constraints | paper | draft |
| [Trad, Ulrych & Sacchi (2002)](sources/trad2002_radon_interpolation.md) | Accurate interpolation with high-resolution time-variant Radon transforms | paper | draft |
| [Zwartjes & Sacchi (2007)](sources/zwartjes2006_fourier_reconstruction.md) | Fourier reconstruction of nonuniformly sampled, aliased seismic data | paper | draft |
| [Tropp & Gilbert (2007)](sources/tropp2007_omp.md) | Signal recovery from random measurements via orthogonal matching pursuit | paper | draft |
| [Feng et al. (2022)](sources/feng2022_cnn_radon.md) | De-aliased high-resolution Radon transform with CNN sparse priors | paper | draft |
| [Abma & Kabir (2005)](sources/abma2005_interpolation_comparison.md) | Comparisons of interpolation methods | paper | draft |
| [Tang et al. (2017)](sources/tang2017_5d_mpfi_srme.md) | 5D MPFI and its application in SRME for large-offset coil data | paper | draft |
| [Spitz (1991)](sources/spitz1991_fx_interpolation.md) | Seismic trace interpolation in the F-X domain | paper | draft |
| [Naghizadeh & Sacchi (2009)](sources/naghizadeh2009_fx_adaptive.md) | f-x adaptive seismic-trace interpolation | paper | draft |
| [Gülünay (2003)](sources/gulunay2003_ft_interpolation.md) | Seismic trace interpolation in the Fourier transform domain | paper | draft |
| [Futterman (1962)](sources/futterman_1962_dispersive_body_waves.md) | Dispersive body waves — KK relations, causality, logarithmic dispersion | paper | draft |
| [Kjartansson (1979)](sources/kjartansson_1979_constant_q.md) | Constant Q — wave propagation and attenuation; Table 1 theory taxonomy | paper | draft |
| [Wang (2002)](sources/wang_2002_stable_inverse_q.md) | A stable and efficient approach of inverse Q filtering | paper | draft |
| [Wang (2006)](sources/wang_2006_inverse_q_resolution.md) | Inverse Q-filter for seismic resolution enhancement — stabilized, continuous Q | paper | draft |
| [Schönleber (2014)](sources/schonleber_2014_kk_system_theory.md) | Simple KK derivation from system theory (causality → Hilbert pair) | paper | draft |
| [Cheng & Margrave (2012, 2013)](sources/cheng_margrave_2012_2013_q_estimation.md) | Comparison of Q-estimation methods (spectral ratio, centroid shift, match-filter) | CREWES reports | draft |
| [Paradigm QAPP/QEST](sources/paradigm_qapp_qest.md) | Q compensation and estimation reference guide (production parameters) | software doc | draft |

## Comparisons

| Page | Summary | Status |
|------|---------|--------|
| [Deconvolution methods](comparisons/deconvolution_methods.md) | Side-by-side comparison of deconvolution techniques | draft |

## Lecture-ready pages

| Page | Lecture | Status |
|------|---------|--------|
| [Term 1 Lecture 1 — Introduction to seismic data processing](lecture_ready/term01_lec01_introduction_to_seismic_processing.md) | term01_lec01 | lecture-ready |
| [Term 1 Lecture 2 — Amplitude Corrections and Quality Control of Input Data](lecture_ready/term01_lec02_amplitude_correction_and_qc.md) | term01_lec02 | lecture-ready |
| [Term 1 Lecture 3 — Kinematics, Velocities and Field Statics](lecture_ready/term01_lec03_kinematics_and_field_statics.md) | term01_lec03 | lecture-ready |
| [Term 1 Lecture 4 — Advanced Statics and the Link to Velocity Analysis](lecture_ready/term01_lec04_advanced_statics_and_velocity_link.md) | term01_lec04 | lecture-ready |
| [Term 1 Lecture 6 — Single-channel deconvolution](lecture_ready/term01_lec06_single_channel_deconvolution.md) | term01_lec06 | lecture-ready |
| [Term 1 Lecture 7 — Surface-consistent deconvolution](lecture_ready/term01_lec07_surface_consistent_deconvolution.md) | term01_lec07 | lecture-ready |
| [Term 3 Lecture 1 — Quality Control of Seismic Processing and Introduction to 3D Seismic Data](lecture_ready/term03_lec01_processing_qc_and_3d_introduction.md) | term03_lec01 | draft |
| [Term 3 Lecture 2 — Statics and Velocity Modeling](lecture_ready/term03_lec02_statics_and_velocity_modeling.md) | term03_lec02 | draft |
| [Term 3 Lecture 3 — Surface Waves](lecture_ready/term03_lec03_surface_waves.md) | term03_lec03 | draft |
| [Term 3 Lecture 5 — Broadband Deconvolution](lecture_ready/term03_lec05_broadband_deconvolution.md) | term03_lec05 | draft |

---

## Maintenance notes

- Status values: `stub`, `draft`, `reviewed`, `lecture-ready`.
- Source summary pages should link to every concept they inform.
- Concept pages should list sources in their frontmatter.
- Update this index whenever a new page is added or a status changes.
