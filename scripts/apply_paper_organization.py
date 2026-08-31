#!/usr/bin/env python3
"""
Apply the organization plan from papers/_organization_report.csv.

- Creates topic folders under papers/.
- Moves each unique file to its proposed topic folder with the clean filename.
- Moves duplicate files to papers/duplicates/ (quarantine, not delete).
- Moves remaining uncategorized files to papers/uncategorized/.
- Leaves papers/raw/ untouched as the original archive.

Usage:
    python scripts/apply_paper_organization.py [--dry-run]
"""

import argparse
import csv
import shutil
from pathlib import Path

RAW_DIR = Path("papers/raw")
BASE_DIR = Path("papers")
REPORT_CSV = BASE_DIR / "_organization_report.csv"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def unique_dst(dst: Path, used: set) -> Path:
    """Ensure destination path is unique by appending a counter if needed."""
    if dst not in used and not dst.exists():
        used.add(dst)
        return dst
    stem, suffix = dst.stem, dst.suffix
    counter = 1
    while True:
        candidate = dst.parent / f"{stem}_{counter}{suffix}"
        if candidate not in used and not candidate.exists():
            used.add(candidate)
            return candidate
        counter += 1


def safe_move(src: Path, dst: Path, dry_run: bool, used: set) -> None:
    dst = unique_dst(dst, used)
    if not src.exists():
        print(f"  SKIP: source missing: {src}")
        return
    if dry_run:
        print(f"  WOULD MOVE: {src} -> {dst}")
        return
    ensure_dir(dst.parent)
    shutil.move(str(src), str(dst))
    print(f"  MOVED: {src} -> {dst}")


def main():
    parser = argparse.ArgumentParser(description="Apply paper organization plan.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without moving files.")
    args = parser.parse_args()

    if not REPORT_CSV.exists():
        print(f"Report not found: {REPORT_CSV}")
        print("Run scripts/organize_papers.py first.")
        return

    with open(REPORT_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Applying organization for {len(rows)} entries (dry-run={args.dry_run})...\n")

    duplicates_dir = BASE_DIR / "duplicates"
    uncategorized_dir = BASE_DIR / "uncategorized"
    used = set()

    for r in rows:
        current_rel = Path(r["current_path"])
        src = RAW_DIR / current_rel

        if r["is_duplicate_of"]:
            dst = duplicates_dir / current_rel.name
            print(f"[DUPLICATE] {current_rel}")
            safe_move(src, dst, args.dry_run, used)
            continue

        topic = r["suggested_topic"]
        if topic == "uncategorized":
            proposed_name = Path(r["proposed_path"]).name
            dst = uncategorized_dir / proposed_name
            print(f"[UNCATEGORIZED] {current_rel}")
            safe_move(src, dst, args.dry_run, used)
            continue

        proposed_path = Path(r["proposed_path"])
        dst = BASE_DIR / proposed_path
        print(f"[{topic}] {current_rel}")
        safe_move(src, dst, args.dry_run, used)

    print("\nDone.")
    if args.dry_run:
        print("This was a dry run. No files were moved.")
    else:
        print("Files have been moved out of papers/raw/.")


if __name__ == "__main__":
    main()
