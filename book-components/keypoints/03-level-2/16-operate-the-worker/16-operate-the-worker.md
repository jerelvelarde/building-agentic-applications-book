---
chapter: 16
title: Operate the Worker
plan_title: Operating Machine Agents
part: Level 2
target_words: 2000
target_pages: 10
status: ready-to-draft
---

# Chapter 16 — Operate the Worker

## Hook

The browser disconnects mid-run, the worker finishes a write, the queue retries, and a second worker starts from stale state. Operations determines whether this is one task or three incidents.

## Reader outcome

Operate machine agents as durable workers with queues, leases, isolated workspaces, budgets, verification, audit, recovery, and incident response.

## Core claims

- Persist a run independently from a browser or terminal session.
- Queue, lease, heartbeat, and make side effects idempotent.
- Distinguish discard, restore, revert, and compensate.
- Cancellation has multiple granularities; process termination does not undo completed effects.
- Logs need enough decision evidence for recovery without becoming a secret warehouse.
- Roll out authority from synthetic/read-only to narrowly approved writes.

## Code, figure, and table inventory

- **Schema:** durable `MachineRun` with requester, workspace revision/worktree, status, policy, isolation, budgets, checkpoints, artifacts.
- **Table:** recovery taxonomy and cancellation semantics.
- **Dashboard:** verified outcomes, denials, approvals, retries, cost, egress, rollback, stale environments.
- **Runbook:** suspicious behavior containment and rebuild.

## Canonical evidence

- Level 2 packet Chapter 16, acceptance tests, and claim map.
- First-party worktree/checkpoint sources cited there.

## Exercise

Run a game day: cancel mid-tool, restart gateway while waiting for approval, retry after external success, revoke credential lease, fail verification, discard worktree, and restore/revert a separate committed change.

## Failure and security section

Cover duplicate writes, stale workers, silent sandbox unavailability, leaked logs, orphaned worktrees/checkpoints, failed compensation, and trying to “clean” a potentially compromised persistent host.

## Production checklist

- [ ] Durable run state and worker lease.
- [ ] Idempotency/external operation IDs.
- [ ] Verified outcome metrics.
- [ ] Cancellation acknowledgements truthful.
- [ ] Retention/cleanup automated.
- [ ] Kill/revoke/contain/rebuild runbook tested.
- [ ] Clean-machine acceptance suite passes.

## Quotable line target

> Autonomy becomes operable when every run can be located, bounded, verified, stopped, and recovered without relying on the model's memory of what happened.

## Bridge

Level 2 usually has one operator and one environment. Part IV adds multiple requesters, shared identity, durable social context, and organizational accountability.

## Budget

2,000 prose words; 10 pages; operations artifact heavy.
