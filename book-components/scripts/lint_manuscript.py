#!/usr/bin/env python3
"""Lint the Agentic Applications manuscript against its canonical book sources.

The linter deliberately reports editorial debt instead of rewriting prose or
silently accepting a partially complete manuscript. A clean exit means every
enabled structural rule passed; exit 1 means manuscript violations were found;
exit 2 means the linter could not establish a trustworthy configuration.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote, urlsplit


FIGURE_ID_RE = re.compile(r"\bFIG-CH(?P<chapter>\d{2})-(?P<ordinal>\d{2})\b")
REFERENCE_ID_RE = re.compile(r"\bREF-CH(?P<chapter>\d{2})-(?P<ordinal>\d{2})\b")
SNIPPET_ID_RE = re.compile(r"\b(?:L[123]|PROD)-[A-Z][A-Z0-9-]*\b")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
CHAPTER_HEADING_RE = re.compile(
    r"^Chapter\s+(?P<number>\d{1,2})\s+[—-]\s+(?P<title>.+?)\s*$"
)
FENCE_RE = re.compile(r"^\s*(?P<marker>`{3,}|~{3,})(?:[^`~].*)?$")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
MARKDOWN_LINK_URL_RE = re.compile(r"!?\[[^\]]*\]\(\s*https?://[^)]*\)", re.I)
MARKDOWN_LINK_RE = re.compile(r"(?P<label>!?\[[^\]]*\])\([^)]*\)")
AUTOLINK_RE = re.compile(r"<https?://[^>]+>", re.I)
URL_RE = re.compile(r"https?://[^\s<>]+", re.I)
IMAGE_LINK_RE = re.compile(r"!\[[^\]]*\]\((?P<target>[^)]+)\)")
HTML_IMAGE_RE = re.compile(r"<img\b[^>]*\bsrc=[\"'](?P<target>[^\"']+)[\"'][^>]*>", re.I)
RESIDUE_RE = re.compile(r"\b(?:TODO|TBD|FIXME)\b|\[NEED\s+RESEARCH\]", re.I)
COPILOT_KIT_RE = re.compile(r"\bCopilot\s+Kit\b", re.I)
PRODUCT_RE = re.compile(
    r"\b(?:CopilotKit|LangChain|LangGraph|LangSmith|OpenTag|Claude\s+Tag|"
    r"Claude\s+Code|OpenClaw|Hermes|Channels\s+SDK|AG-UI|MCP|"
    r"CopilotKit\s+Intelligence)\b|@[a-z0-9-]+/[a-z0-9-]+",
    re.I,
)
TIME_TRIGGER_RE = re.compile(
    r"\b(?:current(?:ly)?|as\s+of|available|availability|supports?|"
    r"ships?|preview|beta|early\s+access|waitlist(?:ed)?|generally\s+available|"
    r"GA|v\d+|renamed|deprecated|pricing|release(?:d|s)?|runtime-verified|live)\b",
    re.I,
)
SEMVER_RE = re.compile(r"(?<!\d)\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?\b")
VERSION_CLAIM_RE = re.compile(
    r"\b(?:exact|current|deployed|selected|package|runtime|product|API)\s+versions?\b|"
    r"\bversions?'s\b|\bversions?\s+(?:\d|used|deployed|selected|pin|number|matrix)\b",
    re.I,
)
PINNED_CLAIM_RE = re.compile(
    r"\b(?:pinned|captured)\b.{0,50}\b(?:package|source|revision|commit|release|repository)\b|"
    r"\b(?:package|source|revision|commit|release|repository)\b.{0,50}\b(?:pinned|captured)\b",
    re.I,
)
IMPERATIVE_RE = re.compile(
    r"^(?:before\b.{0,40},\s*)?(?:verify|pin|recheck|reproduce|map|choose|test|"
    r"confirm|refresh|capture|run|select|inspect|document)\b",
    re.I,
)
CLAIM_VERB_RE = re.compile(
    r"\b(?:is|are|has|have|supports?|ships?|uses?|requires?|includes?|contains?|"
    r"reports?|documents?|provides?|exposes?|defines?|registers?|resolves?|passes?|"
    r"compiles?|connects?)\b",
    re.I,
)
MARKDOWN_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".avif"}


class LintConfigurationError(RuntimeError):
    """Raised when canonical lint inputs are absent or malformed."""


@dataclass(frozen=True)
class Violation:
    rule: str
    path: str
    line: int
    column: int
    message: str
    excerpt: str
    value: str | None = None

    def sort_key(self) -> tuple[str, int, int, str, str]:
        return (self.path, self.line, self.column, self.rule, self.message)


@dataclass(frozen=True)
class AllowlistEntry:
    rule: str
    reason: str
    path: str = "*"
    line: int | None = None
    value: str | None = None
    message_contains: str | None = None

    def matches(self, violation: Violation) -> bool:
        if self.rule not in {"*", violation.rule}:
            return False
        if not fnmatch.fnmatch(violation.path, self.path):
            return False
        if self.line is not None and self.line != violation.line:
            return False
        if self.value is not None and self.value != violation.value:
            return False
        return not (
            self.message_contains is not None
            and self.message_contains not in violation.message
        )


@dataclass
class MarkdownDocument:
    path: Path
    relative_path: str
    lines: list[str]
    code_lines: set[int]
    frontmatter_lines: set[int]
    headings: list[tuple[int, int, str]]
    chapter: int | None
    chapter_title: str | None
    chapter_heading_line: int | None

    def visible_line(self, line_number: int) -> bool:
        return (
            line_number not in self.code_lines
            and line_number not in self.frontmatter_lines
        )


@dataclass(frozen=True)
class ManifestAsset:
    asset_id: str
    chapter: int
    path: str
    status: str
    line: int


@dataclass(frozen=True)
class Contract:
    chapter: int
    exercise: bool
    failure_security: bool
    checklist: bool
    bridge: bool


DEFAULT_CONFIG: dict[str, Any] = {
    "manuscript_globs": ["sections/**/*.md"],
    "exclude_globs": [],
    "require_all_chapters": True,
    "require_all_manifest_figures_referenced": True,
    "verification_marker": "Verified July 2026",
    "verification_window_lines": 5,
    "allowlist": [],
}


def _read_required(path: Path) -> str:
    if not path.is_file():
        raise LintConfigurationError(f"Required canonical input is missing: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise LintConfigurationError(f"Canonical input is not UTF-8: {path}") from error


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def load_config(path: Path) -> dict[str, Any]:
    raw = _read_required(path)
    try:
        supplied = json.loads(raw)
    except json.JSONDecodeError as error:
        raise LintConfigurationError(f"Invalid JSON in {path}: {error}") from error
    if not isinstance(supplied, dict):
        raise LintConfigurationError(f"Lint config must be a JSON object: {path}")
    config = {**DEFAULT_CONFIG, **supplied}
    if not isinstance(config["manuscript_globs"], list) or not config["manuscript_globs"]:
        raise LintConfigurationError("manuscript_globs must be a non-empty list")
    if not isinstance(config["exclude_globs"], list):
        raise LintConfigurationError("exclude_globs must be a list")
    if not isinstance(config["verification_window_lines"], int) or config["verification_window_lines"] < 0:
        raise LintConfigurationError("verification_window_lines must be a non-negative integer")
    if not isinstance(config["verification_marker"], str) or not config["verification_marker"].strip():
        raise LintConfigurationError("verification_marker must be a non-empty string")
    if not isinstance(config["allowlist"], list):
        raise LintConfigurationError("allowlist must be a list")
    return config


def load_allowlist(config: dict[str, Any]) -> list[AllowlistEntry]:
    entries: list[AllowlistEntry] = []
    for index, raw in enumerate(config["allowlist"], 1):
        if not isinstance(raw, dict):
            raise LintConfigurationError(f"allowlist entry {index} must be an object")
        rule = raw.get("rule")
        reason = raw.get("reason")
        if not isinstance(rule, str) or not rule:
            raise LintConfigurationError(f"allowlist entry {index} needs a rule")
        if not isinstance(reason, str) or not reason.strip():
            raise LintConfigurationError(
                f"allowlist entry {index} needs a non-empty reason; silent suppression is forbidden"
            )
        line = raw.get("line")
        if line is not None and (not isinstance(line, int) or line < 1):
            raise LintConfigurationError(f"allowlist entry {index} has an invalid line")
        entries.append(
            AllowlistEntry(
                rule=rule,
                reason=reason,
                path=str(raw.get("path", "*")),
                line=line,
                value=str(raw["value"]) if "value" in raw else None,
                message_contains=(
                    str(raw["message_contains"])
                    if "message_contains" in raw
                    else None
                ),
            )
        )
    return entries


def _frontmatter_lines(lines: list[str]) -> set[int]:
    if not lines or lines[0].strip() != "---":
        return set()
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return set(range(1, index + 2))
    return set()


def _fence_map(
    lines: list[str], relative_path: str
) -> tuple[set[int], list[Violation]]:
    code_lines: set[int] = set()
    violations: list[Violation] = []
    opening: tuple[str, int, int] | None = None
    for line_number, line in enumerate(lines, 1):
        match = FENCE_RE.match(line)
        if opening is None:
            if match:
                marker = match.group("marker")
                opening = (marker[0], len(marker), line_number)
                code_lines.add(line_number)
            continue
        code_lines.add(line_number)
        if match:
            marker = match.group("marker")
            if marker[0] == opening[0] and len(marker) >= opening[1]:
                opening = None
    if opening is not None:
        line_number = opening[2]
        violations.append(
            Violation(
                "unbalanced-fence",
                relative_path,
                line_number,
                1,
                "Code fence opens here but is never closed with a compatible marker.",
                lines[line_number - 1].strip(),
            )
        )
    return code_lines, violations


def parse_document(path: Path, root: Path) -> tuple[MarkdownDocument, list[Violation]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError as error:
        raise LintConfigurationError(f"Manuscript file is not UTF-8: {path}") from error
    relative_path = _relative(path, root)
    code_lines, violations = _fence_map(lines, relative_path)
    frontmatter = _frontmatter_lines(lines)
    headings: list[tuple[int, int, str]] = []
    chapter: int | None = None
    chapter_title: str | None = None
    chapter_heading_line: int | None = None
    previous_level: int | None = None
    for line_number, line in enumerate(lines, 1):
        if line_number in code_lines or line_number in frontmatter:
            continue
        match = HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        title = re.sub(r"\s+#+\s*$", "", match.group(2)).strip()
        headings.append((line_number, level, title))
        if previous_level is not None and level > previous_level + 1:
            violations.append(
                Violation(
                    "heading-hierarchy",
                    relative_path,
                    line_number,
                    1,
                    f"Heading jumps from H{previous_level} to H{level}.",
                    line.strip(),
                )
            )
        previous_level = level
        chapter_match = CHAPTER_HEADING_RE.match(title) if level == 1 else None
        if chapter_match:
            if chapter is not None:
                violations.append(
                    Violation(
                        "duplicate-chapter-heading",
                        relative_path,
                        line_number,
                        1,
                        f"File contains a second Chapter heading (Chapter {chapter_match.group('number')}).",
                        line.strip(),
                        chapter_match.group("number"),
                    )
                )
            else:
                chapter = int(chapter_match.group("number"))
                chapter_title = chapter_match.group("title").strip()
                chapter_heading_line = line_number
    return (
        MarkdownDocument(
            path=path,
            relative_path=relative_path,
            lines=lines,
            code_lines=code_lines,
            frontmatter_lines=frontmatter,
            headings=headings,
            chapter=chapter,
            chapter_title=chapter_title,
            chapter_heading_line=chapter_heading_line,
        ),
        violations,
    )


def load_canonical_titles(path: Path) -> dict[int, str]:
    titles: dict[int, str] = {}
    row_re = re.compile(r"^\|\s*(\d{1,2})\s*\|\s*\*?([^|*]+?)\*?\s*\|")
    for line in _read_required(path).splitlines():
        match = row_re.match(line)
        if not match:
            continue
        chapter = int(match.group(1))
        title = match.group(2).strip()
        if chapter in titles:
            raise LintConfigurationError(
                f"Duplicate Chapter {chapter} in canonical title guide: {path}"
            )
        titles[chapter] = title
    if not titles:
        raise LintConfigurationError(f"No canonical chapter titles found in {path}")
    return titles


def _parse_frontmatter_values(path: Path) -> dict[str, str]:
    lines = _read_required(path).splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return values
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"\'')
    raise LintConfigurationError(f"Unclosed frontmatter in keypoint file: {path}")


def load_contracts(root: Path) -> dict[int, Contract]:
    contracts: dict[int, Contract] = {}
    keypoints_root = root / "keypoints"
    if not keypoints_root.is_dir():
        raise LintConfigurationError(f"Required keypoints directory is missing: {keypoints_root}")
    for path in sorted(keypoints_root.rglob("*.md")):
        values = _parse_frontmatter_values(path)
        raw_chapter = values.get("chapter")
        if raw_chapter is None or not raw_chapter.isdigit():
            continue
        chapter = int(raw_chapter)
        text = _read_required(path)
        contract = Contract(
            chapter=chapter,
            exercise=bool(re.search(r"^##\s+Exercise\b", text, re.M | re.I)),
            failure_security=bool(
                re.search(r"^##\s+Failure and security section\b", text, re.M | re.I)
            ),
            checklist=bool(re.search(r"^##\s+Production checklist\b", text, re.M | re.I)),
            bridge=bool(re.search(r"^##\s+Bridge\b", text, re.M | re.I)),
        )
        if chapter in contracts:
            raise LintConfigurationError(
                f"Multiple keypoint files define Chapter {chapter}: {path}"
            )
        contracts[chapter] = contract
    if not contracts:
        raise LintConfigurationError("No chapter contracts found in keypoints")
    return contracts


def load_manifest(path: Path) -> tuple[dict[str, ManifestAsset], list[Violation], dict[str, ManifestAsset]]:
    figures: dict[str, ManifestAsset] = {}
    references: dict[str, ManifestAsset] = {}
    violations: list[Violation] = []
    relative = "images/FIGURE MANIFEST.md"
    row_re = re.compile(
        r"^\|\s*`(?P<id>(?:FIG|REF)-CH\d{2}-\d{2})`\s*\|\s*(?P<chapter>\d+)\s*\|"
        r"\s*`(?P<path>[^`]+)`\s*\|(?P<rest>.*)$"
    )
    for line_number, line in enumerate(_read_required(path).splitlines(), 1):
        match = row_re.match(line)
        if not match:
            continue
        asset_id = match.group("id")
        cells = [cell.strip() for cell in match.group("rest").split("|")]
        status = cells[1] if len(cells) > 1 else ""
        asset = ManifestAsset(
            asset_id=asset_id,
            chapter=int(match.group("chapter")),
            path=match.group("path"),
            status=status,
            line=line_number,
        )
        target = figures if asset_id.startswith("FIG-") else references
        if asset_id in target:
            violations.append(
                Violation(
                    "duplicate-figure-id",
                    relative,
                    line_number,
                    1,
                    f"Manifest defines {asset_id} more than once.",
                    line.strip(),
                    asset_id,
                )
            )
        else:
            target[asset_id] = asset
    if not figures:
        raise LintConfigurationError(f"No FIG-CHNN-NN rows found in {path}")
    return figures, violations, references


def load_snippet_ids(path: Path) -> set[str]:
    snippet_ids: set[str] = set()
    row_re = re.compile(r"^\|\s*`?((?:L[123]|PROD)-[A-Z][A-Z0-9-]*)`?\s*\|")
    for line in _read_required(path).splitlines():
        match = row_re.match(line)
        if match:
            snippet_ids.add(match.group(1))
    if not snippet_ids:
        raise LintConfigurationError(f"No snippet IDs found in {path}")
    return snippet_ids


def collect_manuscript_files(root: Path, config: dict[str, Any]) -> list[Path]:
    files: set[Path] = set()
    for pattern in config["manuscript_globs"]:
        files.update(path for path in root.glob(pattern) if path.is_file())
    excluded = [str(pattern) for pattern in config["exclude_globs"]]
    selected = sorted(
        path
        for path in files
        if not any(fnmatch.fnmatch(_relative(path, root), pattern) for pattern in excluded)
    )
    if not selected:
        raise LintConfigurationError(
            "No manuscript files matched manuscript_globs; refusing to report a false green"
        )
    return selected


def _column(line: str, token: str) -> int:
    index = line.find(token)
    return index + 1 if index >= 0 else 1


def _strip_inline_code(line: str) -> str:
    return INLINE_CODE_RE.sub("", line)


def _strip_markdown_link_destinations(line: str) -> str:
    return MARKDOWN_LINK_RE.sub(r"\g<label>", line)


def _image_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split(maxsplit=1)[0]


def _local_asset_exists(source: Path, root: Path, raw_target: str) -> tuple[bool, str]:
    target = unquote(_image_target(raw_target))
    parsed = urlsplit(target)
    if parsed.scheme or target.startswith("#"):
        return True, target
    clean_path = parsed.path
    if not clean_path or Path(clean_path).suffix.lower() not in MARKDOWN_IMAGE_SUFFIXES:
        return True, clean_path
    candidate = Path(clean_path)
    candidates = [candidate] if candidate.is_absolute() else [source.parent / candidate, root / candidate]
    return any(path.is_file() for path in candidates), clean_path


def _local_asset_manifest_path(source: Path, root: Path, raw_target: str) -> str | None:
    """Resolve a local Markdown image to the project-relative manifest path."""
    target = unquote(_image_target(raw_target))
    parsed = urlsplit(target)
    if parsed.scheme or target.startswith("#"):
        return None
    clean_path = parsed.path
    if not clean_path or Path(clean_path).suffix.lower() not in MARKDOWN_IMAGE_SUFFIXES:
        return None
    candidate = Path(clean_path)
    candidates = [candidate] if candidate.is_absolute() else [source.parent / candidate, root / candidate]
    for path in candidates:
        if path.is_file():
            return _relative(path.resolve(), root)
    return None


def _has_verification_marker(
    document: MarkdownDocument,
    line_number: int,
    marker: str,
    window: int,
) -> bool:
    start = max(1, line_number - window)
    end = min(len(document.lines), line_number + window)
    for nearby in range(start, end + 1):
        if document.visible_line(nearby) and marker.lower() in document.lines[nearby - 1].lower():
            return True
    return False


def _time_sensitive_claim(line: str) -> bool:
    without_links = _strip_markdown_link_destinations(line)
    if SEMVER_RE.search(without_links):
        return True
    if not PRODUCT_RE.search(without_links):
        return False
    normalized = without_links.lstrip().lstrip("> ").strip()
    if normalized.startswith("- [ ]") or IMPERATIVE_RE.search(normalized):
        return False
    if normalized.startswith("- ") and not CLAIM_VERB_RE.search(normalized):
        return False
    return bool(
        TIME_TRIGGER_RE.search(without_links)
        or VERSION_CLAIM_RE.search(without_links)
        or PINNED_CLAIM_RE.search(without_links)
    )


def _screenshot_misclaim(
    document: MarkdownDocument,
    line_number: int,
    reference_tokens: set[str],
) -> str | None:
    start = max(1, line_number - 2)
    end = min(len(document.lines), line_number + 2)
    context = " ".join(
        document.lines[index - 1]
        for index in range(start, end + 1)
        if document.visible_line(index)
    )
    lower = context.lower()
    if not any(token.lower() in lower for token in reference_tokens):
        return None
    current_line = document.lines[line_number - 1].lower()
    fresh_language = re.search(
        r"\b(?:fresh|live|runtime-verified|runtime proof|proof from (?:this|the) run|"
        r"captured (?:live|from (?:this|the) run))\b",
        current_line,
    )
    if not fresh_language:
        return None
    negated = re.search(
        r"\b(?:reference-only|not fresh|no fresh|not live|not runtime|isn't runtime|"
        r"is not runtime|cannot be|must not be|demo frame|reference frame)\b",
        lower,
    )
    return None if negated else fresh_language.group(0)


class ManuscriptLinter:
    def __init__(self, root: Path, config: dict[str, Any]):
        self.root = root.resolve()
        self.config = config
        self.allowlist = load_allowlist(config)
        self.canonical_titles = load_canonical_titles(
            self.root / "keypoints/chapter-titles-guide.md"
        )
        self.contracts = load_contracts(self.root)
        self.figures, self.manifest_violations, self.references = load_manifest(
            self.root / "images/FIGURE MANIFEST.md"
        )
        self.figures_by_path = {asset.path: asset for asset in self.figures.values()}
        self.snippet_ids = load_snippet_ids(
            self.root / "materials/code-excerpts/CODE EXCERPT CATALOG.md"
        )
        self.files = collect_manuscript_files(self.root, config)
        self.documents: list[MarkdownDocument] = []
        self.raw_violations: list[Violation] = []
        self.allowlisted_violations: list[Violation] = []

    def _add(
        self,
        rule: str,
        document: MarkdownDocument,
        line: int,
        message: str,
        *,
        token: str | None = None,
        value: str | None = None,
    ) -> None:
        excerpt = document.lines[line - 1].strip() if 1 <= line <= len(document.lines) else ""
        self.raw_violations.append(
            Violation(
                rule,
                document.relative_path,
                line,
                _column(document.lines[line - 1], token) if token and 1 <= line <= len(document.lines) else 1,
                message,
                excerpt,
                value,
            )
        )

    def _lint_chapter_identity(self, document: MarkdownDocument) -> None:
        filename_match = re.match(r"^(\d{2})-", document.path.name)
        expected_from_filename = int(filename_match.group(1)) if filename_match else None
        is_chapter_file = expected_from_filename not in {None, 0}
        if is_chapter_file and document.chapter is None:
            self._add(
                "missing-chapter-heading",
                document,
                1,
                "Chapter file has no '# Chapter N — Canonical Title' heading.",
            )
            return
        if document.chapter is None:
            return
        line = document.chapter_heading_line or 1
        if expected_from_filename is not None and expected_from_filename != document.chapter:
            self._add(
                "chapter-number-drift",
                document,
                line,
                f"Filename implies Chapter {expected_from_filename}, but heading declares Chapter {document.chapter}.",
                value=str(document.chapter),
            )
        canonical = self.canonical_titles.get(document.chapter)
        if canonical is None:
            self._add(
                "unknown-chapter-number",
                document,
                line,
                f"Chapter {document.chapter} is absent from the canonical title guide.",
                value=str(document.chapter),
            )
        elif document.chapter_title != canonical:
            self._add(
                "chapter-title-drift",
                document,
                line,
                f"Chapter {document.chapter} title must be '{canonical}', not '{document.chapter_title}'.",
                value=str(document.chapter),
            )

    def _lint_contract(self, document: MarkdownDocument) -> None:
        if document.chapter is None:
            return
        contract = self.contracts.get(document.chapter)
        if contract is None:
            self._add(
                "missing-keypoint-contract",
                document,
                document.chapter_heading_line or 1,
                f"No canonical keypoint contract exists for Chapter {document.chapter}.",
                value=str(document.chapter),
            )
            return
        h2 = [title.lower() for _, level, title in document.headings if level == 2]
        required: list[tuple[bool, str, bool]] = [
            (contract.exercise, "Exercise", any(title.startswith("exercise") for title in h2)),
            (
                contract.failure_security,
                "an explicit failure/security section",
                any(
                    re.search(r"\b(?:failure|security|threat|attack|risk|adversarial|drill)\b", title)
                    for title in h2
                ),
            ),
            (
                contract.checklist,
                "Builder Checklist or Production Checklist",
                any(
                    "builder checklist" in title
                    or "production checklist" in title
                    or "production gate" in title
                    for title in h2
                ),
            ),
            (contract.bridge, "next-chapter Bridge", any(title.startswith("bridge") for title in h2)),
        ]
        for expected, label, present in required:
            if expected and not present:
                self._add(
                    "missing-chapter-contract",
                    document,
                    document.chapter_heading_line or 1,
                    f"Chapter {document.chapter} is missing {label}, required by its canonical keypoints.",
                    value=label,
                )

    def _lint_lines(self, document: MarkdownDocument) -> dict[str, list[tuple[MarkdownDocument, int]]]:
        figure_refs: dict[str, list[tuple[MarkdownDocument, int]]] = defaultdict(list)
        reference_tokens: set[str] = set()
        for asset in self.references.values():
            if "reference-only" in asset.status.lower():
                reference_tokens.update({asset.asset_id, asset.path, Path(asset.path).name})

        for line_number, line in enumerate(document.lines, 1):
            if not document.visible_line(line_number):
                continue

            residue = RESIDUE_RE.search(line)
            if residue:
                self._add(
                    "draft-residue",
                    document,
                    line_number,
                    f"Drafting residue '{residue.group(0)}' must not enter review prose.",
                    token=residue.group(0),
                    value=residue.group(0).upper(),
                )

            spelling = COPILOT_KIT_RE.search(line)
            if spelling:
                self._add(
                    "product-spelling",
                    document,
                    line_number,
                    "Use the canonical product spelling 'CopilotKit'.",
                    token=spelling.group(0),
                    value=spelling.group(0),
                )

            for figure_match in FIGURE_ID_RE.finditer(line):
                figure_id = figure_match.group(0)
                figure_refs[figure_id].append((document, line_number))
                if figure_id not in self.figures:
                    self._add(
                        "unknown-figure-id",
                        document,
                        line_number,
                        f"{figure_id} is absent from images/FIGURE MANIFEST.md.",
                        token=figure_id,
                        value=figure_id,
                    )
                if document.chapter is not None and int(figure_match.group("chapter")) != document.chapter:
                    self._add(
                        "figure-chapter-mismatch",
                        document,
                        line_number,
                        f"{figure_id} is assigned to Chapter {int(figure_match.group('chapter'))}, not Chapter {document.chapter}.",
                        token=figure_id,
                        value=figure_id,
                    )

            for snippet_match in SNIPPET_ID_RE.finditer(
                _strip_markdown_link_destinations(line)
            ):
                snippet_id = snippet_match.group(0)
                if snippet_id not in self.snippet_ids:
                    self._add(
                        "unknown-snippet-id",
                        document,
                        line_number,
                        f"{snippet_id} is absent from the code excerpt catalog.",
                        token=snippet_id,
                        value=snippet_id,
                    )

            for match in IMAGE_LINK_RE.finditer(line):
                exists, target = _local_asset_exists(document.path, self.root, match.group("target"))
                if not exists:
                    self._add(
                        "missing-local-image",
                        document,
                        line_number,
                        f"Local image target does not exist: {target}",
                        token=target,
                        value=target,
                    )
                manifest_path = _local_asset_manifest_path(
                    document.path, self.root, match.group("target")
                )
                asset = self.figures_by_path.get(manifest_path or "")
                is_canonical_placement = asset and (
                    document.chapter == asset.chapter
                    or (document.chapter is None and asset.chapter == 27)
                )
                if is_canonical_placement and asset.asset_id not in figure_refs:
                    figure_refs[asset.asset_id].append((document, line_number))
            for match in HTML_IMAGE_RE.finditer(line):
                exists, target = _local_asset_exists(document.path, self.root, match.group("target"))
                if not exists:
                    self._add(
                        "missing-local-image",
                        document,
                        line_number,
                        f"Local image target does not exist: {target}",
                        token=target,
                        value=target,
                    )

            prose_without_inline = _strip_inline_code(line)
            for url_match in URL_RE.finditer(prose_without_inline):
                url = url_match.group(0).rstrip(".,;:!?)\"]}")
                if url.lower().startswith("http://"):
                    self._add(
                        "insecure-http-url",
                        document,
                        line_number,
                        f"Use HTTPS or remove the insecure URL: {url}",
                        token=url,
                        value=url,
                    )
            without_link_destinations = MARKDOWN_LINK_URL_RE.sub("", prose_without_inline)
            without_link_destinations = AUTOLINK_RE.sub("", without_link_destinations)
            for url_match in URL_RE.finditer(without_link_destinations):
                url = url_match.group(0).rstrip(".,;:!?)\"]}")
                self._add(
                    "bare-url",
                    document,
                    line_number,
                    f"Replace bare URL with a descriptive Markdown link: {url}",
                    token=url,
                    value=url,
                )

            misclaim = _screenshot_misclaim(document, line_number, reference_tokens)
            if misclaim:
                self._add(
                    "reference-screenshot-misclaim",
                    document,
                    line_number,
                    "Reference-only screenshot material is described as fresh/live/runtime proof.",
                    token=misclaim,
                    value=misclaim,
                )

            marker = str(self.config["verification_marker"])
            if marker.lower() not in line.lower() and _time_sensitive_claim(line):
                if not _has_verification_marker(
                    document,
                    line_number,
                    marker,
                    int(self.config["verification_window_lines"]),
                ):
                    self._add(
                        "unverified-time-sensitive-claim",
                        document,
                        line_number,
                        f"Time-sensitive product/version claim needs a nearby '{marker}' marker.",
                        value=marker,
                    )
        return figure_refs

    def run(self) -> tuple[list[Violation], list[Violation]]:
        self.raw_violations = list(self.manifest_violations)
        self.documents = []
        all_figure_refs: dict[str, list[tuple[MarkdownDocument, int]]] = defaultdict(list)
        chapter_documents: dict[int, list[MarkdownDocument]] = defaultdict(list)

        for path in self.files:
            document, parse_violations = parse_document(path, self.root)
            self.documents.append(document)
            self.raw_violations.extend(parse_violations)
            self._lint_chapter_identity(document)
            self._lint_contract(document)
            if document.chapter is not None:
                chapter_documents[document.chapter].append(document)
            for figure_id, occurrences in self._lint_lines(document).items():
                all_figure_refs[figure_id].extend(occurrences)

        for chapter, documents in chapter_documents.items():
            if len(documents) > 1:
                for duplicate in documents[1:]:
                    self._add(
                        "duplicate-chapter-number",
                        duplicate,
                        duplicate.chapter_heading_line or 1,
                        f"Chapter {chapter} appears in more than one manuscript file.",
                        value=str(chapter),
                    )

        if self.config["require_all_chapters"]:
            for chapter, title in self.canonical_titles.items():
                if chapter not in chapter_documents:
                    self.raw_violations.append(
                        Violation(
                            "missing-canonical-chapter",
                            "keypoints/chapter-titles-guide.md",
                            1,
                            1,
                            f"Manuscript is missing Chapter {chapter} — {title}.",
                            "",
                            str(chapter),
                        )
                    )

        for figure_id, occurrences in all_figure_refs.items():
            if len(occurrences) > 1:
                for document, line_number in occurrences[1:]:
                    self._add(
                        "duplicate-figure-reference",
                        document,
                        line_number,
                        f"{figure_id} is placed/referenced more than once in the manuscript.",
                        token=figure_id,
                        value=figure_id,
                    )

        if self.config["require_all_manifest_figures_referenced"]:
            for figure_id, asset in self.figures.items():
                if figure_id not in all_figure_refs:
                    self.raw_violations.append(
                        Violation(
                            "missing-figure-reference",
                            "images/FIGURE MANIFEST.md",
                            asset.line,
                            1,
                            f"Manifest figure {figure_id} is not referenced in the manuscript.",
                            figure_id,
                            figure_id,
                        )
                    )

        for asset in self.figures.values():
            if not (self.root / asset.path).is_file():
                self.raw_violations.append(
                    Violation(
                        "missing-figure-asset",
                        "images/FIGURE MANIFEST.md",
                        asset.line,
                        1,
                        f"Manifest path for {asset.asset_id} does not exist: {asset.path}",
                        asset.path,
                        asset.asset_id,
                    )
                )

        violations: list[Violation] = []
        allowlisted: list[Violation] = []
        for violation in sorted(self.raw_violations, key=Violation.sort_key):
            if any(entry.matches(violation) for entry in self.allowlist):
                allowlisted.append(violation)
            else:
                violations.append(violation)
        self.allowlisted_violations = allowlisted
        return violations, allowlisted

    def report(self) -> dict[str, Any]:
        violations, allowlisted = self.run()
        counts = Counter(violation.rule for violation in violations)
        return {
            "schema_version": 1,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "root": str(self.root),
            "inputs": [_relative(path, self.root) for path in self.files],
            "summary": {
                "files": len(self.files),
                "violations": len(violations),
                "allowlisted": len(allowlisted),
                "by_rule": dict(sorted(counts.items())),
            },
            "violations": [asdict(violation) for violation in violations],
            "allowlisted_violations": [asdict(violation) for violation in allowlisted],
        }


def _print_human(report: dict[str, Any]) -> None:
    summary = report["summary"]
    print(
        f"Manuscript lint: {summary['violations']} violation(s) in "
        f"{summary['files']} file(s); {summary['allowlisted']} allowlisted."
    )
    for violation in report["violations"]:
        print(
            f"{violation['path']}:{violation['line']}:{violation['column']}: "
            f"{violation['rule']}: {violation['message']}"
        )
        if violation["excerpt"]:
            print(f"    {violation['excerpt']}")
    if summary["by_rule"]:
        print("\nBy rule:")
        for rule, count in summary["by_rule"].items():
            print(f"  {rule}: {count}")


def _write_json(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Book project root (defaults to the parent of scripts/).",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Config path (defaults to scripts/manuscript-lint-config.json under root).",
    )
    parser.add_argument("--json-output", type=Path, help="Also write the complete JSON report here.")
    parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Standard-output format.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    root = args.root.resolve()
    config_path = args.config.resolve() if args.config else root / "scripts/manuscript-lint-config.json"
    try:
        config = load_config(config_path)
        report = ManuscriptLinter(root, config).report()
    except LintConfigurationError as error:
        print(f"manuscript lint configuration error: {error}", file=sys.stderr)
        return 2

    if args.json_output:
        output_path = args.json_output
        if not output_path.is_absolute():
            output_path = root / output_path
        _write_json(output_path, report)
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        _print_human(report)
    return 1 if report["summary"]["violations"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
