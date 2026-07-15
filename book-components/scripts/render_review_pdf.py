#!/usr/bin/env python3
"""Render selected review-PDF pages to PNGs with bundled Poppler."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from pypdf import PdfReader


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
DEFAULT_PDF = REPOSITORY_ROOT / "book" / "agentic-applications-2026-first-draft.pdf"
DEFAULT_OUTPUT = PROJECT_ROOT / "tmp" / "first-draft-rendered"
POPPLER = (
    Path.home()
    / ".cache"
    / "codex-runtimes"
    / "codex-primary-runtime"
    / "dependencies"
    / "bin"
    / "override"
    / "pdftoppm"
)


def page_spec(value: str, page_count: int) -> list[int]:
    if value.strip().lower() == "all":
        return list(range(1, page_count + 1))
    pages: set[int] = set()
    for item in value.split(","):
        item = item.strip()
        if not item:
            continue
        if "-" in item:
            start, end = (int(piece) for piece in item.split("-", 1))
            pages.update(range(start, end + 1))
        else:
            pages.add(int(item))
    invalid = [page for page in pages if page < 1 or page > page_count]
    if invalid:
        raise SystemExit(f"page numbers outside 1-{page_count}: {invalid}")
    return sorted(pages)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--pages", default="all", help="all, comma list, or ranges such as 1,4,8-10")
    parser.add_argument("--dpi", type=int, default=144)
    parser.add_argument("--clean", action="store_true", help="Remove existing page PNGs first")
    args = parser.parse_args()

    pdf = args.pdf.resolve()
    if not pdf.exists():
        raise SystemExit(f"PDF not found: {pdf}")
    if not POPPLER.exists():
        raise SystemExit(f"bundled pdftoppm not found: {POPPLER}")
    page_count = len(PdfReader(str(pdf)).pages)
    pages = page_spec(args.pages, page_count)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    if args.clean:
        for path in output.glob("page-*.png"):
            path.unlink()

    for page in pages:
        prefix = output / f"page-{page:03d}"
        subprocess.run(
            [
                str(POPPLER),
                "-f",
                str(page),
                "-l",
                str(page),
                "-r",
                str(args.dpi),
                "-png",
                "-singlefile",
                str(pdf),
                str(prefix),
            ],
            check=True,
            cwd=PROJECT_ROOT,
        )
    print(f"rendered {len(pages)} of {page_count} pages to {output}")


if __name__ == "__main__":
    main()
