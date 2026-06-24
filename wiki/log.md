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

## [2026-06-24] todo | Remaining work

- Add FX-deconvolution, robust deconvolution, and MBWP source summaries.
- Build comparison page: predictive vs. surface-consistent deconvolution.
- Review English notes with instructor and adjust content/timing as needed.
- Optionally build final PowerPoint slides from outlines.
- Translate exercises and slide outlines to Russian.
