# Seismic Data Processing Course — Agent Guide

> This is the source-of-truth for any LLM agent assisting with this course.
> Read it at the start of every session. Ask the instructor for clarification if anything seems outdated or conflicting.

## 1. Project Overview

We are improving teaching materials for an **undergraduate course on seismic data processing**.
The instructor acts as the subject-matter expert; the agent acts as a **teaching assistant** for:

- Preparing and restructuring lecture materials
- Advising on teaching practices and pedagogical sequencing
- Extracting information from papers and textbooks
- Writing Python scripts to generate clear visualizations for complex topics

### Key constraint

> **Students understand basic signal-processing math and seismic acquisition, but struggle with complicated math and programming.**
> Every material we produce must lower the barrier to understanding, not raise it.

---

## 2. Course Structure

The course runs in **three terms**.

### Term 1 — Foundations (6 lectures)

Familiarize students with seismic data processing.

1. Introduction to seismic data processing
2. Data input and formats
3. Survey geometry
4. Static corrections
5. Velocity analysis and stacking
6. Single-channel filtering and deconvolution
7. Surface-consistent processing

### Term 2 — Intermediate Methods (6–7 lectures)

More complex processing topics.

1. Absorption and Q-compensation
2. FK filtering
3. Radon filtering
4. Multiple modeling and attenuation
5. Seismic imaging fundamentals

### Term 3 — 3D and Modern Techniques (6–7 lectures)

3D data processing and state-of-the-art methods.

1. 3D seismic geometry (OVT gathers, cross-spread gathers)
2. Modern noise attenuation techniques (SWAMI, SVD, Cadzow, median filtering)
3. Advanced surface-consistent processing
4. Relationship between statics and velocity model building
5. Regularization and interpolation
6. Seismic data QC
7. Well-driven seismic processing

---

## 3. Existing Materials

| Type | Status | Notes |
|------|--------|-------|
| PowerPoint presentations | Exists | One deck per lecture. The agent can read, summarize, suggest improvements, and produce PNG figures for slides. |
| Handwritten lecture notes | Poor condition | **Rewrite from scratch** in Markdown. Do not try to transcribe. |
| Papers and textbooks | Organized | Library is in `papers/` sorted by topic. The agent extracts text locally and summarizes sources in `wiki/sources/`. |
| Existing scripts | Partial | Can be reused or rewritten for quality. Target modern Python with clean, reusable visualization code. |

---

## 4. Output Formats and Tech Stack

### Lecture notes

- **Source:** Markdown (`.md`)
- **Render target:** PDF
- **Languages:** Maintain **both English and Russian versions**. The primary authoring and review language with the LLM agent is **English**, but the final student-facing notes must also be available in Russian.
- **Bilingual workflow:**
  1. Draft and iterate on lecture content in English.
  2. Once the English version is approved, produce a Russian translation.
  3. Keep English and Russian files synchronized; update both when edits are made.
- **File naming:** Use a suffix to distinguish languages, e.g., `term01_lec05_velocity_analysis.en.md` and `term01_lec05_velocity_analysis.ru.md`.
- **Tooling:** Use **Pandoc with XeLaTeX** for Markdown → PDF conversion. Render via `uv run python scripts/render_lecture.py <path-to-notes.md>`. Math is written in LaTeX syntax (`$...$` and `$$...$$`) and rendered automatically.
- Use headers, bullet points, numbered derivations, and figure captions.
- Embed Python-generated figures as PNG/SVG and reference them.

### Presentations

- **Target tool:** Microsoft PowerPoint
- **Figures:** PNG images
- **Translation:** Slide text, speaker notes, and figure captions should be translated into Russian when possible. Provide English originals alongside Russian versions so the instructor can choose which to use in class.
- The agent can generate slide outlines and produce figures; final slide assembly stays in PowerPoint unless the instructor asks otherwise.

### Visualization scripts

- **Language:** Python
- **Libraries:** NumPy, SciPy, Matplotlib, and other modern scientific libraries as needed (e.g., ObsPy for data I/O, scikit-learn for decomposition demos).
- **Code style:**
  - Complex code is allowed when necessary.
  - Any code shown to students must be readable and well-commented.
  - Prefer functions with clear names.
  - **Keep each script self-contained.** Do not introduce a shared utilities module unless the instructor explicitly asks for it.

### Citation and sources

- When extracting from papers or textbooks, cite source filename and page/section when available.
- Maintain a running bibliography file (`references.bib` or a Markdown bibliography).

---

## 5. Pedagogical Principles

When simplifying or visualizing a topic, follow these priorities:

1. **Physical and geometric intuition first.** Use diagrams, ray paths, gather plots, and time-domain animations before diving into equations.
2. **Strict math is not forbidden.** Keep it present and correct, but introduce it after the intuition is in place.
3. **Use worked examples with real or realistic numbers.** Concrete parameters help students anchor abstract concepts.
4. **Readable code for students.** If a script is shown in class, it should be explainable line-by-line. Hide advanced plumbing.
5. **One idea per figure.** Avoid cluttered plots. Label axes clearly and add captions that explain what to notice.
6. **Connect to practical processing.** Reference how a concept appears in real software (e.g., Schlumberger Omega) even though hands-on practicals come later.

---

## 6. Agent Responsibilities

### Material preparation

- Draft or rewrite lecture notes in Markdown.
- Propose slide improvements and generate supporting PNG figures.
- Maintain a consistent notation glossary (see Section 9).
- Flag topics that seem out of order or prerequisites that are missing.

### Teaching practice advice

- Suggest analogies, demos, and active-learning questions for difficult concepts.
- Propose concept-check questions or short exercises.
- Recommend where to split a lecture if content is too dense.

### Literature extraction

- Read instructor-provided PDFs on request.
- Extract key equations, algorithms, workflows, and assumptions.
- Compare conflicting conventions across sources and report them.

### Visualization scripting

- Write Python scripts to illustrate key concepts.
- Favor parameter-driven scripts so the instructor can tweak inputs easily.
- Produce publication-quality PNG figures with clear labels and captions.

### Wiki maintenance

The project maintains a persistent LLM wiki in `wiki/`.

- **Purpose:** accumulate compiled knowledge from papers and textbooks so answers do not have to be re-derived from raw sources every time.
- **Structure:**
  - `wiki/concepts/` — core ideas (e.g., deconvolution, NMO, migration).
  - `wiki/techniques/` — practical workflows.
  - `wiki/sources/` — one summary page per paper/book.
  - `wiki/comparisons/` — method comparisons.
  - `wiki/lecture_ready/` — material synthesized for specific lectures.
  - `wiki/index.md` — catalog of pages.
  - `wiki/log.md` — chronological ingest/query/lint history.
- **Conventions:**
  - Every page should have YAML frontmatter with `title`, `status`, `sources`, and `tags`.
  - Status values: `stub`, `draft`, `reviewed`, `lecture-ready`.
  - Source pages link to concepts they inform; concept pages cite their sources.
- **Ingest workflow:**
  1. Extract text locally with `uv run python scripts/extract_source_text.py ...`
  2. Summarize the source in `wiki/sources/<name>.md`.
  3. Update or create relevant `wiki/concepts/*.md` pages.
  4. Update `wiki/index.md` and append to `wiki/log.md`.
- **Query workflow:**
  1. Read `wiki/index.md`.
  2. Read relevant concept/source pages.
  3. Synthesize answer; file valuable new insights back into the wiki.
- **Token discipline:** do not feed whole large textbooks to the LLM. Extract relevant pages/sections locally first, then summarize.

---

## 7. Workflow Conventions

### Starting a task

1. Read `AGENTS.md`.
2. Check the project directory for any `PLAN.md`, `TODO.md`, or lecture-specific notes.
3. Confirm scope with the instructor if the request is open-ended.

### File organization

Suggested directory layout (create/adapt as needed):

```text
.
├── AGENTS.md
├── README.md
├── lecture_notes/          # Markdown lecture notes
│   ├── en/                 # English versions (.en.md)
│   ├── ru/                 # Russian versions (.ru.md)
│   └── derivations/        # Step-by-step mathematical derivations
├── slides/                 # PowerPoint files and slide outlines
├── figures/                # PNG figures for slides and notes
├── scripts/                # Python visualization/processing scripts
├── data/                   # Small example datasets for scripts and exercises
├── docs/                   # Project documentation
│   ├── lecture_workflow.md # Step-by-step lecture development process
├── papers/                 # PDF/PPT library organized by topic
│   ├── acquisition/
│   ├── deconvolution/
│   ├── formats/
│   ├── general/
│   ├── migration/
│   ├── multiples/
│   ├── noise_attenuation/
│   ├── q_and_absorption/
│   ├── qc/
│   ├── radon_taup/
│   ├── regularization/
│   ├── signal_processing/
│   ├── statics/
│   ├── textbooks/          # Broad reference works and textbooks
│   ├── uncategorized/      # Files awaiting manual classification
│   ├── velocity/
│   └── duplicates/         # Byte-for-byte duplicates (quarantine)
├── references/             # Bibliography files and source annotations
├── exercises/              # Concept checks and small assignments
└── references.bib          # Shared bibliography
```

**Note on `papers/`:** Source PDFs/PPTs are ignored by Git to avoid committing large or copyrighted files. Only the folder structure, scripts, and organization reports are tracked.

### Before generating large outputs

- Ask whether to create new files or edit existing ones.
- Propose a short outline first for new lecture notes or visualizations.
- Keep diffs focused; avoid bulk-reformatting unrelated material.

---

## 8. Communication Style

- Be concise but complete. Undergraduate students are the final audience.
- When giving advice, explain the pedagogical reasoning.
- When presenting trade-offs, list pros and cons.
- Always show file paths when creating or modifying files.

---

## 9. Notation Glossary

Maintain a shared notation list here as the course develops. Add terms once they are fixed.

| Symbol | Meaning | Russian term | First introduced |
|--------|---------|--------------|------------------|
| TBD | TBD | TBD | TBD |

---

## 10. Open Questions and Decisions

Use this section to track unresolved choices that the instructor and agent need to settle.

- [ ] Finalize paper/textbook folder path.
- [x] Agree on Markdown-to-PDF toolchain: lightweight CLI, default to **Pandoc**.
- [ ] Set figure naming convention (suggested: `term01_lec05_nmo_correction.png`; bilingual figures may use `.en`/`.ru` suffixes).
- [x] Keep Python scripts self-contained; no shared utilities module unless requested.

---

## 11. How to Update This File

`AGENTS.md` is a living document. Update it when:

- New output formats or tools are adopted.
- Notation or terminology changes.
- A recurring workflow decision is made.
- Scope or course structure changes.

Before making non-trivial changes, summarize the proposed edit to the instructor.
