# Book components

This folder contains the durable source system used to write, illustrate, build, and improve the book. It is intentionally behind the reader-facing `book/`, `builder-guide/`, and `companion/` entry points.

| Path | Source of truth for |
| --- | --- |
| [`sections/`](sections/) | Canonical manuscript, ordered by part and chapter |
| [`keypoints/`](keypoints/) | Master outline and chapter contracts |
| [`images/`](images/) | Publication figures, repository captures, and editable diagram source |
| [`materials/`](materials/) | Source registry, excerpt provenance, and evidence packets |
| [`authoring/`](authoring/) | Reader persona, style, terminology, page allocation, screenshot, and evidence rules |
| [`scripts/`](scripts/) | Manuscript linting, PDF build, rendering, and validation |
| [`TRACKING.md`](TRACKING.md) | Compact live tracker for the next improvements |

## Build the First Draft

The build uses the bundled document runtime available in Codex:

```bash
RUNTIME="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies"
"$RUNTIME/python/bin/python3" book-components/scripts/build_review_pdf.py \
  --first-draft \
  --output book/agentic-applications-2026-first-draft.pdf
```

Validate the manuscript and diagrams:

```bash
python3 book-components/scripts/lint_manuscript.py
python3 -m unittest discover -s book-components/scripts/tests -p 'test_*.py' -v
node book-components/images/diagrams/source/validate.mjs
```

Render and validate the PDF:

```bash
RUNTIME="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies"
"$RUNTIME/python/bin/python3" book-components/scripts/render_review_pdf.py \
  --pdf book/agentic-applications-2026-first-draft.pdf \
  --output book-components/tmp/first-draft-rendered \
  --pages all \
  --clean
"$RUNTIME/python/bin/python3" book-components/scripts/validate_final_pdf.py
```

Generated page renders, contact sheets, and working prompts live under ignored paths. Only the PDF, build manifest, and compact validation report are published under `book/`.
