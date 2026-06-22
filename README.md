# Seismic Data Processing Course Materials

This repository contains teaching materials and tooling for an undergraduate course on seismic data processing.

## Structure

| Directory | Purpose |
|-----------|---------|
| `AGENTS.md` | Instructions for the LLM teaching assistant |
| `lecture_notes/` | Markdown lecture notes in English and Russian |
| `slides/` | PowerPoint presentations and outlines |
| `figures/` | PNG/SVG figures for notes and slides |
| `scripts/` | Python scripts for text extraction, organization, and visualization |
| `data/` | Small example datasets |
| `papers/` | PDF/PPT library organized by topic |
| `wiki/` | Persistent LLM-maintained knowledge base |
| `exercises/` | Concept checks and small assignments |
| `references/` | Bibliography and source annotations |
| `docs/` | Project documentation, including the lecture development workflow |

## Python environment

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Install dependencies and create the virtual environment
uv sync

# Run a script
uv run python scripts/extract_source_text.py papers/deconvolution/file.pdf

# Add a package
uv add <package>
```

## Usage guide

### Organize a new batch of papers

Drop PDFs/PPTs into `papers/raw/`, then run the organization script to get a proposed topic structure:

```bash
uv run python scripts/organize_papers.py
```

Review `papers/_organization_report.csv`, then apply the plan:

```bash
# Dry run first
uv run python scripts/apply_paper_organization.py --dry-run

# Apply for real
uv run python scripts/apply_paper_organization.py
```

### Ingest a source into the wiki

Extract text from a PDF or PPTX locally:

```bash
uv run python scripts/extract_source_text.py papers/deconvolution/file.pdf -o wiki/sources/_raw_text
```

Then create or update a source summary in `wiki/sources/`, update the relevant concept pages in `wiki/concepts/`, and refresh `wiki/index.md` and `wiki/log.md`.

### Lint the wiki

Check the wiki for missing frontmatter, dead links, orphan pages, and other structural issues:

```bash
# Strict mode (stubs count as errors)
uv run python scripts/lint_wiki.py

# Lenient mode (stubs reported as warnings only)
uv run python scripts/lint_wiki.py --warn-stub
```

### Prepare lecture materials

1. Use the wiki to find and synthesize content for a lecture.
2. Draft lecture notes in `lecture_notes/en/`.
3. Generate supporting figures with self-contained Python scripts in `scripts/` and save them to `figures/`.
4. Translate notes to Russian in `lecture_notes/ru/`.
5. Render PDFs with a lightweight CLI tool such as Pandoc.

## Wiki workflow

The `wiki/` directory follows the LLM-wiki / second-brain pattern: raw sources are summarized once into concept and source pages, and those summaries are reused for lecture preparation and Q&A.

See `wiki/README.md` for detailed conventions.

## Lecture development workflow

For a step-by-step guide on how to turn existing slide decks and rough outlines into finished, bilingual lecture notes and updated slides, see `docs/lecture_workflow.md`.

## Git notes

- Source PDFs, PPTs, and large data files in `papers/` and `data/` are ignored by Git.
- Folder structure is preserved with `.gitkeep` files.
