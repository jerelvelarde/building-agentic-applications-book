#!/usr/bin/env python3
"""Count Markdown prose and code by section and compare chapter targets.

By default the script reads Markdown under ``sections/``. Until section files
exist, it falls back to the retained monolithic draft. Pass files or directories
explicitly to inspect keypoints or another manuscript slice.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


WORD_RE = re.compile(r"\b[\w]+(?:[’'-][\w]+)*\b", re.UNICODE)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
CHAPTER_HEADING_RE = re.compile(
    r"^(?:chapter\s+)?(\d{1,2})(?:\.|:|\s+[—-]|\s+)(?:\s*)(.+)$", re.I
)
TARGET_ROW_RE = re.compile(
    r"^\|\s*(\d{1,2})\s*\|.*?\|\s*([\d,]+)\s*\|\s*(\d+)\s*\|"
)


@dataclass
class SectionCount:
    file: Path
    heading: str
    level: int
    chapter: int | None
    prose_words: int = 0
    code_words: int = 0


def strip_frontmatter(lines: list[str]) -> list[str]:
    if not lines or lines[0].strip() != "---":
        return lines
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[index + 1 :]
    return lines


def chapter_from_path(path: Path) -> int | None:
    matches = [re.match(r"^(\d{2})-", part) for part in path.parts]
    chapters = [int(match.group(1)) for match in matches if match]
    return chapters[-1] if chapters else None


def chapter_from_heading(heading: str) -> int | None:
    match = CHAPTER_HEADING_RE.match(heading.strip())
    if not match:
        return None
    chapter = int(match.group(1))
    return chapter if 1 <= chapter <= 99 else None


def clean_prose(line: str) -> tuple[str, str]:
    """Return prose text and extracted inline-code text."""
    inline: list[str] = []

    def take_inline(match: re.Match[str]) -> str:
        inline.append(match.group(1))
        return " "

    line = re.sub(r"`([^`]+)`", take_inline, line)
    line = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"\1", line)
    line = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", line)
    line = re.sub(r"<https?://[^>]+>", " ", line)
    line = re.sub(r"<!--.*?-->", " ", line)
    line = re.sub(r"^\s*(?:[-+*]|\d+[.)])\s+", "", line)
    line = re.sub(r"[*_~>#|]", " ", line)
    return line, " ".join(inline)


def parse_markdown(path: Path, root: Path) -> list[SectionCount]:
    lines = strip_frontmatter(path.read_text(encoding="utf-8").splitlines())
    path_chapter = chapter_from_path(path.relative_to(root))
    sections: list[SectionCount] = []
    current = SectionCount(path, "(preamble)", 0, path_chapter)
    sections.append(current)
    in_fence = False
    fence_marker = ""
    in_comment = False

    for raw in lines:
        line = raw
        if in_comment:
            if "-->" in line:
                line = line.split("-->", 1)[1]
                in_comment = False
            else:
                continue
        if "<!--" in line:
            before, after = line.split("<!--", 1)
            line = before
            if "-->" not in after:
                in_comment = True

        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            continue

        if in_fence:
            current.code_words += len(WORD_RE.findall(line))
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            heading = heading_match.group(2).strip()
            detected = chapter_from_heading(heading)
            chapter = detected if detected is not None else path_chapter
            current = SectionCount(path, heading, len(heading_match.group(1)), chapter)
            sections.append(current)
            continue

        prose, inline_code = clean_prose(line)
        current.prose_words += len(WORD_RE.findall(prose))
        current.code_words += len(WORD_RE.findall(inline_code))

    return [section for section in sections if section.prose_words or section.code_words]


def load_targets(path: Path) -> dict[int, tuple[int, int]]:
    targets: dict[int, tuple[int, int]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = TARGET_ROW_RE.match(line)
        if match:
            targets[int(match.group(1))] = (
                int(match.group(2).replace(",", "")),
                int(match.group(3)),
            )
    if len(targets) != 26:
        raise ValueError(f"Expected 26 chapter targets in {path}, found {len(targets)}")
    return targets


def collect_markdown(inputs: list[Path]) -> list[Path]:
    files: set[Path] = set()
    for item in inputs:
        if item.is_dir():
            files.update(path for path in item.rglob("*.md") if path.name != "README.md")
        elif item.suffix.lower() == ".md" and item.exists():
            files.add(item)
    return sorted(files)


def default_inputs(root: Path) -> list[Path]:
    section_dir = root / "sections"
    section_files = collect_markdown([section_dir]) if section_dir.exists() else []
    if section_files:
        return section_files
    draft = root / "The Builder's Guide to Agentic Applications 2026 — Draft.md"
    return [draft] if draft.exists() else []


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="*", help="Markdown files or directories")
    parser.add_argument("--strict", action="store_true", help="Fail on missing/out-of-range chapters")
    parser.add_argument("--tolerance", type=float, default=12.0, help="Allowed target variance percent")
    parser.add_argument("--summary-only", action="store_true", help="Hide per-section counts")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    requested = [Path(value).resolve() for value in args.inputs]
    files = collect_markdown(requested) if requested else default_inputs(root)
    if not files:
        print("No Markdown manuscript files found.", file=sys.stderr)
        return 2

    targets = load_targets(root / "docs" / "page-allocation.md")
    sections = [section for path in files for section in parse_markdown(path, root)]

    if not args.summary_only:
        print("SECTION COUNTS")
        print("prose  code  chapter  section")
        for section in sections:
            chapter = str(section.chapter) if section.chapter is not None else "-"
            print(
                f"{section.prose_words:5d} {section.code_words:5d} "
                f"{chapter:>7}  {relative(section.file, root)} :: {section.heading}"
            )

    chapter_prose = {chapter: 0 for chapter in targets}
    chapter_code = {chapter: 0 for chapter in targets}
    for section in sections:
        if section.chapter in targets:
            chapter_prose[section.chapter] += section.prose_words
            chapter_code[section.chapter] += section.code_words

    failures = 0
    print("\nCHAPTER TARGET VALIDATION")
    print("ch  prose  code  target  pages  delta      status")
    for chapter, (target_words, target_pages) in targets.items():
        actual = chapter_prose[chapter]
        code = chapter_code[chapter]
        if actual == 0:
            status = "MISSING"
            delta = -100.0
        else:
            delta = ((actual - target_words) / target_words) * 100
            status = "OK" if abs(delta) <= args.tolerance else ("UNDER" if delta < 0 else "OVER")
        if status != "OK":
            failures += 1
        print(
            f"{chapter:2d} {actual:6d} {code:5d} {target_words:7d} "
            f"{target_pages:6d} {delta:+7.1f}%  {status}"
        )

    total_prose = sum(section.prose_words for section in sections)
    total_code = sum(section.code_words for section in sections)
    print(
        f"\nTOTAL: {total_prose:,} prose words, {total_code:,} code words, "
        f"{len(files)} file(s), {failures} chapter target warning(s)."
    )
    if not requested and not (root / "sections").exists():
        print("NOTE: sections/ is absent; counted the retained monolithic draft.")
    return 1 if args.strict and failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
