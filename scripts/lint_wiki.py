#!/usr/bin/env python3
"""
Health-check the wiki for structural issues.

Checks:
- YAML frontmatter is present and valid on every markdown page.
- Every concept/technique/comparison/lecture_ready page has a valid status.
- Orphan pages (no inbound links from other wiki pages).
- Missing source references (frontmatter sources without a corresponding file).
- Dead internal links (links to non-existent pages).
- Untagged pages (no tags in frontmatter).
- Pages with status 'stub' that have been around a long time.

Usage:
    uv run python scripts/lint_wiki.py [--wiki wiki/]
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

WIKI_ROOT = Path("wiki")
VALID_STATUSES = {"stub", "draft", "reviewed", "lecture-ready"}


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and remaining body from markdown content."""
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    frontmatter_raw = parts[1].strip()
    body = parts[2]
    metadata = {}
    key = None
    for line in frontmatter_raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("-"):
            # list item
            value = stripped.lstrip("-").strip()
            if key:
                metadata[key].append(value)
        else:
            if ":" in stripped:
                key, value = stripped.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if value == "":
                    metadata[key] = []
                else:
                    metadata[key] = value
    return metadata, body


def find_wiki_pages(wiki_root: Path) -> list[Path]:
    """Return all markdown files under wiki_root, excluding _raw_text and README/index/log."""
    pages = []
    for path in wiki_root.rglob("*.md"):
        if "_raw_text" in path.parts:
            continue
        if path.name in {"README.md", "index.md", "log.md"}:
            continue
        pages.append(path)
    return sorted(pages)


def extract_internal_links(body: str, page_path: Path) -> list[tuple[str, Path]]:
    """Extract internal markdown links and resolve them relative to the page."""
    links = []
    # Pattern: [text](path)
    for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", body):
        link_target = match.group(2)
        # Skip external links and anchors-only
        if link_target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        # Strip anchor
        link_target = link_target.split("#", 1)[0]
        if not link_target:
            continue
        # Resolve relative to page directory
        if link_target.startswith("/"):
            resolved = (page_path.parent.parent / link_target.lstrip("/")).resolve()
        else:
            resolved = (page_path.parent / link_target).resolve()
        links.append((match.group(1), resolved))
    return links


def lint_wiki(wiki_root: Path) -> dict:
    pages = find_wiki_pages(wiki_root)
    issues = defaultdict(list)
    all_page_paths = {p.resolve(): p for p in pages}
    inbound_links = defaultdict(list)
    source_pages = set()

    for page in pages:
        rel_path = page.relative_to(wiki_root)
        content = page.read_text(encoding="utf-8")
        metadata, body = parse_frontmatter(content)

        # 1. Frontmatter presence
        if not metadata:
            issues["missing_frontmatter"].append(str(rel_path))
            continue

        # 2. Required fields
        for field in ("title", "status"):
            if field not in metadata:
                issues[f"missing_{field}"].append(str(rel_path))

        # 3. Valid status
        status = metadata.get("status")
        if status and status not in VALID_STATUSES:
            issues["invalid_status"].append(f"{rel_path}: {status}")

        # 4. Untagged pages
        tags = metadata.get("tags", [])
        if not tags:
            issues["untagged"].append(str(rel_path))

        # 5. Source references
        sources = metadata.get("sources", [])
        if isinstance(sources, str):
            sources = [sources]
        for src in sources:
            src_path = (wiki_root / "sources" / f"{src}.md").resolve()
            source_pages.add(src_path)
            if src_path not in all_page_paths:
                issues["missing_source_page"].append(f"{rel_path} -> sources/{src}.md")

        # 6. Dead internal links
        for text, resolved in extract_internal_links(body, page):
            if resolved.suffix == "":
                resolved = resolved.with_suffix(".md")
            if resolved not in all_page_paths:
                issues["dead_link"].append(f"{rel_path}: [{text}]({resolved.name})")
            else:
                inbound_links[resolved].append((str(rel_path), text))

    # 7. Orphan pages (pages with no inbound links)
    for page in pages:
        resolved = page.resolve()
        if resolved not in inbound_links:
            rel_path = page.relative_to(wiki_root)
            # Source pages are allowed to be orphans (they are referenced by frontmatter)
            if resolved not in source_pages:
                # Index is also allowed
                issues["orphan_page"].append(str(rel_path))

    # 8. Stub pages
    for page in pages:
        content = page.read_text(encoding="utf-8")
        metadata, _ = parse_frontmatter(content)
        if metadata.get("status") == "stub":
            rel_path = page.relative_to(wiki_root)
            issues["stub_page"].append(str(rel_path))

    return dict(issues)


def main():
    parser = argparse.ArgumentParser(description="Lint the course wiki.")
    parser.add_argument("--wiki", default="wiki", help="Path to the wiki root directory")
    parser.add_argument("--warn-stub", action="store_true", help="Report stub pages as warnings, not errors")
    args = parser.parse_args()

    wiki_root = Path(args.wiki)
    if not wiki_root.exists():
        print(f"Wiki directory not found: {wiki_root}")
        sys.exit(1)

    issues = lint_wiki(wiki_root)

    stub_items = issues.pop("stub_page", [])

    if not issues and not stub_items:
        print("Wiki looks healthy. No issues found.")
        sys.exit(0)

    print("Wiki lint results:\n")
    total_errors = 0
    for category, items in issues.items():
        print(f"## {category.replace('_', ' ').title()} ({len(items)})")
        for item in items:
            print(f"  - {item}")
        total_errors += len(items)
        print()

    if stub_items:
        print(f"## Stub Pages ({len(stub_items)})")
        for item in stub_items:
            print(f"  - {item}")
        print()

    print(f"Total errors: {total_errors}")
    if stub_items:
        print(f"Stub warnings: {len(stub_items)} (use --warn-stub to treat as non-fatal)")

    if total_errors > 0:
        sys.exit(1)
    elif stub_items and not args.warn_stub:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
