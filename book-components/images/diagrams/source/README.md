# Diagram source workspace

This directory is the durable maintenance entrypoint for the book's editorial diagrams. Reader-facing SVGs stay one directory above so existing manuscript paths do not change.

## Source ownership

`registry.json` maps generated SVGs to their canonical generator. Any SVG not listed as generated is hand-authored and is edited in place.

Rules:

1. Fix generated diagrams in the owning generator, then regenerate. Never patch only the generated SVG.
2. Fix hand-authored diagrams in the SVG itself.
3. Preserve the `1600 × 900` viewBox, `<title>`, `<desc>`, and font fallbacks.
4. Keep arrows and relationship labels in dedicated gutters. Connector endpoints must stop at a card edge or explicit port, never inside body copy.
5. Size chips from the rendered label, not a guessed fixed width.
6. Treat the PDF page as the final layout. An SVG that looks fine at full size may fail at a 5.5-inch print width.

## Build and validate

From the book root:

```bash
node book-components/images/diagrams/source/build-all.mjs
```

The command runs both deterministic generators and then validates the complete SVG inventory. To validate without regenerating:

```bash
node book-components/images/diagrams/source/validate.mjs
```

After any fix:

1. Rebuild `book/agentic-applications-2026-first-draft.pdf`.
2. Render the exact affected PDF page at 180 DPI.
3. Inspect text bounds, chips, cards, connector gutters, arrowheads, labels, captions, and surrounding prose.
4. Run the whole-book PDF validator only after the current batch of visual fixes is complete.

## Recurrent failure classes

- fixed-width chip clips a spaced monospace label;
- card heading or body line exceeds its card;
- arrow or label shares a baseline with body copy;
- several arrows converge into one unreadable knot;
- active timeline span is calculated beyond its enclosing lane;
- staggered rows overlap because the vertical step is smaller than row height;
- full-size SVG is readable but the embedded print-scale figure is not.

When one instance is fixed, inspect sibling diagrams produced by the same helper or generator.
