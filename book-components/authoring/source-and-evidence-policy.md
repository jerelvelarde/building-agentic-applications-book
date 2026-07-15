---
title: Source and Evidence Policy
status: active-drafting
updated: 2026-07-14
---

# Source and evidence policy

The book may draft actively while some implementations remain unresolved, but it must never blur what is known, observed, inferred, or proposed.

## Evidence labels

| Code | Label | Meaning | Reader-facing treatment |
|---|---|---|---|
| **D** | Documented | Current primary documentation states the behavior. | Cite the official page and access date; pin a version where API details matter. |
| **S** | Source-present | Implementation is visible at an immutable repository commit. | Link the exact file/commit; do not claim it ran. |
| **R** | Runtime-verified | The exact scenario ran in a recorded environment with commands, output, and capture metadata. | May be presented as demonstrated behavior. |
| **EA** | Early access | Officially beta, preview, waitlisted, internal, or otherwise availability-limited. | Name the exact status and date. |
| **E** | Editorial synthesis | The book's definition, model, or recommendation derived from evidence. | Own it as the book's framework; do not attribute it to the industry. |
| **A** | Aspirational | Target architecture, hardening step, or companion capability not present at the source pin. | Label as target, exercise, or proposed implementation. |

Multiple labels may apply. `S/EA` means source exists but availability is limited. `D/E` means documentation supports a book-specific synthesis.

## Source hierarchy

Prefer, in order:

1. Standards, specifications, and official protocol documentation.
2. Immutable source files and tagged releases in official repositories.
3. Official product documentation and release notes.
4. Primary research papers or authoritative security guidance.
5. Maintainer statements with stable links.
6. Runtime evidence produced by the book's pinned companion environment.

Use secondary analysis only for context or discovery. Do not base API, availability, security, or product-capability claims on marketing summaries, search snippets, or unsourced social posts.

## Claim record

Every central or time-sensitive claim needs:

```yaml
claim_id: L3-IDENTITY-01
claim: Identity resolution is not authorization.
status: E/S
sources:
  - <immutable source or primary documentation>
accessed: 2026-07-14
chapter: 19
publication_refresh: required | not-required
notes: <scope, contradiction, or limitation>
```

Evidence packets may hold this metadata. Reader-facing prose should receive ordinary citations and concise qualifications, not unexplained internal labels.

## Repository evidence rules

- Pin a full commit SHA or release tag.
- Link the exact file and relevant symbol where practical.
- Record license and attribution requirements before excerpting.
- Treat comments, committed screenshots, and tests as source artifacts, not proof that the current environment works.
- Preserve repository gaps. Never describe a proposed LangGraph, sandbox, approval, or governance layer as if it exists upstream.
- When a private or user-owned repository has no license, obtain explicit publication permission before printing code.

For author-owned repositories commissioned as canonical examples for this book, the source registry may carry a dated author-permission record in place of a public license. The record must name the owner, repositories, allowed code and screenshot use, attribution, date, and any privacy limits. Permission does not promote source-present evidence to runtime-verified evidence.

## Runtime verification rules

A claim reaches **R** only when the run record includes:

- repository and immutable revision;
- exact dependency lock or resolved versions;
- OS/runtime/device or channel environment;
- setup and execution commands;
- synthetic fixture or safe test data;
- expected and observed result;
- test/log/trace path;
- capture time;
- known failures or exclusions;
- redaction review.

A health endpoint or rendered shell verifies only that layer. It does not promote an unavailable adapter, model call, simulator flow, or external side effect to runtime-verified.

## Contradictions and drift

When docs and source disagree:

1. Record both with dates and versions.
2. Select the exact release used by the companion.
3. Run the disputed behavior.
4. Teach the tested release and add a version note.
5. Never splice APIs from multiple versions into one snippet.

Refresh at publication freeze:

- product availability and supported channels;
- model and package names;
- hook signatures and import paths;
- security guidance and standards revisions;
- managed-versus-self-hosted responsibilities;
- pricing, quotas, regions, and retention claims if included;
- Claude Tag, OpenTag, OpenClaw, Hermes, and CopilotKit Intelligence comparisons.

## Evidence gates by artifact

| Artifact | Minimum evidence |
|---|---|
| Conceptual diagram | E with supporting D/S sources where factual |
| API snippet | S plus compile/test before final review |
| “Working” code claim | R |
| Product comparison row | D or S with date; R for hands-on observations |
| Screenshot labeled as proof | R |
| Security guarantee | Enforced implementation plus adversarial test; do not infer from UI |
| Production-ready claim | All relevant chapter gates, not a single successful run |

## Active drafting rule

Drafting is **ACTIVE**. Unresolved code, availability, or screenshot facts do not pause conceptual prose. They do constrain wording:

- write verified concepts now;
- place unresolved facts in the chapter keypoints/evidence queue;
- use explicit target-architecture labels for hardening work;
- do not fabricate a result to make the prose feel complete;
- replace every research flag before publication lock or list it transparently in the review handoff.
