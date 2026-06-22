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

## Python environment

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
# Run a script
uv run python scripts/extract_source_text.py papers/deconvolution/file.pdf

# Add a package
uv add <package>
```

## Wiki workflow

The `wiki/` directory follows the LLM-wiki / second-brain pattern: raw sources are summarized once into concept and source pages, and those summaries are reused for lecture preparation and Q&A.

See `wiki/README.md` for detailed conventions.

## Git notes

- Source PDFs, PPTs, and large data files in `papers/` and `data/` are ignored by Git.
- Folder structure is preserved with `.gitkeep` files.
