# Wiki Log

Chronological record of ingests, queries, and lint passes.

## [2026-07-13] figures | Term 3 Lecture 1 — figure-list cleanup

- Generated `figures/term03_lec01/term03_lec01_input_vs_processing_qc.png` with a Russian graphviz flowchart.
- Reused existing raw images:
  - `slides/raw/field_layout_3d.png` as `figures/term03_lec01/term03_lec01_3d_geometry_elements.png`.
  - `slides/raw/unit_cell.png` as `figures/term03_lec01/term03_lec01_unit_cell.png`.
  - `slides/raw/cross-spread.png` as `figures/term03_lec01/term03_lec01_cross_spread_gather.png`.
  - `slides/raw/ovt_construction.png` as `figures/term03_lec01/term03_lec01_ovt_panel.png`.
  - `slides/raw/binning.png` as `figures/term03_lec01/term03_lec01_binning_midpoint_distribution.png`.
- Removed the following planned figures from the lecture notes and slide outline; the instructor will show real-data examples in class instead:
  - `term03_lec01_attribute_maps.png`
  - `term03_lec01_residual_nmo_qc.png`
  - `term03_lec01_noise_attenuation_difference.png`
  - `term03_lec01_wavelet_stability_map.png`
  - `term03_lec01_seismic_well_tie.png`
  - `term03_lec01_avo_qc.png`
  - `term03_lec01_3d_fold_map.png`
  - `term03_lec01_ovt_offset_distribution.png`
  - `term03_lec01_iso_workflow.png`
- Renumbered the remaining Term 3 Lecture 1 figures in the lecture notes (Figure 1–Figure 6).
- Translated lecture notes to Russian: `lecture_notes/ru/term03_lec01_processing_qc_and_3d_introduction.ru.md`.
- Updated the generated-figures table on `wiki/lecture_ready/term03_lec01_processing_qc_and_3d_introduction.md`.
- Built starter slide deck: `slides/term03/lec01_processing_qc_and_3d_introduction/lec01_processing_qc_and_3d_introduction.pptx`.
- Fixed slide outline formatting: added `---` separators so `build_slides.py` parses the outline correctly. Rebuilt deck with content and embedded figures.

## [2026-07-12] concept | Term 3 Lecture 1 — QC and 3D introduction

Started work on Term 3 Lecture 1 (quality control of seismic processing and introduction to 3D seismic data):

- Created slide outline: `slides/term03/lec01_processing_qc_and_3d_introduction/slide_outline.md`.
- Drafted English lecture notes: `lecture_notes/en/term03_lec01_processing_qc_and_3d_introduction.en.md`.
- Created wiki concept pages:
  - `wiki/concepts/seismic_processing_qc.md` — processing-stage QC.
  - `wiki/concepts/seismic_well_tie.md` — synthetic seismograms and wavelet estimation.
  - `wiki/concepts/avo_analysis.md` — AVO/AVAz as a QC tool.
  - `wiki/concepts/3d_seismic_acquisition.md` — 3D geometry basics, unit cell, fold.
  - `wiki/concepts/cross_spread_gather.md` — cross-spread gathers.
  - `wiki/concepts/ovt_cov_panels.md` — OVT/COV panels.
  - `wiki/concepts/grid_binning.md` — CMP grid binning.
- Created lecture-ready page: `wiki/lecture_ready/term03_lec01_processing_qc_and_3d_introduction.md`.
- Updated `wiki/index.md` with new pages and lecture-ready entry.

## [2026-07-12] ingest | Vermeer ch.2 and AVO/well-tie references

Expanded wiki with sourced details:

- Extracted Vermeer (2012), Chapter 2 (pages 42–72) to `/tmp/opencode/vermeer_ch2/chapter2.txt`.
- Updated `wiki/sources/vermeer_2012_3d_seismic_survey_design.md` to reference new 3D concept pages and Term 3 Lecture 1.
- Expanded `wiki/concepts/3d_seismic_acquisition.md` with geometry classes (areal, parallel, orthogonal, slanted, zigzag), 3D subsets, minimal data sets, unit cell, fold formulas, aspect ratios, spatial continuity, and symmetric sampling.
- Expanded `wiki/concepts/cross_spread_gather.md` with properties, extraction from orthogonal geometry, comparison with template, and limitations.
- Expanded `wiki/concepts/ovt_cov_panels.md` with pseudo-COV construction, OVT parameters, reciprocal OVTs, and coverage/fold notes.
- Expanded `wiki/concepts/grid_binning.md` with natural bin size, offset distribution in the unit cell, and midpoint smear discussion.
- Expanded `wiki/concepts/seismic_processing_qc.md` with multi-attribute assessment and detailed QC workflows.
- Expanded `wiki/concepts/seismic_well_tie.md` with time-depth conversion, Roy-White method, and common pitfalls.
- Expanded `wiki/concepts/avo_analysis.md` with AVO classes, intercept-gradient crossplots, Ruger equation, and AVO QC workflow.
- Created source pages for cited papers not in the local library:
  - `wiki/sources/white_1998_properties_of_the_statistical_wavelet.md`
  - `wiki/sources/shuey_1985_simplification_of_zoeppritz_equations.md`
  - `wiki/sources/ruger_1997_azimuthal_avo_analysis.md`
- Updated `wiki/index.md` with new source pages.
- Ran `uv run python scripts/lint_wiki.py`; no issues found.

## [2026-07-12] refine | Slide outline aligned with refined lecture notes

Updated `slides/term03/lec01_processing_qc_and_3d_introduction/slide_outline.md` to match the refined lecture notes:

- **Slide 13 (Seismic well tie):** added time-depth conversion, Roy-White frequency-domain method, PEP vs NMSE accuracy metrics, White (1997) phase-error tolerances, and the need to repeat ties after conditioning.
- **Slide 14 (AVO analysis):** added the two-term Shuey approximation, intercept-gradient crossplot, and the Rüger (1996) HTI/orthorhombic azimuthal AVO equation.
- **Slide 16 (3D acquisition):** added 3D symmetric sampling and minimal data sets.
- **Slide 20 (Fold):** added inline/crossline fold formulas and the Vermeer midpoint-area / unit-cell-area interpretation.
- **Slide 22 (OVT/COV):** added unit-cell-sized tiles and pseudo-COV gathers.
- **Slide 23 (OVT construction):** added reciprocal OVTs and their role in reducing edge effects.
- **Slide 26 (Comprehension questions):** added questions on PEP/NMSE, AVO mismatch, and reciprocal OVTs / symmetric sampling.

## [2026-07-12] refine | Term 3 Lecture 1 English notes refined with ingested sources

Refined `lecture_notes/en/term03_lec01_processing_qc_and_3d_introduction.en.md` using the papers extracted from `papers/qc/` and Vermeer Chapter 2:

- **Seismic well tie (§1.10):**
  - Added time-depth conversion equation and the role of checkshots.
  - Added the Roy-White frequency-domain wavelet estimation method (Walden & White, 1998) as a noisy input-output problem with multiple coherence analysis.
  - Added White (1997) phase-error tolerances for different applications (correlation, AVO, zero-phasing, absolute-impedance inversion).
  - Added the distinction between goodness-of-fit (PEP) and true accuracy (NMSE), and the rule of keeping analysis bandwidth well below data bandwidth.
  - Noted that the best match location for time-migrated data is often up-dip from the well.
  - Added Carvajal et al. (2023) note that well ties should be repeated after seismic conditioning.

- **AVO QC (§1.11):**
  - Added the two-term Shuey approximation and the intercept-gradient crossplot.
  - Added the Rüger (1996) HTI azimuthal AVO equation and noted the orthorhombic extension.
  - Clarified that AVAz inversion targets symmetry-plane directions and fracture parameters.

- **3D acquisition (§2.1–2.7):**
  - Added the concept of 3D symmetric sampling and minimal data sets.
  - Expanded the fold section with inline/crossline fold formulas and the Vermeer midpoint-area / unit-cell-area interpretation.
  - Expanded the OVT section to describe pseudo-COV gathers, unit-cell-sized tiles, and reciprocal OVTs for spatial continuity.

- **Suggested reading:** updated to use the correct local source citations.

Ran `uv run python scripts/lint_wiki.py`; no issues found.

## [2026-07-12] ingest | Corrected AVO/well-tie sources and ingested actual papers from `papers/qc/`

The previous White (1998) and Rüger (1997) source pages were hallucinated; they have been removed. The actual papers supplied by the instructor in `papers/qc/` have been ingested:

- `papers/qc/10.1190@1.1826488.pdf` — Rüger (1996), SEG Expanded Abstracts, "Variation of P-wave reflectivity with offset and azimuth in anisotropic media."
- `papers/qc/white1997.pdf` — White (1997), "The accuracy of well ties: practical procedures and examples."
- `papers/qc/walden1998.pdf` — Walden & White (1998), IEEE TGRS, "Seismic wavelet estimation: a frequency domain solution to a geophysical noisy input-output problem."
- `papers/qc/shuey1985.pdf` — Shuey (1985), *Geophysics*.
- `papers/qc/93120-well-tie-tutorial-and-its-importan.pdf` — Carvajal et al. (2023), GeoConvention, "Well tie tutorial..."
- `papers/qc/longbottom1988.pdf` — Longbottom et al. (1988), *Geophysical Prospecting*, "Principles and application of maximum kurtosis phase estimation."

Actions taken:

- Removed `wiki/sources/white_1998_properties_of_the_statistical_wavelet.md` and `wiki/sources/ruger_1997_azimuthal_avo_analysis.md`.
- Created accurate source pages:
  - `wiki/sources/ruger_1996_p_wave_reflectivity_offset_azimuth.md`
  - `wiki/sources/white_1997_accuracy_of_well_ties.md`
  - `wiki/sources/walden_white_1998_seismic_wavelet_estimation.md`
  - `wiki/sources/carvajal_2023_well_tie_tutorial.md`
  - `wiki/sources/longbottom_1988_maximum_kurtosis_phase_estimation.md`
- Updated `wiki/sources/shuey_1985_simplification_of_zoeppritz_equations.md` to point to the actual PDF and removed the "not in library" note.
- Updated frontmatter sources and in-text references in `wiki/concepts/seismic_well_tie.md` and `wiki/concepts/avo_analysis.md`.
- Updated frontmatter sources and suggested reading in `wiki/lecture_ready/term03_lec01_processing_qc_and_3d_introduction.md`.
- Updated frontmatter sources and suggested reading in `lecture_notes/en/term03_lec01_processing_qc_and_3d_introduction.en.md`.
- Updated `wiki/index.md` with the corrected source entries.
- Ran `uv run python scripts/lint_wiki.py`; no issues found.

## [2026-07-11] lecture-ready | Term 1 Lectures 6 and 7

Updated `wiki/lecture_ready/term01_lec06_single_channel_deconvolution.md` and `wiki/lecture_ready/term01_lec07_surface_consistent_deconvolution.md` from `draft` to `lecture-ready`:

- Changed frontmatter status to `lecture-ready` and removed redundant `lecture-ready` tag.
- Added one-line summary, key concepts covered, generated-figures table, lecture-materials list, related concept pages, and instructor notes to match the lecture-ready format.
- Fixed the Lecture 6 dipole Z-transform to match the lecture notes ($W(z) = a + bz^{-1}$, minimum phase when the zero is inside the unit circle).
- Aligned the Lecture 7 surface-consistent equations with the notation used in the lecture notes and glossary.
- Referenced all generated artifacts: English and Russian notes, rendered PDFs, derivations, exercises, slide outlines, starter PowerPoint decks, and figure scripts.
- Added a note that the Lecture 6 slide outline still contains the old dipole formula and should be aligned before presentation.

Updated `wiki/index.md` to reflect the new status.

Ran `uv run python scripts/lint_wiki.py`; no issues found.

## [2026-06-22] init | Wiki structure and deconvolution pilot

- Created `wiki/` structure: `concepts/`, `techniques/`, `sources/`, `comparisons/`, `lecture_ready/`.
- Added `index.md` and this `log.md`.
- Installed local Python environment with `uv` and packages `python-pptx`, `pymupdf`.
- Created `scripts/extract_source_text.py` for local PDF/PPT text extraction.

## [2026-06-22] ingest | Deconvolution sources

Extracted and summarized deconvolution sources:

- Hutchinson & Link (1984) — surface-consistent deconvolution.
- Verschuur (2006) EAGE EET 03 — predictive deconvolution.
- CGG ODT04 Part 1 — the seismic wavelet.

Created initial concept pages:

- `concepts/deconvolution.md`
- `concepts/seismic_wavelet.md`
- `concepts/predictive_deconvolution.md`
- `concepts/surface_consistent_deconvolution.md`
- `concepts/wiener_filter.md`

## [2026-06-24] ingest | Hatton, Margrave, Yilmaz deconvolution sources

- Installed `djvulibre` and extracted text from the Russian DJVU edition of Hatton, Worthington & Makin (1986).
- Extracted pages 125–205 from Margrave (2006) *Methods of Seismic Data Processing*.
- Extracted pages 145–215 from Yilmaz (2001) *Seismic Data Analysis* Vol. 1.
- Created/updated source pages:
  - `wiki/sources/hatton_worthington_makin_1986_seismic_data_processing.md`
  - `wiki/sources/margrave_2006_methods_of_seismic_data_processing.md`
  - `wiki/sources/yilmaz_2001_seismic_data_analysis_deconvolution.md`

## [2026-06-24] concept | Phase and deconvolution concept pages

- Added `wiki/concepts/minimum_phase.md` with the dipole-based front-loading proof from Hatton.
- Added `wiki/concepts/deterministic_deconvolution.md`.
- Added `wiki/concepts/statistical_deconvolution.md`.
- Updated existing concept pages (`deconvolution.md`, `wiener_filter.md`, `predictive_deconvolution.md`, `surface_consistent_deconvolution.md`) with new sources and cross-links.

## [2026-06-24] lecture-ready | Two-session deconvolution outline

- Confirmed lecture numbering with instructor: split into `term01_lec06` (single-channel) and `term01_lec07` (surface-consistent + practical).
- Drafted outline at `lecture_notes/_drafts/term01_deconvolution_two_session_outline.md`.
- Created lecture-ready pages:
  - `wiki/lecture_ready/term01_lec06_single_channel_deconvolution.md`
  - `wiki/lecture_ready/term01_lec07_surface_consistent_deconvolution.md`
- Updated `wiki/index.md`.

## [2026-06-24] review | Fixes to Lecture 6 notes and figures

- Removed duplicate figure captions in `lecture_notes/en/term01_lec06_single_channel_deconvolution.en.md` and `lecture_notes/en/term01_lec07_surface_consistent_deconvolution.en.md` by emptying image alt text (Pandoc was auto-generating captions from alt text).
- Rewrote `scripts/figures/term01_lec06/plot_deterministic_decon.py` to use a true minimum-phase wavelet from spectral factorization; the convolution output now shows a clear compressed spike.
- Updated the instrument-response example in Lecture 6 to describe a known geophone + recording-system response and its deterministic inverse operator.
- Updated `scripts/figures/term01_lec06/plot_spiking_decon.py` to include input and output amplitude spectra; switched to a true minimum-phase wavelet.
- Updated `scripts/figures/term01_lec06/plot_predictive_decon.py` to include the input reflectivity series as the top panel and to use a true minimum-phase wavelet.
- Regenerated all affected PNGs and re-rendered the Lecture 6 PDF.

## [2026-06-24] lecture | English notes, figures, and slide outlines for term01_lec06 and term01_lec07

- Wrote English lecture notes:
  - `lecture_notes/en/term01_lec06_single_channel_deconvolution.en.md`
  - `lecture_notes/en/term01_lec07_surface_consistent_deconvolution.en.md`
- Rendered both to PDF successfully.
- Generated figures:
  - `figures/term01_lec06/` — convolutional model, dipoles, phase wavelets, deterministic decon, prewhitening, spiking, predictive.
  - `figures/term01_lec07/` — surface-consistent model, synthetic example, parameter scan, deterministic demo, Wiener matrix demo.
- Added self-contained Python scripts:
  - `scripts/figures/term01_lec06/`
  - `scripts/figures/term01_lec07/` (includes practical demos)
- Created exercises:
  - `exercises/term01_lec06_single_channel_deconvolution.md`
  - `exercises/term01_lec07_surface_consistent_deconvolution.md`
- Created slide outlines:
  - `slides/term01/lec06_single_channel_deconvolution/slide_outline.md`
  - `slides/term01/lec07_surface_consistent_deconvolution/slide_outline.md`
- Added `scipy` to `pyproject.toml` for minimum-phase spectral factorization and matrix demos.
- Updated notation glossary in `AGENTS.md`.

## [2026-06-24] fix | Predictive deconvolution figure — simplified wavelet, proper alignment

- Replaced the spectral-factorization minimum-phase wavelet with a clean causal
  one-sided `exp(-αt)·cos(2πf₀t)` wavelet (peak at t=0, no rolling artifacts).
- Simplified reverberation model to a single delayed scaled copy.
- Reduced spiking operator length (n_op=12) so reverberations remain visible.
- Reduced gapped operator length (n_op=20) to avoid cross-correlation between
  the first reverberation and the second primary.
- Applied filters with `np.convolve(mode="full")[:n]` for correct time alignment.
- Verified numerically: spiking preserves reverb at 91%; gapped suppresses
  reverb to 8–12% while preserving primary wavelets at >99.7%.

## [2026-06-24] fix | Spiking deconvolution figure — causal wavelet, full-conv alignment

- Replaced `design_minimum_phase_wavelet` with the same causal `exp(-αt)·cos()`
  wavelet used in the predictive-decon figure.
- Changed `np.convolve(mode="same")` → `mode="full")[:n]` for exact alignment
  (0-sample error at all 6 spike locations).
- Set operator length to match wavelet length (n_op=32).
- Recovered wavelet: peak at sample 0, 98.3% energy in first 5 samples,
  sidelobes at 5.5% of peak.

## [2026-06-24] docs | Expanded Wiener filter derivation

- Rewrote `lecture_notes/derivations/wiener_deconvolution_derivation.en.md`.
- Added full worked numerical example (3×3 matrix, 5-sample trace).
- Added prewhitening intuition (eigenvalue shift, condition number).
- Added filter-length trade-off discussion (short vs long filter table).
- Added §13 mapping derivation steps to the Python implementation.
- Added figure reference to `demo_wiener_matrix.py`.

## [2026-06-24] docs | PEF Z-transform derivation

- Wrote `lecture_notes/derivations/pef_ztransform_derivation.en.md`.
- Shows how the PEF arises from predictive deconvolution:
  `F(z) = 1 - z^{-α} H(z)`.
- Single-multiple example: `F(z) = 1 + cz^{-α}` cancels `1/(1+cz^{-α})`.
- Expanded §4.2: explicit link from α=1 PEF to spiking deconvolution,
  including the innovation-filter argument and a dipole worked example.
- Summary table mapping Z-domain forms to time-domain effects.

## [2026-06-24] fix | Zero-location error in dipole section

- Switched from non-standard `W(z) = a + bz` (positive powers) to standard
  signal-processing convention `W(z) = a + b z^{-1}`.
- Fixed: minimum-phase zeros are INSIDE the unit circle (was: outside).
- Fixed: causal inverse expands in negative powers z^{-k} (was: positive).
- Fixed the non-causal inverse expansion accordingly.
- Updated equation labels and added explicit mixed-phase converse.

## [2026-06-24] translate | Russian versions of all 4 documents

- `lecture_notes/ru/term01_lec06_single_channel_deconvolution.ru.md`
- `lecture_notes/ru/term01_lec07_surface_consistent_deconvolution.ru.md`
- `lecture_notes/derivations/wiener_deconvolution_derivation.ru.md`
- `lecture_notes/derivations/pef_ztransform_derivation.ru.md`
- All 4 rendered to PDF successfully.
- Code comments kept in English (XeLaTeX monospace font lacks Cyrillic).

## [2026-06-27] ingest | Term 1 Lecture 1 — introduction sources

Extracted raw text to `wiki/sources/_raw_text/`:

- `ODT01A_DATA_ANALYSIS_PART1_v8.2.txt`
- `ODT01A_DATA_ANALYSIS_PART2_v8.3.txt`
- `Methods of Seismic Data Processing.txt` (pages 1–40, Chapter 1)
- `Geometry Land.txt` (minimal content — 6 kB single slide)
- `SEG-Yrev2Release.txt`
- `SEG SPS Format rev 2.1.txt`
- `Steve J Hill - Introduction to Seismic Processing.txt`

Created source summaries:

- `wiki/sources/hill_ruger_2020_illustrated_seismic_processing_preimaging.md`
- `wiki/sources/cgg_odt01_data_analysis_part1.md`
- `wiki/sources/cgg_odt01_data_analysis_part2.md`
- `wiki/sources/seg_y_rev2_format.md`
- `wiki/sources/seg_sps_format_rev21.md`
- `wiki/sources/vermeer_2012_3d_seismic_survey_design.md`

Updated source summary:

- `wiki/sources/margrave_2006_methods_of_seismic_data_processing.md` (added Chapter 1 big-picture relevance)

Created concept pages:

- `wiki/concepts/seismic_data_processing.md`
- `wiki/concepts/seismic_acquisition.md`
- `wiki/concepts/common_midpoint.md`
- `wiki/concepts/seismic_data_sorts.md`
- `wiki/concepts/seismic_data_formats.md`

Updated `wiki/index.md` with new pages. Ready to draft lecture outline for `term01_lec01`.

## [2026-06-27] lecture | Term 1 Lecture 1 — English notes, Russian translation, figures, outline, exercises

- Finalized outline: `lecture_notes/_drafts/term01_lec01_introduction_to_seismic_processing_outline.md`.
- Dispatched worker subagents to create 9 self-contained Python figure scripts in `scripts/figures/term01_lec01/`:
  - `plot_exploration_workflow.py`
  - `plot_idealized_vs_recorded_trace.py`
  - `plot_distortions_overview.py`
  - `plot_kinematic_vs_dynamic.py`
  - `plot_processing_flow.py` (rewritten for clean layout)
  - `plot_2d_acquisition_geometry.py`
  - `plot_cmp_gather_stack.py`
  - `plot_data_sorts.py`
  - `plot_segy_structure.py` (contrast fixed)
- Generated PNGs in `figures/term01_lec01/`.
- Wrote English lecture notes: `lecture_notes/en/term01_lec01_introduction_to_seismic_processing.en.md`.
- Rendered English PDF successfully.
- Dispatched worker subagent to translate notes to Russian: `lecture_notes/ru/term01_lec01_introduction_to_seismic_processing.ru.md`.
- Rendered Russian PDF successfully.
- Created slide outline: `slides/term01/lec01_introduction_to_seismic_processing/slide_outline.md`.
- Created exercises: `exercises/term01_lec01_introduction_to_seismic_processing.md`.
- Updated lecture-ready page status to `lecture-ready` and refreshed `wiki/index.md`.

## [2026-06-29] lecture | Term 1 Lecture 03 — Kinematics, Velocities and Field Statics

- Confirmed split of original kinematics/statics lecture into Lecture 03 (velocities, NMO, field statics, refraction) and Lecture 04 (layer replacement, residual statics, floating datum).
- Extracted text from existing materials: `slides/raw/term01_lecture02_kinematics.pptx` and `slides/raw/plan_term01_lecture02_kinematics.docx`.
- Drafted outline: `lecture_notes/_drafts/term01_lec03_kinematics_and_field_statics_outline.md`.
- Generated 7 self-contained Python figure scripts in `scripts/figures/term01_lec03/` and PNGs in `figures/term01_lec03/`.
- Wrote English lecture notes: `lecture_notes/en/term01_lec03_kinematics_and_field_statics.en.md`.
- Rendered PDF successfully.
- Created exercises: `exercises/term01_lec03_kinematics_and_field_statics.md`.
- Created slide outline and starter PowerPoint deck in `slides/term01/lec02_kinematics_and_field_statics/`.
- Updated `wiki/index.md` and `AGENTS.md` notation glossary.
- Wiki lint passes with only stub warnings.

## [2026-06-29] wiki | Populated sources and concepts for Lectures 02 and 03

- Extracted and summarized:
  - `papers/statics/What's the Datum.pdf` → `wiki/sources/noble_2020_whats_the_datum.md`
  - `papers/statics/Jones - Near Surface.pdf` → `wiki/sources/jones_2012_incorporating_near_surface_velocity_anomalies.md`
  - `papers/statics/Refraction_Seismic.pdf` → `wiki/sources/refraction_seismic_university_notes.md`
- Updated `wiki/sources/hatton_worthington_makin_1986_seismic_data_processing.md` with Section 5.10 (residual statics, Gauss–Seidel) and Section 3.7.1 (datum/floating datum).
- Updated `wiki/sources/cgg_odt01_data_analysis_part1.md` to link to `normal_moveout`.
- Created/upgraded concept pages:
  - `wiki/concepts/normal_moveout.md` — draft
  - `wiki/concepts/velocity_analysis.md` — draft
  - `wiki/concepts/seismic_velocities.md` — draft
  - `wiki/concepts/static_corrections.md` — draft
  - `wiki/concepts/residual_statics.md` — draft
  - `wiki/concepts/floating_datum.md` — draft
  - `wiki/concepts/layer_replacement.md` — draft
- Wiki lint now passes cleanly.

## [2026-06-29] lecture | Term 1 Lecture 04 — Advanced Statics and the Link to Velocity Analysis

- Drafted outline: `lecture_notes/_drafts/term01_lec04_advanced_statics_and_velocity_link_outline.md`.
- Wrote English lecture notes: `lecture_notes/en/term01_lec04_advanced_statics_and_velocity_link.en.md`.
- Rendered PDF successfully.
- Dispatched a worker subagent to create 6 self-contained Python figure scripts in `scripts/figures/term01_lec04/` and PNGs in `figures/term01_lec04/`.
- Regenerated the statics-velocity-bias figure after identifying that it did not show a velocity bias; corrected the script so the semblance peak and $t^2$ vs $x^2$ slope both shift.
- Created exercises: `exercises/term01_lec04_advanced_statics_and_velocity_link.md`.
- Created slide outline and starter PowerPoint deck in `slides/term01/lec03_advanced_statics_and_velocity_link/`.
- Created lecture-ready page: `wiki/lecture_ready/term01_lec04_advanced_statics_and_velocity_link.md`.
- Updated `wiki/index.md` and linked `wiki/concepts/static_corrections.md` to the new lecture-ready page.
- Wiki lint passes cleanly.

## [2026-06-29] todo | Remaining work

- Add FX-deconvolution, robust deconvolution, and MBWP source summaries.
- Build comparison page: predictive vs. surface-consistent deconvolution.
- Review English notes for term01_lec06/lec07 with instructor and adjust content/timing as needed.
- Optionally build final PowerPoint slides for term01_lec06/lec07 from outlines.
- Translate exercises and slide outlines for term01_lec06/lec07 to Russian.
- Optionally assemble the PowerPoint deck for term01_lec01 from the slide outline.
- Translate Lecture 03 and Lecture 04 notes, exercises, and slide outlines to Russian once English versions are approved.
- Renumber remaining Term 1 lectures after the split is finalized.

## [2026-06-27] todo | Remaining work

- Add FX-deconvolution, robust deconvolution, and MBWP source summaries.
- Build comparison page: predictive vs. surface-consistent deconvolution.
- Review English notes for term01_lec06/lec07 with instructor and adjust content/timing as needed.
- Optionally build final PowerPoint slides for term01_lec06/lec07 from outlines.
- Translate exercises and slide outlines for term01_lec06/lec07 to Russian.
- Optionally assemble the PowerPoint deck for term01_lec01 from the slide outline.
- Draft Lecture 04 (advanced statics, layer replacement, floating datum) after Lecture 03 is approved.
- Renumber remaining Term 1 lectures after the split is finalized.

## [2026-07-01] ingest | OCR extraction of Margrave Chapters 5–7 for Lectures 2 and 3

- Used the new Unlimited-OCR pipeline (`scripts/extract_source_text_ocr.py`) to extract pages 206–298 of Margrave (2006) *Methods of Seismic Data Processing*.
- Covered:
  - Chapter 5: Surface-consistent methods, statics and datums, residual statics, refraction statics.
  - Chapter 6: Velocity definitions (instantaneous, average, RMS, interval), Dix formula, Snell's law, ray parameter, raytracing in v(z).
  - Chapter 7: Normal moveout, stacking velocity, dipping-reflector NMO, NMO in v(z) medium, CMP stacking, ZOS model, Fresnel zones.
- Saved raw OCR text to `wiki/sources/_raw_text/Methods of Seismic Data Processing.txt`.
- Updated `wiki/sources/margrave_2006_methods_of_seismic_data_processing.md` with the new chapters and added concepts to the frontmatter.
- Updated concept pages:
  - `concepts/static_corrections.md`
  - `concepts/residual_statics.md`
  - `concepts/floating_datum.md`
  - `concepts/layer_replacement.md`
  - `concepts/seismic_velocities.md`
  - `concepts/normal_moveout.md`
  - `concepts/velocity_analysis.md`
- Updated lecture-ready pages:
  - `lecture_ready/term01_lec03_kinematics_and_field_statics.md`
  - `lecture_ready/term01_lec04_advanced_statics_and_velocity_link.md`
- Ran `uv run python scripts/lint_wiki.py`; no issues found.

## [2026-07-04] docs | Gauss–Seidel derivation for residual statics

Created a new step-by-step derivation document:
- `lecture_notes/derivations/gauss_seidel_residual_statics_derivation.en.md`
- Rendered PDF: `lecture_notes/derivations/gauss_seidel_residual_statics_derivation.en.pdf`

Content:
- 4-component model and construction of the sparse design matrix.
- Least-squares objective and why direct inversion of $G^\top G$ is impractical.
- Gauss–Seidel update formulas for source, receiver, offset-class, and CMP components.
- The specific sweep order requested: initialise source/receiver statics to zero, estimate CMP terms as averages of measured shifts, update source and receiver statics, then feed the updated values back into the CMP estimate at the start of the next sweep.
- Worked numerical example with 2 sources, 2 receivers, 1 offset class, and 2 CMPs (4 traces).
- Discussion of the under-constrained nature and the zero-mean constraint.

Linked the derivation from `lecture_notes/en/term01_lec04_advanced_statics_and_velocity_link.en.md` §3.3 and listed it in `wiki/lecture_ready/term01_lec04_advanced_statics_and_velocity_link.md`.

Ran `uv run python scripts/lint_wiki.py`; no issues found.

## [2026-07-04] lecture | Lecture 4 notes — three-step workflow, NMO-stretch windowing, and expanded exercises

Further polished `lecture_notes/en/term01_lec04_advanced_statics_and_velocity_link.en.md`:

- Added an explicit **three-step workflow** at the start of §2: form reference traces → estimate time shifts by cross-correlation → decompose into surface-consistent source and receiver statics.
- Noted in §2.2 that reference traces can be internal (selected from the same data set) or external (e.g., stacked or filtered data).
- Added the **NMO-stretch** point to the correlation-window QC: after NMO correction, shallow parts of traces are stretched and distorted, so they are a poor choice for the correlation window.

Re-rendered the English PDF successfully.

Expanded `exercises/term01_lec04_advanced_statics_and_velocity_link.md`:
- Added concept-check question on correlation domains.
- Added concept-check question on the overdetermined/under-constrained nature of the surface-consistent system.
- Added detailed answers for both new questions.

Updated `wiki/lecture_ready/term01_lec04_advanced_statics_and_velocity_link.md` instructor notes to mention the NMO-stretch windowing consideration.

Ran `uv run python scripts/lint_wiki.py`; no issues found.

## [2026-07-04] lecture | Lecture 4 notes — correlation domains and over/under-constrained system

Updated `lecture_notes/en/term01_lec04_advanced_statics_and_velocity_link.en.md` with insights from Li (1999), Chapters 1–2:

- Added §2.2.1 **Correlation domains** with a table showing which static and dynamic factors contribute to traveltime differences in common-source, common-receiver, common-offset, and common-midpoint domains. Explains why source/receiver statics can be isolated in some domains while both appear together in CMP/common-offset gathers.
- Added §3.2.1 **Overdetermined and under-constrained** explaining the dual nature of the surface-consistent system: many more traces than unknowns (robust statistics) yet non-unique because a constant can be traded between source and receiver statics without changing the fit. This motivates the zero-mean constraint and the separate handling of long-wavelength statics.

Updated the slide outline (`slides/term01/lec03_advanced_statics_and_velocity_link/slide_outline.md`) with two new slides covering the same points.

Re-rendered the English PDF successfully.

Updated `wiki/lecture_ready/term01_lec04_advanced_statics_and_velocity_link.md` to list the new concepts and add Li (1999) to the source frontmatter.

Ran `uv run python scripts/lint_wiki.py`; no issues found.

## [2026-07-04] ingest | Li (1999) M.Sc. thesis, Chapters 1–2

Extracted text from `papers/statics/Li-MSc-1999.pdf`, pages 16–49 (document pages 1–34), covering Chapters 1 and 2 of Xinxiang Li's M.Sc. thesis *Residual statics analysis using prestack equivalent offset migration*.

Created source summary:
- `wiki/sources/li_1999_introduction_to_residual_statics_analysis.md` (status: reviewed).

Key insights captured:
- Three basic assumptions of statics analysis: frequency/amplitude independent, time-invariant, and surface-consistent.
- Physical justification of surface consistency: low-velocity near surface forces rays toward vertical by Snell's law, making near-surface traveltime depend mainly on source/receiver location.
- Field statics categories (elevation, refraction, uphole) and the distinction between long-wavelength field statics and short-wavelength residual statics.
- Residual statics as relative shifts with zero mean; a bulk shift biases velocity analysis, motivating floating datum.
- Three-step residual statics workflow: form reference traces, estimate time shifts by cross-correlation, decompose into surface-consistent components.
- Internal vs external reference traces; advantages and limitations of NMO correction before statics analysis.
- Cross-correlation basics, normalized correlation, correlation domains (source/receiver/CMP/offset), cycle skipping, and trace windowing considerations.
- Decomposition: initial two-component model, over-determined/under-constrained nature, subsurface-consistent (structure) term, residual NMO term after NMO correction.
- Iterative techniques: Gauss-Seidel, reference-trace updating, velocity updating, and convergence limitations tied to cable length and CDP fold.

Updated concept pages to cite the new source:
- `wiki/concepts/residual_statics.md` — added source to frontmatter and expanded the Gauss–Seidel discussion with the over-determined/under-constrained point.
- `wiki/concepts/static_corrections.md` — added source to frontmatter and noted Li's framing of near-surface traveltime anomalies as the core problem.
- `wiki/concepts/floating_datum.md` — added source to frontmatter and added the relativity-of-residual-statics argument for using a floating datum.
- `wiki/concepts/velocity_analysis.md` — added source to frontmatter and cited Li for the unchanged-curvature velocity-bias explanation.

Updated `wiki/index.md`:
- Added Li (1999) to the Sources table.
- Corrected inconsistent status values for Hutchinson & Link, Verschuur (2006), CGG ODT04 Part 1, and Hill & Rüger (2020) to match their actual frontmatter statuses.

Ran `uv run python scripts/lint_wiki.py`; no issues found.

## [2026-07-04] feedback | Sync Lecture 4 review into wiki

Refined wiki pages following the latest review of `lecture_notes/en/term01_lec04_advanced_statics_and_velocity_link.en.md`:

- `wiki/lecture_ready/term01_lec04_advanced_statics_and_velocity_link.md`
  - Added the new `term01_lec04_velocity_and_statics.png` figure to the figures table.
  - Updated key concepts to stress that long-wavelength statics shift $t_0$ but leave curvature unchanged.
  - Replaced the simplified floating-datum equation with the four-step operational workflow and the residual static equations.
  - Added instructor notes on the new figure, the curvature argument, non-surface-consistent residuals after long-wavelength removal, source/receiver QC, and correlation-window avoidance of first arrivals and multiples.

- `wiki/concepts/floating_datum.md`
  - Clarified that the velocity bias comes from fitting unchanged curvature to a hyperbola with the wrong $t_0$.
  - Replaced the generic `Δt_floating = Δt_total − Δt_smoothed` definition with the four-step workflow: smooth source/receiver fields, interpolate to CMPs, subtract half of the long-wavelength component from each side, apply residual corrections.
  - Added the consequence that residual source/receiver statics are no longer strictly surface-consistent after the long-wavelength component is removed in the CMP domain.

- `wiki/concepts/residual_statics.md`
  - Added the physical justification for surface consistency: sharp near-surface velocity contrast forces vertical rays, so near-surface traveltime depends mainly on source/receiver location.
  - Removed the specific `0.5–1 s` correlation-window recommendation; added the rule that windows must avoid first arrivals (too shallow) and multiples (too deep).
  - Added a "Quality control" subsection: source and receiver statics should have the same sign in nearby locations, except for buried sources.
  - Noted that after long-wavelength removal in the CMP domain, residuals are no longer strictly surface-consistent.

- `wiki/concepts/velocity_analysis.md`
  - Updated the "Bias from statics" section to state that the curvature is unchanged and that the same curvature is fitted to a wrong $t_0$.

- `wiki/concepts/static_corrections.md`
  - Connected the vertical-ray approximation to the sharp weathering-layer velocity contrast.
  - Added the source/receiver consistency QC point (with the buried-source exception).

Ran `uv run python scripts/lint_wiki.py`; no issues found.

## [2026-07-06] ingest | Term 1 Lecture 2 amplitude correction and QC sources

Extracted text from source materials for Term 1 Lecture 2 (amplitude corrections and quality control of input data):

- `papers/textbooks/Yilmaz - Seismic Data Analysis_1.pdf` (Ch. 1.3, pp. 25–31) — amplitude, gain control, geometric spreading, AGC, AVO.
- `papers/textbooks/Steve J Hill - Introduction to Seismic Processing.pdf` (Ch. 21, pp. 88–100) — deterministic vs. statistical amplitude correction, spherical divergence, AGC, display issues.
- `papers/signal_processing/metcas - SCAC.ppt.pdf` (full slide deck) — surface-consistent amplitude correction, 4-factor model, Gauss–Seidel iteration, QC.
- `papers/general/ODT01A_DATA_ANALYSIS_PART1_v8.2.pptx` — attenuation definition, direct-arrival QC, divergence correction.
- `papers/general/ODT01A_DATA_ANALYSIS_PART2_v8.3.pptx` — 2D/3D geometry, sorting domains, attribute maps, QC domains.

Created new source pages:

- `wiki/sources/yilmaz_practical_seismic_data_analysis_amplitude.md`
- `wiki/sources/hill_introduction_to_seismic_processing_ch21.md`
- `wiki/sources/brown_2002_surface_consistent_amplitude_correction.md`

Updated existing source pages:

- `wiki/sources/cgg_odt01_data_analysis_part1.md` — added attenuation and direct-arrival QC content.
- `wiki/sources/cgg_odt01_data_analysis_part2.md` — added QC attribute maps and relation to Lecture 2.

Created new concept pages:

- `wiki/concepts/amplitude_effects.md`
- `wiki/concepts/spherical_divergence.md`
- `wiki/concepts/automatic_gain_control.md`
- `wiki/concepts/surface_consistent_amplitude.md`
- `wiki/concepts/seismic_data_qc.md`

Updated `wiki/index.md` with the new concept and source pages.

Ran `uv run python scripts/lint_wiki.py`; no issues found.

## [2026-07-06] lecture-ready | Term 1 Lecture 2 amplitude correction and QC

Created lecture-ready page for Term 1 Lecture 2:

- `wiki/lecture_ready/term01_lec02_amplitude_correction_and_qc.md`

Updated `wiki/index.md` to include the new lecture-ready page.

Ran `uv run python scripts/lint_wiki.py`; no issues found.

## [2026-07-10] wiki | Spectral-analysis and filtering concepts for Term 1 Lecture 5

Extracted source text for the new Term 1 Lecture 5 (spectral analysis and frequency filtering):

- Hatton, Worthington & Makin (1986) DJVU pages 19–23, 29–32, 47–48 — Fourier theory, DFT, aliasing, filtering, spectral analysis.
- Margrave (2006) *Methods of Seismic Data Processing*, PDF pages 36–111 — Chapter 2 signal-processing concepts.
- Yilmaz, *Practical Seismic Data Analysis*, PDF pages 20–31 — sampling, z-transform, aliasing, Fourier amplitude spectrum.

Created concept pages:

- `wiki/concepts/spectral_analysis.md`
- `wiki/concepts/frequency_filtering.md`
- `wiki/concepts/discrete_fourier_transform.md`
- `wiki/concepts/aliasing.md`

Updated source summaries:

- `wiki/sources/hatton_worthington_makin_1986_seismic_data_processing.md`
- `wiki/sources/margrave_2006_methods_of_seismic_data_processing.md`
- `wiki/sources/yilmaz_practical_seismic_data_analysis_amplitude.md`

Updated `wiki/index.md` with the new concept pages and source-title change.

## [2026-07-11] translate | Russian version of Term 1 Lecture 5

Created `lecture_notes/ru/term01_lec05_spectral_analysis_and_filtering.ru.md` — full Russian translation of the English lecture notes on spectral analysis and frequency filtering.

Updated `wiki/index.md` to include the new Russian notes.
