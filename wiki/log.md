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

## [2026-06-22] todo | Open questions from pilot

- Add FX-deconvolution, robust deconvolution, and MBWP source summaries.
- Build comparison page: predictive vs. surface-consistent deconvolution.
- Create first lecture-ready page for Term 1 deconvolution lecture.
