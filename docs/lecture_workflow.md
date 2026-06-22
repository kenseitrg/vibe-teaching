# Lecture Development Workflow

This document describes the end-to-end process for turning existing materials into a polished, bilingual lecture using the wiki, lecture notes, and slide pipeline.

## Goal

For each lecture, produce:

1. A `lecture_notes/en/termXX_lecYY_<topic>.en.md` file (authoritative content).
2. A `lecture_notes/ru/termXX_lecYY_<topic>.ru.md` file (Russian translation).
3. Updated or enhanced PowerPoint slides in `slides/termXX/lecYY_<topic>/`.
4. Self-contained Python scripts in `scripts/figures/termXX_lecYY/` that generate PNG figures for the slides and notes.
5. A short set of comprehension questions at the end of the lecture notes.

## Precondition

The general infrastructure is already in place:

- `AGENTS.md` defines agent behavior, conventions, and pedagogical rules.
- `wiki/` is initialized as a persistent knowledge base.
- `scripts/extract_source_text.py`, `scripts/lint_wiki.py`, and paper organization scripts are available.
- The `uv` Python environment is configured.

---

## Step-by-step process for one lecture

### Step 0 — Pick the lecture and gather inputs

1. Decide the lecture:
   - Term number (`term01`, `term02`, `term03`).
   - Lecture number (`lec05`).
   - Short topic slug (e.g., `velocity_analysis`, `deconvolution`).
2. Collect inputs:
   - Existing PowerPoint: copy into `slides/raw/termXX_lecYY_<topic>.pptx`.
   - Existing lecture plan/outline (Word/PDF): copy into `slides/raw/_plan_termXX_lecYY_<topic>.docx`.
   - Relevant sources from `papers/`, or note which ones to look up.

### Step 1 — Extract text from existing materials

Run the local extraction script on the PPT and any plan document:

```bash
uv run python scripts/extract_source_text.py \
  slides/raw/termXX_lecYY_<topic>.pptx \
  -o slides/raw/_text

uv run python scripts/extract_source_text.py \
  slides/raw/_plan_termXX_lecYY_<topic>.docx \
  -o slides/raw/_text
```

Review the extracted text briefly with the agent. It gives a structured view of what the slides currently cover.

### Step 2 — Ensure relevant wiki sources are ingested

Check `wiki/index.md` to see whether key papers for this lecture are already summarized. If not:

1. Identify the 2–5 most important sources for this lecture.
2. Extract their text:
   ```bash
   uv run python scripts/extract_source_text.py papers/<topic>/source.pdf -o wiki/sources/_raw_text
   ```
3. Create/update source summary pages in `wiki/sources/`.
4. Update or create concept pages in `wiki/concepts/`.
5. Update `wiki/index.md` and append to `wiki/log.md`.
6. Run the linter:
   ```bash
   uv run python scripts/lint_wiki.py
   ```

### Step 3 — Build or update the lecture outline

Create an outline file `lecture_notes/_drafts/termXX_lecYY_<topic>_outline.md` with:

- Learning objectives (3–5 bullet points).
- Prerequisites students should already know.
- Section breakdown with estimated timing for a 90-minute lecture:
  - Introduction (5–10 min)
  - Main part 1 (20–25 min)
  - Main part 2 (20–25 min)
  - Main part 3 / examples (15–20 min)
  - Comprehension questions / discussion (10–15 min)
  - Buffer for questions (5–10 min)
- List of figures/visualizations needed.
- List of key equations (if any).
- For each key equation, decide whether to:
  - Include it directly in the lecture notes (brief, conceptual derivation).
  - Create a separate derivation document in `lecture_notes/derivations/` (step-by-step, full mathematical detail).
- Links to relevant `wiki/concepts/` pages.

Review and adjust this outline with the instructor before writing prose.

### Step 4 — Write the English lecture notes

Create `lecture_notes/en/termXX_lecYY_<topic>.en.md` from the outline.

Guidelines:

- Follow the pedagogical rules in `AGENTS.md`:
  - Physical/geometric intuition before equations.
  - Keep math present but undergraduate-friendly.
  - Use worked examples with realistic numbers.
  - Embed generated figures and reference them.
- Cite wiki source pages and papers where appropriate.
- Include key equations. For equations whose full derivation is too long for the notes, reference the matching derivation document in `lecture_notes/derivations/`.
- Include comprehension questions at the end.
- Use consistent notation; add new terms to the notation glossary in `AGENTS.md`.

### Step 5 — Plan and generate figures

For each figure in the outline:

1. Decide what concept it illustrates and what the student should notice.
2. Create a self-contained Python script in `scripts/figures/termXX_lecYY/`.
3. Run it to produce PNGs in `figures/termXX_lecYY/`.
4. Embed the PNG in the lecture notes and reference it in the slide outline.

Naming convention:

```text
figures/termXX_lecYY/termXX_lecYY_<concept>.png
scripts/figures/termXX_lecYY/plot_<concept>.py
```

For bilingual figures, generate separate `.en.png` and `.ru.png` versions if axis labels or annotations differ.

### Step 6 — Produce the Russian translation

Once the English notes are stable, create `lecture_notes/ru/termXX_lecYY_<topic>.ru.md`.

Approach:

- Translate section by section.
- Keep figure references identical (same filenames).
- Use a shared glossary of technical terms to keep terminology consistent.
- Review the translation with the agent for accuracy and readability.

### Step 7 — Update or rebuild the PowerPoint slides

Slides should be derived from the lecture notes, not the other way around.

1. Create/update a slide outline in `slides/termXX/lecYY_<topic>/slide_outline.md`:
   - One slide per bullet with title, body text, and figure reference.
2. Generate any missing slide-specific PNG figures.
3. Build the PowerPoint manually in `slides/termXX/lecYY_<topic>/lecYY_<topic>.pptx`.
   - The agent can assist with outlines and figures; final assembly remains in PowerPoint.
4. Translate slide text, notes, and captions into Russian and save a copy if needed.

### Step 8 — Add exercises / concept-checks

Create or update `exercises/termXX_lecYY_<topic>.md` with:

- 3–5 comprehension questions.
- 1–2 short numerical or conceptual problems.
- Optional: a small Python demo or data-exploration task.

### Step 9 — Review and lint

1. Run the wiki linter:
   ```bash
   uv run python scripts/lint_wiki.py
   ```
2. Check figure scripts still run cleanly.
3. Read the lecture notes aloud or ask the agent to flag dense sections.
4. Verify timing estimates add up to ~90 minutes.
5. Update `wiki/index.md` and `wiki/log.md` with the new lecture-ready page.

### Step 10 — Commit

Commit the new/changed files:

```bash
git add lecture_notes/ slides/ scripts/figures/ figures/ exercises/ wiki/
git commit -m "Add Term X Lecture Y: <topic>"
```

---

## File naming convention

| Artifact | Path pattern | Example |
|----------|--------------|---------|
| English notes | `lecture_notes/en/termXX_lecYY_<topic>.en.md` | `lecture_notes/en/term01_lec05_velocity_analysis.en.md` |
| Russian notes | `lecture_notes/ru/termXX_lecYY_<topic>.ru.md` | `lecture_notes/ru/term01_lec05_velocity_analysis.ru.md` |
| Figures | `figures/termXX_lecYY/termXX_lecYY_<concept>.png` | `figures/term01_lec05/term01_lec05_nmo_correction.png` |
| Figure scripts | `scripts/figures/termXX_lecYY/plot_<concept>.py` | `scripts/figures/term01_lec05/plot_nmo_correction.py` |
| Slide outline | `slides/termXX/lecYY_<topic>/slide_outline.md` | `slides/term01/lec05_velocity_analysis/slide_outline.md` |
| Slide deck | `slides/termXX/lecYY_<topic>/lecYY_<topic>.pptx` | `slides/term01/lec05_velocity_analysis/lec05_velocity_analysis.pptx` |
| Exercises | `exercises/termXX_lecYY_<topic>.md` | `exercises/term01_lec05_velocity_analysis.md` |
| Wiki lecture-ready page | `wiki/lecture_ready/termXX_lecYY_<topic>.md` | `wiki/lecture_ready/term01_lec05_velocity_analysis.md` |
| Derivation document | `lecture_notes/derivations/<topic>_derivation.en.md` | `lecture_notes/derivations/wiener_deconvolution_derivation.en.md` |

---

## Timing and iteration

| Step | Estimated time | Who drives |
|------|----------------|------------|
| 0–1: Gather and extract | 10–20 min | Agent + instructor |
| 2: Wiki ingest | 20–40 min | Agent |
| 3: Outline | 15–30 min | Agent + instructor |
| 4: English notes | 45–90 min | Agent |
| 5: Figures | 30–90 min | Agent |
| 6: Russian notes | 30–60 min | Agent + instructor review |
| 6a: Derivation documents | 30–60 min | Agent |
| 7: Slides | 30–60 min | Instructor (agent assists) |
| 8: Exercises | 15–30 min | Agent |
| 9: Review | 15–30 min | Both |
| 10: Commit | 5 min | Agent |

A complete lecture can typically be prepared in **1–2 focused sessions** once the wiki is populated for the topic.

---

## Special cases

### Lecture with no existing slides

Follow the same workflow, but Step 1 is skipped. Spend more time in Step 2 (wiki ingest) and Step 3 (outline).

### Lecture that needs major slide rework

Use the existing PPT as a reference for scope only. Treat the lecture notes as the new authoritative source and rebuild slides in Step 7.

### Lecture heavily based on one textbook

Do not ingest the whole book. Identify the specific chapters/sections relevant to the lecture, extract only those pages, and create focused source summaries.

### Lecture that reuses figures from the internet

Replace internet images with self-generated PNGs in Step 5. Keep a list of replaced images in `slides/termXX/lecYY_<topic>/replaced_figures.md` for attribution or reference.

### Lecture with important derivations

If a topic depends on a key equation whose derivation is too detailed for the main notes (e.g., Wiener deconvolution normal equations):

1. State the equation and its meaning in the lecture notes.
2. Create a separate derivation document in `lecture_notes/derivations/<topic>_derivation.en.md`.
3. Include the full step-by-step derivation, starting from the convolutional model.
4. Translate the derivation document to Russian if students are expected to read it in Russian.
5. Link to it from the lecture notes and optionally from the wiki concept page.

---

## Maintenance after delivery

After giving the lecture:

1. Update the lecture-ready wiki page with any student questions or clarifications.
2. Fix figure scripts if errors are found.
3. Update comprehension questions based on what students struggled with.
4. Append a brief entry to `wiki/log.md`.
