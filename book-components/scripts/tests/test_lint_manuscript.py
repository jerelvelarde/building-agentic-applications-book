from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "valid-project"
sys.path.insert(0, str(SCRIPTS_DIR))

from lint_manuscript import (  # noqa: E402
    LintConfigurationError,
    ManuscriptLinter,
    load_config,
)


class ManuscriptLinterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name) / "book"
        shutil.copytree(FIXTURE, self.root)
        self.section = self.root / "sections" / "01-canonical-title.md"
        self.config_path = self.root / "scripts" / "manuscript-lint-config.json"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def lint(self, config_updates: dict[str, object] | None = None):
        config = load_config(self.config_path)
        if config_updates:
            config.update(config_updates)
        return ManuscriptLinter(self.root, config).run()[0]

    def rules(self, config_updates: dict[str, object] | None = None) -> list[str]:
        return [violation.rule for violation in self.lint(config_updates)]

    def append(self, text: str) -> None:
        self.section.write_text(
            self.section.read_text(encoding="utf-8") + text,
            encoding="utf-8",
        )

    def test_valid_fixture_passes(self) -> None:
        self.assertEqual([], self.lint())

    def test_manifest_figure_is_referenced_by_markdown_image_path(self) -> None:
        text = self.section.read_text(encoding="utf-8")

        self.assertNotIn("FIG-CH01-01", text)
        self.assertNotIn("missing-figure-reference", self.rules())

    def test_unbalanced_fence_and_heading_jump_report_exact_lines(self) -> None:
        self.append("\n#### Skipped heading\n\n```python\nprint('open')\n")

        violations = self.lint()

        self.assertIn("heading-hierarchy", [item.rule for item in violations])
        fence = next(item for item in violations if item.rule == "unbalanced-fence")
        self.assertEqual("```python", fence.excerpt)
        self.assertGreater(fence.line, 1)

    def test_chapter_title_and_filename_number_drift(self) -> None:
        self.section.write_text(
            self.section.read_text(encoding="utf-8").replace(
                "# Chapter 1 — Canonical Title", "# Chapter 1 — Improvised Title"
            ),
            encoding="utf-8",
        )
        renamed = self.section.with_name("02-canonical-title.md")
        self.section.rename(renamed)
        self.section = renamed

        rules = self.rules()

        self.assertIn("chapter-title-drift", rules)
        self.assertIn("chapter-number-drift", rules)

    def test_figure_ids_duplicate_manifest_rows_and_missing_images_are_checked(self) -> None:
        manifest = self.root / "images" / "FIGURE MANIFEST.md"
        manifest.write_text(
            manifest.read_text(encoding="utf-8")
            + "| `FIG-CH01-01` | 1 | `images/diagrams/duplicate.svg` | Original | Review-ready |\n",
            encoding="utf-8",
        )
        self.append(
            "\n> **FIG-CH01-99 — Unknown**\n"
            "> **FIG-CH01-99 — Repeated**\n"
            "![Missing](../images/does-not-exist.png)\n"
        )

        rules = self.rules()

        self.assertIn("duplicate-figure-id", rules)
        self.assertIn("unknown-figure-id", rules)
        self.assertIn("duplicate-figure-reference", rules)
        self.assertIn("missing-local-image", rules)

    def test_editorial_residue_urls_brand_and_unknown_snippets_fail(self) -> None:
        self.append(
            "\nTODO: Copilot Kit should print `L1-MISSING`. "
            "See http://example.test and https://example.test/bare. "
            "A pinned [source](https://example.test/file#L1-L24) is not a snippet ID.\n"
        )

        violations = self.lint()
        rules = [item.rule for item in violations]

        self.assertIn("draft-residue", rules)
        self.assertIn("product-spelling", rules)
        self.assertIn("unknown-snippet-id", rules)
        self.assertIn("insecure-http-url", rules)
        self.assertIn("bare-url", rules)
        unknown = [item.value for item in violations if item.rule == "unknown-snippet-id"]
        self.assertEqual(["L1-MISSING"], unknown)

    def test_reference_only_screenshot_cannot_be_called_live_proof(self) -> None:
        self.append("\nREF-CH01-01 is a fresh live runtime-verified screenshot.\n")

        rules = self.rules()

        self.assertIn("reference-screenshot-misclaim", rules)

    def test_time_sensitive_claim_needs_nearby_verification_marker(self) -> None:
        self.section.write_text(
            self.section.read_text(encoding="utf-8").replace(
                "> **Verified July 2026:** CopilotKit currently names this API v2.\n",
                "CopilotKit currently names this API v2.\n",
            ),
            encoding="utf-8",
        )

        rules = self.rules()

        self.assertIn("unverified-time-sensitive-claim", rules)

    def test_keypoint_contract_drives_required_chapter_sections(self) -> None:
        text = self.section.read_text(encoding="utf-8")
        text = text[: text.index("## Failure modes")]
        self.section.write_text(text, encoding="utf-8")

        violations = [
            item for item in self.lint() if item.rule == "missing-chapter-contract"
        ]

        self.assertEqual(4, len(violations))
        self.assertTrue(any("Bridge" in item.message for item in violations))

    def test_allowlist_is_narrow_and_requires_a_reason(self) -> None:
        self.append("\nUse snippet `L1-MISSING` for the negative example.\n")
        config = load_config(self.config_path)
        config["allowlist"] = [
            {
                "rule": "unknown-snippet-id",
                "path": "sections/*.md",
                "value": "L1-MISSING",
                "reason": "Fixture proves exact-value suppression.",
            }
        ]

        violations, allowlisted = ManuscriptLinter(self.root, config).run()

        self.assertNotIn("unknown-snippet-id", [item.rule for item in violations])
        self.assertIn("unknown-snippet-id", [item.rule for item in allowlisted])

        config["allowlist"] = [{"rule": "unknown-snippet-id"}]
        with self.assertRaises(LintConfigurationError):
            ManuscriptLinter(self.root, config)

    def test_invalid_config_fails_instead_of_reporting_green(self) -> None:
        self.config_path.write_text("{}\n", encoding="utf-8")
        config = load_config(self.config_path)
        shutil.rmtree(self.root / "sections")

        with self.assertRaises(LintConfigurationError):
            ManuscriptLinter(self.root, config)


if __name__ == "__main__":
    unittest.main()
