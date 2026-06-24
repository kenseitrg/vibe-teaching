#!/usr/bin/env python3
"""
Render a Markdown lecture note file to PDF using Pandoc + LaTeX.

Usage:
    uv run python scripts/render_lecture.py lecture_notes/en/file.md
    uv run python scripts/render_lecture.py lecture_notes/en/file.md -o output.pdf
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Render lecture notes Markdown to PDF.")
    parser.add_argument("input", help="Input Markdown file")
    parser.add_argument("--output", "-o", help="Output PDF path (default: same stem as input)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else input_path.with_suffix(".pdf")

    if not shutil.which("pandoc"):
        print("pandoc not found. Install it first.", file=sys.stderr)
        sys.exit(1)

    # Compute resource path relative to input file so image links resolve.
    resource_path = input_path.parent

    # Detect language from filename suffix for font selection
    stem = input_path.stem  # e.g. "term01_lec06_single_channel_deconvolution.ru"
    lang = "ru" if stem.endswith(".ru") else "en"

    cmd = [
        "pandoc",
        str(input_path),
        "-o", str(output_path),
        "--pdf-engine=xelatex",
        "-V", "geometry:margin=2.5cm",
        "-V", "fontsize=11pt",
        "-V", f"lang={lang}",
        "--resource-path", str(resource_path),
    ]

    if lang == "ru":
        # DejaVu Serif supports Cyrillic glyphs
        cmd += ["-V", "mainfont=DejaVu Serif"]

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"Rendered: {output_path}")


if __name__ == "__main__":
    main()
