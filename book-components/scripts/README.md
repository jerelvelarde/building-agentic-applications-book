# Manuscript scripts

## Final publication build

Build the complete 2026 edition from the project root:

```bash
RUNTIME="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies"
"$RUNTIME/python/bin/python3" book-components/scripts/build_review_pdf.py \
  --first-draft \
  --output book/agentic-applications-2026-first-draft.pdf
```

Final mode requires Chapters 1 through 26 exactly once and writes the dated
`book/build-manifest.json` with page, section, word, figure, byte, and SHA-256
counts. The original review PDF is not overwritten.

Render and scan the full artifact with:

```bash
RUNTIME="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies"
"$RUNTIME/python/bin/python3" book-components/scripts/validate_final_pdf.py
```

This creates page renders, overview and detail contact sheets, and
`book/first-draft-validation.json`. It exits nonzero for blank or malformed renders,
editorial residue, missing-image notices, adjacent duplicate pages, or text
extraction anomalies.

## Integrity linter

Run the book-specific structural and evidence checks from the project root:

```bash
python3 book-components/scripts/lint_manuscript.py
```

The command prints `file:line:column` findings and exits:

- `0` when every enabled rule passes;
- `1` when manuscript violations exist;
- `2` when canonical inputs or lint configuration are missing or malformed.

Write the same result as machine-readable JSON without changing its exit semantics:

```bash
python3 book-components/scripts/lint_manuscript.py \
  --json-output tmp/manuscript-lint.json
```

Configuration lives in `book-components/scripts/manuscript-lint-config.json`. Legitimate exceptions
must be narrow and carry a written reason; for example:

```json
{
  "allowlist": [
    {
      "rule": "duplicate-figure-reference",
      "path": "sections/05-production/26-*.md",
      "value": "FIG-CH01-01",
      "reason": "Chapter 26 intentionally cross-references the opening model."
    }
  ]
}
```

Allowlist entries may constrain `rule`, globbed `path`, exact `line`, exact `value`,
or `message_contains`. The linter rejects entries without a non-empty `reason`.
Do not allowlist an unresolved drafting or evidence problem merely to get a green run.

Run the focused standard-library test suite with:

```bash
python3 -m unittest discover -s book-components/scripts/tests -p 'test_*.py' -v
```
