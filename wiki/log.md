# Wiki Log

Chronological record of ingests, queries, and lint passes.

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

## [2026-06-29] lecture | Term 1 Lecture 02 — Kinematics, Velocities and Field Statics

- Confirmed split of original kinematics/statics lecture into Lecture 02 (velocities, NMO, field statics, refraction) and Lecture 03 (layer replacement, residual statics, floating datum).
- Extracted text from existing materials: `slides/raw/term01_lecture02_kinematics.pptx` and `slides/raw/plan_term01_lecture02_kinematics.docx`.
- Drafted outline: `lecture_notes/_drafts/term01_lec02_kinematics_and_field_statics_outline.md`.
- Generated 7 self-contained Python figure scripts in `scripts/figures/term01_lec02/` and PNGs in `figures/term01_lec02/`.
- Wrote English lecture notes: `lecture_notes/en/term01_lec02_kinematics_and_field_statics.en.md`.
- Rendered PDF successfully.
- Created exercises: `exercises/term01_lec02_kinematics_and_field_statics.md`.
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

## [2026-06-29] lecture | Term 1 Lecture 03 — Advanced Statics and the Link to Velocity Analysis

- Drafted outline: `lecture_notes/_drafts/term01_lec03_advanced_statics_and_velocity_link_outline.md`.
- Wrote English lecture notes: `lecture_notes/en/term01_lec03_advanced_statics_and_velocity_link.en.md`.
- Rendered PDF successfully.
- Dispatched a worker subagent to create 6 self-contained Python figure scripts in `scripts/figures/term01_lec03/` and PNGs in `figures/term01_lec03/`.
- Regenerated the statics-velocity-bias figure after identifying that it did not show a velocity bias; corrected the script so the semblance peak and $t^2$ vs $x^2$ slope both shift.
- Created exercises: `exercises/term01_lec03_advanced_statics_and_velocity_link.md`.
- Created slide outline and starter PowerPoint deck in `slides/term01/lec03_advanced_statics_and_velocity_link/`.
- Created lecture-ready page: `wiki/lecture_ready/term01_lec03_advanced_statics_and_velocity_link.md`.
- Updated `wiki/index.md` and linked `wiki/concepts/static_corrections.md` to the new lecture-ready page.
- Wiki lint passes cleanly.

## [2026-06-29] todo | Remaining work

- Add FX-deconvolution, robust deconvolution, and MBWP source summaries.
- Build comparison page: predictive vs. surface-consistent deconvolution.
- Review English notes for term01_lec06/lec07 with instructor and adjust content/timing as needed.
- Optionally build final PowerPoint slides for term01_lec06/lec07 from outlines.
- Translate exercises and slide outlines for term01_lec06/lec07 to Russian.
- Optionally assemble the PowerPoint deck for term01_lec01 from the slide outline.
- Translate Lecture 02 and Lecture 03 notes, exercises, and slide outlines to Russian once English versions are approved.
- Renumber remaining Term 1 lectures after the split is finalized.

## [2026-06-27] todo | Remaining work

- Add FX-deconvolution, robust deconvolution, and MBWP source summaries.
- Build comparison page: predictive vs. surface-consistent deconvolution.
- Review English notes for term01_lec06/lec07 with instructor and adjust content/timing as needed.
- Optionally build final PowerPoint slides for term01_lec06/lec07 from outlines.
- Translate exercises and slide outlines for term01_lec06/lec07 to Russian.
- Optionally assemble the PowerPoint deck for term01_lec01 from the slide outline.
- Draft Lecture 03 (advanced statics, layer replacement, floating datum) after Lecture 02 is approved.
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
  - `lecture_ready/term01_lec02_kinematics_and_field_statics.md`
  - `lecture_ready/term01_lec03_advanced_statics_and_velocity_link.md`
- Ran `uv run python scripts/lint_wiki.py`; no issues found.
