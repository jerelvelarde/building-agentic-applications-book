#!/usr/bin/env python3
"""Validate the complete first-draft PDF and build visual-inspection contact sheets."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat
from pypdf import PdfReader


COMPONENT_ROOT = Path(__file__).resolve().parents[1]
ROOT = COMPONENT_ROOT.parent
PDF = ROOT / "book/agentic-applications-2026-first-draft.pdf"
RENDERED = COMPONENT_ROOT / "tmp/first-draft-rendered"
CONTACTS = COMPONENT_ROOT / "tmp/first-draft-contact-sheets"
REPORT = ROOT / "book/first-draft-validation.json"
BUILD_MANIFEST = ROOT / "book/build-manifest.json"

RESIDUE = re.compile(
    r"final edition|publication edition|review[- ]draft|partial draft|current review|figure unavailable|missing image|"
    r"pending figure|\bTODO\b|\bTBD\b|NEED RESEARCH|FIG-CH\d",
    re.I,
)
CODE_LABEL = re.compile(r"^(?:TYPESCRIPT|TSX|JAVASCRIPT|PYTHON|YAML|JSON|BASH|SHELL|TEXT|SQL)$", re.M)
FIGURE_LABEL = re.compile(r"\b(?:Figure|Evidence plate)\s+(?:\d+|[A-Z])", re.I)
TABLE_CUES = re.compile(r"\b(?:matrix|scorecard|checklist|decision table|control record|failure mode)\b", re.I)


def normalize_render_names(folder: Path, pages: int) -> list[Path]:
    folder.mkdir(parents=True, exist_ok=True)
    for path in sorted(folder.glob("rendered-*.png")):
        match = re.search(r"(\d+)$", path.stem)
        if match:
            path.replace(folder / f"page-{int(match.group(1)):03d}.png")
    result = [folder / f"page-{number:03d}.png" for number in range(1, pages + 1)]
    missing = [str(path.relative_to(ROOT)) for path in result if not path.exists()]
    if missing:
        raise SystemExit(f"missing rendered pages: {missing[:10]}")
    return result


def label_font(size: int = 22) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def contact_sheet(paths: list[Path], output: Path, columns: int, rows: int, cell: tuple[int, int]) -> None:
    margin, label_height = 18, 34
    sheet = Image.new(
        "RGB",
        (columns * cell[0] + (columns + 1) * margin, rows * (cell[1] + label_height) + (rows + 1) * margin),
        "#D9DDEA",
    )
    draw = ImageDraw.Draw(sheet)
    font = label_font(20)
    for index, path in enumerate(paths):
        row, column = divmod(index, columns)
        x = margin + column * (cell[0] + margin)
        y = margin + row * (cell[1] + label_height + margin)
        with Image.open(path) as source:
            image = source.convert("RGB")
            image.thumbnail(cell, Image.Resampling.LANCZOS)
        px = x + (cell[0] - image.width) // 2
        py = y + label_height + (cell[1] - image.height) // 2
        sheet.paste(image, (px, py))
        draw.text((x, y), path.stem.replace("page-", "Page "), fill="#11152B", font=font)
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, optimize=True)


def write_contact_sheets(pages: list[Path], selected: list[int]) -> dict[str, list[str]]:
    CONTACTS.mkdir(parents=True, exist_ok=True)
    for old in CONTACTS.glob("*.png"):
        old.unlink()
    overview: list[str] = []
    for index in range(0, len(pages), 20):
        path = CONTACTS / f"overview-{index // 20 + 1:02d}.png"
        contact_sheet(pages[index : index + 20], path, 4, 5, (250, 324))
        overview.append(str(path.relative_to(ROOT)))
    details: list[str] = []
    selected_paths = [pages[number - 1] for number in selected]
    for index in range(0, len(selected_paths), 4):
        path = CONTACTS / f"detail-{index // 4 + 1:03d}.png"
        contact_sheet(selected_paths[index : index + 4], path, 2, 2, (570, 738))
        details.append(str(path.relative_to(ROOT)))
    return {"overview": overview, "detail": details}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, default=PDF)
    parser.add_argument("--rendered", type=Path, default=RENDERED)
    args = parser.parse_args()
    pdf = args.pdf.resolve()
    reader = PdfReader(str(pdf))
    count = len(reader.pages)
    images = normalize_render_names(args.rendered.resolve(), count)
    texts = [(page.extract_text() or "") for page in reader.pages]

    blank_pages: list[int] = []
    tiny_or_oversized: list[dict[str, object]] = []
    residue: list[dict[str, object]] = []
    anomalies: list[dict[str, object]] = []
    duplicate_adjacent: list[list[int]] = []
    signatures: list[str] = []

    for number, (path, text) in enumerate(zip(images, texts), 1):
        size = path.stat().st_size
        if size < 10_000 or size > 8_000_000:
            tiny_or_oversized.append({"page": number, "png_bytes": size})
        with Image.open(path) as source:
            gray = source.convert("L").resize((96, 124), Image.Resampling.BILINEAR)
            stat = ImageStat.Stat(gray)
            extrema = gray.getextrema()
            signatures.append(hashlib.sha256(gray.tobytes()).hexdigest())
        if number != 1 and len(re.sub(r"\s+", "", text)) < 12 and stat.stddev[0] < 5 and extrema[0] > 245:
            blank_pages.append(number)
        for match in RESIDUE.finditer(text):
            residue.append({"page": number, "match": match.group(0)})
        for token in ("�", "\x00"):
            if token in text:
                anomalies.append({"page": number, "token": repr(token)})
        if number > 1 and signatures[-1] == signatures[-2]:
            duplicate_adjacent.append([number - 1, number])

    chapter_starts: dict[int, int] = {}
    for number, text in enumerate(texts, 1):
        for match in re.finditer(r"^CHAPTER\s+(\d{1,2})\s*$", text, re.M):
            chapter = int(match.group(1))
            if 1 <= chapter <= 26:
                chapter_starts.setdefault(chapter, number)
    chapter_ends: dict[int, int] = {}
    for chapter in range(1, 27):
        start = chapter_starts.get(chapter)
        if start is None:
            continue
        next_start = chapter_starts.get(chapter + 1, count + 1)
        chapter_ends[chapter] = next_start - 1

    part_openers = sorted(
        {
            number
            for number, text in enumerate(texts, 1)
            if re.search(r"\b(?:Level [123]|Production engineering|Field guide)\b", text, re.I)
            and len(text) < 1800
        }
    )
    figure_pages = [number for number, text in enumerate(texts, 1) if FIGURE_LABEL.search(text)]
    code_pages = [number for number, text in enumerate(texts, 1) if CODE_LABEL.search(text)]
    table_pages = [number for number, text in enumerate(texts, 1) if TABLE_CUES.search(text)]
    selected = sorted(
        {1, 2, count, *part_openers, *chapter_starts.values(), *chapter_ends.values(), *figure_pages, *code_pages, *table_pages}
    )
    contacts = write_contact_sheets(images, selected)

    findings = {
        "blank_pages": blank_pages,
        "tiny_or_oversized_pages": tiny_or_oversized,
        "missing_image_notices_or_editorial_residue": residue,
        "adjacent_duplicate_pages": duplicate_adjacent,
        "text_extraction_anomalies": anomalies,
    }
    report = {
        "pdf": str(pdf.relative_to(ROOT)),
        "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "pages": count,
        "rendered_pages": len(images),
        "chapter_starts": chapter_starts,
        "chapter_ends": chapter_ends,
        "part_opener_candidates": part_openers,
        "figure_pages": figure_pages,
        "code_pages": code_pages,
        "table_or_checklist_pages": table_pages,
        "detailed_visual_inspection_pages": selected,
        "contact_sheets": contacts,
        "findings": findings,
        "blocking_finding_count": sum(len(value) for value in findings.values()),
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if BUILD_MANIFEST.exists():
        manifest = json.loads(BUILD_MANIFEST.read_text(encoding="utf-8"))
        manifest["validation_report"] = str(REPORT.relative_to(ROOT))
        manifest["blocking_finding_count"] = report["blocking_finding_count"]
        manifest["qa"] = {
            "rendered_pages": report["rendered_pages"],
            "rendered_directory": str(args.rendered.resolve().relative_to(ROOT)),
            "contact_sheets": contacts,
            "detailed_visual_inspection_pages": selected,
        }
        BUILD_MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if report["blocking_finding_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
