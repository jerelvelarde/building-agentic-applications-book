#!/usr/bin/env python3
"""Build the local review PDF for The Builder's Guide to Agentic Applications.

The compiler intentionally uses only manuscript files, local assets, and the
Codex bundled document runtime. It is a review compiler rather than a
publisher-specific typesetter: source Markdown remains the editorial source of
truth, while this script provides a deterministic, inspectable reading copy.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from reportlab import rl_config

# Stable object ordering and timestamps make unchanged local inputs reproducible.
rl_config.invariant = 1

from PIL import Image as PILImage
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Flowable,
    Frame,
    HRFlowable,
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    LongTable,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.xpreformatted import XPreformatted


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
SECTION_ROOT = PROJECT_ROOT / "sections"
IMAGE_ROOT = PROJECT_ROOT / "images"
OUTPUT_PDF = REPOSITORY_ROOT / "book" / "agentic-applications-2026-first-draft.pdf"
MANIFEST_PATH = REPOSITORY_ROOT / "book" / "build-manifest.json"
TEMP_ROOT = PROJECT_ROOT / "tmp" / "pdfs"
PUBLICATION_MODE = False

RUNTIME_ROOT = Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies"
RUNTIME_PYTHON = RUNTIME_ROOT / "python" / "bin" / "python3"
RUNTIME_NODE = RUNTIME_ROOT / "node" / "bin" / "node"
RUNTIME_SHARP = RUNTIME_ROOT / "node" / "node_modules" / "sharp"
RUNTIME_FONT_ROOT = (
    RUNTIME_ROOT
    / "native"
    / "libreoffice-headless"
    / "libreoffice"
    / "LibreOfficeDev.app"
    / "Contents"
    / "Resources"
    / "fonts"
    / "truetype"
)

PAGE_WIDTH, PAGE_HEIGHT = LETTER
LEFT_MARGIN = 0.72 * inch
RIGHT_MARGIN = 0.72 * inch
TOP_MARGIN = 0.78 * inch
BOTTOM_MARGIN = 0.70 * inch
CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN

NAVY = colors.HexColor("#11143D")
INK = colors.HexColor("#20233B")
MUTED = colors.HexColor("#57575B")
LILAC = colors.HexColor("#BEC2FF")
PURPLE = colors.HexColor("#6A5AE0")
MINT = colors.HexColor("#85ECCE")
MINT_DARK = colors.HexColor("#14795F")
PALE_LILAC = colors.HexColor("#F3F1FC")
PALE_MINT = colors.HexColor("#ECFBF6")
PAPER = colors.HexColor("#FAFAFC")
BORDER = colors.HexColor("#DBDBE5")
CODE_BG = colors.HexColor("#11142F")
CODE_TEXT = colors.HexColor("#E8EAFE")
CODE_MUTED = colors.HexColor("#AEB5D9")
WHITE = colors.white


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def normalize_text(value: str) -> str:
    """Normalize dash glyphs that frequently fail in print pipelines."""

    return value.translate(
        str.maketrans(
            {
                "\u2010": "-",
                "\u2011": "-",
                "\u2012": "-",
                "\u2013": "-",
                "\u2014": "-",
                "\u2212": "-",
                "\u00a0": " ",
            }
        )
    )


def font_path(filename: str) -> Path:
    path = RUNTIME_FONT_ROOT / filename
    if not path.exists():
        fail(f"bundled font not found: {path}")
    return path


def register_fonts() -> None:
    font_files = {
        "BookSans": "DejaVuSans.ttf",
        "BookSans-Bold": "DejaVuSans-Bold.ttf",
        "BookSans-Italic": "DejaVuSans-Oblique.ttf",
        "BookSans-BoldItalic": "DejaVuSans-BoldOblique.ttf",
        "BookMono": "DejaVuSansMono.ttf",
        "BookMono-Bold": "DejaVuSansMono-Bold.ttf",
    }
    for name, filename in font_files.items():
        pdfmetrics.registerFont(TTFont(name, str(font_path(filename))))
    pdfmetrics.registerFontFamily(
        "BookSans",
        normal="BookSans",
        bold="BookSans-Bold",
        italic="BookSans-Italic",
        boldItalic="BookSans-BoldItalic",
    )
    pdfmetrics.registerFontFamily(
        "BookMono",
        normal="BookMono",
        bold="BookMono-Bold",
        italic="BookMono",
        boldItalic="BookMono-Bold",
    )


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="BookSans",
            fontSize=10.15,
            leading=15.2,
            textColor=INK,
            spaceAfter=8.5,
            splitLongWords=True,
            allowWidows=0,
            allowOrphans=0,
        ),
        "lead": ParagraphStyle(
            "Lead",
            fontName="BookSans",
            fontSize=12.2,
            leading=18.2,
            textColor=NAVY,
            spaceAfter=16,
        ),
        "h1": ParagraphStyle(
            "Heading1",
            fontName="BookSans-Bold",
            fontSize=24,
            leading=29,
            textColor=NAVY,
            spaceBefore=10,
            spaceAfter=14,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "Heading2",
            fontName="BookSans-Bold",
            fontSize=16.5,
            leading=21,
            textColor=NAVY,
            spaceBefore=18,
            spaceAfter=8,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "Heading3",
            fontName="BookSans-Bold",
            fontSize=12.7,
            leading=16.5,
            textColor=PURPLE,
            spaceBefore=14,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "h4": ParagraphStyle(
            "Heading4",
            fontName="BookSans-Bold",
            fontSize=10.4,
            leading=14,
            textColor=MINT_DARK,
            spaceBefore=10,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "list": ParagraphStyle(
            "ListBody",
            fontName="BookSans",
            fontSize=9.8,
            leading=14.4,
            textColor=INK,
            leftIndent=0,
            spaceAfter=2.5,
        ),
        "quote": ParagraphStyle(
            "Quote",
            fontName="BookSans-Italic",
            fontSize=11,
            leading=16,
            textColor=NAVY,
            spaceAfter=0,
        ),
        "callout": ParagraphStyle(
            "Callout",
            fontName="BookSans",
            fontSize=9.4,
            leading=14.2,
            textColor=INK,
        ),
        "callout_label": ParagraphStyle(
            "CalloutLabel",
            fontName="BookSans-Bold",
            fontSize=8.1,
            leading=10,
            textColor=PURPLE,
            spaceAfter=4,
        ),
        "caption": ParagraphStyle(
            "Caption",
            fontName="BookSans",
            fontSize=8.2,
            leading=11.4,
            textColor=MUTED,
            spaceBefore=5,
            spaceAfter=13,
        ),
        "editorial": ParagraphStyle(
            "EditorialStatus",
            fontName="BookMono",
            fontSize=7.1,
            leading=10,
            textColor=MUTED,
        ),
        "table_header": ParagraphStyle(
            "TableHeader",
            fontName="BookSans-Bold",
            fontSize=7.8,
            leading=10.5,
            textColor=WHITE,
        ),
        "table_cell": ParagraphStyle(
            "TableCell",
            fontName="BookSans",
            fontSize=7.7,
            leading=10.8,
            textColor=INK,
            splitLongWords=True,
        ),
        "code": ParagraphStyle(
            "Code",
            fontName="BookMono",
            fontSize=7.15,
            leading=9.65,
            textColor=CODE_TEXT,
            leftIndent=0,
            rightIndent=0,
        ),
        "code_label": ParagraphStyle(
            "CodeLabel",
            fontName="BookMono-Bold",
            fontSize=6.7,
            leading=8.5,
            textColor=MINT,
        ),
        "title": ParagraphStyle(
            "BookTitle",
            fontName="BookSans-Bold",
            fontSize=34,
            leading=38,
            textColor=NAVY,
            alignment=TA_LEFT,
            spaceAfter=16,
        ),
        "subtitle": ParagraphStyle(
            "BookSubtitle",
            fontName="BookSans",
            fontSize=16,
            leading=22,
            textColor=PURPLE,
            alignment=TA_LEFT,
            spaceAfter=25,
        ),
        "small": ParagraphStyle(
            "Small",
            fontName="BookSans",
            fontSize=8.2,
            leading=12.2,
            textColor=MUTED,
        ),
        "toc_title": ParagraphStyle(
            "TOCTitle",
            fontName="BookSans-Bold",
            fontSize=26,
            leading=31,
            textColor=NAVY,
            spaceAfter=18,
        ),
        "footnote": ParagraphStyle(
            "Footnote",
            fontName="BookSans",
            fontSize=7.6,
            leading=10.5,
            textColor=MUTED,
            leftIndent=12,
            firstLineIndent=-12,
            spaceAfter=4,
        ),
    }


STYLES: dict[str, ParagraphStyle]


def strip_front_matter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    metadata: dict[str, str] = {}
    if not lines or lines[0].strip() != "---":
        return metadata, text
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return metadata, text
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("\"'")
    return metadata, "\n".join(lines[end + 1 :]).lstrip()


def prepare_front_matter(text: str) -> tuple[dict[str, str], str]:
    metadata, body = strip_front_matter(text)
    lines = body.splitlines()
    promise = next(
        (i for i, line in enumerate(lines) if line.startswith("## The promise of this book")),
        0,
    )
    contents = next(
        (i for i, line in enumerate(lines) if line.startswith("## Contents")),
        len(lines),
    )
    first_part = next(
        (i for i, line in enumerate(lines) if re.match(r"^# Part\s+[IVX]+", line)),
        len(lines),
    )
    selected = lines[promise:contents]
    if first_part < len(lines):
        selected += [""] + lines[first_part:]
    selected = [
        line
        for line in selected
        if not line.startswith("## Introduction")
    ]
    return metadata, "\n".join(selected).strip()


def discover_sections() -> list[Path]:
    if not SECTION_ROOT.exists():
        fail(f"section directory not found: {SECTION_ROOT}")
    paths = sorted(SECTION_ROOT.rglob("*.md"), key=lambda p: p.relative_to(SECTION_ROOT).as_posix())
    if not paths:
        fail("no section Markdown files found")
    front = SECTION_ROOT / "00-front-matter.md"
    if front in paths:
        paths.remove(front)
        paths.insert(0, front)
    return paths


def chapter_info(paths: Sequence[Path]) -> list[tuple[int, str, Path]]:
    chapters: list[tuple[int, str, Path]] = []
    for path in paths:
        metadata, _ = strip_front_matter(path.read_text(encoding="utf-8"))
        if not metadata.get("chapter", "").isdigit():
            continue
        chapters.append((int(metadata["chapter"]), metadata.get("title", path.stem), path))
    return sorted(chapters)


def inline_markup(text: str) -> str:
    text = normalize_text(text.strip())
    tokens: list[str] = []

    def protect(value: str) -> str:
        key = f"ZZTOKEN{len(tokens)}ZZ"
        tokens.append(value)
        return key

    # Code spans are protected before general escaping/formatting.
    text = re.sub(
        r"`([^`]+)`",
        lambda m: protect(
            f'<font name="BookMono" size="8.5" color="#11143D" backColor="#EDEDF5">'
            f"{html.escape(normalize_text(m.group(1)))}"
            "</font>"
        ),
        text,
    )

    def link_repl(match: re.Match[str]) -> str:
        label = html.escape(normalize_text(match.group(1)))
        url = html.escape(match.group(2), quote=True)
        return protect(f'<link href="{url}" color="#5B4FD1"><u>{label}</u></link>')

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_repl, text)
    text = re.sub(
        r"\[\^([^\]]+)\]",
        lambda m: protect(
            f'<super><link href="#fn-{html.escape(m.group(1))}" color="#5B4FD1">'
            f"{html.escape(m.group(1))}</link></super>"
        ),
        text,
    )
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"<i>\1</i>", text)
    for index, value in enumerate(tokens):
        text = text.replace(f"ZZTOKEN{index}ZZ", value)
    return text


class CoverPage(Flowable):
    def __init__(self, image_path: Path):
        super().__init__()
        self.image_path = image_path
        self.width = PAGE_WIDTH
        self.height = PAGE_HEIGHT

    def wrap(self, avail_width: float, avail_height: float) -> tuple[float, float]:
        return avail_width, avail_height

    def draw(self) -> None:
        with PILImage.open(self.image_path) as image:
            image_width, image_height = image.size
        scale = min(PAGE_WIDTH / image_width, PAGE_HEIGHT / image_height)
        width = image_width * scale
        height = image_height * scale
        x = (PAGE_WIDTH - width) / 2
        y = (PAGE_HEIGHT - height) / 2
        self.canv.setFillColor(WHITE)
        self.canv.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        self.canv.drawImage(
            str(self.image_path),
            x,
            y,
            width,
            height,
            preserveAspectRatio=True,
            anchor="c",
            mask="auto",
        )


class OpeningHeading(Flowable):
    toc_level = 0

    def __init__(self, eyebrow: str, title: str, subtitle: str = "", *, kind: str = "front"):
        super().__init__()
        self.eyebrow = normalize_text(eyebrow)
        self.title = normalize_text(title)
        self.subtitle = normalize_text(subtitle)
        self.kind = kind
        self.toc_text = self.title if not subtitle else f"{self.title}: {self.subtitle}"
        self.width = CONTENT_WIDTH
        self.height = 6.05 * inch if kind == "part" else 1.9 * inch

    def wrap(self, avail_width: float, avail_height: float) -> tuple[float, float]:
        self.width = avail_width
        return avail_width, min(self.height, avail_height)

    def draw(self) -> None:
        canvas = self.canv
        if self.kind == "part":
            canvas.setFillColor(NAVY)
            canvas.roundRect(0, 0, self.width, self.height, 24, fill=1, stroke=0)
            canvas.setFillColor(LILAC)
            canvas.setFillAlpha(0.22)
            canvas.circle(self.width - 20, self.height - 30, 125, fill=1, stroke=0)
            canvas.setFillColor(MINT)
            canvas.setFillAlpha(0.18)
            canvas.circle(25, 20, 115, fill=1, stroke=0)
            canvas.setFillAlpha(1)
            canvas.setFont("BookMono-Bold", 9)
            canvas.setFillColor(MINT)
            canvas.drawString(34, self.height - 62, self.eyebrow.upper())
            title = Paragraph(
                inline_markup(self.title),
                ParagraphStyle(
                    "PartTitle",
                    fontName="BookSans-Bold",
                    fontSize=30,
                    leading=36,
                    textColor=WHITE,
                ),
            )
            _, title_height = title.wrap(self.width - 68, 180)
            title.drawOn(canvas, 34, self.height - 105 - title_height)
            if self.subtitle:
                subtitle = Paragraph(
                    inline_markup(self.subtitle),
                    ParagraphStyle(
                        "PartSubtitle",
                        fontName="BookSans",
                        fontSize=12,
                        leading=18,
                        textColor=colors.HexColor("#E5E7FF"),
                    ),
                )
                _, subtitle_height = subtitle.wrap(self.width - 68, 120)
                subtitle.drawOn(canvas, 34, 46 + subtitle_height)
            canvas.setStrokeColor(MINT)
            canvas.setLineWidth(3)
            canvas.line(34, 34, self.width * 0.38, 34)
            canvas.setStrokeColor(LILAC)
            canvas.line(self.width * 0.38, 34, self.width - 34, 34)
            return

        canvas.setFont("BookMono-Bold", 8.5)
        canvas.setFillColor(PURPLE)
        canvas.drawString(0, self.height - 18, self.eyebrow.upper())
        title = Paragraph(
            inline_markup(self.title),
            ParagraphStyle(
                "OpeningTitle",
                fontName="BookSans-Bold",
                fontSize=27,
                leading=32,
                textColor=NAVY,
            ),
        )
        _, title_height = title.wrap(self.width, 100)
        title.drawOn(canvas, 0, self.height - 34 - title_height)
        if self.subtitle:
            subtitle = Paragraph(
                inline_markup(self.subtitle),
                ParagraphStyle(
                    "OpeningSubtitle",
                    fontName="BookSans",
                    fontSize=13,
                    leading=18,
                    textColor=MUTED,
                ),
            )
            _, sub_height = subtitle.wrap(self.width, 70)
            subtitle.drawOn(canvas, 0, self.height - 46 - title_height - sub_height)
        canvas.setStrokeColor(MINT)
        canvas.setLineWidth(3)
        canvas.line(0, 7, self.width * 0.38, 7)
        canvas.setStrokeColor(LILAC)
        canvas.line(self.width * 0.38, 7, self.width, 7)


class ChapterHeading(OpeningHeading):
    toc_level = 1

    def __init__(self, number: int, title: str):
        super().__init__(f"Chapter {number}", title, kind="chapter")
        self.number = number
        self.toc_text = f"{number}. {normalize_text(title)}"
        self.height = 1.72 * inch


class BookDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs):
        super().__init__(filename, **kwargs)
        self.current_chapter = "The Builder's Guide to Agentic Applications"

    def beforeDocument(self) -> None:  # noqa: N802 - ReportLab API
        # multiBuild runs the same document more than once to resolve the TOC.
        # Reset running-header state so the final pass never inherits the last
        # chapter title from the preceding pass.
        self.current_chapter = "The Builder's Guide to Agentic Applications"

    def afterFlowable(self, flowable: Flowable) -> None:  # noqa: N802 - ReportLab API
        if not hasattr(flowable, "toc_level"):
            return
        level = int(getattr(flowable, "toc_level"))
        text = str(getattr(flowable, "toc_text"))
        key = getattr(flowable, "bookmark_key", "")
        if not key:
            digest = hashlib.sha1(f"{level}:{text}".encode("utf-8")).hexdigest()[:12]
            key = f"section-{digest}"
            setattr(flowable, "bookmark_key", key)
        self.canv.bookmarkPage(key)
        self.canv.addOutlineEntry(text, key, level=level, closed=False)
        display_page = max(1, self.page - 1)
        self.notify("TOCEntry", (level, text, display_page, key))
        if isinstance(flowable, ChapterHeading):
            self.current_chapter = flowable.toc_text
        elif isinstance(flowable, OpeningHeading) and flowable.kind == "part":
            self.current_chapter = flowable.title


def draw_footer(canvas, doc) -> None:
    page_number = canvas.getPageNumber() - 1
    if page_number < 1:
        return
    canvas.saveState()
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.45)
    canvas.line(LEFT_MARGIN, 0.50 * inch, PAGE_WIDTH - RIGHT_MARGIN, 0.50 * inch)
    canvas.setFont("BookMono-Bold", 7)
    canvas.setFillColor(PURPLE)
    canvas.drawCentredString(PAGE_WIDTH / 2, 0.30 * inch, str(page_number))
    canvas.restoreState()


def draw_body_page(canvas, doc) -> None:
    draw_footer(canvas, doc)
    canvas.saveState()
    canvas.setFont("BookSans", 7.2)
    canvas.setFillColor(MUTED)
    header = normalize_text(getattr(doc, "current_chapter", ""))
    if len(header) > 72:
        header = header[:69] + "..."
    canvas.drawString(LEFT_MARGIN, PAGE_HEIGHT - 0.42 * inch, header)
    canvas.setFont("BookMono-Bold", 6.8)
    canvas.setFillColor(PURPLE)
    edition_label = "2026 FIRST DRAFT" if PUBLICATION_MODE else "2026 REVIEW EDITION"
    canvas.drawRightString(PAGE_WIDTH - RIGHT_MARGIN, PAGE_HEIGHT - 0.42 * inch, edition_label)
    mid = PAGE_WIDTH / 2
    y = PAGE_HEIGHT - 0.52 * inch
    canvas.setLineWidth(1.6)
    canvas.setStrokeColor(MINT)
    canvas.line(LEFT_MARGIN, y, mid, y)
    canvas.setStrokeColor(LILAC)
    canvas.line(mid, y, PAGE_WIDTH - RIGHT_MARGIN, y)
    canvas.restoreState()


def draw_opening_page(canvas, doc) -> None:
    draw_footer(canvas, doc)


def paragraph(text: str, style: str = "body") -> Paragraph:
    return Paragraph(inline_markup(text), STYLES[style])


def quote_box(text: str) -> Table:
    quote = Paragraph(inline_markup(text), STYLES["quote"])
    table = Table([[quote]], colWidths=[CONTENT_WIDTH], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE_LILAC),
                ("BOX", (0, 0), (-1, -1), 0.6, LILAC),
                ("LINEBEFORE", (0, 0), (0, -1), 4, PURPLE),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                ("TOPPADDING", (0, 0), (-1, -1), 11),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
            ]
        )
    )
    return table


CALLOUT_LABELS = {
    "builder decision": ("BUILDER DECISION", PALE_MINT, MINT_DARK),
    "boundary check": ("BOUNDARY CHECK", PALE_LILAC, PURPLE),
    "failure mode": ("FAILURE MODE", colors.HexColor("#FFF4F1"), colors.HexColor("#A34132")),
    "version note": ("VERSION NOTE", colors.HexColor("#F3F4F8"), MUTED),
    "production gate": ("PRODUCTION GATE", PALE_MINT, MINT_DARK),
    "in the wild": ("IN THE WILD", PALE_LILAC, PURPLE),
    "reader outcome": ("READER OUTCOME", PALE_MINT, MINT_DARK),
}


def callout_box(text: str) -> Table:
    plain = re.sub(r"\*\*", "", text).strip()
    label_key = next((key for key in CALLOUT_LABELS if plain.lower().startswith(key)), "")
    if not label_key:
        return quote_box(plain)
    label, background, accent = CALLOUT_LABELS[label_key]
    body = plain[len(label_key) :].lstrip(" .:-")
    content = [
        Paragraph(label, STYLES["callout_label"]),
        Paragraph(inline_markup(body), STYLES["callout"]),
    ]
    table = Table([[content]], colWidths=[CONTENT_WIDTH], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), background),
                ("BOX", (0, 0), (-1, -1), 0.55, accent),
                ("LINEBEFORE", (0, 0), (0, -1), 4, accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 13),
                ("RIGHTPADDING", (0, 0), (-1, -1), 13),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return table


def code_blocks(code: str, language: str) -> list[Flowable]:
    language = normalize_text(language.strip() or "text")
    raw_lines = normalize_text(code.rstrip()).replace("\t", "    ").splitlines() or [""]
    lines: list[str] = []
    for raw_line in raw_lines:
        remaining = raw_line
        while len(remaining) > 96:
            split_at = remaining.rfind(" ", 68, 96)
            if split_at < 0:
                split_at = 96
            lines.append(remaining[:split_at].rstrip() + "  \\")
            remaining = "    " + remaining[split_at:].lstrip()
        lines.append(remaining)
    chunks = [lines[i : i + 32] for i in range(0, len(lines), 32)]
    result: list[Flowable] = []
    for index, chunk in enumerate(chunks):
        label = language.upper()
        if len(chunks) > 1 and index:
            label += "  /  CONTINUED"
        label_para = Paragraph(html.escape(label), STYLES["code_label"])
        escaped = html.escape("\n".join(chunk))
        pre = XPreformatted(escaped, STYLES["code"])
        table = Table([[label_para], [pre]], colWidths=[CONTENT_WIDTH], hAlign="LEFT")
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
                    ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#34385F")),
                    ("LINEBELOW", (0, 0), (-1, 0), 0.4, colors.HexColor("#34385F")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 11),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 11),
                    ("TOPPADDING", (0, 0), (-1, 0), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
                    ("TOPPADDING", (0, 1), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 1), (-1, -1), 9),
                ]
            )
        )
        result.extend([Spacer(1, 4), KeepTogether([table]), Spacer(1, 10)])
    return result


def parse_table(lines: Sequence[str]) -> LongTable:
    raw_rows: list[list[str]] = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        raw_rows.append(cells)
    if len(raw_rows) >= 2 and all(re.fullmatch(r":?-{3,}:?", cell) for cell in raw_rows[1]):
        raw_rows.pop(1)
    column_count = max(len(row) for row in raw_rows)
    rows: list[list[Paragraph]] = []
    for row_index, row in enumerate(raw_rows):
        row += [""] * (column_count - len(row))
        style = "table_header" if row_index == 0 else "table_cell"
        rows.append([Paragraph(inline_markup(cell), STYLES[style]) for cell in row])

    max_lengths = []
    for column in range(column_count):
        max_lengths.append(max(8, min(48, max(len(row[column]) for row in raw_rows))))
    total = sum(max_lengths)
    widths = [CONTENT_WIDTH * length / total for length in max_lengths]
    minimum = 0.78 * inch if column_count <= 5 else 0.52 * inch
    widths = [max(minimum, width) for width in widths]
    scale = CONTENT_WIDTH / sum(widths)
    widths = [width * scale for width in widths]

    table = LongTable(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.35, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    for row_index in range(1, len(rows)):
        if row_index % 2 == 0:
            commands.append(("BACKGROUND", (0, row_index), (-1, row_index), colors.HexColor("#F7F7FB")))
    table.setStyle(TableStyle(commands))
    return table


def rasterize_svg(path: Path) -> Path:
    if not RUNTIME_NODE.exists() or not RUNTIME_SHARP.exists():
        fail(
            "SVG rendering requires the bundled Node + sharp runtime at "
            f"{RUNTIME_ROOT}. See book-components/README.md."
        )
    cache = TEMP_ROOT / "diagram-cache"
    cache.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    output = cache / f"{path.stem}-{digest}.png"
    if output.exists():
        return output
    script = (
        "const sharp=require(process.argv[1]);"
        "sharp(process.argv[2],{density:192}).resize({width:1800,withoutEnlargement:false})"
        ".png().toFile(process.argv[3]).catch(e=>{console.error(e);process.exit(1)})"
    )
    subprocess.run(
        [str(RUNTIME_NODE), "-e", script, str(RUNTIME_SHARP), str(path), str(output)],
        check=True,
        cwd=PROJECT_ROOT,
    )
    return output


def find_figure_asset(figure_number: str) -> Path | None:
    match = re.fullmatch(r"(\d+)\.(\d+)", figure_number)
    if not match:
        return None
    chapter, figure = (int(match.group(1)), int(match.group(2)))
    prefix = f"fig-ch{chapter:02d}-{figure:02d}-"
    matches = sorted((IMAGE_ROOT / "diagrams").glob(prefix + "*"))
    if not matches:
        matches = sorted(IMAGE_ROOT.rglob(prefix + "*"))
    return matches[0] if matches else None


def image_flowables(path: Path, caption: str, status: str = "") -> list[Flowable]:
    image_path = rasterize_svg(path) if path.suffix.lower() == ".svg" else path
    with PILImage.open(image_path) as image:
        pixel_width, pixel_height = image.size
    width = CONTENT_WIDTH
    height = width * pixel_height / pixel_width
    if height > 4.65 * inch:
        height = 4.65 * inch
        width = height * pixel_width / pixel_height
    picture = Image(str(image_path), width=width, height=height)
    picture.hAlign = "CENTER"
    frame = Table([[picture]], colWidths=[CONTENT_WIDTH], hAlign="LEFT")
    frame.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PAPER),
                ("BOX", (0, 0), (-1, -1), 0.55, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    caption_items = [Paragraph(inline_markup(caption), STYLES["caption"])]
    if status:
        caption_items.append(Paragraph(inline_markup(status), STYLES["editorial"]))
    return [Spacer(1, 7), frame, *caption_items, Spacer(1, 4)]


def figure_flowables(text: str) -> list[Flowable] | None:
    lines = [re.sub(r"^>\s?", "", line).strip() for line in text.splitlines()]
    joined = normalize_text(" ".join(line for line in lines if line))
    canonical = re.search(
        r"\*\*FIG-CH(\d{1,2})-(\d{1,2})\s*[-–—:]\s*(.+?)\*\*",
        joined,
        re.IGNORECASE,
    )
    legacy = re.search(
        r"\*\*Figure\s+(\d+)\.(\d+)\s*[-–—:]\s*(.+?)\*\*",
        joined,
        re.IGNORECASE,
    )
    match = canonical or legacy
    if not match:
        return None
    chapter, ordinal, raw_title = match.groups()
    number = f"{int(chapter)}.{int(ordinal)}"
    title = normalize_text(raw_title)
    status_match = re.search(r"Capture status:\s*(.+)$", joined, re.IGNORECASE)
    status = normalize_text(status_match.group(1)) if status_match else ""
    caption = f"Figure {number} - {title}"
    asset = find_figure_asset(number)
    if asset:
        return image_flowables(asset, caption, "Original editorial diagram embedded from the local SVG source.")
    pending = status or "Visual pending a source-pinned runtime capture."
    content = [
        Paragraph("FIGURE PENDING", STYLES["callout_label"]),
        Paragraph(inline_markup(caption), STYLES["callout"]),
        Spacer(1, 4),
        Paragraph(inline_markup(pending), STYLES["editorial"]),
    ]
    table = Table([[content]], colWidths=[CONTENT_WIDTH], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F6F6FA")),
                ("BOX", (0, 0), (-1, -1), 0.55, BORDER),
                ("LINEBEFORE", (0, 0), (0, -1), 4, LILAC),
                ("LEFTPADDING", (0, 0), (-1, -1), 13),
                ("RIGHTPADDING", (0, 0), (-1, -1), 13),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return [Spacer(1, 6), table, Spacer(1, 10)]


def markdown_image_flowables(line: str, source_path: Path) -> list[Flowable] | None:
    match = re.fullmatch(r"!\[([^]]*)\]\(([^)]+)\)", line.strip())
    if not match:
        return None
    alt, raw_path = match.groups()
    candidate = (source_path.parent / raw_path).resolve()
    if not candidate.exists():
        candidate = (PROJECT_ROOT / raw_path).resolve()
    if not candidate.exists():
        return [callout_box(f"Failure mode - Missing local image: {raw_path}"), Spacer(1, 8)]
    return image_flowables(candidate, alt or candidate.stem)


def parse_markdown(text: str, source_path: Path) -> list[Flowable]:
    _, body = strip_front_matter(text)
    lines = body.splitlines()
    story: list[Flowable] = []
    footnotes: list[tuple[str, str]] = []
    index = 0

    while index < len(lines):
        line = lines[index].rstrip()
        stripped = line.strip()
        if not stripped:
            index += 1
            continue

        footnote = re.match(r"^\[\^([^]]+)\]:\s*(.*)$", stripped)
        if footnote:
            footnotes.append((footnote.group(1), footnote.group(2)))
            index += 1
            continue

        if stripped.startswith("```"):
            language = stripped[3:].strip()
            index += 1
            block: list[str] = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                block.append(lines[index])
                index += 1
            index += 1
            story.extend(code_blocks("\n".join(block), language))
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            level, title = len(heading.group(1)), normalize_text(heading.group(2))
            title = re.sub(r"\*\*", "", title).strip()
            part_match = re.match(r"Part\s+([IVX]+)\s*[-:]\s*(.+)", title, re.IGNORECASE)
            chapter_match = re.match(r"Chapter\s+(\d+)\s*[-:]\s*(.+)", title, re.IGNORECASE)
            if level == 1 and part_match:
                story.extend(
                    [
                        NextPageTemplate("opening"),
                        PageBreak(),
                        OpeningHeading(
                            f"Part {part_match.group(1)}",
                            part_match.group(2),
                            kind="part",
                        ),
                        Spacer(1, 12),
                        NextPageTemplate("body"),
                    ]
                )
            elif level == 1 and chapter_match:
                story.extend(
                    [
                        NextPageTemplate("opening"),
                        PageBreak(),
                        ChapterHeading(int(chapter_match.group(1)), chapter_match.group(2)),
                        Spacer(1, 10),
                        NextPageTemplate("body"),
                    ]
                )
            else:
                story.extend([CondPageBreak(0.82 * inch), Paragraph(inline_markup(title), STYLES[f"h{level}"])])
            index += 1
            continue

        if stripped.startswith(">"):
            block: list[str] = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                block.append(lines[index])
                index += 1
            block_text = "\n".join(block)
            figure = figure_flowables(block_text)
            if figure:
                story.extend(figure)
            else:
                plain = " ".join(re.sub(r"^>\s?", "", item).strip() for item in block)
                story.extend([callout_box(plain), Spacer(1, 10)])
            continue

        inline_image = markdown_image_flowables(stripped, source_path)
        if inline_image:
            story.extend(inline_image)
            index += 1
            continue

        if stripped.startswith("|") and index + 1 < len(lines) and lines[index + 1].strip().startswith("|"):
            block = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                block.append(lines[index])
                index += 1
            story.extend([Spacer(1, 4), parse_table(block), Spacer(1, 11)])
            continue

        if re.fullmatch(r"-{3,}|\*{3,}", stripped):
            story.extend([Spacer(1, 4), HRFlowable(width="100%", thickness=1.2, color=LILAC), Spacer(1, 9)])
            index += 1
            continue

        list_match = re.match(r"^(\s*)([-+*]|\d+\.)\s+(.+)$", line)
        if list_match:
            ordered = list_match.group(2).endswith(".") and list_match.group(2)[0].isdigit()
            items: list[ListItem] = []
            while index < len(lines):
                match = re.match(r"^(\s*)([-+*]|\d+\.)\s+(.+)$", lines[index])
                if not match:
                    break
                item_text = match.group(3).strip()
                item_text = re.sub(r"^\[ \]\s*", "□ ", item_text)
                item_text = re.sub(r"^\[[xX]\]\s*", "■ ", item_text)
                items.append(
                    ListItem(
                        Paragraph(inline_markup(item_text), STYLES["list"]),
                        leftIndent=15,
                    )
                )
                index += 1
            list_options = {
                "bulletType": "1" if ordered else "bullet",
                "leftIndent": 18,
                "bulletFontName": "BookSans-Bold",
                "bulletFontSize": 8,
                "bulletColor": PURPLE,
                "spaceBefore": 2,
                "spaceAfter": 8,
            }
            if ordered:
                list_options["start"] = "1"
            story.append(ListFlowable(items, **list_options))
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            candidate = lines[index].rstrip()
            candidate_stripped = candidate.strip()
            if not candidate_stripped:
                break
            if (
                candidate_stripped.startswith(("#", ">", "```", "|", "!["))
                or re.match(r"^(\s*)([-+*]|\d+\.)\s+", candidate)
                or re.fullmatch(r"-{3,}|\*{3,}", candidate_stripped)
                or re.match(r"^\[\^[^]]+\]:", candidate_stripped)
            ):
                break
            paragraph_lines.append(candidate_stripped)
            index += 1
        story.append(paragraph(" ".join(paragraph_lines)))

    if footnotes:
        story.extend([CondPageBreak(1.2 * inch), Paragraph("Notes", STYLES["h3"])])
        for key, value in footnotes:
            story.append(
                Paragraph(
                    f'<a name="fn-{html.escape(key)}"/><b>{html.escape(key)}.</b> {inline_markup(value)}',
                    STYLES["footnote"],
                )
            )
    return story


def title_pages(
    metadata: dict[str, str],
    chapters: Sequence[tuple[int, str, Path]],
    *,
    final: bool = False,
) -> list[Flowable]:
    title = metadata.get("title", "The Builder's Guide to Agentic Applications 2026")
    subtitle = metadata.get("subtitle", "Applications. Machines. Organizations.")
    author = metadata.get("author", "Jerel Velarde")
    updated = metadata.get("updated", "2026")
    chapter_numbers = [number for number, _, _ in chapters]
    if chapter_numbers:
        if len(chapter_numbers) == 1:
            included = f"Chapter {chapter_numbers[0]}"
        else:
            included = f"Chapters {min(chapter_numbers)}-{max(chapter_numbers)}"
    else:
        included = "front matter only"

    title_story: list[Flowable] = [
        Spacer(1, 0.95 * inch),
        Table(
            [[Paragraph("COPILOTKIT × JEREL VELARDE", STYLES["code_label"])]],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                    ("BOX", (0, 0), (-1, -1), 0, NAVY),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            ),
            hAlign="LEFT",
        ),
        Spacer(1, 0.55 * inch),
        Paragraph(inline_markup(title), STYLES["title"]),
        Paragraph(inline_markup(subtitle), STYLES["subtitle"]),
        HRFlowable(width="100%", thickness=3, color=MINT, spaceBefore=10, spaceAfter=24),
        Paragraph(
            f"<b>{html.escape(author)}</b><br/>Staff Applied AI Engineer<br/>CopilotKit",
            STYLES["lead"],
        ),
        Spacer(1, 2.0 * inch),
        Paragraph(
            "THE BUILDERS GUIDE · FIRST DRAFT · 2026"
            if final
            else "THE BUILDERS GUIDE · REVIEW DRAFT · 2026",
            STYLES["small"],
        ),
        NextPageTemplate("opening"),
        PageBreak(),
        Spacer(1, 0.55 * inch),
        Paragraph("First draft" if final else "Review edition", STYLES["toc_title"]),
        Paragraph(
            (
                "A complete first draft of the 2026 builder's guide to designing, building, and operating "
                "agentic applications across application, machine, and organizational surfaces."
                if final
                else "A local reading copy for technical, editorial, and visual review. "
                "This file is not a publication-ready release."
            ),
            STYLES["lead"],
        ),
        callout_box(
            f"Version note - Built from the current workspace snapshot dated {updated}. "
            f"It includes {included} ({len(chapters)} chapter files). "
            + (
                "The first draft contains all 26 numbered chapters, five primary part openers, "
                "front matter, production engineering, and the field guide."
                if final
                else "Undrafted chapters are intentionally absent rather than represented by filler pages."
            )
        ),
        Spacer(1, 18),
        Paragraph("Edition and rights", STYLES["h2"]),
        Paragraph(
            f"Copyright © 2026 {author}. All rights reserved. "
            + ("First draft. " if final else "Review draft. ")
            + "Code and third-party product references retain their respective licenses and marks.",
            STYLES["body"],
        ),
        Paragraph(
            "The book is an engineering field guide, not financial, legal, security, or compliance advice. "
            "Repository observations are tied to the source pins cited in the manuscript.",
            STYLES["body"],
        ),
        Paragraph("Format", STYLES["h2"]),
        Paragraph(
            "This edition uses US Letter (8.5 × 11 inches). The supplied 1103 × 1426 cover has an "
            "almost identical aspect ratio, so it can fill the first page without distortion or meaningful "
            "cropping.",
            STYLES["body"],
        ),
        Paragraph("Build provenance", STYLES["h2"]),
        Paragraph(
            "Generated deterministically from local Markdown, local image assets, and the bundled Codex "
            "ReportLab/Poppler runtime. Exact commands are recorded in book-components/README.md.",
            STYLES["body"],
        ),
        NextPageTemplate("opening"),
        PageBreak(),
    ]
    return title_story


def toc_flowables(*, final: bool = False) -> list[Flowable]:
    toc = TableOfContents()
    toc.dotsMinLevel = 0
    toc.levelStyles = [
        ParagraphStyle(
            "TOCPart",
            fontName="BookSans-Bold",
            fontSize=10.5,
            leading=18,
            textColor=NAVY,
            leftIndent=0,
            firstLineIndent=0,
            spaceBefore=9,
        ),
        ParagraphStyle(
            "TOCChapter",
            fontName="BookSans",
            fontSize=9.4,
            leading=15,
            textColor=INK,
            leftIndent=16,
            firstLineIndent=0,
        ),
    ]
    return [
        Spacer(1, 0.25 * inch),
        Paragraph("Contents" if final else "Contents in this review draft", STYLES["toc_title"]),
        Paragraph(
            (
                "All 26 chapters, part openers, and the field guide appear below."
                if final
                else "Only sections present in the workspace at build time appear below."
            ),
            STYLES["small"],
        ),
        Spacer(1, 12),
        toc,
    ]


def build_story(
    paths: Sequence[Path], *, final: bool = False
) -> tuple[list[Flowable], dict[str, str], list[tuple[int, str, Path]]]:
    cover = REPOSITORY_ROOT / "book" / "cover.png"
    if not cover.exists():
        fail(f"canonical cover not found: {cover}")
    front_metadata: dict[str, str] = {}
    front_body = ""
    if paths and paths[0].name == "00-front-matter.md":
        front_metadata, front_body = prepare_front_matter(paths[0].read_text(encoding="utf-8"))
    chapters = chapter_info(paths)
    story: list[Flowable] = [NextPageTemplate("opening"), CoverPage(cover), PageBreak()]
    story.extend(title_pages(front_metadata, chapters, final=final))
    story.extend(toc_flowables(final=final))
    story.extend(
        [
            NextPageTemplate("opening"),
            PageBreak(),
            OpeningHeading("Introduction", "Open the hood", kind="front"),
            Spacer(1, 8),
            NextPageTemplate("body"),
        ]
    )
    if front_body:
        story.extend(parse_markdown(front_body, paths[0]))
    for path in paths[1:] if paths and paths[0].name == "00-front-matter.md" else paths:
        story.extend(parse_markdown(path.read_text(encoding="utf-8"), path))
    if not final:
        story.extend(
            [
                Spacer(1, 20),
                HRFlowable(width="100%", thickness=2, color=LILAC),
                Spacer(1, 12),
                Paragraph("End of current review-draft content", STYLES["h3"]),
                Paragraph(
                    "The compiler has reached the final Markdown section currently present in the workspace. "
                    "Planned later chapters are intentionally not represented as completed pages.",
                    STYLES["small"],
                ),
            ]
        )
    return story, front_metadata, chapters


def validate_runtime() -> None:
    if Path(sys.executable).resolve() != RUNTIME_PYTHON.resolve():
        print(
            "warning: build is not running under the bundled Python runtime. "
            f"Recommended: {RUNTIME_PYTHON} {Path(__file__).name}",
            file=sys.stderr,
        )
    for required in [RUNTIME_PYTHON, RUNTIME_NODE, RUNTIME_SHARP, RUNTIME_FONT_ROOT]:
        if not required.exists():
            fail(f"bundled dependency missing: {required}")


def manuscript_word_counts(paths: Sequence[Path]) -> dict[str, int]:
    """Count prose and code with the same parser as the editorial word-count gate."""
    from count_words import parse_markdown as parse_word_counts

    sections = [section for path in paths for section in parse_word_counts(path, PROJECT_ROOT)]
    prose = sum(section.prose_words for section in sections)
    code = sum(section.code_words for section in sections)
    return {"prose": prose, "code": code, "total": prose + code}


def manuscript_figure_counts(paths: Sequence[Path]) -> dict[str, int]:
    references: list[str] = []
    pattern = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
    for path in paths:
        references.extend(pattern.findall(path.read_text(encoding="utf-8")))
    local = [reference for reference in references if not reference.startswith(("http://", "https://"))]
    return {
        "embedded_references": len(local),
        "unique_embedded_assets": len(set(local)),
    }


def build_pdf(output_path: Path, *, final: bool = False) -> dict[str, object]:
    global PUBLICATION_MODE
    PUBLICATION_MODE = final
    validate_runtime()
    register_fonts()
    global STYLES
    STYLES = build_styles()
    paths = discover_sections()
    story, metadata, chapters = build_story(paths, final=final)
    if final and [number for number, _, _ in chapters] != list(range(1, 27)):
        fail("final build requires exactly Chapters 1-26 in order")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    TEMP_ROOT.mkdir(parents=True, exist_ok=True)

    cover_frame = Frame(0, 0, PAGE_WIDTH, PAGE_HEIGHT, id="cover-frame", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    body_frame = Frame(
        LEFT_MARGIN,
        BOTTOM_MARGIN,
        CONTENT_WIDTH,
        PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN,
        id="body-frame",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    document = BookDocTemplate(
        str(output_path),
        pagesize=LETTER,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title=metadata.get("title", "The Builder's Guide to Agentic Applications 2026"),
        author=metadata.get("author", "Jerel Velarde"),
        subject="2026 first draft" if final else "2026 review draft",
        creator="Local deterministic ReportLab compiler",
    )
    document.addPageTemplates(
        [
            PageTemplate(id="cover", frames=[cover_frame]),
            PageTemplate(id="opening", frames=[body_frame], onPage=draw_opening_page),
            PageTemplate(id="body", frames=[body_frame], onPage=draw_body_page),
        ]
    )
    document.multiBuild(story, maxPasses=4)

    reader = PdfReader(str(output_path))
    page_count = len(reader.pages)
    if page_count < 5:
        fail(f"generated PDF unexpectedly short: {page_count} pages")
    if not (reader.pages[0].mediabox.width == PAGE_WIDTH and reader.pages[0].mediabox.height == PAGE_HEIGHT):
        fail("generated cover page size does not match US Letter")
    result: dict[str, object] = {
        "build_date": "2026-07-15",
        "pdf": str(output_path.relative_to(REPOSITORY_ROOT)),
        "sha256": hashlib.sha256(output_path.read_bytes()).hexdigest(),
        "bytes": output_path.stat().st_size,
        "format": "US Letter (8.5 x 11 inches)",
        "pages": page_count,
        "section_count": len(paths),
        "sections": [str(path.relative_to(REPOSITORY_ROOT)) for path in paths],
        "source_paths": {
            "manuscript": [str(path.relative_to(REPOSITORY_ROOT)) for path in paths],
            "cover": "book/cover.png",
            "figure_manifest": "book-components/images/FIGURE MANIFEST.md",
        },
        "chapter_numbers": [number for number, _, _ in chapters],
        "chapter_count": len(chapters),
        "word_counts": manuscript_word_counts(paths),
        "figure_counts": manuscript_figure_counts(paths),
        "cover": "book/cover.png",
        "runtime_python": "bundled-workspace-runtime/python/bin/python3",
        "runtime_node": "bundled-workspace-runtime/node/bin/node",
        "status": "first draft" if final else (
            "partial review draft" if len(chapters) < 26 else "complete chapter set review draft"
        ),
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT_PDF, help="Output PDF path")
    parser.add_argument("--first-draft", action="store_true", help="Build the complete first draft")
    parser.add_argument("--final", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    result = build_pdf(args.output.resolve(), final=args.first_draft or args.final)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
