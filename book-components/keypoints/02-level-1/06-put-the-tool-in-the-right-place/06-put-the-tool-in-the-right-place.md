---
chapter: 6
title: Put the Tool in the Right Place
plan_title: Tools, Frontend Tools, and Tool Calls
part: Level 1
target_words: 2400
target_pages: 10
status: ready-to-draft
---

# Chapter 6 — Put the Tool in the Right Place

## Hook

Contrast two “add transaction” tools with the same schema: one mutates local client state; the other derives identity server-side, validates the ledger, writes idempotently, and returns an audit receipt.

## Reader outcome

Place a capability in the frontend, backend, external worker, renderer, or human boundary based on context, credentials, duration, impact, and recoverability.

## Core claims

- `useFrontendTool`, `useRenderTool`, and `useHumanInTheLoop` solve different jobs.
- Schemas validate shape; they do not authorize identity, tenant, resource, or business invariants.
- Read and write capabilities should be separated and phase-allowlisted.
- Retries require idempotency at the side-effect boundary, not merely in the agent loop.

## Code, figure, and table inventory

- **Code:** one finance read tool; one new server-authorized transaction tool; one named backend renderer (`L1-03`, `L1-04`, `L1-06`).
- **Decision tree:** client context → secret → duration → side effect → human review.
- **Table:** frontend/backend/external/human tool tradeoffs.
- **Knobs:** impact, reversibility, approval, timeout, retry, idempotency, data class.

## Canonical evidence

- Level 1 packet sections 7–9, tool-placement table, security statement, and snippets L1-03–L1-07.
- Finance `reads.tsx`, `transactions.tsx`, `accounts.tsx`, `budgets.tsx` at the pinned SHA.

## Exercise

Classify five capabilities from an existing app. Move one secret-bearing or privileged client action behind a server tool and add unauthorized, cross-tenant, invalid-domain, and duplicate-request tests.

## Failure and security section

Cover client secrets, confused deputy, schema-only security, unsafe retries, tool-result injection, and a wildcard renderer exposing sensitive arguments.

## Production checklist

- [ ] Placement decision documented.
- [ ] Trusted principal derived server-side.
- [ ] Domain and tenant checks enforced.
- [ ] Writes idempotent and auditable.
- [ ] Timeouts/retries match side-effect safety.
- [ ] Renderers redact sensitive fields.

## Quotable line target

> A tool's schema tells you what an argument looks like; its boundary tells you whether the action is allowed.

## Bridge

Once execution is in the right place, Chapter 7 makes its semantic result visible and interactive.

## Budget

2,400 prose words; 10 pages; code/table heavy.
