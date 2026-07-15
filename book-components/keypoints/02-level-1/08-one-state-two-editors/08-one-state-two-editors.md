---
chapter: 8
title: One State, Two Editors
plan_title: Shared State, Persistence, and the LangGraph Extension
part: Level 1
target_words: 2500
target_pages: 11
status: ready-to-draft
---

# Chapter 8 — One State, Two Editors

## Hook

The user changes a transaction category while the agent applies an older full-state snapshot. The UI looks synchronized, but the user's correction disappears.

## Reader outcome

Design typed state ownership, conflict handling, durable thread persistence, and recovery without conflating UI state, task state, memory, or traces.

## Core claims

- Shared state is a contract with ownership and versions, not a chat transcript.
- Store semantic data, not rendered prose.
- Agent-owned, UI-owned, jointly edited, backend-owned, and derived fields need different update rules.
- LangGraph checkpoints provide thread-scoped recovery when configured; stores provide cross-thread memory. Neither reverses external effects.
- The audited examples do not prove durable LangGraph behavior; this chapter's durability is a tested companion extension.

## Code, figure, and table inventory

- **Code:** typed ledger state; reducer/versioned patch; stale-revision rejection; checkpointer/thread config (`L1-08`).
- **Figure:** state ownership and conflict/rebase sequence.
- **Table:** view/task/thread/user/institutional/trace state.
- **Screenshot:** conflict surfaced, refresh/rejoin, historical tool card.

## Canonical evidence

- Level 1 packet sections 10–12 and snippets L1-08/L1-10.
- AG-UI state snapshots/deltas and LangGraph persistence sources cited there.
- `authoring/terminology.md` state and memory definitions.

## Exercise

Assign owner, update rule, revision strategy, and persistence target to each ledger field. Create one concurrent edit test and prove the newer user edit is preserved or explicitly rebased.

## Failure and security section

Cover stale snapshots, cross-user thread IDs, schema-version mismatch, sensitive server data projected to clients, poisoned memory, and traces used as a database.

## Production checklist

- [ ] Field ownership and reducers documented.
- [ ] Stable authenticated thread IDs.
- [ ] Stale updates rejected/rebased.
- [ ] Checkpointer encrypted, retained, migrated, and tested.
- [ ] Memory provenance/TTL/correction defined.
- [ ] External side effects have independent receipts/idempotency.

## Quotable line target

> Shared state is not one object that everyone may overwrite; it is a negotiated contract between actors with different authority.

## Bridge

Durable state lets a run pause safely. Chapter 9 decides where and how a human should intervene.

## Budget

2,500 prose words; 11 pages; one conflict and one resume proof.
