# Diagram system

These SVGs are original editorial diagrams for *The Builder's Guide to Agentic Applications 2026*. They are not runtime evidence and do not reproduce any third-party product interface or logo.

## Visual rules

- Canvas: `1600 × 900`, landscape, designed to remain readable at a 5.5-inch book text width.
- Primary face: `Plus Jakarta Sans` with system sans-serif fallbacks.
- Technical labels: `Spline Sans Mono` with system monospace fallbacks.
- Verified CopilotKit palette references: lilac `#BEC2FF`, mint `#85ECCE`, pale lavender `#EDEDF5`, near-black `#010507`, secondary text `#57575B`, and border `#DBDBE5`.
- Dark navy `#11143D` is an **implementation default** selected to align with the supplied cover; it is not asserted as a verified CopilotKit token.
- Gradients remain atmospheric or structural. They are never the only carrier of meaning.
- Every SVG includes a `<title>`, `<desc>`, visible labels, and a non-color cue for state or category.
- No third-party marks are embedded. Product and protocol names appear only as editorial text where needed.

## Source, ownership, and export

Use [`source/`](source/) as the maintenance entrypoint. It records which SVGs are generated, which are hand-authored, how to regenerate them, and the print-scale QA required after every diagram fix.

- For a generated SVG, the owning `.mjs` generator is the source of record. Never patch only the generated SVG.
- For a hand-authored SVG, the SVG itself is the source of record.
- Keep reader-facing assets in this directory so manuscript links remain stable.

Regenerate and validate every code-owned diagram with:

```bash
node book-components/images/diagrams/source/build-all.mjs
```

Export a review PNG at 2× with either command:

```bash
rsvg-convert -w 3200 -h 1800 input.svg -o output.png
```

```bash
magick -background none -density 192 input.svg output.png
```

Before publication, verify the SVG parser, export, grayscale legibility, minimum type size, and PDF embedding. Render the exact PDF page at 180 DPI and inspect chips, card edges, connector gutters, arrowheads, and labels. Do not rasterize the source in place.

## Provenance

All diagrams in this directory have status `original diagram`. Their claims derive from the book's master outline and evidence packets, but the compositions and artwork are original to this manuscript.
