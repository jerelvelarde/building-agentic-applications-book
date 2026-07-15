---
chapter: 22
title: Operate the Organizational Actor
plan_title: Operating Organizational Agents
part: Level 3
target_words: 2500
target_pages: 11
status: review-draft
---

# Chapter 22 — Operate the Organizational Actor

## Hook

The agent is technically live, but no one owns policy changes, a revoked connector leaves schedules running, duplicate events create two writes, and deleting a user leaves derived memory behind.

## Reader outcome

Roll out and operate an organizational agent with staged authority, SLOs, spend controls, incident response, retention, revocation, and decommissioning.

## Core claims

- Expand authority gradually: synthetic → private read-only → narrow tools → drafts → reversible writes → high-impact writes → machine delegation → curated memory → ambient/scheduled work.
- Track safety and product outcomes together; completion rate alone can reward excessive authority.
- High-risk dependencies must define fail-open/fail-closed behavior.
- Kill switches and disable controls need tenant, workspace, channel, tool, credential, schedule, and worker granularity.
- Decommissioning includes platform install, OAuth/Entra, service identities, webhooks, queues, memory, traces, backups, schedules, and delegated artifacts.

## Code, figure, and table inventory

- **Table:** staged rollout and exit evidence.
- **Dashboard:** acknowledgement, retries, policy decisions, approvals, idempotency conflicts, cost, memory, isolation, containment.
- **Runbooks:** duplicate event, revoked credential, poisoned memory, partial startup, failed tool, offboarding.
- **Deliverable:** Level 3 readiness scorecard/game-day script.

## Canonical evidence

- Level 3 packet rollout, SLO/metrics, operational controls, failure modes, and drafting checklist.

## Exercise

Run four game-day scenarios before writes: duplicate platform delivery, wrong approver, credential revocation, process restart before approval. Add one memory-poisoning/deletion scenario before enabling institutional memory.

## Failure and security section

Cover partial adapter startup shown as healthy, store failure continuing on high-risk paths, stale actions after restart, tool partial success, agent credential compromise, memory poisoning, and offboarding gaps.

## Production checklist

- [ ] Stage exit criteria evidence-based.
- [ ] Global and scoped kill/revoke controls.
- [ ] On-call and incident owners named.
- [ ] Idempotent replay/dead-letter procedure.
- [ ] Retention/export/delete/legal-hold mapped.
- [ ] Decommission game day completed.

## Quotable line target

> An organizational agent is not fully deployed until the organization knows how to constrain it, observe it, revoke it, and erase what should not outlive it.

## Bridge

Part V unifies all three levels around evaluation, security, reliability, cost, and the smallest sufficient authority.

## Budget

1,900 prose words; 9 pages; rollout and operations artifact heavy.
