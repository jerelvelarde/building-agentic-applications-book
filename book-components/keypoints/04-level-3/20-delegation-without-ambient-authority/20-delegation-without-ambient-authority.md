---
chapter: 20
title: Delegation Without Ambient Authority
plan_title: Delegation, Memory, and Human Governance
part: Level 3
target_words: 2500
target_pages: 11
status: review-draft
---

# Chapter 20 — Delegation Without Ambient Authority

## Hook

A Slack agent delegates “investigate the bug” by forwarding the thread and its broad service credentials to a machine worker. The worker receives social context, secrets, and more authority than the task requires.

## Reader outcome

Design bounded Level 3-to-Level 2 delegation, institutional-memory promotion, and a cross-system audit trail.

## Core claims

- A delegated task should transfer a typed, expiring capability and acceptance criteria—not an unconstrained transcript or ambient credentials.
- Preserve requester/agent identity, tenant/channel scope, repository revision, paths, commands, network, secrets, budgets, approval classes, and revocation handle.
- Returned machine evidence must include files, commands, tests, diffs/hashes, external calls, exceptions, environment, and provenance.
- Transcripts are not institutional memory; durable knowledge requires source, scope, sensitivity, review, effective dates, correction, expiry, and deletion.
- Audit events live outside ordinary conversational state.

## Code, figure, and table inventory

- **Schema:** signed delegation envelope and returned evidence bundle.
- **Schema:** candidate memory → reviewed institutional record.
- **Schema:** unified audit event linking platform event, org run, machine run, proposal, trace, commit/result.
- **Sequence:** channel request → policy/approval → short-lived grant → sandbox worker → artifacts → separate merge/publish approval.

## Canonical evidence

- Level 3 packet memory taxonomy, audit model, delegation envelope/flow, prohibited shortcuts.
- Level 2 packet action intent, worker isolation, verification, and recovery.

## Exercise

Delegate read-only repository analysis to a sandboxed worker. Deny writes/network, return exact evidence, review one candidate memory with provenance, and prove revocation prevents a late tool call.

## Failure and security section

Cover credential forwarding, policy loss during handoff, repository injection overriding task policy, unproven “done,” transcript poisoning, cross-channel memory leakage, and deletion that misses derived copies.

## Production checklist

- [ ] Signed typed envelope with expiry/nonce/revocation.
- [ ] Short-lived scoped credentials only.
- [ ] Worker boundary and allowed effects enforced.
- [ ] Evidence bundle content-addressed.
- [ ] Memory promotion reviewed and reversible.
- [ ] Cross-system audit correlation complete.

## Quotable line target

> A safe handoff transfers a bounded capability and a chain of accountability, not the authority of the room it came from.

## Bridge

With the control requirements visible, Chapter 21 compares which responsibilities a direct, open-source, or managed product may own.

## Budget

2,300 prose words; 10 pages; schemas and delegation figure heavy.
