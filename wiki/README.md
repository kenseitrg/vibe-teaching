# Course Wiki

This directory implements a **persistent LLM-maintained wiki** (inspired by [Karpathy's LLM wiki / second-brain pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)) for the seismic data processing course.

## Purpose

The wiki sits between the raw paper/PPT library (`papers/`) and the student-facing materials (`lecture_notes/`, `slides/`, `figures/`). It stores:

- Summaries of papers and textbooks.
- Concept and technique pages.
- Comparisons and syntheses.
- Lecture-ready distillations.

Knowledge is **compiled once and kept current** rather than re-derived from raw sources every time.

## Structure

| Directory | Content |
|-----------|---------|
| `concepts/` | Core seismic processing concepts (e.g., deconvolution, NMO, migration). |
| `techniques/` | Practical workflows and parameter choices. |
| `sources/` | One summary page per paper/book/course. |
| `comparisons/` | Side-by-side comparisons of methods. |
| `lecture_ready/` | Pages already synthesized for a specific lecture. |
| `index.md` | Catalog of all pages. Updated after every ingest. |
| `log.md` | Chronological record of ingests, queries, and lint passes. |

## Page conventions

Each markdown page should include YAML frontmatter:

```yaml
---
title: Page Title
status: draft    # stub | draft | reviewed | lecture-ready
sources:         # list of source page IDs (without path)
  - source_page_id
tags: [tag1, tag2]
---
```

## Workflows

### Ingest a new source

1. Add the PDF/PPT to the appropriate `papers/<topic>/` folder.
2. Extract text locally:
   ```bash
   uv run python scripts/extract_source_text.py papers/<topic>/<file> -o wiki/sources/_raw_text
   ```
3. Create or update `wiki/sources/<descriptive_name>.md`.
4. Update related `wiki/concepts/*.md` pages.
5. Update `wiki/index.md` and append to `wiki/log.md`.

### Answer a course question

1. Read `wiki/index.md` to find relevant pages.
2. Read the relevant concept/source pages.
3. Synthesize the answer and, if valuable, file it back as a new wiki page.

### Lint the wiki

Periodically run a lint pass:

- Check for contradictions between pages.
- Find orphan pages with no inbound links.
- Identify concepts mentioned but lacking their own page.
- Suggest missing cross-references.

## Local tools

- `scripts/extract_source_text.py` — extract text from PDF/PPT/PPTX.
- `scripts/organize_papers.py` — organize `papers/raw/` by topic.
- `scripts/apply_paper_organization.py` — apply the organization plan.

## Note

Only markdown files and scripts are tracked by Git. Source PDFs/PPTs in `papers/` are ignored.
