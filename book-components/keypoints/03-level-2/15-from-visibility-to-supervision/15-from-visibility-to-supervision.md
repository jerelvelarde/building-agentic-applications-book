---
chapter: 15
title: From Visibility to Supervision
plan_title: Supervising Hermes with CopilotKit
part: Level 2
target_words: 2700
target_pages: 12
status: implementation-gated
---

# Chapter 15 — From Visibility to Supervision

## Hook

Open with the compelling demo: Hermes edits the application while CopilotKit renders the tool call and diff. Then annotate the gaps—YOLO default, working-directory convention, external adapter, unauthenticated routes, best-effort Undo.

## Reader outcome

Connect an application control plane to a machine harness and climb from observable activity to authenticated, scoped, approved, isolated, recoverable execution.

## Core claims

- The pinned repositories prove the UI/AG-UI seam, not a complete production machine run.
- A renderer makes work legible; a trusted policy/execution broker authorizes and confines it.
- The hardened ladder is visibility → authentication → scope → approval → isolation → recovery → verification.
- Do not rebuild every machine capability as a browser tool; supervise the harness through typed events and server policy.

## Code, figure, and table inventory

- **Code:** pinned route/provider/launcher/DiffCard; annotated unsafe baseline.
- **Target code:** server tool broker resolving identity/workspace, canonicalizing intent, leasing credentials, enforcing policy, invoking isolated worker.
- **Sequence:** UI → authenticated gateway → policy/approval → worker → verifier.
- **Screenshots:** plan, real tool call, content-addressed diff, approval, policy denial, checks, recovery; all runtime-gated.

## Canonical evidence

- Level 2 packet Chapter 15 and exact pinned links.
- Hermes entry in `reference-projects/README.md` and `materials/evidence-packets/level-2-machines.md`.
- Level 2 capture notes: shell HTTP verification is not adapter/model/tool verification.

## Exercise

Reproduce the baseline only after pinning the external Hermes runtime. Disable permissive execution, authenticate the gateway, bind a workspace, deny one path/network action, approve one exact edit, run tests, and discard/restore the candidate.

## Failure and security section

Show external adapter absence, YOLO mode, symlink escape risk, client-selected root, secret inheritance, fake readiness, concurrent-edit Undo failure, and UI cancellation without worker acknowledgement.

## Production checklist

- [ ] External runtime/adapter pinned and licensed.
- [ ] No permissive published profile.
- [ ] Authenticated service and user identity.
- [ ] Enforced workspace/tool/network scope.
- [ ] Approval bound to canonical intent.
- [ ] Isolated worker and credential lease.
- [ ] Real verifier and recovery evidence.

## Quotable line target

> A panel that shows a command after it ran is observability; supervision begins when the system can decide whether it may run at all.

## Bridge

A single hardened run is not an operating model. Chapter 16 handles queues, failures, budgets, cleanup, and incidents.

## Budget

2,700 prose words; 12 pages; highest runtime evidence requirement in Level 2.
