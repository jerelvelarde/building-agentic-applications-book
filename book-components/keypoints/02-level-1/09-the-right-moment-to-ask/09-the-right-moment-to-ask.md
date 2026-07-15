---
chapter: 9
title: The Right Moment to Ask
plan_title: Human Control on Web and Mobile
part: Level 1
target_words: 2400
target_pages: 11
status: ready-to-draft
---

# Chapter 9 — The Right Moment to Ask

## Hook

Show two approval cards: “Allow” and a transaction proposal with account, amount, source, impact, exact edit, expiry, reviewer identity, and approve/edit/reject. Only one supports judgment.

## Reader outcome

Place meaningful human intervention at the correct enforcement boundary and implement immediate and durable pause/resume patterns.

## Core claims

- Human-in-the-loop is an execution pattern, not a modal style.
- `useHumanInTheLoop` blocks a client tool; LangGraph `interrupt` can durably suspend runtime execution when checkpointed.
- Approval must bind an eligible principal to an exact proposal/version and expire when the proposal changes.
- Resume can restart a node; pre-interrupt side effects must be idempotent or moved after the decision.
- Stop, cancel, rollback, and compensation need separate UI language.

## Code, figure, and table inventory

- **Code:** finance immediate approval (`L1-09`); durable interrupt and idempotent server write (`L1-10`).
- **Sequence:** client HITL vs runtime interrupt.
- **Table:** pause enforcement, durability, use case, failure.
- **Screenshots:** pending, edited, approved receipt, rejected, disconnected/rejoined mobile.

## Canonical evidence

- Level 1 packet sections 12–14 and approval hierarchy.
- Finance transaction/budget/account HITL sources.
- Contradictory CopilotKit/LangGraph interrupt support remains runtime-gated.

## Exercise

Implement approve/edit/reject for a synthetic transaction. Disconnect before deciding, resume the same thread, and prove exactly one authorized write with an immutable receipt.

## Failure and security section

Test stale approval, wrong reviewer, double click/replay, expired decision, authorization change, resume replay, and stop-after-write confusion.

## Production checklist

- [ ] Decision boundary server-enforced where consequential.
- [ ] Exact proposal hash/version and expiry bound.
- [ ] Approver authenticated and eligible.
- [ ] Reauthorization before execution.
- [ ] Idempotent write and receipt.
- [ ] Disconnect/resume and rejection tested.

## Quotable line target

> The goal is not to put a human everywhere; it is to put the right human at the last responsible moment before consequence.

## Bridge

Control works in the happy path. Chapter 10 makes the whole Level 1 system deployable and operable.

## Budget

2,400 prose words; 11 pages; approval UI and sequence heavy.
